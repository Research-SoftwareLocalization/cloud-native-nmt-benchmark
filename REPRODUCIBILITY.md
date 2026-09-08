# Reproducibility

This repository contains the source strings, translation outputs, scripts, and environment specification needed to reproduce the results in the paper.

## Pipeline overview

1. Source strings: `data/source/en.txt` (10,228 software UI strings)
2. Google Translate baseline: `data/baseline_google_translate/{lang}.txt`
3. NLLB-200 outputs: `data/nllb200/{lang}.txt`
4. IndicTrans2 outputs: `data/indictrans2/{lang}.txt` (6 Indic languages)
5. Microsoft Translator outputs: `data/microsoft_translator/{lang}.txt`
6. Amazon Translate outputs: `data/amazon_translate/{lang}.txt`
7. Metrics: computed by `scripts/compute_metrics.py`

## Target languages (12)

hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh

## Systems

| System | Type | Model / Method | Run date | Reproducible? |
| --- | --- | --- | --- | --- |
| Google Translate (baseline) | Commercial | GOOGLETRANSLATE(), Google Sheets | 3 Sep 2026 | No (server-side model changes) |
| NLLB-200 | Open | facebook/nllb-200-distilled-600M (transformers 5.16.1) | 5 Sep 2026 | Yes (deterministic, greedy) |
| IndicTrans2 | Open | ai4bharat/indictrans2-en-indic-1B (transformers 4.46.1, gated) | 5 Sep 2026 | Yes (deterministic, greedy) |
| Amazon Translate | Commercial | Amazon Translate API (boto3), us-east-1 | 7 Sep 2026 | No (server-side model changes) |
| Microsoft Translator | Commercial | Azure AI Translator API v3.0 | 6 Sep 2026 | No (server-side model changes) |

## Environment

See `RUN_ENVIRONMENT.md` for the full specification. Pinned dependency versions: `requirements-lock.txt` (NLLB-200 environment), `requirements-indictrans2.txt` (IndicTrans2 environment), and `requirements-metrics.txt` (metric computation environment: sacrebleu, nltk, rouge-score, unbabel-comet, bert-score, setuptools<81).

NLLB-200 and IndicTrans2 use DIFFERENT, incompatible transformers versions (5.16.1 vs 4.46.1) and must be run in separate environments/runtimes.

## Reproducing NLLB-200

Install pinned dependencies and run the driver (indented = code):

```
pip install -r requirements-lock.txt
python scripts/run_all_nllb200.py

```

## Reproducing IndicTrans2

IndicTrans2 requires a separate environment and gated-model access:

```
pip install "transformers==4.46.1" IndicTransToolkit sentencepiece
# restart the runtime so the pinned transformers version loads
# request access at https://huggingface.co/ai4bharat/indictrans2-en-indic-1B
# authenticate:  huggingface-cli login   (or huggingface_hub.login)
python scripts/run_all_indictrans2.py

```

Each output file must contain exactly 10,228 lines.

## Reproducing Microsoft Translator

Microsoft Translator is a commercial API; its output is a frozen snapshot, not byte-reproducible. To regenerate (results may differ from the recorded run):

```
pip install requests tqdm
# set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION
python scripts/run_all_microsoft.py

```

On the Free F0 tier expect HTTP 429 rate limiting; the script handles it (Retry-After, 65s fallback wait, 8 retries, 0.5s inter-batch pause).

## Reproducing Amazon Translate

Amazon Translate is a commercial API; its output is a frozen snapshot, not byte-reproducible. To regenerate (results may differ from the recorded run):

```
pip install boto3 tqdm
# set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
python scripts/run_all_amazon.py

```

## Notes on reproducibility

- Open-source models (NLLB-200, IndicTrans2) with greedy decoding are deterministic: identical inputs and pinned versions yield identical outputs.
- IndicTrans2 is a gated Hugging Face repository; reproduction requires requesting access and authenticating with a Hugging Face read token.
- Commercial systems (Google, Amazon, Microsoft) update server-side without notice; their output files in this repository are the frozen record of what those systems produced on the recorded run dates.

