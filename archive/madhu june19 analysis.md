# Analysis — jun19romanoutputs

---

## 0. Why Romanized Languages Matter

Romanized script — typing a non-Latin language using the Latin alphabet — is not a niche behavior. It is the dominant way hundreds of millions of people interact with digital systems, including AI, because most keyboards default to QWERTY and native-script IMEs remain cumbersome on mobile.

### Global romanized script users (estimated)

| Language | Native script | Romanized variant | Native speakers | Est. romanized users | Primary region |
|----------|--------------|-------------------|-----------------|----------------------|----------------|
| Hindi | Devanagari | Hinglish | ~600M | ~500M | India |
| Bengali | Bengali | Banglish | ~230M | ~140M | India, Bangladesh |
| Marathi | Devanagari | Romanized Marathi | ~83M | ~55M | India |
| Telugu | Telugu | Romanized Telugu | ~85M | ~62M | India |
| Tamil | Tamil | Tanglish | ~80M | ~56M | India, Sri Lanka, Singapore |
| Kannada | Kannada | Romanized Kannada | ~45M | ~32M | India |
| Arabic | Arabic | Arabizi / Franco-Arabic | ~400M | ~120M | Middle East, North Africa |
| Persian | Persian | Finglish | ~80M | ~32M | Iran, diaspora |
| Greek | Greek | Greeklish | ~13M | ~5M | Greece, Cyprus |
| Russian | Cyrillic | Translit | ~150M | ~20M | Russia, diaspora |
| **Total** | | | **~1.77B** | **~1B+** | |

> **Note:** All romanized-user counts in the table above are rough approximations, not measured demographics, and should be treated as order-of-magnitude estimates only (derived from smartphone penetration, keyboard-adoption studies, and corpus analysis). The one set of figures here that is empirically grounded is the Hindi/Telugu romanization prevalence (83% and 73%), which comes from Khullar et al., "Script Gap" (arXiv:2512.10780, 2025). That paper measured the proportion of romanized vs. native-script inputs in a **real-world patient-messaging corpus** (de-identified WhatsApp maternal-health queries) — it is explicitly *not* a social-media measurement; the authors frame it as the first prevalence evidence beyond social media.

### Why this population is invisible to NLP benchmarks

1. **Standard datasets use native script.** XQuAD, IndicQA, MLQA — all use formal written script. No benchmark measures romanized input at scale.
2. **Language detectors misread romanized text as English.** Standard `langdetect` classifies "nenu chemistry student ni" (Telugu) as English. The data never gets labeled as Telugu.
3. **Tokenizers are not trained on romanized Indic.** A romanized Telugu word like "untundi" is tokenized as random English subwords with no learned semantic meaning.
4. **The population is large and growing.** India has 700M+ smartphone users. Most native-language digital communication happens in romanized form, not native script.

### How many people use romanized languages globally?

**Approximately 1 billion people** type their native language in Latin script — making it one of the largest underserved populations in NLP. (Order-of-magnitude estimate; see the caveat above.)

- **~850M from India alone** — India has 700M+ smartphone users, and the dominant input method for native languages on mobile is romanized Latin, not native script. Khullar et al. (arXiv:2512.10780) measured romanization prevalence at 83% for Hindi and 73% for Telugu in a real-world maternal-health messaging corpus.
- **~120M from the Arabic-speaking world** — Arabizi is the default for youth communication across Egypt, Saudi Arabia, UAE, and North Africa.
- **~50M from Persian, Greek, Russian** combined — Finglish, Greeklish, and Cyrillic translit add a smaller but meaningful global tail.

Even at half this estimate — **500 million people** — no major NLP benchmark measures how AI performs for this population. They are effectively invisible to standard evaluation.

**The gap:** models are benchmarked on a script that users don't type. This study measures what happens in the script they actually use.

> **Supporting evidence worth leaning on:** Khullar et al. (arXiv:2512.10780) is directly relevant beyond the prevalence figure. In a safety-critical setting (maternal/newborn triage over WhatsApp; ~133k conversations, stratified sample of ~3,153 messages), they find that romanized input degrades LLM triage performance by **up to 24 points** relative to native script, across multiple languages and models — independent external support for the motivation of this study.

---

