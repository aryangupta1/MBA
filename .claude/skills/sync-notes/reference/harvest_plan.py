#!/usr/bin/env python3
"""Phase 1 of sync-notes: turn the Notion inventory into a scoped harvest plan.

    python3 harvest_plan.py DMBA6008 [--week "Week 4"] [--changed-only] [--json]

Reads the inventory TSVs the agent refreshed in Phase 0 and writes plan.json (every
in-scope note's destination path in the vault). Prints the pages to fetch.

Scope is deliberately COURSE-AT-A-TIME. A full-vault re-harvest is 296 fetches and is
almost never what Aryan means by "sync notion".

--changed-only trims to notes whose Notion `edited` is newer than the last sync. Use it
only when Aryan asks for a quick pass: Notion does NOT bump a parent's last-edited time
when a sub-page's body is edited, so this mode misses edits made inside sub-pages, which
is exactly where his lecture notes live. The default fetches the whole scope.
"""
import csv, os, re, json, sys, collections, argparse

VAULT = os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA"))
SYNC = os.path.join(VAULT, ".mba-sync")
STATE = os.path.join(SYNC, "notes-state.json")

ILLEGAL = re.compile(r'[:/\\?*"<>|]')
def safe(s):
    s = ILLEGAL.sub("", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")

def rows(name):
    p = os.path.join(SYNC, name)
    if not os.path.exists(p):
        sys.exit(f"FATAL: missing inventory {p} — run Phase 0 first")
    with open(p, newline="", encoding="utf-8") as f:
        return [r for r in csv.reader(f, delimiter="\t") if r]

SEMDIR = {"SEM 1 2026": "Semester 1 2026", "SEM 2 2026": "Semester 2 2026"}

ap = argparse.ArgumentParser()
ap.add_argument("course")
ap.add_argument("--week", default=None, help="substring match on the notebook/week name")
ap.add_argument("--changed-only", action="store_true")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

courses = {r[0]: dict(code=r[1], name=r[2], semester=r[3], status=r[4]) for r in rows("courses.tsv")}
notebooks = {r[0]: dict(topic=r[1], course=r[2], confidence=r[3]) for r in rows("notebooks.tsv")}
notes = [dict(id=r[0], name=r[1], type=r[2], notebook=r[3], course=r[4],
              created=r[5], edited=r[6]) for r in rows("notes.tsv")]

want = a.course.upper().replace(" ", "")
course_ids = {cid for cid, c in courses.items() if c["code"].upper() == want}
if not course_ids:
    sys.exit(f"FATAL: no course {a.course}. Known: {sorted(c['code'] for c in courses.values())}")

state = json.load(open(STATE)) if os.path.exists(STATE) else {"notes": {}}
known = state.get("notes", {})

plan, skipped = [], []
for n in notes:
    nb = notebooks.get(n["notebook"])
    course_id = nb["course"] if nb else (n["course"] if n["course"] != "-" else None)
    if course_id not in course_ids:
        continue
    c = courses[course_id]
    week = nb["topic"] if nb else None
    if a.week and (week is None or a.week.lower() not in week.lower()):
        continue
    parts = [SEMDIR[c["semester"]], f'{c["code"]} {safe(c["name"])}', safe(week) if nb else "_Unfiled"]
    d = os.path.join(*parts)
    rec = dict(id=n["id"], name=n["name"], type=n["type"], dir=d,
               file=os.path.join(d, safe(n["name"]) + ".md"),
               course=c["code"], course_name=c["name"], semester=c["semester"],
               notebook=week, confidence=nb["confidence"] if nb else None,
               created=n["created"], edited=n["edited"])
    prev = known.get(n["id"])
    rec["status"] = "NEW" if not prev else ("CHANGED" if prev.get("edited") != n["edited"] else "UNCHANGED")
    if a.changed_only and rec["status"] == "UNCHANGED":
        skipped.append(rec); continue
    plan.append(rec)

dupes = [f for f, k in collections.Counter(p["file"] for p in plan).items() if k > 1]

with open(os.path.join(SYNC, "plan.json"), "w") as f:
    json.dump(plan, f, indent=1)

if a.json:
    print(json.dumps(dict(plan=plan, skipped=len(skipped), collisions=dupes), indent=1)); sys.exit(0)

print(f"scope: {want}" + (f"  week~{a.week!r}" if a.week else "  (all weeks)"))
print(f"to fetch: {len(plan)} top-level notes" + (f"   (+{len(skipped)} unchanged, skipped)" if skipped else ""))
if dupes:
    print(f"  WARNING filename collision: {dupes}")
by = collections.Counter(p["status"] for p in plan)
print(f"  {dict(by)}")
print()
for p in plan:
    print(f'{p["status"]:9} {p["id"]}  {p["name"]}   [{p["notebook"] or "_Unfiled"}]')
print()
print("Fetch each id with notion-fetch, RECURSIVELY into child pages, and write the")
print(f'verbatim body to {os.path.join(SYNC, "raw")}/<id>.txt — then run ingest.py on it.')
