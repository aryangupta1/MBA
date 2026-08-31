#!/usr/bin/env python3
"""Build the unlisted per-week Live Session pages from the Obsidian vault.

These pages carry publish:false material by Aryan's explicit instruction
(2026-08-31): one hidden page per week, unlisted URL, no password gate.
Third-party material is withheld regardless of that instruction.
"""
import os, re, html, json, sys

VAULT = os.path.expanduser("~/MBA/Semester 2 2026")
OUT   = "only-accessible-by-url"

# ── Redactions applied to every note, no exceptions ───────────────────────────
# The repo has a never-publish rule on lecturer and classmate names.
LECTURER_NAMES = ["Guy"]

# The Week 3 slide is a class slide with the lecturer's webcam thumbnail in the
# corner. Its seven questions are transcribed instead; the image is not published.
IMAGE_WITHHELD = {
  "3bf7b336873c8061b545e1b5340877d7-01-image.png": {
    "why": "This is a class slide with the lecturer's webcam thumbnail in the corner. "
           "The slide's seven questions are transcribed below; the image itself is withheld.",
    "transcript": ["Test a Personas Role Play — 7 Questions",
      "1. Do they own a watch? Which type or brand?",
      "2. Do they have Private Health Care?",
      "3. Do they own a car? Which year and model?",
      "4. Do they train and actively keep fit?",
      "5. Do they care about status symbols?",
      "6. Would they care about the environment?",
      "7. If they watched TV … Formula 1 or Women’s Cricket"],
  },
}
# Genuine diagrams with no people in them, safe to publish.
IMAGE_ALT = {
  "3b37b336873c8016b48ce3c9c9787cf0-01-image.png":
    "A flow diagram. Assets lead to revenue and revenue to profit; those three feed ROA. "
    "Separately risk and capital structure feed WACC. ROA and WACC meet at the test "
    "ROA greater than WACC, which answers ‘Is value created?’, and that leads on to NPV, "
    "which answers ‘How much value?’.",
}

PAGES = [
  # code, week no, week title, [(heading, relative path)], note
  ("DMBA6005", 1, "Project Management", [
      ("Class Diary", "DMBA6005 Agile Project Development/Week1 Project Management/Class Diary.md")]),
  ("DMBA6005", 3, "Ideation and Prototyping", [
      ("Live", "DMBA6005 Agile Project Development/Week 3 Ideation and Prototyping/Live.md")]),
  ("DMBA6005", 4, "Scope and CX", [
      ("Live", "DMBA6005 Agile Project Development/Week 4 Scope and CX/Live.md")]),
  ("DMBA6005", 5, "Costing and estimation", [
      ("Live", "DMBA6005 Agile Project Development/Week 5 Costing and importance of project estimation/Live.md"),
      ("Live Prep — Global Green Books class prep", "DMBA6005 Agile Project Development/Week 5 Costing and importance of project estimation/Live/Live Prep.md")]),
  ("DMBA6008", 1, "Key value principles", [
      ("Live Session Diary", "DMBA6008 Finance, Strategy and Technology/Week 1 Key value principles/Live Session Diary.md")]),
  ("DMBA6008", 2, "Drivers of Returns", [
      ("Live", "DMBA6008 Finance, Strategy and Technology/Week 2 Drivers of Returns/Live.md"),
      ("Diary", "DMBA6008 Finance, Strategy and Technology/Week 2 Drivers of Returns/Live/Diary.md"),
      ("Discussion Questions", "DMBA6008 Finance, Strategy and Technology/Week 2 Drivers of Returns/Live/Discussion Questions.md")]),
  ("DMBA6008", 3, "Investment Evaluation Tools", [
      ("Live", "DMBA6008 Finance, Strategy and Technology/Week 3 Investment Evaluation Tools/Live.md"),
      ("Pre-Class Prep — Gilead investment case", "DMBA6008 Finance, Strategy and Technology/Week 3 Investment Evaluation Tools/Live/Pre-Class Prep.md")]),
  ("DMBA6008", 4, "Project Evaluation", [
      ("Live Session", "DMBA6008 Finance, Strategy and Technology/Week 4 Project Evaluation/Live Session.md"),
      ("Prep — Alstonville Limited case", "DMBA6008 Finance, Strategy and Technology/Week 4 Project Evaluation/Live Session/Prep.md"),
      ("Diary", "DMBA6008 Finance, Strategy and Technology/Week 4 Project Evaluation/Live Session/Diary.md")]),
]

SUBJ = {
  "DMBA6005": dict(name="Agile Project Development", spaced="DMBA 6005", hub="DMBA6005-weeks.html",
                   accent="#A8722C", deep="#6F4A17", soft="#F7EFE2"),
  "DMBA6008": dict(name="Finance, Strategy and Technology", spaced="DMBA 6008", hub="DMBA6008-weeks.html",
                   accent="#2F5470", deep="#1F3B51", soft="#E9EFF4"),
}

