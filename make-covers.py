#!/usr/bin/env python3
"""Render the social cover images in the orizuru world.

Only the platforms that actually take a cover are here. Crunchbase, Clutch and
Trustpilot show a logo and no banner — assets/logo-transparent.png covers those.

Every layout keeps its content clear of the platform's own overlay: X and both
LinkedIn covers get an avatar or logo dropped onto their lower left, and the
cover is cropped differently on mobile, so nothing that must be read lives
there. The reserved boxes are stated per preset below.

  python3 make-covers.py                 # all
  python3 make-covers.py x github        # just these

Output: ~/Desktop/mentio-social/
"""
import pathlib
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent
OUT_DIR = pathlib.Path.home() / "Desktop" / "mentio-social"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ROOT / "assets" / "fonts"

MARK = (
    '<svg class="mk" xmlns="http://www.w3.org/2000/svg" viewBox="37 34 26 31">'
    '<defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#E5383B"/><stop offset="1" stop-color="#FF6B35"/>'
    "</linearGradient></defs>"
    '<rect x="38" y="35.5" width="9.6" height="21.6" rx="4.8" fill="url(#mg)"/>'
    '<rect x="52.7" y="40" width="9" height="17.1" rx="4.5" fill="url(#mg)"/>'
    '<rect x="38" y="60.4" width="24" height="3.4" rx="1.7" fill="url(#mg)"/>'
    "</svg>"
)

# the hero's own fold sequence: creased sheet -> fold -> crane.
# tall version for upright panels, wide version for the thin LinkedIn strip.
_CREASE = (
    '<g stroke="rgba(255,245,235,.55)" fill="none" stroke-width="1.4">'
    '<rect x="14" y="14" width="92" height="92"/>'
    '<path d="M14 14 L106 106 M106 14 L14 106" stroke-dasharray="5 4"/>'
    '<path d="M60 14 V106 M14 60 H106" stroke-dasharray="1 3 6 3"/></g>'
)
_CRANE = (
    '<g stroke="#FFF5EB" fill="none" stroke-width="1.8" '
    'stroke-linejoin="round" stroke-linecap="round">'
    '<path d="M196 88 L172 64 L196 30 L220 64 Z"/>'
    '<path d="M172 64 L150 46 L158 40 L172 52"/>'
    '<path d="M156 44 L150 36 L160 39"/>'
    '<path d="M220 64 L244 84 L236 60"/>'
    '<path d="M196 30 L188 8 L212 22 Z" stroke-dasharray="5 4"/>'
    '<path d="M196 88 L196 64" stroke-dasharray="1 3 6 3"/></g>'
)
FOLD_TALL = (
    '<svg class="fold" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 268">'
    f'<g transform="translate(40,4)">{_CREASE}</g>'
    '<g stroke="rgba(255,245,235,.75)" fill="none" stroke-width="1.6">'
    '<path d="M100 124 V150 M100 150 l-3.5 -6 M100 150 l3.5 -6"/></g>'
    f'<g transform="translate(-97,164)">{_CRANE}</g></svg>'
)
FOLD_WIDE = (
    '<svg class="fold" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 288 120">'
    f"{_CREASE}"
    '<g stroke="rgba(255,245,235,.75)" fill="none" stroke-width="1.4">'
    '<path d="M120 60 H146 M146 60 l-6 -3.5 M146 60 l-6 3.5"/></g>'
    f"{_CRANE}</svg>"
)

RAIL = "".join(
    f"<span>{n}</span>" + ("<i></i>" if n != "Bing Copilot" else "")
    for n in ("ChatGPT", "Perplexity", "Gemini", "Google AI Overviews", "Bing Copilot")
)

