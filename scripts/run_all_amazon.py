"""
Parallel driver for Amazon Translate across all 12 target languages.

Runs scripts/translate_amazon.py for multiple languages CONCURRENTLY (one
subprocess per language, capped by --workers). Each language writes its own
output file sequentially via the worker, so 1:1 line alignment within a file
is preserved exactly; concurrency is only across languages, never within a
file. Resumable: languages already at 10,228 lines are skipped.

Amazon Translate is a commercial system; its output is a frozen record of the
translations produced on the recorded run date (see RUN_ENVIRONMENT.md).

Speedup note:
    Amazon Translate has no batch text endpoint, so throughput is bounded by
    the account request-rate (TPS) limit, shared across all concurrent calls.
    Running languages in parallel raises aggregate throughput up to that cap.
    If you see heavy ThrottlingException retries, lower --workers.

Requires AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).

Usage:
    python scripts/run_all_amazon.py                 # default 6 workers
    python scripts/run_all_amazon.py --workers 8
"""
import os, sys, argparse, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

LANGS = ["hi", "ar", "bn", "de", "es", "fr", "ja", "mr", "pa", "ta", "te", "zh"]
OUT = "data/amazon_translate"
EXPECTED_LINES = 10228
SCRIPT = os.path.join("scripts", "translate_amazon.py")
os.makedirs(OUT, exist_ok=True)


def line_count(p):
    return sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0


def run_lang(lang):
    """Translate one language in its own subprocess. Returns (lang, status)."""
    out_file = f"{OUT}/{lang}.txt"
    if line_count(out_file) == EXPECTED_LINES:
        return (lang, "skip")
    proc = subprocess.run(
        [sys.executable, SCRIPT, "--lang", lang],
        capture_output=True, text=True,
    )
    n = line_count(out_file)
    if proc.returncode != 0 or n != EXPECTED_LINES:
        return (lang, f"FAIL (rc={proc.returncode}, lines={n})")
    return (lang, "done")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6,
                    help="number of languages to translate concurrently")
    args = ap.parse_args()

    todo = [l for l in LANGS if line_count(f"{OUT}/{l}.txt") != EXPECTED_LINES]
    skipped = [l for l in LANGS if l not in todo]
    for l in skipped:
        print(f"[skip] {l}: already complete")
    if not todo:
        print("All languages already complete.")
        return

    print(f"Translating {len(todo)} languages with {args.workers} concurrent workers: {todo}")
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(run_lang, l): l for l in todo}
        for fut in as_completed(futures):
            lang, status = fut.result()
            print(f"[{status}] {lang}")
            if status.startswith("FAIL"):
                failures.append((lang, status))

    if failures:
        print("\nFAILED languages (re-run to resume):")
        for lang, status in failures:
            print(f"  {lang}: {status}")
        sys.exit(1)
    print("\nAll requested languages complete.")


if __name__ == "__main__":
    main()
