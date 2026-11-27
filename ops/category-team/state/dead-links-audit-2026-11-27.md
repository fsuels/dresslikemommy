# Dead collection / product link audit - 2026-11-27

Read-only audit. Sources: Shopify Admin GraphQL (collections, menus, articles, pages, products), theme source at origin/main (508a6c7), no storefront requests. Nothing was changed.

Method notes
- "Active published" = product status ACTIVE and published to the Online Store channel. Counts come from the first 250 products per collection; a value marked "+" is a lower bound (collection has more than 250 products).
- Theme guard: `snippets/collection-storefront-visible.liquid` already hides menu/search entries whose collection has `products_count < 1`, and `snippets/style-journal-internal-links.liquid` (lines ~354-390) swaps `family-swimsuits` out of the journal-article link cards. Those two paths are protected. Hard-coded HTML (homepage template text) is not.

## Totals

| Metric | Value |
|---|---|
| Collections total | 54 |
| Published to Online Store | 51 (unpublished: family-bundle-eligible, matching-family-pet-outfits, skirts-archived) |
| Empty-but-published (0 active published products) | 7: bottoms, family-swimsuits, jumpsuits, leggings, matching-couples-t-shirts, mini-dresses, rompers |
| Referenced and empty | 7 (only 1 is on the live storefront: family-swimsuits; the other 6 appear only in menus that nothing renders, see below) |
| Referenced and MISSING handle | 0 live. `family-matching-outfits` is only a last-resort fallback inside guarded Liquid (301 to matching-outfits exists); `family-matching` is a comment (301 exists) |
| Referenced and UNPUBLISHED | 0 |
| Collection links in 121 published articles + 20 pages | 0 broken (all targets exist with active products; `/collections/all` is built-in) |
| Product links in articles/pages | 727 links to 180 distinct products: 0 missing, 0 not active |

## Problems, most visible first

| # | Where | Target | Status | Best replacement |
|---|---|---|---|---|
| 1 | Homepage `templates/index.json` line 268, section footer_body ("Matching Family Sets" block), anchor text "matching beach swimsuits" | `/collections/family-swimsuits` | EMPTY (19 products, 0 active) | `swimsuits` (31 active) |
| 2 | Homepage same block, line 268, anchor "mother daughter matching dresses" | `/collections/formal-dresses` | OK but thin (1 active) and mismatched to the anchor text | `mother-daughter-matching-dresses` (37 active) |
| 3 | Main menu (`main-menu`) | all 15 items checked | OK, no problem | - |
| 4 | Footer menus (`footer-menu`, `-2`, `-3`) and `footer-group.json` | no collection links | OK | - |
| 5 | Mega-menu feature card `snippets/header-mega-menu-feature-card.liquid` lines 56 and 107 (matches `/collections/family-swimsuits`, or menu handle `family-swimsuits`) | `family-swimsuits` | EMPTY, but only reachable if a menu item points to it; the current `main-menu` does not | If the menu is ever re-added use `swimsuits` (31 active); otherwise remove the dead branch |
| 6 | Orphan menu `family-matching` item "Swimsuits" | `/collections/family-swimsuits` | EMPTY (menu is not used by header/footer) | `swimsuits` (31 active), or delete the menu |
| 7 | Orphan menu `mommy-me` item "Bottoms"; orphan menu `popular-pages` item "Bottoms" | `/collections/bottoms` | EMPTY (16 products, 0 active) | `pants` (2 active, thin) or remove the link |
| 8 | Orphan menu `bottoms` item "Leggings" | `/collections/leggings` | EMPTY (14, 0 active) | `pants` (2 active) or remove |
| 9 | Orphan menu `dresses` items "Jumpers", "Mini Dresses", "Rompers & Jumpsuits" | `/collections/jumpsuits`, `/collections/mini-dresses`, `/collections/rompers` | EMPTY (4, 22, 20 products, all 0 active) | `dresses` (37 active) or `mother-daughter-matching-dresses` (37 active); or remove |
| 10 | Orphan menu `couples` item "T-Shirts" | `/collections/matching-couples-t-shirts` | EMPTY (15, 0 active) | `couples` (59 active) |
| 11 | Collection pages / theme snippets | no hard-coded links to an empty collection found; `main-collection-product-grid`, `collection-empty-recovery`, `collection-hub-subcategory-cards`, cart and search all point to populated handles (matching-outfits 150+, swimsuits 31, pajamas 25, mommy-and-me 111+, new-arrivals 205+) | OK | - |
| 12 | Articles and pages (121 published articles, 20 pages) | no dead collection or product links; journal guide cards already swap out `family-swimsuits` | OK | - |

Notes on menus: the Admin API lists 20+ menus, but the theme renders only `main-menu` (header) and `footer-menu`, `footer-menu-2`, `footer-menu-3` (footer and help hub). Items 6-10 are therefore not shown to shoppers today; they are cleanup, not live dead ends. Items 1 and 2 are the only live broken or weak links.

## Empty-but-published collections that nothing live links to

These stay in the sitemap and can be indexed by Google as empty pages. Unpublish them, or repopulate them, or 301 to the replacement.

| Handle | Products (active) | Suggested 301 / replacement |
|---|---|---|
| bottoms | 16 (0) | pants (2 active) or tops-adjacent: mommy-and-me |
| leggings | 14 (0) | pants (2 active) |
| jumpsuits | 4 (0) | dresses (37 active) |
| rompers | 20 (0) | dresses (37 active) |
| mini-dresses | 22 (0) | dresses (37 active) |
| matching-couples-t-shirts | 15 (0) | couples (59 active) |
| family-swimsuits | 19 (0) | swimsuits (31 active); only after link #1 is fixed (no 301 exists for it today) |

Other low-stock published collections (not empty, for awareness): `best-sellers` shows 2 active in the first 250 of 521 products (lower bound; likely more), `formal-dresses` 1, `pants` 2.

Unpublished collections (family-bundle-eligible, matching-family-pet-outfits, skirts-archived) have no references in the theme, menus, articles or pages.

## Limits

Collection counts are capped at 250 products sampled. Theme was read from origin/main, not the live theme in Shopify; a theme published from another branch could differ. Dynamic handles built by string concatenation in Liquid were not resolved beyond the visible `collections['...']` lookups.
