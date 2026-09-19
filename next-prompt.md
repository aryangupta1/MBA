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

## Do first

1. Still owed to Aryan from 2026-09-12 — see Open threads item 1.

## Open threads

- [ ] The 2026-09-12 "Do first" list is still unreported to Aryan: (1) the transcript incident of
      2026-09-12; (2) the access code is six characters; (3) how assessment pages look / whether
      6005 Final Version belongs behind the gate; (4) the unseen pages; (5) approve the hook
      (`/hooks`); (6) the `$28.888m` / `$22.888m` line.
- [ ] Add the no-transcript rule to `~/MBA/.mba-sync/AGENT-INSTRUCTIONS.md` itself.
- [ ] `practice/build.py` skips a page that already has practice content — use `strip.py` first.
      Worth a line in the SKILL.md Phase 3c.
- [ ] Acronyms/formulas splice is still hand-scripted per week — worth a `splice_ref.py`.
- [ ] `semester-2-private-notes.html` is stale and needs its own password to rebuild or delete.
- [ ] Four syllabus files still cannot be migrated (`file://` refs in Notion).
- [ ] Lecturer name and email remain in git history from `7a63ab5`; not scrubbed, not asked.
- [ ] No `Live` note yet for 6005 Weeks 6–7 or 6008 Weeks 5 and 7.
- [ ] `harvest_plan.py` writes one `plan.json` per course — re-run it for each course before its apply
      (did so this session).
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
