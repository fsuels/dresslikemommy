# Spanish Family-Tops Taxonomy Cleanup

Date: 2026-05-10

## Scope

- Owner request: clean the underlying Spanish taxonomy translations for the affected `family-tops` products so the customer-facing Spanish facets match the category cleanly.
- Surface changed: Shopify Admin native translation rows on product taxonomy metafield resources only.
- Collection checked: `/es/collections/family-tops?page=1&sort_by=created-descending`.

## Root Cause

- The collection-grid visibility issue had already been fixed in theme code, but the Spanish Type facet still exposed a stale Daddy & Me-style taxonomy label for active family top products.
- Admin readback showed affected active products had:
  - `custom.category1` source `Family Matching` translated to `Papá y yo`
  - `custom.subcategory` source `Family Tops` translated to `Camisetas de papá y yo`
- Those translated metafield values fed the Spanish collection facets, producing a mismatched Type bucket for family top products.

## Changes

- Registered `30` Spanish native translation rows for `15` active products in the Shopify `family-tops` collection:
  - `custom.category1`: `Family Matching` -> `Emparejamiento familiar`
  - `custom.subcategory`: `Family Tops` -> `Tops familiares`
- Scope was intentionally limited to active products currently visible in the collection.
- No source product metafield values were changed; only Spanish translation rows on the metafield resources were updated.

Affected active handles:

- `battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids`
- `beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design`
- `colorful-family-matching-love-t-shirts-fun-bold-lettering-design-in-multiple-colors`
- `colorful-i-love-family-matching-t-shirts-set-for-the-whole-family`
- `cute-dinosaur-family-matching-t-shirts-what-are-you-doing-hug-design`
- `cute-family-matching-cartoon-t-shirts-sun-cloud-plant-design-in-5-colors`
- `eternal-love-family-matching-t-shirts-colorful-heart-design`
- `family-matching-original-remix-encore-t-shirt-set-fun-family-outfits-for-all-ages`
- `happy-flower-family-matching-t-shirts-colorful-floral-print-for-parents-kids`
- `love-grows-family-matching-t-shirts-watering-can-plant-design`
- `matching-family-love-balloon-t-shirt-set-heart-love-design-in-4-colors`
- `matching-family-love-t-shirt-set-adorable-family-heart-design`
- `matching-family-minimalist-heart-t-shirt-set-simple-love-design-in-4-colors`
- `matching-family-plug-lightbulb-t-shirt-set-unique-family-connection-design`
- `need-more-family-matching-drink-t-shirt-set-beer-coffee-milk-juice-family-outfit`

## Verification

- Shopify Admin write/readback:
  - Planned translation updates: `30`
  - Affected active products: `15`
  - Registered translation updates: `30`
  - Readback passed: `30`
  - Readback failed: `0`
- Post-write active collection distribution:
  - Active family-tops products: `26`
  - Bad active translation rows for `Papá y yo` / `Camisetas de papá y yo`: `0`
  - `custom.subcategory` Spanish facet sources now distribute as:
    - `Tops familiares`: `18`
    - `Tops`: `3`
    - blank translation for English source `Tops`: `5`
- Public Spanish collection readback:
  - URL: `https://www.dresslikemommy.com/es/collections/family-tops?page=1&sort_by=created-descending&cache_bust=taxonomy-cleanup-20260510`
  - HTTP `200`
  - Product cards: `26`
  - `Camisetas de papá y yo`: `0`
  - Type facet region: `Tops (8)` and `Tops familiares (18)`, with `26 productos`.
- Public Spanish product taxonomy JSON readback for `eternal-love-family-matching-t-shirts-colorful-heart-design`:
  - `category1`: `Emparejamiento familiar`
  - `subcategory`: `Tops familiares`
  - `subcategory2`: blank
  - `type`: `pending`
- The only remaining `Papá y yo` occurrences on that public product page were the normal header/menu links to `/es/collections/daddy-me`, not product taxonomy or the family-tops facet.

## Guardrails

- No Shopify product status, publication, price, variant, inventory, handle, image, source/vendor URL, tag, SEO, collection membership, or source taxonomy value changes.
- No Shopify theme edit or push.
- No Merchant Center, Google Ads, Pinterest, GA4/GTM, feed, budget, bid, product-scope, product-group, conversion, checkout payment, or order changes.

## Residual Risk

- The cleanup intentionally skipped archived products. A pre-write scan found additional archived family-tops products with the stale Spanish Daddy & Me-style translations; they are not public in the active collection now, but should be rechecked before any archived item is republished.
- Spanish facets now use both `Tops` and `Tops familiares` because the collection contains products with different English taxonomy sources (`Tops` and `Family Tops`). The incorrect Daddy & Me label is gone; unifying those labels further would be a separate merchandising/taxonomy decision.

## Evidence

- Raw Admin write/readback JSON: `spanish_family_tops_taxonomy_translation_cleanup.json`
- Related solved collection parity report: `../2026-05-10-localized-collection-grid-count-parity/LOCALIZED_COLLECTION_GRID_COUNT_PARITY_REPORT.md`
