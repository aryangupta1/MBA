# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-09-07 (evening)
**Left by:** Built the two **master search pages** on Aryan's instruction — one dictionary per
Semester 2 subject, every term, acronym, formula and flashcard across all weeks, searchable.
Committed and pushed.

---

## What was built — 2026-09-07

| Page | Entries | Terms | Acronyms | Formulas | Flashcards |
| --- | --- | --- | --- | --- | --- |
| `DMBA6008-search.html` (Weeks 0–5) | 1,157 | 372 | 64 | 201 | 520 |
| `DMBA6005-search.html` (Weeks 0–6) | 915 | 339 | 35 | 41 | 500 |

- **Generated, not hand-written.** `.claude/skills/sync-subject/reference/search/build_search.py`
  extracts the `TERMS` / `ACRONYMS` / `FORMULAS` / `CARDS` arrays from the built week pages
  (bracket-aware scanner, evaluated in Node — a build-time tool only; the site still has no
  dependencies) and splices them into `reference/search/search-shell.html`. Run
  `python3 .claude/skills/sync-subject/reference/search/build_search.py all` from the repo
  root. Every count on the page comes from the arrays. Extraction was cross-checked against
  every week page's hero pills and reference-tab counts: zero mismatches.
- **Derived, so binding on every re-sync** — same status as `reference/practice/`. The skill
  now has a **Phase 3d** for it; `subjects.json` gained `searchPage`; the week shell gained a
  `{{SEARCH_PAGE}}` placeholder that Phase 4 must fill (`docs/workflows.md` has the recipe).
- **Wiring:** each hub has a pinned `.lookup` search card (a `GET ?q=` form) above the week
  grid and a `Master search →` hero pill; every week page has a second back pill `Search all
  weeks`; both pages are registered in `library.html` under the hub entry.
- **Design:** Open-window DESK profile, stylesheet sliced from `week-shell.html`, no new
  token. Same-named entries across weeks group into one card with a sense per week. On
  phones the filter chips fold behind a `Filters` toggle (open they made the sticky bar
  ~320 px tall). Documented in `docs/design-system.md` §5 and the folder `README.md`.
- **Verified in Chrome** at desktop and 390 px: no console errors, no horizontal overflow,
  searches (`npv`, `roa wacc`, `(1 + r)^t`, `working capital`, `velocity`), the hub form
  landing with `?q=WACC`, the week-page pills, the 6005 palette and dock ring. `checks.py`
  clean on both search pages, both hubs and two week pages.

## Do first

1. **Ask Aryan how the search pages look** — he has not seen them. Open
   `DMBA6008-search.html`, try a lookup, then a phone width.
2. **Ask him to approve the hook** (`/hooks`). Tenth session that `next-prompt.md` had to be
   read by hand.
3. He has also not yet seen **DMBA 6008 Week 5** and **DMBA 6005 Week 6** from earlier today.
4. The two unanswered questions from 2026-08-31 still stand: the **AI-use remark** in the 6008
   Week 1 diary on an unlisted page, and whether the **private pages should be password-gated**.

## Open threads

- [ ] **The `buildRef` skill text is now fixed** (Phase 3b says the call blocks must be
      emitted). What is still missing is a splice that emits them automatically — today it is
      "copy from `DMBA6008-week4.html`". Worth folding into the next sync's tooling.
- [ ] **No unlisted Live page for 6008 Week 5 or 6005 Week 6** — no Live note yet. When one
      lands, re-run `.claude/private-pages/build.py`.
- [ ] **`semester-2-private-notes.html` is stale and needs its password to rebuild or delete.**
- [ ] **Four syllabus files still cannot be migrated** (`file://` refs in Notion).
- [ ] **Lecturer name and email remain in git history** from `7a63ab5`; not scrubbed, not asked.
- [ ] Possible follow-ups Aryan may ask for, not started: deep-linking a search result to
      the right **tab** of its week page (the week pages do not read a hash today), and a
      cross-subject search (the pages are deliberately one per subject, as asked).

## Settled — do not re-open

- **The search pages add no content.** A wrong entry is fixed on the week page, then rebuilt.
- **One search page per subject**, alongside the weeks, as Aryan asked — not one site-wide.
- **DMBA 6005 Week 3 `Live`** stays off public week pages (`subjects.json` ruling).
- **Formula images are transcribed, never published.**
- **DMBA 6008 Week 4's lease inconsistency stays unreconciled** ($2000 prose vs 2,200 calc).
- **Live material on unlisted pages is authorised; on public week pages it is not.**
- **Notion is a live note-taking surface feeding the vault. Never publish from it directly.**

## Do not

- Do not hand-edit `DMBA60xx-search.html`; change the shell or the source page and rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log.
- Do not link `only-accessible-by-url/` from any indexed page.
- Do not tidy his typos (`sprintsn`, `aroujnd`, `Agile's flexibility scope`, and so on).
- Do not derive a number the notes leave unstated.
