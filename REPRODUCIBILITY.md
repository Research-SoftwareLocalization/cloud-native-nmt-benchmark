# Reproducibility

This repository contains the source strings, translation outputs, scripts, and environment specification needed to reproduce the results in the paper.

## Pipeline overview

1. Source strings: `data/source/en.txt` (10,228 software UI strings)
2. Google Translate baseline: `data/baseline_google_translate/{lang}.txt`
3. NLLB-200 outputs: `data/nllb200/{lang}.txt`
4. IndicTrans2 outputs: `data/indictrans2/{lang}.txt` (6 Indic languages)
5. MADLAD-400 outputs: `data/madlad400/{lang}.txt`
6. Microsoft Translator outputs: `data/microsoft_translator/{lang}.txt`
7. Metrics: computed by `scripts/compute_metrics.py`

## Target languages (12)

hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh

## Systems

| System | Type | Model / Method | Run date | Reproducible? |
| --- | --- | --- | --- | --- |
| Google Translate (baseline) | Commercial | GOOGLETRANSLATE(), Google Sheets | 3 Sep 2026 | No (server-side model changes) |
| NLLB-200 | Open | facebook/nllb-200-distilled-600M (transformers 5.16.1) | 5 Sep 2026 | Yes (deterministic, greedy) |
| IndicTrans2 | Open | ai4bharat/indictrans2-en-indic-1B (transformers 4.46.1, gated) | 5 Sep 2026 | Yes (deterministic, greedy) |
| MADLAD-400 | Open | google/madlad400-3b-mt (FP16) | 17 Sep 2026 | Yes (deterministic, greedy) |
| Microsoft Translator | Commercial | Azure AI Translator API v3.0 | 6 Sep 2026 | No (server-side model changes) |

## Environment

See `RUN_ENVIRONMENT.md` for the full specification. Pinned dependency versions: `requirements-lock.txt` (NLLB-200 environment), `requirements-indictrans2.txt` (IndicTrans2 environment), `requirements-madlad400.txt` (MADLAD-400 environment), and `requirements-metrics.txt` (metric computation environment: sacrebleu, nltk, rouge-score, unbabel-comet, bert-score, setuptools<81).

NLLB-200, IndicTrans2, and MADLAD-400 use separate environments and should be run under their respective pinned requirements.

## Reproducing NLLB-200

Install pinned dependencies and run the driver:

```bash
pip install -r requirements-lock.txt
python scripts/run_all_nllb200.py
```

## Reproducing IndicTrans2

IndicTrans2 requires a separate environment and gated-model access:

```bash
pip install "transformers==4.46.1" IndicTransToolkit sentencepiece
python scripts/run_all_indictrans2.py
```

Each output file must contain exactly 10,228 lines.

## Reproducing MADLAD-400

Install pinned dependencies and run the driver:

```bash
pip install -r requirements-madlad400.txt
python scripts/run_all_madlad400.py
```

Each output file must contain exactly 10,228 lines.

## Reproducing Microsoft Translator

Microsoft Translator is a commercial API; its output is a frozen snapshot, not byte-reproducible. To regenerate:

```bash
pip install requests tqdm
python scripts/run_all_microsoft.py
```

## Notes on reproducibility

- Open-source models (NLLB-200, IndicTrans2, MADLAD-400) with greedy decoding are deterministic: identical inputs and pinned versions yield identical outputs.
- IndicTrans2 is a gated Hugging Face repository; reproduction requires requesting access and authenticating with a Hugging Face read token.
- Commercial systems (Google, Microsoft) update server-side without notice; their output files in this repository are the frozen record of what those systems produced on the recorded run dates.