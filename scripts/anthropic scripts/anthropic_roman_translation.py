#!/usr/bin/env python3
"""
anthropic_roman_translation.py — Romanize rows from data/oasst2_processed.csv
into Hindi, Telugu, Kannada, and Tamil via the Anthropic API.

Fixes applied vs. the original version:
1. Default model corrected — "claude-opus-4-8" isn't a real model id.
   Default is now "claude-opus-4-7"; override with ANTHROPIC_MODEL if needed.
   (Verify the exact current id against docs.claude.com before a big run.)
2. Extended-thinking response parsing fixed — previously read content[0]
   directly, which breaks when thinking is enabled (content[0] is a
   ThinkingBlock, not text). Now finds the text block by type.
3. Incremental per-row writes + resume support — previously held all
   results for a language in memory and wrote once at the end, so a
   crash partway through lost everything for that language. Now each
   row is appended to disk immediately, and re-running skips message_ids
   already present in the output file.
4. max_tokens raised from 4000 to 6000 for headroom on long responses.
5. input_tokens now tracked alongside output_tokens, with an estimated
   cost printed at the end (rate configurable via env vars).
"""

import argparse
import csv
import json
import os
import sys
import time
import traceback

from dotenv import load_dotenv
from anthropic import Anthropic

print("Initializing script...", flush=True)

load_dotenv()

CWD_PATH = os.path.join("data", "oasst2_processed.csv")
HERE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "oasst2_processed.csv")

if os.path.exists(CWD_PATH):
    INPUT_CSV = CWD_PATH
elif os.path.exists(HERE_PATH):
    INPUT_CSV = HERE_PATH
else:
    INPUT_CSV = CWD_PATH

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "anthropic")

# FIX 1: was "claude-opus-4-8" (not a real model id). Confirm the current
# id before a full run — this default is just a safe known-good fallback.
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-7")

MAX_RETRIES = 7

# Used only for the end-of-run cost estimate. Override via env vars if rates
# have changed, e.g. ANTHROPIC_PRICE_INPUT=3 ANTHROPIC_PRICE_OUTPUT=15
PRICE_PER_M_INPUT = float(os.getenv("ANTHROPIC_PRICE_INPUT", "5.00"))
PRICE_PER_M_OUTPUT = float(os.getenv("ANTHROPIC_PRICE_OUTPUT", "25.00"))

ENV_THINKING = os.getenv("ANTHROPIC_THINKING", "").lower()
if ENV_THINKING in ("true", "1", "yes"):
    IS_REASONING_MODEL = True
elif ENV_THINKING in ("false", "0", "no"):
    IS_REASONING_MODEL = False
else:
    model_lower = MODEL.lower()
    IS_REASONING_MODEL = any(x in model_lower for x in ("3-7", "3.7"))

LANGUAGES = {
    "hindi":   {"name": "Hindi",   "example": 'e.g. "Namaste, aap kaise hain? Main theek hoon."'},
    "telugu":  {"name": "Telugu",  "example": 'e.g. "Namaskaram, meeru ela unnaru? Nenu bagunnaanu."'},
    "kannada": {"name": "Kannada", "example": 'e.g. "Namaskara, neevu hegiddira? Naanu chennagiddini."'},
    "tamil":   {"name": "Tamil",   "example": 'e.g. "Vanakkam, neenga eppadi irukkinga? Naan nalla irukkan."'},
}


def build_system_prompt(lang_key: str) -> str:
    m = LANGUAGES[lang_key]
    return (
        f"Translate English to natural conversational {m['name']}, then romanize "
        f"in Latin letters only (a-z). {m['example']}\n\n"
        f"Keep English loanwords speakers actually use (doctor, phone, office, etc.). "
        f"Preserve formatting, line breaks, names, numbers, URLs.\n\n"
        f"Input: English `query` and `response`. Output valid raw JSON only. "
        f"Do not include any markdown code blocks, explanations, or introductory text. "
        f"Your entire response must be parseable by json.loads():\n"
        f'{{"romanized_query": "...", "romanized_response": "..."}}'
    )


def build_user_prompt(query, response):
    return (
        "Romanize the following English query and response as instructed.\n\n"
        + json.dumps({"query": query, "response": response}, ensure_ascii=False)
    )


def extract_text(completion):
    """FIX 2: pick the text block by type instead of assuming content[0] is
    text. With extended thinking enabled, content[0] is a ThinkingBlock and
    has no .text attribute — this looks past it for the actual text block."""
    for block in completion.content:
        if getattr(block, "type", None) == "text":
            return block.text
    raise ValueError("No text block found in response content")


