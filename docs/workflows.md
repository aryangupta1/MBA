# Workflows

Step-by-step recipes. Each assumes you have read [conventions.md](conventions.md) and
[style-guide.md](style-guide.md).

## Add a reading summary, case study, or assessment overview

1. **Name the file** — `DMBA<code>-<kebab-slug>.html` in the repo root.
2. **Copy the skeleton** from [conventions.md](conventions.md#anatomy-of-a-standalone-page),
   or start from the closest existing page of the same type and replace its content. The
   nearest neighbours:
   - reading summary → `DMBA6001-short-history-of-AI.html`
   - case study with tabs → `DMBA6004-week5-case-study.html`
   - assessment overview → `DMBA6002-Assessment3-Overview.html`
   - infographic → `DMBA6002-Infographic-Anthropomorphic-Agents-PNAS2025.html`
3. **Choose a palette and font pairing** that suits the material, declare it in `:root`,
   and load fonts with a single Google Fonts link.
4. **Write the content.** Prose rules in [content-guide.md](content-guide.md). Do not
   invent citations.
5. **Add a back link** to `library.html?subject=DMBA600X` as the first body element.
6. **Register it in `library.html`** — add `{ title, href, description }` to the right
   array in `articlesBySubject`. *Skipping this makes the page unreachable.*
7. **Check it**: open the file, resize to a phone width, tab through the interactive
   elements, and walk the path `index.html` → library → the page.

## Add a blog post

1. `mkdir -p blogs/blog-<N>/images` where `<N>` is the next number in sequence.
2. Copy `blogs/blog-4/index.html` as the starting point — it is the most complete example
   (figures, references, acknowledgement, microdata).
3. Update in the copy:
   - `<title>` — `<Short title> — DMBA 6001 Blog`
   - `<meta name="description">`
   - `.course-line`, `.post-title` (with `itemprop="headline"`)
   - `.post-meta` — `<span itemprop="datePublished" content="YYYY-MM-DD">DD Mon YYYY</span>`
     plus the topic
   - the `.prose` body, figures, `.references` list, and `.ack` block
4. Add figures to `images/` as `img-000.png`, `img-001.png`, … in document order.
   Reference them with explicit `width`/`height`, `alt`, `loading="lazy"`,
   `decoding="async"`.
5. Add `note.txt` if the figures need a provenance note.
6. **List the post in `blogs/index.html`** — a new `<li class="post-card">` with `<time
   datetime="YYYY-MM-DD">`, the linked `<h2>`, and a one-line summary. Keep the list in
   date order.
7. Drop the submitted PDF at `blogs/blog-<N>/post.pdf` (and `blogs/agup0534-blog-post-<N>.pdf`
   if following the existing pattern).
8. Verify relative paths: shared assets are at `../assets/…` from inside a post directory.
9. Toggle dark mode on the page and re-read it — the theme is shared, so a hard-coded
   colour will be obvious.

## Add an unlisted appendix

1. Create `only-accessible-by-url/<kebab-slug>.html`.
2. Include `<meta name="robots" content="noindex, nofollow, noarchive">`.
3. Confirm `robots.txt` still covers the directory (it does, for both `/MBA/` and root
   paths).
4. **Do not link it** from `index.html`, `library.html`, or any post.
5. Nothing confidential — see [content-guide.md](content-guide.md#unlisted-content-and-privacy).

## Add a new subject

1. New key in `articlesBySubject` in `library.html`, plus the code added to
   `validSubjects`.
2. New `--course-<x>` stripe colour in the `:root` of `index.html`, and a matching
   `.card--<code>` rule.
3. New `<a class="card card--<code>" href="library.html?subject=DMBA<code>">` in the
   `index.html` grid. Use `card--wide` if the count leaves an odd card on the bottom row.
4. Update the subject table in [`../CLAUDE.md`](../CLAUDE.md#what-this-repo-is).

## Change the blog theme

`blogs/assets/blog-theme.css` is shared by the index and all four posts.

1. Make the change with tokens, not literals.
2. Add any new token to **both** `:root` and `[data-theme="dark"]`.
3. Open all five pages (`blogs/index.html` and each `blogs/blog-N/index.html`) in both
   light and dark mode before calling it done.

## Rebuild a subject's master search page

`DMBA<code>-search.html` indexes every term, acronym, formula and flashcard from the
subject's week pages. It is derived from those pages, so **it must be rebuilt whenever any
week page of that subject changes** — a new week, a re-sync, a fixed definition.

1. Make sure the week pages are final first: the script reads their `TERMS`, `ACRONYMS`,
   `FORMULAS` and `CARDS` arrays, so run it after the practice content is spliced.
2. Rebuild:

   ```bash
   python3 .claude/skills/sync-subject/reference/search/build_search.py finance   # or agile, 6008, 6005, all
   ```

   It prints a per-week counts table; every number should equal the week page's own hero
   pills and reference-tab counts. A mismatch means a week page is malformed.
3. `python3 .claude/skills/sync-subject/reference/checks.py DMBA<code>-search.html`.
4. Open it, type a term you know is on a week page, follow its week pill back, and check it
   at 390px. Try the hub's search card too — it lands on the page with `?q=` filled in.
5. No `library.html` edit is needed unless the page is new to the subject; both existing
   search pages are already registered under their hub entries.

## Rebuild the live-session pages

`live/<CODE>-week<N>.html`, `live/<CODE>-assessment<N>.html` and `live/<CODE>.html` are
generated from the vault's Live Session notes and assessment notebooks, encrypted under
`LIVE_ACCESS_CODE` from `.env`. Rebuild after any `sync-notes` run that touches a Live
Session or Assessment note.

1. Confirm `.env` exists in the repo root with `LIVE_ACCESS_CODE=<code>` and that
   `git check-ignore .env` prints it — it must never be committed.
2. If a new week has a Live note, look at every image it embeds first, then append the week
   to `PAGES` in `.claude/private-pages/build.py`. A **new assessment notebook needs no code
   change** — any vault folder named `Assessment <N> …` under a semester-2 subject is
   discovered — but look at its images too. Either way: a formula screenshot goes in
   `IMAGE_FORMULA` (transcribed, exactly), a screenshot of other text such as a rubric in
   `IMAGE_TRANSCRIBED` (transcribed, exactly), a diagram with no person in it in
   `IMAGE_ALT`, anything with an identifiable person in `IMAGE_WITHHELD`.
3. `python3 .claude/private-pages/build.py` (needs `node`). It prints the redactions it
   applied; the 6008 Week 1 lecturer-name redaction should always be there.
4. `grep -c '<img\|prod-files' live/*.html` should print `0` for every file — nothing
   readable ships.
5. Open the subject hub, follow the `Live sessions →` pill, try a wrong code, then the real
   one; open a week page and an assessment page in the same tab and confirm each unlocks
   without asking again, and that the index lists every notebook under "Assessment
   notebooks". WebCrypto needs a secure context, so test over `http://localhost` or the
   live site, not `file://`.
6. Update the tables in `only-accessible-by-url/SECRET-PAGES.md`.

## Modify the hub or the library

`index.html` and `library.html` are the entry path for every reader.

- Keep the fallback behaviour in `library.html`: an unknown `?subject=` resolves to
  `DMBA6002` rather than rendering an empty page.
- Keep `validSubjects` and the keys of `articlesBySubject` in sync.
- After any change, load `library.html` with each subject code **and** with a bad one.

## Preview and publish

```bash
open index.html                     # straight from the filesystem — no server needed
python3 -m http.server 8000         # if you need real URL/query-param behaviour
```

Publishing:

```bash
git status
git add <specific files>
git commit -m "Add DMBA6001 <artefact> page"
git push                            # this publishes to https://aryangupta1.github.io/MBA/
```

There is no staging environment — **a push is a deploy**. Only commit or push when the
user asks.

## Verification checklist

Before reporting a page as done:

- [ ] Opens in a browser with no console errors
- [ ] Readable at ~375px wide, and at desktop width
- [ ] All links resolve; all images load
- [ ] Registered in `library.html` (or `blogs/index.html` for a post)
- [ ] Reachable by walking from `index.html`
- [ ] Focus is visible when tabbing; interactive elements are real buttons/links
- [ ] References and the AI-use acknowledgement are present and accurate
- [ ] `next-prompt.md` updated for the next session