BASE = """
@font-face{font-family:'Source Serif 4';font-weight:200 900;src:url(FONTS/source-serif-4-latin-wght-normal.woff2) format('woff2-variations')}
@font-face{font-family:'Source Sans 3';font-weight:200 900;src:url(FONTS/source-sans-3-latin-wght-normal.woff2) format('woff2-variations')}
:root{--paper:#F0EAE0;--paper2:#F7F2E9;--ink:#1C1713;--ink-soft:#4A423A;--ink-faint:#6E655A;
--verm:#C73E2A;--gold:#C9A227;--crease:rgba(28,23,19,.35);
--serif:'Source Serif 4',Georgia,serif;--sans:'Source Sans 3',Helvetica,Arial,sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--paper);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .035 0'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)'/%3E%3C/svg%3E");
font-family:var(--sans);color:var(--ink-soft);-webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.edge{position:absolute;left:0;right:0;top:0;background:var(--verm)}
.brand{display:flex;align-items:center;gap:14px}
.chip{border-radius:5px;border:1px solid var(--crease);background:#fff;display:flex;align-items:center;justify-content:center}
.chip .mk{width:64%;height:64%;display:block}
.word{font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
h1{font-family:var(--serif);font-weight:600;color:var(--ink);line-height:1.12;letter-spacing:-.015em}
h1 .hot{color:var(--verm);-webkit-box-decoration-break:clone;box-decoration-break:clone;
background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 12' preserveAspectRatio='none'%3E%3Cpath d='M3 8 Q 40 4 80 7 T 197 5' stroke='%23C73E2A' stroke-width='4.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E") no-repeat left 100%;
background-size:100% .13em;padding-bottom:.08em}
.panel{background:var(--verm);position:absolute;display:flex;align-items:center;justify-content:center;overflow:hidden}
.panel .fold{display:block}
.price{display:inline-flex;align-items:center;gap:9px;background:var(--verm);color:#fff;font-weight:700;
letter-spacing:.09em;text-transform:uppercase;padding:11px 17px;border-radius:3px;white-space:nowrap}
.price .dot{width:8px;height:8px;border-radius:50%;background:var(--gold)}
.rail{display:flex;align-items:center;gap:16px;color:var(--ink-faint);letter-spacing:.18em;
text-transform:uppercase;font-weight:600;white-space:nowrap}
.rail i{width:4px;height:4px;border-radius:50%;background:var(--gold);display:inline-block}
.url{font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--ink)}
"""

