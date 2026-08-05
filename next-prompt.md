# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-05
**Left by:** condensed the DMBA 6008 summaries to budget, added QA gate 6 (length), rewrote
the volume rules across the skill and docs, committed and pushed

---

## Current focus

**Launch DMBA 6005 — Agile Project Development — and make it live.**

Aryan is writing his `Week1: Project Management` notes in Notion. When they are done he will
say **"update agile"**. That is the whole job: build Week 0 and Week 1 together, register
them, and **un-mute the subject on the homepage**.

**The hold is lifted and un-muting is pre-approved.** Aryan gave the yes on 2026-08-05
("ensure handoff is focused on kicking off the next subject and making it live"). Do not
re-ask whether to un-mute — but *do* confirm the notes actually exist before building.

## Do first

1. **Verify the trigger before anything else.** DMBA 6005 launches only when notebook
   `3b17b336873c80ada0b3f4a02cb2dea8` (`Week1: Project Management`) holds a
   **`Pre-Live Session`** note. As of 2026-08-05 it held only a `Class Diary`, which is a
   `Live Session` note and can **never** be published.
   - **If the note is not there yet: say so plainly and stop.** Do not build a one-week
     subject, and do not un-mute a subject with no material.
2. Run the skill: `.claude/skills/sync-subject/` — `SKILL.md` is the procedure and outranks
   `docs/notion-sync-automation.md`, which is only the rationale. Build **Week 0 and Week 1
   in the same run**; Aryan decided against shipping a one-week subject.
3. **Make it live** (this is the part that is new, and easy to forget):
   - `subjects.json` → `DMBA6005.live` is `false`; set it `true`.
   - `index.html` → drop `card--muted` from the DMBA 6005 card and rewrite its `card-desc`.
   - `library.html` → add to **both** `articlesBySubject` **and** `validSubjects`. A subject
     in one but not the other silently falls back to DMBA 6002.
4. Run all six gates, then **open it in a browser** and walk `index.html` →
   `library.html?subject=DMBA6005` → hub → week page → back link.

## The length budget — read before building anything

Week 0 of DMBA 6008 shipped at ~4,000 words per topic against a stated 900–1400 budget that
nothing measured. Aryan called it "waaaay too long" and it was condensed in three passes on
2026-08-05 (~11,850 → ~8,270 summary words, entirely prose; every table, figure, formula and
worked example byte-identical). The rules now:

- **≤ 160 words of flowing prose per `.block`**, floor 900 per topic.
- Tables, figures, worked examples, callouts and formulas **do not count** — they carry the
  study material. Connective paragraphs are what bloat.
- **Gate 6 in `checks.py` measures it and blocks publication.**
  `checks.py --lengths <page>.html` prints the table without failing — use it *mid-build*,
  not after assembly.
- **Name the number in every builder agent's prompt.** The budget sat in `fragment-spec.md`
  the whole time and was still blown 3×. Naming it is the fix.
- Match `DMBA6008-week1.html` — 134 prose words per block. **Do not copy week 0's density.**
- The four things that caused the bloat are listed in `fragment-spec.md` §5: prose restating
  the adjacent table, repeated callouts, a closing block that re-summarises, and definitions
  repeated in every block that touches the term.

## Settled for DMBA 6005 — do not re-ask

