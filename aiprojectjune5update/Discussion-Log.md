# Discussion Log

Chronological record of what we discussed and decided, by date. Lighter than `research-context.md` (which holds the structured decisions) — this is the running narrative. Newest entries at the bottom.

---

## 2026-06-03 — Deep literature check + reframe + pilot

- **Verified the landscape via OpenAlex** (web search/fetch broken in the terminal; used `curl` to OpenAlex API). Found the field is crowded.
- **Threat found — Script Gap (arXiv:2512.10780, Dec 2025):** prior work already shows romanization hurts LLMs on *classification* (health triage) and reports prevalence (Hindi 83%, Telugu 73%). Killed 3 of our planned "firsts."
- **IndicKLAR (2026):** code-mixing *closes* the knowledge-recall gap — different construct (recall, not generation quality).
- **Verified citations:** Petrov (real, "up to 15x"; 8.34x still to check). Foroutan (real, arXiv:2508.04796; Gini 0.064→0.011 ✓, Telugu 32.73→33.52 = within noise, NOT an improvement). Foroutan's own Table 2 gift: Telugu 33.5 vs English 44.2 vs random 30.0 → **parity ≠ capability**.
- **THE REFRAME:** moved the contribution from "romanization causes a gap" (taken) to **"the gap is invisible to automatic metrics on open-ended generation — only native speakers catch it."** Korean = negative control.
- **Pilot run (on Claude Opus 4.8):** found anglicized "Telugu," native-script corruption on screen, kramam→karam romanization ambiguity, an agency error ("doctor tho review cheyinchandi"), content shrinkage (half the words in Telugu), and low diversity across fresh sessions. All invisible to metrics → thesis holds.
- **Token finding:** native Telugu cost collapsed 5.9x (cl100k) → 1.01x (o200k). Cost is being solved by industry → don't make the paper about cost. Words rescue the signal tokens hide (tokens/word: Telugu ~2x even on o200k).
- **Created:** References.md, Future-Ideas.md, Prompt-Responses.md. Updated research-context.md.

## 2026-06-04 — Team buy-in + data-collection plan

- **Team adopted the idea.** 
- **Data plan changed:** target **≥200 real romanized prompts**. Debated LLM-generating prompts → rejected (synthetic = clean = hides the gap, and circular). Resolution: **LLM seeds scenarios, humans author the romanized text themselves**; synthetic stays the control arm.
- **Sources prioritized:** Form (primary, consented) → chat history (gold) → YouTube comments → corpora → Reddit (low yield, supplementary).
- **BLEU/BERT clarified:** they need a same-language reference open-ended tasks lack → run them to *show they fail*, not to grade. Native rubric + Cohen's κ = ground truth.
- **Global angle:** planned Arabic (Arabizi, active), Persian (Finglish, active), Greek (Greeklish, *declined* → second control). Indic = spine (friends cover); non-Indic = collection+tokenization in v1, human-eval if evaluators found, else v2.
- **GenAI4World fit:** resolved as **global framing, Indic execution** — generalizable method + cross-family Korean control + ~1.3B footprint in discussion. Getting v1 accepted = platform for global v2.
- **Reddit recruitment messages drafted** (Arabic/Greek/Persian + generic). Noted: country subs are English-dominant → better for recruiting evaluators than harvesting prompts.
- **Cost reality:** scraping uses no LLM tokens (free APIs); run on free Colab; only real spend = the 200×5 eval runs (~few $, mostly free).

## 2026-06-05 — Handoff + execution focus

- **Gut-check ("are we going crazy?"):** no — idea is sound, pilot proved it, we own a defensible corner. Real risk = scope creep + over-planning. Cure = run the smallest real version (collect ~30 prompts, run, score).
- **Laptop switch:** moving to personal laptop to save tokens/money. Recommended local coding model: **Ollama + Qwen2.5-Coder** (7B@16GB / 14B+@32GB; check for Qwen3-Coder). Token counting is free/offline (`tiktoken`/HF) — no API needed.
- **Reddit scraping plan:** free via PRAW + Reddit API creds, run on Colab; filter by per-language keyword lists (standard langID misreads romanized Indic as English) + question markers; anonymize; manual native review. Expect low yield — supplementary to the Form.
- **Created START-HERE.md** — portable handoff doc to continue on the other laptop.
- **Still open:** run the pilot proper (the gate); update the two stale planning docs; recruit non-Indic evaluators.
