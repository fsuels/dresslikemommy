# Translation freshness and recently viewed language repairs

Root-owned files: assets/cart.js, ops/scripts/sync_shopify_translations.py, ops/scripts/poll_shopify_product_translations.py and their focused regression tests. Current user requests fixing repeated language errors and releasing through main. These changes are within that scope.

Live before-state: fresh /da browser DOM shows Swedish `Röd Panda Mamma och jag Pyjamasar — Matchande` and English `Family Matching T-Shirts - Tropical Print` inside CartDrawer-RecentlyViewedGrid. Exact Shopify global Danish title records are Danish, current and have no market overrides (products/priority_danish_before.json). The underlying problem is the shared localStorage key retaining previously viewed titles across languages. The repair keys future history by the current Shopify route root and leaves legacy storage untouched without rendering titles of unknown language. No new requests, cart quantity/checkout behavior or cached prices are introduced.

Offline script review found two stale-source hazards. The CSV synchronizer now rejects a candidate whose English source differs from the current key value. The product poller now requires fresh existing bodies before applying deterministic label-only repair; outdated bodies must be translated from current source, or remain held in deterministic-only mode.

Checks run:17recently-viewed/cart regression tests PASS;3translation-source-freshness regression tests PASS; existing full-product localization gate PASS; node --check assets/cart.js PASS; scoped git diff --check PASS; strict continuity CONTINUITY_OK. Bundled Python uses the existing user site-packages path for requests; no dependency was installed. Independent review and live main sync are separate release requirements.
