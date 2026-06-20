#!/usr/bin/env python3
"""
ollama_romanize.py — Re-run romanization with local Ollama/Qwen using the
existing split CSVs in output/.

Default input:
    output/romanized_<lang>_split.csv

Default output:
    output/ollama_romanized_<lang>_split.csv

Setup:
    1. Install Ollama for macOS.
    2. In one terminal, start Ollama if it is not already running:
           ollama serve
    3. Pull/run Qwen once:
           ollama run qwen3:8b

Run:
    python3 ollama_romanize.py --rows 10
    python3 ollama_romanize.py --rows 10 --languages hindi telugu kannada
    python3 ollama_romanize.py --model qwen3:4b --rows 100

Notes:
    - This script uses only Python's standard library.
    - It makes one model call per row per language with query and response
      together. Ollama's eval_count is captured as the combined output-token
      count for romanized_query + romanized_response + JSON syntax.
"""

import argparse
import csv
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(HERE, "output")

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MAX_RETRIES = 4

LANGUAGES = {
    "hindi": {
        "name": "Hindi",
        "example": 'Example style: "Namaste, aap kaise hain? Main theek hoon."',
    },
    "telugu": {
        "name": "Telugu",
        "example": 'Example style: "Namaskaram, meeru ela unnaru? Nenu bagunnaanu."',
    },
    "kannada": {
        "name": "Kannada",
        "example": 'Example style: "Namaskara, neevu hegiddira? Naanu chennagiddini."',
    },
}


def build_system_prompt(lang_key):
    m = LANGUAGES[lang_key]
    return (
        f"Translate English to natural conversational {m['name']}, then romanize "
        f"in Latin letters only (a-z). {m['example']}\n\n"
        "Keep English loanwords speakers actually use (doctor, phone, office, etc.). "
        "Preserve formatting, line breaks, names, numbers, URLs.\n\n"
        "Input: English `query` and `response`. Output JSON only:\n"
        '{"romanized_query": "...", "romanized_response": "..."}'
    )


def build_user_prompt(query, response):
    return (
        "Romanize the following English query and response as instructed.\n\n"
        + json.dumps({"query": query, "response": response}, ensure_ascii=False)
    )


