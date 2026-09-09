# Live-session pages

Every **Live Session** page on this site, grouped by subject. These carry my live-session
notes — the material that is deliberately kept off the public week pages.

**Last updated:** 2026-09-09

> This file still lives in `only-accessible-by-url/` so `robots.txt` covers it. The pages
> themselves moved to **`live/`** on 2026-09-09 and are now **access-code protected**: the
> old unlisted plaintext pages (`<CODE>-week<N>-private.html`) were deleted in the same change.

---

## How these are protected

| Control | Status |
| --- | --- |
| Content encrypted in the file (AES-256-GCM, key from PBKDF2-SHA256 × 310,000 over the access code) | **yes** — every page under `live/` |
| Access code | `LIVE_ACCESS_CODE` in the repo's `.env` (git-ignored); the build reads it, the reader types it once per tab |
| `noindex, nofollow, noarchive, nosnippet` meta tag | on every page |
| `robots.txt` disallow on `/live/` | in place |
| Linked from the site | **yes** — a `Live sessions →` pill and a pinned card on each subject hub, and a `library.html` entry |

> [!note]
> **What the gate does and does not do.** Nothing readable is committed: the page ships a
> ciphertext and a salt, and the browser derives the key from the code you type. Anyone who
> guesses the code can read everything, so its strength is the whole defence. Unlocking one
> page keeps the whole subject open for that tab (`sessionStorage`); **Lock these pages** or
> closing the tab forgets it.

**What is withheld from these pages regardless of the above:** the lecturer's name, any
classmate's name or words, live-session transcripts and class chat logs (never harvested
into the vault at all), any image with an identifiable person in it, and formula screenshots
(transcribed as text, like the public pages).

Rebuild after any `sync-notes` run that touches a Live Session note:

```sh
python3 .claude/private-pages/build.py      # needs node and .env
```

---

## DMBA 6005 — Agile Project Development — `live/DMBA6005.html`

| Week | Page | Notes on it | Flags |
| --- | --- | --- | --- |
| **1** — Project Management | `live/DMBA6005-week1.html` | Class Diary | — |
| **3** — Ideation and Prototyping | `live/DMBA6005-week3.html` | Live | image withheld |
| **4** — Scope and CX | `live/DMBA6005-week4.html` | Live | — |
| **5** — Costing and estimation | `live/DMBA6005-week5.html` | Live, Live Prep — Global Green Books class prep | — |

## DMBA 6008 — Finance, Strategy and Technology — `live/DMBA6008.html`

| Week | Page | Notes on it | Flags |
| --- | --- | --- | --- |
| **1** — Key value principles | `live/DMBA6008-week1.html` | Live Session Diary | lecturer name withheld |
| **2** — Drivers of Returns | `live/DMBA6008-week2.html` | Live, Diary, Discussion Questions | — |
| **3** — Investment Evaluation Tools | `live/DMBA6008-week3.html` | Live, Pre-Class Prep — Gilead investment case | — |
| **4** — Project Evaluation | `live/DMBA6008-week4.html` | Live Session, Prep — Alstonville Limited case, Diary | 1 note empty in vault |
| **6** — Equity hurdle rate and valuation applications | `live/DMBA6008-week6.html` | Live, Live Prep — MedScope Technologies case | 3 formula images transcribed |

Live URLs follow `https://aryangupta1.github.io/MBA/live/<file>`.

---

## Weeks with no live page

- **DMBA 6005 Week 0, Week 2, Week 6** — no Live Session note exists in the vault for these weeks.
- **DMBA 6008 Week 0, Week 5** — same.

A week gets a page the moment a Live Session note appears for it in the vault and
`build.py`'s `PAGES` list is extended.

---

## Other unlisted pages (not live-session material)

Still in this directory, listed here so this file is the complete index:

| Page | What it is | Gate |
| --- | --- | --- |
| [`semester-2-private-notes.html`](semester-2-private-notes.html) | The original hand-built combined private page — semester 2 live sessions and shadow boxing, as at 2026-08-19 | **password** (its own, AES-256-GCM) |
| [`metadata.html`](metadata.html) | Semester 1 artefact | none |
| [`power-interest.html`](power-interest.html) | Semester 1 artefact | none |
| [`stakeholder-mapping.html`](stakeholder-mapping.html) | Semester 1 artefact | none |

The combined page is **stale** — it predates DMBA 6005 Weeks 4–6 and DMBA 6008 Weeks 4–6.
The `live/` pages supersede it; it has not been deleted because rebuilding or removing it
needs its own password.
