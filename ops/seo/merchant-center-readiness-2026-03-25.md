# Merchant Center Readiness Audit

Date: 2026-03-25

## What Is Already Good

Live product structured data in the theme already includes:
- `AggregateOffer`
- `MerchantReturnPolicy`
- `OfferShippingDetails`
- brand output
- price and availability output

This means the theme is not starting from zero for Google merchant listings.

## Current Data Gaps From The Export

Source: `products_export_1 2.csv`

For active published products:
- Total active published products: `283`
- Missing Google product category: `283`
- Missing MPN: `283`
- Missing any barcode on variants: `193`
- Missing type: `90`
- Missing SEO description in export: `142`

Top active product types:
- `Family Matching`: `106`
- `UNKNOWN`: `90`
- `Swimsuits`: `31`
- `Dresses`: `16`
- `Maternity`: `14`
- `Sweaters`: `7`
- `Couples`: `7`
- `Tops`: `6`

## Highest-Risk Merchant Center Problems

1. Broken live product titles
- `164` planned repairs are already documented in `ops/seo/product_title_repair_plan.csv`.
- This is the highest-urgency feed cleanup item.

2. Missing Google product category on every active published product
- Fill this in for the highest-volume categories first:
  - Family Matching
  - Swimsuits
  - Dresses
  - Maternity
  - Couples

3. Limited identifier coverage
- `193` active published products have no barcode on any variant.
- If you do not have GTINs, make sure the products are consistently treated as custom products in Google/Shopify setup.

4. Weak taxonomy coverage
- `90` active published products have no `Type`.
- The largest problem bucket is `UNKNOWN`.

## Recommended Merchant Center Order Of Operations

1. Repair the `164` broken titles.
2. Fill Google product category for active products.
3. Normalize `Type` for the `UNKNOWN` bucket.
4. Add GTIN/barcode where real manufacturer IDs exist.
5. If no GTIN exists, confirm Google custom-product handling is consistent.
6. Connect Google Merchant Center diagnostics to a weekly cleanup routine.

## Notes

- Shopify export columns for `SEO Title` being mostly blank are not automatically a problem by themselves if product titles are clean and the storefront title tags are good.
- The bigger risk is feed/title quality, missing product categorization, and inconsistent identifiers.
