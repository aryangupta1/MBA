#!/usr/bin/env python3
"""Phase 0 discovery for sync-subject, sourced from the Obsidian vault (not Notion).

Walks ~/MBA for one subject, applies the publish filter and the subject's syncRules,
and diffs every topic against the recorded state by content hash.

    python3 vault_discover.py DMBA6008 [--json]

A "topic" is the fan-out unit Phase 2 and Phase 3 expect: the first level beneath a
week's note. A note with a sibling folder is a container and its children are the
topics; a note without one is itself a single topic. A topic's content is its own file
plus every descendant beneath it, so grandchildren are never lost.
"""
import os, sys, re, json, hashlib, argparse

VAULT = os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA"))
def _repo_root():
    """Derive the repo from this file's own location — never from the working directory,
    which is routinely changed to the vault during a sync."""
    d = os.path.dirname(os.path.abspath(__file__))
    while d != "/":
        if os.path.isdir(os.path.join(d, ".claude")):
            return d
        d = os.path.dirname(d)
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

REPO = _repo_root()
SUBJECTS = os.path.join(REPO, ".claude/skills/sync-subject/subjects.json")
STATE = os.path.join(REPO, "docs/vault-sync-state.json")

FM = re.compile(r"^---\n(.*?)\n---\n", re.S)

def frontmatter(path):
    m = FM.match(open(path, encoding="utf-8").read())
    if not m: return {}
    out = {}
    for line in m.group(1).splitlines():
        if line.startswith(("  - ", "  -")) or not line.strip(): continue
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"')
    return out

def body(path):
    t = open(path, encoding="utf-8").read()
    return FM.sub("", t, count=1)

def week_num(folder):
    m = re.search(r"week\s*(\d+)", folder, re.I)
    return int(m.group(1)) if m else None

def descendants(md_path):
    """A note's own file plus every file beneath its same-named folder, recursively."""
    files = [md_path]
    sub = os.path.splitext(md_path)[0]
    if os.path.isdir(sub):
        for root, _, names in os.walk(sub):
            files += [os.path.join(root, n) for n in sorted(names) if n.endswith(".md")]
    return sorted(files)

def load_rules(code, subjects):
    return subjects.get(code, {}).get("syncRules", [])

def rule_hit(rules, title, week_no, notion_id=None):
    """Return the rule id that excludes this title, or None.

    allowedNotionIds is an explicit carve-out. It exists because a note Aryan approved can
    sit in _Unfiled with no week number, where a week-based rule would wrongly drop it.
    """
    t = (title or "").lower()
    for r in rules:
        rid = r.get("id", "")
        if notion_id and notion_id in r.get("allowedNotionIds", []):
            continue
        if rid == "no-pre-class-prep" and t.startswith("pre-class prep"):
            return rid
        if rid == "no-shadow-boxing-after-week-0" and t.startswith("shadow boxing") and week_no not in (0,):
            return rid
    return None

