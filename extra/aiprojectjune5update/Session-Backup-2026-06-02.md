# Session Backup — 2026-06-02 (afternoon, before laptop restart)

**Purpose:** Comprehensive backup of today's session work, captured before Madhu's laptop restart. After restart, merge the relevant pieces of this file into `research-context.md`.

**Permissions note at time of backup:** Bash/ls and Read on this directory were returning EPERM errors mid-session. Only Write succeeded. May be a macOS TCC issue tied to whatever "issues" prompted the restart.

---

## Quick orientation for future Claude sessions

If you're a future Claude reading this after restart, the four primary working files in this project are:

1. **`research-context.md`** — Master context file. History of all sessions, refined understanding of papers, locked decisions.
2. **`Paper-Execution-Plan.md`** — Execution plan with timeline (June 23 deadline), 7 phases, 10 tasks, prompt categories, risk register, ownership matrix.
3. **`Prompt-Collection.md`** — Sample prompts per language (Telugu, Hindi, Kannada, Korean, Tamil, Marathi, Mandarin), guide for native-speaker contributors.
4. **`Team-Summary.md`** — Narrower team-facing summary, can be shared via email.

This file (`Session-Backup-2026-06-02.md`) is additive — it captures today's session work that hadn't yet been merged into research-context.md when permissions broke.

---

## Today's session at a glance

**Date:** 2026-06-02 (afternoon)
**Mode:** Execution planning + key methodology refinement based on native-speaker feedback
**User:** Madhu Beesetty (note: earlier sessions used "Mahesh" in research-context.md teaching preferences — that may be incorrect. Madhu is the actual name.)

### What we did

1. Confirmed paper submission timeline: **June 23 deadline, June 20 internal final draft**
2. Locked language scope for human evaluation (3 confirmed + 3 pending, 1 negative control)
3. **Reframed Korean** from positive case to negative control based on Tia Kim's feedback
4. Reviewed 4 references shared by teammates
5. Created 2 new files (`Paper-Execution-Plan.md`, `Prompt-Collection.md`)
6. Worked through several conceptual questions about WHY this problem exists

---

## Locked decisions today

### Language scope (human evaluation)

| Language | Status | Prompts target | Owner |
|---|---|---|---|
| Telugu | **Confirmed** | 75–100 | Madhu (native) |
| Hindi | **Confirmed** | 75–100 | Team-internal |
| Kannada | **Confirmed** | 50 | Madhu's girlfriend |
| Tamil | *Pending* | 30–50 | Office colleague — must confirm by June 8 |
| Marathi | *Pending* | 15–20 | Office colleague — must confirm by June 8 |
| Mandarin | *Pending* | 15–20 | Office colleague — must confirm by June 8 |
| Korean | **Negative control only** | 0 (human eval) | Tokenization-only in Task 3 |

**June 8 EOD = hard deadline** for pending contributors to confirm. Anything without confirmation by then drops from human-eval scope (still kept in tokenization).

### Korean reframe — important detail

Madhu showed Tia Kim (Korean office colleague) the Korean sample prompts. Tia's feedback:

- Korean Koreans do NOT code-switch English+Korean in chat. They use English loanwords ("bus", "OK") but don't mix mid-sentence.
- Even Korean-Americans (like Tia herself) default to monolingual when typing to ChatGPT.
- Code-switching for Korean-Americans is a SPOKEN behavior, not a typed one.
- K-drama portrayal of upper-class code-switching is unrealistic for everyday digital chat.

**Decision:** Korean becomes the negative control in the paper:
- Tokenization-only (Task 3), no human evaluation needed
- Predicted: token cost asymmetry persists but evaluation gap is small (because no code-switching pattern to fail on)
- This STRENGTHENS the paper — isolates code-switching specifically as the gap-driver, rules out "AI is just bad at any non-English" as alternative explanation

**Discussion-section observation worth recording:**
> Modality preference differs across bilingual communities. Korean-Americans code-switch in speech but default to monolingual typing. Indians code-switch in both. The Romanization/code-switching pattern we measure is culturally specific, not a universal bilingual phenomenon.

### Methodology refinements (locked)

**Two complementary contributions in the paper:**

1. **WIDE tokenization study** — 10+ languages, computational, cheap. Replicates Petrov + extends with Romanized/code-switched variants nobody else has measured.
2. **DEEP human-evaluation study** — 3-4 languages, requires native speakers. The novel contribution.

**Three-way comparison** for tokenization analysis:
- Native script (e.g., తెలుగు) from FLORES
- GT-Romanized (standardized): "Namaste, meeru ela unnaru?"
- Real-user Romanized (idiosyncratic): "namaste meeru ela vunnaru?" or "namste ela unnaru?"

If we can show LLMs handle #1 and #2 well but fail on #3, that's the paper's central finding in a single graph.

**Real user data ONLY** for human evaluation. Google Translate is allowed for:
- Baseline/control comparison
- Reference text for automatic metrics (BLEU/BERTScore)
- Tokenization counting (parallel sentences across languages)

GT is NEVER used as a substitute for the real-user prompt data.

**Pilot test recommended** before committing 18 days:
- 5 prompts × 2 models × 1 native speaker per language
- ~2 hours total
- Three possible outcomes: confirms hypothesis (proceed) / refutes hypothesis (reframe as "industry improved") / shows subtle gap (most interesting outcome)
- Cheap insurance against the hypothesis being wrong

