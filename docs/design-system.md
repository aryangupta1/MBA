# DESK — the house design system

**Status:** live since 2026-08-09. Governs `index.html` and every 2026 Semester 2 page.
**Read this before changing the look of any page it covers.**

---

## 1. The idea

The site is a **desktop**.

A wallpaper of rolling hills under a blue sky is the ground. Content sits on it as **paper**
— pinned, taped, slightly askew — or inside a **macOS window** with traffic lights and an
address bar. A **dock** floats at the foot of every screen and is the site's navigation.

Two rules follow from the metaphor, and they explain most of the decisions below:

1. **A window means "a thing you opened."** A week study page is one window containing the
   whole week. A subject card is a small window you can open. Never nest a window in a
   window.
2. **The pinboard is where things are collected.** Cream, faint graph grid, doodles behind,
   cards rotated a degree or two. If a screen is a list of things, it is a pinboard.

The reference the language was drawn from is a Framer portfolio template (`creatiie`) —
specifically its wallpaper hero, its dock, and the way clicking a project opens a macOS
window over a dimmed desktop. That last move is exactly what a week study page is.

---

## 2. Scope

| Covered | Not covered |
| --- | --- |
| `index.html` | `library.html` |
| `DMBA6008-weeks.html`, `DMBA6005-weeks.html` | every `DMBA6001/6002/6004-*.html` page |
| `DMBA6008-week0/1.html`, `DMBA6005-week0/1.html` | `blogs/` (owns `blogs/assets/`) |
| `.claude/skills/sync-subject/reference/week-shell.html` | `only-accessible-by-url/` |

Semester 1 pages keep the visual identity they were written with — that is a standing
constraint in [`../CLAUDE.md`](../CLAUDE.md), not an oversight. `library.html` says so to
the reader: a `.notice` panel appears at the top of the `DMBA6001`, `DMBA6002` and
`DMBA6004` lists explaining that those pages are preserved as published rather than
restyled. Add a subject to `heritageSubjects` in `library.html` to opt it in; the notice
never shows on a Semester 2 list or on the all-subjects index.

There is still **no build step and no shared stylesheet.** Every page carries the system
inline in its own `<style>` block. That is duplication on purpose: it is what keeps each
page a single openable file. When you change a token, change it in every covered page.

---

## 3. Tokens

Declared on `:root` in each page. Names are stable; treat them as the API.

### Surfaces

| Token | Value | Use |
| --- | --- | --- |
| `--paper` | `#F4F1E9` | the pinboard ground |
| `--paper2` | `#EFEBE1` | a shade down — hero gradients, table headers |
| `--surface` | `#FFFFFF` | cards, windows |
| `--surface2` | `#FBFAF7` | inset panels, the sticky tab strip |
| `--rule` | `rgba(28,26,22,.07)` | the graph grid lines, drawn at **111 px** |
| `--line` / `--line2` | `#E4E0D5` / `#EFEBE2` | hairline borders, strong then soft |

### Ink

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#141317` | headings, body emphasis |
| `--ink2` | `#57534B` | body copy, descriptions |
| `--ink3` | `#8C867A` | captions, counts, hints |

### Accents

`--lime #D6F24E` · `--butter #EDE884` · `--blush #F9DCDC` · `--sky #D7E4F8` ·
`--mint #D1EEDA` · `--lilac #E6DDF3` · `--sand #F2EEBD` · `--pin #E8453C` ·
`--ink-blue #3B6FE0`

Lime is the "yes" colour — primary CTA, progress fill, the folded corner. Butter is the
footer. The five pastels tint list rows, dock tiles and section eyebrows; they carry no
meaning, they just keep a list of five things from looking like a table.

### Window chrome

`--tl-red #FD5D5C` · `--tl-amber #FAC900` · `--tl-green #28C840` — the traffic lights,
lifted from macOS. Always 11 px, always in that order, always `aria-hidden`.

### Subject identity

A subject owns exactly **four** values. Nothing else changes between subjects.

