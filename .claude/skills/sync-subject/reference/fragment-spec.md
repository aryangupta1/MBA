# Fragment spec

**You are a fragment-building agent for one topic of one week.** This document is the whole
contract. Read it before you write anything.

Everything you emit is spliced into a page shell that already defines every class, every
font and every colour. You are writing *content*, never a page.

---

## 1. Content rules — these override everything else

1. **Your harvested Markdown file is the only permitted source.** You have been given one
   file. Nothing else — not your own knowledge of finance, project management or anything
   else, not the web, not the other topics' files.
2. **Do not add.** No invented examples, no invented companies, no invented figures, no
   "for instance" that is not in the source. If the source says a thing once and vaguely,
   your page says it once and vaguely.
3. **Do not complete.** The source contains truncated sentences (`"Analysts may examine
   profit before and "`) and headings with nothing under them. Reproduce them as they are,
   or omit them. Never finish the thought.
4. **Do not improve the argument.** This is submitted university coursework. Restructuring
   and condensing the author's own notes is the point of the pipeline; generating new
   academic claims is not.
5. **Never invent or alter a citation, DOI, URL, quote or statistic.**
6. **What you may fix:** typos and grammar in flowing prose, and Notion escaping artefacts
   (`\$` → `$`).
   **What you may not touch:** numbers, dollar figures, percentages, dates, defined terms,
   formulas, company names, and anything inside a quotation.
7. **Empty means empty.** If your source file is empty or nearly so, say so in your return
   manifest and emit an honest "not yet written" block. Do not fill the gap.
   `DMBA6008-week0.html`'s fourth topic panel is the precedent — copy its approach.
8. **Australian spelling**, matching the author's notes.

If you are unsure whether something is in the source: it is not. Leave it out.

---

## 2. What you output

**One file**, at the path you were given, with exactly three delimited sections:

```
===SUMMARY===
<div class="block"> … </div>
===TERMS===
{ term: '…', src: '…', def: '…' },
{ term: '…', src: '…', def: '…', formula: '…' },
===CARDS===
{ q: '…', a: '…' },
{ q: '…', a: '…' },
```

- `SUMMARY` is an **HTML fragment**. No `<html>`, `<head>`, `<body>`, `<style>`, `<script>`,
  and no `<section class="panel">` — the shell supplies those.
- `TERMS` and `CARDS` are **JS object literals, one per line, each ending in a comma.** The
  assembly step concatenates them into an array literal. Single-quote your strings and
  escape any interior apostrophe as `\'`, or use the typographic `’` (preferred — the rest
  of the site uses it).
- Return to the orchestrator a **short manifest only**: term count, card count, figure
  count, and anomalies. Never return the content itself.

### Field shapes

