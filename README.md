# MBA — a shared second brain

Notes, reading summaries, case-study analyses, and blog posts from an MBA at the
University of Sydney Business School. Published as a plain static site:

**→ [aryangupta1.github.io/MBA](https://aryangupta1.github.io/MBA/)**

Written for my own revision, shared in case it is useful to anyone taking the same
subjects.

## What's here

| Subject | Content |
| --- | --- |
| **DMBA 6001** — Leading Strategic Digital Transformation | Reading summaries, case studies, and a four-part blog series on trust in hospitality |
| **DMBA 6002** — Digital disruption & organisations | Assessment overviews, cheat sheets, and reading infographics |
| **DMBA 6004** — Remote & hybrid work | Remote-work playbook summaries and weekly case studies |

Start at [`index.html`](index.html), pick a subject, and browse its library.

## How it's built

Hand-written HTML. No framework, no build step, no dependencies, no JavaScript beyond a
few inline lines where a page needs tabs or a theme toggle.

Each artefact is a single self-contained file with its own inline styles and its own
visual identity chosen to suit the material. The exception is [`blogs/`](blogs/), which
shares one stylesheet and a light/dark toggle.

```
index.html          hub — pick a subject
library.html        per-subject index (?subject=DMBA6001)
DMBA*.html          one file per artefact
blogs/              blog sub-site with a shared theme
```

To run it locally, open `index.html` in a browser. That's the whole toolchain.

```bash
git clone https://github.com/aryangupta1/MBA.git
cd MBA
open index.html          # or: python3 -m http.server 8000
```

## Contributing

Corrections are welcome — a wrong citation, a broken link, a mangled layout, or a claim
I've misread from a source. Open an issue or a pull request.

Before you send a PR:

- Read [`docs/`](docs/) — [conventions](docs/conventions.md) for file naming and page
  structure, [style guide](docs/style-guide.md) for design tokens and accessibility.
- Register any new page in the `articlesBySubject` object in `library.html`, or it won't
  be reachable.
- Keep pages self-contained: no new dependencies, no build step.
- Check your change at mobile width and confirm focus outlines still show when tabbing.

Two things I won't merge: rewrites of the academic arguments themselves, and any change to
a citation that isn't a correction against the actual source.

## Notes

Coursework is my own; the reference lists on each page credit the sources they summarise.
Where generative AI assisted (mostly figures and reference-checking), each blog post says
so explicitly in its acknowledgement block.

Nothing here is an official University of Sydney publication.

— Aryan Gupta · [agup0543@uni.sydney.edu.au](mailto:agup0543@uni.sydney.edu.au)
