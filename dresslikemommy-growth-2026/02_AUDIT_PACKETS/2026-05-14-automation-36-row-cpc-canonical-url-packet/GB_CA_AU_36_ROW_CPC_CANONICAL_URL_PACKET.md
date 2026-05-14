# GB/CA/AU 36-Row CPC Canonical URL Packet

Timestamp: 2026-05-14 14:57 EDT

Scope: repo-local canonical copy plus public/read-only route readback for the existing GB/CA/AU 36-row CPC validation packet. No Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, product-scope, or live theme write occurred.

## Result

The packet is now ready for authenticated CPC validation without redirect cleanup:

- Source rows: `36`
- Rows canonicalized from `/collections/family-matching` to `/collections/matching-outfits`: `11`
- Unique market/route URLs: `12`
- Public route fetches: `24`
- Non-200 route fetches: `0`
- Redirected fetches: `0`
- Supplier/source-domain or URL-brand hits: `0`
- Stale seasonal/local-inventory trust hits: `0`

Rows by market:

- GB: `12`
- CA: `12`
- AU: `12`

The authenticated `$0.15` CPC/auction-entry gate remains open. This packet does not authorize upload/apply/add keyword/bid/status/budget/negative changes.

## Route Readback

| Market | Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URLs | Shipping signal | Title |
|---|---|---|---:|---|---:|---:|---:|---|---|
| AU | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| AU | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| AU | `/collections/matching-outfits` | text_html | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| AU | `/collections/matching-outfits` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| AU | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| AU | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| AU | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| AU | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| CA | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| CA | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| CA | `/collections/matching-outfits` | text_html | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| CA | `/collections/matching-outfits` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| CA | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| CA | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| CA | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| CA | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| GB | `/collections/family-swimsuits` | text_html | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| GB | `/collections/family-swimsuits` | star_cache_bust | `200` | False | `0` | `0` | `3` | True | `Matching Family Bathing Suits | Family Swimwear` |
| GB | `/collections/matching-outfits` | text_html | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| GB | `/collections/matching-outfits` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Family Matching Outfits | Mommy and Me` |
| GB | `/collections/mommy-and-me` | text_html | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| GB | `/collections/mommy-and-me` | star_cache_bust | `200` | False | `0` | `0` | `39` | True | `Mommy and Me Outfits | Dresses, Swimsuits and Matching Sets` |
| GB | `/collections/pajamas` | text_html | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |
| GB | `/collections/pajamas` | star_cache_bust | `200` | False | `0` | `0` | `25` | True | `Mommy and Me Pajamas - Matching Family Sleepwear | Dress Like Mommy` |

## Exact Next Gate

Run authenticated read-only Google Ads / Keyword Planner validation for `gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv` at max CPC `$0.15`. Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass, fresh before-state Ads readback, and after-state readback.

## Files

- Canonical validation CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_clean_route_cpc_validation_rows_canonical_urls.csv`
- Public route readback rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_canonical_url_public_readback_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_canonical_url_packet_summary.json`
