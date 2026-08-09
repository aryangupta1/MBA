---
name: sync-subject
description: Sync a semester-2 subject's Notion notebooks into this repo's week study pages. Use when Aryan says "update finance", "sync 6008", "update agile", "sync my notes", or names a subject alongside Notion. Harvests Pre-Live Session notes only, builds the summary / key concepts / flashcards page, registers it, and runs six QA gates before reporting.
---

# sync-subject

Turns Notion coursework notes into week study pages in this repo.

**Read first, every run:** [docs/notion-sync.md](../../../docs/notion-sync.md) — the Notion
schema, the two content shapes, the gotchas, and the publish rules. This file is the
procedure; that file is the ground truth about the data.

---

## The three rules that outrank everything else

1. **Only `Pre-Live Session` notes are published.** `Live Session` notes are classroom
   diaries containing candid remarks about lecturers, about other students' use of AI, and
   about what will be examined. `Assessment` notes are unsubmitted academic work. GitHub
   Pages makes every committed file public. If you are ever unsure of a note's `Type`, do
   not publish it.
2. **An empty topic renders as empty.** Never fill a gap with generated material.
   `DMBA6008-week0.html`'s fourth panel is the precedent — an honest "not yet written"
   block listing what is pending.
3. **Do not commit or push.** `CLAUDE.md` forbids it unless Aryan asks.

Also excluded by default, as personal study telemetry: `Confidence`, `Last Reviewed`,
`Days Since`, `Favorite`, and the unticked todo lists on notebook pages.
(Confirmed by Aryan 2026-08-05: confidence stays off the public site.)

---

## Files this skill owns

| Path | What it is |
| --- | --- |
| `subjects.json` | code ↔ aliases ↔ Notion id ↔ palette ↔ fonts, plus the global Notion ids and the stale-note id |
| `reference/week-shell.html` | the week page with `{{PLACEHOLDER}}` and `<!--INSERT:-->` slots. Built on the **DESK** design system — read [`docs/design-system.md`](../../../docs/design-system.md) before touching its `<style>` block or page chrome |
| `reference/fragment-spec.md` | hand this to every fragment-building agent, verbatim |
| `reference/checks.py` | QA gates 2, 3, 5 and 6 — structure, SVG overflow, inline-layout, prose length |
| `../../../docs/notion-sync-state.json` | the manifest: what was published and when |

`reference/checks.py` is a verification tool. It never writes to a page and nothing in the
deploy path calls it, so it is not a build step.

---

## Setup check

Notion MCP tools are **deferred** — load schemas before use:

```
ToolSearch("select:mcp__notion__notion-fetch,mcp__notion__notion-query-data-sources")
```

If `claude mcp list` shows Notion as `Needs authentication`, stop and ask Aryan to run
`/mcp`. Nothing downstream works without it.

`notion-query-data-sources` is **metered** on this plan. `notion-fetch` on a relation URL is
not. One query to list a course's notebooks is fine; a query per note is waste — fetch.

---

## Phase 0 — Resolve and diff *(inline, no agents)*

1. Resolve Aryan's word to a subject via `subjects.json` `aliases`. "finance" → `DMBA6008`.
   If it matches nothing, ask — do not guess.
2. Fetch the course page, then each notebook in its `Notebooks` relation.
   - **Skip any `<page>` carrying a `deleted` attribute** — archived notebooks stay in the
     relation.
   - **Skip empty placeholder notebooks** (`New Notebook` and anything like it).
3. Fetch each note in each notebook's `Notes` relation, for `Type` and `Edited Time`.
   - **Skip the stale note id in `subjects.json` `_globals.staleNoteId`.** It 404s from
     every notebook and is not a failure.
4. **Detect the content shape per note, at runtime.** If the note's `<content>` is nothing
   but `<page url=…>` links, it is a container (Shape A) — recurse to the leaves. Otherwise
   the body is the content (Shape B). Never trust `contentShapeHint`; a subject can change
   shape between weeks.
5. Record the change signals. **A child page has no `Edited Time`** — only a Notes database
   row does; fetching a child returns `{"title": …}` and nothing else. The signals that do
   exist, in descending order of trust:

   | Signal | Where | Trust |
   | --- | --- | --- |
   | `contentHash` of the harvested Markdown | computed by this skill | **exact** |
   | note `Edited Time` | Notes row property | exact, but only for the note row |
   | tree shape — child ids and titles | the fetch | exact for added/removed/renamed pages |
   | `observedAt` — the `as of <ISO>` stamp in the fetch envelope | every page | strong hint |

   `observedAt` was verified on 2026-08-05 to be a *content* timestamp, not a fetch
   timestamp: the same page fetched twice minutes apart returned an identical value, and
   siblings returned different ones. It is undocumented, so treat it as a hint.

   **The rule:** a week is CHANGED if the note's `Edited Time`, any `observedAt`, or the
   tree shape moved. That can over-trigger, which costs one harvest — cheap. The
   `contentHash` then decides whether to actually rebuild, so a false alarm never churns
   reviewed prose.

   **Deep pass.** The residual risk is under-triggering: a grandchild edited with no
   recorded timestamp moving. If Aryan says he edited a sub-page, or a week looks wrong,
   re-harvest every topic and compare hashes rather than trusting the cheap pass.

