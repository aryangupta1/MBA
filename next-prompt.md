# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-04
**Left by:** semester-refactor session

---

## Current focus

**Explore the Notion MCP server and work out — with Aryan — what it should actually be
used for.** Requested by the user on 2026-08-04. This is a **collaborative, exploratory**
session, not a build session. Do not go build an integration on your own; the point is to
try things, show Aryan what is possible, and agree on a direction together.

### State of play

`claude mcp list` reports:

```
notion: https://mcp.notion.com/mcp (HTTP) - ! Needs authentication
```

So the server is **already configured but not authenticated**. Authentication is
interactive and Aryan has to do it — ask them to run `/mcp` and complete the Notion login
before anything else. Nothing else in this focus can proceed until that is done.

### How to run the session

1. Get Notion authenticated (above). Confirm with `claude mcp list`.
2. **Explore before proposing.** Load the Notion tool schemas (they are deferred — use
   `ToolSearch` with `notion`) and see what the server actually exposes: search, page
   read, page create, database query, block append, comments. Read-only calls first.
3. Ask Aryan what already lives in their Notion — is it MBA coursework, a task system,
   reading notes, something unrelated to this repo? **Do not assume it mirrors this
   site.** The direction depends entirely on what is in there.
4. Talk through candidate directions together rather than picking one. Things worth
   putting on the table:
   - Notion as the **drafting surface**, this repo as the **published surface** — draft
     reading summaries in Notion, hand-convert to a page here.
   - Notion as the **source of truth for the registry** — a Notion database of artefacts
     that `library.html`'s `articlesBySubject` is generated from. Note this collides with
     the repo's "no build step" hard constraint unless generation is a manual, occasional,
     human-run step producing committed HTML.
   - Notion for **coursework tracking only** (assessment due dates, reading backlog) with
     no coupling to the site at all — the lowest-risk option.
   - Pulling Semester 2 (DMBA 6008, DMBA 6005) material out of Notion as it accumulates.
5. **Produce planning docs.** That is the deliverable for this focus. Put them in `docs/`
   as Markdown, in the register of the existing docs (see [docs/README.md](docs/README.md)
   and add whatever you create to that index). Suggested shape — agree it with Aryan
   first, do not just write all of these:
   - `docs/notion-integration.md` — what the integration is for, what it will and will not
     do, which constraints it must respect.
   - A short decision record of the options considered and why one was chosen.

### Constraints that bind this exploration

- **No build step, no dependencies** (see [CLAUDE.md](CLAUDE.md#hard-constraints)). Any
  direction that needs a sync script running on every page load, an npm package, or a
  generator in the deploy path is out. A human-run one-off script that emits HTML which
  then gets committed is arguably fine — but **ask Aryan before writing one.**
- **Privacy.** Notion content may include personal or unsubmitted academic material.
  Reading it into context is fine; writing any of it into this repo makes it public via
  GitHub Pages. Never move content from Notion into a committed file without Aryan saying
  so explicitly for that specific content.
- **Academic integrity** (see [docs/content-guide.md](docs/content-guide.md)). Pulling
  Aryan's own notes across is fine. Generating academic prose from them is not.

## Do first

1. Read [CLAUDE.md](CLAUDE.md) if it is not already in context.
2. `git status` — expect the semester-refactor changes below if still uncommitted.
3. Ask Aryan to authenticate Notion via `/mcp`.

## Recently shipped (uncommitted — the user has not asked for a commit)

The semester refactor is **done**. `index.html`, `library.html`, `CLAUDE.md`, and
`docs/style-guide.md` are modified in the working tree.

1. `index.html` — the flat subject grid is now two `<section class="semester">` blocks.
   **Semester 2 sits above Semester 1** (deliberate — the current semester leads).
2. Each `.section-head` carries a status pill: Semester 2 is `.status--live`
   ("In progress", accent red); Semester 1 is `.status--done` ("Completed", course-a
   green). Both are dot + uppercase Syne pills.
3. **2026 Semester 2** — DMBA 6008 (Finance, Strategy and Technology) and DMBA 6005
   (Agile Project Development). Both use `.card--muted` (dashed, translucent, no shadow)
   because they have no content yet — Aryan chose this over styling them like Semester 1.
   They are still real links to an empty library. **When a Semester 2 subject gets its
   first page, drop `card--muted` from that card.**
4. **2026 Semester 1** — the three existing cards unchanged (6001 / 6002 / 6004, with 6004
   still `card--wide`), followed by a `.sem-note` footnote: "Semester 1 is where this site
   was born. The improvements and learnings from building it will be carried into
   Semester 2."
5. New stripe tokens `--course-d` (`#2f5470`, petrol blue → 6008) and `--course-e`
   (`#a8722c`, ochre → 6005), plus `.card--6008` / `.card--6005`. Recorded in
   [docs/style-guide.md](docs/style-guide.md#house-palette-shared-surfaces).
   `.card--muted:hover .arrow` now takes `var(--stripe)` instead of a hard-coded grey.
6. The fade-up stagger is driven off **page position**, not semester —
   `.semester:nth-of-type(2) …` — so reordering the two sections again will not break it.
7. `library.html` — `DMBA6008: []` and `DMBA6005: []` added to `articlesBySubject`, and
   both codes added to `validSubjects`.

Verified: both files parse with no unclosed or mismatched tags; the registry resolves
`DMBA6008` and `DMBA6005` to empty arrays, so the "No articles in this library yet."
branch fires and the heading renders "DMBA 6008 Library". **Not verified:** nobody has
eyeballed the hub at mobile width since the reorder — two sections, two status pills, and
a footnote change the vertical rhythm.

## Open threads

- [ ] The Notion exploration above.
- [ ] Nobody has visually checked `index.html` at narrow width post-refactor.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask the user first, since it rewrites tracked state.
- [ ] Content pages (e.g. `DMBA6001-*.html`) have no "back to library" link. Adding one is
      the documented convention now; retrofit existing pages when you next edit them. See
      [docs/conventions.md](docs/conventions.md#navigation).
- [ ] DMBA 6004's full subject title is still unknown — the repo only refers to it by code
      and by topic ("Remote & hybrid work"). Do not invent one; ask Aryan if it is needed.

## Do not

- Do not build a Notion integration unilaterally. Agree the direction with Aryan first.
- Do not restyle existing pages wholesale. Each page owns its own visual identity; the
  style guide governs *new* pages and shared surfaces only.
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not commit or push unless the user asks.

## Notes for the next session

- The `SessionStart` hook lives at `.claude/hooks/load-next-prompt.sh`, wired up in
  `.claude/settings.json`, and was verified working on 2026-08-04. If this note did not
  appear at the top of your context, the hook is not firing — tell the user to open
  `/hooks` once or restart the session.
- `library.html`'s `articlesBySubject` object is the site's only registry. A page that is
  not listed there has no inbound link. `articlesBySubject` and `validSubjects` must be
  updated **together** — a subject in one but not the other silently falls back to
  DMBA 6002. Any Notion-driven registry idea has to respect this pairing.
- Query-string pages need a real URL to test locally:
  `open "file:///Users/aryan/Documents/MBA/library.html?subject=DMBA6008"`.
  Plain `open library.html?subject=…` fails — the shell treats it as a filename.
- MCP tools in this session are **deferred**: their schemas are not loaded until you call
  `ToolSearch`. `ToolSearch` with query `notion` (or `select:<exact_tool_name>`) loads them.
