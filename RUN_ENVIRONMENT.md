# Run Environment

## MADLAD-400 Translation Run

- Date of run: 17 September 2026
- Platform: Lightning AI Studio
- GPU: NVIDIA T4
- Model: google/madlad400-3b-mt
- Precision: torch.float16 (to prevent CUDA OOM)
- Batch size: 16
- Decoding: greedy (num_beams=1, do_sample=False)
- Tokenizer input truncation: max_length=512
- Max generated tokens: 256
- Source strings: 10,228 (data/source/en.txt)
- Target languages (12): hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh
- Pinned dependencies: requirements-madlad400.txt

## NLLB-200 Translation Run

- Date of run: 5 September 2026
- Platform: Google Colab
- GPU: Tesla T4
- CUDA version: 12.8
- Python: 3.13.15
- torch: 2.11.0+cu128
- transformers: 5.16.1
- Model: facebook/nllb-200-distilled-600M
- Batch size: 32
- Decoding: greedy (num_beams=1, model default)
- Tokenizer input truncation: max_length=512
- Source strings: 10,228 (data/source/en.txt)
- Target languages (12): hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh
- Pinned dependencies: requirements-lock.txt

## IndicTrans2 Translation Run

- Date of run: 5 September 2026
- Platform: Google Colab
- GPU: Tesla T4
- Python: 3.13.15
- transformers: 4.46.1 (pinned)
- huggingface-hub: 0.36.2 (downgraded by the IndicTransToolkit install)
- IndicTransToolkit: installed via pip (provides IndicProcessor)
- Model: ai4bharat/indictrans2-en-indic-1B
- Batch size: 32
- Decoding: greedy (num_beams=1)
- Max generated tokens: 256
- Tokenizer input truncation: max_length=512
- Preprocessing/postprocessing: IndicTransToolkit IndicProcessor (REQUIRED)
- Target languages (6 Indic): hi, bn, mr, pa, ta, te
- Pinned dependencies: requirements-indictrans2.txt

## Microsoft Translator Run

- Date of run: 6 September 2026
- Platform: local (Windows laptop); no GPU required (hosted API)
- Service: Microsoft Translator (Azure AI Translator)
- API version: 3.0
- Pricing tier: Free F0
- Batch size: 50 texts per request
- Source strings: 10,228 (data/source/en.txt)
- Target languages (12): hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh

## Metric Computation Run

- Date of run: 8 September 2026
- Platform: Lightning AI Studio, GPU (NVIDIA)
- Python: 3.12 (Lightning cloudspace environment)
- Pinned dependencies: requirements-metrics.txt
- Key library versions:
  - sacrebleu 2.6.0
  - nltk 3.10.3
  - rouge-score
  - unbabel-comet 2.2.7
  - bert-score 0.3.13
  - torch 2.8.0+cu128, torchmetrics 0.10.3
  - setuptools 80.10.2
- Metrics computed (8): BLEU, METEOR, chrF++, ROUGE-L, TER (lexical); COMET, BERTScore (neural); CometKiwi (reference-free)
- Reference for the 7 reference-based metrics: Google Translate baseline output
- Gated models: Unbabel/wmt22-comet-da and Unbabel/wmt22-cometkiwi-da require Hugging Face access approval and authentication.

## Google Translate Baseline

- Date of run: 3 September 2026
- Method: GOOGLETRANSLATE() function in Google Sheets