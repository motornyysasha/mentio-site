#!/usr/bin/env python3
"""Render tools/og-card.html into assets/og.png (1200x630).

Renders at 2x with headless Chrome, then downsamples — Chrome's 1x text
rasterisation is noticeably coarser than a supersampled 2x pass, and OG
cards get re-scaled again by every social platform.

Usage: python3 make-og.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "tools" / "og-card.html"
OUT = ROOT / "assets" / "og.png"
W, H = 1200, 630

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    if not SRC.exists():
        sys.exit(f"Source card missing: {SRC}")

    with tempfile.TemporaryDirectory() as tmp:
        shot = pathlib.Path(tmp) / "og@2x.png"
        # --headless=new is required on Chrome 151+: the legacy --headless
        # never exits here, so we also poll for the file and kill the process.
        proc = subprocess.Popen(
            [
                CHROME,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-sandbox",
                "--force-device-scale-factor=2",
                # local @font-face files load over file:// only with this
                "--allow-file-access-from-files",
                f"--user-data-dir={tmp}/profile",
                f"--window-size={W},{H}",
                f"--screenshot={shot}",
                SRC.as_uri(),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(60):
            if shot.exists() and shot.stat().st_size > 0:
                break
            time.sleep(1)
        proc.terminate()
        if not shot.exists() or shot.stat().st_size == 0:
            sys.exit("Chrome produced no screenshot")

        subprocess.run(
            ["sips", "-z", str(H), str(W), str(shot), "--out", str(OUT)],
            check=True,
            capture_output=True,
        )

    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
