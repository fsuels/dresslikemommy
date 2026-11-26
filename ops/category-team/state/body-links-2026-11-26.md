# Body link audit, 2026-11-26 (read-only, Admin API)

Scope: 328 ACTIVE products, English descriptionHtml plus 20 translated body_html. Totals: 291 links, 4727 images, 459 finding rows. Locale-prefix mismatches: 0. Translated links without locale prefix: 262 (all absolute https://www.dresslikemommy.com/... , no /it etc). No vendor hosts found. All images except 1 on cdn.shopify.com; 204 of 205 unique image filenames exist in Admin files.

Problem counts by type:

- markup | stray meta tag pasted into body | 168 rows
- product | redirected (active target) | 62 rows
- product | product is ARCHIVED | 42 rows
- product | redirect to missing/inactive target /collections/swimsuits | 23 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- product | redirected (active target) | 21 rows
- external | Shopify admin UI markup pasted into translation (Polaris bre | 16 rows
- image | filename not found in Admin files list (low confidence; may  | 1 rows

## Pattern A: swim thumbnails on father-son swim/trunk bodies (13 EN links, 274 rows across locales)

All 9 listed products below are father-son/dad-son swim trunks that end with thumbnail links to mother-daughter swimsuits (cross-category). Old handles are 301-redirected to ACTIVE mommy-and-me swimsuit products (so links work), except ARCHIVED ones. Suggested fix per row: remove the whole thumbnail block from the father-son bodies (preferred: wrong audience), or if kept, replace by the redirect target. Redirect targets are all ACTIVE.

| handle | old handle | status/redirect | proposed fix |
|---|---|---|---|
| father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear | tropical-one-shoulder-ruffle-swimsuit-for-women-and-girls-vibrant-floral-print-asymmetrical-design-family-matching-swimwear | product is ARCHIVED | remove link keeping text |
| father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear | chic-tropical-floral-high-neck-swimsuit-set-for-women-and-girls-zippered-sleeveless-quick-dry-swimwear | redirected (active target) | replace with tropical-zip-mommy-and-me-swimsuits |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | chic-ocean-blue-mother-daughter-swimsuit-duo-stylish-ruffle-top-with-paisley-high-waisted-bottoms | product is ARCHIVED | remove link keeping text |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | vibrant-halter-neck-one-piece-swimsuit-with-waist-tie-detail-mother-daughter-matching-swimwear-in-exquisite-baroque-print | redirected (active target) | replace with blue-baroque-mommy-and-me-swimsuits |
| father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print | chic-tropical-ruffle-one-piece-swimsuit-lush-botanical-print-with-elegant-solid-trim-for-mother-child | redirected (active target) | replace with red-botanical-mommy-and-me-swimsuits |
| father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print | elegant-tropical-high-waisted-swimsuit-set-for-mother-and-daughter-radiant-red-halter-neck-design | redirected (active target) | replace with red-tropical-mommy-and-me-swimsuits |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | modern-monochrome-one-shoulder-swimsuit-with-animal-print-ruffle-elegant-poolside-duo-for-mother-and-child | redirected (active target) | replace with animal-ruffle-mommy-and-me-swimsuits |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | elegant-long-sleeve-leopard-print-swimsuit-for-mother-and-daughter | redirected (active target) | replace with leopard-mesh-mommy-and-me-swimsuits |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | chic-floral-ruffle-one-shoulder-swimsuit-for-women-and-girls-elegant-asymmetrical-swimwear-set-in-vibrant-tropics-print | redirected (active target) | replace with pink-tropical-mommy-and-me-swimsuits |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | mother-daughter-vibrant-two-piece-swimsuit-set-with-flowing-skirt-matching-family-swimwear-collection | redirected (active target) | replace with swirl-print-mommy-and-me-swimsuits |
| green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days | chic-family-bonding-mother-daughter-matching-swimsuit-set-with-long-sleeved-cover-up | redirect to missing/inactive target /collections/swimsuits | remove link keeping text |
| matching-dad-and-son-green-stripe-swim-trunks-beach-shorts | mother-daughter-vibrant-two-piece-swimsuit-set-with-flowing-skirt-matching-family-swimwear-collection | redirected (active target) | replace with swirl-print-mommy-and-me-swimsuits |
| matching-dad-and-son-pink-orange-chevron-swim-trunks | mother-daughter-vibrant-two-piece-swimsuit-set-with-flowing-skirt-matching-family-swimwear-collection | redirected (active target) | replace with swirl-print-mommy-and-me-swimsuits |

Locale coverage: every EN row repeats identically in all 20 translations (fr has 14 because one extra link); see findings.json for each locale row.

Sub-pattern A1: 42 rows (2 EN links x 21) point to ARCHIVED products (paisley-blue-yellow and tropical-floral father-son bodies): remove link keeping text / remove thumbnail.
Sub-pattern A2: green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days links a missing handle (chic-family-bonding-mother-daughter... cover-up, queue item 62) that redirects only to /collections/swimsuits: remove thumbnail block.

## Pattern B: Shopify admin UI markup pasted into translations of golden-daisy-mommy-and-me-set (16 locales: ar, cs, da, el, fi, he, hi, ja, ko, nl, no, pl, pt-BR, ro, ru, sv)

Each translated body contains a stray `<meta>` plus an `<a href="https://admin.shopify.com/.../products" class="Polaris-Breadcrumbs...">` breadcrumb, with the first bullet text corrupted after it. Fix: delete the block and restore the sentence from the English body (re-translate the bullet). Not affected: en, de, es, fr, it.

## Pattern C: stray `<meta charset>` tag in bodies of 8 dad-son tropical shirt products, all 21 locales (168 rows)

Handles: father-son-matching-cotton-tropical-shirts-black-white-palm-print, matching-dad-son-cotton-hawaiian-shirts-palm-print-men-kids, matching-dad-son-navy-tropical-cotton-shirts, matching-dad-son-tropical-cotton-shirt-short-sleeve, matching-father-son-tropical-floral-shirt-100-cotton-short-sleeve-button-up-teal-green, matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi, men-s-boys-cotton-hawaiian-shirt-tropical-leaf-print-short-sleeve-button-up-green-black, men-s-short-sleeve-cotton-button-up-shirt-gray-paisley-print
Fix: delete the `<meta ...>` tag, no other change.

## Pattern D: one image filename not found

dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set, fr only: low confidence, verify before changing.

## Not found

No broken collection or page links (275 collection-scoped links all use existing /collections/swimsuits). No links to blogs or pages. Variant ids (?variant=) were not validated.
