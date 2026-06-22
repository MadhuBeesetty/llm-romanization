"""
Strategic Row Selector for Human Evaluation
============================================
Paper thesis: "Automatic metrics (BGE-M3, BERTScore) assign passing scores to LLM romanized
outputs that native speakers would reject — the failure is invisible."

Three failure modes to prove:
  Mode 1: Model returns pure English verbatim → BGE=1.000 (wrong language, perfect score)
  Mode 2: Model returns native script instead of romanized → BGE=0.80-0.84 (wrong script, passing score)
  Mode 3: BGE inflates quality (BGE=0.93, BERTScore=0.64 on same row — huge disagreement)

Selection targets per language (20 rows total, ≥3 per model):
  - 2-3 Mode 1 rows (BGE very high + pure English output)
  - 2-3 Mode 2 rows (native script detected, BGE passing)
  - 2-3 Mode 3 rows (BGE vs BERTScore huge divergence)
  - 4-5 Model-divergence rows (same prompt, one model ≥0.85, another <0.60)
  - 3-4 Hard prompt rows (emotional/narrative/roleplay)
  - 2-3 Good anchor rows (clean romanization, BGE>0.85)
"""

import pandas as pd
import numpy as np
import re
import os

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE_SCORED = "/Users/mbeesetty/Documents/AI-paper-research/sharing-llm-research/output"
BASE_BGE    = "/Users/mbeesetty/Documents/AI-paper-research/llm-romanization/bge_m3_results"
OUT_DIR     = "/Users/mbeesetty/Documents/AI-paper-research/sharing-llm-research/human_eval_files"

os.makedirs(OUT_DIR, exist_ok=True)

SCORED_FILES = {
    ("anthropic", "hindi"):   f"{BASE_SCORED}/anthropic_output/anthropic_romanized_hindi_scored.csv",
    ("anthropic", "kannada"): f"{BASE_SCORED}/anthropic_output/anthropic_romanized_kannada_scored.csv",
    ("anthropic", "telugu"):  f"{BASE_SCORED}/anthropic_output/anthropic_romanized_telugu_scored.csv",
    ("gpt",       "hindi"):   f"{BASE_SCORED}/gpt/gpt_romanized_hindi_scored.csv",
    ("gpt",       "kannada"): f"{BASE_SCORED}/gpt/gpt_romanized_kannada_scored.csv",
    ("gpt",       "telugu"):  f"{BASE_SCORED}/gpt/gpt_romanized_telugu_scored.csv",
    ("gemini",    "hindi"):   f"{BASE_SCORED}/gemini/gemini_romanized_hindi_scored.csv",
    ("gemini",    "kannada"): f"{BASE_SCORED}/gemini/gemini_romanized_kannada_scored.csv",
    ("gemini",    "telugu"):  f"{BASE_SCORED}/gemini/gemini_romanized_telugu_scored.csv",
    ("ollama",    "hindi"):   f"{BASE_SCORED}/ollama/ollama_romanized_hindi_split_scored.csv",
    ("ollama",    "kannada"): f"{BASE_SCORED}/ollama/ollama_romanized_kannada_improved_split_scored.csv",
    ("ollama",    "telugu"):  f"{BASE_SCORED}/ollama/ollama_romanized_telugu_split_scored.csv",
}

BGE_FILES = {
    ("anthropic", "hindi"):   f"{BASE_BGE}/anthropic_hindi_bge_scores.csv",
    ("anthropic", "kannada"): f"{BASE_BGE}/anthropic_kannada_bge_scores.csv",
    ("anthropic", "telugu"):  f"{BASE_BGE}/anthropic_telugu_bge_scores.csv",
    ("gpt",       "hindi"):   f"{BASE_BGE}/gpt_hindi_bge_scores.csv",
    ("gpt",       "kannada"): f"{BASE_BGE}/gpt_kannada_bge_scores.csv",
    ("gpt",       "telugu"):  f"{BASE_BGE}/gpt_telugu_bge_scores.csv",
    ("gemini",    "hindi"):   f"{BASE_BGE}/gemini_hindi_bge_scores.csv",
    ("gemini",    "kannada"): f"{BASE_BGE}/gemini_kannada_bge_scores.csv",
    ("gemini",    "telugu"):  f"{BASE_BGE}/gemini_telugu_bge_scores.csv",
    # Ollama not in BGE files — handled by using scored-CSV bge column
}

LANGUAGES = ["hindi", "kannada", "telugu"]
MODELS    = ["anthropic", "gpt", "gemini", "ollama"]

