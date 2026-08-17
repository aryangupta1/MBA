# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-17
**Left by:** A sync. Aryan said *"Resync, commit and push"* without naming a subject, so both
were diffed. **DMBA 6008 Week 3 — Investment Evaluation Tools — is new and published**, and
**DMBA 6005 Week 3 was rebuilt** because its two empty sub-pages had been written. Everything
else in both subjects was unchanged and nothing else was rebuilt. **Committed and pushed**,
as asked.

---

## Read this first — the hook did not fire

**`next-prompt.md` was NOT injected into this session's context.** It had to be opened by
hand. The 2026-08-15 fix to `settings.json` is present and correct — the command is
`bash "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/hooks/load-next-prompt.sh"`, the script exists and
is executable — so the remaining explanation is the one the last session named: **a
project-scope hook awaiting Aryan's approval, which cannot be granted from inside a session.**

**Ask him to open `/hooks` once and approve it.** Until then, every session must open this
file by hand, and a session that forgets will silently ignore a binding handoff.

## Current focus

**Nothing in flight.** Both subjects match Notion as of 2026-08-17.

## What is new

### DMBA 6008 Week 3 — `DMBA6008-week3.html`, new

15 blocks, 5 figures, 30 terms, 40 cards, 5 acronyms, 8 formulas. Two written topics and
**two empty ones**:

| Week 3 sub-page | State |
| --- | --- |
| Concept of present value | published, ~355 words |
| Investment Appraisal | published, ~894 words |
| Internal rate of return | **empty** — honest "not yet written" block |
| Problems with common approaches | **empty** — honest "not yet written" block |

It is a **thin week by design** — about 1,250 words of source across two topics. The prose
was scaled down to match rather than padded, so its blocks run well under budget. That is
correct, not a defect.

**No Discussion tab.** Week 3's notebook has no Live note yet, so the page has five tabs.
The moment one appears, the Week 2 carve-out applies to its `Discussion Questions` child
**and nothing else**.

### DMBA 6005 Week 3 — `DMBA6005-week3.html`, rebuilt

Was 20 blocks / 8 figures / 37 terms / 50 cards. Now **36 blocks, 15 figures, 73 terms,
98 cards, 5 acronyms, 27 formulas**. Both placeholder blocks are gone:

| Week 3 sub-page | State |
| --- | --- |
| Personas | **written 2026-08-15**, ~1,425 words → blocks 19–27 |
| Long-term strategic value for `$RUs` | **written 2026-08-15**, ~1,476 words → blocks 28–36 |

The two already-published topics, `Ideation and design thinking` and `Why we prototype`,
were **not** re-harvested or regenerated — their `observedAt` predates the 08-15 publish, so
their reviewed prose was left exactly as it was and the new fragments were spliced in where
the placeholders stood. Do the same next time: replacing a placeholder is a splice, not a
rebuild.

## Do first

1. **Aryan has seen none of this.** Built and pushed on his instruction, without review.
2. **Two things to put to him:**
   - **The `$RUs` case now has real strategic content on the site.** `Long-term strategic
     value` is nine blocks of his own strategy argument. Worth him reading before anyone
     else does.
   - **Ask about the mistyped note.** See below.
3. **The skipped-images question is now materially worse and needs a decision** — see below.

## The images question has stopped being cosmetic

**6 more images were skipped, and this time they carry the algebra.** In DMBA 6008 Week 3:

| Topic | Skipped | What was in them |
| --- | --- | --- |
| Concept of present value | 2 | the **symbolic present-value formula** and its worked example |
| Investment Appraisal | 4 | the **Average ROA calculation**, a straight-line depreciation illustration, and two on **Excel's `NPV()`** behaviour |

The prose introduces every one of these and then does not state it. **This is the highest-risk
shape in the whole pipeline**, because any model building the page already knows all of these
formulas from training and supplying one would look exactly like transcription. Both builders
were told not to; both figcaptions say in words that the formula sits in an image and is not
reproduced; the fidelity gate was aimed at it specifically — **and it still caught an ROA
definition restated in prose.** That was cut.

Running total of real content loss: **6 in 6008 Week 3, 4 in Week 0's fourth topic, 2 in
Week 2's `DuPont model example` — 12 images.** Publishing any of them means downloading and
committing the file, which needs Aryan's say-so. **Ask.**

