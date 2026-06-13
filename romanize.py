#!/usr/bin/env python3
"""
romanize.py — Romanize the first N (Query, Response) rows from
data/oasst2_processed.csv into Hindi, Telugu and Kannada via the OpenAI API.
Writes output/romanized_<lang>.csv per language.

Reproducibility:
    OPENAI_MODEL=gpt-4o    -> reproducible (temperature=0 + seed=42 both honored)
    OPENAI_MODEL=gpt-5.5   -> NOT reproducible (temperature locked at 1, seed
                              is ignored by reasoning models). Use only when
                              you want best quality and don't need re-run match.

Setup: pip install openai python-dotenv ; set OPENAI_API_KEY in .env
Run:   python romanize.py [--rows 10] [--languages hindi telugu kannada]
"""

import argparse
import csv
import json
import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(HERE, "data", "oasst2_processed.csv")
OUTPUT_DIR = os.path.join(HERE, "output")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
SEED = int(os.getenv("OPENAI_SEED", "42"))
MAX_RETRIES = 4

# Reasoning models (GPT-5 family, o-series) lock temperature at 1 and ignore
# seed -> no determinism lever. gpt-4o/gpt-4.1 honor both.
IS_REASONING_MODEL = MODEL.lower().startswith(("gpt-5", "o1", "o3", "o4"))

LANGUAGES = {
    "hindi":   {"name": "Hindi",
                "example": 'e.g. "Namaste, aap kaise hain? Main theek hoon."'},
    "telugu":  {"name": "Telugu",
                "example": 'e.g. "Namaskaram, meeru ela unnaru? Nenu bagunnaanu."'},
    "kannada": {"name": "Kannada",
                "example": 'e.g. "Namaskara, neevu hegiddira? Naanu chennagiddini."'},
}


def build_system_prompt(lang_key: str) -> str:
    m = LANGUAGES[lang_key]
    return (
        f"Translate English to natural conversational {m['name']}, then romanize "
        f"in Latin letters only (a-z). {m['example']}\n\n"
        f"Keep English loanwords speakers actually use (doctor, phone, office, etc.). "
        f"Preserve formatting, line breaks, names, numbers, URLs.\n\n"
        f"Input: English `query` and `response`. Output JSON only:\n"
        f'{{"romanized_query": "...", "romanized_response": "..."}}'
    )


def build_user_prompt(query, response):
    return ("Romanize the following English query and response as instructed.\n\n"
            + json.dumps({"query": query, "response": response}, ensure_ascii=False))


def romanize_pair(client, lang_key, query, response):
    system_prompt = build_system_prompt(lang_key)
    user_prompt = build_user_prompt(query, response)
    send_temperature = not IS_REASONING_MODEL
    send_seed = True
    send_reasoning_effort = IS_REASONING_MODEL  # only for gpt-5.x / o-series

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            kwargs = {
                "model": MODEL,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
            if send_temperature:
                kwargs["temperature"] = 0
            if send_seed:
                kwargs["seed"] = SEED
            if send_reasoning_effort:
                kwargs["reasoning_effort"] = "low"
            completion = client.chat.completions.create(**kwargs)
            data = json.loads(completion.choices[0].message.content)
            return {
                "romanized_query": data.get("romanized_query", "").strip(),
                "romanized_response": data.get("romanized_response", "").strip(),
                "system_fingerprint": getattr(completion, "system_fingerprint", "") or "",
            }
        except Exception as err:
            msg = str(err).lower()
            if send_temperature and "temperature" in msg:
                send_temperature = False
                continue
            if send_seed and "seed" in msg:
                send_seed = False
                continue
            if send_reasoning_effort and "reasoning" in msg:
                send_reasoning_effort = False
                continue
            if attempt == MAX_RETRIES:
                raise
            print(f"      attempt {attempt} failed ({err}); retrying...",
                  file=sys.stderr)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"romanize_pair exhausted all retries for {lang_key}")


def read_rows(path, n):
    if not os.path.exists(path):
        sys.exit(f"Input CSV not found: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        return [row for i, row in enumerate(csv.DictReader(f)) if i < n]


def write_output(lang_key, results):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"romanized_{lang_key}.csv")
    fields = ["message_id", "language", "query_en", "response_en",
              "romanized_query", "romanized_response", "system_fingerprint"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    return out_path


def main():
    p = argparse.ArgumentParser(description="Romanize CSV prompts/responses.")
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--languages", nargs="+", default=list(LANGUAGES.keys()),
                   choices=list(LANGUAGES.keys()))
    args = p.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Add it to .env.")

    client = OpenAI()
    rows = read_rows(INPUT_CSV, args.rows)
    repro = "NOT reproducible (reasoning model)" if IS_REASONING_MODEL \
        else "reproducible (temperature=0 + seed)"
    print(f"Model: {MODEL}  [{repro}]")
    print(f"Loaded {len(rows)} rows from {INPUT_CSV}\n")

    for lang_key in args.languages:
        lang_name = LANGUAGES[lang_key]["name"]
        print(f"=== {lang_name} ===")
        results = []
        for idx, row in enumerate(rows, start=1):
            q = row.get("Query", "") or ""
            r = row.get("Response", "") or ""
            print(f"  [{idx}/{len(rows)}] {row.get('message_id', '')[:8]}...")
            pair = romanize_pair(client, lang_key, q, r)
            results.append({
                "message_id": row.get("message_id", ""),
                "language": lang_name,
                "query_en": q,
                "response_en": r,
                **pair,
            })
        print(f"  -> {write_output(lang_key, results)}\n")
    print("Done.")


if __name__ == "__main__":
    main()