# Hard prompt keywords (emotional, narrative, roleplay, creative)
HARD_PROMPT_PATTERNS = [
    r"\bplay\b", r"\bdialogue\b", r"\bstory\b", r"\bnarrat", r"\bemotion",
    r"\bfeel", r"\bgrief\b", r"\bsorrow", r"\blove\b", r"\banger\b",
    r"\bpoem\b", r"\bsong\b", r"\blyric", r"\broleplay\b", r"\bcharacter\b",
    r"\bpretend\b", r"\bimagine\b", r"\bfiction", r"\bcreative",
    r"\bmonologue\b", r"\bscene\b", r"\bletter\b", r"\bdear\b",
    r"\bwrite a\b", r"\bcompose\b", r"\bcry\b", r"\bweep\b", r"\bheart\b",
]
HARD_PATTERN = re.compile("|".join(HARD_PROMPT_PATTERNS), re.IGNORECASE)

# Native script Unicode ranges (for Mode 2 detection)
DEVANAGARI_RANGE = (0x0900, 0x097F)   # Hindi
KANNADA_RANGE    = (0x0C80, 0x0CFF)
TELUGU_RANGE     = (0x0C00, 0x0C7F)

SCRIPT_RANGES = {
    "hindi":   [DEVANAGARI_RANGE],
    "kannada": [KANNADA_RANGE],
    "telugu":  [TELUGU_RANGE],
}

def has_native_script(text, lang):
    if not isinstance(text, str) or not text.strip():
        return False
    ranges = SCRIPT_RANGES.get(lang, [])
    for ch in text:
        cp = ord(ch)
        for lo, hi in ranges:
            if lo <= cp <= hi:
                return True
    return False

def count_native_chars(text, lang):
    if not isinstance(text, str):
        return 0
    ranges = SCRIPT_RANGES.get(lang, [])
    count = 0
    for ch in text:
        cp = ord(ch)
        for lo, hi in ranges:
            if lo <= cp <= hi:
                count += 1
    return count

def word_count(text):
    if not isinstance(text, str):
        return 0
    return len(text.split())

def is_mostly_english(text, romanized_response):
    """
    Mode 1 check: romanized_response looks like pure English (verbatim from English input).
    Heuristic: overlap between response_en and romanized_response is very high,
    AND romanized_response has almost no Indic script chars.
    """
    if not isinstance(text, str) or not isinstance(romanized_response, str):
        return False
    # Tokenize to words
    eng_words = set(w.lower().strip(".,!?;:\"'()") for w in text.split())
    rom_words = set(w.lower().strip(".,!?;:\"'()") for w in romanized_response.split())
    if not eng_words or not rom_words:
        return False
    overlap = len(eng_words & rom_words) / max(len(rom_words), 1)
    return overlap > 0.6

# ─────────────────────────────────────────────────────────────────────────────
# LOAD ALL DATA
# ─────────────────────────────────────────────────────────────────────────────

def load_all_data():
    """Load all 12 scored files and 9 BGE files, normalize columns, merge BGE."""
    dfs = []
    for (model, lang), path in SCORED_FILES.items():
        try:
            df = pd.read_csv(path, low_memory=False)
        except Exception as e:
            print(f"  WARNING: Could not load {path}: {e}")
            continue

        # Normalize model column (Ollama files have model as actual model name like qwen3.5:35b)
        # We label it with the provider key
        df["provider"] = model
        df["lang_key"] = lang

        # Ensure standard columns exist
        required = ["message_id", "response_bge_cosine_similarity",
                    "response_word_overlap", "response_non_latin_chars",
                    "response_bert_f1", "query_en", "response_en",
                    "romanized_query", "romanized_response"]
        for col in required:
            if col not in df.columns:
                df[col] = np.nan

        # Add BGE-M3 from separate file if available
        bge_key = (model, lang)
        if bge_key in BGE_FILES:
            try:
                bge_df = pd.read_csv(BGE_FILES[bge_key])
                bge_df = bge_df.rename(columns={"bge_m3_cosine": "bge_m3_score"})
                df = df.merge(bge_df[["message_id", "bge_m3_score"]], on="message_id", how="left")
            except Exception as e:
                print(f"  WARNING: Could not load BGE file for {model}/{lang}: {e}")
                df["bge_m3_score"] = df["response_bge_cosine_similarity"]
        else:
            # For Ollama, use the scored CSV bge score as best proxy
            df["bge_m3_score"] = df["response_bge_cosine_similarity"]

        dfs.append(df)

    if not dfs:
        raise RuntimeError("No data files could be loaded!")

    all_data = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(all_data)} total rows across all models/languages")
    return all_data

# ─────────────────────────────────────────────────────────────────────────────
# SCORING HELPERS (Parameters 1-5)
# ─────────────────────────────────────────────────────────────────────────────

