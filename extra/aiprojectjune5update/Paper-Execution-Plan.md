# Paper Execution Plan
**Workshop:** GenAI4World @ COLM 2026, San Francisco
**Submission deadline:** June 23, 2026
**Internal final draft deadline:** June 20, 2026
**Today:** June 1, 2026
**Working window:** ~22 days

---

## Locked Scope Decisions

### Topic
Topic 2 — *Evaluation Beyond Performance*. We measure the evaluation gap between standard automatic metrics and how real Indian-language users actually communicate with AI systems.

### Languages (7 total, tiered depth)

| Tier | Languages | Prompts/language | Depth |
|---|---|---|---|
| **A** (core) | Telugu, Hindi | 75–100 | Full methodology, full paper sections, deep analysis |
| **B** (extended) | Tamil, Kannada | 30–50 | Full methodology, smaller sample, secondary sections |
| **C** (cross-family validation) | Korean, Mandarin, Marathi | 15–20 | Lightweight: tokenization counts + spot-check outputs only |

**Total target:** ~280 prompts across 7 languages.

**Why tier C exists:** widens the paper's argument from "Indic languages are failed" to "non-English non-Western use is systematically failed across language families." Better fits GenAI4World's *globalizing* theme.

### Data source rule (LOCKED)
**Real user prompts only.** Google Translate is used ONLY as a baseline/control (to show models pass on GT output but fail on real input) and for tokenization counting. Never as a substitute for native-speaker contributions.

### Models to test
- GPT-4o (OpenAI)
- Claude (Anthropic)
- Gemini (Google)
- Llama 3 (Meta — via HuggingFace or Together AI)
- One Indic-tuned model (e.g., MuRIL) for comparison

---

## Phase-by-Phase Plan

### Phase 1 — Setup (June 2–4, ~3 days)
- [ ] Lock Topic 2 formally with team — written confirmation from every member
- [ ] Verify workshop logistics: deadline timezone, page limit, LaTeX template, anonymized review?
- [ ] Set up shared workspace (Overleaf for paper, Google Drive for data, shared spreadsheet for prompts)
- [ ] Obtain API keys: GPT-4o, Claude, Gemini, Together AI for Llama
- [ ] Confirm budget for API calls (~$50–100 total estimate)
- [ ] Identify owner per language (see Ownership Matrix below)

### Phase 2 — Methodology Design (June 4–8, ~5 days)
- [ ] Finalize prompt collection protocol (see "Prompt Categories" section)
- [ ] Design native-speaker evaluation rubric (see "Evaluation Rubric" section)
- [ ] Pilot run: collect 5–10 prompts from one Telugu speaker, score with rubric, validate protocol
- [ ] Refine protocol + rubric based on pilot

### Phase 3 — Data Collection (June 6–15, parallel with Phase 2 once protocol stable)
- [ ] Tier A — Telugu: 75–100 prompts
- [ ] Tier A — Hindi: 75–100 prompts
- [ ] Tier B — Tamil: 30–50 prompts
- [ ] Tier B — Kannada: 30–50 prompts
- [ ] Tier C — Korean: 15–20 prompts
- [ ] Tier C — Mandarin: 15–20 prompts
- [ ] Tier C — Marathi: 15–20 prompts
- [ ] **Hard checkpoint June 12:** if <50% collected, drop tier B or tier C

### Phase 4 — Tokenization Experiment (June 6–10, parallel)
- [ ] Build comparison script: ~20 equivalent sentences across English, Telugu/Hindi (script), Romanized Telugu/Hindi, Hinglish, Tenglish
- [ ] Run through GPT-4o (`tiktoken`), Claude (`count_tokens` API), Gemini SDK, Llama (HuggingFace)
- [ ] Output: comparison table of token counts + ratios
- [ ] Bonus novelty: Romanized + code-switched counts that no prior paper has

### Phase 5 — LLM Evaluation (June 13–17, 5 days)
- [ ] Build script to send all prompts through each model + capture responses
- [ ] Apply automatic metrics: BLEU, BERTScore, English LLM-as-judge
- [ ] Distribute outputs to native speakers for rubric scoring
- [ ] Compute auto-vs-human gap per language per category

### Phase 6 — Writing (June 15–20, parallel with Phase 5 once results trickle in)
- [ ] Draft Intro (with three-paper narrative arc + hero anecdotes)
- [ ] Draft Related Work
- [ ] Draft Methodology
- [ ] Draft Results
- [ ] Draft Discussion + Limitations
- [ ] Draft Conclusion
- [ ] Internal review round 1 — June 18
- [ ] Internal review round 2 — June 20
- [ ] Final polish

### Phase 7 — Submit (June 21–23, 2-day buffer)
- [ ] Format compliance check against workshop template
- [ ] Final read-through
- [ ] Submit by June 22 (one-day safety buffer before June 23 deadline)

---

## Prompt Categories (the framework, not the full list)

