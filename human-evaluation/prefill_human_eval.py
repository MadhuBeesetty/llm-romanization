"""
Rebuilds human eval files with 10 parameters.
Columns 1-5 are pre-filled automatically.
Columns 6-10 are left blank for native-speaker evaluators.

Scoring logic
─────────────
1. Response Completeness (0-2)
   0 = empty/whitespace
   1 = very short (<25% of English reference word count)
   2 = complete

2. Script Purity (0-2)
   2 = 0 non-Latin chars
   1 = 1-10 non-Latin chars (word-level leakage)
   0 = >10 non-Latin chars (sentence/paragraph in native script)

3. English-Romanized Balance (0-3)
   Based on response_word_overlap ratio (Jaccard overlap with English source)
   3 = overlap < 0.30   (well romanized)
   2 = 0.30–0.50        (slightly English-heavy)
   1 = 0.50–0.70        (too much English)
   0 = > 0.70           (barely romanized / copied)

4. Romanization Consistency (0-3)
   Checks within the response for:
   - Mixed diacritics (ā/ē/ī/ō/ū alongside plain a/e/i/o/u for same sound)
   - Vowel length inconsistency (aa vs a, ee vs i, oo vs u for same word root)
   - Case inconsistency mid-sentence
   3 = no detectable issues
   2 = 1-2 minor inconsistencies
   1 = 3+ inconsistencies
   0 = completely inconsistent scheme

5. Semantic Faithfulness (0-3)
   Based on response_bge_cosine_similarity
   3 = BGE ≥ 0.85
   2 = BGE 0.70–0.85
   1 = BGE 0.50–0.70
   0 = BGE < 0.50 or empty
"""

import re
import pandas as pd
from pathlib import Path

BASE     = Path(__file__).parent
EVAL_DIR = BASE / "human_eval_files"

FILES = {
    ("anthropic", "hindi"):   BASE / "output/anthropic_output/anthropic_romanized_hindi_scored.csv",
    ("anthropic", "kannada"): BASE / "output/anthropic_output/anthropic_romanized_kannada_scored.csv",
    ("anthropic", "telugu"):  BASE / "output/anthropic_output/anthropic_romanized_telugu_scored.csv",
    ("gpt",       "hindi"):   BASE / "output/gpt/gpt_romanized_hindi_scored.csv",
    ("gpt",       "kannada"): BASE / "output/gpt/gpt_romanized_kannada_scored.csv",
    ("gpt",       "telugu"):  BASE / "output/gpt/gpt_romanized_telugu_scored.csv",
    ("gemini",    "hindi"):   BASE / "output/gemini/gemini_romanized_hindi_scored.csv",
    ("gemini",    "kannada"): BASE / "output/gemini/gemini_romanized_kannada_scored.csv",
    ("gemini",    "telugu"):  BASE / "output/gemini/gemini_romanized_telugu_scored.csv",
    ("ollama",    "hindi"):   BASE / "output/ollama/ollama_romanized_hindi_split_scored.csv",
    ("ollama",    "kannada"): BASE / "output/ollama/ollama_romanized_kannada_improved_split_scored.csv",
    ("ollama",    "telugu"):  BASE / "output/ollama/ollama_romanized_telugu_split_scored.csv",
}

HUMAN_COLS = [
    "6_naturalness_fluency (0-3)",
    "7_grammar_correctness (0-2)",
    "8_word_choice_accuracy (0-2)",
    "9_register_appropriateness (0-2)",
    "10_overall_usability (0-3)",
    "evaluator_notes",
]

KEEP_COLS = ["message_id", "query_en", "response_en", "romanized_query", "romanized_response"]

# ─── scoring functions ────────────────────────────────────────────────────────

def score_completeness(row) -> tuple[int, str]:
    resp = str(row.get("romanized_response", "") or "").strip()
    ref  = str(row.get("response_en", "") or "").strip()
    if not resp:
        return 0, "Empty response"
    resp_words = len(resp.split())
    ref_words  = len(ref.split()) if ref else 0
    if ref_words > 0 and resp_words < 0.25 * ref_words:
        return 1, f"Short: {resp_words} words vs {ref_words} in English ref"
    return 2, f"{resp_words} words"


def score_script_purity(row) -> tuple[int, str]:
    # Prefer pre-computed column; fall back to counting
    non_latin = row.get("response_non_latin_chars", None)
    if pd.isna(non_latin):
        resp = str(row.get("romanized_response", "") or "")
        non_latin = sum(1 for c in resp if c.isalpha() and ord(c) > 127)
    non_latin = int(non_latin)
    if non_latin == 0:
        return 2, "No native script chars"
    elif non_latin <= 10:
        return 1, f"{non_latin} non-Latin chars (word-level leakage)"
    else:
        return 0, f"{non_latin} non-Latin chars (sentence/paragraph in native script)"