| Array | Fields |
| --- | --- |
| `TERMS` | `term` (the name), `src` (which sub-page it came from), `def` (the definition), `formula` (optional), `own: true` (optional — set **only** when the definition is copied word for word from the author's own "Key Definitions" table; it renders a distinguishing chip) |
| `CARDS` | `q`, `a` |

---

## 3. Class vocabulary

These and nothing else. A class not on this list is not styled by the shell.

**Structure**

| Class | Use |
| --- | --- |
| `.block` | One numbered section of the summary. Wraps everything. |
| `.block-num` | The eyebrow inside `.block` — `01 / The core idea` |
| `h2`, `h3`, `p`, `ul`, `ol`, `strong`, `em` | Plain content |

**Emphasis and framing**

| Class | Use |
| --- | --- |
| `.formula`, `.formula-stack` | A formula, and a stack of them |
| `.callout--ask` | A question the notes pose |
| `.callout--key` | The one line that matters |
| `.takeaways` | Closing bullet list of a block |
| `.steps` | An ordered procedure |
| `.table-scroll` | **Wraps every `<table>`.** Without it, wide tables break mobile. |
| `.verdict--pos`, `.verdict--neu`, `.verdict--neg` | A good / neutral / bad judgement chip in a table cell |
| `.example-grid`, `.example` | Worked examples side by side |

**Figures**

```html
<figure>
  <div class="fig-frame">
    <svg viewBox="0 0 720 210" role="img" aria-labelledby="XXfig1-title XXfig1-desc">
      <title id="XXfig1-title">…</title>
      <desc id="XXfig1-desc">…</desc>
      …
    </svg>
  </div>
  <figcaption>…</figcaption>
</figure>
```

---

## 4. SVG rules

Hand-authored inline SVG only. There is no layout engine and no library — if a label is too
wide it simply overflows, and that is the single most common defect in this repo.

1. **`viewBox="0 0 720 H"`. No `width`, no `height` attribute.** The frame scales it.
2. **Literal hex fills and strokes.** CSS custom properties do not inherit reliably into
   every SVG attribute. Use the palette values you were given.
3. **Text classes only:** `.svg-label`, `.svg-sub`, `.svg-mono`, `.svg-eyebrow`.
4. **Every `<text>` must fit its box.** Budget ~6.5px per character at 12px and ~5.4px at
   10px, and compare against the parent `<rect>`'s width. Split long labels across two
   `<text>` lines rather than shrinking the font below 10px.
5. **A unique id prefix per agent** — you will be assigned one (`bs`, `pl`, `cf`, …). Every
   `id` you emit starts with it. Fragments are concatenated into one page and unprefixed
   ids collide, silently breaking `aria-labelledby`.
6. **`role="img"` plus `<title>` and `<desc>`**, both referenced by `aria-labelledby`. The
   `<desc>` must describe the mechanism in words, for a screen reader.
7. **A diagram must show a mechanism or a comparison.** A flow, a decomposition, a
   before/after, a gauge, a matrix. Never decoration, never a picture of a list.

### Choosing the figure

Match the figure to the material, not to the last subject you built.

| Material | Figures that work |
| --- | --- |
| Formula-driven (finance) | Flow chains, waterfalls, spread gauges, stacked bars, worked numeric examples |
| Case-based (strategy) | Option-comparison matrices, journey strips, decision trees |
| Process (agile) | Cycle diagrams, board/timeline strips, sequence flows |

Do not force finance's visual language onto a case study, or a case study's onto a process.

---

## 5. Volumes

**The budget is per `.block`, and it is measured.**

| Thing | Target |
| --- | --- |
| Flowing prose | **≤ 160 words per `.block`**, floor 900 per topic |
| Blocks per topic | 6–11 |
| Figures | 2–4 per topic |
| Glossary terms | 12–22 per topic |
| Flashcards | 18–28 per topic |

"Flowing prose" means `<p>` text. It excludes tables, figures, worked examples, callouts,
formulas, `.steps` and `.takeaways` — those carry the study material and are not what
bloats. Connective paragraphs are.

`DMBA6008-week1.html`, the worked reference, runs **134 prose words per block**. That is the
density to match.

Check it before you hand back:

```sh
python3 .claude/skills/sync-subject/reference/checks.py --lengths <page>.html
```

Scale down honestly for a thin source. A 700-word case study does not owe anyone a full
budget — pad and you have broken rule 2.

### Why this is a hard gate now

The first DMBA 6008 build shipped **~4,000 words per topic against a stated 900–1400
budget**, roughly 3× over. The number was in this file the whole time and was ignored,
because nothing measured it. It is measured now, and gate 6 blocks publication.

### The four things that caused it

1. **Prose that restates the table or figure beside it.** If the next element already says
   it in a table row, do not also say it in a sentence. Introduce the table, do not
   summarise it.
2. **Repeated callouts.** One `callout--key` per block, maximum. The first build had a block
   with three, two of which restated the block above.
3. **A closing block that re-summarises the topic.** If the block has a `.takeaways` list or
   a summary table, that *is* the summary — it does not also need two paragraphs of
   narrative in front of it.
4. **Definitions restated in every block that touches the term.** Define it once, in the
   block that introduces it.

---

## 6. Flashcard quality

- One idea per card. If the answer needs a semicolon and an "and also", it is two cards.
- The answer must be checkable out loud in a sentence or two.
- Mirror the material: formula topics get "compute this" and "what does this ratio tell
  you"; case topics get "given this symptom, which option and why".
- No card whose answer is not in the source.

---

## 7. Worked reference

`DMBA6008-week1.html` is the reference implementation — 8 blocks, 5 figures, 20 terms,
25 cards, and 134 prose words per block. Read its `#panel-summary` markup and its `TERMS` /
`CARDS` arrays before writing your first line. Match its density and its register.

Do **not** use `DMBA6008-week0.html` as a density reference. It was the first build, it
shipped roughly 3× over budget, and it was condensed after the fact on 2026-08-05 — its
balance-sheet and P&L topics are still over. Its *structure* (subtabbed topics, the honest
"not yet written" fourth panel) is worth copying; its verbosity is not.
