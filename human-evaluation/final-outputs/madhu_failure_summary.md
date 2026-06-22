# Failure Catalog — Romanized Indic LLM Outputs

**Study:** *The Invisible Gap: Evaluating LLMs the Way Indians Actually Use Them* (GenAI4World @ COLM 2026)

**Scope:** All 4 providers × 3 languages (Telugu, Kannada, Hindi), ~142 responses each (~1,700 total). Two failure modes that automatic metrics largely miss.

**Detection thresholds:** English-only = word-overlap with English reference ≥ 0.90 and < 10 native-script chars. Degeneration = a single word repeated ≥ 20× consecutively, OR a 4-word phrase repeated ≥ 50×.


---

## Failure 1 — Output is (near-)entirely English

The model returns the answer in English instead of the romanized target language. Automatic semantic metrics reward this heavily (BGE ≈ 1.0, BERTScore ≈ 1.0) because the *meaning* is correct — the language failure is invisible to them.


**Total instances (overlap ≥ 0.90): 70**


| Model | verbatim (≥0.95) | near-verbatim (0.90–0.95) | genuine failures* | English-task** |
|---|---|---|---|---|
| gpt | 0 | 0 | 0 | 0 |
| anthropic | 5 | 5 | 2 | 8 |
| gemini | 5 | 4 | 2 | 7 |
| ollama | 44 | 7 | 41 | 10 |

*genuine failures = creative/informational prompts that expected the target language but came out English. **English-task = prompts that operate on English text (OCR cleanup, capitalize, email-improve, CV, grammar-fix, song-rewrite) where English output is defensible.


**Key points:**

- **gpt never produced pure English** (0 instances) — it romanizes even English-operating tasks.

- **anthropic (10) and gemini (9)** are almost entirely English-task rows (defensible); only ~2 each are genuine failures.

- **ollama is the failure engine: 51 instances, 41 of them genuine failures** on prompts that clearly wanted the target language.


**Genuine English-only failures (not English-task):**


| Model | Lang | overlap | message_id | prompt |
|---|---|---|---|---|
| anthropic | telugu | 0.91 | `434e4845` | Generate python code based on based on the evaluation p… |
| anthropic | telugu | 0.93 | `c28478dc` | Biochemically, ginger can stimulate the production of d… |
| gemini | kannada | 1.00 | `6acf77db` | I want you to imagine that you are J. R. R. Tolkien. We… |
| gemini | telugu | 0.91 | `434e4845` | Generate python code based on based on the evaluation p… |
| ollama | hindi | 1.00 | `b0214be4` | Please design a PhD research paper around Developing in… |
| ollama | kannada | 1.00 | `86123d17` | Walter Burley-Griffin designed the city of Canberra, th… |
| ollama | kannada | 0.93 | `a73dc9d7` | I'm a 26 year old, 6foot tall male, I weight 130 pounds… |
| ollama | kannada | 1.00 | `fa12b6ed` | On Arch Linux, how do I allow a user to use `sudo` for … |
| ollama | kannada | 0.96 | `91301122` | I need help creating a meal plan to build muscle while … |
| ollama | kannada | 1.00 | `e676ec87` | I want to learn how to engineer prompts for AI models s… |
| ollama | kannada | 1.00 | `cbd9cb0d` | Hello, Open Assistant. Could you give a few examples of… |
| ollama | kannada | 0.94 | `434e4845` | Generate python code based on based on the evaluation p… |
| ollama | kannada | 1.00 | `c28478dc` | Biochemically, ginger can stimulate the production of d… |
| ollama | kannada | 1.00 | `df17c57d` | Hi, my cat just chewed on a small weed outside that loo… |
| ollama | kannada | 1.00 | `613e14c6` | How do object-oriented programming principles such as e… |
| ollama | kannada | 0.90 | `f1f852c8` | Please provide me with a 12 month planting schedule for… |
| ollama | kannada | 1.00 | `612f2803` | i'm writing a dungeons and dragons campaign for a coupl… |
| ollama | kannada | 1.00 | `9043b45f` | I want to buy headphones. It is your job to suggest me … |
| ollama | kannada | 1.00 | `39b22099` | Narrate the history of development of paper like you're… |
| ollama | kannada | 1.00 | `13dc183f` | Hi how are you.