## A note named `Live` is typed `Pre-Live Session`

`3bf7b336873c8061b545e1b5340877d7`, new in the **DMBA 6005 Week 3** notebook on 2026-08-17.
It is **empty**, so nothing was published and the mismatch cost nothing this run.

It matters the moment it has content: **rule 1 keys off `Type`, not the name.** A live-session
diary carrying `Pre-Live Session` would pass straight through the filter that exists to catch
it. **Ask Aryan whether the Type is right before publishing anything from it.** Recorded in
`docs/notion-sync-state.json` → `DMBA6005.openQuestions`.

## The defect worth re-reading — a typo repaired in four places

Aryan writes *"examining **decisions** such as: Think → Feel → Say → Do"*. `decisions` is
plainly the wrong word; he means dimensions.

The first Personas build **preserved it in the prose and silently corrected it to
"dimensions" in the SVG `<title>`, the SVG eyebrow, the figcaption and a flashcard.** Four
places, all reading as his framing, all passing every static check. Only the adversarial
fidelity gate caught it.

The fix was to **reword around the noun** rather than assert either version — "What an
empathy map examines", "WHAT THE MAP EXAMINES", "Think, Feel, Say and Do are only half of
it", and a card that quotes his line whole. **Diagram text is where this kind of drift
hides.** Same lesson as the `diamond` defect on 2026-08-15.

## Author quirks reproduced verbatim — do not "fix" these

New in **6008 Week 3**:

- **`$16.m`** — a mid-number truncation; the decimal has no digit. His own arithmetic on the
  same line, `(33+0)/2`, would give 16.5. It appears in the summary, a term and a card.
  **Never complete it.**
- `mesaure`; `economically more value` (a word is missing); `a different decisions`;
  `Both product the same NPV`.
- **His number formatting is inconsistent by section** — `$112,000` / `$101,818` /
  `$110,000` / `$100,000` with separators in the discounting and benchmark passages,
  `$2000` / `$1818` / `$101818` / `$100000` without them in the NPV passage. Reproduced
  section by section, including inside one figure that shows both styles in its two columns.
  **Never normalise.**
- **WACC and CF0 are used and never expanded.** The Acronyms tab gives them the standard
  expansion and its intro says so.
- Six H1 headings carry no body text of their own.

New in **6005 Week 3**:

- **`Type of Personas`** — singular, and **empty**: it has no body of its own. The page says
  so rather than glossing it, the same way the A–E framework is handled.
- The good-example callout has an **opening curly quote that is never closed** and no
  terminal full stop.
- **`Adviser` here, `advisor` elsewhere in the same week.** Both preserved.
- `In scrum` lowercase alongside the capitalised heading `User Stories in Scrum`.
- `one-of transaction`; `Shorty-term success`; `The project. should therefore serve:`;
  `strengthen $RUs position as:`; `Google Ads or App Or Social Media`; lowercase
  `Google ads` in the arrow chain against `Google Ads` elsewhere.
- **`customer lifecycle value` and `customer lifetime value` both appear.** Never reconcile.
- **`User→Need→Value` and `user→need→value`** differ only in spacing and case. Both survive
  as separate Formulas entries, each pointing at the other.

Still standing from earlier syncs: the A–E framework that is headings and nothing else
(**never write a gloss for one**); `SGR = ROE x Retention Rate` (6008 W0) vs `SGR is driven
by Return on Assets, Leverage and Retention` (6008 W2) — **never reconciled**; lowercase `x`
as his multiplication sign; the 103-day / 102-day funding gap; `absorb sustainable cash`;
`Volume x Margin` vs `Volume + Margin`; `…beyond the mechanics of Scru,`; `Sponsor buy-in is
built before funding formal decisions`; `Their financial requir`; `strictly liner`;
`weak thinning`; the Week 0 typo list; and **no dates anywhere in the Agile material**.

## Still empty, still honest placeholders — do not fill

- **6005 W1 → `Creating your reflective journal`** — re-checked 2026-08-17, still empty
- **6008 W3 → `Internal rate of return`**
- **6008 W3 → `Problems with common approaches`**

6005 Week 3's two are **gone** — he wrote them. Note the 6008 pair need **no cross-reference
pointer**, unlike the old `Personas` block: IRR is not covered anywhere else on that page.

