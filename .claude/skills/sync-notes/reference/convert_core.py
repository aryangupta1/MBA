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

def convert(text):
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
