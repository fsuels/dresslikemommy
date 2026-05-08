# Merchant Source Recheck Subagent Report - 2026-05-07

Generated: 2026-05-07 14:13 EDT

## Scope

Read-only/local Merchant and Shopify source-refresh diagnostics after the approved single-product Google & YouTube publication toggle.

Blocked actions preserved:

- No Merchant source refresh/sync click.
- No publication toggle repeat.
- No Shopify product data edit.
- No feed upload or supplemental upload.
- No Ads, Pinterest, campaign, budget, bid, status, product-scope, product-group, feed-label, pixel, or conversion-goal change.

## Latest Readbacks

Merchant browser RPC sample:

- Output: `merchant-browser-rpc-sample-latest/merchant_exact_label_readback_refresh_check.json`
- Generated: `2026-05-07T14:12:57`
- Sample item: `shopify_US_7227254276193_41871113158753`
- US/en source: `Shopify App API`
- Source ID: `10627623003`
- Latest observed source timestamp: `2026-05-07T14:14:02+00:00`
- Labels remained intact:
  - `custom_label_0=paid_eligible`
  - `custom_label_1=margin_medium`
  - `custom_label_2=swimsuits`
  - `custom_label_3=aov_medium`
  - `custom_label_4=us_test_ready`
- Gate status: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Full expected label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`

Shopify paid-cohort variant age_group dry-run:

- Output: `shopify-variant-age-group-readonly-latest/summary.json`
- Execution: `false`
- Target paid variant rows: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason counts: `already_correct=780`

Google & YouTube sample publication dry-run:

- Output: `google-publication-sample-dry-run-latest/summary.json`
- Product: `7227254276193`
- Handle: `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter`
- Product status: `ACTIVE`
- Google & YouTube published: `true`
- Online Store published: `true`
- Storefront URL present: `true`
- All prices positive: `true`
- Execution: `false`

Google API diagnostics attempt:

- Output: `api-diagnostics-current-paid-cohort-latest/merchant_center_api_diagnostics_summary.json`
- Mode: read-only Google API diagnostics
- Current variant rows scanned: `780`
- Merchant evidence rows: `0`
- Result: blocked by token scopes, not by product data.
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes.

## Interpretation

The sample Merchant US/en item still has the old `Shopify App API` source timestamp `2026-05-07T14:14:02+00:00`, which is older than the Shopify-side `mm-google-shopping.age_group` repair timestamp from the prior action packet (`2026-05-07T17:12:10Z`).

The Shopify-side paid cohort remains fixed: all `780` current paid variants are already correct and no age_group updates are planned.

The approved sample toggle appears restored correctly: the sample product remains active, published to Google & YouTube, published to Online Store, and price-valid in the dry-run readback.

The exact current blocker is Merchant / Google & YouTube source propagation or source refresh, plus lack of Google API scopes for a full programmatic product-status export. More Shopify data edits and an immediate repeated toggle are not evidence-supported.

## Commands Run

```bash
python3 ops/scripts/check_merchant_center_clean_labels_live.py --account 124884876 --cdp-port 9222 --sample-offer-id shopify_US_7227254276193_41871113158753 --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/merchant-source-recheck/merchant-browser-rpc-sample-latest
```

```bash
python3 ops/scripts/repair_paid_cohort_variant_age_group.py --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/merchant-source-recheck/shopify-variant-age-group-readonly-latest
```

```bash
python3 ops/scripts/google_publication_republish_probe.py --handle mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/merchant-source-recheck/google-publication-sample-dry-run-latest
```

```bash
python3 ops/scripts/export_merchant_center_api_diagnostics.py --merchant-id 124884876 --input-eligibility dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/merchant-source-recheck/api-diagnostics-current-paid-cohort-latest
```

## Next Safe Action

Wait longer for Google & YouTube / Merchant API processing, then recheck only:

1. Merchant browser RPC sample timestamp for `shopify_US_7227254276193_41871113158753`.
2. Full Merchant diagnostics/product-issues export if browser download or API scopes are available.
3. Shopify final publication state for product `7227254276193`.

Expected success signal:

- Sample Merchant timestamp advances beyond the Shopify age_group write time `2026-05-07T17:12:10Z`, and/or paid-cohort US/en `Missing age group` materially drops from the prior `754`.

Do not repeat the single-product toggle, click sync/refresh, upload feeds, or edit product data without fresh explicit action-time approval.
