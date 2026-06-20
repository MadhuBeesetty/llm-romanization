# References — Running Bibliography

**Purpose:** Single place for every paper/source we've discussed, with what it is, how we'd cite it, and whether it's been verified. Pull from here when drafting Related Work and building the `.bib`. Living doc — add as we go.

**Companion to** `research-context.md` (decisions/narrative) and the planning docs.

### Verification legend
- ✅ **verified** this session — read full text or confirmed via API (title/authors/venue/key numbers checked)
- 🟡 **metadata-only** — title/abstract seen via OpenAlex search; not full-read
- ⚪ **from memory** — mentioned in discussion, NOT checked this session → **verify before citing**
- ❌ **rejected / off-topic** — kept here so we don't re-litigate

### Relationship tags
`[ARC]` core narrative arc · `[OUTRUN]` prior work to cite + differentiate · `[BACKGROUND]` cite as setup, not headline · `[MOTIVATION]` · `[PHENOMENON/DATA]` romanization prevalence/datasets · `[METHOD/BENCHMARK]` · `[REJECTED]`

---

## 1. Tokenization & cost (the setup — now BACKGROUND, not headline)

- ✅ `[ARC][BACKGROUND]` **Petrov et al. 2023** — *Language Model Tokenizers Introduce Unfairness Between Languages* — NeurIPS 2023, **arXiv:2305.15425**. Foundational cost-asymmetry; abstract says "up to 15x" token-length differences. ⚠️ specific **8.34x Telugu** is a table cell still to confirm.
- ✅ `[ARC][BACKGROUND]` **Foroutan, Meister, Paul, Niklaus, Ahmadi, Bosselut, Sennrich 2025** — *Parity-Aware Byte-Pair Encoding: Improving Cross-lingual Fairness in Tokenization* — **arXiv:2508.04796v2** (22 Aug 2025), EPFL/ETH Zurich. Verified numbers: Gini 0.064→0.011; Telugu 32.73→33.52 (within noise — capability unchanged); **"parity ≠ capability" gift** (Telugu 33.5 vs English 44.2 vs random 30.0, on 3B from-scratch models).
- ✅ `[BACKGROUND]` **Ahia et al. 2023** — *Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models* — EMNLP 2023 (DOI 10.18653/v1/2023.emnlp-main.614). Economic/cost asymmetry; "Telugu users subsidize English users" framing.
- 🟡 `[BACKGROUND]` **Lundin, Zhang, Karim, Louzan, Wei, Adelani, Carroll 2026** — *The Token Tax: Systematic Bias in Multilingual Tokenization* — AfricaNLP 2026. Current systematic tokenization-bias study (no real abstract retrieved — verify scope).
- 🟡 `[BACKGROUND]` **2025** — *Tokenization efficiency of current foundational large language models for the Ukrainian language* — Frontiers in AI, 2025. Single-language tokenizer-efficiency case study (the "Ukraine" paper). NOTE: Ukrainian is **Cyrillic**, this is tokenization efficiency, not romanization — adjacent, cite as "fertility varies by language even on current models."
- ✅ `[BACKGROUND]` **Shravan 2026** — *BrahmicTokenizer-131K: An Indic-Capable Drop-In Replacement for o200k_base* — arXiv 2026. Indic tokenizer fix; shows the cost problem is being actively patched.
- 🟡 `[BACKGROUND]` **2026** — *The cost of language: tokenization as a metric of labor*. Economic/labor framing of token cost.
- ⚪ `[BACKGROUND]` **OpenAI 2024** — GPT-4o launch tokenizer-improvement table (per-language token reductions, e.g. Telugu ~3.5x fewer, Hindi ~2.9x, Gujarati ~4.4x). Vendor artifact, not a paper. ⚠️ **verify on OpenAI's GPT-4o announcement page** — this is the source that makes the "o200k closed the cost gap" observation non-novel.

## 2. LLM evaluation on romanized / code-switched Indic (OUR neighborhood — cite + outrun)

