# Paid Growth Measurement + Ads Branch Continuation Report

Date: 2026-05-10

Anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-measurement-prepurchase-branch-gated`

## Executive Result

The sprint advanced the measurement gate, but did not close it.

Pre-purchase measurement now has fresh browser evidence in `GBP` and `EUR`: product/cart/checkout-entry events carry correct market currency/value into Google/GA requests. Google Ads conversion-action settings also read back clean for the primary `Google Shopping App Purchase` action.

The remaining blocker is narrower and clearer: the official Shopify Google & YouTube app's non-US `purchase` event still needs proof on the thank-you/order-status surface. No payment or order was created in this session.

The `RO` / `PT` / `GR` Ads branch was not executed because the latest owner instruction did not give exact branch approval to retry `RO` or skip/park `RO`. Current Ads state remains `12 built / 3 absent / 2 parked`.

## Guardrails Honored

No live spend, campaign enablement, budget/bid/status changes, PMax enable, Standard Shopping changes, product-scope/feed-label/product-group changes, conversion-goal changes, Merchant uploads, Shopify live product-data changes, checkout payment, order, refund, or cancelation occurred.

## Parent/Orchestrator Work

- Read the canonical paid-growth continuation prompt and continuity files.
- Used parallel sidecars for disjoint local-only lanes.
- Ran safe browser measurement checks for `GB` and `DE`.
- Ran read-only Google Ads conversion-action readback.
- Integrated evidence into this packet and durable tracker/worklog memory.

## Sidecar Results

### Ads Branch Decision

File: `lanes/ads-branch-decision/ADS_BRANCH_DECISION.md`

Conclusion:

- Built and read back clean: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Absent/uncreated: `RO`, `PT`, `GR`.
- Parked: `FR`, `BE`.
- The next Ads action needs exact owner direction:
  - retry `RO` with a new one-country preview after confirming no in-progress row and no RO campaign, or
  - skip/park `RO` and continue one country at a time with `PT`, then `GR`.

### Measurement Historical Hunt

File: `lanes/measurement-browser-readback/HISTORICAL_NON_US_PURCHASE_EVIDENCE_HUNT.md`

Conclusion:

- Existing repo evidence contains strong US/USD purchase proof only.
- No historical non-US Shopify order, GA4 DebugView, Tag Assistant, Google Ads conversion request, or raw purchase-event proof was found.
- The non-US purchase-event gate remains open.

### North Star Lane Board

File: `lanes/north-star-lane-board/NORTH_STAR_LANE_BOARD.md`

Conclusion:

- Closest safe path to the North Star is measurement proof, then explicit Ads branch choice, then tightly controlled paused-infrastructure completion.
- Live non-US spend remains blocked until measurement, catalog/feed, URL, and approval gates are cleared.

## Browser Measurement Findings

Detailed report: `lanes/measurement-browser-readback/MEASUREMENT_BROWSER_READBACK.md`

### GB / GBP

- Tag Assistant connected to the storefront.
- Tags observed: `AW-853411529`, `G-N4EQNK0MMB`, `GT-WRH8Q3MD`.
- Checkout-entry page used `en-GB`.
- `begin_checkout` carried `currency: GBP`, `value: 15`, and country `GB`.
- No payment/order.

### DE / EUR

- Separate Chrome CDP capture reached checkout entry.
- `add_to_cart` and `begin_checkout` Google/GA requests carried `EUR`.
- Google Ads `begin_checkout` label `ditQCJzowY8YEMmN-JYD` carried `value=17.95` and `currency_code=EUR`.
- No payment/order.

### Google Ads Conversion Action

Readback generated in `lanes/measurement-browser-readback/google_ads_conversion_value_readback/`.

Key status:

- `purchase_conversion_value_gate_status`: `PASS_PURCHASE_CONVERSION_VALUE_TRACKING_VERIFIED__NO_CURRENT_AD_ATTRIBUTION`.
- Primary account-level purchase action count: `1`.
- Target action: `Google Shopping App Purchase`.
- Target action is primary and account-level.
- Dynamic value setting is proven.
- Enhanced conversions are enabled.
- Recent request exists from `2026-05-09T02:40:54.022671+00:00`.
- Campaign enable allowed: `false`.

## Problem Status Changes

- `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`: remains `OWNER_APPROVAL_REQUIRED_FOR_PURCHASE_EVENT_PROOF`, but now has a stronger partial pass: `GBP` and `EUR` pre-purchase events are presentment-aware through checkout entry.
- `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`: remains `PARTIAL_12_APPLIED_RO_STALE_PREVIEW_NOT_VISIBLE_PT_GR_ABSENT_FR_STALE_PREVIEW_BE_THROTTLE`; latest branch-decision sidecar confirms current state and exact branch approval requirement.

## Next Best Action

Measurement:

- If a genuine non-US order occurs, capture Tag Assistant/GA4/Google Ads evidence for the official app `purchase` event currency, value, transaction id, and duplicate behavior.
- If no genuine order is available, request exact owner approval for a controlled non-US test purchase/refund/cancel procedure.

Ads branch:

- Ask the owner for an exact branch decision:
  - retry `RO`, or
  - skip/park `RO` and proceed `PT` then `GR`.

Do not enable any non-US campaign until the measurement gate is closed or the owner explicitly accepts the risk in a fresh approval.
