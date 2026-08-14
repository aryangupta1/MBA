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

### Step 3b — Derive the Acronyms and Formulas tabs

These two tabs are **derived from the assembled page, not harvested from Notion.** Run the
extraction after Step 4 has produced the page, against the page itself — the summary blocks,
the `TERMS` array and the `CARDS` array. Deriving them from the built page rather than the
raw harvest means they can only ever contain material that already passed gate 1.

Both are a reference index, not new content, and the same "do not add" rule governs them:

- **A formula is copied character for character.** If the notes write
  `ROA = Asset Utilisation x Profit Margin` with a lowercase `x`, it stays a lowercase `x`.
  Never substitute the textbook form of a relationship — DMBA 6008 states the sustainable
  growth rate one way in Week 0 (`SGR = ROE x Retention Rate`) and a different way in Week 2
  (`SGR is driven by Return on Assets, Leverage and Retention`). **Both are correct, because
  both are his.** Do not reconcile them, and never let one week's algebra leak into another's.
- If the same relationship appears in two genuinely different vocabularies on one page,
  **list both** — the difference is his.
- An **acronym** takes the page's own expansion where the page gives one. Where it does not,
  the standard expansion is allowed (an expansion is a dictionary fact, not an argument), but
  the panel's intro paragraph must say so, and a definition is never invented — an entry with
  nothing to say gives the expansion and stops.
- Skip markup: class names, `aria-*` values, SVG ids, course codes and site chrome are not
  acronyms.

Order acronyms alphabetically; order formulas as the page introduces them, so they follow
the week's teaching sequence.

**Emit a tab only if its array is non-empty.** An Agile or strategy week legitimately has no
formulas, and gets no Formulas tab. Do not pad one to fill the template.

The slots are `<!--INSERT:ACRONYMS_TAB-->` / `<!--INSERT:ACRONYMS_PANEL-->` /
`<!--INSERT:ACRONYMS_DATA-->` and the same three for `FORMULAS`. The shared `buildRef()`
renderer already sits in the shell and no-ops when a tab is absent.

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
- **Empty pages are real content signals.** Render them honestly as "not yet written".
  **Never fill a gap with invented material.** The live example is DMBA 6005 Week 1's
  `Creating your reflective journal`, still `<empty-block/>`. The original example — DMBA
  6008 Week 0's "Assessing Financial Performance", ten blank children matching an unticked
  todo item — **was written on 2026-08-12/13 and is now published**, which is the point:
  emptiness is a fact about the day you looked. Re-check every placeholder on every run.
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

**When skipping an image costs content, say so.** DMBA 6008 Week 2's `DuPont model example`
is the live case: despite its title, every number and the whole algebraic decomposition lived
in two Notion images, so the harvestable text contains no worked example at all. The published
topic is therefore qualitative only. That is the correct outcome under the images policy, but
it is a real loss and Aryan cannot see it from the page — report it, and offer to commit the
images if he wants the example.

Also excluded by default, as personal study telemetry rather than coursework:

- the Notebooks `Confidence` field (`Not Confident` etc.)
- `Last Reviewed`, `Days Since`, `Favorite`
- the unticked todo lists on notebook pages

Publishing any of these is a per-subject decision for the author, not a default.

### The one carve-out — DMBA 6008 discussion questions

Aryan directed on 2026-08-10 that DMBA 6008's live-session **`Discussion Questions`**
sub-page be published from **Week 2 onwards**, as a fourth tab on the week page.

Take that child page and **nothing else** from a `Live Session` note. The rest of those notes
stays unpublished and rule 1 still governs it. First run, 2026-08-12: the Week 2 `Live` note
(`3b97b336873c80f88fa0d476b75e6439`) contained *only* the Discussion Questions child, so
nothing had to be cut — do not assume that holds next time.

The tab is also the only place on the site where the **"do not add" rule is suspended**: the
supplied answers are marked *"Supplied AI-generated responses"* in Notion, and Aryan asked for
them to be improved with outside knowledge, industry examples and diagrams. Two guardrails
apply, and they are what keep it honest:

