# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-09-12
**Left by:** Aryan's instruction: *"New changes have been made to the notion, update and sync
accordingly. Commit and push directly to master"*, then *"Also let's add assessment notebooks
to the live sessions btw. And update doco accordingly. Utilise sub-agents effectively."*
Full-scope Notion → vault harvest of both semester-2 subjects; the only new material was
**DMBA 6008 Assessment 2 — Part A**. Assessment notebooks are now **gated pages under `live/`**.
Committed and pushed.

---

## What was built — 2026-09-12

**The sync.** One metered query. One new top-level note: `Part A` (Type `Assessment`) in a new
notebook *Assessment 2: Company Valuation*, with one sub-page `Overview` (Aryan's Cogstate
valuation notes — tables, formulas, no images). Harvest fanned out to **9 agents** across
both subjects' full scope (31 top-level notes) because sub-page edits don't bump Notion's
edited time. Diffed against `backup-20260912-152126`: **every existing raw file
byte-identical**, 0 whitespace-only, 0 real changes; 2 NEW (Part A + Overview, confirmed by my
own `notion-fetch`). `apply_harvest`: 2 NEW, no conflicts. `verify.py`: only the two known
failures (transcript/chat wikilinks; MedScope LaTeX artefact). `vault_discover`: **no public
topic changed in either subject**, so no week page or search page was rebuilt.

**Incident, contained.** The agent covering the 6008 Assessment 1 `Plan` recursed into its
`Live Session Transcript` / `Live Session Chat` sub-pages and harvested the **Week 3 and Week 4
transcripts and chat logs** (8 raw files, ~290 KB, classmates' names). My prompt to that batch
omitted the no-transcript line. All 8 raw files and their `children.d` rows were **deleted
before apply** — none were in the backup or the state, none reached the vault, no attachments.
The agent's session transcript in the Claude temp dir still holds the fetched text; not in the
repo or the vault. **Every future harvest prompt must carry the no-transcript rule.**

**Assessment notebooks on the gated pages** (`.claude/private-pages/build.py`):
- `live/<CODE>-assessment<N>.html`, one per vault folder `Assessment <N> …` — **discovered, not
  listed**. Every note in the notebook, top-level in created order, sub-pages after their
  parent (`Parent — Child`). A stale assessment page is removed on rebuild.
- Built: **DMBA6005-assessment1** (Plan, Final Version), **DMBA6008-assessment1** (Plan),
  **DMBA6008-assessment2** (Part A, Part A — Overview).
- Subject index `live/<CODE>.html` now has a **Weeks** section and an **Assessment notebooks**
  section.
- **Tab links on every gated page** (Aryan, same day: *"Where are the assessment notebook? It
  should fall under the live tab links"* — first cut only listed them at the bottom of the
  index). `subject_tabs()` renders **All · Week N … | Assessment N …** at the top of the index,
  every week page and every assessment page, current page highlighted. Derived from `PAGES` +
  discovered notebooks — no hand list.
- New `IMAGE_TRANSCRIBED` table — the 6008 A1 rubric (two text screenshots) is a transcribed
  table; PNGs not published.
- `<mention-page>` links now render as `Week › Note` titles from vault frontmatter instead of
  being dropped (the 6005 Plan had three empty bullets otherwise).
- Verified in Chrome over `http://127.0.0.1`: wrong code rejected, test code unlocks, both
  6008 assessment pages and the 6005 one auto-unlock in the tab, rubric renders, no body
  overflow (Chrome would not go below ~780 px). Rebuilt with the real code afterwards; no
  `<img>`/`prod-files` in any live file.

**Docs** (sub-agent): `.claude/private-pages/README.md`, `CLAUDE.md`, `docs/architecture.md`,
`conventions.md`, `content-guide.md`, `workflows.md`, `vault-sync.md`, `design-system.md`;
hub `.lookup--live` card copy on both hubs and both `library.html` descriptions now mention
assessment notebooks (copy only, no CSS). `SECRET-PAGES.md` has a new "Assessment notebooks"
table.

## Do first

1. **Tell Aryan about the transcript incident above** — contained, nothing published, but he
   should know an agent read those pages.
2. **Tell Aryan the access code is six characters** (carried over) — assessment work now sits
   behind it too, which raises the stakes. Longer code: change `.env`, re-run `build.py`, commit.
3. Ask how the **assessment pages** look — and whether he wants the **6005 Final Version**
   (his submitted video script) behind the gate at all; it was included because he asked for
   the notebooks, not by a note-by-note ruling.
4. Still unseen by him: Week 6 page, live index, hub card, search pages, 6008 Wk 5, 6005 Wk 6.
5. Ask him to approve the hook (`/hooks`) — twelfth session reading this by hand.
6. Mention the `$28.888m` / `$22.888m` line (carried over).

## Open threads

- [ ] **Add the no-transcript rule to `~/MBA/.mba-sync/AGENT-INSTRUCTIONS.md` itself**, so it
      is not left to each prompt. (Not done this session — `.mba-sync` is outside the repo.)
- [ ] **Acronyms/formulas splice is still hand-scripted per week** — worth a `splice_ref.py`.
- [ ] **Sync-notes image expiry**: write and ingest each raw file immediately; re-fetch on fail.
- [ ] `semester-2-private-notes.html` is stale and needs its own password to rebuild or delete.
- [ ] Four syllabus files still cannot be migrated (`file://` refs in Notion).
- [ ] Lecturer name and email remain in git history from `7a63ab5`; not scrubbed, not asked.
- [ ] No `Live` note yet for **6005 Week 6** or **6008 Week 5**; when one lands, add it to
      `PAGES` in `build.py` and rebuild. (Assessments need no code change.)
- [ ] `harvest_plan.py` writes one `plan.json` per course — running it for two courses in a
      row leaves only the second's plan, so `apply_harvest` silently skips the first. Re-run it
      for each course before its apply (done manually this session).

## Settled — do not re-open

- **Live pages and assessment notebooks are gated and linked; the gate is the control.** Never
  build one without it, never commit `.env`, never print the code.
- **Assessment notebooks are discovered from the vault** — no hand list.
- **Third-party material stays withheld on gated pages too** — names, transcripts, chat, images
  with people. Text screenshots (formulas, rubrics) are transcribed, never published.
- **The search pages add no content.** One per subject, rebuilt after every week change.
- **DMBA 6005 Week 3 `Live`** stays off public week pages. **Notion feeds the vault only.**
- **DMBA 6008 Week 4's lease inconsistency and Week 6's $28.888m line stay unreconciled.**

## Do not

- Do not hand-edit `DMBA60xx-search.html` or anything under `live/`; rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` or `.env` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log — **and say so in every harvest prompt.**
- Do not tidy his typos (`sprintsn`, `Estimate value at exist`, `What is answers`, `FCC`, …).
- Do not derive a number the notes leave unstated.
