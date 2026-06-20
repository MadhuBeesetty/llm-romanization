# GenAI4World Research Paper — Day 1 Meeting Summary
**Date:** May 30, 2026
**Workshop Target:** GenAI4World @ COLM 2026, San Francisco
**Workshop URL:** https://sites.google.com/view/genai4world/home
**Team:** Indian students — Telugu and Hindi native speakers

---

## Agenda for Tomorrow's Meeting

1. Review all 6 research topics
2. Review deep research done on Topic 2
3. Discuss which topic best fits our team's strengths
4. Assign tasks based on chosen topic
5. Agree on timeline and next steps

---

## About the Workshop

GenAI4World is the **first workshop on Globalizing Tasks, Evaluations, and Systems**, co-located with COLM 2026 in San Francisco. The workshop's central theme is:

> *"Globalization, not localization — not merely adapting systems to fit diverse contexts, but allowing global diversity to shape how they are built from the ground up."*

The workshop explicitly calls out **code-switching** as an open problem and welcomes empirical papers that expose real-world failures in current AI systems.

---

## Our Key Asset

We have direct access to **Telugu and Hindi native speakers** — this is rare and powerful for this workshop. Telugu alone has 80M+ speakers and is one of the most underrepresented languages in NLP research. Combined with Hindi (600M+ speakers), we have a compelling case study that covers a massive real-world population.

---

## The 6 Research Topics

### Topic 1 — Globalizing Tasks
**Core question:** Which NLP tasks are culturally inappropriate or absent for non-Western users?

Most NLP tasks (sentiment analysis, question answering, summarization) were designed around English and Western assumptions. Simply translating them into Telugu or Hindi doesn't fix the cultural misalignment — the task itself may be wrong.

**Example:** Indirect speech acts are culturally normal in Telugu. A model trained to flag "unhelpful" responses would incorrectly penalize culturally appropriate indirect communication.

**Our opportunity:** Audit 3-4 standard NLP tasks for cultural misalignment in Telugu/Hindi. Show tasks are not just missing but actively wrong.

**Difficulty:** Medium
**Paper type:** Empirical audit

---

### Topic 2 — Evaluation Beyond Performance ⭐ MOST RESEARCHED
**Core question:** What do standard metrics miss for Telugu and Hindi speakers?

Standard metrics (accuracy, F1, BLEU) give models a "pass" — but real Indian users code-switch, write in Romanized script, and use colloquial language that no benchmark measures.

#### The 3-Paper Narrative We Built

**Paper 1 — Petrov et al. (NeurIPS 2023)**
*"Language Model Tokenizers Introduce Unfairness Between Languages"*

- Proves tokenization discriminates against non-English languages BEFORE the model even runs
- Same sentence = dramatically more tokens in Telugu/Hindi vs English
- Telugu: **8–13x more tokens** than English depending on model
- Hindi: **4–7.5x more tokens** than English
- Three real harms: higher API cost, longer latency, smaller context window
- Telugu speakers using GPT-4 pay **8.34x more per word** than English speakers
- **Does NOT build a solution** — theoretical sketch only

**Paper 2 — Kanjirangat et al. (EMNLP 2025)**
*"Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks"*

- Proves tokenization unfairness directly hurts real downstream task performance
- Introduces **Information Parity (IP)** as a new metric alongside Tokenization Parity (TP)
- TP predicts syntactic/surface tasks; IP predicts semantic tasks
- Encoder models (BERT) consistently outperform GPT-style models on dialectal tasks
- LLaMA tokenizer actively garbles non-Latin scripts into broken Latin characters
- **Does NOT cover** code-switching, Romanized text, or Telugu specifically

**Paper 3 — Foroutan, Meister et al. (arXiv, August 2025)**
*"Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization"*

- **THE SOLUTION** to Petrov's problem — actually builds and tests the fix
- Modified BPE algorithm: at each merge step, optimize for worst-compressed language instead of global frequency
- Gini inequality coefficient drops from 0.064 → 0.011 (**83% reduction in inequality**)
- Zero impact on downstream performance
- Telugu accuracy improves: 32.73% → 33.52%
- **Still only tested on clean, formal, monolingual text**
- **Does NOT cover** code-switching, Romanized input, or colloquial language

#### The Gap We Fill

Even after the infrastructure is fixed (Foroutan 2025), standard evaluation still fails real users. Code-switching, Romanized Telugu, and colloquial register are completely unmeasured by any existing benchmark.

#### Real Example from Our Session

A team member typed in the session:
> *"manam ikkada yem madladathunamo neeku ardam avthunda?"*

