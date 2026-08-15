# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-15
**Left by:** A sync. Aryan said *"New updates made, sync. Commit and push when done, im off
to sleep"* without naming a subject, so both were diffed. **DMBA 6005 Week 3 — Ideation and
Prototyping — is new and published**; everything else in both subjects was unchanged and
nothing else was rebuilt. **Committed and pushed**, as asked.

---

## Current focus

**Nothing in flight.** Both subjects match Notion as of 2026-08-15.

## What is new

`DMBA6005-week3.html` — 20 blocks, 8 figures, 37 terms, 50 cards, 4 acronyms, 11 formulas.
Two written topics and **two empty ones**:

| Week 3 sub-page | State |
| --- | --- |
| Ideation and design thinking | published, ~1,410 words |
| Why we prototype | published, ~1,330 words |
| Personas | **empty** — honest "not yet written" block |
| Long-term strategic value for `$RUs` | **empty** — honest "not yet written" block |
| Shadow Boxing | **excluded** by `syncRules`, never fetched |

## Do first

1. **Aryan has seen none of this.** Built and pushed while he slept.
2. **Three things to put to him**, all easy to reverse:
   - **The tab row now wraps at every width** (see below). It changes how every week page
     looks between ~700 px and ~968 px. He has not seen it.
   - **Week 3 publishes with half its topics empty.** That follows the Week 1 precedent and
     the alternative was withholding 2,740 words he just wrote, but it is his call.
   - **The `Personas` chip needed a pointer** to stop it contradicting the page — see below.
3. **The DuPont images question is still open and unchanged** — 6 skipped images with real
   content loss (4 in 6008 Week 0's fourth topic, 2 in Week 2's `DuPont model example`).
   Week 3 skipped none; it contains no images at all.

## The one judgement call worth re-reading

**`Personas` is both a written section and an empty sub-page in the same week.** Notion has
a `Personas` sub-page with nothing in it, while the `Ideation and design thinking` notes
cover personas properly (weak vs strong, grounded in evidence). Left bare, clicking the
dimmed `Personas` topic chip would have shown only "not yet written" on a week that
obviously does cover personas.

