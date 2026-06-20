"""
BGE-M3 semantic similarity evaluation.

For each model × language file in jun19romanoutputs/, computes cosine similarity
between response_en (English reference) and romanized_response (model output in
romanized Indic script). Outputs per-row scores + aggregate summary.
"""

import csv
import os
import numpy as np
from pathlib import Path
from FlagEmbedding import BGEM3FlagModel

DATA_DIR = Path(__file__).parent / "jun19romanoutputs"
OUT_DIR = Path(__file__).parent / "bge_m3_results"
OUT_DIR.mkdir(exist_ok=True)

FILES = {
    ("anthropic", "hindi"):  "anthropic_romanized_hindi.csv",
    ("anthropic", "kannada"): "anthropic_romanized_kannada.csv",
    ("anthropic", "telugu"): "anthropic_romanized_telugu.csv",
    ("gpt",       "hindi"):  "gpt_romanized_hindi.csv",
    ("gpt",       "kannada"): "gpt_romanized_kannada.csv",
    ("gpt",       "telugu"): "gpt_romanized_telugu.csv",
    ("gemini",    "hindi"):  "gemini_romanized_hindi.csv",
    ("gemini",    "kannada"): "gemini_romanized_kannada.csv",
    ("gemini",    "telugu"): "gemini_romanized_telugu.csv",
}

BATCH_SIZE = 32


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def load_pairs(filepath: Path) -> list[dict]:
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ref = (row.get("response_en") or "").strip()
            hyp = (row.get("romanized_response") or "").strip()
            if ref and hyp:
                rows.append({
                    "message_id": row["message_id"],
                    "response_en": ref,
                    "romanized_response": hyp,
                })
    return rows


def embed_in_batches(model: BGEM3FlagModel, texts: list[str]) -> np.ndarray:
    all_vecs = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        out = model.encode(batch, batch_size=len(batch), max_length=512)
        all_vecs.append(out["dense_vecs"])
    return np.vstack(all_vecs)


def main():
    print("Loading BGE-M3 model (first run downloads ~2 GB)...")
    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    print("Model loaded.\n")

    summary_rows = []

    for (model_name, language), filename in FILES.items():
        filepath = DATA_DIR / filename
        if not filepath.exists():
            print(f"  [SKIP] {filename} not found")
            continue

        print(f"Processing {model_name} / {language} ...")
        pairs = load_pairs(filepath)
        if not pairs:
            print(f"  [SKIP] no valid rows")
            continue

        refs = [p["response_en"] for p in pairs]
        hyps = [p["romanized_response"] for p in pairs]

        ref_vecs = embed_in_batches(model, refs)
        hyp_vecs = embed_in_batches(model, hyps)

        scores = [cosine_sim(ref_vecs[i], hyp_vecs[i]) for i in range(len(pairs))]

        # Write per-row results
        out_file = OUT_DIR / f"{model_name}_{language}_bge_scores.csv"
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["message_id", "model", "language", "bge_m3_cosine"])
            for p, s in zip(pairs, scores):
                writer.writerow([p["message_id"], model_name, language, round(s, 6)])

        mean_score = float(np.mean(scores))
        print(f"  n={len(scores)}  mean_cosine={mean_score:.4f}  → {out_file.name}")
        summary_rows.append({
            "model": model_name,
            "language": language,
            "n": len(scores),
            "mean_bge_m3": round(mean_score, 4),
            "std_bge_m3": round(float(np.std(scores)), 4),
            "min_bge_m3": round(float(np.min(scores)), 4),
            "max_bge_m3": round(float(np.max(scores)), 4),
        })

    # Write summary
    summary_path = OUT_DIR / "summary.csv"
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["model", "language", "n", "mean_bge_m3", "std_bge_m3", "min_bge_m3", "max_bge_m3"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\nSummary written to {summary_path}")
    print("\n=== RESULTS ===")
    print(f"{'Model':<12} {'Language':<10} {'N':>4} {'Mean':>7} {'Std':>7} {'Min':>7} {'Max':>7}")
    print("-" * 55)
    for r in summary_rows:
        print(f"{r['model']:<12} {r['language']:<10} {r['n']:>4} {r['mean_bge_m3']:>7.4f} {r['std_bge_m3']:>7.4f} {r['min_bge_m3']:>7.4f} {r['max_bge_m3']:>7.4f}")


if __name__ == "__main__":
    main()
