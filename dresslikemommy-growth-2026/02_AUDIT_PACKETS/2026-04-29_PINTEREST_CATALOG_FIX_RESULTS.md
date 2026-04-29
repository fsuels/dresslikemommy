# PINTEREST_CATALOG_FIX_RESULTS

Generated: 2026-04-29

## Scope

Operator request: fix the Pinterest catalog/product-group issues identified from the 2026-04-28 authenticated Pinterest capture.

Live changes were limited to Shopify catalog source data. No Pinterest campaign, ad, budget, bid, product-group promotion, inventory quantity, or Merchant Center write was made.

## Fixed

### Warning 188: sale_price greater than price/list_price

- Source fix: cleared invalid Shopify `compareAtPrice` values where `compareAtPrice <= price`.
- Scope: active products published to both Online Store and Pinterest.
- Live result: 3,220 variants across 129 products updated; 0 failures.
- Verification: post-write rescan found 0 remaining in-scope invalid compare-at rows.
- Rollback source: `ops/reports/pinterest-catalog-fix-2026-04-29-clear-invalid-live-price-plan.json`.

Artifacts:

- `ops/reports/pinterest-catalog-fix-2026-04-29-clear-invalid-live-summary.json`
- `ops/reports/pinterest-catalog-fix-2026-04-29-post-price-verification-summary.json`

### Warning 1039: description_html too long

- Source fix: trimmed over-10,000-character product descriptions and localized product `body_html` translations.
- Scope: active products published to both Online Store and Pinterest.
- Live result: 2 source descriptions and 411 localized translations across 28 products updated; 0 errors.
- Verification: post-write rescan found 0 remaining in-scope rows over 10,000 chars.

Artifacts:

- `ops/reports/pinterest-description-html-fix-2026-04-29-live-summary.json`
- `ops/reports/pinterest-description-html-fix-2026-04-29-post-verification-summary.json`
- `ops/reports/pinterest-description-html-fix-2026-04-29-live-changes.csv`

Residual:

- This run did not capture full old HTML values for rollback. If copy restoration is needed, use Shopify product history/backups rather than guessing from truncated content.

### Warning 126: shallow google_product_category

- Source fix: updated `backless-striped-jumpsuit`.
- Before: Shopify category blank; `mc-facebook.google_product_category = 1604`.
- After: Shopify category `Apparel & Accessories > Clothing > One-Pieces`; Google/Pinterest feed override `Apparel & Accessories > Clothing > One-Pieces > Jumpsuits & Rompers`.
- Verification: Shopify Admin API readback confirmed the category and metafield values.

Artifacts:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-category-fix/summary.json`

## Reconciled But Not Changed

### Products out of stock

- Current active Pinterest scope: 7,324 variants.
- Zero-or-less inventory rows: 97.
- Shopify sellable despite zero/negative inventory (`inventoryPolicy=CONTINUE`, `availableForSale=true`): 65.
- True unavailable rows (`inventoryPolicy=DENY`, `availableForSale=false`): 32.
- Fully unavailable products: 0.
- Mixed products with unavailable variants: 5.

Decision: no inventory or publication write was made. Forcing stock would risk selling unavailable sizes, and product-level Pinterest unpublish would remove sellable variants because all true unavailable variants are inside mixed products.

Artifacts:

- `ops/reports/pinterest-out-of-stock-reconciliation-2026-04-29-summary.json`
- `ops/reports/pinterest-out-of-stock-reconciliation-2026-04-29.csv`

## Product Groups And Paid Spend

Pinterest reporting showed 0 campaigns, 0 ads, and $0.00 spend across 30/90/365-day captured windows, so there was no live paid spend or product-group promotion to optimize. Existing product groups remain evidence-only until campaigns exist.
