#!/usr/bin/env python3
"""Render the brand mark into the raster logo files the site and profiles need.

The mark itself is assets/logo-mark.svg (two bars + underline, #E5383B -> #FF6B35).
Its paths sit in a 100x100 box but only occupy x 38-62 / y 35.5-63.8, so every
output crops tight to the mark ("37 34 26 31", the same window the header chip
uses) and then scales it deliberately — the old files inherited the padded box
and rendered the mark at a quarter of the frame, which reads as a mistake at
icon sizes.

Outputs:
  assets/logo.png              512x512, paper ground  (Schema.org logo)
  assets/apple-touch-icon.png  180x180, paper ground, full bleed (iOS masks it)
  assets/logo-transparent.png  1024x1024, no ground   (external profiles)

Usage: python3 make-logo.py
"""
import pathlib
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAPER = "#F7F2E9"

# the mark, cropped to its own bounds
MARK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="37 34 26 31">'
    '<defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#E5383B"/><stop offset="1" stop-color="#FF6B35"/>'
    "</linearGradient></defs>"
    '<rect x="38" y="35.5" width="9.6" height="21.6" rx="4.8" fill="url(#mg)"/>'
    '<rect x="52.7" y="40" width="9" height="17.1" rx="4.5" fill="url(#mg)"/>'
    '<rect x="38" y="60.4" width="24" height="3.4" rx="1.7" fill="url(#mg)"/>'
    "</svg>"
)

# name, size, background (None = transparent), size of the SVG BOX as % of the
# canvas — the mark is taller than wide, so it fills that box by height
TARGETS = [
    ("logo.png", 512, PAPER, 70),
    ("apple-touch-icon.png", 180, PAPER, 68),
    ("logo-transparent.png", 1024, None, 92),
]


def page(size, bg, pct):
    ground = f"background:{bg};" if bg else ""
    return (
        "<!doctype html><meta charset='utf-8'><style>"
        "*{margin:0;padding:0}"
        f"html,body{{width:{size}px;height:{size}px;{ground}"
        "display:flex;align-items:center;justify-content:center}"
        # a square box + the SVG's default xMidYMid meet: the mark is taller
        # than it is wide, so sizing by width alone overflows and clips it
        f"svg{{width:{pct}%;height:{pct}%;display:block}}"
        f"</style>{MARK}"
    )


def render(html_path, out, size, transparent, tmp):
    """Chrome 151 never exits on the legacy --headless: use --headless=new and
    poll for the file. Rendered at 2x, then downsampled for clean edges."""
    shot = pathlib.Path(tmp) / "shot.png"
    if shot.exists():
        shot.unlink()
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-sandbox",
        "--force-device-scale-factor=2",
        f"--user-data-dir={tmp}/profile",
        f"--window-size={size},{size}",
        f"--screenshot={shot}",
    ]
    if transparent:
        # without this Chrome paints an opaque white sheet behind the page
        cmd.append("--default-background-color=00000000")
    cmd.append(html_path.as_uri())

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if shot.exists() and shot.stat().st_size > 0:
            break
        time.sleep(1)
    proc.terminate()
    if not shot.exists() or shot.stat().st_size == 0:
        sys.exit(f"Chrome produced no screenshot for {out.name}")
    subprocess.run(
        ["sips", "-z", str(size), str(size), str(shot), "--out", str(out)],
        check=True,
        capture_output=True,
    )


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp) / "logo.html"
        for name, size, bg, pct in TARGETS:
            work.write_text(page(size, bg, pct), encoding="utf-8")
            out = ROOT / "assets" / name
            render(work, out, size, bg is None, tmp)
            ground = bg if bg else "transparent"
            print(f"  {name}: {size}x{size}, {ground} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
