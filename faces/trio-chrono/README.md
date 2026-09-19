# Trio Chrono

An analogue chronograph dial: twelve numbered cells round the rim, three subdials, a green seconds disc that turns under a yellow pointer, and a date pill. Black or white dial, picked in the face settings. Built for the Forerunner 965 (454 x 454 AMOLED).

What moves:

- blue hour hand, white (or black) minute hand
- the green disc turns once a minute; the yellow pointer reads the second
- left subdial: white hand is steps against the goal, red hand is battery
- right subdial: white hand is local time on 24 hours, red hand is UTC
- bottom subdial: red hand is seconds
- the pill shows the day of the month

Always-on draws the same dial as lines only, thin hands, and the disc as an outline, then nudges it a few pixels each minute. That keeps the lit pixels near 7% of the screen, under Garmin's 10% cap for AMOLED always-on.

## Art

The static dial is baked into bitmaps by `render_dial.py`, which draws everything at four times the size and scales down. It writes the three dials, both discs, the launcher icon, and the 500 px store icon. Rerun it from the repo root after changing any number in it:

```
python3 faces/trio-chrono/render_dial.py
```

The one bitmap font is the date, cut from `assets/fonts/Outfit[wght].ttf`:

```
python3 scripts/cut_font.py --ttf "assets/fonts/Outfit[wght].ttf" --size 20 --weight 500 --chars 0123456789 --out faces/trio-chrono/resources/fonts/date
```

## Build and sideload

From the repo root, `scripts/face.sh build trio-chrono` and `scripts/face.sh run trio-chrono`. For the watch, copy `bin/trio-chrono.prg` into `GARMIN/APPS/` over USB.
