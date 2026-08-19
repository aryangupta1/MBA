#!/usr/bin/env python3
"""Phase 3 of sync-notes: convert harvested Notion dumps into vault notes WITHOUT
destroying anything Aryan wrote in Obsidian.

    python3 apply_harvest.py [--dry-run] [--seed] [--force PATH_OR_ID ...]

Aryan writes in BOTH tools. A blind rebuild would silently delete Obsidian-only work, so
every note is classified against two independent hashes before it is touched:

    notion_changed = sha256(raw dump)  != state.raw_sha
    local_changed  = sha256(vault .md) != state.file_sha   (what THIS sync last wrote)

    notion  local   ->  action
    ------  -----       ------
      no      no        UNCHANGED   nothing written
      yes     no        UPDATED     safe to overwrite
      no      yes       KEPT-LOCAL  his edit stands; Notion had nothing new to say
      yes     yes       CONFLICT    his file is LEFT ALONE; Notion's version is parked
                                    beside it as <name>.notion-incoming.md

Nothing in this script ever overwrites an edited file. --force is the only override and
it backs the file up to <name>.local-backup.md first.
"""
import os, re, json, csv, glob, sys, hashlib, argparse, datetime

VAULT = os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA"))
SYNC = os.path.join(VAULT, ".mba-sync")
RAW = os.path.join(SYNC, "raw")
STATE = os.path.join(SYNC, "notes-state.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert_core import convert, unescape, safe

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ap.add_argument("--seed", action="store_true",
                help="adopt the vault as-is as the baseline; write nothing")
ap.add_argument("--force", nargs="*", default=[],
                help="notion ids to overwrite despite local edits (backs up first)")
a = ap.parse_args()
FORCE = set(a.force)

def sha(b):
    if isinstance(b, str): b = b.encode("utf-8")
    return hashlib.sha256(b).hexdigest()

def file_sha(p):
    return sha(open(p, "rb").read()) if os.path.exists(p) else None

plan = json.load(open(os.path.join(SYNC, "plan.json")))
byid = {p["id"]: p for p in plan}

children = []
for cpath in [os.path.join(SYNC, "children.tsv")] + sorted(glob.glob(os.path.join(SYNC, "children.d", "*.tsv"))):
    if os.path.exists(cpath):
        with open(cpath, newline="", encoding="utf-8") as f:
            children += [r for r in csv.reader(f, delimiter="\t") if r and len(r) >= 3]
_seen, _u = set(), []
for r in children:
    if r[0] not in _seen:
        _seen.add(r[0]); _u.append(r)
children = _u

kids_of, child_meta = {}, {}
for cid, pid, title in [(r[0], r[1], r[2]) for r in children]:
    kids_of.setdefault(pid, []).append(cid)
    child_meta[cid] = dict(id=cid, parent=pid, name=title)

def resolve(cid):
    m = child_meta[cid]; p = m["parent"]
    if p in byid:
        parent_dir = os.path.join(byid[p]["dir"], safe(byid[p]["name"])); root = byid[p]
    else:
        if p not in child_meta:
            return None, None
        pp, root = resolve(p)
        if pp is None: return None, None
        parent_dir = os.path.splitext(pp)[0]
    return os.path.join(parent_dir, safe(m["name"]) + ".md"), root

def yaml_str(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

def frontmatter(d):
    lines = ["---"]
    for k, v in d.items():
        if v is None or v == "" or v == "-": continue
        if isinstance(v, list):
            lines.append(f"{k}:"); lines += [f"  - {yaml_str(x)}" for x in v]
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    return "\n".join(lines)

state = json.load(open(STATE)) if os.path.exists(STATE) else {"version": 1, "notes": {}}
notes_state = state.setdefault("notes", {})
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

tally = {k: [] for k in ("NEW", "UPDATED", "UNCHANGED", "KEPT-LOCAL", "CONFLICT", "FORCED", "NO-RAW")}

def handle(nid, path, fm, rawtext, edited):
    """Classify and write one page. Returns the action taken."""
    full = os.path.join(VAULT, path)
    rendered = frontmatter(fm) + "\n\n" + convert(rawtext) + "\n"
    r_sha, n_sha = sha(rawtext), sha(rendered)
    prev = notes_state.get(nid, {})
    disk = file_sha(full)

    notion_changed = prev.get("raw_sha") != r_sha
    local_changed = disk is not None and prev.get("file_sha") not in (None, disk)
    exists = disk is not None

    def record(fs):
        notes_state[nid] = dict(path=path, raw_sha=r_sha, file_sha=fs,
                                edited=edited, synced=now)

    if a.seed:
        record(disk); return "UNCHANGED"

    if not exists:
        if not a.dry_run:
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w", encoding="utf-8").write(rendered)
            record(n_sha)
        return "NEW"

    if local_changed and nid in FORCE:
        if not a.dry_run:
            os.replace(full, os.path.splitext(full)[0] + ".local-backup.md")
            open(full, "w", encoding="utf-8").write(rendered)
            record(n_sha)
        return "FORCED"

    if local_changed and notion_changed:
        side = os.path.splitext(full)[0] + ".notion-incoming.md"
        if not a.dry_run:
            open(side, "w", encoding="utf-8").write(rendered)
            # raw_sha advances so the same conflict is not re-reported forever;
            # file_sha does NOT, because his file is still his.
            notes_state[nid] = dict(path=path, raw_sha=r_sha, file_sha=prev.get("file_sha"),
                                    edited=edited, synced=now, conflict=side[len(VAULT) + 1:])
        return "CONFLICT"

    if local_changed:
        return "KEPT-LOCAL"

    if notion_changed or disk != prev.get("file_sha"):
        if disk == n_sha:
            if not a.dry_run: record(n_sha)
            return "UNCHANGED"
        if not a.dry_run:
            open(full, "w", encoding="utf-8").write(rendered)
            record(n_sha)
        return "UPDATED"

    return "UNCHANGED"

for p in plan:
    raw = os.path.join(RAW, p["id"] + ".txt")
    if not os.path.exists(raw):
        tally["NO-RAW"].append(p["file"]); continue
    text = open(raw, encoding="utf-8").read()
    kids = [safe(child_meta[c]["name"]) for c in kids_of.get(p["id"], [])]
    fm = {"title": unescape(p["name"]), "course": p["course"], "course_name": p["course_name"],
          "semester": p["semester"], "week": p["notebook"], "type": p["type"],
          "confidence": p["confidence"],
          "publish": "true" if p["type"] == "Pre-Live Session" else "false",
          "notion_id": p["id"], "created": p["created"], "edited": p["edited"],
          "tags": [f"course/{p['course']}", f"type/{(p['type'] or 'untyped').replace(' ', '-')}"]}
    if kids: fm["subpages"] = kids
    tally[handle(p["id"], p["file"], fm, text, p["edited"])].append(p["file"])

# children of in-scope notes only
def in_scope(cid):
    seen = set()
    while cid in child_meta and cid not in seen:
        seen.add(cid); cid = child_meta[cid]["parent"]
    return cid in byid

for cid, m in child_meta.items():
    if not in_scope(cid): continue
    raw = os.path.join(RAW, cid + ".txt")
    path, root = resolve(cid)
    if path is None: continue
    if not os.path.exists(raw):
        tally["NO-RAW"].append(path); continue
    text = open(raw, encoding="utf-8").read()
    kids = [safe(child_meta[c]["name"]) for c in kids_of.get(cid, [])]
    fm = {"title": unescape(m["name"]), "course": root["course"], "course_name": root["course_name"],
          "semester": root["semester"], "week": root["notebook"], "type": root["type"],
          "publish": "true" if root["type"] == "Pre-Live Session" else "false",
          "parent_note": unescape(root["name"]), "notion_id": cid,
          "tags": [f"course/{root['course']}", f"type/{(root['type'] or 'untyped').replace(' ', '-')}"]}
    if kids: fm["subpages"] = kids
    tally[handle(cid, path, fm, text, root["edited"])].append(path)

if not a.dry_run:
    state["version"] = 1
    json.dump(state, open(STATE, "w"), indent=1)

print("DRY RUN — nothing written\n" if a.dry_run else ("SEEDED baseline\n" if a.seed else ""))
for k in ("NEW", "UPDATED", "CONFLICT", "KEPT-LOCAL", "FORCED", "UNCHANGED", "NO-RAW"):
    v = tally[k]
    if not v: continue
    print(f"{k:11} {len(v)}")
    if k in ("CONFLICT", "KEPT-LOCAL", "FORCED", "NO-RAW", "NEW", "UPDATED"):
        for f in v[:40]: print(f"    {f}")

if tally["CONFLICT"]:
    print("\n*** CONFLICTS — your Obsidian edits were NOT overwritten. ***")
    print("Notion's version sits beside each file as <name>.notion-incoming.md.")
    print("Diff, merge by hand, then delete the sidecar. Nothing is lost either way.")