| Subject | `--accent` | `--accent-deep` | `--accent-soft` | `--accent-glow` |
| --- | --- | --- | --- | --- |
| DMBA 6008 Finance | `#2F5470` | `#1F3B51` | `#E9EFF4` | `rgba(47,84,112,.13)` |
| DMBA 6005 Agile | `#A8722C` | `#6F4A17` | `#F7EFE2` | `rgba(168,114,44,.13)` |

Semester-1 hues are kept as `--course-6001/6002/6004` on `index.html` so the archive cards
stay recognisable.

> **Why the accents did not change.** The inline SVG figures inside the week pages hard-code
> their fills as hex literals (`#2f5470`, `#e9eff4`, `#a8722c`, …) — roughly 40–90 per page.
> Keeping each subject's accent hue means every existing figure still harmonises with its
> page. The week pages also alias `--petrol`, `--petrol-deep`, `--petrol-soft` and
> `--petrol-glow` to the `--accent*` values for the same reason. **Do not remove those
> aliases** until the figures are migrated to `var(--…)`.

### Geometry and elevation

`--r-win 24px` (windows) · `--radius-lg 20px` (cards) · `--radius 14px` (small) ·
`--r-pill 999px` · `--bar 46px` (window title bar height — the sticky tab strip offsets from
it) · `--shell 1080–1180px`.

`--sh-win 0 4px 29px rgba(0,0,0,.16)` is the macOS window shadow, measured from the
reference. Stack it with `--sh-card` for lift and `--sh-float` when a window sits over the
wallpaper.

---

## 4. Type

Two families, both from Google Fonts. **No third font, and no per-subject pairing** — that
practice was retired when this system landed.

| Token | Family | Role |
| --- | --- | --- |
| `--font-display` / `--display` | **Mona Sans** | display headings, numerals, dock labels |
| `--font-sans` / `--ui` | **Plus Jakarta Sans** | everything else |
| `--font-mono` | system mono stack | formulas, code, figure numbers |

```html
<link href="https://fonts.googleapis.com/css2?family=Mona+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
```

**The display voice is loud and tight:** weight 800, `text-transform: uppercase`,
`letter-spacing: -.035em`, `line-height: .92`. That treatment belongs to `h1`, section
headings and the footer statement — the things a reader should see from across the room.

**Content headings are not shouted.** Inside a study page, `h2`/`h3`/`h4` use Mona Sans at
700–800 but stay in sentence case with normal line-height. Uppercase a heading someone has
to *read*, and you have made the page worse.

Body is 16 px / 1.62. The `.lede` / `.standfirst` step is `clamp(1rem, 1.7vw, 1.2rem)` at
1.55 and is capped near 48–60ch.

---

## 5. Components

### `.dock` — site navigation

Fixed, centred, bottom 18 px. Glass (`backdrop-filter: blur(22px) saturate(180%)`), 52 px
tiles that lift and scale on hover, a tooltip from `data-label`, tinted by `data-tint`.
`aria-current="page"` rings the current tile.

**Every covered page carries the same dock, in the same order:** Home · Library ‖ 6008 ·
6005 ‖ 6001 · 6002 · 6004. `body` gets `padding-bottom: 104px` (84 px under 600 px) so
content never hides behind it. On phones the tooltips are dropped and the strip scrolls.

### `.wallpaper` — the hero

A CSS-only scene: a sky gradient, three blurred radial clouds, and an inline SVG of four
hill bands. **There are no image files anywhere in this system** — the only external request
on any page is the Google Fonts stylesheet, which is the standing constraint.

Reuse the SVG verbatim (`viewBox="0 0 1440 600"`, `preserveAspectRatio="none"`, four paths
with the `h1`–`h4` gradients). A `::after` radial scrim at ~24 % keeps white type legible
where it crosses the hills.

### `.win` — the macOS window

```html
<div class="win">
  <div class="win-bar">
    <span class="win-lights" aria-hidden="true"><i></i><i></i><i></i></span>
    <span class="win-addr">DMBA 6008 &nbsp;/&nbsp; Week 0 — Fundamentals of financial management</span>
    <span class="win-tool" aria-hidden="true">MBA</span>
  </div>
  …
</div>
```

