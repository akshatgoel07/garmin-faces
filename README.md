# garmin-faces

Watch faces for Garmin AMOLED watches, written in Monkey C for the Connect IQ store.

First target is the Forerunner 965 (454 x 454 AMOLED). The first face is a typographic one: big fitted digits, a premium sans, nothing else.

## Layout

```
faces/      one folder per watch face, each a Connect IQ project
scripts/    build, font cutting, and sideload helpers
docs/       design sheets and decisions
```

## Setup

You need:

- Java 17 or newer
- VS Code with the Garmin Monkey C extension
- The Connect IQ SDK, installed through Garmin's SDK Manager
- A developer key, made once from VS Code (`Monkey C: Generate a Developer Key`). Keep it outside the repo. Losing it means you cannot update a published face.

Install the SDK Manager from https://developer.garmin.com/connect-iq/sdk/ and sign in with your Garmin Connect account.

## Build and test

Open a face folder in VS Code, pick a device, and run it in the simulator with `Monkey C: Run`. To test on the watch, build with `Monkey C: Build for Device`, then copy the `.prg` from `bin/` into `GARMIN/APPS/` on the watch over USB.

## Always-on rule

Garmin AMOLED watches cap an always-on face at 10% of pixels lit and redraw once a minute. Every face here ships a separate low-power layout that stays under the cap. The design sheet in `docs/design/` measures it.

## Publishing

Listing a free face on the Connect IQ store costs nothing. Charging through Garmin costs $100 a year plus 15% per sale. Upload from the developer dashboard at https://apps.garmin.com/developer/dashboard.

## Fonts

Typefaces are cut to bitmap fonts at build time. Only fonts under the SIL Open Font License go in this repo.