- ✅ `[OUTRUN]` **Khullar, Desai, Malviya, Dalmia, Shi 2025** — *Script Gap: Evaluating LLM Triage on Indian Languages in Native vs Romanized Scripts in a Real World Setting* — Univ. Pittsburgh, **arXiv:2512.10780** (v1 Dec 2025, v2 Mar 2026). THE prior work. Triage **classification** w/ ground truth; romanized degrades up to 24pts; **prevalence Hindi 83% / Telugu 73% / 56% overall**. We differ: open-ended **generation quality** + auto-vs-human gap + negative control.
- ✅ `[OUTRUN]` **IndicKLAR 2026** — *Evaluating Cross-lingual Knowledge Consistency in Code-Mixed vis-a-vis Indian Languages using IndicKLAR* — **arXiv:2605.29637**. Knowledge **recall**; native-verified 3-way English/code-mixed/native; 9 open-weight models; code-mixing *closes* the recall gap. We differ: generation quality, not recall. ⚠️ verify: is their "code-mixed" Romanized or native-script?
- ✅ `[BACKGROUND]` **2025** — *Beyond Monolingual Assumptions: A Survey of Code-Switched NLP in the Era of LLMs across Modalities* — arXiv (IIT Gandhinagar group). 327 studies; names **"fair evaluation" as an open problem** → cite as "the field calls this open; we address it."
- 🟡 `[OUTRUN?]` **2026** — *Can Large Language Models Understand, Reason About, and Generate Code-Switched Text?* — check overlap with our generation angle (metadata only).
- ⚪ `[OUTRUN?]` **Marchisio et al. 2024 (Cohere)** — *Understanding and Mitigating Language Confusion in LLMs* (Language Confusion Benchmark) — ~EMNLP 2024. Measures responding in the **wrong language**. Closest neighbor to our **response-script** idea — but language, not romanized-script choice. ⚠️ verify; key differentiator for the response-script angle.

## 3. Romanization phenomenon, transliteration & datasets (Bins A & B — cite for prevalence/non-standardness)

- ✅ `[PHENOMENON/DATA]` **Roark et al. 2020** — *Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset* — LREC 2020 (aclanthology 2020.lrec-1.294). 12 South Asian langs; THE citation that romanization is widespread.
- ✅ `[PHENOMENON/DATA]` **Baruah et al. 2024** — *Transliteration Characteristics in Romanized Assamese Language Social Media Text* — ACM TALLIP 23(2), Art. 33, Feb 2024. Evidence that real romanization is **non-standard / idiosyncratic** (one-to-many, many-to-one, intra-word variation). Supports our real-user-vs-standardized distinction.
- ✅ `[METHOD/BENCHMARK]` **2023** — *Distinguishing Romanized Hindi from Romanized Urdu* — CAWL 2023 (aclanthology 2023.cawl-1.5). LangID; romanized langs get conflated.
- ✅ `[METHOD/BENCHMARK]` **2025** — *Modeling Romanized Hindi and Bengali: Dataset Creation and Multilingual LLM Integration* — **arXiv:2511.22769** (Nov 2025). Transliteration dataset + LLM integration. ⚠️ skim eval section — resource, not a competing eval.
- ✅ `[METHOD/BENCHMARK]` **Kirov, Johny et al. 2023** — *Context-aware Transliteration of Romanized South Asian Languages* — Computational Linguistics 2023 (DOI 10.1162/coli_a_00510, Google).
- ✅ `[METHOD/BENCHMARK]` **Husain, Dabre, Kumar, Gala, Jayakumar, Puduppully, Kunchukuttan 2024** — *RomanSetu: Efficiently unlocking multilingual capabilities of LLMs via Romanization* — ACL 2024 (pp. 15593–15615). Using romanization to *help* LLMs — relevant counterpoint. (confirmed via Script Gap bibliography)
- ✅ `[METHOD/BENCHMARK]` **Madhani et al. 2023** — *Aksharantar: Open Indic-language Transliteration datasets and models for the Next Billion Users* — Findings of EMNLP 2023 (DOI 10.18653/v1/2023.findings-emnlp.4; arXiv:2205.03018).
- ⚪ `[METHOD/BENCHMARK]` **FIRE shared tasks on transliterated search** (Choudhury, Roy et al. 2013–2014) — early evidence of romanized/mixed-script IR at scale.

## 4. Code-switching benchmarks & multilingual eval

