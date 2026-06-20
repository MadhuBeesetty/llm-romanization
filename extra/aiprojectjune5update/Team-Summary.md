# Our Paper Proposal — What I'm Pitching

Hey team,

Pulling together where I'm landing on our paper, so we can decide as a group whether to go this direction or push back.

## The pitch

**Standard evaluation benchmarks give models a "pass" for Telugu and Hindi, but they don't measure how real Indian users actually use AI. We can prove this gap exists and propose how to close it.**

The three papers we've been reading (Petrov, Kanjirangat, Foroutan) all study clean, formal, monolingual Telugu and Hindi. Even Foroutan's parity-aware BPE — the closest thing to an infrastructure fix — only works on text that looks like a textbook. None of them touch the way people actually type:

- Code-switching ("can you reschedule mana meeting to tomorrow?")
- Romanized script ("manam ikkada yem madladathunamo neeku ardam avthunda?")
- Colloquial spoken register

That's our gap. Models pass every standard test and still fail real users. We can show that empirically.

## Why this gap is the right one to pick

A few reasons:

1. **It survives Foroutan.** Even if every model adopted parity-aware tokenization tomorrow, the evaluation gap stays. Our contribution is time-resilient.
2. **It plays to our unique asset.** Native Telugu and Hindi speakers — that's something most research teams writing in this space don't have direct access to.
3. **It's concrete enough to ship at a workshop.** Not a position paper, not a giant dataset effort — just a measurable gap nobody's measured yet.
4. **The workshop explicitly calls out code-switching as an open problem.** We're directly on their wavelength.

## Methodology

Recommended path (Option A — lower effort, high impact):

**1. Collect 100 to 200 real prompts** from Telugu and Hindi native speakers (us + our connections). Mix should cover:
- Romanized Telugu and Hindi
- Code-switched (English + Telugu/Hindi)
- Colloquial / spoken register
- Realistic everyday use cases — questions, planning, drafting messages, venting, etc.

**2. Run them through 4 to 5 major LLMs** — GPT-4o, Gemini, Claude, Llama 3, plus ideally one Indic-tuned model for comparison.

**3. Score the outputs two ways:**
- Standard automatic metrics (BLEU, BERTScore, English LLM-as-judge) — these will mostly give a pass
- Native-speaker rubric — fluency, register appropriateness, semantic accuracy, cultural fit

The delta between the two scores is the paper's central finding.

**4. Propose a lightweight evaluation rubric** that other researchers can apply to their own Indic-language work. This is our methodological contribution beyond just measuring the gap.

Optional stretch (Option B — higher effort, higher payoff): clean up the collected prompts into a small reusable evaluation dataset and release it publicly. Becomes an instant citation magnet for anyone doing Indic NLP. Worth doing only if we have the bandwidth.

## A quick empirical anchor we can run today

Independent of the prompt-collection work, we can run a tokenization counting experiment right now: take 10 to 20 equivalent sentences in English, Hindi, and Telugu, run them through each model's tokenizer, count tokens, and plot the ratio. We already know roughly what to expect from Petrov, but having our own numbers strengthens the paper. Could be done in an afternoon.

Stretch: extend it to Romanized Telugu and Hinglish — and there, no one has numbers yet, so even basic measurement is novel.

## What I need from each of you

1. **Confirm or push back on this direction.** If anyone would rather take a different topic, now's the time to say so.
2. **Native Telugu and Hindi speakers** — 30 to 60 minutes of your time to contribute realistic prompts. We'll do this in a structured way so it's not a free-for-all.
3. **One or two volunteers** to run the tokenization counting experiment across GPT-4o, Gemini, Claude, Llama. This is the empirical anchor — needed early.
4. **One person to own workshop logistics** — submission deadline, page limit, formatting rules.

Open to feedback on any of this. Happy to walk through any part in more detail before we lock the plan in.
