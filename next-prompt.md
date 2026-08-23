# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-23
**Left by:** A full Notion→vault→website sync, committed and pushed. Aryan had written new
material in Notion; four things came down. (1) **DMBA 6008 Week 4 is now complete** — its
three "not yet written" topics were written and are published, which is the big one.
(2) **DMBA 6005 Week 4 is a new page**, live. (3) A new **Assessment 1 notebook** landed in
6008, `publish: false`. (4) DMBA 6008 Week 3's `Live` note grew, `publish: false`.
Working tree clean; `master` level with `origin/master`.

---

## The one thing worth learning from this run

**A sub-page edit does not bump its parent note's `Edited Time` in Notion.** The skill warns
about it; this run is the proof. DMBA 6008 Week 4's `Learn` note reported **UNCHANGED** at
every level the inventory can see — same timestamp as 2026-08-18 — while three of its four
sub-pages had gone from empty to ~650 words each. A timestamp-driven sync would have missed
the single most important change in the workspace.

**So: after the inventory pass, always re-fetch the sub-pages of any week that is published
in progress or otherwise incomplete.** That is where his writing actually lands.

## What came down — 2026-08-23

One metered `notion-query-data-sources` call. Live inventory: **91 notes**, against 88 cached
— three new. Plus one changed, plus the invisible sub-page edits above.

| What | Type | Where it went |
| --- | --- | --- |
| DMBA 6008 Wk4 `Strategy and Finance` | Pre-Live | **Published** — was empty |
| DMBA 6008 Wk4 `Golden rules of project evaluation` | Pre-Live | **Published** — was empty |
| DMBA 6008 Wk4 `Application and solution` | Pre-Live | **Published** — was empty |
| DMBA 6005 Wk4 `Learn` + 4 topic sub-pages | Pre-Live | **Published** — new page |
| DMBA 6005 Wk4 `Live` | Live Session | vault only |
| DMBA 6005 Wk4 `Shadow Boxing` | (blank in Notion) | vault only; also excluded by `syncRules` |
| DMBA 6008 `Assessment 1: Financial Analysis` → `Plan` | Assessment | vault only |
| DMBA 6008 Wk3 `Live` | Live Session | vault only — gained IRR-vs-NPV and breakout notes |

`apply_harvest.py`: **8 NEW, 4 UPDATED, 94 UNCHANGED, zero conflicts.** Nothing of his was
overwritten. The raw cache was backed up first (`backup-20260823-171237`) and diffed — exactly
the 12 intended files changed, no whitespace damage, because the harvest was done inline
rather than by agents.

## Two things deliberately left undone — tell Aryan

1. **The Assessment 1 `Plan` note has two sub-pages that were NOT harvested**: `Live Session
   Transcript` and `Live Session Chat`. A transcript and a class chat log would carry **the
   lecturer's name and classmates' words** into the vault, and sync-notes rule 3 forbids that
   absolutely. They are the **only** two unresolved wikilinks `verify.py` reports — that gate
   failure is expected and documented, not a defect. **Do not "fix" it by fetching them.**
   If Aryan wants that material, ask him how he wants it de-identified first.
2. **The `Plan` note's two rubric images were not downloaded.** Notion's presigned URLs had
   already expired by the time the raw was written. The note is `publish: false`, so nothing
   on the site is missing; the vault copy just has no rubric screenshots. Trivial to re-fetch
   if he wants them.

## What was published

### DMBA 6008 Week 4 — finished

The three placeholder blocks and the "one topic of four" closing block were replaced with
**16 real blocks**. Page went 8 → 21 summary blocks, 1 → 4 figures, 12 → **48** key terms,
20 → **58** flashcards, 4 → **23** formulas, 3 → **9** acronyms, 5 → **14** quiz questions,
4 → **6** scenarios.

- **No images this time** — all three new topics are pure text, so the transcribe-vs-publish
  decision did not arise. The whole Woods Ltd model went into `FORMULAS` as text, and the
  Formulas search filter was verified working on it (`working capital` → 5 of 23).
- Every stale sentence was swept: meta description, standfirst, hub card, `library.html`
  entry, the three panel intros and the closing block. Nothing still says "in progress".
