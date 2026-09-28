import argparse
import torch
from pathlib import Path
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / 'data' / 'source' / 'en.txt'
OUTPUT_DIR = BASE_DIR / 'data' / 'madlad400'

LANG_CODES = {
    'de': '<2de>', 'fr': '<2fr>', 'zh': '<2zh>', 'es': '<2es>',
    'ja': '<2ja>', 'hi': '<2hi>', 'ar': '<2ar>', 'bn': '<2bn>',
    'mr': '<2mr>', 'pa': '<2pa>', 'ta': '<2ta>', 'te': '<2te>',
}
ALL_LANGS = list(LANG_CODES.keys())

MODELS = {
    '3B': 'google/madlad400-3b-mt',
    '7B': 'google/madlad400-7b-mt',
    '10B': 'google/madlad400-10b-mt'
}

def translate_madlad(model, tokenizer, texts, target_lang_tag, device, batch_size=16):
    translations = []
    for i in tqdm(range(0, len(texts), batch_size), desc=f'MADLAD en->{target_lang_tag}'):
        batch = texts[i:i + batch_size]
        tagged_batch = [f"{target_lang_tag} {text}" for text in batch]
        
        inputs = tokenizer(tagged_batch, return_tensors="pt", padding=True, truncation=True,
                          max_length=512).to(device)

        with torch.no_grad():
            # Enforce greedy decoding to match NLLB-200 / IndicTrans2 methodology
            generated = model.generate(
                **inputs, 
                max_new_tokens=256,
                num_beams=1,
                do_sample=False
            )

        decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
        translations.extend(decoded)
        
        # Free memory aggressively after each batch
        del inputs, generated
        torch.cuda.empty_cache()

    return translations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='all')
    parser.add_argument('--model', default='3B', choices=['3B', '7B', '10B'])
    parser.add_argument('--batch-size', type=int, default=16)
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")

    model_name = MODELS[args.model]
    print(f"Loading model: {model_name} in float16...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # LOAD IN FP16 TO PREVENT OOM
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, 
        torch_dtype=torch.float16
    ).to(device)
    model.eval()
    print("Model loaded.")

    with open(SOURCE_FILE, 'r', encoding='utf-8') as sf:
        sources = [line.strip() for line in sf.readlines()]
    print(f"Loaded {len(sources)} source strings")

    langs = ALL_LANGS if args.lang == 'all' else [args.lang]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        madlad_tag = LANG_CODES[lang]
        print(f"\nTranslating en -> {lang} ({madlad_tag})...")
        translations = translate_madlad(model, tokenizer, sources, madlad_tag, device, args.batch_size)

        output_file = OUTPUT_DIR / f'{lang}.txt'
        with open(output_file, 'w', encoding='utf-8') as of:
            for t in translations:
                of.write(t.replace('\n', ' ').strip() + '\n')
        print(f"  Saved: {output_file} ({len(translations)} lines)")

if __name__ == '__main__':
    main()
