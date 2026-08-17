#!/usr/bin/env python3
"""Splice the three practice components into a semester-2 week page.

    study path   "How to master this week" — the first block of the summary
                 panel: a numbered route through the modes this week has.
    quiz         a multiple-choice tab with a hint and per-option feedback.
    apply        an "Apply it" tab of scenarios with staged hints and a
                 walkthrough.

All three are *derived from the built page*, the same way the Acronyms and
Formulas tabs are. Nothing here reads Notion. The authored part is one JSON
file per page in ./data; everything mechanical — the stylesheet, the panel
markup, the renderer — is shared, so a re-sync replaces data and never markup.

Run from the repo root:

    python3 .claude/skills/sync-subject/reference/practice/build.py PAGE.html [...]

Each page is skipped if it already carries the component, so the script is
safe to re-run. To rebuild a page after re-authoring its JSON, first strip the
old components (see README.md) or rebuild the page from scratch.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.getcwd()


# ── shared helpers ────────────────────────────────────────────────────────

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def js_literal(items):
    """A JSON array as a JS array literal, one entry per line."""
    rows = []
    for it in items:
        s = json.dumps(it, ensure_ascii=False, separators=(", ", ": "))
        s = s.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        rows.append("        " + s)
    return "[\n" + ",\n".join(rows) + "\n      ]"


def tpl(name):
    return open(os.path.join(HERE, "tpl", name), encoding="utf-8").read()


def load(page):
    return json.load(open(os.path.join(HERE, "data", page.replace(".html", ".json")),
                          encoding="utf-8"))


def tab_labels(text):
    """{data-panel: visible label} straight off the page's own tab row."""
    out = {}
    for m in re.finditer(
            r'data-panel="([a-z]+)"[^>]*>(?:<span class="tab-num"[^>]*>\d+</span>)?([^<]+)</button>',
            text):
        out[m.group(1)] = m.group(2).strip()
    return out


SUMMARY_ANCHOR = ('<section class="panel active" id="panel-summary" role="tabpanel" '
                  'aria-labelledby="tab-summary" tabindex="0">')


# ── the quiz and apply-it tabs ────────────────────────────────────────────

TAB_TPL = """      <button class="tab" id="tab-quiz" role="tab" aria-selected="false" aria-controls="panel-quiz"
        data-panel="quiz" tabindex="-1"><span class="tab-num" aria-hidden="true">{qn}</span>Quiz</button>
      <button class="tab" id="tab-apply" role="tab" aria-selected="false" aria-controls="panel-apply"
        data-panel="apply" tabindex="-1"><span class="tab-num" aria-hidden="true">{an}</span>Apply it</button>
"""

PANEL_TPL = """
    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 {qn} \u00b7 QUIZ \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
    <section class="panel" id="panel-quiz" role="tabpanel" aria-labelledby="tab-quiz" tabindex="0" hidden>
      <div class="block">
        <span class="block-num">{qn} / Test yourself</span>
        <h2>Quiz</h2>
        <p>{quiz_intro}</p>

        <div class="quizbar">
          <div class="quiz-score">
            <span><strong id="quiz-done">0</strong> of <span id="quiz-total">0</span> answered</span>
            <span><strong id="quiz-right">0</strong> correct</span>
          </div>
          <span class="progress"><span class="progress-fill" id="quiz-fill"></span></span>
          <button class="btn btn--ghost" id="quiz-reset" type="button">Start over</button>
        </div>
        <p class="quiz-verdict" id="quiz-verdict" role="status" aria-live="polite" hidden></p>

        <div class="quiz-list" id="quiz-list"></div>
      </div>
    </section>

    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 {an} \u00b7 APPLY IT \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
    <section class="panel" id="panel-apply" role="tabpanel" aria-labelledby="tab-apply" tabindex="0" hidden>
      <div class="block">
        <span class="block-num">{an} / Put it to work</span>
        <h2>Apply it</h2>
        <p>{apply_intro}</p>

        <div class="scen-list" id="scen-list"></div>
      </div>
    </section>
"""


