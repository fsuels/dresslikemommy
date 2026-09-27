# Collection membership cleanup: approval packet

Status: READ-ONLY packet, prepared 2026-09-27. Nothing was written to Shopify, the theme, locales or git. Every change below needs owner approval.

Machine-readable twin: `collection_membership.json`. It has rules before and after, full member diffs, mutations, rollbacks and the manual-order snapshots.

## Why this matters

`snippets/collection-grid-product-visible.liquid` drops cards at render time when a product belongs to another audience branch. Filtering after `paginate` causes three problems: pages come out short or empty, the "N products" label counts hidden items, and filter counts include products the shopper never sees. Removing those products from the collections in Admin fixes all three at the source. The snippet then has nothing left to hide.

### How the snippet decides (evaluated in Python, 1:1 with the Liquid)

- The branch comes from the collection metafield `custom.category1`, which no collection has set. Without it, the handle list decides: mommy, family, daddy, couples or maternity. `mother-daughter-matching-dresses` is forced to mommy.
- The product key comes from `custom.category1`, falling back to a `category1:` tag, and is normalised by substring (mommy/mami/mother/daughter, famil/rodzin, daddy/pap/father/tata, …).
- A product is hidden if its key belongs to another branch and it lacks the branch tag. It is also hidden if it has no key and no branch tag.
- Mommy branch only: a product is also hidden if it has the `Family Matching` tag and its title or handle contains "family matching".
- Force-visible exceptions: collection id 290635284577 (`couples`) and the `family-pajamas` handle.
- The snippet runs only in the non-interleave grid branch. The default view of mommy and family hubs uses the interleave branch (sort `created-descending`, no filter), which skips it. That default view shows every member: see `new-matching-outfits`, `popular-mommy-me-1` and `matching-outfits` below.

### Verification

- 37 of the 43 snippet handles resolve to a collection, 29 of them non-empty. For 26 of the 29, the Python evaluation matches the live rendered grid exactly, compared as handle sets across every page. The other 3 are the interleave hubs, which render all members in the default view. Under `sort_by=price-ascending` they match the evaluation, checked on `new-matching-outfits` (107) and `matching-outfits` (27).
- Admin rules re-evaluated in Python reproduce storefront `products.json` membership exactly. The only exception is 6 stale-index members, noted below.
- The brief's live examples reproduce: pajamas shows 22 of 39 with an empty page 2, mommy-and-me 107 of 146, matching-family-vacation-outfits 48 of 104, sweaters 5 of 19.

## Summary

| Collection | Type / sort | Published | Visible | Hidden | Recommended change | Visible loss | Added |
|---|---|---|---|---|---|---|---|
| `mommy-and-me` | SMART / MANUAL | 146 | 107 | **39** | `TAG EQUALS "Mommy and Me" AND TAG NOT_EQUALS "Family Matching"` | 0 | 0 |
| `new-matching-outfits` | SMART / CREATED_DESC | 146 | 107 | **39** | `TAG EQUALS "Mommy and Me" AND TAG NOT_EQUALS "Family Matching"` | 0 (+ default-view loss, see flags) | 0 |
| `popular-mommy-me-1` | SMART / CREATED_DESC | 146 | 107 | **39** | `TAG EQUALS "Mommy and Me" AND TAG NOT_EQUALS "Family Matching"` | 0 (+ default-view loss, see flags) | 0 |
| `pajamas` | SMART / MANUAL | 39 | 22 | **17** | `TAG EQUALS "Mommy and Me" AND TAG EQUALS "Pajamas" AND TAG NOT_EQUALS "Family Matching"` | 0 | 0 |
| `tops` | SMART / CREATED_DESC | 20 | 1 | **19** | `TAG EQUALS "Tops" AND TAG EQUALS "Mommy and Me" AND TAG NOT_EQUALS "Family Matching"` | 0 | 0 |
| `sweaters` | SMART / CREATED_DESC | 19 | 5 | **14** | `TAG EQUALS "Mommy and Me" AND TAG EQUALS "Sweaters" AND TAG NOT_EQUALS "Family Matching"` | 0 | 0 |
| `matching-outfits` | SMART / CREATED_DESC | 79 | 27 | **52** | `TAG EQUALS "Family Matching"` | 0 (+ default-view loss, see flags) | 89 |
| `matching-family-vacation-outfits` | SMART / BEST_SELLING | 104 | 48 | **56** | `TAG EQUALS "vacation" AND TAG EQUALS "Family Matching"` | 4 (0 with the tag pre-step) | 0 |
| `matching-hawaiian-outfits` | SMART / BEST_SELLING | 9 | 1 | **8** | `TAG EQUALS "hawaiian" AND TAG EQUALS "Family Matching"` | 0 | 0 |

No hidden products, so no change is needed: `dresses`, `mother-daughter-matching-dresses`, `swimsuits`, `bottoms`, `leggings`, `pants`, `formal-dresses`, `maxi-dresses`, `midi-dresses`, `mini-dresses`, `sundresses`, `jumpsuits`, `rompers`, `new-women-outfits`, `popular-family-matching`, `family-pajamas`, `family-swimsuits`, `family-sets`, `family-tops`, `family-sweaters`, `daddy-and-me`, `daddy-me`, `daddy-me-t-shirts`, `daddy-me-shirts`, `trunks`, `couples`, `matching-couples-t-shirts`, `maternity`.

Handles in the snippet that do not resolve to a collection: `skirts`, `mommy-and-me-easter-dresses`, `easter-matching-outfits`, `spring-matching-outfits`, `family-matching-outfits`, `couple-matching`.

Every collection in scope is a smart collection, so there are no manual product removals. Each fix is a rule edit. When the current rule set is "any condition" (OR) with one rule, the edit switches it to "all conditions". An OR set with several rules cannot be narrowed by adding a condition, which is why vacation needs a different approach.

## Top recommendations (in order)

