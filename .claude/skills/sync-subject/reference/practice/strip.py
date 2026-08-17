#!/usr/bin/env python3
"""Remove the practice components from a week page, so they can be rebuilt.

`build.py` deliberately refuses to touch a page that already carries a
component — splicing over the top would leave two of everything. When a week
changes and its practice content has to be re-derived, run this first:

    python3 .claude/skills/sync-subject/reference/practice/strip.py PAGE.html
    python3 .claude/skills/sync-subject/reference/practice/build.py PAGE.html

It removes exactly what `build.py` adds and nothing else — the two stylesheets,
the two tab buttons, the two panels, the two scripts, the `00 / Start here`
block and the hero's quiz pill — then asserts the page is clean of every marker.
Run from the repo root.
"""

import os
import re
import sys

REPO = os.getcwd()

CSS_MARK = "    /* ── Quiz & Apply it ─"
JS_MARK = "  <script>\n    /* ── Quiz & Apply it ─"
PANEL_MARK = "\n    <!-- ══"


def cut(text, start, end, what):
    """Remove text[start:end], asserting the span was actually found."""
    assert start != -1 and end != -1 and start < end, "could not locate %s" % what
    return text[:start] + text[end:]


def strip_block_at(text, at):
    """Remove one balanced <div> …</div> starting at `at`.

    Takes the newline and indent that precede the opening tag and the single
    newline that follows the closing one, so the surrounding markup is left
    exactly as it was before the block was spliced in.
    """
    depth, end = 0, None
    for m in re.finditer(r"<div\b|</div>", text[at:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            end = at + m.end()
            break
    assert end is not None, "unbalanced study-path block"
    if end < len(text) and text[end] == "\n":
        end += 1
    return text[:text.rfind("\n", 0, at)] + text[end:]


def strip(page):
    path = os.path.join(REPO, page)
    text = open(path, encoding="utf-8").read()
    removed = []

    # 1. both stylesheets — quiz.css then path.css, both appended before </style>
    i = text.find(CSS_MARK)
    if i != -1:
        text = cut(text, i, text.index("\n  </style>", i) + 1, "practice stylesheets")
        removed.append("stylesheets")

    # 2. both scripts — appended before </body>
    # build.py splices each script as "\n" + js before "\n</body>", and js
    # itself opens with a newline — so the cut has to take the blank line that
    # separates the last synced script from the first practice one.
    i = text.find(JS_MARK)
    if i != -1:
        text = cut(text, text.rfind("\n", 0, i), text.index("\n</body>", i) + 1,
                   "practice scripts")
        removed.append("scripts")

    # 3. the two panels — appended before </main>
    i = text.find('<!-- ══')
    while i != -1 and "QUIZ" not in text[i:i + 80]:
        i = text.find('<!-- ══', i + 1)
    if i != -1:
        text = cut(text, text.rfind("\n", 0, text.rfind("\n", 0, i)), text.index("\n  </main>", i),
                   "quiz and apply panels")
        removed.append("panels")

    # 4. the two tab buttons
    before = text
    text = re.sub(r'      <button class="tab" id="tab-(?:quiz|apply)"[\s\S]*?</button>\n', "", text)
    if text != before:
        removed.append("tabs")

    # 5. the study-path block
    i = text.find('<span class="block-num">00 / Start here</span>')
    if i != -1:
        text = strip_block_at(text, text.rfind('<div class="block"', 0, i))
        removed.append("study path")

    # 6. the hero's quiz pill
    before = text
    text = re.sub(r'\n *<span class="pill">\d+ quiz questions</span>', "", text)
    if text != before:
        removed.append("hero pill")

    for marker in ('id="panel-quiz"', 'id="panel-apply"', 'id="tab-quiz"', 'class="path"',
                   "Quiz & Apply it", "00 / Start here", "quiz questions</span>"):
        assert marker not in text, "%s: %r survived the strip" % (page, marker)

    open(path, "w", encoding="utf-8").write(text)
    return "%-22s removed: %s" % (page, ", ".join(removed) or "nothing")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        print(strip(p))