REDACTED = []

def strip_fm(t):
    if t.startswith("---"):
        parts = t.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return t

def redact(text, where):
    for name in LECTURER_NAMES:
        new, n = re.subn(r"\b%s\b" % re.escape(name), "[lecturer]", text)
        if n:
            REDACTED.append(f"{where}: lecturer name withheld ({n}x)")
            text = new
    return text

def _emphasise(text):
    """Balanced emphasis. His notes overlap runs like ***a **b** c***, which a naive
    regex turns into crossed tags, so toggle against a stack and always close cleanly."""
    out, stack = [], []
    def toggle(tag):
        if tag in stack:
            above = []
            while stack[-1] != tag:
                t = stack.pop(); out.append("</%s>" % t); above.append(t)
            stack.pop(); out.append("</%s>" % tag)
            for t in reversed(above):
                stack.append(t); out.append("<%s>" % t)
        else:
            stack.append(tag); out.append("<%s>" % tag)
    i = 0
    while i < len(text):
        if text[i] == "*":
            n = 0
            while i + n < len(text) and text[i + n] == "*":
                n += 1
            if n >= 3:   toggle("strong"); toggle("em")
            elif n == 2: toggle("strong")
            else:        toggle("em")
            i += n
        else:
            out.append(text[i]); i += 1
    while stack:
        out.append("</%s>" % stack.pop())
    return "".join(out)

def inline(s):
    s = html.escape(s, quote=False)
    # restore the underline tags the notes use deliberately
    s = s.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")
    s = re.sub(r"&lt;mention-page url=&quot;[^&]*&quot;\s*/&gt;", "", s)
    s = re.sub(r"&lt;mention-page url=\"[^\"]*\"\s*/&gt;", "", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[\[([^\]|]+?)\]\]", r"<span class='wl'>\1</span>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" rel="noopener">\1</a>', s)
    return _emphasise(s)

def img_block(fname):
    if fname in IMAGE_WITHHELD:
        w = IMAGE_WITHHELD[fname]
        lines = "".join("<li>%s</li>" % html.escape(x) for x in w["transcript"][1:])
        return ('<div class="withheld"><p class="withheld-why"><strong>Image withheld.</strong> %s</p>'
                '<p class="withheld-title">%s</p><ol class="withheld-list">%s</ol></div>'
                % (html.escape(w["why"]), html.escape(w["transcript"][0]), lines))
    alt = IMAGE_ALT.get(fname, "")
    if not alt:
        return '<div class="withheld"><p class="withheld-why"><strong>Image withheld</strong> — not reviewed for publication.</p></div>'
    return ('<figure class="fig"><img src="../assets/notes/private/%s" alt="%s">'
            '<figcaption>%s</figcaption></figure>' % (html.escape(fname), html.escape(alt), html.escape(alt)))

