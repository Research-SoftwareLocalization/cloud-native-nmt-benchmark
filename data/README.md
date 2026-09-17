# Data Directory

## Expected File Format

Each system directory should contain one `.txt` file per language, with one translated string per line (aligned with the source file).

### Source strings
```
data/source/en.txt          # 10,228 lines, one English source string per line
```

### Translations (one file per language)
```
data/baseline_google_translate/de.txt
data/baseline_google_translate/fr.txt
data/baseline_google_translate/zh.txt
data/baseline_google_translate/es.txt
data/baseline_google_translate/ja.txt
data/baseline_google_translate/hi.txt
data/baseline_google_translate/ar.txt
data/baseline_google_translate/bn.txt
data/baseline_google_translate/mr.txt
data/baseline_google_translate/pa.txt
data/baseline_google_translate/ta.txt
data/baseline_google_translate/te.txt
```

Same structure for: `microsoft_translator/`, `nllb200/`, `madlad400/`

For `indictrans2/` (Indic languages only):
```
data/indictrans2/hi.txt
data/indictrans2/bn.txt
data/indictrans2/mr.txt
data/indictrans2/pa.txt
data/indictrans2/ta.txt
data/indictrans2/te.txt
```

### Important
- All files must have the **same number of lines** (10,228)
- Lines are aligned: line N in any translation file corresponds to line N in `source/en.txt`
- UTF-8 encoding
- No headers; just one string per line
