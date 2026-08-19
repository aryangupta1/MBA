# Obsidian vault → site sync

How Aryan's coursework notes become week study pages in this repo. Written 2026-08-18, when
the source moved from Notion to an Obsidian vault; updated 2026-08-19, when Notion came back
as a second note-taking surface feeding that vault.

```
Notion  --sync-notes-->  Obsidian vault (~/MBA)  --sync-subject-->  week pages
                              SOURCE OF TRUTH
```

**The vault is the only thing pages are ever built from.** Aryan still writes in Notion and
likes its editor, but Notion is an *input to the vault*, never a publishing source — it has
no record of what has been reconciled against his Obsidian edits, so building a page from it
directly could ship over work he did in the vault.

This supersedes [notion-sync.md](notion-sync.md), which is kept as history of the retired
Notion→website pipeline. The procedures that actually run are
[sync-notes](../.claude/skills/sync-notes/SKILL.md) (Notion → vault) and
[sync-subject](../.claude/skills/sync-subject/SKILL.md) (vault → pages); this file is the
ground truth about the data.

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

## 3c. Two note-taking surfaces, one vault

Aryan writes in **both** Notion and Obsidian. `sync-notes` reconciles them on the way in,
and it never destroys Obsidian-only work. Every page is classified against two independent
hashes held in `~/MBA/.mba-sync/notes-state.json`:

- `raw_sha` — the Notion dump as of the last sync. Different now ⇒ **Notion changed**.
- `file_sha` — the vault file *as the sync itself last wrote it*. Different from what is on
  disk now ⇒ **Aryan edited it in Obsidian**.

| Notion changed | Obsidian edited | Action |
| --- | --- | --- |
| no | no | `UNCHANGED` |
| yes | no | `UPDATED` — safe overwrite |
| no | yes | `KEPT-LOCAL` — his edit stands |
| **yes** | **yes** | **`CONFLICT`** — vault file untouched; Notion's version parked as `<name>.notion-incoming.md` |

**Never merge a conflict yourself.** The content is his academic prose; show him both sides
and let him decide. `--force` exists for him to authorise, not for Claude to choose.

One caveat worth knowing: **Notion does not bump a parent note's last-edited time when a
sub-page's body is edited**, and his lecture notes live in sub-pages. So timestamp-based
triage (`--changed-only`) under-reports. The default re-fetches the scope and diffs on real
content.

---

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

### Formula images are transcribed, not published — settled 2026-08-19

The backfill that closed this gap found that **16 of DMBA 6008's 17 publishable images were
formulas**, not diagrams: LaTeX renders of equations, black text on white. Publishing them as
PNGs would have been the wrong fix on every axis.

- The Formulas tab has a **search filter**. An image cannot be filtered, so a formula shipped
  as a PNG is invisible to the one feature built to find it.
- `.formula` is a **dark box with light text**. A black-on-white PNG dropped into it reads as
  broken.
- Text stays sharp at any zoom and is readable to a screen reader. A 5 KB PNG of an equation
  is none of those things.

So the rule is: **look at the image before publishing it.** If it is a formula, transcribe it
into `.formula` in the prose and add an entry to the `FORMULAS` array. If it is a genuine
diagram, publish it with real alt text. One image met that bar — the Week 0 slide showing the
three statements as one system, which nothing on the page reproduced.

Transcribe **exactly** what the image shows. Never derive, complete or improve a formula: in
Week 3 the notes repeat one NPV() image where the text implies a second, different equation,
and that gap is stated in words rather than filled in.

This closed the gap where prose depended on a figure the page never showed — DMBA 6008 Week 3
critiqued average accounting ROA while its definition sat in a skipped image. It now carries
the definition.

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

Notion→vault sync state is seeded for all **296** pages as of 2026-08-19
(`~/MBA/.mba-sync/notes-state.json`), so the conflict guard has a baseline for every note.

| | DMBA 6008 | DMBA 6005 |
| --- | --- | --- |
| Weeks in the vault | 0–4 | 0–3 |
| Weeks published | **0–4** | 0–3 |
| Outstanding | Week 4 published in progress (2026-08-19, Aryan's call) — 3 of its 4 topics are still empty in the source and render as "not yet written" | none |
| Held for review | — | Week 3 `Live` |

Empty in the source, so empty on the page: DMBA 6008 Week 4's `Strategy and Finance`,
`Golden rules of project evaluation`, `Application and solution`; DMBA 6005 Week 1's
`Creating your reflective journal`.
