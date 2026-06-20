# Problem Statement — LOCKED (2026-06-03)

**Paper:** GenAI4World @ COLM 2026 · Topic 2 (Evaluation Beyond Performance)
**Chosen spine:** Metrics-vs-humans divergence on Romanized/code-mixed Indic generation.

---

## The problem statement (formal)

> Standard automatic metrics (BLEU, BERTScore, LLM-as-judge) assign passing scores to LLM
> responses on Romanized and code-mixed Telugu, Hindi, and Kannada **generation** tasks,
> while native speakers judge those same responses unusable. Because these are open-ended
> generation tasks with no ground-truth answer, the failure is **invisible to automatic
> evaluation** and visible only to native speakers. We quantify this metric-vs-human
> divergence and use **Korean as a cross-lingual negative control** — a language whose
> speakers type in native script and do not code-switch — to isolate Romanization and
> code-switching as the driver, rather than "non-English" in general.

## One-line version (for abstract / pitch)

> *Models can pass every standard evaluation while systematically failing real Indian-language
> users — and we show the standard metrics themselves are blind to it.*

---

## Contributions (what we claim)

1. **The divergence finding.** We measure the gap between automatic-metric scores and
   native-speaker scores on the *same* model outputs, for real Romanized/code-mixed prompts.
   The gap is the central result.
2. **A native-speaker generation rubric** (fluency, register, semantic accuracy, cultural fit
   + binary "would you use this?") that other researchers can reuse for Indic generation eval.
3. **A cross-lingual negative control (Korean)** that isolates Romanization/code-switching as
   the cause and rules out the "AI is just bad at any non-English" alternative explanation.
4. **A mechanism (diglossia + optional-vs-forced IME conversion)** explaining *why* Romanized
   input reaches the model for Indic but not CJK — the "why" no competitor explains.

## What is explicitly NOT a contribution (demoted to background)

- Tokenization cost/fertility (Petrov, Foroutan, o200k collapse) — crowded, vendor-instrumented, and points the *opposite* way (Romanized is cheaper). Setup only.
- Romanization prevalence numbers — cite Script Gap (83% Hindi / 73% Telugu) + Dakshina; our corpus only corroborates.
- "First to show Romanized degrades LLMs" — taken by Script Gap. We build past it, not claim it.

---

## How it differs from the closest prior work

| Prior work | What they measure | Our difference |
|---|---|---|
| Script Gap (Khullar 2025) | Classification (triage) with ground-truth labels | We measure open-ended **generation** with no ground truth |
| IndicKLAR (2026) | Factual **recall** | We measure generation **quality** (register/fluency/culture) |
| RomanSetu / RomanLens | Romanization as efficiency/representation gain | We measure user-facing **output acceptability**, not efficiency |
| Petrov / Foroutan | Tokenization cost & fairness | Token parity ≠ capability parity; cost is not our claim |

The 4-question competitor filter: a paper only competes with us if it (1) judges generation output quality, (2) uses native-speaker judgment, (3) compares against automatic metrics (the gap), (4) on real Romanized input. Nothing found hits all four.

---

## The gate (read this before committing the team)

This problem statement is **only valid if the pilot shows divergence.** Run `Pilot-Kit.md` first:

- **Metrics and natives diverge** (judge passes responses natives reject) → this statement holds. Proceed: lock Topic 2 with the team, recruit, run the full study.
- **Metrics and natives agree** → the "invisible" claim collapses. Fall back to the safety net below — *same data, weaker claim, still publishable.*

**Safety net (automatic fallback, no extra work):** "We extend Script Gap from classification to open-ended generation, confirming via native-speaker evaluation that Romanized-input degradation persists on the tasks users actually perform." Uses the identical collected prompts and scores. Worst case is still a paper.

---

## Scope (locked)

- Human-eval languages: **Telugu, Hindi, Kannada** (+ pending Tamil/Marathi/Mandarin by June 8).
- Negative control: **Korean** (tokenization + small generation set, no full human-eval).
- Models: GPT-4o, Claude, Gemini, Llama 3.3, one Indic-tuned (Sarvam/MuRIL).
- Data: real user prompts only; Google Translate as baseline/control, never as source data.

## Immediate next step

Run the pilot (`Pilot-Kit.md`). That single result decides whether this is the paper or whether you reframe to the fallback. Do it before asking anyone to commit 17 days.
