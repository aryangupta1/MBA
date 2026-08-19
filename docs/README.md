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
| [design-system.md](design-system.md) | **DESK** — the house design system: the desktop metaphor, tokens, components, the three page profiles. Governs `index.html` and all Semester 2 pages |
| [style-guide.md](style-guide.md) | The older language — design tokens, typography, colour, layout, components, motion, accessibility. Still governs `library.html`, Semester 1 pages and `blogs/` |
| [content-guide.md](content-guide.md) | Voice, referencing, AI-use acknowledgement, unlisted content, academic integrity |
| [workflows.md](workflows.md) | Recipes: new reading summary, new blog post, new unlisted appendix, publishing |
| [vault-sync.md](vault-sync.md) | **Live ground truth** — the Obsidian vault layout, the `publish` flag, topics, images, conflict handling, and what must never ship |
| [vault-sync-state.json](vault-sync-state.json) | Machine-written record of what has been published from the vault, and when |
| [notion-sync.md](notion-sync.md) | History — the retired Notion→**website** pipeline. Its schema notes and markup quirks are still reused by `sync-notes` |
| [notion-sync-automation.md](notion-sync-automation.md) | Design rationale behind the sync skill — change detection, the QA gates, extending it to DMBA 6005 |
| [notion-sync-state.json](notion-sync-state.json) | Superseded by `vault-sync-state.json`. History only |
| [next-prompt-protocol.md](next-prompt-protocol.md) | How `next-prompt.md` is injected, honoured, and updated |

### The syncs are skills, not docs

Aryan writes notes in **both Notion and Obsidian**; the vault is the source of truth for
publishing. Three skills, each run on command:

```
Notion --sync-notes--> Obsidian vault (~/MBA) --sync-subject--> week pages
Notion --sync-assignments--> the vault's assignment tracker
```

| Skill | Say | Does |
| --- | --- | --- |
| [`sync-notes`](../.claude/skills/sync-notes/SKILL.md) | *"sync notion"* | Pulls Notion notes into the vault. **Never overwrites an Obsidian edit** |
| [`sync-subject`](../.claude/skills/sync-subject/SKILL.md) | *"update finance"* | Builds week pages from the vault, six QA gates |
| [`sync-assignments`](../.claude/skills/sync-assignments/SKILL.md) | *"sync assignments"* | Mirrors the Notion Assignments/Exams database into the vault |

`notion-sync-automation.md` is why `sync-subject` is shaped the way it is.

## The one-paragraph summary

Hand-written static HTML, no build step, published by GitHub Pages from `master`. The
root directory holds one self-contained file per artefact. `index.html` links to
`library.html?subject=DMBA600X`, which reads an inline JavaScript object to render the
list of pages for that subject — **that object is the site's only registry**. `blogs/` is a
separate sub-site with a shared stylesheet and a dark-mode toggle.
`only-accessible-by-url/` holds unlisted pages that are deliberately not indexed.
