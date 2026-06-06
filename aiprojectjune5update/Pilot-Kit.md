# Pilot Kit — Metrics-vs-Humans Divergence Test

**Purpose:** Settle, in ~2–3 hours, the one question the whole paper now rests on:

> On open-ended Romanized Telugu generation tasks, do **automatic metrics (LLM-as-judge)** and a **native speaker** DISAGREE about output quality?

- **They diverge** (judge says pass, native says fail) → the "invisible to automatic metrics" thesis holds. Commit the team to the 17-day plan.
- **They agree** → the thesis collapses. Reframe NOW (fallback: "we extend Script Gap to generation") before sinking 17 days.

This is solo work. No API keys, no recruitment, no budget. Use the ChatGPT and Claude chat UIs by hand.

---

## Why these prompts (read before running)

The reframe says prior work already covered **classification** (Script Gap) and **factual recall** (IndicKLAR) — tasks with a ground-truth answer. Our untouched corner is **open-ended generation**, where there is no correct answer to check against, so automatic metrics can only judge surface plausibility.

So every pilot prompt below is a **generation task** — drafting, explaining, rewriting, register-shifting — *not* a factual question. If you swap in Q&A prompts you will accidentally re-test Script Gap's territory and the pilot won't mean anything. Keep them generative.

All prompts are Romanized colloquial Telugu (with natural code-switching), because that's the real-user input the paper is about.

---

## Step 1 — The 8 prompts

Send each one **as-is** to both models. Do not clean them up, do not add "please respond in Telugu" — real users don't. One fresh chat per prompt (no shared context).

| ID | Category | Prompt (send exactly as written) |
|---|---|---|
| P1 | Draft / casual register | `mowa ki late avtundi dinner ki ani amma ki oka casual telugu message draft chey` |
| P2 | Register shift (formal) | `naa boss garki leave kavali repu, oka polite formal telugu lo message rayi` |
| P3 | Explain in native register | `UPI ela work avtundo 60 years paiina unna maa thatha ki simple telugu lo explain chey` |
| P4 | Code-switched drafting | `naa friend birthday ki funny ga wishes cheppali, telugu lo but keep it casual not too formal` |
| P5 | Cultural / kinship | `atta gariki sankranti ki em gift ivvali, oka chinna respectful telugu message tho pampali` |
| P6 | Emotional / venting reply | `rendu rojulnunchi sariga nidra ravatledu, stress ga undi — naaku telugu lo oka supportive reply ivvu` |
| P7 | Rewrite / tone softening | `ee message ni soft ga marchu: "nuvvu cheppindi correct kadu, malli chey"` |
| P8 | Idiom / wordplay | `"avunu kada ante kadu antaru" anే saying ni oka real-life situation tho telugu lo explain chey` |

Tip: also keep P1–P8 handy in romanized form so you can paste fast.

---

## Step 2 — Collect responses

You'll have 8 prompts × 2 models = **16 responses**. Paste each into the response log (bottom of this file), labeled e.g. `P1-GPT`, `P1-Claude`.

Note for each whether the model replied in: native Telugu script / Romanized Telugu / English / mixed. (This is itself a finding — a model that silently switches to English is already failing the user.)

---

## Step 3 — Score with the AUTOMATIC metric (LLM-as-judge)

This is the metric most likely to *falsely* pass a bad response, so it's the right one to stress-test. Skip BLEU/BERTScore for the pilot (they need reference texts; add them only if the full study proceeds).

Open a **fresh** chat (use GPT-4o as the judge, or whichever model you did NOT generate the response with, to avoid self-grading bias). Paste this judge prompt, filling in the original prompt + the response:

```
You are evaluating the quality of an AI assistant's response to a user
who wrote in Romanized/colloquial Telugu.

USER PROMPT:
<paste the original prompt, e.g. P1>

AI RESPONSE:
<paste the model's response>

Rate the AI RESPONSE on a 1–5 scale for each dimension (5 = excellent):
- Fluency: is it natural, well-formed Telugu?
- Register appropriateness: does it match the casual/formal level the user used?
- Semantic accuracy: does it actually do what the user asked?
- Cultural fit: are kinship terms, honorifics, festivals, idioms handled correctly?

Return ONLY this, no explanation:
Fluency: X
Register: X
Semantic: X
Cultural: X
Overall (avg): X.X
```

Record the judge's 4 scores + overall for each of the 16 responses.

---

## Step 4 — Score as the NATIVE SPEAKER (you)

Score the **same 16 responses** yourself on the **same 4 dimensions, same 1–5 scale**. Score honestly as a user, not as a researcher hoping for a result. Then add the binary flag that automatic metrics can't capture:

> **Would you actually accept and send/use this response as-is?  YES / NO**

That accept/reject flag is the crux — it's the human judgment no metric reproduces.

---

## Step 5 — The divergence analysis (the actual result)

For each response, compute **Gap = (LLM-judge Overall) − (Your Overall)**.

Then look at three things:

1. **Mean gap.** A consistently positive gap (judge scores higher than you) = metrics are too generous = thesis supported.
2. **The accept/reject contradiction count.** How many responses did the LLM-judge score ≥4 ("pass") that you flagged **NO** ("would not use")? This is the headline number. Even 4–5 out of 16 is a strong pilot signal.
3. **Direction consistency.** Does the judge over-score *systematically* (most/all responses) or only on a couple? Systematic = real effect; scattered = noise.

### Decision rule

| Pilot outcome | What it means | Action |
|---|---|---|
| Judge systematically scores higher; several "judge-pass / native-reject" cases | Divergence is real → **the paper exists** | Proceed: lock Topic 2, recruit, commit 17 days |
| Judge and you broadly agree (gaps near 0, few/no contradictions) | "Invisible" thesis collapses | **Reframe before committing.** Fallback: "we extend Script Gap to generation," or pivot the angle |
| Mixed / subtle (small but real gap on register & cultural fit only) | Most interesting outcome — gap is dimension-specific | Proceed, but narrow the paper's claim to the dimensions that diverged |

---

## Scoring sheet

Fill this in as you go. (LLM = automatic judge, Me = native.)

| ID | Model | Reply lang | LLM Overall | My Overall | Gap (LLM−Me) | I'd use it? |
|---|---|---|---|---|---|---|
| P1 | GPT | | | | | |
| P1 | Claude | | | | | |
| P2 | GPT | | | | | |
| P2 | Claude | | | | | |
| P3 | GPT | | | | | |
| P3 | Claude | | | | | |
| P4 | GPT | | | | | |
| P4 | Claude | | | | | |
| P5 | GPT | | | | | |
| P5 | Claude | | | | | |
| P6 | GPT | | | | | |
| P6 | Claude | | | | | |
| P7 | GPT | | | | | |
| P7 | Claude | | | | | |
| P8 | GPT | | | | | |
| P8 | Claude | | | | | |

**Summary:** mean gap = ____ | judge-pass / native-reject count = ____ / 16 | verdict = ____

---

## Response log

Paste raw responses here so the pilot is reproducible / shareable with the team.

### P1 — GPT
```

```
### P1 — Claude
```

```
### P2 — GPT
```

```
### P2 — Claude
```

```
*(continue for P3–P8…)*
