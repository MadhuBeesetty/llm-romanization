# Human Evaluation Scoring Guide
## Romanized Indic LLM Response Quality Study

**Paper:** The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them  
**Venue:** GenAI4World @ COLM 2026

---

## What You Are Evaluating

You will be given 80 rows (20 rows × 4 LLMs) in your language file.

Each row has:
- **query_en** — the original question in English (for reference only)
- **response_en** — the original English answer (for reference only)
- **romanized_query** — the same question typed in romanized script (e.g., Hinglish, Tenglish, Kanglish)
- **romanized_response** — the LLM's answer in romanized script ← **this is what you are rating**

> Your job: Read the `romanized_response` and score it on 5 parameters (columns 6–10).  
> Columns 1–5 are already filled in by the system. You do not need to change them.

---

## What is Romanized Script?

Romanized script means writing your native language using English (Latin) letters.

**Examples:**

| Language | Native Script | Romanized |
|----------|--------------|-----------|
| Hindi | मैं ठीक हूँ | Main theek hoon |
| Telugu | నేను బాగున్నాను | Nenu baagunnanu |
| Kannada | ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ | Naanu chennaagiddene |

This is how hundreds of millions of Indians type on their phones every day. The LLMs were asked to respond in this style.

---

## The 5 Parameters You Need to Score

> **Important:** Do NOT look at the auto-filled scores (columns 1–5) before you write your own scores. Score independently first, then you may check the auto scores for reference.

---

### Parameter 6 — Naturalness / Fluency `(0–3)`

**Question: Does this read like how a real person from your community would actually type?**

Imagine receiving this message from a friend or a helpful assistant on WhatsApp. Does it feel natural?

| Score | Meaning | Example |
|-------|---------|---------|
| **3** | Completely natural. You would believe a native speaker typed this. No awkward phrasing. | "Yaar, yeh topic bahut interesting hai. Basically, elliptic curves ka matlab hai..." |
| **2** | Mostly natural. One or two phrases feel slightly off or stiff, but you can follow it easily. | "Yeh concept ko samjhne ke liye, hum pehle dekhen..." (slightly translated-feeling) |
| **1** | Sounds like a translation. Grammatically follows the romanized language rules but feels robotic or foreign. | "Iss samay mein, yeh viषय ko dhyan mein rakhna zaroori hai ki..." |
| **0** | Unnatural or incomprehensible. You cannot tell what language this is trying to be. | Random mixing with no consistent pattern, or pure copied English. |

**What to watch for:**
- Does the sentence structure follow your language's natural flow, or does it feel like English word order?
- Are common filler words used naturally? (e.g., "toh", "na", "yaar" for Hindi; "ante", "kada" for Telugu; "andre", "nodri" for Kannada)
- Does it feel like something you'd actually send someone, or does it feel like a textbook?

---

### Parameter 7 — Grammar Correctness `(0–2)`

**Question: Is the romanized grammar correct for your language?**

This is about whether the grammatical structure of the language is correct — verb forms, postpositions, gender agreement, etc. — just written in Latin script instead of native script.

| Score | Meaning | Example |
|-------|---------|---------|
| **2** | Grammatically correct throughout. No errors that would confuse a native speaker. | "Woh school ja raha hai" ✓ |
| **1** | Minor errors but the meaning is still clear. A native speaker would notice but understand. | "Woh school jaata" (missing auxiliary) — understandable but wrong |
| **0** | Grammatically broken. A native speaker cannot parse the intended meaning. | "School ja woh hai raha" — completely broken word order |

**What to watch for:**
- Verb endings (e.g., "-ta hai" vs "-te hain" vs "-ti hai" for Hindi gender/number)
- Postpositions placed correctly (e.g., "ke saath", "ke liye" not "saath ke")
- Sentence endings match the register (question vs statement vs command)

> **Note:** Do NOT penalize for English technical words used as-is (e.g., "algorithm", "Python", "temperature"). These are natural in code-mixed speech.

---

### Parameter 8 — Word Choice Accuracy `(0–2)`

**Question: Are the right words used, or are there mistranslations or wrong vocabulary?**

| Score | Meaning | Example |
|-------|---------|---------|
| **2** | All word choices are correct and natural for the language. | "Woh bahut khush tha" — "khush" is the right word for happy |
| **1** | 1–2 wrong word choices but the overall meaning is still clear. A native speaker would notice something is off. | Using a Hindi word that technically exists but sounds unnatural in this context |
| **0** | Wrong words that change the meaning or cause real confusion. | Using a word from a different language (e.g., a Tamil word in a Telugu response) or a completely wrong word for the concept |

