#!/usr/bin/env python3
"""Build a subject's master search page from its published week pages.

    python3 .claude/skills/sync-subject/reference/search/build_search.py [SUBJECT|all] [--json] [--dry-run] [--out DIR]

SUBJECT is a code (`DMBA6008`) or an alias from `subjects.json` (`finance`, `agile`).
Default is `all` — every subject flagged `live: true`.

The page is DERIVED, not synced. Its only input is the four JS arrays every built
week page already carries — `TERMS`, `ACRONYMS`, `FORMULAS`, `CARDS` — read straight
out of `DMBA<code>-week<N>.html`. Nothing here reads the vault or Notion, so the
search page can never say something a week page does not. A re-sync that changes
a week must re-run this so the index catches up (see README.md).

The array literals are JavaScript, not JSON (unquoted keys, single quotes, and on
some pages `[].concat(tag(BS, [...]))` with string constants declared above), so
they are evaluated by `node` in a bare `vm` context with no DOM. Node is a machine
tool used only at build time; the site itself still has no dependencies.

Output: `DMBA<code>-search.html` in the repo root, spliced from `search-shell.html`
in this folder. `--json` prints the data object instead; `--dry-run` prints the
counts table without writing anything.
"""
import os, re, sys, json, glob, html, shutil, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def _repo_root():
    d = HERE
    while d != "/":
        if os.path.isdir(os.path.join(d, ".claude")) and os.path.isfile(os.path.join(d, "library.html")):
            return d
        d = os.path.dirname(d)
    return os.getcwd()


REPO = _repo_root()
SUBJECTS_JSON = os.path.join(HERE, "..", "..", "subjects.json")
SHELL = os.path.join(HERE, "search-shell.html")
NODE_FALLBACK = "/Users/aryan/.nvm/versions/node/v20.9.0/bin/node"
ARRAYS = ("TERMS", "ACRONYMS", "FORMULAS", "CARDS")
DATA_MARK = re.compile(r"/\*SEARCH_DATA\*/.*?/\*END_SEARCH_DATA\*/", re.S)


def die(msg):
    sys.stderr.write("build_search: " + msg + "\n")
    sys.exit(1)


# ── Subjects ────────────────────────────────────────────────────────────────
def load_subjects():
    with open(SUBJECTS_JSON, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, dict)}


def resolve(target, subjects):
    if target in ("all", None):
        return [c for c, s in subjects.items() if s.get("live")]
    t = target.lower()
    for code, s in subjects.items():
        if t == code.lower() or t in [a.lower() for a in s.get("aliases", [])]:
            if not s.get("live"):
                die(f"{code} is not live in subjects.json; nothing to index")
            return [code]
    die(f"unknown subject {target!r}; try one of " + ", ".join(subjects))


# ── JS extraction ───────────────────────────────────────────────────────────
def scripts_of(text):
    return [m.group(1) for m in re.finditer(r"<script[^>]*>(.*?)</script>", text, re.S)]


def scan_expression(src, start):
    """Return src[start:end] — the expression text up to the `;` that closes the
    statement at bracket depth 0, honouring strings and comments."""
    i, n, depth = start, len(src), 0
    while i < n:
        c = src[i]
        if c in "'\"`":
            q = c
            i += 1
            while i < n and src[i] != q:
                i += 2 if src[i] == "\\" else 1
            i += 1
            continue
        if src.startswith("//", i):
            i = src.find("\n", i)
            if i == -1:
                break
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j == -1:
                die("unterminated comment in script")
            i = j + 2
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ";" and depth == 0:
            return src[start:i]
        i += 1
    die("statement never terminated")


def extract_arrays(page_text, page_name):
    """Find each `var NAME =` statement plus the string constants it may lean on."""
    found, prelude = {}, []
    for script in scripts_of(page_text):
        for m in re.finditer(r"\bvar\s+([A-Za-z_$][\w$]*)\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")\s*;", script):
            prelude.append(f"var {m.group(1)} = {m.group(2)};")
        for name in ARRAYS:
            if name in found:
                continue
            m = re.search(r"\bvar\s+" + name + r"\s*=\s*", script)
            if not m:
                continue
            found[name] = scan_expression(script, m.end())
    if "TERMS" not in found or "CARDS" not in found:
        die(f"{page_name}: could not find TERMS/CARDS arrays")
    return found, prelude


