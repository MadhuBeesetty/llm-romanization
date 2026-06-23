# Changes Made — Jun 23 Session

## 1. Model Name Fixes
- `gemini-2.0-flash` → `gemini-2.5-flash` (reproducibility.tex)
- `GPT-4o` → `GPT-5.5` everywhere: introduction.tex, method.tex, results.tex, discussion.tex, conclusion.tex, limitations.tex, reproducibility.tex
- `GPT-4o` → `GPT-5.5` in plot_metrics.py (MODELS list, all DATA dict keys, COLORS dict)

---

## 2. Abstract — Complete Rewrite
- Old abstract described only Ollama/Qwen3.5-35B (single model, wrong numbers)
- New abstract: 4-model study, correct findings (0.73–0.84 band, 1.43-point human gap, 0.004 BGE diff, Gemini/Ollama failure modes)
- Fixed "instead of [blank]" bug — removed Devanagari native-script example that pdfLaTeX couldn't render

---

## 3. LaTeX Preamble (colm2026_conference.tex)
- Added `\usepackage{fontspec}` and `\usepackage{polyglossia}` (were missing)
- Fixed typo: `\setdefauultlanguage` → `\setdefaultlanguage`
- Added missing font families: `\kannadafont`, `\tamilfont`, `\cyrillicfont`
- Switched to pdfLaTeX-compatible mode for Overleaf: replaced fontspec/polyglossia with `\usepackage[utf8]{inputenc}` and stub `\newcommand` font definitions
- Changed `[submission]` → `[final]` to show author names
- Added author block: 4x Madhu Sudhan Rao Beesetty (PayPal) with equal-contribution footnote

---

## 4. Native Script Font Wrapping (results.tex)
- Wrapped native script words with font commands:
  - `{\cyrillicfont\emph{единственный}}`
  - `{\telugufont\emph{అవును}}`
  - `{\tamilfont\emph{சாத்தியம்}}`
  - `{\hindifont\emph{मानना}}`

---

## 5. Bold Paragraph Label Cleanup (space saving)
- **results.tex**: Removed 8 `\noindent{\sffamily\bfseries...}\enspace` labels; integrated into prose
- **discussion.tex**: Converted 6 labels to `\paragraph{}`
- **method.tex**: Converted 3 labels to `\paragraph{}`

---

## 6. Introduction Cuts (space saving)
- Removed "At first glance, this task may appear..." paragraph
- Removed "Our initial experiments revealed..." paragraph
- Collapsed joint-generation rationale to 2 sentences
- Collapsed failure-aware policy explanation to 1 sentence + forward ref
- Compressed results-preview paragraph to 2 sentences
- Compressed contributions list from 5 bullets to 3

---

## 7. Related Work Compression (space saving)
- Reduced from 3 paragraphs to 2
- Removed 83%/73% prevalence stat (already in Introduction)
- Removed benchmark-gap content already covered in Introduction
- Target: ~150 words (was ~250)

---

## 8. Method Section
- Added `\label{sec:method}` to fix broken `??` cross-reference
- Removed metric-blindness preamble from `\paragraph{Human evaluation.}` (repeated in Results)
- Rewrote human evaluation paragraph:
  - Correctly describes humans scoring from scratch (not correcting LLM pre-fills)
  - LLM was calibration reference on a subset only
  - All scores are native-speaker judgments
  - All three languages (including Hindi) fully native-speaker evaluated
  - Improved category 2 and 6 descriptions (from Claude web suggestion)

---

## 9. Results Section
- Human evaluation framing tightened: removed re-explanation of methodology that belongs in Method
- Annotation procedure paragraph removed from Results (moved to Method)
- Fixed LLM judge comparison paragraph: reframed as a diagnostic finding, not a workflow step
- Summary table paragraph compressed: removed all numbers already stated in preceding paragraphs
- Cyrillic/cross-script sub-types paragraph compressed from ~15 lines to ~6 lines

---

## 10. Discussion Section
- Converted `\noindent{\sffamily\bfseries}` labels to `\paragraph{}`
- **Reordered paragraphs**: Output-token efficiency now comes before Naturalness (fixes Table 5 floating before naturalness text in PDF)
- Merged output-token prose with table — removed standalone paragraph that just re-stated the table caption
- Changed table placement from `[t]` to `[h]` to keep it adjacent to its text
- Removed "Gemini 0.630→0.82 counterfactual" sentence (already in Results §3.2)
- Removed "Implications for multilingual evaluation" paragraph (restated in Abstract + Conclusion)
- Removed "Query-type effects" paragraph (tangential to main thesis)
- Trimmed §Naturalness to qualitative examples only (removed Ollama quantitative re-statements)

---

## 11. Limitations Section
- §Automatic metrics: compressed from 8 lines to 2 sentences
- §Languages and models: Expanded to cover global romanization context:
  - Arabic (Arabizi), Urdu (Roman Urdu), Farsi (Finglish), Thai, Indonesian/Malay, Greek (Greeklish)
  - Notes the metric blind spot likely generalizes to all these communities

---

## 12. Conclusion Section
- Third finding compressed: removed detailed BGE score enumeration, replaced with one sentence highlighting the 1.43-point vs 0.004 contrast

---

## 13. Reproducibility (Appendix)
- Updated model IDs: `gpt-4o-2024-11-20` → `gpt-5.5`, `gemini-2.0-flash` → `gemini-2.5-flash`
- Removed "Hindi provisional" language — updated to reflect all three languages are native-speaker reviewed
- Removed "LLM-judge pre-fills" framing — updated to reflect correct workflow

