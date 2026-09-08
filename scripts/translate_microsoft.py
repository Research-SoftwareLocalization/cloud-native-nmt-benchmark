"""
Translate source strings using Microsoft Translator API (Azure).

Usage:
    python scripts/translate_microsoft.py --lang de
    python scripts/translate_microsoft.py --lang all

Requires: AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION env vars
    pip install requests

Reproducibility notes:
    Microsoft Translator is a commercial system whose model is updated
    server-side without notice. Outputs are a frozen record of the
    translations produced on the recorded run date (see RUN_ENVIRONMENT.md).

Hardening (parity with the open-source pipelines):
    - Preserves exact line alignment: every source line yields exactly one
      output line, so the output always has the same number of lines as
      the source (10,228). Empty/whitespace-only source lines are passed
      through as empty output lines (never sent to the API).
    - Verifies the output line count matches the source count and raises if
      not, so a truncated/partial run fails loudly instead of silently.
    - Retries each batch a few times on transient API errors before failing.
"""

import argparse
import os
import time
import requests
from pathlib import Path
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / 'data' / 'source' / 'en.txt'
OUTPUT_DIR = BASE_DIR / 'data' / 'microsoft_translator'

ENDPOINT = 'https://api.cognitive.microsofttranslator.com/translate'
API_VERSION = '3.0'

LANG_CODES = {
    'de': 'de', 'fr': 'fr', 'zh': 'zh-Hans', 'es': 'es', 'ja': 'ja',
    'hi': 'hi', 'ar': 'ar', 'bn': 'bn', 'mr': 'mr', 'pa': 'pa',
    'ta': 'ta', 'te': 'te',
}
ALL_LANGS = list(LANG_CODES.keys())

BATCH_SIZE = 50          # Microsoft allows up to 100 texts per request
MAX_RETRIES = 8          # more attempts, since F0 free tier throttles aggressively
RETRY_BACKOFF = 5.0      # base seconds for exponential backoff on transient errors
RATE_LIMIT_WAIT = 65.0   # fallback wait (s) on HTTP 429 when no Retry-After header
INTER_BATCH_SLEEP = 0.5  # small pause between batches to stay under the F0 rate cap


def translate_nonempty_batch(batch, target_lang, api_key, region):
    """Translate a batch of NON-EMPTY texts, with retries. Returns list of same length."""
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
    }
    params = {'api-version': API_VERSION, 'from': 'en', 'to': LANG_CODES[target_lang]}
    body = [{'Text': t} for t in batch]

    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(ENDPOINT, params=params, headers=headers, json=body, timeout=60)
            # Handle rate limiting (429) explicitly: honor Retry-After, wait long, retry.
            if resp.status_code == 429:
                retry_after = resp.headers.get('Retry-After')
                wait = float(retry_after) if retry_after else RATE_LIMIT_WAIT
                if attempt < MAX_RETRIES:
                    print(f"    [429] rate limited; waiting {wait:.0f}s before retry {attempt+1}/{MAX_RETRIES}")
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"Rate limited (429) after {MAX_RETRIES} attempts")
            resp.raise_for_status()
            results = resp.json()
            out = [r['translations'][0]['text'] for r in results]
            if len(out) != len(batch):
                raise ValueError(f"API returned {len(out)} items for a batch of {len(batch)}")
            return out
        except RuntimeError:
            raise
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)  # exponential-ish backoff
            else:
                raise RuntimeError(f"Batch failed after {MAX_RETRIES} attempts: {e}") from last_err


def translate_all(sources, target_lang, api_key, region):
    """Translate all sources, preserving 1:1 line alignment (empties passed through)."""
    translations = [None] * len(sources)

    # indices of non-empty source lines
    nonempty_idx = [i for i, s in enumerate(sources) if s.strip()]
    # fill empties immediately
    for i, s in enumerate(sources):
        if not s.strip():
            translations[i] = ''

    for b in tqdm(range(0, len(nonempty_idx), BATCH_SIZE), desc=f'en->{target_lang}'):
        idx_batch = nonempty_idx[b:b + BATCH_SIZE]
        text_batch = [sources[i] for i in idx_batch]
        out = translate_nonempty_batch(text_batch, target_lang, api_key, region)
        for i, tr in zip(idx_batch, out):
            translations[i] = tr
        time.sleep(INTER_BATCH_SLEEP)  # pace requests to stay under the F0 rate cap

    # safety: no None left
    if any(t is None for t in translations):
        raise RuntimeError("Internal error: some lines were not translated")
    return translations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='all')
    args = parser.parse_args()

    api_key = os.environ.get('AZURE_TRANSLATOR_KEY')
    region = os.environ.get('AZURE_TRANSLATOR_REGION', 'eastus')
    if not api_key:
        raise ValueError("Set AZURE_TRANSLATOR_KEY environment variable")

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        sources = [line.rstrip('\n') for line in f.readlines()]
    n_src = len(sources)
    print(f"Loaded {n_src} source strings")

    langs = ALL_LANGS if args.lang == 'all' else [args.lang]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        if lang not in LANG_CODES:
            print(f"  Skipping {lang}: not a configured language")
            continue
        print(f"\nTranslating en -> {lang}...")
        translations = translate_all(sources, lang, api_key, region)

        if len(translations) != n_src:
            raise RuntimeError(
                f"Line count mismatch for {lang}: {len(translations)} != {n_src}. Not writing."
            )

        output_file = OUTPUT_DIR / f'{lang}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for t in translations:
                f.write(t.replace('\n', ' ').strip() + '\n')
        print(f"  Saved: {output_file} ({len(translations)} lines)")


if __name__ == '__main__':
    main()
