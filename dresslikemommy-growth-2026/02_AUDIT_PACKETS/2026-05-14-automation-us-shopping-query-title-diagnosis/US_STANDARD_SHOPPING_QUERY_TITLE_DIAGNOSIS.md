# US Standard Shopping Query And Title Diagnosis
Timestamp: 2026-05-14 12:43 EDT

Scope: repo-local analysis plus public storefront route readbacks. No Google Ads, Merchant, Shopify Admin, feed, product, product-group, bid, budget, status, or conversion write occurred.

## Decision

`US_STANDARD_SHOPPING_QUERY_TITLE_DIAGNOSIS_READY__NO_LIVE_WRITE`

The highest-priority authenticated CPC validation row remains gated by `AUTOMATION_CAPABILITY_MISMATCH`, so this pass moved the US Standard Shopping lane forward with a safe local diagnosis. The result is not a product/feed edit request yet; it is the exact read-only export and title-diagnostic scope needed before a title/feed approval packet.

## Current Shopping Evidence Used

- Current readback: `2026-05-14` Standard Shopping yesterday view for campaign `23802638621`.
- Yesterday: `17` impressions, `0` clicks, `$0.00` cost, `0.00` conversions/value.
- Visible yesterday search terms: `family pictures outfits` (`2` impr), `family same outfit` (`1` impr), `mommy and me wedding guest dresses` (`1` impr), all `0` clicks and `$0.00` cost.
- Product groups yesterday: `swimsuits` `8` impr, `daddy_me` `4`, `family_matching` `3`, `mommy_me` `2`, `pajamas` `0`; all `0` clicks/cost.
- Older all-time visible Shopping baseline showed real historical demand but no purchases: top rows included `mommy and me dresses` (`13` clicks / `482` impr / `$2.99` cost), `mommy and me outfits`, `matching sibling outfits`, `family matching outfits`, and `matching mom and me dresses`; all `0.00` conversions.

## Diagnosis

- Do not add negatives from yesterday: the three terms had no clicks, no cost, and are plausibly relevant to Dress Like Mommy.
- Do not change product-group bids/statuses from this data: product groups have impressions but no spend or conversion signal in yesterday's view.
- The sales-moving gap is product/feed-title clarity, not a live write: Shopping is matching broad family-photo and mommy/wedding intent, but we need a current item-level export to see which item IDs/titles received impressions and whether titles clearly contain buyer terms such as `mommy and me`, `mother daughter`, `matching family`, `family photo`, `wedding guest`, `swimsuit`, or `pajamas`.
- The local candidate CSV maps each visible query to paid-cohort handles so the next authenticated export can verify title and product-fit mismatches without guessing.

## Public Route Readback

| Route | Status | Supplier hits | URL-brand hits | Result |
|---|---:|---:|---:|---|
| `/collections/mommy-and-me` | `200` | `0` | `0` | `clean_public_route` |
| `/collections/family-matching` | `200` | `0` | `0` | `clean_public_route` |
| `/collections/pajamas` | `200` | `0` | `0` | `clean_public_route` |
| `/collections/family-swimsuits` | `200` | `0` | `0` | `clean_public_route` |
| `/collections/daddy-and-me` | `200` | `0` | `0` | `clean_public_route` |
| `/collections/vacation` | `ERROR` | `None` | `None` | `hold_or_verify_before_traffic` |
| `/collections/matching-dresses` | `200` | `4` | `0` | `hold_or_verify_before_traffic` |

## Files

- `us_shopping_query_title_summary.json`
- `us_shopping_query_title_candidates.csv`
- `us_shopping_route_checks.csv`

## Exact Next Action

Run an authenticated read-only Standard Shopping product-item export for campaign `23802638621` with columns: item ID, product title, product group/custom label, impressions, clicks, cost, search term/query where available, conversion value, and landing URL. Join it to `us_shopping_query_title_candidates.csv`. Only if the export proves a mismatch, prepare a narrow Shopify/Merchant title/feed approval packet; do not edit product data or product groups from this local diagnosis alone.

## Guardrails Preserved

- No Google Ads, Merchant, Shopify Admin, Pinterest, GA4/GTM, billing, bid, budget, status, feed, product, product-group, conversion, credential, or destructive filesystem write.
- No negative keyword action from zero-click zero-cost search terms.
- No Computer Use startup probing or permission repair.
