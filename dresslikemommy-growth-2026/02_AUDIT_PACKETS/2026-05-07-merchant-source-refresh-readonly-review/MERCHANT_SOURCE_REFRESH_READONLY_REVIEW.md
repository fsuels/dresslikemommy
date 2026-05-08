# Merchant Source Refresh Read-Only Review - 2026-05-07

## Scope

Continue the paid-growth sprint toward clean paid catalog readiness without repeating already-completed age_group fixes.

This pass was read-only for external systems. No sync, upload, source edit, product edit, publication toggle, ad edit, campaign edit, budget edit, bid edit, product-scope edit, product-group edit, feed-label edit, pixel edit, or conversion-goal edit was performed.

## Duplicate-Fix Check

Prior anchors showed:

- `AGENT_CONTINUITY_ANCHOR: 2026-05-06-merchant-paid-cohort-age-group-upload-accepted-diagnostic-not-cleared`
- `AGENT_CONTINUITY_ANCHOR: 2026-05-07-merchant-paid-cohort-shopify-variant-age-group-repair`
- `AGENT_CONTINUITY_ANCHOR: 2026-05-07-merchant-feed-refresh-age-group-recheck-not-cleared`
- `AGENT_CONTINUITY_ANCHOR: 2026-05-07-paid-growth-ai-army-continuation-local-claim-cleanup`

Result: the Shopify ProductVariant `mm-google-shopping.age_group` repair was already completed and verified. This pass verified current state instead of redoing Shopify product data edits.

## Readbacks

Shopify paid-cohort age_group dry-run:

- Target paid variant rows: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason: `already_correct`

Sample Shopify source row:

- Merchant item: `shopify_US_7227254276193_41871113158753`
- Shopify variant: `gid://shopify/ProductVariant/41871113158753`
- Product: `gid://shopify/Product/7227254276193`
- Product status: `ACTIVE`
- Online Store published: `true`
- Google & YouTube published: `true`
- Variant `mm-google-shopping.age_group`: `toddler`
- Variant age_group metafield updated at: `2026-05-07T17:12:10Z`

Merchant browser RPC sample:

- Sample US/en source: `Shopify App API`
- Source ID: `10627623003`
- Feed label: `US`
- Last updated UTC: `2026-05-07T14:14:02+00:00`
- `custom_label_0`: `paid_eligible`
- `custom_label_1`: `margin_medium`
- `custom_label_2`: `swimsuits`
- `custom_label_3`: `aov_medium`
- `custom_label_4`: `us_test_ready`
- Full label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`

Merchant data sources page:

- Page: `Data sources - Merchant Center`
- Account: `124884876`
- US primary source visible as:
  - `Shopify App API`
  - Feed label: `US`
  - Source: `Merchant API`
  - Products: `5,824`
  - Status: `Needs update`
  - Country/language: `United States` / `English`

Official Google API attempt:

- Token source: `gcloud auth print-access-token`
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.

Dry-run publication probe:

- Sample product is active, Online Store published, Google & YouTube published, has a storefront URL, and has positive prices.
- Execution was `false`; no unpublish/republish mutation ran.

## Interpretation

The current blocker is not missing Shopify age_group data. Shopify shows the paid-cohort variant values as correct, and the sample variant age_group was updated at `2026-05-07T17:12:10Z`.

The Merchant sample US/en row still shows a Shopify App API timestamp of `2026-05-07T14:14:02Z`, older than the Shopify variant age_group write. The US data source also still shows `Needs update`. This points to Google & YouTube / Merchant API source propagation or app-source refresh, not another blind Shopify data repair.

The official Google API path is not currently usable from the local `gcloud` token because it lacks Merchant/Content scopes. Browser/CDP readbacks remain the available live read-only path.

## Evidence

- `api-diagnostics-current-paid-cohort/merchant_center_api_diagnostics_summary.json`
- `merchant-browser-rpc-sample/merchant_exact_label_readback_refresh_check.json`
- `merchant-data-sources-page/merchant_data_sources_page_visible_text.json`
- `merchant-data-sources-page/merchant_data_sources_page_visible_text.txt`
- `merchant-data-sources-page/merchant_data_sources_scroll_probe.json`
- `merchant-data-sources-page/merchant_data_sources_page.png`
- `merchant-data-sources-page/merchant_data_sources_us_visible_step_0.png`
- `shopify-source-sample-readback/sample_variant_age_group_source_readback.json`
- `shopify-variant-age-group-readonly/summary.json`
- `google-publication-sample-dry-run/summary.json`

## Guardrails Preserved

No changes were made to:

- Shopify product titles, descriptions, status, publications, prices, inventory, tags, options, images, or live product data.
- Merchant Center sources, uploads, supplemental feeds, product data, source refresh/sync actions, or issue states.
- Google Ads, Pinterest, GA4/GTM, pixels, campaigns, budgets, bids, product scope, product groups, feed labels, or conversion goals.
- Standard Shopping, PMax, Brand Search, Remarketing, or nonbrand Search.

## Next Best Action

The closest path to the North Star is an owner-approved source-refresh action, not more age_group data edits.

Recommended approval gate:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH ACTION: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; THEN ATTEMPT ONLY ONE SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE OR ONE SINGLE-PRODUCT GOOGLE & YOUTUBE UNPUBLISH/REPUBLISH PROBE ON PRODUCT 7227254276193 IF NO OFFICIAL RESYNC EXISTS; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`
