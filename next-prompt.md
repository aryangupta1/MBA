# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-05
**Left by:** notion-sync session — connected Notion MCP, built the DMBA 6008 week pages from
Aryan's notebooks, and wrote the sync documentation

---

## Current focus

**Automate the Notion → site sync so Aryan can say "Update finance" and get it.**

The design is already written — read [docs/notion-sync-automation.md](docs/notion-sync-automation.md)
in full before doing anything. It specifies the skill layout, change detection, the six
phases, and the four QA gates. Do not redesign it from scratch; do resolve the open
decisions in its §8 with Aryan.

Build it as a **skill** at `.claude/skills/sync-subject/`, not a script — the repo forbids a
build step, and the work (condensing prose, drawing SVG, writing recall questions) is
model-shaped. See §2 of that doc for the reasoning and the file layout.

### Do first

1. Confirm Notion is authenticated (`claude mcp list`). If it says `Needs authentication`,
   ask Aryan to run `/mcp`. Nothing else can proceed until that is done.
2. Read [docs/notion-sync.md](docs/notion-sync.md) — the schema, the two content shapes,
   and the publish rules. Then [docs/notion-sync-automation.md](docs/notion-sync-automation.md).
3. Settle the five open decisions in notion-sync-automation.md §8 with Aryan **before**
   writing the skill. The manifest-file decision (§3) in particular changes the design.
4. Then build `.claude/skills/sync-subject/` and dry-run it against DMBA 6008 — it should
   report "nothing changed", since 6008 is fully synced as of 2026-08-05.

## Open threads