def post_json(url, payload, timeout):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_json_object(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            recovered = recover_romanized_value(candidate)
            if recovered:
                return {"romanized": recovered}

    recovered = recover_romanized_value(text)
    if recovered:
        return {"romanized": recovered}

    raise ValueError(f"Model did not return JSON: {text[:300]}")


def recover_json_value(text, key):
    """Recover text from common malformed Ollama/Qwen JSON-ish responses."""
    marker = f'"{key}"'
    marker_pos = text.find(marker)
    if marker_pos == -1:
        return ""

    colon_pos = text.find(":", marker_pos + len(marker))
    if colon_pos == -1:
        return ""

    value = text[colon_pos + 1 :].strip()
    if value.startswith('"'):
        value = value[1:]
    if value.endswith("}"):
        value = value[:-1].rstrip()
    if value.endswith('"'):
        value = value[:-1]

    value = value.replace('\\"', '"').replace("\\n", "\n").strip()
    return value


def recover_romanized_value(text):
    return recover_json_value(text, "romanized")


def clean_model_text(text):
    text = (text or "").strip()
    text = re.sub(r"(?is)<think>.*?</think>", "", text).strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            for key in ("romanized", "text", "output", "translation"):
                if key in parsed:
                    return str(parsed[key]).strip()
        if isinstance(parsed, str):
            return parsed.strip()
    except json.JSONDecodeError:
        pass

    lowered = text.lower()
    for prefix in (
        "romanized response:",
        "romanized query:",
        "romanized:",
        "response:",
        "query:",
        "output:",
    ):
        if lowered.startswith(prefix):
            text = text[len(prefix) :].strip()
            break

    return text.strip().strip('"').strip()


def looks_like_echoed_input(output, source_text):
    lowered = (output or "").lower().lstrip()
    bad_markers = (
        "field:",
        "english_text:",
        "<<<begin_english>>>",
        "<<<end_english>>>",
        "<<start_romanized",
        "<<end_romanized",
        "start_romanized",
        "end_romanized",
    )
    if any(marker in lowered[:500] for marker in bad_markers):
        return True

    source_start = (source_text or "").strip()[:160].lower()
    output_start = (output or "").strip()[:220].lower()
    if source_start and source_start[:80] in output_start:
        return True

    copied_phrases = 0
    source_sentences = re.split(r"(?<=[.!?])\s+", (source_text or "").strip())
    output_lower = (output or "").lower()
    for sentence in source_sentences:
        normalized = re.sub(r"\s+", " ", sentence.strip().lower())
        if len(normalized) < 40:
            continue
        if normalized in output_lower:
            if len(normalized) >= 90:
                return True
            copied_phrases += 1
        if copied_phrases >= 2:
            return True

    source_words = re.findall(r"[a-zA-Z']+", (source_text or "").lower())
    output_words_text = " ".join(re.findall(r"[a-zA-Z']+", output_lower))
    copied_windows = 0
    for index in range(0, max(0, len(source_words) - 7)):
        phrase = " ".join(source_words[index : index + 8])
        if len(phrase) < 45:
            continue
        if phrase in output_words_text:
            copied_windows += 1
        if copied_windows >= 3:
            return True

    return False


def romanize_pair(args, lang_key, query, response):
    endpoint = args.ollama_url.rstrip("/") + "/api/chat"
    start_time = time.time()

    for attempt in range(1, MAX_RETRIES + 1):
        payload = {
            "model": args.model,
            "stream": False,
            "format": "json",
            "think": False,
            "options": {
                "temperature": args.temperature,
                "num_predict": args.num_predict,
            },
            "messages": [
                {"role": "system", "content": build_system_prompt(lang_key)},
                {"role": "user", "content": build_user_prompt(query, response)},
            ],
        }
        try:
            result = post_json(endpoint, payload, args.timeout)
            content = result.get("message", {}).get("content", "")
            try:
                data = extract_json_object(content)
            except ValueError:
                data = {}
            romanized_query = str(data.get("romanized_query", "")).strip()
            romanized_response = str(data.get("romanized_response", "")).strip()

            if not romanized_query:
                romanized_query = recover_json_value(content, "romanized_query")
            if not romanized_response:
                romanized_response = recover_json_value(content, "romanized_response")
            if not romanized_query or not romanized_response:
                if attempt == MAX_RETRIES:
                    output_tokens = int(result.get("eval_count") or 0)
                    elapsed = time.time() - start_time
                    missing = []
                    if not romanized_query:
                        missing.append("romanized_query")
                    if not romanized_response:
                        missing.append("romanized_response")
                    print(
                        "      warning: saving partial output; missing "
                        + ", ".join(missing),
                        file=sys.stderr,
                    )
                    return (
                        romanized_query,
                        romanized_response,
                        output_tokens,
                        elapsed,
                    )
                raise ValueError(f"Model did not return both JSON fields: {content[:300]}")
            output_tokens = int(result.get("eval_count") or 0)
            elapsed = time.time() - start_time
            return romanized_query, romanized_response, output_tokens, elapsed
        except (socket.timeout, TimeoutError) as err:
            raise RuntimeError(
                f"Ollama request exceeded the {args.timeout}s timeout."
            ) from err
        except urllib.error.URLError as err:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    "Could not reach Ollama. Make sure `ollama serve` is running "
                    f"and the model `{args.model}` is available."
                ) from err
        except Exception as err:
            if attempt == MAX_RETRIES:
                raise
            print(f"      attempt {attempt} failed: {err}", file=sys.stderr)

        wait = 2 ** attempt
        print(f"      retrying in {wait}s...", file=sys.stderr)
        time.sleep(wait)

    raise RuntimeError("unreachable retry state")


def read_rows(path, rows_limit):
    if not os.path.exists(path):
        sys.exit(f"Input CSV not found: {path}")

    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if rows_limit is None:
        return rows
    return rows[:rows_limit]


def language_input_path(input_dir, lang_key):
    return os.path.join(input_dir, f"romanized_{lang_key}_split.csv")


