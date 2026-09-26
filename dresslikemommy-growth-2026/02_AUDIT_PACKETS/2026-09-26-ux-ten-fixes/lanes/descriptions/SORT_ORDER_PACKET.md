# Collection default sort order — approval packet (Lane D)

Status: **PROPOSAL ONLY**. No collection, menu or theme writes were made. All data below is a read-only Admin GraphQL (API 2026-07) and storefront readback from 2026-09-26 (~19:00 UTC).

## 1. What was checked

- `/collections/all` default sort: **LIVE_VERIFIED** `title-ascending` ("Alphabetically, A-Z" is the `selected` option in the live sort `<select>`; `/collections/all/products.json` and the page's ItemList JSON-LD both start "Autumn Woodland Bunny", "Bamboo Garden Panda", "Beanie Ghost"). The canonical URL is `https://www.dresslikemommy.com/collections/all` and stays the same with `?sort_by=…` (verified).
- There is **no** collection with handle `all` in Admin (46 collections listed), so `/collections/all` is Shopify's built-in all-products page. Its sort can't be set anywhere in Admin.
- `/collections/family-pajamas` default: **LIVE_VERIFIED** `CREATED_DESC`. Position 1 is `snowflake-reindeer-family-matching-onesie-pajamas` (Christmas onesie, created 2026-09-25). The six Halloween pajamas follow at positions 2–7.
- Menus: read via GraphQL `menus` (18 menus). The main menu links NEW ARRIVALS, MOMMY & ME, DADDY & ME, COUPLES, MATERNITY and FAMILY MATCHING (with 8 children). Its "Shop" item points at `/`, and `snippets/header-mega-menu.liquid:96-98` rewrites it to `routes.all_products_collection_url` (`/collections/all`). So the alphabetical page is the store's main "Shop" destination.
- 45 of 46 collections are published to the Online Store (`skirts-archived` is not). "Live" below means ACTIVE products published to the Online Store. Admin `productsCount` also counts archived and draft products.

### Evidence that challenges "BEST_SELLING for broad collections"

The `BEST_SELLING` previews (Admin `collection.products(sortKey: BEST_SELLING)`, live products only) for broad collections put **summer** products first in late September:
- `mommy-and-me`: one-shoulder swimsuit, hollow-out bikini, two-piece swimsuit, sunflower maxi dress, …
- `new-women-outfits` (FAMILY MATCHING): Skyfade, Tropical Palm, Sunlit Floral sets, …
- `daddy-me`: five swim trunks, then short-sleeve floral shirts.

The existing `CREATED_DESC` already puts the 20 new Halloween/Christmas products first on those pages. The 2026-09-25 holiday products have no sales history yet, so switching broad collections to `BEST_SELLING` now would **hide** the Q4 assortment. Recommendation: keep broad collections on `CREATED_DESC` through Q4 and revisit `BEST_SELLING` in January 2027. Full previews: `data/best_selling_preview.json`.

## 2. `/collections/all` (built-in) — options

Before: built-in, `TITLE_ASC`. Target: `CREATED_DESC` (newest first) through Q4, matching `new-arrivals`.

**Option A — theme link change (recommended first; no Admin write; reversible by git).** Point the "Shop" nav link at the sorted URL. Patch in `snippets/header-mega-menu.liquid` line 98 (the file is not in any current claim; the parent applies it):
```liquid
-          assign nav_link_url = routes.all_products_collection_url
+          assign nav_link_url = routes.all_products_collection_url | append: '?sort_by=created-descending'
```
Optional, same pattern: the empty-cart buttons `sections/main-cart-items.liquid:32,39` (Lane C's file) and `snippets/cart-drawer.liquid:44`, plus `sections/main-404.liquid:45`.
- Risks: direct, organic and bookmarked visits to `/collections/all` stay alphabetical. The canonical ignores `sort_by` (verified), so there is no duplicate-URL SEO risk. Shoppers who pick another sort keep their own choice. Locale prefixes are kept because `routes.all_products_collection_url` is locale-aware.
- Rollback: revert the one line.

**Option B — Admin: create a real smart collection with handle `all` (controls every visit).** A collection with handle `all` takes over the built-in page. This is **EXPECTED** from Shopify's documented behavior and is **not verified on this store**, so treat the first apply as a test.
```graphql
mutation { collectionCreate(input: {
  title: "All Matching Outfits", handle: "all", sortOrder: CREATED_DESC,
  ruleSet: { appliedDisjunctively: false, rules: [{ column: VARIANT_PRICE, relation: GREATER_THAN, condition: "0" }] }
}) { collection { id handle sortOrder productsCount { count } } userErrors { field message } } }
# then publish it to Online Store: publishablePublish(id: <new id>, input: [{ publicationId: "gid://shopify/Publication/55169925" }])
```
- Risks:
  1. Membership now depends on the rule. A product priced 0, or a future rule edit, drops out of "all". The gift card (price > 0) is included, like today.
  2. It becomes an ordinary collection. It appears in `sitemap_collections`, `/collections` lists and Search & Discovery filter config, and it needs `title`/`body_html`/`meta_*` translations in the 20 non-primary locales. The theme h1 is safe: `snippets/collection-seo-fallback.liquid` keys "All Matching Outfits" by handle `all` with a locale key.
  3. The `all` handle is reserved-looking. If Shopify rejects it or suffixes it (`all-1`), stop: that proves the takeover path isn't available.
  4. Any app or feed that expects the built-in behavior.
- Rollback: `collectionDelete(input:{id})` on the created collection. Only this new object is removed, and the built-in page returns (EXPECTED). Unpublishing alone isn't a proven rollback.
- Readback: the `/collections/all` sort `<select>` shows `created-descending` selected, and the products.json first item is a 2026-09-25/26 product.

## 3. Seasonal MANUAL order — `family-pajamas` and `pajamas`

**Dependency / blocker:** another session may be editing the `family-pajamas` rules ("Family Matching Pajamas collection matching rule"). Current rule (read 2026-09-26, `updatedAt` 2026-09-25T21:00:57Z): `TYPE EQUALS "Matching Family Pajamas" AND TAG EQUALS "Pajamas"` (28 live). Apply this sort change only **after** that rule change lands and its membership is read back. Then re-read the member list, because manual positions only cover current members. **One writer per collection:** don't run this in parallel with the rules edit.

Before: `CREATED_DESC` on both (`family-pajamas` gid `Collection/140957614177`; `pajamas` gid `Collection/240129605`).
After: `MANUAL` with this top 8 (window 2026-09-26 → 2026-10-14):

| Pos | Handle | Product gid | Why |
|---|---|---|---|
| 1 | beanie-ghost-family-matching-pajamas | 9472997720161 | Halloween two-piece, whole family |
| 2 | pumpkin-ghost-family-matching-pajamas | 9472970096737 | Halloween two-piece |
| 3 | boo-stripe-family-matching-pajamas | 9473003323489 | Halloween two-piece |
| 4 | trick-or-treat-family-matching-pajamas | 9473013448801 | Halloween two-piece |
| 5 | spooky-skeleton-family-matching-onesie-pajamas | 9472933757025 | Halloween onesie |
| 6 | monster-bloom-family-matching-onesie-pajamas | 9472866091105 | Halloween onesie |
| 7 | snowflake-reindeer-family-matching-onesie-pajamas | 9473151696993 | Only live Christmas pajama; early Christmas shoppers |
| 8 | autumn-woodland-bunny-mommy-and-me-pajamas | 7533454098529 | Fall-tagged long-sleeve |

Positions 9+: the remaining long-sleeve/fall members (eucalyptus-bunny-gauze `7533454655585`, polar-adventure `7533453934689`, bamboo-garden-panda-cotton, red-panda), then the short-sleeve summer sets in their current order. `pajamas` has one extra member (`cute-matching-mom-and-daughter-cartoon-pajama-set-…`). Put it after position 8.

Why Oct 14: the storefront's delivery estimate is 12–16 days, so Halloween orders after about Oct 15 are unlikely to arrive in time. The same cutoff is in the worklog next action `HOLIDAY_ORDER_BY_BADGES_BEFORE_2026-10-05`.
**Scheduled second change (~2026-10-15):** move `snowflake-reindeer` (and any new Christmas pajamas) to position 1 and push the six Halloween products below the long-sleeve set. **After 2026-11-01:** set Halloween last.

Apply (per collection, after owner OK):
```graphql
mutation { collectionUpdate(input: { id: "gid://shopify/Collection/140957614177", sortOrder: MANUAL }) { collection { sortOrder } userErrors { message } } }
mutation { collectionReorderProducts(id: "gid://shopify/Collection/140957614177", moves: [
  { id: "gid://shopify/Product/9472997720161", newPosition: "0" }, { id: "gid://shopify/Product/9472970096737", newPosition: "1" },
  { id: "gid://shopify/Product/9473003323489", newPosition: "2" }, { id: "gid://shopify/Product/9473013448801", newPosition: "3" },
  { id: "gid://shopify/Product/9472933757025", newPosition: "4" }, { id: "gid://shopify/Product/9472866091105", newPosition: "5" },
  { id: "gid://shopify/Product/9473151696993", newPosition: "6" }, { id: "gid://shopify/Product/7533454098529", newPosition: "7" } ]) { job { id } userErrors { message } } }
```
Repeat with `gid://shopify/Collection/240129605` for `pajamas`. `collectionReorderProducts` is asynchronous, so poll `job(id){done}` before the readback.
- Readback: `/collections/family-pajamas/products.json?limit=8` returns the eight handles in order, and the live sort `<select>` shows `manual` ("Featured") selected.
- Risks: MANUAL needs upkeep. New matching products are added at the end, so a new Christmas pajama launched in October won't surface until someone reorders. The two scheduled follow-ups above are required, or the order goes stale the same way the current one did.
- Rollback: `collectionUpdate(input:{id, sortOrder: CREATED_DESC})` on each. Manual positions are ignored once the sort isn't MANUAL.
- Credible alternative: keep `CREATED_DESC` and accept the Christmas onesie at #1 (Halloween is still #2–#7). It needs zero upkeep but gives up about 3 weeks of Halloween-first merchandising.

## 4. `new-pajama-drop` and the hardcoded "latest 19 arrivals"

`new-pajama-drop` (gid `Collection/355463725153`) is a MANUAL-membership collection of 19 April 2026 pajamas. None of the 7 September pajamas are in it. Every English pajama PDP says "Looking for the newest prints first? Shop the New Pajama Drop with the latest 19 arrivals in one edit." (`snippets/product-internal-links.liquid:72`, English-only branch). The count is hardcoded, and the "newest" claim is now false. The theme patch is in `INTEGRATION.md`. Membership refresh (optional, owner decision): `collectionAddProducts` with the 7 new pajama gids, or retire the link.

## 5. Adjacent findings (no action in this packet)

- Main-menu collections with **0 live products**: `maternity` (MATERNITY top-level item) and `family-swimsuits` (FAMILY MATCHING › Swimsuits). Also 0: `bottoms`, `leggings`, `mini-dresses`, `rompers`, `jumpsuits` (secondary menus). Shoppers land on empty grids.
- `christmas-pajamas` has 1 live product (41 others archived or draft; Snowflake Reindeer is the only live Christmas pajama) and `christmas-tops` has 1. Neither is in a menu, but both are thin landing pages if anything links to them.
- `couples` (main menu) has 2 live products.

## 6. Full table (all 46 collections, before → proposed)

| Handle | Title | Type | Before `sortOrder` | Proposed | Live / all products | Menus | Reason |
|---|---|---|---|---|---|---|---|
| `all` (built-in) | All Matching Outfits (theme title) | built-in | TITLE_ASC (Alphabetically, A-Z; LIVE_VERIFIED) | CREATED_DESC via one of the §2 options (**change**) | all published | main-menu "Shop" (theme rewrites the link) | Alphabetical order puts "Autumn Woodland Bunny" first; newest-first matches the Q4 holiday focus. |
| `new-matching-outfits` | New Mommy & Me | smart | CREATED_DESC | CREATED_DESC (keep) | 136 / 455 | new-arrivals | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `mommy-and-me` | Mommy and Me Matching Outfits for  | smart | CREATED_DESC | CREATED_DESC (keep) | 136 / 455 | main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `new-arrivals` | New Arrivals | smart | CREATED_DESC | CREATED_DESC (keep) | 134 / 584 | main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `new-women-outfits` | Family Matching Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 106 / 295 | main-menu, new-arrivals | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `popular-family-matching` | Popular Family Matching Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 106 / 295 | best-sellers | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `matching-family-vacation-outfits` | Matching Family Vacation Outfits | smart | BEST_SELLING | BEST_SELLING (keep) | 104 / 252 | main-menu | No change: already BEST_SELLING. |
| `matching-outfits` | Family Matching Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 79 / 557 | primary-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `family-tops` | Family Matching Tops | smart | CREATED_DESC | CREATED_DESC (keep) | 49 / 78 | family-matching, main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `daddy-me` | Daddy & Me Matching Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 45 / 64 | main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `family-sets` | Family Matching Sets | smart | CREATED_DESC | CREATED_DESC (keep) | 43 / 88 | family-matching, main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `dresses` | Dresses | smart | CREATED_DESC | CREATED_DESC (keep) | 37 / 134 | mommy-me, popular-pages | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `mother-daughter-matching-dresses` | Mother Daughter Matching Dresses | smart | CREATED_DESC | CREATED_DESC (keep) | 37 / 134 | main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `swimsuits` | Mother Daughter Swimsuits | smart | CREATED_DESC | CREATED_DESC (keep) | 35 / 110 | mommy-me, popular-pages | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `pajamas` | Pajamas | smart | CREATED_DESC | MANUAL (**change**) | 29 / 60 | main-menu, mommy-me, popular-pages | Same seasonal order as family-pajamas (28 of its 29 live products are shared). |
| `family-pajamas` | Family matching Pajamas | smart | CREATED_DESC | MANUAL (**change**) | 28 / 28 | family-matching | Seasonal: Halloween first until Oct 14, then Christmas first (see §3). Blocked on the peer rules edit. |
| `sundresses` | Sundresses | smart | CREATED_DESC | CREATED_DESC (keep) | 25 / 40 | dresses | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `tops` | Tops | smart | CREATED_DESC | CREATED_DESC (keep) | 20 / 43 | mommy-me, popular-pages | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `family-sweaters` | Family Matching Sweaters & Jackets | smart | CREATED_DESC | CREATED_DESC (keep) | 20 / 56 | family-matching, main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `sweaters` | Coats & Sweaters | smart | CREATED_DESC | CREATED_DESC (keep) | 19 / 48 | mommy-me, popular-pages | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `midi-dresses` | Midi Dresses | smart | CREATED_DESC | CREATED_DESC (keep) | 17 / 56 | dresses | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `maxi-dresses` | Maxi Dresses | smart | CREATED_DESC | CREATED_DESC (keep) | 15 / 28 | dresses | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `trunks` | Trunks | smart | CREATED_DESC | CREATED_DESC (keep) | 12 / 16 | daddy-me | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `daddy-me-t-shirts` | Daddy & Me T-Shirts | smart | CREATED_DESC | CREATED_DESC (keep) | 11 / 13 | daddy-me | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `matching-hawaiian-outfits` | Matching Hawaiian Outfits for Fami | smart | BEST_SELLING | BEST_SELLING (keep) | 9 / 26 | main-menu | No change: already BEST_SELLING. |
| `pants` | Pants | smart | CREATED_DESC | CREATED_DESC (keep) | 2 / 5 | bottoms | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `couples` | Matching Couples Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 2 / 19 | main-menu | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `formal-dresses` | Formal Dresses | smart | BEST_SELLING | BEST_SELLING (keep) | 1 / 8 | dresses | No change: already BEST_SELLING. |
| `jumpsuits` | Jumpsuits | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 4 | dresses | No change: 0 live products (see §5 empty-collection finding). |
| `mini-dresses` | Mini Dresses | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 22 | dresses | No change: 0 live products (see §5 empty-collection finding). |
| `rompers` | Mother Daughter Rompers & Jumpsuit | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 20 | dresses | No change: 0 live products (see §5 empty-collection finding). |
| `bottoms` | Bottoms | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 16 | mommy-me, popular-pages | No change: 0 live products (see §5 empty-collection finding). |
| `leggings` | Leggings | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 14 | bottoms | No change: 0 live products (see §5 empty-collection finding). |
| `maternity` | Maternity | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 20 | main-menu, mommy-me | No change: 0 live products (see §5 empty-collection finding). |
| `family-swimsuits` | Family Matching Swimsuits | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 19 | family-matching, main-menu | No change: 0 live products (see §5 empty-collection finding). |
| `popular-mommy-me-1` | Popular Mommy & Me | smart | CREATED_DESC | CREATED_DESC (keep) | 136 / 455 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `best-sellers` | Mommy and Me Matching Outfits – Dr | smart | BEST_SELLING | BEST_SELLING (keep) | 72 / 521 | — | No change: already BEST_SELLING. |
| `daddy-and-me` | Matching Daddy and Me Outfits | smart | CREATED_DESC | CREATED_DESC (keep) | 45 / 64 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `fall-winter` | Fall & Winter | smart | BEST_SELLING | BEST_SELLING (keep) | 27 / 217 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `daddy-me-shirts` | Daddy & Me Shirts | smart | CREATED_DESC | CREATED_DESC (keep) | 23 / 23 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `new-pajama-drop` | New Pajama Drop | manual | CREATED_DESC | CREATED_DESC (keep) | 19 / 19 | — | No change to sort; membership is a stale manual list (19 April pajamas). See §4. |
| `christmas-sweaters` | Christmas Sweaters | smart | CREATED_DESC | CREATED_DESC (keep) | 13 / 18 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `valentines-day-matching-outfits-1` | Valentine's Day Matching Outfits | smart | BEST_SELLING | BEST_SELLING (keep) | 3 / 4 | — | No change: already BEST_SELLING. |
| `skirts-archived` | Skirts | smart | CREATED_DESC | CREATED_DESC (keep) | 1 / 3 | — | No change: not on Online Store. |
| `christmas-tops` | Christmas Tops | smart | CREATED_DESC | CREATED_DESC (keep) | 1 / 14 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `christmas-pajamas` | Matching Family Christmas Pajamas | smart | CREATED_DESC | CREATED_DESC (keep) | 1 / 42 | — | Keep through Q4: BEST_SELLING preview surfaces summer swim/dresses first; CREATED_DESC surfaces the new holiday products. Revisit Jan 2027. |
| `matching-couples-t-shirts` | Matching Couples T-Shirts | smart | CREATED_DESC | CREATED_DESC (keep) | 0 / 15 | — | No change: 0 live products (see §5 empty-collection finding). |
