# Google Shopping Parent-Outfit Label-Precedence Repair Execution

UTC execution window: `2026-05-20T12:37Z` to `2026-05-20T14:09Z`

## Scope

Owner approved only the Google Shopping parent-outfit label-precedence repair:

- Keep all Shopping V2 campaigns paused.
- Keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.
- Read back the older Merchant label source state.
- Update only the smallest Merchant supplemental label source needed so approved parent-outfit rows win `custom_label_0=paid_eligible` and `custom_label_4=us_parent_outfit_ready_v20260520`.
- Preserve non-parent rows and known non-label attributes.
- Do not change Shopify titles, prices, handles, body, SEO, inventory, publications, campaigns, budgets, bids, statuses, product groups, conversions, or billing.

No Google Ads campaign/budget/bid/status/product-group/conversion/billing write occurred. No Shopify write occurred. No activation discussion is allowed from this result.

## Source State Readback

Data-source readback found four active US/en supplemental sources joined to `Shopify App API`:

- `10663204023` / `google_shopping_parent_outfit_merchant_supplemental_update_20260520.tsv`
- `10626787326` / `supplemental_feed_pilot.txt`
- `10651516446` / `upload_paid_cohort_age_group_only.txt`
- `10645919470` / `upload_variant_custom_labels_1_3.tsv`

The smallest source that owned the old `custom_label_0` and `custom_label_4` stack was `10626787326` / `supplemental_feed_pilot.txt`.

Before upload, source `10626787326` read:

- Last updated: `May 6, 2026 3:26 PM`
- Total updated products: `5,933`
- Matched products: `5,771`
- Attribute names: all recognized
- Source issue: `162` `Offer does not exist`

Evidence:

- `merchant_sources_cdp_readback_20260520T123918Z.json`
- `merchant_source_10626787326_before_label_precedence_repair_20260520T124157Z.json`

## File Built

Built a deterministic replacement file from the last repo-backed source `upload_matched_full_clean_labels_with_age_group.csv` and the approved parent-outfit spec `merchant_label_update_spec.csv`.

Output files:

- `google_shopping_parent_outfit_label_precedence_repair_10626787326.csv`
- `google_shopping_parent_outfit_label_precedence_repair_10626787326.txt`
- `google_shopping_parent_outfit_label_precedence_repair_10626787326_summary.json`
- Script: `build_google_shopping_parent_outfit_label_precedence_repair.py`

Local validation:

- Output rows: `6,121`
- Unique IDs: `6,121`
- Duplicate IDs: `0`
- Preserved non-parent base rows: `1,590`
- Changed existing approved parent rows: `4,343`
- Added approved parent rows not present in the old source file: `188`
- Preserved existing `age_group` values where source `10626787326` already had them.
- Did not synthesize `age_group` for the `188` newly added approved parent rows.

## Merchant Upload Readback

Uploaded `google_shopping_parent_outfit_label_precedence_repair_10626787326.txt` only to Merchant supplemental source `10626787326` / `supplemental_feed_pilot.txt`.

After upload, source `10626787326` read:

- Last updated: `May 20, 2026 8:45 AM`
- Total updated products: `6,121`
- Matched products: `5,284`
- Attribute names: all recognized
- Source issue: `837` `Offer does not exist`

The larger missing-offer count is from reprocessing the old source file against the current Shopify App API primary source. Non-parent rows were preserved as approved; no campaign activation followed.

Evidence:

- `merchant_source_10626787326_upload_click_readback_20260520T124533Z.json`
- `merchant_source_10626787326_after_label_precedence_repair_20260520T140920Z.json`

## Gate Readbacks

The strict parent-outfit gate improved from `145` ready rows before repair to `4,390` ready rows after propagation.

Latest formal gate:

- Evidence: `google_shopping_parent_outfit_merchant_feed_gate_20260520T141425Z.json`
- Gate passed: `false`
- Expected rows: `4,531`
- Ready rows: `4,390`
- Missing expected rows: `141`
- Label mismatches on ready rows: `0`
- Image mismatches on ready rows: `0`
- Missing live images: `0`
- Bad catchall units: `0`
- V2 campaigns paused: `true`
- Old test campaign paused: `true`

Final label diagnostic:

- Evidence: `google_ads_label_precedence_probe_final_after_wait_20260520T140538Z.json`
- Rows with `custom_label_3=parent_outfit`: `4,390`
- Rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `4,388`
- Expected rows not present as `parent_outfit`: `141`
- Expected parent-outfit rows still on old labels: `2`
- Note: the later `20260520T141425Z` gate shows ready-label rows caught up to `4,390`; the remaining gate blocker is `141` missing expected rows.

## Current Status

The label-precedence repair worked: the old label stack is no longer the material blocker in the latest gate. The strict gate still fails closed because the expected set still includes `141` rows that are not present as live `parent_outfit` offers.

All Shopping V2 campaigns remain paused. The old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` campaign remains paused. Catchalls remain excluded. Ready-row images are clean.

## Next Valid Action

Do not activate or discuss activation. The next safe action is read-only:

1. Rerun the gate after normal propagation to confirm ready rows stay at `4,390`.
2. If ready rows stay at `4,390`, treat the remaining blocker as the `141` missing offers and prepare a separate exact approval packet before any Shopify/Merchant primary-source repair.
3. Keep all Shopping campaigns paused until the full gate passes and the owner gives separate activation approval.
