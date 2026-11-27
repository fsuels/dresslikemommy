# Search demand without a good landing page (Experto SEO, 2026-11-27)

Source: Search Console, last 28 days, queries sorted by impressions (first 230 rows), position 8-30, kids' pajama queries excluded.

| Query | Impr | Clicks | Pos | Google's landing page today |
| --- | --- | --- | --- | --- |
| matching family outfits | 2,662 | 4 | 11.2 | not checked in this unit (hub worked on 11-26) |
| family matching outfits | 2,636 | 12 | 11.6 | not checked in this unit |
| matching family christmas sweaters | 1,216 | 5 | 9.3 | not checked (Christmas hubs worked on 11-26) |
| mommy and me outfits | 1,035 | 2 | 14.5 | not checked |
| matching christmas sweaters for family | 788 | 2 | 8.6 | not checked |
| matching family shirts | 785 | 0 | 11.9 | one product (minimalist heart T-shirt) 744; family-tops 31 |
| family outfits | 480 | 2 | 8.8 | not checked |
| family matching shirts | 469 | 0 | 10.3 | one product 462; family-tops 9 |
| family matching sweaters | 425 | 4 | 11.0 | not checked |
| matching family sweaters | 402 | 4 | 12.9 | products, mainly Jingle Bells Santa |
| matching outfits for family | 277 | 0 | 15.3 | not checked |
| matching family outfits for pictures | 271 | 0 | 9.9 | not checked |
| beste weihnachtsoutfits für familienfotos | 267 | 0 | 8.9 | German card-photo guide (title already matches) |
| family matching holiday sweaters | 149 | 0 | 13.8 | not checked |
| family holiday sweaters | 133 | 1 | 9.2 | Jingle Bells Santa product 116 |

Also: matching family sweatshirts 115 (13.5) lands mainly on the home page, not on matching-family-sweatshirts.

## Chosen
1. matching family shirts -> /collections/family-tops
2. matching family sweaters and family holiday sweaters -> /collections/family-sweaters and /collections/christmas-sweaters
3. matching family sweatshirts -> /collections/matching-family-sweatshirts

The collection pages already carry the wording in title/H1/intro; the gap was the link signal from the product pages Google picks.

## Change (commit f5f27b5, snippets/product-internal-links.liquid, English only)
Before: these product pages linked the hubs only with generic anchors (Tops, View similar styles; Jingle Bells also "Christmas Sweaters").
After: one sentence under the description, e.g. "Browse all matching family shirts to compare designs and choose a size for each person."; sweatshirts and sweaters link their own hub; Christmas sweaters add "See our family holiday sweaters for Christmas."
Live read (built-in browser): heart T-shirt, Jingle Bells sweater, Scribble Heart sweatshirt show the link; Spanish page unchanged. Live theme equals main (0 differences).
Rollback: revert f5f27b5.

Effect not measured; re-check these queries and landing pages around 2026-12-11.

## Translated product pages (commit e97017d, es, de, fr, it, cs, ro)

Before: no hub link outside English. After: the same sentence in each language, linking the localized collection.
Rule (all 7 languages): handle contains "family", not pajamas; collection membership matching-family-sweatshirts, else family-sweaters (+ christmas-sweaters link), else family-tops. It adds 8 family tops/cardigans in English that the title rule missed. Texts are inline in the snippet; no locale files changed.

| Lang | sweatshirts | sweaters | shirts | holiday sweaters | Source (GSC 16 months) |
| --- | --- | --- | --- | --- | --- |
| es | sudaderas familiares a juego | suéteres familiares | camisetas familiares a juego | suéteres navideños para la familia | "sueter familiares", "sueter navideño familia" |
| de | Familien-Sweatshirts im Partnerlook | Familienpullover | Familien-Shirts im Partnerlook | Weihnachtspullover für Familie und Geschwister | "familienpullover", "geschwister weihnachtspullover" |
| fr | sweats famille assortis | pulls assortis pour la famille | t-shirts et chemises assortis pour la famille | pulls de Noël assortis pour la famille | "sweat famille assorti", "pull de noel assortis famille" |
| it | felpe coordinate famiglia | maglioni coordinati per la famiglia | magliette famiglia coordinate | maglioni natalizi per la famiglia | "felpe coordinate famiglia" |
| cs | rodinné mikiny | rodinné svetry | rodinná trička | vánoční svetry pro celou rodinu | "rodinné mikiny", "rodinné svetry" |
| ro | hanorace pentru familie | pulovere asortate pentru familie | tricouri asortate pentru familie | pulovere de Crăciun pentru familie | "hanorace familie", "pulovere craciun familie" |

Anchors without local data use natural names consistent with collection titles.
Live read (built-in browser, 6 s apart): es, de, cs sweater; fr, ro tee/top; it sweatshirt: link present with language prefix. Main kept the file after Shopify's sync (b37cf8d, 0 changes). Rollback: revert e97017d.
Seen, not touched: product titles "Topuri inimă de caise albastră" (ro, broken) and "Cuore scarabocchiato Felpe per la famiglia" (it, word order).