def score_completeness(row):
    """1: Response Completeness (0-2)"""
    resp = row.get("romanized_response", "")
    ref  = row.get("response_en", "")
    if not isinstance(resp, str) or not resp.strip():
        return 0, "Empty romanized response"
    resp_wc = word_count(resp)
    ref_wc  = word_count(ref) if isinstance(ref, str) else 0
    if ref_wc > 0 and resp_wc < 0.25 * ref_wc:
        return 1, f"Short response: {resp_wc} words vs ref {ref_wc} words (<25%)"
    return 2, f"Complete: {resp_wc} words (ref ~{ref_wc})"

def score_script_purity(row, lang):
    """2: Script Purity (0-2) — 2=no native chars, 1=1-10, 0=>10"""
    resp = row.get("romanized_response", "")
    # Prefer pre-computed column if reliable
    native_count = row.get("response_non_latin_chars", None)
    if native_count is None or (isinstance(native_count, float) and np.isnan(native_count)):
        native_count = count_native_chars(resp, lang)
    else:
        native_count = int(native_count)
    if native_count == 0:
        return 2, "No native script characters detected"
    elif native_count <= 10:
        return 1, f"Minor native script leakage: {native_count} chars"
    else:
        return 0, f"Heavy native script presence: {native_count} chars"

def score_english_balance(row):
    """3: English-Romanized Balance (0-3): overlap<0.30→3, 0.30-0.50→2, 0.50-0.70→1, >0.70→0"""
    overlap = row.get("response_word_overlap", np.nan)
    if isinstance(overlap, float) and np.isnan(overlap):
        return 1, "Word overlap unknown"
    overlap = float(overlap)
    if overlap < 0.30:
        return 3, f"Good romanization mix: word overlap={overlap:.2f}"
    elif overlap < 0.50:
        return 2, f"Moderate English overlap: {overlap:.2f}"
    elif overlap < 0.70:
        return 1, f"High English overlap: {overlap:.2f}"
    else:
        return 0, f"Response appears verbatim English: overlap={overlap:.2f}"

def score_romanization_consistency(row, lang):
    """4: Romanization Consistency (0-3)"""
    resp = row.get("romanized_response", "")
    if not isinstance(resp, str) or not resp.strip():
        return 0, "No response to evaluate"

    issues = []
    # Check for diacritics mixed with plain vowels (e.g. "aa" vs "ā")
    has_macron    = bool(re.search(r"[āīūēōĀĪŪ]", resp))
    has_plain_aa  = bool(re.search(r"\baa\b|\bii\b|\buu\b", resp, re.IGNORECASE))
    if has_macron and has_plain_aa:
        issues.append("mixed diacritics+plain vowels")

    # Case variation in proper romanization contexts
    # (excessive ALL-CAPS words that aren't acronyms)
    caps_words = re.findall(r"\b[A-Z]{3,}\b", resp)
    real_caps  = [w for w in caps_words if w not in ("THE", "AND", "FOR", "WITH", "FROM")]
    if len(real_caps) > 3:
        issues.append(f"excessive caps: {real_caps[:3]}")

    # Mixed scripts check (native + latin in same sentence)
    if has_native_script(resp, lang):
        issues.append("mixed scripts")

    # Inconsistent spacing around punctuation
    if re.search(r"\w,\w", resp) and re.search(r"\w , \w", resp):
        issues.append("inconsistent punctuation spacing")

    if not issues:
        return 3, "Consistent romanization style"
    elif len(issues) == 1:
        return 2, f"Minor inconsistency: {issues[0]}"
    elif len(issues) == 2:
        return 1, f"Frequent inconsistencies: {'; '.join(issues)}"
    else:
        return 0, f"Severe inconsistencies: {'; '.join(issues)}"

def score_semantic_faithfulness(row):
    """5: Semantic Faithfulness (0-3): BGE≥0.85→3, 0.70-0.85→2, 0.50-0.70→1, <0.50→0"""
    bge = row.get("bge_m3_score", row.get("response_bge_cosine_similarity", np.nan))
    if isinstance(bge, float) and np.isnan(bge):
        bge_fallback = row.get("response_bge_cosine_similarity", np.nan)
        bge = bge_fallback
    if isinstance(bge, float) and np.isnan(bge):
        return 1, "BGE score unavailable"
    bge = float(bge)
    if bge >= 0.85:
        return 3, f"High semantic similarity: BGE={bge:.3f}"
    elif bge >= 0.70:
        return 2, f"Moderate semantic similarity: BGE={bge:.3f}"
    elif bge >= 0.50:
        return 1, f"Low semantic similarity: BGE={bge:.3f}"
    else:
        return 0, f"Very low semantic similarity: BGE={bge:.3f}"

