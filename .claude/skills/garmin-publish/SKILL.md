---
name: garmin-publish
description: Ship a face to the Connect IQ store. Use when the user says publish, upload, submit, release, new version, or asks about the store, review, or pricing.
---

# garmin-publish

Free listings cost nothing. Selling through Garmin costs $100 a year plus 15% a sale, and India is not a supported merchant country. KiezelPay is the fallback, 27% a sale.

## Before upload

1. Bump `version` in `manifest.xml`. The store form must match it.
2. `scripts/face.sh build <face>`, run it, check wake and always-on in the simulator.
3. `scripts/face.sh export <face>` for the `.iq`.
4. `docs/store/<face>/` holds `listing.md`, `icon-500.png` (500 x 500, under 300 KB), and square screenshots (under 150 KB each). Keep `listing.md` in step with what is live.
5. Merge to `main` first. What is published should be what `main` builds.

## Upload

Dashboard: https://apps.garmin.com/developer/dashboard. The Claude Chrome extension needs the user signed in to Garmin in that Chrome and site access on `apps.garmin.com` and `sso.garmin.com`, or the user uploads by hand from the checklist in `listing.md`. Stop before the final Submit and ask.

Review takes about two business days. Garmin rejects faces that copy its own stock designs.

## After approval

Tag the commit `<face>-v<version>` and note the store URL in `docs/store/<face>/listing.md`.
