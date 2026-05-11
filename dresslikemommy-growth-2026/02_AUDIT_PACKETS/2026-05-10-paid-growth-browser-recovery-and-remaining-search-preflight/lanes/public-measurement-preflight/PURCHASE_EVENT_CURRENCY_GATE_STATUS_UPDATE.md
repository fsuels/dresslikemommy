# Purchase Event Currency Gate Status Update

Generated: 2026-05-10
Lane: `public-measurement-preflight`
Mode: local/read-only sidecar investigation only

## Decision

`PURCHASE_CURRENCY_GATE_STILL_OPEN__PRE_PURCHASE_PRESENTMENT_SUPPORTED`

Local evidence can support the pre-purchase currency story, but it cannot prove the official Google & YouTube Shopify app's non-US `purchase` event currency. Non-US paid Search enablement should remain blocked on this measurement gate until a real non-US purchase event is observed or an owner-approved controlled test order is run and captured.

## What Local Evidence Proves

- The theme initializes `window.dataLayer` and loads `assets/analytics.js`; there is no theme-level Google purchase tag in `layout/theme.liquid` (`layout/theme.liquid:300-330`).
- Product-page currency metadata is presentment-aware: `snippets/meta-tags.liquid:269-280` resolves `og:price:currency` from `cart.currency.iso_code`, then `localization.country.currency.iso_code`, then shop currency / `USD`.
- `assets/analytics.js:126-138` resolves ecommerce event currency from `og:price:currency`, then `window.Shopify.currency.active`, then `USD`.
- `assets/analytics.js:382-392` stamps item-level `currency`; `assets/analytics.js:448-465` stamps event-level `currency`.
- The pre-purchase ecommerce pushes are theme-owned: `view_cart` (`assets/analytics.js:924-933`), `begin_checkout` (`assets/analytics.js:950-959`), `view_item` (`assets/analytics.js:962-970`), and `add_to_cart` (`assets/analytics.js:973-984`).
- Existing lane evidence already concludes `PL`, `CZ`, `RO`, `PT`, and `GR` carried expected storefront/cart/checkout-to-shipping currencies before payment, while explicitly not closing the purchase gap (`PUBLIC_MEASUREMENT_PREFLIGHT_REPORT.md:11-24`, `:114-132`).
- The prior paid-value gate proves US/USD purchase measurement only: order `#9476` fired Google Ads purchase value `19.99`, currency `USD`, and GA4 purchase value `19.99`, currency `USD` (`FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md:5-26`).

## What Local Evidence Cannot Prove

- The actual `currency` parameter sent by the official Google & YouTube Shopify app on a non-US checkout `purchase`.
- Whether Google Ads receives a non-US purchase as presentment currency, FX-converted USD, or a bad mismatch such as `currency=USD` with the presentment numeric value.
- Whether GA4 receives non-US `purchase.currency` as presentment currency before converting revenue into the GA4 property reporting currency.
- Whether Google Ads conversion diagnostics show any currency/value warnings for non-US purchases.

Reason: the theme does not author `purchase`. The purchase event is app-fired from Shopify checkout / thank-you by the official Google & YouTube app, so repo code and no-payment checkout evidence stop one step before the event that Google Ads optimizes against.

## Can Tag Assistant / GA4 Realtime Prove Anything Short Of Purchase?

Yes, but only the pre-purchase layer:

- Tag Assistant + GA4 Realtime can prove live browser delivery of `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` with market-presentment currency.
- This is useful because it validates that storefront, theme dataLayer, Google tag visibility, and GA4 event intake agree before payment.
- It does not prove app-fired purchase currency unless a `purchase` event actually occurs in that session or appears from a genuine/historical non-US order.

Short of a purchase, Tag Assistant / GA4 Realtime should be treated as `PARTIAL_PASS_PRE_PURCHASE_ONLY`, not a launch-clearing pass.

## Remaining Gate To Close

Minimum passing evidence:

- Capture one non-US `purchase` event from the official Google & YouTube Shopify app.
- Confirm Google Ads purchase request includes expected conversion endpoint/label, one order/transaction id, `value`, and `currency`.
- Confirm paired GA4 purchase request includes the same transaction id, `value`, and `currency`.
- Acceptable outcomes:
  - Best: `currency=<presentment>` and `value=<presentment amount>`.
  - Acceptable if documented: `currency=USD` and `value=<FX-converted USD amount>`.
  - Blocking fail: `currency=USD` with unconverted presentment numeric value, missing currency, missing value, duplicate purchase fires, or no Google Ads purchase request.

## Exact Owner Approval If Controlled Test Purchase Is Required

Use this only if no genuine non-US organic order or historical Tag Assistant / GA4 DebugView purchase event is available:

`APPROVE CONTROLLED NON-US PURCHASE MEASUREMENT PROOF ONLY: RUN ONE LOW-VALUE NON-US TEST PURCHASE FOR DRESSLIKEMOMMY USING A COUNTRY-QUALIFIED STOREFRONT SESSION, CAPTURE TAG ASSISTANT/DEVTOOLS/GA4 DEBUGVIEW EVIDENCE FOR THE OFFICIAL GOOGLE & YOUTUBE APP PURCHASE EVENT CURRENCY, VALUE, TRANSACTION_ID, AND GOOGLE ADS CONVERSION REQUEST, THEN IMMEDIATELY REFUND AND CANCEL THE TEST ORDER IF THE PLATFORM ALLOWS; DO NOT ENABLE ANY CAMPAIGN, DO NOT CHANGE BUDGETS/BIDS/STATUSES, DO NOT CHANGE CONVERSION GOALS/ACTIONS, DO NOT EDIT SHOPIFY PRODUCTS/THEME/CUSTOMER EVENTS, DO NOT EDIT MERCHANT/PINTEREST/ADS SETTINGS, DO NOT CREATE INVENTORY OR LOCAL-PICKUP CLAIMS, AND STORE ONLY SANITIZED EVIDENCE.`

If the owner wants a specific market named in the approval, use `GB` first because GBP is non-USD and has already passed no-payment checkout UI evidence. `DE` or `IT` are also reasonable EUR checks, but a non-EUR market gives stronger proof that the pixel is not silently flattening all non-US currency handling.

## Recommended Report Path

This file is written under the current session packet lane:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md`

Parent integration can cite this as a sidecar status update. No `ops/PROBLEM_TRACKER.md`, coordination, worklog, theme, Shopify, Ads, Merchant, Pinterest, or credential files were modified.
