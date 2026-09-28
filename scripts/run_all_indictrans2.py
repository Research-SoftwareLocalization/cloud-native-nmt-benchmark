"""
Driver for IndicTrans2 translation across the 6 supported Indic languages.

Runs scripts/translate_indictrans2.py once per language and verifies each
output has 10,228 lines. Resumable: re-running skips languages already
complete (10,228 lines).

IndicTrans2 supports only Indic languages; the non-Indic pairs
(de, es, fr, ja, zh, ar) are handled by other systems.

Run environment: Google Colab, NVIDIA T4 GPU (see RUN_ENVIRONMENT.md).
Model: ai4bharat/indictrans2-en-indic-1B. Greedy decoding (num_beams=1).
Requires: pip install IndicTransToolkit  (in addition to transformers/torch).
"""
import os, subprocess

LANGS = ["hi", "bn", "mr", "pa", "ta", "te"]
OUT = "data/indictrans2"
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
        ["python", "scripts/translate_indictrans2.py", "--lang", lang, "--batch-size", "32"]
    ).returncode
    if rc != 0 or line_count(out_file) != EXPECTED_LINES:
        print(f"[fail] {lang} incomplete ({line_count(out_file)} lines). Stopping.")
        break
    print(f"[done] {lang} translated")
