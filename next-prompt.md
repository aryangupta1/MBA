# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-10-24
**Left by:** Aryan: *"sync notion, new updates have been made utilise sub agents for efficiency,
commit and push once done direct to master."* Ran the full chain for both semester-2 subjects
and **committed and pushed to `master`** on his instruction.

---

## What this session did

- **Notion changed its markup format** (first seen 2026-10-23). `notion-fetch` now returns
  HTML-flavoured content: `<b>`, `<ul><li>`, `<p />`, multi-line `<page>` tags, two-space
  indents and `$x$` equations. Images come back as `<image source="notion-file-block://…">`
  with the signed URLs in a separate `references` map. Fixed for good:
  - `convert_core.py` gained `to_legacy()`. Both formats now give the same vault note:
    131 of 150 unchanged pages converted byte-identical, and the rest differed only in
    equivalent markup.
  - The latent `text\n---` setext bug in `normalise()` is also fixed.
  - New `reference/compare_harvest.py <backup> [--apply]` compares words, not bytes.
  - `ingest.py` takes a `refs.json` as its second argument.
  - `~/MBA/.mba-sync/AGENT-INSTRUCTIONS.md` tells harvesters how to use it.
  - The sync-notes `SKILL.md` documents all of this.
- **sync-notes**, both courses, full scope, 9 harvest agents. Backup at
  `~/MBA/.mba-sync/backup-20261023-221558/`.
  - 150 re-harvested pages had **0 word-level changes**, so their raw bytes were restored and
    nothing was rewritten.
  - **26 NEW notes:** 6008 Weeks 8–9, 6005 Weeks 8–10. One spot-checked against my own
    fetch matched.
  - 0 conflicts. `verify.py` reported ALL CHECKS PASSED.
- **Four new 6008 `Live` notes (Weeks 5, 7, 8, 9) contain only a `Transcript` child page.**
  Skipped per the no-transcript rule. No raw file, no vault note (NO-RAW), no gated page.
- **Published 5 pages:** `DMBA6008-week8.html` (6 topics) and `-week9.html` (5);
  `DMBA6005-week8.html`, `-week9.html`, `-week10.html` (2 topics each, Shadow Boxing
  excluded by syncRule).
  - All 16 Week 8 images were formula renders, transcribed by hand, not published.
  - Gate-1/4 agents ran on all five pages, and every finding was fixed or ruled on.
  - Hubs, library, index (counts were stale at 6/7 weeks and are now 10/11), both search
    pages (1,935 / 1,462), state and docs are all updated.

## Do first

Nothing pending from the agenda. Wait for Aryan.

## Open threads — each needs Aryan, not code

- [ ] Gate leftovers judged acceptable, not changed: inferred branch labels on the 6008 Week 8
      H3 figure; the 6005 Week 9 cyber figure ties reporting to the Notify step; and the quiz
      intro template line "Every wrong option is a mistake someone actually makes" (5 pages).
- [ ] **Lecturer name and email in git history** (from `7a63ab5`). Removing them means
      rewriting `master` and force-pushing — only on his explicit go.
- [ ] **Four syllabus images** (6001, 6002, 6004, 6008) stay in Notion. Download by hand if wanted.
- [ ] Approve the SessionStart hook via `/hooks` if the note stops appearing.
- [ ] Whether DMBA 6005 Assessment 1 `Final Version` belongs behind the gate (it is there now).
- [ ] No real `Live` diary yet for 6005 Weeks 6–10 or 6008 Weeks 5, 7–9 (6008's are
      transcript-only). When one lands, add it to `PAGES` in `build.py`.
- [ ] Headless Chrome cannot render narrower than ~500px, so phone-width screenshots crop.
      Check one new page on a real phone.

## Settled — do not re-open

- **Nina Harding, the mediator cited in 6005 Week 8's conflict note, is named on the page**
  (Aryan, 2026-10-24: "name"). **"credit spread" for "credit spend"** in 6008 Week 9 approved.

- **Live pages and assessment notebooks are gated and linked; the gate is the control.** Never
  build one without it, never commit `.env`, never print the code.
- **Assessment notebooks are discovered from the vault** — no hand list.
- **Third-party material stays withheld on gated pages too** — names, transcripts, chat, images
  with people. Text screenshots (formulas, rubrics) are transcribed, never published.
- **The search pages add no content.** One per subject, rebuilt after every week change.
- **DMBA 6005 Week 3 `Live`** stays off public week pages. **Notion feeds the vault only.**
- **DMBA 6008 Week 4's lease inconsistency and Week 6's $28.888m line stay unreconciled.**
- **Shadow Boxing after Week 0 stays off every page**, public and gated (precedent kept this run).

## Notes for the next session

- Run `compare_harvest.py` instead of a byte diff. Expect FORMAT, not phantom changes.
- Harvest agents must fetch image pages with `include_file_urls: true` and pass the
  references JSON to `ingest.py`. Say so, and say the no-transcript rule, in every prompt.
- `notion-query-data-sources` is truncated (`has_more`) but ordered by `Edited Time` desc.
- A shared builder brief worked well: one agent per week page doing fragments, assembly, 3b
  and 3c, then one context-starved gate agent per page.

## Do not

- Do not hand-edit `DMBA60xx-search.html` or anything under `live/`; rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` or `.env` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log — **and say so in every harvest prompt.**
- Do not tidy his typos (`sprintsn`, `Estimate value at exist`, `What is answers`, `FCC`, …).
- Do not derive a number the notes leave unstated.