- **Type pairing: Sora + Karla**, `--course-e` ochre palette. `fontHref` is in
  `subjects.json`. Details in
  [docs/notion-sync-automation.md §7](docs/notion-sync-automation.md#7-extending-to-dmba-6005).
- **Un-muting is approved** (2026-08-05) — conditional only on the subject actually having
  published pages.
- `New Notebook` (`3b37b336873c80db9388ee1a56192b33`) is an empty placeholder. Skip it;
  never render it as a week.
- Week 0's `$RUs` note is **Shape B (inline)** — content sits on the note page itself. One
  topic, so one agent.
- Week 0 is a **strategic case, not a formula topic**: reach for option-comparison matrices,
  a customer-journey strip and a decision-rule table — not equations. Cards shift from
  "compute this" to "given this symptom, which option and why". Agile weeks proper will want
  cycle diagrams and board/timeline strips; do not reuse Week 0's option-matrix vocabulary
  just because it is there.

## Open threads

- [ ] **The skill has never run end-to-end.** Only Phase 0 has ever executed. Phases 2–6 fire
      for the first time on this DMBA 6005 launch — expect to babysit it, and check the
      harvest output before letting builders loose on it.
- [ ] **No page has been checked at narrow width**, and the flashcard flip has not been tried
      on a real touch device. Static checks cannot catch layout; Aryan found the last layout
      bug by looking at the page after every gate passed.
- [ ] **DMBA 6008 Week 0 → "Assessing Financial Performance" is still empty in Notion.**
      Re-checked 2026-08-05. `DMBA6008-week0.html` renders an honest "not yet written" panel
      listing the ten pending sub-pages — **that panel is the thing to replace** when Aryan
      writes them.
- [ ] Optional, only if Aryan raises it: DMBA 6008 week 0 still reads long at 31 blocks even
      at budget. The lever is **structural, not verbal** — merge Goodwill into Intangibles and
      fold Asset quality into blocks 05/06, ~31 blocks → ~24. Costs no content. Ask first.
- [ ] `.DS_Store` and `blogs/.DS_Store` are tracked in git. Untrack them and add a
      `.gitignore` when convenient — ask first, it rewrites tracked state.
- [ ] Content pages (e.g. `DMBA6001-*.html`) still have no "back to library" link; the three
      `DMBA6008-*.html` pages do. Retrofit the old ones when next editing them. See
      [docs/conventions.md](docs/conventions.md#navigation).
- [ ] DMBA 6004's full subject title is unresolved — Notion says "Digital Collaboration, Work
      and Organisation", the repo uses a short topic label. **Ask before reconciling.** Same
      mismatch for DMBA 6002.

## Do not

- **Do not publish `Live Session` or `Assessment` notes.** Only `Pre-Live Session`. GitHub
  Pages makes everything public. DMBA 6005 Week 1's `Class Diary` and the DMBA 6008 Week 1
  diary both contain candid remarks about the lecturer, about classmates' AI use, and about
  what will be examined. See
  [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published).
- **Do not fill an empty Notion topic with generated content.** An empty topic renders empty.
  `DMBA6008-week0.html`'s fourth panel is the precedent.
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since` — Aryan confirmed
  2026-08-05 this telemetry stays private.
- Do not reference or commit a Notion image. Aryan decided 2026-08-05 that **images are
  skipped**; the sync reports the count per week so he can ask for a specific one.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not add a build step, npm dependency, or generator in the deploy path.
  (`reference/checks.py` is a verification tool — nothing at serve time calls it.)
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not restyle existing pages wholesale; each page owns its visual identity.
- Do not regenerate the semester-1 subjects (`DMBA6001`, `DMBA6002`, `DMBA6004`) — they are
  `Completed` and hand-written from before this pipeline.
- **Do not commit or push unless asked.** The working tree was clean as of 2026-08-05: the
  condensation, the new gate and the doc rewrites are all on `origin/master`.

## Notes for the next session

- **The pipeline hinges on the Notes `Type` field.** Everything else is plumbing.
- **Detect content shape at runtime, never trust the config.** DMBA 6008 Week 1 proves both
  shapes coexist inside one note: `Key Value Principle` is a container, `Key Definitions` is
  inline.
- **A child page has no `Edited Time`** — only a Notes database row does. Change detection
  leans on the `as of` stamp in the fetch envelope, which was verified to be a content
  timestamp, plus a content hash. Rationale in
  [docs/notion-sync-automation.md §3](docs/notion-sync-automation.md#3-change-detection).
- `notion-query-data-sources` is **metered**; `notion-fetch` on a relation URL is not.
- MCP tools are **deferred** — load schemas via `ToolSearch` (`select:<exact_tool_name>`).
- Before choosing fonts for any future subject, inventory what is taken (thirteen already
  are): `grep -rhoE 'family=[A-Za-z+]+' --include='*.html' .`
- ⚠️ **The `SessionStart` hook did not fire on 2026-08-05** — this file was not in context and
  had to be read manually. The script is fine (run by hand, emitted correct JSON) and
  `.claude/settings.json` is wired correctly, so the likely cause is the project hook not
  being trusted/loaded. **If this note is not at the top of your context, read it yourself
  and tell Aryan to open `/hooks` once.**
