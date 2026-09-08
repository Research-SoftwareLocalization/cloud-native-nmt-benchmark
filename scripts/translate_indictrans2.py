"""
Translate source strings using IndicTrans2 (AI4Bharat, open-source).

Supports 6 Indic languages: hi, bn, mr, pa, ta, te.
Runs locally. No API key needed.

IMPORTANT: IndicTrans2 requires the IndicTransToolkit IndicProcessor for
preprocessing (script normalization + language-tag prefixing) and
postprocessing (script restoration). Passing raw text to the tokenizer,
as a naive NLLB-style script would, produces degraded/incorrect output.

Usage:
    python scripts/translate_indictrans2.py --lang hi
    python scripts/translate_indictrans2.py --lang all

Requires:
    pip install transformers torch sentencepiece
    pip install IndicTransToolkit

Run environment (recorded for reproducibility):
    Model: ai4bharat/indictrans2-en-indic-1B
    Decoding: greedy (num_beams=1), max_new_tokens=256
    Tokenizer input truncation: max_length=512
    Batch size: 32
"""

import argparse
import torch
from pathlib import Path
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit.processor import IndicProcessor

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / 'data' / 'source' / 'en.txt'
OUTPUT_DIR = BASE_DIR / 'data' / 'indictrans2'

# IndicTrans2 target-language codes (Flores-200 style)
LANG_CODES = {
    'hi': 'hin_Deva', 'bn': 'ben_Beng', 'mr': 'mar_Deva',
    'pa': 'pan_Guru', 'ta': 'tam_Taml', 'te': 'tel_Telu',
}
ALL_LANGS = list(LANG_CODES.keys())

MODEL_NAME = 'ai4bharat/indictrans2-en-indic-1B'
SRC_LANG = 'eng_Latn'
BATCH_SIZE = 32


def translate_indictrans2(model, tokenizer, ip, texts, tgt_code, device, batch_size=32):
    """Translate texts en->tgt using IndicTrans2 with proper pre/post-processing."""
    translations = []

    for i in tqdm(range(0, len(texts), batch_size), desc=f'IT2 en->{tgt_code}'):
        batch = texts[i:i + batch_size]

        # 1. Preprocess: normalize + prepend language tags (REQUIRED by IndicTrans2)
        pre = ip.preprocess_batch(batch, src_lang=SRC_LANG, tgt_lang=tgt_code)

        # 2. Tokenize
        inputs = tokenizer(pre, return_tensors="pt", padding=True,
                           truncation=True, max_length=512).to(device)

        # 3. Generate (greedy decoding to match NLLB-200 methodology)
        with torch.no_grad():
            generated = model.generate(
                **inputs,
                num_beams=1,
                num_return_sequences=1,
                max_new_tokens=256,
            )

        # 4. Decode
        with tokenizer.as_target_tokenizer():
            decoded = tokenizer.batch_decode(
                generated, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )

        # 5. Postprocess: restore native script, strip language tags (REQUIRED)
        final = ip.postprocess_batch(decoded, lang=tgt_code)
        translations.extend(final)

    return translations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='all')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE)
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    print(f"Loading IndicTrans2: {MODEL_NAME}...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True).to(device)
    model.eval()
    ip = IndicProcessor(inference=True)
    print("Model + IndicProcessor loaded.")

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        sources = [line.rstrip('\n') for line in f.readlines()]
    print(f"Loaded {len(sources)} source strings")

    langs = ALL_LANGS if args.lang == 'all' else [args.lang]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        if lang not in LANG_CODES:
            print(f"  Skipping {lang}: not an IndicTrans2-supported Indic language")
            continue

        tgt_code = LANG_CODES[lang]
        print(f"\nTranslating en -> {lang} ({tgt_code})...")
        translations = translate_indictrans2(
            model, tokenizer, ip, sources, tgt_code, device, args.batch_size
        )

        output_file = OUTPUT_DIR / f'{lang}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for t in translations:
                f.write(t.replace('\n', ' ').strip() + '\n')
        print(f"  Saved: {output_file} ({len(translations)} lines)")

    print(f"\nIndicTrans2 covers Indic languages only: {ALL_LANGS}")


if __name__ == '__main__':
    main()