def score_en_balance(row) -> tuple[int, str]:
    overlap = row.get("response_word_overlap", None)
    if pd.isna(overlap):
        resp = str(row.get("romanized_response", "") or "").lower().split()
        ref  = str(row.get("response_en", "") or "").lower().split()
        if not resp or not ref:
            return 0, "Empty"
        s1, s2 = set(resp), set(ref)
        overlap = len(s1 & s2) / len(s1 | s2) if s1 | s2 else 0
    overlap = float(overlap)
    if overlap < 0.30:
        return 3, f"Overlap={overlap:.2f} — well romanized"
    elif overlap < 0.50:
        return 2, f"Overlap={overlap:.2f} — slightly English-heavy"
    elif overlap < 0.70:
        return 1, f"Overlap={overlap:.2f} — too much English"
    else:
        return 0, f"Overlap={overlap:.2f} — barely romanized"


# Diacritic chars that appear in some romanization schemes
DIACRITIC_RE = re.compile(r'[āēīōūṁṇṭḍśṣḥÀ-öø-ÿ]', re.IGNORECASE)
# Vowel-length variation pairs to check
VOWEL_PAIRS = [
    (r'\baa\b', r'\ba\b'),   # aa vs a
    (r'\bee\b', r'\bi\b'),   # ee vs i
    (r'\boo\b', r'\bu\b'),   # oo vs u
]

def score_romanization_consistency(row) -> tuple[int, str]:
    resp = str(row.get("romanized_response", "") or "").strip()
    if not resp:
        return 0, "Empty — no scheme to evaluate"

    issues = []

    # 1. Mixed diacritics: has BOTH diacritic chars AND plain equivalents
    has_diacritics = bool(DIACRITIC_RE.search(resp))
    plain_vowels   = bool(re.search(r'[aeiou]', resp, re.IGNORECASE))
    if has_diacritics and plain_vowels:
        issues.append("mixed diacritics with plain vowels")

    # 2. Vowel-length inconsistency (aa and a both present for same root patterns)
    words = set(re.findall(r'\b[a-z]+\b', resp.lower()))
    for long_pat, short_pat in VOWEL_PAIRS:
        long_words  = {w for w in words if re.search(long_pat[2:-2], w)}
        short_words = {w for w in words if re.search(short_pat[2:-2], w) and not re.search(long_pat[2:-2], w)}
        # Check if same root word appears in both short and long form
        for lw in long_words:
            root = re.sub(r'aa|ee|oo', '', lw)
            if any(root in sw for sw in short_words if len(root) > 2):
                issues.append(f"vowel inconsistency: '{lw}'")
                break

    # 3. Repeated word with different case (mid-sentence capitalization chaos)
    tokens = re.findall(r'\b[a-zA-Z]{3,}\b', resp)
    lower_tokens = [t.lower() for t in tokens]
    seen = {}
    for orig, low in zip(tokens, lower_tokens):
        if low in seen and seen[low] != orig:
            issues.append(f"case inconsistency: '{seen[low]}' vs '{orig}'")
            break
        seen[low] = orig

    n = len(set(issues))  # deduplicate
    if n == 0:
        return 3, "No consistency issues detected"
    elif n == 1:
        return 2, f"Minor: {issues[0]}"
    elif n == 2:
        return 1, f"Multiple: {'; '.join(set(issues))}"
    else:
        return 0, f"Frequent: {'; '.join(set(issues))}"


def score_semantic_faithfulness(row) -> tuple[int, str]:
    resp = str(row.get("romanized_response", "") or "").strip()
    if not resp:
        return 0, "Empty response"
    bge = row.get("response_bge_cosine_similarity", None)
    if pd.isna(bge):
        return 1, "BGE score unavailable"
    bge = float(bge)
    if bge >= 0.85:
        return 3, f"BGE={bge:.3f}"
    elif bge >= 0.70:
        return 2, f"BGE={bge:.3f}"
    elif bge >= 0.50:
        return 1, f"BGE={bge:.3f}"
    else:
        return 0, f"BGE={bge:.3f} — low semantic match"


# ─── main ────────────────────────────────────────────────────────────────────

