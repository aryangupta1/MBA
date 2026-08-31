# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-31
**Left by:** A full Notion→vault→website sync, plus a new kind of page. **DMBA 6005 Week 5
is published**, and **every Live Session note is now on an unlisted per-week page** by
Aryan's explicit instruction. Committed and pushed; working tree clean.

---

## The one thing worth learning from this run

**His notes contain overlapping emphasis runs that a regex cannot parse.** Patterns like
`***Consequently, **forecast returns were inflated** “execution challenges”**` appear
throughout the 6008 live-session prep notes. A naive `**(.+?)**` / `*(.+?)*` pair turns
those into crossed tags, and two of the eight private pages failed a tag-balance check
before this was caught.

`.claude/private-pages/build.py` now uses a **stack-based emphasis tokeniser** that closes
and reopens tags around a mismatch and force-closes anything still open at end of line, so
the output is balanced whatever the input does. **Any future markdown→HTML work in this repo
should reuse `_emphasise()` rather than reaching for a regex.**

## What came down — 2026-08-31

One metered `notion-query-data-sources` call. Live inventory: **96 notes**, against 91
cached — five new, one changed, nothing deleted.

| What | Type | Where it went |
| --- | --- | --- |
| DMBA 6005 Wk5 `Learn` + `Working out costs` + `Non-financial options` | Pre-Live | **Published** — new public week page |
| DMBA 6005 Wk5 `Live` + `Live Prep` | Live Session | vault + **unlisted page** |
| DMBA 6005 `Assessment 1: User Stories & Pre-mortem` → `Plan`, `Final Version` | Assessment | vault only |
| DMBA 6008 Wk4 `Live Session` + `Prep` + `Diary` | Live Session | vault + **unlisted page** |
| DMBA 6008 `Assessment 1` → `Plan` | Assessment | vault only — **its two rubric images downloaded this time** |

`apply_harvest.py`: **10 NEW, 1 UPDATED, zero conflicts.** Nothing of his was overwritten.
Backed up first (`backup-20260831-181924`) and diffed — exactly the 11 intended files
changed, no whitespace damage, because the harvest was done **inline, not by agents**.

`verify.py`: 5 of 6 gates pass. The failure is the **expected** one — `Live Session
Transcript` and `Live Session Chat` are the only unresolved wikilinks, and they are
deliberately never harvested. **Do not "fix" it by fetching them.** There are now four such
sub-pages, not two: Week 3's pair and Week 4's pair.

## The new thing: unlisted live-session pages

Aryan asked for the live pages published but hidden. Asked how, he chose **one page per
week** and **unlisted URL only, no password** — after being shown plainly that this means
plaintext in a public repo.

```
only-accessible-by-url/<CODE>-week<N>-private.html   8 pages: 6005 wk1,3,4,5 · 6008 wk1,2,3,4
only-accessible-by-url/SECRET-PAGES.md               the index, grouped by subject
.claude/private-pages/build.py                       the builder — idempotent, re-run any time
.claude/private-pages/README.md                      what it will not publish, and why
```

`SECRET-PAGES.md` sits **inside** `only-accessible-by-url/` on purpose: the repo has no
`.nojekyll`, so a root-level `.md` can be served as a public page, and an index of unlisted
URLs must not be. `robots.txt` already disallows that whole directory.

**The withholdings are enforced in code and are not preferences:**

- The lecturer's first name appears once, in DMBA 6008 Week 1's diary
  (`… found some “fakes” last semester`). It renders as `[lecturer]`.
- The DMBA 6005 Week 3 class slide has the **lecturer's webcam thumbnail** in the corner.
  Its seven questions are transcribed as text; the PNG is not published.
- The 6008 Week 1 ROA/WACC diagram has no people in it and **is** published, at
  `assets/notes/private/`.
- Any image not in `IMAGE_ALT` renders as a withheld placeholder. **Look at an image before
  adding it.**

## What was published publicly

### DMBA 6005 Week 5 — new

