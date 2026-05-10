# Localized Collection Grid Count Parity Report

Date: 2026-05-10

## Issue

The owner reported that switching the `family-sets` collection from English to another language showed fewer products in the category.

Public pre-readback confirmed the mismatch on page 1 of:

`/collections/family-sets?page=1&sort_by=created-descending`

| Route | Product count text | Rendered product cards before fix |
|---|---:|---:|
| English | 55 products | 35 |
| Spanish | 55 productos | 22 |
| Italian | 55 prodotti | 21 |
| Romanian | 55 produse | 23 |
| Portuguese | 55 products/products localized | 23 |

## Root Cause

`snippets/collection-grid-product-visible.liquid` filtered collection cards by comparing `product.metafields.custom.category1` to English constants such as `Family Matching`.

On translated storefronts Shopify returns localized metafield values. Public PDP analytics JSON showed examples:

- Spanish: `Emparejamiento familiar`
- Italian: `Corrispondenza familiare`

Those valid products remained in the collection count, but the theme skipped their cards because the localized metafield did not equal the English string.

## Fix

Updated `snippets/collection-grid-product-visible.liquid` to normalize collection and product taxonomy values into stable internal keys before comparing:

- `mommy`
- `family`
- `daddy`
- `couples`
- `maternity`

The existing anti-leak collection guard remains in place. The fix only changes theme rendering logic and does not edit products, product status, variants, prices, inventory, SEO, Shopify Markets, Merchant, feeds, ads, or checkout.

After the first live fix, the owner asked to monitor other localized collections and check translated taxonomy labels first if a mismatch appeared. A broader local-preview sweep found one additional mismatch:

| Route | English cards | Spanish cards before additional fix | Product count text |
|---|---:|---:|---|
| `/collections/family-tops?page=1&sort_by=created-descending` | 26 | 11 | 26 products / 26 productos |

Sampling the missing Spanish products confirmed a translated taxonomy-label issue. The same products were English `Family Matching / Family Tops`, but Spanish PDP data exposed `Papá y yo / Camisetas de papá y yo`. The final theme guard now lets the stable branch tag override contradictory localized `category1` values for the current branch, instead of trusting the translated metafield label blindly.

## Verification

- `shopify theme check --path . --fail-level error` passed: 264 files inspected, no offenses.
- `git diff --check -- snippets/collection-grid-product-visible.liquid` passed.
- Scoped live push to theme `134923321441` / `DLM CRO Preview 2026-05-06` succeeded for only `snippets/collection-grid-product-visible.liquid`.
- Pulled the live snippet back to `/tmp/dlm-live-theme-verify` and diffed it against local; no differences.
- Shopify local preview with store data passed:

| Route | Status | Product count text | Rendered cards after fix | First product |
|---|---:|---:|---:|---|
| `/collections/family-sets?page=1&sort_by=created-descending` | 200 | 55 products | 35 | `sunlit-floral-family-matching-set` |
| `/es/collections/family-sets?page=1&sort_by=created-descending` | 200 | 55 productos | 35 | `sunlit-floral-family-matching-set` |
| `/it/collections/family-sets?page=1&sort_by=created-descending` | 200 | 55 prodotti | 35 | `sunlit-floral-family-matching-set` |
| `/ro/collections/family-sets?page=1&sort_by=created-descending` | 200 | 55 produse | 35 | `sunlit-floral-family-matching-set` |
| `/pt-br/collections/family-sets?page=1&sort_by=created-descending` | 200 | Portuguese route | 35 | `sunlit-floral-family-matching-set` |

Public live Spanish readback through web fetch passed after the live push:

- `/es/collections/family-sets` returned the localized page, not a 500.
- The page showed `55 productos`.
- Previously missing products appeared at the start of the grid, including Sunlit Floral, Willow Wildflower, Coastal Blue Stripe, Blue Check, and Geometric Blue.

Additional monitoring and final readback:

- Local preview sweep covered `22` collection handles x `7` localized routes (`es`, `it`, `ro`, `pt-br`, `de`, `fr`, `pl`) for `154` localized checks.
- After the stable-tag override patch, the sweep returned `0` card-count mismatches.
- Final local-preview examples:
  - `family-sets`: EN/ES/IT/RO/PT-BR/DE/FR/PL all rendered `36` page-1 cards with `55` product count text.
  - `family-tops`: EN/ES/IT/RO/PT-BR/DE/FR/PL all rendered `26` cards with `26` product count text.
- `shopify theme check --path . --fail-level error` passed again with `264` files inspected and no offenses.
- `git diff --check -- snippets/collection-grid-product-visible.liquid` passed.
- Scoped live push to theme `134923321441` succeeded again for only `snippets/collection-grid-product-visible.liquid`.
- Pulled the live snippet back to `/tmp/dlm-live-theme-verify-20260510-collection-monitor` and diffed it against local; no differences.
- Public live Spanish `/es/collections/family-tops` web readback showed `26 productos` and rendered the previously hidden family T-shirt products.

Raw local Python requests to the public storefront remained temporarily blocked by Shopify HTTP `429` after earlier rapid probes, so repeated raw public curls were stopped to avoid extending rate limiting.

## Status

Solved by scoped live theme patch, broader localized collection monitoring, live snippet pullback, and public Spanish readbacks.

## Next

If future collection/product taxonomy translations are added, keep the collection grid filter comparing canonical internal keys or stable tags, not translated customer-facing labels. The underlying Spanish product taxonomy translation for some family tops still labels the Type facet as `Camisetas de papá y yo`; product visibility is fixed, but a later Shopify Admin translation cleanup could polish that customer-facing filter label.
