#!/usr/bin/env python3
"""Render the static art for Trio Chrono at 454 px.

Writes into resources/drawables/: the dial for the dark, light and
always-on themes, the green seconds disc (full and outline), and the
launcher icon. Also writes docs/store/trio-chrono/icon-500.png.

Run from the repo root:
  python3 faces/trio-chrono/render_dial.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "faces", "trio-chrono", "resources", "drawables")
FONT = os.path.join(ROOT, "assets", "fonts", "Outfit[wght].ttf")

W = 454          # fr965
R = W / 2
S = 4            # supersample, downscaled with Lanczos

GREEN = (5, 106, 46)
YELLOW = (245, 179, 0)
RED = (227, 58, 30)

THEMES = {
    "dark": dict(bg=(16, 16, 16), text=(242, 242, 242), tick=(138, 138, 138), line=(58, 58, 58),
                 band=(30, 30, 30), band_edge=(46, 46, 46), disc=(6, 6, 6), fill=True),
    "light": dict(bg=(232, 232, 224), text=(17, 17, 17), tick=(150, 150, 146), line=(186, 186, 180),
                  band=(243, 242, 237), band_edge=(200, 200, 194), disc=(216, 215, 207), fill=True),
    # always-on: lines and text only, so the lit pixel count stays under Garmin's 10%
    "aod": dict(bg=(0, 0, 0), text=(242, 242, 242), tick=(138, 138, 138), line=(70, 70, 70),
                band=None, band_edge=(70, 70, 70), disc=None, fill=False),
}

# subdial centres as fractions of R, and what each one is labelled with
# (text, bearing in degrees clockwise from 12, radius as a fraction of R)
SUBDIALS = [
    dict(c=(-0.31, -0.16), arc=(349, 180, "ccw"), tick_step=6, dark_every=30,
         outer=[("50", 330), ("40", 270), ("30", 210)],
         inner=[("20", 330, 0.15), ("10", 270, 0.15), ("0", 210, 0.16), ("29", 30, 0.16)]),
    dict(c=(0.31, -0.16), arc=(11, 180, "cw"), tick_step=11.25, dark_every=45,
         outer=[("12", 0), ("15", 45), ("18", 90), ("21", 135)],
         inner=[("24", 356, 0.15), ("6", 90, 0.17), ("11", 161, 0.165)]),
    dict(c=(0.0, 0.37), arc=(105, 259, "cw"), tick_step=6, dark_every=30,
         outer=[("15", 90), ("20", 126), ("30", 180), ("40", 238)],
         inner=[("45", 86, 0.18), ("50", 127, 0.166), ("60", 180, 0.172), ("10", 239, 0.155)]),
]
SUB_DISC, SUB_BAND, SUB_LABEL, SUB_ARC = 0.185, 0.275, 0.322, 0.325

_fonts = {}


def font(size, weight=400):
    key = (size, weight)
    if key not in _fonts:
        f = ImageFont.truetype(FONT, round(size * S))
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]


def pol(cx, cy, bearing, r):
    """point at r px from (cx, cy) along a clock bearing, in 454 px space"""
    a = math.radians(bearing)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def sp(p):
    return p[0] * S, p[1] * S


def line(d, p0, p1, width, color):
    d.line([sp(p0), sp(p1)], fill=color, width=round(width * S))


def circle(d, c, r, fill=None, outline=None, width=1):
    x, y = sp(c)
    d.ellipse([x - r * S, y - r * S, x + r * S, y + r * S], fill=fill, outline=outline, width=round(width * S))


def arc(d, c, r, start, end, width, color):
    """arc in PIL angles (0 = 3 o'clock, clockwise) from clock bearings"""
    x, y = sp(c)
    d.arc([x - r * S, y - r * S, x + r * S, y + r * S], start - 90, end - 90, fill=color, width=round(width * S))


def label(img, text, center, rotation, size, color, weight=500, halo=None, halo_color=None):
    """text centred on its ink box, rotated clockwise by `rotation` degrees"""
    f = font(size, weight)
    l, t, r, b = f.getbbox(text)
    if halo:
        h = round(halo * S)
        l, t, r, b = l - h, t - h, r + h, b + h
    w, hgt = r - l, b - t
    layer = Image.new("RGBA", (w, hgt), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    kw = dict(font=f, fill=color)
    if halo:
        kw.update(stroke_width=round(halo * S), stroke_fill=halo_color)
    d.text((-l, -t), text, **kw)
    layer = layer.rotate(-rotation, resample=Image.BICUBIC, expand=True)
    x, y = sp(center)
    img.alpha_composite(layer, (round(x - layer.width / 2), round(y - layer.height / 2)))


def upright(bearing):
    """rotation that keeps a radial label readable: top faces out on the upper half, in on the lower"""
    b = bearing % 360
    return b if b <= 90 or b >= 270 else b - 180


def triangle(d, tip, base_c, half_w, fill=None, outline=None, width=1):
    """isoceles triangle from base centre to tip"""
    dx, dy = tip[0] - base_c[0], tip[1] - base_c[1]
    n = math.hypot(dx, dy)
    px, py = -dy / n * half_w, dx / n * half_w
    pts = [sp(tip), sp((base_c[0] + px, base_c[1] + py)), sp((base_c[0] - px, base_c[1] - py))]
    if fill:
        d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=round(width * S), joint="curve")


def render_dial(theme):
    t = THEMES[theme]
    img = Image.new("RGBA", (W * S, W * S), t["bg"] + (255,))
    d = ImageDraw.Draw(img)
    c = (R, R)

    # ring: dividers between the twelve cells, minute ticks, inner circle
    for k in range(12):
        b = 15 + 30 * k
        line(d, pol(R, R, b, 0.61 * R), pol(R, R, b, 0.96 * R), 1.2, t["line"])
    for m in range(60):
        if m % 5:
            line(d, pol(R, R, m * 6, 0.886 * R), pol(R, R, m * 6, 0.926 * R), 1.2, t["tick"])
    circle(d, c, 0.61 * R, outline=t["line"], width=1.2)

    # cardinals: filled triangle at the rim, big numeral inside it
    for k, num in enumerate(("12", "3", "6", "9")):
        b = k * 90
        triangle(d, pol(R, R, b, 0.905 * R), pol(R, R, b, 0.945 * R), 5, fill=t["text"])
        label(img, num, pol(R, R, b, 0.80 * R), 0, 28, t["text"])
    # the other eight five-minute marks: small numeral, outline triangle inside it
    for k in range(12):
        if k % 3 == 0:
            continue
        b = k * 30
        label(img, "%02d" % (k * 5), pol(R, R, b, 0.93 * R), upright(b), 19, t["text"])
        triangle(d, pol(R, R, b, 0.86 * R), pol(R, R, b, 0.895 * R), 4.5, outline=t["text"], width=1.1)

    # yellow pointer for the seconds disc
    triangle(d, pol(R, R, 0, 0.29 * R), pol(R, R, 0, 0.51 * R), 12, fill=YELLOW)

    for sd in SUBDIALS:
        sc = (R + sd["c"][0] * R, R + sd["c"][1] * R)
        if t["fill"]:
            circle(d, sc, SUB_BAND * R, fill=t["band"])
        circle(d, sc, SUB_BAND * R, outline=t["band_edge"], width=1)
        if t["fill"]:
            circle(d, sc, SUB_DISC * R, fill=t["disc"])
        step = sd["tick_step"]
        n = round(360 / step)
        for i in range(n):
            b = i * step
            if b % sd["dark_every"] == 0:
                line(d, pol(*sc, b, 0.21 * R), pol(*sc, b, 0.27 * R), 2, t["text"])
            else:
                line(d, pol(*sc, b, 0.205 * R), pol(*sc, b, 0.24 * R), 1.1, t["tick"])
        a0, a1, way = sd["arc"]
        if way == "cw":
            arc(d, sc, SUB_ARC * R, a0, a1, 2, RED)
        else:
            arc(d, sc, SUB_ARC * R, a1, a0, 2, RED)
        for text, b in sd["outer"]:
            label(img, text, pol(*sc, b, SUB_LABEL * R), upright(b), 19, t["text"], halo=2.5, halo_color=t["bg"])
        for text, b, r in sd["inner"]:
            label(img, text, pol(*sc, b, r * R), upright(b), 19, t["text"])

    return img.resize((W, W), Image.LANCZOS)


def render_disc(outline_only):
    """the green seconds disc, numbers running anticlockwise so the disc turns clockwise"""
    D = 136
    cx = cy = D / 2
    img = Image.new("RGBA", (D * S, D * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    white = (242, 242, 242)
    if outline_only:
        circle(d, (cx, cy), 65, outline=GREEN, width=2)
    else:
        circle(d, (cx, cy), 66, fill=GREEN)
    for k in range(6):
        b = 30 + 60 * k
        line(d, pol(cx, cy, b, 27), pol(cx, cy, b, 66), 1.6, white)
    for s in range(0 if outline_only else 60):
        r0 = 54 if s % 5 == 0 else 57.5
        line(d, pol(cx, cy, s * 6, r0), pol(cx, cy, s * 6, 63), 1.2, white)
    for k in range(6):
        b = -60 * k
        label(img, str(10 * k), pol(cx, cy, b, 33), b, 22, white)
    if not outline_only:
        circle(d, (cx, cy), 27, fill=(0, 0, 0))
    return img.resize((D, D), Image.LANCZOS)


def render_icon(size):
    """dark dial centre with the green disc, cropped to a circle"""
    dial = render_dial("dark")
    disc = render_disc(False)
    dial.alpha_composite(disc, (round(R - disc.width / 2), round(R - disc.height / 2)))
    crop = 150
    icon = dial.crop((round(R - crop), round(R - crop), round(R + crop), round(R + crop))).resize((size * S, size * S), Image.LANCZOS)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, icon.width - 1, icon.height - 1], fill=255)
    icon.putalpha(mask)
    return icon.resize((size, size), Image.LANCZOS)


def snap_dark(img):
    """always-on art: turn the faint anti-alias fringe black so every lit pixel earns its place"""
    return img.convert("RGB").point(lambda v: 0 if v < 64 else v)


def lit_pixels(img):
    return sum(1 for p in img.convert("RGB").getdata() if max(p) > 0)


def main():
    os.makedirs(OUT, exist_ok=True)
    for theme in THEMES:
        img = render_dial(theme)
        if theme == "aod":
            img = snap_dark(img)
        img.convert("RGB").save(os.path.join(OUT, "dial_%s.png" % theme))
        print("dial_%s.png lit pixels %d (%.1f%%)" % (theme, lit_pixels(img), 100 * lit_pixels(img) / (W * W)))
    render_disc(False).save(os.path.join(OUT, "disc.png"))
    disc = render_disc(True)
    a = disc.split()[3].point(lambda v: 0 if v < 64 else v)
    disc.putalpha(a)
    disc.save(os.path.join(OUT, "disc_aod.png"))
    print("disc_aod.png lit pixels %d" % lit_pixels(disc))
    render_icon(65).save(os.path.join(OUT, "launcher_icon.png"))
    store = os.path.join(ROOT, "docs", "store", "trio-chrono")
    os.makedirs(store, exist_ok=True)
    render_icon(500).save(os.path.join(store, "icon-500.png"))


if __name__ == "__main__":
    main()
