"""
Romanization script using Claude API.
Reads native script text from source CSVs and converts to Roman alphabet.
Supports resume - skips already processed rows.
"""

import csv
import os
import time
from pathlib import Path

import anthropic

# ── Configuration ────────────────────────────────────────────────────────────

MODEL = "claude-opus-4-8"

INPUT_FILES = [
    "../hindi_xquad_native_50.csv",
    "../kannada_indicqa_50.csv",
    "../telugu_indicqa_50.csv",
    # Add more files here, e.g.:
    # "../greek_xquad_50.csv",
]

OUTPUT_DIR = Path("output")

# Seconds to wait between API calls (avoids rate limits)
DELAY_BETWEEN_CALLS = 0.5

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a romanization expert. Your task is to convert text written in a non-Latin script into Roman alphabet (Latin script) using standard romanization conventions.

Rules:
- Preserve the phonetic sounds accurately
- Use conventional romanization schemes (e.g., IAST-inspired for Indic scripts)
- Do NOT translate — only transliterate the sounds
- Return ONLY the romanized text, with no explanation or extra text"""


def make_prompt(text: str, language: str) -> str:
    return f"Romanize this {language} text:\n\n{text}"


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_existing(output_path: Path) -> set:
    """Return set of already-processed IDs from output file."""
    if not output_path.exists():
        return set()
    with open(output_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["id"] for row in reader}


def get_output_path(input_file: str) -> Path:
    stem = Path(input_file).stem  # e.g. "hindi_xquad_native_50"
    return OUTPUT_DIR / f"romanized_{stem}.csv"


OUTPUT_FIELDNAMES = [
    "id", "language", "script", "source",
    "original_text", "romanized_text",
    "input_tokens", "output_tokens",
]


def append_row(output_path: Path, row: dict, write_header: bool):
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ── Main processing ───────────────────────────────────────────────────────────

def process_file(client: anthropic.Anthropic, input_file: str):
    input_path = Path(input_file)
    output_path = get_output_path(input_file)

    if not input_path.exists():
        print(f"  [SKIP] File not found: {input_path}")
        return

    # Load source rows
    with open(input_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Check which IDs are already done
    done_ids = load_existing(output_path)
    remaining = [r for r in rows if r["id"] not in done_ids]

    print(f"\n{'─'*60}")
    print(f"File   : {input_path.name}")
    print(f"Total  : {len(rows)} rows")
    print(f"Done   : {len(done_ids)} already processed")
    print(f"To do  : {len(remaining)} remaining")

    if not remaining:
        print("  ✓ All rows already processed, skipping.")
        return

    total_input_tokens = 0
    total_output_tokens = 0

    for i, row in enumerate(remaining, 1):
        text = row["text"]
        language = row.get("language", "unknown")
        row_id = row["id"]

        print(f"  [{i}/{len(remaining)}] {row_id}: {text[:50]}...")

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": make_prompt(text, language)}
                ],
            )

            romanized = response.content[0].text.strip()
            input_tok = response.usage.input_tokens
            output_tok = response.usage.output_tokens
            total_input_tokens += input_tok
            total_output_tokens += output_tok

            out_row = {
                "id": row_id,
                "language": language,
                "script": row.get("script", ""),
                "source": row.get("source", ""),
                "original_text": text,
                "romanized_text": romanized,
                "input_tokens": input_tok,
                "output_tokens": output_tok,
            }

            write_header = not output_path.exists()
            append_row(output_path, out_row, write_header)

            print(f"         → {romanized[:60]}")
            print(f"           tokens: {input_tok} in / {output_tok} out")

        except anthropic.RateLimitError:
            print("  [RATE LIMIT] Waiting 60 seconds...")
            time.sleep(60)
            # Retry once
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": make_prompt(text, language)}
                ],
            )
            romanized = response.content[0].text.strip()
            out_row = {
                "id": row_id,
                "language": language,
                "script": row.get("script", ""),
                "source": row.get("source", ""),
                "original_text": text,
                "romanized_text": romanized,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
            write_header = not output_path.exists()
            append_row(output_path, out_row, write_header)

        except Exception as e:
            print(f"  [ERROR] {row_id}: {e}")
            # Write error row so we know it failed
            out_row = {
                "id": row_id,
                "language": language,
                "script": row.get("script", ""),
                "source": row.get("source", ""),
                "original_text": text,
                "romanized_text": f"ERROR: {e}",
                "input_tokens": 0,
                "output_tokens": 0,
            }
            write_header = not output_path.exists()
            append_row(output_path, out_row, write_header)

        time.sleep(DELAY_BETWEEN_CALLS)

    print(f"\n  ✓ Done: {output_path}")
    print(f"  Total tokens: {total_input_tokens} input / {total_output_tokens} output")
    cost_input = total_input_tokens / 1_000_000 * 5.00   # Opus 4.8 input rate
    cost_output = total_output_tokens / 1_000_000 * 25.00  # Opus 4.8 output rate
    print(f"  Estimated cost: ${cost_input + cost_output:.4f}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Model : {MODEL}")
    print(f"Files : {len(INPUT_FILES)}")

    grand_total_cost = 0.0

    for input_file in INPUT_FILES:
        process_file(client, input_file)

    print(f"\n{'='*60}")
    print("All files processed.")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