1. **No financial statistic about a real company, ever.** Companies illustrate a mechanism.
   Any ROA, margin, turnover, revenue, rate or date-stamped figure is a blocking defect.
   Illustrative arithmetic needs invented inputs and an explicit label.
2. **A provenance note heads the panel**, stating the answers were AI-generated and have been
   rewritten — so the tab is never mistaken for Aryan's own coursework.

### Per-subject exclusions — `syncRules`

Beyond the `Type` filter, a subject can carry named exclusions in `subjects.json` under
`syncRules`. They are author decisions, not inferences, and they are **permanent until the
author revokes them** — a run must not treat an excluded note as a gap to be filled later.

**A `syncRule` binds both discovery flows.** Notes reach the pipeline two ways: the
per-notebook `Notes` relation walk, and the Course-level `Notes` relation walk that catches
notes carrying no `Notebook` relation. A rule enforced in only one flow is not enforced —
the note simply arrives through the other. Apply exclusions in Phase 0, before shape
detection and before any harvest agent is spawned, and report each as
`SKIPPED  <rule id>`.

| Subject | Rule | Effect |
| --- | --- | --- |
| DMBA 6005 | `no-shadow-boxing-after-week-0` | No note or sub-page whose title starts with `Shadow Boxing` is published for **Week 1 or any later week**. Week 0's `Shadow Boxing` method note (`3ae7b336873c803ab350c8e418970044`) is already published and stays. Set by Aryan, 2026-08-10. |

An excluded note gets **no** "not yet written" placeholder, **no** topic chip on the hub
page, and contributes **no** terms or flashcards. It is out of scope, not pending.

Academic integrity, unchanged from [content-guide.md](content-guide.md): summarising and
restructuring the student's own notes is fine and is the whole point of this pipeline.
Generating new academic argument, inventing a citation, or "improving" a claim is not.

---

## 7. Current state

**DMBA 6008 Finance, Strategy and Technology** — synced 2026-08-15 (re-checked; every topic
`observedAt` identical to the state record, no notebook or note added, nothing rebuilt).

| Week | Notion notebook | Published |
| --- | --- | --- |
| Week 0 | `3a17b336873c805b9c4acdff38033d35` | `DMBA6008-week0.html` — balance sheet, P&amp;L, cash flow, and **assessing financial performance, written 2026-08-12/13 and published 2026-08-14**. All four topics are now live; the "not yet written" panel is gone. |
| Week 1 | `3b27b336873c8070953fd96878f5f2dc` | `DMBA6008-week1.html` — key value principles, concepts, assessing performance, key definitions |
| Week 2 | `3b77b336873c802182a3cf5b76484dd1` | `DMBA6008-week2.html` — the asset mix as a business-model signal, drivers of return, the DuPont decomposition, sustainable growth, plus the live-session discussion questions |

> **The Week 2 `Live` note grew a second child on 2026-08-15 and it was not published.**
> `3b97b336873c80f88fa0d476b75e6439` now holds `Discussion Questions` **and `Diary`**
> (`3ba7b336873c80f4addce7004f01a76e`). The carve-out in §6 covers the discussion page and
> nothing else, so `Diary` was not fetched, harvested or read. This is the first time the
> carve-out has had to actually *exclude* something — when it was written the Live note had
> only the one child, so nothing had to be cut. Expect every future Live note to be mixed.

> **Week 0's fourth topic is the case that justifies the deep pass.** When Aryan wrote it,
> the note row's `Edited Time` **did not move** — it still reads 2026-07-24. Only the
> grandchild's `observedAt` did. A run trusting `Edited Time` alone would have reported the
> week unchanged and silently missed 5,090 words. The topic was also **restructured**: ten
> blank sub-pages (including `Sustainable Growth Part 1`, `Part 2` and `Summary`) became
> eight written ones. Tree shape is a change signal for exactly this reason.

> **The same concept is now stated two ways across the subject, and both are correct.**
> Week 0 gives `SGR = ROE x Retention Rate`; Week 2 gives `SGR is driven by Return on
> Assets, Leverage and Retention` and never writes the product form. **Do not reconcile
> them** — each page reproduces the algebra of the notes it was built from, and a future
> sync must not let one week's form leak into the other.

