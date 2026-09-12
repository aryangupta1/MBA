# Live-session pages and assessment notebooks (access-code gated)

`build.py` renders two kinds of `publish: false` vault material into gated HTML pages, per
subject:

- **Live Session notes** — one page per week at `live/<CODE>-week<N>.html`.
- **Assessment notebooks** (since 2026-09-12) — one page per notebook at
  `live/<CODE>-assessment<N>.html`, e.g. `live/DMBA6008-assessment2.html`.

Plus one index per subject at `live/<CODE>.html`, with two sections: the week cards, then an
**"Assessment notebooks"** section with one card per notebook.

Every page's content is **encrypted at build time** (AES-256-GCM, key from PBKDF2-SHA256
over the access code) and decrypted in the browser after the reader types the code. Week and
assessment pages share one gate: the same code, the same `sessionStorage` unlock per subject
(enter it once and every page of that subject stays open for the tab), and the same "Lock
these pages" button.

Run it from the repo root:

```sh
python3 .claude/private-pages/build.py
```

It needs `node` (the encryption step only — a build-time tool, the site itself still has no
dependencies) and a `.env` in the repo root holding `LIVE_ACCESS_CODE=<code>`. `.env` is
git-ignored and must stay that way. `LIVE_ACCESS_CODE=<throwaway> python3 …/build.py`
overrides it for a browser test; rebuild with the real code before committing.

It is idempotent — it rewrites every page each run — so re-run it after any `sync-notes`
that touches a **Live Session or Assessment** note, then update
`only-accessible-by-url/SECRET-PAGES.md`. A fresh salt and IV are drawn on every run, so the
ciphertext changes even when the content did not; that is expected.

## History

- **2026-08-31** — unlisted plaintext pages under `only-accessible-by-url/`, no gate, by
  Aryan's instruction.
- **2026-09-09** — moved to `live/`, gated with the access code, linked from each hub and
  from `library.html`, on Aryan's instruction. The plaintext pages were deleted.
- **2026-09-12** — assessment notebooks added behind the same gate ("add assessment
  notebooks to the live sessions", Aryan). Discovered from the vault rather than listed;
  the subject index gained an "Assessment notebooks" section; `IMAGE_TRANSCRIBED` and
  `<mention-page>` resolution added.

## Why this exists separately from `sync-subject`

`sync-subject` publishes **only** `Pre-Live Session` notes to the public week pages, and that
rule has not changed. This script is the deliberate, separate path for the material that rule
excludes — Live Session diaries, and Aryan's own assessment working and submitted work
(`type: Assessment`, `publish: false`). Neither appears on any public page; the gate is the
only place they are published.

## What it will not publish, regardless of instruction

These are enforced in code at the top of `build.py` and are not a matter of preference. They
apply to assessment pages exactly as to week pages:

- **`LECTURER_NAMES`** — every occurrence is replaced with `[lecturer]`. The repo has a
  never-publish rule on lecturer and classmate names.
- **`IMAGE_WITHHELD`** — an image containing an identifiable person is never emitted. The
  DMBA 6005 Week 3 class slide carries the lecturer's webcam thumbnail, so its seven
  questions are transcribed as text and the PNG stays in the vault.
- **`IMAGE_FORMULA`** — a formula screenshot is transcribed as text, exactly as the image
  shows it, and the PNG is not published — the same rule as the public week pages.
- **`IMAGE_TRANSCRIBED`** — a screenshot of other text (a table, a rubric) is transcribed
  as HTML, exactly as the image shows it, and the PNG is not published. The same principle
  as `IMAGE_FORMULA`. First use: the DMBA 6008 Assessment 1 rubric — two screenshots of a
  four-criterion High Distinction rubric — rendered as a table.
- **Any image not in `IMAGE_ALT`** renders as a withheld placeholder rather than being
  published unreviewed. **Look at an image before adding it to any of the four tables.**
- Live-session **transcripts and class chat logs** never reach the vault at all, so they
  cannot reach these pages. Do not add them. A wikilink to such an un-harvested page (e.g.
  `[[Live Session Transcript]]` in an assessment `Plan`) renders as its title only — there
  is no content behind it to render.

## Links between notes

- **Wikilinks** render as the target's title.
- **`<mention-page>` links** (Notion page mentions carried into the vault) render as
  `Week › Note`, resolved from each vault note's frontmatter (`notion_id`, `week`, `title`),
  plus `~/MBA/.mba-sync/notebooks.tsv` for notebook mentions. The week is always prefixed
  because bare names like `Learn` and `Live` are ambiguous. They were previously dropped
  silently.

## Tab links

Every gated page — the index, each week, each assessment notebook — opens with one row of
tab links across the whole subject: **All · Week 1 · Week 3 … | Assessment 1 · Assessment 2**,
current page filled in the accent, assessment tabs tinted `--accent-soft`. It is built by
`subject_tabs()` from `PAGES` and the discovered notebooks, so a new week or notebook joins
the row on the next build. Added 2026-09-12 after Aryan asked for the notebooks to sit under
the live tab links rather than only at the bottom of the index. The row scrolls sideways on
its own at narrow widths; the page body never does.

## Adding a week

Append to `PAGES`. Each entry is `(code, week number, week title, [(heading, vault path)])`.
A note that is empty in the vault renders an honest "nothing was written under it" line —
never generate filler for it. The subject index and its "weeks with no live page" list are
derived from `PAGES` and from the `<CODE>-week*.html` files in the repo root.

## Adding an assessment

Nothing to do. Unlike the weeks, assessment notebooks are **discovered, not listed**:
`build.py` finds every vault folder named `Assessment <N> …` under each semester-2 subject
and renders every note in it — top-level notes in created order, each followed by its
sub-pages (the folder beside it), depth-first. A sub-page's heading is `Parent — Child`. A
new notebook appears on the next `build.py` run with no code change, and gets its card in
the subject index's "Assessment notebooks" section. Look at any images it embeds before the
run, though — an unreviewed image renders as a withheld placeholder until it is added to
one of the four tables.
