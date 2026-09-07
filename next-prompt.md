# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-09-07
**Left by:** A full Notion→vault→website sync on Aryan's "sync and push" instruction. Two new
weeks published — **DMBA 6008 Week 5 (Business evaluation)** and **DMBA 6005 Week 6
(Scheduling and design sprints)** — plus a latent bug fixed on the Week 5 page from last
session. Committed and pushed.

---

## The one thing worth learning from this run

**`week-shell.html` defines `buildRef()` but never calls it.** The `sync-subject` skill says
"the shared `buildRef()` renderer is already in the shell … so there is no JS to write". That
is wrong: the two `buildRef('acronyms', …)` / `buildRef('formulas', …)` call blocks must be
emitted after the arrays, or the tabs render a count and an empty list. `DMBA6005-week5.html`
shipped that way on 2026-08-31 and nobody noticed because `checks.py` cannot see it; it was
caught this run only because the Formulas tab was opened in a browser. Fixed on all three
pages. **Copy the call blocks from `DMBA6008-week4.html` (or any of the three fixed pages)
whenever a reference tab is added, and open the tab in a browser before reporting.** The skill
text has not been corrected yet — see Open threads.

## What came down — 2026-09-07

One metered `notion-query-data-sources` call. Live inventory **98 notes** against 96 cached:
two new, nothing changed, nothing deleted. Both new notes are Pre-Live `Learn` containers in
two new notebooks. Harvested **inline, not by agents** (nine raw files, eleven images), diffed
against `backup-20260907-180755`: only the nine new files differ.

| What | Sub-pages | Where it went |
| --- | --- | --- |
| DMBA 6005 `Week 6: Scheduling and design sprintsn` (typo is Notion's) → `Learn` | Scrum · Gantt Charts · Critical path diagrams | vault + **published** `DMBA6005-week6.html` |
| DMBA 6008 `Week 5: Business Evaluation` → `Learn` | How much cash for the owners · Simple business valuation · Business valuation: DCF Model · Business valuation: Financial drivers | vault + **published** `DMBA6008-week5.html` |

`apply_harvest.py`: **9 NEW, zero conflicts.** `verify.py`: 5 of 6, the expected wikilink
failure only (`Live Session Transcript` / `Live Session Chat`, never harvested — do not fix).

## What was published

**All eleven Week 5 images were LaTeX formula renders** — transcribed into `.formula` divs and
the 33-entry Formulas tab, PNGs deleted from `assets/`. Nothing new under `assets/notes/`.

| Page | Blocks | Figures | Terms | Cards | Acronyms | Formulas | Quiz | Scenarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DMBA6008-week5.html` | 26 | 12 | 58 | 87 | 12 | 33 | 10 | 5 |
| `DMBA6005-week6.html` | 22 | 9 | 43 | 62 | 3 | 2 | 10 | 5 |

Gate 1 ran adversarially on both and each found **one blocking defect, both fixed**: the
6008 equity-value bar figure had drawn the explicit-FCFE segment as `633.8 − 384.1`, a number
the notes never state (now two equal boxes, labelled not to scale); the 6005 critical-path
figure description defined the critical path by *count* of activities instead of *duration*.
A dozen minor wording glosses were tightened on each. The derived tabs (acronyms, formulas,
quiz, scenarios, study path) were checked by a second agent per page: PASS on both.

**`Critical path diagrams` is only partly written in the source** — 104 words, ending at two
empty headings. The page has two blocks for it, the second saying so; the quiz asks one
question on what is stated and there is no scenario. **When he writes the rest, that topic's
hash changes and the whole week re-syncs.**

Also this run: hub cards and pills (6005 → 7 weeks, 6008 → 6 weeks), `library.html`
registrations, `index.html` week counts (were stale at "4 weeks" on both cards), the nine
stale `Synced from Notion` footers reworded to "now kept in my Obsidian vault. Last built on
<original date>", `docs/vault-sync-state.json`, `docs/vault-sync.md` §7, `CLAUDE.md`.

## Do first

1. **Ask Aryan to approve the hook** (`/hooks`). Ninth session that `next-prompt.md` had to be
   read by hand.
2. **Ask him how the two new pages look** — both were opened in a browser at desktop and
   420px, the Formulas tab, a flashcard flip and the library→page path were checked, but he
   has not seen them.
3. The two unanswered questions from 2026-08-31 still stand: the **AI-use remark** in the 6008
   Week 1 diary on an unlisted page, and whether the **private pages should be password-gated**.

## Open threads

- [ ] **Fix the `sync-subject` skill text** (Phase 3b, "there is no JS to write") and have
      the splice emit the `buildRef` calls. The scratchpad `reftabs.py` used this run was
      session-local and is gone; the call blocks are in any of the three fixed pages.
- [ ] **No unlisted Live page for the two new weeks** — there is no Live note for either yet.
      When one lands, `.claude/private-pages/build.py` re-run is the job.
- [ ] **`semester-2-private-notes.html` is stale and needs its password to rebuild or delete.**
- [ ] **Four syllabus files still cannot be migrated** (`file://` refs in Notion).
- [ ] **Lecturer name and email remain in git history** from `7a63ab5`; not scrubbed, not asked.

## Settled — do not re-open

- **DMBA 6005 Week 3 `Live`** stays off public week pages (`subjects.json` ruling).
- **Formula images are transcribed, never published.** Eleven more confirmed it this run.
- **DMBA 6008 Week 4's lease inconsistency stays unreconciled** ($2000 prose vs 2,200 calc).
- **Live material on unlisted pages is authorised; on public week pages it is not.**
- **Notion is a live note-taking surface feeding the vault. Never publish from it directly.**

## Do not

- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log.
- Do not link `only-accessible-by-url/` from any indexed page.
- Do not tidy his typos (`sprintsn` in the vault week name, `aroujnd`, `Agile's flexibility
  scope`, and so on). Page titles are editorial and may differ from the vault folder name.
- Do not derive a number the notes leave unstated — the explicit-FCFE PV in 6008 Week 5 is
  the live example.
