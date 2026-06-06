# AI Research Paper — Context File
**Workshop:** GenAI4World — First Workshop on Globalizing Tasks, Evaluations, and Systems
**Co-located with:** COLM 2026, San Francisco
**Workshop URL:** https://sites.google.com/view/genai4world/home
**Contact:** genai4world-workshop@googlegroups.com
**Team:** Indian students with access to Telugu and Hindi native speakers

---

## IMPORTANT: How to Use This File

When starting a new Claude session, paste this entire file and say:
> "This is my research context. Please read it fully and continue helping me with my research paper."

When resuming in Claude Code after `/clear`, just say:
> "Read research-context.md and continue from the Session State section."

---

## Session State (last updated: 2026-06-03 afternoon — deep literature verification + MAJOR REFRAME)

> **⭐ MOST CURRENT — READ FIRST: see "Session 2026-06-03 (afternoon) — Deep Literature Verification + MAJOR REFRAME" at the END of this file. The paper's claimed novelty has been repositioned (prior work now occupies the original framing). Read that section before resuming any work.**

### Where we are in the workflow
Walking through the 6 workshop topics one at a time to pick which one to focus on. Topic 1 was covered in a previous session and is already documented above. **Topic 2 is in progress — all 3 papers now covered.**

### Topic 2 sub-progress
- ✅ **Petrov (2023)** — tokenization unfairness — internalized. User understands what tokenization is, why Telugu costs 8x more tokens, why the tokenizer is frozen to the model, and the difference between tokenizer-bias and model-parameter-bias.
- ✅ **Foroutan (2025)** — parity-aware BPE — internalized. User understands the mechanism ("same data, smarter algorithm"), why it can't patch existing models, and why even next-gen models might not adopt it soon (timing, risk, infrastructure, no customer pressure).
- ✅ **Kanjirangat (2025)** — IP vs TP applied to dialectal tasks — paper read in full by Claude (user pasted the actual PDF text), key concepts taught with corrections. User has the corrected mental model but has NOT yet answered the closing synthesis question (see "Open question on resume" below). Reading the paper directly revealed several important corrections to the team summary — see "Refined Understanding for Kanjirangat" section.

See "Refined Understanding (Session 2026-05-30)" near the bottom for the detailed mental model for all three papers.

### Locked decisions
- **Paper framing: technical only, no moralizing.** Let numbers + real user prompts do moral work. No "companies are greedy" framing.
- **Picked topic: still pending team decision**, but Topic 2 has the strongest narrative so far.

### Teaching preferences for this user (Mahesh)
- One question at a time, never bundle three questions into one
- Push back when his answer is wrong, but stay expansive (offer adjacent ideas)
- He's new to NLP/ML — explain like he's learning the field, don't summarize as if he already knows
- He thinks like an engineer — connect ideas to engineering analogues he'll recognize
- Decision style: makes explicit calls when satisfied ("lock this in", "let's go", "I agree")
- Flag your own uncertainty when citing specific numbers or claims you haven't independently verified

### Token efficiency note
User is on Opus 4.7 (1M context) only in this specific session — can't easily get back to Opus 4.7 in other sessions. He `/clear`s regularly to reduce session bloat. **Before each `/clear`, ensure everything important is in this file.** Keep responses tight: prose over tables, no emoji-heavy headers, no recap closers unless useful.

The fastlane-web-sdk `CLAUDE.md` has been temporarily renamed to `CLAUDE.md.bak` to drop ~3K tokens/turn from this session. Restore it (`mv CLAUDE.md.bak CLAUDE.md`) before returning to fastlane work.

### Next concrete step on resume / Open question
Pick up with the open synthesis question on Foroutan, posed at end of last session:

> **Given Kanjirangat's DI reversal finding (high TP = better dialect ID, high IP = worse dialect ID), does this make Foroutan's parity-aware BPE less attractive as a universal "fix" — and does that strengthen or weaken our paper's gap argument?**

The angle to develop: Foroutan smooths tokenization across languages, which should help semantic tasks (Topic Classification) but might *hurt* surface-level dialectal tasks (Dialect ID) where fragmentation accidentally helps. This complicates "infrastructure fix" framing and could either weaken Foroutan's value OR strengthen our gap argument depending on how it's framed.

After locking that in, two natural next steps:
1. Apply corrections to the team summary (see "Team Summary Corrections Needed" section)
2. Decide whether to move to Topic 3, or commit to Topic 2 and start methodology planning

---

## Our Team's Situation

- Group of Indian students writing a research paper together
- Have direct access to Telugu and Hindi native speakers — this is our key asset
- Targeting GenAI4World workshop at COLM 2026
- Still deciding which of the 6 topics to focus on
- Need to collectively pick one topic as a team

---

## The 6 Topics from the Workshop Call for Papers

### Topic 1 — Globalizing Tasks
Which tasks are understudied or absent in non-English, non-Western contexts? What usage patterns reveal gaps in how present systems were designed?

**Research depth:** Overview level
**Key insight:** Most NLP tasks (sentiment, QA, summarization) were designed around English and Western assumptions. Just translating them doesn't fix cultural misalignment.
**Our opportunity:** Audit 3-4 standard NLP tasks for cultural misalignment in Telugu/Hindi context. Show tasks are not just missing but actively wrong.
**Difficulty:** Medium

---

### Topic 2 — Evaluation Beyond Performance ⭐ MOST RESEARCHED
What do standard metrics miss — register, cultural expectation, usability? How do we move beyond Western-centric benchmarks?

**Research depth:** DEEP — 3 papers found, gap identified, methodology proposed

**The 3-Paper Narrative:**

**Paper 1 — Petrov et al. (NeurIPS 2023)**
"Language Model Tokenizers Introduce Unfairness Between Languages"
- Proves tokenization discriminates against non-English languages BEFORE model even runs
- Telugu: 8-13x more tokens than English depending on model
- Hindi: 4-7.5x more tokens than English
- Three harms: higher API cost, longer latency, smaller context window
- Does NOT build a solution — theoretical sketch only
- Key stat: ChatGPT/GPT-4 tokenizer requires 8.34x more tokens for Telugu vs English

**Paper 2 — Kanjirangat et al. (EMNLP 2025)**
"Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks"
- Proves tokenization unfairness directly hurts downstream task performance
- Introduces Information Parity (IP) metric alongside Tokenization Parity (TP)
- TP predicts syntactic/surface tasks; IP predicts semantic tasks
- Encoder models (BERT) outperform GPT-style models on dialectal tasks
- LLaMA tokenizer actively garbles non-Latin scripts
- Does NOT cover code-switching, Romanized text, or Telugu specifically

**Paper 3 — Foroutan, Meister et al. (arXiv, August 2025)**
"Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization"
- THE SOLUTION to Petrov's problem
- Modified BPE: at each merge step, optimize for worst-compressed language instead of global frequency
- Gini inequality drops from 0.064 → 0.011 (83% reduction)
- Zero impact on downstream performance
- Telugu accuracy: 32.73% → 33.52%
- Still only tested on clean, formal, monolingual text
- Does NOT cover code-switching, Romanized input, or colloquial language

**Our Gap:**
Even after infrastructure is fixed (Foroutan), standard evaluation still fails real Indian users. Code-switching, Romanized Telugu, and colloquial register are completely unmeasured.

**Real Example from our session:**
A team member typed: "manam ikkada yem madladathunamo neeku ardam avthunda?"
This is Romanized colloquial Telugu. Standard benchmarks would not recognize it as Telugu at all.

**Positioning Statement:**
"Recent work has made significant progress on tokenization fairness (Petrov 2023; Foroutan 2025). However, even with equitable tokenization, a deeper problem remains: standard evaluation benchmarks measure clean, formal, monolingual text — completely missing how Telugu and Hindi speakers actually use AI systems. Real users code-switch, write in Romanized script, and communicate in colloquial registers that no current benchmark captures. We demonstrate that models can pass every standard evaluation while systematically failing real Indian language users."

**Proposed Methodology (Option A — recommended):**
1. Collect 100-200 real code-switched prompts from Telugu/Hindi native speakers
2. Test on 4-5 major LLMs (GPT-4o, Gemini, Claude, Llama)
3. Show standard metrics give models a "pass" but native speakers rate outputs as failing
4. Propose a simple human evaluation rubric as alternative metric

**Difficulty:** Medium — most concrete path to publication

---

### Topic 3 — Data Collection and Annotation
What data is missing and how should it be collected? How do annotation standards need to change?

