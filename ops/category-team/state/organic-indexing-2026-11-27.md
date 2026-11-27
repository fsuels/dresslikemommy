# Indexing of today's collections (Experto SEO, 2026-11-27, Search Console URL inspection + live reads)

| URL | Google | Google canonical | Last crawl |
| --- | --- | --- | --- |
| /collections/family-tops | indexed | same | 11-26 02:41 |
| /collections/family-sweaters | indexed | same | 11-23 |
| /collections/matching-family-sweatshirts | indexed | same | 11-26 16:46 |
| /collections/christmas-sweaters | indexed | same | 11-26 17:50 |
| /collections/mommy-and-me | indexed | same | 11-20 |
| /collections/maternity | indexed | same | 11-19 |
| /collections/dresses | NOT indexed: duplicate | /collections/mother-daughter-matching-dresses | 11-25 |
| /collections/mother-daughter-matching-dresses | indexed | same | 11-25 |
| /es/collections/matching-outfits | indexed | same | 11-23 |
| /de/collections/matching-outfits | NOT indexed: crawled, currently not indexed | declared self | 11-04 |
| /fr/collections/matching-outfits | indexed | same | 11-24 |
| /it/collections/matching-outfits | indexed | same | 11-25 03:07 |
| /nl/collections/matching-outfits | indexed | same | 11-25 14:50 |
| /ro/collections/christmas-sweaters | indexed | same | 11-25 |
| /ro/collections/matching-family-christmas-outfits | indexed | same | 11-23 |
| /sv/collections/matching-family-christmas-outfits | indexed | same | 11-24 |
| /cs/collections/matching-family-sweatshirts | indexed | same | 11-13 |

All crawls are older than today's changes. Other local versions (for example maternity in each language, sv dresses) were not inspected.

## Theme checks (live read: /collections/dresses, /de/collections/matching-outfits, /pt/collections/maternity)
- Canonical: self, with language prefix. No robots noindex.
- hreflang: x-default = English; 21 language codes; pt points to /pt (served as pt-BR). Language-only codes, no region codes. Nothing broken.
- Sitemap: the 10 handles are in the collection sitemap for en, es, de, fr, it, cs, ro, nl, sv.
- No theme change made: no clear defect.

## Indexing requests
- Accepted: /collections/family-tops.
- Refused: /collections/family-sweaters, "Quota Exceeded" (daily). Stopped; not requested: family-sweaters, matching-family-sweatshirts, christmas-sweaters, mommy-and-me, and /de/collections/matching-outfits. Retry after the daily reset.

## For decision (not changed)
1. Duplicate dresses collections: dresses (35 active) is wholly inside mother-daughter-matching-dresses (37). Google indexes the second in English. Today's English description and product-page links went to /collections/dresses. Menus link dresses twice and the other once. Swedish search traffic lands on /sv/collections/dresses, so a blanket canonical swap needs a per-language check first. Recommendation: after checking each language in Search Console, set one canonical per language (as the theme already does for daddy-and-me) and point the product links at the winner.
2. /de/collections/matching-outfits not indexed since the 11-04 crawl: request indexing after the quota resets.

## Dresses consolidation (commit 3760ced + Admin), done 2026-11-27
- Same dresses confirmed (35 of dresses are all inside the 37 of mother-daughter-matching-dresses).
- Theme: /collections/dresses declares canonical to /collections/mother-daughter-matching-dresses with the language prefix; product links, mega menu, breadcrumbs, journal links, hub cards, home category tile link and English title/description/intro point to the chosen collection. No redirect, nothing deleted.
- Admin: 2 menu items and 22 guides (437 translations) repointed, 0 outdated. Rollback: ops/organic/receipts/2026-11-27/dresses-consolidation/ and revert 3760ced.
- Same commit: it matching-outfits title/H1/description now "Vestiti coordinati".
- Release note: THEME_LOCK was taken over during the publish; another agent applied the files to the live theme. Read-only check 08:47Z: theme and locales equal main.
- Live read (6 loads): canonical correct on en, es, de /collections/dresses; chosen collection shows the new English title, H1 and intro, no link to the old URL on it or on a product page; it title correct. es and de /collections/dresses still show their own titles (expected, canonical only).

## Pending 2026-11-28 (after the indexing quota resets)
Request indexing: /collections/mother-daughter-matching-dresses, /de/collections/matching-outfits (reason given: crawled, currently not indexed; self canonical; last crawl 11-04), /collections/family-sweaters, /collections/matching-family-sweatshirts, /collections/christmas-sweaters, /collections/mommy-and-me.
