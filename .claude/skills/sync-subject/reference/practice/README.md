# The practice components

Three things every semester-2 week page carries, on top of the five modes the
sync produces:

| Component | Where it lives | What it is |
| --- | --- | --- |
| **Study path** | first block of the Summary panel, `00 / Start here` | "How to master this week" — a numbered route through the modes this week actually has, each step able to jump to its tab |
| **Quiz** | its own tab | multiple choice, four options, one right, a hint per question and a note on every option |
| **Apply it** | its own tab | scenarios with three staged hints, a walkthrough and a self-mark checklist |

**They are derived from the built page, not from Notion** — exactly like the
Acronyms and Formulas tabs. Nothing in this folder reads a notebook.

## Files

```
practice/
  build.py         splices all three into a page; safe to re-run
  tpl/quiz.css     stylesheet for the quiz and apply-it panels
  tpl/quiz.js      the shared renderer for both
  tpl/path.css     stylesheet for the study path
  data/<PAGE>.json the authored content, one file per week page
```

`build.py` runs from the repo root:

```
python3 .claude/skills/sync-subject/reference/practice/build.py DMBA6008-week3.html
```

It skips a component the page already has, so re-running is harmless. To
**rebuild** a page's practice content after re-authoring its JSON, regenerate
the page first and then run this — splicing over the top will not replace what
is already there.

## When a week changes, this changes

**This is binding on every sync.** A week page that gains a topic, loses a
placeholder, or has its prose reviewed has changed the material the quiz and
the scenarios are drawn from, so:

1. **Re-derive the JSON for that page** from the rebuilt page — new questions
   for the new material, and any question whose answer the change invalidated
   removed or rewritten.
2. **Re-check the study path.** A week that gains a topic needs its route
   updated; a week whose placeholder was filled must stop saying the topic is
   not written.
3. **Sweep the counts.** The hero pill (`N quiz questions`), the hub card and
   the hub's mode list all quote numbers.

The same rules that govern the page govern this content: it is **extraction,
not addition**. Everything must be supported by what the page states; no
formula that sat in an unpublished image, no repaired typo, no completed
truncation, no reconciled inconsistency, and nothing from a Live Session note.

## The data shape

```jsonc
{
  "page": "DMBA6008-week3.html",
  "quizIntro": "One paragraph, 40–70 words, in the page's voice.",
  "applyIntro": "One paragraph, 40–70 words.",

  "studyPath": {
    "intro": "One or two sentences: the route, and roughly how long a full pass takes.",
    "steps": [                       // 5–7, sequential
      {
        "goto": "summary",           // a data-panel key on THIS page, or null
        "label": "Read the summary in order",
        "detail": "Two or three sentences of advice specific to this week.",
        "time": "~25 min"
      }
    ],
    "close": "One sentence: the concrete test for whether the week has landed."
  },

  "quiz": [                          // scale to the page: ~1 per 3 blocks
    {
      "topic": "Concept of present value",   // an existing data-topic or TERMS src
      "q": "The stem.",
      "hint": "A nudge that does not name the answer or eliminate an option.",
      "options": [                   // exactly 4, exactly one ok:true
        { "t": "…", "ok": false, "note": "Why this is wrong, grounded in the page." },
        { "t": "…", "ok": true,  "note": "Why this is right." },
        { "t": "…", "ok": false, "note": "…" },
        { "t": "…", "ok": false, "note": "…" }
      ]
    }
  ],

  "scenarios": [                     // 4–6
    {
      "topic": "Investment Appraisal",
      "title": "Three to six words",
      "setup": "2–4 sentences. Qualitative unless the page supplies the figures.",
      "task": "One sentence: what you are being asked to decide.",
      "hints": ["widest", "narrower", "narrowest — still not the answer"],
      "walkthrough": ["step", "step", "step"],       // 3–6
      "checklist": ["a point a strong answer covers"] // 3–5
    }
  ]
}
```

`build.py` asserts every one of those shape constraints before it touches a
page, so a malformed file fails loudly rather than shipping.

### Authoring rules that are not in the schema

- **Vary where the correct answer sits.** Not index 1 every time.
- **Distractors are the confusions a real learner has**, not filler — profit
  versus cash flow, present value versus the future surplus, a persona versus
  a user story. An obviously silly option wastes the question.
- **No "all of the above", no "none of the above"**, at most one negated stem
  per quiz.
- **A topic the page marks unwritten gets nothing** — no question, no scenario,
  no hint that speculates about its contents.
- **The study path's `detail` is where the value is.** A step that would read
  the same on any page of the site is a wasted step.
- Australian spelling, literal UTF-8 punctuation, plain text — the renderer
  escapes everything, so an HTML entity in the JSON ships double-escaped.

## Gate note

`checks.py` counts `<ol class="path">` as an artefact rather than flowing
prose, the same way it already treats `.steps` and `.takeaways`. The study
path is navigation advice, not week prose, and on a short week it would
otherwise push the topic over its budget.
