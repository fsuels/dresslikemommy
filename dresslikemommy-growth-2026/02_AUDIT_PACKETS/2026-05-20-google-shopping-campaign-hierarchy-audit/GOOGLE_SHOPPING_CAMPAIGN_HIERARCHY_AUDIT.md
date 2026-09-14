# Google Shopping Campaign Hierarchy Audit

Generated: `2026-05-20`

Mode: read-only Google Ads API readback plus local collection/feed join and public Shopify product image readback. No Google Ads, Merchant, Shopify, Pinterest, feed, product, product-group, bid, budget, status, conversion, billing, or theme write occurred.

## Verdict

- The campaign is currently `PAUSED`; historical performance remains available for audit.
- The campaign does **not** mirror the storefront hierarchy as Mommy & Me / Family Matching / Daddy & Me with subgroups underneath. Its listing groups are built around `custom_label_4 = us_test_ready`, then peer `custom_label_2` values: `mommy_me`, `family_matching`, `daddy_me`, `pajamas`, `swimsuits`, plus an empty catch-all.
- The performance data is item/variant-level: multiple size/color variants from the same outfit received impressions and clicks. The saved parent rollup shows the outfit-level view the store needs.
- The smarter structure is parent/outfit-first reporting and bidding: keep Merchant variants for size/color availability, but group and label them by parent outfit and collection hierarchy, with the parent/collection image reused where appropriate.