`DMBA6005-week5.html`, from `week-shell.html`. 17 blocks, **7 figures**, 38 terms, 53 cards,
**3 formulas** (the subject's first Formulas tab), 3 acronyms, 10 quiz questions, 5 scenarios,
a 7-step study path. Registered in `library.html`; hub card added and its pill moved
5 → 6 weeks published.

Figures are process and portfolio vocabulary, not finance's: a cost-escalation loop, the
three viability gates, an ROI/NPV horizon band, the weighted-scoring mechanism, ten
experiment squares read two ways, an exploitation/exploration split bar, and execution
measures nested inside an outcomes ring.

**Its footer says "Built from my Obsidian vault on 31 August 2026", not "Synced from Notion".**
The other nine week pages still carry the stale Notion wording — see Open threads.

## Gates

`checks.py` clean on the new page — prose **1,469 / 2,880**, comfortably inside budget.
Gate 1 done by tracing every formula and claim back to the two topic markdown files; gate 4
swept for Live/Assessment content, lecturer fields and telemetry, all zero. The page's inline
JS was **parsed with `node --check` and the four arrays evaluated**, which is worth repeating —
it is how the `Σ` and `×` escapes in `FORMULAS` were confirmed to render.

The eight private pages were tag-balance checked, id-duplicate checked, back-link checked and
`noindex` checked; all eight pass.

**Checked in a browser:** the week page, the hub, `library.html?subject=DMBA6005`, and two
private pages were opened. **Aryan has not yet confirmed how they look** — ask him.

## Do first

1. **Ask him to approve the hook** (`/hooks`). Eighth session running that `next-prompt.md`
   was not auto-injected — it had to be read manually. `settings.json` is correct; it needs
   his one-time approval.
2. **Ask whether the private pages should keep the AI-use remark.** DMBA 6008 Week 1's diary
   says *"Most people if not all will be using AI to aid their assignments…"*. No individual
   is named, so it does not breach the name rule and it was published — but it is a candid
   remark about the cohort now sitting in plaintext in a public repo. **His call, and he has
   not been asked yet.**
3. **Ask whether he wants the private pages password-gated after all.** He chose unlisted-only
   with the tradeoff stated, but the offer stands and `semester-2-private-notes.html` already
   has a working AES-256-GCM + PBKDF2 implementation to copy.

## Open threads

- [ ] **Nine week pages still say "Synced from Notion on …" in the footer.** Pages have been
      built from the vault since 2026-08-18, so it is false on all of them. Only
      `DMBA6005-week5.html` is correct. A one-line sweep, still not done — it was out of
      scope this run too.
- [ ] **`semester-2-private-notes.html` is stale and cannot be updated.** It predates 6005
      Weeks 4–5 and 6008 Week 4. The new per-week pages supersede it, but **rebuilding or
      deleting it needs its password**, which no session has. Ask him for it, or ask whether
      to just delete it.
- [ ] **Four syllabus files could not be migrated** (6001, 6002, 6004, 6008) — Notion exposes
      them as internal `file://` refs. He must download them by hand.
- [ ] **The lecturer's name and email are still in git history**, `7a63ab5` onward. Scrubbing
      needs a history rewrite and force-push; not done, not asked.

## Settled — do not re-open

- **DMBA 6005 Week 3 `Live`** — held back from public week pages, permanently. Enforced in
  `subjects.json` → `DMBA6005.needsReview.ruling`. It appears on unlisted pages only.
- **Formula images are transcribed, never published** (2026-08-19).
- **Notion is a live note-taking surface**, feeding the vault. Never publish from it directly.
- **DMBA 6008 Week 4's lease inconsistency stays unreconciled.** His prose says five payments
  of $2000; the calculation uses 2,200; only 2,200 reproduces his own $9,174. Both are on the
  page with a note that they differ. **Do not silently fix either number.**
- **Live Session material on unlisted pages is authorised; on public week pages it is not.**
  `sync-subject` rule 1 is unchanged. The unlisted pages are not a precedent for the week pages.

## Do not

- Do not build a page from Notion. Pull into the vault with `sync-notes`, publish from there.
- Do not commit `~/MBA` to this repo.
- Do not write back to Notion from any skill. Every sync is one-way.
- Do not harvest a Live Session transcript or chat log into the vault.
- Do not link `only-accessible-by-url/` from any indexed page.
- Do not put an index of unlisted URLs at the repo root — there is no `.nojekyll`.
- Do not tidy his typos. They are preserved deliberately: `aroujnd`, `stand out form the rest`,
  `not is simply staying within the budget`, `Agile's flexibility scope`.
