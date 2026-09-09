#!/usr/bin/env python3
"""Build the access-code-gated per-week Live Session pages from the Obsidian vault.

One page per week per subject under live/<CODE>-week<N>.html, plus one index page per
subject at live/<CODE>.html. Every page's content is encrypted at build time with
AES-256-GCM under a key derived (PBKDF2-SHA256, 310k rounds) from LIVE_ACCESS_CODE in
the repo's .env file; the browser decrypts with WebCrypto after the reader enters the
code. Nothing readable is committed. Aryan asked for this on 2026-09-09, replacing the
unlisted plaintext pages of 2026-08-31.

These pages carry publish:false material by his explicit instruction. Third-party
material is withheld regardless: no lecturer or classmate name, no transcript, no chat
log, no image with an identifiable person in it.

Run from the repo root:  python3 .claude/private-pages/build.py
Needs: python3, node (for the AES-GCM encryption step only — a build-time tool, the
site itself still has no dependencies), and .env with LIVE_ACCESS_CODE=<code>.
"""
import os, re, html, json, sys, glob, subprocess

VAULT = os.path.expanduser("~/MBA/Semester 2 2026")
OUT   = "live"
ENV   = ".env"
BUILT_ON = "9 September 2026"

# ── Access code ──────────────────────────────────────────────────────────────
def access_code():
    # An environment variable wins, so a throwaway code can be used for a browser test
    # (LIVE_ACCESS_CODE=test python3 build.py) — rebuild with the real one afterwards.
    if os.environ.get("LIVE_ACCESS_CODE", "").strip():
        return os.environ["LIVE_ACCESS_CODE"].strip()
    if not os.path.exists(ENV):
        sys.exit("FATAL: no .env in the repo root — add LIVE_ACCESS_CODE=<code> to it")
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line.startswith("LIVE_ACCESS_CODE="):
            v = line.split("=", 1)[1].strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            if v:
                return v
    sys.exit("FATAL: LIVE_ACCESS_CODE is not set in .env")

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
# Formula renders (LaTeX screenshots, black on white). Transcribed as text, exactly as
# the image shows, never derived or completed. The PNG is not published — same rule as
# the public week pages (CLAUDE.md, "formulas are transcribed, not published").
IMAGE_FORMULA = {
  "3d57b336873c80608602eae49708d1aa-01-Screenshot_2026-09-09_at_12.12.19_am.png":
    ["Post-money valuation = Investment / Ownership", "= 3 / 0.227 = $13.22m"],
  "3d57b336873c80608602eae49708d1aa-02-Screenshot_2026-09-09_at_12.36.48_am.png":
    ["β<sub>L</sub> = β<sub>U</sub> [1 + (1 − T) D/E]"],
  "3d57b336873c80608602eae49708d1aa-03-Screenshot_2026-09-09_at_12.37.06_am.png":
    ["D/E ↑ → β<sub>L</sub> ↑ → r<sub>e</sub> ↑"],
}

