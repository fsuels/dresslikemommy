# Google Shopping Parent-Outfit Merchant Feed Update Approval Packet

Generated: `2026-05-20`

Mode: approval packet only. No Google Ads, Merchant Center, Shopify, feed upload, product data, budget, bid, status, conversion, billing, or activation write occurred while preparing this packet.

## Why This Exists

The paused V2 Shopping structures exist and are safe, but the Merchant/feed gate failed closed:

- V2 campaigns stayed paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` stayed paused.
- Listing groups: `60`.
- Included subgroup units: `12`.
- Excluded catchall units: `24`.
- Bad catchall units: `0`.
- Expected included variant rows: `4531`.
- Live Shopping products with `custom_label_4=us_parent_outfit_ready_v20260520`: `0`.

Conclusion: the Ads shell is ready and paused, but the product/feed label and hero-image contract is not live. Activation is still blocked.

## Smallest Proposed Write

Use a Merchant supplemental feed update first, not Shopify Admin product edits.

Reason: the paused V2 campaigns only need the Merchant offer attributes to match the parent-outfit contract. A supplemental feed is the narrowest reversible surface because it targets specific Merchant offer IDs and does not alter storefront product identity, titles, prices, variants, publication state, or Shopify product media.

Upload-ready local file:

- `google_shopping_parent_outfit_merchant_supplemental_update_20260520.csv`

Columns:

- `id`
- `item_group_id`
- `image_link`
- `custom_label_0`
- `custom_label_1`
- `custom_label_2`
- `custom_label_3`
- `custom_label_4`

Scope:

- Rows to update: `4531` included Merchant offer IDs.
- Unique offer IDs: `4531`.
- Parent outfits represented: `210`.
- Parent counts: Mommy & Me `99`, Family Matching `77`, Daddy & Me `34`.
- Excluded rows not uploaded: `156`.
- Missing `item_group_id`: `0`.
- Missing `image_link`: `0`.
- Parents with multiple proposed image links: `0`.

If Merchant Center cannot accept `item_group_id` or `image_link` through a supplemental source, stop. Do not fall back to Shopify Admin product edits without a fresh, narrower approval packet.

## Attribute Contract

| Attribute | Value source |
|---|---|
| `id` | Current Merchant offer ID from `merchant_label_update_spec.csv` |
| `item_group_id` | Shopify parent product ID, shared by all variants of one outfit |
| `image_link` | Parent/collection hero image for every variant in the same outfit |
| `custom_label_0` | `paid_eligible` |
| `custom_label_1` | Parent lane: `mommy_and_me`, `family_matching`, `daddy_and_me` |
| `custom_label_2` | Subgroup: `dresses`, `swimwear`, `pajamas`, `tops_shirts`, `sets`, `sweaters_outerwear` |
| `custom_label_3` | `parent_outfit` |
| `custom_label_4` | `us_parent_outfit_ready_v20260520` |

## Explicit Non-Scope

Do not:

- Enable, unpause, or otherwise activate any V2 Shopping campaign.
- Edit `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
- Change Ads budgets, bids, product groups, listing groups, conversion goals, or billing.
- Change Shopify titles, prices, handles, variants, publication state, product media, or storefront content.
- Include the `156` excluded rows.
- Include historic hard-404 parents or archived/unpublished products.
- Change Pinterest, GA4, GTM, Search, PMax, or any non-Shopping surface.

## Before-State Readback Required

Immediately before any approved upload:

1. Confirm all V2 Shopping campaigns are still `PAUSED` / `PAUSED`.
2. Confirm old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` is still `PAUSED` / `PAUSED`.
3. Run `run_google_shopping_parent_outfit_merchant_feed_gate.py` and save the output.
4. Confirm current live ready-label rows are still known and record the count.
5. Confirm the upload file still validates:
   - `4531` rows.
   - `4531` unique IDs.
   - `210` parent outfits.
   - `0` missing `item_group_id`.
   - `0` missing `image_link`.
   - `0` duplicate IDs.
   - `0` excluded rows included.

## Approved Action If Phrase Is Given

If and only if the owner gives the exact approval phrase below, perform the smallest Merchant supplemental feed action:

1. In Merchant Center account `124884876`, create or update a supplemental source for the US feed using `google_shopping_parent_outfit_merchant_supplemental_update_20260520.csv`.
2. Use it only to supplement the `4531` offer IDs in the CSV.
3. Trigger or wait for feed processing.
4. Do not change campaign statuses, budgets, bids, product groups, conversion goals, or billing.
5. Do not edit Shopify product data.
6. Stop on login, CAPTCHA, permission, policy, upload schema error, account switcher, destructive prompt, or if Merchant shows a broader overwrite than the CSV scope.

## After-State Readback Required

After Merchant/feed processing completes:

1. Rerun `run_google_shopping_parent_outfit_merchant_feed_gate.py`.
2. Required pass values:
   - V2 campaigns paused.
   - Old test campaign paused.
   - Listing groups `60`.
   - Included subgroup units `12`.
   - Excluded catchall units `24`.
   - Bad catchall units `0`.
   - Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4531`.
   - Matching expected item IDs: `4531`.
   - Missing expected rows: `0`.
   - Unexpected ready-label rows: `0`.
   - Parent counts: Mommy & Me `99`, Family Matching `77`, Daddy & Me `34`.
   - Label mismatches: `0`.
   - Image mismatches: `0`.
   - Missing live images: `0`.
3. Obtain a Merchant/feed-capable export or UI/API readback proving `item_group_id` is live for the `210` parent groups.
4. Do not discuss activation unless every readback above passes.

## Exact Approval Phrase

> I approve the Google Shopping parent-outfit Merchant supplemental feed update only: keep all V2 Shopping campaigns paused and keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused; upload or update only google_shopping_parent_outfit_merchant_supplemental_update_20260520.csv for the 4,531 included offer IDs; set only item_group_id, image_link, and custom_label_0 through custom_label_4 from the packet; do not edit Shopify products, do not include excluded/404/archived products, do not enable spend, do not change Ads budgets/bids/statuses/product groups/conversions/billing, and after feed processing rerun the Merchant/feed gate before any activation discussion.

## Evidence Files

- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260520T062057Z.md`
- `google_shopping_parent_outfit_merchant_feed_gate_20260520T062057Z.json`
- `merchant_label_update_spec.csv`
- `google_shopping_parent_outfit_merchant_supplemental_update_20260520.csv`
- `google_shopping_parent_outfit_merchant_supplemental_update_20260520_summary.json`
- `run_google_shopping_parent_outfit_merchant_feed_gate.py`
