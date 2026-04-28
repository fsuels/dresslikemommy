# Upload Pack For Clean Subset Pass 2

Use these CSVs first:

1. `01_shopify_variant_export_with_cost_per_item.csv`
   - Fresh Shopify Admin read generated 2026-04-28.
   - 7,324 active variant rows.
   - `unit_cost` is present on every row.
   - Includes Shopify product/variant IDs, SKU, barcode/GTIN, price, compare-at price, inventory, product type, vendor, tags, collections, primary image URL, online-store URL, sales-channel publication names, and market availability proxy.

2. `05_merchant_center_current_product_rows_from_browser_rpc.csv`
   - Current Merchant Center product-list rows collected read-only from the already logged-in browser on 2026-04-28.
   - 7,324 rows written, one per active Shopify variant requested.
   - 5,969 rows have current Merchant Center matches in USD/en from the Shopify App API source.
   - 1,355 rows have no current browser-RPC product-list match; these align with variants not currently online-store available and must remain excluded/needs data.
   - Raw Merchant Center enum fields are included as `*_raw`; do not translate those into approved/limited/not approved unless you can prove the enum mapping from the UI.

3. `02_merchant_center_issue_diagnostics_equivalent_report.csv`
   - Best local Merchant Center equivalent currently available.
   - Source is a prior Merchant Center issue reconciliation export for current Shopify-style item IDs.
   - This is not a complete current Merchant Center issue diagnostics download; rows absent here must remain `NEEDS_DATA`, not approved.

4. `09_merchant_center_browser_rpc_normalized_evidence.csv`
   - Conservative normalized evidence built from file `05`.
   - The repo converter only treats the independently sampled raw combination as approved: `calculated_status_raw=4`, `aggregated_status_raw=2`, `main_image_thumbnail_status_raw={"2": 2}`, `availability_raw=0`, `language_code=en`, `price_currency=USD`, and `primary_source_name=Shopify App API`.
   - Raw `3` remains `Limited`; raw `1` remains `Not approved`; unmatched rows remain `NEEDS_DATA`.

Current official Merchant Center API export is blocked:
- `merchant_center_current_api_attempt_summary.json` shows Google returned `403 PERMISSION_DENIED` because the local `gcloud` token lacks Merchant Center/Content API scopes.
- `02b_merchant_center_current_api_attempt_header_only.csv` is included only to prove the current API attempt produced no evidence rows.
- `merchant_center_browser_rpc_export_summary.json` documents the read-only browser export that produced file `05`.
- `merchant_center_browser_rpc_evidence_summary.json` documents the normalized browser-RPC evidence that produced file `09`.

Extra local review outputs already generated:
- `03_current_clean_subset_master_review_only.csv`
- `04_current_supplemental_labels_review_only_do_not_upload.csv`
- `06_google_shopping_us_clean_subset_paid_eligible.csv`
- `07_google_shopping_fix_before_paid.csv`
- `08_google_ads_paused_standard_shopping_build_plan.md`
- `09_merchant_center_browser_rpc_normalized_evidence.csv`
- `clean_subset_summary.json`

Current result from the local generator:
- `paid_eligible=true`: 784 variant rows across 81 products.
- Launch decision: `READY_FOR_PAUSED_BUILDOUT`.
- This means the review-only paid-eligible subset exists for a paused Standard Shopping buildout; it does not approve a live upload, campaign creation, spend, or campaign enablement.
- Main remaining exclusions are missing GTIN/SKU, missing PDP verification, limited/not-approved Merchant Center status, no current browser-RPC match, image/feed issues, and weak initial collection filters.
- PDP evidence is current as of the latest live QA file: 1,335 rows passed PDP checks, 48 rows failed, and 5,941 rows still need PDP verification.

Hard rule for Pass 2:
- Do not mark rows `paid_eligible=true` from the Merchant Center equivalent alone.
- Do not mark rows `paid_eligible=true` from raw browser-RPC enum fields except through the conservative normalized evidence in file `09`.
- Treat missing Merchant Center status, destination, issue, image, price, availability, shipping, or return evidence as `NEEDS_DATA`.
- Do not upload supplemental labels or create campaigns from this packet without owner approval.
