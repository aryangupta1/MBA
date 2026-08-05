# Automating the Notion sync

Design for turning the manual pipeline in [notion-sync.md](notion-sync.md) into one
instruction: **"Update finance."**

**Built on 2026-08-05 as the `sync-subject` skill** — `.claude/skills/sync-subject/`. This
document is now the *design rationale*; `SKILL.md` is the procedure that actually runs, and
where the two disagree, `SKILL.md` wins. Read [notion-sync.md](notion-sync.md) first — this
assumes the schema, the two content shapes, and the publish rules from that document.

---

## 1. What "Update finance" should do

```
Aryan: Update finance

Claude: Checked DMBA 6008 against Notion.

        NEW      Week 2 "Cost of capital" — 1 pre-live note, 4 sub-pages, ~3,100 words
        CHANGED  Week 0 → "Assessing Financial Performance" — was empty, now has 6 of 10
                 sub-pages written (~2,400 words)
        UNCHANGED Week 1

        Live-session notes found in Week 2. Not publishing them (see docs/notion-sync.md §6).

        [asks what to build]
```

…then it harvests, builds, registers, verifies, and reports — without further babysitting.

The value is not saving keystrokes. It is that the **six places a new week has to be
reflected** (harvest, summary, glossary, flashcards, hub card, registry) stay in step, and
that the publish rules are applied every time rather than remembered every time.

---

## 2. Where the automation lives

A **Claude Code skill**, so it is invocable as `/sync-subject` and also matches the natural
phrasing "update finance".

```
.claude/skills/sync-subject/
├── SKILL.md                  the procedure — phases, gates, stop conditions
├── subjects.json             code ↔ Notion id ↔ file prefix ↔ page palette
└── reference/
    ├── fragment-spec.md      the class vocabulary agents may emit (see §6)
    └── week-shell.html       the page shell with {{TERMS}} {{CARDS}} {{SUMMARY}} slots
```

Why a skill and not a hook or a script:

- **No build step is allowed** (`CLAUDE.md` hard constraints). A skill is instructions, not
  code in the deploy path — nothing new runs when the site is served.
- Hooks fire on events; this is user-initiated.
- The work is genuinely model-shaped: condensing prose, drawing diagrams, writing recall
  questions. A deterministic script cannot do it. What a script *could* do — diffing Notion
  against a manifest — is small enough to live as a documented tool sequence.

`subjects.json` — **the real file is `.claude/skills/sync-subject/subjects.json`; read that,
not this.** The shape, abbreviated:

```json
{
  "DMBA6008": {
    "aliases": ["finance", "6008", "fst"],
    "notionCourseId": "3097b336873c80c0948dcc805089b071",
    "filePrefix": "DMBA6008",
    "stripe": "--course-d",
    "palette": { "accent": "#2f5470", "deep": "#1f3b51", "soft": "#e9eff4" },
    "fonts": "Newsreader + Inter",
    "contentShapeHint": "container",
    "live": true
  },
  "DMBA6005": {
    "aliases": ["agile", "6005", "apd"],
    "notionCourseId": "3a17b336873c80c284a7cd6be4a60c4d",
    "filePrefix": "DMBA6005",
    "stripe": "--course-e",
    "palette": { "accent": "#a8722c", "deep": "#6f4a17", "soft": "#f7efe2" },
    "fonts": "Sora + Karla",
    "contentShapeHint": "inline",
    "live": false,
    "waitingFor": "Week 1's Pre-Live Session note — build nothing before then"
  }
}
```

The real file also carries `fontHref`, `hubPage`, `cardClass`, `referencePage`, per-subject
`blockers`, a `_completedSem1` id lookup, and a `_globals` block holding the data-source URLs,
the stale-note id and the publish rules. `contentShape` was renamed `contentShapeHint` to make
it obvious it is **a hint, not a fact** — always detect shape at runtime.

---

## 3. Change detection

The sync needs to know what is new since last time. Two options:

**Option A — manifest file (recommended).** Commit `docs/notion-sync-state.json`:

```json
{
  "DMBA6008": {
    "lastSync": "2026-08-05",
    "weeks": {
      "Week 1": {
        "notebookId": "3b27b336873c8070953fd96878f5f2dc",
        "page": "DMBA6008-week1.html",
        "notes": [
          { "id": "3b27b336873c802e89a3cda117f1ff5e", "name": "Learn",
            "type": "Pre-Live Session", "editedTime": "2026-08-05T07:37:12.896Z",
            "published": true }
        ]
      }
    }
  }
}
```