**DMBA 6005 Agile Project Development** — synced 2026-08-15. Weeks 0–2 re-probed and
byte-identical, so only **Week 3** was built. Launched with two weeks at once, and the
`index.html` card un-muted in the same run.

| Week | Notion notebook | Published |
| --- | --- | --- |
| Week 0 | `3ae7b336873c806da6b6e5630c66e3bb` | `DMBA6005-week0.html` — the `$RUs` digital innovation case, plus the `Shadow Boxing` method note |
| Week 1 | `3b17b336873c80ada0b3f4a02cb2dea8` | `DMBA6005-week1.html` — project management before execution, the StellarCX engagement, context analysis (partial) |
| Week 2 | `3b37b336873c80db9388ee1a56192b33` | `DMBA6005-week2.html` — CX, Agile history and Scrum roles, bidding and winning projects. **This notebook was the empty `New Notebook` placeholder until 2026-08-08, when it was renamed `Week 2: Agile` and filled.** |
| Week 3 | `3bc7b336873c8073a251daf6ee7701de` | `DMBA6005-week3.html` — design thinking and ideation, and why we prototype. **Two of its four in-scope sub-pages are empty** and render as honest "not yet written" blocks: `Personas` and `Long-term strategic value for $RUs`. |

> **Week 3 has a topic chip that would contradict the page if left bare.** The empty
> `Personas` sub-page sits alongside a *written* personas section inside the ideation
> topic, so clicking the dimmed `Personas` chip would show only "not yet written" on a week
> that plainly does cover personas. Its block therefore carries a pointer to block 06. When
> an empty topic's subject is covered elsewhere on the same page, say so — it costs one
> sentence and it is the difference between honest and broken-looking.

> **Its `Ideation and design thinking` topic contains a framework that is all headings and
> no body.** `A - Architecture & Technology`, `B - Business & Experience`, `C - Change &
> Capability`, `D - Data & AI`, `E - Execution` have nothing written under any of them. The
> page lists them as bare labels and states in words that the notes record nothing under
> them. **Never invent a gloss for any of the five** — they are the most invitingly
> fillable blanks in either subject.

Three things about 6005 that differ from 6008, and will bite a later run:

- **It uses both content shapes.** Week 0's notes are inline (Shape B); Week 1's `Learn`
  note is a container (Shape A) with five sub-pages. `contentShapeHint` in `subjects.json`
  says `inline` and is wrong for Week 1 — which is exactly why the shape is detected per
  note at runtime.
- **One pre-live note belongs to no week.** `Shadow Boxing`
  (`3ae7b336873c803ab350c8e418970044`) has a `Course` relation but no `Notebook` relation,
  so walking notebooks alone misses it. Aryan directed on 2026-08-06 that it publish under
  Week 0. Walk the Course's `Notes` relation too, and reconcile against the notebooks.
- **Week 1 is partly unwritten, and stays that way on the page.** `Context Analysis for
  $RUs` ends mid-word at *"Their financial requir"* and `Creating your reflective journal`
  is empty. The page reproduces the truncation exactly and carries an honest "not yet
  written" block. **Never complete the sentence.**
- **No Shadow Boxing content after Week 0.** `syncRules` → `no-shadow-boxing-after-week-0`
  (§6), set by Aryan on 2026-08-10. `Shadow Boxing Week 1`
  (`3b37b336873c80698a11eb104e178cb1`) and every later one are dropped in Phase 0, in both
  discovery flows. They were removed from the Week 1 page and the hub on the same day, so a
  later run finding them again must skip them rather than re-add them.

The case-study characters in `Your project with StellarCX` — Chris Gold, Dirk, Ivy, Andrew,
Jeremy, Annie, and the client Murray — were confirmed by Aryan on 2026-08-06 to be
**fictional simulation characters**, not lecturers or classmates, and are cleared for
publication. Re-check if the cast changes.

See [notion-sync-automation.md](notion-sync-automation.md#extending-to-dmba-6005) for the
design rationale.