Native speakers should generate prompts that cover ALL of these categories. This taxonomy ensures we can break down results by failure type.

### 1. Romanized colloquial questions
Everyday questions written in Latin script in spoken/casual register. Most common real-world failure mode.

### 2. Code-switched everyday requests
Mixed English + native language in one sentence. Tests whether the model handles language boundaries gracefully.

### 3. Cultural / kinship references
Prompts that require knowing kinship terms, festivals, food names, or regional context that English doesn't map to.

### 4. Tasks requiring native fluency
"Draft a message to my mom," "summarize this in casual Telugu," "explain X to a child."

### 5. Idioms / proverbs / wordplay
Phrases that fail under literal translation. Strongest exposure of semantic failures.

### 6. Register-sensitive content
Formal vs casual, honorifics, asking for polite refusals — exposes register-awareness gaps.

### 7. Romanized voice transcripts
Prompts that look like how people actually text — abbreviations, dropped letters, mixed scripts.

---

## Prompt Examples Per Language

**IMPORTANT:** These are starter examples written by Claude based on pattern recognition. **Native speakers must validate, correct, and expand them.** Some may have grammar errors or unnatural phrasing.

### Telugu (target: 75–100 prompts)

**Romanized colloquial questions**
1. "nuvvu ee weekend free na? cinema ki vellam ante?"
2. "manam ikkada yem madladathunamo neeku ardam avthunda?"
3. "naa boss tho ela matladali, raise adgali ante?"
4. "ee traffic enti ra baba, em cheyali?"

**Code-switched everyday requests**
5. "Diwali ki amma ki gift em konukunte best ga untundi?"
6. "office lo deadline undi, can you help me write a polite extension email?"
7. "naa friend ki birthday wishes ela cheppali, formal kaakunda?"

**Cultural / kinship references**
8. "atta gaariki gift ela select cheyali for Sankranti?"
9. "mama gariki phone chesinappudu enti adagali first?"
10. "ammamma chesina pulihora recipe cheppu, simple ga"

**Tasks requiring native fluency**
11. "Draft a casual Telugu message to my brother saying I'll be late for dinner"
12. "Explain photosynthesis in simple Telugu but keep technical English terms"
13. "Summarize this English news article in 3 lines of Telugu"

**Idioms / proverbs**
14. "'paamu kanavachindi ante kanvachindi' anedi enti meaning?"
15. "Translate 'avunu kada ante kadu antaru' into English with cultural context"

### Hindi (target: 75–100 prompts)

**Romanized colloquial / Hinglish**
1. "yaar tomorrow ka meeting ka agenda kya hai?"
2. "mom ne kaha hai ki tum dinner ke liye ghar aana"
3. "this assignment me itna stress ho raha hai, kya karu?"
4. "best Indian food spot Bay Area me konsa hai?"

**Code-switched everyday requests**
5. "mere boss bahut strict hai, kaise impress karu professionally?"
6. "Diwali decorations ke liye amazon par kya order karu?"
7. "office me promotion ke liye apply karne ka right time kab hai?"

**Cultural / kinship references**
8. "Chacha ji ko shaadi ki invitation kaise bheju, formal hindi me?"
9. "Karwa Chauth ke liye kya gift ideas hain bhabhi ke liye?"
10. "Bua ji ke ghar jana hai, kya le ke jau gift me?"

**Tasks requiring native fluency**
11. "Draft a polite refusal in Hindi for a wedding I can't attend"
12. "Explain how UPI works in casual Hindi for someone above 60"
13. "Summarize today's news in 3 short lines of Hindi"

**Idioms / proverbs**
14. "'andhon mein kaana raja' iska kya matlab hai aur kab use karte hain?"
15. "'naach na jaane aangan tedha' — explain with a modern example"

### Tamil (target: 30–50 prompts)

1. "indha weekend evening la mama vandhuva nu sonna, what to cook?"
2. "nee oru advice kudunga sis, ennoda career switch panrenna?"
3. "Pongal-ku amma seyra payasam recipe sollu"
4. "office la boss ku polite ah email anuppanum, draft pannu"
5. "Chennai la best filter coffee spot edhu?"
6. "'kallai pol vaazha' iduku enna meaning?"

### Kannada (target: 30–50 prompts)

1. "Naanu Bengaluru ge baruva plan idhe weekend, suggest some places"
2. "Amma helidha rava idli recipe heng madbeku?"
3. "Office alli boss ge polite ah email bareyokke help maadi"
4. "Mysore Dasara ge gift ideas kodi"
5. "'Aanege saaviradashida bele' iduga enu meaning?"

### Marathi (target: 15–20 prompts, light coverage)

1. "Aaj evening la party ahe, kay ghaalu?"
2. "Mumbai madhe best vada pav konta?"
3. "Office madhe promotion sathi kasa apply karaycha?"
4. "Aaji ne sangitlela puran poli recipe sang"

### Korean (target: 15–20 prompts, light coverage)

