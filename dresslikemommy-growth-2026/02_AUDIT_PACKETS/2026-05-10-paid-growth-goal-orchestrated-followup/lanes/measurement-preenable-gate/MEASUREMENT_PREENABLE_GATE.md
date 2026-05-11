# Measurement Pre-Enable Gate: Non-US Purchase Currency/Value

Generated: 2026-05-10
Worker: Worker B
Lane: `measurement-preenable-gate`
Mode: local/read-only only. No browser use, no network checkout probing, no payment, no order, no Shopify/Admin/Ads/GA4/GTM/Merchant/Pinterest/theme writes.

## Decision

`NON_US_LIVE_ENABLE_BLOCKED__PRE_PURCHASE_PRESENTMENT_SUPPORTED__PURCHASE_EVENT_CURRENCY_VALUE_NOT_PROVEN`

The safe current position is unchanged: non-US Search can remain paused infrastructure, but live non-US enablement must stay blocked until the official Shopify Google & YouTube app's non-US `purchase` event is proven to send correct value/currency into GA4/Google Ads, or until the owner explicitly accepts that risk.

## What Is Proven

### Storefront and theme pre-purchase currency

- Theme initializes `window.dataLayer` and lazy-loads `assets/analytics.js` from `layout/theme.liquid:300-342`.
- Product-page currency metadata is presentment-aware: `snippets/meta-tags.liquid:267-280` sets `og:price:currency` from `cart.currency.iso_code`, then `localization.country.currency.iso_code`, then shop currency, with `USD` only as fallback.
- Theme ecommerce currency resolution is presentment-aware before purchase: `assets/analytics.js:126-138` reads `og:price:currency`, then `window.Shopify.currency.active`, then `USD`.
- Theme item/event ecommerce payloads stamp currency:
  - `assets/analytics.js:382-392` item-level `currency`.
  - `assets/analytics.js:448-465` event-level `currency` and `value`.
  - `assets/analytics.js:809-821` cart snapshot item-level `currency`.
- Theme pre-purchase dataLayer pushes exist for:
  - `view_cart`: `assets/analytics.js:913-933`.
  - `begin_checkout`: `assets/analytics.js:936-959`.
  - `view_item`: `assets/analytics.js:962-970`.
  - `add_to_cart`: `assets/analytics.js:973-984`.
- Prior no-payment storefront/cart/checkout-to-shipping packets support pre-purchase presentment for non-US markets, including GB/CA/AU/ES/IT/RO/PT and later CH/DK/DE/NL/SE/PL/CZ/GR. This is checkout readiness evidence only.
- The prior paid-value proof is US/USD only: the 2026-04-30 live paid order evidence proved Google Ads/GA4 purchase value/currency for a US order, not for non-US presentment.

### Theme does not own purchase

- A read-only search for `purchase`, `checkout_completed`, `thank_you`, `order_status`, `transaction_id`, and `order_id` across `assets/analytics.js`, `layout`, `snippets`, `sections`, and `templates` found no theme purchase-event implementation. Hits were copy text only, not tracking code.
- Therefore, repo/theme evidence can prove pre-purchase dataLayer behavior, but it cannot prove checkout thank-you/order-status `purchase` behavior.

## What Is Not Proven

- The actual `currency` parameter sent by the official Shopify Google & YouTube app on a non-US `purchase`.
- The actual `value` parameter sent for a non-US order.
- Whether Google Ads receives non-US purchases as:
  - presentment currency plus presentment value, such as `GBP 24.95`;
  - FX-converted USD value plus `USD`;
  - or the blocking bad case: `USD` currency with an unconverted non-US numeric value.
- Whether GA4 receives non-US `purchase.currency` before any property-level reporting-currency conversion.
- Whether a non-US order fires exactly one Google Ads purchase request and one paired GA4 purchase event with the same transaction/order ID.
- Whether current Google Ads conversion diagnostics show any non-US currency/value warning.

This is the open risk tracked as `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`.

## Safest Read-Only Browser Checklist

This checklist is useful and safe because it does not submit payment or create an order. It can produce a partial measurement pass only.

1. Open logged-in Tag Assistant, GA4 DebugView or Realtime, and Google Ads conversion diagnostics.
2. In Google Ads, open `Google Shopping App Purchase` read-only. Capture status, last received, value setting, include-in-conversions, diagnostics, and any currency/value warning. Do not click Save/Edit.
3. Start Tag Assistant preview for `https://www.dresslikemommy.com/`.
4. For at least one EUR market and one non-EUR market, walk a country-qualified storefront path: product page -> add to cart -> cart -> begin checkout. Stop before payment.
5. Confirm Tag Assistant and GA4 show `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` with the storefront-presentment currency.
6. Check GA4 DebugView/Realtime and Google Ads conversion activity for any genuine historical or live organic non-US `purchase` event. If one exists, capture sanitized `transaction_id`, `value`, `currency`, item detail, and Google Ads conversion request evidence.
7. If no genuine or historical non-US purchase event exists, stop. Mark the result `PARTIAL_PASS_PRE_PURCHASE_ONLY`.

This read-only path is insufficient when it does not observe a real non-US `purchase` event. Pre-purchase events do not prove the app-fired checkout purchase payload that Google Ads optimizes against.

## Controlled Test Purchase Approval Wording

Use this only if no genuine non-US organic order, historical thank-you replay, Tag Assistant recording, GA4 DebugView event, or Google Ads conversion activity can prove the purchase path:

