# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-12 (second session)
**Left by:** the Summary & visuals panel is now **indexed, collapsible and searchable** on all
six week pages and in the shell. Earlier the same day: a re-sync of both subjects, DMBA 6008
Week 2's **Sustainable Growth** topic, and the **Discussion questions** tab.
**The index work is NOT committed** — Aryan did not ask. Everything before it is pushed.

---

## Current focus

**Nothing in flight.** Both subjects match Notion as of 2026-08-12.

**Uncommitted in the working tree:** the summary index / collapse / search enhancement on the
six week pages, `week-shell.html`, `docs/design-system.md` and `SKILL.md`. Ask before
committing it.

### The summary index — what it is and why it works this way

Aryan's complaint was that a 31-block week is "a cluster fuck of notes" with no way in. The
Summary & visuals panel now builds a `.toc` card at load — search box, Expand/Collapse-all,
and a two-column list of every section — and turns each `.block` into a `<details>` folded
behind its own heading.

**It is generated at runtime from the blocks already on the page, and that is deliberate.**
Nothing in the authored markup changed, so: the index cannot drift from the content, a
re-sync inherits it for free, `checks.py` still measures the same `.block` elements, and with
JS off the page reads exactly as before. **Do not hand-author a contents list.**

Rules it applies: a week over **12 sections opens collapsed** (an outline you pick from);
shorter weeks stay open. Search filters the index and the body together and auto-expands
matches. A week split into topic subpanels gets **one index per subpanel**; a subpanel with
fewer than four sections gets none. It reuses the existing `.toolbar` / `.search` / `.count`
components rather than adding new ones.

Verified: all six pages, 106 links, zero console errors, zero horizontal overflow at 390 px
(the list drops to one column), and the six QA gates still pass.

## Do first

1. **A hard rule now has a carve-out. Read it before any sync.** Rule 1 was "never publish a
   `Live Session` note". Aryan directed on 2026-08-10 that DMBA 6008's live-session
   **`Discussion Questions` sub-page** be published from **Week 2 onwards**. It is a *narrow*
   carve-out: take that child page and **nothing else**. Everything else in a Live note —
   lecturer remarks, classmates' AI use, what will be examined, notes-to-self — is still
   never published. On the first run the Week 2 `Live` note happened to contain only the
   Discussion Questions child, so nothing had to be cut. **Do not assume that next time.**
   Full detail in [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published)
   and `SKILL.md`.
2. **The Discussion tab is the only place on the site where "do not add" is suspended.**
   Aryan asked for the supplied answers to be improved with outside research, industry
   examples and diagrams. That licence covers **that tab only**. Summaries, key concepts and
   flashcards remain transcriptions of his own notes. Two guardrails are load-bearing:
   **no financial statistic about any real company**, and **a provenance note heading the
   panel** so nobody mistakes the tab for his coursework.
3. **The DuPont images question is still open** and is the most useful thing to ask him.
   `DuPont model example` is titled "example" but every number lives in two Notion images,
   which are never published. That topic is still qualitative only. Ask whether he wants the
   two images downloaded and committed.

## What this sync changed

| Page | Change |
| --- | --- |
| `DMBA6008-week2.html` | **Sustainable Growth** written in Notion 08-11 → 9 new blocks, 3 figures, 20 terms, 28 cards. The "not yet written" placeholder is gone. **New Discussion tab**: 8 questions, 8 figures, 12 example cards. Page now 31 summary blocks, 20 figures, 73 terms, 108 cards. |
| `DMBA6008-weeks.html` | Week 2 card: Sustainable Growth chip un-pended, counts refreshed, discussion count added |
| `library.html` | Week 2 description updated |
| six week pages + shell | **Callout bug fixed** — see below |

**Everything else was genuinely unchanged** and was deliberately not rebuilt: 6008 Weeks 0
and 1, 6005 Weeks 0, 1 and 2. Their notes and topic `observedAt` values were byte-identical.

## Still empty, still honest placeholders — do not fill

- **DMBA 6008 W0 → `Assessing Financial Performance`.** Re-checked 2026-08-12: all ten
  sub-pages still blank (spot-checked four). The page's "not yet written" panel stands.
- **DMBA 6005 W1 → `Creating your reflective journal`.** Still `<empty-block/>`.

## Author quirks reproduced verbatim — do not "fix" these

- **Sustainable Growth writes its own algebra.** The source gives
  `Retention Ratio = 1 - Dividend Payout Ratio`, `SGR is driven by Return on Assets, Leverage
  and Retention`, `Growth > SGR → Higher Leverage`. **The textbook `g = ROE × b` form is NOT
  in his notes and must never be substituted.** Also preserved: "Higher dividend payouts
  therefore leaves" was corrected to "leave" (grammar in prose is permitted; algebra is not).
