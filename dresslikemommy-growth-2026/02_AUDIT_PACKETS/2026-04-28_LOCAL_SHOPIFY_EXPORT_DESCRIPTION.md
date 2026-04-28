# 2026-04-28 LOCAL_SHOPIFY Export Description

Generated: 2026-04-28
Mode: read/export/analyze only. No Shopify writes and no implementation edits.

## Date Windows

- Last 30 complete days: 2026-03-29 through 2026-04-27, end exclusive 2026-04-28.
- Last 90 complete days: 2026-01-28 through 2026-04-27, end exclusive 2026-04-28.
- Last 365 complete days: 2025-04-28 through 2026-04-27, end exclusive 2026-04-28.

## Files Created

- `../01_EXPORTS_RAW/SHOPIFY/2026-04-28_LOCAL_SHOPIFY_EXPORT_raw.json`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_ANALYSIS_v1.json`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_financial_summary.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_variant_financials.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_product_eligibility.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_custom_labels.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_feed_defects.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_localization_defects.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_exclude_from_paid.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_public_site_validation.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_theme_tracking_defects.csv`
- `../03_LOCAL_ANALYSIS/2026-04-28_LOCAL_SHOPIFY_public_theme_validation.json`
- `../05_SCREENSHOTS/2026-04-28_LOCAL_SHOPIFY_SCREENSHOTS/README.md`

## Privacy/Safety

The export intentionally omits customer names, emails, phone numbers, shipping/billing addresses, cookies, tokens, card/payment details, and Shopify order names. Order-level data is limited to dates, totals, fee totals, source fields, line-item product/variant references, quantities, and refund amounts.

## Data Sources

- Shopify Admin GraphQL API 2026-04: products, variants, inventory item unit costs, inventory quantities, product metafields, media/image dimensions, collections, locales, markets, product translations, orders, line items, refunds, transaction fee totals.
- Shopify REST Admin API 2026-04: shipping zones summary.
- Local theme files: `layout/`, `sections/`, `snippets/`, `templates/`, `assets/`, `config/`, `locales/`, `ops/customer-events/`.
- Public read-only HTTP checks: home, `/collections/bottoms`, `/collections/all`, one sample PDP, Spanish/French localized sample PDPs, shipping/refund policies.

## Known Limitations

- INSUFFICIENT_EVIDENCE: ad spend and conversion-value exports are missing, so paid ROAS/CAC cannot be computed by platform.
- INSUFFICIENT_EVIDENCE: SKU-level costs are missing for 5928 active variants, so those variants are UNKNOWN_MARGIN.
- INSUFFICIENT_EVIDENCE: Playwright is not installed locally, so this pass created the required screenshot folder but did not capture browser screenshots.
- Translation English-fragment detection is heuristic and must be reviewed before edits.
- Market-country readiness needs operator confirmation because shipping zones include a Rest of world wildcard.