`APPROVE CONTROLLED NON-US PURCHASE MEASUREMENT PROOF ONLY: RUN ONE LOW-VALUE NON-US TEST PURCHASE FOR DRESSLIKEMOMMY USING A COUNTRY-QUALIFIED STOREFRONT SESSION, CAPTURE TAG ASSISTANT/DEVTOOLS/GA4 DEBUGVIEW EVIDENCE FOR THE OFFICIAL GOOGLE & YOUTUBE APP PURCHASE EVENT CURRENCY, VALUE, TRANSACTION_ID, AND GOOGLE ADS CONVERSION REQUEST, THEN IMMEDIATELY REFUND AND CANCEL THE TEST ORDER IF THE PLATFORM ALLOWS; DO NOT ENABLE ANY CAMPAIGN, DO NOT CHANGE BUDGETS/BIDS/STATUSES, DO NOT CHANGE CONVERSION GOALS/ACTIONS, DO NOT EDIT SHOPIFY PRODUCTS/THEME/CUSTOMER EVENTS, DO NOT EDIT MERCHANT/PINTEREST/ADS SETTINGS, DO NOT CREATE INVENTORY OR LOCAL-PICKUP CLAIMS, AND STORE ONLY SANITIZED EVIDENCE.`

Best first controlled market if the owner asks: `GB`, because GBP is non-USD and already has no-payment checkout UI evidence. `RO` is also valuable for RON, but run only one low-value order unless the owner explicitly approves more.

## Pass / Fail

### Pass

The gate passes only when evidence shows a non-US `purchase` event from the official Shopify Google & YouTube app with:

- one transaction/order ID;
- correct `value`;
- correct `currency`;
- paired GA4 purchase event;
- Google Ads purchase conversion request;
- no duplicate purchase fires;
- no Google Ads diagnostics warning that invalidates currency/value.

Acceptable currency/value outcomes:

- `currency=<presentment>` with presentment value.
- `currency=USD` with documented FX-converted USD value.

### Partial Pass

`view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` show correct presentment currency in Tag Assistant/GA4, but no non-US `purchase` event is observed. This supports storefront and pre-purchase tracking only. It does not clear live enablement.

### Fail

- Missing purchase `currency`.
- Missing purchase `value`.
- `currency=USD` with unconverted non-US presentment numeric value.
- Duplicate purchase fires.
- No Google Ads purchase request.
- GA4 and Google Ads disagree in a way that makes ROAS unreliable.
- Duplicate Primary purchase actions or a campaign-level conversion-goal surprise is found before enablement.

## Why Enablement Remains Blocked

The owner target is about `650% ROAS`. If non-US purchase value/currency is wrong, campaign decisions can be wrong even when clicks and orders are real. A campaign can look profitable or unprofitable because measurement is mis-currencied, not because the market works or fails.

Therefore, no non-US Search campaign should be enabled until this gate passes, or until the owner explicitly accepts the measurement risk in the same action-time approval that names the affected country/campaign.

## Evidence Read

- `ops/PROBLEM_TRACKER.md`, entry `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`.
- `ops/AGENT_WORKLOG.md`, latest anchor `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-ro-parked-preview-not-visible`.
- `assets/analytics.js`.
- `layout/theme.liquid`.
- `snippets/meta-tags.liquid`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/measurement-gate-recheck/PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/public-measurement-preflight/PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/measurement-readback-recipe/MEASUREMENT_READBACK_RECIPE.md`.

## Commands / Read-Only Inspections Run

- `rg -n "PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT|AGENT_CONTINUITY_ANCHOR|measurement|purchase|currency" ops/PROBLEM_TRACKER.md ops/AGENT_WORKLOG.md assets/analytics.js`
- `rg --files dresslikemommy-growth-2026/02_AUDIT_PACKETS | rg "(MEASUREMENT_CONVERSION_GAP_REPORT|PURCHASE_EVENT_CURRENCY_GATE_RECHECK|measurement|MEASUREMENT|decision|DECISION|gate|GATE)"`
- `ls -la dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/lanes/measurement-preenable-gate`
- `sed -n '202,248p' ops/PROBLEM_TRACKER.md`
- `sed -n '33617,33672p' ops/AGENT_WORKLOG.md`
- `sed -n '1,260p' .../MEASUREMENT_CONVERSION_GAP_REPORT.md`
- `sed -n '1,240p' .../PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md`
- `sed -n '1,240p' .../MEASUREMENT_READBACK_RECIPE.md`
- `sed -n '1,220p' .../PURCHASE_EVENT_CURRENCY_GATE_STATUS_UPDATE.md`
- `nl -ba assets/analytics.js | sed -n '110,155p;370,475p;795,835p'`
- `nl -ba assets/analytics.js | sed -n '900,990p'`
- `nl -ba snippets/meta-tags.liquid | sed -n '260,282p'`
- `nl -ba layout/theme.liquid | sed -n '296,342p'`
- `rg -n "\\bpurchase\\b|checkout_completed|thank_you|order_status|transaction_id|order_id" assets/analytics.js layout snippets sections templates`

## Guardrails Honored

- No browser use.
- No network checkout probe.
- No payment, refund, cancelation, or order.
- No Shopify Admin, Google Ads, GA4, GTM, Merchant, Pinterest, theme, tracker, worklog, or coordination edit.
- Only this file was written, under the assigned Worker B lane.
