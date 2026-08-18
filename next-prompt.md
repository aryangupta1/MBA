# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-18
**Left by:** A sync, then two rulings from Aryan. **DMBA 6008 Week 3's last two placeholders
are written and published** — the page roughly doubled. **DMBA 6005 was byte-stable and
nothing was rebuilt.** Aryan then ruled on the two questions the sync raised: **the
lecturer's details never appear on a page**, and **`Pre-Class Prep` is excluded outright**.
Both are now enforceable rules, not notes. **Committed and pushed**, as asked.

---

## Read this first — the hook did not fire

**`next-prompt.md` was NOT injected into this session's context**, for the fourth session
running. `settings.json` is correct and the script exists and is executable, so the
remaining explanation is a **project-scope hook awaiting Aryan's approval, which cannot be
granted from inside a session.**

**Ask him to open `/hooks` once and approve it.**

## Do first

1. **The one thing still outstanding: the DMBA 6005 `Live` note.** It is named `Live`,
   typed `Pre-Live Session`, and it now has content that reads as a classroom diary. See
   below. Nothing was fetched beneath it and nothing was published, but **rule 1 keys off
   `Type`**, so it would sail through the filter that exists to catch it. **It still needs an
   answer from him.**
2. **The lecturer's name is off the site, and the residue is in git history only.** It was a
   hero pill on `DMBA6008-weeks.html`, from Notion's `Courses.Professor` column, live since
   commit `7a63ab5` — the very first sync. Removed from the working tree on 2026-08-18, and
   the field is now on the never-publish list, so it cannot come back. **It is still in git
   history**, in `7a63ab5` and every commit up to its removal. Scrubbing that would mean
   rewriting history and force-pushing; **not done, and he has not asked.** Raise it once.
3. Aryan has seen none of this week's content. Built and published on his instruction,
   without review.

## What changed — DMBA 6008 Week 3 only

Both remaining placeholders were written in Notion on 2026-08-17 and are now published.

| | before | now |
| --- | --- | --- |
| summary blocks | 15 | **25** |
| figures | 5 | **11** |
| key terms | 30 | **66** |
| flashcards | 40 | **96** |
| acronyms / formulas | 5 / 8 | **7 / 13** |
| quiz / scenarios | 15 / 4 | **26 / 7** |

- **`Internal rate of return`** — 549 words, 5 blocks, **0 images**. IRR as the rate where
  NPV = 0, IRR against accounting return, the ranking conflict with NPV, and Excel.
- **`Problems with common approaches`** — 676 words, 7 blocks, **1 image skipped**. The three
  evaluation criteria, payback and its problems, average accounting ROA, IRR's reinvestment
  and scale problems, why NPV is preferred.

**Everything else in both subjects is untouched.** Weeks 0–2 of 6008 and all four weeks of
6005 were re-probed topic by topic and every `observedAt` is byte-identical to the record.

## The two Live notes — one settled, one still open

### DMBA 6008 Week 3 — `3bf7b336873c80cdaafbfc4954a7a028`, Type `Live Session` — SETTLED

New on 2026-08-17. Its **only child is `Pre-Class Prep`**, not `Discussion Questions`.

**Aryan ruled on 2026-08-18 that the carve-out does not reach it.** `Pre-Class Prep` is now
excluded outright by `subjects.json` → `DMBA6008.syncRules` → **`no-pre-class-prep`**: it is
dropped in Phase 0, **its content is never fetched at all**, and it gets no placeholder, no
topic chip and no contribution to terms, cards, quiz or scenarios. Handle it exactly the way
DMBA 6005 handles `Shadow Boxing` after Week 0.

**Do not re-open this.** The name invites the argument that "pre-class" means pre-live; that
argument is closed. Week 3 has no Discussion tab and must not gain one from this note.

### DMBA 6005 Week 3 — `3bf7b336873c8061b545e1b5340877d7`, named `Live`, typed `Pre-Live Session`

