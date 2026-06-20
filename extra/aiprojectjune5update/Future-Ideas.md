# Future Ideas — Follow-up Paper Backlog

**Purpose:** Park good ideas here so v1 stays tight. These are candidate follow-up papers / extensions to look into *after* the June 23 deadline. Companion to `research-context.md` and `References.md`.

**Legend:** STRONG = novel + feasible · MEDIUM = interesting but harder/partly occupied · PARK = revisit later, may or may not be viable.

---

## 1. Response-script behavior — STRONG
When a user types romanized, what script does the LLM reply in (native / romanized / English / mixed), and is it usable? Measure the response-script distribution across models + languages, the usability consequence (user romanizes because they can't read native script comfortably → native-script reply is a failure), and a mitigation (detect the user's readable script and match it). No prior work found. The basic version rides in v1; the deep version is its own paper.

## 2. Global romanization — STRONG (the "v2")
Extend the v1 generation-quality method beyond Indic to Arabizi (~400M), Banglish (~270M), Roman Urdu (~230M), Pinglish (~80M), etc. ~1.3B people. Fits GenAI4World's "globalizing" theme. Needs native speakers per language, so it can't be v1. Mention in v1 discussion as the implication; build next.

## 3. Release the prompt corpus as a dataset/benchmark — STRONG, low effort
Publish the collected real romanized prompts + native-speaker quality ratings as a reusable resource. You're collecting it anyway; packaging it is a separate, citable contribution (benchmarks get cited).

## 4. Tokenization "cost-is-closed" longitudinal snapshot — PARK (look into later, if even possible)
The idea: be the citable reference that documents the Indic tokenization cost gap has closed on frontier tokenizers.

> If you state "cost is solved," you'll be citing them — and a reviewer asks "what did you add?" To actually become the reference everyone cites for "Indic tokenization cost is closed," you'd need a rigorous, systematic, multi-language, multi-tokenizer (ideally longitudinal) study. That's a real paper's worth of work.

**Note:** we can look into this later — *if it's even possible*. Requires: many languages × many tokenizers (GPT-4o/o200k, cl100k, Claude, Gemini, Llama, MuRIL/Sarvam, BrahmicTokenizer) × ideally tracked across model generations, on parallel content (FLORES), reporting tokens + words + tokens/word. Risk: the claim is already partly owned by OpenAI (2024 table) and Foroutan (2025), so novelty depends on systematicity/coverage no one else has done. Only worth it if we can clearly out-measure what exists.

## 5. Sociolinguistic mechanism — MEDIUM
Why Indic romanizes and persists (diglossia: English = High register; mother tongue = oral/Low register → serialized to Latin; CJK input methods force native-script conversion, Indic don't; code-switching breaks transliteration IMEs; and Indic Romanization persists despite good IMEs, unlike Greeklish/Translit which declined). Hard to make empirically rigorous for an NLP venue — better as v1's "why" section than a standalone, unless written as a position paper.

## 6. Safety in high-stakes domains beyond healthcare — MEDIUM
Script Gap covered maternal-health triage; Yong/Tamkin covered jailbreaks. Possible follow-up only if an unoccupied high-stakes domain is found (legal, financial, government services in romanized Indic).

## 7. LLM-as-judge is also blind — STRONG
Does LLM-as-judge (a standard automatic metric) itself fail on romanized Telugu — i.e., can GPT-4-as-judge even tell a good Telugu answer from a bad one? Show it diverges from native speakers too. Meta-finding: *"you can't evaluate low-resource generation with an LLM judge, because the judge shares the blind spot."* Cheap (reuse v1's responses + human scores; just add the LLM-judge). Strengthens the "invisible to metrics" thesis from the inside.

## 8. Did quality close like cost did? (longitudinal) — STRONG
Cost collapsed across model generations (GPT-3.5 → 4o). Run the same romanized prompts through old and new versions and track whether the *generation-quality* gap is closing too. *"Cost closed; did quality?"* Directly extends the 2026-06-03 cost-collapse finding.

## 9. Equity has migrated from cost to quality — STRONG (very on-theme)
Old framing: "Telugu users pay more." Cost is closing → the sharper claim is **"Telugu users now pay the same and get worse."** A short conceptual/measurement piece documenting that equity has shifted from a cost gap to a quality gap.

## 10. Honorifics & kinship probe — STRONG (focused)
Indian languages encode honorific/kinship systems English has no equivalent for (formal vs casual "you," elder/younger sibling terms, in-law terms). Focused test: do LLMs get honorifics/kinship right? Clean cultural-misalignment probe, deeply measurable, English-untranslatable.

## 11. User coping strategies — MEDIUM-STRONG (needs user study)
Flip the lens to the user: how do Indians *adapt* to bad support — switch to English mid-chat, re-spell, re-prompt, give up? A behavioral study of workarounds. The human side is undocumented.

## 12. Conversion-first intervention — MEDIUM-STRONG (actionable)
Does converting romanized → native script first (RomanSetu-style) actually *fix* generation quality, or does the model still fail? Tests whether the problem is input-parsing or deeper. Gives a *solution* angle, not just a diagnosis.

## 13. Two more (one-liners) — MEDIUM
- **Code-switch direction asymmetry:** does "English matrix + Telugu insertion" break differently than "Telugu matrix + English insertion"? (Matrix Language Frame theory.)
- **Multi-turn drift:** does quality decay as a romanized conversation gets longer and context fills with romanized text?

---

## How to use this doc
Add any new "down the lane" idea here with a one-line description + a STRONG/MEDIUM/PARK tag, so it's captured without bloating v1. Revisit after the deadline.
