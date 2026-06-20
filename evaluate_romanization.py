#!/usr/bin/env python3
"""
Evaluate English-to-romanized outputs with BERTScore and BGE-M3 similarity.

Install:
    pip install bert-score torch transformers
    ollama pull bge-m3

Examples:
    python evaluate_romanization.py
    python evaluate_romanization.py --inputs output/ollama_romanized_hindi_split.csv
    python evaluate_romanization.py --device cuda --embedding-batch-size 16

The default run produces one table per language:
    output/hindi_evaluation_results.csv
    output/telugu_evaluation_results.csv
    output/kannada_evaluation_results.csv
"""

import argparse
import csv
import json
import math
import os
import sys
import urllib.error
import urllib.request


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(HERE, "output")

SOURCE_FIELDS = [
    "message_id",
    "language",
    "model",
    "query_en",
    "response_en",
    "romanized_query",
    "romanized_response",
    "romanized_total_tokens",
]

METRIC_FIELDS = [
    "query_bertscore_precision",
    "query_bertscore_recall",
    "query_bertscore_f1",
    "query_bge_cosine_similarity",
    "response_bertscore_precision",
    "response_bertscore_recall",
    "response_bertscore_f1",
    "response_bge_cosine_similarity",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add BERTScore and Ollama BGE-M3 similarity to romanized CSVs."
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        help=(
            "Input CSV files. Default: one preferred generated CSV each for "
            "Hindi, Telugu, and Kannada."
        ),
    )
    parser.add_argument(
        "--ollama-url",
        default=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        help="Ollama base URL.",
    )
    parser.add_argument(
        "--embedding-model",
        default="bge-m3",
        help="Ollama embedding model.",
    )
    parser.add_argument(
        "--bert-model",
        default="bert-base-multilingual-cased",
        help="Hugging Face model used by BERTScore.",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="BERTScore device, such as cuda or cpu. Default: automatic.",
    )
    parser.add_argument("--bert-batch-size", type=int, default=8)
    parser.add_argument("--embedding-batch-size", type=int, default=16)
    parser.add_argument("--timeout", type=int, default=600)
    return parser.parse_args()


def default_inputs():
    preferred = {
        "hindi": [
            "ollama_romanized_hindi_split.csv",
            "qwen_transformers_romanized_hindi_split.csv",
        ],
        "telugu": ["ollama_romanized_telugu_split.csv"],
        "kannada": [
            "ollama_romanized_kannada_improved_split.csv",
            "ollama_romanized_kannada_split.csv",
        ],
    }
    paths = []
    for candidates in preferred.values():
        for filename in candidates:
            path = os.path.join(DEFAULT_OUTPUT_DIR, filename)
            if os.path.exists(path):
                paths.append(path)
                break
    return paths


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        try:
            first_row = next(reader)
        except StopIteration:
            return [], SOURCE_FIELDS

    has_header = "message_id" in first_row and "query_en" in first_row
    with open(path, newline="", encoding="utf-8-sig") as handle:
        if has_header:
            dict_reader = csv.DictReader(handle)
        else:
            print(f"  warning: no CSV header detected; using known column order")
            dict_reader = csv.DictReader(handle, fieldnames=SOURCE_FIELDS)
        rows = list(dict_reader)
        fieldnames = list(dict_reader.fieldnames or SOURCE_FIELDS)
    return rows, fieldnames


def normalize(text):
    return " ".join((text or "").split())


def metric_pairs(rows):
    pairs = []
    for row_index, row in enumerate(rows):
        for field_name, english_key, romanized_key in (
            ("query", "query_en", "romanized_query"),
            ("response", "response_en", "romanized_response"),
        ):
            english = normalize(row.get(english_key, ""))
            romanized = normalize(row.get(romanized_key, ""))
            if english and romanized:
                pairs.append(
                    {
                        "row_index": row_index,
                        "field_name": field_name,
                        "english": english,
                        "romanized": romanized,
                    }
                )
    return pairs


def post_json(url, payload, timeout):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def cosine_similarity(left, right):
    if not left or not right or len(left) != len(right):
        return None
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return None
    return dot / (left_norm * right_norm)


def add_bge_scores(pairs, args):
    endpoint = args.ollama_url.rstrip("/") + "/api/embed"
    total = len(pairs)
    for start in range(0, total, args.embedding_batch_size):
        batch = pairs[start : start + args.embedding_batch_size]
        texts = []
        for pair in batch:
            texts.extend([pair["english"], pair["romanized"]])

        result = post_json(
            endpoint,
            {
                "model": args.embedding_model,
                "input": texts,
                "truncate": True,
            },
            args.timeout,
        )
        embeddings = result.get("embeddings", [])
        if len(embeddings) != len(texts):
            raise RuntimeError(
                f"Ollama returned {len(embeddings)} embeddings for "
                f"{len(texts)} texts."
            )

        for offset, pair in enumerate(batch):
            pair["bge_cosine"] = cosine_similarity(
                embeddings[offset * 2], embeddings[offset * 2 + 1]
            )
        print(
            f"    BGE-M3: {min(start + len(batch), total)}/{total}",
            flush=True,
        )


