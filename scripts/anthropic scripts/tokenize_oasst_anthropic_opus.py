#!/usr/bin/env python3
"""
tokenize_oasst2.py — Get exact token counts for all OASST2 reference responses.

This script reads oasst2_processed.csv and uses Claude's API to measure
the exact number of tokens needed to represent each Response.

Output: oasst2_with_tokens.csv (adds 'response_tokens' column)

Setup:
    pip install anthropic python-dotenv pandas
    Add ANTHROPIC_API_KEY=sk-ant-... to .env

Run:
    python tokenize_oasst2.py                # all 142 responses
    python tokenize_oasst2.py --rows 5       # test with 5 first
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(HERE, "data", "oasst2_processed.csv")
OUTPUT_DIR = os.path.join(HERE, "output")

MAX_RETRIES = 3
DELAY_BETWEEN_CALLS = 0.5  # seconds


def tokenize_response(client, response_text: str) -> int:
    """
    Send response text to Claude and get the exact token count.
    We treat the response as user input and measure its input_tokens.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Send a minimal message with just the response text
            # We measure input_tokens to get the token count of the response
            message = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=10,  # Minimal response needed
                messages=[{"role": "user", "content": response_text}],
            )
            # input_tokens tells us how many tokens the response_text consumed
            return message.usage.input_tokens

        except Exception as err:
            msg = str(err).lower()
            if "rate" in msg or "429" in msg:
                print(f"      rate limit hit — waiting 60s...", file=sys.stderr)
                time.sleep(60)
                continue
            if attempt == MAX_RETRIES:
                raise
            wait = 2 ** attempt
            print(f"      attempt {attempt} failed ({err}); retrying in {wait}s...",
                  file=sys.stderr)
            time.sleep(wait)

    raise RuntimeError("Exhausted retries")


def main():
    p = argparse.ArgumentParser(description="Tokenize OASST2 responses.")
    p.add_argument("--rows", type=int, default=None,
                   help="Limit to first N rows (omit for all 142)")
    p.add_argument("--input", default=DEFAULT_INPUT,
                   help=f"Path to input CSV (default: {DEFAULT_INPUT})")
    args = p.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY not set. Add it to your .env file.")

    try:
        import anthropic
    except ImportError:
        sys.exit("Run: pip install anthropic pandas python-dotenv")

    client = anthropic.Anthropic(api_key=api_key)

    # Load input
    if not os.path.exists(args.input):
        sys.exit(f"Input file not found: {args.input}")

    df = pd.read_csv(args.input)
    if args.rows:
        df = df.head(args.rows)

    print(f"Tokenizing {len(df)} OASST2 responses...\n")

    # Process each row
    token_counts = []
    for idx, row in enumerate(df.itertuples(), start=1):
        msg_id = row.message_id
        response = row.Response

        print(f"  [{idx:>3}/{len(df)}]  {msg_id[:8]}...", end="  ")

        tokens = tokenize_response(client, response)
        token_counts.append(tokens)

        print(f"{tokens:>5} tokens")

        time.sleep(DELAY_BETWEEN_CALLS)

    # Add token counts to dataframe
    df["response_tokens"] = token_counts

    # Save output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "oasst2_with_tokens.csv")
    df.to_csv(output_path, index=False)

    # Summary stats
    print(f"\n{'='*50}")
    print(f"Done. Output: {output_path}\n")
    print(f"Token count statistics for {len(df)} OASST2 responses:")
    print(f"  Min:    {df['response_tokens'].min()}")
    print(f"  Max:    {df['response_tokens'].max()}")
    print(f"  Avg:    {df['response_tokens'].mean():.1f}")
    print(f"  Median: {df['response_tokens'].median():.0f}")
    print(f"  Total:  {df['response_tokens'].sum():,} tokens")

    # Cost estimate
    total_tokens_processed = df["Response"].str.len().sum() / 4  # rough estimate for input
    input_cost = (total_tokens_processed / 1_000_000) * 5
    output_cost = (10 * len(df) / 1_000_000) * 25  # 10 tokens output per call
    total_cost = input_cost + output_cost
    print(f"\nEstimated cost: ${total_cost:.2f}")


if __name__ == "__main__":
    main()
