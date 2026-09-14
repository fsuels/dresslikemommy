Confidence: H for local source and regression results; current rendered V7/V8 behavior remains unverified in this lane.

The existing [MAIN capture](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/root_landing_qa/ROOT_RENDERED.json:10) records four English buying labels on the Romanian Together Heart PDP. Its theme binding is MAIN 133290917985. This is prior rendered evidence, not a new browser observation.

V7 already contains all five Romanian choose-role, choose-options, choose-member, add-piece and ready labels in [ruler-sync.js](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/assets/product-desktop-ux-20260513-ruler-sync.js:646). The complete asset executes correctly in jsdom: actual `getLocaleRoot`/`uiLabel` return these labels for both `ro` and `ro-RO`, and retain EN/ES/JA/AR holdouts. [main-product.liquid](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/sections/main-product.liquid:933) loads it. No JavaScript repair is indicated by these checks.

V7 [ro.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/candidate/locales/ro.json:283) already has qualified Romanian returns; captured [MAIN ro.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/source/main/locales/ro.json:282) retains older English returns. V8 translates exactly seven remaining security/privacy/policy-link leaves in [proposed ro.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/proposed/locales/ro.json:281). Exact source/translation pairs preserve the existing payment claims. Every other JSON leaf, deadline, eligibility condition, exclusion, URL and placeholder is unchanged from V7. Tests also preserve its 30-day delivery-based return period, 7-day damage process, and return-shipping responsibility.

The separate `ro-RO.json` proposal changes footer headings only: its purchase-confidence JSON still includes English security and returns copy. Romanian runtime fallback does not establish server-side locale repair.

VERIFIED: 21/21 tests pass in [romanian-guidance.test.mjs](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/romanian-guidance.test.mjs). Checks bind five MAIN text files to captured MD5s, preserve 44 V7 runtime/data assets plus four PDP templates, and constrain the proposal to six locale overlays plus the footer. MAIN runtime is metadata-only `OnlineStoreThemeFileBodyUrl`; its contents were neither read nor downloaded. A differing checksum alone does not diagnose its English-label behavior.

Executed from `/Users/fsuels/Projects/dresslikemommy`:

```text
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/romanian-guidance.test.mjs
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/romanian-guidance.test.mjs
```

Both commands passed. No network, browser, API, canonical or external writes occurred; only this report and the assigned test were written. Public HTTP 429 gate remains active. Shopify Liquid rendering, current storefront appearance, and conversion impact were not tested.

Next action: parent combined V8 checks and independent review, because they assess the complete seven-file proposal while preserving uploaded V7. Continuation: “Include Romanian regressions in the offline V8 seven-file review.”