- Still standing from earlier syncs: `absorb sustainable cash`; `Volume x Margin` vs
  `Volume + Margin`; `…beyond the mechanics of Scru,`; `Sponsor buy-in is built before funding
  formal decisions`; the sprint-length hedge; and **no dates anywhere in the Agile material**.

## The bug this sync found

**`.callout` is a flex row, so two or more sibling `<p>` render side by side as columns.**
It had shipped in seven callouts across two pages. Fixed by wrapping multi-paragraph callout
bodies in a `<div>`, plus a new rule `.callout > div { flex: 1 1 auto; min-width: 0 }` added
to all six week pages and the shell. Recorded in
[docs/design-system.md](docs/design-system.md). If you author a callout with more than one
paragraph, wrap them.

## Open threads

- [ ] **Aryan has seen none of this.** Verified headlessly only. The Discussion tab in
      particular is new UI he has not looked at.
- [ ] **`checks.py` does not measure the Discussion panel.** It reports the `summary` topic
      only, so the 160-words-per-block budget on the eight question blocks was enforced by the
      building agents, not by the tool. Worth teaching it about `#panel-discussion`.
- [ ] **The inline SVG figures still hard-code their fills** — the one real cleanup left.
      See [docs/design-system.md §3](docs/design-system.md#3-tokens).
- [ ] `.DS_Store` and `blogs/.DS_Store` are still tracked. Untrack when convenient — ask
      first, it rewrites tracked state.
- [ ] Semester 1 content pages still have no "back to library" link.
- [ ] DMBA 6004's full subject title is unresolved. **Ask before reconciling.** Same for 6002.

## Do not

- **Do not publish anything from a `Live Session` note except DMBA 6008's
  `Discussion Questions` child page, Week 2 onwards.** Everything else in those notes stays
  private. `Class Diary` (6005) and the 6008 Week 1 diary remain excluded.
- **Do not relax "do not add" outside the Discussion tab.**
- **Do not put a financial statistic about a real company anywhere in the Discussion tab.**
  Companies illustrate a mechanism. Illustrative arithmetic needs invented inputs and a label.
- **Do not sync any DMBA 6005 `Shadow Boxing` content for Week 1 or later** —
  `syncRules` → `no-shadow-boxing-after-week-0`, binding on both discovery flows.
- **Do not trust a "skip this notebook" note without re-checking it.** 6005's `New Notebook`
  became `Week 2: Agile`. Emptiness is a fact about the day you looked.
- **Do not fill an empty Notion topic**, and **do not finish a truncated sentence or word.**
- **Do not restyle a DESK page ad hoc**; **do not add `overflow: hidden` to `.win`**; **do not
  touch the week pages' ids, `data-panel`, `aria-selected`, `aria-pressed` or the
  `.tab`/`.panel`/`.term`/`.flip`/`.face-*` class names.**
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since`.
- Do not commit a Notion image without asking — see "Do first" #3.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not regenerate the semester-1 subjects, and do not remove the "Heritage pages" notice.
- **Do not commit or push unless asked.**

## Notes for the next session

- **A fourth tab needs no JS change.** The inline script maps `data-panel` → `panel-<value>`
  generically and its arrow keys walk whatever `.tab` elements exist, so adding
  `data-panel="discussion"` + `#panel-discussion` just works. `week-shell.html` carries
  `<!--INSERT:DISCUSSION_TAB-->` and `<!--INSERT:DISCUSSION_PANEL-->`; a week without
  discussion questions leaves both empty and renders three tabs.
- **6005 W1's note-level `observedAt` moved with no publishable cause** — the only candidate
  is the excluded Shadow Boxing sub-page being renamed. The new value is now recorded so it
  stops re-triggering a harvest.
- **Cards are stored in topic order and terms carry a `src`.** That asymmetry is what makes
  surgical per-topic splices possible.
- **`library.html`'s `articlesBySubject` is the site's only registry.**
- **Serve the site to look at it** — Chrome tools refuse `file://`.
  `python3 -m http.server 8787 --bind 127.0.0.1`. `scroll-behavior: smooth` is on, so a
  screenshot taken straight after `scrollTo` catches the page mid-flight.
- `notion-query-data-sources` is **metered**; `notion-fetch` is not. This sync used fetches only.
- MCP tools are **deferred** — load via `ToolSearch` (`select:<exact_tool_name>`).
- ⚠️ **macOS blocked all access to `~/Documents` mid-session on 2026-08-12** — every read
  returned `Operation not permitted`, even with the sandbox disabled, because it is a TCC
  privacy gate rather than anything Claude Code controls. Aryan fixed it via **System Settings
  → Privacy & Security → Full Disk Access**. If the repo suddenly reads as missing, check that
  before assuming anything is wrong with the files.
- ⚠️ **The `SessionStart` hook still has not fired since 2026-08-05.** If this note is not at
  the top of your context, read it yourself and tell Aryan to open `/hooks` once.
