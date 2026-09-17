"""
Driver for MADLAD-400 translation across all 12 target languages.

Runs scripts/translate_madlad400.py once per language and verifies each output
has 10,228 lines. Resumable: re-running skips languages already complete.

Run environment: Lightning AI Studio, NVIDIA GPU (see RUN_ENVIRONMENT.md).
Model: google/madlad400-3b-mt.
"""
import os, subprocess

LANGS = ["hi","ar","bn","de","es","fr","ja","mr","pa","ta","te","zh"]
OUT = "data/madlad400"
os.makedirs(OUT, exist_ok=True)

def line_count(p):
    return sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0

for lang in LANGS:
    out_file = f"{OUT}/{lang}.txt"
    if line_count(out_file) == 10228:
        print(f"[skip] {lang}: already complete")
        continue
    
    print(f"[run] translating {lang} ...")
    rc = subprocess.run(
        ["python", "scripts/translate_madlad400.py", "--lang", lang, "--model", "3B", "--batch-size", "32"]
    ).returncode
    
    if rc != 0 or line_count(out_file) != 10228:
        print(f"[fail] {lang} incomplete ({line_count(out_file)} lines). Stopping.")
        break
    
    print(f"[done] {lang} translated")