**This is the one that matters.** Flagged as an empty curiosity last session; it now has
**~120 words plus 1 image**, and the body reads unmistakably as a **live-session classroom
diary** — an in-class pre-mortem on a named external project, and an instruction-to-self
about a persona test. Nothing beneath it was fetched and nothing was published.

This is exactly the failure the open question predicted: **rule 1 keys off `Type`, not the
name**, so a mistyped diary sails straight through the filter that exists to catch it.

**Ask whether the `Type` is wrong.** If he corrects it to `Live Session` the note drops out
permanently. If he insists the `Type` is right, it **still** needs a human read against
rule 1 before a single line ships. Recorded in `docs/notion-sync-state.json` →
`DMBA6005.openQuestions`.

## The images question — now seven on this page alone

**13 images have been skipped site-wide.** The new one is the worst kind: the
`Problems with common approaches` section headed *"Why it is Weak for Investment Appraisal"*
is a three-part critique of average accounting ROA, and **the page never defines average
ROA**, because its definition and calculation are in that image. Running total: **7 in 6008
Week 3, 4 in Week 0's fourth topic, 2 in Week 2's `DuPont model example`.**

The fidelity gate was aimed at exactly this and **confirmed it did not recur** — no
numerator, denominator, formula or worked percentage for average ROA appears anywhere on the
page. Publishing any image means downloading and committing the file, which needs Aryan's
say-so. **Ask** — per image or as a policy.

## Author quirks new this run — do not "fix" these

- **`=IFR(CF0:CFn)`** — his own misspelling of IRR in the Excel section. It appears **8 times**
  on the page (prose, a formula div, an SVG `<desc>`, an SVG `<text>`, a term, a flashcard, an
  acronym def, a formula entry) and the corrected `=IRR(` appears **nowhere**. A first draft
  of the quiz called it "the typo" in his first-person voice; that was cut. **Never annotate
  it, never correct it.**
- **`2-year-payback`** — his hyphenation. Preserved in prose, an SVG eyebrow, a term and both
  formula entries.
- **`Both recover their nominal investment but still destroy economic value`** — no full stop.
  The body prose reproduces it without one.
- **`Where common appraisals measure conflict, rely on NPV`** — his closing callout, garbled
  as written. Reproduced word for word with no note attached.
- **Bare unit-less numbers** in the payback example (`100`, `50`, `86.8`, `-13.2`) against
  `20m` / `40m` / `16.4m` in the scale table. **Never normalise.**
- **The "Main Problems" table's first row records a strength** (`Recognises cash flow` /
  `Useful starting point`) under a heading of problems. Reproduced in place, with a neutral
  line above it saying so rather than relabelling the row.

Still standing from earlier syncs: **`$16.m` — never complete it** (his own `(33+0)/2` would
give 16.5); `mesaure`; `economically more value`; `a different decisions`;
`Both product the same NPV`; the section-by-section number formatting; the lowercase `x`;
6008 Week 0's `SGR = ROE x Retention Rate` against Week 2's ROA/Leverage/Retention statement
(**never reconciled**); and, in 6005, `customer lifecycle value` vs `customer lifetime value`,
`Adviser`/`advisor`, both spacings of `User→Need→Value`, `one-of transaction`,
`Shorty-term success`, `…beyond the mechanics of Scru,`, and **no dates anywhere**.

## Still empty, still an honest placeholder — do not fill

**6005 W1 → `Creating your reflective journal`** is now the **only** placeholder left on the
site. Re-checked 2026-08-18: still returns `<empty-block/>`, `observedAt` unmoved.
6008 Week 3's pair are gone — he wrote them.

**Do not trust that.** Two of three placeholders standing on 2026-08-15 were written within
24 hours, and these two were written within a day of being reported empty. **Re-check every
one, every run.**

## What the gates caught — worth reading before the next build

**Gate 1 on `Internal rate of return` returned three BLOCKING findings, all fixed:**

1. The **IRR acronym entry imported a risk claim from another topic** — "IRR incorporates
   cash flow and timing but not project risk… must be compared against an independently
   estimated hurdle rate" — and tagged it `src: 'Internal rate of return'`. The word *risk*
   appears nowhere in that harvest. Rewritten to what the topic actually says.