**Task:** Each model (Anthropic, GPT, Gemini) was given 142 English OASST2 Q&A pairs and asked to translate + romanize both the query and response into Hindi, Telugu, and Kannada. The output is a parallel corpus of romanized translations — not model responses to romanized queries.  
**Reference:** `romanized_{lang}_split.csv` — a Claude Opus 4.8 translation+romanization of the same OASST2 pairs, used as the reference for BLEU/BERTScore.  
**Metrics:** BLEU (sacrebleu), BERTScore F1 (xlm-roberta-base, n=30), native-script leakage count, cross-lingual BERTScore (model romanized output vs OASST2 English GT), BGE-M3 cosine similarity (BAAI/bge-m3, full 142 rows, 2026-06-20).

> **Methodology notes (read before citing the metrics):**
> 1. **Specify every model/version.** The "anthropic" arm and the Opus 4.8 reference are both Claude-family. The exact model and snapshot for each of the three arms — and for the reference generator — must be stated. Using a Claude-generated reference to score a Claude arm is a conflict reviewers will flag. Mitigating fact from the data itself: there is **no self-preference** — GPT scores *higher* against the Claude reference than the Anthropic arm does (74.7 vs 60.7 on Hindi), the opposite of what bias would produce.
> 2. **Ship the reference file.** Without `romanized_{lang}_split.csv` the Section 1 BLEU column and all BERTScore values cannot be reproduced or checked (see the unverified flag below).
> 3. **BERTScore n=30.** The Section 1 BERTScore is computed on 30 of 142 examples; report n for the Section 4 cross-lingual scores too, and state whether `rescale_with_baseline` was used (raw F1 in the 0.90+ band is hard to interpret without it).

---

## 1. Main metrics table

> ⚠️ **Unverified:** The **BLEU** and **BERTScore F1** columns below could not be independently reproduced, because the reference file (`romanized_{lang}_split.csv`) was not available and the BERTScore encoder (xlm-roberta-base) could not be run in this environment. They are carried over from the original pipeline as-is. The **script-leakage** and **avg words/response** columns *were* independently recomputed from the raw output files and are corrected here.

| model | language | BLEU (unverified) | BERTScore F1 (unverified) | script leakage | avg words/response |
|-------|----------|------|--------------|----------------|--------------------|
| anthropic | hindi | 60.7 | 0.949 | 0 / 142 (0%) | 314 |
| gpt | hindi | 74.7 | 0.968 | 0 / 142 (0%) | 315 |
| gemini | hindi | 60.1 | 0.945 | 8 / 142 (5.6%) | 314 |
| anthropic | kannada | 38.1 | 0.908 | 1 / 142 (0.7%) | 247 |
| gpt | kannada | 53.3 | 0.928 | 2 / 142 (1.4%) | 250 |
| gemini | kannada | 36.8 | 0.902 | 16 / 141 (11.3%) | 249 |
| anthropic | telugu | 42.7 | 0.923 | 2 / 142 (1.4%) | 261 |
| gpt | telugu | 58.5 | 0.947 | 1 / 142 (0.7%) | 255 |
| gemini | telugu | 39.8 | 0.916 | 24 / 142 (16.9%) | 255 |

> **Denominator note:** Only the **Gemini Kannada** file is genuinely short one row (141 instead of 142 — message_id `4f64ca9b-c4b1-4ac1-a18f-298fd84353c9` is missing). All other files have the full 142 rows, so their leakage is reported out of 142. Two additional data-quality issues, both Gemini-only: the missing Kannada row, and one **empty** Gemini Telugu response.

---

## 2. Cross-model BLEU (no reference — model vs model)

These values were independently recomputed with sacrebleu from the actual output files and reproduce to within ~0.5 BLEU.

| pair | hindi | kannada | telugu |
|------|-------|---------|--------|
| anthropic vs gpt | 63.8 | 41.1 | 47.0 |
| anthropic vs gemini | 63.8 | 38.6 | 44.3 |
| gpt vs gemini | 62.1 | 39.2 | 43.8 |

---

## 3. Key findings

**Single-reference BLEU magnitude does not track quality.**  
Anthropic vs GT (60.7) is essentially equal to Anthropic vs GPT (63.8, independently verified): two models compared to each other score about the same as either one compared to the "ground truth." The reference is just one valid romanization among many, not a gold standard, so the absolute BLEU number cannot be read as a quality score. **Caveat — BLEU is not pure noise:** GPT vs GT (74.7) is ~11 points higher than GPT's cross-model BLEU (62–64), which means BLEU-against-the-reference does carry a signal — it tracks *stylistic proximity to that particular reference* (GPT's romanization style is closest to the Opus 4.8 reference), not quality. The accurate claim is therefore "single-reference BLEU conflates similarity-to-the-reference with quality," not "BLEU is uninterpretable."

