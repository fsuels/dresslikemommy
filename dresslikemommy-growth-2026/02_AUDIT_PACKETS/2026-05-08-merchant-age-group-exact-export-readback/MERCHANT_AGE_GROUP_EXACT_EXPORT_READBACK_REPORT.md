# Merchant Age Group Exact Export Readback

Generated: 2026-05-08 02:55 EDT

Scope: read-only Merchant Center account `124884876` product-issues export and local reconciliation. No Merchant upload, source sync/refresh/update click, product edit, Shopify product/publication edit, local inventory feed/claim, Google Ads/Pinterest/GA4/theme edit, budget/bid/status/product-scope/feed-label/product-group/conversion-goal change, checkout payment/order, spend, or enablement was made.

## Result

Status: `US_EN_PAID_COHORT_AGE_GROUP_CLEARED`.

The exact product-issues export downloaded successfully after switching from the cleared prioritized-fixes screen into `View all issues`.

Key reconciliation:

- Export file: `raw/product-issues-browser-export/product_issues_2026-05-08_01-58-05.csv`
- Export rows: `33,620`
- Paid cohort input: `780` item IDs from `paid_cohort_age_group_after_patch_rows.csv`
- Prior exact paid-cohort `US` / `en` / `United States` `Missing age group`: `623`
- Current exact paid-cohort `US` / `en` / `United States` `Missing age group`: `0`
- Delta: `-623`
- Sample item `shopify_US_7227254276193_41871113158753`: not in the current paid-cohort US/en age_group issue set

This closes `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT` for the original US/en paid-growth gate.

## Nuance Found

The all-issues export still contains paid-cohort item IDs with `Missing age group`, but only in a Spanish-language US context:

- `625` unique paid item IDs
- `1,250` rows total
- Context: feed label `US`, language `es`, country `United States`
- Traffic split: `625` `Shopping ads` rows and `625` `Free listings` rows

This is tracked separately as `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`. It does not reopen the solved US/en blocker, but it should be diagnosed read-only before Spanish-language US paid testing or broader catalog cleanup.

## Method

1. Opened a dedicated Merchant diagnostics CDP target.
2. Set Chrome download behavior to this packet's raw export folder.
3. Confirmed the prioritized diagnostics page now says `Great, all your prioritized fixes are resolved`.
4. Clicked only the read-only `View all issues` control to expose the full issues table.
5. Clicked only the table export control labelled `Download a file containing all the currently filtered product issues`.
6. Clicked the ready-download notification.
7. Reconciled the CSV against the `780` paid-cohort item IDs.
8. Ran a read-only sample source/label probe on one US/es-affected item.

## Evidence

- `merchant_exact_product_issues_export.py`
- `merchant_exact_product_issues_export_result.json`
- `raw/product-issues-browser-export/download_attempt_summary_priority.json`
- `raw/product-issues-browser-export/diagnostics_page_text_before_download_priority.txt`
- `raw/product-issues-browser-export/product_issues_2026-05-08_01-58-05.csv`
- `reconciliation/merchant-product-issues-summary-2026-05-08-0252.json`
- `reconciliation/merchant-product-issues-paid-us-en-missing-age-group-ids-2026-05-08-0252.txt`
- `reconciliation/merchant-product-issues-paid-us-en-missing-age-group-rows-2026-05-08-0252.csv`
- `reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`
- `raw/browser-source-readback-us-es-sample/merchant_exact_label_readback_refresh_check.json`

## Verification

- `python3 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/merchant_exact_product_issues_export.py`
- `python3 -m json.tool .../merchant_exact_product_issues_export_result.json`
- `python3 -m json.tool .../reconciliation/merchant-product-issues-summary-2026-05-08-0252.json`
- `python3 -m json.tool .../reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`

## Next

No Ads or Pinterest account writes were made because the current session does not contain either exact approval gate.

Next safe branches:

1. If the owner gives exact approval for paused non-US Google Search shells, create/import only paused non-US Search infrastructure and read it back.
2. If the owner gives exact approval for paused Pinterest US drafts, use the clean 342-row EN-US scope and 4 exclusions, keep every entity paused, and read it back.
3. Without either approval, continue read-only/local work: diagnose the US/es Merchant source path, run GB/CA/AU no-payment checkout QA, and prepare ROAS/creative/reporting packets.
