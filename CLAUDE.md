# garmin-faces

Connect IQ watch faces in Monkey C. First target is the Forerunner 965. First face is `faces/duo-bold`, submitted to the store as 0.1.0 on 2026-09-12.

All prose in this repo (README, docs, commit messages, PRs) follows the voice guide:

@~/Development/skills/voice.md

## Rules

- One face per folder under `faces/`. One face per store listing. Variants are settings inside a face, never a second face in the same app.
- Never commit a developer key, `bin/`, or `.prg` files.
- Fonts are cut by `scripts/cut_font.py`. Only SIL OFL fonts go in `assets/fonts/`.
- Build, run, and export through `scripts/face.sh`. Check both display modes in the simulator before any release.
- Store assets and listing copy live in `docs/store/<face>/`.

## Skills

- `garmin-new-face` to take a new face from idea to store-ready. Start here for any new face.
- `garmin-face` for building, simulator driving, fonts, device limits, and scaffolding a new face.
- `garmin-publish` for the store checklist and pricing facts.

## Design

`docs/design/fitted-design-sheet.html` is the design sheet the first face came from. Open it in a browser.
