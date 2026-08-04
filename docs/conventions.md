# Conventions

## File naming

### Standalone artefact pages (repo root)

```
DMBA<code>-<kebab-slug>.html
```

Examples: `DMBA6001-short-history-of-AI.html`, `DMBA6002-Assessment3-Overview.html`,
`DMBA6004-week5-case-study.html`.

Rules:

- Subject code with **no space or hyphen** inside it: `DMBA6001`, not `DMBA-6001`.
- Lowercase kebab-case slug describing the artefact. Acronyms may keep their casing
  (`-AI`, `-PNAS2025`).
- Prefix multi-part families for grouping: `DMBA6002-Infographic-<source>.html`,
  `DMBA6002-Assessment<N>-Overview.html`.
- No dates or version numbers in filenames — git holds history.

**Known legacy exceptions** (do not rename; renaming breaks any shared URL):
`DMBA-6001-john_deere_case_study.html`, `DMBA-6001-telecom-iot.html`,
`DMBA-6004-Week6-case.md`. New files follow the canonical form.

### Blog posts

```
blogs/blog-<N>/index.html      post, N in publication order
blogs/blog-<N>/images/img-00N.png   figures, zero-padded, in document order
blogs/blog-<N>/post.pdf        submitted PDF
blogs/blog-<N>/note.txt        optional provenance/attribution note
```

### Unlisted pages

```
only-accessible-by-url/<kebab-slug>.html
```

No subject prefix — these are appendices reached only by a direct link.

### Source material

Reading PDFs sit beside their summary page in the repo root, named after the source
(`peter-et-al-2025-the-benefits-and-dangers-of-anthropomorphic-conversational-agents.pdf`).
Blog submission PDFs live in `blogs/`.

## Anatomy of a standalone page

Every standalone page follows this skeleton. Match it.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><!-- Artefact name, human readable --></title>
  <link href="https://fonts.googleapis.com/css2?family=…&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      /* every colour and size used on this page, named */
    }

    /* page styles, grouped by section, top of page to bottom */
  </style>
</head>
<body>
  <!-- semantic content -->
  <script>
    /* only if the page needs interactivity; vanilla JS, IIFE-wrapped */
  </script>
</body>
</html>
```

Required in every page:

- `<!DOCTYPE html>` and `lang="en"`.
- UTF-8 charset and the responsive viewport meta.
- A meaningful `<title>` — it is what appears in a browser tab and a shared link.
- A `:root` block declaring every colour as a custom property. No raw hex values scattered
  through the rules.
- The universal `box-sizing: border-box` reset.

Add `<meta name="description" content="…">` on pages meant to be shared or indexed.
Unlisted pages instead carry `<meta name="robots" content="noindex, nofollow, noarchive">`.

## Registration

**Every new reader-facing page must be registered in `library.html`.** Add an entry to the
correct subject array in `articlesBySubject`:

```js
{ title: 'A Short History of AI', href: 'DMBA6001-short-history-of-AI.html',
  description: 'Reading summary — A Short History of AI' },
```

- `title` — what the reader clicks. Short.
- `href` — path relative to the repo root.
- `description` — one line of context. Prefix with the kind of artefact where it helps:
  `Reading summary — …`, `Case Study — …`, `Infographic — …`, `Visual Overview — …`.
- Order within a subject array is the display order. Newest or most relevant near the top
  of its group; keep related items adjacent.

Adding a **new subject** means: a new key in `articlesBySubject`, the code added to
`validSubjects`, a new card in `index.html`, and a `--course-*` stripe colour.

## Navigation

- `index.html` → `library.html?subject=…` → artefact page.
- `library.html` links back to `index.html` via the `.back` link.
- Blog posts link back to `../index.html` (the blog index) via `.back-row`.
- **Convention for new standalone pages: include a back link to
  `library.html?subject=DMBA600X`** as the first element in the body, styled to match the
  page. Most existing artefact pages predate this and have no back link; add one when you
  are already editing a page, not as a standalone sweep.

## Directory placement

| Putting what | Goes where |
| --- | --- |
| A reader-facing artefact page | Repo root, `DMBA<code>-<slug>.html`, registered in `library.html` |
| A blog post | `blogs/blog-<N>/index.html`, listed in `blogs/index.html` |
| An appendix that must not be indexed | `only-accessible-by-url/`, never linked from an indexed page |
| A figure for a blog post | `blogs/blog-<N>/images/` |
| A source reading PDF | Repo root, beside its summary |
| Internal notes for future sessions | `docs/` or `next-prompt.md` — never a reader-facing page |

Do not create new top-level directories without a reason; the flat root is intentional.

## HTML style

- Two-space indentation. Some older files use four inside `<style>` — match the file you
  are in, not the guide.
- Semantic elements: `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>`,
  `<figure>`/`<figcaption>`, `<time datetime="YYYY-MM-DD">`.
- Class names are kebab-case and descriptive of role, not appearance: `.milestone-card`,
  `.q-panel`, `.crit-track`. BEM-ish modifiers where useful: `.card--muted`, `.card--6001`.
- `aria-hidden="true"` on purely decorative elements (arrows, dots, rules).
- Images: always `alt`, plus explicit `width`/`height`, `loading="lazy"` and
  `decoding="async"` for anything below the fold.
- Escape `&` as `&amp;` in text content.

## JavaScript style

Only when the page genuinely needs it.

- Vanilla JS, wrapped in an IIFE: `(function () { … })();`
- `var` and `function` declarations — match the existing plain-ES5 register so the files
  need no transpilation and read consistently.
- No dependencies, no `fetch`, no analytics.
- Guard DOM access (`if (!btn) return;`) so a page still renders if markup changes.

## Git

- Work on `master`. **Pushing publishes the site.**
- Commit messages in the existing style: short, lowercase, descriptive of the artefact
  (`Add DMBA6002 Assessment 3 Overview page`, `blog 4`, `fix formatting`). Prefer the
  descriptive form over one-word messages.
- One commit per artefact or per coherent fix.
- Do not commit or push unless the user asks for it.
- `.DS_Store` files are currently tracked. Leave them alone unless asked to clean up —
  untracking them changes files the user did not ask you to touch.
