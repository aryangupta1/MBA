# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-14
**Left by:** DMBA 6008 Week 0's fourth topic — **Assessing Financial Performance** — is
written and published, so no week on the site carries a "not yet written" panel any more.
Both subjects also gained two new reference tabs, **Acronyms** and **Formulas**.
Aryan asked for all of it in one go and went to bed, so it is **committed and pushed**.

---

## Current focus

**Nothing in flight.** Both subjects match Notion as of 2026-08-14.

## The thing worth knowing from this session

**Week 0's fourth topic is the case that justifies the deep pass, and it nearly slipped
through.** When Aryan wrote those 5,090 words, the Notes row's `Edited Time` **did not
move** — it still reads `2026-07-24T07:23:49.527Z`. Only the grandchild page's `observedAt`
did. A run trusting `Edited Time` alone would have reported Week 0 unchanged.

The topic was also **restructured, not just filled**: ten blank sub-pages (including
`Sustainable Growth Part 1`, `Part 2` and `Summary`) became **eight written ones**. Tree
shape is a change signal for exactly this reason. Recorded in
[docs/notion-sync.md §7](docs/notion-sync.md#7-current-state).

## The two new tabs

Acronyms and Formulas sit after the deck on each week page. They are **derived from the
assembled page, not harvested from Notion** — from the summary blocks, `TERMS` and `CARDS` —
which means they can only ever contain material that already passed gate 1. Rules are in
[docs/notion-sync.md §3b](docs/notion-sync.md) and `SKILL.md` Phase 3b.

**Neither adds a component.** Both render `.term` cards through one shared `buildRef()`
helper with the same `.toolbar` / `.search` / `.count` filtering as Key concepts. The only
new CSS is `.term-abbr` (mono, bold, `--accent-deep`) and `.term-long`. No new tokens.

**A tab is emitted only if its array is non-empty**, the same rule the Discussion tab
follows. What each week ended up with:

| Page | Acronyms | Formulas |
| --- | --- | --- |
| `DMBA6008-week0` | 23 | **82** |
| `DMBA6008-week1` | 6 | 23 |
| `DMBA6008-week2` | 7 | 16 |
| `DMBA6005-week0` | 1 | **none — no tab** |
| `DMBA6005-week1` | 5 | **none — no tab** |
| `DMBA6005-week2` | 8 | 9 |

`week-shell.html` carries `<!--INSERT:ACRONYMS_TAB-->` / `_PANEL` / `_DATA` and the same
three for `FORMULAS`, so the next sync inherits all of it.

## Do first

1. **Aryan has seen none of this.** It was built and pushed while he slept. The reference
   tabs in particular are new UI he has not looked at.
2. **Two judgement calls to put to him**, both easy to reverse:
   - **`DMBA6005-week0` has an Acronyms tab holding exactly one entry** (CEO). It is
     truthful — that week genuinely uses one abbreviation — but a one-card tab may read as
     broken. Ask whether he wants a minimum threshold.
   - **`DMBA6005-week0` and `-week1` have no Formulas tab at all**, because those weeks
     state no formulas. That is content-driven and deliberate, but it makes the tab row
     differ between weeks of the same subject.
3. **The DuPont images question is still open, and it just got bigger.** Week 0's new topic
   skipped **4 more images**, and two of them (in `Risks` and `Cash`) almost certainly carry
   formula definitions — the prose says *"A useful performance ratio is:"* and then an
   image. Together with Week 2's `DuPont model example`, that is **6 skipped images with
   real content loss**. Ask whether to download and commit them.

## A hard rule with a carve-out — read before any sync

Rule 1 is "never publish a `Live Session` note". Aryan directed on 2026-08-10 that DMBA
6008's live-session **`Discussion Questions` sub-page** be published from **Week 2 onwards**.
It is a *narrow* carve-out: take that child page and **nothing else**. Lecturer remarks,
classmates' AI use, what will be examined, notes-to-self — still never published. Full detail
in [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published).

The Discussion tab is also **the only place on the site where "do not add" is suspended**.
Two guardrails are load-bearing: **no financial statistic about any real company**, and **a
provenance note heading the panel**.

## Author quirks reproduced verbatim — do not "fix" these

- **The same concept is now stated two ways across the subject, and both are correct.**
  Week 0 gives `SGR = ROE x Retention Rate`; Week 2 gives `SGR is driven by Return on
  Assets, Leverage and Retention` and never writes the product form. **Do not reconcile
  them.** Each page reproduces the algebra of the notes it was built from.
- **Lowercase `x` is his multiplication sign** in Week 0 — `ROA = Asset Utilisation x Profit
  Margin`, `ROE = ROA x Financial Leverage`, `SGR = 50%x50% = 25%`. He uses `÷` elsewhere in
  the same topic (`Debt ÷ Assets`). Both were verified character-exact by gate 1. Never
  normalise one to the other.
- New Week 0 typos, all deliberate: `originate primary from`; `simple because it has`;
  `Debt must be services`; `profit fails` / `profits failing` / `A failing interest cover`
  (he means *falling*); `failing asset utilisation`; `a good analyst therefore sues ratios`;
  `additional business or financial riskl`; `Earnings may be more less predictable`;
  `Has new equity been issues?`; `highlights investing whether deterioration`. The sub-page
  title `Sustainable Growth Part` is genuinely cut short — **do not complete it**.
- **Week 0 states its funding gap as 103 days in `Working Capital Assessment` and 102 days
  in the `Cash Flow` topic's operating-cash-cycle case.** They may be different examples or
  it may be a slip, but it is his either way and both are reproduced as written. Worth
  mentioning to him; **do not silently reconcile them.**
- Still standing from earlier syncs: `absorb sustainable cash`; `Volume x Margin` vs
  `Volume + Margin`; `…beyond the mechanics of Scru,`; `Sponsor buy-in is built before
  funding formal decisions`; the sprint-length hedge; `Their financial requir`; and **no
  dates anywhere in the Agile material**.

## Still empty, still an honest placeholder — do not fill

- **DMBA 6005 W1 → `Creating your reflective journal`.** Still `<empty-block/>`. This is now
  the **only** one left, and therefore the live example the docs point at.

## What changed on the mobile layout

`.tablist` is a flex row with `overflow-x: auto` **and a hidden scrollbar**, so tabs past the
viewport were unreachable with no affordance. At 390 px the row needs ~945 px for six tabs
against ~351 px available. A new `@media (max-width: 700px)` block wraps the row, trims
`.tab` padding and font, and hides the decorative `.tab-num`; six tabs then wrap to three
reachable rows. **The overflow itself pre-dated these tabs** — three tabs already needed
~508 px — so this fixed a latent bug rather than one I introduced. Documented in
[docs/design-system.md](docs/design-system.md).

## Verification actually performed

- `checks.py` on all six week pages — **0 findings** (gates 2, 3, 5, 6).
- **Gate 1 (fidelity)**, adversarial and context-starved, over the new Week 0 topic: **no
  blocking defects.** All 24 formulas character-exact, all 18 numbers traced, all three
  worked examples stop where the source stops, no real company or statistic anywhere. It
  found three wording departures, **all three fixed**: `The source particularly highlights`
  had been reworded to `The notes particularly highlight`; a comma splice had been tidied to
  a semicolon; and a flashcard said `profits fell` where he wrote `profits failing`.
- **Gate 4 (privacy)**: the harvester swept all eight sub-pages and found **no classroom-diary
  material** — no lecturer remarks, no comments about other students, no exam hints.
- Browser: both new tabs on 6008 W1, 6005 W0 and W2; Week 0's rebuilt subpanel; the hub
  card; `library.html?subject=DMBA6008` with all 10 links returning 200; zero console
  errors; zero horizontal page overflow.

## Open threads

- [ ] **`checks.py` does not measure the new panels.** It reports the `summary` topic only,
      so neither Discussion nor the two reference tabs are covered by the prose gate. Worth
      teaching it about `#panel-discussion`, `#panel-acronyms` and `#panel-formulas`.
- [ ] **A `desc` on Week 2's Discussion tab states the sustainable growth relation in the
      textbook `ROE × retention` form**, in `dqb5-desc`. Left alone deliberately: the
      Discussion tab is licensed to use outside knowledge, and Week 0 turns out to state
      that same form in his own notes. Flagging it only so nobody "discovers" it later and
      assumes it is a defect.
- [ ] **The inline SVG figures still hard-code their fills** — the one real cleanup left.
      See [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved. **Ask before reconciling.** Same for 6002.

## Do not

- **Do not publish anything from a `Live Session` note except DMBA 6008's
  `Discussion Questions` child page, Week 2 onwards.**
- **Do not relax "do not add" outside the Discussion tab.** The Acronyms and Formulas tabs
  are *extraction*, not authorship — a formula is copied character for character, and an
  acronym never gets an invented definition.
- **Do not reconcile Week 0's and Week 2's statements of sustainable growth.**
- **Do not put a financial statistic about a real company anywhere in the Discussion tab.**
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later** —
  `syncRules` → `no-shadow-boxing-after-week-0`, binding on both discovery flows.
- **Do not trust a "this is empty" note without re-checking it.** 6005's `New Notebook`
  became `Week 2: Agile`; 6008 Week 0's fourth topic was empty for three weeks and then
  wasn't. Emptiness is a fact about the day you looked.
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**; **do not
  touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed` or the
  `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names.**
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking — see "Do first" #3.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.** (This session was asked.)

## Notes for the next session

- **A new tab needs no JS change.** The inline script maps `data-panel` → `panel-<value>`
  generically and its arrow keys walk whatever `.tab` elements exist. The reference tabs
  needed only data plus `buildRef()`.
- **The summary index is generated at runtime** from the `.block` elements already on the
  page — do not hand-author a contents list. Week 0's new subpanel inherited it for free and
  opens collapsed, because it is over the 12-section threshold.
- **`data-topic` is authored, but sub-tabbed weeks do not use it.** DMBA 6008 Week 0 drives
  its four topics from authored `.subtabs` + `.subpanel`s, so its blocks carry no
  `data-topic` — the new ones correctly do not either. Flat weeks do need it.
- **Terms may repeat within a topic when the `src` differs.** Week 0's new topic defines
  `Return on Equity (ROE)`, `Financial Leverage`, `Financial Risk`, `Business Risk` and
  `Working Capital` twice, from different sub-pages, with genuinely different framings. The
  rendered card shows `src`, so they are disambiguated, and the panel intro says so. This is
  the first time it happens *within* one topic rather than across topics.
- **Cards are stored in topic order and terms carry a `src`.** That asymmetry is what makes
  surgical per-topic splices possible.
- **`library.html`'s `articlesBySubject` is the site's only registry.**
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`. Note that `resize_window` did **not**
  change the viewport in this session, so narrow-width checks had to be done by measuring
  intrinsic widths in JS rather than by screenshotting a phone-sized window.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not. This sync used fetches only.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS can block all access to `~/Documents`** via TCC. If the repo suddenly reads as
  missing, check System Settings → Privacy & Security → Full Disk Access before assuming
  anything is wrong with the files.
- ⚠️ **The `SessionStart` hook still has not fired since 2026-08-05.** If this note is not at
  the top of your context, read it yourself and tell Aryan to open `/hooks` once.