1. **Mommy branch: add `Product tag is not equal to "Family Matching"`** to `mommy-and-me`, `pajamas`, `tops` and `sweaters`, switching them to "all conditions". Result: 39 + 17 + 19 + 14 hidden products removed, **0 visible-product loss, 0 added**. The two alternatives tested are worse: `title does not contain "family matching"` loses 3 visible products in mommy-and-me and 1 in sweaters. A `custom.category1 = Mommy and Me` condition is also zero-loss but first needs a metafield-definition change, because the definition has `smartCollectionCondition.enabled=false`.
2. **Family hub `matching-outfits`: replace the 8 legacy product-type rules with `Product tag is equal to "Family Matching"`**, the rule `popular-family-matching` already uses. It removes 52 Mommy & Me / Daddy & Me items with 0 loss in the snippet view, and adds 89 Family Matching items. Its old type rules (`Tops`, `Dresses`, `Family Matching`…) no longer match the current product types, so the collection had drifted.
3. **`matching-family-vacation-outfits`: first add tag `vacation` to 4 products, then set the rules to `tag = vacation AND tag = Family Matching`.** This removes 56 hidden products with 0 loss. Without the tag pre-step, 4 visible products are lost. `matching-hawaiian-outfits` gets `tag = hawaiian AND tag = Family Matching` and ends with 1 product.

Lower priority: `new-matching-outfits` and `popular-mommy-me-1` get the same edit as #1, but see the default-view flag.

## Flags and risks

- **Default-view loss on interleave hubs.** `new-matching-outfits`, `popular-mommy-me-1` (39 each) and `matching-outfits` (52) show the hidden products today in their default view. They are hidden only once a filter or another sort is applied, so the change removes products shoppers can currently see there. Mommy-and-me itself is sorted `MANUAL`, uses the filtered branch, and has no such loss.
- **Thin collections.** After the change `tops` and `matching-hawaiian-outfits` hold 1 product each. They already render only 1, but a 1-item collection linked from navigation looks broken.
- **Product decision on vacation and hawaiian.** The products being removed are real Mommy & Me and Daddy & Me beach items. For a "vacation" landing page, the alternative is a theme exemption like `family-pajamas`, which would keep all 104 visible. That is a theme change and outside this packet.
- **Stale smart-collection index.** 6 family tops/sweaters without a `Mommy and Me` tag are still members of the mommy hubs and `tops`. This was first noted in the 2026-09-26 issue-10 worklog. Any rule edit forces re-evaluation and removes them; they are included in the hidden counts.
- **Future products.** Under the new mommy rule, a product tagged both `Mommy and Me` and `Family Matching` is excluded even if its title does not say "family matching". Today there are 0 such visible products, all 33 triple-tagged items are already hidden, and the product data is consistent: every product carrying both tags has `category1 = Family Matching`.
- **Manual order.** `mommy-and-me` (MANUAL) loses positions 426–479 of 479 (the tail), so the visible order does not change. In `pajamas` (MANUAL) the 17 removed items sit at the top of the manual list, which is why page 1 had only 22 cards. Both full orders are in the JSON (`manual_order_before`).

## Side effects

- **feeds**: ops/cloudflare/merchant-feed-worker reads productType and tags per product; no collection membership or collection URL is used. Rule edits do not change feed rows. The optional "vacation" tag pre-step is not in any feed tag map.
- **ads_landing_pages**: grep of ops/marketing + ops/cloudflare: /collections/mommy-and-me, /collections/pajamas, /collections/matching-outfits appear only in keyword_universe.csv (LOCAL_ONLY_VALIDATE_NOT_UPLOADED / HOLD) and historical logs. No reference to new-matching-outfits, popular-mommy-me-1, tops, sweaters, matching-family-vacation-outfits, matching-hawaiian-outfits. LIVE_READBACK_REQUIRED: confirm live Google Ads / Pinterest final URLs before applying.
- **interleave_branch**: sections/main-collection-product-grid.liquid skips the snippet for mommy/family hubs when sort is created-descending and no filter is set, so those hubs show every published member in the default view.
- **stale_index**: 6 family tops/sweater without a "Mommy and Me" tag are still members of mommy-and-me, new-matching-outfits, popular-mommy-me-1, tops (and 1 in sweaters). Any rule edit forces re-evaluation and removes them.

## Per-collection detail

### `mommy-and-me` — Mommy and Me Matching Outfits for Mother and Daughter

- Collection `gid://shopify/Collection/320794427489` · SMART · sort `MANUAL` · Admin productsCount 479 (all statuses) · published 146 · visible 107 · hidden 39
- Rules now (ANY): TAG EQUALS "Mommy and Me"
- Live render: label `146 products`, cards per page [36, 36, 35, 0, 0]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A tag!=FM: after 107, removes hidden 39, visible loss 0, adds 0
  - B title!~family matching: after 104, removes hidden 39, visible loss 3 ['matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids', 'matching-family-tropical-floral-beach-outfits-navy-and-orange-flower-print-dresses-shirts-set', 'royal-blue-high-neck-halter-swimsuit-set-with-paisley-print-bottoms-elegant-family-beachwear'], adds 0
  - C cat1=MM: after 107, removes hidden 39, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Mommy and Me"; TAG NOT_EQUALS "Family Matching"
