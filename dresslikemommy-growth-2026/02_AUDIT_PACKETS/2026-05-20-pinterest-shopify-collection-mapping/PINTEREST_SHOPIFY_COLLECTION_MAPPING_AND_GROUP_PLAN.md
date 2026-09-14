# Pinterest Shopify Collection Mapping And Group Plan

Date: 2026-05-20

## Executive Decision

Do not attach or restart the paused Pinterest campaign from the earlier `22/73/6` label groups. Those groups were based on current feed category labels, not on the Shopify storefront collections the owner wants to advertise.

The clean paid structure should be collection-led:

| Group type | Purpose | Count |
|---|---:|---:|
| Mirror: Mommy & Me all | Storefront collection readback for `/collections/mommy-and-me` | 99 |
| Mirror: Family Matching all | Storefront category hub readback for `/collections/new-women-outfits` | 77 |
| Mirror: Daddy & Me all | Public Daddy shirt/t-shirt subcategory products that map to the feed | 34 |
| Primary paid: Mommy & Me | Storefront collection-intent lane | 99 |
| Primary paid: Family Matching | Storefront collection-intent lane | 77 |
| Primary paid: Daddy & Me | Public Daddy shirt/t-shirt subcategory products that map to the feed | 34 |

## Count Reconciliation

Owner-stated target:

| Lane | Owner count | Verified current count | Status |
|---|---:|---:|---|
| Mommy & Me | 99 | 99 | Matches |
| Family Matching | 77 | 77 from `/collections/new-women-outfits` | Matches the live category hub; broader alias `/collections/matching-outfits` is 78 |
| Daddy & Me | 36 | 34 public/feed-mapped shirt/t-shirt products | Mismatch: two products behind the 36 count are archived/unpublished |

The safest launch count is `99/77/34` until the two archived Daddy & Me t-shirt products are restored and public/feed-mapped. The broader Daddy & Me main collection reads `45` because it includes trunks/swimwear.

## Overlap Rules

Priority order for paid traffic:

1. Daddy & Me gets Daddy-specific shirt/t-shirt products first.
2. Family Matching gets the current `77`-product storefront category hub.
3. Mommy & Me gets the current `99`-product storefront collection.

Verified overlaps:

| Overlap | Count | Paid-lane handling |
|---|---:|---|
| Mommy & Me and Family Matching | 0 | No conflict under the corrected `77`-product Family hub |
| Family Matching and Daddy public subcategory | 0 | No conflict under the corrected `77`-product Family hub |
| Mommy & Me and Daddy public subcategory | 0 | No conflict |

## Clean Pinterest Group Names

Create these only after the count mismatch is accepted or fixed:

| Recommended Pinterest group | Selector source | Count |
|---|---|---:|
| `DLM_PIN_US_COLLECTION_MOMMY_AND_ME_ALL_99_20260520` | `item_group_id` list from `mirror_mommy_and_me_all_99` | 99 |
| `DLM_PIN_US_COLLECTION_FAMILY_MATCHING_ALL_77_20260520` | `custom_label_2 = family_matching` after approved feed upload/reingestion | 77 |
| `DLM_PIN_US_COLLECTION_DADDY_AND_ME_ALL_34_20260520` | `custom_label_2 = daddy_and_me` after approved feed upload/reingestion | 34 |
| `DLM_PIN_US_PAID_MOMMY_AND_ME_PRIMARY_99_20260520` | `custom_label_2 = mommy_and_me` after approved feed upload/reingestion | 99 |
| `DLM_PIN_US_PAID_FAMILY_MATCHING_PRIMARY_77_20260520` | `custom_label_2 = family_matching` after approved feed upload/reingestion | 77 |
| `DLM_PIN_US_PAID_DADDY_AND_ME_PRIMARY_34_20260520` | `item_group_id` list from `primary_daddy_and_me_subcat_available_34` | 34 |

## Selector Files

- `pinterest_shopify_collection_mapping.csv` maps every included product handle to Shopify collection membership, current feed label, feed row count, overlap count, and recommended primary paid lane.
- `pinterest_shopify_collection_mapping_summary.json` stores the count reconciliation.
- `feeds/pinterest_us_collection_intent.tsv` is the local regenerated feed with `custom_label_2` carrying the primary paid lane and `custom_label_3` carrying collection memberships.
- `pinterest_collection_intent_feed_parent_readback.csv` stores parent-level readback from the regenerated feed labels.

## Launch Gate

No campaign restart should occur until:

1. The owner accepts `99/77/34`, restores the two archived Daddy & Me t-shirt products so `36` becomes public/feed-mapped, or explicitly chooses the broader `45`-product Daddy main collection.
2. The new Pinterest group selector counts match the intended group counts before save.
3. The paused campaign settings are re-read: catalog sales, optimization, bid mode, max CPC, daily budget, selected source, selected product groups, and paused/active status.
4. Fresh owner approval is given for that exact current screen.
