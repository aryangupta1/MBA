# Documentation

Internal documentation for the MBA coursework site. Not reader-facing — these files live
in the repo for the author and for Claude Code sessions. They are excluded from search
engines via `robots.txt`.

Start at [`../CLAUDE.md`](../CLAUDE.md) for the short version and the hard constraints.

## Contents

| Doc | What it covers |
| --- | --- |
| [architecture.md](architecture.md) | Site map, the two page families, routing through `library.html`, deployment |
| [conventions.md](conventions.md) | File naming, directory layout, page anatomy, registration, navigation, git |
| [style-guide.md](style-guide.md) | Design tokens, typography, colour, layout, components, motion, accessibility |
| [content-guide.md](content-guide.md) | Voice, referencing, AI-use acknowledgement, unlisted content, academic integrity |
| [workflows.md](workflows.md) | Recipes: new reading summary, new blog post, new unlisted appendix, publishing |
| [next-prompt-protocol.md](next-prompt-protocol.md) | How `next-prompt.md` is injected, honoured, and updated |

## The one-paragraph summary

Hand-written static HTML, no build step, published by GitHub Pages from `master`. The
root directory holds one self-contained file per artefact. `index.html` links to
`library.html?subject=DMBA600X`, which reads an inline JavaScript object to render the
list of pages for that subject — **that object is the site's only registry**. `blogs/` is a
separate sub-site with a shared stylesheet and a dark-mode toggle.
`only-accessible-by-url/` holds unlisted pages that are deliberately not indexed.
