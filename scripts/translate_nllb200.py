"""
Translate source strings using NLLB-200 (Meta, open-source).

Runs locally on GPU/CPU. No API key needed.

Usage:
    python scripts/translate_nllb200.py --lang de
    python scripts/translate_nllb200.py --lang all
    python scripts/translate_nllb200.py --lang all --model 3.3B  # Larger model

Requires: pip install transformers torch sentencepiece
"""

import argparse
import torch
from pathlib import Path
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / 'data' / 'source' / 'en.txt'
OUTPUT_DIR = BASE_DIR / 'data' / 'nllb200'

# NLLB-200 language codes (FLORES-200 format)
LANG_CODES = {
    'de': 'deu_Latn', 'fr': 'fra_Latn', 'zh': 'zho_Hans', 'es': 'spa_Latn',
    'ja': 'jpn_Jpan', 'hi': 'hin_Deva', 'ar': 'arb_Arab', 'bn': 'ben_Beng',
    'mr': 'mar_Deva', 'pa': 'pan_Guru', 'ta': 'tam_Taml', 'te': 'tel_Telu',
}
ALL_LANGS = list(LANG_CODES.keys())
SOURCE_LANG = 'eng_Latn'

MODELS = {
    '600M': 'facebook/nllb-200-distilled-600M',
    '1.3B': 'facebook/nllb-200-distilled-1.3B',
    '3.3B': 'facebook/nllb-200-3.3B',
}

BATCH_SIZE = 32


def translate_nllb(model, tokenizer, texts, target_lang_code, device, batch_size=32):
    """Translate texts using NLLB-200."""
    tokenizer.src_lang = SOURCE_LANG
    translations = []

    for i in tqdm(range(0, len(texts), batch_size), desc=f'NLLB en->{target_lang_code}'):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True,
                          max_length=512).to(device)

        target_lang_id = tokenizer.convert_tokens_to_ids(target_lang_code)

        with torch.no_grad():
            generated = model.generate(
                **inputs,
                forced_bos_token_id=target_lang_id,
                max_new_tokens=256,
            )

        decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
        translations.extend(decoded)

    return translations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='all')
    parser.add_argument('--model', default='1.3B', choices=['600M', '1.3B', '3.3B'])
    parser.add_argument('--batch-size', type=int, default=32)
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")

    model_name = MODELS[args.model]
    print(f"Loading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    model.eval()
    print("Model loaded.")

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        sources = [line.strip() for line in f.readlines()]
    print(f"Loaded {len(sources)} source strings")

    langs = ALL_LANGS if args.lang == 'all' else [args.lang]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        nllb_code = LANG_CODES[lang]
        print(f"\nTranslating en -> {lang} ({nllb_code})...")
        translations = translate_nllb(model, tokenizer, sources, nllb_code, device, args.batch_size)

        output_file = OUTPUT_DIR / f'{lang}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for t in translations:
                f.write(t.replace('\n', ' ').strip() + '\n')
        print(f"  Saved: {output_file} ({len(translations)} lines)")


if __name__ == '__main__':
    main()
