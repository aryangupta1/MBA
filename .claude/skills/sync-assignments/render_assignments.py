#!/usr/bin/env python3
"""Render the Notion Assignments/Exams rows into the Obsidian vault, and report what moved.

Input   ~/MBA/.mba-sync/assignments.tsv   title <tab> type <tab> status <tab> due <tab> course
Output  ~/MBA/Assignments & Exams.md
Also    ~/MBA/.mba-sync/assignments.prev.tsv   (snapshot, for the next run's diff)

The whole note is regenerated every run, so additions, deletions, status changes and
date changes are all handled by construction. Nothing is merged in place.
"""
import csv, os, sys, collections, datetime

VAULT = os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA"))
SYNC = os.path.join(VAULT, ".mba-sync")
SRC = os.path.join(SYNC, "assignments.tsv")
PREV = os.path.join(SYNC, "assignments.prev.tsv")
NOTE = os.path.join(VAULT, "Assignments & Exams.md")
CALLOUT = os.path.join(SYNC, "dashboard-callout.md")

def load(path):
    if not os.path.exists(path):
        return []
    return [r for r in csv.reader(open(path), delimiter="\t") if r and len(r) >= 5]

rows = load(SRC)
if not rows:
    sys.exit(f"ERROR: {SRC} is missing or empty — query Notion first (see SKILL.md).")

prev = load(PREV)
courses = {}
for r in csv.reader(open(os.path.join(SYNC, "courses.tsv")), delimiter="\t"):
    if r: courses[r[1]] = (r[2], r[3])

# ---------- diff against the previous snapshot ----------
def key(r): return (r[0], r[4])          # title + course identifies a row
old = {key(r): r for r in prev}
new = {key(r): r for r in rows}
added   = [new[k] for k in new if k not in old]
removed = [old[k] for k in old if k not in new]
changed = [(old[k], new[k]) for k in new if k in old and old[k] != new[k]]

# ---------- render ----------
ORDER = ["DMBA6008", "DMBA6005", "DMBA6001", "DMBA6002", "DMBA6004", "-"]
by = collections.defaultdict(list)
for title, typ, status, due, code in rows:
    by[code].append((due, title, typ, status))

LABEL = {"Complete": "done", "In Progress": "in progress", "Not Started": "not started"}
today = datetime.date.today().isoformat()

out = ["---", 'title: "Assignments & Exams"', 'type: "tracker"', 'publish: "false"',
       f'source: "Notion — Assignments/Exams database"', f'synced: "{today}"',
       "tags:", '  - "index"', '  - "tracker"', "---", "",
       "# Assignments & Exams", "",
       f"Synced from the Notion **Assignments/Exams** database on {today} — {len(rows)} rows.",
       "Notion remains the place to create and track assignments; this note is the read-only",
       "mirror inside the vault. Edit in Notion, then re-sync — local edits here are overwritten.", "",
       "> [!warning] Not for publication",
       "> Personal study planning. Marked `publish: false`; it must never reach the website.", ""]

open_items = [(c, r) for c in by for r in by[c] if r[3] in ("Not Started", "In Progress")]
out += ["## Still open", ""]
if open_items:
    out += ["| Due | Course | Item | Status |", "|---|---|---|---|"]
    for code, (due, title, typ, status) in sorted(open_items, key=lambda x: (x[1][0] or "9999")):
        overdue = due not in ("-", "") and due < today
        mark = " ⚠️" if overdue else ""
        out.append(f"| {due if due != '-' else '—'}{mark} | {code if code != '-' else '—'} | {title} | **{LABEL.get(status, status)}** |")
    out.append("")
    if any(d[1][0] not in ("-", "") and d[1][0] < today for d in open_items):
        out += ["⚠️ = past its due date and still not complete.", ""]
else:
    out += ["Nothing outstanding.", ""]

for code in ORDER:
    if code not in by: continue
    if code == "-":
        out += ["## General / unassigned", ""]
    else:
        name, sem = courses.get(code, (code, ""))
        out += [f"## {code} — {name}", "", f"*{sem}*", ""]
    out += ["| Due | Item | Type | Status |", "|---|---|---|---|"]
    for due, title, typ, status in sorted(by[code], key=lambda x: (x[0] or "9999")):
        out.append(f"| {due if due != '-' else '—'} | {title} | {typ} | {LABEL.get(status, status)} |")
    out.append("")

if os.path.exists(CALLOUT):
    out += [open(CALLOUT).read().rstrip(), ""]

with open(NOTE, "w") as f:
    f.write("\n".join(out).rstrip() + "\n")

# snapshot for next run
with open(PREV, "w", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(rows)

# ---------- report ----------
print(f"wrote {NOTE}")
print(f"  {len(rows)} rows · {len(open_items)} still open")
if not prev:
    print("  (no previous snapshot — first sync, so no diff)")
else:
    print(f"  added {len(added)} · removed {len(removed)} · changed {len(changed)}")
    for r in added:   print(f"    + {r[4]} {r[0]} ({r[2]}, due {r[3]})")
    for r in removed: print(f"    - {r[4]} {r[0]}")
    for o, n in changed:
        diffs = []
        for i, lbl in ((1, "type"), (2, "status"), (3, "due")):
            if o[i] != n[i]: diffs.append(f"{lbl} {o[i]} -> {n[i]}")
        print(f"    ~ {n[4]} {n[0]}: {'; '.join(diffs)}")