PAGES = [
  # code, week no, week title, [(heading, relative path)]
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
  ("DMBA6008", 6, "Equity hurdle rate and valuation applications", [
      ("Live", "DMBA6008 Finance, Strategy and Technology/Week 6 Equity Hurdle rate and valuation applications/Live.md"),
      ("Live Prep — MedScope Technologies case", "DMBA6008 Finance, Strategy and Technology/Week 6 Equity Hurdle rate and valuation applications/Live/Live Prep - MedScope Technologies.md")]),
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
    # restore the underline and line-break tags the notes use deliberately
    s = s.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")
    s = re.sub(r"&lt;br\s*/?&gt;", "<br>", s)
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
    if fname in IMAGE_FORMULA:
        return '<div class="formula">%s</div>' % "<br>".join(IMAGE_FORMULA[fname])
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

        if line.lstrip().startswith(">"):
            close_lists()
            body = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
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

# ── Encryption (build-time only, via node's crypto) ───────────────────────────
NODE_JS = r"""
const c=require("crypto"); let d="";
process.stdin.setEncoding("utf8"); process.stdin.on("data",x=>d+=x);
process.stdin.on("end",()=>{
  const code=process.env.LIVE_CODE; const salt=c.randomBytes(16), iv=c.randomBytes(12);
  const key=c.pbkdf2Sync(code,salt,310000,32,"sha256");
  const ci=c.createCipheriv("aes-256-gcm",key,iv);
  const ct=Buffer.concat([ci.update(d,"utf8"),ci.final(),ci.getAuthTag()]);
  process.stdout.write(JSON.stringify({v:1,kdf:"PBKDF2-SHA256",iter:310000,
    salt:salt.toString("base64"),iv:iv.toString("base64"),ct:ct.toString("base64")}));
});
"""
def encrypt(plain, code):
    r = subprocess.run(["node", "-e", NODE_JS], input=plain, capture_output=True, text=True,
                       env={**os.environ, "LIVE_CODE": code})
    if r.returncode != 0:
        sys.exit("FATAL: node encryption failed: " + r.stderr)
    blob = json.loads(r.stdout)
    assert "<" not in r.stdout, "payload must be safe inside a <script> block"
    return r.stdout

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
  [hidden]{display:none!important}
  .wrap{max-width:860px;margin:0 auto;padding:clamp(20px,5vw,56px) clamp(16px,4vw,32px)}
  a{color:var(--accent-deep)}
  .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

  /* gate */
  .gate{min-height:100svh;display:grid;place-items:center;padding:24px}
  .gate-card{width:100%%;max-width:440px;background:var(--surface);border:1px solid var(--line);
             border-radius:var(--r-lg);box-shadow:var(--sh);padding:clamp(24px,5vw,36px)}
  .gate-kicker{font-family:var(--font-d);font-size:.7rem;font-weight:700;letter-spacing:.14em;
               text-transform:uppercase;color:var(--accent-deep);margin:0 0 10px}
  .lock{font-size:28px;line-height:1}
  .gate-card h1{font-family:var(--font-d);font-weight:800;font-size:1.5rem;letter-spacing:-.02em;
                color:var(--ink);margin:12px 0 6px}
  .gate-card p{margin:0 0 18px;font-size:.9rem;color:var(--ink3)}
  .field{display:flex;gap:8px}
  .field input{flex:1;min-width:0;font:inherit;font-size:.95rem;padding:11px 14px;border:1px solid var(--line);
               border-radius:var(--r);background:var(--paper2);color:var(--ink)}
  .field input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:transparent}
  .btn{font:inherit;font-weight:600;font-size:.9rem;padding:11px 18px;cursor:pointer;border:0;
       border-radius:var(--r);background:var(--accent);color:#fff}
  .btn:hover{background:var(--accent-deep)}
  .btn:disabled{opacity:.6;cursor:progress}
  .msg{margin-top:12px;font-size:.85rem;min-height:1.2em}
  .msg--err{color:#A3302B}
  .gate-foot{margin-top:20px;padding-top:16px;border-top:1px solid var(--line2);font-size:.78rem;
             color:var(--ink3);line-height:1.55}
  .gate-foot a{color:var(--ink3)}

  /* document */
  .backlinks{display:flex;flex-wrap:wrap;gap:6px 18px;margin-bottom:18px}
  .backlink{display:inline-block;font-size:.85rem;color:var(--ink3);text-decoration:none}
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
  .formula{background:var(--ink);color:#F5F2EC;font-family:var(--font-m);font-size:.92rem;line-height:1.8;
           padding:12px 16px;border-radius:var(--r);margin:14px 0;overflow-x:auto}
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

  /* index list */
  .weeks{list-style:none;margin:0 0 26px;padding:0;display:grid;gap:14px}
  .wk{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);
      border-radius:var(--r-lg);box-shadow:var(--sh);padding:18px 22px;
      transition:transform .18s ease,box-shadow .18s ease}
  .wk:hover{transform:translateY(-2px);box-shadow:0 1px 2px rgba(20,19,23,.05),0 14px 30px rgba(20,19,23,.1)}
  .wk-num{font-family:var(--font-d);font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
          color:var(--accent-deep)}
  .wk h2{font-family:var(--font-d);font-weight:700;font-size:1.1rem;color:var(--ink);margin:4px 0 6px;letter-spacing:-.01em}
  .wk p{margin:0;font-size:.88rem;color:var(--ink3)}
  .wk-flags{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px}
  .flag{font-family:var(--font-d);font-size:.68rem;letter-spacing:.04em;padding:3px 9px;border-radius:var(--r-pill);
        background:var(--surface2);color:var(--ink3)}
  .none{font-size:.88rem;color:var(--ink3)}
  .none ul{margin:6px 0 0;padding-left:1.25rem}

  .doc-foot{margin:32px 0 0;padding-top:18px;border-top:1px solid var(--line);font-size:.8rem;color:var(--ink3)}
  .doc-foot p{margin:0 0 6px}
  .lock-btn{font:inherit;font-size:.8rem;font-weight:600;color:var(--ink3);background:none;border:1px solid var(--line);
            border-radius:var(--r-pill);padding:6px 14px;cursor:pointer;margin-top:8px}
  .lock-btn:hover{color:var(--accent-deep);border-color:var(--accent-deep)}
"""

GATE_JS = r"""
(function(){
  var KEY='mba-live-code';
  var gate=document.getElementById('gate'), doc=document.getElementById('doc'),
      form=document.getElementById('form'), pw=document.getElementById('pw'),
      go=document.getElementById('go'), msg=document.getElementById('msg');
  var blob=JSON.parse(document.getElementById('payload').textContent);
  function b64(s){var b=atob(s),a=new Uint8Array(b.length);for(var i=0;i<b.length;i++)a[i]=b.charCodeAt(i);return a;}
  function say(t,err){msg.className=err?'msg msg--err':'msg';msg.textContent=t;}
  function unlock(code){
    if(!window.crypto||!window.crypto.subtle){
      say('This browser cannot decrypt the page here (WebCrypto needs https:// or localhost).',true);
      return Promise.reject(new Error('no-webcrypto'));
    }
    var enc=new TextEncoder();
    return crypto.subtle.importKey('raw',enc.encode(code),'PBKDF2',false,['deriveKey'])
      .then(function(base){return crypto.subtle.deriveKey(
        {name:'PBKDF2',salt:b64(blob.salt),iterations:blob.iter,hash:'SHA-256'},
        base,{name:'AES-GCM',length:256},false,['decrypt']);})
      .then(function(key){return crypto.subtle.decrypt({name:'AES-GCM',iv:b64(blob.iv)},key,b64(blob.ct));})
      .then(function(plain){
        doc.innerHTML=new TextDecoder().decode(plain);
        try{sessionStorage.setItem(KEY,code);}catch(e){}
        gate.hidden=true; doc.hidden=false; window.scrollTo(0,0);
        Array.prototype.forEach.call(doc.querySelectorAll('[data-lock]'),function(b){
          b.addEventListener('click',function(){try{sessionStorage.removeItem(KEY);}catch(e){} location.reload();});
        });
      });
  }
  form.addEventListener('submit',function(e){
    e.preventDefault(); go.disabled=true; say('Unlocking…');
    unlock(pw.value).catch(function(err){
      go.disabled=false;
      if(!err||err.message!=='no-webcrypto'){say('Wrong access code.',true);}
      pw.select();
    });
  });
  var saved=null; try{saved=sessionStorage.getItem(KEY);}catch(e){}
  if(saved){
    say('Unlocking…');
    unlock(saved).catch(function(){try{sessionStorage.removeItem(KEY);}catch(e){} say(''); pw.focus();});
  } else { pw.focus(); }
})();
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
<div class="gate" id="gate">
  <div class="gate-card">
    <div class="lock" aria-hidden="true">🔒</div>
    <p class="gate-kicker">%(spaced)s &middot; %(gate_kicker)s</p>
    <h1>%(gate_title)s</h1>
    <p>%(gate_blurb)s</p>
    <form id="form" autocomplete="off">
      <div class="field">
        <label class="sr-only" for="pw">Access code</label>
        <input type="password" id="pw" placeholder="Access code" autocomplete="current-password" required>
        <button class="btn" type="submit" id="go">Unlock</button>
      </div>
      <p class="msg" id="msg" role="status" aria-live="polite"></p>
    </form>
    <p class="gate-foot">The notes are encrypted with AES-256-GCM and the key is derived from the access code with PBKDF2. Nothing readable is stored in this file. Once unlocked, every live page of this subject stays open until you close the tab or press <em>Lock</em>. <a href="../%(hub)s">Back to the %(spaced)s week hub</a>.</p>
  </div>
</div>
<main class="wrap" id="doc" hidden></main>
<script id="payload" type="application/json">%(payload)s</script>
<script>%(js)s</script>
</body>
</html>
"""

WEEK_DOC = """  <nav class="backlinks" aria-label="Back">
    <a class="backlink" href="../%(hub)s">&larr; %(spaced)s week hub</a>
    <a class="backlink" href="%(code)s.html">&larr; All live sessions</a>
  </nav>
  <p class="eyebrow">%(spaced)s &middot; %(name)s &middot; Week %(wk)d</p>
  <h1>%(wtitle)s</h1>
  <p class="standfirst">My live-session notes for this week. These are working notes, not a study page &mdash; they are not published on the public week page.</p>
  <div class="badges">
    <span class="badge">Live session</span>
    <span class="badge badge--warn">Access code &mdash; not indexed</span>
  </div>
%(body)s
  <div class="doc-foot">
    <p>%(spaced)s %(name)s &middot; Week %(wk)d &middot; live session</p>
    <p>Built from my Obsidian vault on %(built)s. Lecturer and classmate names are withheld from every page on this site.</p>
    <button type="button" class="lock-btn" data-lock>Lock these pages</button>
  </div>
"""

INDEX_DOC = """  <nav class="backlinks" aria-label="Back">
    <a class="backlink" href="../%(hub)s">&larr; %(spaced)s week hub</a>
  </nav>
  <p class="eyebrow">%(spaced)s &middot; %(name)s</p>
  <h1>Live sessions</h1>
  <p class="standfirst">My in-class notes, one page per week &mdash; the material that is deliberately kept off the public week pages. You are unlocked for this subject until you close the tab or press <em>Lock</em>.</p>
  <div class="badges">
    <span class="badge">%(count)d live page%(plural)s</span>
    <span class="badge badge--warn">Access code &mdash; not indexed</span>
  </div>
  <ul class="weeks">
%(cards)s  </ul>
  <div class="none">
    <p>Weeks with no live page yet &mdash; no Live Session note exists in the vault for them. A week gets a page here the moment one appears.</p>
    <ul>%(missing)s</ul>
  </div>
  <div class="doc-foot">
    <p>%(spaced)s %(name)s &middot; live sessions index</p>
    <p>Built from my Obsidian vault on %(built)s. Lecturer and classmate names, transcripts and class chat logs are withheld from every page on this site.</p>
    <button type="button" class="lock-btn" data-lock>Lock these pages</button>
  </div>
"""

def published_weeks(code):
    return sorted(int(m.group(1)) for f in glob.glob(f"{code}-week*.html")
                  for m in [re.match(rf"{code}-week(\d+)\.html", f)] if m)

def build():
    code_secret = access_code()
    os.makedirs(OUT, exist_ok=True)
    made, index = [], {}
    for code, wk, wtitle, notes in PAGES:
        s = SUBJ[code]
        chunks, flags = [], []
        for heading, rel in notes:
            path = os.path.join(VAULT, rel)
            if not os.path.exists(path):
                print("MISSING", rel); flags.append("note missing"); continue
            full = open(path, encoding="utf-8").read()
            raw = strip_fm(full)
            ntype = re.search(r'^type:\s*"([^"]*)"', full, re.M)
            ntype = ntype.group(1) if ntype else ""
            before = len(REDACTED)
            raw = redact(raw, f"{code} wk{wk} {heading}")
            if len(REDACTED) > before: flags.append("lecturer name withheld")
            if any(f in raw for f in IMAGE_WITHHELD): flags.append("image withheld")
            if any(f in raw for f in IMAGE_FORMULA): flags.append("formulas transcribed")
            body = md(raw).strip()
            if not body:
                body = '<p class="empty">This note is empty in my vault &mdash; nothing was written under it.</p>'
                flags.append("1 note empty in vault")
            extra = ""
            if heading == "Discussion Questions":
                extra = ('<div class="notice"><p><strong>Provenance.</strong> The answers below are the '
                         'supplied AI-generated responses distributed with the discussion questions. They are '
                         'not my own writing, and they are reproduced here unedited.</p></div>')
            chunks.append('  <section class="note">\n    <div class="note-head"><h2>%s</h2><span class="note-type">%s</span></div>\n%s%s\n  </section>'
                          % (html.escape(heading), html.escape(ntype or "Note"), extra, body))
        doc = WEEK_DOC % dict(hub=s["hub"], spaced=s["spaced"], code=code, name=html.escape(s["name"]),
                              wk=wk, wtitle=html.escape(wtitle), body="\n".join(chunks), built=BUILT_ON)
        page = TPL % dict(
            title="%s Week %d — live notes" % (s["spaced"], wk),
            css=CSS % dict(accent=s["accent"], deep=s["deep"], soft=s["soft"]),
            spaced=s["spaced"], hub=s["hub"], gate_kicker="Week %d live notes" % wk,
            gate_title="Enter the access code", gate_blurb="Live-session notes for week %d. Unlocking here unlocks every live page of %s in this tab." % (wk, s["spaced"]),
            payload=encrypt(doc, code_secret), js=GATE_JS)
        out = os.path.join(OUT, "%s-week%d.html" % (code, wk))
        open(out, "w", encoding="utf-8").write(page)
        made.append(out)
        index.setdefault(code, []).append(dict(wk=wk, title=wtitle, notes=[h for h, _ in notes], flags=sorted(set(flags))))
        print("built %-32s %6d bytes  (%d note%s)" % (out, len(page), len(notes), "" if len(notes)==1 else "s"))

    for code, s in SUBJ.items():
        rows = sorted(index.get(code, []), key=lambda r: r["wk"])
        cards = ""
        for r in rows:
            fl = "".join('<span class="flag">%s</span>' % html.escape(f) for f in r["flags"])
            cards += ('    <li><a class="wk" href="%s-week%d.html"><span class="wk-num">Week %02d</span>'
                      '<h2>%s</h2><p>%s</p>%s</a></li>\n'
                      % (code, r["wk"], r["wk"], html.escape(r["title"]), html.escape(", ".join(r["notes"])),
                         ('<div class="wk-flags">%s</div>' % fl) if fl else ""))
        have = {r["wk"] for r in rows}
        missing = "".join("<li>Week %d</li>" % w for w in published_weeks(code) if w not in have) or "<li>none</li>"
        doc = INDEX_DOC % dict(hub=s["hub"], spaced=s["spaced"], name=html.escape(s["name"]),
                               count=len(rows), plural="" if len(rows)==1 else "s", cards=cards,
                               missing=missing, built=BUILT_ON)
        page = TPL % dict(
            title="%s — live sessions" % s["spaced"],
            css=CSS % dict(accent=s["accent"], deep=s["deep"], soft=s["soft"]),
            spaced=s["spaced"], hub=s["hub"], gate_kicker="Live sessions",
            gate_title="Enter the access code", gate_blurb="My in-class notes for %s, one page per week. Unlocking here unlocks every live page of the subject in this tab." % s["spaced"],
            payload=encrypt(doc, code_secret), js=GATE_JS)
        out = os.path.join(OUT, "%s.html" % code)
        open(out, "w", encoding="utf-8").write(page)
        made.append(out)
        print("built %-32s %6d bytes  (index, %d week%s)" % (out, len(page), len(rows), "" if len(rows)==1 else "s"))

    print()
    if REDACTED:
        print("REDACTIONS APPLIED:")
        for r in REDACTED: print("  -", r)
    else:
        print("no redactions triggered")
    return made

if __name__ == "__main__":
    build()
