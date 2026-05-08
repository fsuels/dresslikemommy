# Merchant Source Refresh Action - 2026-05-07

## Scope

Owner approved the exact Google & YouTube / Merchant source-refresh action gate.

Allowed action:

- Read back Shopify Google & YouTube publication state.
- Read back Merchant US `Shopify App API` source details and sample item timestamps.
- Attempt one safe official app/source resync if clearly available.
- If no official resync was available, run one single-product Google & YouTube unpublish/republish probe on product `7227254276193`.

Blocked actions preserved:

- No product data edits.
- No feed label changes.
- No supplemental uploads.
- No ads/campaign/budget/bid/product-scope/product-group/pixel/conversion-goal changes.

## Pre-Action Readbacks

Shopify publication sample dry-run:

- Product: `7227254276193`
- Product status: `ACTIVE`
- Online Store published: `true`
- Google & YouTube published: `true`
- Storefront URL present: `true`
- Positive prices: `true`
- Dry-run preconditions: all passed

Shopify age_group dry-run:

- Target paid variants: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason: `already_correct`

Merchant browser RPC sample:

- Item ID: `shopify_US_7227254276193_41871113158753`
- Source: `Shopify App API`
- Source ID: `10627623003`
- Feed label/language: `US` / `en`
- Last updated UTC: `2026-05-07T14:14:02+00:00`
- Labels intact:
  - `custom_label_0=paid_eligible`
  - `custom_label_1=margin_medium`
  - `custom_label_2=swimsuits`
  - `custom_label_3=aov_medium`
  - `custom_label_4=us_test_ready`

Source UI review:

- Merchant data-source page visible text showed `Shopify App API` rows with `Needs update`, but no clear safe one-click source resync/refresh action was exposed in the trusted read-only capture.
- Shopify Google app URL redirected to Shopify login in this CDP profile, so no official app resync button could be safely verified there.

## Action Taken

Because no clearly verified official resync/refresh control was available, ran the approved fallback:

`python3 ops/scripts/google_publication_republish_probe.py --handle mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-merchant-source-refresh-action/executed-google-publication-sample-toggle --execute --pause-seconds 5`

Execution result:

- Unpublish from Google & YouTube: `success`
- Republish to Google & YouTube: `success`
- Final Google & YouTube publication state: `true`
- Final Online Store publication state: `true`

## Post-Action Readbacks

Final Shopify publication readback:

- Product remained `ACTIVE`.
- Online Store published: `true`
- Google & YouTube published: `true`
- Storefront URL present.
- Positive prices still true.

Final Shopify sample variant readback:

- Variant `41871113158753` still has `mm-google-shopping.age_group=toddler`.
- Age group metafield updated at `2026-05-07T17:12:10Z`.
- Product Google & YouTube published: `true`.

Post-toggle Merchant browser RPC sample after about 30 seconds:

- Item ID: `shopify_US_7227254276193_41871113158753`
- Source remained `Shopify App API`.
- Source ID remained `10627623003`.
- Feed label/language remained `US` / `en`.
- Last updated UTC remained `2026-05-07T14:14:02+00:00`.
- Paid labels remained intact.

Merchant diagnostics UI recheck:

- Diagnostics page URL: `https://merchants.google.com/mc/products/diagnostics?a=124884876&marketingMethod=16&priorityFixes=true`
- Diagnostics timestamp visible: `Last updated at 2:01 PM May 7, 2026`
- `Missing age group` remained visible on the sample paid product row.
- `Missing local inventory data` also remained visible; this is separate from the age_group source-refresh action.

## Interpretation

The approved one-product Google & YouTube publication toggle completed and restored final publication state correctly.

The Merchant sample row did not update within the short post-toggle readback window. This does not prove the toggle failed; Merchant / Google & YouTube propagation may take longer than the immediate readback window. For now, treat the paid-cohort age_group Merchant clear as still pending.

Do not repeat the same toggle immediately. The next useful step is a later Merchant sample timestamp and product-issues export recheck after the source has had time to process.

## Evidence

- `pre-action-google-publication-sample-dry-run/summary.json`
- `pre-action-merchant-browser-rpc-sample/merchant_exact_label_readback_refresh_check.json`
- `pre-action-shopify-variant-age-group-readonly/summary.json`
- `pre-action-source-ui-readbacks/summary.json`
- `executed-google-publication-sample-toggle/summary.json`
- `post-toggle-google-publication-final-readback/summary.json`
- `post-toggle-shopify-sample-readback/sample_variant_age_group_source_readback.json`
- `post-toggle-shopify-variant-age-group-readonly/summary.json`
- `post-toggle-merchant-browser-rpc-sample-30s/merchant_exact_label_readback_refresh_check.json`
- `post-toggle-merchant-ui-recheck/summary.json`
- `post-toggle-merchant-ui-recheck/diagnostics.txt`
- `post-toggle-merchant-ui-recheck/diagnostics.png`

## Guardrails Preserved

No changes were made to:

- Shopify product title, body, status, prices, inventory, tags, options, images, metafields, or feed labels.
- Merchant Center sources, source settings, feed labels, supplemental feeds, uploads, or product data.
- Google Ads, Pinterest, GA4/GTM, pixels, campaigns, budgets, bids, statuses, product scope, product groups, or conversion goals.
- Standard Shopping, PMax, Brand Search, Remarketing, or nonbrand Search.

Only the approved temporary Google & YouTube publication state for one product was toggled and restored.

## Next Best Action

Wait for Google & YouTube / Merchant API processing, then recheck:

1. Merchant browser RPC sample timestamp for `shopify_US_7227254276193_41871113158753`.
2. Merchant diagnostics/product-issues export for current paid-cohort US/en `Missing age group`.
3. Final Shopify product publication state for product `7227254276193`.

Expected success:

- The sample Merchant US/en source timestamp advances beyond `2026-05-07T17:12:10Z`, and/or
- paid-cohort US/en `Missing age group` drops materially from the prior `754`.
