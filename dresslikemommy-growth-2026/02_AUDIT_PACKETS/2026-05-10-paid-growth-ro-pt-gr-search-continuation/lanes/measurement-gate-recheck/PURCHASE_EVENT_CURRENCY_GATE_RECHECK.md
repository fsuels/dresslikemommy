# Purchase Event Currency Gate Recheck

Generated: 2026-05-10

Lane: `measurement-gate-recheck`

Mode: local/read-only sidecar only. No browser/account access, no checkout payment, no order, no GA4/Tag Assistant login, no Shopify/Admin writes, no theme edits, no Ads/Merchant/Pinterest writes.

## Decision

`GATE_STILL_OPEN__PRE_PURCHASE_PRESENTMENT_SUPPORTED__PURCHASE_EVENT_CURRENCY_NOT_PROVEN`

The current evidence supports non-US storefront/cart/checkout-to-shipping presentment before payment. It does not prove the official Shopify Google & YouTube app's `purchase` event currency/value for non-US orders. Non-US campaign enablement should remain blocked on this measurement gate until a non-US `purchase` event is observed in Tag Assistant/GA4/Google Ads, or until the owner approves one controlled non-US test purchase and capture.

## What Is Proven

- Theme setup initializes `window.dataLayer` and lazy-loads `assets/analytics.js` from `layout/theme.liquid:300-330`.
- Product currency metadata is presentment-aware: `snippets/meta-tags.liquid:267-280` sets `og:price:currency` from cart currency, localized country currency, shop currency, then `USD` fallback.
- Theme pre-purchase ecommerce currency resolution is presentment-aware: `assets/analytics.js:126-138` reads `og:price:currency`, then `window.Shopify.currency.active`, then `USD`.
- Theme pre-purchase ecommerce payloads stamp item-level and event-level currency: `assets/analytics.js:382-392` and `assets/analytics.js:448-465`.
- Theme pre-purchase pushes exist for `view_cart`, `begin_checkout`, `view_item`, and `add_to_cart`: `assets/analytics.js:913-984`.
- Existing no-payment evidence supports storefront/cart/checkout-to-shipping presentment for the current remaining-market cluster: `RO=RON`, `PT=EUR`, `GR=EUR`, plus recent `PL=PLN` and `CZ=CZK`.
- The prior paid-value gate proved only the US/USD purchase path: order `#9476` sent Google Ads purchase value `19.99`, currency `USD`, and GA4 purchase value `19.99`, currency `USD`.

## What Is Not Proven

- The actual `currency` parameter sent by the official Google & YouTube Shopify app on a non-US `purchase`.
- Whether Google Ads receives non-US purchases as presentment currency, FX-converted USD, or a broken mismatch such as `currency=USD` with an unconverted presentment value.
- Whether GA4 receives non-US `purchase.currency` before converting reporting into the GA4 property currency.
- Whether one non-US order produces exactly one Google Ads purchase conversion request and one paired GA4 purchase event with the same transaction/order id.
- Whether Google Ads conversion diagnostics currently show currency/value warnings for non-US purchase traffic.

Reason: repo/theme code does not author the `purchase` event. Purchase measurement is expected from the official Shopify Google & YouTube app on checkout thank-you/order-status surfaces, so local code and no-payment checkout evidence stop before the event that paid campaigns optimize against.

## Exact Next Browser-Enabled Readback Path

