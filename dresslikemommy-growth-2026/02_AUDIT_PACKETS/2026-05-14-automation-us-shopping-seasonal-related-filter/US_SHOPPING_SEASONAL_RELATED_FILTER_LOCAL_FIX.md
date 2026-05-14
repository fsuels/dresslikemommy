# US Shopping Seasonal Related-Product Filter Local Fix

Generated: `2026-05-14T17:38:55Z`

## Scope

- Lane: US Standard Shopping held PDP public-landing cleanup.
- Product checked: `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`.
- Related problem: `PROB-2026-05-14-US-SHOPPING-QUERY-TITLE-FIT`.
- Repo-local theme edit only. No live Shopify theme push, no Shopify Admin product edit, no Merchant/feed/product-group edit, and no Ads write occurred.

## Why This Was Executable

The top queue rows still require authenticated account surfaces. This unattended automation runtime is already recorded as `AUTOMATION_CAPABILITY_MISMATCH` for those lanes, so the next safe sales-moving step was to reduce a public-landing blocker locally.

The prior held-PDP packet had two rows for the swim-trunks handle excluded until stale seasonal copy was clean. A fresh source-context readback showed the stale `Christmas` hits were not on the current product content. They came from related-product card metadata and image alt text inside the PDP recommendations section.

## Public Source Context

Fresh public GETs for:

`https://www.dresslikemommy.com/products/dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set?country=US`

showed:

- `detail.1688.com`: `0` hits.
- `1688.com`: `0` hits.
- `Christmas`: `4` hits.
- `Christmas` contexts were related product cards, including `data-analytics-pattern="Christmas"` and related-card image alt text containing `christmas print`.

Fresh public GETs for:

`https://www.dresslikemommy.com/products/chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit?country=US`

showed:

- `detail.1688.com`: `12` hits in Shopify injected product variant JSON, with `product.vendor` equal to a source URL.
- This is a Shopify product-data issue, not safely solvable by the related-product theme filter.

## Local Fix

Updated `snippets/buy-box-similar-styles.liquid` so related-product recommendations skip Christmas/Santa/Xmas products unless the current PDP is also a Christmas/Santa/Xmas context.

This keeps Christmas products available on true seasonal pages, while preventing a non-seasonal swim PDP from exposing stale Christmas metadata in its paid-landing source.

## Verification

- `shopify theme check --path . --fail-level error --output json` returned `[]`.
- `python3.13 -m json.tool dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-held-pdp-repair-packet/us_shopping_held_pdp_repair_summary.json` passed.
- Public source context fetch identified the issue source before the patch.

## Decision

- The dynamic swim-trunks held rows now have a local theme repair ready, but they remain excluded from paid export/title decisions until the theme change is live-synced and public source readback shows `0` stale seasonal hits.
- The chic sequin lace held rows remain excluded until owner-approved Shopify product/vendor/source cleanup removes the source URL from Shopify injected product JSON.
- The green-and-white weak-fit row remains source-clean but should enter decisions only if authenticated item-level export proves impressions/relevance.

## Next Safe Action

If the owner approves live theme sync for this local fix:

`APPROVE LIVE THEME SYNC FOR US SHOPPING SEASONAL RELATED-PRODUCT FILTER ONLY: push the local related-product recommendation filter in snippets/buy-box-similar-styles.liquid so non-seasonal PDPs do not render Christmas/Santa/Xmas related-product metadata; no Shopify Admin product data, Merchant, Google Ads, Pinterest, budget, bid, status, conversion, feed, product-scope, price, discount, or policy changes; read back the dynamic swim-trunks PDP public source before and after and keep it out of paid export/use unless stale seasonal hits are zero.`

