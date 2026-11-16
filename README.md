[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23019912.svg)](https://doi.org/10.5281/zenodo.23019912)

# Benchmarking Neural Machine Translation for Cloud-Native Software Localization Pipelines

A multi-metric evaluation of commercial and open-source Neural Machine Translation (NMT) systems across high-resource and low-resource languages on authentic software UI strings from the OPUS KDE4 corpus.

## Paper

**Title:** Benchmarking Neural Machine Translation for Cloud-Native Software Localization Pipelines: A Multi-Metric Evaluation Across High-Resource and Low-Resource Languages  
**Authors:** Neeraj Kumar Sharma, Subhrakanta Panda, Lalita Bhanu Murthy Neti  
**Affiliation:** BITS Pilani, Hyderabad Campus, Hyderabad, 500078, India  
**Target Journal:** Journal of Cloud Computing (Springer Nature)

## Overview

This study benchmarks four alternative NMT systems (one commercial: Microsoft Translator; three open-source: NLLB-200, MADLAD-400, and IndicTrans2) against Google Translate as the industry-standard baseline across 12 language pairs (5 high-resource + 7 low-resource) on 10,228 authentic software UI strings, using 8 evaluation metrics including CometKiwi reference-free quality estimation.

### Evaluated NMT Systems

| System | Type | Role | Coverage |
| --- | --- | --- | --- |
| Google Translate | Commercial | **Baseline** | All 12 language pairs |
| Microsoft Translator | Commercial | Evaluated | All 12 language pairs |
| NLLB-200 (`facebook/nllb-200-distilled-600M`) | Open-source | Evaluated | All 12 language pairs |
| MADLAD-400 (`google/madlad400-3b-mt`) | Open-source | Evaluated | All 12 language pairs |
| IndicTrans2 (`ai4bharat/indictrans2-en-indic-1B`) | Open-source | Evaluated | 6 Indic language pairs |

### Target Languages (12)

- **High-resource (5):** German (`de`), French (`fr`), Chinese (`zh`), Spanish (`es`), Japanese (`ja`)
- **Low-resource (7):** Hindi (`hi`), Arabic (`ar`), Bengali (`bn`), Marathi (`mr`), Punjabi (`pa`), Tamil (`ta`), Telugu (`te`)

### Evaluation Metrics (8)

| Metric | Category | Reference |
| --- | --- | --- |
| BLEU | Reference-based (lexical) | Papineni et al. (2002) |
| METEOR | Reference-based (lexical) | Banerjee & Lavie (2005) |
| chrF++ | Reference-based (lexical) | Popovic (2015) |
| ROUGE-L | Reference-based (lexical) | Lin (2004) |
| TER | Reference-based (lexical) | Snover et al. (2006) |
| COMET | Reference-based (neural) | Rei et al. (2020) |
| BERTScore | Reference-based (neural) | Zhang et al. (2020) |
| CometKiwi | **Reference-free (neural QE)** | Rei et al. (2022) |

## Repository Structure

```text
cloud-native-nmt-benchmark/
├── README.md                          # Repository overview and setup guide
├── REPRODUCIBILITY.md                 # End-to-end reproduction instructions
├── RUN_ENVIRONMENT.md                 # Hardware and software run specifications
├── LICENSE                            # MIT License (code and scripts)
├── DATA_LICENSE.md                    # Data provenance and licensing terms
├── CITATION.cff                       # Citation metadata
├── CHECKSUMS.txt                      # SHA-256 checksums for all 55 corpus files
├── CHECKSUMS_SHA256.txt               # SHA-256 checksum manifest
├── CHECKSUMS_MD5.txt                  # MD5 checksum manifest
├── requirements.txt                   # General Python dependencies
├── requirements-lock.txt              # Pinned environment for NLLB-200
├── requirements-madlad400.txt         # Pinned environment for MADLAD-400
├── requirements-indictrans2.txt       # Pinned environment for IndicTrans2
├── requirements-metrics.txt           # Pinned environment for metric evaluation
├── data/
│   ├── README.md                      # Corpus alignment and formatting details
│   ├── source/en.txt                  # 10,228 English KDE4 UI source strings
│   ├── baseline_google_translate/     # Google Translate baseline outputs (12 langs)
│   ├── microsoft_translator/          # Microsoft Translator outputs (12 langs)
│   ├── nllb200/                       # NLLB-200 outputs (12 langs)
│   ├── madlad400/                     # MADLAD-400 outputs (12 langs)
│   └── indictrans2/                   # IndicTrans2 outputs (6 Indic langs)
├── metrics/
│   ├── results/                       # Reference-based metric scores and pivot tables
│   └── cometkiwi/                     # CometKiwi reference-free QE scores
├── findings/
│   └── bleu_comet_disagreements/      # 719 verified lexical-neural disagreement cases
├── figures/                           # Generated publication figures
├── scripts/                           # Translation, evaluation, and analysis scripts
├── nmt_benchmarking_pipeline.ipynb    # Interactive execution notebook
├── main.tex                           # LaTeX manuscript source
└── main.pdf                           # Compiled manuscript PDF
```

## Dataset

- **Source:** OPUS KDE4 parallel corpus (v.2) — https://opus.nlpl.eu/datasets/KDE4
- **Corpus citation:** Tiedemann, J. (2012). Parallel Data, Tools and Interfaces in OPUS. *Proceedings of LREC 2012*.
- **Size:** 10,228 English software UI strings (`data/source/en.txt`)
- **Baseline:** Google Translate outputs generated on 3 September 2026 via `GOOGLETRANSLATE()` in Google Sheets

## Setup & Reproduction

```bash
# Clone the repository
git clone https://github.com/Research-SoftwareLocalization/cloud-native-nmt-benchmark.git
cd cloud-native-nmt-benchmark

# Verify corpus and translation output checksums
sha256sum -c CHECKSUMS.txt
md5sum -c CHECKSUMS_MD5.txt

# Run open-source translations (in their respective pinned environments)
pip install -r requirements-lock.txt && python scripts/run_all_nllb200.py
pip install -r requirements-indictrans2.txt && python scripts/run_all_indictrans2.py
pip install -r requirements-madlad400.txt && python scripts/run_all_madlad400.py

# Compute reference-based and reference-free metrics
pip install -r requirements-metrics.txt
python scripts/compute_metrics.py
python scripts/compute_cometkiwi.py
python scripts/analysis.py
```

## API Keys

Commercial NMT reproduction requires an Azure AI Translator API key:

```bash
export AZURE_TRANSLATOR_KEY="your-key"
python scripts/run_all_microsoft.py
```

NLLB-200, IndicTrans2, and MADLAD-400 run locally with deterministic greedy decoding and do not require commercial API keys.

## License

Code and scripts in this repository are licensed under the [MIT License](LICENSE). See [DATA_LICENSE.md](DATA_LICENSE.md) for source corpus and model output licensing terms.

## Citation

If you use this dataset or code, please cite:

```bibtex
@article{sharma2026benchmarking,
  title={Benchmarking Neural Machine Translation for Cloud-Native Software Localization Pipelines: A Multi-Metric Evaluation Across High-Resource and Low-Resource Languages},
  author={Sharma, Neeraj Kumar and Panda, Subhrakanta and Neti, Lalita Bhanu Murthy},
  journal={Journal of Cloud Computing},
  year={2026},
  publisher={Springer Nature},
  doi={10.5281/zenodo.23019912}
}
```
