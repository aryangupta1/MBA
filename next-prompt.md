# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-08-05
**Left by:** skill-build session — built the `sync-subject` skill, settled every open design
decision with Aryan, dry-ran it against DMBA 6008, committed and pushed

---

## Current focus

**Nothing in flight.** The Notion sync is built and every decision behind it is settled.

Say **"update finance"** and `.claude/skills/sync-subject/` runs the whole pipeline —
harvest, build, register, five QA gates. Its `SKILL.md` is the procedure and outranks
`docs/notion-sync-automation.md`, which is now just the rationale.

**Do not say "update agile" yet** — DMBA 6005 is deliberately on hold, see the first open
thread.

## Do first

Nothing is queued. Ask Aryan what he wants, or offer the oldest open thread: **nobody has
looked at any page at narrow width**, including `index.html` since the semester refactor and
all three DMBA 6008 pages since they were built.

## Open threads

- [ ] **DMBA 6005 is on hold by choice — build nothing, not even unpublished pages.** Aryan
      decided 2026-08-05 to wait until `Week1: Project Management` has a `Pre-Live Session`
      note, then launch Week 0 and Week 1 together rather than ship a one-week subject.
      *Trigger:* a `Pre-Live Session` note under notebook `3b17b336873c80ada0b3f4a02cb2dea8`
      — today it holds only a `Class Diary`, which is a `Live Session` note and can never be
      published. When it fires, **say so and ask** — do not just run.
      *Settled, do not re-ask:* pairing is **Sora + Karla** on `--course-e` ochre. Details in
      `subjects.json` and [docs/notion-sync-automation.md §7](docs/notion-sync-automation.md#7-extending-to-dmba-6005).
      **Un-muting the `index.html` card still needs its own yes.**
- [ ] **The skill has never run end-to-end.** Only Phase 0 has executed. Phases 2–6 fire for
      the first time whenever new Notion content lands — expect to babysit that first run.
- [ ] **No page has been checked at narrow width**, and the flashcard flip has not been tried
      on a real touch device. Static checks cannot catch layout; Aryan found the last layout
      bug by looking at the page after every gate passed.
- [ ] **DMBA 6008 Week 0 → "Assessing Financial Performance" is still empty in Notion.**
      Re-checked 2026-08-05. `DMBA6008-week0.html` renders an honest "not yet written" panel
      listing the ten pending sub-pages — **that panel is the thing to replace** when Aryan
      writes them.
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
  Pages makes everything public. The DMBA 6008 Week 1 diary in particular has candid remarks
  about the lecturer, about classmates' AI use, and about what will be examined — it is
  recorded in `docs/notion-sync-state.json` as `published: false`. See
  [docs/notion-sync.md §6](docs/notion-sync.md#6-what-must-never-be-published).
- **Do not fill an empty Notion topic with generated content.** An empty topic renders empty.
- Do not publish `Confidence`, `Last Reviewed`, `Favorite` or `Days Since` — Aryan confirmed
  2026-08-05 this telemetry stays private.
- Do not reference or commit a Notion image. Aryan decided 2026-08-05 that **images are
  skipped**; the sync reports the count per week so he can ask for a specific one.
- Do not write to Notion. One-way: Notion authoritative, repo publish-only.
- Do not add a build step, npm dependency, or generator in the deploy path.
  (`reference/checks.py` is a verification tool — nothing at serve time calls it.)
- Do not rename the legacy `DMBA-6001-*.html` files — shared URLs point at them.
- Do not restyle existing pages wholesale; each page owns its visual identity.
- **Do not commit or push unless asked.** Nothing is outstanding: Aryan asked for a commit
  and push on 2026-08-05, so the skill, the state file and the doc edits are all on
  `origin/master`, as is the DMBA 6008 page build before them. **The working tree is clean.**

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
