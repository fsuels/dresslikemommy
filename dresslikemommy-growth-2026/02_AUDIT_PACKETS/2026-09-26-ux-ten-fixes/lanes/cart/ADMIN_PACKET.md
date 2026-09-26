# ADMIN APPROVAL PACKET — make `best-sellers` a complete best-selling source (optional, NOT applied)

Status: PREPARED, not approved, not executed. Recommendation: do not apply this just for the empty-cart row this season.
Even after the fix, the top active sellers are summer/beach items (see NOTES.md). The fix matters if the owner later wants
a truthful "Popular with Families" / "Best Sellers" row or wants the `best-sellers` page to reflect real sales.

- Target: collection `best-sellers`, `gid://shopify/Collection/57621741665`, title "Mommy and Me Matching Outfits – Dresses, Swimsuits & More".
- Before-state (read 2026-09-26): sortOrder `BEST_SELLING`; disjunctive rules, all `TYPE EQUALS`: Dresses, Bottoms, Pajamas, Tops, Swimsuits, Family Matching.
- Gap: active product types that are not matched include Swimwear (44), Matching Family Sets (41), Matching Family Pajamas (28),
  Matching Family Dresses (17), Matching Family Tops (17), Matching Family Sweaters (15), Sets (13), Sweaters (7),
  Matching Family Swimwear (2), Matching Family Outerwear (1), Matching Family Skirts (1).
- Change: add `TYPE EQUALS` rules for each missing type listed above (keep appliedDisjunctively=true and sortOrder BEST_SELLING).
  Mutation: `collectionUpdate(input:{id:"gid://shopify/Collection/57621741665", ruleSet:{appliedDisjunctively:true, rules:[<existing 6> + <11 new>]}})`.
- Side effects: the public `/collections/best-sellers` page and any menu or section using it gain about 180 active products.
  The Merchant/Pinterest feeds do not use collection membership. Confirm with `ops/marketing` before running, because this is a Shopify production write.
- Rollback: run `collectionUpdate` again with the 6 original rules above.
- After-state readback: `collectionByHandle(handle:"best-sellers"){ sortOrder ruleSet{rules{condition}} productsCount{count} }`
  and `/collections/best-sellers/products.json?limit=4` should list skyfade-family-matching-set and chic-family-tides near the top.
- Theme follow-up if approved and wanted: in both lane files, swap `collections['new-arrivals']` to `collections['best-sellers']` and the
  heading key to `sections.cart.popular_with_families` (or `sections.breadcrumbs.label_best_sellers`). Both keys already exist.