2. **The author's misspelling was labelled a typo** in a quiz explanation written in his
   first-person voice. Cut.
3. **"One fixed ranking, the same at every hurdle rate"** — a builder inference asserted in
   **five places at once** (an SVG `<text>`, an SVG `<desc>`, a figcaption, a quiz note and a
   scenario walkthrough). His notes say only *"Using IRR alone would therefore rank Project B
   above Project A"* and never claim invariance. All five reworded.

**Gate 1 on `Problems with common approaches` returned no BLOCKING findings** — the
average-ROA invention did not recur.

**Gate 4 caught the lecturer's name**, a hub reading `3 weeks published` over four cards, and
**a study path naming a "capital-rationing" scenario that does not exist**. All fixed.

**The lesson, for the third sync running: diagram text and derived-tab `src` attribution are
where drift hides.** Neither is prose, so neither reads as a claim — and both sailed past
every static check.

## Verification actually performed

- `checks.py` on the rebuilt page, both hubs, `index.html` and `library.html` — **0 findings**.
- **Gate 1 (fidelity)**, adversarial and context-starved, one agent per new topic. Four
  BLOCKING across the two, all fixed; ~15 NOTEs, the substantive ones fixed.
- **Gate 4 (privacy)**, full-file sweep of the page and the hub. Three findings, all fixed.
  No live-session material, no telemetry, no statistic about any real company, no
  `only-accessible-by-url` link. Excel is the only product named and only as behaviour.
- **Browser at `127.0.0.1:8788`**: all 7 tabs, **all 26 quiz questions answered** with the
  counters agreeing, 7 scenarios with 28 reveals, the study path's tab-jump working, all four
  topic chips filtering to the right block counts (5 + 8 + 5 + 7 + the study path = 26),
  **0 duplicate ids, 0 broken aria targets, 0 SVG text outside its viewBox, 0 horizontal
  overflow, 0 console errors**. Every relative link on the hub returns 200.
- `strip.py` + `build.py` verified as an **exact byte round-trip on all eight week pages**
  before the rebuild was allowed to start.

## Open threads

- [x] ~~Does the carve-out extend to `Pre-Class Prep`?~~ **No** — Aryan, 2026-08-18.
      Excluded outright by `no-pre-class-prep`; never fetched.
- [x] ~~The lecturer's name was public since the first sync.~~ **Removed 2026-08-18**, and
      `Professor`/`Email`/`Location`/`Time` added to `_globals.neverPublishFields` so it
      cannot return. Gate 4 now checks for it by name.
- [ ] **Is the 6005 `Live` note's `Type` correct?** Now urgent — it has content.
- [ ] **Scrub the lecturer's name from git history?** Needs a force-push and rewrites every
      commit since `7a63ab5`. **Aryan's call — ask once, do not do it unprompted.**
- [ ] **The 13 skipped images.** Needs a yes/no, per image or as a policy.
- [ ] **`checks.py` still does not measure the new panels' prose** — it reports the `summary`
      topic only, so Discussion, Acronyms, Formulas, Quiz and Apply it sit outside the gate.
      Unchanged for five sessions.
- [ ] **A `desc` on 6008 Week 2's Discussion tab states sustainable growth in the textbook
      `ROE × retention` form**, in `dqb5-desc`. Left alone deliberately.
- [ ] **The inline SVG figures still hard-code their fills.** The one real cleanup left.
- [ ] **Study-path voice drifts between pages** — 6008 W3 is first person, 6005 W3 second
      person. Each page is internally consistent. **Ask before normalising.**
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved. **Ask before reconciling.** Same for 6002.

## Do not

- **Do not publish anything from a `Live Session` note except DMBA 6008's
  `Discussion Questions` child page, Week 2 onwards.** Neither `Diary` nor `Pre-Class Prep`
  is covered, and **`Pre-Class Prep` must not even be fetched** — `no-pre-class-prep`.
