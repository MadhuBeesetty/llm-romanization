# Session Backup — 2026-06-02 (Part 2: Tasks, Next Steps, Resume Notes)

Continuation of `Session-Backup-2026-06-02.md`. Read that first.

---

## Current task list (10 tasks, all pending as of session end)

1. **Verify workshop submission logistics** — deadline TZ, page limit, LaTeX template, anonymized review
2. **Lock Topic 2 formally with team** — get written confirmation from every member
3. **Run tokenization counting experiment** — replicate Petrov on latest LLMs + extend with Romanized/code-switched + 10+ language scope (refined today to include Korean as control, possibly Japanese/Mandarin too)
4. **Design prompt collection protocol** — finalize template (mostly done in `Prompt-Collection.md`)
5. **Recruit speakers + collect prompts** — tiered ~280 prompts (Korean dropped today — needs Task update)
6. **Set up LLM API access and run all prompts** — GPT-4o, Claude, Gemini, Llama 3, Indic-tuned model
7. **Design native-speaker evaluation rubric** — 4 dimensions × 1-5 scale + binary accept flag
8. **Apply automatic metrics + native-speaker scoring** — compute auto-vs-human gap
9. **Draft paper (all sections)** — Intro, Related Work, Methodology, Results, Discussion, Conclusion
10. **Team review cycles + final submit** — 2 review rounds + format check

**Task update needed (deferred due to permissions issue):** Task 5 should explicitly note Korean is excluded from human evaluation. Suggested new description:

