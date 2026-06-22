# Romanized Indic LLM Evaluation — Study & Scoring Summary

**Paper:** *The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them*
**Venue:** GenAI4World @ COLM 2026
**Contact:** Mahesh (Madhu Beesetty)

This document explains what the study is, how the evaluation rows were chosen, and the parameters used to rate each response. Read it before scoring your language file.

---

## 1. What we are doing and why

Hundreds of millions of Indians type their native language in **romanized script** — Hindi/Telugu/Kannada written with English letters (e.g., "namaste, kaise ho" instead of नमस्ते). We asked four LLMs to answer everyday questions in this romanized style and are evaluating how good the answers are.

The core claim of the paper is the **"invisible gap"**: standard automatic metrics (BGE-M3 cosine similarity, BERTScore) give *passing scores to outputs that a native speaker rejects*. A response can be returned entirely in English, or collapse into repeating one word, and still score near-perfect on a semantic metric — because those metrics measure meaning overlap, not whether the output is actually usable native-language text. The only reliable detector is a native speaker. This evaluation is how we show that gap with real numbers.

---

## 2. Data and models

- **Source prompts:** OASST2 (open-source human Q&A), ~142 question–answer pairs per language.
- **Languages:** Telugu, Kannada, Hindi.
- **Models (4):** `anthropic`, `gpt`, `gemini`, `ollama` (a local open-weights model).
- **Task given to each model:** take the English Q&A and produce the answer in romanized form of the target language.
- **Total pool:** ~142 responses × 4 models × 3 languages ≈ 1,700 responses.

Each response carries the English question (`query_en`) and English reference answer (`response_en`) for context, plus the model's `romanized_response` — **the thing being rated.**

---

## 3. How we picked the rows to evaluate

We did **not** sample randomly. We **purposively selected ~20 rows per language** (at least 3 per model, ~5 on average) chosen to surface the specific ways romanized output fails. This makes the set a **diagnostic set** — it is designed to expose metric blind spots and to give native speakers a manageable, high-signal workload.

The selection targets these categories:

| Category | What it captures |
|---|---|
| **Mode 1 — pure / mostly English** | Model returned the answer in English instead of the target language (metrics still score it high). |
| **Mode 2 — native-script leakage** | Romanized text with stray native-script characters mixed in (wrong script). |
| **Mode 3 — metric divergence** | Rows where BGE and BERTScore disagree (used where both metrics were available). |
| **Hard prompts** | Creative / emotional / roleplay prompts where quality is hard to auto-judge (plays, dialogues, stories). |
| **Good anchors** | Clean, high-quality responses, included as a baseline for comparison. |
| **English-task rows** | Prompts that *operate on English text* (OCR cleanup, "capitalize this", improve-my-email, CV, grammar-fix). English output here is arguably defensible, so these rows are **flagged separately** (`eng_task_flag`) for a later policy decision. |

**Important caveat for the paper:** because the 20 rows are selected *on* failure conditions, you **cannot** read an unbiased population failure rate off them ("X% of outputs fail"). They demonstrate that failures exist and that metrics miss them. For representative rates, we run a **separate scan over all ~142 responses per model** (see the failure catalog) — that is where the population-level numbers come from.

> Note: `ollama` was added with its own scored data later, so it also appears as a focused 5-per-language set. When the files are consolidated, ollama rows are de-duplicated into their language.

---

## 4. The parameters we use to rate each response

Each response is scored on **10 parameters, maximum 25 points**. Parameters 1–5 are **automatic / metric-derived**; parameters 6–10 are the **human judgment** (the part native-speaker reviewers fill in).

| # | Parameter | Scale | Filled by | What it measures |
|---|---|---|---|---|
| 1 | Response Completeness | 0–2 | Auto | Did the model fully answer (vs. empty / truncated)? |
| 2 | Script Purity | 0–2 | Auto | Native-script characters present? (0 chars = 2, 1–10 = 1, >10 = 0) |
| 3 | English–Romanized Balance | 0–3 | Auto | How much is genuine target language vs. verbatim English (from word-overlap). |
| 4 | Romanization Consistency | 0–3 | Auto | Consistent spelling/style; no script-mixing or stray diacritics. |
| 5 | Semantic Faithfulness | 0–3 | Auto | Does the meaning match the reference? (from BGE-M3: ≥0.85→3, ≥0.70→2, ≥0.50→1, else 0) |
| **6** | **Naturalness / Fluency** | **0–3** | **Human** | **Does it read like how a real person from your community would actually type?** |
| **7** | **Grammar Correctness** | **0–2** | **Human** | **Is the grammar correct (verb forms, postpositions, agreement)?** |
| **8** | **Word Choice Accuracy** | **0–2** | **Human** | **Right words used, or mistranslations / wrong-language words?** |
| **9** | **Register Appropriateness** | **0–2** | **Human** | **Is the tone/formality right (e.g., aap vs tu; casual vs formal)?** |
| **10** | **Overall Usability** | **0–3** | **Human** | **"Would I actually use this response as-is?" — your gut judgment.** |

