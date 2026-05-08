# Merchant Read-Only Source / Product-Issues Recheck

Generated: 2026-05-07 23:19 EDT / 2026-05-08 UTC

Lane: Merchant read-only source/product-issues recheck.

Scope: read-only only. No Merchant upload, source sync/refresh, source edit, product data edit, Google & YouTube toggle, Shopify product-data mutation, ads/campaign/budget/bid/status/conversion-goal change, product-scope change, product-group change, feed-label change, Pinterest change, payment, or order action was made.

## Outcome

Status: `PARTIAL_IMPROVEMENT_NOT_CLEARED`.

The current product-issues export shows Merchant has improved from the prior paid-cohort US/en `Missing age group` count of `754` to `623`, a decrease of `131` unique paid-cohort US/en item IDs. The gate is still not clear because `623` paid-cohort US/en items remain affected, including the sample item `shopify_US_7227254276193_41871113158753`.

The sample US/en Merchant row is still on source `10627623003` / `Shopify App API` with last updated timestamp `2026-05-07T14:14:02+00:00`, which is still older than the documented Shopify variant `age_group` repair timestamp `2026-05-07T17:12:10Z`.

## Fresh Readbacks

### Source timestamp sample

Command:

```bash
python3 ops/scripts/check_merchant_center_clean_labels_live.py --account 124884876 --cdp-port 9222 --sample-offer-id shopify_US_7227254276193_41871113158753 --expected-labels-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/upload_matched_full_clean_labels_with_age_group.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-checkout-merchant-pinterest-readbacks/lanes/merchant/browser-source-readback
```

Result:

- Gate status: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Full label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`
- US/en source: `10627623003` / `Shopify App API`
- US/en source timestamp: `2026-05-07T14:14:02+00:00`
- Paid labels still visible: `paid_eligible`, `margin_medium`, `swimsuits`, `aov_medium`, `us_test_ready`
- Observed sample label mismatches: `0`

### Product-issues browser export

Method: clicked only the Merchant diagnostics table download button labelled `Download a file containing all the currently filtered product issues`, with CDP download behavior pointed into this lane packet.

Raw export:

- `product-issues-browser-export/product_issues_2026-05-07_23-18-05.csv`
- Export rows: `34,710`
- Diagnostics page visible timestamp: `Last updated at 11:18 PM May 7, 2026`

Current issue counts from the export:

- `Missing age group`: `14,766` rows; `4,270` unique item IDs
- `Missing local inventory data`: `10,994` rows
- `Missing color`: `5,664` rows
- `Missing gender`: `2,174` rows
- `Product page unavailable`: `651` rows
- Other smaller rows are in `merchant-product-issues-summary-2026-05-07-2318.json`

Paid-cohort reconciliation:

- Paid cohort size: `780`
- Paid-cohort US/en/United States unique item IDs with `Missing age group`: `623`
- Traffic split: `623` Free listings rows and `623` Shopping ads rows
- Delta vs prior known `754`: `-131`
- Sample item still affected: `true`

Dropshipping note: `Missing local inventory data` is not a product-data fix target for Dress Like Mommy. DLM has no physical store and no owned physical inventory, so do not create local inventory feeds, local stock claims, warehouse claims, store pickup claims, or guaranteed on-hand inventory claims to clear that Merchant diagnostic.

### API product-issues path

Command:

```bash
python3 ops/scripts/export_merchant_center_api_diagnostics.py --merchant-id 124884876 --input-eligibility dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-checkout-merchant-pinterest-readbacks/lanes/merchant/api-product-issues
```

Result:

- Token source: `gcloud auth print-access-token`
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Current variant rows scanned: `780`
- API evidence rows: `0`

Interpretation: exact current product-issues counts were available through the read-only browser CSV export, but the official API path remains blocked by local OAuth scope.

## Raw Artifacts

- `browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `api-product-issues/merchant_center_api_diagnostics_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_evidence.csv`
- `api-product-issues/merchant_center_api_diagnostics_raw.jsonl`
- `diagnostics-browser-readback/diagnostics_page_summary.json`
- `diagnostics-browser-readback/diagnostics_page_text.txt`
- `product-issues-browser-export/download_attempt_summary.json`
- `product-issues-browser-export/product_issues_2026-05-07_23-18-05.csv`
- `merchant-product-issues-summary-2026-05-07-2318.json`
- `merchant-product-issues-paid-us-en-missing-age-group-ids-2026-05-07-2318.txt`
- `merchant-product-issues-paid-us-en-missing-age-group-rows-2026-05-07-2318.csv`

## Guardrails Preserved

No changes were made to Merchant Center sources, feed files, uploads, source refresh/sync state, Shopify product data, Google & YouTube publication state, Google Ads, Pinterest, GA4/GTM, pixels, budgets, bids, campaign status, conversion goals, product scope, product groups, feed labels, shipping rates, Markets, checkout, payments, or orders.

## Next Safe Action

Continue read-only monitoring until the paid-cohort US/en `Missing age group` count reaches `0` or materially stops improving. Do not repeat the Google & YouTube toggle, edit Shopify product data, upload feeds, or click a source refresh/sync control without fresh exact owner approval and just-in-time readbacks.

If the count remains stuck and a safe official source refresh/resync control is available, request explicit approval before any click:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH REVIEW: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; ATTEMPT ONLY A SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`
