# Source-reference product tag cleanup — approval packet and execution (2026-09-26)

**Result: DONE, LIVE_VERIFIED.** The owner approved "All 59 products" in chat on 2026-09-26.
- `tagsRemove` ran on 59 products: 89 tags removed, 0 userErrors.
- Per-product readback: 0 matching tags remain and all other tags are preserved. Status is unchanged.
- Full re-scan of 859 products: 0 matches. Only the 59 target products changed.
- The 7 active products' public `/products/<handle>.js` show 0 matching tags.
- Redacted after-state: `after_state_redacted.json`.

Rule: AGENTS.md says to keep vendor/source URLs out of public fields. Product tags are public, because Shopify exposes them on `/products/<handle>.js` and `.json`. LIVE_VERIFIED 2026-09-26: `/products/father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set.js` returns the tag `offer/<12-digit id>.html`.

## Scan (read-only Admin GraphQL `2026-01`, all statuses)

- Scanned 859 products: 257 ACTIVE, 574 ARCHIVED, 28 DRAFT.
- Match (case-insensitive): `offer/`, `.html`, `1688`, `http`.
- Result: 59 products and 89 tags matched. There are 7 ACTIVE products with 1 tag each, 52 ARCHIVED products and 0 DRAFT products.
- A wider sweep also looked for `.htm`, `taobao`, `tmall`, `aliexpress`, `alibaba`, `item/`, `www.`, `.com`, `spm=` and bare IDs of 9 or more digits. It found no further tags.
- Tag shapes found:
  - `/offer/<12 digits>.html`: 48
  - `offer/<12 digits>.html`: 24
  - `/<12 digits>.html`: 10
  - Taobao item URL: 2
  - Tmall item URL: 1
  - `/offer/<12 digits>.htm`: 1
  - `/offer/<12 digits>.html?`: 1
  - `<12 digits>.html`: 1
  - `/item/<11 digits>.html`: 1

Exact tag strings are not stored in the repo. See `before_state_redacted.json` for per-product IDs, shapes and `sha256_12` hashes.

## ACTIVE products (7). Each removes exactly one tag, `offer/<12 digits>.html`, and it is the same ID on all 7.

| Handle | Title |
|---|---|
| father-baby-matching-big-trouble-and-little-trouble-t-shirt-onesie-set-playful-family-outfit | Daddy and Me Matching Shirts – Big Trouble and Little Trouble T-Shirt and Onesie Set |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | Daddy and Me Matching Shirts – Mr. Fix It and Mr. Broke It T-Shirt and Onesie Set |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | Daddy and Me Matching Shirts – Player 1 and Player 2 Gamer T-Shirt and Onesie Set |
| father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set | Daddy and Me Matching Shirts – Whole Pizza and Pizza Slice T-Shirt Set |
| daddy-baby-bestie-heart-matching-t-shirt-onesie-set-adorable-father-and-child-outfit | Daddy and Me Matching Shirts – Bestie Heart T-Shirt and Onesie Set |
| family-matching-original-remix-encore-t-shirt-set-fun-family-outfits-for-all-ages | Family Matching T-Shirts – Original, Remix and Encore Set |
| need-more-family-matching-drink-t-shirt-set-beer-coffee-milk-juice-family-outfit | Family Matching T-Shirts – Need More Beer, Coffee, Milk and Juice Set |

## ARCHIVED products (52, 82 tags)

These are listed in `before_state_redacted.json`. They are not reachable on the storefront while archived. The tags still leak through Admin exports, and they would leak publicly if a product is ever unarchived.

## Dependency check: nothing depends on these tags

- Smart collections: 49 collections, 48 of them smart. No rule condition contains `offer`, `html`, `1688`, `http` or the ID. Every TAG rule uses `EQUALS` on a merchandising tag.
- Merchant feed worker (`ops/cloudflare/merchant-feed-worker`): it reads tags only for an exact Final Sale match (`generator.js:73`), and it already drops tags that contain a URL (`collector.js:108-115`).
- Pinterest feed worker: it does not read product tags. It asserts that no supplier hostname appears in the source or output.
- Theme Liquid/JS: no `product.tags` logic matches these patterns. The existing `1688` references are brand/vendor guards, not tag logic.
- Not checked: Shopify-native Google & YouTube or Pinterest app field mappings. These are not repo-controlled, and the tags are not a documented custom-label source.

## Write plan (approved and executed)

- Mutation: `tagsRemove(id, tags)` per product. Only tags that match the regex in the live readback taken immediately before the write are removed. Other tags, and the title, status, SEO, variants and publications, are not touched.
- After-state: re-read tags on every product, and re-scan all products for matches. Expected: 0.
- Public check: `/products/<handle>.js` on the 7 active products shows 0 matching tags.
- Rollback: `tagsAdd` with the exact prior strings. These are saved locally outside the repo in the session scratchpad (`hits_before.json`) and are not committed.
