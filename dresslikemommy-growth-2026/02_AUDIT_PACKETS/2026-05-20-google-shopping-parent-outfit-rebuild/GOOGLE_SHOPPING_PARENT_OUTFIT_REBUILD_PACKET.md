# Google Shopping Parent-Outfit Rebuild Packet

Generated: `2026-05-20`

Mode: local/no-write rebuild packet. No Google Ads, Merchant, Shopify, Pinterest, feed, product, product-group, budget, bid, status, conversion, billing, or theme write occurred.

## Decision

- Keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.
- Do not reuse its mixed product-group tree.
- Rebuild around parent outfits: three top-level Shopping lanes, subgroups underneath, shared `item_group_id`, parent hero images, no catchall leakage, and no 404/archived products.

## Proposed Paused Structure

| Campaign | Parent lane | Parent outfits | Status if imported | Inventory scope |
|---|---|---:|---|---|
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `mommy_and_me` | 99 | `PAUSED` | `custom_label_0=paid_eligible AND custom_label_1=mommy_and_me AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `family_matching` | 77 | `PAUSED` | `custom_label_0=paid_eligible AND custom_label_1=family_matching AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2` | `daddy_and_me` | 34 | `PAUSED` | `custom_label_0=paid_eligible AND custom_label_1=daddy_and_me AND custom_label_4=us_parent_outfit_ready_v20260520` |

## Subgroup Ad Groups

| Campaign | Ad group | Parent outfits | Variant rows | Scope |
|---|---|---:|---:|---|
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Dresses` | 28 | 395 | `custom_label_1=mommy_and_me AND custom_label_2=dresses AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Swimwear` | 35 | 574 | `custom_label_1=mommy_and_me AND custom_label_2=swimwear AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Pajamas` | 22 | 252 | `custom_label_1=mommy_and_me AND custom_label_2=pajamas AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Tops & Shirts` | 7 | 90 | `custom_label_1=mommy_and_me AND custom_label_2=tops_shirts AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Sets` | 2 | 47 | `custom_label_1=mommy_and_me AND custom_label_2=sets AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `Mommy & Me - Sweaters & Outerwear` | 5 | 61 | `custom_label_1=mommy_and_me AND custom_label_2=sweaters_outerwear AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `Family Matching - Dresses` | 5 | 116 | `custom_label_1=family_matching AND custom_label_2=dresses AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `Family Matching - Tops & Shirts` | 64 | 2276 | `custom_label_1=family_matching AND custom_label_2=tops_shirts AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `Family Matching - Sets` | 1 | 23 | `custom_label_1=family_matching AND custom_label_2=sets AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `Family Matching - Sweaters & Outerwear` | 7 | 175 | `custom_label_1=family_matching AND custom_label_2=sweaters_outerwear AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2` | `Daddy & Me - Tops & Shirts` | 28 | 390 | `custom_label_1=daddy_and_me AND custom_label_2=tops_shirts AND custom_label_4=us_parent_outfit_ready_v20260520` |
| `DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2` | `Daddy & Me - Sets` | 6 | 132 | `custom_label_1=daddy_and_me AND custom_label_2=sets AND custom_label_4=us_parent_outfit_ready_v20260520` |

## Validation Summary

- Included parent outfits: `210`.
- Included variant rows: `4531`.
- Parent lane counts: `{"daddy_and_me": 34, "family_matching": 77, "mommy_and_me": 99}`.
- Subcategory counts: `{"dresses": 33, "pajamas": 22, "sets": 9, "sweaters_outerwear": 12, "swimwear": 35, "tops_shirts": 99}`.
- Public URL hard failures (`404`) inside proposed included scope: `0`.
- Public URL non-200 probe warnings inside proposed included scope: `210`; these are not hard exclusions because the current-active feed is the active-product source and automated storefront probes can return `403`.
- Missing `item_group_id` inside proposed included scope: `0`.
- Missing hero image inside proposed included scope: `0`.
- Excluded current-feed parents: `13`.
- Historic 404 Shopping parents held out: `5`.
- Known archived Daddy & Me targets held out: `2`.

Daddy & Me is `34` active/feed-mapped parent outfits right now, not `36`; two Daddy & Me t-shirt products are archived/unpublished and must stay out until restored and reverified.

## Label Contract

| Field | Proposed use |
|---|---|
| `item_group_id` | Shopify parent product ID, shared by every size/color variant of the same outfit |
| `image_link` | Parent/collection hero image for every variant in the same outfit |
| `custom_label_0` | `paid_eligible` inclusion gate |
| `custom_label_1` | parent collection lane: `mommy_and_me`, `family_matching`, `daddy_and_me` |
| `custom_label_2` | subgroup: `dresses`, `swimwear`, `pajamas`, `tops_shirts`, `sets`, `sweaters_outerwear` |
| `custom_label_3` | `parent_outfit` |
| `custom_label_4` | `us_parent_outfit_ready_v20260520` readiness/version gate |

## Approval Boundary

This packet is not a live approval to upload Merchant labels or create Google Ads campaigns. Creating even paused Shopping campaigns, changing product groups, changing feed labels, or uploading feed changes is a live external write and needs fresh action-time approval plus before/after readback.

Exact approval phrase for the next live step, if accepted later:

> Approve the Google Shopping parent-outfit paused rebuild only: keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused, create/import only paused V2 Shopping structures from the packet, do not enable spend, do not change budgets/bids/statuses beyond paused draft requirements, do not include catchalls, and read back counts/images before any activation discussion.

## Files

- `shopping_parent_outfit_manifest.csv`: parent outfit inclusion/exclusion manifest.
- `merchant_label_update_spec.csv`: per-variant feed label/image/item_group_id specification.
- `shopping_campaign_blueprint.csv`: three paused top-level Shopping lanes.
- `shopping_ad_group_blueprint.csv`: subgroup ad groups under each lane.
- `shopping_product_group_tree.csv`: no-catchall product group tree spec.
- `excluded_products_do_not_advertise.csv`: 404/archived/current-feed excluded products.
- `google_shopping_parent_outfit_rebuild_summary.json`: machine-readable summary.