**What to watch for:**
- Words that are technically in the language but feel borrowed or unusual
- Concepts where the model used a rare/formal/archaic word when a common word exists
- Mistranslations where the word chosen has a different meaning than intended

---

### Parameter 9 — Register Appropriateness `(0–2)`

**Question: Is the tone and formality level right for this type of conversation?**

"Register" means whether the language is appropriately formal or informal for the context. In Indian languages, this often involves:
- Formal pronouns vs casual (e.g., "aap" vs "tum" vs "tu" in Hindi; "meeru" vs "neenu" in Telugu)
- Respectful verb forms vs casual verb forms
- Use of honorifics

| Score | Meaning | Example |
|-------|---------|---------|
| **2** | Register is correct. A casual question gets a casual response; a formal or technical question gets an appropriately formal response. | A recipe question gets a friendly, casual response; a legal or medical question gets a careful, respectful response |
| **1** | Slightly off — a bit too formal or too casual for the context, but not jarring. | A casual "tell me about cats" question gets a very stiff, textbook-style response |
| **0** | Completely wrong register. Jarring mismatch that would feel disrespectful or confusing. | A serious question about health gets a very casual, flippant response, or vice versa |

**What to watch for:**
- Pronoun choice ("aap" vs "tu" in Hindi)
- Verb form choice (polite vs casual endings)
- Tone — does it feel appropriate for the topic?

---

### Parameter 10 — Overall Usability `(0–3)`

**Question: If an AI assistant sent you this response on WhatsApp after you typed your question in romanized script, would you accept it?**

This is your overall judgment. Trust your gut as a native speaker.

| Score | Meaning |
|-------|---------|
| **3** | I would use this response as-is. It answers my question naturally in my language. |
| **2** | Usable, but I would fix 1–2 things before forwarding it. |
| **1** | Not usable. I would need to rewrite most of it. |
| **0** | Completely rejected. Empty, incomprehensible, or wrong language. |

> This is the most important score. When in doubt, ask yourself: "Would I actually use this?"

---

## How to Fill in the Sheet

1. Open your language file (`human_eval_ALL_hindi.csv` / `human_eval_ALL_telugu.csv` / `human_eval_ALL_kannada.csv`) in Excel or Google Sheets.
2. For each row, read:
   - `query_en` — to understand what the question was about
   - `romanized_response` — the actual response to rate ← focus here
3. Fill in scores for columns **6, 7, 8, 9, 10**
4. Add any free-text observations in `evaluator_notes` (optional but very helpful for the paper)
5. You do NOT need to change columns 1–5

---

## Tips for Evaluators

**Do:**
- Read the full response before scoring, not just the first sentence
- Use `query_en` to understand context, but rate the romanized response on its own merits
- Trust your instinct as a native speaker — if something feels off, it probably is
- Use `evaluator_notes` to flag interesting failure examples (e.g., "model used Telugu words in a Kannada response")

**Don't:**
- Penalize a response for including English technical terms — this is natural code-mixing
- Penalize for using a different valid romanization spelling (e.g., "aadmi" vs "aadmee" are both acceptable)
- Give all 3s or all 0s without reading — the responses vary a lot in quality
- Skip rows — every row needs all 5 scores

---

## Score Summary Reference

| # | Parameter | Scale | Who fills |
|---|-----------|-------|-----------|
| 1 | Response Completeness | 0–2 | Auto-filled |
| 2 | Script Purity | 0–2 | Auto-filled |
| 3 | English-Romanized Balance | 0–3 | Auto-filled |
| 4 | Romanization Consistency | 0–3 | Auto-filled |
| 5 | Semantic Faithfulness | 0–3 | Auto-filled |
| **6** | **Naturalness / Fluency** | **0–3** | **You** |
| **7** | **Grammar Correctness** | **0–2** | **You** |
| **8** | **Word Choice Accuracy** | **0–2** | **You** |
| **9** | **Register Appropriateness** | **0–2** | **You** |
| **10** | **Overall Usability** | **0–3** | **You** |

**Maximum total score per row: 25 points**  
*(Auto: 2+2+3+3+3=13) + (Human: 3+2+2+2+3=12)*

---

## Questions?

Contact Mahesh (Madhu Beesetty) if anything is unclear before you start.  
Please complete your file by **June 22, 2026** so scores can be compiled before the deadline.