The address bar states **where you are**, not a decoration — on a subject card it shows the
real href; on a study page it shows subject / week / title.

> **`.win` must not have `overflow: hidden`.** The window title bar and the tab strip are
> `position: sticky` and need the viewport as their scrollport. Corners are rounded on the
> first child (`.win-bar`) and the last (`footer.page-foot`) instead. This is load-bearing;
> adding `overflow:hidden` silently kills both sticky headers.

### Paper: `.paper`, `.week`, `.subject`, `.upcoming`

White, rounded 20–24 px, soft shadow, rotated ±1–2°, straightened and lifted on hover.
Fastened with one of two fasteners, never both:

- **a pin** — a 13–14 px red radial dot at the top edge (`.upcoming`, `.sem-note`)
- **a paperclip** — a `::before` with `border-bottom-color: transparent` hooked over the top
  edge (`.subject`, `.week`, and every `.eyebrow`)

### `.eyebrow` — the section sticker

A strip of tape with a paperclip, rotated −3° to −6°, sitting above a section heading. Tint
it with a pastel or `--accent-soft`. One per section; it names the section in two or three
words so the display heading does not have to.

### Rows and tiles

`.row-tile` / `.mode` — full-width pastel pills with a hard offset shadow
(`6px 6px 0 rgba(20,19,23,.06)`) that slide right on hover. Use for a short list of parallel
things. `.explain-grid` numbers them with a CSS counter, `decimal-leading-zero`.

### Footer

Butter panel, a giant italic Mona Sans watermark drifting behind at
`rgba(255,255,255,.3–.45)`, and one large display statement. The marquee is decorative,
`aria-hidden`, and stops under `prefers-reduced-motion`.

### The fourth tab

A week page carries three tabs by default — Summary & visuals, Key concepts, Flashcards. A
week that has discussion questions gets a fourth, **Discussion**, wired the same way: a
`.tab` with `data-panel="discussion"` and a `<section class="panel" id="panel-discussion">`.
The existing script picks it up with no change, because it maps `data-panel` to
`panel-<value>` generically and its arrow-key handler walks whatever `.tab` elements exist.

`week-shell.html` carries `<!--INSERT:DISCUSSION_TAB-->` and
`<!--INSERT:DISCUSSION_PANEL-->`; a week without discussion questions leaves both empty and
renders three tabs.

> **A `.callout` with more than one paragraph must wrap them in a `<div>`.** `.callout` is a
> flex row, so sibling `<p>` elements lay out *side by side* — three paragraphs render as
> three columns. The rule `.callout > div { flex: 1 1 auto; min-width: 0 }` exists for this.
> Found and fixed on 2026-08-12 after it shipped in seven callouts.

### The summary index — contents, collapse, search

A week's Summary & visuals panel builds its own **index** at load: a `.toc` card holding a
search box, Expand/Collapse-all buttons and a two-column list of every section. Each `.block`
is turned into a `<details class="block-d">` whose `<summary>` is the eyebrow plus the `h2`,
so the whole section folds away behind its own heading.

**It is generated at runtime from the blocks already on the page.** Nothing in the authored
markup changes, which is deliberate and worth preserving:

- the index can never drift out of sync with the content,
- a re-sync inherits it with no extra work,
- `checks.py` still measures exactly the same `.block` elements for the prose budget,
- and with JavaScript off the page reads as it always did — every section open, no index.

**A week longer than 12 sections opens collapsed**, as an outline you pick from; a shorter one
stays open and reads straight through. Searching filters the index and the body together and
auto-expands whatever matches. A week split into topic subpanels gets one index per subpanel;
a subpanel with fewer than four sections gets none, since it navigates fine on its own.

The search reuses the existing `.toolbar` / `.search` / `.count` components rather than
introducing new ones.

### Study-page components

The week pages keep their full component vocabulary and their entire inline script
untouched — `.block` / `.block-num`, `.callout--key` / `--ask`, `.table-scroll`, `.formula`,
`.example`, `.principle`, `.fig-frame`, `.term*`, `.chip`, `.flip` / `.face`, `.verdict--*`.
Only their skin changed. The JS contract is unchanged and is documented in
[`notion-sync.md`](notion-sync.md); the short version:

