# #10 approval packet — `/collections/mommy-and-me` default order (NOT EXECUTED)

Status: PREPARED, awaiting owner approval. No Admin mutation was run by lane L4.
Evidence: read-only Admin GraphQL via the Shopify connector, 2026-09-26; storefront `/collections/mommy-and-me/products.json`.

## Before-state (LIVE_VERIFIED 2026-09-26)
- Collection `gid://shopify/Collection/320794427489`, title "Mommy and Me Matching Outfits for Mother and Daughter", templateSuffix "" (default).
- Type: smart (automated). ruleSet: `appliedDisjunctively: true`, one rule `TAG EQUALS "Mommy and Me"`.
- `sortOrder: CREATED_DESC` (newest first). productsCount 455 (Admin); active products tagged "Mommy and Me": 134; storefront grid shows 136.
- Of the 134 active: **27 also carry the tag "Daddy and Me"** (dad-inclusive whole-family sets); 107 do not.
- Because the 20 newest products are the Sept-2026 Christmas/Halloween family sweaters and pajamas (all dad-inclusive), CREATED_DESC puts them first: storefront positions 1–20 are dad-inclusive family sets.
- Anomaly (owner check): some storefront members lack the "Mommy and Me" tag in Admin (e.g. `together-heart-family-matching-sweaters`, `playful-cat-parade-family-matching-tops`, `midnight-paint-splash-family-matching-tops`, `sky-daisy-doodle-family-matching-tops`, `coastal-banana-leaf-family-matching-tops`, `monochrome-palm-family-matching-tops`). They are family (adult + child) items without a "Daddy and Me" tag, so the proposal below does not move them. Either the collection index lags a tag edit or the tags differ from what the product query returned; readback before acting.

## Recommended change (Option A — reversible, keeps membership, SEO and ad landing URL intact)
Step 1 — switch the default order to manual:
```graphql
mutation SetManual($input: CollectionInput!) {
  collectionUpdate(input: $input) { collection { id sortOrder } userErrors { field message } }
}
```
Variables: `{"input": {"id": "gid://shopify/Collection/320794427489", "sortOrder": "MANUAL"}}`

Step 1b — readback: `{ collection(id:"gid://shopify/Collection/320794427489") { sortOrder products(first:25) { nodes { handle } } } }` — confirm the starting manual order (expected to follow the prior newest-first order; if it does not, stop and re-plan).

Step 2 — move the 27 dad-inclusive products to the end, keeping their relative order (moves apply in sequence; `newPosition` >= count places at the end):
```graphql
mutation Reorder($id: ID!, $moves: [MoveInput!]!) {
  collectionReorderProducts(id: $id, moves: $moves) { job { id done } userErrors { field message } }
}
```
Variables: [`issue10_reorder_variables.json`](issue10_reorder_variables.json) (27 moves, all `newPosition: "100000"`). Poll `job(id:)` until `done: true`.

Result: the grid opens with the 107 mom-and-child items (newest first: navy-sprig, coral-blossom, red-tropical-leaf dresses ...), and whole-family sets follow.
Trade-off: with MANUAL order, **new products are added at the end**, so future mom-and-child launches must be moved up (or re-run Step 2 for new dad-inclusive items).

### Dad-inclusive products moved to the end
| # | handle | product id |
|---|---|---|
| 1 | `jingle-bells-santa-family-matching-sweaters` | `9473193377889` |
| 2 | `santa-hat-reindeer-family-matching-sweaters` | `9473193148513` |
| 3 | `nordic-heart-reindeer-family-matching-sweaters` | `9473153826913` |
| 4 | `ho-ho-santa-family-matching-sweaters` | `9473153794145` |
| 5 | `santa-tree-delivery-family-matching-sweaters` | `9473153761377` |
| 6 | `candy-cane-reindeer-family-matching-sweaters` | `9473153728609` |
| 7 | `nordic-reindeer-family-matching-sweaters` | `9473153630305` |
| 8 | `reindeer-string-lights-family-matching-sweaters` | `9473153433697` |
| 9 | `reindeer-row-family-matching-sweaters` | `9473153335393` |
| 10 | `christmas-stocking-family-matching-sweaters` | `9473153269857` |
| 11 | `santa-tree-topper-family-matching-sweaters` | `9473152647265` |
| 12 | `snowflake-reindeer-family-matching-onesie-pajamas` | `9473151696993` |
| 13 | `polar-bear-christmas-family-matching-sweaters` | `9473017643105` |
| 14 | `christmas-reindeer-family-matching-sweaters` | `9473017348193` |
| 15 | `trick-or-treat-family-matching-pajamas` | `9473013448801` |
| 16 | `boo-stripe-family-matching-pajamas` | `9473003323489` |
| 17 | `beanie-ghost-family-matching-pajamas` | `9472997720161` |
| 18 | `pumpkin-ghost-family-matching-pajamas` | `9472970096737` |
| 19 | `spooky-skeleton-family-matching-onesie-pajamas` | `9472933757025` |
| 20 | `monster-bloom-family-matching-onesie-pajamas` | `9472866091105` |
| 21 | `sunshine-daisy-family-matching-set` | `7585980055649` |
| 22 | `sky-blue-family-matching-set` | `7585867628641` |
| 23 | `sunset-ombre-family-matching-set` | `7585867432033` |
| 24 | `matching-family-beach-outfits-with-floral-dresses-and-shorts` | `7510267494497` |
| 25 | `blue-tropical-floral-family-matching-beach-dress-and-shirt-set` | `7505375232097` |
| 26 | `tropical-palm-floral-family-matching-shirt-and-dress-set` | `7505374838881` |
| 27 | `tropical-floral-family-matching-shirt-and-dress-outfit-set` | `7505372282977` |

## Alternative (Option B — tighter membership, NOT recommended without SEO/ads review)
Make the collection "Mommy and Me AND NOT Daddy and Me":
`collectionUpdate(input: {id: "gid://shopify/Collection/320794427489", ruleSet: {appliedDisjunctively: false, rules: [{column: TAG, relation: EQUALS, condition: "Mommy and Me"}, {column: TAG, relation: NOT_EQUALS, condition: "Daddy and Me"}]}})`
This removes 27 products from a paid/organic landing collection, so it needs a paid-growth and feed check first. Rollback: restore `{appliedDisjunctively: true, rules: [{column: TAG, relation: EQUALS, condition: "Mommy and Me"}]}`.

## Rollback (Option A)
`collectionUpdate(input: {id: "gid://shopify/Collection/320794427489", sortOrder: CREATED_DESC})` — restores the exact prior default order. When the sort is not MANUAL, the manual positions are ignored. Theme sort URLs (`?sort_by=`) are not affected either way.

## Verification after execution
- Admin readback: `sortOrder == MANUAL`, and none of the 27 handles in `products(first:100)` positions 1–107.
- Storefront: `/collections/mommy-and-me/products.json?limit=24` shows no `*-family-matching-*` handles from the table in the first 24; check `/de/collections/mommy-and-me` too.

## Out-of-lane coordination
One writer per collection surface: claim `collection:mommy-and-me` in `ops/AGENT_COORDINATION.md` before executing (parent-owned file).