def compute_auto_scores(row, lang):
    """Compute all 5 auto-fill scores. Returns dict."""
    c_score, c_reason   = score_completeness(row)
    sp_score, sp_reason = score_script_purity(row, lang)
    b_score, b_reason   = score_english_balance(row)
    r_score, r_reason   = score_romanization_consistency(row, lang)
    s_score, s_reason   = score_semantic_faithfulness(row)
    return {
        "1_response_completeness": c_score,
        "1_auto_reason": c_reason,
        "2_script_purity": sp_score,
        "2_auto_reason": sp_reason,
        "3_english_romanized_balance": b_score,
        "3_auto_reason": b_reason,
        "4_romanization_consistency": r_score,
        "4_auto_reason": r_reason,
        "5_semantic_faithfulness": s_score,
        "5_auto_reason": s_reason,
    }

# ─────────────────────────────────────────────────────────────────────────────
# FILTER: EXCLUDE BAD ROWS
# ─────────────────────────────────────────────────────────────────────────────

def is_valid_row(row):
    """Returns True if row passes all exclusion criteria."""
    resp = row.get("romanized_response", "")
    if not isinstance(resp, str) or not resp.strip():
        return False, "empty"
    wc = word_count(resp)
    if wc < 20:
        return False, f"too short ({wc} words)"
    # Garbled: very high ratio of non-alphanumeric chars
    non_alpha = len(re.findall(r"[^\w\s.,!?;:\"\'\(\)\-]", resp))
    if non_alpha > 0.3 * len(resp):
        return False, "garbled"
    return True, "ok"

# ─────────────────────────────────────────────────────────────────────────────
# DETECTION: FAILURE MODES
# ─────────────────────────────────────────────────────────────────────────────

def detect_mode1(row):
    """Mode 1: BGE very high + output is pure English verbatim."""
    bge = float(row.get("bge_m3_score", row.get("response_bge_cosine_similarity", 0)))
    overlap = float(row.get("response_word_overlap", 0))
    native = float(row.get("response_non_latin_chars", 0))
    # Criteria: BGE>=0.95, overlap>0.70 (mostly English words), minimal native chars
    if bge >= 0.95 and overlap >= 0.65 and native < 5:
        return True, f"Mode 1: BGE={bge:.3f} but output is pure English (overlap={overlap:.2f})"
    # Softer: BGE>=0.90, overlap>0.80
    if bge >= 0.90 and overlap >= 0.80:
        return True, f"Mode 1: BGE={bge:.3f} high but verbatim English (overlap={overlap:.2f})"
    return False, ""

def detect_mode2(row, lang):
    """Mode 2: Native script returned instead of romanized → BGE passing."""
    bge = float(row.get("bge_m3_score", row.get("response_bge_cosine_similarity", 0)))
    native = float(row.get("response_non_latin_chars", 0))
    resp = row.get("romanized_response", "")
    resp_len = len(resp) if isinstance(resp, str) else 0

    # Criteria: heavy native script presence AND passing BGE
    if native > 20 and bge >= 0.65:
        native_ratio = native / max(resp_len, 1)
        return True, f"Mode 2: {native:.0f} native script chars (ratio={native_ratio:.2f}), BGE={bge:.3f}"
    # Also check actual script detection
    if has_native_script(resp, lang) and count_native_chars(resp, lang) > 15 and bge >= 0.60:
        n = count_native_chars(resp, lang)
        return True, f"Mode 2: {n} native script chars detected, BGE={bge:.3f} (passing)"
    return False, ""

def detect_mode3(row):
    """Mode 3: BGE high but BERTScore F1 much lower (huge disagreement)."""
    bge = float(row.get("bge_m3_score", row.get("response_bge_cosine_similarity", np.nan)))
    bert_f1 = float(row.get("response_bert_f1", np.nan))
    if np.isnan(bge) or np.isnan(bert_f1):
        return False, ""
    gap = bge - bert_f1
    # Strong disagreement: BGE>0.85, BERTScore<0.70, gap>0.18
    if bge >= 0.85 and bert_f1 < 0.70 and gap >= 0.18:
        return True, f"Mode 3: BGE={bge:.3f} vs BERTScore={bert_f1:.3f} (gap={gap:.3f})"
    # Moderate disagreement
    if bge >= 0.80 and bert_f1 < 0.68 and gap >= 0.15:
        return True, f"Mode 3: BGE={bge:.3f} vs BERTScore={bert_f1:.3f} (gap={gap:.3f})"
    return False, ""

def is_hard_prompt(row):
    """Check if the English query matches hard prompt patterns."""
    q = row.get("query_en", "")
    if not isinstance(q, str):
        return False
    return bool(HARD_PATTERN.search(q))

