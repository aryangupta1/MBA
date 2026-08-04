# Style guide

## The governing principle

**Shared surfaces are consistent; artefact pages are individual.**

- `index.html`, `library.html`, and `blogs/assets/blog-theme.css` are the house style.
  Changes there are changes to the whole site — make them deliberately and check every
  page they touch.
- Each standalone artefact page picks a palette and font pairing that suits its material.
  A page about the history of AI reads as an archival document; a Giant Swarm case study
  reads as a dark technical brief. **This is a feature.** Do not homogenise existing pages.

What *is* universal is the mechanics below: token discipline, responsive behaviour,
accessibility, and restraint with motion.

## House palette (shared surfaces)

Used by `index.html` and `library.html`.

| Token | Value | Role |
| --- | --- | --- |
| `--accent` | `#C23B22` | Primary accent, links, emphasis (USyd-adjacent red) |
| `--bg` / `--bg1` | `#F7F5F0` / `#f0ece4` | Page background, warm paper |
| `--bg0` | `#e8e4db` | Deeper background for gradients |
| `--surface` | `#FFFFFF` / `#fffcf7` | Cards, panels |
| `--ink` | `#1A1916` / `#141210` | Primary text |
| `--ink2` | `#4A4840` | Secondary text |
| `--ink3` | `#8A877E` | Muted text, eyebrows, captions |
| `--border` | `#E2DED6` | Hairlines |
| `--course-a` | `#1f5c4b` | DMBA 6001 stripe (green) |
| `--course-b` | `#b83822` | DMBA 6002 stripe (red) |
| `--course-c` | `#6b6560` | DMBA 6004 stripe (grey) |

Fonts: **Syne** (600–800) for headings, labels, and codes; **DM Sans** (300–500) for body.

## Blog palette (`blogs/assets/blog-theme.css`)

Light/dark pair driven by `[data-theme="dark"]` on `<html>`, toggled by
`blogs/assets/theme.js` and persisted to `localStorage` under `dmba-blog-theme`. It also
respects `prefers-color-scheme` on first visit.

| Token | Light | Dark |
| --- | --- | --- |
| `--bg` | `#fafafa` | `#0b0f14` |
| `--bg-elev` | `#ffffff` | `#111827` |
| `--text` | `#23262d` | `#e5e7eb` |
| `--text-muted` | `#6b7280` | `#9ca3af` |
| `--border` | `#e5e7eb` | `#1f2937` |
| `--accent` | `#2563eb` | `#60a5fa` |
| `--accent-hover` | `#1d4ed8` | `#93c5fd` |

Fonts: **IBM Plex Sans** for prose, **IBM Plex Mono** for metadata, nav, and captions.
Measure is capped at `--measure: 65ch`.

If you add a colour to the blog theme, add it to **both** blocks. A token defined only in
`:root` silently keeps its light value in dark mode.

## Token discipline

Every page declares its palette in `:root` and refers to it by name.

```css
:root {
  --paper: #faf7f2;
  --ink: #2a2a2a;
  --accent: #E64626;
  --radius: 16px;
  --font-display: 'Fraunces', serif;
}
```

- Name tokens by **role** (`--ink2`, `--surface`, `--accent`), not by appearance
  (`--dark-grey`, `--orange`).
- Pages that need a per-component override use a local custom property with a default:
  `.card { --stripe: var(--accent); }` then `.card--6001 { --stripe: var(--course-a); }`.
- `rgba()` literals are fine for shadows and glazes; keep them next to the token they
  derive from.

## Typography

- **Pair a display face with a text face.** Existing pairings: Syne + DM Sans (hub),
  IBM Plex Sans + Mono (blog), Playfair Display + IBM Plex (history), Fraunces + Spline
  Sans (assessment overview), DM Serif Display + DM Mono + Syne (case study).
- Load fonts through a **single** Google Fonts `<link>` with `&display=swap`, requesting
  only the weights actually used. Add `<link rel="preconnect">` for
  `fonts.googleapis.com` and `fonts.gstatic.com` (crossorigin).