def process_file(model: str, language: str, scored_path: Path) -> pd.DataFrame:
    eval_path = EVAL_DIR / f"human_eval_{model}_{language}.csv"
    if not eval_path.exists():
        print(f"  [SKIP] {eval_path.name} not found")
        return None

    eval_df   = pd.read_csv(eval_path, low_memory=False)
    scored_df = pd.read_csv(scored_path, low_memory=False)

    # Filter scored_df to the 20 selected message_ids, preserving eval order
    selected_ids = eval_df["message_id"].tolist()
    scored_sub   = scored_df[scored_df["message_id"].isin(selected_ids)].copy()
    scored_sub   = scored_sub.set_index("message_id").reindex(selected_ids).reset_index()
    merged       = scored_sub

    # Score each row
    scores = {
        "1_response_completeness (0-2)": [],
        "1_notes": [],
        "2_script_purity (0-2)": [],
        "2_notes": [],
        "3_english_romanized_balance (0-3)": [],
        "3_notes": [],
        "4_romanization_consistency (0-3)": [],
        "4_notes": [],
        "5_semantic_faithfulness (0-3)": [],
        "5_notes": [],
    }
    for _, row in merged.iterrows():
        s1, n1 = score_completeness(row)
        s2, n2 = score_script_purity(row)
        s3, n3 = score_en_balance(row)
        s4, n4 = score_romanization_consistency(row)
        s5, n5 = score_semantic_faithfulness(row)
        scores["1_response_completeness (0-2)"].append(s1)
        scores["1_notes"].append(n1)
        scores["2_script_purity (0-2)"].append(s2)
        scores["2_notes"].append(n2)
        scores["3_english_romanized_balance (0-3)"].append(s3)
        scores["3_notes"].append(n3)
        scores["4_romanization_consistency (0-3)"].append(s4)
        scores["4_notes"].append(n4)
        scores["5_semantic_faithfulness (0-3)"].append(s5)
        scores["5_notes"].append(n5)

    # Build output dataframe
    out = pd.DataFrame()
    out["row_num"]  = range(1, len(merged) + 1)
    out["model"]    = model
    out["language"] = language
    out["message_id"]          = merged["message_id"].values
    out["query_en"]            = merged["query_en"].values if "query_en" in merged else ""
    out["response_en"]         = merged["response_en"].values if "response_en" in merged else ""
    out["romanized_query"]     = merged["romanized_query"].values if "romanized_query" in merged else ""
    out["romanized_response"]  = merged["romanized_response"].values if "romanized_response" in merged else ""

    # Auto-filled columns
    out["1_response_completeness (0-2)"]  = scores["1_response_completeness (0-2)"]
    out["1_auto_reason"]                  = scores["1_notes"]
    out["2_script_purity (0-2)"]          = scores["2_script_purity (0-2)"]
    out["2_auto_reason"]                  = scores["2_notes"]
    out["3_english_romanized_balance (0-3)"] = scores["3_english_romanized_balance (0-3)"]
    out["3_auto_reason"]                  = scores["3_notes"]
    out["4_romanization_consistency (0-3)"] = scores["4_romanization_consistency (0-3)"]
    out["4_auto_reason"]                  = scores["4_notes"]
    out["5_semantic_faithfulness (0-3)"]  = scores["5_semantic_faithfulness (0-3)"]
    out["5_auto_reason"]                  = scores["5_notes"]

    # Blank human columns
    for col in HUMAN_COLS:
        out[col] = ""

    return out


def main():
    all_outputs = {lang: [] for lang in ["hindi", "kannada", "telugu"]}

    for (model, language), scored_path in FILES.items():
        if not scored_path.exists():
            print(f"  [SKIP] {scored_path.name} not found")
            continue
        print(f"  Scoring {model:10} {language} ...", end=" ")
        result = process_file(model, language, scored_path)
        if result is None:
            continue
        out_path = EVAL_DIR / f"human_eval_{model}_{language}.csv"
        result.to_csv(out_path, index=False)
        avg_auto = result[["1_response_completeness (0-2)",
                            "2_script_purity (0-2)",
                            "3_english_romanized_balance (0-3)",
                            "4_romanization_consistency (0-3)",
                            "5_semantic_faithfulness (0-3)"]].mean()
        print(f"done  | avg auto scores: completeness={avg_auto.iloc[0]:.1f}  purity={avg_auto.iloc[1]:.1f}  balance={avg_auto.iloc[2]:.1f}  consistency={avg_auto.iloc[3]:.1f}  semantic={avg_auto.iloc[4]:.1f}")
        all_outputs[language].append(result)

    # Rebuild combined per-language files
    for lang, frames in all_outputs.items():
        if frames:
            combined = pd.concat(frames, ignore_index=True)
            combined["row_num"] = range(1, len(combined) + 1)
            combined_path = EVAL_DIR / f"human_eval_ALL_{lang}.csv"
            combined.to_csv(combined_path, index=False)
            print(f"\n  Combined → human_eval_ALL_{lang}.csv  ({len(combined)} rows, {len(combined.columns)} columns)")

    print(f"\nDone. Files in: {EVAL_DIR}")
    print("\nColumn guide:")
    print("  Columns 1-5 + *_auto_reason : pre-filled by script (Claude)")
    print("  Columns 6-10 + evaluator_notes : blank — fill these in")


if __name__ == "__main__":
    main()