I have a strange question. In the wiza… |
| ollama | kannada | 0.91 | `96569f40` | Compose a highly sophisticated, expertly written, and i… |
| ollama | kannada | 0.95 | `5e8fddd4` | I need to write a eulogy, but am having problems with t… |
| ollama | kannada | 0.99 | `2a21eda6` | The European Union uses carbon dioxide equivalent (CO2-… |
| ollama | kannada | 0.91 | `dbf902b9` | I just inherited a coconut farm from my uncle. I grew u… |
| ollama | kannada | 1.00 | `2453d1f8` | Hello Assistant, 

Could you please outline a calm, opt… |
| ollama | kannada | 0.91 | `74059dfd` | I cant stop procrastinating. Its two am and i should sl… |
| ollama | kannada | 1.00 | `39f7578e` | I remember an airliner crash, but I do not know what pl… |
| ollama | kannada | 1.00 | `6fd86f73` | Create an outline of a professional legal memorandum wr… |
| ollama | kannada | 0.91 | `945f0c72` | Help me to optimize this code:
doe = DistanceOnEarth()
… |
| ollama | kannada | 1.00 | `38bc5a19` | Let's come up with a rich and complex alien world setti… |
| ollama | kannada | 1.00 | `84731e63` | Here is a problem I run into with modern social media: … |
| ollama | kannada | 1.00 | `c10ee1ad` | Is there a way to convert a .png or .svg into a .ai fil… |
| ollama | telugu | 1.00 | `ed5dbe6a` | Kindly analyse the ways in which the game Mancala/ Owar… |
| ollama | telugu | 1.00 | `86123d17` | Walter Burley-Griffin designed the city of Canberra, th… |
| ollama | telugu | 1.00 | `cbd9cb0d` | Hello, Open Assistant. Could you give a few examples of… |
| ollama | telugu | 1.00 | `c28478dc` | Biochemically, ginger can stimulate the production of d… |
| ollama | telugu | 1.00 | `4f64ca9b` | hello chat

i had a cool dream once i was in space jump… |
| ollama | telugu | 1.00 | `b0214be4` | Please design a PhD research paper around Developing in… |
| ollama | telugu | 1.00 | `613e14c6` | How do object-oriented programming principles such as e… |
| ollama | telugu | 1.00 | `9043b45f` | I want to buy headphones. It is your job to suggest me … |
| ollama | telugu | 1.00 | `95e49506` | Please list the various phases in Intermittent Fasting … |
| ollama | telugu | 1.00 | `0deb2fca` | Improve the writing in the following email:

Good morni… |
| ollama | telugu | 1.00 | `2453d1f8` | Hello Assistant, 

Could you please outline a calm, opt… |
| ollama | telugu | 1.00 | `945f0c72` | Help me to optimize this code:
doe = DistanceOnEarth()
… |
| ollama | telugu | 1.00 | `8228234f` | Please list me some ideas for magical abilities in a ma… |

---

## Failure 2 — ollama hallucination / endless repetition loop

ollama collapses into repeating a single word or short phrase, often for hundreds to thousands of tokens. The rubric's consistency check (P4) is **blind** to this — it scores all of them 3 ("consistent romanization style") — and BGE ranges 0.39–0.72, sometimes still "passing."


**Total instances: 13 — all ollama (clean models: 0).**


| Lang | kind | repeated token/phrase | times | response length | prompt |
|---|---|---|---|---|---|
| hindi | phrase_loop | `aate hi aate hi` | 1244× | 2598 words | Write the dialog for the following scene: The superhero… |
| hindi | phrase_loop | `parivaar par parivaar par` | 955× | 2022 words | The European Union uses carbon dioxide equivalent (CO2-… |
| kannada | word_loop | `ellu` | 2017× | 2020 words | Please correct the spelling and grammar of the followin… |
| kannada | word_loop | `ondu` | 1965× | 2010 words | I was having a conversation with a programming AI assis… |
| kannada | word_loop | `yaaru` | 1964× | 1997 words | Can you write a motivation letter to apply to an Applie… |
| kannada | word_loop | `nadike` | 1322× | 1333 words | I have the following python function:

```python
def re… |
| kannada | word_loop | `nimmu` | 1296× | 1325 words | Write a story about the meaning of life. Make it whatev… |
| kannada | word_loop | `kotha` | 1219× | 1357 words | Could you write me a ruby program which reads a csv fil… |
| kannada | word_loop | `samskaranada` | 750× | 813 words | What are the fundamentals of art and how can they be us… |
| kannada | phrase_loop | `(x,y) niddi (0,0) niddi` | 111× | 1031 words | What does this Python code do?
```
import random


def … |
| kannada | phrase_loop | `bekkaru gatiyaguttu, bekkaru g…` | 393× | 804 words | You are a physician seeing a patient in clinic with new… |
| kannada | phrase_loop | `nammagalu ninda chinnagalu nam…` | 397× | 1218 words | Please list the four most common tunings for guitar. Fo… |
| telugu | phrase_loop | `chala time nundi chala` | 778× | 2357 words | Make the beginning of a play, based on the Plaça del Di… |

**Most extreme:** Kannada, spelling-correction prompt — the word **"ellu"** repeated **2,017 times** in a row (BGE still 0.39).


**Why metrics miss it:** consistency-rubric P4 = 3 for every loop; BGE/BERTScore measure semantic overlap, which stays moderate because the few real words present still match the reference topic.


---

## Note on the evaluation set

- The pure-English **Kannada Row 1** (Walter Burley-Griffin essay), which the native speaker scored 0/0/0/0/0, has been **removed from the active scoring set and replaced** with a genuine Kannada row (anthropic, Irish bodhrán). The English-only failure it represented is preserved here in the catalog above.

- Full Opus-4.8 LLM-judge scores (parameters 1–10) for all 75 picked rows are in `FINAL_LLM_judge_all_rows.csv`.
