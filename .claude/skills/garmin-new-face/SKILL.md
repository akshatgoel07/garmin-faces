---
name: garmin-new-face
description: Take a new Garmin watch face from idea to store-ready, end to end. Use when the user says new face, another watch face, design a face, or gives a face idea. Covers design options, the user's pick, scaffold, fonts, build, simulator checks in both display modes, store assets, and the PR.
---

# garmin-new-face

Read `garmin-face` for commands and limits, `garmin-publish` for the store step. This skill is the order of work. Do not skip a step; say `skip: <reason>` if one does not apply.

## 1. Brief

Get from the user or infer: the device (default fr965), what the face shows, the feel. Keep the element list short. Every extra readout costs memory and always-on pixels.

## 2. Design sheet

Copy `docs/design/fitted-design-sheet.html` to `docs/design/<face>-design-sheet.html` and replace the variants. Three to five, at the device's real pixel size, live time, wake and always-on states, typeface and accent switches, and the canvas that measures always-on pixel load. Publish it as an artifact, take one screenshot look, fix what it shows, publish again.

Present the variants in a table with tradeoffs and one recommendation. Ask the user to pick variant, typeface, accent. This is the one question in the flow that is theirs.

## 3. Scaffold

Copy `faces/duo-bold` to `faces/<face>`. New UUID, name, entry, class names. Write the layout as constants scaled from the design sheet's base coordinates. Cut fonts with `scripts/cut_font.py`, filtered to the exact characters drawn. Launcher icon at the device size.

Delegate the code to a subagent with the layout numbers and the font list, then review the diff yourself.

## 4. Build and test

```
scripts/face.sh build <face>
scripts/face.sh run <face>
```

In the simulator check, and screenshot each with `scripts/face.sh shot`:

- wake in 12 hour and 24 hour
- always-on, via Settings > Display Mode > Always-On, and confirm the simulator draws the low power layout rather than falling back
- memory in the status bar stays under the device's watch face limit

Fix, rebuild, recheck. Not done until both display modes render as designed.

## 5. Store assets

`docs/store/<face>/`: `listing.md` from the Duo Bold one, `icon-500.png`, square screenshots of wake and always-on. Export the `.iq` with `scripts/face.sh export <face>`.

## 6. Ship

Branch, commits in the repo voice, PR with the simulator evidence and the always-on pixel figure. Then hand to `garmin-publish`. The user uploads or approves the upload; the final Submit is theirs.

## Reply

What was built, the pick that drove it, screenshots, memory and pixel numbers, the PR link, what is left.