- [ ] **DMBA 6005 is not synced.** Only its Week 0 is publishable — one pre-live note, a
      ~700-word case study called `$RUs`. `Week1: Project Management` has its pre-live
      unwritten (only a `Class Diary` live-session note exists) and `New Notebook` is an
      empty placeholder. It also needs its own type pairing and the `--course-e` ochre
      palette. Full detail in
      [docs/notion-sync-automation.md](docs/notion-sync-automation.md#7-extending-to-dmba-6005).
      **Ask before un-muting the 6005 card on `index.html`** — that is a visible claim that
      the subject has material.
- [ ] **DMBA 6008 Week 0 → "Assessing Financial Performance" is empty in Notion.** All ten
      sub-pages are blank and the item is unticked in the notebook todo. `DMBA6008-week0.html`
      renders an honest "not yet written" panel listing the ten pending sub-pages. When Aryan
      writes those notes, that panel is the thing to replace. Nothing was invented to fill it.
- [ ] The Week 1 **live-session diary** is harvested but deliberately unpublished — it has
      candid remarks about the lecturer, about classmates' AI use, and about what will be
      examined. Held at `scratchpad/notion/wk1-live-diary.md` (session-scoped, will not
      survive). If Aryan wants any of it, he has to say so for that specific content.
- [ ] Nobody has visually checked `index.html` at narrow width since the semester refactor.
      Still open from the previous session.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask first, it rewrites tracked state.
- [ ] Content pages (e.g. `DMBA6001-*.html`) still have no "back to library" link. The three
      new `DMBA6008-*.html` pages **do** have one. Retrofit the old pages when next editing
      them. See [docs/conventions.md](docs/conventions.md#navigation).
- [ ] DMBA 6004's full subject title is still unknown in this repo. Notion calls it "Digital
      Collaboration, Work and Organisation" — but the repo has always used the short topic
      label. **Ask Aryan before reconciling**; the same mismatch exists for DMBA 6002.

## Do not

- **Do not publish `Live Session` or `Assessment` notes.** Only `Pre-Live Session`. This is
  the single most important rule of the sync — GitHub Pages makes everything public. See
  [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published).
- **Do not fill an empty Notion topic with generated content.** An empty topic renders as
  empty. This already came up once and the honest panel is the precedent.
- Do not publish the `Confidence`, `Last Reviewed`, `Favorite` or `Days Since` fields — they
  are personal study telemetry, excluded by default.
- Do not reference a Notion image URL in a committed page. They are presigned S3 links that
  expire in 5 minutes. Publishing one means downloading and committing the file — ask first.
- Do not add a build step, an npm dependency, or a generator in the deploy path.
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not restyle existing pages wholesale; each page owns its visual identity.
- Do not commit or push unless the user asks. **The 2026-08-05 work is uncommitted.**

## Recently shipped (uncommitted — the user has not asked for a commit)

1. **`DMBA6008-weeks.html`** — new subject hub listing each week as a card.
2. **`DMBA6008-week0.html`** — Fundamentals of financial management. Four topic sub-tabs
   (balance sheet / P&L / cash flow / the empty one), 12 SVG figures, 66 key concepts,
   88 flashcards. ~247KB.
3. **`DMBA6008-week1.html`** — Key value principles. 5 SVG figures, 20 key concepts,
   25 flashcards. **This is the reference implementation** — clone its `<style>` and
   `<script>` for any new week page.
4. `library.html` — three DMBA6008 entries added to `articlesBySubject`.
5. `index.html` — `card--muted` dropped from the DMBA 6008 card, description rewritten.
   DMBA 6005 is still muted.
6. `docs/notion-sync.md`, `docs/notion-sync-automation.md` — new; both indexed in
   `docs/README.md` and `CLAUDE.md`.
7. `CLAUDE.md` — subject table updated for DMBA 6008.

Verified: all five pages parse with balanced tags; every `aria-labelledby` / `aria-controls`
resolves; all 20 registry hrefs resolve; both inline scripts pass `node --check`; no
duplicate `id`s; every SVG text label sits inside its viewBox.

An adversarial fidelity agent checked Week 0's numbers, companies, formulas and figures
against the harvested notes. Every dollar figure, percentage, day count and company
attribution traced to source. **Four defects were found and fixed:** figure `bsfig1` asserted
that non-current assets are "depreciated over their useful lives" when the notes say land is
not depreciated and goodwill is not amortised; figure `bsfig3` fused two separate worked
examples into one claim; and two glossary `src` labels named the wrong sub-page. A fifth
flag was a false positive — the agent had the harvest files but not the notebook page, which
does carry the todo list the panel refers to.

**Aryan found a rendering bug the static checks missed:** `.flip-inner` was a `<span>` with no
`display: block`, so the flashcard collapsed. Both week pages now use `display: grid` on
`.flip-inner` with `grid-area: 1 / 1` on `.face`, which also lets the card grow to fit long
answers instead of clipping them. See
[docs/notion-sync-automation.md §4 Phase 5](docs/notion-sync-automation.md#phase-5--qa-fan-out-adversarial)
for the proposed fifth QA gate.

**Still not verified:** nobody has eyeballed the pages at narrow width, and the flip has not
been checked on a real touch device.

## Notes for the next session

- **The whole pipeline hinges on the Notes `Type` field** (`Pre-Live Session` / `Live Session`
  / `Assessment`). Everything else is plumbing.
- **Two content shapes exist and a harvester must detect which.** DMBA 6008's pre-live notes
  are containers whose prose sits 2–3 levels down in child pages; DMBA 6005's sits inline on
  the note page itself. Detect at runtime — do not trust a per-subject config.
- `notion-query-data-sources` is **metered** on this Notion plan. `notion-fetch` on a relation
  URL is not. Prefer fetch.
- A stale Note URL `83e72ed6-425f-4c30-9f45-c2f9c45e08fd` sits in the `Notes` relation of
  every 6008 and 6005 notebook and 404s. Skip it; it is not a failure.
- An archived notebook still appears in the Course's `Notebooks` relation, flagged `deleted`
  on the returned `<page>` element. Skip those.
- **The agent fan-out unit is the topic within a week, not the week.** Week 0 had three
  topics → three harvesters and three fragment builders. A one-topic week gets one agent.
- Give each fragment-building agent a **unique SVG id prefix** (`bs`, `pl`, `cf`) or
  `aria-labelledby` targets collide when fragments are concatenated.
- Splice fragments into the page shell with a script, not by hand — the summary blobs are
  5–7k words each and there is no reason to route them through context. The Week 0 shell used
  `<!--INSERT:TOPIC-->` and `/*BS_TERMS*/[]/*END*/` markers.
- `library.html`'s `articlesBySubject` and `validSubjects` must be updated **together** — a
  subject in one but not the other silently falls back to DMBA 6002.
- Query-string pages need a real URL to test locally:
  `open "file:///Users/aryan/Documents/MBA/library.html?subject=DMBA6008"`.
- MCP tools are **deferred**: schemas load only via `ToolSearch` (`select:<exact_tool_name>`).
- The `SessionStart` hook lives at `.claude/hooks/load-next-prompt.sh`, wired in
  `.claude/settings.json`. If this note did not appear at the top of your context, the hook is
  not firing — tell the user to open `/hooks` once or restart the session.
