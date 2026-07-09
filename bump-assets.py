#!/usr/bin/env python3
"""Cache busting: stamp current content hashes of style.css/site.js into all HTML pages.
Run after any change to assets/, before committing."""
import hashlib, pathlib, re

root = pathlib.Path(__file__).parent
vcss = hashlib.md5((root / "assets/style.css").read_bytes()).hexdigest()[:8]
vjs = hashlib.md5((root / "assets/site.js").read_bytes()).hexdigest()[:8]
count = 0
for f in root.rglob("*.html"):
    if ".git" in str(f):
        continue
    h = f.read_text()
    h2 = re.sub(r'/assets/style\.css(\?v=[0-9a-f]+)?"', f'/assets/style.css?v={vcss}"', h)
    h2 = re.sub(r'/assets/site\.js(\?v=[0-9a-f]+)?"', f'/assets/site.js?v={vjs}"', h2)
    if h2 != h:
        f.write_text(h2)
        count += 1
print(f"css={vcss} js={vjs}, updated {count} pages")
