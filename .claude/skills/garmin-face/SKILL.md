---
name: garmin-face
description: Build, run, and check a Connect IQ watch face in this repo. Use when adding a face, changing one, cutting fonts, running the simulator, checking always-on, or exporting the store package.
---

# garmin-face

One face per folder under `faces/`. One face per store listing; Garmin allows no bundles. Variants ship as settings inside one face.

## Commands

All from the repo root. Device defaults to `fr965`.

```
scripts/face.sh build <face>      compile to faces/<face>/bin/<face>.prg
scripts/face.sh run <face>        start the simulator and load the face
scripts/face.sh shot <face>       screenshot the simulator window
scripts/face.sh export <face>     release .iq for the store
```

The SDK lives under `~/Library/Application Support/Garmin/ConnectIQ/`, the active one named in `current-sdk.cfg`. The signing key is `~/.garmin/developer_key.der`. Never copy it into the repo.

## Simulator

Menus you drive with `osascript` against process `simulator`:

- Settings > Display Mode > High Power / Always-On switches wake and always-on. This is the low power test.
- Settings > Time Display picks 12 or 24 hour.
- File > View Watchface Diagnostics shows pixel use.

Toggle a menu item:

```
osascript -e 'tell application "System Events" to tell process "simulator" to click menu item "Always-On" of menu 1 of menu item "Display Mode" of menu "Settings" of menu bar 1'
```

`screencapture` needs the simulator in front, or you capture whatever is on top. `scripts/face.sh shot` handles that. There is no `timeout` on macOS; background `monkeydo` and kill it.

## Device limits

fr965: 454 x 454 AMOLED, watch face memory 131072 bytes, launcher icon 65 px, API level 5.2. Read others from `Devices/<id>/compiler.json`.

Always-on on AMOLED: at most 10% of pixels lit, one redraw a minute, and the simulator rejects a frame that breaks it. Shift the drawing a few pixels each minute for burn-in.

## Fonts

Bitmap fonts come from `scripts/cut_font.py`, which cuts a TTF into BMFont `.fnt` plus a PNG atlas. Only fonts under the SIL Open Font License go in `assets/fonts/`. Each face README lists its exact cut commands; rerun them after changing size, weight, chars, or tracking. Filter every font to the characters it draws, memory is tight.

## New face

Copy `faces/duo-bold`, then:

1. New UUID in `manifest.xml` (`uuidgen | tr -d - | tr A-F a-f`), new `name`, `entry`, and class names.
2. Cut fonts, update `resources/fonts/fonts.xml`.
3. Launcher icon at the device's size.
4. `README.md` in the face folder, voice per repo `CLAUDE.md`.
5. Build, run, check both display modes, then `docs/store/<face>/` with listing copy, 500 px icon, and square screenshots.
