# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Session start — read this first

1. **`next-prompt.md` is injected into your context automatically** by a `SessionStart`
   hook (`.claude/hooks/load-next-prompt.sh`). It is the handoff note from the previous
   session and is **binding**.
2. The only exception: if the user's message contains **"Adhoc chat, ignore next prompt"**,
   skip the agenda in `next-prompt.md` entirely and just answer what is asked.
3. **Before the session ends, update `next-prompt.md`.** Full rules in
   [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).

## What this repo is

A **static website** of MBA coursework for the University of Sydney Business School —
reading summaries, case-study analyses, assessment overviews, infographics, and a blog.
It is published with **GitHub Pages** from the `master` branch at
`https://aryangupta1.github.io/MBA/`.

Author: Aryan Gupta (`agup0543@uni.sydney.edu.au`).

Subjects are grouped by semester on `index.html`.

**2026 Semester 1**

| Code | Subject | Content |
| --- | --- | --- |
| DMBA 6001 | Leading Strategic Digital Transformation | Reading summaries, case studies, blog series |
| DMBA 6002 | Digital disruption & organisations | Assessment overviews, cheat sheets, reading infographics |
| DMBA 6004 | Remote & hybrid work | Playbook summaries, weekly case studies |

**2026 Semester 2**

| Code | Subject | Content |
| --- | --- | --- |
| DMBA 6008 | Finance, Strategy and Technology | Weeks 0–3. Week hub + per-week study pages, built from the vault. Three core modes — summary & visuals, key concepts, flashcards — plus **acronyms** and **formulas** where the week has them, and **discussion questions** where a Live note supplies them (Week 2 only so far). Every week also carries a **quiz**, an **Apply it** tab and a **study path**, all derived from the built page |
| DMBA 6005 | Agile Project Development | Weeks 0–3. Week hub + per-week study pages, same modes, built from the vault. Live since 2026-08-06 |

The **quiz, Apply-it and study-path components are not synced from any source** — they are
derived from the assembled page and live in
[`.claude/skills/sync-subject/reference/practice/`](.claude/skills/sync-subject/reference/practice/README.md).
**A re-sync that changes a week must re-derive that week's practice content**; that folder's
`README.md` is binding.

Semester 2 pages are built from the Obsidian vault by the **`sync-subject` skill**
(`.claude/skills/sync-subject/`) — Aryan says *"update finance"* and it assembles, builds,
registers, and runs six QA gates. To pull his latest **Notion** writing into the vault first,
use **`sync-notes`**. Read [docs/vault-sync.md](docs/vault-sync.md) before touching those
pages — in particular, only **Pre-Live Session** notes may be published.

## Where the notes actually live — updated 2026-08-19

Aryan takes coursework notes in **both Notion and Obsidian**, and intends to keep doing so.
He likes Notion's editor; the **Obsidian vault at `~/MBA` is where he is migrating to** and
is the **single source of truth for publishing**. Everything was migrated across on
2026-08-18 — both semesters, all five subjects.

```
Notion  --sync-notes-->  Obsidian vault (~/MBA)  --sync-subject-->  week pages in this repo
                              SOURCE OF TRUTH
```

Notion is an **input to the vault, never a publishing source**. It has no record of what has
been reconciled against his Obsidian edits, so a page built from it directly could ship over
work he did in the vault.

| Thing | Lives in | Kept in sync by |
| --- | --- | --- |
| Coursework notes | **Notion and Obsidian**, reconciled in the vault | **`sync-notes`** skill, on command |
| Assignments, deadlines, quizzes | **Notion**, mirrored into the vault | **`sync-assignments`** skill, on command |
| Published week pages | this repo | **`sync-subject`** skill — reads the vault only |

The vault mirrors Notion's structure: `Semester N 2026/DMBA<code> <name>/<Week>/<Note>.md`,
container notes get a folder of sub-pages beside them, images live in `_attachments/`.
Every note carries frontmatter with `course`, `week`, `type`, `notion_id` and a **`publish`**
flag — `true` only for `Pre-Live Session` notes, `false` for Live Session diaries and
assessment work. Sync data and the harvest record sit in `~/MBA/.mba-sync/`.

### Both surfaces are live, so edits can collide

`sync-notes` classifies every page against two hashes — did Notion change, and did the vault
file change since the sync last wrote it. **A note edited in Obsidian is never overwritten.**
If both sides changed, the vault file is left alone and Notion's version is parked beside it
as `<name>.notion-incoming.md` for Aryan to merge. Never merge his academic prose yourself,
and never pass `--force` without his explicit say-so.

**`sync-subject` reads the vault, not Notion** (rebuilt 2026-08-18). Phase 0 discovers and
diffs via `reference/vault_discover.py`; Phase 2 assembles local markdown — no MCP, no
network, no metering. Change detection is an exact sha256 per topic, recorded in
`docs/vault-sync-state.json`.

> Never reach for `notion-fetch` to get coursework prose for a page. Pull it into the vault
> with `sync-notes` first, then publish from the vault.

The vault is **not** part of this repo and is **not** published. Do not add it to git here,
and do not copy `publish: false` content into any page under this repo.