A note is **changed** when its `Edited Time` is newer than the recorded value; a notebook is
**new** when it is absent. This is exact and costs one fetch per note.

**Resolved 2026-08-05 — the leaf-timestamp plan does not work as written.** This section
originally said the manifest should record `editedTime` for every leaf page of a container
note. It cannot: `Edited Time` is a *Notes database row* property, and a child page inside a
note is not a row. Fetching one returns `{"title": …}` and no timestamps at all.

What is actually available, in descending order of trust:

| Signal | Where it comes from | Trust |
| --- | --- | --- |
| `contentHash` of the harvested Markdown | computed by the skill | **exact** |
| note `Edited Time` | Notes row property | exact, for the note row only |
| tree shape — child ids and titles | the fetch | exact for added / removed / renamed pages |
| `observedAt` — the `as of <ISO>` stamp in the fetch envelope | every page, including children | strong hint |

`observedAt` was tested on 2026-08-05: the same page fetched twice minutes apart returned an
identical value (`07:36:00.112Z`), and sibling pages returned different values — so it tracks
content, not fetch time. It is undocumented, hence a hint rather than proof.

**The two-stage rule the skill implements.** A week is CHANGED when the note's `Edited Time`,
any `observedAt`, or the tree shape moved — this over-triggers, and over-triggering costs one
harvest. The `contentHash` then decides whether to rebuild, so a false alarm never churns
prose that was already reviewed. The residual risk is *under*-triggering, and the answer to
that is a **deep pass**: re-harvest every topic and compare hashes, run on request or on
suspicion.

**Option B — no state, always re-harvest.** Simpler and always correct, but re-reads
everything and re-derives pages that have not changed, which risks churning prose that was
already reviewed and approved. Cost is real but not prohibitive at current volumes.

**Recommendation: Option A.** It is not a build artefact — it is a record of what was
published, which is exactly the kind of thing this repo already keeps in `next-prompt.md`.
Confirm with Aryan before committing a new tracked JSON file.

---

## 4. The phases

### Phase 0 — Resolve and diff *(inline, no agents)*

Resolve the alias → subject. Fetch the course row, its notebooks, and each note's properties.
Compare against the manifest. Produce the NEW / CHANGED / UNCHANGED table.

**Stop condition:** if nothing changed, say so and stop. Do not rebuild pages to prove the
tool ran.

### Phase 1 — Scope negotiation *(one question, then commit)*

Use `AskUserQuestion` — this is a genuine fork where the answer changes the work:

> **What should I rebuild for DMBA 6008?**
> - **Everything that changed** *(recommended)* — new Week 2 page, plus Week 0's summary,
>   glossary and cards regenerated
> - **New weeks only** — build Week 2, leave Week 0 as published
> - **Flashcards and glossary only** — refresh recall material across all changed weeks,
>   leave the summaries and visuals untouched
> - **Summaries and visuals only** — leave the decks alone

That last pair is the "update quizzes, or all" distinction. It matters because the three
modes have different review costs: a regenerated glossary is cheap to eyeball, a regenerated
summary with five hand-drawn SVGs is not.

Ask **once**, at the start. Do not re-ask per week.

### Phase 2 — Harvest *(fan out, one agent per topic)*

