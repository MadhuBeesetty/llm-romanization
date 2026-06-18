#!/usr/bin/env python3
"""
run_claude_eval.py — Run romanized prompts through Claude and save responses
with output token counts.

Input (default): data/romanized_{hindi,telugu,kannada}_split.csv
    Uses romanized_query as the prompt sent to Claude.
    Also supports data/prompts.csv (columns: prompt_id, language, category, prompt_text).

Output: output/<input_basename>_output.csv  (one file per input)

Setup:
    pip install anthropic python-dotenv
    Set ANTHROPIC_API_KEY in .env

Run:
    python run_claude_eval.py                      # all 3 split CSVs, all rows each
    python run_claude_eval.py --rows 10            # first 10 rows per file (for testing)
    python run_claude_eval.py --input data/romanized_hindi_split.csv  # one file only
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
DEFAULT_INPUTS = [
    os.path.join(DATA_DIR, "romanized_hindi_split.csv"),
    os.path.join(DATA_DIR, "romanized_telugu_split.csv"),
    os.path.join(DATA_DIR, "romanized_kannada_split.csv"),
]
OUTPUT_DIR = os.path.join(HERE, "output")

# Current Claude model — update here if you want to switch
MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")

# System prompt — tells Claude to respond naturally to the user's language
SYSTEM_PROMPT = (
    "You are a helpful assistant. The user may write in romanized Indic script, "
    "code-switched text, or colloquial register. Respond naturally and helpfully "
    "in the language and register the user would find most useful. "
    "Do not add meta-commentary about the language or script."
)

MAX_RETRIES = 4


def run_prompt(client, prompt_text: str) -> dict:
    """Send one prompt to Claude; return response text + token counts."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt_text}],
            )
            return {
                "response_text": message.content[0].text,
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "stop_reason": message.stop_reason,
            }
        except Exception as err:
            if attempt == MAX_RETRIES:
                raise
            wait = 2 ** attempt
            print(f"      attempt {attempt} failed ({err}); retrying in {wait}s...",
                  file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("Exhausted retries")


def normalize_row(row: dict, idx: int) -> dict:
    """Map romanized-split or prompt-collection columns to a common shape."""
    if "romanized_query" in row:
        return {
            "prompt_id": row.get("message_id", f"row_{idx}"),
            "language": row.get("language", ""),
            "category": row.get("category", ""),
            "prompt_text": row.get("romanized_query", ""),
        }
    return {
        "prompt_id": row.get("prompt_id", f"row_{idx}"),
        "language": row.get("language", ""),
        "category": row.get("category", ""),
        "prompt_text": row.get("prompt_text", ""),
    }


def read_rows(path: str, n: int | None) -> list[dict]:
    if not os.path.exists(path):
        sys.exit(f"Input CSV not found: {path}\n"
                 f"Expected romanized-split columns (message_id, language, romanized_query) "
                 f"or prompt-collection columns (prompt_id, language, category, prompt_text)")
    with open(path, newline="", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))
    rows = [normalize_row(row, idx) for idx, row in enumerate(raw_rows, start=1)]
    if n:
        rows = rows[:n]
    return rows


def write_output(results: list[dict], input_path: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Extract the original filename (e.g., "prompts.csv")
    base_name = os.path.basename(input_path)
    # Split name and extension (e.g., "prompts" and ".csv")
    name, ext = os.path.splitext(base_name)

    # Construct the new filename (e.g., "prompts_output.csv")
    out_filename = f"{name}_output{ext}"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    fields = [
        "prompt_id", "language", "category",
        "prompt_text", "response_text",
        "input_tokens", "output_tokens", "stop_reason",
        "model", "timestamp_utc",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    return out_path


def process_input(client, input_path: str, n: int | None) -> str:
    rows = read_rows(input_path, n)
    print(f"Input:  {input_path}  ({len(rows)} rows)")
    print()

    results = []
    total_output_tokens = 0

    for idx, row in enumerate(rows, start=1):
        prompt_id = row["prompt_id"]
        prompt_text = row["prompt_text"]
        language = row["language"]
        category = row["category"]

        label = f"{language} / {category}" if category else language
        print(f"  [{idx:>4}/{len(rows)}]  {prompt_id}  ({label})")

        result = run_prompt(client, prompt_text)
        total_output_tokens += result["output_tokens"]

        results.append({
            "prompt_id": prompt_id,
            "language": language,
            "category": category,
            "prompt_text": prompt_text,
            "response_text": result["response_text"],
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "stop_reason": result["stop_reason"],
            "model": MODEL,
            "timestamp_utc": datetime.utcnow().isoformat(),
        })

        time.sleep(0.5)

    out_path = write_output(results, input_path)

    print()
    print(f"Done: {os.path.basename(input_path)}")
    print(f"Output:              {out_path}")
    print(f"Total output tokens: {total_output_tokens:,}")
    print(f"Avg output tokens:   {total_output_tokens / len(results):.1f}")
    print()
    return out_path


def main():
    p = argparse.ArgumentParser(description="Run prompts through Claude, save responses.")
    p.add_argument("--rows", type=int, default=None,
                   help="Limit to first N rows per input file (omit for all)")
    p.add_argument("--input", nargs="+", default=DEFAULT_INPUTS,
                   help="One or more input CSV paths (default: all 3 romanized split files)")
    args = p.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY is not set. Add it to .env or export it.")

    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic package not found. Run: pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Model:  {MODEL}")
    print(f"Files:  {len(args.input)}")
    print()

    for input_path in args.input:
        process_input(client, input_path, args.rows)


if __name__ == "__main__":
    main()
