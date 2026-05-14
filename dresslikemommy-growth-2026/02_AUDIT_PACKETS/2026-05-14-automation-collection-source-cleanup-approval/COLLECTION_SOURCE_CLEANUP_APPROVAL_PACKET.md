# Collection Source Cleanup Approval Packet

Timestamp: 2026-05-14 15:38 EDT automation run

Scope: public/read-only storefront source readback for the remaining supplier-leaking collection routes in the paid-growth keyword universe. No Shopify Admin, Google Ads, Merchant, Pinterest, GA4/GTM, billing, feed, product, campaign, budget, bid, status, conversion, product-scope, or live theme write occurred.

## Result

`/collections/swimsuits` and `/collections/matching-dresses` still expose supplier-source URLs through Shopify automatic product JSON in public collection HTML. This is not the already-sanitized theme `data-analytics-*` attribute path.

Keep both routes excluded from paid traffic until one of these happens:

- exact owner-approved Shopify product/vendor source cleanup is performed for the product rows below and public source readback returns `0` supplier hits, or
- future paid keyword rows continue to use clean alternate routes such as `/collections/family-swimsuits`, `/collections/mommy-and-me`, or `/collections/matching-outfits`.

Dirty product counts by route:

- `/collections/swimsuits`: `2`
- `/collections/matching-dresses`: `1`

Keyword-universe rows still pointing at these dirty routes:

- `/collections/swimsuits`: `3`
- `/collections/matching-dresses`: `5`

## Public Route Readback

Leak-hit check counted `detail.1688.com`, `1688.com`, `alibaba.com`, `aliexpress.com`, `data-analytics-vendor="http`, and `data-item-brand="http`.

| Route | Market | Header variant | Status | Supplier/url-brand hits | Source-product count | Product URL count | Decision |
|---|---|---|---:|---:|---:|---:|---|
| /collections/swimsuits | US | text/html | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | US | star | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | GB | text/html | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | GB | star | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | CA | text/html | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | CA | star | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | AU | text/html | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/swimsuits | AU | star | `200` | `8` | `2` | `39` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | US | text/html | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | US | star | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | GB | text/html | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | GB | star | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | CA | text/html | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | CA | star | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | AU | text/html | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |
| /collections/matching-dresses | AU | star | `200` | `4` | `1` | `38` | `keep_excluded_until_product_vendor_source_clean` |

## Product Rows Requiring Cleanup Or Exclusion

The raw source URL is intentionally not stored in this packet. Product handles, IDs, source domain, and public source counts are enough for cleanup approval without committing source URLs.

| Route | Product handle | Product ID | Type | Source domain | Required action |
|---|---|---:|---|---|---|
| `/collections/matching-dresses` | `chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit` | `7108104061025` | `Sets` | `detail.1688.com` | `owner_approved_shopify_vendor_source_cleanup_or_keep_route_excluded` |
| `/collections/swimsuits` | `elegant-chocolate-brown-monokini-for-mother-daughter-duo-sleek-halter-neckline-with-playful-polka-dot-tie-sides` | `7108928766049` | `Swimwear` | `detail.1688.com` | `owner_approved_shopify_vendor_source_cleanup_or_keep_route_excluded` |
| `/collections/swimsuits` | `matching-mommy-and-me-two-piece-tankini-swimsuit-set` | `6949538529377` | `Swimwear` | `detail.1688.com` | `owner_approved_shopify_vendor_source_cleanup_or_keep_route_excluded` |

## Keyword Rows Still On Dirty Routes

These are not live upload rows. They remain local-only until rerouted or the product/vendor source cleanup is approved and read back clean.

| Market | Keyword | Threshold | Landing route | Current action |
|---|---|---|---|---|
| US | `mother daughter wedding guest dresses` | `GREEN` | `/collections/matching-dresses` | `use_for_us_shopping_query_and_future_search_packet` |
| US | `beige mother daughter dresses` | `YELLOW` | `/collections/matching-dresses` | `validate_active_products_before_search_packet` |
| US | `chiffon mother daughter dresses` | `YELLOW` | `/collections/matching-dresses` | `validate_active_products_before_search_packet` |
| US | `matching family swimsuits` | `GREEN` | `/collections/swimsuits` | `use_for_us_shopping_query_and_future_search_packet` |
| US | `mommy and me swimsuits` | `GREEN` | `/collections/swimsuits` | `use_for_us_shopping_query_and_future_search_packet` |
| US | `mother daughter bathing suits` | `GREEN` | `/collections/swimsuits` | `use_for_us_shopping_query_and_future_search_packet` |
| US | `mother daughter matching maxi dresses` | `GREEN` | `/collections/matching-dresses` | `use_for_us_shopping_query_and_future_search_packet` |
| US | `mother daughter holiday dresses` | `YELLOW` | `/collections/matching-dresses` | `validate_season_and_product_fit` |

## Exact Approval Packet If Owner Wants Cleanup

Approval phrase:

`Approve Shopify product/vendor source cleanup for the product handles in COLLECTION_SOURCE_CLEANUP_APPROVAL_PACKET.md. Do not change prices, status, publications, product scope, feeds, campaigns, budgets, bids, or conversion settings. After cleanup, run public source readbacks on /collections/swimsuits and /collections/matching-dresses for US/GB/CA/AU and keep rows excluded unless supplier hits are 0.`

Before-state readback:

- Save public source counts for both routes across `US`, `GB`, `CA`, and `AU` with `Accept: text/html` and `Accept: */*`.
- Confirm affected product handles are the same rows listed here.

After-state pass criteria:

- both routes return `200` for all four markets and both header variants,
- `detail.1688.com`, `1688.com`, `alibaba.com`, and `aliexpress.com` counts are `0`,
- URL-like analytics vendor or item brand hits are `0`,
- no local-inventory, warehouse, retail-store, or stale seasonal blocker is introduced.

## Guardrails

- This packet is not approval to edit Shopify Admin or product data.
- This packet is not Google Ads, Merchant, feed, title, product-group, bid, budget, status, or keyword-upload authority.
- Keep the current GB/CA/AU 36-row CPC validation packet on its clean canonical routes; do not move it back to these dirty routes.

## Files

- Route rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_route_rows.csv`
- Product rows: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_product_rows.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_approval_summary.json`
- Generator: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/build_collection_source_cleanup_approval.py`
