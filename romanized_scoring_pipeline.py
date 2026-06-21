from pathlib import Path
import argparse
import unicodedata
import pandas as pd

from scripts.llm_service import EmbeddingClient
from bert_score import BERTScorer


def latin_vs_non_latin_ratio(text: str):
    latin = 0
    non_latin = 0

    for ch in str(text):
        if not ch.isalpha():
            continue

        try:
            if "LATIN" in unicodedata.name(ch):
                latin += 1
            else:
                non_latin += 1
        except ValueError:
            non_latin += 1

    total = latin + non_latin

    return {
        "latin_chars": latin,
        "non_latin_chars": non_latin,
        "latin_ratio": latin / total if total else 0,
        "non_latin_ratio": non_latin / total if total else 0,
    }


def word_overlap_ratio(text1, text2):
    words1 = set(str(text1).lower().split())
    words2 = set(str(text2).lower().split())

    if not words1 and not words2:
        return 0.0

    return len(words1 & words2) / len(words1 | words2)


def add_embedding_scores(df, embedder):
    query_scores = []
    response_scores = []

    for _, row in df.iterrows():
        try:
            query_scores.append(
                embedder.cosine_similarity(
                    str(row["query_en"]),
                    str(row["romanized_query"]),
                )
            )
        except Exception:
            query_scores.append(None)

        try:
            response_scores.append(
                embedder.cosine_similarity(
                    str(row["response_en"]),
                    str(row["romanized_response"]),
                )
            )
        except Exception:
            response_scores.append(None)

    df["query_bge_cosine_similarity"] = query_scores
    df["response_bge_cosine_similarity"] = response_scores

    return df


def add_bert_scores(df, scorer):
    query_p, query_r, query_f1 = scorer.score(
        df["romanized_query"].astype(str).tolist(),
        df["query_en"].astype(str).tolist(),
    )

    resp_p, resp_r, resp_f1 = scorer.score(
        df["romanized_response"].astype(str).tolist(),
        df["response_en"].astype(str).tolist(),
    )

    df["query_bert_precision"] = query_p.cpu().numpy()
    df["query_bert_recall"] = query_r.cpu().numpy()
    df["query_bert_f1"] = query_f1.cpu().numpy()

    df["response_bert_precision"] = resp_p.cpu().numpy()
    df["response_bert_recall"] = resp_r.cpu().numpy()
    df["response_bert_f1"] = resp_f1.cpu().numpy()

    return df


def add_text_metrics(df):
    df["query_word_overlap"] = df.apply(
        lambda r: word_overlap_ratio(
            r["query_en"],
            r["romanized_query"],
        ),
        axis=1,
    )

    df["response_word_overlap"] = df.apply(
        lambda r: word_overlap_ratio(
            r["response_en"],
            r["romanized_response"],
        ),
        axis=1,
    )

    query_stats = pd.json_normalize(
        df["romanized_query"].apply(latin_vs_non_latin_ratio)
    )
    query_stats.columns = [f"query_{c}" for c in query_stats.columns]

    response_stats = pd.json_normalize(
        df["romanized_response"].apply(latin_vs_non_latin_ratio)
    )
    response_stats.columns = [f"response_{c}" for c in response_stats.columns]

    return pd.concat([df, query_stats, response_stats], axis=1)


def process_file(path, scorer, embedder):
    print(f"Processing: {path}")

    df = pd.read_csv(path)

    df = add_embedding_scores(df, embedder)
    df = add_bert_scores(df, scorer)
    df = add_text_metrics(df)

    output_file = f"{Path(path).with_suffix('')}_scored.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")


from pathlib import Path

def default_inputs():

    candidates = [

        Gemini
        r".\output\gemini\gemini_romanized_telugu.csv",
        r".\output\gemini\gemini_romanized_hindi.csv",
        r".\output\gemini\gemini_romanized_kannada.csv",

        Ollama
        r".\output\ollama\ollama_romanized_telugu_split.csv",
        r".\output\ollama\ollama_romanized_hindi_split.csv",
        r".\output\ollama\ollama_romanized_kannada_improved_split.csv",

        GPT
        r".\output\gpt\gpt_romanized_telugu.csv",
        r".\output\gpt\gpt_romanized_hindi.csv",
        r".\output\gpt\gpt_romanized_kannada.csv",

        Anthropic
        r".\output\anthropic_output\anthropic_romanized_telugu.csv",
        r".\output\anthropic_output\anthropic_romanized_hindi.csv",
        r".\output\anthropic_output\anthropic_romanized_kannada.csv",
    ]

    existing_files = [file_path for file_path in candidates if Path(file_path).exists()]

    return existing_files

def main():
    inputs = default_inputs()

    if not inputs:
        raise FileNotFoundError(
            "No romanized CSV files found."
        )

    print("Files to process:")
    for f in inputs:
        print(f"  {f}")

    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--bert-model",
        default="bert-base-multilingual-cased",
    )

    parser.add_argument(
        "--device",
        default=None,
        help="cuda or cpu",
    )

    parser.add_argument(
        "--bert-batch-size",
        type=int,
        default=8,
    )

    args = parser.parse_args()

    scorer = BERTScorer(
        model_type=args.bert_model,
        batch_size=args.bert_batch_size,
        device=args.device,
        rescale_with_baseline=False,
    )

    embedder = EmbeddingClient()

    for file_path in inputs:
        process_file(
            file_path,
            scorer,
            embedder,
        )

    print("All files completed.")


if __name__ == "__main__":
    main()
