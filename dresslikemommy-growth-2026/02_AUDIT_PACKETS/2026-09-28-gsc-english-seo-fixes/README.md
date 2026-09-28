# GSC English SEO fixes (2026-09-28)

Owner request (chat): "fix all this! very important!" about a pasted 3-month Search Console brief (Jun 26 – Sep 25 2026). Session "English collection pages SEO ranking". Split with session "Family-matching collection SEO ranking", which owns matching-outfits, new-women-outfits, family-sets, daddy-me*, and the main menu.

## What GSC showed (read live 2026-09-28, 3 months)

| Query / page | Impr. | Pos | Clicks | Page Google used |
|---|---:|---:|---:|---|
| family matching shirts | 1,110 | 16.8 | 0 | heart T-shirt product (1,060), /collections/family-tops (55) |
| matching family shirts | 956 | 18 | 1 | same heart T-shirt product (753), family-tops (88) |
| mommy and me matching pajamas | 316 | 10.4 | 1 | non-www homepage (310); /collections/pajamas only 4 |
| Thanksgiving queries (25 variants) | 690 | 30.1 | 0 | a blog post dated "2016" recommending Christmas pajamas (654); no Thanksgiving collection existed |
| matching family sweaters | 286 | 26.5 | 1 | /collections/family-sweaters (272), so no cannibalization |
| /collections/couples | 3,380 | 40.9 | 3 | queries: his and hers matching clothes, men and women matching outfits, matching couple outfits |
| /collections/mommy-and-me | 3,700 | 50.9 | 3 | queries: mommy and me outfits/clothes/dresses |

Root cause found: `snippets/collection-seo-fallback.liquid` generates the H1, hero copy and guide on most collections, so admin descriptions never render. `/collections/pajamas` (mommy and me) showed the H1 "Matching Family Pajamas", the same as `/collections/family-pajamas`.

## Done (all LIVE_VERIFIED 2026-09-28)

1. **Theme `6c70aff` on main, synced to MAIN 133290917985 (0 drift).** Adds a new snippet `snippets/collection-guide-english-terms.liquid` and English-only hooks in `collection-seo-fallback` and `collection-seo-content`.
   - Title, H1, meta, lead and buyer guide for `couples`, `pajamas`, `family-tops`, `family-sweaters` and `thanksgiving-family-outfits`.
   - Live English H1s: Mommy and Me Pajamas, Family Matching Shirts & Tops, Matching Family Sweaters, Matching Couple Outfits, Matching Family Thanksgiving Outfits.
   - Localized pages (de/da/el checked) are unchanged. No Liquid errors, and canonicals are unchanged.
2. **Admin SEO title, meta and description** for the same 4 collections. Couples is special-cased in the theme to render its admin description; the new copy renders there.
3. **New collection** `/collections/thanksgiving-family-outfits` (id 364000444513).
   - Manual, 30 ACTIVE fall knits, plaid button-ups and sweatshirts.
   - Published to the Online Store.
4. **Heart T-shirt product SEO title** → "Matching Family Shirts – Minimalist Heart T-Shirts, 4 Colors".
5. **Thanksgiving blog post** `best-matching-outfits-for-thanksgiving-dinner` rewritten. The URL is kept.
   - New title, SEO title and description.
   - 8 current products; all 9 product links return 200.
   - Photo, sizing and order-early tips. Thanksgiving is Nov 26 2026, and the post points to each product page's delivery estimate.
6. **Link paragraph** to the new collection inserted in 4 other Thanksgiving/November posts.
7. **Grinch (trademark risk):** product blocks removed from 3 published posts that still featured archived Grinch products. The live pages now show 0 "grinch" mentions. The 6 Grinch products stay ARCHIVED; their URLs 301 to /collections/christmas-pajamas.
8. **GSC Request indexing:** all 6 changed URLs (Thanksgiving collection and post, family-tops, pajamas, family-sweaters, couples).

## Checked, no change needed

- **Non-www homepage:** `https://dresslikemommy.com/` returns 301 to www. GSC URL Inspection says "Page with redirect", with www as both the user and Google canonical. The www homepage canonical and og:url point to www. The impressions are Google reporting a redirected URL; nothing to fix.
- **sweaters vs family-sweaters:** GSC shows family-sweaters takes 272/286 impressions, so there is no cannibalization. The two pages target different terms (mommy and me vs family).
- **mommy-and-me:** the theme already forces the target title ("Mommy and Me Outfits – Matching Mother Daughter Clothes") and a buyer guide (released 2026-09-27, near the end of the GSC window). The gap is authority and links, not on-page copy.
- **Hindi/Spanish:** kept. Removing a language creates thousands of 404/redirect URLs, the same churn that caused the ranking collapse (seo.md D1). Decide per Shopify revenue by market, not CTR.

## Rollback

- Theme: `git revert 6c70aff`, then `python3 ops/scripts/sync_live_theme_from_main.py --apply`.
- Collections: restore `seo` and `descriptionHtml` from `collections_before.json`. Delete collection 364000444513.
- Product: restore the seo.title from `receipts_collections.json`.
- Articles: restore bodies from `receipts_articles.json` and `receipts_grinch_removal.json` (`before`/`before_body`). The original title of 559651979361 was "Best Matching Outfits for Thanksgiving Dinner"; delete the global.title_tag and description_tag metafields.

## Measure (external clock: Google recrawl)

Re-read GSC Performance for the same queries and pages 28 days after 2026-09-28. Expect position and CTR gains on the thanksgiving, shirts, pajamas and couples queries. Kill criterion: no position gain and 0 clicks by the Thanksgiving week.