def node_bin():
    return shutil.which("node") or (NODE_FALLBACK if os.path.exists(NODE_FALLBACK) else None)


def evaluate(found, prelude, page_name):
    node = node_bin()
    if not node:
        die("node is required to evaluate the page's JS arrays and was not found on PATH")
    body = "\n".join(prelude) + "\n"
    body += "function tag(topic, arr){ return arr.map(function(o){ o.topic = topic; return o; }); }\n"
    body += "var __out = {};\n"
    for name in ARRAYS:
        expr = found.get(name, "[]")
        body += f"__out[{json.dumps(name)}] = ({expr});\n"
    body += "__out;"
    runner = (
        "const vm=require('vm');let s='';process.stdin.setEncoding('utf8');"
        "process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{"
        "try{const r=vm.runInNewContext(s,{},{timeout:5000});process.stdout.write(JSON.stringify(r));}"
        "catch(e){process.stderr.write(String(e&&e.stack||e));process.exit(2);}});"
    )
    p = subprocess.run([node, "-e", runner], input=body, capture_output=True, text=True)
    if p.returncode != 0:
        die(f"{page_name}: node could not evaluate its arrays:\n{p.stderr.strip()}")
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        die(f"{page_name}: node output was not JSON ({e})")


# ── Page metadata ───────────────────────────────────────────────────────────
TITLE_RE = re.compile(r"<title>\s*Week\s+(\d+)\s*[—–-]+\s*(.*?)\s*[—–-]+\s*DMBA\s*\d{4}\s*</title>", re.S)


def week_meta(page_text, page_name):
    m = TITLE_RE.search(page_text)
    if not m:
        die(f"{page_name}: <title> is not in the `Week N — Title — DMBA nnnn` form")
    return int(m.group(1)), html.unescape(m.group(2)).strip()


def _s(v):
    return v.strip() if isinstance(v, str) else v


def entries_for(week_n, arrays):
    out = []
    for o in arrays["TERMS"]:
        e = {"t": "term", "w": week_n, "name": _s(o.get("term")), "src": _s(o.get("src")),
             "topic": _s(o.get("topic")), "def": _s(o.get("def")), "formula": _s(o.get("formula"))}
        if o.get("own"):
            e["own"] = True
        out.append(e)
    for o in arrays["ACRONYMS"]:
        out.append({"t": "acronym", "w": week_n, "abbr": _s(o.get("abbr")), "long": _s(o.get("long")),
                    "src": _s(o.get("src")), "def": _s(o.get("def")), "topic": _s(o.get("topic"))})
    for o in arrays["FORMULAS"]:
        out.append({"t": "formula", "w": week_n, "name": _s(o.get("name")), "expr": _s(o.get("expr")),
                    "src": _s(o.get("src")), "def": _s(o.get("def")), "topic": _s(o.get("topic"))})
    for o in arrays["CARDS"]:
        out.append({"t": "card", "w": week_n, "q": _s(o.get("q")), "a": _s(o.get("a")), "topic": _s(o.get("topic"))})
    # Drop absent fields only. `w` can legitimately be 0, so no truthiness test here.
    return [{k: v for k, v in e.items() if v is not None and v != ""} for e in out]


def week_pages(code):
    pat = os.path.join(REPO, f"{code}-week[0-9]*.html")
    files = [f for f in glob.glob(pat) if re.search(r"-week\d+\.html$", f)]
    files.sort(key=lambda f: int(re.search(r"-week(\d+)\.html$", f).group(1)))
    if not files:
        die(f"no {code}-week<N>.html pages found in {REPO}")
    return files