This is Romanized colloquial Telugu meaning "Do you understand what we are talking about here?" This single sentence demonstrates every failure mode our paper is about:
- Written in Roman script (not Telugu script)
- Colloquial spoken Telugu (not formal written Telugu)
- No benchmark recognizes or evaluates this form
- A model that responds in English, formal Telugu, or gibberish would **pass standard metrics but fail the real user**

This is our paper's opening anecdote.

#### Positioning Statement (Draft)

> *"Recent work has made significant progress on tokenization fairness (Petrov 2023; Foroutan 2025). However, even with equitable tokenization, a deeper problem remains: standard evaluation benchmarks measure clean, formal, monolingual text — completely missing how Telugu and Hindi speakers actually use AI systems. Real users code-switch, write in Romanized script, and communicate in colloquial registers that no current benchmark captures. We demonstrate that models can pass every standard evaluation while systematically failing real Indian language users — an invisible inequity that persists even after infrastructure-level fixes."*

#### Proposed Methodology

**Option A (Recommended — lower effort, high impact):**
1. Collect 100–200 real code-switched prompts from Telugu/Hindi native speakers
2. Test on 4–5 major LLMs (GPT-4o, Gemini, Claude, Llama)
3. Show standard metrics give models a "pass" but native speakers rate outputs as failing
4. Propose a simple human evaluation rubric as alternative metric

**Option B (Higher effort, higher citation potential):**
1. Build a small rigorous code-switched evaluation dataset for Telugu-English and Hindi-English
2. Release publicly — instant citation magnet for future researchers

**Difficulty:** Medium — most concrete path to publication

---

### Topic 3 — Data Collection and Annotation
**Core question:** What data is missing, and who should be collecting and labeling it?

Two sub-problems:

**Sub-problem 1 — Data Scarcity:**
- Common Crawl (powers most LLM training) is ~46% English despite English being ~17% of internet users
- Telugu content online mostly exists in Romanized form — scrapers don't recognize it as Telugu
- Model never learned Telugu properly in the first place

**Sub-problem 2 — Annotation Bias:**
- Most annotation outsourced to workers who lack cultural context for the language they're labeling
- Annotators from different cultures disagree on toxicity, sentiment, subjectivity at rates far higher than within-culture disagreement
- Current pipelines treat this disagreement as noise — but it's actually meaningful cultural signal
- Who annotates determines what gets labeled as harmful, neutral, or positive

**Interesting insight from our discussion:**
YouTube has enormous Telugu/Hindi audio data but converting it to usable training data has unsolved bottlenecks:
- Telugu ASR models have 30-40% word error rate
- Code-switching breaks ASR models
- ASR often outputs Romanized instead of Telugu script
- Copyright/legal issues with YouTube content
- Still need human annotation after transcription

This could be a bridge between Topic 3 and Topic 6.

**Our opportunity:** Run an annotation study — give 50-100 Telugu/Hindi sentences to native speakers, compare labels to Western-built ground truth, show systematic cultural disagreement as meaningful signal.

**Difficulty:** Medium-High
**Paper type:** Annotation study

---

### Topic 4 — Innovations and Vulnerabilities from the World
**Core question:** What do global users expose that English testing never catches?

Two angles:

**Vulnerability angle:**
- Safety filters trained on English fail in low-resource languages including Romanized Telugu
- Hallucination rates 2-3x higher in low-resource languages
- Transliteration attacks — Romanized Telugu bypasses safety classifiers trained on clean scripts
- Models confidently generate wrong information in Telugu more often than in English

**Innovation angle:**
- Indian users pioneer code-switched prompting strategies that improve task performance
- Users who switch to Hindi mid-conversation sometimes get better results
- Users who prompt in Chinese reportedly get lower API costs (mentioned in workshop description itself)
- These workarounds are undocumented and unstudied

**Our opportunity:** Test safety filters with Romanized Telugu prompts and document bypass rates. OR survey Indian users about their AI workarounds.

**Difficulty:** Medium — vulnerability testing is straightforward and could be done quickly
**Paper type:** Red-teaming study or user survey

---

### Topic 5 — Modeling for Global Understanding
**Core question:** What does it mean to build a model not anchored to any single culture?

- No agreed definition of "cultural understanding" in AI
- Current multilingual models are essentially English models that also speak other languages
- Models default to Western cultural assumptions even when prompted in Telugu/Hindi
- Key debate: should models be culturally neutral OR culturally adaptive? No consensus

**Our opportunity:** Best suited as a position or survey paper. Hard to make a concrete empirical contribution in a short workshop paper.

