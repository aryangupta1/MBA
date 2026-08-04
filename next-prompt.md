# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-04
**Left by:** repo-setup session (CLAUDE.md + docs scaffolding + SessionStart hook)

---

## Current focus

**Refactor the root page into semester views.** Requested by the user on 2026-08-04, not
yet started.

Today `index.html` shows a flat grid of three subject cards. It needs to group subjects by
semester, with a second semester added.

**2026 Semester 1** — the three existing subjects, unchanged:

| Code | Subject |
| --- | --- |
| DMBA 6001 | Leading Strategic Digital Transformation |
| DMBA 6002 | Digital disruption & organisations |
| DMBA 6004 | Remote & hybrid work |

**2026 Semester 2** — two new subjects, no content yet:

| Code | Subject |
| --- | --- |
| DMBA 6008 | Finance, Strategy and Technology |
| DMBA 6005 | Agile Project Development |

What the change involves:

1. `index.html` — replace the single `.grid` with one section per semester, each with its
   own `.section-head` label ("2026 Semester 1", "2026 Semester 2") and card grid. Keep
   the existing hero, card component, stripe treatment, and animation stagger; this is a
   grouping change, not a redesign.
2. `index.html` `:root` — add stripe colours for the two new subjects (`--course-d`,
   `--course-e`) that sit with the existing house palette, plus `.card--6008` /
   `.card--6005` rules. See [docs/style-guide.md](docs/style-guide.md#house-palette-shared-surfaces).
3. `library.html` — add `DMBA6008` and `DMBA6005` keys to `articlesBySubject` (empty
   arrays are fine; the page already renders "No articles in this library yet.") and add
   both codes to `validSubjects`. **Both must be updated together** or the new cards fall
   back to DMBA 6002.
4. Confirm the empty-library state actually renders for the two new subjects, and check
   the hub at mobile width — two grouped sections change the vertical rhythm.
5. Update the subject table in [CLAUDE.md](CLAUDE.md#what-this-repo-is) to include the
   semester grouping and the new subjects.

Open questions to put to the user if they matter:

- Should Semester 2 be visually de-emphasised (e.g. the existing `.card--muted` dashed
  style) until it has content, or presented identically to Semester 1?
- Is DMBA 6004's full subject title known? The repo only ever refers to it by code and by
  topic — do not invent one.

## Do first

1. Read [CLAUDE.md](CLAUDE.md) if it is not already in context.
2. Open [docs/workflows.md](docs/workflows.md#add-a-new-subject) — the "Add a new subject"
   recipe covers most of steps 2–3 above.
3. Confirm the working tree is clean (`git status`) before starting.

## Open threads

- [ ] The semester refactor above.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask the user first, since it rewrites tracked state.
- [ ] Content pages (e.g. `DMBA6001-*.html`) have no "back to library" link. Adding one is
      the documented convention now; retrofit existing pages when you next edit them. See
      [docs/conventions.md](docs/conventions.md#navigation).

## Do not

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
  not listed there has no inbound link.