def add_bert_scores(pairs, args):
    try:
        from bert_score import BERTScorer
    except ImportError:
        sys.exit(
            "bert-score is not installed. Run: "
            "pip install bert-score torch transformers"
        )

    kwargs = {
        "model_type": args.bert_model,
        "batch_size": args.bert_batch_size,
        "rescale_with_baseline": False,
    }
    if args.device:
        kwargs["device"] = args.device

    scorer = BERTScorer(**kwargs)
    candidates = [pair["romanized"] for pair in pairs]
    references = [pair["english"] for pair in pairs]
    precision, recall, f1 = scorer.score(
        candidates,
        references,
        batch_size=args.bert_batch_size,
        verbose=True,
    )

    for index, pair in enumerate(pairs):
        pair["bert_precision"] = float(precision[index])
        pair["bert_recall"] = float(recall[index])
        pair["bert_f1"] = float(f1[index])


def format_score(value):
    if value is None:
        return ""
    return f"{value:.6f}"


def language_key(input_path, rows):
    if rows:
        language = (rows[0].get("language", "") or "").strip().lower()
        if language in ("hindi", "telugu", "kannada"):
            return language
    filename = os.path.basename(input_path).lower()
    for language in ("hindi", "telugu", "kannada"):
        if language in filename:
            return language
    return "unknown"


def write_evaluated(input_path, rows, source_fields, pairs):
    metrics_by_row = {}
    for pair in pairs:
        metrics_by_row[(pair["row_index"], pair["field_name"])] = pair

    language = language_key(input_path, rows)
    output_path = os.path.join(
        os.path.dirname(input_path),
        f"{language}_evaluation_results.csv",
    )
    fieldnames = list(dict.fromkeys(source_fields + METRIC_FIELDS))
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        for row_index, row in enumerate(rows):
            output_row = dict(row)
            for field_name in ("query", "response"):
                pair = metrics_by_row.get((row_index, field_name))
                output_row[f"{field_name}_bertscore_precision"] = format_score(
                    pair.get("bert_precision") if pair else None
                )
                output_row[f"{field_name}_bertscore_recall"] = format_score(
                    pair.get("bert_recall") if pair else None
                )
                output_row[f"{field_name}_bertscore_f1"] = format_score(
                    pair.get("bert_f1") if pair else None
                )
                output_row[f"{field_name}_bge_cosine_similarity"] = format_score(
                    pair.get("bge_cosine") if pair else None
                )
            writer.writerow(output_row)
    return output_path


def print_averages(pairs):
    for field_name in ("query", "response"):
        selected = [
            pair for pair in pairs if pair["field_name"] == field_name
        ]
        if not selected:
            continue
        bert_average = sum(pair["bert_f1"] for pair in selected) / len(selected)
        cosine_values = [
            pair["bge_cosine"]
            for pair in selected
            if pair.get("bge_cosine") is not None
        ]
        cosine_average = (
            sum(cosine_values) / len(cosine_values)
            if cosine_values
            else float("nan")
        )
        print(
            f"    {field_name}: mean BERTScore F1={bert_average:.6f}, "
            f"mean BGE cosine={cosine_average:.6f}"
        )


def main():
    args = parse_args()
    inputs = args.inputs or default_inputs()
    if not inputs:
        sys.exit("No romanized output CSV files found.")

    print(f"BERTScore model: {args.bert_model}")
    print(f"Ollama embedding model: {args.embedding_model}")
    print(f"Ollama URL: {args.ollama_url}\n")

    for input_path in inputs:
        if not os.path.exists(input_path):
            print(f"Skipping missing file: {input_path}", file=sys.stderr)
            continue

        print(f"=== {input_path} ===")
        rows, source_fields = read_csv(input_path)
        pairs = metric_pairs(rows)
        print(f"  rows: {len(rows)}; non-empty field pairs: {len(pairs)}")
        if pairs:
            print("  Calculating BERTScore...", flush=True)
            add_bert_scores(pairs, args)
            print("  Calculating BGE-M3 cosine similarity...", flush=True)
            try:
                add_bge_scores(pairs, args)
            except (urllib.error.URLError, TimeoutError) as error:
                raise RuntimeError(
                    "Could not use Ollama embeddings. Ensure Ollama is running "
                    f"and `{args.embedding_model}` is installed."
                ) from error

        output_path = write_evaluated(
            input_path, rows, source_fields, pairs
        )
        print_averages(pairs)
        print(f"  -> {output_path}\n")

    print("Done.")


if __name__ == "__main__":
    main()
