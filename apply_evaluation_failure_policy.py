#!/usr/bin/env python3
"""Apply the final failure-scoring policy to existing evaluation CSVs."""

import csv
import os


HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(HERE, "output")

LANGUAGES = ("hindi", "telugu", "kannada")

QUERY_METRICS = (
    "query_bertscore_precision",
    "query_bertscore_recall",
    "query_bertscore_f1",
    "query_bge_cosine_similarity",
)

RESPONSE_METRICS = (
    "response_bertscore_precision",
    "response_bertscore_recall",
    "response_bertscore_f1",
    "response_bge_cosine_similarity",
)


def normalize(text):
    return " ".join((text or "").split())


def main():
    for language in LANGUAGES:
        path = os.path.join(
            OUTPUT_DIR, f"{language}_evaluation_results.csv"
        )
        with open(path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [
                row
                for row in reader
                if normalize(row.get("message_id")).upper() != "MEAN"
            ]

        seen_ids = set()
        output_rows = []
        duplicate_count = 0
        copied_count = 0
        blank_query_count = 0
        blank_response_count = 0

        for row in rows:
            message_id = normalize(row.get("message_id"))
            if message_id and message_id in seen_ids:
                duplicate_count += 1
                continue
            if message_id:
                seen_ids.add(message_id)

            query_en = normalize(row.get("query_en"))
            response_en = normalize(row.get("response_en"))
            romanized_query = normalize(row.get("romanized_query"))
            romanized_response = normalize(row.get("romanized_response"))

            copied = (
                (query_en and query_en == romanized_query)
                or (response_en and response_en == romanized_response)
            )
            if copied:
                copied_count += 1
                for field in QUERY_METRICS + RESPONSE_METRICS:
                    row[field] = "0.000000"
            else:
                if not romanized_query:
                    blank_query_count += 1
                    for field in QUERY_METRICS:
                        row[field] = "0.000000"
                if not romanized_response:
                    blank_response_count += 1
                    for field in RESPONSE_METRICS:
                        row[field] = "0.000000"

            output_rows.append(row)

        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fieldnames,
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(output_rows)

        print(
            f"{language}: rows={len(output_rows)}, duplicates_removed="
            f"{duplicate_count}, copied_rows_zero={copied_count}, "
            f"blank_queries_zero={blank_query_count}, "
            f"blank_responses_zero={blank_response_count}"
        )


if __name__ == "__main__":
    main()
