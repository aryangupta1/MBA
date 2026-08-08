# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-06
**Left by:** launched DMBA 6005 — built Week 0 and Week 1 from Notion, registered them,
un-muted the homepage card. All six gates pass. **Nothing is committed.**

---

## Current focus

**Nothing in flight.** DMBA 6005 is live. The next sync is triggered by Aryan, not by this
file — he says *"update agile"* or *"update finance"* and the skill runs.

## Do first

1. **Ask whether to commit.** The 2026-08-06 DMBA 6005 launch is **uncommitted** in the
   working tree: `DMBA6005-week0.html`, `DMBA6005-week1.html`, `DMBA6005-weeks.html` (new),
   plus edits to `index.html`, `library.html`, `CLAUDE.md`, `docs/notion-sync.md`,
   `docs/notion-sync-state.json`, `.claude/skills/sync-subject/{SKILL.md,subjects.json}`.
   `.claude/skills/` and `docs/notion-sync-state.json` are still **untracked**.
2. If Aryan reports anything wrong with the new pages, the harvest they were built from is
   **gone** (session scratchpad). Re-harvest from Notion; the `contentHash` values in
   `docs/notion-sync-state.json` tell you whether the source has moved since.

## What DMBA 6005 shipped as

| Page | Content | Built |
| --- | --- | --- |
| `DMBA6005-week0.html` | `$RUs` digital innovation case + `Shadow Boxing` method | 7 blocks, 4 figures, 14 terms, 28 cards, 330 prose words |
| `DMBA6005-week1.html` | Intro to PM, StellarCX engagement, context analysis (partial) | 15 blocks, 5 figures, 32 terms, 53 cards, 1,043 prose words |

Both are well under the 160-words-per-block budget — the sources are thin, and padding to
budget would have broken the "do not add" rule.

## Open threads

- [ ] **DMBA 6005 Week 1 has three gaps that are gaps on purpose.** When Aryan writes them,
      **replace the honest blocks — never generate into them**:
      - `Context Analysis for $RUs` (`3b37b336873c8065bf14cfea1eb81df7`) ends **mid-word** at
        *"Their financial requir"*. The page reproduces exactly that and stops.
      - `Creating your reflective journal` (`3b37b336873c80cc83a8f80730d28817`) — empty.
      - `Shadow Boxing Week 1` (`3b37b336873c80698a11eb104e178cb1`) — empty.
      All three are block `14 / Not yet written` and block `13`'s closing note.
- [ ] **Three typos were preserved verbatim, deliberately** — they are the author's words and
      fixing them would change meaning. Worth Aryan correcting **in Notion**, then re-syncing:
      - Week 0: *"could invest in technology that **does** address its real strategic need"* —
        almost certainly missing "not", which inverts the sentence.
      - Week 1: *"two connected **question**"*, *"frustrated mainly poor visibility"* (missing
        "by"), *"the selected approach **is build** through short Agile iterations"*.
- [ ] **No page has been checked at narrow width**, and the flashcard flip has not been tried
      on a real touch device. Aryan found the last layout bug by looking after every gate
      passed. The five 6005/library/index pages were opened in a browser on 2026-08-06 but
      **Aryan has not yet confirmed them**.
- [ ] **DMBA 6008 Week 0 → "Assessing Financial Performance" is still empty in Notion.**
      Re-checked 2026-08-05. `DMBA6008-week0.html` renders an honest "not yet written" panel
      listing the ten pending sub-pages — **that panel is the thing to replace**.
- [ ] Optional, only if Aryan raises it: DMBA 6008 week 0 still reads long at 31 blocks even
      at budget. The lever is **structural, not verbal** — merge Goodwill into Intangibles and
      fold Asset quality into blocks 05/06, ~31 blocks → ~24. Costs no content. Ask first.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask first, it rewrites tracked state.
