#!/usr/bin/env python3
"""Cache busting: stamp current content hashes of style.css/site.js/og*.png into all HTML pages.
Run after any change to assets/, before committing.

The OG card is stamped too, and each page gets the card for ITS language:
social scrapers cache link previews by image URL for days and offer no purge,
so a redesigned (or wrong-language) card under the old URL would keep showing."""
import hashlib, pathlib, re

root = pathlib.Path(__file__).parent
LOCALES = ("ua", "de", "fr", "pl", "es")  # everything else is the EN root


def digest(name):
    return hashlib.md5((root / "assets" / name).read_bytes()).hexdigest()[:8]


vcss, vjs = digest("style.css"), digest("site.js")
vlogo, vicon = digest("logo.png"), digest("apple-touch-icon.png")
og = {loc: (f"og-{loc}.png", digest(f"og-{loc}.png")) for loc in LOCALES}
og["en"] = ("og.png", digest("og.png"))

count = 0
for f in root.rglob("*.html"):
    if ".git" in str(f) or "tools" in f.parts:
        continue
    rel = f.relative_to(root)
    loc = rel.parts[0] if rel.parts[0] in LOCALES else "en"
    name, vog = og[loc]
    h = f.read_text()
    h2 = re.sub(r'/assets/style\.css(\?v=[0-9a-f]+)?"', f'/assets/style.css?v={vcss}"', h)
    h2 = re.sub(r'/assets/site\.js(\?v=[0-9a-f]+)?"', f'/assets/site.js?v={vjs}"', h2)
    h2 = re.sub(r'/assets/logo\.png(\?v=[0-9a-f]+)?"', f'/assets/logo.png?v={vlogo}"', h2)
    h2 = re.sub(
        r'/assets/apple-touch-icon\.png(\?v=[0-9a-f]+)?"',
        f'/assets/apple-touch-icon.png?v={vicon}"',
        h2,
    )
    # matches any card, so a page moving between locales is re-pointed too
    h2 = re.sub(r'/assets/og(-[a-z]{2})?\.png(\?v=[0-9a-f]+)?"', f'/assets/{name}?v={vog}"', h2)
    if h2 != h:
        f.write_text(h2)
        count += 1
print(f"css={vcss} js={vjs} og={ {k: v[1] for k, v in og.items()} }, updated {count} pages")
