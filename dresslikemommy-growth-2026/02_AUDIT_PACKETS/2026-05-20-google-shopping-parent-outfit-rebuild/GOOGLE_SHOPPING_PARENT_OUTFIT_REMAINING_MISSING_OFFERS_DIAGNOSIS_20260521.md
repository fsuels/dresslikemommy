# Google Shopping Parent-Outfit Remaining Missing Offers Diagnosis

UTC readback window: `2026-05-21T08:59Z` to `2026-05-21T09:00Z`

## Why

The `20260521T085030Z` read-only gate stayed failed closed at `4,390 / 4,531` ready rows. This diagnosis checks whether the remaining `141` rows are still missing in Shopify, merely unlabeled in Google Ads, or absent from the Google Ads Shopping-product surface.

## Shopify Readback

Evidence:

- `google_shopping_remaining_missing_offers_shopify_readback_20260521T085916Z.json`
- `google_shopping_remaining_missing_offer_variant_readback_20260521T085916Z.csv`

Findings:

- Missing expected rows checked: `141`
- Parent products checked: `8`
- All `8` products found in Shopify Admin.
- All `8` products are `ACTIVE`.
- All `8` products are published to `Google & YouTube`.
- All `8` products are published to `Online Store`.
- All `141` missing expected variant IDs still exist in Shopify.

Conclusion: the remaining blocker is not missing Shopify products, missing Shopify variants, or missing product-level Google & YouTube publication.

## Google Ads Shopping-Product Presence Probe

Evidence:

- `google_ads_missing_offer_item_id_presence_probe_20260521T090020Z.json`
- `google_ads_missing_offer_item_id_presence_found_20260521T090020Z.csv`
- `google_ads_missing_offer_item_id_presence_absent_20260521T090020Z.csv`

Findings:

- Expected missing item IDs checked: `141`
- Rows found in Google Ads Shopping-product surface: `72` rows / `70` unique item IDs
- Rows absent from Google Ads Shopping-product surface: `71`
- Found-row status: all `NOT_ELIGIBLE`
- Found-row availability: all `IN_STOCK`
- Found-row labels: all blank `custom_label_0..4`

Found but unlabeled rows by parent:

| Parent product ID | Handle | Rows found in Google Ads with blank labels |
|---|---|---:|
| `6718948147297` | `matching-mom-child-one-shoulder-swimsuit` | `40` |
| `6719764463713` | `matching-mommy-and-me-hollow-out-bikini` | `10` |
| `6719792873569` | `matching-mommy-me-sunflower-print-swimsuit` | `10` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `2` |
| `7535944368225` | `powder-blue-mommy-and-me-set` | `10` |

Absent rows by parent:

| Parent product ID | Handle | Rows absent from Google Ads |
|---|---|---:|
| `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `20` |
| `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `10` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `6` |
| `7562834215009` | `white-crochet-mommy-and-me-set` | `35` |

## Smallest Repair Now Indicated

With fresh exact approval only:

1. Refresh the already-approved parent-outfit supplemental sources so the `70` unique now-visible blank-label item IDs can receive the approved ready labels and parent images.
2. For the `71` item IDs absent from Google Ads, repair only the Google & YouTube / Merchant primary-source presence for the four affected parent products listed above.
3. Stop if the only available path is a broad account sync, broad source reset, product recreation, campaign/feed rewrite, or any title/price/handle/body/SEO/inventory/budget/bid/status/product-group/conversion/billing change.
4. Wait for processing and rerun the counts/images/no-catchall gate.

No external write was performed in this diagnosis.
