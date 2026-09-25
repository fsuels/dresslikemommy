# Seasonal homepage hero — Halloween & winter (2026-09-25)

Owner request (chat, 2026-09-25): improve the homepage hero image for the current season, Halloween and winter.

## What changed (LIVE since 2026-09-25 20:38 UTC)

- `templates/index.json` → `hero_banner_main` only. The summer beach slides were replaced by two art-directed slides:
  1. **Halloween.** A midnight-plum sky with a crescent moon, and a trio of arched frames:
     - `pumpkin-ghost-family-matching-pajamas` (image 1)
     - `boo-stripe-family-matching-pajamas` (image 4)
     - `spooky-skeleton-family-matching-onesie-pajamas` (image 1)

     Slide click goes to `/collections/family-pajamas`; its grid opens with all six Halloween sets.
  2. **Winter.** An evergreen sky with snowfall, and a trio of arched frames:
     - `cable-horse-family-matching-tops` (image 4)
     - `family-matching-red-cable-knit-cardigans-elegant-heart-button-design` (image 1)
     - `family-matching-cable-knit-sweaters-heart-embroidered-unisex-pullovers` (image 1)

     Slide click goes to `/collections/family-sweaters`, which contains all three.
- Copy (all 21 storefront languages, from `snippets/hero-seasonal-copy.liquid`):
  - Eyebrow: "The Halloween & Winter Edit"
  - H1: "Spooky nights. Snowy mornings. Matching families."
  - The subheading names Halloween pajamas and family sweaters.
  - CTAs: Shop Halloween Pajamas → family-pajamas, Shop Cozy Sweaters → family-sweaters, Shop Family Matching Outfits → new-women-outfits. The third CTA keeps the exact-anchor SEO link from anchor `2026-09-24-family-matching-outfits-seo-target`.
- `sections/hero-banner.liquid` (backward compatible; every new setting defaults to the old behavior):
  - Slide settings: an optional transparent **foreground art** layer that is never cropped (`art_theme_asset`), and a per-slide **link**.
  - Section settings:
    - `eyebrow`
    - `seasonal_copy`: pre-translated copy, because Translate & Adapt keeps serving the previous season's translations after the English source changes
    - `button_style: seasonal`
    - `show_mobile_heading`
    - `text_scrim_opacity`
  - The slider now waits for all of a slide's images before fading it in.
  - Seasonal buttons override the global dark-pill rule in `assets/theme-inline-body-static-05.css`.
- New assets:
  - `assets/hero-{halloween,winter}-sky.jpg` (2400×1000, about 110 KB)
  - `-sky-mobile.jpg` (1000×1100, about 50 KB)
  - `-art-{760,1140,1520}.webp`: transparent art with a responsive srcset. A 1x desktop screen downloads the 760 or 1140 file (about 80–210 KB).
- Old hero assets (`hero-desktop.jpg`, `hero-family-boardwalk-premium*.jpg`, …) are untouched, for rollback.

## Verification (local)

- `shopify theme check`: 278 files, 0 offenses. `git diff --check` is clean. Both hero inline scripts pass `node --check`.
- Real Liquid render: `tools/render_hero_harness.js` uses liquidjs 10.20.1, the copy bundled inside the installed Shopify CLI. It renders the actual section, snippet and `index.json` into script-free copies of the live homepage for all 21 languages.
- Layout sweep (`tools/hero_layout_sweep.html`): 21 languages × 7 widths (320–1440) = 147 cases, with **0 problems** on the final build (`layout_sweep_summary.json`). Earlier iterations caught and fixed:
  - controls touching the arches on small phones
  - long translated labels running into the art at 768/1024
  - the eyebrow wrapping at 320
  - the mobile CTA card growing over the controls (German)
  - a Finnish label overflowing its pill at 320