## A hard rule with a carve-out — read before any sync

Rule 1 is "never publish a `Live Session` note". Aryan directed on 2026-08-10 that DMBA
6008's live-session **`Discussion Questions` sub-page** be published from **Week 2 onwards**.
It is a *narrow* carve-out: that child page and **nothing else**.

The Week 2 `Live` note still has two children — `Discussion Questions` and **`Diary`**
(`3ba7b336873c80f4addce7004f01a76e`). `Diary` was **not fetched, not harvested, not read**,
for the second consecutive run. Assume every future Live note is mixed.

Week 2's Discussion Questions child is **unchanged** (`observedAt` 2026-08-11T14:05:19.512Z),
so its tab was not touched. Week 3 has no Live note at all.

The Discussion tab remains the only place on the site where "do not add" is suspended, and
its two guardrails are load-bearing: **no financial statistic about any real company**, and
**a provenance note heading the panel**.

## Verification actually performed

- `checks.py` on **all nine** week pages plus both hubs, `index.html` and `library.html` —
  **0 findings** (gates 2, 3, 5, 6). One SVG-overflow hit was found and fixed en route
  (a `<text>` split across two source lines in 6005 W3's `ltvfig1`; each `<text>` is now on
  one line, which is also the house convention).
- **Gate 1 (fidelity)**, adversarial and context-starved, one agent per topic, four topics.
  **Three BLOCKING findings on 6008 `Investment Appraisal`, all fixed:** an invented
  Average-ROA definition restated in prose where the source has only a skipped image; a claim
  that the profit/cash gap "runs in both directions", which his own `Cash Flow = Profit +
  Depreciation` contradicts; and **a figure that fabricated an entire four-period mirrored
  cash-flow profile for two projects** the notes give no figures for — it was replaced with a
  single discount-decay panel carrying no magnitudes. **One BLOCKING finding on 6005
  `Personas`, fixed:** the `decisions`→`dimensions` repair described above.
- ~20 further NOTEs, the substantive ones fixed: a figcaption claiming the discounted surplus
  is "the same result the NPV calculation reaches" (his notes stress the two amounts are *not*
  the same); a `Economic Equivalence` term coined where he wrote only "economically
  equivalent"; invented SVG chip labels `Evidence base` / `Edge test`; a figcaption inventing
  "the first sprint"; an arrow imputing causation between "no new customer behaviour" and
  "revenue may actually fall", which his notes attribute to discounts; and four vocabulary
  leaks (`wedge`, `candidate measure`, `ties up`, `steep`).
- **Gate 4 (privacy)**: full-file sweep of both pages. Clean. No live-session material, no
  uncleared names, no telemetry, no Shadow Boxing trace on the 6005 page, no
  `only-accessible-by-url` link. Two real companies appear and both are qualitative only —
  **Excel** (software behaviour, 6008) and **Google Ads** (a channel option, 6005). No
  financial statistic about either.
- **Gate 4 also caught a self-contradiction the fidelity gates could not see:** 6005 Week 3's
  standfirst still read *"two sub-pages I have not written yet"* on a page that now has all
  four written, and its footer still said "Synced from Notion on 15 August 2026". Both fixed,
  and the `<meta name="description">` extended. **When a placeholder is filled, the hero and
  the footer are part of the edit.**
- Browser, served at `127.0.0.1:8787`: both pages — all five tabs switching, the deck
  flipping (`aria-pressed` toggles) and advancing, every topic chip filtering to the right
  block count (6005: 10 + 8 + 9 + 9 = 36), 0 duplicate ids, 0 broken `aria-labelledby`,
  every table inside a scrolling `.table-scroll`, 0 console errors, 0 horizontal overflow at
  1280 px and at 420 px, the tab row wrapping cleanly on mobile. Hub → week → back walked on
  both subjects; every relative link on both hubs returns 200; `library.html?subject=DMBA6008`
  lists all five 6008 links, all 200.

## Open threads

- [ ] **The 12 skipped images.** Now the biggest real gap on the site. See above — needs a
      yes/no from Aryan, per image or as a policy.
