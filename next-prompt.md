# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-17
**Left by:** A feature session, not a sync. Aryan asked for **a quiz tab on every semester-2
week**, plus **a second learning tab of my choosing** (he picked **Apply it**), and then
mid-session for **a "how to master this week" panel on every page**. All three now ship on
all eight week pages. Nothing was re-synced; no Notion call was made. **Committed and
pushed**, as asked.

---

## Read this first — the hook did not fire

**`next-prompt.md` was NOT injected into this session's context.** It had to be opened by
hand, for the third session running. `settings.json` is correct and the script exists and is
executable, so the remaining explanation is a **project-scope hook awaiting Aryan's
approval, which cannot be granted from inside a session.**

**Ask him to open `/hooks` once and approve it.** Until then, every session must open this
file by hand.

## Current focus

**Nothing in flight.** Both subjects still match Notion as of 2026-08-17 — this session did
not touch the synced material.

## What is new — three practice components on all eight week pages

| Component | Where it sits | What it does |
| --- | --- | --- |
| **Study path** | first block of the Summary panel, `00 / Start here` | "How to master this week" — a 5–7 step route, each step with a time estimate and a button that jumps to its tab |
| **Quiz** | its own tab | four options, one right, a hint per question, a note on **every** option, running score, Start over |
| **Apply it** | its own tab | scenarios with three staged hints, a walkthrough and a self-mark checklist |

Counts per page:

| Page | Questions | Scenarios | Path steps | Tabs now |
| --- | --- | --- | --- | --- |
| DMBA6008-week0 | 24 | 6 | 7 | 7 |
| DMBA6008-week1 | 12 | 4 | 7 | 7 |
| DMBA6008-week2 | 22 | 6 | 7 | **8** (it has Discussion) |
| DMBA6008-week3 | 15 | 4 | 7 | 7 |
| DMBA6005-week0 | 12 | 4 | 6 | **6** (no Formulas tab) |
| DMBA6005-week1 | 18 | 5 | 7 | **6** (no Formulas tab) |
| DMBA6005-week2 | 18 | 5 | 7 | 7 |
| DMBA6005-week3 | 22 | 6 | 7 | 7 |

### The important structural fact

**None of it is synced from Notion. All of it is derived from the built page**, exactly like
the Acronyms and Formulas tabs — which means it can only ever contain material that already
passed gate 1.

It lives in **`.claude/skills/sync-subject/reference/practice/`**:

```
practice/
  README.md        the data schema, the authoring rules, the rebuild procedure — BINDING
  build.py         splices all three into a page, asserting the shape first; safe to re-run
  tpl/quiz.css     stylesheet for the quiz and apply-it panels
  tpl/quiz.js      the shared renderer for both
  tpl/path.css     stylesheet for the study path
  data/<PAGE>.json the authored content, one file per week page — all eight committed
```

## Do first

1. **Aryan has seen none of this.** Built and pushed on his instruction, without review.
2. **Point him at one page and one tab.** `DMBA6008-week3.html` → Quiz is the sharpest test
   of whether the questions are actually useful to him, because that week is the thinnest
   and the most constrained by unpublished images.
3. **The 12 skipped images are still the biggest real gap on the site** and still need a
   yes/no. See below — unchanged from the last session.

## The rule Aryan added this session — read before any sync

> *"Future syncing and re-syncs need to update quiz and apply it accordingly based on new
> information."*

This is now written into **`SKILL.md` Phase 3c**, **`docs/notion-sync.md` §3c**, **CLAUDE.md**
and the `practice/README.md`. In practice, when a week changes:

1. **Re-derive that page's JSON** from the rebuilt page — new questions for the new
   material, and any question the change invalidated rewritten or dropped.
2. **Re-check the study path.** A week that gains a topic needs its route updated; a filled
   placeholder must stop being described as unwritten.
3. **Sweep the counts** — the hero pill `N quiz questions`, the hub card's `whats-inside`
   chips (quiz questions **and** scenarios), and the hub's mode list.

**`build.py` skips a component the page already has.** To rebuild, regenerate the page and
then run it — splicing over the top will not replace what is there.

## How this was built, if it needs doing again

Eight agents, one per page, each given only a **digest** of its page (the real file with
`<style>` and every inline `<svg>` stripped — 6008 Week 0 went 380 KB → 283 KB). Each wrote
a JSON file and edited no HTML; one Python script did every splice, so all eight pages are
mechanically identical. The same eight agents were then resumed with a follow-up for the
study path, which cost a fraction of a fresh spawn because they still had the page in
context. **That resume-rather-than-respawn move is worth repeating.**

