# Localized Product Size Chart Repair Report

Date: 2026-05-10

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-localized-product-size-chart-repair-live`

Problem: `PROB-2026-05-10-LOCALIZED-SIZE-CHARTS`

## Result

Closed as `SOLVED_READBACK_PASSED`.

The owner-reported failure was real: active products could have valid English size-chart tables while their native Shopify `body_html` translations had no table markup. That made localized PDPs hide or fail to build the modern size guide.

The repair applied three layers:

1. Live data repair: restored size-chart table coverage in published locale `body_html` translations for every active product whose English source body has a size-chart table.
2. Theme fallback: published a scoped fallback so the PDP can recover the guide from the default-locale product JSON if a future localized body loses table markup.
3. Workflow guardrail: updated the canonical listing prompts and translation automation so future listings must pass localized size-chart readback before completion.

## Live Repair Scope

- Active products scanned: `327`
- Active products with source size-chart tables: `268`
- Published non-primary locales checked: `20`
- Owner example handle: `geometric-blue-family-matching-set`
- Live translations registered during this repair: `1090`
  - Example targeted pass: `20`
  - Full first pass: `728`
  - Missing/blank body_html catch-up pass: `342`

No product status, publication, handle, variant, price, inventory, image, tag, SEO, Ads, Merchant, Pinterest, feed, or conversion settings were changed.

## Final Admin Readback

Strict final command:

```bash
python3 ops/scripts/repair_localized_product_size_charts.py --fail-on-missing --report-json dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-repair/lanes/admin-audit/full_active_size_chart_final_readback.json --report-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-localized-product-size-chart-repair/lanes/admin-audit/full_active_size_chart_final_readback.csv
```

Result:

- `products_scanned`: `327`
- `products_with_source_size_chart`: `268`
- `products_with_missing_locale_size_chart`: `0`
- `planned_translation_count`: `0`
- `registered_translation_count`: `0`
- `error_count`: `0`

## Public Storefront QA

Spanish example:

- URL: `https://www.dresslikemommy.com/es/products/geometric-blue-family-matching-set?variant=44085198422113&country=ES`
- Browser readback: `lang=es`
- Localized description tables: `2`
- Localized size-chart tables: `2`
- Modern size guide: visible and expandable
- Expanded guide content: visible family size rows
- Verification wall: none
- Screenshot: `lanes/public-qa/geometric-blue-es-size-guide.png`

Italian spot-check:

- URL: `https://www.dresslikemommy.com/it/products/geometric-blue-family-matching-set?variant=44085198422113&country=IT`
- Browser readback: `lang=it`
- Localized description tables: `2`
- Localized size-chart tables: `2`
- Modern size guide: visible and expandable
- Expanded guide rows: `16`
- Verification wall: none

## Files Changed

- `assets/product-desktop-ux.js`
- `snippets/product-desktop-ux.liquid`
- `ops/scripts/poll_shopify_product_translations.py`
- `ops/scripts/repair_localized_product_size_charts.py`
- `ops/tests/test_product_translation_size_labels.py`
- `ops/prompts/START-HERE.md`
- `ops/prompts/shopify-listing-master-prompt.md`
- `ops/prompts/shopify-listing-from-1688.md`
- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_COORDINATION.md`
- `ops/AGENT_WORKLOG.md`
- `AGENTS.md`

## Theme Publish

Scoped live push:

```bash
shopify theme push --theme 134923321441 --only snippets/product-desktop-ux.liquid --only assets/product-desktop-ux.js --allow-live
```

Result: pushed successfully to theme `DLM CRO Preview 2026-05-06` / `#134923321441`.

## Verification Commands

```bash
node --check assets/product-desktop-ux.js
python3 -m py_compile ops/scripts/repair_localized_product_size_charts.py ops/scripts/poll_shopify_product_translations.py
python3 ops/tests/test_product_translation_size_labels.py
python3 ops/tests/test_translation_utils_html_protection.py
python3 ops/tests/test_translation_utils_cleanup_rules.py
git diff --check -- ops/scripts/poll_shopify_product_translations.py ops/scripts/repair_localized_product_size_charts.py ops/tests/test_product_translation_size_labels.py snippets/product-desktop-ux.liquid assets/product-desktop-ux.js ops/prompts/START-HERE.md ops/prompts/shopify-listing-master-prompt.md ops/prompts/shopify-listing-from-1688.md ops/AGENT_COORDINATION.md ops/PROBLEM_TRACKER.md
shopify theme check --path . --fail-level error
```

All listed checks passed. Python test runs emitted the existing local LibreSSL/urllib3 warning only.

## Future Listing Guard

For every future product listing or product body update with a size chart:

```bash
python3 ops/scripts/poll_shopify_product_translations.py --handles <handle> --execute --force-refresh
python3 ops/scripts/repair_localized_product_size_charts.py --handles <handle> --execute
python3 ops/scripts/repair_localized_product_size_charts.py --handles <handle> --fail-on-missing
```

The listing is not complete unless the strict readback returns:

- `products_with_missing_locale_size_chart=0`
- `planned_translation_count=0`
- `error_count=0`

If the strict readback fails, keep the product unpublished or unresolved, record the handle/locale in `ops/PROBLEM_TRACKER.md`, and repair before shipping.
