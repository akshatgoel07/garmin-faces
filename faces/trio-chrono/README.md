# Trio Chrono

An analogue chronograph dial: twenty-four rim divisions with twelve numbered markers, three subdials, a green seconds disc that turns under a yellow pointer, and a date pill. Black or white dial, picked in the face settings. Built for the Forerunner 965 (454 x 454 AMOLED).

What moves:

- blue hour hand, white (or black) minute hand
- the green disc turns once a minute; the yellow pointer reads the second
- left subdial: white hand is steps against the goal, red hand is battery
- right subdial: white hand is local time on 24 hours, red hand is UTC
- bottom subdial: red hand is seconds
- the pill shows the day of the month

Always-on draws the dial as lines, thin hands, and the disc as an outline, then nudges it a few pixels each minute. The disc covers the subdial labels beneath it so their text does not overlap. The complete frame must stay under Garmin's 10% lit-pixel cap; the design sheet estimates the count at 454 px.

## Art

The static dial is baked into bitmaps by `render_dial.py`, which draws everything at four times the size and scales down. It writes the three dials, both discs, the launcher icon, and the 500 px store icon. Rerun it from the repo root after changing any number in it:

```
python3 faces/trio-chrono/render_dial.py
```

The dial uses Futura Medium, the font named by the reference author. The renderer reads the installed macOS font at `/System/Library/Fonts/Supplemental/Futura.ttc`; it does not bundle the font. On other systems, set `TRIO_FONT` to an installed Futura Medium file. The checked-in bitmaps build on any platform without the font.

The renderer also writes `date_numbers.png`: all 31 dates at 30 degrees, in dark and light ink. Each cell is 52 × 44 px, arranged in eight columns. The watch draws one cell over the matching surround baked into the dial. This keeps the date's type, angle and centring the same in the design sheet and simulator.

The layout measurements and comparison are in [the visual review](../../docs/design/trio-chrono-review.md).

## Build and sideload

From the repo root, `scripts/face.sh build trio-chrono` and `scripts/face.sh run trio-chrono`. For the watch, copy `bin/trio-chrono.prg` into `GARMIN/APPS/` over USB.
