# US Search Active-Product Validation Packet

Timestamp: 2026-05-15 04:27 EDT

Scope: repo-local, no-upload US Search validation input built only from `GREEN` US keyword-universe rows whose canonical route has public active-product proof. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

- Base keyword rows: `12`
- Exact/phrase forecast rows: `24`
- Unique canonical routes: `3`
- Public route fetches: `6`
- Non-200 route fetches: `0`
- Redirected fetches: `0`
- Supplier/source-domain or URL-brand hits: `0`
- Stale seasonal/local-inventory trust hits: `0`

Rows by route:

- `/collections/matching-outfits`: `4`
- `/collections/mommy-and-me`: `4`
- `/collections/pajamas`: `4`

Rows by category:

- `Beach Days`: `1`
- `Birthdays`: `1`
- `Pajamas`: `4`
- `Photo Days`: `3`
- `Vacation`: `3`

This is a validation input only. It is not an upload file and does not create a `GREEN` live action row. The authenticated `$0.15` CPC/search-feasibility gate remains open.

## Route Readback

| Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Keyword count | Title |
|---|---|---:|---|---:|---:|---:|---|---:|---|
| /collections/matching-outfits | text_html | `200` | False | `0` | `0` | `39` | True | `4` | `Family Matching Outfits | Mommy and Me` |
| /collections/matching-outfits | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `4` | `Family Matching Outfits | Mommy and Me` |
| /collections/mommy-and-me | text_html | `200` | False | `0` | `0` | `39` | True | `4` | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| /collections/mommy-and-me | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `4` | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| /collections/pajamas | text_html | `200` | False | `0` | `0` | `25` | True | `4` | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| /collections/pajamas | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `4` | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |

## Exact Next Gate

After Google Ads API Basic Access approval, run this packet through the read-only forecast harness or a correctly scoped Keyword Planner export using United States, English, exact/phrase rows, and max CPC `$0.15`. Promote only rows that produce real `PASS_015_CPC_GATE` evidence, reviewer pass, fresh before-state Ads readback, and an after-state readback plan.

## Files

- Base validation CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_12_active_product_cpc_validation_rows.csv`
- Exact/phrase matrix: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_12_active_product_cpc_validation_matrix.csv`
- Public route readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_active_product_route_readback.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_active_product_validation_summary.json`
