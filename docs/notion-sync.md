# Notion → site sync

How coursework notes in Notion become week study pages in this repo. Written 2026-08-05,
after the first run of the pipeline against **DMBA 6008 Finance, Strategy and Technology**.

This document describes the **manual pipeline that works today**. The design for automating
it (`"Update finance"` → one command) lives in
[notion-sync-automation.md](notion-sync-automation.md).

---

## 1. What is in Notion

The MBA workspace is a personal Notion workspace, reached over the **Notion MCP server**
(`https://mcp.notion.com/mcp`). It is authenticated interactively and per-machine — a new
session may need `/mcp` before any of this works. MCP tool schemas are deferred; load them
with `ToolSearch` (`select:mcp__notion__notion-fetch`, etc.).

Top-level page: **MBA** — `3097b336-873c-8025-b728-d96b85cbfec0`

### The three databases that matter

```
Courses  ──┬── Notebooks (one per week) ──── Notes (Pre-Live / Live / Assessment)
           └── Notes (direct relation, mirrors the notebook relation)
```

| Database | Data source URL | Title column |
| --- | --- | --- |
| Courses | `collection://3097b336-873c-81b6-aa7c-000b6577c6c6` | `Name` |
| Notebooks | `collection://3097b336-873c-814d-b93f-000b3ee9948a` | `Topic` |
| Notes | `collection://3097b336-873c-816a-b24d-000b141a5afe` | `Name` |

**Courses** columns: `Course Code`, `Name`, `Semester` (`SEM 1 2026` \| `SEM 2 2026`),
`Status` (`Planned` \| `In Progress` \| `Completed`), `Professor`, `Notebooks` (relation),
`Notes` (relation), `Assignments`, `Syllabus`, `Email`, `Location`, `Time`.

**Notebooks** columns: `Topic` (the week name), `Course` (relation), `Notes` (relation),
`Confidence` (`Not Confident` \| `Somewhat Confident` \| `Confident`).

**Notes** columns: `Name`, **`Type`** (`Pre-Live Session` \| `Live Session` \| `Assessment`),
`Notebook` (relation), `Course` (relation), `Related Notes`, `Assignments`, `Favorite`,
`Last Reviewed`, `Created Time`, `Edited Time`, `Days Since` (formula).