# size, extra css, body. "reserved" documents the platform overlay we design around.
PRESETS = {
    # avatar circle lands bottom-left, roughly 240x240 from the left edge
    "x": dict(
        file="x-header-1500x500.png",
        size=(1500, 500),
        reserved="avatar bottom-left ~340x260",
        css="""
.edge{height:6px}
.panel{right:0;top:0;bottom:0;width:400px}
.panel .fold{width:62%}
.brand{position:absolute;left:96px;top:52px}
.chip{width:48px;height:48px}.word{font-size:27px}
.mid{position:absolute;left:300px;top:132px;right:440px}
h1{font-size:52px}
.rail{margin-top:26px;font-size:13px}
.price{position:absolute;left:300px;top:372px;font-size:15px}
.url{position:absolute;right:440px;top:382px;font-size:15px}
""",
        body=f"""
<div class="edge"></div>
<div class="brand"><span class="chip">{MARK}</span><span class="word">Mentio</span></div>
<div class="mid">
  <h1>Your customers are asking AI.<br><span class="hot">Is it answering with you?</span></h1>
  <div class="rail">{RAIL}</div>
</div>
<span class="price"><span class="dot"></span>GEO audit €99</span>
<span class="url">mentio.agency</span>
<div class="panel">{FOLD_TALL}</div>
""",
    ),
    # company logo tile overlaps the lower left, and the strip is only 191px tall
    "linkedin": dict(
        file="linkedin-company-1128x191.png",
        size=(1128, 191),
        reserved="logo tile lower-left ~250x191",
        css="""
.edge{height:4px}
.panel{right:0;top:0;bottom:0;width:236px}
.panel .fold{width:88%}
.mid{position:absolute;left:286px;top:50px}
h1{font-size:30px;line-height:1}
.rail{margin-top:15px;font-size:11px;gap:13px}
.url{position:absolute;right:268px;top:54px;font-size:13px}
""",
        body=f"""
<div class="edge"></div>
<div class="mid">
  <h1>Get cited by AI, <span class="hot">not just ranked.</span></h1>
  <div class="rail">{RAIL}</div>
</div>
<span class="url">mentio.agency</span>
<div class="panel">{FOLD_WIDE}</div>
""",
    ),
    # profile photo lands lower-left; mobile crops hard to the centre
    "linkedin-personal": dict(
        file="linkedin-personal-1584x396.png",
        size=(1584, 396),
        reserved="profile photo lower-left ~420x220, mobile crops to centre",
        css="""
.edge{height:5px}
.panel{right:0;top:0;bottom:0;width:360px}
.panel .fold{width:60%}
.brand{position:absolute;left:390px;top:56px}
.chip{width:42px;height:42px}.word{font-size:23px}
.mid{position:absolute;left:390px;top:136px;right:400px}
h1{font-size:40px}
.rail{margin-top:22px;font-size:12px}
.price{position:absolute;left:390px;top:296px;font-size:14px}
""",
        body=f"""
<div class="edge"></div>
<div class="brand"><span class="chip">{MARK}</span><span class="word">Mentio</span></div>
<div class="mid">
  <h1>Your customers are asking AI. <span class="hot">Is it answering with you?</span></h1>
  <div class="rail">{RAIL}</div>
</div>
<span class="price"><span class="dot"></span>GEO audit €99</span>
<div class="panel">{FOLD_TALL}</div>
""",
    ),
    # no overlay: GitHub renders the whole card when the repo is shared
    "github": dict(
        file="github-social-1280x640.png",
        size=(1280, 640),
        reserved="none",
        css="""
.edge{height:6px}
.panel{right:0;top:0;bottom:0;width:440px}
.panel .fold{width:70%}
.brand{position:absolute;left:80px;top:70px}
.chip{width:54px;height:54px}.word{font-size:30px}
.mid{position:absolute;left:80px;top:206px;right:452px}
h1{font-size:47px}
.rail{margin-top:28px;font-size:13px;gap:14px}
.price{position:absolute;left:80px;bottom:74px;font-size:15px}
.url{position:absolute;left:290px;bottom:88px;font-size:15px}
""",
        body=f"""
<div class="edge"></div>
<div class="brand"><span class="chip">{MARK}</span><span class="word">Mentio</span></div>
<div class="mid">
  <h1>Your customers are asking AI.<br><span class="hot">Is it answering with you?</span></h1>
  <div class="rail">{RAIL}</div>
</div>
<span class="price"><span class="dot"></span>GEO audit €99</span>
<span class="url">mentio.agency</span>
<div class="panel">{FOLD_TALL}</div>
""",
    ),
}


def render(name, tmp):
    p = PRESETS[name]
    w, h = p["size"]
    html = (
        "<!doctype html><meta charset='utf-8'><style>"
        + BASE.replace("FONTS", FONTS.as_uri())
        + f"html,body{{width:{w}px;height:{h}px}}"
        + p["css"]
        + "</style>"
        + p["body"]
    )
    work = pathlib.Path(tmp) / f"{name}.html"
    work.write_text(html, encoding="utf-8")
    shot = pathlib.Path(tmp) / f"{name}.png"

    # Chrome 151 never exits on the legacy --headless; poll for the file instead
    proc = subprocess.Popen(
        [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
            "--force-device-scale-factor=2", "--allow-file-access-from-files",
            f"--user-data-dir={tmp}/profile", f"--window-size={w},{h}",
            f"--screenshot={shot}", work.as_uri(),
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(60):
        if shot.exists() and shot.stat().st_size > 0:
            break
        time.sleep(1)
    proc.terminate()
    if not shot.exists() or shot.stat().st_size == 0:
        sys.exit(f"Chrome produced no screenshot for {name}")

    out = OUT_DIR / p["file"]
    subprocess.run(["sips", "-z", str(h), str(w), str(shot), "--out", str(out)],
                   check=True, capture_output=True)
    print(f"  {name:18} {w}x{h}  {out.name}  ({out.stat().st_size // 1024} KB)")


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    wanted = sys.argv[1:] or list(PRESETS)
    unknown = [x for x in wanted if x not in PRESETS]
    if unknown:
        sys.exit(f"Unknown preset(s): {', '.join(unknown)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for name in wanted:
            render(name, tmp)
    print(f"\n-> {OUT_DIR}")


if __name__ == "__main__":
    main()
