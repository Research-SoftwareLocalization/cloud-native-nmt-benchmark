# Run Environment

## NLLB-200 Translation Run

- Date of run: 5 September 2026
- Platform: Google Colab
- GPU: Tesla T4
- CUDA version: 12.8
- Python: 3.13.15
- torch: 2.11.0+cu128
- transformers: 5.16.1
- Model: facebook/nllb-200-distilled-600M
- Model revision (HF commit sha, current as of run date): f8d333a098d19b4fd9a8b18f94170487ad3f821d
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
- transformers: 4.46.1 (pinned; see note below)
- huggingface-hub: 0.36.2 (downgraded by the IndicTransToolkit install)
- IndicTransToolkit: installed via pip (provides IndicProcessor)
- Model: ai4bharat/indictrans2-en-indic-1B
- Model revision (HF commit sha, current as of run date): 10e65a9951a1e922cd109a95e8aba9357b62144b
- Batch size: 32
- Decoding: greedy (num_beams=1)
- Max generated tokens: 256
- Tokenizer input truncation: max_length=512
- Preprocessing/postprocessing: IndicTransToolkit IndicProcessor (REQUIRED)
- Target languages (6 Indic): hi, bn, mr, pa, ta, te
- Pinned dependencies: requirements-indictrans2.txt

### IndicTrans2 environment notes

- transformers 5.16.1 (used for NLLB-200) is INCOMPATIBLE with IndicTransToolkit: it fails at import with "cannot import name 'PreTrainedTokenizerBase' from 'transformers.tokenization_utils'". IndicTrans2 must therefore run in a separate environment pinned to transformers==4.46.1, with a runtime restart after install.
- The model is a GATED Hugging Face repository. Reproduction requires requesting access at [https://huggingface.co/ai4bharat/indictrans2-en-indic-1B](https://huggingface.co/ai4bharat/indictrans2-en-indic-1B) and authenticating with a Hugging Face read token.
- The IndicTransToolkit install downgrades huggingface-hub to 0.36.2, producing harmless dependency-conflict warnings from diffusers/gradio (not used here).
- The decode step uses tokenizer.as_target_tokenizer(), which emits a deprecation warning under 4.46.1 (slated for removal in Transformers v5). This is benign and is another reason the 4.x pin is recorded.

## Microsoft Translator Run

- Date of run: 6 September 2026
- Platform: local (Windows laptop); no GPU required (hosted API)
- Service: Microsoft Translator (Azure AI Translator)
- API version: 3.0
- Pricing tier: Free F0
- Batch size: 50 texts per request
- Source strings: 10,228 (data/source/en.txt)
- Target languages (12): hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh
- Client dependencies: requests, tqdm (do not affect output; hosted model)

### Microsoft Translator notes

- Commercial, server-side model: outputs are a frozen record of what the service produced on the run date; results may differ if regenerated later. Not reproducible by pinning a local environment.
- The Free F0 tier aggressively rate-limits (HTTP 429). The script honours the Retry-After header, uses a 65s fallback wait on 429, MAX_RETRIES=8, and a 0.5s inter-batch pause. These affect only pacing, not the translations.

## Amazon Translate Run

- Date of run: 7 September 2026
- Platform: local (Windows laptop); no GPU required (hosted API)
- Service: Amazon Translate (AWS)
- Access: boto3 client, region us-east-1
- Concurrency: language-level parallel driver (run_all_amazon.py); each string translated by a single TranslateText call
- Source strings: 10,228 (data/source/en.txt)
- Target languages (12): hi, ar, bn, de, es, fr, ja, mr, pa, ta, te, zh
- Client dependencies: boto3, tqdm (do not affect output; hosted model)

### Amazon Translate notes

- Commercial, server-side model: outputs are a frozen record of what the service produced on the run date; results may differ if regenerated later. Not reproducible by pinning a local environment.
- The hardened worker raises loudly on persistent API errors (no silent source fallback), handles ThrottlingException with retries, and verifies the output line count before writing.

## Metric Computation Run

- Date of run: 8 September 2026
- Platform: Lightning AI Studio, GPU (NVIDIA)
- Python: 3.12 (Lightning cloudspace environment)
- Pinned dependencies: requirements-metrics.txt
- Key library versions:- sacrebleu 2.6.0 (BLEU, chrF++, TER; with sacrebleu[ja] -> mecab-python3 1.0.12, ipadic 1.0.0 for Japanese BLEU tokenization)
- nltk 3.10.3 (METEOR)
- rouge-score (ROUGE-L)
- unbabel-comet 2.2.7 (COMET and CometKiwi)
- bert-score 0.3.13 (BERTScore)
- torch 2.8.0+cu128, torchmetrics 0.10.3
- setuptools 80.10.2 (pinned <81 so that pkg_resources remains available for the comet/pytorch_lightning/torchmetrics import chain)
- Metrics computed (8): BLEU, METEOR, chrF++, ROUGE-L, TER (lexical); COMET, BERTScore (neural); CometKiwi (reference-free)
- Reference for the 7 reference-based metrics: Google Translate baseline output
- Gated models: Unbabel/wmt22-comet-da and Unbabel/wmt22-cometkiwi-da require Hugging Face access approval and authentication.

### Metric computation notes

- This metrics environment is SEPARATE from the translation environments. It uses torch 2.8.0, whereas the NLLB-200 run used torch 2.11.0 and IndicTrans2 used transformers 4.46.1. Metric library versions do not affect the translation outputs; they only affect metric computation, and are pinned here for reproducibility.
- Lexical metrics are deterministic under the pinned versions. The neural and reference-free metrics (COMET, BERTScore, CometKiwi) are also deterministic given the same model checkpoints and pinned versions.
- Fair-comparison note: IndicTrans2 supports only the six Indic languages (hi, bn, mr, pa, ta, te). It must be compared against other systems only on those six languages; averaging it against systems evaluated on all twelve is not a valid comparison.

## Google Translate Baseline

- Date of run: 3 September 2026
- Method: GOOGLETRANSLATE() function in Google Sheets
- Note: Google updates its NMT models server-side; results may vary if reproduced later.

