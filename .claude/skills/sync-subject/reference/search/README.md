# The master search page

One page per live semester-2 subject — `DMBA<code>-search.html` — that indexes every
**term, acronym, formula and flashcard** from every published week page of that subject,
so a definition is one search box away instead of a week-page guess and a tab.

**It is derived from the built week pages, not synced from anything.** Like the
`practice/` components, nothing in this folder reads the vault or Notion. The only input
is the four JS arrays each week page already carries — `TERMS`, `ACRONYMS`, `FORMULAS`,
`CARDS` — so the search page can never state something a week page does not.

## Build it

From the repo root:

```
python3 .claude/skills/sync-subject/reference/search/build_search.py            # every live subject
python3 .claude/skills/sync-subject/reference/search/build_search.py finance    # one subject, by code or alias
python3 .claude/skills/sync-subject/reference/search/build_search.py 6005 --dry-run   # counts only, writes nothing
python3 .claude/skills/sync-subject/reference/search/build_search.py 6008 --json      # the data object, for inspection
```

`--out DIR` writes somewhere other than the repo root. The script prints a per-week
counts table; those numbers should equal the week page's own hero pills and reference-tab
counts, and a mismatch means a week page is malformed, not that the index is wrong.

**This is binding on every re-sync:** a run that adds or rebuilds a week page must re-run
this afterwards, or the index silently lags the weeks. It is idempotent and takes a second.

`node` is used at build time to evaluate the pages' JS array literals (they are
JavaScript, not JSON — unquoted keys, single quotes, and `[].concat(tag(...))` on the
multi-topic pages). It is a machine tool on the author's Mac, like `sips` for images; the
site itself still ships with no dependencies and the generated page is one self-contained
HTML file.

## The data contract

The page's script receives one object at `/*SEARCH_DATA*/…/*END_SEARCH_DATA*/`:

```jsonc
{
  "subject": {"code":"DMBA6008","spaced":"DMBA 6008","name":"Finance, Strategy and Technology","hub":"DMBA6008-weeks.html"},
  "built": "2026-09-07",
  "weeks": [{"n":0,"title":"Fundamentals of financial management","href":"DMBA6008-week0.html",
             "counts":{"term":107,"acronym":23,"formula":86,"card":146}}],
  "entries": [
    {"t":"term",    "w":0,"name":"Balance Sheet","src":"Summing up the balance sheet","topic":"The Balance Sheet","def":"…","formula":"Assets = …","own":true},
    {"t":"acronym", "w":4,"abbr":"NPV","long":"Net Present Value","src":"Recap of NPV","def":"…"},
    {"t":"formula", "w":4,"name":"Present value of a future cash flow","expr":"PV = CFt / (1 + r)^t","src":"Recap of NPV","def":"…"},
    {"t":"card",    "w":4,"q":"…","a":"…","topic":"…"}
  ]
}
```

Keys with no value are omitted (`topic` only exists on the multi-topic weeks; `own` only on
a term from Aryan's own *Key Definitions*, which then has no `src`). Source order is kept
within a week; weeks ascend. Text is verbatim from the week page — the same rule as
everywhere else: no formula is repaired, no typo tidied.

Template placeholders the script fills: `{{ACCENT}} {{ACCENT_DEEP}} {{ACCENT_SOFT}}
{{ACCENT_GLOW}} {{FONT_HREF}}` (from `subjects.json`), `{{SUBJECT_CODE}}
{{SUBJECT_CODE_SPACED}} {{SUBJECT_NAME}} {{HUB_PAGE}} {{WEEK_COUNT}} {{WEEK_RANGE}}
{{TERM_COUNT}} {{ACRONYM_COUNT}} {{FORMULA_COUNT}} {{CARD_COUNT}} {{ENTRY_COUNT}}
{{BUILD_DATE}} {{DOCK_CURRENT_6008}} {{DOCK_CURRENT_6005}}`. A leftover `{{…}}` fails the build.

## The page

The template is `search-shell.html` in this folder. It is an **Open window** page in the
DESK system (`docs/design-system.md` §5, "The master search page"): the fixed dimmed desk,
a back pill to the hub, and one window holding the hero, a sticky search bar, the results,
a short "How it works" block and the butter footer, with the standard dock underneath and
the subject's tile ringed `aria-current="page"`.

### Where the stylesheet came from

The `<style>` block is the week shell's, **sliced**: the tokens, `.term*`, `.toolbar` /
`.search` / `.count`, `.subtab`, `.btn`, the footer, the dock and the accessibility rules —
followed by the search additions. There is still no shared stylesheet, by rule, so **when a
token or one of those components changes in `week-shell.html`, make the same change here by
hand** (or re-slice). The four `{{ACCENT*}}` placeholders are the only per-subject knobs,
exactly as on a week page.

### What it renders

- **The sticky `.searchbar`** sits under the window title bar the way a week's `.tabs`
  strip does. It holds the search box and count, and three groups of `.subtab[aria-pressed]`
  chips: **type** (Everything · Key concepts · Acronyms · Formulas · Flashcards, each with its
  count), **week**, and **order** (A to Z · By week).
- **On a phone (≤ 600 px) the three chip rows fold behind a `.facets-toggle` button** that
  names the current selection ("Everything · All weeks · A to Z"); open, they made the sticky
  bar ~320 px tall on an 844 px screen. `aria-expanded` on the button, `.facets-open` on the
  bar.
- **Browsing A to Z with no query** draws a `.letters` thumb index (letters with no entries
  disabled) and a `.letter-head` between groups. Clicking a letter renders the whole list
  and scrolls to it.
- **Each result is a `.term` card** with a `.term-meta` row — the kind label, a `.term-week`
  pill linking to the week page, `Key Definitions` (`.term-src--own`) where the week page
  tags a term that way, and the source topic — then the heading, definition, formula or
  expansion using the week pages' own `.term-name` / `.term-def` / `.term-formula` /
  `.term-abbr` / `.term-long`.
- **A heading that appears in more than one week is one card** (`.senses`, one `.sense` per
  week, weeks ascending). Flashcards are only merged if the question is identical.
- **Flashcard answers sit behind a `.reveal` disclosure**, the same one the Quiz tab uses,
  so the page works for recall as well as lookup.
- Matches are wrapped in `<mark>`. Results render **80 groups at a time**; `.more` appends
  the next 80.
- `/` focuses the box, `Esc` clears it. The state — `q`, `type`, `week`, `order` — is
  mirrored to the address bar with `replaceState`, so a lookup can be bookmarked and the
  hub's `.lookup` form (`GET ?q=`) lands on live results.

### Matching and ranking

Every whitespace-separated token in the query must match somewhere in the entry (heading,
expansion or formula, definition, answer, source, topic — folded to lower case with curly
quotes and dashes normalised). Score per token: a hit at the **start of the heading** beats
a hit at a **word boundary inside it**, beats one **elsewhere in the heading**, beats one in
the **expansion or formula**, beats one in the **definition**. An exact heading match gets a
bonus; a flashcard loses half a point on ties so glossary entries surface first. With no
query, the order chip decides.

### Wiring

- `library.html` registers each search page directly under its hub entry.
- Each hub carries a `.lookup` search card and a `Master search →` hero pill.
- Each week page carries a second back pill, `.back--search` ("Search all weeks"). In
  `week-shell.html` that href is **`{{SEARCH_PAGE}}`**, filled by the sync from
  `subjects.json` → `searchPage` (Phase 4). A shipped page must never contain the literal
  placeholder.

The page adds **no content of its own**. If an entry is wrong here, it is wrong on the week
page, and that is where it gets fixed — then rebuild.
