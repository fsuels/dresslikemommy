# Merchant PT URL Readback Monitor

Generated: 2026-05-08 01:12 EDT

Lane: Merchant read-only monitoring sidecar for `2026-05-08-paid-growth-pt-presentment-url-readback`.

Session/tab label used: `DLM-MERCHANT-US-SourceRefresh-PT-URL-20260508`.

## Status

Status: `PARKED_ON_USER_STOP_EXPORT_BLOCKED`.

The lane was stopped at the owner's request. I stopped the running CDP helper process and did not take any further browser/account actions.

## Current Evidence

- Merchant account visible: `Dresslikemommy` / `124884876`.
- Fresh read-only sample source readback completed at `2026-05-08T01:06:10`.
- Sample item: `shopify_US_7227254276193_41871113158753`.
- Sample US/en source remains `10627623003` / `Shopify App API`.
- Sample US/en source timestamp remains `2026-05-07T14:14:02+00:00`.
- Campaign filter labels still visible on sample: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`.
- Full expected sample labels still visible: `paid_eligible`, `margin_medium`, `swimsuits`, `aov_medium`, `us_test_ready`.

Visible diagnostics text captured from Merchant Center:

- Visible page timestamp: `Last updated at 1:02 AM May 8, 2026`.
- Visible first-page range: `1 - 5 of 10,985`.
- `Missing age group` present on the visible diagnostics table.
- `Missing local inventory data` present on the visible diagnostics table.
- Sample title `Mommy and Me Maxi Dresses - Yellow | Dress Like Mommy Child 2 Years / Yellow` present and visibly still includes `Missing age group`.

Exact paid-cohort `Missing age group` count:

- Fresh exact CSV count was not obtained before the lane was stopped.
- Last completed exact export from the prior anchor remains the latest exact count available in evidence: `623` paid-cohort US/en United States unique item IDs, with the sample item still affected.

## Export / API Blockers

- Merchant diagnostics download button was clicked read-only, but the CSV did not materialize in the lane download directory before stop.
- Merchant UI showed a `Ready to download` notification in visible text, but the helper did not complete a usable CSV export before the owner stopped the lane.
- Merchant API and Content API product-issues paths remain blocked by local OAuth scope:
  - Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.
  - Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.

## Dropshipping / Local Inventory Note

`Missing local inventory data` is present, but it is not a product-data fix target for Dress Like Mommy. DLM is dropshipping, has no physical store, and does not hold owned physical inventory. Do not create local inventory feeds, local stock claims, warehouse claims, store pickup claims, or guaranteed on-hand inventory claims to clear that diagnostic.

## Guardrails Preserved

No Merchant upload, source sync/refresh click, source edit, Google & YouTube publication toggle, Shopify product-data edit, local inventory feed/claim, Google Ads edit, feed/product-scope/feed-label/product-group change, budget/bid/status/conversion-goal change, Pinterest edit, shipping-rate/Market change, payment, or order action was made.

## Artifacts

- `browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `diagnostics-visible-summary.json`
- `product-issues-browser-export/diagnostics_page_text_before_download.txt`
- `product-issues-browser-export/download_attempt_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_evidence.csv`
- `api-product-issues/merchant_center_api_diagnostics_raw.jsonl`
- `merchant_cdp_readonly_monitor.py`

## Next Safe Action

Leave this lane parked unless the parent asks for a later fresh export retry. If retried, use the same read-only Merchant tab/session separation and do not click source refresh/sync, upload, fix, save, product toggle, or any local-inventory action.