**BLEU variation is driven by romanization diversity, not quality.**  
Hindi BLEU: 60–75. Kannada: 37–53. Telugu: 40–58. The cross-language gap reflects that Kannada/Telugu have more romanization spelling variation (e.g., "Howdu" vs "Haudu" vs "Avunu" for simple affirmations). Lower BLEU does not by itself mean worse output. (Note: within a single language, the across-model spread — e.g., Hindi GPT 74.7 vs Gemini 60.1 — is largely the reference-proximity effect described above, not a quality ranking.)

**BERTScore is flat across all models and languages, and its encoder is blind to the script.**  
Range: 0.902–0.968. Gemini Telugu — with ~17% native-script corruption — scores 0.916; Anthropic Telugu — near-zero corruption — scores 0.923. Difference: 0.007. Two reasons this metric cannot separate clean from corrupted romanized output: (a) it is computed on only n=30 examples, so a 0.007 gap is well inside the noise floor; and (b) xlm-roberta-base has essentially no meaningful representation for romanized Indic text (it was trained on native scripts), so its similarity scores sit in an uninformative high band regardless of corruption. BERTScore as configured here cannot be used to discriminate quality.

**Gemini has a real, measurable, statistically significant script-corruption problem.**  
Telugu: 24/142 responses (16.9%) contain native Telugu characters. Kannada: 16/141 (11.3%). Hindi: 8/142 (5.6%). Anthropic and GPT are at or below 1.4% everywhere.  
*Severity is not uniform:* of Gemini's 24 flagged Telugu responses, **3 are rendered entirely in native Telugu script** (a complete romanization failure), while the remaining ~21 are otherwise-clean romanizations with a single stray native-script word.  
Examples from Gemini Telugu word-level leaks: `"...vaadyamulalo <native> ..."`, `"...hybridization ane<native>..."`, `"...<native> undi..."`.  
This failure is automatable and statistically significant. Fisher's exact test, Gemini vs GPT on Telugu (24/142 vs 1/142): **p = 5.8 × 10⁻⁷**. Pooled across all three languages (Gemini 48/425 vs GPT 3/426): **p = 5.7 × 10⁻¹²**. BERTScore does not catch any of it.

---

## 4. Cross-lingual BERTScore (model romanized output vs OASST2 English GT)

Reference = original English GT response. Ceiling = the Claude Opus 4.8 reference romanization scored against the same English GT.

> ⚠️ **Unverified:** These BERTScore values could not be independently reproduced (encoder unavailable in this environment); they are carried over from the original pipeline. n for this table is unstated and should be reported.

| | hindi | telugu | kannada |
|---|---|---|---|
| GT romanized (ceiling) | 0.861 | 0.836 | 0.815 |
| anthropic | **0.874** | **0.853** | 0.810 |
| gpt | 0.866 | 0.839 | **0.821** |
| gemini | 0.865 | 0.831 | **0.813** |

Models score at or above the ceiling in most cases. The likely reason is that models retain English technical vocabulary in their romanized output (e.g. "algorithm", "O(n log n)"), which boosts cross-lingual similarity against the English GT, while a model that fully transliterates all content words into romanized Indic scores lower. So English retention appears to be a **contributing factor** that BERTScore rewards over authentic transliteration.

**This mechanism is partial, not absolute.** Checking English-loanword density against the scores: it holds for Hindi and Telugu (the Anthropic arm is the most English-heavy *and* scores highest on both), but it **reverses for Kannada**, where GPT has the lowest English density yet the highest cross-lingual score. English retention is therefore one driver among several, not the sole explanation. (Measurement caveat: cleanly quantifying "English content" inside romanized Latin-script text is genuinely hard, since romanized Indic and English share the alphabet; a proper test needs a romanized-vs-English token classifier rather than a loanword heuristic.)

Gemini Telugu is the only model-language pair that drops below its ceiling (0.831 vs 0.836), consistent with its ~17% native-script corruption.

---

## 5. BGE-M3 Semantic Similarity (English GT vs Romanized Model Response)

**Script:** `llm-romanization/bge_m3_eval.py` | **Model:** `BAAI/bge-m3` (dense embeddings, fp16) | **Date:** 2026-06-20  
**What it measures:** cosine similarity between the English reference response (`response_en`) and the model's actual romanized output (`romanized_response`), using a state-of-the-art multilingual embedding model that handles 100+ languages.  
**Why BGE-M3:** Unlike xlm-roberta-base (used in Section 4 BERTScore), BGE-M3 was explicitly trained for cross-lingual retrieval and has meaningful representations for romanized Indic text.

