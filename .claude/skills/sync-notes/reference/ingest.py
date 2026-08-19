#!/usr/bin/env python3
"""Post-process one raw Notion page dump: download its images NOW (presigned URLs
expire in ~5 minutes) and rewrite them to vault-relative attachment paths."""
import sys, os, re, subprocess, hashlib

VAULT = os.path.expanduser("~/MBA")
ATT = os.path.join(VAULT, "_attachments")
raw_path = sys.argv[1]
key = os.path.splitext(os.path.basename(raw_path))[0]

with open(raw_path) as f:
    text = f.read()

# Notion emits images either as markdown or as an <img>/<image> tag.
PATTERNS = [
    re.compile(r'!\[[^\]]*\]\((https?://[^)\s]+)\)'),
    re.compile(r'<im(?:g|age)[^>]*src="(https?://[^"]+)"[^>]*/?>'),
    re.compile(r'<image[^>]*>\s*(https?://\S+?)\s*</image>'),
]

urls = []
for p in PATTERNS:
    urls += p.findall(text)
urls = list(dict.fromkeys(urls))

mapping = {}
for i, url in enumerate(urls, 1):
    base = url.split("?")[0].rstrip("/").split("/")[-1]
    base = re.sub(r'[^A-Za-z0-9._-]', '_', base) or "image"
    if "." not in base:
        base += ".png"
    name = f"{key}-{i:02d}-{base}"
    dest = os.path.join(ATT, name)
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-o", dest, url],
                       capture_output=True, text=True)
    ok = r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 0
    if ok:
        # reject HTML error bodies masquerading as an image
        with open(dest, "rb") as fh:
            head = fh.read(200).lower()
        if b"<html" in head or b"<?xml" in head and b"error" in head:
            ok = False
            os.remove(dest)
    if ok:
        mapping[url] = name
        print(f"  IMG ok  {name}  ({os.path.getsize(dest)} bytes)")
    else:
        print(f"  IMG FAIL {url[:90]}  rc={r.returncode} {r.stderr[:120]}")

for url, name in mapping.items():
    text = text.replace(url, f"ATTACHMENT::{name}")

with open(raw_path, "w") as f:
    f.write(text)
print(f"  images: {len(mapping)}/{len(urls)} downloaded")
