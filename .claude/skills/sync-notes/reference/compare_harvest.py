#!/usr/bin/env python3
"""Phase 2 check of sync-notes: classify a fresh harvest against the pre-run backup.

    python3 compare_harvest.py ~/MBA/.mba-sync/backup-<stamp>            # report only
    python3 compare_harvest.py ~/MBA/.mba-sync/backup-<stamp> --apply    # restore baselines

Every raw file written since the backup is put in one of four buckets:

    IDENTICAL   byte-for-byte the same as the backup
    FORMAT      same words, different bytes — agent whitespace, or Notion's markup format
                changing under us (it switched to an HTML-flavoured form on 2026-10-23).
                --apply restores the backup's bytes, so apply_harvest.py sees no change and
                rewrites nothing.
    REAL        the words differ. Verify each with your own notion-fetch before applying.
    NEW         no backup copy — a page that did not exist at the last sync.

Words are compared after both sides go through convert(), with markup, URLs and image
references (old `![[…]]` or new `<image source=…>`) reduced to placeholders. That makes
the check blind to formatting by design, and only to formatting.
"""
import glob, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert_core import convert

SYNC = os.path.join(os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA")), ".mba-sync")

def words(t):
    t = re.sub(r'<image source="[^"]*"\s*/>|!\[\[[^\]]*\]\]', " IMG ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[*_#>|`=~\\\-\[\]!()]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    backup = os.path.abspath(os.path.expanduser(args[0]))
    braw = os.path.join(backup, "raw")
    since = os.path.getmtime(os.path.join(backup, "notes-state.json"))
    out = {k: [] for k in ("IDENTICAL", "FORMAT", "REAL", "NEW")}
    for p in sorted(glob.glob(os.path.join(SYNC, "raw", "*.txt"))):
        if os.path.getmtime(p) < since:
            continue
        k = os.path.basename(p)
        bp = os.path.join(braw, k)
        if not os.path.exists(bp):
            out["NEW"].append(k); continue
        n, o = open(p, encoding="utf-8").read(), open(bp, encoding="utf-8").read()
        if n == o:
            out["IDENTICAL"].append(k)
        elif words(convert(n)) == words(convert(o)):
            out["FORMAT"].append(k)
            if "--apply" in sys.argv:
                shutil.copy2(bp, p)
        else:
            out["REAL"].append(k)
    for k, v in out.items():
        print(f"{k:10} {len(v)}")
        if k in ("REAL", "NEW"):
            for f in v:
                print(f"    {f}")
    if out["FORMAT"]:
        print("\nFORMAT files " + ("restored to the backup's bytes." if "--apply" in sys.argv
                                   else "would be restored by --apply."))

if __name__ == "__main__":
    main()
