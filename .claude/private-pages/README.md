# Live-session pages (access-code gated)

`build.py` renders the Obsidian vault's **Live Session** notes into one HTML page per week,
per subject, at `live/<CODE>-week<N>.html`, plus one index per subject at `live/<CODE>.html`.
Every page's content is **encrypted at build time** (AES-256-GCM, key from PBKDF2-SHA256
over the access code) and decrypted in the browser after the reader types the code.

Run it from the repo root:

```sh
python3 .claude/private-pages/build.py
```

It needs `node` (the encryption step only — a build-time tool, the site itself still has no
dependencies) and a `.env` in the repo root holding `LIVE_ACCESS_CODE=<code>`. `.env` is
git-ignored and must stay that way. `LIVE_ACCESS_CODE=<throwaway> python3 …/build.py`
overrides it for a browser test; rebuild with the real code before committing.

It is idempotent — it rewrites every page each run — so re-run it after any `sync-notes`
that touches a Live Session note, then update `only-accessible-by-url/SECRET-PAGES.md`.
A fresh salt and IV are drawn on every run, so the ciphertext changes even when the content
did not; that is expected.

## History

- **2026-08-31** — unlisted plaintext pages under `only-accessible-by-url/`, no gate, by
  Aryan's instruction.
- **2026-09-09** — moved to `live/`, gated with the access code, linked from each hub and
  from `library.html`, on Aryan's instruction. The plaintext pages were deleted.

## Why this exists separately from `sync-subject`

`sync-subject` publishes **only** `Pre-Live Session` notes to the public week pages, and that
rule has not changed. This script is the deliberate, separate path for the material that rule
excludes.

## What it will not publish, regardless of instruction

These are enforced in code at the top of `build.py` and are not a matter of preference:

- **`LECTURER_NAMES`** — every occurrence is replaced with `[lecturer]`. The repo has a
  never-publish rule on lecturer and classmate names.
- **`IMAGE_WITHHELD`** — an image containing an identifiable person is never emitted. The
  DMBA 6005 Week 3 class slide carries the lecturer's webcam thumbnail, so its seven
  questions are transcribed as text and the PNG stays in the vault.
- **`IMAGE_FORMULA`** — a formula screenshot is transcribed as text, exactly as the image
  shows it, and the PNG is not published — the same rule as the public week pages.
- **Any image not in `IMAGE_ALT`** renders as a withheld placeholder rather than being
  published unreviewed. **Look at an image before adding it to any of the three tables.**
- Live-session **transcripts and class chat logs** never reach the vault at all, so they
  cannot reach these pages. Do not add them.

## Adding a week

Append to `PAGES`. Each entry is `(code, week number, week title, [(heading, vault path)])`.
A note that is empty in the vault renders an honest "nothing was written under it" line —
never generate filler for it. The subject index and its "weeks with no live page" list are
derived from `PAGES` and from the `<CODE>-week*.html` files in the repo root.
