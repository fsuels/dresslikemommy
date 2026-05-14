# GB/CA/AU 36-Row CPC Public Route Refresh

Timestamp: 2026-05-14 14:37 EDT

Scope: public/read-only route refresh for the existing 36-row GB/CA/AU CPC validation packet. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

The exact 36-row packet still has public-clean final URLs for CPC validation:

- Rows checked from source packet: `36`
- Unique market/route URLs: `12`
- Public route fetches: `24`
- Non-200 route fetches: `0`
- Redirected fetches: `6`
- Supplier/source-domain or URL-brand hits: `0`
- Stale seasonal/local-inventory trust hits: `0`

Rows by market:

- GB: `12`
- CA: `12`
- AU: `12`

The authenticated CPC/auction-entry gate remains blocked in this automation runtime because the shell has no Google Ads env keys and the Python Google Ads client package is not installed. This refresh does not authorize upload/apply/add keyword/bid/status/budget/negative changes.

Non-blocking URL note: the `/collections/family-matching` packet URLs redirect cleanly to `/collections/matching-outfits?country=...`. This is not a source-cleanliness blocker, but future live packets should prefer canonical final URLs after the authenticated CPC gate.

## Route Readback

| Market | Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Title |
|---|---|---|---:|---|---:|---:|---:|---|---|
| AU | `/collections/family-matching` | text_html | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| AU | `/collections/family-matching` | star_cache_bust | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| AU | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| AU | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| AU | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| AU | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| AU | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| AU | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| CA | `/collections/family-matching` | text_html | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| CA | `/collections/family-matching` | star_cache_bust | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| CA | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| CA | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| CA | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| CA | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| CA | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| CA | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| GB | `/collections/family-matching` | text_html | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| GB | `/collections/family-matching` | star_cache_bust | `200` | True | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| GB | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| GB | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| GB | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| GB | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| GB | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| GB | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |

## Exact Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for `gb_ca_au_36_clean_route_cpc_validation_rows.csv` at max CPC `$0.15`. Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass and after-state readback.

## Files

- Source packet CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv`
- Public route rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/gb_ca_au_36_row_public_route_readback_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/gb_ca_au_36_row_public_route_readback_summary.json`
