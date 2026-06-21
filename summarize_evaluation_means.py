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


def normalize(text):
    return " ".join((text or "").split())


def calculate_means(path):
    values = {field: [] for field in METRIC_FIELDS}
    seen_ids = set()
    duplicate_rows = 0
    copied_queries = 0
    copied_responses = 0
    copied_rows = 0

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
            message_id = (row.get("message_id") or "").strip()
            if message_id and message_id in seen_ids:
                duplicate_rows += 1
                continue
            if message_id:
                seen_ids.add(message_id)

            query_is_copy = (
                bool(normalize(row.get("query_en")))
                and normalize(row.get("query_en"))
                == normalize(row.get("romanized_query"))
            )
            response_is_copy = (
                bool(normalize(row.get("response_en")))
                and normalize(row.get("response_en"))
                == normalize(row.get("romanized_response"))
            )
            copied_queries += int(query_is_copy)
            copied_responses += int(response_is_copy)
            if query_is_copy or response_is_copy:
                copied_rows += 1
                for field in METRIC_FIELDS:
                    values[field].append(0.0)
                continue

            for field in METRIC_FIELDS:
                score = parse_score(row.get(field))
                values[field].append(score if score is not None else 0.0)

    means = {}
    counts = {}
    for field, scores in values.items():
        means[field] = sum(scores) / len(scores) if scores else None
        counts[field] = len(scores)
    exclusions = {
        "duplicate_rows": duplicate_rows,
        "copied_queries": copied_queries,
        "copied_responses": copied_responses,
        "copied_rows": copied_rows,
    }
    return means, counts, exclusions


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

        means, counts, exclusions = calculate_means(input_path)
        row = {
            "language": language,
            "source_file": filename,
            **{field: format_score(means[field]) for field in METRIC_FIELDS},
            "query_rows_in_mean": counts["query_bertscore_f1"],
            "response_rows_in_mean": counts["response_bertscore_f1"],
            "copied_queries_detected": exclusions["copied_queries"],
            "copied_responses_detected": exclusions["copied_responses"],
            "copied_rows_scored_zero": exclusions["copied_rows"],
            "duplicate_reruns_skipped": exclusions["duplicate_rows"],
        }
        summary_rows.append(row)
        print(
            f"{language}: skipped {exclusions['duplicate_rows']} duplicate "
            f"reruns; assigned zero to "
            f"{exclusions['copied_rows']} complete rows containing "
            f"{exclusions['copied_queries']} copied queries and "
            f"{exclusions['copied_responses']} copied responses"
        )

    if not summary_rows:
        sys.exit("No evaluation result CSV files were found.")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fieldnames = [
        "language",
        "source_file",
        *METRIC_FIELDS,
        "query_rows_in_mean",
        "response_rows_in_mean",
        "copied_queries_detected",
        "copied_responses_detected",
        "copied_rows_scored_zero",
        "duplicate_reruns_skipped",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
