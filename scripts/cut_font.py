#!/usr/bin/env python3
"""Cut a TTF into a Garmin bitmap font: a BMFont text .fnt plus a PNG atlas.

Example:
  python3 scripts/cut_font.py --ttf "assets/fonts/Outfit[wght].ttf" \
      --size 228 --weight 700 --chars 0123456789 --tracking -0.06 \
      --out faces/duo-bold/resources/fonts/digits_bold
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

GUTTER = 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ttf", required=True)
    ap.add_argument("--size", type=int, required=True)
    ap.add_argument("--weight", type=float, default=None, help="wght axis value for variable fonts")
    ap.add_argument("--chars", required=True)
    ap.add_argument("--tracking", type=float, default=0.0, help="em fraction added to every xadvance")
    ap.add_argument("--out", required=True, help="path stem; writes stem.fnt and stem.png")
    a = ap.parse_args()

    font = ImageFont.truetype(a.ttf, a.size)
    if a.weight is not None:
        font.set_variation_by_axes([a.weight])

    chars = list(dict.fromkeys(a.chars))
    glyphs = []
    # Pillow's getbbox folds side bearings into the box, so measure the ink
    # from a rendered mask to get true offsets
    pad = a.size
    for ch in chars:
        scratch = Image.new("L", (a.size * 3, a.size * 3), 0)
        ImageDraw.Draw(scratch).text((pad, pad), ch, font=font, fill=255)
        ink = scratch.getbbox()
        if ink is None:
            left, top, right, bottom = 0, 0, 0, 0
        else:
            left, top, right, bottom = (v - pad for v in ink)
        glyphs.append((ch, left, top, right, bottom, font.getlength(ch)))

    # the line box hugs the ink of the chars in use, so Garmin's vertical
    # centering lands on the visual middle of the digits, not the em box
    inked = [g for g in glyphs if g[4] > g[2]]
    ink_top = min(g[2] for g in inked)
    ink_bottom = max(g[4] for g in inked)
    ascent, _ = font.getmetrics()
    line_height = ink_bottom - ink_top
    base = ascent - ink_top

    atlas_w = sum(max(g[3] - g[1], 1) for g in glyphs) + GUTTER * (len(glyphs) + 1)
    atlas_h = line_height + GUTTER * 2
    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)

    tracking_px = round(a.tracking * a.size)
    lines = []
    x = GUTTER
    for ch, left, top, right, bottom, advance in glyphs:
        blank = bottom <= top
        w = 1 if blank else right - left
        h = 1 if blank else bottom - top
        yoffset = 0 if blank else top - ink_top
        y = GUTTER + yoffset
        if not blank:
            draw.text((x - left, y - top), ch, font=font, fill=(255, 255, 255, 255))
        lines.append(
            f"char id={ord(ch)} x={x} y={y} width={w} height={h} "
            f"xoffset={left} yoffset={yoffset} xadvance={round(advance) + tracking_px} page=0 chnl=15"
        )
        x += w + GUTTER

    stem = a.out
    os.makedirs(os.path.dirname(stem) or ".", exist_ok=True)
    png_name = os.path.basename(stem) + ".png"
    atlas.save(stem + ".png")

    face = os.path.splitext(os.path.basename(a.ttf))[0]
    fnt = [
        f'info face="{face}" size={a.size} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={GUTTER},{GUTTER} outline=0',
        f"common lineHeight={line_height} base={base} scaleW={atlas_w} scaleH={atlas_h} pages=1 packed=0 alphaChnl=0 redChnl=4 greenChnl=4 blueChnl=4",
        f'page id=0 file="{png_name}"',
        f"chars count={len(lines)}",
        *lines,
    ]
    with open(stem + ".fnt", "w") as f:
        f.write("\n".join(fnt) + "\n")
    print(f"{stem}.png {atlas_w}x{atlas_h}, {len(lines)} glyphs, lineHeight {line_height}, base {base}")


if __name__ == "__main__":
    main()
