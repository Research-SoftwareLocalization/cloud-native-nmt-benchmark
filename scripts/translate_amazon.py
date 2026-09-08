"""
Translate source strings using Amazon Translate (AWS).

Usage:
    python scripts/translate_amazon.py --lang de
    python scripts/translate_amazon.py --lang all

Requires: AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) and boto3
    pip install boto3

Reproducibility notes:
    Amazon Translate is a commercial system whose model is updated
    server-side without notice. Outputs are a frozen record of the
    translations produced on the recorded run date (see RUN_ENVIRONMENT.md).

Hardening (parity with translate_microsoft.py):
    - Preserves exact 1:1 line alignment: every source line yields exactly one
      output line. Empty/whitespace-only source lines are passed through as
      empty output lines (never sent to the API).
    - NO silent source fallback: on a persistent API error the script raises
      loudly instead of writing the English source into the output (which
      would invisibly corrupt results).
    - Verifies the output line count equals the source count (10,228) before
      writing; raises on mismatch so a partial run fails loudly.
    - Retries each string on throttling / transient errors with exponential
      backoff, honoring AWS ThrottlingException.
"""

import argparse
import os
import time
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from tqdm import tqdm

BASE_DIR = Path(__file__).parent.parent
SOURCE_FILE = BASE_DIR / 'data' / 'source' / 'en.txt'
OUTPUT_DIR = BASE_DIR / 'data' / 'amazon_translate'

# Amazon Translate language codes
LANG_CODES = {
    'de': 'de', 'fr': 'fr', 'zh': 'zh', 'es': 'es', 'ja': 'ja',
    'hi': 'hi', 'ar': 'ar', 'bn': 'bn', 'mr': 'mr', 'pa': 'pa',
    'ta': 'ta', 'te': 'te',
}
ALL_LANGS = list(LANG_CODES.keys())

MAX_RETRIES = 8
RETRY_BACKOFF = 2.0        # base seconds for exponential backoff
THROTTLE_WAIT = 30.0       # fallback wait (s) on throttling
INTER_CALL_SLEEP = 0.05    # small pause between calls to ease throttling


def translate_one(client, text, target_lang):
    """Translate a single non-empty string, with retries. Raises on persistent failure."""
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = client.translate_text(
                Text=text,
                SourceLanguageCode='en',
                TargetLanguageCode=LANG_CODES[target_lang],
            )
            return resp['TranslatedText']
        except ClientError as e:
            code = e.response.get('Error', {}).get('Code', '')
            last_err = e
            if code in ('ThrottlingException', 'TooManyRequestsException', 'ThrottledException'):
                if attempt < MAX_RETRIES:
                    time.sleep(THROTTLE_WAIT)
                    continue
                raise RuntimeError(f"Throttled after {MAX_RETRIES} attempts") from last_err
            # other transient errors: backoff and retry
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
            else:
                raise RuntimeError(f"Failed after {MAX_RETRIES} attempts: {e}") from last_err
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * attempt)
            else:
                raise RuntimeError(f"Failed after {MAX_RETRIES} attempts: {e}") from last_err


def translate_all(client, sources, target_lang):
    """Translate all sources, preserving 1:1 line alignment (empties passed through)."""
    translations = [None] * len(sources)
    for i, s in enumerate(sources):
        if not s.strip():
            translations[i] = ''

    nonempty_idx = [i for i, s in enumerate(sources) if s.strip()]
    for i in tqdm(nonempty_idx, desc=f'en->{target_lang}'):
        translations[i] = translate_one(client, sources[i], target_lang)
        time.sleep(INTER_CALL_SLEEP)

    if any(t is None for t in translations):
        raise RuntimeError("Internal error: some lines were not translated")
    return translations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', default='all')
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()

    client = boto3.client('translate', region_name=args.region)

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
        translations = translate_all(client, sources, lang)

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
