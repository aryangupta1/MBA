# Obsidian vault → site sync

How Aryan's coursework notes become week study pages in this repo. Written 2026-08-18, when
the source moved from Notion to an Obsidian vault.

This supersedes [notion-sync.md](notion-sync.md), which is kept as history of the retired
pipeline. The procedure that actually runs is
[.claude/skills/sync-subject/SKILL.md](../.claude/skills/sync-subject/SKILL.md); this file is
the ground truth about the data.

---

## 1. Where the notes are

**`~/MBA`** — an Obsidian vault, migrated out of Notion on 2026-08-18. Override with
`MBA_VAULT` if it moves. It is **not** part of this repo and must never be committed here.

```
~/MBA/
├── Semester 1 2026/            DMBA6001, DMBA6002, DMBA6004  (completed, hand-written pages)
├── Semester 2 2026/
│   └── DMBA6008 Finance, Strategy and Technology/
│       ├── DMBA6008 Index.md               generated index — has no notion_id, skip it
│       └── Week 3 Investment Evaluation Tools/
│           ├── Learn.md                    the note (a container)
│           ├── Learn/                      its sub-pages = the TOPICS
│           │   ├── Investment Appraisal.md
│           │   └── Concept of present value.md
│           └── Live.md                     publish: false
├── _attachments/               every image, as real files
└── .mba-sync/                  migration record and tooling
```

**Notion still exists, but holds only the Assignments/Exams database.** It is synced by the
separate `sync-assignments` skill into `~/MBA/Assignments & Exams.md`, which is
`publish: false` and never reaches the site. No coursework prose comes from Notion again.

## 2. Frontmatter — the contract

Every migrated note carries:

| Key | Meaning |
| --- | --- |
| `publish` | **`true` only for former `Pre-Live Session` notes.** The publish filter |
| `type` | `Pre-Live Session` / `Live Session` / `Assessment` |
| `course`, `week`, `semester` | placement |
| `notion_id` | provenance. **A file without one is repo-generated — skip it** |
| `subpages` | a container's children |

## 3. Topics — the fan-out unit

A **topic** is the first level beneath a week's note. A note with a same-named folder beside
it is a container and its children are the topics; a note without one is itself a single
topic. A topic's content is its own file **plus every descendant**, so grandchildren are
never dropped — DMBA 6008 Week 0 nests three levels deep.

`reference/vault_discover.py` computes this, applies the filters, and diffs by sha256.
Do not re-derive it by hand.

### 3b. Acronyms and Formulas tabs

Unchanged from the Notion era, because they are derived from the **assembled page**, never
from the source. That is deliberate: it means they can only contain material that already
passed gate 1.

- **A formula is copied character for character.** If the notes write
  `ROA = Asset Utilisation x Profit Margin` with a lowercase `x`, it stays a lowercase `x`.
  Never substitute the textbook form. DMBA 6008 states the sustainable growth rate one way in
  Week 0 and differently in Week 2. **Both are correct, because both are his.** Do not
  reconcile them, and never let one week's algebra leak into another's.
- If the same relationship appears in two genuinely different vocabularies on one page,
  **list both** — the difference is his.
- An **acronym** takes the page's own expansion where the page gives one. Where it does not,
  the standard expansion is allowed, but the panel's intro must say so, and a definition is
  never invented — an entry with nothing to say gives the expansion and stops.
- Skip markup: class names, `aria-*` values, SVG ids, course codes and site chrome are not
  acronyms.

## 4. Change detection

sha256 of each topic's markdown, recorded in [vault-sync-state.json](vault-sync-state.json).
Exact — no timestamp guesswork, no metering, no under-triggering on a deep edit.

That file was **seeded on 2026-08-18** for weeks that already had a page. The seed asserts
those pages match the vault; it was **not** verified line by line. If a page looks out of step
with the vault, re-harvest that week rather than trusting the hash.

## 5. Images — published since 2026-08-18

Images used to be skipped: Notion served 5-minute presigned URLs that a committed page could
not reference. **The vault holds the real files**, so that constraint is gone and Aryan
approved publishing them.

`reference/publish_images.py` copies a week's images to `assets/notes/<code>/wk<N>/`,
downscaling anything wider than 1600px. Three guarantees:

- **Output filenames use the full Notion id.** Ids in this workspace share long prefixes;
  8- and 12-char truncations both silently overwrote images during development. The script
  refuses to publish if two sources map to one filename.
- **It never inflates a file.** `sips` runs only when an image is genuinely oversized —
  re-encoding a small PNG can multiply its size.
- **It does not write alt text.** It emits `alt="TODO"`; the page builder must describe what
  the figure shows. A filename is not alt text.

This closes the gap where prose depended on a figure the page never showed — DMBA 6008 Week 3
critiques average accounting ROA while its definition sat in a skipped image.

`assets/` is the **second documented exception** to the self-contained-page rule, alongside
`blogs/assets/`. See `CLAUDE.md`.

## 6. What must never be published

`CLAUDE.md` and [content-guide.md](content-guide.md) bind here. GitHub Pages makes anything
committed public.

| `type` | `publish` | Publish? |
| --- | --- | --- |
| `Pre-Live Session` | `true` | **Yes** — the student's own structured study material |
| `Live Session` | `false` | **No** — classroom diaries |
| `Assessment` | `false` | **No** — unsubmitted academic work |

Live-session notes contain candid remarks about the lecturer, about other students' use of
AI, and about what will be examined. They are in the vault because it is his private
notebook; they are `publish: false` because none of that belongs on a public site.

**`publish: true` is necessary but not sufficient.** `subjects.json` `needsReview` holds notes
whose frontmatter says publishable but whose body says otherwise — DMBA 6005's Week 3 `Live`
is typed `Pre-Live Session` but reads as a classroom diary. Those are **held back** by
`vault_discover.py` and need a ruling from Aryan. Do not argue one into a build.

`syncRules` still bind: DMBA 6005 `no-shadow-boxing-after-week-0`, DMBA 6008
`no-pre-class-prep`. `allowedNotionIds` is the precise carve-out for an approved exception —
6005's Week 0 `Shadow Boxing` sits in `_Unfiled` with no week number, and without it a
week-based rule silently strips already-published content.

### Never publish a real person's contact details

The lecturer's `Professor`, `Email`, `Location` and `Time` were **deliberately excluded from
the vault entirely** at migration, so they cannot leak from this source. A hub's meta-row is
the status pill and the week count and nothing else. Set by Aryan 2026-08-18 after
`DMBA6008-weeks.html` was found to have been publishing the lecturer's name since the first
sync commit.

## 7. Current state

| | DMBA 6008 | DMBA 6005 |
| --- | --- | --- |
| Weeks in the vault | 0–4 | 0–3 |
| Weeks published | 0–3 | 0–3 |
| Outstanding | **Week 4 is NEW** — 3 of its 4 topics are empty in the source | none |
| Held for review | — | Week 3 `Live` |

Empty in the source, so empty on the page: DMBA 6008 Week 4's `Strategy and Finance`,
`Golden rules of project evaluation`, `Application and solution`; DMBA 6005 Week 1's
`Creating your reflective journal`.
