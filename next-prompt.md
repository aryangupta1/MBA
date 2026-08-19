# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-19
**Left by:** Two jobs. (1) Notion is **not** retired — Aryan still writes there and will use
both tools until he's comfortable in Obsidian; built the **`sync-notes`** skill (Notion →
vault) and rewired every doc that said otherwise. (2) **Fixed the images**, which turned out
to mean the opposite of publishing them: 16 of 17 were formula screenshots and were
transcribed into the pages as text. Nothing is committed.

---

## The shape of things now

```
Notion  --sync-notes-->  Obsidian vault (~/MBA)  --sync-subject-->  week pages in this repo
                              SOURCE OF TRUTH
Notion  --sync-assignments-->  the vault's assignment tracker
```

**The vault is still the only thing pages are built from.** Notion is an *input to the
vault*, never a publishing source — it has no idea what has been reconciled against his
Obsidian edits, so building a page from it directly could ship over work he did in the vault.
`sync-subject` was NOT loosened; it still reads the vault and only the vault.

## What was built this session

### `sync-notes` — the new skill (`.claude/skills/sync-notes/`)

Phase 0 refresh inventory (one metered query) → 1 scope → 2 harvest with agents →
3 apply with the **conflict guard** → 4 `verify.py` → 5 offer to hand off to `sync-subject`.

**He writes in both tools, so edits collide. This is the whole point of the skill.** Every
page is classified against two hashes in `~/MBA/.mba-sync/notes-state.json`:

| Notion changed | Obsidian edited | Action |
| --- | --- | --- |
| no | no | `UNCHANGED` |
| yes | no | `UPDATED` |
| no | yes | `KEPT-LOCAL` — his edit stands |
| **yes** | **yes** | **`CONFLICT`** — vault file untouched, Notion's version parked as `<name>.notion-incoming.md` |

All three non-trivial branches were **tested against a real note and the vault restored
byte-identically**. Baseline seeded for all **296** pages.

**Never merge a conflict yourself** — it is his academic prose. **Never pass `--force`**
without him saying so; it exists for him to authorise.

### Verified against live Notion, not assumed

- Cached inventory matches live: 88 rows, identical newest-4 timestamps. Nothing has changed
  in Notion since the migration.
- Re-fetched DMBA 6008 Week 4's `Learn` — **byte-identical** to the cached raw.
- Full scoped pipeline run → 5 pages, all `UNCHANGED`. Idempotent.
- `verify.py` → **all six checks pass**, 225 `publish: true` / 72 `false`.

### One real correction found

The Notes data source columns are **`"Created Time"` / `"Edited Time"`**, *not* the
`date:Created time:start` form the old docs implied — those two are `created_time` /
`last_edited_time` system properties. The wrong form costs a metered query. Corrected and
noted in the skill.

## The image backfill — done, and not the way it looked

Aryan said "fix the images" on 2026-08-19. **Looking at them first changed the job entirely.**

Of the 17 publishable images in DMBA 6008 (DMBA 6005 has **none** — its only image sits under
a Shadow Boxing note his own rule excludes), **16 were LaTeX renders of equations**, black text
on white. Publishing those as PNGs would have been wrong on every axis: the Formulas tab has a
**search filter** an image cannot participate in, `.formula` is a **dark box with light text**
that a black-on-white PNG looks broken inside, and text stays sharp and reaches a screen reader.

So they were **transcribed into the pages as text**, into the existing `.formula` divs and
`FORMULAS` arrays:

| Page | Formulas added | Formula count |
| --- | --- | --- |
| DMBA6008-week0 | 4 (ROA identity expanded, ROE = Profit / Equity, leverage→ROE, ↓ROA+↑Leverage) | 82 → 86 |
| DMBA6008-week2 | 4 (common-size %, asset utilisation, algebraic ROA and ROE) | 16 → 18 |
| DMBA6008-week3 | 5 (PV symbolic + worked, Average ROA, average book value, Excel NPV()) | 13 → 18 |

**One image was published** — the Week 0 lecture slide showing the three statements as one
system, which nothing on the page reproduced. It carries a full alt-text description and a
caption naming the two arrows that are its point. `assets/` now holds exactly that one file.
The other 16 PNGs were deleted rather than shipped as orphans.

**The Week 3 ROA gap is closed.** The page now defines average ROA where it critiques it.
Every *"held as images / not reproduced / were not published"* sentence across the three pages
was hunted down and corrected, including the study-path and Formulas-tab intros.

Verified: all three pages parse clean, `checks.py` reports **no findings**, the published
image loads at its true 1600×1084, and the new Week 3 formulas **filter correctly** in the
Formulas search — the exact capability an image could never have had.

**The rule is now written down in three places** (`CLAUDE.md`, `docs/vault-sync.md`,
`sync-subject/SKILL.md`): **look at every image before publishing it.** Formula → transcribe.
Genuine diagram → publish with real alt text. Transcribe *exactly*; never derive, complete or
improve a formula — that is writing his academic content.

> One honest gap, left as a gap: Week 3's notes repeat the same `NPV()` image twice where the
> prose implies the second should show CF0 added. The page states that in words rather than
> inventing the equation. **Worth telling Aryan so he can fix the Notion source.**

## Do first

1. **Ask him to approve the hook** (`/hooks`). Sixth session running that `next-prompt.md`
   was not auto-injected. `settings.json` is correct; it needs his one-time approval.
2. **Nothing is committed.** `git status`: `sync-notes/` and `assets/` untracked, plus edits
   to the three DMBA 6008 week pages, `CLAUDE.md`, `docs/README.md`, `docs/vault-sync.md`,
   `docs/notion-sync.md`, `.claude/skills/sync-subject/SKILL.md`.
3. **DMBA 6008 Week 4 is NEW and unpublished.** Confirmed from live Notion: only
   `Recap of NPV` (2,646 bytes) has content; `Strategy and Finance`,
   `Golden rules of project evaluation` and `Application and solution` are **0 bytes — empty
   in Notion itself**. Do not generate filler. Worth telling him they're blank so he can
   write them. **Its 2 images are both formulas** — the multi-period `PV = CFt / (1+r)^t` and
   a lease worked example totalling $9,174 — so transcribe them, do not publish them.

## Settled — do not re-open

- **DMBA 6005 Week 3 `Live`** — Aryan ruled 2026-08-18: **hold it back.** Never published, in
  any week, in any rebuild, regardless of its `Pre-Live Session` Type. Enforced in
  `subjects.json` → `DMBA6005.needsReview.ruling`. The Type argument is closed.
- **Notion is a live note-taking surface again** (2026-08-19). Any doc still saying his notes
  "are no longer in Notion" is stale — that phrasing was purged this session.
- **Formula images are transcribed, never published** (2026-08-19). Settled during the
  backfill and written into three docs. Do not paste equation PNGs onto a page.

## Still open

- **Four syllabus files could not be migrated** (6001, 6002, 6004, 6008). Notion exposes them
  as internal `file://` refs, not signed URLs. He must download them by hand if he wants them.
- **The lecturer's name and email are still in git history**, `7a63ab5` onward. Scrubbing
  needs a history rewrite and force-push; not done, not asked. They were kept out of the
  vault entirely.

## Do not

- Do not build a page from Notion. Pull into the vault with `sync-notes`, publish from there.
- Do not commit `~/MBA` to this repo.
- Do not write back to Notion from any skill. Every sync is one-way.
- Do not add a third exception to the self-contained-page rule without asking.
