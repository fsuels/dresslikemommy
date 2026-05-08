# Merchant Feed Refresh Age Group Recheck - 2026-05-07

## Scope

Read-only recheck after the next Merchant Center / Google & YouTube feed refresh.

Expected success gate:

- Current paid-cohort US/en `Missing age group` should drop from `754` to `0` or materially decrease.
- Product/source timestamps should show refreshed Shopify App API item data.

## Live Merchant readback

- Merchant Center account: `124884876`
- Diagnostics URL: `https://merchants.google.com/mc/products/diagnostics?a=124884876&marketingMethod=16&priorityFixes=true`
- Previous diagnostics timestamp: `12:43 PM May 7, 2026`
- Fresh diagnostics timestamp: `1:15 PM May 7, 2026`
- Visible diagnostics still showed `Missing age group` for paid-cohort sample rows.

Evidence:

- `merchant-diagnostics-recheck-visible-2026-05-07.png`
- `merchant-product-issues-refresh-product_issues_2026-05-07_13-17-26.csv`

## Product issues export result

Fresh export:

- Rows: `37,033`
- Total `Missing age group` rows: `16,222`
- Unique item IDs with `Missing age group`: `4,588`

Current paid cohort comparison:

- Paid cohort size: `780`
- Paid cohort item IDs with `Missing age group` anywhere: `777`
- Paid cohort US/en/United States item IDs with `Missing age group`: `754`
- Paid cohort US/en traffic split:
  - `754` Free listings rows
  - `754` Shopping ads rows

Comparison to previous Merchant export:

- Previous paid cohort US/en `Missing age group`: `754`
- New paid cohort US/en `Missing age group`: `754`
- Delta: `0`
- Gate result: `NOT_CLEARED`

Evidence:

- `merchant-product-issues-paid-cohort-age-group-summary-after-refresh-2026-05-07.json`
- `merchant-product-issues-paid-us-en-missing-age-group-ids-after-refresh-2026-05-07.txt`
- `merchant-product-issues-paid-us-en-missing-age-group-rows-after-refresh-2026-05-07.csv`

## Shopify data readback

The live Shopify ProductVariant data remains correct.

Read-only post-refresh Shopify Admin dry-run result:

- Target paid variant rows: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason: `already_correct`

Evidence:

- `shopify-variant-age-group-post-refresh-readonly/summary.json`
- `shopify-variant-age-group-post-refresh-readonly/post_write_variant_age_group_readback.csv`

## API/source timestamp readback

Sample paid item:

- Item ID: `shopify_US_7227254276193_41871113158753`
- Product detail tab still shows no `Age group` attribute.
- Product detail tab shows:
  - `Last update`: `3 hrs ago`
  - `Source`: `API`

US primary source list:

- Source name: `Shopify App API`
- Feed label: `US`
- Source: `Merchant API`
- Products: `5,824`
- Status: `Needs update`
- Country/language: `United States` / `English`

Evidence:

- `merchant-product-detail-tab-sample-after-1315-refresh.png`
- `merchant-data-sources-scrolled-after-1315-refresh.png`

## Interpretation

Merchant diagnostics did refresh at `1:15 PM May 7, 2026`, but the paid-cohort age-group issue did not improve. The current evidence points to a diagnostics refresh over stale API item data, not a successful Shopify App API item refresh carrying the newly written variant-level `mm-google-shopping.age_group` values.

The Shopify-side data is still correct for all `780` current paid variants, so more blind Shopify data edits are not the next best move.

## Guardrails preserved

No changes were made to:

- Shopify products, variants, titles, descriptions, status, prices, inventory, tags, options, images, or publications.
- Merchant Center sources, supplemental feeds, uploads, or product data.
- Google Ads, Pinterest, GA4/GTM, pixels, campaigns, budgets, bids, product scope, product groups, feed labels, or conversion goals.

## Next best action

Inspect and repair the Google & YouTube / Merchant API source refresh path before making more product data changes.

Recommended next approval gate:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH REVIEW: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; ATTEMPT ONLY A SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`
