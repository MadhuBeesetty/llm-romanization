#!/usr/bin/env python3
"""
romanize_gemini.py — Romanize the first N (Query, Response) rows from
data/oasst2_processed.csv into Hindi, Telugu and Kannada via the Gemini API.
Saves intermediate progress incrementally and supports resuming/rerunning.

Setup: pip install google-genai python-dotenv ; set GEMINI_API_KEY in .env
Run:   python romanize_gemini.py [--rows 10] [--languages hindi telugu kannada]
"""

import argparse
import csv
import json
import os
import random
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(HERE, "data", "oasst2_processed.csv")
OUTPUT_DIR = os.path.join(HERE, "output", "gemini")

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# --- RETRY CONFIGURATION FOR 503 ERRORS ---
MAX_RETRIES = 3   
BASE_DELAY = 1       
MAX_DELAY = 5       

LANGUAGES = {
    "hindi":   {"name": "Hindi",
                "example": 'e.g. "Namaste, aap kaise hain? Main theek hoon."'},
    "telugu":  {"name": "Telugu",
                "example": 'e.g. "Namaskaram, meeru ela unnaru? Nenu bagunnaanu."'},
    "kannada": {"name": "Kannada",
                "example": 'e.g. "Namaskara, neevu hegiddira? Naanu chennagiddini."'},
}

CSV_FIELDS = ["message_id", "language", "query_en", "response_en",
              "romanized_query", "romanized_response", "output_tokens"]


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

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.0,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=512
                ),
                max_output_tokens=3000,
            )
            
            completion = client.models.generate_content(
                model=MODEL,
                contents=user_prompt,
                config=config
            )
            
            response_text = completion.text.strip()
            print(response_text)
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
                
            data = json.loads(response_text)
            
            out_tokens = 0
            if completion.usage_metadata:
                out_tokens = completion.usage_metadata.candidates_token_count
            
            return {
                "romanized_query": data.get("romanized_query", "").strip(),
                "romanized_response": data.get("romanized_response", "").strip(),
                "output_tokens": out_tokens,
            }
        except Exception as err:
            if attempt == MAX_RETRIES:
                raise
            
            calculated_delay = min(MAX_DELAY, BASE_DELAY * (2 ** (attempt - 1)))
            sleep_time = random.uniform(1, calculated_delay)
            
            print(f"      attempt {attempt} failed ({err}); retrying in {sleep_time:.2f} seconds...",
                  file=sys.stderr)
            time.sleep(sleep_time)
            
    raise RuntimeError(f"romanize_pair exhausted all retries for {lang_key}")


def read_rows(path, n):
    if not os.path.exists(path):
        sys.exit(f"Input CSV not found: {path}")
    with open(path, newline="", encoding="utf-8") as f:
        return [row for i, row in enumerate(csv.DictReader(f)) if i < n]


def get_existing_message_ids(out_path):
    """Reads the existing output file to find IDs that are already completed."""
    if not os.path.exists(out_path):
        return set()
    try:
        with open(out_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return {row["message_id"] for row in reader if row.get("message_id")}
    except Exception:
        # If the file is corrupted or empty, treat it as empty
        return set()


def append_row_to_output(out_path, result):
    """Appends a single processed row safely to the CSV file."""
    file_exists = os.path.exists(out_path) and os.path.getsize(out_path) > 0
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not file_exists:
            w.writeheader()
        w.writerow(result)


def main():
    p = argparse.ArgumentParser(description="Romanize CSV prompts/responses using Gemini.")
    p.add_argument("--rows", type=int, default=5)
    p.add_argument("--languages", nargs="+", default=list(LANGUAGES.keys()),
                   choices=list(LANGUAGES.keys()))
    args = p.parse_args()

    if not os.getenv("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set. Add it to .env.")

    client = genai.Client()
    rows = read_rows(INPUT_CSV, args.rows)
    
    print(f"Model: {MODEL}")
    print(f"Loaded {len(rows)} target rows from {INPUT_CSV}\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_output_tokens = 0

    for lang_key in args.languages:
        lang_name = LANGUAGES[lang_key]["name"]
        print(f"=== {lang_name} ===")
        
        out_path = os.path.join(OUTPUT_DIR, f"gemini_romanized_{lang_key}.csv")
        
        # Fetch already processed IDs for this specific language file
        existing_ids = get_existing_message_ids(out_path)
        if existing_ids:
            print(f"  Found {len(existing_ids)} rows already processed in {out_path}. They will be skipped.")

        for idx, row in enumerate(rows, start=1):
            msg_id = row.get("message_id", "")
            
            # Skip if this row was already successfully saved in a previous execution
            if msg_id in existing_ids:
                continue
                
            q = row.get("Query", "") or ""
            r = row.get("Response", "") or ""
            print(f"  [{idx}/{len(rows)}] {msg_id[:8]}...")
            
            try:
                # Attempt to process the pair with exponential backoff inside
                pair = romanize_pair(client, lang_key, q, r)
                total_output_tokens += pair.get("output_tokens", 0)
                
                result = {
                    "message_id": msg_id,
                    "language": lang_name,
                    "query_en": q,
                    "response_en": r,
                    **pair,
                }
                
                # Save immediately to prevent loss if subsequent rows fail or script is stopped
                append_row_to_output(out_path, result)
                
            except Exception as err:
                # Skip if all retry attempts fail entirely (e.g., long-lasting 503 error)
                print(f"  [ERROR] Row {msg_id[:8]} failed completely after all retries: {err}. Skipping row...", 
                      file=sys.stderr)
                continue

            # --- ADD THIS LINE TO RESPECT THE 5 RPM LIMIT ---
            # Wait 12.5 seconds between requests (60 seconds / 5 requests = 12s + buffer)
            print("  [Throttling] Waiting 1 seconds to respect rate limits...")
            time.sleep(1)
                
        print(f"  -> Intermediate progress saved to {out_path}\n")
        
    print(f"Total output tokens generated this session: {total_output_tokens}")
    print("Done.")


if __name__ == "__main__":
    main()