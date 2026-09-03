# Duo Bold

Hours over minutes in heavy Outfit, white on black, the date in small caps under the minutes. Built for the Forerunner 965 (454 x 454 AMOLED).

Awake it draws the bold digits and the date. Always-on it draws the same digits at hairline weight, no date, and nudges them a few pixels each minute. That keeps the draw under Garmin's 10% pixel cap for AMOLED always-on.

## Fonts

The three bitmap fonts in `resources/fonts/` are cut from `assets/fonts/Outfit[wght].ttf` with `scripts/cut_font.py`. Regenerate them from the repo root:

```
python3 scripts/cut_font.py --ttf "assets/fonts/Outfit[wght].ttf" --size 228 --weight 700 --chars 0123456789 --tracking -0.06 --out faces/duo-bold/resources/fonts/digits_bold
python3 scripts/cut_font.py --ttf "assets/fonts/Outfit[wght].ttf" --size 228 --weight 100 --chars 0123456789 --tracking -0.04 --out faces/duo-bold/resources/fonts/digits_thin
python3 scripts/cut_font.py --ttf "assets/fonts/Outfit[wght].ttf" --size 21 --weight 500 --chars "0123456789 ADEFHIMNORSTUW" --tracking 0.14 --out faces/duo-bold/resources/fonts/date
```

## Build and sideload

Open this folder in VS Code with the Monkey C extension, pick `fr965`, and run `Monkey C: Run` for the simulator. For the watch, run `Monkey C: Build for Device`, then copy `bin/duo-bold.prg` into `GARMIN/APPS/` on the watch over USB.
