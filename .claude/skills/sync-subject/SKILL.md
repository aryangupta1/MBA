---
name: sync-subject
description: Sync a semester-2 subject from Aryan's Obsidian vault (~/MBA) into this repo's week study pages. Use when Aryan says "update finance", "sync 6008", "update agile", "sync my notes", or names a subject alongside his notes. Publishes only notes flagged publish:true, builds the summary / key concepts / flashcards page, registers it, and runs six QA gates before reporting.
---

# sync-subject

Turns Aryan's Obsidian coursework notes into week study pages in this repo.

**The source is the vault at `~/MBA`, not Notion.** He migrated every note out of Notion on
2026-08-18 and now keeps Notion only for assignment tracking. Nothing in this skill reads
the Notion Notes database any more — if you find yourself reaching for `notion-fetch` to get
coursework prose, stop: you are reading a dead source.

**Read first, every run:** [docs/vault-sync.md](../../../docs/vault-sync.md) — the vault
layout, the publish flag, and the rules about what may never ship. This file is the
procedure; that file is the ground truth about the data.
[docs/notion-sync.md](../../../docs/notion-sync.md) describes the retired Notion pipeline and
is kept for history only.

---

## The three rules that outrank everything else

1. **Only `Pre-Live Session` notes are published.** `Live Session` notes are classroom
   diaries containing candid remarks about lecturers, about other students' use of AI, and
   about what will be examined. `Assessment` notes are unsubmitted academic work. GitHub
   Pages makes every committed file public. If you are ever unsure of a note's `Type`, do
   not publish it.
2. **An empty topic renders as empty.** Never fill a gap with generated material — an honest
   "not yet written" block listing what is pending. `DMBA6005-week1.html`'s
   `Creating your reflective journal` is the live example. `DMBA6008-week0.html`'s fourth
   panel was the original one and **was filled on 2026-08-14**, which is the lesson worth
   keeping: a placeholder is a claim about the day you looked, so **re-check every one on
   every run** rather than trusting this file.
3. **Do not commit or push.** `CLAUDE.md` forbids it unless Aryan asks.

Also excluded by default, as personal study telemetry: `Confidence`, `Last Reviewed`,
`Days Since`, `Favorite`, and the unticked todo lists on notebook pages.
(Confirmed by Aryan 2026-08-05: confidence stays off the public site.)

**And never publish a real person's contact details.** The Courses row carries `Professor`,
`Email`, `Location` and `Time`. **None of them may appear on a page.** A hub's meta-row is
the status pill and the week count and nothing else. Set by Aryan on **2026-08-18**, after
`DMBA6008-weeks.html` was found to have been publishing the lecturer's name as a hero pill
since the first sync — it survived every run because nothing was looking for it. The full
list lives in `subjects.json` → `_globals.neverPublishFields`.

### `Pre-Class Prep` is excluded outright — it is not a second carve-out

Any page titled `Pre-Class Prep`, in any note, in any week, is **dropped in Phase 0 and
never fetched**. Not to check it, not to summarise it, not to decide whether it looks
publishable. `subjects.json` → `DMBA6008.syncRules` → `no-pre-class-prep`, set by Aryan on
**2026-08-18**.

It first appeared as the only child of DMBA 6008 Week 3's `Live` note. The name invites the
argument that "pre-class" means pre-live; **that argument is closed.** Treat it exactly the
way DMBA 6005 treats `Shadow Boxing` after Week 0 — a hard exclusion reported as
`SKIPPED  no-pre-class-prep`, with no placeholder, no topic chip, and no contribution to
terms, flashcards, quiz questions or scenarios.

### The only carve-out from rule 1 — DMBA 6008 discussion questions

Aryan directed on **2026-08-10** that DMBA 6008's live-session **`Discussion Questions`
sub-page** be published, from **Week 2 onwards**, as a fourth tab.

This is a **narrow carve-out, not a repeal, and it has not been widened.** It covers a
child page named `Discussion Questions` and no other. Its two known siblings — `Diary` and
`Pre-Class Prep` — are both outside it, and `Pre-Class Prep` is separately excluded by
`no-pre-class-prep` above. Take the `Discussion Questions` child page and
**nothing else** from a `Live Session` note. Everything else in those notes — remarks about
the lecturer, about classmates' use of AI, about what will be examined, notes-to-self — stays
unpublished, and rule 1 still governs it. If a future Live note mixes diary material *into*
the discussion page, cut it and say so in the report.

