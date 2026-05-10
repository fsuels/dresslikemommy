# Family Dress And T-Shirt Size Guide Repair

Date: 2026-05-10 EDT

## Scope

- Owner-reported URL: `https://www.dresslikemommy.com/products/family-matching-dress-and-t-shirt-set-summer-fun-for-the-whole-family?variant=40913273815137`
- Product: `family-matching-dress-and-t-shirt-set-summer-fun-for-the-whole-family`
- Variant: `40913273815137` / `T-Shirt / Boy 6T`
- Live theme: `134923321441` / `DLM CRO Preview 2026-05-06`

## Root Cause

The source product has a valid header-grouped size chart. English could already split the chart into Mother, Father, Girl, and Boy cards because headers such as `Son Shirt Bust` matched the theme's role parser.

Localized chart headers such as Spanish `Busto de la camisa del hijo` and `Busto del vestido de la hija` did not reliably parse into role-specific header groups on the live theme. The localized PDP could fall back to one large all-size comparison table, which mixed son-shirt and daughter-dress columns in the selected-size snapshot.

## Changes

- Updated `assets/product-desktop-ux.js` so localized role aliases retain accent-sensitive forms instead of deduping them away.
- Added child kinship aliases already needed by localized chart headers, including son/daughter terms such as `hijo`, `hija`, `filho`, `filha`, `figlio`, `figlia`, `sohn`, `tochter`, and `fils`.
- Added role-header cleanup so grouped table metric labels become readable, for example `Busto de la camisa` instead of `Busto de la camisa del`.
- Preserved the default-locale size-guide fallback path that depends on `data-product-handle` in `snippets/product-desktop-ux.liquid`.

## Live Push

Scoped live push only:

- `assets/product-desktop-ux.js`
- `snippets/product-desktop-ux.liquid`

No Shopify Admin product data, product status, handle, variants, prices, inventory, tags, SEO, Shopify Markets, checkout settings, Merchant, Google Ads, Pinterest, feed, analytics, campaign, budget, bid, conversion-goal, payment, or order changes were made.

## Verification

- Public product JSON readback for the owner URL confirmed the product has `21` variants, selected variant `40913273815137` is `T-Shirt / Boy 6T`, and the source description contains one `size-chart` table.
- Pre-fix public English render already showed a selected snapshot; pre-fix public Spanish render showed the guide but fell back to `Comparar todos los tamaños` / one mixed all-size table.
- Local VM parser check against the Spanish translated header set split the chart into `mother`, `father`, `girl`, and `boy` groups and kept the Boy group to shirt columns only.
- Targeted Admin/API mapping audit passed for `es,it,ro,pt-BR,de,fr`: `126` variant-locale checks, `0` unmatched.
- `node --check assets/product-desktop-ux.js` passed.
- `shopify theme check --path . --fail-level error` passed with `264` files inspected and no offenses.
- `git diff --check -- assets/product-desktop-ux.js snippets/product-desktop-ux.liquid` passed.
- Scoped live push succeeded.
- Live pullback from theme `134923321441` matched local for both pushed files.
- Post-push public Spanish readback for the owner product with `country=ES` returned:
  - `lang=es`
  - selected snapshot present
  - selected text `Niño 6T/130`
  - summary `Comparar tamaños de familia`
  - grouped role cards present, including `Niño`
  - one-big `Comparar todos` fallback absent
  - no `Product desktop UX init failed`, `ReferenceError`, or `TypeError`
- Owner-requested browser hard-refresh follow-up: Chrome DevTools first showed the stale tab still loading an old `product-desktop-ux.js` asset and rendering `Comparar todos los tamaños`. Fresh storefront HTML then returned the updated asset URL; after a cache-busted navigation plus cache-ignored reload, the Spanish owner URL rendered selected `Niño 6T/130`, summary `Comparar tamaños de familia`, no mixed fallback, and no console errors.

## Residual Risk

The exact English route worked before the patch and the Spanish route passed after the patch. Other published locales are covered by Admin/API row-mapping audit, but only Spanish was browser-rendered publicly in this follow-up to avoid excessive public probing and Shopify rate limiting.