| model | language | n | mean cosine | std | min | max |
|-------|----------|---|-------------|-----|-----|-----|
| anthropic | hindi | 142 | **0.839** | 0.074 | 0.499 | 0.951 |
| anthropic | telugu | 142 | 0.813 | 0.065 | 0.571 | 0.940 |
| anthropic | kannada | 142 | 0.763 | 0.084 | 0.428 | 0.915 |
| gpt | hindi | 142 | 0.828 | 0.073 | 0.602 | 0.944 |
| gpt | telugu | 142 | 0.795 | 0.063 | 0.519 | 0.916 |
| gpt | kannada | 142 | 0.761 | 0.078 | 0.495 | 0.928 |
| gemini | hindi | 142 | 0.821 | 0.079 | 0.582 | 0.952 |
| gemini | telugu | 141 | 0.771 | 0.077 | 0.533 | 0.915 |
| gemini | kannada | 141 | 0.769 | 0.077 | 0.502 | 1.001 |

**Per-row scores:** `llm-romanization/bge_m3_results/{model}_{language}_bge_scores.csv`  
**Summary CSV:** `llm-romanization/bge_m3_results/summary.csv`

### Findings

**Kannada consistently scores lowest** across all three models (0.761–0.769) vs Hindi (0.821–0.839). This is consistent with Kannada showing the most romanization spelling variation and the highest script-leakage from Gemini.

**Hindi scores highest** for all models — likely because Hinglish has the most training-data coverage, so BGE-M3 has better representations for romanized Hindi.

**Models are clustered** within each language. The inter-model spread within a language is ~0.01–0.04, much smaller than the inter-language spread (~0.07). Language is a stronger predictor of score than model choice.

**The scores look superficially acceptable (0.76–0.84).** This is the key paper point: an automatic metric signals "decent quality" across all models and languages. This is the contrast point with the planned human evaluation — native speakers are expected to find failures that BGE-M3 cosine similarity cannot surface. The metric-blindness thesis holds even with a better cross-lingual embedder.

**Gemini Telugu drops noticeably** (0.771 vs Anthropic 0.813), consistent with its 17% native-script corruption. BGE-M3 is more sensitive to this than xlm-roberta-base BERTScore (0.007 gap there vs 0.042 gap here) — but still not sensitive enough to flag it as an obvious failure.

---

## 6. What this means for the paper

**Corrected framing:** This data measures how well each model translates English content into romanized Indic — not how models handle romanized input. The task is: given English Q&A, produce a fluent romanized Hindi/Telugu/Kannada version.

| claim | supported by this data? |
|-------|------------------------|
| Single-reference BLEU magnitude does not track romanized-translation quality | Yes — cross-model BLEU ≈ model-vs-GT BLEU; the reference is not a gold standard. (But BLEU-vs-reference does encode style-proximity: GPT-vs-GT is well above GPT's cross-model BLEU.) |
| BERTScore (xlm-roberta-base, n=30) cannot discriminate quality levels here | Yes — range 0.902–0.968, flat even across corrupted outputs; under-powered at n=30 and the encoder is script-blind |
| BERTScore rewards English-heavy output over authentic transliteration | Partially — holds for Hindi/Telugu, reverses for Kannada; contributing factor, not sole driver |
| Gemini has a distinct script-corruption failure vs Anthropic/GPT | Yes — 16.9% Telugu, 11.3% Kannada vs ≤1.4% for others; automatable; Fisher p = 5.7 × 10⁻¹² pooled |
| Models fail in ways native speakers would reject | Not yet — no human ratings collected |

---

## 7. What's still needed

- **Ship the reference file** (`romanized_{lang}_split.csv`) and **specify the exact model/version** of all three arms and the reference generator, so Section 1 and Section 4 become reproducible and the reference-circularity concern is resolved.
- **Human ratings on 20–30 responses** — score on fluency, register, semantic accuracy, script usability. Show human scores vary while BERTScore stays flat at 0.90+. That table is the core finding.
- **Report n and rescaling for all BERTScore tables**, and re-run the main BERTScore on the full 142 (not n=30) before drawing the "flat" conclusion.
- **Split the leakage metric** into whole-response failures vs single-word leaks (already done for Gemini Telugu: 3 full failures + ~21 word-level leaks); apply the same split to all cells.
- **A proper English-retention vs cross-lingual-BERTScore correlation** (romanized-vs-English token classifier), to put the Section 4 mechanism on firmer footing than a loanword heuristic.
- **Real user romanized prompts (arm C)** — current data is all synthetic. Arm C (real user input) is where quality failures are expected to be more pronounced, and where Khullar et al.'s 24-point degradation finding is most directly relevant.
