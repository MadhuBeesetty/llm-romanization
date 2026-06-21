import pandas as pd
from pathlib import Path
from glob import glob

files = glob(r"..\output\**\*_scored.csv", recursive=True)

results = []

for file in files:

    df = pd.read_csv(file)

    ## Filters
    invalid_mask = (
        (df["query_word_overlap"] == 1)
        | (df["response_word_overlap"] == 1)
        | (df["query_non_latin_chars"] > 0)
        | (df["response_non_latin_chars"] > 0)
    )

    df.loc[
        invalid_mask,
        [
            "query_bge_cosine_similarity",
            "response_bge_cosine_similarity",
            "query_bert_f1",
            "query_bert_precision",
            "query_bert_recall",
            "response_bert_f1",
            "response_bert_precision",
            "response_bert_recall",
        ],
    ] = 0

    results.append(
        {
            "file": Path(file).stem,
            "rows": len(df),
            "invalid_rows": invalid_mask.sum(),
            "query_bge": df["query_bge_cosine_similarity"].mean().round(3),
            "response_bge": df["response_bge_cosine_similarity"].mean().round(3),
            "query_bert_f1": df["query_bert_f1"].mean().round(3),
            "query_bert_precision": df["query_bert_precision"].mean().round(3),
            "query_bert_recall": df["query_bert_recall"].mean().round(3),
            "response_bert_f1": df["response_bert_f1"].mean().round(3),
            "response_bert_precision": df["response_bert_precision"].mean().round(3),
            "response_bert_recall": df["response_bert_recall"].mean().round(3),
            "query_overlap": sum(df["query_word_overlap"] == 1),
            "response_overlap": sum(df["response_word_overlap"]== 1),
            "query_non_latin_ratio": sum(df["query_non_latin_chars"] > 0),
            "response_non_latin_ratio": sum(df["response_non_latin_chars"] > 0),
        }
    )

summary = pd.DataFrame(results)
summary.rename({"query_overlap": "llm repeated query",
                "response_overlap": "llm repeated response",
                "query_non_latin_ratio": "native_text_in_query",
                "response_non_latin_ratio": "native_text_in_response"}, axis=1, inplace=True)

print(summary.round(3))