# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-10-24
**Left by:** Aryan's brief *"Build the gated IO prep live page for DMBA 6005"* (a prompt file
in his Downloads; it names classmates and must never be committed). Built
`live/DMBA6005-io-prep.html`, then **committed and pushed to `master`** on his instruction.

---

## What this session did

- **The IO prep page.** `live/DMBA6005-io-prep.html` is gated with the same code and unlock as
  every other live page. Its 11 in-page tabs:
  - overview and game plan
  - short notes
  - in-depth notes, Weeks 0–10
  - acronyms (67)
  - glossary and formulas
  - characters
  - Shadow Boxing
  - decision log
  - mock Q&A (92 questions)
  - critical reflection
  - sources and `[VERIFY]` list
  
  It joins the 6005 live tab row as **IO prep** and gets an "Exam prep" card on
  `live/DMBA6005.html`. For the oral on **Mon 26 Oct 2026** (Notion Assignments DB).
- **New page type in `build.py`:** `PREP_PAGES`.
  - The source Markdown sits outside git and outside the vault's notes:
    `~/MBA/.mba-sync/io-prep/DMBA6005/NN-slug.md`. Tabs 04/05 come from
    `~/MBA/.mba-sync/io-prep/gen_glossary_DMBA6005.py <repo>`.
  - `md(prep=True)` adds `formula` fences and checklists.
  - `GATE_JS` now calls `window.afterUnlock(doc)`.
  - `BUILT_ON` is now 24 October 2026, so every live page was re-encrypted.
  - Documented in `.claude/private-pages/README.md`, `SECRET-PAGES.md` and `CLAUDE.md`.
- **Content route:** 6 reader agents, then 2 writer agents (decision log/reflection and Q&A),
  then a fresh-context fidelity reviewer.
  - The reviewer raised 0 critical, 3 major and 8 minor findings plus 6 gaps. All were fixed;
    the gaps became Q87–Q92.
  - The reviewer checked every deck number and about 75 vault claims against their sources.
- **sync-notes, DMBA 6005, full re-harvest** (Aryan chose it over skipping): 65 pages,
  **0 REAL changes**, nothing written to the vault, `verify.py` ALL CHECKS PASSED. Backup:
  `~/MBA/.mba-sync/backup-20261024-003757/`.
- **sync-assignments was not completed.** The Notion query came back `has_more`, i.e.
  truncated, so the tracker was not regenerated: that would have dropped rows. The vault
  tracker still says the oral is 1 Nov; Notion says **26 Oct**.

## Do first

Nothing pending from the agenda. Wait for Aryan. If he edits the IO prep source, re-run
`python3 .claude/private-pages/build.py` (real code from `.env`).

## Open threads — each needs Aryan, not code

- [ ] **IO prep `[VERIFY]` items:**
  - the four engagement measures (the deck names only return rate; a set is proposed)
  - sprint length
  - BAC ($80k vs $88–90k)
  - "free"
  - the A1–A6 story-id mapping
  - the slide 5 story numbers
  - no risk owners
  - the IO weighting and rubric, which are only in his brief
  
  Full list on the page's Sources tab.
- [ ] `sync-assignments` needs a paginated query (the DB has >100 rows now) before the tracker can be regenerated safely.
- [ ] Gate leftovers judged acceptable, not changed:
  - the inferred branch labels on the 6008 Week 8 H3 figure
  - the 6005 Week 9 cyber figure tying reporting to the Notify step
  - the quiz intro line "Every wrong option is a mistake someone actually makes"
- [ ] **Lecturer name and email in git history** (from `7a63ab5`). Removing them means
  rewriting `master` and force-pushing. Only on his explicit go.
- [ ] **Four syllabus images** (6001, 6002, 6004, 6008) stay in Notion. Download by hand if wanted.
- [ ] Approve the SessionStart hook via `/hooks` if the note stops appearing.
- [ ] Whether DMBA 6005 Assessment 1 `Final Version` belongs behind the gate (it is there now).
- [ ] No real `Live` diary yet for 6005 Weeks 6–10 or 6008 Weeks 5, 7–9 (6008's are
  transcript-only). When one lands, add it to `PAGES` in `build.py`.
- [ ] Check one new page on a real phone.

## Settled — do not re-open

- **Shadow Boxing after Week 0 is allowed on gated pages** (Aryan, 2026-10-24, for the IO prep
  page). It stays **off every public page** (`syncRules` `no-shadow-boxing-after-week-0`).
- **Teammates appear by role only** (Teammate G, Teammate C) on every page, gated or not.
- **Nina Harding, the mediator cited in 6005 Week 8's conflict note, is named on the page**
  (Aryan, 2026-10-24: "name"). **"credit spread" for "credit spend"** in 6008 Week 9 approved.
- **Live pages, assessment notebooks and prep pages are gated and linked; the gate is the
  control.** Never build one without it, never commit `.env`, never print the code.
- **Assessment notebooks are discovered from the vault.** Keep no hand list. Prep pages are listed in `PREP_PAGES`.
- **Third-party material stays withheld on gated pages too:** names, transcripts, chat, and
  images with people. Text screenshots (formulas, rubrics) are transcribed, never published.
- **The search pages add no content.** One per subject, rebuilt after every week change.
- **DMBA 6005 Week 3 `Live`** stays off public week pages. **Notion feeds the vault only.**
- **DMBA 6008 Week 4's lease inconsistency and Week 6's $28.888m line stay unreconciled.**

## Notes for the next session

- Never commit the IO prep source, the glossary generator or Aryan's prompt file. They hold
  plaintext group work, and the prompt names a classmate.
- Run `compare_harvest.py` instead of a byte diff. Expect FORMAT, not phantom changes.
- Harvest agents must fetch image pages with `include_file_urls: true` and pass the
  references JSON to `ingest.py`. Every harvest prompt must say so and must state the
  no-transcript rule.
- `notion-query-data-sources` results are truncated (`has_more`) but ordered by `Edited Time` desc.

## Do not

- Do not hand-edit `DMBA60xx-search.html` or anything under `live/`; rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` or `.env` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log — **and say so in every harvest prompt.**
- Do not tidy his typos (`sprintsn`, `Estimate value at exist`, `What is answers`, `FCC`, …).
- Do not derive a number the notes leave unstated.
