# START HERE — Project Handoff (portable)

**Working title:** *The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them*
**Venue:** GenAI4World @ COLM 2026 · **Submission:** June 23, 2026 · **Internal draft:** June 20
**Owner:** Madhu Beesetty (+ team of 4)

> This doc is a self-contained quickstart. Deep detail lives in the companion files below. To resume with an AI assistant, paste this doc (or say "read research-context.md and continue").

## Companion docs (in this folder)
- **research-context.md** — full decisions, reframe, pilot results, data plan (the master file).
- **References.md** — running bibliography, ~25 sources, verification + cite-priority tags.
- **Future-Ideas.md** — follow-up paper backlog (13 ideas, STRONG/MEDIUM/PARK).
- **Prompt-Responses.md** — saved pilot output (the flawed Telugu response).
- **Paper-Execution-Plan.md / Prompt-Collection.md** — ⚠️ STALE (pre-reframe; ignore until updated).

## The one-liner
LLMs fail when Indians type their language in English letters (romanized), on everyday generation tasks — and the failures are **invisible to automatic metrics**, visible only to native speakers. We measure that gap, with Korean as a negative control.

## Problem statement
Indians type to AI romanized/code-switched, not in native script. On open-ended tasks (messaging family, emotional/cultural/register-sensitive writing) LLMs produce answers that *pass* automatic metrics but a native speaker rejects: anglicized register, wrong word choice, ambiguous romanization, native-script replies that are unreadable on the user's screen. These tasks have no ground truth, so metrics can't see it.

## The pipeline (5 steps)
1. Pilot — DONE (gap confirmed qualitatively).
2. Collect ≥200 **real** romanized prompts (Telugu/Hindi/Kannada).
3. Run through 5 LLMs, **fresh session per response**.
4. Score each response **twice**: automatic metrics + native-speaker rubric.
5. **The gap between the two scores = the finding.** Korean control should show no gap.

## Data-collection plan (finalized)
- Target: **≥200 real romanized prompts.** Real-user authorship is the spine.
- **HARD RULE:** no LLM-generated/translated prompts as main data (clean = hides the gap, and circular). LLM may seed *scenarios* only; humans **author** the romanized text. Synthetic = control arm only.
- **Three arms:** A native script · B synthetic/GT-romanized (control) · C real-user romanized (key). Finding = models pass B, fail C.
- **Sources (priority):** 1) Google Form via team+friends (primary, consented) 2) real chat history (gold) 3) YouTube comments (filtered) 4) corpora (Dakshina/GLUECoS/LinCE/Dravidian-CodeMix) 5) Reddit (low yield — use for dataset pointers + non-Indic evaluators, not prompts).
- **Ethics:** consent + anonymize; Form is cleanest.

## Languages & roles
- **Indic — Telugu/Hindi/Kannada (friends cover; extendable):** full human-eval. **Spine.** Cap count (3 well > 6 thin).
- **Arabic (Arabizi) + Persian (Finglish):** extend the gap; collection+tokenization in v1, human-eval if evaluators found, else v2.
- **Greek (Greeklish, declined):** control/counterfactual (IME improved → romanization died).
- **Korean:** negative control (no romanization).

## The 5 models + cost
- **Free:** Gemini (Google AI Studio), Llama (Groq free / HF local), Sarvam-M (HF local) — *use Sarvam-M for generation, NOT MuRIL (MuRIL is an encoder, tokenization only)*.
- **Paid (~a few $ at this scale, or office access):** GPT-4o, Claude.
- Token counting is **free & offline** (`tiktoken` for GPT, HuggingFace for open models) — no API needed. Run on **Google Colab** (free).

## Methodology rules (don't break these)
- Real prompts, not synthetic, for arm C.
- Fresh session per response (no in-context mirroring — it transliterates instead of regenerating).
- BLEU/BERTScore are run to **show they fail**, not to grade (no same-language reference for open-ended tasks).
- Native rubric = fluency · register · semantic accuracy · cultural fit · **response-script usability** + binary accept/reject.
- Inter-rater reliability: 20% double-scored, report **Cohen's κ**.
- Measure **words + tokens + tokens/word** on parallel content (words reveal content shrinkage that tokens hide).

## Next concrete actions (in order)
1. **Get ~30 real prompts** and run the pilot proper (metrics vs your native judgment must diverge). This gates everything.
2. Ship the **Google Form** to team + friends' networks.
3. (Optional) Run the **Reddit/YouTube scraper** on Colab (free) for supplementary data.
4. Update the two stale planning docs to the reframe.
5. Recruit non-Indic evaluators (Arabic/Greek/Persian) via Reddit if pursuing those in v1.

## Setup on this laptop
- **Local coding model:** Ollama + `qwen2.5-coder` (7B if 16GB RAM, 14B+ if 32GB; check for Qwen3-Coder). Optional: Continue.dev in VS Code for offline coding help.
- **Scraping/eval:** Google Colab (free, no install) — PRAW for Reddit, `tiktoken`/HF for tokens, `langdetect`+keyword lists for romanized filtering (note: standard langID misreads romanized Indic as English — use per-language keyword filters).

## Risk (documented)
If LLMs turn out good → not a failure. Three publishable outcomes: big gap / small-mixed gap / no gap ("frontier closed it" — still a contribution via the method + control). Pilot first to find out cheaply.
