# GB/CA/AU Keyword Route Reroute Report

Timestamp: 2026-05-14 11:40 EDT

Scope: repo-local keyword-universe repair plus public storefront readbacks. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or live theme write occurred.

## Result

The highest-priority remaining P0 queue row still requires authenticated Google Ads / Keyword Planner CPC validation. This automation runtime is already recorded as `AUTOMATION_CAPABILITY_MISMATCH` for authenticated account surfaces, so the safe executable lane was the route-cleanliness blocker that was preventing more `GREEN` rows from reaching that CPC validation step.

Updated `ops/marketing/keyword_universe.csv` so:

- GB/CA/AU rows already routed to `/collections/mommy-and-me`, `/collections/family-matching`, and `/collections/pajamas` now say `route_clean_cpc_validation_required`.
- GB/CA/AU vacation rows that used the `404` `/collections/vacation` route are rerouted to the most relevant clean route:
  - mother/daughter dress intent to `/collections/mommy-and-me`
  - family/travel/tropical intent to `/collections/family-matching`
- GB/CA/AU matching-dress wedding-guest rows that used supplier-leaking `/collections/matching-dresses` are rerouted to `/collections/mommy-and-me`.
- GB/CA/AU daddy rows that used Christmas-metadata `/collections/daddy-and-me` are rerouted to `/collections/family-matching`, which currently shows father/son and family matching products without the Christmas-pattern blocker.
- GB/CA/AU swimwear rows remain held on `/collections/swimsuits`; no clean swim-specific route exists yet, and product/vendor-source repair would require a separate safe path or fresh approval.

## Validation

CSV parse and count check:

- Total rows: `105`
- Thresholds: `77 GREEN`, `20 YELLOW`, `8 RED`
- GB/CA/AU `GREEN` rows with `cpc_validation_required`: `31`
- GB/CA/AU swimwear rows still blocked for supplier JSON vendor: `5`
- GB/CA/AU rows still routed to `/collections/vacation`: `0`
- GB/CA/AU rows still routed to `/collections/matching-dresses`: `0`
- GB/CA/AU rows still routed to `/collections/daddy-and-me`: `0`

Public readback for the three now-valid destination routes:

| Route | GB | CA | AU |
|---|---|---|---|
| `/collections/mommy-and-me` | `200`, `0` leak hits | `200`, `0` leak hits | `200`, `0` leak hits |
| `/collections/family-matching` | `200`, `0` leak hits | `200`, `0` leak hits | `200`, `0` leak hits |
| `/collections/pajamas` | `200`, `0` leak hits | `200`, `0` leak hits | `200`, `0` leak hits |

Leak-hit check counted `detail.1688.com`, `1688.com`, `alibaba.com`, `aliexpress.com`, `data-analytics-vendor="https://`, and `data-item-brand="https://`.

## What Did Not Change

- No live Google Ads keyword upload/apply/add action.
- No bid, budget, status, negative, campaign, ad group, ad, or conversion change.
- No Shopify product/vendor metadata edit.
- No live theme publish.
- No Merchant, Pinterest, GA4/GTM, billing, feed, or product-scope write.

## Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for the 31 GB/CA/AU `GREEN` rows that now have clean routes. Only prepare a bounded action row if the exact candidate set proves auction-entry feasibility at max CPC `$0.15`, passes reviewer checks, and has an after-state readback plan.