Its block therefore carries one extra sentence pointing at **06 / Representing users**. That
is a statement about the page, not added course content. **If Aryan writes the `Personas`
sub-page, that pointer goes away with the block.** Recorded in
[docs/notion-sync.md §7](docs/notion-sync.md#7-current-state).

## The mobile fix from 2026-08-14 was too narrow, and is now corrected

Last session made `.tablist` wrap under `@media (max-width: 700px)`. **That was a guessed
number and it left a large clipping band.** Measured on the real pages this session:

| Tabs | Row needs | Clipped below |
| --- | --- | --- |
| 6 (`DMBA6008-week2`) | ~857 px | **~968 px viewport** |
| 5 (`DMBA6005-week3`) | ~727 px | **~840 px viewport** |

So 6008 Week 2 was hiding its `Formulas` tab on any ordinary laptop window, with the
scrollbar suppressed and no affordance. `flex-wrap: wrap` now sits on `.tablist` itself,
**unconditionally** — it engages only when the row does not fit, so wide viewports are
untouched. The 700 px query survives for the cosmetic trim only (padding, font, `.tab-num`,
radius). Applied to `week-shell.html` and all seven week pages. Documented in
[docs/design-system.md](docs/design-system.md).

**Do not move wrapping back inside a media query.**

## Author quirks reproduced verbatim — do not "fix" these

New in Week 3:

- **An entire framework that is headings and nothing else.** `A - Architecture &
  Technology`, `B - Business & Experience`, `C - Change & Capability`, `D - Data & AI`,
  `E - Execution` have **no body text under any of them**. The page lists them as bare
  labels and says so. These are the most invitingly fillable blanks in either subject —
  **never write a gloss for one.**
- `strictly liner` (he means *linear*); `Teams can return to earlier to earlier stages`;
  `Bringing customers directly into workshoips`; `Which problems or solution should we
  pursue?`; `weak thinning` (he means *thinking*); `what are we chanigng`; `what should be
  prototypes.`; `evidence can improve planning` (a word is missing); and two sentences
  beginning with a lowercase `it`.
- **He spells it `advisor` and `adviser` in the same section.** Both preserved where each
  appears. Do not normalise.
- **No formula anywhere in the week** — its "formulas" tab holds arrow chains and identities,
  the same convention Week 2 set.

Still standing from earlier syncs: `SGR = ROE x Retention Rate` (6008 W0) vs `SGR is driven
by Return on Assets, Leverage and Retention` (6008 W2) — **never reconciled**; lowercase `x`
as his multiplication sign; the 103-day / 102-day funding gap; `absorb sustainable cash`;
`Volume x Margin` vs `Volume + Margin`; `…beyond the mechanics of Scru,`; `Sponsor buy-in is
built before funding formal decisions`; `Their financial requir`; the Week 0 typo list; and
**no dates anywhere in the Agile material**.

## Still empty, still honest placeholders — do not fill

- **6005 W1 → `Creating your reflective journal`**
- **6005 W3 → `Personas`**
- **6005 W3 → `Long-term strategic value for $RUs`**

Three now, where there was one. All three are `<empty-block/>` in Notion today.

## A hard rule with a carve-out — read before any sync

Rule 1 is "never publish a `Live Session` note". Aryan directed on 2026-08-10 that DMBA
6008's live-session **`Discussion Questions` sub-page** be published from **Week 2 onwards**.
It is a *narrow* carve-out: that child page and **nothing else**.

**This session was the first time the carve-out had to actually exclude something.** The
Week 2 `Live` note has gained a second child, **`Diary`**
(`3ba7b336873c80f4addce7004f01a76e`). It was **not fetched, not harvested, not read**. When
the carve-out was written the Live note had only one child, so nothing had to be cut —
assume every future Live note is mixed.

The Discussion tab remains the only place on the site where "do not add" is suspended, and
its two guardrails are load-bearing: **no financial statistic about any real company**, and
**a provenance note heading the panel**.

## Verification actually performed

- `checks.py` on **all seven** week pages — **0 findings** (gates 2, 3, 5, 6).
- **Gate 1 (fidelity)**, adversarial and context-starved, one agent per topic. **One
  BLOCKING finding, fixed:** two glossary definitions defined `Problem space` / `Solution
  space` as "the first/second **diamond**". The word *diamond* is nowhere in the Week 3
  source — it is Week 1's Double Diamond vocabulary leaking across weeks. Reworded to
  "the first of the two passes" / "the second pass", and the two `FORMULAS` entries renamed
  to match. *Diamond* now survives only in two SVG `<desc>` elements, where it describes the
  shape actually drawn, which is correct for a screen reader.
- Seven further NOTEs, six fixed: an unsourced figcaption claim that polishing "buys
  information"; an unsourced "a wrong turn costs one pass rather than a project"; invented
  "six feature slots, five of which" counts in an SVG `<desc>`; an unsourced "the same budget
  spent two ways"; `measuring commercial value` where he wrote `Measure commercial value`;
  and a term that had quietly repaired one of the protected lowercase-`it` sentences with an
  em dash. One NOTE left alone deliberately: `Prototype fidelity`'s definition now quotes his
  heading and his `low-fidelity` wording rather than glossing the concept.
- **Gate 4 (privacy)**: full-file sweep. No classroom-diary material, no real names, no
  telemetry fields, no Shadow Boxing content, no `only-accessible-by-url` link.
- Browser, served at `127.0.0.1:8787`: all five tabs, the deck flipping and advancing, all
  three filters, every topic chip, the wrapped tab row on both a 5-tab and a 6-tab page,
  hub → week → back, `library.html?subject=DMBA6005` with all 5 links returning 200, zero
  console errors, zero horizontal overflow.

## Open threads

- [ ] **`checks.py` still does not measure the new panels.** It reports the `summary` topic
      only, so Discussion, Acronyms and Formulas are outside the prose gate. Unchanged from
      last session; worth teaching it `#panel-discussion`, `#panel-acronyms`,
      `#panel-formulas`.
- [ ] **A `desc` on 6008 Week 2's Discussion tab states sustainable growth in the textbook
      `ROE × retention` form**, in `dqb5-desc`. Left alone deliberately — flagged only so
      nobody "discovers" it later.
- [ ] **The inline SVG figures still hard-code their fills** — the one real cleanup left.
      See [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved. **Ask before reconciling.** Same for 6002.

## Do not

- **Do not publish anything from a `Live Session` note except DMBA 6008's
  `Discussion Questions` child page, Week 2 onwards.** The `Diary` sibling is not covered.
- **Do not relax "do not add" outside the Discussion tab.** Acronyms and Formulas are
  *extraction* — a formula is copied character for character, an acronym never gets an
  invented definition, and where a standard expansion is used the panel intro must say so.
- **Do not write a gloss for any of Week 3's A–E headings.**
- **Do not let one week's vocabulary or algebra leak into another's** — the `diamond` defect
  above is the live example, and it passed every static check.
- **Do not reconcile 6008 Week 0's and Week 2's statements of sustainable growth.**
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later** —
  `syncRules` → `no-shadow-boxing-after-week-0`, binding on both discovery flows. It has now
  excluded a sub-page in three consecutive weeks; expect one every week.
- **Do not trust a "this is empty" note without re-checking it.** Emptiness is a fact about
  the day you looked.
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**; **do not
  touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed` or the
  `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names.**
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.** (This session was asked.)

## Notes for the next session

- **A new week costs two harvesters, two builders, one reference-tab agent and three gate
  agents.** That was this run, and it was the right size. Keep the fan-out to topics.
- **Probe topics, not notes, when diffing.** The note row's `Edited Time` lies: Week 3's
  reads 14:38 on 08-14, two minutes after creation, while the sub-pages were written later —
  only the envelope `observedAt` moved. Same shape as 6008 Week 0's fourth topic. A cheap
  probe agent that fetches every topic and returns *only* `observedAt` + word count + child
  list is enough, and it keeps the prose out of the orchestrator's context.
- **The empty-topic block is per topic, not per week.** Two empty topics need two blocks, or
  only one chip gets dimmed.
- **The summary index is generated at runtime** from the `.block` elements — never
  hand-author a contents list.
- **`data-topic` is authored**, and flat weeks need it on every block.
- **`library.html`'s `articlesBySubject` and `validSubjects` must be edited together.**
- Hub per-week counts and `index.html`'s "N weeks" are hand-written and are the easiest
  thing to leave stale. Note `index.html` has **two** cards reading "3 weeks" — 6008's is
  correct and must not be swept up in an edit to 6005's.
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`. **Chrome caches aggressively across a CSS
  edit** — append `?v=N` or you will measure the old stylesheet and think your fix failed.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not. This sync used fetches only.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS can block all access to `~/Documents`** via TCC. If the repo suddenly reads as
  missing, check System Settings → Privacy & Security → Full Disk Access.
- ✅ **The `SessionStart` hook was diagnosed and fixed on 2026-08-15.** It had been dead
  since 08-05 because `settings.json` invoked the script through `$CLAUDE_PROJECT_DIR`,
  which is not always exported — unset, the path became `/.claude/hooks/…` and bash exited
  **127 before running a line**. The script was always fine, which is why testing it by hand
  never reproduced the fault. Both ends are now defensive.

  **If you are reading this file because it appeared in your context automatically, the fix
  worked and nothing more is needed.** If you had to open it by hand, the hook is still not
  being invoked — ask Aryan to open `/hooks` once, since a project-scope hook may be awaiting
  his approval and that cannot be done from inside a session.

  **The fix could not be verified end-to-end from inside the session that made it**: the
  harness gates execution of scripts under `.claude/hooks/`, so running the hook by hand hung
  every time. The reasoning and the reproduction are in
  [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md); this session is the test.
