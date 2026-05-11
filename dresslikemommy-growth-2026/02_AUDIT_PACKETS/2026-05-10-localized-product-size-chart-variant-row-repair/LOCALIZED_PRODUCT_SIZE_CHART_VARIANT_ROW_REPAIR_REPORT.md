# Localized Product Size Chart Variant Row Repair

Date: 2026-05-10

Status: `SOLVED_READBACK_PASSED`

## Scope

Owner reported that localized PDPs still failed to show size chart details, including:

- `https://www.dresslikemommy.com/es/products/geometric-blue-family-matching-set?variant=44085199274081`
- Active listings in all published storefront languages.

This pass repaired both layers:

- Localized `body_html` size-chart table coverage in Shopify Admin translations.
- Storefront selected-variant row matching in `assets/product-desktop-ux.js`.

## Root Causes

- Localized size labels such as Spanish `Infantil 1-2 anos` parsed as generic `child`, while chart rows parsed as `boy` or `girl`; strict role equality hid the selected row.
- Some localized products had one source chart table translated but not the complete source table set.
- Some translated size-chart headings and headers did not split wide family charts into role-specific cards.
- Some active legacy variants are larger than the source chart max row; exact rows do not exist, so the browser must show the nearest available row instead of blanking the guide.
- Table selection could prefer a generic table by context before checking a stable `size-chart-*` table id.

## What Changed

- Hardened localized selected-row matching in `assets/product-desktop-ux.js`:
  - SKU/current-variant role inference before translated option text.
  - Compatible role groups: `child` can match `boy`, `girl`, or `baby`; `adult` can match `mother` or `father`.
  - Localized role/header aliases for translated son/daughter/mother/father chart headers.
  - Stable table-id garment selection before weaker heading/context matches.
  - Shirt/shorts/shared-set compatibility for products with related source tables.
  - Adult nearest-row fallback for variants beyond the max source chart size, with nearest-size tie-break.

- Hardened Admin repair scripts:
  - `repair_localized_product_size_charts.py` now treats incomplete source table coverage as repair-worthy, not just total chart absence.
  - `poll_shopify_product_translations.py` now uses complete source table-set coverage for translation polling/repair.
  - Added `audit_localized_size_chart_variant_mapping.py` to fail future listing work when localized active variants cannot map to a chart row.

- Hardened listing prompts:
  - New listing workflow must run localized table repair/readback and variant-row mapping audit before completion.

## Shopify Writes

- Registered `354` localized body translations to restore complete source table sets across `24` active products.
- Force-rebuilt localized size-chart table sections for `28` failing handles, registering `560` translations.
- Scoped-pushed `assets/product-desktop-ux.js` to live theme `134923321441`.

No product status, publication, handle, image, price, inventory, tags, SEO, Merchant, Google Ads, Pinterest, checkout, payment, or order changes were made.

## Verification

- Complete table-set final readback:
  - Products scanned: `327`
  - Products with source size chart: `268`
  - Missing localized size chart/table set: `0`
  - Planned repairs: `0`
  - Errors: `0`
  - Evidence: `lanes/admin-audit/full_active_complete_table_set_FINAL_READBACK_AFTER_FORCE.json`

- Variant row mapping final active-catalog audit:
  - Products scanned: `327`
  - Products with source size chart: `268`
  - Variant-locale checks: `25,160`
  - Products with unmatched variants: `0`
  - Unmatched variant-locale count: `0`
  - Evidence: `lanes/admin-audit/full_active_variant_row_mapping_FINAL_ZERO_UNMATCHED.json`

- Public browser readback, owner exact URL:
  - URL: `https://www.dresslikemommy.com/es/products/geometric-blue-family-matching-set?variant=44085199274081&country=ES`
  - `lang=es`
  - Selected options: `Shorts`, `Infantil 1-2 anos`
  - Hidden variant: `44085199274081`
  - Visible snapshot: `DETALLES DE TU TALLA Nino 1-2 anos`
  - Selected row count: `1`
  - Reconstructed fallback tables: `0`

- Public browser readback, extra localized edge case:
  - URL: `https://www.dresslikemommy.com/el/products/blue-check-family-matching-set?variant=44087754489953&country=GR`
  - `lang=el`
  - Selected options: `Shorts`, `Adult 3XL`
  - Hidden variant: `44087754489953`
  - Visible snapshot now resolves to nearest available adult chart row `Adult L`
  - Selected row count: `1`

- Code/theme checks:
  - `node --check assets/product-desktop-ux.js` passed.
  - `python3 -m py_compile` passed for the changed Python scripts.
  - `shopify theme check --path . --fail-level error` passed with `264` files inspected and no offenses.

## Future Guard

Run these before considering any new listing complete:

```bash
python3 ops/scripts/repair_localized_product_size_charts.py --execute
python3 ops/scripts/repair_localized_product_size_charts.py --fail-on-missing
python3 ops/scripts/audit_localized_size_chart_variant_mapping.py --fail-on-unmatched
```

For a single new handle, pass `--handles <handle>` to the same scripts before publishing or calling the listing done.
