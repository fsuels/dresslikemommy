# Lessons the team applies on every run (max 30 lines, newest first)

One line each: what to do, and the dated evidence. Written only by the self-improvement routine (`dlm-self-improve`) or the CEO. A lesson that stops being true is deleted, not kept.

- Theme releases: after each commit hold THEME_LOCK 3 full minutes, fetch, and confirm the next "Update from Shopify" export kept your values before releasing it (four releases in 7 minutes let a stale export revert da/fi/no/pt-BR on main, 2026-11-27).
- Write THEME_LOCK, re-read it 5 seconds later, and continue only if it still names you (two agents overwrote each other's lock, 2026-11-27).
- `sync-locales`/`sync-theme`: run the read-only listing in one call, read it, then `--apply` in a separate call; `--apply` has no per-file filter and publishes every pending file on main, other sessions' included; locale work uses `sync-locales` (2026-11-27).
- If an export reverted main, do not re-apply: restore the values with a normal work-copy commit, check the read-only listing, then publish normally (2026-11-27).
- Read the live storefront only with the built-in browser, one load every 10 s; curl-style reads got 403 "Verifying your connection" twice; never try to pass that check (2026-11-27).
- Blog/article work: filter to published articles first (121 of 313 are published) (2026-11-27).
- Register conversion or rewriting long prose is not a Sonnet job (failed 10 of 20); Opus with a pre-write pass for verb agreement, mixed buttons and doubled words went 24% -> 6% -> 3% errors (2026-11-27).
- Product gallery (media-gallery.js) changes: test the full sequence colour -> swipe -> back -> other colour before release; a partial test shipped a shrunken photo, reverted ab38ad5 -> c3c4605 (2026-11-27).
- Admin `translationsRegister` by bulk script was refused four times (cs typos, titles, sv products, menus); sentence-by-sentence writes inside a hand-translation lane went through. A refusal is final: log it for the owner, never reroute (2026-11-27).
- Before fixing a claim in a translation, compare with the current English: if English says the same, it is an English-source issue for the owner list, not a translation fix (2026-11-27).
- Hand-translated bodies or guides: the author (stronger model for the prose) reads every English text and its translation in full, never a prefix or phrase-reuse pipeline; apply `ops/sourcing/translation_style/STYLE_RULES*.md`, grep those rules over the whole batch, check the closing sentence; start the next batch only when Calidad's sample of this one is under 20% clear errors (V54 prefix pipeline; V70 31% errors, V74 31% calques; 201-250 re-read changed 51 of 51, 2026-11-27).
- Translated Google titles: never cut a product name to fit a length. After writing translations (new listing or batch) and to find cut ones, run `/usr/bin/python3 ops/scripts/check_listing_claims.py --handles <h1,h2> --all-locales --rule cut-search-title`; do not crawl pages or pull translatableResources to find them (244 cut titles fixed by hand, one query about 60k characters, 2026-11-27).
- Translation batch or theme change that alters non-English text: apply or build for cs plus ONE other affected language first, read that real output (live or Admin; theme logic: run it on all active products it touches), have it checked (Calidad for batches over 20 values), and only then do the other languages (V19 defects stuck live in 11 languages after the repair was denied; V26 cart labels cut in cs after "renders as before"; 2026-11-26).
- Changed a `templates/*.json`? `sync-theme` "0 differ" skips it: before logging it live run `/usr/bin/python3 ops/scripts/check_live_templates.py --tree <work copy> templates/<file>.json`; DIFFERS = not live: log it so, never route around a denied upsert (guide captions never went live and left main, home grid stayed old, 2026-11-26).
- New draft prices: the autosource quick price runs low (CNY 3 domestic, 7.11 FX). Before review run `/usr/bin/python3 ops/scripts/price_floor_check.py --freight-cny <today> --fx <today> --item child=<cny>:<price> --item adult=<cny>:<price>` with the same-day quote; every item OK (red-heart repriced twice, 2026-11-26).
- Link the hero photo to every variant and a photo to every colour BEFORE asking Calidad for a review (red-heart HOLD, 2026-11-26).
- Read three translated product pages for corrupt or cut text before review (red-heart HOLD, 2026-11-26).
- Run `ceo_worktree.py finish --name <n>` right after the live readback; leftovers filled the disk (2026-11-25).
- When a relay is due, keep working on small units until the successor exists; never end with nothing running (owner, 2026-11-26).
- A "checked, all fine" run is not work: pick an item that changes what a shopper or Google sees (owner, 2026-11-25).