1. Open a logged-in browser session with Tag Assistant, GA4 DebugView or Realtime, Google Ads conversions UI, and DevTools Network available.
2. In Google Ads, open Tools and settings -> Conversions -> `Google Shopping App Purchase`. Capture settings and diagnostics: status recording, last received, value setting, include in conversions, endpoint/label if visible, and no currency/value warnings.
3. Start Tag Assistant preview for `https://www.dresslikemommy.com/`.
4. In a fresh storefront session, walk country-qualified non-US product -> add to cart -> cart -> begin checkout, stopping before payment. For this RO/PT/GR continuation lane, use `RO`, `PT`, and `GR`; add one stronger non-USD control such as `GB` or `CZ` if time allows.
5. In Tag Assistant and GA4 Realtime/DebugView, capture `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` details. Treat this only as `PARTIAL_PASS_PRE_PURCHASE_ONLY`; it must show expected presentment currency (`RO=RON`, `PT=EUR`, `GR=EUR`, optional `GB=GBP` or `CZ=CZK`).
6. Search GA4 Realtime/DebugView and Google Ads conversion activity for any genuine or historical non-US `purchase` event. If found, capture event parameters: `transaction_id` or order id, `value`, `currency`, item array, and Google Ads conversion endpoint/label.
7. If no genuine/historical non-US purchase event is available, stop and request owner approval using the exact phrase below before creating any order.
8. If a controlled purchase is approved, run exactly one low-value non-US test order in the selected market, capture Tag Assistant/DevTools/GA4 evidence, then immediately refund/cancel if the platform allows. Store sanitized evidence only.

Passing evidence requires a non-US `purchase` with one transaction/order id, correct value/currency, paired GA4 purchase, Google Ads purchase request, and no duplicate purchase fires. Acceptable outcomes are `currency=<presentment>` with presentment value, or documented `currency=USD` with FX-converted USD value. Blocking outcomes are missing currency, missing value, duplicate fires, no Google Ads purchase request, or `currency=USD` with unconverted presentment numeric value.

## Exact Owner Approval If A Real Test Purchase Is Required

Use this only if no genuine non-US organic order or historical Tag Assistant / GA4 DebugView purchase event can prove the path:

`APPROVE CONTROLLED NON-US PURCHASE MEASUREMENT PROOF ONLY: RUN ONE LOW-VALUE NON-US TEST PURCHASE FOR DRESSLIKEMOMMY USING A COUNTRY-QUALIFIED STOREFRONT SESSION, CAPTURE TAG ASSISTANT/DEVTOOLS/GA4 DEBUGVIEW EVIDENCE FOR THE OFFICIAL GOOGLE & YOUTUBE APP PURCHASE EVENT CURRENCY, VALUE, TRANSACTION_ID, AND GOOGLE ADS CONVERSION REQUEST, THEN IMMEDIATELY REFUND AND CANCEL THE TEST ORDER IF THE PLATFORM ALLOWS; DO NOT ENABLE ANY CAMPAIGN, DO NOT CHANGE BUDGETS/BIDS/STATUSES, DO NOT CHANGE CONVERSION GOALS/ACTIONS, DO NOT EDIT SHOPIFY PRODUCTS/THEME/CUSTOMER EVENTS, DO NOT EDIT MERCHANT/PINTEREST/ADS SETTINGS, DO NOT CREATE INVENTORY OR LOCAL-PICKUP CLAIMS, AND STORE ONLY SANITIZED EVIDENCE.`

Recommended first controlled market if the owner asks: `GB`, because GBP is non-USD and has prior no-payment checkout UI evidence. `RO` is also useful because it proves RON behavior for the current continuation cluster, but use only one low-value test order unless the owner approves more.

## Evidence Re-Read

- `ops/PROBLEM_TRACKER.md` entry `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PUBLIC_MEASUREMENT_PREFLIGHT_REPORT.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`.

## Commands Run

- `rg` over `ops/`, packet reports, theme files, and measurement keywords.
- `sed` on continuity/problem/coordination/worklog excerpts and the latest measurement reports.
- `find` over measurement packet paths and the requested continuation packet path.
- `nl -ba` on `assets/analytics.js`, `snippets/meta-tags.liquid`, and `layout/theme.liquid` for current line evidence.
- `mkdir -p` for this lane folder.

## Blockers

- No browser/account access in this sidecar lane, so Tag Assistant, GA4 DebugView/Realtime, Google Ads conversion diagnostics, and historical conversion activity could not be read.
- No purchase/payment/order was allowed or attempted.
- Local code can prove pre-purchase event construction, not the app-fired checkout `purchase` event.
- Existing `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` should remain `OWNER_APPROVAL_REQUIRED_FOR_PURCHASE_EVENT_PROOF` until the browser-enabled readback or approved test purchase passes.
