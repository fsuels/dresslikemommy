# Powder Blue Top/Pants Option Repair

Date: 2026-05-19 EDT

Live URL: https://www.dresslikemommy.com/products/powder-blue-mommy-and-me-set

## Owner Request

Fix the Powder Blue listing because the top and pants are sold separately and the options needed to show that.

## Before State

- Product ID: `7535944368225`
- Handle: `powder-blue-mommy-and-me-set`
- Status: `active`
- Published at: `2026-04-23T11:07:10-04:00`
- Options: `Size`, `Color`
- Variant count: `8`
- Storefront visible issue: no `Type` / piece selector; the shopper could only choose size.

## Change Made

- Added `Type` as option 1 with values `Top` and `Pants`.
- Moved `Size` to option 2 and kept the same 8 size values.
- Kept `Color` as option 3 with value `Blue`.
- Reused the existing 8 variant IDs as `Top` variants.
- Created 8 matching `Pants` variants for the same sizes.
- Preserved product handle, active status, publication, title, prices, compare-at prices, inventory policy, and inventory management.
- Set inventory item costs to the established 50% half-up rule:
  - `28.99 -> 14.50`
  - `31.99 -> 16.00`

## After State

- Options: `Type`, `Size`, `Color`
- Variant count: `16`
- Top variant IDs preserved:
  - `44076870664289`, `44076870697057`, `44076870729825`, `44076870762593`
  - `44076870795361`, `44076870828129`, `44076870860897`, `44076870893665`
- New Pants variant IDs:
  - `44861276651617`, `44861276684385`, `44861276717153`, `44861276749921`
  - `44861276782689`, `44861276815457`, `44861276848225`, `44861276880993`

## Verification

- Shopify Admin readback passed:
  - Product stayed `active`.
  - Published timestamp stayed `2026-04-23T11:07:10-04:00`.
  - Options read back as `Type`, `Size`, `Color`.
  - Variant count read back as `16`.
  - All inventory item costs matched the 50% half-up rule.
- Public storefront readback passed:
  - Rendered page shows `1. Choose piece`.
  - Rendered `name="options[Type]"`.
  - Rendered `Top` and `Pants`.
  - Product JSON exposes all 16 variants.
- Cart add checks passed:
  - Top variant `44076870664289` returned HTTP `200`.
  - Pants variant `44861276651617` returned HTTP `200`.
- Localized size-chart variant-row audit passed:
  - `products_scanned=1`
  - `variant_locale_checks=320`
  - `products_with_unmatched_variants=0`
  - `unmatched_variant_locale_count=0`

## Evidence Files

- `raw/before_product.json`
- `raw/update_payload_summary.json`
- `raw/after_product_immediate.json`
- `raw/admin_after_summary.json`
- `raw/storefront_after.html`
- `raw/storefront_product_after.json`
- `variant_row_mapping_audit.json`
- `variant_row_mapping_audit.csv`

## Guardrails Preserved

- No publish/unpublish action.
- No handle change.
- No price increase.
- No unrelated Shopify product edits.
- No source/vendor URLs added to customer-visible data.
- No Ads, Merchant, Pinterest, GA4/GTM, billing, credential, theme, or destructive git/filesystem changes.

## Residual Risks

- Resolved in follow-up: `translation_polish/POWDER_BLUE_OPTION_TRANSLATION_POLISH.md` registered translations for `Type`, `Top`, and `Pants` across all published non-primary locales.
- Remaining caveat: the short commerce-label translations were not reviewed by native speakers.
