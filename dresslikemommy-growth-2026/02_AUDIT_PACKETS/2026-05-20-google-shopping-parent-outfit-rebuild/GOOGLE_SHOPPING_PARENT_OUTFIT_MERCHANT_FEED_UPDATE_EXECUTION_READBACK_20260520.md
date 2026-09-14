# Google Shopping Parent-Outfit Merchant Supplemental Feed Execution Readback

UTC execution window: `2026-05-20T06:37Z` to `2026-05-20T07:06Z`

## Scope

Owner approval in this session covered the bounded feed gate only:

- Keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.
- Keep all V2 Shopping campaigns paused.
- Upload/update only the parent-outfit Merchant supplemental file.
- Do not enable spend, change campaign budgets/bids/statuses/product groups/conversions/billing, or activate Shopping.

## Before-State Gate

Command:

```bash
/tmp/dlm-google-ads-venv/bin/python dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/run_google_shopping_parent_outfit_merchant_feed_gate.py
```

Before-state timestamp: `20260520T063747Z`

- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected included variant rows: `4531`
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `0`
- V2 campaign status ok: `true`
- Old test campaign paused: `true`
- Bad catchall units: `0`

## File Uploaded

Merchant Center accepted tab-delimited uploads for this flow, so the approved CSV was converted to a TSV with the same columns and row values.

- CSV source: `google_shopping_parent_outfit_merchant_supplemental_update_20260520.csv`
- Uploaded TSV: `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv`
- TSV line count: `4532` including header
- Data rows: `4531`
- Unique offer IDs: `4531`
- Duplicate IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parents with multiple proposed image links: `0`
- Excluded rows not uploaded: `156`

The TSV was scanned for source/vendor URL patterns before upload; no source-host hits were found.

## Merchant Source Created

- Merchant account: `124884876`
- Supplemental source ID: `10663204023`
- Source title: `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv`
- Source type: `File (manual)`
- Content: `Product data`
- Source URL: `https://merchants.google.com/mc/products/sources/joindetails?a=124884876&joinFeedId=10663204023&tab=processing`
- Screenshot after create: `merchant_supplemental_upload_after_create_20260520.png`
- Screenshot after processing: `merchant_supplemental_upload_processed_20260520.png`

## Merchant Processing Readback

Merchant Center readback on the source detail page:

- Total updated products: `4,531`
- Matched products: `4,390`
- Attribute names: `All recognized`
- Supplemental product data file: `1 issue found`
- Issue: `Offer does not exist`
- Affected products: `141`

This means the supplemental label/image file itself was accepted, but not every intended offer ID currently exists in the selected primary Merchant source.

## Missing Offer Diagnosis

Google Ads Shopping-product readback for Merchant `124884876`, feed label `US`, found `10,841` live US product rows. Comparing the `4,531` supplemental IDs against that live surface found `139` IDs missing from the Google Ads Shopping-product readback.

Generated diagnostics:

- `google_shopping_parent_outfit_offer_ids_missing_from_ads_product_readback_20260520T070653Z.csv`
- `google_shopping_parent_outfit_missing_offer_id_parent_summary_20260520T070653Z.csv`
- `google_shopping_parent_outfit_missing_offer_shopify_readback_20260520T070653Z.json`

Missing rows by lane:

- Mommy & Me: `139`
- Family Matching: `0`
- Daddy & Me: `0`

Affected parent products:

| Parent product ID | Lane | Subgroup | Missing rows | Parent rows in spec | Entire parent missing |
|---|---|---:|---:|---:|---|
| `6718948147297` | `mommy_and_me` | `swimwear` | `40` | `40` | `true` |
| `7562834215009` | `mommy_and_me` | `sets` | `35` | `35` | `true` |
| `6718945034337` | `mommy_and_me` | `swimwear` | `20` | `20` | `true` |
| `6719764463713` | `mommy_and_me` | `swimwear` | `10` | `10` | `true` |
| `6719774720097` | `mommy_and_me` | `swimwear` | `10` | `10` | `true` |
| `6719792873569` | `mommy_and_me` | `swimwear` | `10` | `10` | `true` |
| `7535944368225` | `mommy_and_me` | `tops_shirts` | `8` | `16` | `false` |
| `7227254276193` | `mommy_and_me` | `dresses` | `6` | `8` | `false` |

Shopify Admin readback showed all 8 parent products are `ACTIVE` and online-store published. The blocker is therefore not that the products are archived in Shopify; it is that the relevant offer IDs are not fully present/matched in the current Google/Merchant primary product source.

## After-State Gate

Command:

```bash
/tmp/dlm-google-ads-venv/bin/python dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/run_google_shopping_parent_outfit_merchant_feed_gate.py
```

After-state timestamp: `20260520T070653Z`

- Gate passed: `false`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Expected included variant rows: `4531`
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `0`
- Missing expected rows: `4531`
- Label mismatches: `0`
- Image mismatches: `0`
- Missing live images: `0`
- V2 campaign status ok: `true`
- Old test campaign paused: `true`
- Included subgroup units: `12`
- Excluded catchall units: `24`
- Bad catchall units: `0`
- Merchant Content API scope available: `false`

## Conclusion

The approved supplemental feed update was executed and partially accepted by Merchant Center, but the activation gate remains closed. The feed file fixed the label/image contract for the matched product rows at the Merchant source level, but the live Google Ads Shopping-product readback has not yet exposed the new readiness label, and Merchant reported missing primary offers for `141` rows.

All V2 Shopping structures remain paused. The old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` campaign remains paused. No activation or spend change occurred.

## Next Required Fix

Do not activate or discuss activation yet. The next safe step is a separate primary-source repair/readback for the 8 affected Mommy & Me parent products so their Google/Merchant offers exist before the supplemental label/image gate is rerun.