6. Compare against `docs/notion-sync-state.json` and print the table:

```
NEW        Week 2 "Cost of capital" — 1 pre-live note, 4 sub-pages, ~3,100 words
CHANGED    Week 0 → "Assessing Financial Performance" — was empty, now 6 of 10 written
UNCHANGED  Week 1
SKIPPED    Live-session note in Week 2 — not publishable (docs/notion-sync.md §6)
SKIPPED    3 images in Week 2 — see "Images" below
```

**Stop condition: if nothing changed, say so and stop.** Do not rebuild pages to prove the
tool ran.

---

## Phase 1 — Scope *(one question, then commit)*

Ask **once**, with `AskUserQuestion`, only if something changed:

> **What should I rebuild for DMBA 6008?**
> - **Everything that changed** *(recommended)*
> - **New weeks only** — leave already-published weeks alone
> - **Flashcards and key concepts only** — refresh recall material, leave summaries and visuals
> - **Summaries and visuals only** — leave the decks alone

The split matters because review cost differs: a regenerated glossary is cheap to eyeball,
a regenerated summary with five hand-drawn SVGs is not.

Do not re-ask per week.

---

## Phase 2 — Harvest *(fan out: one agent per topic)*

**The fan-out unit is the topic within a week, not the week.** A four-topic week gets four
agents. A one-topic week gets one. Never manufacture topic divisions to fill a template.

Each agent:
- recursively fetches its own subtree,
- writes `scratchpad/notion/wk<N>-<topic>.md` **verbatim** — preserving typos, Australian
  spelling, awkward phrasing, truncated sentences and empty headings,
- returns **a manifest only** (titles, word counts, anomalies). Never the content. The
  orchestrator's context stays clean and the prose never round-trips through it.

Conversions the harvester performs:

| Notion output | Becomes |
| --- | --- |
| `<table>` + `<colgroup>` | GitHub-flavoured Markdown table |
| `<callout icon="X">text</callout>` | `> [!X] text` |
| `<empty-block/>`, `<table_of_contents/>` | dropped |
| `\$`, `\>`, `\<` | `$`, `>`, `<` |
| `` $`Profit = Revenue - Expenses`$ `` | plain text — a Notion equation-block artefact |
| image | recorded in the manifest as `IMAGE: <caption>`, **not** downloaded, **not** linked |

**Images are skipped** (decided by Aryan 2026-08-05). Notion serves 5-minute presigned S3
URLs, so a committed page cannot reference one; publishing an image means downloading and
committing the file. Report the count per week so Aryan can ask for a specific one.

**Gate:** a topic the harvester reports as empty stays empty on the page.

---

## Phase 3 — Build fragments *(fan out: one agent per topic)*

Each agent gets, and only gets:

1. `reference/fragment-spec.md` verbatim,
2. `DMBA6008-week1.html` as the worked reference,
3. **its own** harvested Markdown file,
4. **a unique SVG id prefix** (`bs`, `pl`, `cf`, …) — without this, `aria-labelledby`
   targets collide when fragments are concatenated,
5. the subject's palette hex values from `subjects.json`.

Honour the Phase 1 scope: a "flashcards only" run asks for `CARDS` and nothing else.

Each returns `SUMMARY` (HTML fragment), `TERMS` and `CARDS` (JS object literals, one per
line). Format and rules are all in the fragment spec.

**Tell every builder its prose budget explicitly, in words, in the prompt** — do not rely on
it reading §5. State: *"≤ 160 words of `<p>` prose per `.block`; tables, figures and worked
examples do not count."* The first build had the budget available and blew it 3×; naming
the number in the prompt is cheap insurance. Then verify with `checks.py --lengths` before
assembling, not after.

---

## Phase 4 — Assemble and register

**Splice with a script, not by hand.** Summary blobs run 5–7k words each and there is no
reason to route them through context.