## Two decisions worth knowing about

- **`checks.py` was changed.** `<ol class="path">` now counts as an artefact rather than
  flowing prose, alongside `.steps` and `.takeaways`. Without it the study path pushed
  **6008 Week 1** over its prose budget by 325 words — the path is navigation advice, not
  week prose, and a short week would otherwise fail a gate for gaining a UI panel.
- **No new design token.** Right and wrong reuse the `--pos*` / `--neg*` verdict tokens every
  week page already defines. The components are documented in
  [docs/design-system.md §5](docs/design-system.md#the-practice-components--study-path-quiz-apply-it).

## Two small things left deliberately

- **Voice drifts between pages.** 6008 Week 3's study path is first person ("when I can
  explain…"); 6005 Week 3's is second person ("when you can take…"). Each page is internally
  consistent. Worth normalising to first person one day, since the rest of the site is his
  own notes — **ask before doing it**, it is a voice decision, not a bug.
- **The hub footers still read "Read it. Look it up. Drill it."** Left alone as a slogan
  rather than an enumeration. The hub *lede* and the mode grid were updated and now name
  five modes.

## Still empty, still honest placeholders — do not fill

- **6005 W1 → `Creating your reflective journal`** — the study path on that page says plainly
  the material is not there. No question, scenario or hint touches it.
- **6008 W3 → `Internal rate of return`**
- **6008 W3 → `Problems with common approaches`**

Neither 6008 pair is covered anywhere else on the page, so **IRR is not tested and must not
be** until he writes it.

## The images question — unchanged and still the biggest gap

**12 images have been skipped and several carry the algebra**: the symbolic present-value
formula and its worked example, the Average ROA calculation, a straight-line depreciation
illustration and two on Excel's `NPV()` (6008 W3, 6 images); 4 in Week 0's fourth topic;
2 in Week 2's `DuPont model example`.

**The quiz made this worse, not better** — every one of those was a question I could not
write. The 6008 Week 3 agent was told explicitly not to supply them and did not; its single
Average ROA question tests the *limitation* the prose states instead, and the string `16.m`
appears nowhere in its data, so there was no opening to complete the truncation.

Publishing any image means downloading and committing the file, which needs Aryan's say-so.
**Ask** — per image or as a policy.

## A note named `Live` is typed `Pre-Live Session`

`3bf7b336873c8061b545e1b5340877d7`, in the **DMBA 6005 Week 3** notebook. Still **empty**, so
it has cost nothing. It matters the moment it has content: **rule 1 keys off `Type`, not the
name.** Ask Aryan whether the Type is right before publishing anything from it. Recorded in
`docs/notion-sync-state.json` → `DMBA6005.openQuestions`.

## Author quirks reproduced verbatim — do not "fix" these

Everything from the last three syncs still stands, and the practice content was written
against all of it. In **6008**: `$16.m` (**never complete it**), `mesaure`,
`economically more value`, `a different decisions`, `Both product the same NPV`, the
section-by-section number formatting (`$112,000`/`$101,818` in one passage, `$2000`/`$1818`/
`$101818`/`$100000` in another — **never normalise**), the lowercase `x` as his
multiplication sign, and the two irreconcilable statements of sustainable growth
(`SGR = ROE x Retention Rate` in W0, "driven by ROA, Leverage and Retention" in W2).
In **6005**: `Type of Personas` (singular and empty), the A–E headings with no bodies,
`customer lifecycle value` alongside `customer lifetime value`, `Adviser`/`advisor`,
both spacings of `User→Need→Value`, `one-of transaction`, `Shorty-term success`,
`The project. should therefore serve:`, `…beyond the mechanics of Scru,`, `strictly liner`,
`weak thinning`, and **no dates anywhere in the Agile material**.

**The `decisions` → `dimensions` trap is now handled in three places on 6005 W3** — the
prose, the figures, and now the quiz. The quiz question asks what empathy mapping
*investigates* and quotes `Think → Feel → Say → Do` as he writes it, so the noun is never
restated, corrected or replaced. **Keep it that way.**

## Verification actually performed

- `checks.py` on **all eight** week pages, both hubs, `index.html` and `library.html` —
  **0 findings**.
- **Browser, served at `127.0.0.1:8787`**, every page loaded in an iframe harness and driven:
  every tab clicked, **every question on every page answered** (24/12/22/15/12/18/18/22 — the
  score counters all agreed with the answer counts), every scenario and every study path
  rendered, **0 duplicate ids, 0 broken `aria-labelledby`/`aria-controls`, 0 horizontal
  overflow, 0 console errors** across all eight.
- Path buttons confirmed switching tabs; topic chips confirmed leaving the study-path block
  visible under every filter (it carries no `data-topic`, by design); the tab row confirmed
  wrapping cleanly at 500 px with seven tabs.
- **One real defect found and fixed in flight**: the study-path buttons rendered
  `Open Summary &amp; visuals` because the label is lifted off the page's own tab button and
  was being escaped twice. Fixed in the 8 pages and in `build.py`.

## Open threads

- [ ] **The 12 skipped images.** Needs a yes/no from Aryan, per image or as a policy.
- [ ] **Is that `Live` note's `Type` correct?**
- [ ] **Normalise the study-path voice to first person?** Ask first.
- [ ] **`checks.py` still does not measure the new panels' prose.** It reports the `summary`
      topic only, so Discussion, Acronyms, Formulas, Quiz and Apply it are outside the prose
      gate. Unchanged for four sessions.
- [ ] **A `desc` on 6008 Week 2's Discussion tab states sustainable growth in the textbook
      `ROE × retention` form**, in `dqb5-desc`. Left alone deliberately.
- [ ] **The inline SVG figures still hard-code their fills.** See
      [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved. **Ask before reconciling.** Same for 6002.

## Do not

- **Do not treat the practice content as free-form.** It is **extraction, not addition** —
  the same standard as Acronyms and Formulas. No formula that sat in an unpublished image,
  no repaired typo, no completed truncation, no reconciled inconsistency, nothing from a
  Live Session note, and nothing from a topic the page marks unwritten.
- **Do not publish anything from a `Live Session` note except DMBA 6008's
  `Discussion Questions` child page, Week 2 onwards.** The `Diary` sibling is not covered.
- **Do not trust a note's name over its `Type`, or its `Type` over its name, without asking**
  when the two disagree.
- **Do not repair a typo inside a figure, a figcaption, an SVG `<desc>`, a flashcard, a quiz
  option or a scenario while preserving it in the prose.** Either it is his line everywhere
  or it is your wording everywhere.
- **Do not touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed`, the
  `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names — or `data-state` on `.opt`**, which
  is the quiz's source of truth for feedback the way `aria-pressed` is for the flip.
- **Do not convert the study path to a runtime render.** It is static markup on purpose, so
  the summary panel still reads with JS off.
- **Do not move the tab row's wrapping back inside a media query.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**.
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later.** (Week 0's is
  published and legitimate; the Week 0 quiz draws on it.)
- **Do not trust a "this is empty" note without re-checking it.**
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.** (This session was asked.)

## Notes for the next session

- **Hand an agent a digest, not the page.** Stripping `<style>` and every inline `<svg>` cut
  6008 Week 0 from 380 KB to 283 KB and the small pages by half, and lost nothing an author
  of questions needs. The one-liner is in this session's scratchpad but is three lines of
  `re.sub` and is faster to rewrite than to find.
- **Resume an agent rather than spawning a new one** when the follow-up is about the same
  page. The study-path round cost roughly a tenth of the first round.
- **Give each agent the page-specific traps in its prompt.** The 6005 Week 3 agent was told
  about `decisions`/`dimensions` up front and handled it correctly first time; the equivalent
  defect in the last session took an adversarial gate to catch.
- **`build.py` asserts before it writes** — four options, exactly one correct, a note on
  every option, three hints, 3–6 walkthrough steps, 3–5 checklist items, 5–7 path steps, and
  every `goto` an actual tab on that page. A malformed file fails loudly rather than
  shipping. Keep it that way.
- **The tab numbers are computed, not hard-coded.** `build.py` counts the tabs the page
  already has, so a week that later gains a Discussion or Formulas tab renumbers correctly.
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`. An **iframe harness** on the index page
  drives all eight pages in one `javascript_tool` call and is far quicker than eight
  navigations. **Chrome caches aggressively across a CSS edit** — append `?v=N` or reload.
  Note the Chrome `javascript_tool` **blocks scripts that build `key=value` strings**; return
  arrays or objects instead.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS can block all access to `~/Documents`** via TCC. If the repo suddenly reads as
  missing, check System Settings → Privacy & Security → Full Disk Access.