---

## 14. Figures
- Merged two separate full-width figures (bge_cosine.pdf, bert_scores.pdf) into one side-by-side figure at 0.48\linewidth each
- Saves approximately 0.5 page

---

## 15. Data Corrections
- Ollama Kannada token count: 1,768 → **541** (excludes 49 degenerate rows that hit 4,096-token limit)
- Ollama Overall token count: 976 → **567**
- 73 rows → **72**, "~24 per language" → **24 per language** everywhere
- Hindi provisional caveat removed from: results.tex (×4), method.tex, reproducibility.tex
- English-only rates corrected: Telugu 14.7% → **11.3%**, Kannada 30.4% → **16.2%** (verified against actual scored CSVs)

---

## 16. Author Block (colm2026_conference.tex)
- Switched `[submission]` → `[final]` so author names show in compiled PDF
- Added 4 identical author entries (Madhu Sudhan Rao Beesetty, PayPal) as placeholders
- Teammates to replace their own entries in Overleaf before submission
- Email in `\small` font (not monospace) for cleaner layout
- Equal contribution footnote removed (not needed for identical placeholder entries)

---

## 17. Human Evaluation Framing Corrections
- Rewrote method.tex human eval paragraph: humans scored from scratch; LLM provided calibration reference on a subset only (not a full pre-fill)
- Removed all "LLM-judge draft" / "pre-filled scoring sheets" / "corrected any value they disagreed with" language
- All scores (all three languages) now correctly described as native-speaker judgments
- results.tex LLM-judge comparison reframed as a diagnostic finding, not a workflow step
- reproducibility.tex updated to match

---

## 18. Quality Review Fixes (final round)
- **limitations.tex**: "73 total" → "72 total" in Human evaluation coverage paragraph
- **results.tex**: Table 2 (tab:human-eval) caption — fixed garbled "Telugu and Kannada rows have native-speaker judgments across all three languages" fragment
- **results.tex**: Language ordering corrected — "Human scores follow the same language ordering" was wrong; Kannada (7.11) > Telugu (6.89) in human scores, reversing the auto-metric order
- **results.tex**: Awkward sentence fixed — "A direct test of why semantic metrics miss..." reworded
- **results.tex**: Table 1 caption now includes "repetition loop" as fourth failure type (was missing)
- **results.tex**: Clarifying note added — 13 degeneration instances (strict policy) vs 49 token-limit rows are different things, now explained
- **results.tex**: Failure table caption now explains why table count (39, strict word-overlap=1.0) differs from text count (70, ≥0.90 threshold)
- **introduction.tex**: Deleted 68-line commented-out old introduction block
- **introduction.tex**: Added model versions on first mention (Claude Opus~4.8, Gemini~2.5-flash)
- **method.tex**: "the qwen" → "Qwen3.5-35B"
- **discussion.tex**: Added closing synthesis sentence to avoid abrupt section ending
- **discussion.tex**: Output-token efficiency paragraph and table moved before Naturalness paragraph (fixes table floating above its text in PDF)

---

## 19. Figures — Regenerated and Separated
- Reran `plot_metrics.py` to regenerate both PDFs with correct **GPT-5.5** label (was showing "GPT 4o" from old figures)
- Split side-by-side layout back into **two separate full-width figures**:
  - `fig:bge-cosine` — BGE-M3 cosine similarity (queries + responses), full `\linewidth`
  - `fig:bert-scores` — BERTScore F1/Precision/Recall (queries + responses), full `\linewidth`, new label added
- Each figure now readable and properly labelled in the compiled PDF

---

## 20. Author Block Formatting
- Removed excess vertical spacing: affiliation and email now inline on same lines using `\small`
- Cleaner 2×2 grid layout in compiled PDF
- Placeholder entries (3×) ready for teammates to replace with their own details

---

## 21. Results Section — Further Compression
- **Human eval opening**: 5 sentences → 2 lines (removed BGE/BERTScore mechanics explanation, kept the key 0.733–0.837 band point)
- **LLM judge paragraph**: ~10 lines → 5 lines (kept MAD 4/12, 10.4 vs 3/12 example, forward ref; cut re-explanation of scoring)
- **English-only paragraph**: ~150 words → ~60 words (kept all key numbers, cut per-model breakdown prose)

---

## 22. Method, Limitations, Abstract — Further Compression
- **Method §Generation**: 3 paragraphs (~12 lines) → 1 paragraph (~3 lines); all content preserved
- **Limitations §Languages and models**: ~19 lines → ~4 lines; kept Arabizi/Roman Urdu/Finglish/Greeklish examples and metric blind spot generalization
- **Abstract**: Merged paragraphs 2 and 3 into one paragraph; saves ~3 lines

---

## 23. Quality Review Fixes
- **`\ref{sec:human-eval}`** label verified exists in results.tex — no fix needed
- **Figure prose reference** added: "Figure~\ref{fig:bge-cosine} visualizes..."
- **"English copy" → "English-only"** standardized everywhere (2 remaining instances fixed)
- **"native speakers readily identify"** varied: intro bullet → "consistently flag"; conclusion uses "readily detect"; limitations uses "readily observe"
- **Petrov double citation** — was already clean in current files; appeared only in old compiled PDF

---

## 24. Zip Files Created
- `jun23draft.zip` — latest version, ready for Overleaf upload
- Compile with **pdfLaTeX** (fontspec removed for compatibility)
- Switch to **XeLaTeX** after deadline for full native-script rendering
- Title confirmed: **"The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them"** (unchanged)