The discussion tab is also the **only** place on the site where the "do not add" rule is
suspended. Aryan asked for the supplied answers to be improved with outside knowledge, real
industry examples and diagrams. That licence covers **this tab only** — the summary, key
concepts and flashcards remain a transcription of his own notes.

Two guardrails make that safe, and they are not optional:

- **Never state a financial statistic about a real company.** Use companies for durable,
  structural, common-knowledge mechanics. Any ROA, margin, turnover, revenue, rate, share
  price or date-stamped figure is a publication-blocking defect. Illustrative arithmetic is
  allowed only with invented inputs and an explicit "illustrative" label.
- **Carry a provenance note at the top of the panel** saying the source answers were
  AI-generated and that these have been rewritten, so a reader is never misled into thinking
  the tab is Aryan's own coursework.

Build it with `{{DISCUSSION_TAB}}`-style slots: `week-shell.html` carries
`<!--INSERT:DISCUSSION_TAB-->` and `<!--INSERT:DISCUSSION_PANEL-->`. A week with no
discussion questions leaves both empty and shows three tabs, not four.

---

## Files this skill owns

| Path | What it is |
| --- | --- |
| `subjects.json` | code ↔ aliases ↔ palette ↔ fonts ↔ `syncRules` ↔ `needsReview`. The Notion ids in it are now only provenance |
| `reference/week-shell.html` | the week page with `{{PLACEHOLDER}}` and `<!--INSERT:-->` slots. Built on the **DESK** design system — read [`docs/design-system.md`](../../../docs/design-system.md) before touching its `<style>` block or page chrome |
| `reference/fragment-spec.md` | hand this to every fragment-building agent, verbatim |
| `reference/checks.py` | QA gates 2, 3, 5 and 6 — structure, SVG overflow, inline-layout, prose length |
| `reference/practice/` | the study path, Quiz and Apply-it components — `build.py`, the shared `tpl/`, the authored `data/<PAGE>.json`, and a `README.md` that is binding on every re-sync |
| `../../../docs/vault-sync-state.json` | the manifest: what was published, and each topic's content hash |
| `reference/vault_discover.py` | Phase 0 — discovery and diff against the vault |
| `reference/publish_images.py` | Phase 2 — copies a week's images into `assets/notes/` |

`reference/checks.py` is a verification tool. It never writes to a page and nothing in the
deploy path calls it, so it is not a build step.

---

## Setup check

No MCP, no network, no authentication. The source is local markdown.

Confirm the vault is present and readable before starting:

```
ls ~/MBA/"Semester 2 2026"
```

If it is missing, stop and ask Aryan — do NOT fall back to Notion. Notion is a note-taking
surface, not a publishing source: it has no record of what has been reconciled against his
Obsidian edits, so publishing from it directly could ship over work he did in the vault.
Pull it down with `sync-notes` first, then publish from the vault.

Override the vault location with `MBA_VAULT` if it ever moves.

---

## Phase 0 — Resolve and diff *(inline, no agents)*

1. Resolve Aryan's word to a subject via `subjects.json` `aliases`. "finance" → `DMBA6008`.
   If it matches nothing, ask — do not guess.
2. Run the discovery script. It does the whole of discovery and diffing:

```
python3 "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/skills/sync-subject/reference/vault_discover.py" DMBA6008
```

   Use the absolute form — the working directory is routinely changed to the vault during a
   sync, and a relative path breaks the moment it is.
   Add `--json` when you need the machine-readable form (Phase 2 and the image step use it).

3. **Read its output as the plan.** It prints one line per week and per topic:

```
UNCHANGED  Week 2 Drivers of Returns  — 4 topic(s), 2,546 words, 4 image(s)
NEW        Week 4 Project Evaluation  — 4 topic(s), 363 words, 2 image(s)
             NEW       Recap of NPV  (363w, 2img)
             NEW       Strategy and Finance  (0w, 0img)
SKIPPED    Week 2 — Live — publish=false (Live Session)
SKIPPED    Week 3 — Learn / Shadow Boxing — syncRules: no-shadow-boxing-after-week-0
NEEDS REVIEW  Week 3 — "Live" — HELD BACK, not published
```

