# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-10
**Left by:** a full sync of both Semester 2 subjects. **Two new Week 2 pages** published and
**DMBA 6005 Week 1 rebuilt** now that its Context Analysis topic is finished. Committed and
pushed to `master`.

---

## Current focus

**Nothing in flight.** Both subjects are synced to Notion as of 2026-08-10. The next sync is
triggered by Aryan — he says *"update finance"* or *"update agile"*.

## Do first — read these two, they are the live decisions

1. **DMBA 6008 Week 2 has a real content hole caused by the images policy.** The topic
   `DuPont model example` is titled "example" but its entire worked example — every number,
   and the algebraic decomposition — lives in **two Notion images**, and images are never
   published (they are 5-minute presigned S3 URLs). The published topic is therefore
   **qualitative only, with no numbers at all**. That is correct under the policy but it is a
   genuine loss. **Ask Aryan whether he wants those two images downloaded and committed** so
   the worked example can exist. This is the single most useful question to put to him.
2. **`Shadow Boxing Week 1` was renamed and may now have content.** It is now
   `Shadow Boxing: Cost, Scope or Schedule?` (`3b37b336873c80698a11eb104e178cb1`). It was
   **not harvested and not read** — `syncRules` excludes it before shape detection, by his
   2026-08-10 instruction. So nobody knows whether he has since written it. If he asks "where
   is my Shadow Boxing week 1 content", the answer is: excluded on purpose, and reversing that
   is a one-line change to `subjects.json`.

## What this sync published

| Page | Content | Built |
| --- | --- | --- |
| `DMBA6008-week2.html` **new** | Assets reflect the business model · Drivers of returns · DuPont model example | 23 blocks, 9 figures, 53 terms, 80 cards |
| `DMBA6005-week2.html` **new** | Delivering a valuable customer experience · Agile History and Scrum Roles · Bidding and winning projects | 28 blocks, 12 figures, 60 terms, 84 cards |
| `DMBA6005-week1.html` rebuilt | Context Analysis for $RUs went from a truncated stub to ten full blocks | 24 blocks, 8 figures, 51 terms, 76 cards |

Unchanged and deliberately not rebuilt: DMBA 6008 Weeks 0 and 1, DMBA 6005 Week 0. Their
notes and every `observedAt` were byte-identical to the state record.

**Two stale rules were found and corrected — both would have silently dropped content:**

- `subjects.json` told every run to skip notebook `3b37b336873c80db9388ee1a56192b33` as "an
  empty placeholder called New Notebook". Aryan **renamed it `Week 2: Agile` on 2026-08-08
  and filled it.** The skip rule is gone, and `SKILL.md` now says to re-check skipped
  notebooks every run. **A notebook being empty is a fact about the day you looked.**
- The `no-shadow-boxing-after-week-0` rule did its job on its first real run: it excluded the
  renamed Week 1 note *and* a `Shadow Boxing` sub-page inside the new Week 2 note. Both
  discovery flows were needed.

## What was deliberately left out — Aryan cannot see these from the pages

- **`Sustainable Growth`** (DMBA 6008 Week 2) is **empty in Notion**. The page carries an
  honest "not yet written" block. **That block is the thing to replace. Never fill it.**
- **`Creating your reflective journal`** (DMBA 6005 Week 1) is still empty. Same treatment.
- **4 Notion images skipped** — 1 in `Assets reflect the business model`, 1 in
  `Drivers of returns`, **2 in `DuPont model example`** (see "Do first" #1).
- **Both Live Session diaries** excluded, as always.
- **Three legacy DMBA 6008 notes** (`The balance sheet`, `The profit and loss statement`,
  `Cash Flow`, all `30d7b336…`) sit in the **archived** Week 0 notebook and carry **no `Type`
  property at all**. Rule 1 applies — unsure of a Type means do not publish. They are also
  superseded by the current Week 0 note, and `Cash Flow` ends abruptly at a bare
  `# Free Cash Flow (FCF)` heading.

## Author quirks reproduced verbatim — do not "fix" these

Each was checked and deliberately preserved, because changing them changes meaning:

- **`absorb sustainable cash`** (6008 W2, drivers) — almost certainly meant *unsustainable*.
- **`Volume x Margin`** in a heading vs **`Volume + Margin`** in a table, same topic, not
  harmonised.
- **`…beyond the mechanics of Scru,`** (6005 W2, agile) — the source's final takeaway ends
  mid-word with a stray comma. Completing it to "Scrum" is forbidden.
- **`Sponsor buy-in is built before funding formal decisions`** (6005 W2, bidding) — garbled,
  apparently missing a word. Not repaired by guessing.
- Sprint length stays hedged as **"commonly framed in the course as around two weeks"**.
- The Agile source contains **no dates at all** — no year, no Snowbird, no signatories. None
  were added, and none may be.

Worth Aryan correcting **in Notion**, then re-syncing — plus the older ones still open:
*"two connected question"*, *"frustrated mainly poor visibility"* (missing "by"), *"the
selected approach is build through short Agile iterations"*, and Week 0's *"could invest in
technology that does address its real strategic need"* (probably missing "not", which inverts
the sentence).

