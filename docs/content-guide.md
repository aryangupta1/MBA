# Content guide

This site holds work submitted for assessment at the University of Sydney Business School.
The rules here are about academic integrity as much as style.

## Academic integrity — read before writing prose

1. **The arguments are the author's.** Do not write, rewrite, extend, or "strengthen" an
   academic argument unless the user explicitly asks for that. The default contribution is
   structure, formatting, layout, typography, and correctness.
2. **Never fabricate a source.** Do not invent, guess at, or "reconstruct" a citation,
   author, year, DOI, URL, page number, quote, or statistic. If a reference is needed and
   was not supplied, ask for it.
3. **Do not alter existing citations** while editing surrounding markup. Reference lists
   are checked against submission copies.
4. **Keep the AI-use acknowledgement true.** If AI assistance changes, the acknowledgement
   text changes with it. Never remove it, and never overstate or understate what was done.
5. When summarising a reading, attribute claims to the source. Paraphrase and cite; do not
   reproduce long passages.

## Voice

- Analytical and direct. Short declarative sentences.
- **Australian English**: *organisation, analyse, personalisation, behaviour, programme*
  (but *program* for software).
- Present tense for what a source argues; past tense for what happened in a case.
- First person is used in the blog series ("I write mostly through a hospitality lens")
  and avoided in reading summaries and case analyses.
- Define an acronym on first use, then use it freely.
- No marketing register, no hype, no emoji in reader-facing content.

## Page types and what they contain

**Reading summary** (`DMBA6001-short-history-of-AI.html`) — the source's argument
condensed into scannable visual sections: key concepts, milestones, people, approaches.
Ends with a footer crediting the source.

**Case study analysis** (`DMBA6004-week5-case-study.html`) — the case questions with
worked answers. The Week 6 pattern is three parts per question: **Answer** (the position),
**Script** (what to say aloud), **Slide content** (what goes on the slide). See
`DMBA-6004-Week6-case.md` for the markdown source of that pattern.

**Assessment overview** (`DMBA6002-Assessment3-Overview.html`) — the brief made
operational: requirements, marking criteria with weightings, word budget, structure,
checklist. This is a planning instrument, so accuracy against the official brief matters
more than presentation.

**Infographic** (`DMBA6002-Infographic-*.html`) — one reading rendered visually. Full
citation of the source article is mandatory and prominent.

**Blog post** (`blogs/blog-N/index.html`) — a 700–1000 word argued piece with figures, an
APA reference list, and an AI-use acknowledgement. The DMBA 6001 series is a single
sustained argument about trust in hospitality; each post should connect back to that
thread.

## Referencing

APA 7, matching the existing reference lists.

- Section markup:

```html
<section class="references" aria-labelledby="ref-heading">
  <h2 id="ref-heading">Reference List</h2>
  <ol>
    <li>Author, A. B., &amp; Author, C. D. (2024). Title of the work in sentence case.
      <em>Journal Name</em>, <em>12</em>(3), 1–17.
      <a href="https://doi.org/…">https://doi.org/…</a></li>
  </ol>
</section>
```

- Alphabetical by first author surname where a list is purely a reference list.
- Journal and book titles in `<em>`. Article titles in sentence case, plain.
- DOIs preferred over URLs, given as full `https://doi.org/…` links.
- In-text citation in the prose: `(Hadan et al., 2024)`.
- Escape ampersands as `&amp;`.

## AI-use acknowledgement

Every blog post carries this block, immediately after the reference list:

```html
<div class="ack">
  <strong>Acknowledgement of AI Use</strong>
  <p>This blog post was researched, written, and argued entirely by the author.
     Generative AI (<!-- named tool and version -->) was used to
     <!-- exactly what it did: produce visual assets, verify references, etc. -->.
     All arguments, analysis, and critical thinking reflect the author's own
     perspective and academic work.</p>
</div>
```

Name the specific tool and describe the specific use. `blogs/blog-N/note.txt` records
image provenance for the same reason — keep it current when figures change.

## Figures

- Numbered and captioned in document order: `Figure 1. Immersion raises the stakes of
  consent and disclosure.`
- Captions are full sentences that say what the figure *shows*, not what it *is*.
- `alt` text describes content for a reader who cannot see it; it is not a duplicate of
  the caption.
- A figure taken from a source is cited in the reference list like any other material.

## Metadata and titles

- `<title>` is the artefact name as a person would say it — it becomes the browser tab and
  the text of a shared link.
- `<meta name="description">` on blog posts and shareable pages: one sentence, under ~155
  characters.
- Dates use `<time datetime="YYYY-MM-DD">` with a human rendering (`26 Apr 2026`).
- The blog footer carries the author's name and university email. Keep it on every post.

## Unlisted content and privacy

`only-accessible-by-url/` exists for appendices that must be reachable by direct link (in
a submission, say) but must not be discoverable.

Requirements for anything placed there:

1. `<meta name="robots" content="noindex, nofollow, noarchive">` in the head.
2. A matching `Disallow` rule in `robots.txt`.
3. **No inbound link from any indexed page** — not `index.html`, not `library.html`, not a
   blog post.

Security by obscurity only. Never put anything genuinely confidential — personal data,
credentials, another person's information, unpublished third-party material — in this
repository at all. It is a public GitHub repo and a public website.