- Screens: `screens/compare-desktop.jpg`, `screens/compare-mobile.jpg`, and individual before/after shots, including German mobile and Japanese desktop.
- Pre-existing bug fixed: Dawn's `a:empty { display: none }` hid the hero's empty overlay link, so clicking the live hero image did nothing. The overlays now use a more specific `display: block` rule, and a click on the arches or sky goes to that slide's collection.
- Independent review (a verifier that did not build the change) found 5 issues. All 5 are fixed and re-verified:
  1. Deploy blocker: the `text_scrim_opacity` range default of 64 was not on its step of 5. Shopify rejects that, and Theme Check does not test it. The step is now 1 and the default stays 64. A custom range validator passes.
  2. Arrow keys on a focused slide link dropped focus to `<body>`. Focus now follows to the new slide's link, verified in headless Chromium with real key presses.
  3. A slide link could have an empty accessible name in other configurations. It now falls back to the slide alt.
  4. A missing art file froze the carousel. Art failures are now non-fatal and the broken art hides itself; verified by pointing slide 2 at a missing file.
  5. On phones, a tall translated CTA card overlapped the next section by up to 28px (Italian at 320). The phone layout was restructured: a fixed-height image stage, with the card in normal flow beneath it. The section grows with the card, and the sweep measures a 12px gap in all 63 phone cases.
- Found in QA: when the three phone buttons stretch to the tallest label, the full pill radius turned tall buttons into circles. That clipped the first line of long labels (Italian). Phone CTAs now use a 2rem radius with vertically centered labels.
- Translate & Adapt link check (read-only): the March export has 0 translated values for hero link fields. The Sept 22 Danish run registered text keys only; links appear only as untranslated source content. Stale link translations are therefore unlikely; the release readback still checks CTA and slide-link targets on ES/DE/JA/AR.
- New slide blocks have no translated alt text, so the seasonal copy set now includes translated alts for 20 languages. English uses each slide's own detailed `image_alt`.
- Not run: `shopify theme dev`, which needs an owner Shopify CLI login (device code). A live readback happens after release.

## Release (done, owner approved in chat: "publish the hero")

- Commit `5074fd8` was pushed to `main` at 20:23 UTC. The GitHub→Shopify sync did not apply it within 12 minutes, the same stall seen in earlier releases.
- Before-state (`release/before_state.json`): theme `133290917985` is role MAIN. The live `sections/hero-banner.liquid` and `templates/index.json` were identical to the pre-release `3019324`, and the 11 new files were absent. Live copies are saved in `release/theme_before/`.
- `themeFilesUpsert` (`tools/theme_release_upsert.py`) wrote the 13 files byte-identical to `5074fd8` at 20:38 UTC, in two batches: assets, snippet and section, then `index.json`. There were 0 userErrors.
- After-state (`release/after_state.json`): all 13 live files equal `5074fd8`.
- Shopify's sync-back commit `9a09846` has 0 file changes, so nothing was reverted. Peer commit `e3d0e07` (cart delivery/returns) was not touched and is still not live.
- Public readback (`release/live_readback.json`, `tools/live_readback.py`) covered all 21 language homepages:
  - The new hero, localized copy, and CTA and slide-link targets are correct on every locale, so there are no stale link translations.
  - There are 0 Liquid errors, and all 10 hero assets return HTTP 200.
- Live browser check at desktop 1440 and mobile 375 matches the approved design. The only console error is Shopify's own `/sf_private_access_tokens` 401, which is unrelated.

## Rollback

- Revert `5074fd8` and push. If the sync stalls again, `themeFilesUpsert` the two files in `release/theme_before/` (byte-identical to `3019324`). The new assets and snippet can stay; they are unused once `index.json` is restored. The old slides use the old assets, and the new settings default to prior behavior.

## Next season

Run `tools/make_hero_art.py` (Pillow) with new product photos (theme `photos`) and palettes. It writes the sky and art files; keep the `NAME-760/1140/1520.webp` convention. Once the Christmas sweater drafts (`polar-bear-…`, `christmas-reindeer-…`) are published, they are natural winter-slide swaps.