## Open threads

- [ ] **Aryan has seen none of this.** Everything was verified headlessly. He has not looked
      at the two new pages, and the flashcards have never been tried on a real touch device.
- [ ] **The adversarial fidelity pass caught four "do not add" violations**, all fixed before
      publication: an invented common-size formula standing in for a skipped image, an
      invented causal feedback loop in a figure, CX levels asserted as *nesting* when the
      source only gives a sequence, and a fabricated clause in a glossary definition. **Gate 1
      is earning its keep — keep running it context-starved.**
- [ ] **The inline SVG figures still hard-code their fills.** Migrating them to `var(--…)`
      remains the one real cleanup — see [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] **`checks.py` has still not been updated for the DESK markup.** It passes clean on all
      six week pages, so this is not urgent, but its SVG and inline-layout gates were written
      against the old shell.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask first, it rewrites tracked state.
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved — Notion says "Digital Collaboration, Work
      and Organisation", the repo uses a short topic label. **Ask before reconciling.** Same
      mismatch for DMBA 6002.
- [ ] The ten new Week 1 context blocks are indented 12 spaces where the file uses 6. Purely
      cosmetic; tidy it if you are editing that region anyway.

## Do not

- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later.** Aryan's rule,
  2026-08-10 — `subjects.json` → `syncRules` → `no-shadow-boxing-after-week-0`, documented in
  [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published) and `SKILL.md`
  Phase 0 §3/§3a. It binds **both** discovery flows. Week 0's method note stays published. An
  excluded note is **out of scope, not pending** — no placeholder, no topic chip, no terms or
  cards. It scopes to notes *titled* `Shadow Boxing`; the Week 1 prose describing the
  simulation came from `Your project with StellarCX` and stays.
- **Do not trust a "skip this notebook" note without re-checking it.** See above.
- **Do not restyle a DESK page ad hoc.** Copy the profile's `<style>` block and change only
  the four `--accent*` values. Read [docs/design-system.md](docs/design-system.md).
- **Do not add `overflow: hidden` to `.win`.** It silently kills the sticky title bar and tab
  strip. Corners are rounded on the first and last children instead.
- **Do not touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed`, or the
  `.tab` / `.panel` / `.term` / `.flip` / `.face-*` class names.** The inline script has no
  null guards and `aria-pressed` on `#flip-card` is the only source of truth for the flip.
- **Do not publish `Live Session` or `Assessment` notes.** Only `Pre-Live Session`.
- **Do not fill an empty Notion topic with generated content**, and **do not finish a
  truncated sentence or a truncated word.**
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not reference or commit a Notion image without asking — see "Do first" #1.
- Do not re-ask whether the StellarCX case names are real: Chris Gold, Dirk, Ivy, Andrew,
  Jeremy, Annie and Murray are **fictional** simulation characters (settled 2026-08-06).
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not add a build step, npm dependency, or generator in the deploy path.
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice on
  their library lists unless they are actually converted.
- **Do not commit or push unless asked.**

## Notes for the next session

- **The `syncRules` mechanism is new and worked.** It lives in `subjects.json` per subject and
  is enforced in Phase 0 before shape detection. Add future exclusions there, not in prose.
- **Cards are stored in topic order**, which is what made the Week 1 surgical splice possible:
  the Context Analysis cards were the last five, and its terms were the three tagged
  `src: 'Context Analysis'`. Terms carry a `src`; cards do not. If a future splice needs to be
  surgical, that asymmetry is the thing to work around.
- **`library.html`'s `articlesBySubject` object is the site's only registry.** It survived the
  design overhaul byte-for-byte and both new pages were added to it this run.
- **Serve the site to look at it** — the Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`, then `http://127.0.0.1:8787/…`. Remember
  `scroll-behavior: smooth` is on: screenshot immediately after a `scrollTo` and you will
  capture the page mid-flight and think you found a bug.
- **The pipeline hinges on the Notes `Type` field.** Everything else is plumbing.
- **Walk the Course's `Notes` relation, not just the notebooks.** Both flows are now numbered
  steps in `SKILL.md` (Phase 0 §3 and §3a).
- **Detect content shape at runtime, never trust `contentShapeHint`.**
- `contentHash` is sha256 of the harvested Markdown, first 12 hex chars, after stripping the
  skill's own `<!-- -->` annotations. Every topic published this run carries a real hash.
- `notion-query-data-sources` is **metered**; `notion-fetch` on a relation URL is not. This
  entire two-subject sync used fetches only — zero metered queries.
- MCP tools are **deferred** — load schemas via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **The `SessionStart` hook has not fired on any session since 2026-08-05** — this file has
  had to be read manually every time. The script is fine and `.claude/settings.json` is wired
  correctly. **If this note is not at the top of your context, read it yourself and tell Aryan
  to open `/hooks` once.**
