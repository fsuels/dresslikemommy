# Pinterest Collection Intent Feed Labels Readback

Date: 2026-05-20

## What Changed Locally

`ops/scripts/generate_pinterest_feed_grouped.py` now emits explicit Shopify collection-intent labels into the Pinterest feed:

| Feed column | Value |
|---|---|
| `custom_label_0` | Market handle, e.g. `us` |
| `custom_label_1` | Existing product type, e.g. `Dresses`, `Family Matching`, `Swimwear` |
| `custom_label_2` | Primary paid lane: `mommy_and_me`, `family_matching`, `daddy_and_me`, or `unassigned` |
| `custom_label_3` | All collection-intent memberships, pipe-separated |
| `custom_label_4` | Label version: `collection_intent_v20260520` |

Priority resolves overlap once:

1. `daddy_and_me`
2. `family_matching`
3. `mommy_and_me`

## Source Collections

| Paid lane | Storefront collection source | Current public/feed-mapped count |
|---|---|---:|
| `mommy_and_me` | `/collections/mommy-and-me` | 99 |
| `family_matching` | `/collections/new-women-outfits` | 77 |
| `daddy_and_me` | `/collections/daddy-me-shirts` + `/collections/daddy-me-t-shirts` | 34 |

Daddy & Me cannot currently label `36` active/feed products because two products in the `daddy-me-t-shirts` collection are archived/unpublished:

| Handle | Status |
|---|---|
| `daddy-me-my-best-lady-my-best-man` | `ARCHIVED`, no `onlineStoreUrl` |
| `father-and-child-pilot-co-pilot-matching-t-shirt-set-perfect-for-daddy-me-outfits` | `ARCHIVED`, no `onlineStoreUrl` |

## Local Feed Readback

Generated local US feed:

- `feeds/pinterest_us_collection_intent.tsv`
- `feeds/pinterest_us_collection_intent.summary.json`
- `pinterest_collection_intent_feed_parent_readback.csv`

Readback:

| Check | Result |
|---|---:|
| Feed rows | 4,687 |
| Unique parent products | 223 |
| Missing `item_group_id` rows | 0 |
| Supplier/source host hits | 0 |
| `mommy_and_me` unique parents | 99 |
| `family_matching` unique parents | 77 |
| `daddy_and_me` unique parents | 34 |
| `unassigned` unique parents | 13 |

## Pinterest Group Filters To Use After Approved Upload/Reingestion

After explicit approval to upload the regenerated feed and after Pinterest source ingestion completes, create groups from label filters:

| Group name | Filter |
|---|---|
| `DLM_PIN_US_PAID_MOMMY_AND_ME_99_20260520` | `custom_label_0 = us` AND `custom_label_2 = mommy_and_me` AND `custom_label_4 = collection_intent_v20260520` |
| `DLM_PIN_US_PAID_FAMILY_MATCHING_77_20260520` | `custom_label_0 = us` AND `custom_label_2 = family_matching` AND `custom_label_4 = collection_intent_v20260520` |
| `DLM_PIN_US_PAID_DADDY_AND_ME_34_20260520` | `custom_label_0 = us` AND `custom_label_2 = daddy_and_me` AND `custom_label_4 = collection_intent_v20260520` |

Do not create a `daddy_and_me` group claiming `36` until the two archived products are restored and public/feed-mapped, or the owner explicitly chooses the broader Daddy & Me main collection, which currently reads `45`.

## Guardrails

No live feed upload, Pinterest source mutation, product group creation, campaign/ad group/ad restart, publish, enable, budget, bid, status, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM write occurred in this pass.

