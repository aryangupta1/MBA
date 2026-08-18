#!/usr/bin/env python3
"""Copy a week's vault images into the repo, downscaled, and report the <img> tags to use.

    python3 publish_images.py DMBA6008 3

Vault images are full-resolution screenshots (up to 2.6MB). They are downscaled with
`sips` — a macOS builtin, not a project dependency — and written to
`assets/notes/<CODE>/wk<N>/`. Nothing is overwritten unless the source differs.

This does NOT write alt text. The page builder must supply a real description of what
each figure shows; a filename is not alt text.
"""
import os, sys, re, json, subprocess, hashlib, shutil

VAULT = os.environ.get("MBA_VAULT", os.path.expanduser("~/MBA"))
ATT = os.path.join(VAULT, "_attachments")

def _repo_root():
    d = os.path.dirname(os.path.abspath(__file__))
    while d != "/":
        if os.path.isdir(os.path.join(d, ".claude")): return d
        d = os.path.dirname(d)
    return os.getcwd()

REPO = _repo_root()
MAX_W = 1600

VAULT_NAME = re.compile(r"^([0-9a-f]{32})-(\d+)-(.*)$")

def slug(s):
    """Vault names are `<32-hex notion id>-<nn>-<original>`, unique by construction.
    Keep enough of the id to STAY unique — stripping it entirely collapses every image
    on a page onto one filename, and they silently overwrite each other."""
    m = VAULT_NAME.match(s)
    if m:
        # Use the FULL notion id. Truncating it collides: sibling pages in this workspace
        # share long id prefixes, so 8- and 12-char prefixes both silently overwrote images.
        nid, idx, base = m.group(1), m.group(2), m.group(3)
        base = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-.")
        return f"{nid}-{idx}-{base}".lower()
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-.").lower()

def main():
    code, wk = sys.argv[1], sys.argv[2]
    disc = subprocess.run(
        [sys.executable, os.path.join(REPO, ".claude/skills/sync-subject/reference/vault_discover.py"),
         code, "--json"], capture_output=True, text=True)
    if disc.returncode:
        sys.exit(disc.stderr)
    data = json.loads(disc.stdout)

    week = next((w for k, w in data["weeks"].items() if str(w["weekNumber"]) == str(wk)), None)
    if not week:
        sys.exit(f"no week {wk} for {code}")

    outdir = os.path.join(REPO, "assets", "notes", code.lower(), f"wk{wk}")
    os.makedirs(outdir, exist_ok=True)
    results = []
    for topic in week["topics"]:
        for rel in topic["files"]:
            text = open(os.path.join(VAULT, rel), encoding="utf-8").read()
            for name in re.findall(r"!\[\[([^\]]+)\]\]", text):
                src = os.path.join(ATT, name)
                if not os.path.exists(src):
                    results.append(dict(topic=topic["topic"], name=name, status="MISSING")); continue
                dst = os.path.join(outdir, slug(name))
                before = os.path.getsize(src)
                stamp = os.path.join(outdir, "." + os.path.basename(dst) + ".src")
                srchash = hashlib.sha256(open(src, "rb").read()).hexdigest()[:16]
                fresh = (os.path.exists(dst) and os.path.getsize(dst) > 0
                         and os.path.exists(stamp) and open(stamp).read().strip() == srchash)
                if not fresh:
                    shutil.copy2(src, dst)
                    # Only resize when the image is actually oversized. Running sips on an
                    # already-small PNG re-encodes it and can inflate it many times over.
                    w = subprocess.run(["sips", "-g", "pixelWidth", dst],
                                       capture_output=True, text=True).stdout
                    m2 = re.search(r"pixelWidth:\s*(\d+)", w)
                    if m2 and int(m2.group(1)) > MAX_W:
                        subprocess.run(["sips", "-Z", str(MAX_W), dst],
                                       capture_output=True, text=True)
                        if os.path.getsize(dst) > before:      # re-encode made it worse
                            shutil.copy2(src, dst)
                    open(stamp, "w").write(srchash)
                after = os.path.getsize(dst)
                results.append(dict(
                    topic=topic["topic"], name=name,
                    src=os.path.relpath(dst, REPO),
                    kb_before=round(before/1024), kb_after=round(after/1024),
                    status="ok"))

    mapping = {}
    for r in results:
        if r["status"] != "ok": continue
        mapping.setdefault(r["src"], set()).add(r["name"])
    clashes = {d: n for d, n in mapping.items() if len(n) > 1}
    if clashes:
        for d, n in clashes.items():
            print(f"FATAL collision: {d} <- {sorted(n)}")
        sys.exit("output filenames are not unique; refusing to publish images")

    total = sum(r.get("kb_after", 0) for r in results if r["status"] == "ok")
    print(f"{code} week {wk} — {len([r for r in results if r['status']=='ok'])} image(s) "
          f"-> assets/notes/{code.lower()}/wk{wk}/  ({total} KB total)\n")
    for r in results:
        if r["status"] != "ok":
            print(f"  MISSING  {r['name']}  (referenced by {r['topic']})"); continue
        print(f"  {r['topic']}")
        print(f"    {r['src']}   {r['kb_before']}KB -> {r['kb_after']}KB")
        print(f'    <img src="{r["src"]}" alt="TODO — describe what this figure shows" loading="lazy">')
    if any(r["status"] != "ok" for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main()