**Max total = 25** (auto 2+2+3+3+3 = 13; human 3+2+2+2+3 = 12).

Rules of thumb baked into the rubric (full detail in `SCORING_GUIDE.md`):
- **Do not penalize English technical terms** (algorithm, Python, temperature) — code-mixing is natural.
- **Do not penalize valid spelling variants** (aadmi vs aadmee).
- **Native-script words that should have been romanized count against Word Choice (P8)** — a decision we adopted during the Kannada session: a stray native-script word costs roughly a point.
- **Register (P9) is the subtle one** — e.g., for the same play prompt one model nailed a casual, friend-like tone while another was "way too formal." Native ears catch this instantly; metrics and the LLM-judge tend not to.

---

## 5. Who assigns which scores

- **Parameters 1–5 (auto):** computed from BGE-M3, BERTScore, word-overlap, and native-character counts. Already filled; reviewers do not change them.
- **Parameters 6–10 (human):** **the native-speaker score — this is the ground truth the paper relies on.**
- **LLM-judge reference (Opus 4.8):** we also generated an independent model judgment across all 10 parameters, stored in the `llm1…llm10` columns. This is a *reference/proxy*, not ground truth. Comparing the human scores against it is itself a result (it tells us how far an LLM-judge can be trusted for this task — early signal: it tends to be a bit lenient on formal phrasing and misses register).

**Current workflow note:** to speed up review, the human columns (`H6…H10`) have been **pre-filled with the LLM-judge draft**. Reviewers **read each `romanized_response` and correct any value they disagree with.** (Cells already scored by a native speaker are preserved and not overwritten.) For the cleanest validation, score from your own judgment first and treat the pre-filled number only as a fallback.

---

## 6. What is in each evaluation file

Files: `FINAL_human_evaluation_telugu.csv`, `_kannada.csv`, `_hindi.csv` (and a consolidated `FINAL_LLM_judge_all_rows.csv`).

Column groups, left to right:
1. **Identity** — `row_num`, `model`, `language`, `message_id`
2. **Content** — `query_en`, `response_en`, `romanized_query`, `romanized_response` *(rate this)*
3. **Selection context** — `selection_category`, `eng_task_flag`
4. **HUMAN scores to fill** — `H6…H10` + `evaluator_notes` *(edit these)*
5. **Reference — auto / measured** — auto 1–5 and/or BGE, BERTScore, word-overlap, native-char counts
6. **Reference — LLM-judge** — `llm1…llm10` + `llm_notes` *(do not edit; kept for comparison)*

---

## 7. What we found so far (failure modes)

Two failure types, catalogued over the full ~142-response set (details in `FINAL_failure_summary.md`):

- **English-only output** — the answer comes back in English. 70 clear cases (word-overlap ≥ 0.90). **gpt: 0** (it always romanizes); anthropic 10 and gemini 9 (mostly defensible English-task rows); **ollama 51, of which ~41 are genuine failures.** These score ~1.0 on BGE/BERTScore yet are unusable as native-language answers.
- **Degeneration / repetition loops** — the model repeats one word or phrase for hundreds to thousands of tokens. **13 cases, every one ollama** (worst: the word "ellu" repeated 2,017× in a row). The automatic consistency check (P4) scores all of them a perfect 3 — fully blind to the failure.

These two findings are the empirical backbone of the "invisible gap" argument.

---

## 8. How to do your review (for evaluators)

1. Open your language file in Excel or Google Sheets.
2. For each row, read `query_en` (context) then `romanized_response` (rate this).
3. Set/correct the five human columns **H6, H7, H8, H9, H10**.
4. Add anything notable to `evaluator_notes` — especially good failure examples (e.g., "used a Telugu word in a Kannada response", "tone too formal for a casual question").
5. Leave columns 1–5 and the `llm…` columns unchanged.
6. Score every row; don't give all-3s or all-0s without reading.

Please return your completed file before **June 22, 2026**.