- Diff: published 146 → 107; removed 39; visible loss 0; added 0
- Flag: MANUAL sort: removed products sit at positions 426-479 of the 479-row manual order (all at the end), so remaining order is unchanged. Rollback via rule restore re-adds them; re-apply manual_order_before with collectionReorderProducts if exact positions matter.
- Flag: Also clears the 6 stale-index members (family tops with no "Mommy and Me" tag) because a rule edit forces re-evaluation.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/320794427489",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/320794427489",ruleSet:{appliedDisjunctively:true,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"}]}}){collection{id productsCount{count}} userErrors{field message}}}` then re-apply `manual_order_before` with `collectionReorderProducts` if exact positions matter.

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `jingle-bells-santa-family-matching-sweaters` | 9473193377889 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 2 | `santa-hat-reindeer-family-matching-sweaters` | 9473193148513 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 3 | `nordic-heart-reindeer-family-matching-sweaters` | 9473153826913 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 4 | `ho-ho-santa-family-matching-sweaters` | 9473153794145 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 5 | `santa-tree-delivery-family-matching-sweaters` | 9473153761377 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 6 | `candy-cane-reindeer-family-matching-sweaters` | 9473153728609 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 7 | `nordic-reindeer-family-matching-sweaters` | 9473153630305 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 8 | `reindeer-string-lights-family-matching-sweaters` | 9473153433697 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 9 | `reindeer-row-family-matching-sweaters` | 9473153335393 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 10 | `christmas-stocking-family-matching-sweaters` | 9473153269857 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 11 | `santa-tree-topper-family-matching-sweaters` | 9473152647265 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 12 | `snowflake-reindeer-family-matching-onesie-pajamas` | 9473151696993 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 13 | `polar-bear-christmas-family-matching-sweaters` | 9473017643105 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 14 | `christmas-reindeer-family-matching-sweaters` | 9473017348193 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 15 | `trick-or-treat-family-matching-pajamas` | 9473013448801 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 16 | `boo-stripe-family-matching-pajamas` | 9473003323489 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 17 | `beanie-ghost-family-matching-pajamas` | 9472997720161 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 18 | `pumpkin-ghost-family-matching-pajamas` | 9472970096737 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 19 | `spooky-skeleton-family-matching-onesie-pajamas` | 9472933757025 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 20 | `together-heart-family-matching-sweaters` | 7672336646241 | Family Matching | Family Matching | Matching Family Sweaters | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 21 | `playful-cat-parade-family-matching-tops` | 7670746775649 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 22 | `midnight-paint-splash-family-matching-tops` | 7670743498849 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 23 | `sky-daisy-doodle-family-matching-tops` | 7670742777953 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 24 | `coastal-banana-leaf-family-matching-tops` | 7670738223201 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 25 | `monochrome-palm-family-matching-tops` | 7670724329569 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 26 | `sunshine-daisy-family-matching-set` | 7585980055649 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sets | has "Family Matching" tag and title/handle says family matching |
| 27 | `sky-blue-family-matching-set` | 7585867628641 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sets | has "Family Matching" tag and title/handle says family matching |
| 28 | `sunset-ombre-family-matching-set` | 7585867432033 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sets | has "Family Matching" tag and title/handle says family matching |
| 29 | `classic-red-plaid-family-matching-pajamas` | 9473583087713 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 30 | `evergreen-fair-isle-family-matching-pajamas` | 9473584529505 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 31 | `jolly-crew-family-matching-pajamas` | 9473584922721 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 32 | `joyful-merry-blessed-family-matching-pajamas` | 9473586266209 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 33 | `let-it-snow-family-matching-pajamas` | 9473586561121 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 34 | `lights-out-reindeer-family-matching-pajamas` | 9473586626657 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 35 | `plaid-reindeer-family-matching-pajamas` | 9473586659425 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 36 | `plaid-tree-trio-family-matching-pajamas` | 9473586692193 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 37 | `snowy-village-stripes-family-matching-pajamas` | 9473588494433 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 38 | `we-are-family-evergreen-family-matching-pajamas` | 9473588592737 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 39 | `we-are-family-red-family-matching-pajamas` | 9473588658273 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |

### `new-matching-outfits` — New Mommy & Me

- Collection `gid://shopify/Collection/33120387169` · SMART · sort `CREATED_DESC` · Admin productsCount 479 (all statuses) · published 146 · visible 107 · hidden 39
- Rules now (ANY): TAG EQUALS "Mommy and Me"
- Live render: label `146 products`, cards per page [36, 36, 36, 36, 2]. default view uses the interleave branch, which does not call the visibility snippet: all published members render; hiding applies only when a filter or non-default sort is active (verified: price-ascending renders 107)
- Candidates tested:
  - A tag!=FM: after 107, removes hidden 39, visible loss 0, adds 0
  - B title!~family matching: after 104, removes hidden 39, visible loss 3 ['matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids', 'matching-family-tropical-floral-beach-outfits-navy-and-orange-flower-print-dresses-shirts-set', 'royal-blue-high-neck-halter-swimsuit-set-with-paisley-print-bottoms-elegant-family-beachwear'], adds 0
  - C cat1=MM: after 107, removes hidden 39, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Mommy and Me"; TAG NOT_EQUALS "Family Matching"
- Diff: published 146 → 107; removed 39; visible loss 0; added 0
- Flag: VISIBLE LOSS IN DEFAULT VIEW: CREATED_DESC + no filter uses the interleave branch, which shows all 146 today. The 39 removed products are visible there now (they are hidden only under filters/other sorts).
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/33120387169",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/33120387169",ruleSet:{appliedDisjunctively:true,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

Hidden products: identical to `mommy-and-me` (same rule, same 146 members).

### `popular-mommy-me-1` — Popular Mommy & Me

- Collection `gid://shopify/Collection/92758114401` · SMART · sort `CREATED_DESC` · Admin productsCount 479 (all statuses) · published 146 · visible 107 · hidden 39
- Rules now (ANY): TAG EQUALS "Mommy and Me"
- Live render: label `146 products`, cards per page [36, 36, 36, 36, 2]. default view uses the interleave branch, which does not call the visibility snippet: all published members render; hiding applies only when a filter or non-default sort is active (verified: price-ascending renders 107)
- Candidates tested:
  - A tag!=FM: after 107, removes hidden 39, visible loss 0, adds 0
  - B title!~family matching: after 104, removes hidden 39, visible loss 3 ['matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids', 'matching-family-tropical-floral-beach-outfits-navy-and-orange-flower-print-dresses-shirts-set', 'royal-blue-high-neck-halter-swimsuit-set-with-paisley-print-bottoms-elegant-family-beachwear'], adds 0
  - C cat1=MM: after 107, removes hidden 39, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Mommy and Me"; TAG NOT_EQUALS "Family Matching"
- Diff: published 146 → 107; removed 39; visible loss 0; added 0
- Flag: VISIBLE LOSS IN DEFAULT VIEW: same interleave behaviour as new-matching-outfits (39 products visible today in default view).
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/92758114401",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/92758114401",ruleSet:{appliedDisjunctively:true,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

Hidden products: identical to `mommy-and-me` (same rule, same 146 members).

### `pajamas` — Pajamas

- Collection `gid://shopify/Collection/240129605` · SMART · sort `MANUAL` · Admin productsCount 84 (all statuses) · published 39 · visible 22 · hidden 17
- Rules now (ALL): TAG EQUALS "Mommy and Me"; TAG EQUALS "Pajamas"
- Live render: label `39 products`, cards per page [22, 0]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A: after 22, removes hidden 17, visible loss 0, adds 0
  - B: after 22, removes hidden 17, visible loss 0, adds 0
  - C: after 22, removes hidden 17, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Mommy and Me"; TAG EQUALS "Pajamas"; TAG NOT_EQUALS "Family Matching"
- Diff: published 39 → 22; removed 17; visible loss 0; added 0
- Flag: MANUAL sort: the 17 hidden family pajama sets occupy the top manual positions (1..), which is why page 1 shows 22 and page 2 is empty. After the change the 22 Mommy & Me pajamas keep their relative order.
- Flag: keyword_universe.csv rows "matching family pajamas" and "family holiday pajamas" (LOCAL_ONLY, not uploaded) point to /collections/pajamas; reroute to /collections/family-pajamas.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240129605",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:EQUALS,condition:"Pajamas"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240129605",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:EQUALS,condition:"Pajamas"}]}}){collection{id productsCount{count}} userErrors{field message}}}` then re-apply `manual_order_before` with `collectionReorderProducts` if exact positions matter.

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `beanie-ghost-family-matching-pajamas` | 9472997720161 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 2 | `pumpkin-ghost-family-matching-pajamas` | 9472970096737 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 3 | `boo-stripe-family-matching-pajamas` | 9473003323489 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 4 | `trick-or-treat-family-matching-pajamas` | 9473013448801 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 5 | `spooky-skeleton-family-matching-onesie-pajamas` | 9472933757025 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 6 | `snowflake-reindeer-family-matching-onesie-pajamas` | 9473151696993 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 7 | `classic-red-plaid-family-matching-pajamas` | 9473583087713 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 8 | `evergreen-fair-isle-family-matching-pajamas` | 9473584529505 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 9 | `jolly-crew-family-matching-pajamas` | 9473584922721 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 10 | `joyful-merry-blessed-family-matching-pajamas` | 9473586266209 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 11 | `let-it-snow-family-matching-pajamas` | 9473586561121 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 12 | `lights-out-reindeer-family-matching-pajamas` | 9473586626657 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 13 | `plaid-reindeer-family-matching-pajamas` | 9473586659425 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 14 | `plaid-tree-trio-family-matching-pajamas` | 9473586692193 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 15 | `snowy-village-stripes-family-matching-pajamas` | 9473588494433 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 16 | `we-are-family-evergreen-family-matching-pajamas` | 9473588592737 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |
| 17 | `we-are-family-red-family-matching-pajamas` | 9473588658273 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Pajamas | has "Family Matching" tag and title/handle says family matching |

### `tops` — Tops

- Collection `gid://shopify/Collection/240128197` · SMART · sort `CREATED_DESC` · Admin productsCount 43 (all statuses) · published 20 · visible 1 · hidden 19
- Rules now (ALL): TAG EQUALS "Tops"; TAG EQUALS "Mommy and Me"
- Live render: label `20 products`, cards per page [1]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A: after 1, removes hidden 19, visible loss 0, adds 0
  - B: after 1, removes hidden 19, visible loss 0, adds 0
  - C: after 1, removes hidden 19, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Tops"; TAG EQUALS "Mommy and Me"; TAG NOT_EQUALS "Family Matching"
