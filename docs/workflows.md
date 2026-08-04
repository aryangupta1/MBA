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