def romanize_pair(client, lang_key, query, response):
    system_prompt = build_system_prompt(lang_key)
    user_prompt = build_user_prompt(query, response)

    send_temperature = True
    send_thinking = IS_REASONING_MODEL

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            kwargs = {
                "model": MODEL,
                "max_tokens": 6000,  # FIX 4: more headroom for long responses
                "system": system_prompt,
                "messages": [
                    {"role": "user", "content": user_prompt},
                ],
            }

            if send_thinking:
                kwargs["thinking"] = {"type": "enabled", "budget_tokens": 1024}
                kwargs["temperature"] = 1.0
            elif send_temperature:
                kwargs["temperature"] = 0.0

            completion = client.messages.create(**kwargs)
            raw_text = extract_text(completion).strip()

            if raw_text.startswith("```json"):
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            data = json.loads(raw_text)

            return {
                "romanized_query": data.get("romanized_query", "").strip(),
                "romanized_response": data.get("romanized_response", "").strip(),
                "system_fingerprint": "",
                "input_tokens": getattr(completion.usage, "input_tokens", 0) or 0,   # FIX 5
                "output_tokens": getattr(completion.usage, "output_tokens", 0) or 0,
            }

        except Exception as err:
            msg = str(err).lower()

            if send_thinking and "thinking" in msg:
                print("      [Warning] Thinking mode rejected. Falling back to standard mode.", flush=True)
                send_thinking = False
                continue
            if send_temperature and "temperature" in msg:
                send_temperature = False
                continue

            if attempt == MAX_RETRIES:
                raise

            if "overloaded" in msg or "529" in msg:
                sleep_duration = 5 * attempt
                print(f"      [Overload] Anthropic API congested (529). Waiting {sleep_duration}s before retry...", flush=True)
                time.sleep(sleep_duration)
            else:
                sleep_duration = 2 ** attempt
                print(f"      attempt {attempt} failed ({err}); retrying in {sleep_duration}s...", flush=True)
                time.sleep(sleep_duration)

    raise RuntimeError(f"romanize_pair exhausted all retries for {lang_key}")


def read_rows(path, n):
    print(f"Attempting to open file: {os.path.abspath(path)}", flush=True)
    if not os.path.exists(path):
        print(f"\n[ERROR] Input CSV not found! Looked everywhere, including:\n -> {os.path.abspath(path)}", flush=True)
        sys.exit(1)
    with open(path, newline="", encoding="utf-8") as f:
        return [row for i, row in enumerate(csv.DictReader(f)) if i < n]


OUTPUT_FIELDS = [
    "message_id", "language", "query_en", "response_en",
    "romanized_query", "romanized_response", "system_fingerprint",
    "input_tokens", "output_tokens",
]


def get_output_path(lang_key):
    return os.path.join(OUTPUT_DIR, f"anthropic_romanized_{lang_key}.csv")


def load_done_ids(out_path):
    """FIX 3 (resume support): message_ids already written for this
    language, so re-running the script skips rows that already succeeded
    instead of redoing (and re-billing) them."""
    if not os.path.exists(out_path):
        return set()
    with open(out_path, newline="", encoding="utf-8") as f:
        return {row["message_id"] for row in csv.DictReader(f)}


def append_row(out_path, row, write_header):
    """FIX 3: write each row to disk immediately instead of accumulating
    everything in memory and writing once at the end of the language."""
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        if write_header:
            w.writeheader()
        w.writerow(row)


def main():
    p = argparse.ArgumentParser(description="Romanize CSV prompts/responses via Anthropic.")
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--languages", nargs="+", default=list(LANGUAGES.keys()),
                   choices=list(LANGUAGES.keys()))
    args = p.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n[ERROR] ANTHROPIC_API_KEY is missing from your environment or .env file!", flush=True)
        sys.exit(1)

    print("Initializing Anthropic API Client...", flush=True)
    client = Anthropic()

    rows = read_rows(INPUT_CSV, args.rows)
    repro = "Extended Thinking Mode (temp=1.0)" if IS_REASONING_MODEL else "Deterministic Mode (temp=0.0)"

    print(f"\nModel: {MODEL}  [{repro}]")
    print(f"Loaded {len(rows)} rows successfully.\n", flush=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_input_tokens = 0
    total_output_tokens = 0

    for lang_key in args.languages:
        lang_name = LANGUAGES[lang_key]["name"]
        out_path = get_output_path(lang_key)
        done_ids = load_done_ids(out_path)
        write_header = not os.path.exists(out_path)

        remaining = [r for r in rows if r.get("message_id", "") not in done_ids]
        print(f"=== Starting Language: {lang_name} ===", flush=True)
        print(f"  Total: {len(rows)} | Already done: {len(done_ids)} | Remaining: {len(remaining)}", flush=True)

        for idx, row in enumerate(remaining, start=1):
            q = row.get("Query", "") or ""
            r = row.get("Response", "") or ""
            msg_id = row.get("message_id", "")
            print(f"  [{idx}/{len(remaining)}] Processing message_id: {msg_id[:8]}...", flush=True)

            pair = romanize_pair(client, lang_key, q, r)
            total_input_tokens += pair.get("input_tokens", 0)
            total_output_tokens += pair.get("output_tokens", 0)

            out_row = {
                "message_id": msg_id,
                "language": lang_name,
                "query_en": q,
                "response_en": r,
                **pair,
            }
            append_row(out_path, out_row, write_header)
            write_header = False

        print(f"  -> File: {out_path}\n", flush=True)

    cost = (total_input_tokens / 1_000_000 * PRICE_PER_M_INPUT
            + total_output_tokens / 1_000_000 * PRICE_PER_M_OUTPUT)

    print(f"Total input tokens:  {total_input_tokens}")
    print(f"Total output tokens: {total_output_tokens}")
    print(f"Estimated cost: ${cost:.4f}  (at ${PRICE_PER_M_INPUT}/M in, ${PRICE_PER_M_OUTPUT}/M out — verify current rates)")
    print("Done completely and successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as global_err:
        print("\n!!!!!!!! CRITICAL CRASH OCCURRED !!!!!!!!", flush=True)
        print(f"Error Details: {global_err}", flush=True)
        print("\nFull Stack Traceback Below:", flush=True)
        traceback.print_exc()
        sys.exit(1)