As [notion-sync.md §3 step 2](notion-sync.md#step-2--harvest-to-markdown-verbatim).
Agents write Markdown to scratchpad and return manifests only.

**Gate:** if a harvest agent reports a topic as empty, it stays empty on the page. It is never
filled in.

### Phase 3 — Build fragments *(fan out, one agent per topic)*

As [notion-sync.md §3 step 3](notion-sync.md#step-3--build-the-page-fragments). Each agent
gets a unique SVG id prefix. Honour the Phase 1 scope — a "flashcards only" run asks for
`CARDS` and nothing else.

### Phase 4 — Assemble and register

Fill the shell. Merge arrays. Update `articlesBySubject` **and** `validSubjects` together.
Drop `card--muted` from `index.html` on a subject's first page. Update the hub page's week
list and its per-week counts.

### Phase 5 — QA *(fan out, adversarial)*

Four checks, run in parallel. These are the point of the whole design — the failure mode of
a generative pipeline is confident, plausible, wrong content.

| Check | What it does | Verdict |
| --- | --- | --- |
| **Fidelity** | Given the built page and the harvest Markdown, find every claim, number, formula, company name and worked example on the page that is **not** traceable to the source. Default to flagging when unsure. | Any hit blocks publication |
| **Structure** | Tag balance, unique `id`s, every `aria-labelledby` resolving, every relative link resolving, no `only-accessible-by-url` link | Any hit blocks |
| **SVG** | Every `<text>` fits its container: estimate ~6.5px/char at 12px, ~5.4px at 10px, compare against the parent `rect` width. Report overflows with the element and the overflow in px | Any hit blocks |
| **Privacy** | Scan the built page for anything sourced from a `Live Session` or `Assessment` note, for lecturer or classmate names, and for `Confidence` / `Last Reviewed` telemetry | Any hit blocks, escalate to Aryan |

The fidelity check must be given the harvest Markdown and the built page **only** — no access
to the model's own memory of what the content said, and no web access. It is checking
transcription, not plausibility.

**What these four gates cannot catch: layout.** On the first run every static check passed —
balanced tags, resolving references, valid JS, SVG labels inside their boxes — while the
flashcard was visibly broken, because `.flip-inner` was a `<span>` with no `display: block`,
so its `width` and `min-height` were silently ignored and the absolutely-positioned faces
collapsed. Aryan spotted it by looking at the page.

Two consequences for the skill:

- **A browser look is a required step, not an optional one.** Finish by `open`-ing each built
  page and asking the author to confirm, or drive it with the `claude-in-chrome` skill if it
  is available. Never report a page as done on static checks alone.
- **Add a fifth, cheap gate: inline-layout sanity.** For every class that sets `width`,
  `height`, `min-height`, `padding` or `margin` and is applied to a `<span>`, confirm the
  span is either given `display: block` / `inline-block` / `flex` / `grid`, or is a child of a
  flex or grid container (which blockifies it). That one rule would have caught this.

A related fix worth carrying forward: the card faces now stack with `display: grid` on
`.flip-inner` plus `grid-area: 1 / 1` on `.face`, rather than `position: absolute; inset: 0`.
Absolute positioning locked the card to a fixed height and clipped the longer Cash Flow
answers; grid stacking sizes it to the taller face.

Tag-balance snippet (referenced from [notion-sync.md §4](notion-sync.md#4-verifying)):

```python
import sys
from html.parser import HTMLParser
VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.errs=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack: self.errs.append(f"stray </{tag}> at {self.getpos()}"); return
        t, pos = self.stack.pop()
        if t != tag:
            self.errs.append(f"</{tag}> at {self.getpos()} closes <{t}> opened at {pos}")
p = P(); p.feed(open(sys.argv[1]).read())
for e in p.errs: print("ERR:", e)
if p.stack: print("UNCLOSED:", p.stack)
if not p.errs and not p.stack: print("OK")
```

### Phase 6 — Report and hand back

Report what was built, what QA flagged, and what was deliberately left out (empty topics,
live-session notes). Update the manifest. Update `next-prompt.md`. **Do not commit** —
`CLAUDE.md` forbids committing unless asked.

---

## 5. Cost and scale

The first run of DMBA 6008 used roughly ten agents: one conventions mapper, three harvesters,
three fragment builders, plus assembly and verification inline. A steady-state run adding one
new week should need **two harvesters and two builders** — the fan-out is per *topic within a
week*, not per week.

Keep the fan-out to topics. A week with one topic gets one agent, not three.

---

## 6. The fragment spec

Agents building page fragments must be handed a spec, or they invent class names and the
assembly step becomes hand-editing. **The spec lives at
`.claude/skills/sync-subject/reference/fragment-spec.md`** and is handed to every fragment
agent verbatim. Its essentials:

- **Content rules.** The harvested Markdown is the only permitted source. No outside
  knowledge, no invented examples, no completed truncations, no invented citations. Typos in
  flowing prose may be fixed; numbers, defined terms, formulas and company names may not be
  touched.
- **Output.** One file, three delimited sections: `SUMMARY` (HTML fragment), `TERMS` (JS
  array literal), `CARDS` (JS array literal). No `<html>`, `<style>` or `<script>`.
- **Class vocabulary.** `.block`, `.block-num`, `.formula` / `.formula-stack`,
  `.callout--ask` / `.callout--key`, `.table-scroll`, `.verdict--pos|neu|neg`, `.steps`,
  `.takeaways`, `.example-grid` / `.example`, `figure > .fig-frame > svg` + `figcaption`.
  Nothing else — everything is defined in the shell.
- **SVG rules.** Hand-authored inline SVG only, `viewBox="0 0 720 H"`, no width/height.
  Literal hex values (CSS custom properties do not inherit into every SVG attribute). Text
  classes `.svg-label` / `.svg-sub` / `.svg-mono` / `.svg-eyebrow`. Every label must fit its
  box. Unique id prefix per agent. Diagrams must show a mechanism or a comparison, never
  decoration.
- **Volumes.** 900–1400 words of summary prose and 2–4 figures per topic; 12–22 glossary
  terms; 18–28 flashcards.

---

## 7. Extending to DMBA 6005

The week/notebook and pre-live/live structure is **identical**, so Phases 0–6 apply unchanged.
Four things differ.

### a. Content shape is inline, not container

DMBA 6008's pre-live notes are containers whose real prose sits two or three levels down.
DMBA 6005's Week 0 note (`$RUs`) holds its content **directly on the note page**. The
harvester must branch on this: if a note's `<content>` is nothing but `<page url=…>` links,
recurse; otherwise take the body.

Record the expected shape in `subjects.json` as a hint, but **detect it at runtime** — a
subject can change shape between weeks, and the detection is trivial.

### b. One topic per week, not four

A DMBA 6008 week fans out to three or four topic agents. DMBA 6005's Week 0 is a single case
study. Fan out **one** agent. Do not manufacture topic divisions to fill a template.

### c. The content is case-based, so the visual and card vocabulary shifts

DMBA 6008 is formula-driven — flows, waterfalls, spread gauges, worked numeric examples.
DMBA 6005's Week 0 is a strategic case: a firm, a problem, three options, a decision rule.
The natural figures are **option-comparison matrices**, **customer-journey stages**
(awareness → engagement → conversion → service experience) and **decision trees**, not
equations. `.formula` will go mostly unused; `.example-grid` becomes an option/benefit/risk
comparison rather than a numeric worked example.

Flashcards shift with it: fewer "compute this", more "given this symptom, which option and
why". The Week 0 case supports that directly — it states which option to choose for each
diagnosis.

Agile weeks proper (ceremonies, artefacts, iteration) will want **cycle diagrams** and
**timeline/board** figures. Do not force the finance visual language onto them.

### d. It needs its own visual identity

`CLAUDE.md`: *never change a page's visual identity without being asked*, and each artefact
family owns its own palette and typography. DMBA 6008 took `--course-d` petrol blue with
Newsreader + Inter.

**Settled 2026-08-05: DMBA 6005 takes `--course-e` ochre `#a8722c` with Sora + Karla.** Sora
for display — geometric, wide, angular terminals, reading like product documentation rather
than academia, which suits agile delivery material; Karla for body, humanist and warm. The
`fontHref` is in `subjects.json`.

The repo's fonts were inventoried before choosing, and thirteen are already spoken for: IBM
Plex Mono, DM Sans, Inter, Syne, IBM Plex Sans, Playfair Display, DM Mono, Newsreader, DM
Serif Display, Fraunces, Spline Sans, Space Mono and Space Grotesk. **Re-run that inventory
before choosing a pairing for any future subject** —
`grep -rhoE 'family=[A-Za-z+]+' --include='*.html' .`

### e. On hold — settled 2026-08-05

Only Week 0 is publishable. `Week1: Project Management` has its `- [ ] Pre-Live` item
unticked and holds only a `Class Diary` live-session note. `New Notebook` is an empty
placeholder and should be skipped, not rendered as a week.

**Aryan's decision: hold the whole subject until Week 1's pre-live note exists**, then launch
Week 0 and Week 1 together rather than ship a one-week subject. **Build nothing before then**
— not even unpublished pages. The trigger to watch is a `Pre-Live Session` note appearing
under notebook `3b17b336873c80ada0b3f4a02cb2dea8`; when it does, say so and ask whether to
run. Un-muting the `index.html` card still needs a separate yes — it is a visible statement
that the subject has material.

### f. Runbook — the first DMBA 6005 sync

Run this once, when Week 1's pre-live note exists **and** Aryan says go.

1. **Confirm the trigger.** Week 1 must have a `Pre-Live Session` note — a `Class Diary`
   alone does not count. The pairing (Sora + Karla) and palette (`--course-e` ochre) are
   already settled; un-muting the `index.html` card still needs its own yes (§7d, §7e).
2. Resolve the course (`3a17b336873c80c284a7cd6be4a60c4d`) and its notebooks. Expect three.
   **Skip `New Notebook`** — it is an empty placeholder, not a week. Skip any notebook whose
   pre-live notes are all empty.
3. Harvest Week 0's `$RUs` note. It is **Shape B (inline)** — the content is on the note page
   itself, so do not go looking for child pages. One agent is enough; there is one topic.
4. Build one fragment. Reach for option-comparison matrices, a customer-journey strip
   (awareness → engagement → conversion → service experience) and a decision-rule table —
   not formulas. The case states which option suits each diagnosis, which makes good
   "given this symptom, which option" flashcards.
5. Create `DMBA6005-weeks.html` and `DMBA6005-week0.html` by cloning `DMBA6008-week1.html`'s
   shell and swapping the palette to `--course-e` ochre and the agreed fonts. Week 0 needs no
   topic sub-tabs — that machinery is only in `DMBA6008-week0.html` because it has four topics.
6. Register both in `articlesBySubject.DMBA6005` in `library.html`. `DMBA6005` is already in
   `validSubjects`, so nothing to add there — but check.
7. Only if Aryan agreed in step 1: drop `card--muted` from the DMBA 6005 card in `index.html`
   and rewrite its `card-desc`.
8. Run all five QA gates, **open the pages in a browser**, then update `CLAUDE.md`'s subject
   table and `next-prompt.md`.

### g. Runbook — updating DMBA 6005 once more weeks land

After the first sync, 6005 is an ordinary subject and the standard flow in §4 applies. The
only 6005-specific things to keep in mind:

- **Week 1 is the one to watch.** `Week1: Project Management` becomes syncable the moment its
  `- [ ] Pre-Live` item is ticked and a `Pre-Live Session` note appears. Until then it has
  only a `Class Diary`, which is a `Live Session` note and **must not be published**.
- **Re-check the content shape every time** (§7a). Aryan may start using child pages for a
  longer week, which flips it to Shape A mid-subject. Detect, do not assume.
- **Agile weeks will not look like the Week 0 case study.** Ceremonies, artefacts and
  iteration want cycle diagrams, board/timeline figures and sequence strips. Do not reuse the
  Week 0 option-matrix vocabulary just because it is already there.
- Add each new week to `DMBA6005-weeks.html` and to `articlesBySubject`, and update the hub
  card's visual / concept / flashcard counts — those are hand-written numbers, and stale
  counts are the easiest thing to leave behind.

---

## 8. Decisions — settled 2026-08-05

All but one were settled with Aryan on 2026-08-05, when the skill was built. The skill at
`.claude/skills/sync-subject/` implements them.

1. **Commit `docs/notion-sync-state.json`?** — **Yes.** It exists, tracked, seeded with the
   DMBA 6008 state.
2. **Manifest granularity for container subjects** — **superseded.** Leaf `Edited Time` does
   not exist; see the rewritten §3 for the signal hierarchy and the two-stage rule.
3. **DMBA 6005 type pairing and whether to go live with one week** (§7d, §7e) — **settled.**
   Pairing is **Sora + Karla**. Go-live is **held until Week 1's pre-live note exists**, then
   both weeks launch together; nothing is built before then. Un-muting the card still needs a
   yes.
4. **Images** — **skip them.** Not downloaded, not linked, not committed. The sync reports
   the count per week so Aryan can ask for a specific one.
5. **Should the hub page show `Confidence`?** — **No.** It stays private, with
   `Last Reviewed`, `Days Since` and `Favorite`.
6. **Does the pipeline ever run in reverse?** — **No.** Notion is authoritative, the repo is
   publish-only. The skill must never write to Notion.