- [ ] Content pages (e.g. `DMBA6001-*.html`) still have no "back to library" link; the
      `DMBA6008-*` and `DMBA6005-*` pages do. Retrofit the old ones when next editing them.
      See [docs/conventions.md](docs/conventions.md#navigation).
- [ ] DMBA 6004's full subject title is unresolved — Notion says "Digital Collaboration, Work
      and Organisation", the repo uses a short topic label. **Ask before reconciling.** Same
      mismatch for DMBA 6002.

## Do not

- **Do not publish `Live Session` or `Assessment` notes.** Only `Pre-Live Session`. GitHub
  Pages makes everything public. DMBA 6005's `Class Diary`
  (`3b17b336873c800e9208ca98bc0a8ada`) and the DMBA 6008 Week 1 diary are both excluded and
  must stay so. See [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published).
- **Do not fill an empty Notion topic with generated content**, and **do not finish a
  truncated sentence.** DMBA 6005 Week 1 is the live example.
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since` — telemetry stays
  private (2026-08-05).
- Do not reference or commit a Notion image; **images are skipped** (2026-08-05). DMBA 6005
  had none in either week.
- Do not re-ask whether to un-mute DMBA 6005 or whether the StellarCX case names are real —
  both were settled 2026-08-06. The names (Chris Gold, Dirk, Ivy, Andrew, Jeremy, Annie,
  Murray) are **fictional** simulation characters.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not add a build step, npm dependency, or generator in the deploy path.
  (`reference/checks.py` is a verification tool — nothing at serve time calls it.)
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not restyle existing pages wholesale; each page owns its visual identity.
- Do not regenerate the semester-1 subjects (`DMBA6001`, `DMBA6002`, `DMBA6004`).
- **Do not commit or push unless asked.**

## Notes for the next session

- **The pipeline hinges on the Notes `Type` field.** Everything else is plumbing.
- **Walk the Course's `Notes` relation, not just the notebooks.** DMBA 6005's `Shadow Boxing`
  note (`3ae7b336873c803ab350c8e418970044`) is `Pre-Live Session` with **no `Notebook`
  relation** — a notebook-only walk misses it entirely. It is published under Week 0 by
  Aryan's direction. This is new as of 2026-08-06 and is a general lesson.
- **Detect content shape at runtime, never trust the config.** DMBA 6005 proves one subject
  can use both: Week 0 inline, Week 1 container. `subjects.json` `contentShapeHint` says
  `inline` and is wrong for Week 1 — it is a hint, nothing more.
- **`checks.py`'s SVG gate counts raw whitespace inside `<text>`.** Wrapping a label across
  source lines inflates its measured width and trips gate 3 as a false positive. Keep each
  `<text>` on one source line; SVG collapses the whitespace on render anyway. This cost two
  spurious findings on 2026-08-06.
- **A child page has no `Edited Time`** — only a Notes database row does. Change detection
  leans on the `as of` stamp in the fetch envelope plus a content hash. Rationale in
  [docs/notion-sync-automation.md §3](docs/notion-sync-automation.md#3-change-detection).
- `contentHash` in `docs/notion-sync-state.json` is sha256 of the harvested Markdown, first
  12 hex chars, computed **after** stripping the skill's own `<!-- -->` annotations.
- `notion-query-data-sources` is **metered**; `notion-fetch` on a relation URL is not. The
  whole 2026-08-06 sync used fetches only — no metered queries.
- MCP tools are **deferred** — load schemas via `ToolSearch` (`select:<exact_tool_name>`).
- Before choosing fonts for any future subject, inventory what is taken (fifteen now are):
  `grep -rhoE 'family=[A-Za-z+]+' --include='*.html' .`
- ⚠️ **The `SessionStart` hook did not fire on 2026-08-05 or 2026-08-06** — this file was not
  in context either time and had to be read manually. The script is fine and
  `.claude/settings.json` is wired correctly, so the likely cause is the project hook not
  being trusted/loaded. **If this note is not at the top of your context, read it yourself
  and tell Aryan to open `/hooks` once.** Two sessions running is no longer a fluke.