> Tiered collection per Paper-Execution-Plan.md:
> - Tier A (Telugu, Hindi): 75-100 prompts each
> - Tier B (Kannada): 50 prompts
> - Pending tier (Tamil, Marathi, Mandarin): 15-50 each IF contributors confirm by June 8
> - Korean DROPPED from human eval (Tia Kim feedback — Korean Koreans don't code-switch in chat). Korean now serves as negative control in Task 3 tokenization only.
> - Real user prompts only — Google Translate is for baseline/control use only, NEVER as primary data source.

**Potential new Task #11 (pilot test):** Recommended but not yet locked.
> Run 5 prompts × 2 models (ChatGPT + Claude) × 1 Telugu native speaker, score outputs, validate or refute the hypothesis before committing 18 days to full collection.

---

## Open threads / next concrete steps when Madhu resumes

### Immediate (this week)

1. **Send recruitment messages** to Tamil, Marathi, Mandarin contacts with June 8 deadline
   - Suggested script in conversation: *"For a research paper deadline I'm working on — can you commit to ~30-60 min of prompt collection now and ~1 hour of response scoring later this month? Need to know by June 8 so I can plan around it."*

2. **Validate the Hindi prompts** in `Prompt-Collection.md` with the Hindi-speaking teammate. Ask for corrections + 30-50 of their own real prompts.

3. **Validate the Kannada prompts** in `Prompt-Collection.md` with girlfriend. Same ask.

4. **Lock Topic 2 formally** — currently each teammate has presented different topics, no formal decision yet. The team "loved" the three-paper narrative when Madhu shared it; need to convert that into formal commit.

5. **Verify workshop logistics** at https://sites.google.com/view/genai4world/home — deadline timezone, page limit, format template.

### This week or next

6. **Decide pilot test** — yes/no
7. **Fill ownership matrix** in `Paper-Execution-Plan.md` with the team — who owns what
8. **Clarify with Surbhi** why she shared T2I papers (arxiv:2304.06034 and 2404.01030). Possible Topic 6 advocacy or misread of scope.
9. **Update research-context.md** to merge today's session backup once permissions allow

---

## Files in this project (status snapshot)

```
/Users/mbeesetty/Documents/AI-paper-research/
├── research-context.md             (master context, last self-update 2026-05-30 evening)
├── Paper-Execution-Plan.md         (CREATED today, current as of 2026-06-02 morning)
├── Prompt-Collection.md            (CREATED today, current as of 2026-06-02 noon)
├── Team-Summary.md                 (CREATED earlier, narrower team-facing summary)
├── Day1-Meeting-Summary.md         (older, from 2026-05-30)
├── Session-Backup-2026-06-02.md    (THIS FILE, Part 1 — covers decisions + insights)
├── Session-Backup-2026-06-02-Part2.md (THIS FILE — tasks, next steps, resume)
└── test-write.tmp                  (delete after restart — was a permissions test)
```

**Items in research-context.md NOT YET REFLECTING today's work:**
- Session State date is still 2026-05-30 (should be 2026-06-02)
- "Refined Understanding" sections don't include today's Korean reframe
- "Papers to Cite" list doesn't include EfficientXLang (Ahuja 2025)
- "Still to do in Topic 2" list is now stale — superseded by today's open threads
- No record of team feedback from Tia Kim
- No record of contrastive framing table

After restart, the merge work is:
1. Update Session State date
2. Append new "Session 2026-06-02" section
3. Add EfficientXLang to Papers to Cite
4. Replace stale "Still to do" with current open threads

---

## Team interactions today

| Person | Topic | Outcome |
|---|---|---|
| Tia Kim (Korean office colleague) | Validated Korean prompt samples | Confirmed Korean Koreans don't code-switch in chat; even Korean-Americans don't code-switch with ChatGPT. Led to Korean reframe. |
| Other team members | (none today) | Need to be looped in on: Korean reframe, methodology refinements, language scope locks |

**People Madhu needs to follow up with:**
- Hindi-speaking teammate (for prompt validation)
- Girlfriend (for Kannada validation)
- Tamil/Marathi/Mandarin office colleagues (recruitment ask + June 8 deadline)
- Surbhi (clarify the T2I papers share)
- Whole team (Topic 2 formal lock)

---

## Important conceptual points from today (for Madhu to remember)

### Scope ≠ Impact

When Madhu felt "lost" about whether limiting to Indian languages addressed a "big issue":

- Indic in scope (Hindi 600M + Telugu 95M + Tamil 75M + Kannada 45M + Marathi 83M) = ~900M people
- Larger than Europe (~750M) or North America (~600M)
- Twice the US population
- Not narrow — just doesn't *sound* impressive until said out loud

### Real user data is essential, not optional

The whole paper's contribution is "we tested with REAL user input." Substituting Google Translate output would reproduce the same flaw as existing benchmarks. The fix that kills the paper: replacing real prompts with GT-generated ones to hit the deadline. Never do this.

### Why scope discipline matters with this deadline

Adding languages has linear data-collection cost but super-linear coordination cost. Every added language requires: native-speaker recruitment, rubric calibration, separate analysis, new paper section. With 22 days, focused depth > scattered breadth.

### Korean validates the approach (negative control insight)

If we ONLY showed Indic failed, a reviewer could say "maybe AI is just bad at any non-English." Korean as a negative control — where users don't code-switch — predicted to show smaller gap. The contrast isolates code-switching as the gap-driver. Stronger experimental design.

---

## When you restart and resume

**Resume in this order:**

1. Open `Session-Backup-2026-06-02.md` (Part 1) and this file (Part 2) — read them
2. Open `Paper-Execution-Plan.md` to refresh the 7-phase timeline
3. Open `Prompt-Collection.md` to remember the 7 categories and sample prompts
4. Send the recruitment messages (Tamil/Marathi/Mandarin) — these unblock the most
5. Ping Hindi teammate + girlfriend for prompt validation
6. In a future Claude session: ask Claude to merge these backup files into `research-context.md` (deferred today due to permissions issue)

**The single most important thing not to lose:** the Korean reframe is THE key insight from today's session. Don't accidentally re-include Korean in human eval. It's tokenization-only / negative control.

---

## Sign-off

Backup created at 2026-06-02 ~afternoon, before Madhu's planned laptop restart due to system issues. Two backup files written because Bash/Read tools were returning EPERM mid-session but Write still worked — defensive split in case one file got corrupted. After restart:
- Delete `test-write.tmp` (was a permissions test)
- Optionally merge these backup files into `research-context.md`
- Resume work from the "Next concrete steps" list above
