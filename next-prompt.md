# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-09
**Left by:** a complete UI overhaul. `index.html`, `library.html` and every Semester 2 page
were rebuilt on a new house design system — **DESK** — documented in
[docs/design-system.md](docs/design-system.md). **Committed and pushed to `master`**
(`90fb6da`, `92f5931`), so it is live on GitHub Pages.

---

## Current focus

**Nothing in flight.** The overhaul is finished and verified. The next sync is triggered by
Aryan, not by this file — he says *"update agile"* or *"update finance"* and the skill runs.

## Do first

1. **Read [docs/design-system.md](docs/design-system.md) before changing how any covered
   page looks.** It is now referenced from `CLAUDE.md`, `docs/README.md` and
   `docs/style-guide.md`, and it wins over the style guide for the pages it lists.
2. **The working tree is clean and `master` is pushed.** The overhaul shipped as two
   commits, which also carried the previously-uncommitted 2026-08-06 DMBA 6005 launch:
   - `90fb6da` — the design system: `docs/design-system.md` (new); `index.html`,
     `library.html`, `DMBA60xx-weeks.html` rebuilt; `DMBA60xx-week0/1.html` re-skinned with
     content and script untouched; `.claude/skills/sync-subject/*` and the docs rewired.
   - `92f5931` — the "Heritage pages" notice on the Semester 1 library lists.
   If Aryan dislikes anything, **revert or amend — do not rebuild from scratch.**

## What the overhaul shipped

Blueprint: the `creatiie.framer.website` template Aryan pointed at — its wallpaper hero, its
dock, and the way clicking a project opens a macOS window over a dimmed desktop.

| Surface | Profile |
| --- | --- |
| `index.html` | wallpaper hero → pinboard of subject windows → butter footer → dock |
| `library.html` | wallpaper hero → pinboard of article cards → dock |
| `DMBA60xx-weeks.html` | wallpaper hero → pinboard of week windows → mode rows → footer → dock |
| `DMBA60xx-weekN.html` | dimmed wallpaper → one macOS window holding the whole week → dock |

Type is **Mona Sans + Plus Jakarta Sans** everywhere. A subject's identity is now **four
`--accent*` values and nothing else** — the per-subject font pairings (Newsreader/Inter,
Sora/Karla, Syne/DM Sans) are retired. No images: the wallpaper is a CSS gradient plus an
inline SVG of hills, so Google Fonts is still the only external request.

**Navigation was rewired** (all of it verified):
- Semester 2 cards on `index.html` now go straight to the **week hub**, not `library.html`.
- Every week page's back link is now its **week hub** ("← All weeks"), consistently.
- `library.html` with no `?subject=` used to silently render **DMBA 6002**. It now renders
  an all-subjects index. That bug was behind the wrong "Browse the library" link Aryan
  spotted; that footer button is now "Back to top".
- The same dock ships on all eight pages, with `aria-current` on the current one.

**Verified:** 86 links and in-page anchors resolve · every Semester 2 page still registered
in `library.html` · zero horizontal overflow at 300 px and 390 px on all eight pages · the
flashcard flip, tab switching, sub-tabs, topic chips and term filter all still work.

## Open threads

- [ ] **Aryan has not yet eyeballed any of this** — it was verified in a headless browser at
      desktop and narrow widths, not on his machine, and never on a real touch device.
- [ ] **The Semester 1 artefact pages and `blogs/` were deliberately left alone.** They keep
      their own identities per `CLAUDE.md`, and `library.html` now says so to the reader: a
      "Heritage pages" notice heads the `DMBA6001` / `6002` / `6004` lists (opt in via
      `heritageSubjects` in `library.html`). If Aryan wants them converted, that is a new job
      and a large one (16 pages) — and it would make that notice a lie.
- [ ] **The inline SVG figures still hard-code their fills** (~40–90 hex literals per week
      page). That is why each subject kept its accent hue and why the week pages still alias
      `--petrol*` to `--accent*`. Migrating those fills to `var(--…)` would be a real
      improvement — see [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] **DMBA 6005 Week 1 has three gaps that are gaps on purpose.** When Aryan writes them,
      **replace the honest blocks — never generate into them**:
      - `Context Analysis for $RUs` (`3b37b336873c8065bf14cfea1eb81df7`) ends **mid-word** at
        *"Their financial requir"*. The page reproduces exactly that and stops.
      - `Creating your reflective journal` (`3b37b336873c80cc83a8f80730d28817`) — empty.
      - `Shadow Boxing Week 1` (`3b37b336873c80698a11eb104e178cb1`) — empty.
- [ ] **Three typos were preserved verbatim, deliberately** — they are the author's words.
      Worth Aryan correcting **in Notion**, then re-syncing:
      - Week 0: *"could invest in technology that **does** address its real strategic need"* —
        almost certainly missing "not", which inverts the sentence.
      - Week 1: *"two connected **question**"*, *"frustrated mainly poor visibility"* (missing
        "by"), *"the selected approach **is build** through short Agile iterations"*.