### What the script decides, so you do not have to

- **A "topic" is the fan-out unit** Phases 2 and 3 expect: the first level beneath a week's
  note. A note with a same-named folder beside it is a container and its children are the
  topics; a note without one is itself a single topic. A topic's content is its own file
  **plus every descendant beneath it**, so grandchildren are never dropped.
- **The publish filter is `publish: true` in frontmatter.** That flag was set at migration
  from the Notion `Type`, so `Live Session` diaries and `Assessment` drafts are already
  `false`. It is a property of the note, not a judgement you make per run.
- **`syncRules` still bind**, and they read from `subjects.json` exactly as before.
  `allowedNotionIds` is a precise carve-out for a note that is approved despite matching a
  rule — DMBA 6005's Week 0 `Shadow Boxing` lives in `_Unfiled` with no week number, and
  without the carve-out a week-based rule silently strips it from a published page.
- **`needsReview` entries are HELD BACK and never published.** They are notes whose
  frontmatter says publishable but whose body says otherwise. Report them to Aryan and wait
  for a ruling; do not argue one into the build.

### Change detection

A topic is **CHANGED** when the sha256 of its markdown (its own file plus all descendants)
differs from `docs/vault-sync-state.json`. This is exact — there is no equivalent of the
Notion era's `observedAt` guesswork, no metering, and no under-triggering on a deep edit.
A week with no recorded hash is **NEW**.

`docs/vault-sync-state.json` was **seeded on 2026-08-18** for weeks that already had a page.
The seed asserts those pages match the vault; it was not verified line by line. If a page
looks out of step with the vault, re-harvest that week rather than trusting the hash.

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

## Phase 2 — Assemble source *(inline, no agents)*

**There is nothing to harvest any more.** The notes are already local markdown, already
converted, already verbatim. Phase 2 is now a file assembly, and it needs no agents, no MCP
and no network.