# ─────────────────────────────────────────────────────────────────────────────
# DETECTION: MODEL DIVERGENCE
# ─────────────────────────────────────────────────────────────────────────────

def find_divergent_prompts(lang_df):
    """
    For each message_id, check if any model scores ≥0.85 while another scores <0.60.
    Returns: dict of message_id → (max_model, max_bge, min_model, min_bge, reason_str)
    """
    divergent = {}
    grouped = lang_df.groupby("message_id")

    for mid, grp in grouped:
        if len(grp) < 2:
            continue
        bge_by_model = {}
        for _, row in grp.iterrows():
            bge = float(row.get("bge_m3_score", row.get("response_bge_cosine_similarity", np.nan)))
            if not np.isnan(bge):
                bge_by_model[row["provider"]] = bge

        if len(bge_by_model) < 2:
            continue

        max_model = max(bge_by_model, key=bge_by_model.get)
        min_model = min(bge_by_model, key=bge_by_model.get)
        max_bge   = bge_by_model[max_model]
        min_bge   = bge_by_model[min_model]

        if max_bge >= 0.85 and min_bge < 0.60:
            reason = (f"Model divergence: {max_model}={max_bge:.3f} vs "
                      f"{min_model}={min_bge:.3f} (same prompt)")
            divergent[mid] = (max_model, max_bge, min_model, min_bge, reason)
        elif max_bge - min_bge >= 0.28:
            # Softer threshold for more coverage
            reason = (f"Model divergence: {max_model}={max_bge:.3f} vs "
                      f"{min_model}={min_bge:.3f} (gap={max_bge-min_bge:.3f})")
            divergent[mid] = (max_model, max_bge, min_model, min_bge, reason)

    return divergent

