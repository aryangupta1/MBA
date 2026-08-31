# Private (unlisted) live-session pages

`build.py` renders the Obsidian vault's **Live Session** notes into one unlisted HTML page
per week, per subject, at `only-accessible-by-url/<CODE>-week<N>-private.html`.

Run it from the repo root:

```sh
python3 .claude/private-pages/build.py
```

It is idempotent — it rewrites every page from the vault each run, so re-run it after any
`sync-notes` that touches a Live Session note, then regenerate the index in
`only-accessible-by-url/SECRET-PAGES.md`.

## Why this exists separately from `sync-subject`

`sync-subject` publishes **only** `Pre-Live Session` notes to the public week pages, and that
rule has not changed. This script is the deliberate, separate path for the material that rule
excludes — authorised by Aryan on 2026-08-31, for unlisted pages only.

## What it will not publish, regardless of instruction

These are enforced in code at the top of `build.py` and are not a matter of preference:

- **`LECTURER_NAMES`** — every occurrence is replaced with `[lecturer]`. The repo has a
  never-publish rule on lecturer and classmate names.
- **`IMAGE_WITHHELD`** — an image containing an identifiable person is never emitted. The
  DMBA 6005 Week 3 class slide carries the lecturer's webcam thumbnail, so its seven
  questions are transcribed as text and the PNG stays in the vault.
- **Any image not in `IMAGE_ALT`** renders as a withheld placeholder rather than being
  published unreviewed. **Look at an image before adding it to `IMAGE_ALT`.**
- Live-session **transcripts and class chat logs** never reach the vault at all, so they
  cannot reach these pages. Do not add them.

## Adding a week

Append to `PAGES`. Each entry is `(code, week number, week title, [(heading, vault path)])`.
A note that is empty in the vault renders an honest "nothing was written under it" line —
never generate filler for it.