def md(text):
    """Small markdown renderer for these notes. Tabs mark list nesting."""
    out, i = [], 0
    lines = text.split("\n")
    list_stack = []   # list of (depth, tag)

    def close_lists(to_depth=-1):
        while list_stack and list_stack[-1][0] > to_depth:
            out.append("</%s>" % list_stack.pop()[1])

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        if not line.strip():
            close_lists(); i += 1; continue

        # callout:  > [!note] emoji   then following "> " lines
        m = re.match(r"^>\s*\[!(\w+)\]\s*(.*)$", line)
        if m:
            close_lists()
            body = []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            out.append('<div class="callout"><p>%s</p></div>' % inline(" ".join(x.strip() for x in body if x.strip())))
            continue

        if line.startswith(">"):
            close_lists()
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(x.strip() for x in body if x.strip())))
            continue

        if re.match(r"^-{3,}$", line.strip()):
            close_lists(); out.append("<hr>"); i += 1; continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_lists()
            lvl = min(len(m.group(1)) + 1, 6)
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl)); i += 1; continue

        # table
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i+1]):
            close_lists()
            def cells(r): return [c.strip() for c in r.strip().strip("|").split("|")]
            head = cells(line); i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            t = ['<div class="tbl"><table><thead><tr>']
            t += ["<th>%s</th>" % inline(c) for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue

        # image on its own line
        m = re.match(r"^!\[\[([^\]]+)\]\]$", line.strip())
        if m:
            close_lists(); out.append(img_block(m.group(1))); i += 1; continue

        # list item
        m = re.match(r"^(\t*)([-*]|\d+\.)\s+(.*)$", raw)
        if m:
            depth = len(m.group(1))
            tag = "ol" if re.match(r"\d+\.", m.group(2)) else "ul"
            while list_stack and list_stack[-1][0] > depth:
                out.append("</%s>" % list_stack.pop()[1])
            if not list_stack or list_stack[-1][0] < depth:
                out.append("<%s>" % tag); list_stack.append((depth, tag))
            elif list_stack[-1][1] != tag:
                out.append("</%s>" % list_stack.pop()[1]); out.append("<%s>" % tag); list_stack.append((depth, tag))
            content = m.group(3)
            im = re.match(r"^!\[\[([^\]]+)\]\]$", content.strip())
            out.append("<li>%s</li>" % (img_block(im.group(1)) if im else inline(content)))
            i += 1; continue

        close_lists()
        out.append("<p>%s</p>" % inline(line.strip()))
        i += 1
    close_lists()
    return "\n".join(out)

CSS = """
  :root{
    --paper:#F5F2EC; --paper2:#FBF9F5; --surface:#FFFFFF; --surface2:#F7F4EE;
    --ink:#141317; --ink2:#3D3A36; --ink3:#8C867A;
    --line:#E2DED5; --line2:#EDE9E1;
    --accent:%(accent)s; --accent-deep:%(deep)s; --accent-soft:%(soft)s;
    --warn:#9A5B22; --warn-soft:#FBF0E4;
    --r:12px; --r-lg:18px; --r-pill:999px;
    --sh:0 1px 2px rgba(20,19,23,.05), 0 8px 24px rgba(20,19,23,.06);
    --font-d:"Mona Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    --font-b:"Plus Jakarta Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    --font-m:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--paper);color:var(--ink2);font-family:var(--font-b);
       font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
  .wrap{max-width:860px;margin:0 auto;padding:clamp(20px,5vw,56px) clamp(16px,4vw,32px)}
  a{color:var(--accent-deep)}
  .backlink{display:inline-block;font-size:.85rem;color:var(--ink3);text-decoration:none;margin-bottom:18px}
  .backlink:hover{color:var(--accent-deep)}
  .eyebrow{font-family:var(--font-d);font-size:.72rem;letter-spacing:.09em;text-transform:uppercase;
           color:var(--accent-deep);margin:0 0 8px;font-weight:700}
  h1{font-family:var(--font-d);font-weight:800;font-size:clamp(1.7rem,4.5vw,2.4rem);
     letter-spacing:-.025em;color:var(--ink);margin:0 0 10px;line-height:1.12}
  .standfirst{margin:0 0 18px;color:var(--ink3);font-size:.95rem}
  .badges{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 26px}
  .badge{font-family:var(--font-d);font-size:.72rem;font-weight:600;letter-spacing:.03em;
         padding:5px 11px;border-radius:var(--r-pill);background:var(--accent-soft);color:var(--accent-deep)}
  .badge--warn{background:var(--warn-soft);color:var(--warn)}
  .notice{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:var(--r);
          padding:13px 16px;margin:0 0 28px}
  .notice p{margin:0;font-size:.87rem;color:var(--warn)}
  .note{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);
        box-shadow:var(--sh);padding:clamp(18px,4vw,30px);margin:0 0 22px}
  .note-head{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;
             border-bottom:1px solid var(--line2);padding-bottom:12px;margin-bottom:16px}
  .note-head h2{font-family:var(--font-d);font-weight:700;font-size:1.15rem;color:var(--ink);
                margin:0;letter-spacing:-.01em}
  .note-type{font-family:var(--font-d);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;
             color:var(--ink3);background:var(--surface2);padding:3px 9px;border-radius:var(--r-pill)}
  .note h3{font-family:var(--font-d);font-weight:700;font-size:1rem;color:var(--ink);margin:22px 0 8px}
  .note h4{font-family:var(--font-d);font-weight:700;font-size:.92rem;color:var(--ink);margin:18px 0 6px}
  .note h5,.note h6{font-family:var(--font-d);font-weight:600;font-size:.86rem;color:var(--ink2);margin:14px 0 6px}
  .note p{margin:0 0 11px}
  .note ul,.note ol{margin:0 0 12px;padding-left:1.25rem}
  .note li{margin-bottom:5px}
  .note li>ul,.note li>ol{margin-top:5px}
  .note hr{border:0;border-top:1px solid var(--line2);margin:20px 0}
  .empty{color:var(--ink3);font-style:italic;font-size:.9rem;margin:0}
  code{font-family:var(--font-m);font-size:.85em;background:var(--surface2);padding:1px 5px;border-radius:4px}
  .wl{font-family:var(--font-m);font-size:.82em;color:var(--ink3);background:var(--surface2);
      padding:1px 6px;border-radius:4px}
  .callout{background:var(--accent-soft);border-radius:var(--r);padding:13px 16px;margin:14px 0}
  .callout p{margin:0;font-size:.92rem;color:var(--accent-deep)}
  blockquote{margin:14px 0;padding:0 0 0 14px;border-left:3px solid var(--line);color:var(--ink3)}
  blockquote p{margin:0;font-size:.92rem}
  .tbl{overflow-x:auto;margin:14px 0;border:1px solid var(--line);border-radius:var(--r)}
  table{border-collapse:collapse;width:100%%;min-width:460px;font-size:.87rem}
  th,td{text-align:left;padding:9px 13px;border-bottom:1px solid var(--line2);vertical-align:top}
  thead th{background:var(--surface2);font-family:var(--font-d);font-size:.75rem;letter-spacing:.03em;
           text-transform:uppercase;color:var(--ink3)}
  tr:last-child td,tr:last-child th{border-bottom:0}
  .withheld{background:var(--warn-soft);border:1px dashed var(--warn);border-radius:var(--r);
            padding:14px 16px;margin:16px 0}
  .withheld-why{margin:0 0 10px;font-size:.85rem;color:var(--warn)}
  .withheld-title{margin:0 0 8px;font-weight:600;color:var(--ink)}
  .withheld-list{margin:0;padding-left:1.25rem;font-size:.9rem}
  .fig{margin:18px 0;padding:0}
  .fig img{width:100%%;height:auto;display:block;border:1px solid var(--line);border-radius:var(--r);background:#fff}
  figcaption{margin-top:9px;font-size:.8rem;color:var(--ink3);line-height:1.55}
  .doc-foot{margin:32px 0 0;padding-top:18px;border-top:1px solid var(--line);font-size:.8rem;color:var(--ink3)}
  .doc-foot p{margin:0 0 6px}
"""

TPL = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mona+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>%(css)s</style>
</head>
<body>
<main class="wrap">
  <a class="backlink" href="../%(hub)s">&larr; %(spaced)s week hub</a>
  <p class="eyebrow">%(spaced)s &middot; %(name)s &middot; Week %(wk)d</p>
  <h1>%(wtitle)s</h1>
  <p class="standfirst">My live-session notes for this week. These are working notes, not a study page &mdash; they are not published on the public week page and are not linked from anywhere on the site.</p>
  <div class="badges">
    <span class="badge">Live session</span>
    <span class="badge badge--warn">Unlisted &mdash; not indexed</span>
  </div>
  <div class="notice"><p><strong>Unlisted, not private.</strong> This page has no password. It is excluded from search engines and linked from nowhere, but it lives in a public repository, so treat anything here as readable by anyone who finds the URL.</p></div>
%(body)s
  <div class="doc-foot">
    <p>%(spaced)s %(name)s &middot; Week %(wk)d &middot; live session</p>
    <p>Built from my Obsidian vault on 31 August 2026. Lecturer and classmate names are withheld from every page on this site.</p>
  </div>
</main>
</body>
</html>
"""

def build():
    made = []
    for code, wk, wtitle, notes in PAGES:
        s = SUBJ[code]
        chunks = []
        for heading, rel in notes:
            path = os.path.join(VAULT, rel)
            if not os.path.exists(path):
                print("MISSING", rel); continue
            raw = strip_fm(open(path, encoding="utf-8").read())
            ntype = re.search(r'^type:\s*"([^"]*)"', open(path, encoding="utf-8").read(), re.M)
            ntype = ntype.group(1) if ntype else ""
            raw = redact(raw, f"{code} wk{wk} {heading}")
            body = md(raw).strip()
            if not body:
                body = '<p class="empty">This note is empty in my vault &mdash; nothing was written under it.</p>'
            extra = ""
            if heading == "Discussion Questions":
                extra = ('<div class="notice"><p><strong>Provenance.</strong> The answers below are the '
                         'supplied AI-generated responses distributed with the discussion questions. They are '
                         'not my own writing, and they are reproduced here unedited.</p></div>')
            chunks.append('  <section class="note">\n    <div class="note-head"><h2>%s</h2><span class="note-type">%s</span></div>\n%s%s\n  </section>'
                          % (html.escape(heading), html.escape(ntype or "Note"), extra, body))
        page = TPL % dict(
            title="%s Week %d — live notes (unlisted)" % (s["spaced"], wk),
            css=CSS % dict(accent=s["accent"], deep=s["deep"], soft=s["soft"]),
            hub=s["hub"], spaced=s["spaced"], name=html.escape(s["name"]),
            wk=wk, wtitle=html.escape(wtitle), body="\n".join(chunks))
        out = os.path.join(OUT, "%s-week%d-private.html" % (code, wk))
        open(out, "w", encoding="utf-8").write(page)
        made.append((out, len(page)))
        print("built %-52s %6d bytes  (%d note%s)" % (out, len(page), len(notes), "" if len(notes)==1 else "s"))
    print()
    if REDACTED:
        print("REDACTIONS APPLIED:")
        for r in REDACTED: print("  -", r)
    else:
        print("no redactions triggered")
    return made

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build()