### Scope discipline (locked)

- Do NOT expand to Arabic, Bengali, or other major Romanization-affected languages for v1
- Do NOT do human-eval on 10+ languages (only tokenization can be wide)
- Position paper as "first of methodological series" — broader feel without scope expansion
- Discussion section can name Arabizi (~400M), Banglish (~270M), Roman Urdu (~230M), Pinglish (~80M) as future work, giving the paper ~1.3B total population reach in implication

---

## New references reviewed today (from teammates)

### 1. EfficientXLang — Ahuja, Vaddamanu, Patra et al. (June 2025) — arXiv:2507.00246

**Title:** "Towards Improving Token Efficiency Through Cross-Lingual Reasoning"

Tests DeepSeek R1, Qwen 2.5, Qwen 3 on math reasoning across 7 typologically diverse languages. Finding: reasoning in non-English languages uses FEWER tokens AND preserves accuracy.

**Relevance:** HIGH but nuanced. The paper is about reasoning chains, not user input. Their finding (non-English more efficient for reasoning) seemingly contradicts Petrov but is actually orthogonal — different domain.

**Must address in related work** or reviewers will use it as counter-evidence. Suggested framing:

> *"EfficientXLang shows reasoning-chain efficiency in well-represented languages — orthogonal to our concern about user-facing input in low-resource and dialectal/Romanized forms."*

### 2. Naik & Nushi 2023 — arXiv:2304.06034 — "Social Biases through the Text-to-Image Generation Lens"

Image-domain bias paper. **DROP — off-topic for Topic 2.** Shared by Surbhi — possibly advocating for Topic 6 (cross-modal) pivot. Worth clarifying.

### 3. Wan, Subramonian, Ovalle et al. 2024 — arXiv:2404.01030 — "Survey of Bias In Text-to-Image Generation"

T2I survey. **DROP — off-topic for Topic 2.** Same Surbhi-shared signal.

### 4. OpenAI Developer Community thread — "Explosion in the number of tokens / words generated"

French developer "Ailogik" reports: 159 French words → 277 tokens = 74% more than expected.

**Relevance: HIGH for narrative.** Can't cite forum thread formally but it's a perfect motivating anecdote for the introduction — real developer, real costs, real-world evidence of the cost gap.

---

## Conceptual insights from today (reusable in paper sections)

### Why models can't just be trained in English alone (6 reasons)

1. Scale prohibitive (~15T training tokens; translating would cost billions $ + months)
2. Translation is lossy (cultural nuance, kinship terms, honorifics all degrade)
3. Model couldn't generate non-English output if all training were English
4. Round-trip translation compounds errors
5. Chicken-and-egg: need a high-quality translator first, which requires a multilingual model
6. Not all knowledge exists in English (medical/legal/literary corpora in many languages)

### Why Romanized Indic isn't in training data (4 reasons)

1. Hard to capture at scale (mostly WhatsApp/private chat, not public web)
2. Data cleaning pipelines treat it as noisy English and filter it out
3. No standardization — every user spells idiosyncratically ("manam"/"manamu"/"manmu")
4. No explicit cross-script pairing — model can't learn "manam"="మనం" without supervision

### Why Korean/Japanese/Mandarin work better than Indic in LLMs

- Strong native-script training data (Naver, Kakao, Baidu, Niconico — huge native-script corpora)
- Active publishing cultures (millions of Korean/Japanese/Chinese books, blogs, code)
- Strong corporate interest in those markets
- AND no Romanization complication on top of the script issue

### Global Romanization parallels (for Discussion / Future Work)

| Language | Population | Romanization name |
|---|---|---|
| Arabic | ~400M | Arabizi / Arabish |
| Bengali | ~270M | Banglish |
| Urdu | ~230M | Roman Urdu |
| Persian/Farsi | ~80M | Pinglish / Fingilish |
| Thai | ~70M | Karaoke spelling |

**Combined: ~1.3B speakers affected by a similar pattern.** Use this number in the Discussion to widen the paper's implication footprint without expanding its data scope.

### European Romanization (history) — useful contrast

- **Greeklish** — peaked 1990s-2000s, declined as Greek IME improved
- **Translit** (Romanized Russian/Cyrillic) — peaked 1990s-2000s, declined as Cyrillic IME improved
- **Key contrast for the paper:** these declined as input methods improved. Indic Romanization PERSISTS despite comparable IME improvements. That persistence is the cultural anomaly worth documenting.

---

## Contrastive framing for the paper (emerged today — KEY INSIGHT)

This single table captures the paper's argument:

| Language group | Native script training | Romanization in chat | Predicted gap |
|---|---|---|---|
| Korean / Japanese / Mandarin | Strong | Rare | Small (control) |
| Telugu / Hindi / Kannada | Weak | Dominant | Large (the finding) |

Reframed contribution statement:

> *"We demonstrate that LLM evaluation gaps for non-English use are not uniform — they cluster around specific conditions (low native-script training resources + dominant Romanized/code-switched user patterns). We characterize this empirically for Telugu, Hindi, and Kannada, using Korean as a negative control to isolate the contributing factors."*

That's much stronger than "AI is bad at Indic." It says: *"We measured WHEN and WHY the AI is bad at non-English, not just THAT it is."*

---