1. Copy `reference/week-shell.html` to `<prefix>-week<N>.html`.
2. Fill every `{{PLACEHOLDER}}`; replace `<!--INSERT:SUMMARY-->` with the concatenated
   summary fragments; replace `/*TERMS*/[]/*END_TERMS*/` and `/*CARDS*/[]/*END_CARDS*/`
   with the merged arrays. `{{TERM_COUNT}}` and `{{CARD_COUNT}}` must match the arrays.
   The four **`{{ACCENT}}` / `{{ACCENT_DEEP}}` / `{{ACCENT_SOFT}}` / `{{ACCENT_GLOW}}`**
   placeholders come straight from `subjects.json` → `palette` → `accent` / `deep` / `soft`
   / `glow`. They are the *only* per-subject visual knobs: every semester-2 page shares one
   stylesheet and one type pair. `{{FONT_HREF}}` is the house font link and is identical for
   every subject — do not swap in a per-subject pairing. `{{HUB_PAGE}}` is the back link and
   comes from `subjects.json` → `hubPage`; a week page's parent is its **week hub**, never
   `library.html`.
3. Update the hub page `<prefix>-weeks.html` — add the week card and fix **its
   hand-written per-week counts**, which are the easiest thing to leave stale.
4. Register in `library.html`. **`articlesBySubject` and `validSubjects` must be edited
   together** — a subject in one but not the other silently falls back to DMBA 6002.
5. On a subject's **first** page only: drop `card--muted` from its `index.html` card, rewrite
   the `card-desc`, and set `live: true` in `subjects.json`. For a subject whose
   `subjects.json` `live` is `false`, **ask first** — un-muting is a visible claim that the
   subject has material.
   **Exception: DMBA 6005 is pre-approved** (Aryan, 2026-08-05). Un-mute it in the same run
   that publishes its first pages, without asking. See the subject note below.

---

## Phase 5 — QA *(six gates)*

The failure mode of a generative pipeline is confident, plausible, wrong content — and, as
week 0 proved, confident, plausible, *far too much* content. These gates are the point of
the whole design.

Gates 2, 3, 5 and 6 are one command:

```sh
python3 .claude/skills/sync-subject/reference/checks.py <page>.html [...]
```

| # | Gate | What it checks | Who |
| --- | --- | --- | --- |
| 1 | **Fidelity** | Every claim, number, formula, company name and worked example on the page traces to the harvest Markdown | agent |
| 2 | **Structure** | Tag balance, duplicate ids, `aria-*` targets resolving, relative paths resolving, no `only-accessible-by-url` link | `checks.py` |
| 3 | **SVG** | Every `<text>` fits its parent `<rect>` and sits inside the viewBox | `checks.py` |
| 4 | **Privacy** | Nothing sourced from a `Live Session` or `Assessment` note; no lecturer or classmate names; no `Confidence` / `Last Reviewed` telemetry | agent |
| 5 | **Layout** | A `<span>` given `width`/`height`/`min-height` must be blockified or have a flex/grid ancestor, or the box is silently dropped | `checks.py` |
| 6 | **Length** | Flowing prose ≤ 160 words per `.block` — the fragment spec's budget, measured | `checks.py` |

**Any hit blocks publication.** A gate-4 hit escalates to Aryan immediately.

Gate 6 exists because the first week-0 build shipped **~4,000 words per topic against a
stated 900–1400 budget** and nobody noticed until Aryan read it. The budget had been in
`fragment-spec.md` from the start; what was missing was measurement. `--lengths` prints the
table without failing, which is the fast way to check a draft mid-build:

```sh
python3 .claude/skills/sync-subject/reference/checks.py --lengths <page>.html
```

`DMBA6008-week0.html` was condensed to budget on 2026-08-05 in three passes: tighten wording,
then delete restatement paragraphs, then strip industry illustrations. All topics now pass.
The page went from ~11,850 summary words to ~8,270 with every table, figure, formula and
worked example intact — the reduction is entirely prose.

**Gate 1 is adversarial and context-starved by design.** Give the agent the built page and
the harvest Markdown and **nothing else** — no web access, no prior knowledge of the
subject, no other topic's harvest. It is checking transcription, not plausibility. Tell it
to default to flagging when unsure. On the first run this caught four real defects,
including a figure asserting that non-current assets are "depreciated over their useful
lives" when the notes say land is not depreciated and goodwill is not amortised.

Gate 5 exists because of a real escape: `.flip-inner` was a `<span>` with `width` and
`min-height` and no `display`, so both were silently dropped and the flashcard collapsed.
Every static check passed. Aryan found it by looking at the page.

### The sixth gate is a pair of human eyes

**A browser look is required, not optional.** Never report a page as done on static checks
alone.

