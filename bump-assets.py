#!/usr/bin/env python3
"""Cache busting: stamp current content hashes of style.css/site.js/og.png into all HTML pages.
Run after any change to assets/, before committing.

og.png is stamped too because social scrapers (LinkedIn, X, Telegram, Facebook)
cache link previews by image URL for days and offer no purge — a redesigned card
under the old URL would keep showing the old one."""
import hashlib, pathlib, re

root = pathlib.Path(__file__).parent
vcss = hashlib.md5((root / "assets/style.css").read_bytes()).hexdigest()[:8]
vjs = hashlib.md5((root / "assets/site.js").read_bytes()).hexdigest()[:8]
vog = hashlib.md5((root / "assets/og.png").read_bytes()).hexdigest()[:8]
count = 0
for f in root.rglob("*.html"):
    if ".git" in str(f):
        continue
    h = f.read_text()
    h2 = re.sub(r'/assets/style\.css(\?v=[0-9a-f]+)?"', f'/assets/style.css?v={vcss}"', h)
    h2 = re.sub(r'/assets/site\.js(\?v=[0-9a-f]+)?"', f'/assets/site.js?v={vjs}"', h2)
    h2 = re.sub(r'/assets/og\.png(\?v=[0-9a-f]+)?"', f'/assets/og.png?v={vog}"', h2)
    if h2 != h:
        f.write_text(h2)
        count += 1
print(f"css={vcss} js={vjs} og={vog}, updated {count} pages")
