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

## 5. Volumes, per topic

| Thing | Target |
| --- | --- |
| Summary prose | 900–1400 words |
| Figures | 2–4 |
| Glossary terms | 12–22 |
| Flashcards | 18–28 |

Scale down honestly for a thin source. A 700-word case study does not owe anyone 1400 words
of summary — pad and you have broken rule 2.

---

## 6. Flashcard quality

- One idea per card. If the answer needs a semicolon and an "and also", it is two cards.
- The answer must be checkable out loud in a sentence or two.
- Mirror the material: formula topics get "compute this" and "what does this ratio tell
  you"; case topics get "given this symptom, which option and why".
- No card whose answer is not in the source.

---

## 7. Worked reference

`DMBA6008-week1.html` is the reference implementation — 5 figures, 20 terms, 25 cards. Read
its `#panel-summary` markup and its `TERMS` / `CARDS` arrays before writing your first line.
Match its density and its register.
