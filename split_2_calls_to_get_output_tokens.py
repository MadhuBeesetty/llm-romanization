#!/usr/bin/env python3
"""
split_2_calls_to_get_output_tokens.py — same job as romanize.py, but makes
TWO separate API calls per row (one for the query, one for the response) so
the API's own usage.completion_tokens gives us a true per-field token count.

Writes output/romanized_<lang>_split.csv with extra columns:
    romanized_query_tokens     (billed completion_tokens for the query call)
    romanized_response_tokens  (billed completion_tokens for the response call)

Trade-off vs romanize.py:
    + Real billed token counts per field (no tiktoken approximation).
    - 2x API calls, 2x latency, ~2x prompt-token cost (system prompt sent twice).

Reproducibility behaves the same as romanize.py:
    gpt-4o  -> reproducible (temperature=0 + seed=42)
    gpt-5.x -> NOT reproducible (reasoning models lock temperature, ignore seed)

Setup: pip install openai python-dotenv ; set OPENAI_API_KEY in .env
Run:   python split_2_calls_to_get_output_tokens.py [--rows 10] \\
           [--languages hindi telugu kannada]
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
        f"Translate the given English text to natural conversational {m['name']}, "
        f"then romanize in Latin letters only (a-z). {m['example']}\n\n"
        f"Keep English loanwords speakers actually use (doctor, phone, office, etc.). "
        f"Preserve formatting, line breaks, names, numbers, URLs.\n\n"
        f"Output JSON only:\n"
        f'{{"romanized": "..."}}'
    )


def build_user_prompt(field_label: str, text: str) -> str:
    return (f"Romanize the following English {field_label} as instructed.\n\n"
            + json.dumps({field_label: text}, ensure_ascii=False))


def romanize_one(client, lang_key, field_label, text):
    """One API call -> (romanized_text, completion_tokens, system_fingerprint)."""
    system_prompt = build_system_prompt(lang_key)
    user_prompt = build_user_prompt(field_label, text)
    send_temperature = not IS_REASONING_MODEL
    send_seed = True
    send_reasoning_effort = IS_REASONING_MODEL

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
            romanized = data.get("romanized", "").strip()
            usage = getattr(completion, "usage", None)
            completion_tokens = getattr(usage, "completion_tokens", 0) or 0
            fingerprint = getattr(completion, "system_fingerprint", "") or ""
            return romanized, completion_tokens, fingerprint
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
    raise RuntimeError(f"romanize_one exhausted retries for {lang_key}/{field_label}")


def read_rows(path, n):
    if not os.path.exists(path):
        sys.exit(f"Input CSV not found: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows if n is None else rows[:n]


def write_output(lang_key, results):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"romanized_{lang_key}_split.csv")
    fields = ["message_id", "language", "query_en", "response_en",
              "romanized_query", "romanized_response",
              "romanized_query_tokens", "romanized_response_tokens",
              "system_fingerprint"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    return out_path


def main():
    p = argparse.ArgumentParser(
        description="Romanize CSV prompts/responses with one API call per field.")
    p.add_argument("--rows", type=int, default=None,
                   help="Cap on number of rows to process. Default: all rows.")
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
    print(f"Loaded {len(rows)} rows from {INPUT_CSV}")
    print("Mode: 2 API calls per row (true per-field output tokens)\n")

    grand_q, grand_r = 0, 0

    for lang_key in args.languages:
        lang_name = LANGUAGES[lang_key]["name"]
        print(f"=== {lang_name} ===")
        results = []
        lang_q, lang_r = 0, 0
        for idx, row in enumerate(rows, start=1):
            q = row.get("Query", "") or ""
            r = row.get("Response", "") or ""
            print(f"  [{idx}/{len(rows)}] {row.get('message_id', '')[:8]}...")

            rq_text, rq_tokens, fp1 = romanize_one(client, lang_key, "query", q)
            rr_text, rr_tokens, fp2 = romanize_one(client, lang_key, "response", r)

            lang_q += rq_tokens
            lang_r += rr_tokens
            print(f"      tokens: query={rq_tokens}  response={rr_tokens}")

            results.append({
                "message_id": row.get("message_id", ""),
                "language": lang_name,
                "query_en": q,
                "response_en": r,
                "romanized_query": rq_text,
                "romanized_response": rr_text,
                "romanized_query_tokens": rq_tokens,
                "romanized_response_tokens": rr_tokens,
                "system_fingerprint": fp1 or fp2,
            })
        grand_q += lang_q
        grand_r += lang_r
        print(f"  {lang_name} totals: query={lang_q} response={lang_r} "
              f"(sum={lang_q + lang_r})")
        print(f"  -> {write_output(lang_key, results)}\n")

    print(f"Token usage summary [{MODEL}]")
    print(f"  romanized_query_tokens total:    {grand_q}")
    print(f"  romanized_response_tokens total: {grand_r}")
    print(f"  grand total output tokens:       {grand_q + grand_r}")
    print("Done.")


if __name__ == "__main__":
    main()