## Destination collections (commit 12cce9d + product order)

| Page | Before | After |
| --- | --- | --- |
| family-tops title | Family Matching Shirts – Tees, Sweatshirts & Button-Ups | Matching Family Shirts \| Family Matching Tees & Button-Ups |
| family-tops H1 | Family Matching Shirts & Tops | Matching Family Shirts & Tops |
| family-tops order | newest first: first 24 were sweatshirts and sweaters | manual: heart T-shirt, tees, button-ups, then sweatshirts and sweaters |
| family-sweaters title | Matching Family Sweaters, Cardigans & Sweatshirts | Matching Family Sweaters for Christmas & the Holidays |
| family-sweaters description and intro | no "holiday sweaters" | "family holiday sweaters" in both |
| family-sweaters order | sweaters and sweatshirts interleaved | sweaters first |
| matching-family-sweatshirts | already carries the query in title, H1, description and intro; 21 sweatshirts only | unchanged |

Product order receipts and rollback: ops/organic/receipts/2026-11-27/hub-order/ (before.json has the previous order and family-tops sortOrder CREATED_DESC). family-tops is now manual: check where newly added products land. No product added or removed; family-tops and family-sweaters keep sweatshirts because their names cover them.

Live read (built-in browser, 2026-11-27 ~06:23Z, 6 s apart): family-tops (36 cards, heart tee first), family-sweaters (36, sweaters first), matching-family-sweatshirts (21), christmas-sweaters (25; one daddy-and-me sweater and one sweatshirt among the sweaters). Titles, H1, description, intro as above. Live theme equals main for code files; main kept the snippet after Shopify's sync cdbf39f.
Incident: both this release and collection-copy-4 (16be3a2) wrote THEME_LOCK in the same minute and committed 2 s apart; both commits are on main. Their lock was left in place. Their locale files were not checked here.
Pending for the next product-internal-links release (Quality V88, optional): fixed category names, keep "a juego" in es/cs, less telegraphic it/fr/de/ro wording.

## Second round: mom-and-daughter and maternity (commit a1972d2)

| Query (28 d) | Impr / pos | Google's landing today | Destination |
| --- | --- | --- | --- |
| mommy and me outfits | 1,035 / 14.5 | home page (913); /collections/mommy-and-me at 66 | mommy-and-me |
| mommy and me dresses (+ christmas dresses 33) | 190 / 14.3 | home page (160) | dresses |
| maternity photoshoot / shoot dress, gown for photoshoot | about 85 listed; maternity queries 595 total | home page 250, single gowns | maternity |
Couples and Valentine queries sit around position 55: outside 8-30, skipped.

Changes
- Product pages (en, es, de, fr, it, cs, ro): mom-and-daughter dresses link the dresses hub, other mom items the mommy-and-me hub, gowns the maternity hub, in local wording. Excluded: pajamas, nightgowns, sleep and robe handles (this also leaves out any gown whose handle says robe only if not maternity). Simulated: 46 mom, 36 dresses, 23 maternity.
- Quality V88 wording applied to the family links (fixed names, "a juego"/equivalents).
- maternity (English): title "Maternity Dresses - Pregnancy & Nursing Styles" -> "Maternity Photoshoot Dresses & Gowns"; H1 "Maternity and Nursing Styles" -> same new wording; description and intro rewritten (the catalogue has no nursing styles).
- dresses (English): title and H1 kept; description and intro rewritten.
- Product order unchanged: gowns and dresses already lead; mommy-and-me already opens with winter knits (it still holds one family sweater).

Live read (built-in browser): maternity (updated on the second load, first was cached), dresses, product pages en maternity/dress/knit, es maternity, cs family tee: links and texts present. Live theme equals main, main kept the files, my lock removed. Rollback: revert a1972d2.
Pending: translated maternity H1/title/intro (theme locales) still mention nursing.

## Maternity: false nursing wording removed (commit f1ca110 + Admin)

- Theme: collection heading in all 35 locale files (1 key each) and the two English fallback strings in collection-seo-fallback. Locale files pushed with sync-locales (backup: ops/organic/receipts/2026-11-27/theme-locale-before-20261127T063804Z), recheck "in sync".
- Admin: maternity collection SEO title, SEO description and body in EN + 20 languages (60/60, 0 outdated). The long body, which also carried free-shipping and returns lines, was replaced by one truthful sentence. Rollback: ops/organic/receipts/2026-11-27/maternity-nursing/before.json.
- Live read: es, de, fr, it, ja, en: new title/heading, no nursing wording. Main kept the change after Shopify sync; lock removed.
- Maternity product pages (23 active, EN + 20): 0 nursing/breastfeeding hits (strict terms).
