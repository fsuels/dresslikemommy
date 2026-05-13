# PDP Size-Chart Role Coverage Repair

Date: 2026-05-13 07:03 EDT

## Reported issue

- `family-matching-hawaiian-shirt-and-floral-dress`: builder size details did not show for `Girl` and `Boy`.
- `willow-wildflower-family-matching-set`: builder size details did not show for `Father`.

## Root cause

The product data and localized size-chart rows were present. The defect was in the PDP matching-set quick-size lookup:

- It indexed only the first size-chart table.
- It keyed rows only by exact text labels.
- It did not preserve role-specific header groups such as `Son Shirt` and `Daughter Dress`.
- It did not use table context such as `Dress (Mom & Girl)` versus `Shirt (Dad & Boy)`.
- It could not match shopper-facing child sizes like `2T` to chart rows such as `24M/90`.

## Fix

Updated `assets/product-desktop-ux.js` and mirrored it to `assets/product-desktop-ux-20260513.js` so the matching-set builder:

- Indexes every size-chart table on the PDP.
- Keeps role/table/garment context in the lookup.
- Builds role-specific measurement rows from header-grouped charts.
- Uses table headings and table IDs to route dress rows to Mother/Girl and shirt rows to Father/Boy.
- Uses conservative comparable size tokens so equivalent child sizing formats still resolve.

## Verification

Commands:

```bash
python3 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles family-matching-hawaiian-shirt-and-floral-dress,willow-wildflower-family-matching-set --fail-on-unmatched --report-json dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-13-size-chart-role-coverage/targeted_variant_mapping.json --report-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-13-size-chart-role-coverage/targeted_variant_mapping.csv
python3 ops/scripts/audit_localized_size_chart_variant_mapping.py --fail-on-unmatched --report-json dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-13-size-chart-role-coverage/all_active_variant_mapping.json --report-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-13-size-chart-role-coverage/all_active_variant_mapping.csv
node --check assets/product-desktop-ux.js
node --check assets/product-desktop-ux-20260513.js
git diff --check -- assets/product-desktop-ux.js assets/product-desktop-ux-20260513.js
shopify theme check --path . --fail-level error --output json
shopify theme push --theme 133290917985 --allow-live --only assets/product-desktop-ux.js --only assets/product-desktop-ux-20260513.js
```

Results:

- Targeted audit: `2` products scanned, `980` variant/locale checks, `0` unmatched variants.
- All-active audit: `327` active products scanned, `268` active products with source size charts, `25,160` variant/locale checks, `0` unmatched variants.
- JS syntax checks: passed.
- Scoped diff whitespace check: passed.
- Theme Check: passed with `[]`.
- Scoped live theme push: passed to `dresslikemommy/main` `#133290917985`.
- Live browser readback loaded `product-desktop-ux-20260513.js?v=108643184503827809621778670037`.

Live readback:

- Hawaiian product:
  - `Mother S`: size details shown with Mom dress measurements only.
  - `Father L`: size details shown with Dad shirt measurements only.
  - `Girl 1-2T`: size details shown with height, bust, and dress length.
  - `Boy 2T`: size details shown with height, bust, shoulder, and shirt length.
- Willow product:
  - `Mother S`: size details shown with dress/skirt measurements.
  - `Father S`: size details shown with shirt measurements including sleeve/shoulder/waist/length.
  - `Girl 1-2 Years`: size details shown with dress/skirt measurements.
  - `Boy 1-2 Years`: size details shown with shirt measurements including shoulder/waist/length.

## Guardrails

- No Shopify Admin product title/body/status/publication/price/SKU/inventory edits.
- No checkout, Ads, Merchant, Pinterest, GA4/GTM, billing, credential, or destructive filesystem actions.
- Live write was limited to the two shared PDP JS theme assets.
