# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-09-20
**Left by:** Aryan: *"Changes have been made to notion, sync, push and commit accordingly straight to
master."* Ran the full chain for both semester-2 subjects and **committed and pushed to `master`**
on his instruction.

---

## What this session did

- **sync-notes**, both courses, full scope, 8 harvest agents. Backup at
  `~/MBA/.mba-sync/backup-20260920-003831/`. 0 whitespace-only diffs, 9 real diffs — the two
  prose-heavy ones re-verified with my own fetch. Applied with no conflicts: 6008 8 new + 1 updated,
  6005 8 new + 6 updated. `verify.py`: only the known transcript/chat wikilinks and a pre-existing
  markup leftover in `Live Prep - MedScope Technologies.md` (untouched since 2026-09-09).
- Transcripts skipped again: the four `Live Session Transcript` / `Live Session Chat` children of the
  6008 Assessment 1 `Plan`. New Shadow Boxing pages for 6005 Weeks 5–7 were harvested into the vault
  (his own case-exercise notes, not a transcript); syncRules keep them off every public page.
- **Published:** `DMBA6008-week7.html` (6 topics; all 9 images were formulas, transcribed) and
  `DMBA6005-week7.html` (3 topics; its 1 image was the EAC/ETC formula, transcribed). Re-synced
  `DMBA6005-week6.html`: `Critical path diagrams` is now fully written, new topic
  `How do you do a big CX Project`. Hubs, library, both search pages (1,531 / 1,141), state and docs
  updated. Gate-1 fidelity agents ran on all three pages; every finding was fixed before commit.
- **Gated pages rebuilt** (`build.py`) for the changed Live / Assessment notes — 6005 Week 5 Live
  (+ `Live Prep`), 6008 Assessment 2 Part A (+ `Valuation inputs`), 6005 Assessment 1 Final Version.

- **SVG label colours fixed site-wide** (Aryan: "yes fix"). The `.svg-*` classes set `fill` in CSS,
  which beat every `fill="…"` attribute on a classed `<text>` — 475 labels on 14 week pages rendered
  in the default ink instead of white / pale / signal red-green. Moved each into `style="fill:…"`.
  `checks.py` now flags the attribute form and `fragment-spec.md` rule 3 says so.

- **Cleared the whole open-thread list** (Aryan: "fix everything in one go"): no-transcript rule
  now in `~/MBA/.mba-sync/AGENT-INSTRUCTIONS.md`; `strip.py` step documented in sync-subject
  Phase 3c; new `reference/splice_ref.py` for the Acronyms/Formulas tabs (Phase 3b);
  `harvest_plan.py` writes `plan-<code>.json` and `apply_harvest.py DMBA6008 DMBA6005` applies
  several courses at once; `verify.py` no longer fails on the expected transcript/chat links or on
  `\\$` inside his own LaTeX — **ALL CHECKS PASSED**; stale `semester-2-private-notes.html`
  deleted (superseded by `live/`), references updated. The 2026-09-12 items were reported to him.

## Do first

Nothing pending from the agenda. Wait for Aryan.

## Open threads — each needs Aryan, not code

- [ ] **Lecturer name and email in git history** (from `7a63ab5`). Removing them means rewriting
      `master` and force-pushing — only on his explicit go.
- [ ] **Four syllabus images** (6001, 6002, 6004, 6008) stay in Notion: they are internal
      `file://` attachments and `notion-download-attachment` only fetches text files the
      integration created. Download by hand if wanted.
- [ ] Approve the SessionStart hook via `/hooks` if the note stops appearing.
- [ ] Whether DMBA 6005 Assessment 1 `Final Version` belongs behind the gate (it is there now).
- [ ] No `Live` note yet for 6005 Weeks 6–7 or 6008 Weeks 5 and 7 — when one lands, `build.py`
      picks it up (add to `PAGES` if it is a new week).
- [ ] The Chrome extension refuses `file://` URLs; serve with `python3 -m http.server` for the
      browser gate.

## Settled — do not re-open

- **Live pages and assessment notebooks are gated and linked; the gate is the control.** Never
  build one without it, never commit `.env`, never print the code.
- **Assessment notebooks are discovered from the vault** — no hand list.
- **Third-party material stays withheld on gated pages too** — names, transcripts, chat, images
  with people. Text screenshots (formulas, rubrics) are transcribed, never published.
- **The search pages add no content.** One per subject, rebuilt after every week change.
- **DMBA 6005 Week 3 `Live`** stays off public week pages. **Notion feeds the vault only.**
- **DMBA 6008 Week 4's lease inconsistency and Week 6's $28.888m line stay unreconciled.**

## Notes for the next session

- Notion `notion-query-data-sources` result is truncated (`has_more`), but it is ordered by
  `Edited Time` desc so every recently edited note is in the first page.
- Say the no-transcript rule in every harvest prompt. This repo's guidance is in **CLAUDE.md**.

## Do not

- Do not hand-edit `DMBA60xx-search.html` or anything under `live/`; rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` or `.env` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log — **and say so in every harvest prompt.**
- Do not tidy his typos (`sprintsn`, `Estimate value at exist`, `What is answers`, `FCC`, …).
- Do not derive a number the notes leave unstated.