Note: Konglish (Korean-English code-switching) has different patterns from Indic code-switching — typically Korean grammar with English nouns, written in Hangul or Romanized.

1. "Oppa, naega sigan eopseo, suggest a quick lunch place"
2. "Mom-i hwana neoljjok inhae, what should I do? help me reply politely"
3. "Annyeong, can you draft a formal email to my sajangnim?"

### Mandarin (target: 15–20 prompts, light coverage)

Note: Chinglish typically has Chinese grammar/topic with English vocabulary insertions.

1. "wo de boss bu dong English, can you help me explain 'I need time off'?"
2. "Mama said wo yao zou jia chi fan, but I have urgent work, kaise reply karu? — sorry, what should I say?"
3. "Chinese New Year ke liye gift suggestions for elderly relatives"

---

## Evaluation Rubric (template)

Each LLM output is scored by a native speaker on 4 dimensions, scale 1–5:

| Dimension | What it measures |
|---|---|
| **Fluency** | Does the output read like natural native-language? |
| **Register appropriateness** | Does it match the casual/formal level of the prompt? |
| **Semantic accuracy** | Does it answer the actual question correctly? |
| **Cultural fit** | Does it handle kinship/festivals/honorifics correctly? |

Plus a binary flag:
- **"Would a native speaker actually accept this response?"** — yes/no

For inter-rater reliability: 20% of outputs scored by 2 raters; report Cohen's kappa.

---

## Paper Structure (target: 6–8 pages workshop length)

1. **Introduction** (~1 page)
   - Hero anecdote (Romanized Telugu sentence)
   - Three-paper narrative arc (Petrov → Kanjirangat → Foroutan → gap)
   - Contribution statement

2. **Related Work** (~1 page)
   - Petrov 2023 (tokenization unfairness)
   - Kanjirangat 2025 (TP/IP downstream impact)
   - Foroutan 2025 (parity-aware BPE)
   - EfficientXLang 2025 (counter-finding on reasoning efficiency — must address)
   - Ahia 2023 (cost asymmetry)
   - MuRIL (Indic models still English-favored)
   - Tamkin 2024 (code-switching safety gaps)

3. **Methodology** (~1.5 pages)
   - Language selection + tier rationale
   - Prompt collection protocol
   - LLM evaluation setup
   - Native-speaker rubric

4. **Results** (~2 pages)
   - Tokenization counting (English/script/Romanized/code-switched)
   - Auto vs human score gap per language per category
   - Subgroup breakdowns

5. **Discussion + Limitations** (~1 page)
   - What the gap means for deployment
   - Why Foroutan-style fixes don't close this gap
   - Limitations: sample sizes, language coverage, rubric subjectivity

6. **Conclusion + Future Work** (~0.5 page)
   - The gap is real, measurable, persistent
   - Recommendation: human-in-the-loop evaluation for low-resource languages
   - Future: more languages, longitudinal study, automated rubric

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Native speakers don't deliver by June 12 | Medium | High | Drop tier B or C; tier A can stand alone |
| API budget overruns | Low | Medium | Pre-compute estimated calls; use `count_tokens` endpoints for free where possible |
| Page limit forces cuts | Medium | Medium | Pre-decide cut order: tier C → tier B → subgroup analyses |
| Rubric calibration weak (low inter-rater agreement) | Medium | High | Pilot calibration before bulk scoring; reject prompts with κ<0.4 |
| EfficientXLang gets cited by reviewers as counter-evidence | High | Low | Address head-on in related work |
| Surbhi pushes for T2I/cross-modal pivot | Medium | Medium | Discuss explicitly in next team meeting; lock decision |

---

## Ownership Matrix (to be filled by team)

| Area | Owner | Backup |
|---|---|---|
| Project management / timeline tracking | Madhu (?) | — |
| Telugu prompt collection + scoring | ? | ? |
| Hindi prompt collection + scoring | ? | ? |
| Tamil collection + scoring | Office colleague | Madhu coordinates |
| Kannada collection + scoring | Girlfriend | Madhu coordinates |
| Marathi collection + scoring | Office colleague | Madhu coordinates |
| Korean collection + scoring | Office colleague | Madhu coordinates |
| Mandarin collection + scoring | Office colleague | Madhu coordinates |
| Tokenization experiment | ? | ? |
| LLM API setup + running prompts | ? | ? |
| Auto metrics implementation | ? | ? |
| Paper writing — Intro / Related Work | ? | ? |
| Paper writing — Methodology / Results | ? | ? |
| Paper writing — Discussion / Conclusion | ? | ? |
| Format check + submission | ? | ? |

**Action required:** team meeting to fill this in. Without explicit owners, work slips.

---

## Key Decisions Still Needed

1. Confirm Topic 2 lock (or surface dissent)
2. Confirm 7-language tiered scope (or argue for narrower)
3. Confirm Google-Translate-as-baseline-only rule
4. Confirm prompt collection protocol after pilot
5. Confirm page limit + paper structure
6. Fill ownership matrix
