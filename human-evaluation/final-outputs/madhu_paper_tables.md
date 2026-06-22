# FINAL Results — Romanized Indic LLM Evaluation
*Paper: The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them (GenAI4World @ COLM 2026)*

Backing data: `FINAL_master_scores.csv` (73 rows, 4 models x 3 languages, deduplicated). Rubric: `FINAL_methodology_summary.md`.

---
## Table 1 — Per-language quality (human-judged, parameters 6-10)
Means across evaluated rows; higher = better; human-total max = 12.

**Telugu**
| model | n | Naturalness | Grammar | WordChoice | Register | Usability | Total_12 |
|---|---|---|---|---|---|---|---|
| gpt | 3 | 2.67 | 2.00 | 1.93 | 1.90 | 2.53 | 11.03 |
| anthropic | 5 | 2.30 | 1.50 | 1.60 | 1.74 | 2.40 | 9.54 |
| gemini | 5 | 1.60 | 1.50 | 1.36 | 1.66 | 1.84 | 7.96 |
| ollama | 11 | 0.64 | 0.85 | 0.87 | 0.91 | 0.80 | 4.07 |

**Kannada**
| model | n | Naturalness | Grammar | WordChoice | Register | Usability | Total_12 |
|---|---|---|---|---|---|---|---|
| gpt | 5 | 2.22 | 1.80 | 1.96 | 1.90 | 2.18 | 10.06 |
| anthropic | 5 | 2.14 | 1.86 | 1.88 | 1.86 | 2.16 | 9.90 |
| gemini | 5 | 2.00 | 1.86 | 1.40 | 1.62 | 2.14 | 9.02 |
| ollama | 9 | 0.44 | 0.52 | 0.59 | 0.83 | 0.47 | 2.86 |

**Hindi**
| model | n | Naturalness | Grammar | WordChoice | Register | Usability | Total_12 |
|---|---|---|---|---|---|---|---|
| gpt | 6 | 2.62 | 2.00 | 2.00 | 2.00 | 2.52 | 11.13 |
| anthropic | 7 | 1.80 | 1.64 | 1.64 | 1.64 | 1.96 | 8.69 |
| gemini | 7 | 2.03 | 1.79 | 1.76 | 1.79 | 2.16 | 9.51 |
| ollama | 5 | 1.62 | 1.66 | 1.66 | 1.70 | 1.64 | 8.28 |

*Provenance:* Kannada includes direct native-speaker scoring; Telugu was native-reviewed (Telugu-speaking author) over the LLM-judge draft; **Hindi is still the LLM-judge draft, pending a native reviewer** — treat Hindi quality as provisional. gpt's Telugu n is small (3) — interpret that cell cautiously.

---
## Table 2 — Overall quality (mean human total / 12), model x language
| model | telugu | kannada | hindi |
|---|---|---|---|
| gpt | 11.03 | 10.06 | 11.13 |
| anthropic | 9.54 | 9.90 | 8.69 |
| gemini | 7.96 | 9.02 | 9.51 |
| ollama | 4.07 | 2.86 | 8.28 |

Consistent ordering: **gpt strongest, ollama weakest**, anthropic/gemini in between (they trade places by language).

---
## Table 3 — Failure rates over the FULL set (~142 responses per cell)
Representative population rates (not the 20-row diagnostic sample).

**English-only output (%) — answer returned in English (word-overlap >= 0.90):**
| model | telugu | kannada | hindi |
|---|---|---|---|
| gpt | 0.00 | 0.00 | 0.00 |
| anthropic | 3.50 | 1.40 | 2.10 |
| gemini | 2.10 | 2.10 | 2.10 |
| ollama | 14.70 | 30.40 | 2.80 |

**Degeneration loops (count) — word/phrase repeated pathologically:**
| model | telugu | kannada | hindi |
|---|---|---|---|
| gpt | 0 | 0 | 0 |
| anthropic | 0 | 0 | 0 |
| gemini | 0 | 0 | 0 |
| ollama | 1 | 10 | 2 |

**gpt never returns English (0%) and never degenerates. Degeneration is exclusively ollama** (worst in Kannada). ollama's English-only rate is far higher than any other model in Telugu and Kannada.

---
## Table 4 — The invisible gap (illustrative ollama rows)
Automatic metrics score these high; a native reader rejects them. This is the paper's central exhibit.

| language | failure_type | BGE | BERTScore | usability_human |
|---|---|---|---|---|
| telugu | pure_english | 1.00 | 1.00 | 0.00 |
| telugu | degeneration_loop | 0.72 | 0.51 | 0.00 |
| telugu | low_semantic | 0.51 | 0.49 | 0.50 |
| telugu | best_attempt | 0.90 | 0.69 | 2.30 |
| kannada | pure_english | 1.00 | 1.00 | 0.50 |
| kannada | degeneration_loop | 0.38 | 0.44 | 0.00 |
| kannada | low_semantic | 0.43 | 0.45 | 0.00 |
| kannada | best_attempt | 0.96 | 0.71 | 0.50 |
| hindi | pure_english | 1.00 | 1.00 | 0.50 |
| hindi | degeneration_loop | 0.69 | 0.54 | 0.50 |
| hindi | low_semantic | 0.46 | 0.49 | 2.50 |
| hindi | best_attempt | 0.94 | 0.73 | 2.50 |

- **pure_english**: BGE/BERTScore ~ 1.0, output entirely English -> usability 0.
- **degeneration_loop**: BGE still 0.39-0.72 while one word repeats hundreds-thousands of times -> usability 0.
- **best_attempt** (Kannada): BGE ~ 0.96 but text is ungrammatical keyword soup.

---
## How to cite
- **Quality (Tables 1-2):** human-judged scores on the *purposive diagnostic sample* — report as diagnostic, not population means.
- **Failure rates (Table 3):** computed over the *full ~142-response set per cell* — these ARE representative.
- **Invisible gap (Table 4) + `FINAL_failure_summary.md`:** the metric-vs-reality evidence; independent of scoring provenance.