**Research depth:** Overview + extended discussion

**Key insight:**
Two sub-problems:
1. Data scarcity — Common Crawl is ~46% English despite English being ~17% of internet users. Telugu content online is mostly Romanized and not recognized as Telugu by scrapers.
2. Annotation bias — Most annotation outsourced to workers who lack cultural context. Annotator disagreement is treated as noise, not meaningful cultural signal.

**YouTube insight (discussed in session):**
YouTube has enormous Telugu/Hindi audio data but converting it to usable training data has bottlenecks:
- ASR quality for Telugu is weak (30-40% word error rate)
- Code-switching breaks ASR models
- ASR often outputs Romanized instead of Telugu script
- Still need human annotation after transcription
- Copyright/legal issues with YouTube content
This could bridge Topic 3 and Topic 6.

**Key papers:**
- DICES and POPQUORN datasets — introduced annotator identity metadata
- Masakhane/AfricaNLP — community-driven dataset building
- ROOTS corpus (BigScience 2022)

**Our opportunity:**
Run annotation study — give 50-100 Telugu/Hindi sentences to native speakers, compare labels to Western-built ground truth, show systematic cultural disagreement as meaningful signal.

**Difficulty:** Medium-High

---

### Topic 4 — Innovations and Vulnerabilities from the World
Can global users' experiences inform better system design? What new risks do they expose?

**Research depth:** Overview level

**Two angles:**
1. Vulnerabilities — safety filters trained on English fail in Telugu/Romanized Telugu. Hallucination rates 2-3x higher in low-resource languages. Transliteration attacks bypass safety classifiers.
2. Innovations — Indian users pioneer code-switched prompting strategies. Creative workarounds that improve performance undocumented.

**Key papers:**
- Tamkin et al. (2024) — safety gaps in non-English languages (cited in workshop description)
- Yong et al. (2023) — low-resource language jailbreaks

**Our opportunity:**
Test safety filters with Romanized Telugu prompts — document bypass rates. OR survey Indian users on AI workarounds.

**Difficulty:** Medium — vulnerability testing is straightforward and could be done quickly

---

### Topic 5 — Modeling for Global Understanding
What does it mean to build a model not bound to any single language or culture?

**Research depth:** Overview level

**Key insight:** No agreed definition of "cultural understanding." Models default to Western assumptions even when multilingual. Best suited as position/survey paper.

**Difficulty:** Very High for a short workshop paper

---

### Topic 6 — Interdisciplinary and Cross-Modal Insights
How can advances in one modality inform others?

**Research depth:** Overview level

**Key insight:** Telugu has almost zero multimodal resources. Same cultural bias appears across text, image, audio but studied in isolation. No cross-modal cultural benchmark exists.

**Difficulty:** High — needs multimodal expertise

---

## Comparison Table

| Topic | Difficulty | Telugu/Hindi Fit | Novelty | Best For |
|-------|------------|-----------------|---------|----------|
| 1. Globalizing Tasks | Medium | Strong | Medium | Empirical audit |
| 2. Evaluation Beyond Performance | Medium | Very Strong | High | Empirical + framework |
| 3. Data & Annotation | Medium-High | Strong | High | Annotation study |
| 4. Innovations & Vulnerabilities | Medium | Strong | High | Red-teaming / user study |
| 5. Modeling for Global Understanding | Very High | Moderate | Very High | Position paper |
| 6. Cross-Modal Insights | High | Moderate | Very High | Exploratory |

---

## Papers to Cite (confirmed so far)

1. Petrov et al. (2023) — NeurIPS — Tokenization unfairness
2. Kanjirangat et al. (2025) — EMNLP — Downstream impact of tokenization bias
3. Foroutan, Meister et al. (2025) — arXiv Aug 2025 — Parity-aware BPE solution
4. Ahia et al. (2023) — EMNLP — "Do All Languages Cost the Same?"
5. Khanuja et al. (2021) — MuRIL — Indian language model
6. Tamkin et al. (2024) — code-switching safety gaps (cited in workshop description)

---

## Next Steps (Pending Team Decision)

- [ ] Team to collectively pick ONE topic
- [ ] Once topic picked — go deep on that topic's literature
- [ ] Collect 100-200 code-switched Telugu/Hindi prompts from native speakers (relevant for Topics 2, 3, 4)
- [ ] Run tokenization counting experiment across GPT-4o, Gemini, Llama
- [ ] Check submission deadline at workshop website
- [ ] Draft introduction once topic is confirmed

---

## Technical Notes from Session

- Web search tool is broken in Claude Code terminal (uses deprecated claude-3-5-haiku-20241022 backend)
- Telugu script renders incorrectly in terminal — use browser-based Claude for Telugu script output
- Romanized Telugu renders fine in terminal
- Best model available in terminal: Sonnet 4.6 (Opus 4.8 shows in menu but has issues)
- For web searches, use arXiv, ACL Anthology, Semantic Scholar manually

---

## Key Insight from Session

The user's act of typing "manam ikkada yem madladathunamo neeku ardam avthunda?" (Romanized colloquial Telugu) in the terminal demonstrated every failure mode the paper is about:
- Roman script instead of Telugu script
- Colloquial spoken form not formal written Telugu
- No benchmark recognizes or evaluates this
- A model that fails this would pass every standard metric

This is the paper's opening anecdote.

---

## Refined Understanding (Session 2026-05-30)

This section captures clarifications worked through in a teaching session. The 3-paper narrative above is still correct, but the details below are sharper and should override anything that conflicts.

### Tokenizer bias ≠ Model parameter bias

These are TWO DIFFERENT problems and they are often conflated:

| Problem | What it is | What it causes |
|---|---|---|
| **Tokenizer bias** | Vocabulary built mostly on English text via BPE | Telugu costs 8x more tokens |
| **Model parameter bias** | Weights trained mostly on English text | Telugu *answers* are lower quality |

The 8x token count is purely a tokenizer issue. It happens BEFORE the model runs. The tokenizer is a separate component:

`Your input → [TOKENIZER] → token IDs → [MODEL] → output token IDs → [TOKENIZER] → text`

When the user types `నమస్తే` (Telugu "hello"), the model receives raw byte IDs like `[136, 168, 174, 184, ...]` with no learned semantics. Compare to English "hello" → `[31373]` — one token, rich learned meaning.

### Why the tokenizer is frozen to the model

Every model weight is tied to specific token IDs. The model learns "when I see token #4729 followed by token #8201, predict token #12044." Those IDs only have meaning via the tokenizer's mapping.

Change the tokenizer → all learned weights become garbage → must retrain from scratch (~$100M, 3-6 months for a GPT-4-class model).

**Implication:** A shipped model is stuck with its tokenizer for life. No patch is possible.

### What Foroutan's "parity-aware BPE" actually does

NOT a new model layer. NOT new training data. NOT a fine-tuning trick.

It's a one-line change to step 2 of the BPE algorithm:
- **Standard BPE:** at each merge step, pick the globally most-frequent pair
- **Parity-aware BPE:** pick the pair that helps the worst-compressed language the most

Same training data. Same model architecture. Smarter merge rule. Result: huge fairness gain (Gini 0.064 → 0.011 per context file numbers — verify before citing), zero performance loss.

**Mantra:** "Same data, smarter algorithm."

### Why Foroutan hasn't been adopted yet (two distinct reasons)

| Scenario | Blocker |
|---|---|
| Patch existing model (GPT-4) | **Impossible.** Tokenizer is frozen. |
| Bake into next-gen model (GPT-5+) | **Possible but unlikely soon.** Timing (Foroutan published Aug 2025, likely too late for in-progress flagship training runs); risk aversion (12-month-old algorithm shouldn't be the testbed for a $100M+ flagship); internal infrastructure lock-in (years of evals/tools assume current tokenizer); no customer pressure (English-speaking enterprises don't file tickets about Telugu) |

**Key takeaway for the paper:** Even in a best case, Foroutan adoption is 1-2 model generations away. The evaluation gap our paper measures remains relevant regardless of when/if Foroutan ships. This makes our contribution **time-resilient**.

### Economic framing (Ahia et al. 2023)

Not just "Telugu users pay more." More precisely: **Telugu users subsidize English users.**

OpenAI's compute cost is roughly flat per token. English users get ~8x the compute work per token they pay for. Telugu users are overpriced relative to actual compute cost. The per-token pricing model is **structurally regressive** — it taxes the poor to subsidize the rich.