# ─────────────────────────────────────────────────────────────────────────────
# MAIN SELECTION LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def select_for_language(lang, all_data, target_n=20, min_per_model=3):
    """
    Select 20 rows for the given language, across all 4 models.
    Returns: DataFrame with exactly 20 rows + metadata columns.
    """
    print(f"\n{'='*60}")
    print(f"  SELECTING FOR: {lang.upper()}")
    print(f"{'='*60}")

    # Filter to this language
    lang_df = all_data[all_data["lang_key"] == lang].copy()
    print(f"  Total rows available: {len(lang_df)}")

    # Exclude invalid rows
    valid_mask = []
    for _, row in lang_df.iterrows():
        ok, _ = is_valid_row(row)
        valid_mask.append(ok)
    lang_df = lang_df[valid_mask].copy()
    print(f"  Valid rows after filtering: {len(lang_df)}")

    if len(lang_df) == 0:
        print("  ERROR: No valid rows!")
        return pd.DataFrame()

    # Tag each row with detected properties
    lang_df["_mode1"]         = False
    lang_df["_mode1_reason"]  = ""
    lang_df["_mode2"]         = False
    lang_df["_mode2_reason"]  = ""
    lang_df["_mode3"]         = False
    lang_df["_mode3_reason"]  = ""
    lang_df["_hard_prompt"]   = False
    lang_df["_is_good"]       = False
    lang_df["_bge"]           = lang_df["bge_m3_score"].fillna(
                                    lang_df["response_bge_cosine_similarity"].fillna(0)
                                 ).astype(float)

    for idx, row in lang_df.iterrows():
        m1, m1r = detect_mode1(row)
        m2, m2r = detect_mode2(row, lang)
        m3, m3r = detect_mode3(row)
        hp       = is_hard_prompt(row)
        bge      = float(row["_bge"])
        good     = (bge >= 0.85 and not m1 and not m2 and not m3
                    and float(row.get("response_non_latin_chars", 0)) < 5
                    and float(row.get("response_word_overlap", 1)) < 0.50)

        lang_df.at[idx, "_mode1"]        = m1
        lang_df.at[idx, "_mode1_reason"] = m1r
        lang_df.at[idx, "_mode2"]        = m2
        lang_df.at[idx, "_mode2_reason"] = m2r
        lang_df.at[idx, "_mode3"]        = m3
        lang_df.at[idx, "_mode3_reason"] = m3r
        lang_df.at[idx, "_hard_prompt"]  = hp
        lang_df.at[idx, "_is_good"]      = good

    # Find divergent prompts
    divergent = find_divergent_prompts(lang_df)
    lang_df["_divergent"]        = lang_df["message_id"].isin(divergent.keys())
    lang_df["_divergent_reason"] = lang_df["message_id"].map(
        lambda mid: divergent[mid][4] if mid in divergent else ""
    )

    print(f"  Mode 1 rows: {lang_df['_mode1'].sum()}")
    print(f"  Mode 2 rows: {lang_df['_mode2'].sum()}")
    print(f"  Mode 3 rows: {lang_df['_mode3'].sum()}")
    print(f"  Hard prompt rows: {lang_df['_hard_prompt'].sum()}")
    print(f"  Divergent prompt rows: {lang_df['_divergent'].sum()}")
    print(f"  Good anchor rows: {lang_df['_is_good'].sum()}")

    # ── Selection algorithm ──────────────────────────────────────────────────
    selected_indices = set()
    selection_reasons = {}

    def add_rows(candidates, reason_template, max_n, prefer_diverse_models=True):
        """Add up to max_n rows from candidates DataFrame."""
        added = 0
        if prefer_diverse_models:
            # Round-robin across models
            by_model = {m: [] for m in MODELS}
            for idx, row in candidates.iterrows():
                by_model[row["provider"]].append(idx)
            model_queues = {m: iter(idxs) for m, idxs in by_model.items() if idxs}
            exhausted = set()
            while added < max_n and len(exhausted) < len(model_queues):
                for m, q in list(model_queues.items()):
                    if m in exhausted:
                        continue
                    try:
                        idx = next(q)
                        if idx not in selected_indices:
                            selected_indices.add(idx)
                            row = candidates.loc[idx]
                            # Build reason
                            if reason_template == "auto":
                                for col in ["_mode1_reason", "_mode2_reason",
                                            "_mode3_reason", "_divergent_reason"]:
                                    if row.get(col, ""):
                                        selection_reasons[idx] = row[col]
                                        break
                                else:
                                    selection_reasons[idx] = "Hard/narrative prompt"
                            else:
                                selection_reasons[idx] = reason_template
                            added += 1
                            if added >= max_n:
                                break
                    except StopIteration:
                        exhausted.add(m)
        else:
            for idx, row in candidates.iterrows():
                if added >= max_n:
                    break
                if idx not in selected_indices:
                    selected_indices.add(idx)
                    selection_reasons[idx] = reason_template
                    added += 1
        return added

    # 1. Mode 1: Pure English outputs with inflated BGE
    mode1_cands = lang_df[lang_df["_mode1"]].sort_values("_bge", ascending=False)
    n1 = add_rows(mode1_cands, "auto", max_n=3)
    print(f"  Selected Mode 1: {n1}")

    # 2. Mode 2: Native script instead of romanized
    mode2_cands = lang_df[lang_df["_mode2"] & ~lang_df.index.isin(selected_indices)].sort_values(
        "response_non_latin_chars", ascending=False)
    n2 = add_rows(mode2_cands, "auto", max_n=3)
    print(f"  Selected Mode 2: {n2}")

    # 3. Mode 3: BGE vs BERTScore divergence
    mode3_cands = lang_df[lang_df["_mode3"] & ~lang_df.index.isin(selected_indices)].copy()
    mode3_cands["_gap"] = mode3_cands["_bge"] - mode3_cands["response_bert_f1"].astype(float)
    mode3_cands = mode3_cands.sort_values("_gap", ascending=False)
    n3 = add_rows(mode3_cands, "auto", max_n=3)
    print(f"  Selected Mode 3: {n3}")

    # 4. Model-divergence rows (choose the LOWER-scoring model's row for human eval—
    #    evaluator sees the failing model's output alongside the metric saying it's "ok")
    div_cands = lang_df[lang_df["_divergent"] & ~lang_df.index.isin(selected_indices)].copy()
    # Prefer the row where BGE is high but human would disagree — pick rows where
    # the provider's row is the HIGH scorer (BGE >= 0.75) to show metric complacency
    div_cands = div_cands.sort_values("_bge", ascending=False)
    # Try to get diverse message_ids (don't select both models for same prompt)
    seen_mids = set()
    div_filtered = []
    for idx, row in div_cands.iterrows():
        mid = row["message_id"]
        if mid not in seen_mids:
            seen_mids.add(mid)
            div_filtered.append(idx)
    div_filtered_df = div_cands.loc[div_filtered]
    n4 = add_rows(div_filtered_df, "auto", max_n=5)
    print(f"  Selected Divergent: {n4}")

    # 5. Hard prompt rows (emotional/narrative/roleplay) not already selected
    hard_cands = lang_df[lang_df["_hard_prompt"] & ~lang_df.index.isin(selected_indices)].copy()
    # Among hard prompts, prioritize ones where BGE>0.75 (metrics look fine but hard to evaluate)
    hard_cands = hard_cands.sort_values("_bge", ascending=False)
    n5 = add_rows(hard_cands, "Hard/narrative/roleplay prompt — evaluator judgment needed", max_n=4)
    print(f"  Selected Hard prompts: {n5}")

    # 6. Good anchors (BGE>0.85, clean output)
    good_cands = lang_df[lang_df["_is_good"] & ~lang_df.index.isin(selected_indices)].copy()
    good_cands = good_cands.sort_values("_bge", ascending=False)
    # Add good anchor rows manually to control labeling
    n6 = 0
    models_covered = {}
    for idx, row in good_cands.iterrows():
        if n6 >= 3:
            break
        if idx not in selected_indices:
            bge_val = float(row["_bge"])
            selected_indices.add(idx)
            selection_reasons[idx] = f"Good anchor: clean romanization BGE={bge_val:.3f}"
            n6 += 1
    print(f"  Selected Good anchors: {n6}")

    # 7. Fill remaining slots to reach target_n
    current_n = len(selected_indices)
    remaining = target_n - current_n
    print(f"  Current count: {current_n}, need {remaining} more")

    if remaining > 0:
        # Fill with high BGE rows where metrics look good but haven't been selected
        fill_cands = lang_df[~lang_df.index.isin(selected_indices)].copy()
        # Prioritize invisible failures: high BGE but some suspicious property
        fill_cands["_priority"] = (
            fill_cands["_bge"].astype(float) * 0.5
            + fill_cands["_hard_prompt"].astype(float) * 0.3
            + (1 - fill_cands["response_word_overlap"].fillna(0.5).astype(float)) * 0.2
        )
        fill_cands = fill_cands.sort_values("_priority", ascending=False)
        n7 = add_rows(fill_cands, "High-BGE row for evaluator baseline", max_n=remaining)
        print(f"  Selected fill: {n7}")

    # ── Enforce min_per_model ────────────────────────────────────────────────
    model_counts = {}
    for idx in selected_indices:
        m = lang_df.at[idx, "provider"]
        model_counts[m] = model_counts.get(m, 0) + 1

    print(f"  Model distribution before enforcement: {model_counts}")

    for model in MODELS:
        count = model_counts.get(model, 0)
        if count < min_per_model:
            needed = min_per_model - count
            model_pool = lang_df[
                (lang_df["provider"] == model) &
                (~lang_df.index.isin(selected_indices))
            ].sort_values("_bge", ascending=False)

            added = 0
            for idx, row in model_pool.iterrows():
                if added >= needed:
                    break
                # Remove lowest-priority existing row if we're over target
                if len(selected_indices) >= target_n:
                    # Find an existing row from an over-represented model to swap
                    over_models = [m for m, c in model_counts.items() if c > min_per_model + 1]
                    if not over_models:
                        # Can't swap without violating other model minimums, just add
                        pass
                    else:
                        # Swap: remove a fill row from an over-represented model
                        swap_model = over_models[0]
                        # Find fill rows from that model
                        swap_pool = [
                            i for i in selected_indices
                            if lang_df.at[i, "provider"] == swap_model
                            and "fill" in selection_reasons.get(i, "").lower()
                        ]
                        if swap_pool:
                            remove_idx = swap_pool[0]
                            selected_indices.discard(remove_idx)
                            del selection_reasons[remove_idx]
                            model_counts[swap_model] = model_counts.get(swap_model, 0) - 1

                selected_indices.add(idx)
                bge_val = float(row["_bge"])
                selection_reasons[idx] = f"Min-model coverage: {model} row (BGE={bge_val:.3f})"
                model_counts[model] = model_counts.get(model, 0) + 1
                added += 1
            print(f"  Added {added} rows for under-represented model: {model}")

    # ── Final trim to exactly target_n ──────────────────────────────────────
    if len(selected_indices) > target_n:
        # Remove lowest-priority extras (prefer keeping failure modes and diverse models)
        priority_order = []
        for idx in selected_indices:
            row = lang_df.loc[idx]
            reason = selection_reasons.get(idx, "")
            score = 0
            if "Mode 1" in reason: score = 100
            elif "Mode 2" in reason: score = 95
            elif "Mode 3" in reason: score = 90
            elif "divergence" in reason.lower(): score = 85
            elif "Hard" in reason: score = 80
            elif "Good anchor" in reason: score = 75
            elif "Min-model" in reason: score = 70
            else: score = 50 + float(row["_bge"]) * 10
            priority_order.append((score, idx))

        priority_order.sort(reverse=True)
        selected_indices = set(idx for _, idx in priority_order[:target_n])
        # Rebuild reasons for kept rows
        selection_reasons = {idx: v for idx, v in selection_reasons.items()
                             if idx in selected_indices}

    # ── Fix good anchor labels (ensure clean strings) ───────────────────────
    for idx in selected_indices:
        reason = selection_reasons.get(idx, "")
        if not isinstance(reason, str):
            bge_val = lang_df.at[idx, "_bge"]
            selection_reasons[idx] = f"Good anchor: clean romanization BGE={bge_val:.3f}"

    # ── Build output DataFrame ───────────────────────────────────────────────
    rows_out = []
    for row_num, idx in enumerate(sorted(selected_indices), start=1):
        row = lang_df.loc[idx]
        lang_name = lang.capitalize()

        auto_scores = compute_auto_scores(row, lang)
        sel_reason  = selection_reasons.get(idx, "Selected row")

        # Build the output record
        record = {
            "row_num":  row_num,
            "model":    row.get("provider", "unknown"),
            "language": lang_name,
            "message_id": row.get("message_id", ""),

            "query_en":          row.get("query_en", ""),
            "response_en":       row.get("response_en", ""),
            "romanized_query":   row.get("romanized_query", ""),
            "romanized_response": row.get("romanized_response", ""),

            "response_bge_cosine_similarity": round(float(row.get("bge_m3_score",
                                                   row.get("response_bge_cosine_similarity", 0))), 4),
            "response_word_overlap":          round(float(row.get("response_word_overlap", 0)), 4),
            "response_non_latin_chars":       int(row.get("response_non_latin_chars", 0)),

            "selection_reason": sel_reason,
        }
        record.update(auto_scores)
        record.update({
            "6_naturalness_fluency":      "",
            "7_grammar_correctness":      "",
            "8_word_choice_accuracy":     "",
            "9_register_appropriateness": "",
            "10_overall_usability":       "",
            "evaluator_notes":            "",
        })
        rows_out.append(record)

    out_df = pd.DataFrame(rows_out)

    # Final model counts
    final_model_counts = out_df["model"].value_counts().to_dict()
    print(f"\n  FINAL MODEL DISTRIBUTION: {final_model_counts}")
    print(f"  FINAL COUNT: {len(out_df)}")

    return out_df

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading all data...")
    all_data = load_all_data()

    all_selections = {}

    for lang in LANGUAGES:
        selection = select_for_language(lang, all_data, target_n=20, min_per_model=3)
        if len(selection) == 0:
            print(f"ERROR: No rows selected for {lang}!")
            continue
        all_selections[lang] = selection

        out_path = f"{OUT_DIR}/strategic_human_eval_{lang}.csv"
        selection.to_csv(out_path, index=False)
        print(f"\n  Written: {out_path}")

    # ─── FINAL SUMMARY ───────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("  FINAL SUMMARY")
    print("="*70)

    for lang, df in all_selections.items():
        print(f"\n{'─'*50}")
        print(f"  Language: {lang.upper()} ({len(df)} rows)")
        print(f"{'─'*50}")

        # Rows per model
        print("  Rows per model:")
        for model, cnt in df["model"].value_counts().items():
            print(f"    {model:12s}: {cnt}")

        # Rows per selection_reason category
        print("  Selection reason categories:")
        cats = {}
        for reason in df["selection_reason"]:
            if "Mode 1" in reason:
                cat = "Mode 1 (pure English)"
            elif "Mode 2" in reason:
                cat = "Mode 2 (native script)"
            elif "Mode 3" in reason:
                cat = "Mode 3 (BGE vs BERT divergence)"
            elif "divergence" in reason.lower():
                cat = "Model divergence"
            elif "Hard" in reason or "narrative" in reason or "roleplay" in reason:
                cat = "Hard/narrative prompt"
            elif "Good anchor" in reason:
                cat = "Good anchor"
            elif "Min-model" in reason:
                cat = "Min-model coverage"
            else:
                cat = "Baseline fill"
            cats[cat] = cats.get(cat, 0) + 1
        for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"    {cat:40s}: {cnt}")

        # BGE distribution
        bge_vals = df["response_bge_cosine_similarity"].dropna()
        print(f"  BGE distribution:")
        print(f"    min={bge_vals.min():.3f}, mean={bge_vals.mean():.3f}, max={bge_vals.max():.3f}")
        print(f"    rows BGE>=0.85: {(bge_vals>=0.85).sum()}")
        print(f"    rows BGE 0.70-0.85: {((bge_vals>=0.70)&(bge_vals<0.85)).sum()}")
        print(f"    rows BGE<0.70: {(bge_vals<0.70).sum()}")

        # Auto score distributions
        print("  Auto score distributions:")
        for col in ["1_response_completeness", "2_script_purity",
                    "3_english_romanized_balance", "4_romanization_consistency",
                    "5_semantic_faithfulness"]:
            vals = df[col].value_counts().sort_index().to_dict()
            print(f"    {col}: {vals}")

    print("\n" + "="*70)
    print("  Output files written to:")
    for lang in all_selections:
        print(f"    {OUT_DIR}/strategic_human_eval_{lang}.csv")
    print("="*70)

if __name__ == "__main__":
    main()