- **The practice JSON was re-derived**, per `practice/README.md`. Study path rewritten from
  a "short week, one topic" route to a seven-step, two-hour route; nine questions and three
  scenarios added covering the new topics; one redundant scenario dropped.

### DMBA 6005 Week 4 — new

`DMBA6005-week4.html`, built from `week-shell.html`. 37 blocks, **9 figures**, 60 terms,
99 cards, 10 acronyms, 12 quiz questions, 6 scenarios. No Formulas tab — it is a case and
process week with no equations, and the spec says do not pad one to fill the template.

Figures are case/process vocabulary, not finance's: a triple-constraint triangle, an
attention→memory→behaviour strip, concentric outer/inner rings, a WBS tree, the six-step
governance cycle with its return arrow, nested UI/UX/CX boxes, a customer-journey strip with
touchpoint markers, the AI-capability-to-relationship chain, and three balance beams for the
unresolved tensions.

## Gates

All six pass on both pages. `checks.py` clean. Prose **1,167 / 3,360** (6008) and
**2,829 / 5,920** (6005) — comfortably inside budget. Gate 1 done by tracing every numeric
token back to the source markdown; gate 4 swept for lecturer fields, telemetry, Pre-Class Prep
and Live-note content, all zero. **Checked in a real browser** at 1400px and at 420px: figures
render, quiz scores, formula filter works, tables scroll inside their own containers, tab bar
wraps cleanly, hub cards and both `library.html` entries live.

**His typos are preserved verbatim, as required** — `executred`, `exlcude`, `componenots`,
`btter`, `acceptnace`, `exeuction`, `become ad hoc?`, `feel distance and abstract`,
`Australian's in their 30s`. Do not tidy them.

## Do first

1. **Ask him to approve the hook** (`/hooks`). Seventh session running that `next-prompt.md`
   was not auto-injected — it had to be read manually. `settings.json` is correct; it needs
   his one-time approval.
2. **Tell him about the two withheld sub-pages** (above). That is his call, not ours.
3. **The private notes page is now stale.** `only-accessible-by-url/semester-2-private-notes.html`
   is hand-built and no skill updates it. Since it was written, DMBA 6008 Week 3's `Live`
   gained the IRR-vs-NPV material and the breakout-session notes, and DMBA 6005 Week 4's
   `Live` is new. **If he wants it current, it must be rebuilt by hand** — and the three
   privacy withholdings re-applied (the 6005 class slide with the webcam thumbnail, the
   Persona C portrait, the lecturer's name).

## Settled — do not re-open

- **DMBA 6005 Week 3 `Live`** — held back from public week pages, permanently. Enforced in
  `subjects.json` → `DMBA6005.needsReview.ruling`. It appears on the password-gated private
  page only; that is not a precedent.
- **Formula images are transcribed, never published** (2026-08-19).
- **Notion is a live note-taking surface**, feeding the vault. Never publish from it directly.
- **DMBA 6008 Week 4's lease inconsistency stays unreconciled.** His prose says five payments
  of $2000; the calculation uses 2,200; only 2,200 reproduces his own $9,174. Both are on the
  page with a note that they differ. **Do not silently fix either number.**

## Still open

- **Four syllabus files could not be migrated** (6001, 6002, 6004, 6008) — Notion exposes them
  as internal `file://` refs. He must download them by hand.
- **The lecturer's name and email are still in git history**, `7a63ab5` onward. Scrubbing needs
  a history rewrite and force-push; not done, not asked.
- **Every week page's footer still says "Synced from Notion on …".** Since 2026-08-18 pages are
  built from the vault, so the wording is stale on all nine. A one-line sweep, but it was not
  asked for and touching nine pages unprompted felt out of scope. Worth doing next time
  something else brings those files into play.

## Do not

- Do not build a page from Notion. Pull into the vault with `sync-notes`, publish from there.
- Do not commit `~/MBA` to this repo.
- Do not write back to Notion from any skill. Every sync is one-way.
- Do not harvest a Live Session transcript or chat log into the vault.
- Do not add a third exception to the self-contained-page rule without asking.