## Hard constraints

- **No build step, no package manager, no framework, no dependencies.** Every page is
  hand-written HTML opened directly in a browser. Do not introduce npm, bundlers,
  Tailwind, React, or a static-site generator.
- **No external JS libraries.** The only external requests are Google Fonts stylesheets.
- **Standalone pages are self-contained** — one file, one inline `<style>` block, inline
  `<script>` if needed. **Two documented exceptions:** the `blogs/` sub-site shares
  `blogs/assets/`, and semester-2 week pages reference figures in `assets/notes/<code>/wk<N>/`.
  The second was added 2026-08-18 when Aryan approved publishing note images. Images are
  copied and downscaled by `sync-subject`'s `publish_images.py`; **every one needs real alt
  text**, and a filename is not alt text. Do not add a third exception without asking.
- **Most of the vault's "images" are formulas, and formulas are transcribed, not published.**
  Of the 17 publishable images in DMBA 6008, 16 were LaTeX renders of equations — black text
  on white. Those belong in the page's existing `.formula` / `FORMULAS` components as text:
  the Formulas tab has a **search filter** an image cannot participate in, `.formula` is a
  **dark box with light text** that a black-on-white PNG looks broken in, and text stays sharp
  and readable to a screen reader. **Look at an image before publishing it.** Publish it only
  when it is a genuine diagram — one figure, the Week 0 three-statement slide, qualified.
  Transcribe **exactly** what the image shows; never derive, complete or improve a formula.
- **`library.html` is the site registry.** A new page that is not added to the
  `articlesBySubject` object in `library.html` is unreachable. Always register it.
- **`index.html` and every Semester 2 page follow the DESK design system.** Read
  [docs/design-system.md](docs/design-system.md) before changing how any of them looks.
  A subject's identity there is **four `--accent*` values and nothing else** — same fonts,
  same components, same dock on every page. If a change needs a second token, stop and ask.
- **Never change a Semester 1 page's visual identity without being asked.** Those artefact
  pages each own their palette and typography by design, and `library.html` and `blogs/`
  still follow the older [style guide](docs/style-guide.md).
- **`only-accessible-by-url/` is unlisted content.** Never link to it from `index.html`,
  `library.html`, or any indexed page. Keep the `noindex` meta and the `robots.txt` rule.
- **Do not commit or push unless the user asks.**

## Academic-integrity constraints

This is submitted university work. Read [docs/content-guide.md](docs/content-guide.md)
before writing or editing any prose.

- **Do not write or rewrite the user's academic arguments** unless explicitly asked.
  Default to formatting, structure, layout, and correctness.
- **Never invent, alter, or "improve" a citation, DOI, URL, quote, or statistic.** If a
  reference is needed and not supplied, ask.
- Preserve the **Acknowledgement of AI Use** block on every blog post, and keep it
  accurate to what actually happened.

## Where to look

| Doc | Use it for |
| --- | --- |
| [docs/README.md](docs/README.md) | Index of all documentation |
| [docs/architecture.md](docs/architecture.md) | Site map, routing, how pages connect, deployment |
| [docs/conventions.md](docs/conventions.md) | File naming, page anatomy, registration, git |
| [docs/design-system.md](docs/design-system.md) | **DESK** — the house system for `index.html` and all Semester 2 pages. Tokens, components, the three page profiles |
| [docs/style-guide.md](docs/style-guide.md) | The older language — still governs `library.html`, Semester 1 pages and `blogs/` |
| [docs/content-guide.md](docs/content-guide.md) | Voice, referencing, AI acknowledgement, privacy |
| [docs/workflows.md](docs/workflows.md) | Step-by-step recipes for common tasks |
| [docs/vault-sync.md](docs/vault-sync.md) | **The live source of truth** — vault layout, the `publish` flag, topics, images, and what must never ship |
| [docs/notion-sync.md](docs/notion-sync.md) | The old Notion→website pipeline. History only — Notion now feeds the **vault**, not pages |
| [.claude/skills/sync-notes/SKILL.md](.claude/skills/sync-notes/SKILL.md) | **Notion → vault.** Pulling his Notion coursework notes down without overwriting Obsidian edits |
| [.claude/skills/sync-subject/SKILL.md](.claude/skills/sync-subject/SKILL.md) | **Vault → website.** The publish procedure — phases, gates, stop conditions |
| [.claude/skills/sync-assignments/SKILL.md](.claude/skills/sync-assignments/SKILL.md) | **Notion → vault.** The Assignments/Exams database into the vault's tracker note |
| [docs/notion-sync-automation.md](docs/notion-sync-automation.md) | Why the sync is shaped that way; the settled design decisions |
| [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md) | How the handoff file works |

## Verifying work

There are no tests. Verification means:

1. Open the changed page in a browser and look at it (`open <file>.html`).
2. Check it at a narrow width — every page is expected to work on mobile.
3. Follow the navigation path a reader would take: `index.html` → `library.html?subject=…`
   → the page.
4. Confirm every relative link and image path resolves (paths differ by directory depth —
   `blogs/blog-N/` pages reach shared assets via `../assets/`).