- ✅ `[METHOD/BENCHMARK]` **Khanuja et al. 2020** — *GLUECoS: An Evaluation Benchmark for Code-Switched NLP* — ACL 2020. Pre-LLM code-switching eval (incl. Hindi-English).
- ✅ `[METHOD/BENCHMARK]` **Aguilar et al. 2020** — *LinCE: A Centralized Benchmark for Linguistic Code-switching Evaluation* — LREC 2020.
- ✅ `[BACKGROUND]` **Kanjirangat, Samardžić, Dolamic, Rinaldi 2025** — *Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks* — **arXiv:2509.20045** (verified in earlier session; EMNLP 2025 acceptance still unconfirmed). TP/IP applied to dialectal tasks; DI reversal finding.
- ✅ `[BACKGROUND]` **Tsvetkov & Kipnis 2024** — *Information Parity: Measuring and Predicting the Multilingual Capabilities of Language Models* — Findings of EMNLP 2024 (DOI 10.18653/v1/2024.findings-emnlp.468). Origin of **Information Parity (IP)**. NOTE: "A. S. Tsvetkov" — NOT Yulia Tsvetkov. Attribution fix — not Kanjirangat's invention.
- ⚪ `[BACKGROUND]` **Petrov et al. (2023/2024)** — origin of **Tokenization Parity (TP)** metric. ⚠️ could not confirm a distinct 2024 paper; TP may trace to Petrov 2023 (arXiv:2305.15425) — verify.
- ⚪ `[BACKGROUND/COUNTER]` **Ahuja et al. 2025** — *EfficientXLang: Towards Improving Token Efficiency Through Cross-Lingual Reasoning* — **arXiv:2507.00246**. Reasoning-chain efficiency; **must address as potential counter-evidence** (it's about reasoning chains, not user input).
- ✅ `[BACKGROUND]` **Pawar, Park et al. 2025** — *Survey of Cultural Awareness in Language Models: Text and Beyond* — Computational Linguistics 2025 (arXiv:2411.00860). For the cultural-fit rubric dimension.

## 5. Sociolinguistic / motivation / economics

- ✅ `[MOTIVATION]` **Azam, Chin & Prakash 2013** — *The Returns to English-Language Skills in India* — Economic Development and Cultural Change (WP 2011, IHDS 2005 data). ~20% some English (4% fluent); +34% wage return; urban/educated/young skew. Use for **diglossia / English-as-economic-register** and population scoping. NOT for the romanization claim. Data is 2005 → frame as structural pattern.
- ⚪ `[MOTIVATION]` **Ferguson 1959** — *Diglossia* — Word 15(2). The High/Low register concept. ⚠️ verify exact citation form.
- ✅ `[BACKGROUND]` **Khanuja et al. 2021** — *MuRIL: Multilingual Representations for Indian Languages* — arXiv:2103.10730. Indic model (kills "Indic-specific models would fix this").
- ⚪ `[BACKGROUND]` **Tamkin et al. 2024 (?)** — code-switching safety gaps (from workshop CFP). ⚠️ UNCONFIRMED — OpenAlex found no matching paper; possibly mis-cited. Verify against the GenAI4World CFP before using.
- ✅ `[BACKGROUND]` **Yong, Menghini et al. 2023** — *Low-Resource Languages Jailbreak GPT-4* — arXiv:2310.02446.

## 6. Rejected / off-topic (do NOT cite as core — logged to avoid re-litigating)

- ❌ **Naik & Nushi 2023** — arXiv:2304.06034 — T2I image bias. Off-topic for Topic 2.
- ❌ **Wan et al. 2024** — arXiv:2404.01030 — T2I bias survey. Off-topic.
- ⚪ **OpenAI Developer Community thread** (French dev "Ailogik", 159 words → 277 tokens). Use as a *motivating anecdote* only, not a formal citation.

---

## Still-to-verify before these enter the `.bib`
- [ ] Petrov 8.34x Telugu cell (arxiv.org/abs/2305.15425)
- [ ] IndicKLAR "code-mixed" = Romanized or native-script? (arxiv.org/abs/2605.29637)
- [ ] OpenAI GPT-4o tokenizer table (May 2024 announcement)
- [ ] Ferguson 1959 exact citation
- [ ] Marchisio et al. 2024 Language Confusion — exact venue + whether it touches script choice
- [ ] Kanjirangat EMNLP 2025 acceptance (vs arXiv-only)
- [ ] All ⚪ memory-only entries — confirm authors/year/venue/arXiv ID

## Notes
- Most ⚪ entries were cleared to ✅ on 2026-06-03 via OpenAlex (IDs/DOIs added). **Remaining unconfirmed (⚪):** Tamkin 2024 (possibly mis-cited — verify against CFP), Marchisio 2024 Language Confusion (OpenAlex didn't surface it — verify), Ferguson 1959 (pre-digital, verify form), Petrov-TP-2024 (may be Petrov 2023), EfficientXLang ID (from earlier session, not re-confirmed).
- Tooling: verify via OpenAlex — `curl -sk "https://api.openalex.org/works/doi:10.xxxx"` or `?search=...`. Web tools (WebSearch/WebFetch) are broken in this environment.
