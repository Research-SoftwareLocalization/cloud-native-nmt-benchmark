# Benchmarking NMT for Multilingual Assistive Technology Interfaces

A multi-metric AI-driven evaluation of Neural Machine Translation systems across high-resource and low-resource languages, using the OPUS KDE4 parallel corpus.

## Paper

**Title:** Benchmarking neural machine translation for multilingual assistive technology interfaces: A multi-metric AI-driven evaluation across high-resource and low-resource languages
**Authors:** Neeraj Kumar Sharma, Pranav Dilip Mate, Ayush Kalra, Subhrakanta Panda, Lalita Bhanu Murthy Neti
**Affiliation:** BITS Pilani, Hyderabad Campus, India
**Target Journal:** Journal of Ambient Intelligence and Smart Environments (JAISE), SAGE Publications

## Overview

This study benchmarks 5 NMT systems against Google Translate as the industry-standard baseline across 12 language pairs (5 high-resource + 7 low-resource), using 8 evaluation metrics including CometKiwi reference-free quality estimation.

### Evaluated NMT Systems

| System | Type | Role |
| --- | --- | --- |
| Google Translate | Commercial | **Baseline** |
| Microsoft Translator | Commercial | Evaluated |
| NLLB-200 | Open-source | Evaluated (all 12 pairs) |
| IndicTrans2 | Open-source | Evaluated (6 Indic pairs) |
| MADLAD-400 | Open-source | Evaluated (all 12 pairs) |

### Target Languages

- **High-resource (5):** German (de), French (fr), Chinese (zh), Spanish (es), Japanese (ja)
- **Low-resource (7):** Hindi (hi), Arabic (ar), Bengali (bn), Marathi (mr), Punjabi (pa), Tamil (ta), Telugu (te)

### Evaluation Metrics

| Metric | Type | Reference |
| --- | --- | --- |
| BLEU | Reference-based | Papineni et al. (2002) |
| METEOR | Reference-based | Banerjee & Lavie (2005) |
| chrF++ | Reference-based | Popovic (2015) |
| ROUGE-L | Reference-based | Lin (2004) |
| TER | Reference-based | Snover et al. (2006) |
| COMET | Reference-based | Rei et al. (2020) |
| BERTScore | Reference-based | Zhang et al. (2020) |
| CometKiwi | **Reference-free** | Rei et al. (2022) |

## Repository Structure

```text
nmt-assistive-benchmarking/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CITATION.cff                       # Citation metadata
├── requirements.txt                   # Python dependencies
├── data/
│   ├── source/                        # KDE4 English source strings
│   ├── baseline_google_translate/     # Google Translate outputs (12 languages)
│   ├── microsoft_translator/          # Microsoft Translator outputs
│   ├── nllb200/                       # NLLB-200 outputs
│   ├── indictrans2/                   # IndicTrans2 outputs (6 Indic languages)
│   └── madlad400/                     # MADLAD-400 outputs (12 languages)
├── metrics/
│   ├── results/                       # Computed metric scores
│   └── cometkiwi/                     # Reference-free QE scores
├── scripts/
│   ├── translate_microsoft.py         # Microsoft Translator API script
│   ├── translate_nllb200.py           # NLLB-200 inference script
│   ├── translate_indictrans2.py       # IndicTrans2 inference script
│   ├── translate_madlad400.py         # MADLAD-400 inference script
│   ├── run_all_madlad400.py           # MADLAD-400 runner script
│   ├── compute_metrics.py             # Compute all 7 reference-based metrics
│   ├── compute_cometkiwi.py           # Compute CometKiwi reference-free scores
│   └── analysis.py                    # Statistical analysis & visualization
└── paper/
    └── nmt_paper_jaise.tex            # LaTeX manuscript (SAGE template)