def placement(rules, notion_id):
    """A week folder name an approved but unfiled note should be published under."""
    for r in rules:
        if notion_id and notion_id in r.get("allowedNotionIds", []):
            return r.get("placeUnderWeek")
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    subjects = json.load(open(SUBJECTS))
    if args.code not in subjects:
        sys.exit(f"unknown subject {args.code}")
    subj = subjects[args.code]
    rules = load_rules(args.code, subjects)
    semdir = {"SEM 1 2026": "Semester 1 2026", "SEM 2 2026": "Semester 2 2026"}[subj["semester"]]

    root = None
    base = os.path.join(VAULT, semdir)
    for d in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if d.startswith(args.code):
            root = os.path.join(base, d); break
    if not root:
        sys.exit(f"no vault folder for {args.code} under {base}")

    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    prev = state.get(args.code, {}).get("weeks", {})

    review_by_id = {n["notionId"]: n for n in subj.get("needsReview", [])}
    weeks, skipped, unfiled, review = {}, [], [], []
    for wk in sorted(os.listdir(root)):
        wdir = os.path.join(root, wk)
        if not os.path.isdir(wdir): continue
        wno = week_num(wk)
        notes = [f for f in sorted(os.listdir(wdir)) if f.endswith(".md")]
        topics = []
        for nf in notes:
            npath = os.path.join(wdir, nf)
            fm = frontmatter(npath)
            if not fm.get("notion_id"):        # index notes this repo generates
                continue
            title = fm.get("title", os.path.splitext(nf)[0])
            if fm.get("publish") != "true":
                skipped.append((wk, title, f"publish=false ({fm.get('type','?')})"))
                continue
            nid = fm.get("notion_id")
            rid = rule_hit(rules, title, wno, nid)
            if rid:
                skipped.append((wk, title, f"syncRules: {rid}")); continue

            sub = os.path.splitext(npath)[0]
            children = ([os.path.join(sub, c) for c in sorted(os.listdir(sub)) if c.endswith(".md")]
                        if os.path.isdir(sub) else [])
            units = [(os.path.splitext(os.path.basename(c))[0], c) for c in children] or [(title, npath)]
            for tname, tpath in units:
                tfm = frontmatter(tpath)
                tnid = tfm.get("notion_id")
                if tnid in review_by_id:
                    review.append((wk, tname, review_by_id[tnid])); continue
                trid = rule_hit(rules, tname, wno, tnid)
                if trid:
                    skipped.append((wk, f"{title} / {tname}", f"syncRules: {trid}")); continue
                files = descendants(tpath)
                text = "\n".join(body(f) for f in files)
                topics.append(dict(
                    topic=tname,
                    notionId=tnid,
                    note=title,
                    files=[os.path.relpath(f, VAULT) for f in files],
                    contentHash=hashlib.sha256(text.encode()).hexdigest()[:12],
                    words=len(text.split()),
                    images=len(re.findall(r"!\[\[([^\]]+)\]\]", text)),
                ))
        if wk == "_Unfiled":
            for t in topics:
                tgt = placement(rules, t.get("notionId"))
                if tgt:
                    dest = next((k for k in weeks if k == tgt or k.startswith(tgt)), None)
                    if dest is None:
                        dest = next((d for d in os.listdir(root)
                                     if d == tgt or d.startswith(tgt)), tgt)
                        weeks.setdefault(dest, dict(weekNumber=week_num(dest), topics=[]))
                    t["placedFrom"] = "_Unfiled"
                    weeks[dest]["topics"].append(t)
                else:
                    unfiled.append((t["topic"], t["words"]))
            continue
        if topics:
            weeks[wk] = dict(weekNumber=wno, topics=topics)

    # ---- diff
    report = []
    for wk, w in weeks.items():
        old = prev.get(wk, {}).get("topics", {})
        oldh = {t["topic"]: t.get("contentHash") for t in old} if isinstance(old, list) else old
        for t in w["topics"]:
            was = (oldh or {}).get(t["topic"])
            t["status"] = "NEW" if was is None else ("UNCHANGED" if was == t["contentHash"] else "CHANGED")
        st = {t["status"] for t in w["topics"]}
        w["status"] = "NEW" if not oldh else ("UNCHANGED" if st == {"UNCHANGED"} else "CHANGED")
        report.append((wk, w))

    out = dict(code=args.code, vaultRoot=os.path.relpath(root, VAULT), weeks=weeks,
               skipped=skipped, unfiled=unfiled)
    if args.json:
        print(json.dumps(out, indent=1)); return

    print(f"{args.code} — {subj['name']}   (source: vault, {os.path.relpath(root, VAULT)})\n")
    for wk, w in sorted(report, key=lambda x: (x[1]["weekNumber"] is None, x[1]["weekNumber"])):
        n_img = sum(t["images"] for t in w["topics"])
        print(f'{w["status"]:<10} {wk}  — {len(w["topics"])} topic(s), '
              f'{sum(t["words"] for t in w["topics"]):,} words, {n_img} image(s)')
        for t in w["topics"]:
            flag = "" if t["status"] == "UNCHANGED" else f'  <-- {t["status"]}'
            print(f'             {t["status"]:<9} {t["topic"]}  ({t["words"]:,}w, {t["images"]}img){flag}')
    for wk, title, why in skipped:
        print(f'SKIPPED    {wk} — {title} — {why}')
    for wk, tname, n in review:
        print(f'\nNEEDS REVIEW  {wk} — "{tname}"  — HELD BACK, not published')
        print(f'              {n["why"]}')
        print(f'              {n["action"]}\n')
    for t, w in unfiled:
        print(f'UNFILED    {t} ({w:,}w) — no week folder; decide placement before publishing')
    changed = [wk for wk, w in report if w["status"] != "UNCHANGED"]
    print(f'\n{len(changed)} week(s) need work' if changed else '\nNothing changed.')

if __name__ == "__main__":
    main()
