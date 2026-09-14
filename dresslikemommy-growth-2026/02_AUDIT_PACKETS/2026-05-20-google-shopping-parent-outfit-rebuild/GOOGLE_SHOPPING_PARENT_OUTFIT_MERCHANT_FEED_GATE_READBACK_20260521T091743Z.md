# Google Shopping Parent-Outfit Merchant / Feed Gate Readback

UTC timestamp: `20260521T091743Z`

## Verdict

- Gate passed: `False`
- Reason: `FAIL_CLOSED__MERCHANT_FEED_LABEL_IMAGE_READBACK_NOT_LIVE`
- Activation discussion allowed: `False`

## Ads Structure Safety Readback

- Campaign status ok: `True`
- Old test campaign paused: `True`
- Listing groups: `60`
- Included subgroup units: `12`
- Excluded catchall units: `24`
- Bad catchall units: `0`

## Live Product / Image Readback

- Expected included variant rows: `4531`
- Expected parent counts by lane: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 99}`
- Live rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4390`
- Live rows matching expected item IDs: `4390`
- Missing expected rows: `141`
- Unexpected ready-label rows: `0`
- Live parent counts by lane from spec join: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 92}`
- Label mismatches: `0`
- Image mismatches: `0`
- Missing live images: `0`

## Item Group Proof

- Google Ads `shopping_product` item_group_id field available: `False`
- Merchant Content API scope available: `False`
- Live item_group_id proven: `False`
- Note: Google Ads shopping_product exposes labels and product_image_uri but not item_group_id; Merchant Content API scope is required for strict live item_group_id proof.

## Existing Old-Label Context

- Rows with old `paid_eligible` + `us_test_ready`: `114`
- Old-label rows matching the new expected item IDs: `0`

## Conclusion

The paused V2 campaign shells remain safe, but the Merchant/feed product gate fails closed because the new parent-outfit readiness label is not live on Shopping products. Do not activate or discuss activation until a separate feed/Merchant update and after-state readback proves the expected parent counts, hero images, and item grouping live.

## Output Files

- JSON: `google_shopping_parent_outfit_merchant_feed_gate_20260521T091743Z.json`
- Ready products CSV: `google_shopping_parent_outfit_ready_products_20260521T091743Z.csv`
- Old-label context CSV: `google_shopping_parent_outfit_old_us_test_ready_products_20260521T091743Z.csv`
