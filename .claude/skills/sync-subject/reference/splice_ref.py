#!/usr/bin/env python3
"""Phase 3b: splice the Acronyms and Formulas tabs into a freshly assembled week page.

    python3 .claude/skills/sync-subject/reference/splice_ref.py PAGE.html REF.json

REF.json (either key may be omitted or have an empty `items`, and then no tab is emitted):

    {
      "acronyms": {"intro": "<p> text, HTML allowed", "placeholder": "try &ldquo;NPV&rdquo;",
                   "items": [{"abbr": "NPV", "long": "Net Present Value", "def": "…", "src": "Topic"}]},
      "formulas": {"intro": "…", "placeholder": "try &ldquo;PV&rdquo;",
                   "items": [{"name": "…", "expr": "…", "def": "…", "src": "Topic"}]}
    }

It fills the six slots the shell carries — <!--INSERT:ACRONYMS_TAB|_PANEL|_DATA--> and the
same for FORMULAS — with the markup and the buildRef() calls used on DMBA6008-week4.html.
The _DATA insert carries the array AND its buildRef() call: the shell only defines
buildRef, it never calls it, and a tab without the call renders a count over an empty list
(DMBA6005-week5.html shipped that way on 2026-08-31).

Run it before practice/build.py, which numbers the Quiz and Apply-it tabs after these.
It refuses a page whose slots are already filled. Content is copied as given — this
script authors nothing.
"""
import json
import sys

SLOTS = ["ACRONYMS_TAB", "ACRONYMS_PANEL", "ACRONYMS_DATA",
         "FORMULAS_TAB", "FORMULAS_PANEL", "FORMULAS_DATA"]

RENDER = {
    "acronyms": """
      buildRef('acronyms', ACRONYMS, function (a) {
        return '<article class="term" data-search="' +
          escapeHtml((a.abbr + ' ' + a.long + ' ' + a.def).toLowerCase()) + '">' +
          '<div class="term-head"><h3 class="term-name">' +
          '<span class="term-abbr">' + escapeHtml(a.abbr) + '</span>' +
          (a.long ? ' &middot; <span class="term-long">' + escapeHtml(a.long) + '</span>' : '') +
          '</h3><span class="term-src">' + escapeHtml(a.src) + '</span></div>' +
          (a.def ? '<p class="term-def">' + escapeHtml(a.def) + '</p>' : '') +
          '</article>';
      }, 'No acronyms match that filter.');""",
    "formulas": """
      buildRef('formulas', FORMULAS, function (f) {
        return '<article class="term" data-search="' +
          escapeHtml((f.name + ' ' + f.expr + ' ' + f.def).toLowerCase()) + '">' +
          '<div class="term-head"><h3 class="term-name">' + escapeHtml(f.name) + '</h3>' +
          '<span class="term-src">' + escapeHtml(f.src) + '</span></div>' +
          '<div class="term-formula">' + escapeHtml(f.expr) + '</div>' +
          (f.def ? '<p class="term-def">' + escapeHtml(f.def) + '</p>' : '') +
          '</article>';
      }, 'No formulas match that filter.');""",
}
TITLE = {"acronyms": ("Acronyms", "Shorthand", "Acronyms &amp; abbreviations", "Filter acronyms"),
         "formulas": ("Formulas", "Quick reference", "Formulas", "Filter formulas")}
REQUIRED = {"acronyms": ("abbr", "long", "def", "src"), "formulas": ("name", "expr", "def", "src")}


def main(page, ref_path):
    html = open(page, encoding="utf-8").read()
    ref = json.load(open(ref_path, encoding="utf-8"))
    missing = [s for s in SLOTS if "<!--INSERT:%s-->" % s not in html]
    if missing:
        sys.exit("%s: slots already filled or absent: %s — start from a fresh week-shell copy"
                 % (page, ", ".join(missing)))

    num = 4  # 01 summary, 02 key concepts, 03 flashcards
    for kind in ("acronyms", "formulas"):
        items = (ref.get(kind) or {}).get("items") or []
        up = kind.upper()
        if not items:
            for part in ("TAB", "PANEL", "DATA"):
                html = html.replace("<!--INSERT:%s_%s-->" % (up, part), "")
            continue
        for i, it in enumerate(items):
            lack = [k for k in REQUIRED[kind] if k not in it]
            if lack:
                sys.exit("%s item %d lacks %s" % (kind, i + 1, lack))
        label, eyebrow, h2, filt = TITLE[kind]
        n = "%02d" % num
        num += 1
        tab = ('      <button class="tab" id="tab-%s" role="tab" aria-selected="false" aria-controls="panel-%s"\n'
               '        data-panel="%s" tabindex="-1"><span class="tab-num" aria-hidden="true">%s</span>%s</button>'
               % (kind, kind, kind, n, label))
        panel = f"""    <section class="panel" id="panel-{kind}" role="tabpanel" aria-labelledby="tab-{kind}" tabindex="0" hidden>
      <div class="block">
        <span class="block-num">{n} / {eyebrow}</span>
        <h2>{h2}</h2>
        <p>{ref[kind].get("intro", "")}</p>

        <div class="toolbar">
          <label class="visually-hidden" for="{kind}-search">{filt}</label>
          <input class="search" id="{kind}-search" type="search" placeholder="Filter &mdash; {ref[kind].get("placeholder", "")}"
            autocomplete="off">
          <span class="count" id="{kind}-count" aria-live="polite">{len(items)} of {len(items)}</span>
        </div>

        <div class="glossary" id="{kind}"></div>
      </div>
    </section>"""
        rows = ",\n".join("        " + json.dumps(it, ensure_ascii=False) for it in items)
        data = "      var %s = [\n%s\n      ];\n%s" % (up, rows, RENDER[kind])
        html = (html.replace("<!--INSERT:%s_TAB-->" % up, tab)
                    .replace("<!--INSERT:%s_PANEL-->" % up, panel)
                    .replace("<!--INSERT:%s_DATA-->" % up, data))
        print("%s: %s tab %s — %d entries" % (page, kind, n, len(items)))

    open(page, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
