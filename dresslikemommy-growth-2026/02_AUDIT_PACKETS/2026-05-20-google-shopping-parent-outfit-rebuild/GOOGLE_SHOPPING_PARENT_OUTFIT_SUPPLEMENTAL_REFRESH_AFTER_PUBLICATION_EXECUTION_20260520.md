# Google Shopping Parent-Outfit Supplemental Refresh After Publication

UTC execution window: `2026-05-20T10:45Z` to `2026-05-20T11:17Z`

## Scope

Owner direction in this thread: fix the stalled parent-outfit Shopping/Merchant gate while keeping all Shopping V2 campaigns paused and keeping `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused.

No campaign activation, spend enablement, budget, bid, status, product-group, conversion, billing, title, price, handle, body, SEO, inventory, or publication write occurred in this pass.

## Before State

Latest stalled gate before this repair: `google_shopping_parent_outfit_merchant_feed_gate_20260520T104330Z.json`.

- Gate passed: `false`
- Expected rows: `4,531`
- Google Ads ready-label rows: `145`
- Missing expected rows: `4,386`
- Label mismatches on ready rows: `0`
- Image mismatches on ready rows: `0`
- Bad catchall units: `0`
- V2 campaigns paused: `true`
- Old test campaign paused: `true`

Merchant source `10663204023` showed:

- Last updated: `May 20, 2026 3:04 AM`
- Total updated products: `4,531`
- Matched products: `4,390`
- Source issue: `141` affected rows with `Offer does not exist`

## Actions Taken

1. Re-opened the authenticated Merchant source detail page through the existing Chrome DevTools session.
2. Re-uploaded the already-approved TSV to the existing supplemental source `10663204023`.
3. Repaired an intermediate bad state where the first low-level upload attempt caused Merchant to show `0` updated / `0` matched rows.
4. Re-uploaded the full approved TSV again through the visible upload dialog and restored the source to the full file state.
5. Reran the read-only Google Ads/Merchant gate.
6. Ran two read-only label-precedence probes to identify why the gate stayed closed.

## After Source Readback

Evidence: `merchant_supplemental_source_after_repair_refresh_20260520T1117Z.json`

- Last updated: `May 20, 2026 7:09 AM`
- Total updated products: `4,531`
- Matched products: `4,390`
- Attribute names: all recognized
- Remaining source issue: `141` affected rows with `Offer does not exist`

## After Gate

Evidence: `google_shopping_parent_outfit_merchant_feed_gate_20260520T111119Z.json`

- Gate passed: `false`
- Expected rows: `4,531`
- Google Ads ready-label rows: `145`
- Missing expected rows: `4,386`
- Label mismatches on ready rows: `0`
- Image mismatches on ready rows: `0`
- Missing live images: `0`
- V2 campaigns paused: `true`
- Old test campaign paused: `true`
- Bad catchall units: `0`

## Root Cause Found

The source refresh is not enough because the existing label stack is still winning `custom_label_0` and `custom_label_4` on most older rows.

Evidence: `google_ads_label_precedence_probe_20260520T1116Z.json`

- Rows with `custom_label_3=parent_outfit`: `4,390`
- Rows with `custom_label_4=us_parent_outfit_ready_v20260520`: `145`
- Rows with `custom_label_0=paid_eligible` and `custom_label_3=parent_outfit`: `785`
- Rows still carrying old `custom_label_4=us_test_ready`: `754`

Merchant browser sample probe:

- Sample expected item `shopify_US_7108953604193_41496508432481` is present and has parent-outfit labels on `custom_label_1..3`.
- The same row still shows `custom_label_4=us_test_ready`, not `us_parent_outfit_ready_v20260520`.
- Evidence: `merchant_browser_label_probe_after_refresh_20260520T1113Z/merchant_exact_label_readback_refresh_check.json`

Shopify product-level `mm-google-shopping.custom_label_0..4` was checked as a possible cause, but it is not the main blocker:

- Parent products read: `210`
- Products with targeted Shopify product-level Google label metafields: `7`
- Target metafields found: `35`
- No Shopify deletion was applied.
- Evidence: `parent_outfit_shopify_google_label_metafield_repair_dry_run_summary_20260520T111633Z.json`

## Current Status

The paused Ads structures remain safe:

- All V2 Shopping campaigns remain paused.
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remains paused.
- Catchalls remain excluded.
- Images are clean on rows where the new ready label is live.

The remaining blocker is not propagation alone. It is label precedence from the existing Merchant/label source stack. The next repair must target the source that still owns `custom_label_0` and `custom_label_4` for the older paid/blocked rows, while preserving all paused campaign guardrails.