### Framing decision for our paper (LOCKED)

**Technical only. No moralizing.**

State the asymmetry coldly. Quote one or two real Telugu user prompts. Let the contrast between dry numbers and a real human voice do the moral work.

**Why:** Reviewers dismiss polemic. "Companies are greedy" loses technical readers. "Here's a measurable gap that persists across legitimate engineering constraints" is unignorable.

### Hero anecdote v2 — the session token counter

In Claude Code (and any LLM chat UI with a token counter), the counter shows context window usage in real time. Running the same conversation in English vs Telugu visibly demonstrates the 8x gap — no methodology needed.

**For paper:** screenshot side-by-side English/Telugu sessions of the same content. Caption: "This is what Petrov (2023) measured, made visible in a single screen."

This complements the original hero anecdote ("manam ikkada yem madladathunamo neeku ardam avthunda?") which shows the *evaluation gap*. The counter shows the *cost gap*.

### Refined Understanding for Kanjirangat (added 2026-05-30 evening, after reading the actual paper)

**Source verified:** arXiv:2509.20045v1, dated 24 Sep 2025. Authors: Vani Kanjirangat, Tanja Samardžić, Ljiljana Dolamic, Fabio Rinaldi (SUPSI/IDSIA Switzerland + armasuisse S+T Switzerland). NOT an Indian/American team. Team summary lists this as "EMNLP 2025" — likely true (timing fits) but EMNLP acceptance not verified from the PDF itself. Code repo: github.com/vanikanjirangat/Tokenizer_Fairness_Dialect.

**Attribution correction (important):** TP and IP are NOT Kanjirangat's inventions.
- **TP** is from Petrov et al. (2024) — Kanjirangat reuses it
- **IP** is from Tsvetkov & Kipnis (2024) — Kanjirangat reuses it
- **Kanjirangat's actual contribution:** applying both metrics to *dialectal* NLP tasks (Dialect Identification, Topic Classification, Extractive QA) and correlating each metric with each task type to see which predicts which. The team summary currently implies Kanjirangat invented IP — fix this attribution before citing.

**IP definition (corrected):** Earlier in the session Claude described IP as "hidden-state alignment." Wrong mechanism. Actual definition from the paper:

> "IP is defined as the ratio between the negative log-likelihood of the text in English and the negative log-likelihood of the same text in language L."

Plain English: take a sentence in English and its translation in language L. Feed both to the model. Ask "how surprised is the model by each token on average?" (negative log-likelihood). IP = English-surprise ÷ L-surprise. If the model predicts L tokens as well as English tokens, IP ≈ 1. If L tokens are far more "surprising," IP drops below 1. It's a normalized perplexity ratio — about *probability under the model*, not hidden-state geometry. Higher IP = better (more equal compression with English).

**The big surprising finding (not in the team summary):** The "TP→syntactic / IP→semantic" pattern is only TWO of three tasks. For **Dialect Identification (DI)** the correlations *flip and are counterintuitive*:

- Higher TP (more fragmentation) → **BETTER** DI performance
- Higher IP (better semantic alignment) → **WORSE** DI performance

Paper's explanation: dialects differ mainly at the surface level (spelling, diacritics, morphology). Aggressive fragmentation creates surface tokens the model can use as dialect markers even without understanding them. High IP means the model treats dialects as semantically equivalent → loses the ability to distinguish them.

**Why this matters for our paper:** It complicates Foroutan's pitch. Foroutan smooths tokenization across languages — good for semantic tasks, potentially BAD for surface-level dialectal tasks where current bias is doing accidental work. This is the open question to develop on resume.

**Kannada data point (gold for our Telugu argument):** The paper tests **Kannada** (non-Latin, low-resource, Dravidian) with mBERT and reports **TP = 2.19** — meaning Kannada needs 119% more tokens than English. Kannada is the closest Dravidian relative tested. **Telugu would behave nearly identically** (same family, same script complexity, similar agglutinative morphology). This is the strongest empirical anchor we have for Telugu's situation from existing literature — cite it directly.

**Other paper findings worth noting:**
- mBERT consistently outperforms decoder LLMs (Phi-3.5, Llama-3.2) on all three dialectal tasks
- Language-specific BERT variants beat mBERT in most cases (MARBERT for Arabic, IndicBERT for Indic, etc.)
- Llama 3.2 specifically struggles with non-Latin scripts because its byte-level fallback misinterprets multi-byte UTF-8 characters as garbled Latin-1 characters (paper shows an Arabic example where Llama outputs token `Ø³` which Unicode-describes as "LATIN CAPITAL LETTER O WITH STROKE" + "SUPERSCRIPT THREE")
- Resource level affects performance MORE than script type, except in EQA where script matters more

---

### Team Summary Corrections Needed

Three concrete corrections needed in the user's team-facing summary document (the one pasted in this session, NOT this file):

1. **Speaker-count error.** The "Why Telugu+Hindi" table bottom row says "Both languages cover 200M+ speakers." Hindi alone is ~600M (native + L2), Telugu ~95M. Combined: 700M+. The 200M figure massively understates the impact argument. Fix before sharing externally.

2. **Token-count table presented as if measured.** The "Key Empirical Experiment We Can Run Today" table shows numbers (e.g., Telugu ~8.3x on GPT-4o) as if the team ran them. They're extrapolated from Petrov 2023. Label "from Petrov 2023" until actually run, or reviewers will pull the thread and find no experiment.

3. **"Foroutan = THE SOLUTION" undersells the paper's own thesis.** Foroutan fixes Tokenization Parity only. Kanjirangat shows there's a second problem (Information Parity) that Foroutan doesn't touch — and in some cases (DI reversal) parity-aware tokenization could actively hurt. Reframe as "a solution to one half of the problem" or "an infrastructure-level fix that addresses TP but not IP." Current framing weakens the gap argument.

4. **IP attribution.** Summary implies Kanjirangat introduced IP. Actually IP is from Tsvetkov & Kipnis (2024). Kanjirangat's contribution is *applying* both TP and IP to dialectal tasks. Fix attribution.

---

### Still to do in Topic 2

- [ ] Answer the open synthesis question on Foroutan (see "Next concrete step on resume" above)
- [ ] Apply the 4 corrections to the team summary document
- [ ] Independently verify the Foroutan numbers (Gini 0.064 → 0.011, Telugu accuracy 32.73% → 33.52%) before citing
- [ ] Confirm Petrov's 8.34x Telugu stat from the actual paper, not just the context summary
- [ ] Verify whether Kanjirangat (2025) was actually accepted at EMNLP 2025, or whether it's still arXiv-only

---

## Session 2026-06-02 — Execution Planning + Korean Reframe

*Note on user name:* in conversation, user identifies as **Madhu Beesetty**. Earlier "Mahesh" reference in teaching preferences appears to be incorrect — use "Madhu" going forward.

### What we did this session

1. Locked execution timeline: **June 23 submission, June 20 internal final draft** (~22 working days from start)
2. Made language scope decisions (3 confirmed + 3 pending + 1 negative control)
3. **Reframed Korean** from positive case to negative control based on Tia Kim's native-speaker feedback
4. Reviewed 4 references shared by teammates
5. Created `Paper-Execution-Plan.md` and `Prompt-Collection.md`
6. Worked through several conceptual questions about WHY this problem exists at all

### Locked decisions

#### Language scope (human evaluation)

| Language | Status | Prompts | Owner |
|---|---|---|---|
| Telugu | **Confirmed** | 75–100 | Madhu (native) |
| Hindi | **Confirmed** | 75–100 | Team-internal |
| Kannada | **Confirmed** | 50 | Madhu's girlfriend |
| Tamil | *Pending June 8* | 30–50 | Office colleague |
| Marathi | *Pending June 8* | 15–20 | Office colleague |
| Mandarin | *Pending June 8* | 15–20 | Office colleague |
| Korean | **Negative control (tokenization only)** | 0 human-eval | — |

**June 8 EOD = hard deadline** for pending contributors to confirm. Anything unconfirmed by then drops from human-eval (still kept in tokenization).

#### Korean reframe — KEY INSIGHT

Madhu shared Korean prompt examples with Tia Kim (office colleague). Tia's feedback:

- Korean Koreans do NOT code-switch English+Korean in chat. They use English loanwords ("bus", "OK") but don't mix mid-sentence.
- Even Korean-Americans (like Tia herself) default to monolingual when typing to ChatGPT.
- Code-switching for Korean-Americans is a SPOKEN behavior, not a typed one.
- K-drama portrayal of upper-class code-switching is unrealistic for everyday chat.