## Current Campaign Readback

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` / `23802638621`
- Status: `PAUSED`; primary status reasons: `CAMPAIGN_PAUSED`, `BIDDING_STRATEGY_LEARNING`
- Channel: `SHOPPING`
- Bidding strategy type: `TARGET_SPEND` (Maximize clicks)
- Feed label: `US`
- Merchant ID: `124884876`
- Budget: `$20.00/day`
- Campaign inventory filter: `custom_label_4 = us_test_ready` and `custom_label_0 = paid_eligible`

### Product Groups

| Attribute index | Value | Listing type | Status | CPC |
|---|---|---:|---|---:|
| `UNSPECIFIED` | `(empty/everything else)` | `SUBDIVISION` | `PAUSED` | `` |
| `INDEX4` | `(empty/everything else)` | `UNIT` | `ENABLED` | `` |
| `INDEX4` | `us_test_ready` | `SUBDIVISION` | `PAUSED` | `$0.01` |
| `INDEX2` | `(empty/everything else)` | `UNIT` | `ENABLED` | `$0.20` |
| `INDEX2` | `daddy_me` | `UNIT` | `ENABLED` | `$0.20` |
| `INDEX2` | `family_matching` | `UNIT` | `ENABLED` | `$0.20` |
| `INDEX2` | `mommy_me` | `UNIT` | `ENABLED` | `$0.20` |
| `INDEX2` | `pajamas` | `UNIT` | `ENABLED` | `$0.20` |
| `INDEX2` | `swimsuits` | `UNIT` | `ENABLED` | `$0.20` |

### Last 7 Days Product Group Reconciliation

The owner-provided outside audit was checked against Google Ads API `product_group_view` with `segments.date DURING LAST_7_DAYS`; the key product-group numbers match.

| Product group | Impr. | Clicks | Cost | Conv. value |
|---|---:|---:|---:|---:|
| `All products` | 2,142 | 51 | $7.57 | $0.00 |
| `All products > us_test_ready` | 2,142 | 51 | $7.57 | $0.00 |
| `mommy_me` | 897 | 29 | $4.07 | $0.00 |
| `swimsuits` | 735 | 13 | $2.03 | $0.00 |
| `family_matching` | 265 | 5 | $0.70 | $0.00 |
| `daddy_me` | 212 | 4 | $0.77 | $0.00 |
| `pajamas` | 33 | 0 | $0.00 | $0.00 |
| `Everything else` under `All products` | 0 | 0 | $0.00 | $0.00 |
| `Everything else` under `us_test_ready` | 0 | 0 | $0.00 | $0.00 |

## Performance Rollup

- Date range: `2026-04-18` to `2026-05-20`
- Item/variant rows with impressions: `151`
- Parent outfits with impressions: `38`
- Item/variant rows with clicks: `48`
- Parent outfits with clicks: `18`
- Total impressions/clicks/cost/conversion value: `7264` / `158` / `$30.62` / `$0.00`
- Parents with multiple variants served: `23`; max variants served for one outfit: `18`
- Public URL/image follow-up found `5` historically served parent handles now return HTTP `404`; the largest is `mommy-and-me-matching-silver-asymmetrical-chiffon-dresses-with-strappy-backs` with `29` clicks, `921` impressions, and `$5.08` cost in the saved period. These must stay excluded from any future Shopping rebuild unless restored and reverified.

## Top Parent Outfits By Clicks

| Clicks | Impr. | Cost | Variants | Main lane | Subcategory | Handle |
|---:|---:|---:|---:|---|---|---|
| 29 | 921 | $5.08 | 4 | `` | `` | `mommy-and-me-matching-silver-asymmetrical-chiffon-dresses-with-strappy-backs` |
| 25 | 1365 | $4.12 | 13 | `` | `` | `elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer` |
| 24 | 1021 | $5.12 | 9 | `family_matching` | `dresses` | `elegant-floral-off-shoulder-mommy-and-me-dress-set-perfect-for-summer-outings` |
| 19 | 570 | $4.46 | 3 | `family_matching` | `dresses` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` |
| 17 | 757 | $3.19 | 8 | `` | `` | `matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set` |
| 10 | 144 | $1.98 | 7 | `mommy_and_me` | `swimwear` | `chic-leopard-print-one-piece-swimsuit-with-ruffle-accent-timeless-mother-daughter-beachwear` |
| 6 | 208 | $1.42 | 13 | `family_matching` | `pajamas` | `cute-matching-mom-and-daughter-cartoon-pajama-set-fun-and-cozy-sleepwear` |
| 6 | 186 | $0.97 | 2 | `mommy_and_me` | `swimwear` | `chic-pink-mermaid-scales-tankini-set-for-mother-and-daughter` |
| 5 | 130 | $1.01 | 4 | `mommy_and_me` | `sets` | `vibrant-rainbow-maxi-dress-set-for-mom-and-daughter-colorful-summer-matching-outfits` |
| 3 | 235 | $0.63 | 18 | `mommy_and_me` | `swimwear` | `chic-family-bonding-mother-daughter-matching-swimsuit-set-with-long-sleeved-cover-up` |
| 3 | 134 | $0.57 | 7 | `` | `` | `vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings` |
| 2 | 336 | $0.50 | 1 | `mommy_and_me` | `sets` | `matching-mommy-me-floral-strappy-back-maxi-dresses-summer-beach-outfit` |
| 2 | 201 | $0.28 | 14 | `` | `` | `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` |
| 2 | 118 | $0.31 | 2 | `mommy_and_me` | `sets` | `elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits` |
| 2 | 22 | $0.40 | 1 | `mommy_and_me` | `swimwear` | `chic-color-block-one-piece-swimsuit-for-mother-daughter-vibrant-sleek-beachwear` |

## Files

- `google_shopping_parent_rollup.csv`: outfit-level rollup with image links and hierarchy mapping.
- `google_shopping_variant_rows.csv`: exact Google Ads item/variant rows that received impressions.
- `google_shopping_live_api_readback.json`: raw structured readback and summaries.
- `google_shopping_products_thumbnail_audit.html`: visual thumbnail view for fast product/image inspection.

## Image Limitation

Google Ads API did not expose the rendered Shopping ad image URL in this readback. The thumbnail audit uses the current local grouped feed `image_link` and the public Shopify first product image, then flags whether those two image URLs match.
