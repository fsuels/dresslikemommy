# Shopping Read-Only Export Queue Report

Generated: `2026-05-15 05:24 EDT`

Mode: read-only Google Ads / Merchant Center evidence collection. No Google Ads, Merchant, Shopify, Pinterest, feed, product, product-scope, product-group, title, budget, bid, status, campaign, conversion, billing, credential, or theme write occurred.

## Queue Result

| Queue item | Result | Decision |
|---|---|---|
| Standard Shopping item export | Completed. Google Ads Products export for campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, date range `2026-04-18 to 2026-05-14`, produced `767` product rows. | US/en item-export lane is closed for this pass. No title/feed/product-group/bid/budget/status/negative write is justified from the export. |
| Merchant `US/es` source `10627981690` | Partially completed. Current Merchant issue export proves live `US/es` blockers still exist, while source/detail sample readback for `10627981690` did not reproduce Missing age_group on the sampled rows. Full source/all-products proof is still missing. | `US/es` is not Shopping-build-ready. Build a no-write issue classification/repair packet, then capture full current source/all-products evidence before any repair/build action. |
| CA/GB/AU Shopping eligibility | Issue-export readback completed, full eligibility proof still incomplete. Current Merchant issue export surfaced `0` issue rows for `CA/en`, `GB/en`, and `AU/en`, but the attempted Merchant country-filter text capture did not verifiably apply country chips and therefore cannot prove active approved product counts. | CA/GB/AU clear visible issue-export blockers only. Do not build Shopping campaigns until all-products/source export proves feed label, country, currency, active approved count, and paid-cohort intersection. |

## Standard Shopping Export

Evidence:

- Raw Google Ads Products export: `raw/google-ads-products/standard_shopping_products_2026-05-15.csv`
- Normalized join input: `standard_shopping_products_normalized_for_join.csv`
- Summary: `standard_shopping_products_export_summary.json`
- Join summary: `standard-shopping-join/us_shopping_auth_export_join_summary_2026-05-15.json`
- Join decisions: `standard-shopping-join/us_shopping_auth_export_joined_decisions_2026-05-15.csv`

Readback:

- Raw export rows: `767`
- Paid-cohort joined rows: `767`
- Missing paid-cohort rows: `0`
- Status counts: `698` Eligible, `52` Not eligible, `17` Eligible (limited)
- Rows with impressions: `112`
- Rows with clicks: `27`
- Total impressions: `3,484`
- Total clicks: `65`
- Total cost: `$14.17`
- Total conversion value: `$0.00`
- Join result: `85` public-clean matches, `30` held matches, `652` unmatched rows, `0` likely title/feed packet candidates

Decision:

- Do not change negatives, bids, budgets, statuses, product groups, product scope, feed attributes, titles, or products from this export.
- The sales-moving issue is now performance/conversion improvement from clean clicked products, not a proven title/feed mismatch.

## Merchant `US/es` Source `10627981690`

Evidence:

- Current issue-export analysis: `../2026-05-15-merchant-shopping-readonly-queue-readback/MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md`
- Source/detail sample readback: `merchant-us-es-source-10627981690-readback/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- Merchant API attempt: `merchant-api-diagnostics-current-paid-cohort/merchant_center_api_diagnostics_summary.json`
- Merchant diagnostics browser export attempt: `merchant-product-issues-export/merchant_exact_product_issues_export_result.json`
- Signed URL capture attempt: `merchant-product-issues-export/raw/product-issues-browser-export/signed_url_capture_summary.json`

Readback:

- Current Merchant issue export: `/Users/fsuels/Downloads/product_issues_2026-05-15_05-10-59.csv`, `266,318` rows, modified `2026-05-15T05:14:16`
- `US/es`: `1,453` issue rows, `354` unique items, `53` paid-cohort issue items
- `US/es` top issues: `708` over capacity rows, `432` Missing age group rows, `202` Missing color rows, `86` Missing gender rows, `12` Product page unavailable rows, `10` Missing size rows, `3` Missing product image rows
- Shopping ads issue rows: `724`
- Shopping ads disapproved rows: `359`
- Source/detail readback found two target `US` / `es` / source `10627981690` rows visible, with effective age_group values and no Missing age_group reproduced on those samples
- Merchant API and Content API read-only attempts returned `403 PERMISSION_DENIED` / insufficient OAuth scopes
- Direct diagnostics CSV download button produced ready-to-download UI but the current packet did not capture a CSV through Chrome; a signed `storage.googleapis.com` download path was blocked by `ERR_BLOCKED_BY_CLIENT`

Decision:

- Treat the current issue export as the stronger current blocker signal for `US/es`; treat the sample-clear source/detail readback as useful but not closing evidence.
- The issue export lacks `source_id`, and the source/detail readback is not a full all-products/source export.
- Do not repair Merchant attributes, upload supplemental feeds, refresh sources, edit Shopify products, alter feed labels, product scope, product groups, bids, budgets, statuses, or create Shopping builds from this mixed evidence alone.

## CA/GB/AU Shopping Eligibility

Evidence:

- Current issue-export analysis: `../2026-05-15-merchant-shopping-readonly-queue-readback/MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md`
- Country filter text attempt: `merchant-ca-gb-au-shopping-eligibility/merchant_ca_gb_au_country_diagnostics_summary.json`

Readback:

- Current issue export found `0` rows for `CA/en`, `GB/en`, and `AU/en`
- This clears visible issue-export rows only; it does not prove active approved product counts, product sources, feed labels, country/currency compatibility, or paid-cohort intersection
- The country-filter text attempt found filter controls and country options, but `chip_country_visible` stayed `false` and the saved page text still showed `Countries: All`; those text captures are global diagnostics, not country-specific eligibility proof

Decision:

- CA/GB/AU English Shopping remains a read-only feasibility lane, not a build-ready lane.
- Next proof must be a current all-products/source export for CA/GB/AU proving feed label, country, currency, active approved count, and paid-cohort intersection.

## Guardrails Preserved

- No Google Ads upload, apply, import, negative, keyword, bid, budget, status, product-group, product-scope, campaign, conversion, billing, or spend write.
- No Merchant upload, source sync, source refresh, product edit, feed edit, capacity request, or source settings change.
- No Shopify Admin product/vendor/source metadata, theme live sync, price, discount, policy, inventory, or publication write.
- No Pinterest, GA4/GTM, credential, mailbox mutation, or destructive filesystem action.

## Next Action

1. Build a no-write `US/es` issue classification/repair approval packet from the current issue rows, separating age_group, color, gender, page, image, size, and Shopping capacity blockers.
2. Capture a full current Merchant all-products/source export for source `10627981690` plus CA/GB/AU English eligibility, with source, feed label, country, currency, active approved count, and paid-cohort intersection.
3. Use clean Standard Shopping clicked PDPs for landing/conversion analysis, not feed/title edits, unless a later exact item-level readback proves a narrow mismatch.
