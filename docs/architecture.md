# Architecture

## Shape of the site

```
/                              GitHub Pages root → https://aryangupta1.github.io/MBA/
├── index.html                 Hub — three subject cards
├── library.html               Per-subject index, driven by ?subject= query param
├── robots.txt                 Excludes unlisted + internal directories
├── CLAUDE.md, next-prompt.md, docs/     Repo-internal, not reader-facing
│
├── DMBA6001-*.html            Standalone artefact pages (reading summaries,
├── DMBA6002-*.html            case studies, assessment overviews, infographics)
├── DMBA6004-*.html            One file each, fully self-contained
├── DMBA6001-blog.html         Legacy redirect → blogs/index.html
│
├── blogs/                     Sub-site with its own shared theme
│   ├── index.html             Post listing
│   ├── assets/
│   │   ├── blog-theme.css     The only shared stylesheet in the repo
│   │   └── theme.js           Light/dark toggle, localStorage key `dmba-blog-theme`
│   ├── blog-1/ … blog-4/
│   │   ├── index.html         The post
│   │   ├── images/img-00N.png Figures
│   │   ├── post.pdf           Submitted PDF version
│   │   └── note.txt           Optional provenance note
│   ├── 6001/index.html        Standalone presentation page (dark theme, unrelated to blog theme)
│   └── agup0534-blog-post-*.pdf   Submitted PDFs
│
├── only-accessible-by-url/    Unlisted appendices — noindex + robots disallow
│   ├── stakeholder-mapping.html
│   ├── power-interest.html
│   └── metadata.html
│
└── *.pdf                      Source readings kept alongside their summary page
```

## Two page families

Everything in the repo is one of two kinds of page. Know which one you are editing before
you touch anything.

### 1. Standalone artefact pages (the majority)

Root-level `DMBA*.html` and everything in `only-accessible-by-url/`.

- **Self-contained.** One HTML file with a single inline `<style>` block and, where
  needed, an inline `<script>`. No external CSS or JS files.
- **Individually themed.** Each page picks its own palette and font pairing to suit the
  material — a warm archival palette for the history-of-AI summary, a dark technical
  palette for the Giant Swarm case study, and so on. This is deliberate.
- Only external requests are Google Fonts `<link>` tags.
- Interactivity, where present, is a few lines of vanilla JS (tab panels, progress bars,
  collapsibles) written inline.

### 2. The `blogs/` sub-site

- Shares `blogs/assets/blog-theme.css` and `blogs/assets/theme.js` across all posts.
- One consistent AstroPaper-inspired reading theme with a light/dark toggle.
- Semantic article markup with schema.org `BlogPosting` microdata.
- Posts link back to `../index.html`; the blog index is reached from
  `library.html?subject=DMBA6001`.

`blogs/6001/index.html` is neither — it is a one-off standalone presentation page that
happens to live under `blogs/`. Treat it as family 1.

## Routing

There is no router and no server-side logic. Navigation is:

```
index.html
   └─ <a href="library.html?subject=DMBA6001">  (one card per subject)
         └─ library.html reads ?subject= and renders a list from an inline JS object
               └─ <a href="DMBA6001-short-history-of-AI.html">
```

`library.html` holds the `articlesBySubject` map:

```js
var articlesBySubject = {
  DMBA6004: [ { title, href, description }, … ],
  DMBA6002: [ … ],
  DMBA6001: [ … ]
};
```

- An unknown or missing `?subject=` falls back to `DMBA6002`.
- `validSubjects` must be kept in sync with the keys of `articlesBySubject`.
- **This object is the site's only registry.** A page not listed here has no inbound link
  and is effectively invisible — which is exactly how `only-accessible-by-url/` works.

## Deployment

- GitHub Pages serves `master` from the repository root. Remote: `github.com/aryangupta1/MBA`.
- **Pushing to `master` publishes.** There is no staging environment and no build step —
  what is in the repo is what is live, within a minute or so.
- Because the site is served under the `/MBA/` path, **always use relative links**
  (`library.html`, `../assets/theme.js`). A root-absolute link (`/library.html`) breaks in
  production while appearing to work locally.
- `robots.txt` covers both `/MBA/only-accessible-by-url/` and `/only-accessible-by-url/`
  so the rules hold whether the site is served from a subpath or a domain root.

## Constraints this architecture implies

- No shared component library exists for standalone pages. Repetition across pages is
  expected and acceptable; do not refactor pages into shared partials — there is no build
  step to assemble them.
- Changing `blogs/assets/blog-theme.css` affects **every** blog post. Check all four.
- Changing `index.html` or `library.html` affects every reader's entry path. These two are
  the only truly shared HTML surfaces.