- Diff: published 20 → 1; removed 19; visible loss 0; added 0
- Flag: Collection becomes 1 product (it already renders 1). Consider hiding it from navigation; out of scope here.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240128197",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Tops"},{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240128197",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Tops"},{column:TAG,relation:EQUALS,condition:"Mommy and Me"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `jingle-bells-santa-family-matching-sweaters` | 9473193377889 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 2 | `santa-hat-reindeer-family-matching-sweaters` | 9473193148513 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 3 | `nordic-heart-reindeer-family-matching-sweaters` | 9473153826913 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 4 | `ho-ho-santa-family-matching-sweaters` | 9473153794145 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 5 | `santa-tree-delivery-family-matching-sweaters` | 9473153761377 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 6 | `candy-cane-reindeer-family-matching-sweaters` | 9473153728609 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 7 | `nordic-reindeer-family-matching-sweaters` | 9473153630305 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 8 | `reindeer-string-lights-family-matching-sweaters` | 9473153433697 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 9 | `reindeer-row-family-matching-sweaters` | 9473153335393 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 10 | `christmas-stocking-family-matching-sweaters` | 9473153269857 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 11 | `santa-tree-topper-family-matching-sweaters` | 9473152647265 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 12 | `polar-bear-christmas-family-matching-sweaters` | 9473017643105 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 13 | `christmas-reindeer-family-matching-sweaters` | 9473017348193 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 14 | `together-heart-family-matching-sweaters` | 7672336646241 | Family Matching | Family Matching | Matching Family Sweaters | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 15 | `playful-cat-parade-family-matching-tops` | 7670746775649 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 16 | `midnight-paint-splash-family-matching-tops` | 7670743498849 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 17 | `sky-daisy-doodle-family-matching-tops` | 7670742777953 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 18 | `coastal-banana-leaf-family-matching-tops` | 7670738223201 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |
| 19 | `monochrome-palm-family-matching-tops` | 7670724329569 | Family Matching | Family Matching | Matching Family Tops | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |

### `sweaters` — Coats & Sweaters

- Collection `gid://shopify/Collection/240153477` · SMART · sort `CREATED_DESC` · Admin productsCount 48 (all statuses) · published 19 · visible 5 · hidden 14
- Rules now (ALL): TAG EQUALS "Mommy and Me"; TAG EQUALS "Sweaters"
- Live render: label `19 products`, cards per page [5]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A: after 5, removes hidden 14, visible loss 0, adds 0
  - B: after 4, removes hidden 14, visible loss 1 ['matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids'], adds 0
  - C: after 5, removes hidden 14, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "Mommy and Me"; TAG EQUALS "Sweaters"; TAG NOT_EQUALS "Family Matching"
- Diff: published 19 → 5; removed 14; visible loss 0; added 0
- Flag: Title is "Coats & Sweaters". The 14 removed are family sweaters, which remain in family-sweaters (20).
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240153477",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:EQUALS,condition:"Sweaters"},{column:TAG,relation:NOT_EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/240153477",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Mommy and Me"},{column:TAG,relation:EQUALS,condition:"Sweaters"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `jingle-bells-santa-family-matching-sweaters` | 9473193377889 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 2 | `santa-hat-reindeer-family-matching-sweaters` | 9473193148513 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 3 | `nordic-heart-reindeer-family-matching-sweaters` | 9473153826913 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 4 | `ho-ho-santa-family-matching-sweaters` | 9473153794145 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 5 | `santa-tree-delivery-family-matching-sweaters` | 9473153761377 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 6 | `candy-cane-reindeer-family-matching-sweaters` | 9473153728609 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 7 | `nordic-reindeer-family-matching-sweaters` | 9473153630305 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 8 | `reindeer-string-lights-family-matching-sweaters` | 9473153433697 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 9 | `reindeer-row-family-matching-sweaters` | 9473153335393 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 10 | `christmas-stocking-family-matching-sweaters` | 9473153269857 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 11 | `santa-tree-topper-family-matching-sweaters` | 9473152647265 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 12 | `polar-bear-christmas-family-matching-sweaters` | 9473017643105 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 13 | `christmas-reindeer-family-matching-sweaters` | 9473017348193 | Family Matching | Mommy and Me, Daddy and Me, Family Matching | Matching Family Sweaters | has "Family Matching" tag and title/handle says family matching |
| 14 | `together-heart-family-matching-sweaters` | 7672336646241 | Family Matching | Family Matching | Matching Family Sweaters | category1='Family Matching' (family) != branch mommy and no "mommy and me" tag; has "Family Matching" tag and title/handle says family matching |

### `matching-outfits` — Family Matching Outfits

- Collection `gid://shopify/Collection/377555589` · SMART · sort `CREATED_DESC` · Admin productsCount 557 (all statuses) · published 79 · visible 27 · hidden 52
- Rules now (ANY): TYPE EQUALS "Bottoms"; TYPE CONTAINS "Coats"; TYPE EQUALS "Dresses"; TYPE EQUALS "Family Matching"; TYPE EQUALS "Pajamas"; TYPE EQUALS "Sweaters"; TYPE EQUALS "Swimsuits"; TYPE EQUALS "Tops"
- Live render: label `79 products`, cards per page [36, 36, 7]. default view uses the interleave branch, which does not call the visibility snippet: all published members render; hiding applies only when a filter or non-default sort is active (verified: price-ascending renders 27)
- Candidates tested:
  - A same as popular-family-matching: after 116, removes hidden 52, visible loss 0, adds 89
  - B type FM + tag FM: after 19, removes hidden 52, visible loss 8 ['family-matching-cable-knit-sweaters-heart-embroidered-unisex-pullovers', 'family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style', 'family-matching-red-cable-knit-cardigans-elegant-heart-button-design', 'family-matching-t-shirt-set-with-colorful-heart-brushstroke-design', 'matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids', 'matching-family-striped-cardigans-navy-and-red-heart-embroidery-knit-sweaters-for-mom-dad-and-kids', 'matching-family-striped-fleece-hoodies-cozy-winter-pullover-for-parents-and-kids', 'playful-graphic-family-matching-tops'], adds 0
  - C cat1=FM: after 116, removes hidden 52, visible loss 0, adds 89
- **Recommended (ALL conditions):** TAG EQUALS "Family Matching"
- Diff: published 79 → 116; removed 52; visible loss 0; added 89
  - Added (all Family Matching, all visible under the snippet): 89 products; full list in the JSON.
- Flag: VISIBLE LOSS IN DEFAULT VIEW: interleave branch shows all 79 today; the 52 Mommy & Me / Daddy & Me products leave the default view.
- Flag: Recommended rule ADDS 89 Family Matching products (all visible under the snippet) and makes the collection equal to popular-family-matching / new-women-outfits (116).
- Flag: keyword_universe.csv (LOCAL_ONLY, not uploaded) routes "mommy daughter vacation dresses", "daddy and me shirts", "dad son matching shirts", "dad and son vacation shirts" here; after the change those need /collections/mommy-and-me or /collections/daddy-me.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/377555589",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/377555589",ruleSet:{appliedDisjunctively:true,rules:[{column:TYPE,relation:EQUALS,condition:"Bottoms"},{column:TYPE,relation:CONTAINS,condition:"Coats"},{column:TYPE,relation:EQUALS,condition:"Dresses"},{column:TYPE,relation:EQUALS,condition:"Family Matching"},{column:TYPE,relation:EQUALS,condition:"Pajamas"},{column:TYPE,relation:EQUALS,condition:"Sweaters"},{column:TYPE,relation:EQUALS,condition:"Swimsuits"},{column:TYPE,relation:EQUALS,condition:"Tops"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `white-rosette-mommy-and-me-dresses` | 7535908946017 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 2 | `blue-tie-dye-butterfly-mommy-and-me-dresses` | 7535362015329 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 3 | `white-lace-mommy-and-me-dresses` | 7535320465505 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 4 | `lavender-mommy-and-me-floral-applique-sleeveless-ruffle-dress` | 7516479848545 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 5 | `mommy-and-me-french-halter-neck-tiered-dress-white-cotton-silk-sleeveless-a-line-beach-dress` | 7516369715297 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 6 | `father-son-matching-cotton-tropical-shirts-black-white-palm-print` | 7502836007009 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 7 | `matching-dad-son-cotton-hawaiian-shirts-palm-print-men-kids` | 7502828601441 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 8 | `matching-father-son-hawaiian-shirts-100-cotton-tropical-print` | 7502793179233 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 9 | `matching-dad-son-palm-print-cotton-button-up-shirt-pink-black` | 7502792949857 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 10 | `matching-men-s-boys-cotton-floral-button-down-shirts-green-daisy-print` | 7502792622177 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 11 | `men-s-cotton-floral-short-sleeve-button-up-shirt-navy-blue` | 7502791671905 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 12 | `men-s-short-sleeve-cotton-button-up-shirt-gray-paisley-print` | 7502791082081 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 13 | `navy-floral-cotton-short-sleeve-button-down-shirt-for-men-boys` | 7502790656097 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 14 | `men-s-boys-matching-hawaiian-shirt-tropical-leaf-rose-print-cotton-short-sleeve` | 7502771781729 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 15 | `men-s-kids-matching-hawaiian-shirt-blue-tropical-cotton-short-sleeve-button-up` | 7502771519585 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 16 | `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | 7502770896993 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 17 | `matching-dad-son-tropical-cotton-shirt-short-sleeve` | 7502770602081 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 18 | `men-s-boys-matching-tropical-floral-shirt-100-cotton-short-sleeve` | 7502770045025 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 19 | `matching-dad-son-navy-tropical-cotton-shirts` | 7502769193057 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 20 | `men-s-boys-matching-tropical-floral-cotton-short-sleeve-button-down-shirt` | 7502768439393 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 21 | `men-s-kids-matching-tropical-floral-cotton-shirt-short-sleeve-button-up-white-holiday-resort-print-dad-son` | 7502768210017 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 22 | `daddy-and-me-matching-floral-shirts-black-rose-print-short-sleeve-button-up-set` | 7502765949025 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 23 | `men-kids-matching-tropical-leaf-print-cotton-short-sleeve-shirt-cream-green` | 7502765719649 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 24 | `matching-father-son-tropical-floral-shirt-100-cotton-short-sleeve-button-up-teal-green` | 7502765097057 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 25 | `men-s-boys-cotton-hawaiian-shirt-tropical-leaf-print-short-sleeve-button-up-green-black` | 7502192214113 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 26 | `matching-dad-son-tropical-cotton-button-up-shirts-set-navy-leaf-print-short-sleeve` | 7502191788129 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 27 | `matching-dad-son-tropical-cotton-button-up-shirts-teal-palm-print` | 7502187888737 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 28 | `family-matching-dad-son-tropical-palm-cotton-shirts-blue` | 7502178222177 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 29 | `daddy-baby-matching-daddysaurus-and-babysaurus-t-shirt-set-fun-dinosaur-dad-and-baby-outfit` | 7230159618145 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 30 | `father-child-matching-striped-tie-t-shirt-set-dad-and-baby-toddler-outfits` | 7230159028321 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 31 | `daddy-me-beer-monster-milk-monster-matching-t-shirt-set` | 7230157226081 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 32 | `daddy-me-matching-family-t-shirt-set-heartfelt-father-child-bond-outfit` | 7230156701793 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 33 | `top-dad-and-top-son-matching-t-shirt-onesie-set-inspired-family-outfit` | 7230155882593 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 34 | `father-and-baby-matching-ctrl-c-ctrl-v-t-shirt-set-copy-and-paste-duo` | 7230151524449 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 35 | `father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set` | 7230150213729 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 36 | `father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift` | 7229835542625 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 37 | `father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads` | 7229828202593 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 38 | `father-baby-matching-big-trouble-and-little-trouble-t-shirt-onesie-set-playful-family-outfit` | 7229825581153 | Daddy and Me | Daddy and Me | Family Matching | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 39 | `mother-daughter-matching-navy-knit-cardigan-set-gingham-ruffle-trim-bow-accent` | 7229132472417 | Mommy and Me | Mommy and Me | Sweaters | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 40 | `stylish-blue-sleeveless-mommy-and-me-dress-set-with-bow-detail-perfect-for-summer-outings` | 7229027876961 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 41 | `elegant-floral-off-shoulder-mommy-and-me-dress-set-perfect-for-summer-outings` | 7229026304097 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 42 | `cute-matching-mom-and-daughter-cartoon-pajama-set-fun-and-cozy-sleepwear` | 7228788867169 | Mommy and Me | Mommy and Me | Pajamas | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 43 | `mother-daughter-matching-summer-dresses-vibrant-printed-sleeveless-maxi-dresses` | 7227630649441 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 44 | `matching-mother-and-daughter-beach-dresses-elegant-cream-chiffon-maxi-dress-set` | 7227438530657 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 45 | `matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids` | 7227435450465 | Mommy and Me | Mommy and Me | Sweaters | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 46 | `matching-mother-and-daughter-heart-knit-cardigans-cream-and-black-sweaters-for-mommy-me` | 7227434958945 | Mommy and Me | Mommy and Me | Sweaters | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 47 | `matching-mommy-me-tiered-smocked-dresses-elegant-puff-sleeve-dress-set` | 7227374534753 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 48 | `matching-mommy-me-colorful-watercolor-maxi-dresses-sleeveless-summer-dress` | 7227356282977 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 49 | `matching-mommy-me-smocked-sundresses-vibrant-floral-and-patterned-summer-dresses` | 7227270791265 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 50 | `matching-mommy-me-sunflower-maxi-dresses-sleeveless-floral-print-summer-dress` | 7227270299745 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 51 | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | 7227254276193 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 52 | `mommy-and-me-matching-pink-sleeveless-summer-dress-elegant-sundress-for-mother-daughter` | 7227252670561 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |

### `matching-family-vacation-outfits` — Matching Family Vacation Outfits

- Collection `gid://shopify/Collection/353856880737` · SMART · sort `BEST_SELLING` · Admin productsCount 252 (all statuses) · published 104 · visible 48 · hidden 56
- Rules now (ANY): TAG EQUALS "vacation"; TAG EQUALS "beach"; TAG EQUALS "resort"
- Live render: label `104 products`, cards per page [14, 17, 17]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A vacation+FM: after 44, removes hidden 56, visible loss 4 ['blue-tropical-floral-family-matching-beach-dress-and-shirt-set', 'matching-family-beach-outfits-with-floral-dresses-and-shorts', 'tropical-floral-family-matching-shirt-and-dress-outfit-set', 'tropical-palm-floral-family-matching-shirt-and-dress-set'], adds 0
  - B beach+FM: after 31, removes hidden 56, visible loss 17 ['black-white-spelling-family-matching-tops', 'blue-apricot-heart-family-matching-tops', 'blue-monstera-citrus-family-matching-tops', 'bright-paint-splash-family-matching-tops', 'coastal-banana-leaf-family-matching-tops', 'coastal-blue-stripe-family-matching-set', 'denim-blue-family-matching-set', 'midnight-paint-splash-family-matching-tops', 'midnight-palm-blossom-family-matching-tops', 'monochrome-palm-family-matching-tops', 'playful-cat-parade-family-matching-tops', 'playful-graphic-family-matching-tops', 'sky-daisy-doodle-family-matching-tops', 'summer-plaid-family-matching-set', 'sunlit-tropical-bloom-family-matching-tops', 'trail-plaid-family-matching-set', 'willow-wildflower-family-matching-set'], adds 0
- **Recommended (ALL conditions):** TAG EQUALS "vacation"; TAG EQUALS "Family Matching"
- Diff: published 104 → 44; removed 60; visible loss 4; added 0
- Pre-step for zero loss: add tag `vacation` to `blue-tropical-floral-family-matching-beach-dress-and-shirt-set` (7505375232097), `matching-family-beach-outfits-with-floral-dresses-and-shorts` (7510267494497), `tropical-floral-family-matching-shirt-and-dress-outfit-set` (7505372282977), `tropical-palm-floral-family-matching-shirt-and-dress-set` (7505374838881).
- Flag: Candidate A alone drops 4 visible products that have Beach/Cruise but not "vacation" tags. Zero-loss path: first add tag "vacation" to those 4 (product tag write; "vacation" is not in the feed worker MATERIAL/PATTERN/final-sale tag maps), then apply A.
- Flag: Product decision: 56 Mommy & Me beach/vacation items leave a collection titled "Matching Family Vacation Outfits". Alternative is a theme-side exemption like family-pajamas (keeps 104 visible) — theme change, not in this packet.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/353856880737",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"vacation"},{column:TAG,relation:EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/353856880737",ruleSet:{appliedDisjunctively:true,rules:[{column:TAG,relation:EQUALS,condition:"vacation"},{column:TAG,relation:EQUALS,condition:"beach"},{column:TAG,relation:EQUALS,condition:"resort"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `matching-mom-child-one-shoulder-swimsuit` | 6718948147297 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 2 | `matching-mommy-and-me-hollow-out-bikini` | 6719764463713 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 3 | `mom-child-matching-two-piece-swimsuit` | 6718945034337 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 4 | `matching-mommy-me-sunflower-print-swimsuit` | 6719792873569 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 5 | `chic-family-tides-mother-daughter-matching-two-piece-swimsuit-with-skirt-vibrant-versatile-swimwear-collection` | 7109502566497 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 6 | `chic-color-block-one-piece-swimsuit-for-mother-daughter-vibrant-sleek-beachwear` | 7109267947617 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 7 | `matching-mommy-me-orange-print-swimsuit` | 6719774720097 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 8 | `chic-floral-ruffle-one-shoulder-swimsuit-for-women-and-girls-elegant-asymmetrical-swimwear-set-in-vibrant-tropics-print` | 7109122097249 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 9 | `pastel-bloom-mommy-and-me-dresses` | 7536086089825 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 10 | `chic-family-bonding-mother-daughter-matching-swimsuit-set-with-long-sleeved-cover-up` | 7109481431137 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 11 | `chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection` | 7109472288865 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 12 | `golden-daisy-mommy-and-me-set` | 7546613530721 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 13 | `polka-dot-mommy-and-me-dresses` | 7536988520545 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 14 | `mother-daughter-matching-swim-set-abstract-print-two-piece-high-waisted-bikini-with-wrap-skirt` | 7109986844769 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 15 | `mother-daughter-vibrant-two-piece-swimsuit-set-with-flowing-skirt-matching-family-swimwear-collection` | 7109517770849 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 16 | `chic-mother-daughter-two-piece-swimsuit-family-matching-swimwear-in-vibrant-colors` | 7109292130401 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 17 | `nautical-charm-flamingo-print-one-piece-swimsuits-for-mother-daughter` | 7109119705185 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 18 | `chic-two-piece-swimsuit-with-skirt-family-matching-swimwear-for-mother-and-daughter-available-in-blue-green-black` | 7109454135393 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 19 | `green-botanical-ruffle-mommy-and-me-dresses` | 7607760257121 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 20 | `blue-daisy-skirted-mommy-and-me-swimsuits` | 7577248596065 | Mommy and Me | Mommy and Me | Matching Family Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 21 | `ivory-dot-mommy-and-me-dresses` | 7537025613921 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 22 | `ivory-cascade-mommy-and-me-set` | 7536703012961 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 23 | `pink-lace-garden-mommy-and-me-dresses` | 7536696295521 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 24 | `powder-blue-mommy-and-me-set` | 7535944368225 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 25 | `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set` | 7109514395745 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 26 | `mommy-me-vibrant-duo-tone-one-piece-swimsuit-with-ring-accent-family-matching-swimwear-collection` | 7109443256417 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 27 | `modern-cow-print-tankini-swimsuit-set-for-mother-and-daughter-stylish-high-waisted-swimwear-with-ruffle-detail` | 7109123670113 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 28 | `elegant-long-sleeve-leopard-print-swimsuit-for-mother-and-daughter` | 7109083267169 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 29 | `chic-striped-one-piece-swimsuit-with-playful-ruffle-detail-a-duo-of-elegance-for-mother-daughter` | 7108992860257 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 30 | `white-crochet-mommy-and-me-set` | 7562834215009 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 31 | `navy-sprig-mommy-and-me-dresses` | 7670609346657 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 32 | `coral-blossom-mommy-and-me-dresses` | 7607764287585 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 33 | `red-tropical-leaf-mommy-and-me-dresses` | 7607762845793 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 34 | `ocean-bloom-mommy-and-me-dresses` | 7607760388193 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 35 | `pink-resort-ruffle-mommy-and-me-dresses` | 7607758422113 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 36 | `red-resort-mommy-and-me-set` | 7545373130849 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 37 | `scarlet-ruffle-mommy-and-me-set` | 7545279217761 | Mommy and Me | Mommy and Me | Matching Family Tops | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 38 | `pastel-watercolor-mommy-and-me-dresses` | 7537978933345 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 39 | `ivory-tiered-ruffle-mommy-and-me-dresses` | 7537369120865 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 40 | `red-gingham-mommy-and-me-set` | 7537366597729 | Mommy and Me | Mommy and Me | Matching Family Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 41 | `willow-mist-mommy-and-me-dresses` | 7537109991521 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 42 | `ruffle-hem-mommy-and-me-dresses` | 7537105961057 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 43 | `black-bow-mommy-and-me-set` | 7536988618849 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 44 | `ivory-bow-back-mommy-and-me-dresses` | 7536704520289 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 45 | `green-lace-garden-mommy-and-me-dresses` | 7536696328289 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 46 | `blush-garden-mommy-and-me-swimsuits` | 7536469639265 | Mommy and Me | Mommy and Me | Matching Family Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 47 | `ivory-ruffle-mommy-and-me-dresses` | 7536309141601 | Mommy and Me | Mommy and Me | Matching Family Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 48 | `white-lace-mommy-and-me-dresses` | 7535320465505 | Mommy and Me | Mommy and Me | Dresses | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 49 | `chic-two-piece-swimsuit-set-ruffle-detail-top-and-high-waisted-bottoms-in-four-vibrant-colors` | 7109298487393 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 50 | `chic-tropical-one-shoulder-ruffle-swimsuit-set-for-mother-and-daughter-vibrant-floral-pattern-with-comfort-stretch` | 7109125537889 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 51 | `mother-daughter-pastel-mermaid-scales-swimsuit-with-frill-detail` | 7109084807265 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 52 | `chic-tropical-floral-high-neck-swimsuit-set-for-women-and-girls-zippered-sleeveless-quick-dry-swimwear` | 7109072257121 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 53 | `elegant-tropical-high-waisted-swimsuit-set-for-mother-and-daughter-radiant-red-halter-neck-design` | 7108996530273 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 54 | `elegant-blue-and-white-floral-one-piece-swimsuit-timeless-style-for-mother-and-daughter` | 7108988764257 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 55 | `modern-monochrome-one-shoulder-swimsuit-with-animal-print-ruffle-elegant-poolside-duo-for-mother-and-child` | 7108986404961 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 56 | `chic-leopard-print-one-piece-swimsuit-with-ruffle-accent-timeless-mother-daughter-beachwear` | 7108984799329 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |

### `matching-hawaiian-outfits` — Matching Hawaiian Outfits for Family

- Collection `gid://shopify/Collection/353857077345` · SMART · sort `BEST_SELLING` · Admin productsCount 26 (all statuses) · published 9 · visible 1 · hidden 8
- Rules now (ALL): TAG EQUALS "hawaiian"
- Live render: label `9 products`, cards per page [1]. rendered handle set equals Python-evaluated visible set
- Candidates tested:
  - A hawaiian+FM: after 1, removes hidden 8, visible loss 0, adds 0
- **Recommended (ALL conditions):** TAG EQUALS "hawaiian"; TAG EQUALS "Family Matching"
- Diff: published 9 → 1; removed 8; visible loss 0; added 0
- Flag: Collection becomes 1 product (it already renders 1). The 8 removed are Mommy & Me / Daddy & Me hawaiian swimwear/sets; same product decision as vacation.
- Apply: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/353857077345",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"hawaiian"},{column:TAG,relation:EQUALS,condition:"Family Matching"}]}}){collection{id productsCount{count}} userErrors{field message}}}`
- Rollback: `mutation{collectionUpdate(input:{id:"gid://shopify/Collection/353857077345",ruleSet:{appliedDisjunctively:false,rules:[{column:TAG,relation:EQUALS,condition:"hawaiian"}]}}){collection{id productsCount{count}} userErrors{field message}}}`

| # | Handle | Product ID | category1 | Audience tags | product_type | Why hidden |
|---|---|---|---|---|---|---|
| 1 | `matching-family-tropical-floral-beach-outfits-navy-and-orange-flower-print-dresses-shirts-set` | 7227439546465 | Mommy and Me | Mommy and Me | Sets | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 2 | `father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear` | 7110356631649 | Daddy and Me | Daddy and Me | Swimwear | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 3 | `tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print` | 7110364856417 | Daddy and Me | Daddy and Me | Swimwear | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 4 | `father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print` | 7110362136673 | Daddy and Me | Daddy and Me | Swimwear | category1='Daddy and Me' (daddy) != branch family and no "family matching" tag |
| 5 | `chic-tropical-one-shoulder-ruffle-swimsuit-set-for-mother-and-daughter-vibrant-floral-pattern-with-comfort-stretch` | 7109125537889 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 6 | `chic-tropical-floral-high-neck-swimsuit-set-for-women-and-girls-zippered-sleeveless-quick-dry-swimwear` | 7109072257121 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 7 | `elegant-tropical-high-waisted-swimsuit-set-for-mother-and-daughter-radiant-red-halter-neck-design` | 7108996530273 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |
| 8 | `chic-tropical-ruffle-one-piece-swimsuit-lush-botanical-print-with-elegant-solid-trim-for-mother-child` | 7108962254945 | Mommy and Me | Mommy and Me | Swimwear | category1='Mommy and Me' (mommy) != branch family and no "family matching" tag |

## Owner steps (Admin UI equivalent)

For each collection: Admin → Products → Collections → open the collection → Conditions.
1. Set "Products must match" to **all conditions**.
2. Add the new condition, for example `Product tag` · `is not equal to` · `Family Matching`.
3. Save.
4. Check that the count on the live collection page equals the "after" number above.

For vacation, add the `vacation` tag to the 4 listed products before editing the rules. For `matching-outfits`, delete the 8 type rules and add `Product tag` · `is equal to` · `Family Matching`.

Verify afterwards: storefront `products.json` count equals the rendered card total, and the count label equals the visible cards on every page.

## Rollback

Each collection has an exact `rollback_mutation` (the prior rule set) above and in the JSON. Restoring the rules re-adds the removed products. For `MANUAL` collections, the re-added products may land in a different position; `manual_order_before` holds the full prior order to reapply with `collectionReorderProducts`. To roll back the vacation tag pre-step, remove the `vacation` tag from those 4 products.

## Evidence limits

- Evaluated against the 268 products published on the Online Store as of 2026-09-27. Draft and archived members also change membership but are never rendered.
- Tag matching is modelled case-insensitively, which reproduced live membership exactly.
- Ads and Pinterest final URLs were checked only against repo files, not live accounts: LIVE_READBACK_REQUIRED.