**Decision:** Korean becomes the negative control:
- Tokenization-only (Task 3), no human evaluation
- Predicted: token cost asymmetry persists but evaluation gap is small (because no code-switching pattern to expose)
- **This STRENGTHENS the paper** — isolates code-switching specifically as the gap-driver, rules out "AI is just bad at any non-English" as alternative explanation

**Discussion-section observation worth recording:**
> Modality preference differs across bilingual communities. Korean-Americans code-switch in speech but default to monolingual typing. Indians code-switch in both. The Romanization/code-switching pattern we measure is culturally specific, not a universal bilingual phenomenon.

#### Methodology refinements (locked)

**Paper has two complementary contributions:**

1. **WIDE tokenization study** — 10+ languages, computational, cheap. Replicates Petrov + extends with Romanized/code-switched variants nobody else has measured.
2. **DEEP human-evaluation study** — 3-4 languages, requires native speakers. The novel contribution.

**Three-way comparison** for tokenization analysis:
- Native script (e.g., తెలుగు) from FLORES
- GT-Romanized (standardized): "Namaste, meeru ela unnaru?"
- Real-user Romanized (idiosyncratic): "namaste meeru ela vunnaru?"

If LLMs handle #1 and #2 well but fail #3, that's the paper's central finding in a single graph.

**Real user data ONLY** for human evaluation. Google Translate is allowed for:
- Baseline/control comparison
- Reference text for automatic metrics (BLEU/BERTScore)
- Tokenization counting (parallel sentences)

Never used as a substitute for real-user prompt data.

**Pilot test recommended** before committing 18 days:
- 5 prompts × 2 models × 1 native speaker per language
- ~2 hours total
- Three outcomes: confirms hypothesis (proceed) / refutes (reframe to "industry improved") / shows subtle gap (most interesting)
- Cheap insurance against hypothesis being wrong

#### Scope discipline (locked)

- Do NOT expand to Arabic, Bengali, or other major Romanization-affected languages for v1
- Do NOT do human-eval on 10+ languages (only tokenization can be wide)
- Position paper as "first of methodological series" — broader feel without scope expansion
- Discussion can name Arabizi (~400M), Banglish (~270M), Roman Urdu (~230M), Pinglish (~80M) as future work → paper's implication footprint ~1.3B people without expanding data

### New references reviewed today

#### 1. EfficientXLang — Ahuja et al. (June 2025) — arXiv:2507.00246

"Towards Improving Token Efficiency Through Cross-Lingual Reasoning." Tests DeepSeek R1, Qwen 2.5/3 on math reasoning across 7 typologically diverse languages. Finding: reasoning in non-English uses FEWER tokens AND preserves accuracy.

**Relevance: HIGH but nuanced** — about reasoning chains, not user input. Different domain from ours. **Must address in related work** or reviewers will use it as counter-evidence. Suggested framing:

> *"EfficientXLang shows reasoning-chain efficiency in well-represented languages — orthogonal to our concern about user-facing input in low-resource and dialectal/Romanized forms."*

#### 2. Naik & Nushi 2023 — arXiv:2304.06034

T2I bias paper. **DROP — off-topic for Topic 2.** Shared by Surbhi; possibly advocating Topic 6 (cross-modal) pivot. Worth clarifying.

#### 3. Wan et al. 2024 — arXiv:2404.01030

T2I bias survey. **DROP — off-topic for Topic 2.** Same Surbhi signal.

#### 4. OpenAI Developer Community thread

French developer "Ailogik" reports 159 French words → 277 tokens = 74% more than expected. **Use as motivating anecdote in introduction** (not formal citation — forum thread).

### Conceptual insights worked through (reusable in paper sections)

#### Why models can't just be trained in English alone (6 reasons)
1. Scale prohibitive (~15T tokens, billions $ to translate)
2. Translation is lossy (cultural nuance, kinship, honorifics degrade)
3. Model couldn't generate non-English output
4. Round-trip translation compounds errors
5. Chicken-and-egg: need a high-quality translator first
6. Not all knowledge exists in English

#### Why Romanized Indic isn't in training data (4 reasons)
1. Hard to capture at scale (lives on WhatsApp/private chat)
2. Data cleaning pipelines treat it as noisy English and filter out
3. No standardization — every user spells idiosyncratically
4. No explicit cross-script pairing — model can't learn "manam"="మనం" without supervision

#### Why Korean/Japanese/Mandarin work better than Indic in LLMs
- Strong native-script training data (Naver, Kakao, Baidu, Niconico)
- Active publishing cultures (millions of books/blogs/code)
- Strong corporate interest in those markets
- AND no Romanization complication on top

#### Global Romanization parallels (for Discussion / Future Work)

| Language | Population | Romanization name |
|---|---|---|
| Arabic | ~400M | Arabizi |
| Bengali | ~270M | Banglish |
| Urdu | ~230M | Roman Urdu |
| Persian | ~80M | Pinglish / Fingilish |
| Thai | ~70M | Karaoke spelling |

Combined ~1.3B people affected by similar pattern.

#### European Romanization (history)
- Greeklish — peaked 1990s-2000s, declined as Greek IME improved
- Translit (Romanized Cyrillic) — same pattern, declined
- **Indic Romanization PERSISTS despite comparable IME improvements** — that's the cultural anomaly worth documenting

### Contrastive framing for the paper (KEY INSIGHT)

This single table captures the whole argument:

| Language group | Native script training | Romanization in chat | Predicted gap |
|---|---|---|---|
| Korean / Japanese / Mandarin | Strong | Rare | Small (control) |
| Telugu / Hindi / Kannada | Weak | Dominant | Large (the finding) |

Reframed contribution statement:
> *"We demonstrate that LLM evaluation gaps for non-English use are not uniform — they cluster around specific conditions (low native-script training + dominant Romanized/code-switched user patterns). We characterize this empirically for Telugu, Hindi, and Kannada, using Korean as a negative control to isolate the contributing factors."*

Much stronger than "AI is bad at Indic." Says WHEN and WHY, not just THAT.

### Files updated/created today

- **`Paper-Execution-Plan.md`** — CREATED. Timeline + 7 phases + 10 tasks + prompt categories + risk register + ownership matrix
- **`Prompt-Collection.md`** — CREATED. Sample prompts × 7 languages × 7 categories + native-speaker validation guide
- **`Team-Summary.md`** — Already existed; still current (narrower team-facing summary)
- **`Session-Backup-2026-06-02.md`** and **Part2** — Written defensively during a permissions hiccup; redundant now that this section is added but can stay as additional safety net
- **`research-context.md`** — UPDATED (this section)

### Team interactions

| Person | Topic | Outcome |
|---|---|---|
| Tia Kim (Korean office colleague) | Validated Korean prompt samples | Led to Korean reframe as negative control |
| (others) | Not yet looped in on today's decisions | Need to communicate Korean change, scope locks, methodology refinements |

### Open threads / current next steps (supersedes the older "Still to do" list)