- Always end a font stack with a system fallback:
  `'DM Sans', system-ui, -apple-system, sans-serif`.
- Body text 14–16px, line-height 1.5–1.7. Prose measure 60–70ch.
- Headings: negative tracking (`letter-spacing: -0.02em` to `-0.035em`), line-height
  1.1–1.35.
- Eyebrows and labels: uppercase, `letter-spacing: 0.12em–0.18em`, 0.58–0.7rem, weight
  600–700, in the muted ink.
- Fluid display sizes: `font-size: clamp(2rem, 5.5vw, 2.75rem)`.

## Layout

- Content column: `max-width` 640–880px for text-led pages, wider only for dashboards and
  maps. Blog measure is 720px wrap / 65ch prose.
- Fluid padding: `padding: clamp(1.35rem, 4vw, 2.5rem)`.
- CSS Grid for card layouts, Flexbox for rows and headers. No floats, no frameworks.
- **Mobile-first**: write the single-column rules, then widen with `min-width` media
  queries. Common breakpoints in use: 480px, 520px, 560px, 700px, 768px.
- Radii: 8–12px for small elements, 16px for cards, 22px for hero panels. Reuse one
  `--radius` token per page rather than picking new numbers.

## Components

Patterns already established — reach for these before inventing new ones.

**Card with a colour stripe** (`index.html`) — a `::before` pseudo-element 3px wide, inset
12px top and bottom, coloured by a `--stripe` custom property.

**Eyebrow + title header** — small uppercase tracked label above a large display heading,
often with a rule or gradient bar beneath.

**Meta pills** — small rounded chips carrying course code, week, or artefact type.

**Callouts** — left border 3px in the accent colour, tinted background, used for key
claims and acknowledgements (`.ack`, `.callout`).

**Tabbed panels** (`DMBA6004-week5-case-study.html`) — `.q-tab` buttons toggling
`.q-panel.active`, driven by a few lines of inline JS.

**Figures** — `<figure class="figure">` with a bordered container, full-width image, and a
monospace `<figcaption>` separated by a top border.

**References list** — `<section class="references">` with a dashed top border, `<h2>`, and
an ordered list in muted text.

## Motion

- Transitions 0.2–0.3s with `ease` or `cubic-bezier(0.22, 1, 0.36, 1)`.
- Entry animations are subtle: 8–12px translate plus fade, staggered 60–80ms across
  sibling cards.
- Hover on cards: `translateY(-2px to -3px)` plus a deeper shadow. Nothing that shifts
  layout.
- **Always honour reduced motion:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Accessibility

Non-negotiable on every page:

- `lang="en"` on `<html>`; a meaningful `<title>`.
- Body text contrast at or above 4.5:1 against its background; muted text at or above 3:1
  and reserved for secondary information.
- Visible focus: `:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }`
  — never `outline: none` without a replacement.
- Decorative elements marked `aria-hidden="true"`.
- Nav landmarks labelled: `aria-label="Primary"`, `aria-labelledby` pointing at the
  section heading, `aria-current="page"` on the active link.
- A skip link on pages with a header (`<a class="skip" href="#main">Skip to content</a>`) —
  see `.skip` in `blog-theme.css`.
- Every `<img>` has an `alt`; decorative images get `alt=""`.
- Interactive controls are real `<button>` or `<a>` elements, never a clickable `<div>`.
- Heading levels descend without skipping.
- Reduced-motion block as above.

## Performance

- Inline the page's CSS — that is the whole point of the self-contained format. Do not
  add a stylesheet request to a standalone page.
- Only external requests are the Google Fonts stylesheet (and, on blog pages,
  `../assets/*`).
- Images: explicit `width`/`height` to reserve space, `loading="lazy"` and
  `decoding="async"` below the fold. Keep PNGs reasonable — under ~500KB.
- Prefer CSS gradients, `box-shadow`, and inline SVG data URIs over image assets for
  decoration.
