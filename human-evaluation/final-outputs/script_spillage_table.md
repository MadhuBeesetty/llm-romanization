# Script Spillage Analysis — LLM Romanization Study

**Scope:** 4 models × 3 languages × 142 rows = 1,704 romanized responses  
**Exclusions applied:**
- `ç` in the *Plaça del Diamant* play row (Catalan source title, not a model error)
- Romanization diacritics (ā, ē, ī, ō, ū, ṭ, ḍ, ṣ, ṇ, ḷ, ṅ, ḻ etc.) — legitimate romanization convention
- Punctuation and non-alphabetic characters

---

## Summary Table

| Model | Language | Telugu | Kannada | Devanagari | Cyrillic (Russian) | Tamil | Malayalam |
|-------|----------|--------|---------|------------|-------------------|-------|-----------|
| Anthropic | Hindi | - | - | - | - | - | - |
| Anthropic | Telugu | 17 (2r) | - | - | **1 (1r)** | - | - |
| Anthropic | Kannada | - | - | 3 (2r) | **5 (3r)** | - | - |
| Gemini | Hindi | - | - | 45 (8r) | - | - | - |
| Gemini | Telugu | **2,635 (24r)** | - | 7 (2r) | **12 (1r)** | 4 (1r) | - |
| Gemini | Kannada | 6 (1r) | **46 (16r)** | - | - | - | 1 (1r) |
| GPT | Hindi | - | - | - | - | - | - |
| GPT | Telugu | - | - | - | - | - | - |
| GPT | Kannada | - | 21 (2r) | - | - | - | - |
| Ollama | Hindi | - | - | - | - | - | - |
| Ollama | Telugu | - | - | - | - | - | - |
| Ollama | Kannada | - | - | - | - | - | - |

*Format: total chars (rows affected). `-` = clean.*

---

## Key Findings

### 1. Gemini is the dominant offender
- **Gemini Telugu**: 2,635 native Telugu script characters across **24 of 142 rows (16.9%)** — entire paragraphs in native Telugu script instead of romanized Latin. Rows 46, 102, and 123 have 300–970 Telugu chars each.
- **Gemini Kannada**: 46 Kannada chars across 16 rows — consistent word-level leakage (e.g. `ಯಾವಾಗಲೂ`, `ಒತ್ತಿ ಹೇಳ`, `ಕಡಿಮೆ`).
- **Gemini Hindi**: 45 Devanagari chars across 8 rows — recurring phrase `मानना` ("believes/thinks") left in native script mid-romanized sentence.

### 2. Russian (Cyrillic) confirmed — not just Indian scripts
- **Gemini Telugu row 53, line 11**: Full Russian word `единственный` ("the only one") inserted mid-Telugu-romanized sentence.
- **Anthropic Kannada**: 5 Cyrillic chars across 3 rows (isolated character leaks, not full words).
- **Anthropic Telugu**: 1 Cyrillic char in 1 row.

### 3. Cross-language script confusion
- **Gemini Kannada row 33**: Telugu script (`అవును`) appearing in a Kannada-language response.
- **Gemini Telugu row 19**: Tamil script (`சாத்தியம்`) appearing alongside Telugu script in the same line — two wrong scripts simultaneously.
- **Gemini Telugu row 125**: Devanagari + Telugu script mixed in one line.

### 4. GPT and Ollama are largely clean
- GPT: Only 21 Kannada chars in 2 rows — minor word-level leakage.
- Ollama: Zero native-script spillage after exclusions.

---

## Implications for Automatic Metrics

Gemini Telugu's BGE-M3 cosine similarity score (mean = 0.771) was the lowest in the dataset,
yet 16.9% of its rows contain complete paragraphs in native Telugu script — a total failure
of the romanization task specification. The metric penalized this somewhat, but not enough
to flag it as a task failure. A native speaker evaluating these rows would reject them outright.
This is a direct, documented instance of the metric-human divergence central to this paper.

---

*Generated: 2026-06-22 | Files: script_spillage_linelog.csv (line-by-line), script_spillage_summary.csv (aggregates)*
