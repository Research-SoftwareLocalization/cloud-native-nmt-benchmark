"""
Driver for Microsoft Translator across all 12 target languages.

Runs scripts/translate_microsoft.py once per language and verifies each
output has 10,228 lines. Resumable: re-running skips languages already
complete (10,228 lines).

Microsoft Translator is a commercial system; its output is a frozen record
of the translations produced on the recorded run date (see RUN_ENVIRONMENT.md).

Requires env vars: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""
import os, subprocess

LANGS = ["hi", "ar", "bn", "de", "es", "fr", "ja", "mr", "pa", "ta", "te", "zh"]
OUT = "data/microsoft_translator"
EXPECTED_LINES = 10228
os.makedirs(OUT, exist_ok=True)


def line_count(p):
    return sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0


for lang in LANGS:
    out_file = f"{OUT}/{lang}.txt"
    if line_count(out_file) == EXPECTED_LINES:
        print(f"[skip] {lang}: already complete")
        continue
    print(f"[run] translating {lang} ...")
    rc = subprocess.run(
        ["python", "scripts/translate_microsoft.py", "--lang", lang]
    ).returncode
    if rc != 0 or line_count(out_file) != EXPECTED_LINES:
        print(f"[fail] {lang} incomplete ({line_count(out_file)} lines). Stopping.")
        break
    print(f"[done] {lang} translated")