def english_query(row):
    return row.get("query_en", "") or ""


def english_response(row):
    return row.get("response_en", "") or ""


def output_path(output_dir, lang_key):
    return os.path.join(output_dir, f"ollama_romanized_{lang_key}_split.csv")


def already_done_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as handle:
        return {row.get("message_id", "") for row in csv.DictReader(handle)}


def open_writer(path, resume):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = [
        "message_id",
        "language",
        "model",
        "query_en",
        "response_en",
        "romanized_query",
        "romanized_response",
        "romanized_total_tokens",
    ]
    mode = "a" if resume and os.path.exists(path) else "w"
    handle = open(path, mode, newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    if mode == "w":
        writer.writeheader()
    return handle, writer


def process_language(args, rows, lang_key, source_path):
    lang_name = LANGUAGES[lang_key]["name"]
    path = output_path(args.output_dir, lang_key)

    output_total = 0
    skipped = 0

    print(f"=== {lang_name} ===")
    print(f"  input:  {source_path}")
    print(f"  output: {path}")

    if not rows:
        print(f"  {lang_name} total output tokens: 0\n")
        return output_total

    done_ids = already_done_ids(path) if args.resume else set()
    handle, writer = open_writer(path, args.resume)
    try:
        for idx, row in enumerate(rows, start=1):
            message_id = row.get("message_id", "")
            if message_id in done_ids:
                skipped += 1
                continue

            query = english_query(row)
            response = english_response(row)
            short_id = (message_id or "no-id")[:8]
            print(f"  [{idx}/{len(rows)}] {short_id}...", flush=True)

            print("      calling Ollama for query+response...", flush=True)
            row_start = time.time()
            try:
                (
                    romanized_query,
                    romanized_response,
                    row_total_tokens,
                    elapsed,
                ) = romanize_pair(args, lang_key, query, response)
            except Exception as err:
                romanized_query = ""
                romanized_response = ""
                row_total_tokens = 0
                elapsed = time.time() - row_start
                print(
                    f"      warning: row failed ({err}); saving blanks and continuing",
                    file=sys.stderr,
                    flush=True,
                )

            output_total += row_total_tokens
            print(
                f"      done in {elapsed:.1f}s; combined output tokens={row_total_tokens}",
                flush=True,
            )

            writer.writerow(
                {
                    "message_id": message_id,
                    "language": lang_name,
                    "model": args.model,
                    "query_en": query,
                    "response_en": response,
                    "romanized_query": romanized_query,
                    "romanized_response": romanized_response,
                    "romanized_total_tokens": row_total_tokens,
                }
            )
            handle.flush()
    finally:
        handle.close()

    if skipped:
        print(f"  skipped existing rows: {skipped}")
    print(
        f"  {lang_name} total output tokens: {output_total}\n"
    )
    return output_total


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Romanize query_en/response_en fields from output/"
            "romanized_<lang>_split.csv using local Ollama."
        )
    )
    parser.add_argument(
        "--input-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Folder containing romanized_<lang>_split.csv input files.",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output folder.")
    parser.add_argument("--rows", type=int, default=None, help="Rows to process. Default: all.")
    parser.add_argument(
        "--languages",
        nargs="+",
        default=list(LANGUAGES.keys()),
        choices=list(LANGUAGES.keys()),
        help="Languages to generate.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name.")
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Append to existing output and skip message_id values already present.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Model: {args.model}")
    print(f"Ollama URL: {args.ollama_url}")
    print(f"Input mode: per-language CSVs from {args.input_dir}")
    print("Mode: 1 Ollama call per row per language for combined output tokens\n")

    grand_total = 0
    for lang_key in args.languages:
        source_path = language_input_path(args.input_dir, lang_key)
        rows = read_rows(source_path, args.rows)
        print(f"Loaded {len(rows)} rows")
        output_total = process_language(args, rows, lang_key, source_path)
        grand_total += output_total

    print("Token usage summary")
    print(f"  grand total output tokens: {grand_total}")
    print("Done.")


if __name__ == "__main__":
    main()
