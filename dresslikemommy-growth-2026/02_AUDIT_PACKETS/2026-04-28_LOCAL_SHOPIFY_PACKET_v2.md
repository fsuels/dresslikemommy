# LOCAL_SHOPIFY_PACKET_v2

Generated: 2026-04-28
Platform: LOCAL_SHOPIFY
Mode: local dry-run only. No deploy. No Shopify writes.
Branch: `dlm-profit-fixes-2026-04-28`

## Executive Summary

- Used the current theme repository plus existing local Shopify export packet v1. No Shopify mutation, deploy, feed upload, or live page edit was performed.
- Scope covered 335 active products and 7324 active variants from the local export.
- Created dry-run diffs and CSVs under `2026-04-28_LOCAL_SHOPIFY_ARTIFACTS/`.
- Key blockers remain owner inputs for shipping coverage, processing/tracking timing, transit ranges, customs/duties stance, returns window/trigger/exclusions, payment wording, and swimwear return handling.
- Unsupported trust claims were found in theme surfaces: `4.8/5`, `15,200+ families`, `Thousands of happy families`, and `Trusted since 2016`. Local Loox evidence only supports 61 active-product reviews across 12 active products, not a storewide 15,200-family claim.

## Artifact Index

See `2026-04-28_LOCAL_SHOPIFY_ARTIFACTS/artifact_manifest.csv` for every proposed diff/CSV with file path, reason, expected impact, risk, verification, rollback, and exact owner approval needed.

## Work Item Results

### 1. FAQ size-guide fix

- Found 45 off-domain `assassinshoodies.com` hits in repo/export evidence.
- Same-domain evidence exists: live digest has `/pages/size-guide` (`PAGE::86424649825`) and `/pages/track-your-order` (`PAGE::18847760481`).
- Dry-run diff: `faq_page_dry_run.diff`.
- No size-chart facts were added or invented.

### 2. Shipping/returns/customs consistency

- Created `policy_truth_table.csv` with missing owner inputs.
- Created `policy_copy_hits.csv` with 2547 exact term hits across theme files, live page digest, and active product export fields.
- No policy copy was written because exact owner values are not approved.

### 3. Recurring/subscription/deferred text

- `sections/main-product.liquid` gates payment terms behind `product.selling_plan_groups.size > 0`.
- `sections/cart-notification-product.liquid` gates selling-plan names behind `item.selling_plan_allocation != null`.
- Locale subscription/deferred strings appear to be Shopify checkout/wallet internals. No edit recommended until Website QA confirms visible shopper text on products with no selling plans.

### 4. Trust/review claims

- Created `trust_review_claims.csv` and `trust_review_claims_dry_run.diff`.
- Proof missing for storewide `4.8/5 by 15,200+ families`, `Thousands of happy families`, and `Trusted since 2016`.
- Proposed action: remove unsupported numeric/store-age claims or replace with neutral non-claim copy after owner approval.

### 5. Delivery estimate block

- Found hardcoded delivery logic in `layout/theme.liquid`, `assets/cart.js`, `sections/main-product.liquid`, `sections/main-cart-footer.liquid`, `snippets/cart-drawer.liquid`, and `snippets/jsonld-seo.liquid`.
- Dry-run diff hides estimate dates unless an approved market/product range data source exists.
- No shipping times were invented.

### 6. Product-card pricing cleanup

- Created `pricing_cleanup_findings.csv` and `pricing_cleanup_dry_run.diff`.
- Unit pricing is preserved when `unit_price_measurement` exists.
- The dry-run only removes a redundant hidden regular-price label in sale-state markup; apply only after Website QA confirms duplicate labels are visible/noisy.

### 7. Collection filters

- Created `collection_filter_value_audit.csv` with 729 candidate/noisy values.
- Proposed canonical groups: role, adult size, child size, category, occasion, color, price.
- Owner approval required before changing Shopify Search & Discovery filter settings.

### 8. Search page recovery

- Created `search_recovery_dry_run.diff` adding draft links to top collections and popular searches on zero-result search pages.
- This is a dry-run only and uses English labels that need localization before live use.

### 9. Localization defects

- Created `localization_defects_exact.csv`.
- Static scan found no local user-facing raw `translation missing` strings to fix; Theme Check passed with 251 files and no offenses.
- No auto-translation of legal/policy copy was performed.

### 10. Feed/product CSVs

Created local CSVs only; nothing was uploaded:

- `missing_unit_costs.csv`: 5928 active variant rows.
- `missing_sku.csv`: 1604 active variant rows.
- `missing_barcode_gtin.csv`: 5897 active variant rows.
- `missing_color_size_gender_age_group.csv`: 388 defect rows.
- `custom_labels.csv`: 7324 rows with custom_label_0 through custom_label_4.

## Residual Risks

- Policy copy remains blocked until owner-approved values exist.
- Dry-run diffs are intentionally not applied to the theme or Shopify pages.
- Search recovery text needs localization and final collection/search-term approval.
- Delivery estimate hiding is safer than inventing times, but may reduce checkout reassurance until approved ranges are supplied.
- Feed CSVs are generated from the local 2026-04-28 export and should be regenerated before any future writeback.

## Next Best Action

Owner should fill/approve `policy_truth_table.csv`, then approve which dry-run diffs move to local implementation and which feed CSVs are allowed to become writeback inputs.