`Type` is the field the whole pipeline pivots on. **Only `Pre-Live Session` notes are
published.** See [§6 What must never be published](#6-what-must-never-be-published).

### Course page IDs

| Code | Notion page | Semester | Status |
| --- | --- | --- | --- |
| DMBA6001 | `3097b336873c80968073e1efcf72711d` | SEM 1 2026 | Completed |
| DMBA6002 | `3097b336873c80e0801fc3d2462d1cf9` | SEM 1 2026 | Completed |
| DMBA6004 | `3097b336873c80d3800df8c3f77b2a8b` | SEM 1 2026 | Completed |
| **DMBA6008** | `3097b336873c80c0948dcc805089b071` | SEM 2 2026 | **In Progress** |
| **DMBA6005** | `3a17b336873c80c284a7cd6be4a60c4d` | SEM 2 2026 | **In Progress** |

Notion's course names are fuller than this repo's shorthand — Notion calls DMBA 6004
"Digital Collaboration, Work and Organisation" and DMBA 6002 "Emerging Technology, Disruption
and Foresight". The repo's `index.html` uses shorter topic labels. **Do not reconcile these
without asking** (`next-prompt.md` has an open thread on DMBA 6004's title).

### Two content shapes — this is the part that varies by subject

The `Notes` row is a *page*, and its content can sit in one of two places:

**Shape A — container note (DMBA 6008).** The note page holds only links to child pages, and
each child may hold further children. The real prose is two or three levels down.

```
Notebook  "Week 0"
└── Note  "Financial Management"          Type: Pre-Live Session
    ├── page "The Balance sheet"
    │   ├── page "Current Assets"          ← prose lives here
    │   └── page "Liabilities"             ← and here
    └── page "Cash Flow"
        └── page "Operating Cash Flow"     ← and here
```

**Shape B — inline note (DMBA 6005).** The note page *is* the content: headings, tables and
callouts sit directly on it, no children.

```
Notebook  "Week 0"
└── Note  "$RUs"                          Type: Pre-Live Session
    (headings, tables, callouts inline)
```

A harvester must handle both: fetch the note, and if its `<content>` is nothing but
`<page url=…>` links, recurse; otherwise take the body as-is.

---

## 2. Where it lands in this repo

Three page kinds, all at repo root, all self-contained (see
[conventions.md](conventions.md)):

| File | Role |
| --- | --- |
| `DMBA<code>-weeks.html` | **Subject hub.** Lists every week as a card. One per subject. |
| `DMBA<code>-week<N>.html` | **Week study page.** Three tabbed modes. One per week. |
| `library.html` | Registry — every new page must be added to `articlesBySubject` |

The week page has exactly three modes, driven off that week's **pre-live** content:

1. **Summary &amp; visuals** — the whole week condensed, with hand-authored inline SVG figures,
   formulas, worked examples and tables.
2. **Key concepts** — a filterable glossary of terms and formulas.
3. **Flashcards** — a flippable deck for active recall.

`DMBA6008-week1.html` is the **reference implementation**. Clone its `<style>` block and its
`<script>` wholesale for a new week; only the three data structures and the summary markup
change:

- `TERMS` — array of `{ term, src, def, formula? }` (add `own: true` for definitions copied
  verbatim from the student's own definitions table, which renders a distinguishing chip)
- `CARDS` — array of `{ q, a }`
- the `#panel-summary` markup

The class vocabulary those fragments may use is specified in
`WEEK-PAGE-SPEC.md` (kept in the session scratchpad and reproduced in
[notion-sync-automation.md](notion-sync-automation.md#the-fragment-spec)).

---

## 3. The pipeline, step by step

### Step 1 — Resolve the course and its weeks

```
fetch  self                          → confirm the right workspace
query  Courses data source           → the course row, its Notebooks relation
fetch  each notebook URL             → week name, Notes relation, Confidence
fetch  each note URL                 → Type, and either children or inline content
```

`notion-query-data-sources` is **metered on this Notion plan** (`available_with_limit`).
Prefer `notion-fetch` on relation URLs, which is not metered. One SQL query to list a
course's notebooks is fine; a query per note is waste.

### Step 2 — Harvest to Markdown, verbatim

Fan out one agent per topic. Each agent recursively fetches its subtree and writes
`scratchpad/notion/wk<N>-<topic>.md` — **verbatim**, preserving typos, Australian spelling and
awkward phrasing. The agent returns only a manifest (titles, word counts, anomalies), never
the content, so the orchestrator's context stays clean.

Conversions the harvester must perform:

| Notion output | Becomes |
| --- | --- |
| `<table>` + `<colgroup>` | GitHub-flavoured Markdown table |
| `<callout icon="X">text</callout>` | `> [!X] text` |
| `<empty-block/>`, `<table_of_contents/>` | dropped |
| `\$`, `\>`, `\<` | `$`, `>`, `<` (Notion escapes these) |
| `$\`Profit = Revenue - Expenses\`$` | plain text — a Notion equation-block artefact |
| image | `![IMAGE](url)`, **not downloaded** — see [§5](#5-gotchas) |

### Step 3 — Build the page fragments

Fan out one agent per topic again, each reading:

1. the fragment spec (class vocabulary, SVG rules, output format),
2. `DMBA6008-week1.html` as the worked reference,
3. **only** its own harvested Markdown file.

Each returns `SUMMARY` (HTML fragment), `TERMS` (JS array), `CARDS` (JS array).

Give each agent a **unique SVG id prefix** (`bs`, `pl`, `cf`) so `aria-labelledby` targets
do not collide when the fragments are concatenated into one page.

### Step 4 — Assemble, register, verify

1. Paste the fragments into the week-page shell; merge the `TERMS` and `CARDS` arrays.
2. Add the page to `articlesBySubject` in `library.html`. **`articlesBySubject` and
   `validSubjects` must be edited together** — a subject in one but not the other silently
   falls back to DMBA 6002.
3. Drop `card--muted` from the subject's card in `index.html` once it has its first page.
4. Verify — see [§4](#4-verifying).

---

## 4. Verifying

There are no tests. Verification is:

```sh
# tag balance — catches the unclosed <div> that a long hand-written page will eventually have
python3 -c "..."   # see notion-sync-automation.md for the snippet

open DMBA6008-weeks.html
open DMBA6008-week1.html
open "file:///Users/aryan/Documents/MBA/library.html?subject=DMBA6008"
```

Then walk the reader's path: `index.html` → `library.html?subject=DMBA6008` →
`DMBA6008-weeks.html` → a week page → back link returns to the library. Check every page at a
narrow width. Check that SVG text sits inside its boxes — hand-authored SVG has no layout
engine, and overflowing labels are the most common defect.

Query-string pages need a real URL locally. Plain `open library.html?subject=…` fails; the
shell treats it as a filename.

---

## 5. Gotchas

These all bit during the first run.

- **Archived notebooks still appear in the relation.** DMBA 6008's Course row lists a
  `Week 0: Fundamentals of financial management` notebook that `notion-fetch` returns with a
  `deleted` attribute on the `<page>` element. Skip anything flagged `deleted`.
- **One Note URL 404s from every notebook.** `83e72ed6-425f-4c30-9f45-c2f9c45e08fd` is in the
  `Notes` relation of every DMBA 6008 and DMBA 6005 notebook and returns `object_not_found`.
  It is a stale or inaccessible relation. Skip it; do not treat it as a failure.
- **Images are useless in a static page.** Notion returns presigned S3 URLs carrying
  `X-Amz-Expires=300`. They die in five minutes. To publish an image it must be downloaded
  (`notion-download-attachment`) and committed to the repo — which makes it public. Ask first.
- **Empty pages are real content signals.** All ten children of DMBA 6008 Week 0's
  "Assessing Financial Performance" are empty, matching the unticked item in that notebook's
  todo list. Render this honestly as "not yet written". **Never fill a gap with invented
  material.**
- **Truncated sentences and bare headings exist.** e.g. `"Analysts may examine profit before and "`,
  and a `# Key Insight` heading with nothing under it. Reproduce or omit — never complete.
- **Notion titles can contain escaped characters.** DMBA 6005's Week 0 note is named
  `\$RUs` in the API and `$RUs` to a reader.
- **`notion-query-data-sources` is metered**; `notion-query-meeting-notes` requires a Business
  upgrade and is unavailable.

---

## 6. What must never be published

`CLAUDE.md` and [content-guide.md](content-guide.md) bind here, and the standing rule from
`next-prompt.md` is: **never move content from Notion into a committed file without explicit
approval for that specific content.** GitHub Pages makes anything committed public.

| Notes `Type` | Publish? |
| --- | --- |
| `Pre-Live Session` | **Yes** — this is the student's own structured study material |
| `Live Session` | **No, by default** — see below |
| `Assessment` | **No** — unsubmitted academic work |

Live-session notes are classroom diaries. DMBA 6008's Week 1 diary contains candid remarks
about the lecturer, about other students' use of AI, and about what will be examined. DMBA
6005's contains a note-to-self. None of that belongs on a public site. It is harvested to
scratchpad for reference and marked **do not publish**.

Also excluded by default, as personal study telemetry rather than coursework:

- the Notebooks `Confidence` field (`Not Confident` etc.)
- `Last Reviewed`, `Days Since`, `Favorite`
- the unticked todo lists on notebook pages

Publishing any of these is a per-subject decision for the author, not a default.

Academic integrity, unchanged from [content-guide.md](content-guide.md): summarising and
restructuring the student's own notes is fine and is the whole point of this pipeline.
Generating new academic argument, inventing a citation, or "improving" a claim is not.

---

## 7. Current state

**DMBA 6008 Finance, Strategy and Technology** — synced 2026-08-05.

| Week | Notion notebook | Published |
| --- | --- | --- |
| Week 0 | `3a17b336873c805b9c4acdff38033d35` | `DMBA6008-week0.html` — balance sheet, P&amp;L, cash flow. "Assessing Financial Performance" is empty in Notion and shown as not yet written. |
| Week 1 | `3b27b336873c8070953fd96878f5f2dc` | `DMBA6008-week1.html` — key value principles, concepts, assessing performance, key definitions |

**DMBA 6005 Agile Project Development** — not yet synced. Three notebooks exist:

| Notebook | State |
| --- | --- |
| `Week 0` (`3ae7b336873c806da6b6e5630c66e3bb`) | One pre-live note, `$RUs` — a ~700-word digital innovation case study, **inline** (Shape B). Ready to sync. |
| `Week1: Project Management` (`3b17b336873c80ada0b3f4a02cb2dea8`) | Pre-live unwritten (`- [ ] Pre-Live` unticked). Only a `Class Diary` live-session note exists. Not publishable yet. |
| `New Notebook` (`3b37b336873c80db9388ee1a56192b33`) | Empty placeholder. Skip. |

See [notion-sync-automation.md](notion-sync-automation.md#extending-to-dmba-6005) for what
changes when the pipeline runs against 6005.