def build_data(code, subj):
    weeks, entries = [], []
    for path in week_pages(code):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n, title = week_meta(text, name)
        found, prelude = extract_arrays(text, name)
        arrays = evaluate(found, prelude, name)
        es = entries_for(n, arrays)
        counts = {k: len(arrays[a]) for k, a in
                  (("term", "TERMS"), ("acronym", "ACRONYMS"), ("formula", "FORMULAS"), ("card", "CARDS"))}
        weeks.append({"n": n, "title": title, "href": name, "counts": counts})
        entries.extend(es)
    return {
        "subject": {"code": code, "spaced": f"{code[:4]} {code[4:]}", "name": subj["name"],
                    "hub": subj["hubPage"]},
        "built": datetime.date.today().isoformat(),
        "weeks": weeks,
        "entries": entries,
    }


# ── Splice ──────────────────────────────────────────────────────────────────
def totals(data):
    t = {"term": 0, "acronym": 0, "formula": 0, "card": 0}
    for w in data["weeks"]:
        for k in t:
            t[k] += w["counts"][k]
    return t


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def splice(data, subj, code):
    if not os.path.isfile(SHELL):
        die(f"template missing: {SHELL}")
    with open(SHELL, encoding="utf-8") as f:
        page = f.read()
    t = totals(data)
    ns = [w["n"] for w in data["weeks"]]
    pal = subj["palette"]
    subs = {
        "ACCENT": pal["accent"], "ACCENT_DEEP": pal["deep"], "ACCENT_SOFT": pal["soft"], "ACCENT_GLOW": pal["glow"],
        "FONT_HREF": subj["fontHref"],
        "SUBJECT_CODE": code, "SUBJECT_CODE_SPACED": data["subject"]["spaced"],
        "SUBJECT_NAME": subj["name"], "HUB_PAGE": subj["hubPage"],
        "WEEK_COUNT": str(len(ns)), "WEEK_RANGE": f"Weeks {min(ns)}–{max(ns)}",
        "TERM_COUNT": str(t["term"]), "ACRONYM_COUNT": str(t["acronym"]),
        "FORMULA_COUNT": str(t["formula"]), "CARD_COUNT": str(t["card"]),
        "ENTRY_COUNT": str(sum(t.values())),
        "BUILD_DATE": long_date(data["built"]),
        "DOCK_CURRENT_6008": ' aria-current="page"' if code == "DMBA6008" else "",
        "DOCK_CURRENT_6005": ' aria-current="page"' if code == "DMBA6005" else "",
    }
    for k, v in subs.items():
        page = page.replace("{{" + k + "}}", v)
    if not DATA_MARK.search(page):
        die("template has no /*SEARCH_DATA*/{}/*END_SEARCH_DATA*/ marker")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = DATA_MARK.sub(lambda _: "/*SEARCH_DATA*/" + blob + "/*END_SEARCH_DATA*/", page, count=1)
    left = sorted(set(re.findall(r"\{\{[A-Z_0-9]+\}\}", page)))
    if left:
        die("unfilled placeholders: " + ", ".join(left))
    return page


def print_table(data):
    print(f"{data['subject']['spaced']} — {data['subject']['name']}")
    print(f"  {'week':<6}{'title':<48}{'terms':>6}{'acro':>6}{'form':>6}{'cards':>6}")
    for w in data["weeks"]:
        c = w["counts"]
        print(f"  {w['n']:<6}{w['title'][:46]:<48}{c['term']:>6}{c['acronym']:>6}{c['formula']:>6}{c['card']:>6}")
    t = totals(data)
    print(f"  {'':<6}{'total':<48}{t['term']:>6}{t['acronym']:>6}{t['formula']:>6}{t['card']:>6}"
          f"   = {sum(t.values())} entries")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = [a for a in argv if a.startswith("--")]
    out_dir = REPO
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            die("--out needs a directory")
        out_dir = argv[i + 1]
        args = [a for a in args if a != out_dir]
    target = args[0] if args else "all"
    subjects = load_subjects()
    codes = resolve(target, subjects)
    for code in codes:
        data = build_data(code, subjects[code])
        if "--json" in flags:
            print(json.dumps(data, ensure_ascii=False, indent=1))
            continue
        print_table(data)
        if "--dry-run" in flags:
            continue
        page = splice(data, subjects[code], code)
        dest = os.path.join(out_dir, f"{code}-search.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {os.path.relpath(dest, REPO)}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
