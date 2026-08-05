# Automating the Notion sync

Design for turning the manual pipeline in [notion-sync.md](notion-sync.md) into one
instruction: **"Update finance."**

Nothing in this document is built yet. It is the handoff for the session that builds it.
Read [notion-sync.md](notion-sync.md) first — this assumes the schema, the two content
shapes, and the publish rules from that document.

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

`subjects.json` sketch:

```json
{
  "DMBA6008": {
    "aliases": ["finance", "6008", "fst"],
    "notionCourseId": "3097b336873c80c0948dcc805089b071",
    "filePrefix": "DMBA6008",
    "stripe": "--course-d",
    "palette": { "accent": "#2f5470", "deep": "#1f3b51", "soft": "#e9eff4" },
    "fonts": "Newsreader + Inter",
    "contentShape": "container"
  },
  "DMBA6005": {
    "aliases": ["agile", "6005", "apd"],
    "notionCourseId": "3a17b336873c80c284a7cd6be4a60c4d",
    "filePrefix": "DMBA6005",
    "stripe": "--course-e",
    "palette": { "accent": "#a8722c", "deep": "#6f4a17", "soft": "#f7efe2" },
    "fonts": "TBD — must differ from every existing pairing",
    "contentShape": "inline"
  }
}
```

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

Caveat worth deciding on: `Edited Time` on a *container* note (Shape A) does not necessarily
move when a grandchild page is edited. For container subjects the manifest should record
`editedTime` for every **leaf** page, not just the note.

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
assembly step becomes hand-editing. The spec used on the first run is reproduced at
`.claude/skills/sync-subject/reference/fragment-spec.md` when the skill is built. Its
essentials:

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
Newsreader + Inter. DMBA 6005 should take `--course-e` ochre `#a8722c` and a **different**
type pairing — every one of Syne/DM Sans, IBM Plex, Playfair, Fraunces/Spline Sans, DM Serif
Display/DM Mono, Space Grotesk and Newsreader/Inter is already spoken for in this repo.
Choose the pairing with Aryan rather than picking one silently.

### e. Current blocker

Only Week 0 is publishable. `Week1: Project Management` has its `- [ ] Pre-Live` item
unticked and holds only a `Class Diary` live-session note. `New Notebook` is an empty
placeholder and should be skipped, not rendered as a week.

**Do not publish a DMBA 6005 hub with one week and two stubs** without checking whether Aryan
wants the subject live yet — un-muting the `index.html` card is a visible statement that the
subject has material.

### f. Runbook — the first DMBA 6005 sync

Run this once, when Aryan says the subject is ready to go live.

1. **Ask two questions first** (§7d, §7e): which type pairing, and whether one published week
   is enough to un-mute the card. Do not guess either.
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

## 8. Open decisions for the next session

1. **Commit `docs/notion-sync-state.json`?** (§3) — a new tracked file, needs approval.
2. **Manifest granularity for container subjects** — leaf `Edited Time` vs note `Edited Time`.
3. **DMBA 6005 type pairing and whether to go live with one week** (§7d, §7e).
4. **Images.** Every Notion image is a 5-minute presigned URL. Publishing one means
   downloading and committing it. Is that wanted, and where do the files live?
5. **Should the hub page show `Confidence`?** It is genuinely useful study telemetry and
   deliberately excluded today as personal.
6. **Does the pipeline ever run in reverse** — a page edited here flowing back to Notion? Not
   designed for. Current model is Notion-authoritative, repo-published.