**Difficulty:** Very High for a short paper
**Paper type:** Position/survey paper

---

### Topic 6 — Interdisciplinary and Cross-Modal Insights
**Core question:** How do biases in one modality (text, image, audio) inform others?

- Image generation models reproduce stereotyped imagery for Indian prompts
- Telugu TTS (text-to-speech) — almost no high-quality open models exist
- Whisper (OpenAI) significantly weaker for tonal languages and non-standard accents
- Social scientists almost entirely absent from NLP dataset design
- No benchmark evaluates the same cultural concept across text, image, and audio simultaneously

**Our opportunity:** Design a small cross-modal cultural evaluation for Telugu/Hindi. Test how models handle a culturally specific Indian concept (like "jugaad" or "izzat") across text, image, and audio modalities.

**Difficulty:** High — needs multimodal expertise
**Paper type:** Exploratory cross-modal study

---

## Comparison Table — All 6 Topics

| Topic | Core Question | Difficulty | Telugu/Hindi Fit | Novelty | Best Paper Type |
|-------|--------------|------------|-----------------|---------|----------------|
| 1. Globalizing Tasks | Are standard NLP tasks culturally appropriate? | Medium | Strong | Medium | Empirical audit |
| 2. Evaluation Beyond Performance | Do metrics capture real usability? | Medium | Very Strong | High | Empirical + framework |
| 3. Data & Annotation | Who builds the data and how? | Medium-High | Strong | High | Annotation study |
| 4. Innovations & Vulnerabilities | What do global users expose? | Medium | Strong | High | Red-teaming / user study |
| 5. Modeling for Global Understanding | What is cultural understanding? | Very High | Moderate | Very High | Position paper |
| 6. Cross-Modal Insights | Do biases transfer across modalities? | High | Moderate | Very High | Exploratory |

---

## Recommendation for the Team

**Best options for a first workshop paper (ranked):**

1. **Topic 2** — Most mature literature, clearest gap, most direct path to publication. We already have 3 papers building a perfect narrative. Our Telugu/Hindi speaker access gives us exactly the empirical data needed.

2. **Topic 4** — Exciting and novel. Safety vulnerabilities in Romanized Telugu is a study we could run this week. Hot topic right now.

3. **Topic 3** — Very doable with our speaker access. Annotation disagreement study is a genuine first for Telugu.

**Avoid for a short workshop paper:**
- Topic 5 — Too broad, hard to make concrete contribution
- Topic 6 — Needs multimodal expertise across the team

---

## Papers to Cite (Confirmed)

| # | Paper | Venue | What it proves |
|---|-------|-------|---------------|
| 1 | Petrov et al. (2023) | NeurIPS | Tokenization unfairness — Telugu 8-13x worse |
| 2 | Kanjirangat et al. (2025) | EMNLP | Unfairness hurts downstream performance |
| 3 | Foroutan, Meister et al. (2025) | arXiv Aug 2025 | Parity-aware BPE solution — infrastructure fixed |
| 4 | Ahia et al. (2023) | EMNLP | "Do All Languages Cost the Same?" |
| 5 | Khanuja et al. (2021) | — | MuRIL — Indian language model, still favors English |
| 6 | Tamkin et al. (2024) | — | Code-switching safety gaps (cited in workshop) |

---

## Action Items After Tomorrow's Meeting

### All team members:
- [ ] Read all 3 core papers (Petrov, Kanjirangat, Foroutan)
- [ ] Vote on which topic to pursue
- [ ] Check workshop submission deadline at workshop website

### Once topic is chosen:
- [ ] Collect 100-200 code-switched Telugu/Hindi prompts from native speakers
- [ ] Run tokenization counting experiment across GPT-4o, Gemini, Llama, Claude
- [ ] Design human evaluation rubric with native speakers
- [ ] Draft introduction using positioning statement above
- [ ] Assign writing sections to team members

### Resources to search for latest papers:
- **arXiv:** arxiv.org — filter by 2025-2026
- **ACL Anthology:** aclanthology.org — ACL, EMNLP, NAACL 2025-2026
- **Semantic Scholar:** search "multilingual evaluation Telugu 2025"
- **Google Scholar:** filter "Since 2025"

---

## Key Takeaway for the Meeting

We are a team of Indian students with direct access to Telugu and Hindi speakers targeting a workshop that explicitly asks for research on exactly this problem. This is a rare alignment of team strengths and workshop needs.

The research gap is real, documented, and wide open. Three papers have built the foundation — our job is to take it one step further by showing what happens to real Indian users in practice.

---

*Document prepared: May 30, 2026*
*Next session: After team meeting*