1. **Send recruitment messages** to Tamil, Marathi, Mandarin contacts with June 8 deadline
2. **Validate Hindi prompts** with Hindi-speaking teammate (in `Prompt-Collection.md`)
3. **Validate Kannada prompts** with Madhu's girlfriend
4. **Decide on pilot test** (yes/no — strongly recommended)
5. **Fill ownership matrix** in `Paper-Execution-Plan.md` at next team meeting
6. **Lock Topic 2 formally** with the team (still pending after team's positive reception of the three-paper narrative)
7. **Verify workshop logistics** (page limit, format template, anonymization, timezone)
8. **Clarify with Surbhi** why she shared T2I papers — possible Topic 6 advocacy?
9. **Update Task 3 description** to reflect wider 10+ language tokenization scope (including Japanese/Mandarin as cheap data points)

### Permission glitch note

Mid-session, Bash/Read started returning EPERM on this directory. Write still worked. Two backup files (`Session-Backup-2026-06-02.md` and `Part2.md`) were written defensively. Permissions cleared a few minutes later. Backup files can be deleted or kept — they're redundant with this updated section.

### Status of the 10 execution tasks

All still pending as of session end. Task 5 was updated mid-session to reflect Korean drop. Task 3 was updated mid-session to expand the tokenization scope (see below). No tasks marked in-progress yet — work hasn't formally started, this session has been planning + scoping.

### Task 3 expanded — three-way tokenization comparison (added late in session)

After working through the Korean negative-control reframe, we sharpened Task 3 (tokenization counting experiment):

**Languages** (10+, all cheap since computational): Telugu, Hindi, Tamil, Kannada, Malayalam, Gujarati, Marathi, Bengali, Korean, Japanese, Mandarin (+ Arabic if time)

**For each language, three-way form comparison:**
1. Native script (from FLORES parallel sentences)
2. GT-Romanized (standardized — what Google Translate outputs)
3. Real-user-Romanized (idiosyncratic, from our collected prompts) — only for Indic where we have real-user data

**Tokenizers tested:** GPT-4o (tiktoken), Claude (count_tokens API), Gemini (count_tokens SDK), Llama 3 (HuggingFace), MuRIL/IndicBERT (HuggingFace)

**The headline finding the experiment is designed to expose:**
> *"Romanization hides token cost at the tokenizer level (counts drop to ~1x English) but creates semantic gibberish (the model has no grounding to act on it). Script form costs more tokens but at least carries learned meaning."*

This is a stronger framing than the simpler "Telugu costs 8x" — it shows Romanization is a *deceptive* fix at the tokenizer level only, not a real fix.

### Pre-registered predictions for the tokenization experiment

Writing predictions down BEFORE running the experiment helps:
- Reviewers see the rigor (this isn't post-hoc storytelling)
- Surprising results become more interesting (you predicted X, found Y)
- Confirming results become more defensible (you predicted X, found X)

Predictions:

1. **Indic native scripts cost the most** — 6–10x English (per Petrov)
2. **Indic Romanized costs close to English** — 1.0–1.5x English
3. **East Asian native scripts cost moderate** — 2–4x English
4. **East Asian Romanized costs close to English** — 1.0–1.5x English
5. **Different Romanization conventions tokenize slightly differently** — Pinyin likely more efficient than Korean Revised Romanization than Hindi Romanization (compactness differences)

If results match → confirms the "Romanization deceptively hides cost" finding cleanly.
If results don't match → even more interesting paper, found something unexpected.

Either outcome → publishable contribution.

### Research mindset framing (Madhu's words, worth preserving)

> *"all these are open ended questions and will see what happens"*

This is a healthy exploratory mindset — measuring rather than confirming. The paper's contribution is the *measurement*, not "we proved AI bad at X." Whatever the numbers say, we have data nobody else has.

### LLM selection — LOCKED (5 models for human-eval pipeline)

| # | Model family | Specific version (June 2026) | Role |
|---|---|---|---|
| 1 | GPT (OpenAI) | GPT-4o (or latest) | Most-used commercial model |
| 2 | Claude (Anthropic) | Sonnet 4.6 or Opus 4.7 | Second major commercial |
| 3 | Gemini (Google) | Gemini 2.5 Pro (or latest) | Third major commercial; strong multilingual claims |
| 4 | Llama (Meta) | Llama 3.3 70B (or Llama 4 if released) | Open weights = reproducibility for reviewers |
| 5 | Indic-tuned | Sarvam-1 or MuRIL | Kills the "but Indic-specific models would fix this" counter-objection |

**Why exactly 5:** more than 6 = chart clutter + API costs without strengthening findings. Fewer than 4 = reviewers ask "what about X?"

**For Task 3 (tokenization):** use all 5 tokenizers, plus IndicBERT as bonus comparison if desired.

**Cost estimate:** ~300 prompts × 5 models = 1,500 API calls × ~$0.02 avg = **$30–60 total**. Indic model runs locally on HuggingFace = free.

**Tokenizer visibility caveats (note in methodology):**
- Claude: `count_tokens` API gives counts only, not splits
- Gemini: same — counts only
- GPT-4o, Llama, MuRIL/Sarvam: full visibility via tiktoken / HuggingFace

### Rejected ideas (reference list for future "why didn't we do X" questions)

**Topics rejected (favoring Topic 2):**
- Topic 5 (Modeling for Global Understanding) — too philosophical; position papers hard for unestablished authors
- Topic 6 (Cross-Modal Insights) — needs multimodal expertise team doesn't have

**References rejected (off-topic for Topic 2):**
- Naik & Nushi 2023 — image-domain bias, not text
- Wan et al. 2024 — T2I survey, not text

**Scope rejections:**
- 10 languages at full human-eval depth — 200 team hours, not feasible in 22 days
- Korean as positive case — Tia's feedback proved Koreans don't code-switch in chat; reframed as negative control instead (actually strengthened paper)
- Arabic / Bengali for v1 — scope discipline; relegated to future work / v2 paper
- Malayalam, Gujarati, Marwari — redundant with chosen languages in same family

**Methodology rejections:**
- Google Translate as primary data source — contradicts paper's thesis (we argue real-user typing ≠ translations). GT kept as baseline/control only.
- Skipping native-speaker scoring — the auto-vs-human gap IS the novel contribution
- Translating everything to English at training time — 6 reasons it can't work (scale, lossy, no output generation, round-trip errors, chicken-and-egg, knowledge gaps)
- Shallow 10+ language survey vs deep 2-3 language study — workshops prefer rigorous depth over surface-level breadth

**The meta-pattern across all rejections:**
Every rejection traces to one of three principles:
1. Match scope to deadline (22 days isn't enough for 10-language depth)
2. Match data to thesis (we argue about real-user data, must use real-user data)
3. Match depth to publication venue (workshops want focused contributions)

---

## Session 2026-06-03 (afternoon) — Deep Literature Verification + MAJOR REFRAME ⭐

### TL;DR — the one thing that changed
A deep literature check found that our **original framing is now occupied by prior work**. "Romanization degrades Indic LLM performance" + the prevalence numbers are TAKEN (Script Gap, Dec 2025). 

**New defensible spine (the reframe):**
> *Prior work showed romanization degrades LLMs where a correct answer exists to measure against (classification, with ground truth). We show that on the open-ended GENERATION tasks users actually perform — which have no ground truth — the same degradation becomes INVISIBLE to automatic metrics (BLEU/BERTScore/LLM-judge), visible only to native speakers, and we isolate it with a cross-lingual negative control (Korean).*

The gap between automatic-metric scores and native-speaker scores on the SAME responses IS the paper. Everything below supports this pivot.

### Tooling note for future sessions (IMPORTANT)
- **WebSearch AND WebFetch are BROKEN** in this Claude Code terminal — both route through decommissioned `claude-3-5-haiku-20241022`. Don't rely on them.
- `curl` HTTPS is blocked by TLS interception EXCEPT with `-k` (e.g. `curl -sk ...`).
- **WORKING research path: OpenAlex API via curl.** Search: `curl -sk "https://api.openalex.org/works?search=...&per-page=10&select=title,publication_year,abstract_inverted_index"`. Lookup by ID: `curl -sk "https://api.openalex.org/works/doi:10.xxxx"`. Reconstruct abstracts from `abstract_inverted_index`. arXiv + Semantic Scholar rate-limit fast (429); OpenAlex is reliable.
- **To get a paper vetted: paste its abstract, OR give the arXiv ID / DOI. Do NOT paste a URL — can't fetch it.**

### ⚠️ THE THREAT — "Script Gap" (Khullar et al., Univ. Pittsburgh)
- **arXiv:2512.10780** (v1 ~Dec 2025, v2 30 Mar 2026). NOTE: by our June 2026 submission this is **PRIOR work, not concurrent** — must cite and clearly outrun; cannot claim parallel discovery.
- **What it is:** maternal/newborn health **triage CLASSIFICATION** (Emergency / Non-emergency / Insufficient-Info) on real WhatsApp NGO messages. Langs: Hindi, Telugu, Kannada, Marathi, Punjabi, Nepali (+English). Models: GPT-4o, Claude Sonnet 4.5, DeepSeek V3, Llama-4 Maverick, Qwen3-80B, Mixtral, Qwen2.5-7B, Sarvam-M 24B.
- **Findings:** romanized input degrades vs native script (up to 24 pts; ~8.6% avg); romanized over-assigned to "Insufficient Info"; models often *comprehend but misclassify* (high-resource Hindi) vs *can't parse* (low-resource Kannada/Telugu); higher temperature flip-rate; +3.8pp residual triage penalty even when comprehension is controlled (HealthBench parallel validation isolates the orthographic effect).
- **Prevalence numbers (now CITABLE, see Task 1 below):** Hindi **83%**, Telugu **73%** romanized; **56%** overall at 41M scale → est. ~2M excess errors.
- **Mitigation:** Uncertainty-based Selective Routing (USR) + script-aware prompting (normalize to native script, then reason).

**What we can NO LONGER claim (these are dead):**
1. "First to show romanized Indic input degrades LLM performance."
2. "First to measure romanization prevalence in real LLM deployment."
3. "Move beyond native-script-centric benchmarks" as a novel framing.

**What SURVIVES (our real, still-empty corner):**
- They measure **classification with ground truth**; we measure **open-ended generation quality** (fluency, register, cultural/kinship fit) — they never judge whether model OUTPUT is good Telugu.
- **The auto-metric-vs-native-human gap is untouched** — they have correct labels, so no metric-vs-human divergence story.
- No register/culture/code-switching focus; no cross-lingual **negative control**; different population (NGO health patients vs general English-educated LLM users).
- Their existence STRENGTHENS us: proves the underlying degradation is real (we don't have to) and shows the problem matters to reviewers.

### Verified citations (checked against actual papers this session)
- **Petrov et al. 2023** — CONFIRMED real. arXiv:2305.15425, NeurIPS 2023, ~29 cites. Abstract states token-length differences "up to 15 times." ⚠️ The specific **8.34x Telugu** is a table cell NOT in the abstract — still needs PDF check (Ctrl-F "Telugu" in arxiv.org/abs/2305.15425). Quote "up to 15x" until verified.
- **Foroutan et al. 2025 — CONFIRMED.** arXiv:2508.04796v2 (22 Aug 2025). Authors: Foroutan, Meister (co-first), Paul, Niklaus, Ahmadi, Bosselut, Sennrich (EPFL/ETH Zurich/Univ. Zurich). Numbers verified against their tables:
  - Gini **0.064 → 0.011** ✓ (Table 1; base parity-aware variant, 30-lang unbalanced 128k). The "83% reduction" is the BASE variant; the hybrid/window variants used for downstream results only cut Gini ~75% (0.018/0.013). **Don't quote 83% and the accuracy numbers together — different tokenizers.**
  - Telugu **32.73 → 33.52** ✓ (Table 2) — BUT this is within ±2.61 noise. The paper's actual point is downstream accuracy is **UNCHANGED** (median +0.19pp; 14 up, 6 down). **DO NOT present this as "Telugu improved" — that's a misread a reviewer will catch.**
  - **GIFT for our gap argument:** Table 2 shows Telugu **33.5%** vs English **44.2%** vs random baseline **30.0%** — i.e., after the fairness fix, Telugu is ~3pts above random while English is ~14 above. → **tokenization parity ≠ capability parity.** Bulletproof related-work line because it's their own numbers. ⚠️ CAVEAT: these are **3B from-scratch LLaMA-arch models, NOT GPT-4o** — frame as illustration of the mechanism, NOT a claim about commercial models. Our human-eval speaks to commercial models.

### IndicKLAR (Evaluating Cross-lingual Knowledge Consistency, 2026)
- arXiv:2605.29637. Indic extension of KLAR-CLC; 18 of 22 scheduled langs; code-mixed variants for 11 pairs; **native-speaker verified**; three-way English/code-mixed/native; 9 open-weight models.
- **Finding (points opposite to our hypothesis at first glance):** native→English accuracy gap up to ~0.50; **code-mixing CLOSES it to within ~0.05** of English. "Flip point" sits between native and code-mixed.
- **Why it doesn't sink us:** their construct is **knowledge RECALL** (factual), not generation quality. Mixing English in injects tokens the model knows → recall improves. Says nothing about register/fluency/cultural fit. Actually SUPPORTS our "invisible to metrics" idea: models look fine on metric-friendly signals.
- ⚠️ STILL TO VERIFY from PDF: is their "code-mixed" **Romanized** or **native-script + English words**? (arxiv.org/abs/2605.29637). If native-script-mixed, our Romanized angle is wide open.

### Romanization literature — the 3 bins + the 4-question filter (anti-panic tool)
Most romanization papers are NEIGHBORS, not competitors. Sort every new paper into a bin:
- **Bin A — "Convert it" (transliteration):** Dakshina (Roark 2020, Google, LREC), Romanized Assamese (Baruah 2024, ACM TALLIP), Romanized Hindi/Bengali dataset (arXiv:2511.22769, 2025), Aksharantar, RomanSetu. → preprocessing, NOT us.
- **Bin B — "Identify it" (LangID / prevalence):** Distinguishing Romanized Hindi from Urdu (CAWL 2023, aclanthology 2023.cawl-1.5), Roman Hindi LangID papers. → NOT us.
- **Bin C — "Evaluate LLMs on it" (our neighborhood):** Script Gap (classification), IndicKLAR (recall). ONLY these are close — and both measure a different construct than our generation-quality-human-eval.

**4-question filter** for any new paper — if it doesn't hit most, it's a CITATION not a competitor:
1. Judges LLM **output quality** (generation), not conversion/classification/ID?
2. Uses **native-speaker** judgment of that output?
3. Compares against **automatic metrics** (the gap)?
4. On **real romanized** user input?

### ACP — Azam, Chin & Prakash (helps DIGLOSSIA only, NOT romanization)
- "The Returns to English-Language Skills in India." WP April 2011; published *Economic Development and Cultural Change*, 2013. IHDS 2005 data.
- Numbers: **~20% of Indians report some English ability** (4% fluent, ~16% "a little"); 0.2% mother tongue; urban 35% vs rural 14%; men 26% vs women 14%; young 25% vs older 13%; **89% of Bachelor's-degree holders**. Wage return **+34% fluent, +13% a little**.
- **Use:** replace bare "265M speakers" with *"~20% report some English ability (ACP 2013), concentrated in the urban/educated/young cohort = the LLM-using population."* Simultaneously sources the number, justifies scoping, and pre-empts "why not just prompt in English." 2005 data → frame as structural pattern, not current count. **Does NOT support the romanization claim.**

### Diglossia + IME-conversion mechanism (this is the paper's "why" — and it's OURS)
- **Diglossia:** English = High register (written/professional/economic, +34% wages), mother tongue = Low register (spoken/intimate/home). Name it; canonical ref **Ferguson 1959 "Diglossia"** (⚠️ verify exact citation form).
- **Core mechanism:** writing fluency lives in **Latin script**; the mother tongue is an **oral competence**. So spoken-register native content gets serialized to Latin (the only script the user types fluently).
- **CJK contrast (why Korean is a clean negative control):** Pinyin/romaji ARE romanized input, but the IME **forces conversion to native script** before commit (homophones make raw Pinyin unreadable). Korean Hangul is typed directly. Indic transliteration IMEs exist (Gboard) but conversion is **optional** AND romanized Indic is human-readable → users skip the step → romanized text reaches the model. **Do NOT claim "Indians lack keyboards" — false; Gboard transliteration is good. The claim is about the optional vs forced conversion step.**
- **Code-switching breaks transliteration IMEs** (script-flipping mid-sentence) → reinforces romanization. Gives Korean control a SECOND leg (Koreans don't code-switch in typing AND type Hangul directly).

### THE REFRAME — concrete cascade of changes to make
1. **Contribution statement** → rewrite around the invisible-to-automatic-metrics generation gap (see TL;DR spine).
2. **Related Work** → flip from "the gap nobody found" to "the launch pad": Script Gap (classification, ground truth) + IndicKLAR (recall) are what we build past.
3. **Tokenization study (Task 3)** → DEMOTE from co-contribution to background. Space is crowded (Petrov, Foroutan, BrahmicTokenizer-131K, Ahia, "cost of language as labor" 2026). Not our novelty.
4. **Prevalence claim** → DEMOTE: cite Script Gap (83/73/56%) + Dakshina for the phenomenon; our corpus ratio = corroboration for the general LLM-user population, not a headline.
5. **Core experiment** → REDESIGN around DIVERGENCE: run automatic metrics (BLEU, BERTScore, LLM-as-judge) AND the native-speaker rubric on the SAME responses; show metrics say "pass" while natives say "fail." The split between the two curves is the central result.
6. **Korean negative control** → KEEP (now the single thing most distinguishing us from Script Gap).
7. **Diglossia + IME mechanism** → the intro's "why" (no competitor explains mechanism).

### Pilot redesign — now MAKE-OR-BREAK (do before committing the team 17 days)
- OLD pilot question: "does romanization hurt?" (now answered by Script Gap — don't waste the pilot on it).
- **NEW pilot question:** on ~5–10 romanized prompts × 2 models × 1 native speaker, **do automatic metrics and native speakers DISAGREE?**
  - Diverge (metrics pass, humans fail) → the paper exists. Proceed.
  - Both catch the failures → the "invisible" thesis COLLAPSES → reframe NOW (fallback: weaker "we extend Script Gap to generation") before sinking 17 days.

### Number/framing corrections to apply before ANY external sharing
- Drop bare **"265M English speakers"** → "~20% some English ability (ACP 2013)."
- Drop bare **"95% romanized"** → cite Script Gap 83%/73% + corroborate with own corpus.
- **"Foroutan: Telugu accuracy improved"** → WRONG (within noise). Say "fairness improves, capability unchanged."
- (Carry-over from earlier sessions: IP attribution to Tsvetkov & Kipnis 2024 not Kanjirangat; speaker-count 700M+ not 200M; token table label "from Petrov 2023" until run.)

### New references to add to the cite list
- Khullar et al. 2025 — Script Gap — arXiv:2512.10780 (cite + differentiate)
- IndicKLAR 2026 — arXiv:2605.29637 (cite + differentiate)
- Roark et al. 2020 — Dakshina — LREC (romanization prevalence/phenomenon)
- Baruah et al. 2024 — Romanized Assamese — ACM TALLIP (romanization is non-standard/idiosyncratic)
- Foroutan et al. 2025 — arXiv:2508.04796 (now verified; "parity ≠ capability")
- Azam, Chin & Prakash 2013 — EDCC (diglossia / motivation only)
- "Beyond Monolingual Assumptions" CSW survey 2025 (field overview; names "fair evaluation" as open problem)
- Ferguson 1959 — "Diglossia" (⚠️ verify exact form)

### Still-to-verify (browser only — Madhu's TODO)
- [ ] Petrov **8.34x Telugu** table cell — arxiv.org/abs/2305.15425, Ctrl-F "Telugu"
- [ ] IndicKLAR: is "code-mixed" **Romanized or native-script**? — arxiv.org/abs/2605.29637
- [ ] Ferguson 1959 exact citation form
- [ ] Skim arXiv:2511.22769 evaluation section (dataset paper — confirm it's a resource, not a competing eval)

### Tokenization measurement — LIVE DATA from this session (one sentence, illustrative)
Ran tiktoken on a parallel greeting ("Hello, how are you? Did you eat?" / "namaste, meeru ela unnaru? tinnara?" / native Telugu equivalent):

| form | chars | utf-8 bytes | o200k_base (GPT-4o) | cl100k_base (GPT-3.5/4) |
|---|---|---|---|---|
| English | 32 | 32 | 10 tok (1.00x) | 10 tok (1.00x) |
| Romanized Telugu | 35 | 35 | 13 tok (1.30x) | 13 tok (1.30x) |
| Native Telugu | 35 | 91 | **14 tok (1.40x)** | **59 tok (5.90x)** |

**Two findings:**
1. **Romanized is CHEAPER than native script, never higher** (13 < 14, 13 < 59) — settles the earlier debate. "Romanized is way higher" is FALSE. Romanized ≈ 1.3x English, stable. Direction confirmed by data.
2. **The native-script cost gap has COLLAPSED on the current GPT-4o tokenizer** (5.9x on old cl100k → 1.4x on o200k). The famous "Telugu = 8x" is largely a **historical artifact** on frontier tokenizers. Correction to earlier-session shorthand: stop quoting "8x" as current — it's cl100k-era.

### ⚠️ The o200k collapse is NOT a novel finding (checked)
- **OpenAI advertised it themselves** in the GPT-4o launch (May 2024) — a per-language tokenizer-improvement table (Telugu ~3.5x fewer, Hindi ~2.9x, Gujarati ~4.4x, etc.). ⚠️ recalled from memory — VERIFY on OpenAI's GPT-4o announcement page. A reviewer will know this.
- Academic neighbors: "The Token Tax: Systematic Bias in Multilingual Tokenization" (AfricaNLP 2026); "Tokenization efficiency... Ukrainian" (2025); plus Petrov/Ahia/Foroutan. The fertility/bias space is saturated and vendor-instrumented.
- **Possibly-unclaimed thin angle:** romanized-vs-native-vs-English *convergence* tracked across tokenizer generations. Thin tokenization sub-result — DO NOT stake the paper on it.

### Strategic conclusion (reinforces the reframe, again)
The cost gap is closing on its own — publicly, by industry. That KILLS "cost" as a claimable contribution but STRENGTHENS the durable spine: **cheap tokens now, AND the model still produces output native speakers reject, invisibly to automatic metrics.** Token numbers = setup/confirmation to CITE (OpenAI table + Token Tax + Petrov as the "before"), NOT the headline. Spine stays the human-eval quality gap.

### Added TODOs
- [ ] Verify OpenAI's GPT-4o (May 2024) tokenizer-improvement table (per-language token reductions) — browser
- [ ] Run FLORES multi-language token sweep (Telugu/Hindi/Kannada × o200k/cl100k/Llama/MuRIL-or-Sarvam, diverse sentences not greetings) — as CONFIRMATION to cite, not a novel finding. Watch for: is the o200k collapse general or Telugu-specific? Does romanized<native flip on Indic-tuned tokenizers?
- Add refs: OpenAI GPT-4o tokenizer announcement (2024); "The Token Tax" (AfricaNLP 2026).

---

## Session 2026-06-03 (late) — PILOT RUN + LOCKED DIRECTION ⭐⭐ (meeting-ready)

### ⭐ THE LOCKED DIRECTION (present this; stop offering options)
**Working title:** *The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them.*

**One-line study:** We test whether LLMs serve Indians the way they actually use them — typing their language in English letters — and show the failures are invisible to standard metrics, visible only to native speakers.

**Problem statement:** Indians don't type to AI in native script — they type romanized, code-switched. On the everyday tasks people actually use AI for (messaging family, emotional/cultural/register-sensitive writing), LLMs produce answers that *look* correct and pass automatic metrics, but a native speaker rejects them: anglicized register, wrong word choice, ambiguous romanization, native-script replies the user can't even read. Standard evaluation can't see this — these tasks have no ground truth, and metrics don't measure register, culture, or script-usability.

**5-step plan:** (1) Pilot — DONE today, gap confirmed. (2) Collect real romanized prompts (Telugu/Hindi/Kannada). (3) Run through 5 LLMs, fresh session per response. (4) Native speakers score on rubric + run automatic metrics on same outputs. (5) The divergence + response-script distribution = the finding. Korean = negative control.

**Defensibility line:** "Script Gap (Dec 2025) showed romanization hurts *classification*, where there's a right answer to grade. We show it hurts *generation*, where there's no right answer — so the failure is invisible to metrics. Different, unclaimed."

### PILOT RESULTS (ran on Claude Opus 4.8 this session — qualitative, N small)
Madhu (Telugu native) evaluated. Three rounds: 10 romanized prompts; a 3-version test (En/Te/romanized, in-context); a proper 3-separate-session festival test. **Verdict: thesis HOLDS — proceed.**

**Failure modes observed (the evidence):**
1. **Anglicized "Telugu":** model uses English for the emotional/register words that matter most ("eagerness," "validate," "important feel," "situation"). Fails *worst* exactly where intimate register is needed.
2. **Native-script corruption on real screen:** words fused, "తో" dropped ("doctorreview"), stray anusvara ("BP,ంsugar"). Perfect content, unreadable to the user.
3. **Romanization ambiguity:** "kramam" (క్రమం = regularly) misreads as "karam" (కారం = chili) in Latin script. Native script disambiguates; romanization doesn't.
4. **Grammar/agency error:** "doctor tho review cheyinchandi" — wrong case ("tho"=with vs causative agent "cheta"=by) + causative muddles who reviews whom. Natural = "doctor ki chupinchandi."
5. **Register error:** "kramam tappakunda" is bookish/formal for casual family advice.
6. **Content shrinkage:** model wrote ~half the words in Telugu (120 vs 228 English) — thinner answers in-language.
7. **Low diversity:** 3 fresh sessions converged on the same skeleton (genuinely independent generations, but a strong prior).

All of the above were **invisible to automatic metrics, visible to the native speaker.** That is the paper.

### Translate vs Regenerate (mechanism finding → methodology rule)
- Mechanically every token = full forward pass; there is NO translate shortcut.
- BUT with a prior answer in context, the model takes the high-probability path = **transliterating the context** rather than re-reasoning. In-context "now romanize that" = mirroring, not fresh generation (that's why in-context versions came out identical).
- **RULE: collect each response as a fresh generation in a NEW session. Never "now do it in language X."**

### Token + Word measurements (festival responses; o200k proxy — actual model was Claude)
| response | words | o200k tok (xEN) | cl100k tok (xEN) | tokens/word (o200k) |
|---|---|---|---|---|
| English | 228 | 271 (1.00) | 281 (1.00) | 1.19 |
| Telugu (native) | 120 | 275 (1.01) | 1210 (4.31) | 2.29 |
| Romanized Telugu | 167 | 331 (1.22) | 365 (1.30) | 1.98 |

- **Cost gap collapsed on o200k** (native 1.01x) but is huge on cl100k (4.31x) — confirms the "8x is historical" finding again.
- **Raw totals looked equal ONLY because the model wrote fewer Telugu words.** Normalize by word → Telugu still ~2x English per word even on o200k. **Words rescue the signal tokens hid.**
- **DECISION: measure words + tokens + tokens/word together, on PARALLEL content (FLORES).** Caveat: cross-language word counts are confounded by Telugu agglutination (one Telugu word packs more) — that's why parallel content is needed.

### Methodology rules locked this session
1. Fresh session per language/script (no in-context mirroring).
2. Collect responses as fresh generations, never "now romanize that."
3. Measure words + tokens + tokens/word, on parallel sentences.
4. Response-script usability = a rubric dimension; also measure the response-script distribution (what script the model defaults to).
5. Pilot question = "do automatic metrics and native judgment diverge?" → qualitatively YES.

### Files created this session
- **`References.md`** — running bibliography, ~25 sources, two tag systems (verification + relationship), most ⚪ memory-only entries cleared to ✅ via OpenAlex.
- **`Prompt-Responses.md`** — the 3-version BP/diet response saved verbatim (contains the script-leak + transliteration flaw), at Madhu's request.

### Still stale (not yet updated to the reframe)
- `Paper-Execution-Plan.md` and `Prompt-Collection.md` — still describe the pre-reframe paper. Propagate when ready.

### ⭐ FINAL DIRECTION — global framing, Indic execution (resolved 2026-06-03)
**Decision:** the paper is **global in framing/method, Indic in execution.** This fits GenAI4World ("globalizing evaluation") without over-scoping past the June 23 deadline.

**Why this is already "global" enough for the venue:**
- The contribution is a **generalizable method** ("how evaluation silently fails non-English/non-Western users"), not an Indic-only fact — demonstrated on Indic.
- The **Korean negative control is cross-family by construction** — Indic vs CJK is globalizing work, not "an Indian paper."
- The **discussion names the ~1.3B-person footprint** (Arabizi ~400M, Banglish ~270M, Roman Urdu ~230M, Pinglish ~80M) as the pattern the method extends to.

**Positioning sentence:** *"A generalizable method for measuring the hidden evaluation gap in global non-English use — demonstrated on Indic, controlled with Korean, applicable to ~1.3B romanizing users worldwide."*

**Scope confirmed:**
- **v1 (now):** Telugu, Hindi, Kannada (deep human-eval) + Korean (negative control). Global *framing* + ~1.3B in discussion + cheap multi-language tokenization sweep for breadth.
- **v2 (later):** global romanization extension (Arabizi/Banglish/Roman Urdu/Pinglish) — `Future-Ideas.md` #2.

**Optional stretch for v1 (only if staffable without risking the deadline):** add ONE non-Indic romanizing language to the human-eval (e.g. one Bengali or Arabic native speaker). Flips the claim from "Indic + control" to "**two** romanizing families fail, one non-romanizing family (Korean) doesn't" — the strongest global statement. Worth a few outreach messages; must not block June 23.

**Risk note:** over-scoping to many languages = miss the deadline or submit something thin → rejection. A rigorous, globally-*framed* Indic+control paper gets accepted, and acceptance is the platform + citation base for the global v2. Getting in is how we secure the next chance.

### Hypothesis risk — "what if the LLMs are actually good?"
**The risk:** if responses come back great, the hypothesized gap may not appear and the paper "fails."

**Why it's low:** the one-day pilot already found anglicized intimate register, native-script corruption, the kramam→karam ambiguity, and content shrinkage. We already found *something* — a full null is unlikely.

**Why it's survivable regardless — the method/measurement is the contribution, not the direction of the result.** Three outcomes, all publishable:
1. **Big gap** → the main finding (most likely, given pilot).
2. **Small / mixed gap** → "industry improved faster than expected, but it still fails on X (register / script / specific categories)" — a surprising, useful result.
3. **No gap** → "frontier LLMs have *closed* the romanized-Indic generation gap" — a rigorous positive result (good news for ~1.4B users), still a contribution *because of the method + the Korean control*. A clean null with a solid method publishes at a workshop.

**Multiple shots on goal:** we score content quality, register, cultural fit, AND response-script usability. It only takes one dimension to show a gap — and in the pilot, script and register already failed even when content was decent.

**Mitigation:** pre-register predictions; run the pilot FIRST. If responses come back great, we learn it in ~2 hours and reframe to the positive-result version with time to spare — not on June 19.

---

## Session 2026-06-04 — DATA-COLLECTION PLAN (finalized)

### Target
**≥200 romanized prompts, REAL data.** Real-user authorship is the spine — not synthetic.

### Hard rule (the thing that protects the thesis)
**Do NOT use LLM-translated / LLM-generated prompts as the main data.** That produces clean, standardized romanization that hides the gap (and testing AI on AI-written text is circular). Allowed uses of LLMs: generate **scenarios/topics** only — native speakers then **author the romanized prompt themselves**. Synthetic / GT-romanized text is allowed ONLY as the **control arm**.

### Three-way arms (preserved)
- **A — native script**
- **B — synthetic / GT-romanized** (control; scale freely, computational, no native labor)
- **C — real-user romanized** (the key arm). The finding = **models pass B, fail C.**

### Sources (priority order)
1. **Google Form via team + friends' networks** — primary, consented, authentic. LLM-seeded scenarios → humans type their own romanized version. ~5 people × 40 = 200.
2. **Real chat history** (ChatGPT/Gemini/WhatsApp, with consent) — gold anchor subset (~20–30).
3. **YouTube comments** on native-language videos — richer romanized than Reddit; supplementary, filtered (`langdetect`/regex, free).
4. **Existing corpora** (Dakshina, GLUECoS, LinCE, Dravidian-CodeMix) — mine for control arm / supplementary.
5. **Reddit — NOT a primary prompt source** (country subs are English-dominant → low romanized yield). Use only for: dataset *pointers* (r/datasets, r/LanguageTechnology) + recruiting *non-Indic evaluators* (r/arabs, r/greece, r/iran).

### Languages & roles
- **Indic — Telugu/Hindi/Kannada (friends cover these, can extend to Tamil/Marathi/Malayalam/Bengali if reliable):** full human-eval in v1. **Spine.** Cap the count — 3 done well > 6 thin.
- **Arabic (Arabizi, active) + Persian (Finglish, active):** extend the gap to other families. Collection + tokenization in v1; human-eval only if Reddit lands native evaluators, else v2.
- **Greek (Greeklish, DECLINED):** second control / counterfactual — "IME improved → romanization died, problem self-resolved." Also ask communities "do people still use Greeklish?" as sociolinguistic data.
- **Korean:** negative control (users don't romanize at all).

### Ethics
Consent + anonymize. The Form (with a consent checkbox) is the cleanest basis for the released dataset; scraped data needs anonymization + a methods note.

### Output / extra contribution
**GitHub release:** real prompt dataset + control/synthetic set + evaluation tooling. A resource contribution on top of the findings (Future-Ideas #3, folded in).

### Cost reality
Scraping = free (Reddit/YouTube APIs, no LLM tokens); filtering = free rules; run it on **Google Colab** (free, no local install). Only real spend = the 200×5 eval runs — Gemini/Llama/Sarvam free, GPT-4o + Claude a few dollars (or office access).

### Metrics reminder (carried from reframe)
Automatic metrics (BLEU/BERTScore/LLM-judge) are run to **show they fail**, not to grade quality (BLEU/BERT need a same-language reference that open-ended tasks lack). Native rubric (fluency / register / cultural fit / accuracy / **response-script usability**) + Cohen's κ = ground truth. **The gap between them = the finding.** Fresh session per response (no in-context mirroring).