- **Do not put a real person on a page.** `Professor`, `Email`, `Location` and `Time` from
  the Courses row are never published. A hub's meta-row is the status pill and the week count
  and nothing else.
- **Do not trust a note's name over its `Type`, or its `Type` over its name, without asking.**
- **Do not supply a formula that exists only in a skipped image**, however certain you are.
  This remains the pipeline's likeliest failure mode.
- **Do not complete `$16.m`**, or any truncation.
- **Do not repair a typo inside a figure, a figcaption, an SVG `<desc>`, a flashcard, a quiz
  option or a scenario while preserving it in the prose** — and **do not annotate one as a
  typo either.** Either it is his string everywhere or it is your wording everywhere.
- **Do not let a derived tab's `src` attribute claim a topic the material did not come from.**
  That is how a risk claim from one topic ended up published as another's.
- **Do not treat the practice content as free-form.** Extraction, not addition — the same
  standard as Acronyms and Formulas.
- **Do not relax "do not add" outside the Discussion tab.**
- **Do not reconcile** 6008 W0's and W2's statements of sustainable growth, or 6005 W3's
  `lifecycle`/`lifetime`, or its two spacings of `User→Need→Value`.
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later.** It was excluded
  in Weeks 1, 2 and 3 again this run. Week 0's stays published.
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**; **do not
  touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed`, `data-state` on
  `.opt`, or the `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names.**
- **Do not convert the study path to a runtime render.** It is static markup so the summary
  panel still reads with JS off.
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.** (This session was asked.)

## Notes for the next session

- **Replacing a placeholder is a splice, not a rebuild — and the practice components make it
  a four-step splice now.** The order that works:
  1. `practice/strip.py PAGE.html` — removes the study path, Quiz and Apply-it components.
     **Verified as an exact byte round-trip with `build.py` on all eight pages**, so this is
     safe. `build.py` refuses a page that still has them, which is why strip comes first.
  2. Swap each `data-topic-empty="true"` block for its fragment, **renumber every `block-num`
     across the whole summary panel in document order**, and extend `TERMS`/`CARDS`.
  3. Re-derive Acronyms and Formulas **from the rebuilt page**, and re-derive the practice
     JSON, then `practice/build.py`.
  4. Sweep the chrome: `<meta description>`, standfirst, hero pills, `#term-count`,
     `#card-total`, `#acronyms-count`, `#formulas-count`, the footer sync date, the hub card's
     description, its topic chips and its five `whats-inside` counts, and the hub's
     `N weeks published` pill.
- **Builders number their own blocks from 01.** Renumber at assembly or the page ships four
  block 01s.
- **Probe topics, not notes.** For the **third** consecutive run a note row's `Edited Time`
  stayed frozen while sub-pages were rewritten underneath it — 6008 Week 3's still reads
  2026-08-16 after 1,225 words landed on 2026-08-17.
- **Hand an agent a digest, not the page.** Stripping `<style>` and every inline `<svg>` cut
  the rebuilt Week 3 from 240 KB to 100 KB and lost nothing an author of questions needs.
- **Give each agent its page's traps in the prompt.** Both harvesters and both builders were
  told about `=IFR` and the average-ROA image up front, and both held — the defects the gates
  did find were ones nobody had thought to warn about.
- **Cost of this run:** 2 probes, 2 harvesters, 2 builders, 1 reference-tab agent, 1 practice
  agent, 3 gate agents. That was about right for one rebuilt week.
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8788 --bind 127.0.0.1`. An **iframe harness** drives every page in
  one `javascript_tool` call. Set `document.documentElement.style.scrollBehavior='auto'`
  before scrolling or screenshots catch the smooth-scroll mid-flight. The Chrome
  `javascript_tool` **blocks scripts that build `key=value` strings**; return objects instead.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not. This sync used fetches only.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS can block all access to `~/Documents`** via TCC. If the repo suddenly reads as
  missing, check System Settings → Privacy & Security → Full Disk Access.