- [ ] **Is that `Live` note's `Type` correct?** See above.
- [ ] **`checks.py` still does not measure the new panels.** It reports the `summary` topic
      only, so Discussion, Acronyms and Formulas are outside the prose gate. Unchanged for
      three sessions; worth teaching it `#panel-discussion`, `#panel-acronyms`,
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
- **Do not trust a note's name over its `Type`, or its `Type` over its name, without asking**
  when the two disagree. See the `Live` / `Pre-Live Session` note above.
- **Do not supply a formula that exists only in a skipped image**, however certain you are of
  it. This is now the pipeline's likeliest failure mode.
- **Do not complete `$16.m`.** Do not complete any truncation.
- **Do not repair a typo inside a figure, a figcaption, an SVG `<desc>` or a flashcard while
  preserving it in the prose.** Either it is his line everywhere or it is your wording
  everywhere. Reword around it if it reads badly.
- **Do not relax "do not add" outside the Discussion tab.** Acronyms and Formulas are
  *extraction* — a formula is copied character for character, an acronym never gets an
  invented definition, and where a standard expansion is used the panel intro must say so.
- **Do not write a gloss for 6005 Week 3's A–E headings, or for its `Type of Personas`.**
- **Do not let one week's vocabulary or algebra leak into another's.**
- **Do not reconcile 6008 Week 0's and Week 2's statements of sustainable growth**, or
  6005 Week 3's `lifecycle`/`lifetime`, or its two spacings of `User→Need→Value`.
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later** —
  `syncRules` → `no-shadow-boxing-after-week-0`, binding on both discovery flows. It has now
  excluded a sub-page in three consecutive weeks; expect one every week.
- **Do not trust a "this is empty" note without re-checking it.** Emptiness is a fact about
  the day you looked — **two of the three placeholders standing on 2026-08-15 were written
  within 24 hours.**
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**; **do not
  touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed` or the
  `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names.**
- **Do not move the tab row's wrapping back inside a media query.** `flex-wrap: wrap` sits on
  `.tablist` unconditionally, by design (2026-08-15).
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.** (This session was asked.)

## Notes for the next session

- **A new week plus a rebuilt week cost two probes, six harvesters, four builders, two
  reference-tab agents and five gate agents.** That was this run and it was about right.
  Keep the fan-out to topics.
- **Probe topics, not notes, when diffing.** DMBA 6005 Week 3's note row `Edited Time` has
  now stayed frozen at 2026-08-14T14:38 through **two** rounds of sub-page writing. Only the
  envelope `observedAt` moved. A run trusting `Edited Time` would have missed 2,900 words.
- **Replacing a placeholder is a splice, not a rebuild.** Match the two placeholder blocks by
  their `data-topic-empty="true"` attribute, swap each for its topic's fragment, then
  renumber every `block-num` eyebrow in the summary panel in document order and extend
  `TERMS`/`CARDS`. Leave the already-reviewed topics untouched. The scripts that did it are
  worth re-deriving rather than hand-editing a 3,900-line page.
- **Builders number their own blocks from 01.** Renumber at assembly across the whole
  concatenation, or the page will have four block 01s.
- **After filling a placeholder, sweep the page chrome**: standfirst, `<meta description>`,
  footer sync date, hero pill counts, `term-count`, `card-total`, the hub card's counts,
  its topic chips, and `index.html`'s "N weeks". Both 6008 and 6005 now read "4 weeks" on
  `index.html` — **check which card you are editing.**
- **The reference tabs are derived from the built page, not the harvest**, and must be
  re-derived whenever the page gains a topic. 6005 Week 3 went 4→5 acronyms and 11→27
  formulas purely from the two new topics.
- **The summary index is generated at runtime** from the `.block` elements — never
  hand-author a contents list. **`data-topic` is authored**, and flat weeks need it on every
  block.
- **`library.html`'s `articlesBySubject` and `validSubjects` must be edited together.**
  (`validSubjects` already had both semester-2 codes; only `articlesBySubject` needed the
  new page.)
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`. **Chrome caches aggressively across a CSS
  edit** — append `?v=N` or you will measure the old stylesheet. Note that the Chrome
  `javascript_tool` **blocks scripts that build `key=value` strings** (it reads them as query
  data); return arrays or objects instead of concatenating with `=`.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not. This sync used fetches only.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS can block all access to `~/Documents`** via TCC. If the repo suddenly reads as
  missing, check System Settings → Privacy & Security → Full Disk Access.