def build_tabs(page, text, data):
    if 'id="panel-quiz"' in text:
        return text, "quiz/apply already present"

    quiz, scen = data["quiz"], data["scenarios"]

    for i, q in enumerate(quiz, 1):
        oks = [o for o in q["options"] if o.get("ok")]
        assert len(q["options"]) == 4, "%s Q%d: %d options" % (page, i, len(q["options"]))
        assert len(oks) == 1, "%s Q%d: %d correct options" % (page, i, len(oks))
        assert all(o.get("note", "").strip() for o in q["options"]), "%s Q%d: an option has no note" % (page, i)
        assert q.get("hint", "").strip(), "%s Q%d: no hint" % (page, i)
        assert q.get("topic", "").strip(), "%s Q%d: no topic" % (page, i)
    for i, s in enumerate(scen, 1):
        assert len(s["hints"]) == 3, "%s S%d: %d hints" % (page, i, len(s["hints"]))
        assert 3 <= len(s["walkthrough"]) <= 6, "%s S%d: %d steps" % (page, i, len(s["walkthrough"]))
        assert 3 <= len(s["checklist"]) <= 5, "%s S%d: %d checks" % (page, i, len(s["checklist"]))

    # Tab numbers follow the tabs the page already has, so a week that gains a
    # Discussion or Formulas tab renumbers correctly without editing this file.
    at = text.index('<div class="tablist" role="tablist">')
    end = text.index("    </div>\n  </nav>", at)
    n = text.count('<button class="tab"', at, end)
    qn, an = "%02d" % (n + 1), "%02d" % (n + 2)

    text = text.replace("\n  </style>", tpl("quiz.css") + "\n  </style>", 1)

    at = text.index('<div class="tablist" role="tablist">')
    end = text.index("    </div>\n  </nav>", at)
    text = text[:end] + TAB_TPL.format(qn=qn, an=an) + text[end:]

    main_end = text.index("\n  </main>")
    text = text[:main_end] + "\n" + PANEL_TPL.format(
        qn=qn, an=an,
        quiz_intro=esc(data["quizIntro"]),
        apply_intro=esc(data["applyIntro"])) + text[main_end:]

    js = tpl("quiz.js")
    js = js.replace("/*QUIZ*/[]/*END_QUIZ*/", "/*QUIZ*/" + js_literal(quiz) + "/*END_QUIZ*/")
    js = js.replace("/*SCENARIOS*/[]/*END_SCENARIOS*/",
                    "/*SCENARIOS*/" + js_literal(scen) + "/*END_SCENARIOS*/")
    text = text.replace("\n</body>", "\n" + js + "\n</body>", 1)

    # The hero pill row carries the counts; add the quiz alongside them.
    text = re.sub(r'(<span class="pill">\d+ flashcards</span>)',
                  r'\1\n        <span class="pill">%d quiz questions</span>' % len(quiz),
                  text, count=1)

    return text, "tabs %s/%s · %d questions · %d scenarios" % (qn, an, len(quiz), len(scen))


# ── the study path ────────────────────────────────────────────────────────

PATH_JS = """
  <script>
    /* ── Study path ─────────────────────────────────────────────────────
       The only behaviour the block needs: a step's button selects its mode
       tab. Everything else about the block is static markup. */
    (function () {
      'use strict';
      var path = document.querySelector('.path');
      if (!path) return;

      path.addEventListener('click', function (e) {
        var node = e.target;
        while (node && node !== path && !(node.classList && node.classList.contains('path-go'))) {
          node = node.parentNode;
        }
        if (!node || node === path) return;
        var tab = document.getElementById('tab-' + node.getAttribute('data-goto'));
        if (!tab) return;
        tab.click();
        tab.scrollIntoView({ block: 'center' });
        tab.focus();
      });
    })();
  </script>
"""


def build_path(page, text, data):
    if 'class="path"' in text:
        return text, "study path already present"

    sp = data["studyPath"]
    steps = sp["steps"]
    assert 5 <= len(steps) <= 7, "%s: %d steps" % (page, len(steps))
    assert sum(1 for s in steps if not s.get("goto")) <= 1, "%s: more than one off-screen step" % page

    labels = tab_labels(text)
    for s in steps:
        g = s.get("goto")
        assert not g or g in labels, "%s: goto '%s' is not a tab on this page" % (page, g)

    lis = []
    for s in steps:
        g = s.get("goto")
        # The label is lifted off the page's own tab button, so it is already
        # escaped — running esc() over it would double-escape the ampersand.
        go = ('\n            <button class="path-go" type="button" data-goto="%s">Open %s '
              '<span aria-hidden="true">&rarr;</span></button>' % (g, labels[g])) if g else ""
        lis.append(
            '          <li class="path-step">\n'
            '            <div class="path-head">\n'
            '              <h3 class="path-label">%s</h3>\n'
            '              <span class="path-time">%s</span>\n'
            '            </div>\n'
            '            <p>%s</p>%s\n'
            '          </li>' % (esc(s["label"]), esc(s["time"]), esc(s["detail"]), go))

    block = (
        '\n      <div class="block">\n'
        '        <span class="block-num">00 / Start here</span>\n'
        '        <h2>How to master this week</h2>\n'
        '        <p>%s</p>\n\n'
        '        <ol class="path">\n%s\n        </ol>\n\n'
        '        <p class="path-close"><strong>The test</strong>%s</p>\n'
        '      </div>\n'
        % (esc(sp["intro"]), "\n".join(lis), esc(sp["close"])))

    text = text.replace("\n  </style>", tpl("path.css") + "\n  </style>", 1)
    at = text.index(SUMMARY_ANCHOR) + len(SUMMARY_ANCHOR)
    text = text[:at] + block + text[at:]
    text = text.replace("\n</body>", "\n" + PATH_JS + "\n</body>", 1)

    return text, "%d steps · %s" % (
        len(steps), " → ".join(s.get("goto") or "off-screen" for s in steps))


# ── driver ────────────────────────────────────────────────────────────────

def build(page):
    path = os.path.join(REPO, page)
    text = open(path, encoding="utf-8").read()
    data = load(page)
    text, m1 = build_tabs(page, text, data)
    text, m2 = build_path(page, text, data)
    open(path, "w", encoding="utf-8").write(text)
    return "%-22s %s | %s" % (page, m1, m2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        print(build(p))
