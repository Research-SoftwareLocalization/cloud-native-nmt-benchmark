# Benchmarking Neural Machine Translation for Cloud-Native Software Localization Pipelines: A Multi-Metric Evaluation Across High-Resource and Low-Resource Languages

A multi-metric AI-driven evaluation of Neural Machine Translation systems across high-resource and low-resource languages, using the OPUS KDE4 parallel corpus.

## Paper

**Title:** Benchmarking Neural Machine Translation for Cloud-Native Software Localization Pipelines: A Multi-Metric Evaluation Across High-Resource and Low-Resource Languages
**Authors:** Neeraj Kumar Sharma, Subhrakanta Panda, Lalita Bhanu Murthy Neti
**Affiliation:** BITS Pilani, Hyderabad Campus, India
**Target Journal:** Journal of Cloud Computing (Special Issue: Resilience-by-Design for Cloud-Native Systems)

## Overview

This study benchmarks 4 NMT systems against Google Translate as the industry-standard baseline across 12 language pairs (5 high-resource + 7 low-resource), using 8 evaluation metrics including CometKiwi reference-free quality estimation.

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
cloud-native-nmt-benchmark-main/
├── .gitignore
├── CHECKSUMS.txt
├── CITATION.cff
├── DATA_LICENSE.md
├── LICENSE
├── README.md
├── REPRODUCIBILITY.md
├── RUN_ENVIRONMENT.md
├── comet_by_system.png
├── data/
│   ├── README.md
│   ├── baseline_google_translate/
│   │   ├── ar.txt
│   │   ├── bn.txt
│   │   ├── de.txt
│   │   ├── es.txt
│   │   ├── fr.txt
│   │   ├── hi.txt
│   │   ├── ja.txt
│   │   ├── mr.txt
│   │   ├── pa.txt
│   │   ├── ta.txt
│   │   ├── te.txt
│   │   └── zh.txt
│   ├── indictrans2/
│   │   ├── bn.txt
│   │   ├── hi.txt
│   │   ├── mr.txt
│   │   ├── pa.txt
│   │   ├── ta.txt
│   │   └── te.txt
│   ├── madlad400/
│   │   ├── ar.txt
│   │   ├── bn.txt
│   │   ├── de.txt
│   │   ├── es.txt
│   │   ├── fr.txt
│   │   ├── hi.txt
│   │   ├── ja.txt
│   │   ├── mr.txt
│   │   ├── pa.txt
│   │   ├── ta.txt
│   │   ├── te.txt
│   │   └── zh.txt
│   ├── microsoft_translator/
│   │   ├── ar.txt
│   │   ├── bn.txt
│   │   ├── de.txt
│   │   ├── es.txt
│   │   ├── fr.txt
│   │   ├── hi.txt
│   │   ├── ja.txt
│   │   ├── mr.txt
│   │   ├── pa.txt
│   │   ├── ta.txt
│   │   ├── te.txt
│   │   └── zh.txt
│   ├── nllb200/
│   │   ├── ar.txt
│   │   ├── bn.txt
│   │   ├── de.txt
│   │   ├── es.txt
│   │   ├── fr.txt
│   │   ├── hi.txt
│   │   ├── ja.txt
│   │   ├── mr.txt
│   │   ├── pa.txt
│   │   ├── ta.txt
│   │   ├── te.txt
│   │   └── zh.txt
│   └── source/
│       └── en.txt
├── findings/
│   └── bleu_comet_disagreements/
│       ├── evaluate_bleu_comet_disagreements.py
│       └── verified_metric_disagreements.csv
├── main.pdf
├── main.tex
├── metric_correlation.png
├── metrics/
│   ├── cometkiwi/
│   │   ├── cometkiwi_pivot.csv
│   │   └── cometkiwi_scores.csv
│   └── results/
│       ├── metric_scores.csv
│       ├── metric_scores_lexical.csv
│       ├── metric_scores_neural.csv
│       └── pivots/
│           ├── pivot_bertscore.csv
│           ├── pivot_bleu.csv
│           ├── pivot_chrf.csv
│           ├── pivot_comet.csv
│           ├── pivot_meteor.csv
│           ├── pivot_rouge_l.csv
│           └── pivot_ter.csv
├── nmt_benchmarking_pipeline.ipynb
├── requirements-indictrans2.txt
├── requirements-lock.txt
├── requirements-madlad400.txt
├── requirements-metrics.txt
├── requirements.txt
└── scripts/
    ├── analysis.py
    ├── compute_cometkiwi.py
    ├── compute_metrics.py
    ├── make_pivots.py
    ├── merge_metric_results.py
    ├── remove_empty_lines.py
    ├── run_all_indictrans2.py
    ├── run_all_madlad400.py
    ├── run_all_microsoft.py
    ├── run_all_nllb200.py
    ├── translate_indictrans2.py
    ├── translate_madlad400.py
    ├── translate_microsoft.py
    └── translate_nllb200.py
```

## Dataset

- **Source:** OPUS KDE4 parallel corpus (v.2) — https://opus.nlpl.eu/datasets/KDE4
- **Corpus citation:** Tiedemann J. (2012). Parallel data, tools and interfaces in OPUS. LREC 2012.
- **Size:** 10,228 English source strings
- **Baseline:** Google Translate outputs generated on 3 September 2026 using GOOGLETRANSLATE() in Google Sheets

## Setup

```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)[username]/nmt-assistive-benchmarking.git
cd nmt-assistive-benchmarking

# Install dependencies
pip install -r requirements.txt

# Run translations
python scripts/translate_microsoft.py
python scripts/translate_nllb200.py
python scripts/translate_indictrans2.py
python scripts/run_all_madlad400.py

# Compute metrics
python scripts/compute_metrics.py
python scripts/compute_cometkiwi.py

# Run analysis
python scripts/analysis.py
```

## API Keys

Commercial NMT systems require API keys. Set these as environment variables:

```bash
export AZURE_TRANSLATOR_KEY="your-key"     # Microsoft Translator
```

NLLB-200, IndicTrans2, and MADLAD-400 run locally and do not require API keys.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
The OPUS KDE4 corpus is distributed under its original license terms.

## Citation

If you use this work, please cite:

```bibtex
@article{sharma2026benchmarking,
  title={Benchmarking neural machine translation for multilingual assistive technology interfaces: A multi-metric AI-driven evaluation across high-resource and low-resource languages},
  author={Sharma, Neeraj Kumar and Panda, Subhrakanta and Neti, Lalita Bhanu Murthy},
  journal={Journal of Ambient Intelligence and Smart Environments},
  year={2026},
  publisher={SAGE Publications}
}
```
