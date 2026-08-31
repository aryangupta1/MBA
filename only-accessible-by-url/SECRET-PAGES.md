# Secret live pages

Every **Live Session** page on this site, grouped by subject. These carry my live-session
notes — the material that is deliberately kept off the public week pages.

**Last updated:** 2026-08-31

> This file lives in `only-accessible-by-url/` on purpose: `robots.txt` disallows this
> whole directory, so an index of unlisted URLs is not itself served as a public page.

---

## How these are protected

| Control | Status |
| --- | --- |
| `noindex, nofollow, noarchive, nosnippet` meta tag | on every page |
| `robots.txt` disallow on `/only-accessible-by-url/` | in place |
| Linked from `index.html`, `library.html` or any week page | **no** — nowhere |
| Password gate | **no** — unlisted URL only |

> [!warning]
> **Unlisted is not private.** These pages are plain HTML in a public GitHub repository.
> Anyone browsing `github.com/aryangupta1/MBA` can read them without ever needing the URL,
> and search engines only stay away because they choose to honour `robots.txt`.
> If you want these genuinely closed, they need the password gate that
> `semester-2-private-notes.html` uses — ask and I'll convert them.

**What is withheld from these pages regardless of the above:** the lecturer's name, any
classmate's name or words, live-session transcripts and class chat logs (never harvested
into the vault at all), and one class slide carrying the lecturer's webcam thumbnail.

---

## DMBA 6005 — Agile Project Development

| Week | Page | Notes on it | Flags |
| --- | --- | --- | --- |
| **1** — Project Management | [`DMBA6005-week1-private.html`](DMBA6005-week1-private.html) | Class Diary | — |
| **3** — Ideation and Prototyping | [`DMBA6005-week3-private.html`](DMBA6005-week3-private.html) | Live | image withheld |
| **4** — Scope and CX | [`DMBA6005-week4-private.html`](DMBA6005-week4-private.html) | Live | — |
| **5** — Costing and estimation | [`DMBA6005-week5-private.html`](DMBA6005-week5-private.html) | Live, Live Prep — Global Green Books class prep | — |

Live URLs:

- Week 1 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6005-week1-private.html>
- Week 3 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6005-week3-private.html>
- Week 4 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6005-week4-private.html>
- Week 5 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6005-week5-private.html>

## DMBA 6008 — Finance, Strategy and Technology

| Week | Page | Notes on it | Flags |
| --- | --- | --- | --- |
| **1** — Key value principles | [`DMBA6008-week1-private.html`](DMBA6008-week1-private.html) | Live Session Diary | lecturer name withheld |
| **2** — Drivers of Returns | [`DMBA6008-week2-private.html`](DMBA6008-week2-private.html) | Live, Diary, Discussion Questions | — |
| **3** — Investment Evaluation Tools | [`DMBA6008-week3-private.html`](DMBA6008-week3-private.html) | Live, Pre-Class Prep — Gilead investment case | — |
| **4** — Project Evaluation | [`DMBA6008-week4-private.html`](DMBA6008-week4-private.html) | Live Session, Prep — Alstonville Limited case, Diary | 1 note empty in vault |

Live URLs:

- Week 1 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6008-week1-private.html>
- Week 2 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6008-week2-private.html>
- Week 3 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6008-week3-private.html>
- Week 4 — <https://aryangupta1.github.io/MBA/only-accessible-by-url/DMBA6008-week4-private.html>

---

## Weeks with no live page

- **DMBA 6005 Week 0, Week 2** — no Live Session note exists in the vault for these weeks.
- **DMBA 6008 Week 0** — same.

A week gets a page here the moment a Live Session note appears for it in the vault.

---

## Other unlisted pages (not live-session material)

Also in this directory, listed here so this file is the complete index:

| Page | What it is | Gate |
| --- | --- | --- |
| [`semester-2-private-notes.html`](semester-2-private-notes.html) | The original hand-built combined private page — semester 2 live sessions and shadow boxing, as at 2026-08-19 | **password** (AES-256-GCM) |
| [`metadata.html`](metadata.html) | Semester 1 artefact | none |
| [`power-interest.html`](power-interest.html) | Semester 1 artefact | none |
| [`stakeholder-mapping.html`](stakeholder-mapping.html) | Semester 1 artefact | none |

The combined page is now **stale** — it predates DMBA 6005 Weeks 4 and 5, DMBA 6008 Week 4,
and the Week 3 IRR-vs-NPV material. The per-week pages above supersede it, but it has not
been deleted because rebuilding or removing it needs its password.