- [ ] **DMBA 6008 Week 0 → "Assessing Financial Performance" is still empty in Notion.**
      Re-checked 2026-08-05. The page renders an honest "not yet written" panel listing the
      ten pending sub-pages — **that panel is the thing to replace**.
- [ ] Optional, only if Aryan raises it: DMBA 6008 week 0 still reads long at 31 blocks. The
      lever is **structural, not verbal** — merge Goodwill into Intangibles and fold Asset
      quality into blocks 05/06, ~31 → ~24 blocks. Costs no content. Ask first.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask first, it rewrites tracked state.
- [ ] Semester 1 content pages still have no "back to library" link. Retrofit when next
      editing them. See [docs/conventions.md](docs/conventions.md#navigation).
- [ ] DMBA 6004's full subject title is unresolved — Notion says "Digital Collaboration, Work
      and Organisation", the repo uses a short topic label. **Ask before reconciling.** Same
      mismatch for DMBA 6002.

## Do not

- **Do not restyle a DESK page ad hoc.** Copy the profile's `<style>` block and change only
  the four `--accent*` values. A second changed token means a new design — stop and ask.
- **Do not add `overflow: hidden` to `.win`.** The window title bar and the tab strip are
  `position: sticky`; that one declaration silently kills both. Corners are rounded on the
  first and last children instead.
- **Do not touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed`, or the
  `.tab` / `.panel` / `.term` / `.flip` / `.face-*` class names.** The inline script has no
  null guards and `aria-pressed` on `#flip-card` is the only source of truth for the flip.
- **Do not restore the per-subject font pairings.** `{{FONT_HREF}}` is the house link for
  every subject now.
- **Do not publish `Live Session` or `Assessment` notes.** Only `Pre-Live Session`. DMBA
  6005's `Class Diary` (`3b17b336873c800e9208ca98bc0a8ada`) and the DMBA 6008 Week 1 diary
  are both excluded and must stay so.
- **Do not fill an empty Notion topic with generated content**, and **do not finish a
  truncated sentence.** DMBA 6005 Week 1 is the live example.
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since` — telemetry stays
  private (2026-08-05).
- Do not reference or commit a Notion image; **images are skipped** (2026-08-05).
- Do not re-ask whether to un-mute DMBA 6005 or whether the StellarCX case names are real —
  both settled 2026-08-06. The names (Chris Gold, Dirk, Ivy, Andrew, Jeremy, Annie, Murray)
  are **fictional** simulation characters.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not add a build step, npm dependency, or generator in the deploy path.
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not regenerate the semester-1 subjects (`DMBA6001`, `DMBA6002`, `DMBA6004`).
- **Do not commit or push unless asked.**

## Notes for the next session

- **`library.html`'s `articlesBySubject` object survived the rebuild byte-for-byte** — it is
  the site's only registry and was preserved deliberately. Verify that with
  `git show HEAD:library.html` before touching it again.
- **The sync pipeline now carries the design.** `reference/week-shell.html` holds the whole
  DESK stylesheet inline; the per-subject knobs are `{{ACCENT}}`, `{{ACCENT_DEEP}}`,
  `{{ACCENT_SOFT}}`, `{{ACCENT_GLOW}}` (from `subjects.json` → `palette`) and `{{HUB_PAGE}}`
  (→ `hubPage`). All five are documented in `SKILL.md` phase 4 step 2.
- **`checks.py` has not been re-run against the new markup.** Its SVG and inline-layout gates
  were written for the old shell — expect to adjust them on the next sync, and read
  [docs/notion-sync-automation.md](docs/notion-sync-automation.md) first.
- **The pipeline hinges on the Notes `Type` field.** Everything else is plumbing.
- **Walk the Course's `Notes` relation, not just the notebooks.** DMBA 6005's `Shadow Boxing`
  note (`3ae7b336873c803ab350c8e418970044`) is `Pre-Live Session` with **no `Notebook`
  relation** — a notebook-only walk misses it entirely.
- **Detect content shape at runtime, never trust the config.** `subjects.json`
  `contentShapeHint` says `inline` for 6005 and is wrong for Week 1. It is a hint, nothing more.
- **A child page has no `Edited Time`** — only a Notes database row does. Change detection
  leans on the `as of` stamp plus a content hash.
- `contentHash` in `docs/notion-sync-state.json` is sha256 of the harvested Markdown, first
  12 hex chars, computed **after** stripping the skill's own `<!-- -->` annotations.
- `notion-query-data-sources` is **metered**; `notion-fetch` on a relation URL is not.
- MCP tools are **deferred** — load schemas via `ToolSearch` (`select:<exact_tool_name>`).
- **To look at a page in the browser, serve it** — the Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1` from the repo root, then
  `http://127.0.0.1:8787/…`. Remember `scroll-behavior: smooth` is on: screenshot immediately
  after a `scrollTo` and you will capture the page mid-flight and think you found a bug.
- ⚠️ **The `SessionStart` hook did not fire on 2026-08-05, 08-06 or 08-09** — this file was not
  in context and had to be read manually each time. The script is fine and
  `.claude/settings.json` is wired correctly. **If this note is not at the top of your
  context, read it yourself and tell Aryan to open `/hooks` once.**