```sh
open <prefix>-week<N>.html
open <prefix>-weeks.html
open "file:///Users/aryan/Documents/MBA/library.html?subject=<CODE>"
```

A query-string page needs a real `file://` URL — `open library.html?subject=…` fails,
because the shell treats it as a filename.

Check at narrow width. Flip a flashcard. Walk the reader's path:
`index.html` → `library.html?subject=…` → hub → week page → back link. Then ask Aryan to
confirm.

---

## Phase 6 — Report and hand back

1. Report what was built, what each gate flagged, and **what was deliberately left out** —
   empty topics, live-session notes, skipped images. The omissions are the part Aryan
   cannot see for himself.
2. Update `docs/notion-sync-state.json` — leaf `Edited Time` for container notes.
3. Update `docs/notion-sync.md` §7 (current state) and `CLAUDE.md`'s subject table if a
   subject changed status.
4. Update `next-prompt.md` per [docs/next-prompt-protocol.md](../../../docs/next-prompt-protocol.md).
5. **Do not commit.**

---

## Cost

The first DMBA 6008 run used about ten agents. A steady-state run adding one new week
should need **two harvesters and two builders**. Keep the fan-out to topics.

---

## Subject-specific notes

### DMBA 6005 — live since 2026-08-06

Launched with Week 0 and Week 1 together; `subjects.json` `live` is `true` and the
`index.html` card is un-muted. **The launch gate is spent — do not re-apply it.** From here
6005 is an ordinary steady-state subject: diff, harvest what changed, rebuild.

Three things a later run will trip over:

- **It uses both content shapes in one subject.** Week 0's notes are inline (Shape B);
  Week 1's `Learn` note is a container (Shape A) with five sub-pages. `contentShapeHint`
  still says `inline` and is wrong for Week 1 — detect per note, as Phase 0 §4 requires.
- **One pre-live note belongs to no notebook.** `Shadow Boxing`
  (`3ae7b336873c803ab350c8e418970044`) has a `Course` relation but **no `Notebook`
  relation**, so walking notebooks alone silently misses it. It is published under Week 0 by
  Aryan's direction (2026-08-06). **Walk the Course's `Notes` relation as well as the
  notebooks**, and reconcile the two — a general lesson, not a 6005 quirk.
- **Week 1 is deliberately incomplete on the page.** `Context Analysis for $RUs` ends
  mid-word at *"Their financial requir"* and is reproduced exactly that far; `Creating your
  reflective journal` and `Shadow Boxing Week 1` are empty and render as an honest "not yet
  written" block. **Those are the things to replace** when Aryan writes them.

Settled, do not re-ask:

- **Type pairing: the house pair, Mona Sans + Plus Jakarta Sans**, with the `--course-e`
  ochre palette (`#A8722C`) as this subject's accent. The per-subject Sora + Karla pairing
  was retired on 2026-08-09 when the DESK design system landed — see
  [`docs/design-system.md`](../../../docs/design-system.md). `fontHref` in `subjects.json`
  now holds the house link for every subject.
- The case characters in `Your project with StellarCX` — Chris Gold, Dirk, Ivy, Andrew,
  Jeremy, Annie, and the client Murray — are **fictional simulation characters**, confirmed
  by Aryan 2026-08-06, and clear gate 4. Re-check only if the cast changes.
- `New Notebook` (`3b37b336873c80db9388ee1a56192b33`) is an empty placeholder. Skip it;
  never render it as a week.
- `Class Diary` (`3b17b336873c800e9208ca98bc0a8ada`) is a `Live Session` note. Never
  publish it.

Its Week 0 is a strategic case, not a formula topic: reach for option-comparison matrices,
a customer-journey strip and a decision-rule table, not equations. Cards shift from
"compute this" to "given this symptom, which option and why". Agile weeks proper will want
cycle diagrams and board/timeline strips — do not reuse Week 0's option-matrix vocabulary
just because it is there. Full detail in
[docs/notion-sync-automation.md §7](../../../docs/notion-sync-automation.md#7-extending-to-dmba-6005).

### Semester 1 subjects are not synced

`DMBA6001`, `DMBA6002` and `DMBA6004` are `Completed`, and their pages are hand-written
from before this pipeline. Do not regenerate them. Their Notion ids are in `subjects.json`
under `_completedSem1` for lookup only.

Notion's course names are fuller than this repo's (Notion calls DMBA 6004 "Digital
Collaboration, Work and Organisation"). **Do not reconcile the titles without asking.**

---

## Direction of flow

Notion is authoritative; the repo is publish-only. **There is no reverse sync.** A page
edited here does not flow back, and this skill must never write to Notion.
