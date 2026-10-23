#!/usr/bin/env python3
"""Notion enhanced-markdown -> Obsidian markdown. Imported by convert_all.py."""
import re

ILLEGAL = re.compile(r'[:/\\?*"<>|]')
def safe(s):
    s = ILLEGAL.sub("", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")

def unescape(t):
    for ch in "$><_*#[]()`~+-.!|":
        t = t.replace("\\" + ch, ch)
    return t

def conv_table(m):
    body = m.group(0)
    opentag = body.split(">", 1)[0]
    header = 'header-row="true"' in opentag
    out = []
    for r in re.findall(r"<tr>(.*?)</tr>", body, re.S):
        cells = [re.sub(r"\s*\n\s*", " ", c).strip()
                 for c in re.findall(r"<td>(.*?)</td>", r, re.S)]
        cells = [c.replace("|", "\\|") for c in cells]
        cells = [re.sub(r"<br\s*/?>", "\u00a7BR\u00a7", c) for c in cells]
        out.append("| " + " | ".join(cells) + " |")
    if not out:
        return ""
    n = max(row.count("|") - 1 for row in out)
    sep = "|" + "---|" * n
    if header:
        out.insert(1, sep)
    else:
        out.insert(0, "|" + "   |" * n)
        out.insert(1, sep)
    return "\n" + "\n".join(out) + "\n"

def conv_callout(icon, inner):
    lines = [l.strip() for l in inner.strip().splitlines()]
    lines = [l for l in lines if l]
    head = ("> [!note] " + (icon or "")).rstrip()
    return "\n" + head + "\n" + "\n".join("> " + l for l in lines) + "\n"


TOGGLE = re.compile(r'^(#{1,6} .*?)\s*\{toggle="true"\}\s*$')
def detoggle(t):
    """Notion toggle headings carry their body indented one tab. Left as-is that body
    renders as a code block, so strip the marker and de-indent the body one level."""
    out, active = [], False
    for line in t.split("\n"):
        m = TOGGLE.match(line)
        if m:
            out.append(m.group(1)); active = True; continue
        if active:
            if line.startswith("\t"):
                out.append(line[1:]); continue
            if line.strip() == "":
                out.append(line); continue
            active = False
        out.append(line)
    return "\n".join(out)

def detoggle_all(t):
    """Toggles nest; each pass unwraps one level, so repeat until stable."""
    for _ in range(10):
        nxt = detoggle(t)
        if nxt == t:
            break
        t = nxt
    return t

# --- Notion's second markup format (first seen 2026-10-23) --------------------------
# notion-fetch switched from enhanced markdown (`**b**`, tab-indented children,
# `<empty-block/>`, one-line `<page>`) to an HTML-flavoured form (`<b>`, `<ul><li>`,
# `<p />`, `<toggle heading=…>`, multi-line `<page>`, two-space list indents, blank lines
# between blocks). to_legacy() rewrites the new form into the old one so everything below
# — and the vault notes it produces — stays exactly as it was.
NEW_FORMAT = re.compile(r'<p />|<p>\s*$|</b>|</i>|<li>|<table-of-contents|<toggle\b|'
                        r'<mention url=|<page url="[^"]*">\s*\n|^(?:  )+(?:[-*+]|\d+[.)]) ', re.M)
def is_new_format(t):
    return bool(NEW_FORMAT.search(t))

def _inline(t):
    for _ in range(5):                        # Notion splits runs: `</i><i>` is one span
        t = re.sub(r'</(b|i|u|s|code)><\1>', '', t)
    t = re.sub(r'<b>(.*?)</b>', r'**\1**', t, flags=re.S)
    t = re.sub(r'<strong>(.*?)</strong>', r'**\1**', t, flags=re.S)
    t = re.sub(r'<i>(.*?)</i>', r'*\1*', t, flags=re.S)
    t = re.sub(r'<em>(.*?)</em>', r'*\1*', t, flags=re.S)
    t = re.sub(r'<s>(.*?)</s>', r'~~\1~~', t, flags=re.S)
    t = re.sub(r'<code>(.*?)</code>', r'`\1`', t, flags=re.S)
    t = re.sub(r'<u>(.*?)</u>', r'<span underline="true">\1</span>', t, flags=re.S)
    t = re.sub(r'<a href="([^"]*)">(.*?)</a>', r'[\2](\1)', t, flags=re.S)
    t = re.sub(r'<mention url="([^"]*)"\s*/>', r'<mention-page url="\1"/>', t)
    return t

def _lists(t):
    """<ul>/<ol> blocks -> `- ` / `1. ` lines, nested lists one tab deeper."""
    tok = re.compile(r'<(/?)(ul|ol|li)>')
    out, stack, buf = [], [], []
    def flush():
        txt = "".join(buf).strip()
        buf.clear()
        if not txt or not stack:
            return
        kind, n = stack[-1]
        mark = f"{n}. " if kind == "ol" else "- "
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        pad = "\t" * (len(stack) - 1)
        out.append(pad + mark + lines[0] + "\n")
        out.extend(pad + "\t" + l + "\n" for l in lines[1:])
    pos = 0
    for m in tok.finditer(t):
        chunk = t[pos:m.start()]
        pos = m.end()
        if stack:
            buf.append(chunk)
        else:
            out.append(chunk)
        close, name = m.group(1), m.group(2)
        if name in ("ul", "ol"):
            flush()
            if close:
                stack and stack.pop()
                if not stack:
                    out.append("\n")
            else:
                if not stack:
                    out.append("\n")
                stack.append([name, 0])
        elif name == "li":
            flush()
            if not close and stack:
                stack[-1][1] += 1
    out.append(t[pos:])
    return "".join(out)

def _toggles(t):
    """<toggle heading="h2">Title … body</toggle> -> `## Title {toggle="true"}` + tabbed body."""
    pat = re.compile(r'<toggle(?: heading="h([1-6])")?[^>]*>\n?(.*?)</toggle>', re.S)
    def rep(m):
        lvl, inner = m.group(1), m.group(2).strip("\n")
        lines = inner.split("\n")
        title, body = lines[0].strip(), lines[1:]
        head = ("#" * int(lvl) + " " + title + ' {toggle="true"}') if lvl else "- " + title
        return head + "\n" + "\n".join("\t" + l if l.strip() else l for l in body) + "\n"
    for _ in range(10):                       # innermost first; toggles nest
        nxt = pat.sub(rep, t)
        if nxt == t:
            break
        t = nxt
    return t

def _block(inner, lead):
    """A block with children: its first line, then each child line indented one tab."""
    lines = [l for l in inner.strip("\n").split("\n") if l.strip()]
    if not lines:
        return ""
    return "\n".join([lead + lines[0]] + ["\t" + l for l in lines[1:]])

def to_legacy(t):
    t = re.sub(r'<table-of-contents[^>]*/>', "<table_of_contents/>", t)
    # inline equations lost their backticks: `$x$` is now what `$\`x\`$` was. Money is
    # always escaped (`\$28.888m`), so an unescaped `$…$` pair on one line is an equation.
    t = re.sub(r'(?<![\\$`])\$(?=\S)([^$\n`]+?)(?<![\s\\])\$(?![`\d])', r'$`\1`$', t)
    t = re.sub(r'<p\s*/>', "<empty-block/>", t)
    t = re.sub(r'<page url="([^"]*)">\s*\n(.*?)\n\s*</page>', r'<page url="\1">\2</page>', t)
    t = re.sub(r'<h([1-6])>\s*\n?(.*?)\n?\s*</h\1>',
               lambda m: "#" * int(m.group(1)) + " " + m.group(2).strip(), t, flags=re.S)
    t = re.sub(r'<quote>\s*\n?(.*?)\n?\s*</quote>', lambda m: _block(m.group(1), "> "), t, flags=re.S)
    t = re.sub(r'<p>\s*\n?(.*?)\n?\s*</p>', lambda m: _block(m.group(1), ""), t, flags=re.S)
    t = _toggles(t)
    t = _lists(t)
    t = _inline(t)
    # space-indented nesting -> one tab per level (outside fenced code). Notion indents a
    # child by its parent marker's width: two spaces under `- `, three under `1. `.
    lines, fence, widths = [], False, []
    for l in t.split("\n"):
        if l.lstrip().startswith("```"):
            fence = not fence
        if not fence:
            if l.strip() == "":
                continue                       # the old format had no blank separators
            m = re.match(r'^( +)(?=\S)', l)
            n = len(m.group(1)) if m else 0
            if not l.startswith("\t"):
                while widths and widths[-1] >= n:
                    widths.pop()
                if n:
                    widths.append(n)
                    l = "\t" * len(widths) + l[n:]
        lines.append(l)
    return "\n".join(lines)

def convert(text):
    if is_new_format(text):
        text = to_legacy(text)
    t = detoggle_all(text)
    # --- drop structural noise (BEFORE the table rule, so <table_of_contents> can't be eaten)
    t = re.sub(r"<table_of_contents[^>]*>", "", t)
    t = re.sub(r"<empty-block[^>]*>", "", t)
    t = re.sub(r"<colgroup>.*?</colgroup>", "", t, flags=re.S)
    t = re.sub(r"<col\s[^>]*>", "", t)
    # --- blocks.  `<table(?=[\s>])` so it never matches <table_of_contents>
    t = re.sub(r"<table(?=[\s>])[^>]*>.*?</table>", conv_table, t, flags=re.S)
    t = re.sub(r'<callout[^>]*icon="([^"]*)"[^>]*>(.*?)</callout>',
               lambda m: conv_callout(m.group(1), m.group(2)), t, flags=re.S)
    t = re.sub(r'<callout[^>]*>(.*?)</callout>',
               lambda m: conv_callout("", m.group(1)), t, flags=re.S)
    # --- inline
    t = re.sub(r'<br\s*/?>', "", t)
    t = t.replace("\u00a7BR\u00a7", "<br>")
    # Notion highlight colours -> Obsidian ==highlight==
    t = re.sub(r'<span[^>]*color="[a-z_]+_bg"[^>]*>(.*?)</span>',
               lambda m: f"=={m.group(1).strip()}==", t, flags=re.S)
    t = re.sub(r'<span[^>]*underline="true"[^>]*>(.*?)</span>',
               lambda m: f"<u>{m.group(1)}</u>", t, flags=re.S)
    t = re.sub(r'<span[^>]*>(.*?)</span>', lambda m: m.group(1), t, flags=re.S)
    t = re.sub(r'<page url="[^"]*">(.*?)</page>',
               lambda m: f"- [[{safe(m.group(1))}]]", t, flags=re.S)
    t = re.sub(r'!\[[^\]]*\]\(ATTACHMENT::([^)\s]+)\)', lambda m: f"\n![[{m.group(1)}]]\n", t)
    t = re.sub(r'<im(?:g|age)[^>]*src="ATTACHMENT::([^"]+)"[^>]*>',
               lambda m: f"\n![[{m.group(1)}]]\n", t)
    t = re.sub(r'ATTACHMENT::(\S+)', lambda m: f"\n![[{m.group(1)}]]\n", t)
    t = re.sub(r'\$`(.+?)`\$', lambda m: m.group(1), t, flags=re.S)
    t = unescape(t)
    # --- emphasis with the space trapped inside the markers (a Notion artefact).
    #     content may not contain * or a newline, so table rows can't be spanned.
    t = re.sub(r'(?<![*\w])\*\*\*(?=\S)([^*\n]*?)([ \t]+)\*\*\*(?!\*)',
               lambda m: f"***{m.group(1)}***{m.group(2)}", t)
    t = re.sub(r'(?<![*\w])\*\*(?=\S)([^*\n]*?)([ \t]+)\*\*(?!\*)',
               lambda m: f"**{m.group(1)}**{m.group(2)}", t)
    t = re.sub(r'(?<![*\w])\*(?=\S)([^*\n]*?)([ \t]+)\*(?!\*)',
               lambda m: f"*{m.group(1)}*{m.group(2)}", t)
    return normalise(t)

LIST = re.compile(r'^(\s*)(?:[-*+]\s|\d+[.)]\s)')
def is_list(l):  return bool(LIST.match(l))
def is_cont(l):  return l.startswith(("\t", "    "))
def is_head(l):  return l.startswith("#")
def is_quote(l): return l.startswith(">")
def is_table(l): return l.startswith("|")
def is_rule(l):  return bool(re.fullmatch(r'(?:-{3,}|\*{3,}|_{3,})', l.strip()))

def normalise(t):
    """Notion emits no blank lines; CommonMark needs them or blocks merge."""
    lines = [l.rstrip() for l in t.split("\n")]
    out = []
    for line in lines:
        prev = out[-1] if out else ""
        blank = (prev.strip() == "")
        if line.strip() == "":
            if not blank and out:
                out.append("")
            continue
        need = False
        if not blank and prev:
            if is_head(line) or is_head(prev):
                need = True                                   # a heading is always its own block
            elif is_rule(line) or is_rule(prev):
                need = True                                   # `text\n---` would be a setext heading
            elif is_table(line) != is_table(prev):
                need = True                                   # entering or leaving a table
            elif is_quote(line) != is_quote(prev):
                need = True                                   # entering or leaving a callout
            elif is_list(line) and not (is_list(prev) or is_cont(prev)):
                need = True
            elif not is_list(line) and not is_cont(line) and (is_list(prev) or is_cont(prev)):
                need = True                                   # paragraph after a list
        if need:
            out.append("")
        out.append(line)
    res = "\n".join(out)
    res = re.sub(r'\n{3,}', "\n\n", res)
    return res.strip()
