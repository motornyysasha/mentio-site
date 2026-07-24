#!/usr/bin/env python3
"""
Обложки для соцсетей Mentio.

Самодостаточный: шрифты берёт из assets/fonts (woff2 → ttf на лету),
знак вырезает из ~/Desktop/mentio-avatar.png по альфа-маске, поэтому
градиент и скругления всегда пиксель-в-пиксель совпадают с логотипом.

    python3 tools/make_social_cover.py x          # X/Twitter 1500x500
    python3 tools/make_social_cover.py linkedin   # LinkedIn 1128x191
    python3 tools/make_social_cover.py all

Зависимости: pillow, fonttools, brotli  (pip3 install pillow fonttools brotli)
Результат кладётся в ~/Desktop/mentio-social/
"""
import os
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_SRC = os.path.join(REPO, "assets", "fonts")
AVATAR = os.path.expanduser("~/Desktop/mentio-avatar.png")
OUT_DIR = os.path.expanduser("~/Desktop/mentio-social")

BG = (11, 11, 16)          # --bg      #0B0B10
RED = (229, 56, 59)        # --red     #E5383B
ORANGE = (255, 107, 53)    # --orange  #FF6B35
TEXT = (237, 237, 242)     # --text
MUTED = (160, 160, 176)    # --muted

# name -> (ширина, высота, где заканчивается безопасная зона по вертикали)
# У X аватар перекрывает низ слева, у LinkedIn — левый край, поэтому
# контент прижимается кверху и не заходит в нижнюю треть.
PRESETS = {
    "x": dict(size=(1500, 500), scale=3, margin=118, top=88,
              mark_h=96, word=86, kick=21, head=46, sub=27, url=32,
              head_text="Get recommended by AI — not just ranked.",
              sub_text="ChatGPT   ·   Perplexity   ·   Gemini   ·   Google AI Overviews   ·   Copilot"),
    "linkedin": dict(size=(1128, 191), scale=4, margin=300, top=44,
                     mark_h=52, word=46, kick=13, head=25, sub=0, url=18,
                     head_text="Get recommended by AI — not just ranked.",
                     sub_text=""),
}


def build_fonts(tmp):
    """woff2 из репозитория -> статические ttf нужных начертаний."""
    from fontTools import ttLib
    from fontTools.varLib import instancer

    jobs = [("space-grotesk-latin-wght-normal", 700, "SpaceGrotesk-Bold.ttf"),
            ("space-grotesk-latin-wght-normal", 500, "SpaceGrotesk-Medium.ttf"),
            ("inter-latin-wght-normal", 400, "Inter-Regular.ttf"),
            ("inter-latin-wght-normal", 600, "Inter-SemiBold.ttf")]
    for src, weight, out in jobs:
        f = ttLib.TTFont(os.path.join(FONTS_SRC, src + ".woff2"))
        f.flavor = None
        static = instancer.instantiateVariableFont(f, {"wght": weight})
        static.save(os.path.join(tmp, out))


def cut_mark(path):
    """Знак без фона: альфа считается как отклонение от цвета фона аватара."""
    im = Image.open(path).convert("RGB")
    solid = Image.new("RGB", im.size, im.getpixel((5, 5)))
    diff = ImageChops.difference(im, solid).convert("L")
    alpha = diff.point(lambda v: 0 if v < 14 else min(255, int((v - 14) * 255 / 22)))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba.crop(alpha.getbbox())


