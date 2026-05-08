# Merchant Currency Readback Monitor

Generated: 2026-05-07 23:59 EDT / 2026-05-08 UTC

Lane: Merchant monitor subagent for the paid-growth currency/presentment readback packet.

Scope: read-only Merchant / Google & YouTube source and product-issues monitor. No Merchant uploads, no source refresh/sync clicks, no Google & YouTube publication toggle, no Shopify product data edits, no local inventory feeds/claims, no Ads/feed/product-scope/feed-label/product-group changes, no payments, and no orders.

## Outcome

Status: `NOT_CLEARED_NO_NEW_IMPROVEMENT`.

Fresh browser export and reconciliation show the paid-cohort US/en `Missing age group` count is still `623` unique item IDs, unchanged from the previous `2026-05-07 23:18 EDT` browser export. The sample item `shopify_US_7227254276193_41871113158753` is still affected.

The sample source readback still shows source `10627623003` / `Shopify App API` with US/en timestamp `2026-05-07T14:14:02+00:00`, still older than the documented Shopify variant `age_group` repair.

Merchant API and Content API product diagnostics remain blocked by local OAuth scope: both returned `403 PERMISSION_DENIED` / insufficient authentication scopes.

## Fresh Readbacks

### Browser source sample

Command:

```bash
python3 ops/scripts/check_merchant_center_clean_labels_live.py --account 124884876 --cdp-port 9222 --sample-offer-id shopify_US_7227254276193_41871113158753 --expected-labels-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/upload_matched_full_clean_labels_with_age_group.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/browser-source-readback
```

Result:

- Gate status: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Full label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`
- US/en source: `10627623003` / `Shopify App API`
- US/en source timestamp: `2026-05-07T14:14:02+00:00`
- Visible labels: `paid_eligible`, `margin_medium`, `swimsuits`, `aov_medium`, `us_test_ready`
- Sample label mismatches: `0`

### Product-issues browser export

Method: CDP read-only click on the Merchant diagnostics table button labelled `Download a file containing all the currently filtered product issues`.

Raw export:

- `product-issues-browser-export/product_issues_2026-05-07_23-57-24.csv`
- Export rows: `34,716`
- Diagnostics page visible timestamp: `Last updated at 11:18 PM May 7, 2026`

Current issue counts from the export:

- `Missing age group`: `14,766` rows; `4,270` unique item IDs
- `Missing local inventory data`: `10,994` rows; `5,673` unique item IDs
- `Missing color`: `5,664` rows
- `Missing gender`: `2,174` rows
- `Product page unavailable`: `657` rows

Paid-cohort reconciliation:

- Paid cohort size: `780`
- Paid-cohort US/en/United States unique item IDs with `Missing age group`: `623`
- Traffic split: `623` Free listings rows and `623` Shopping ads rows
- Delta vs previous `623`: `0`
- Sample item still affected: `true`
- Paid-cohort US/en unique item IDs with `Missing local inventory data`: `771`

Dropshipping note: `Missing local inventory data` is not a product-data fix target for Dress Like Mommy. DLM has no physical store and no owned physical inventory, so do not create local inventory feeds, local stock claims, warehouse claims, store pickup claims, or guaranteed on-hand inventory claims to clear that Merchant diagnostic.

### Data sources visible text

Read-only CDP text capture from Merchant Center data sources confirmed the page is accessible and still contains `Shopify App API` and `Needs update`. The visible first-page table was paginated to non-US sources, so this capture is not a complete US-source detail readback. The targeted sample source readback above remains the stronger US/en evidence.

### API product-issues path

Command:

```bash
python3 ops/scripts/export_merchant_center_api_diagnostics.py --merchant-id 124884876 --input-eligibility dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/merchant/api-product-issues
```

Result:

- Token source: `gcloud auth print-access-token`
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Current variant rows scanned: `780`
- API evidence rows: `0`

## Raw Artifacts

- `browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `api-product-issues/merchant_center_api_diagnostics_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_evidence.csv`
- `api-product-issues/merchant_center_api_diagnostics_raw.jsonl`
- `product-issues-browser-export/download_attempt_summary.json`
- `product-issues-browser-export/diagnostics_page_text_before_download.txt`
- `product-issues-browser-export/product_issues_2026-05-07_23-57-24.csv`
- `merchant-product-issues-summary-2026-05-07-2357.json`
- `merchant-product-issues-paid-us-en-missing-age-group-ids-2026-05-07-2357.txt`
- `merchant-product-issues-paid-us-en-missing-age-group-rows-2026-05-07-2357.csv`
- `page-readbacks/page_readback_summary.json`
- `page-readbacks/diagnostics_visible_text.txt`
- `page-readbacks/data_sources_visible_text.txt`

## Commands / Tools Run

- Read repo guardrails from `AGENTS.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and latest Merchant/paid-growth entries in `ops/AGENT_WORKLOG.md`.
- Ran `python3 ops/scripts/export_merchant_center_api_diagnostics.py ...` for read-only API diagnostics.
- Ran `python3 ops/scripts/check_merchant_center_clean_labels_live.py ...` for read-only browser/CDP sample source timestamp and labels.
- Queried `http://127.0.0.1:9222/json/list` to confirm existing Merchant Center tabs.
- Used a one-off CDP read-only script to set download behavior, capture diagnostics visible text, and click only the product-issues download button.
- Parsed the browser export against the 780-row paid cohort.
- Captured Merchant diagnostics and data-source visible text through CDP.

## Guardrails Preserved

No Merchant upload, feed upload, source sync/refresh click, source edit, Google & YouTube product publication toggle, Shopify product data edit, local inventory feed/claim, Google Ads edit, feed/product-scope/feed-label/product-group change, budget/bid/status/conversion-goal change, Pinterest edit, shipping-rate/Market change, payment, or order action was made.

## Residual Risks

- Merchant API and Content API product-issues paths remain unavailable from this shell because the local Google OAuth token lacks required scopes.
- Browser export is read-only and current, but it depends on the logged-in Merchant UI and visible diagnostic export behavior.
- The data sources page text capture was paginated and did not show the US source row in the visible first-page table.
- Merchant processing may still update later; this readback shows no movement between `23:18` and `23:57` EDT.

## Next Safe Action

Continue read-only monitoring later until paid-cohort US/en `Missing age group` reaches `0` or clearly stalls over a longer processing window. Do not repeat the Google & YouTube toggle, edit Shopify products, upload feeds, click source refresh/sync, or create local-inventory artifacts without fresh exact owner approval and just-in-time readbacks.
