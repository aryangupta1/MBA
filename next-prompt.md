# Next prompt

> Standing handoff note. This file is injected into every new Claude Code session by
> the `SessionStart` hook and is **binding** unless the session opens with
> `Adhoc chat, ignore next prompt`. Protocol: [docs/next-prompt-protocol.md](docs/next-prompt-protocol.md).
>
> Every session must leave this file updated before it ends.

**Last updated:** 2026-09-09 (evening)
**Left by:** Aryan's instruction: *"updates have been made in notion publish them, commit and
push. and also lets make a nav link for the live pages, make the access code protected"*.
Pulled **DMBA 6008 Week 6** from Notion into the vault and published it; moved the live-session
pages to **`live/`** behind an **access-code gate** (AES-256-GCM, code in the git-ignored `.env`);
committed and pushed.

---

## What was built — 2026-09-09

**DMBA 6008 Week 6 — Equity hurdle rate and valuation applications** (`DMBA6008-week6.html`).
Four topics from the vault's `Learn` note: `Equity hurdle rate Beta and CAPM`,
`Beta un-levered versus levered`, `Valuing an early-stage venture`, `Valuing a private company`.
27 blocks, 14 figures, 67 terms, 96 cards, 10 acronyms, 29 formulas, 12 quiz questions,
5 scenarios. All **eleven** source images were LaTeX formula renders and were
**transcribed, not published** (same as Week 5). Gate 1 found five minor added glosses in figure
chrome and glossary defs; all fixed. `checks.py` clean. Verified in Chrome (desktop, 500 px —
Chrome would not go narrower). `DMBA6008-search.html` rebuilt: **1,359 entries**.

**Source inconsistency reproduced, not reconciled** (settled — like Week 4's lease): his
early-stage notes discount the exit value to **$22.888m** but the pre-funding line reads
**`$28.888m - $8m = $14.888m`**. Both appear on the page exactly as written. Worth telling him.

**The sync itself:** one metered Notion query; two new top-level notes (`Learn`, `Live`) in a
new notebook *Week 6: Equity Hurdle rate and valuation applications*; seven raw files written
by hand (no agent fan-out — two notes), 14 images ingested (one presigned URL expired mid-run
and was re-fetched; a helper in `.mba-sync` was **not** added — the re-fetch was done inline).
`apply_harvest`: 7 NEW, no conflicts. `verify.py`: the two pre-existing wikilink misses plus one
new "leftover markup" hit — the `\$…\\boxed{…}` LaTeX artefact pasted into Live Prep Q2, which is
his text and stays. The notebook's `Notes` relation also lists `83e72ed6425f4c309f45c2f9c45e08fd`,
which returns `object_not_found`; ignored. **DMBA 6005 had nothing new.**

**Live pages, gated** — `live/DMBA6008.html`, `live/DMBA6005.html` (per-subject indexes) and
`live/<CODE>-week<N>.html` (9 weeks: 6005 wk 1/3/4/5, 6008 wk 1/2/3/4/6). Built by
`.claude/private-pages/build.py`, which now reads `LIVE_ACCESS_CODE` from `.env`, encrypts
each page's content with node's AES-256-GCM (PBKDF2-SHA256 × 310k, fresh salt/IV per run) and
ships a gate card + WebCrypto decrypt script. Unlocking once keeps the subject open for the tab
(`sessionStorage`); a **Lock these pages** button forgets it. The Week 6 Live Prep's three
formula screenshots are transcribed via a new `IMAGE_FORMULA` table. The old plaintext
`only-accessible-by-url/*-private.html` files were **deleted**; `SECRET-PAGES.md` is rewritten as
the index. `.env` is git-ignored; `robots.txt` disallows `/live/`. Verified in Chrome over
`http://127.0.0.1` (WebCrypto needs a secure context — `file://` will not do): wrong code
rejected, right code unlocks, week page auto-unlocks, no `<img>` or plaintext in any file.

**Nav:** each hub has a fourth hero pill `Live sessions →` and a second pinned card
`.lookup.lookup--live` under the search card; `library.html` lists `live/<CODE>.html` under both
subjects. Documented in `docs/design-system.md`, `architecture.md`, `conventions.md`,
`content-guide.md`, `workflows.md` ("Rebuild the live-session pages"), `CLAUDE.md`.

## Do first

1. **Tell Aryan the access code is six characters** — with the ciphertext public, the code's
   strength is the whole defence. If he wants a longer one: change `.env`, re-run
   `python3 .claude/private-pages/build.py`, commit. Nothing else changes.
2. Ask him how the **Week 6 page**, the **live index** and the **hub card** look. He has still
   not seen the search pages, 6008 Week 5 or 6005 Week 6 either.
3. Ask him to approve the hook (`/hooks`) — eleventh session reading `next-prompt.md` by hand.
4. Mention the `$28.888m` / `$22.888m` line above.

## Open threads

- [ ] **Acronyms/formulas splice is still hand-scripted per week** (this run: inline Python in
      the session, using Week 5's tab/panel/`buildRef` markup as the template). Worth folding
      into a `reference/splice_ref.py` next sync.
- [ ] **Sync-notes image expiry**: presigned URLs live ~5 min from the fetch; on a multi-note
      run write and ingest each raw file immediately, and re-fetch a page whose download failed.
- [ ] `semester-2-private-notes.html` is stale and needs its own password to rebuild or delete.
- [ ] Four syllabus files still cannot be migrated (`file://` refs in Notion).
- [ ] Lecturer name and email remain in git history from `7a63ab5`; not scrubbed, not asked.
- [ ] The **AI-use remark** in the 6008 Week 1 diary is now behind the gate; the 2026-08-31
      question about it is moot unless he wants it cut anyway.
- [ ] No `Live` note yet for **6005 Week 6** or **6008 Week 5**; when one lands, add it to
      `PAGES` in `build.py` and rebuild.

## Settled — do not re-open

- **Live pages are gated and linked; the gate is the control, not obscurity.** Never build a
  live page without it, never commit `.env`, never print the code.
- **Third-party material stays withheld on gated pages too** — names, transcripts, chat, images
  with people.
- **Formula images are transcribed, never published** — on public and gated pages alike.
- **The search pages add no content.** One per subject, rebuilt after every week change.
- **DMBA 6005 Week 3 `Live`** stays off public week pages. **Notion feeds the vault only.**
- **DMBA 6008 Week 4's lease inconsistency and Week 6's $28.888m line stay unreconciled.**

## Do not

- Do not hand-edit `DMBA60xx-search.html` or anything under `live/`; rebuild.
- Do not build a page from Notion; pull with `sync-notes`, publish from the vault.
- Do not commit `~/MBA` or `.env` to this repo, and never write back to Notion.
- Do not harvest a Live Session transcript or chat log.
- Do not tidy his typos (`sprintsn`, `Estimate value at exist`, `operating stock`, and so on).
- Do not derive a number the notes leave unstated.