For each topic Phase 0 marked NEW or CHANGED, concatenate its `files` (from
`vault_discover.py --json`, already in order: the topic's own note then its descendants)
into `scratchpad/vault/wk<N>-<topic>.md`, stripping each file's YAML frontmatter.

That path is the **same contract Phase 3 already consumes** — one markdown file per topic —
so every downstream phase is unchanged.

Do not rewrite the prose while assembling. It is already verbatim: the author's typos,
Australian spelling, truncated sentences and empty headings are all intentional and were
preserved through the migration. Some pages genuinely end mid-thought in the source.

**Gate:** a topic whose assembled file is empty stays empty on the page. Several are
legitimately empty — DMBA 6008 Week 4's `Strategy and Finance`,
`Golden rules of project evaluation` and `Application and solution` are blank in the source.
Render the honest "not yet written" block; never generate filler.

### Images — now published

Images used to be skipped because Notion served 5-minute presigned URLs that a committed
page could not reference. **That constraint is gone**: the vault holds the real files in
`~/MBA/_attachments/`, and Aryan approved publishing them on 2026-08-18.

```
python3 "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/skills/sync-subject/reference/publish_images.py" DMBA6008 3
```

It copies that week's images to `assets/notes/<code>/wk<N>/`, downscales anything wider than
1600px, and prints the `<img>` tag for each. Three things it will not do for you:

- **It does not write alt text.** It emits `alt="TODO"`. The page builder must replace that
  with a real description of what the figure shows. A filename is not alt text.
- **It refuses to publish on a filename collision** rather than letting one image overwrite
  another. Notion ids in this workspace share long prefixes, so output names use the *full*
  id — truncating it collided twice during development.
- **It will not inflate a file.** Small images are copied untouched; `sips` is only invoked
  when an image is genuinely oversized.

#### Look at every image before you publish it — most are formulas

**Running `publish_images.py` does not mean the images belong on the page.** When the backfill
ran on 2026-08-19, **16 of DMBA 6008's 17 publishable images were formulas** — LaTeX renders of
equations, black text on white — and exactly one was a genuine diagram.

**Read each image first.** Then:

| What it is | What to do |
| --- | --- |
| A formula or equation | **Transcribe it as text.** Put it in a `.formula` div in the prose and add an entry to the page's `FORMULAS` array. Do **not** publish the PNG. |
| A genuine diagram, chart or slide | Publish it, with real alt text describing what it shows. |

Formulas are transcribed rather than published because the Formulas tab has a **search
filter** an image cannot participate in, `.formula` is a **dark box with light text** that a
black-on-white PNG looks broken inside, and text stays sharp and reaches a screen reader.

**Transcribe exactly what the image shows.** Never derive, complete or improve a formula —
that is writing Aryan's academic content. Where a source image is missing or duplicated, say
so in words rather than reconstructing the equation. Week 3 repeats one `NPV()` image where
the prose implies a second, different one; the page states that in words and stops there.

**Delete what you do not use.** Unreferenced files under `assets/` are orphans — remove the
PNG and its `.<name>.src` stamp.

After transcribing, update the page's formula **count** (`id="formulas-count"`) and any
narrative that claims things are missing. Search the page for *"not reproduced"*, *"held as
images"* and *"were not published"* — those sentences become false the moment you fix the gap.

This closed the gap where prose depended on a figure the page never showed — DMBA 6008 Week 3
critiqued average accounting ROA while its definition sat in a skipped image. It now carries
the definition.

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

## Phase 3b — Derive the Acronyms and Formulas tabs

Two reference tabs sit after the deck: **Acronyms** and **Formulas**. They are **derived
from the assembled page, not from the harvest** — run this after Phase 4 has built the page,
one agent per page, reading the summary blocks, `TERMS` and `CARDS`. Deriving from the built
page means these tabs can only ever contain material that already passed gate 1.

Hand the agent `docs/vault-sync.md` §3b. The rules that actually bite:

- **A formula is copied character for character** — his lowercase `x`, his `÷`, his spacing.
  **Never substitute a textbook form.** 6008 states the sustainable growth rate one way in
  Week 0 and a different way in Week 2; both are his, do not reconcile them, and never let
  one week's algebra leak into another's.
- An acronym takes the page's own expansion where it gives one; otherwise the standard
  expansion is allowed, but **the panel intro must say so**. Never invent a definition.
- **Emit a tab only if its array is non-empty.** An Agile or strategy week has no formulas
  and gets no Formulas tab. Do not pad one to fill the template.

Slots: `<!--INSERT:ACRONYMS_TAB-->` / `_PANEL` / `_DATA`, and the same three for `FORMULAS`.
The shared `buildRef()` renderer is already in the shell and no-ops when a tab is absent, so
there is no JS to write. Everything renders as `.term` cards — **no new component**.

---

## Phase 3c — Derive the study path, the Quiz and the Apply-it tabs

Three practice components, all **derived from the assembled page** the same way 3b is —
so run this after Phase 4, one agent per page:

| Component | Where | What |
| --- | --- | --- |
| **Study path** | first block of the summary panel, `00 / Start here` | a numbered route through the modes this week has, each step jumping to its tab |
| **Quiz** | its own tab | four options, one right, a hint per question, a note on every option |
| **Apply it** | its own tab | scenarios with three staged hints, a walkthrough and a self-mark checklist |

**Read `reference/practice/README.md` before writing anything.** It carries the data
schema, the authoring rules and the build command. The agent writes **one JSON file** into
`reference/practice/data/<PAGE>.json` and edits no HTML;
`reference/practice/build.py <PAGE>.html` splices all three in and asserts the shape first.

**This is not optional on a re-sync.** A week that gains a topic, loses a placeholder or has
its prose reviewed has changed the material these are drawn from:

- **Re-derive that page's JSON** — new questions for the new material, and any question the
  change invalidated rewritten or dropped.
- **Re-check the study path** — a filled placeholder must stop being described as unwritten.
- **Sweep the counts** — the hero pill `N quiz questions`, the hub card, the hub mode list.

Same standard as everywhere else: **extraction, not addition**. No formula that sat in an
unpublished image, no repaired typo, no completed truncation, no reconciled inconsistency,
nothing from a Live Session note, and nothing from a topic the page marks unwritten.

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
   The summary **index, collapse and search** needs nothing from you — the shell's script
   builds it at load from whatever `.block` elements the summary ends up with. Do not
   hand-author a contents list; it would drift.
   **You must, however, set `data-topic` on every `.block`**, naming the vault topic the
   block was built from: `<div class="block" data-topic="Drivers of returns">`. That is what
   draws the topic chips, and only the sync knows the mapping. Leave it **off** a week-level
   block (a closing takeaway) so it shows under every topic. If a topic is empty in the vault,
   put `data-topic-empty="true"` on its "not yet written" block and it renders as a dimmed
   chip, the way DMBA 6005 Week 1 shows *Creating your reflective journal*. (DMBA 6008
   Week 0 showed *Assessing Financial Performance* that way until it was written and
   published on 2026-08-14 — filling one means dropping both the attribute and the
   `subtab--empty` class.)
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
| 4 | **Privacy** | Nothing sourced from a `Live Session` or `Assessment` note; **no `Professor`, `Email`, `Location` or `Time` from the Courses row**; no lecturer or classmate names anywhere, including a hub's meta-row; no `Confidence` / `Last Reviewed` telemetry; no `Pre-Class Prep` material | agent |
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
2. Update `docs/vault-sync-state.json` — write each rebuilt topic's `contentHash` from
   `vault_discover.py --json`. A week you did not rebuild keeps its recorded hash.
3. Update `docs/vault-sync.md` §7 (current state) and `CLAUDE.md`'s subject table if a
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
- **No Shadow Boxing content after Week 0.** `syncRules` →
  `no-shadow-boxing-after-week-0`, set by Aryan on 2026-08-10. Any note or sub-page whose
  title starts with `Shadow Boxing` outside Week 0 is dropped in Phase 0 — **in both
  discovery flows** — and reported as `SKIPPED`. Week 0's stays published. Do not render a
  "not yet written" placeholder for the excluded ones, do not give them a topic chip on the
  hub, and do not let them contribute terms or flashcards. `Shadow Boxing Week 1`
  (`3b37b336873c80698a11eb104e178cb1`) is empty and is now permanently out of scope, so it
  is no longer a gap waiting to be filled.
- **Week 1 is deliberately incomplete on the page.** `Context Analysis for $RUs` ends
  mid-word at *"Their financial requir"* and is reproduced exactly that far, and `Creating
  your reflective journal` is empty and renders as an honest "not yet written" block.
  **Those are the things to replace** when Aryan writes them. `Shadow Boxing Week 1` used to
  be listed alongside them; it is now excluded by `syncRules` and must not reappear.

Settled, do not re-ask:

- **Type pairing: the house pair, Mona Sans + Plus Jakarta Sans**, with the `--course-e`
  ochre palette (`#A8722C`) as this subject's accent. The per-subject Sora + Karla pairing
  was retired on 2026-08-09 when the DESK design system landed — see
  [`docs/design-system.md`](../../../docs/design-system.md). `fontHref` in `subjects.json`
  now holds the house link for every subject.
- The case characters in `Your project with StellarCX` — Chris Gold, Dirk, Ivy, Andrew,
  Jeremy, Annie, and the client Murray — are **fictional simulation characters**, confirmed
  by Aryan 2026-08-06, and clear gate 4. Re-check only if the cast changes.
- `3b37b336873c80db9388ee1a56192b33` was the empty `New Notebook` placeholder. On
  2026-08-08 Aryan **renamed it `Week 2: Agile` and filled it**, and it is now published.
  The old "skip it" rule was removed on 2026-08-10. **General lesson: a notebook being empty
  is a fact about the day you looked, not a permanent property.** Re-check every notebook
  listed as skipped on each run — including the ones this file tells you to skip.
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

The **Obsidian vault is authoritative**; the repo is publish-only. **There is no reverse
sync.** A page edited here does not flow back to the vault, and this skill must never write
to the vault or to Notion.

Aryan still takes notes in Notion as well as Obsidian, and will for some time. Notion feeds
the vault **upstream of this skill**, through `sync-notes`:

```
Notion --sync-notes--> vault --sync-subject--> week pages
                        ^^^^^  this skill starts here
```

That changes nothing here. **This skill still reads only the vault**, because the vault is
where the two note-taking surfaces are reconciled and where the conflict guard lives. If a
week looks stale, the fix is to run `sync-notes` first — never to read Notion from this
skill.