- `.tab[data-panel]` → `#panel-<value>`, toggling `aria-selected`, `.active` and `hidden`
- `.subtab[aria-controls]` → `#sub-*`, same pattern
- `#flip-card`'s `aria-pressed` is the **only** source of truth for the flip — the 3D
  rotation is pure CSS off that attribute
- filtering hides terms with the `hidden` **attribute**, not a class

Restyling must never change those attributes, ids, or the `.tab` / `.panel` / `.term` /
`.flip` / `.face-*` class names.

---

## 6. The three page profiles

Each covered page is one of three shapes.

| Profile | Pages | Shape |
| --- | --- | --- |
| **Desktop** | `index.html` | wallpaper hero → pinboard of subject windows → butter footer → dock |
| **Folder** | `DMBA60xx-weeks.html` | wallpaper hero (subject identity) → pinboard of week windows → mode explainer rows → butter footer → dock |
| **Open window** | `DMBA60xx-weekN.html` | fixed dimmed wallpaper → back pill → one window holding hero, sticky tabs, content, footer → dock |

The **Open window** profile is the one the reference's project detail inspired: content
floats over a darkened desktop (`.desk` with a `linear-gradient(rgba(10,20,34,.34–.5))`
scrim and a 1.5 px blur on the hills) so the white window reads as focused.

---

## 7. Motion

Transitions are 0.18–0.34 s on `cubic-bezier(.2,.9,.3,1.15)`, or `(.2,.9,.3,1.3)` for the
dock's overshoot. Entrances use `fade-up` — 10–16 px and 0.45 s. Nothing loops except the
status dot's `ping` and the footer marquee's `drift`.

Every covered page ends its stylesheet with the same global reduced-motion block. It is not
optional.

---

## 8. Accessibility

- `:focus-visible` → `3px solid var(--ink-blue)`, offset 3 px, switched to `--ink` over the
  wallpaper and the butter footer.
- A `.skip` link is the first element in `<body>` on every covered page.
- Decoration is `aria-hidden`: doodles, hill SVGs, traffic lights, the footer marquee, the
  arrow glyphs, the `MBA` window tool.
- Dock tiles that show a glyph carry an `.sr-only` label; tiles that show a subject number
  do not need one.
- Verified at **390 px with zero horizontal overflow** on all three profiles. Wide content —
  tables, figures, formulas — scrolls inside its own `overflow-x: auto` frame; the page body
  never does.

---

## 9. Adding or changing a page

1. **Pick a profile** from §6 and copy that page's `<style>` block wholesale. Do not
   hand-write a variant.
2. **Change only the four `--accent*` values** if it is a new subject. If you find yourself
   changing a second token, you are making a new design, not using this one — stop and ask.
3. **Ship the dock** with the standard order, and `body { padding-bottom: 104px }`.
4. **Register the page in `library.html`** — `articlesBySubject` *and* `validSubjects`. A
   page that is not registered is unreachable.
5. **Verify**: open it, check it at 390 px, walk the path a reader takes
   (`index.html` → subject → week), and confirm every relative link resolves.

A new week page is generated, not hand-written: the `sync-subject` skill copies
`reference/week-shell.html`, which already carries this system, and fills
`{{ACCENT}}` / `{{ACCENT_DEEP}}` / `{{ACCENT_SOFT}}` / `{{ACCENT_GLOW}}` from
`subjects.json` → `palette`. `{{FONT_HREF}}` is the house link and is the same for every
subject.

---

## 10. Relationship to `style-guide.md`

[`style-guide.md`](style-guide.md) documents the **older** house language — the warm
`#f5f3ee` paper, the `--course-a…e` stripes, Syne/DM Sans and the per-subject font pairings.
It still governs `library.html`, the Semester 1 artefact pages and the `blogs/` sub-site.

**Where the two disagree about a page listed in §2, this document wins.**