def radial_glow(size, center, radius, color, strength):
    w, h = size
    small = (max(2, w // 12), max(2, h // 12))
    g = Image.new("L", small, 0)
    d = ImageDraw.Draw(g)
    cx, cy = center[0] * small[0] / w, center[1] * small[1] / h
    r = radius * small[0] / w
    steps = 48
    for i in range(steps, 0, -1):
        t = i / steps
        rr = r * t
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=int(strength * (1 - t) ** 2))
    g = g.resize(size, Image.LANCZOS).filter(
        ImageFilter.GaussianBlur(radius=size[0] / 90))
    layer = Image.new("RGBA", size, color + (0,))
    layer.putalpha(g)
    return layer


def render(preset_name, tmp):
    p = PRESETS[preset_name]
    W, H = p["size"]
    S = p["scale"]
    cw, ch = W * S, H * S

    def font(name, px):
        return ImageFont.truetype(os.path.join(tmp, name), px)

    img = Image.new("RGB", (cw, ch), BG).convert("RGBA")
    img = Image.alpha_composite(
        img, radial_glow((cw, ch), (cw * 0.80, ch * 0.10), cw * 0.62, ORANGE, 62))
    img = Image.alpha_composite(
        img, radial_glow((cw, ch), (cw * 0.52, ch * 0.95), cw * 0.50, RED, 40))
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)

    # градиентная линия по нижнему краю
    bar = max(2, int(5 * S * H / 500))
    for x in range(cw):
        t = x / cw
        d.line([(x, ch - bar), (x, ch)],
               fill=tuple(int(RED[i] + (ORANGE[i] - RED[i]) * t) for i in range(3)))

    mark = cut_mark(AVATAR)
    mark_h = p["mark_h"] * S
    mark = mark.resize((int(mark.width * mark_h / mark.height), mark_h), Image.LANCZOS)

    x0, y0 = p["margin"] * S, p["top"] * S
    img.paste(mark, (x0, y0), mark)

    f_word = font("SpaceGrotesk-Bold.ttf", p["word"] * S)
    bb = d.textbbox((0, 0), "Mentio", font=f_word)
    d.text((x0 + mark.width + 30 * S,
            y0 + (mark_h - (bb[3] - bb[1])) // 2 - bb[1]),
           "Mentio", font=f_word, fill=TEXT)

    f_kick = font("Inter-SemiBold.ttf", p["kick"] * S)
    d.text((x0 + 3 * S, y0 - int(2.1 * p["kick"]) * S),
           "G E N E R A T I V E   E N G I N E   O P T I M I Z A T I O N",
           font=f_kick, fill=ORANGE)

    f_head = font("SpaceGrotesk-Medium.ttf", p["head"] * S)
    d.text((x0 + 3 * S, y0 + mark_h + 40 * S * H // 500 + (0 if p["sub"] else -6 * S)),
           p["head_text"], font=f_head, fill=TEXT)

    if p["sub"]:
        f_sub = font("Inter-Regular.ttf", p["sub"] * S)
        d.text((x0 + 3 * S, y0 + mark_h + 108 * S), p["sub_text"],
               font=f_sub, fill=MUTED)

    f_url = font("SpaceGrotesk-Bold.ttf", p["url"] * S)
    ub = d.textbbox((0, 0), "mentio.agency", font=f_url)
    d.text((cw - (ub[2] - ub[0]) - p["margin"] * S // 2, y0 - int(1.9 * p["url"]) * S),
           "mentio.agency", font=f_url, fill=TEXT)

    out = img.resize((W, H), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"mentio-{preset_name}-cover.png")
    out.save(path, optimize=True)
    print(f"{preset_name:9s} {W}x{H}  ->  {path}  ({os.path.getsize(path)} байт)")


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = list(PRESETS) if which == "all" else [which]
    for n in names:
        if n not in PRESETS:
            sys.exit(f"неизвестный пресет: {n}. Доступны: {', '.join(PRESETS)}, all")

    with tempfile.TemporaryDirectory() as tmp:
        build_fonts(tmp)
        for n in names:
            render(n, tmp)

    # аватар 400x400 — соцсети обрезают его в круг
    av = Image.open(AVATAR).convert("RGB").resize((400, 400), Image.LANCZOS)
    ap = os.path.join(OUT_DIR, "mentio-avatar-400.png")
    av.save(ap, optimize=True)
    print(f"avatar    400x400  ->  {ap}  ({os.path.getsize(ap)} байт)")


if __name__ == "__main__":
    main()
