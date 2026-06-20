#!/usr/bin/env python3
"""Calculate mean evaluation metrics for Hindi, Telugu, and Kannada CSVs."""

import argparse
import csv
import os
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(HERE, "output")

LANGUAGE_FILES = {
    "Hindi": "hindi_evaluation_results.csv",
    "Telugu": "telugu_evaluation_results.csv",
    "Kannada": "kannada_evaluation_results.csv",
}

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
        description="Calculate per-language means from evaluation result CSVs."
    )
    parser.add_argument(
        "--input-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory containing the language evaluation CSVs.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Summary CSV path. Default: "
            "<input-dir>/evaluation_metric_means.csv"
        ),
    )
    return parser.parse_args()


def parse_score(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def calculate_means(path):
    values = {field: [] for field in METRIC_FIELDS}

    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in METRIC_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"{path} is missing metric columns: {', '.join(missing)}"
            )

        for row in reader:
            if (row.get("message_id") or "").strip().upper() == "MEAN":
                continue
            for field in METRIC_FIELDS:
                score = parse_score(row.get(field))
                if score is not None:
                    values[field].append(score)

    means = {}
    counts = {}
    for field, scores in values.items():
        means[field] = sum(scores) / len(scores) if scores else None
        counts[field] = len(scores)
    return means, counts


def format_score(value):
    return "" if value is None else f"{value:.6f}"


def main():
    args = parse_args()
    output_path = args.output or os.path.join(
        args.input_dir, "evaluation_metric_means.csv"
    )

    summary_rows = []
    for language, filename in LANGUAGE_FILES.items():
        input_path = os.path.join(args.input_dir, filename)
        if not os.path.exists(input_path):
            print(f"Skipping missing file: {input_path}", file=sys.stderr)
            continue

        means, counts = calculate_means(input_path)
        row = {
            "language": language,
            "source_file": filename,
            **{field: format_score(means[field]) for field in METRIC_FIELDS},
            "query_rows_scored": counts["query_bertscore_f1"],
            "response_rows_scored": counts["response_bertscore_f1"],
        }
        summary_rows.append(row)
        print(f"{language}: calculated means from {filename}")

    if not summary_rows:
        sys.exit("No evaluation result CSV files were found.")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fieldnames = [
        "language",
        "source_file",
        *METRIC_FIELDS,
        "query_rows_scored",
        "response_rows_scored",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
