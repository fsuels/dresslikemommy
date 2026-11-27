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

## Local-language demand, four markets (Search Console 28 d by country; commit eef254a + Admin)

| Query (country) | Impr / pos | Landing today | Change |
| --- | --- | --- | --- |
| vestir familia igual (+ ropa familia a juego) (ES) | 72 / 22 | summer and complete guides | es matching-outfits title "Vestir toda la familia igual: ropa a juego", H1, description, intro; link added to the es complete guide |
| kleding voor gezin (NL) | 93 / 10 | complete guide; collection ~25 | nl matching-outfits title "Matching kleding voor het hele gezin: mama, papa en kind", H1; link added to the nl complete guide |
| pulovere craciun familie (RO) | ~150 / 13-19 | matching-family-christmas-outfits (title also began "Pulovere") | christmas-outfits title now "Ținute de Crăciun asortate pentru familie"; christmas-sweaters title "Pulovere de Crăciun pentru familie, asortate" |
| matchande julkläder familj (SE) | 178 / 9 | christmas-outfits + newborn guide | sv description now opens with "Matchande julkläder för hela familjen" |

Not chosen: SE "matchande klänning mamma dotter" (dresses already answers), CZ Christmas sweaters (already answered), DE/FR/IT lower or already covered; swim queries out of season.
Theme: only collection_seo family_matching keys (es 4, nl 2); locales in sync; main kept them; lock removed. Rollback: revert eef254a; Admin ops/organic/receipts/2026-11-27/locale-demand-4/before.json.
Re-measure ~12-11.

## DE, FR, IT, CZ (Search Console 28 d; commit a646bf4 + Admin)

| Query | Impr / pos | Landing today | Change |
| --- | --- | --- | --- |
| familienoutfits (DE) | 27 / 8.6 | /de home | de matching-outfits title "Familienoutfits im Partnerlook: Mama, Papa & Kinder", H1; link added to the de complete guide |
| tenue famille assortie / assortie famille (FR) | 32 / 12-18 | guides; collection ~78 | fr matching-outfits title "Tenue famille assortie : maman, papa et enfants", H1, description, intro; link in the fr complete guide |
| rodinné mikiny (CZ) | 39 / 8.8 | single sweatshirts | cs matching-family-sweatshirts title, H1 and description start with "Rodinné mikiny" (Admin; product pages already link it) |
| vestiti coordinati famiglia eleganti (IT) | 34 / 9.2 | it matching-outfits (right page) | Admin link with "vestiti coordinati per tutta la famiglia" in the it complete guide. Pending, not done: adding "vestiti" to the it collection title (it.json, left for the owner's release) |

Live read: de, fr, cs collections and the three guides. locales in sync, main kept the keys, lock removed. The immediate recheck after sync-locales --apply shows drift for a short while; a second check a minute later is clean.
Rollback: revert a646bf4; Admin ops/organic/receipts/2026-11-27/locale-demand-de-fr-it-cs/before.json. Re-measure ~12-11.

## Quality V101 fix (commit ebe0205 + Admin)
es title "Vestir a toda la familia igual: ropa a juego" and H1 back to "Ropa a juego para toda la familia"; nl title, H1, description and guide link unified on "Bijpassende kleding voor het hele gezin"; ro christmas-outfits description now starts "Ținute de Crăciun". Live read; locales in sync. Rollback: revert ebe0205; ops/organic/receipts/2026-11-27/v101-fix/before.json.

## Baseline to re-measure about 2026-12-11
Search Console, last 28 days, read 2026-11-27 ~07:10Z (data to about 11-24/25, so it is before today's changes). Landing = the top pages shown, with impressions.

| Query | Impr | Clicks | Pos | Landing today (impr) | Page that should win |
| --- | --- | --- | --- | --- | --- |
| matching family shirts | 772 | 0 | 11.8 | heart T-shirt product 731; cartoon T-shirt product 89 | /collections/family-tops |
| family matching shirts | 463 | 0 | 10.0 | heart T-shirt product 455; family-tops 8 | /collections/family-tops |
| matching family sweaters | 407 | 4 | 12.3 | single sweater products (top by clicks: nordic yoke) | /collections/family-sweaters |
| family matching sweaters | 446 | 5 | 10.7 | Jingle Bells product 215; family-sweaters 35 | /collections/family-sweaters |
| family holiday sweaters | 138 | 1 | 7.9 | Jingle Bells product 125 | /collections/christmas-sweaters |
| matching family sweatshirts | 110 | 1 | 11.6 | home 80 | /collections/matching-family-sweatshirts |
| mommy and me outfits | 1,040 | 2 | 14.6 | home 919 | /collections/mommy-and-me |
| mommy and me dresses | 190 | 2 | 13.9 | home 165 | /collections/dresses |
| maternity photoshoot dress | 29 | 3 | 2.0 | one gown product 25 | /collections/maternity (product already ranks 2; watch only) |
| maternity shoot dresses | 22 | 3 | 2.0 | one gown product 16 | /collections/maternity (same) |
| vestir familia igual (es) | 73 | 0 | 23.1 | es summer guide 58; es complete guide 56 | /es/collections/matching-outfits |
| ropa familia a juego (es) | 46 | 0 | 18.1 | es complete guide 27; summer guide 19 | /es/collections/matching-outfits |
| kleding voor gezin (nl) | 89 | 0 | 10.4 | nl complete guide 64; new-women-outfits 17 | /nl/collections/matching-outfits |
| pulovere craciun familie (ro) | 119 | 1 | 11.7 | ro christmas-outfits 116 | /ro/collections/christmas-sweaters |
| matchande julkläder familj (sv) | 199 | 1 | 8.8 | sv christmas-outfits (two rows 96 and 52) | /sv/collections/matching-family-christmas-outfits |
| familienoutfits (de) | 28 | 0 | 8.7 | /de home 25 | /de/collections/matching-outfits |
| tenue famille assortie (fr) | 18 | 1 | 11.7 | fr complete guide 8; style guide 8 | /fr/collections/matching-outfits |
| tenue assortie famille (fr) | 15 | 0 | 27.4 | fr style guide 7; complete guide 4 | /fr/collections/matching-outfits |
| rodinné mikiny (cs) | 47 | 0 | 8.6 | single sweatshirt products 22 and 22 | /cs/collections/matching-family-sweatshirts |
| vestiti coordinati famiglia eleganti (it) | 34 | 1 | 9.1 | it matching-outfits 31 | /it/collections/matching-outfits (already) |

Success = the expected page appears for the query and its clicks or position improve; compare the same 28-day view.

## Quality V103 fix (Admin only)
cs matching-family-sweatshirts title and search title "Rodinné mikiny a hoodie pro maminku, tatínka a děti"; de complete guide body and description changed from "du" to "Sie" (links unchanged). 4/4, 0 outdated, live read. The a646bf4-round theme texts were not touched. Rollback: ops/organic/receipts/2026-11-27/v103-fix/before.json. Left as is (optional): fr and it wording in the guide link sentences.

## No-cart mismatches, points 4, 6, 7 (Experto SEO, 2026-11-27)
### A. Localized homepage titles (theme key storefront.home_title; descriptions already matched English)
sv, no, nb (was English), da, fi, nl now lead with family outfits, then mom-and-child clothes (sense of the live English title). Risk: dress wording leaves the home title; re-check those home pages about 12-11.
### B. /collections/sweaters
Search Console 28 d: sweaters 1,470 impr / 43 clicks / pos 10.1, queries all mom-and-daughter ("mom and daughter matching sweaters", "mommy and me sweaters"); family-sweaters 870 / 23 / 13.2, family queries. So sweaters = mom-and-daughter page: English title/H1/meta/intro (links family-sweaters), 10 mommy-and-me knits first (Admin, manual order). Collection rules unchanged; breadcrumbs already Mommy and Me. Other languages keep the old text. Order rollback: ops/organic/receipts/2026-11-27/hub-intent/sweaters-order-before.json.
A and B live (b8c9c1a, export 2a3e94f, 11:50Z). Read live: US sweaters title, H1, intro, first 6; titles on /sv /no /da /fi /nl.
### C. Proposal, NOT published: mom-and-daughter row on the homepage
- templates/index.json: add section "mom_daughter_row": {"type": "featured-collection", "settings": {"title": "", "collection": "mommy-and-me", "products_to_show": 4, "columns_desktop": 4, "columns_mobile": "2", "show_view_all": true, "color_scheme": "scheme-1", "padding_top": 24, "padding_bottom": 24}}; in "order" place it right after "hero_banner_main" (second screen).
- Shows today (mommy-and-me manual order): cream heart cardigans, heart-button cardigan and dress set, burgundy ruffle cardigans, navy sprig dress and cardigan.
- sections/featured-collection.liquid: when the title is blank use the collection title (translated), and skip this row for AU/NZ summer (dlm-southern-summer).
- Publish: lock; compare live templates/index.json with origin/main (stop if the theme editor changed it); commit section file + index.json to main; code via sync-theme; index.json through the GitHub theme sync, then read the live file back; if not applied, upload that one file by Admin theme upsert; 3 min hold; check US, es, AU.
- Rollback: revert the commit and repeat.

## Homepage mom-and-daughter row published (833b49b, 12:12Z)
- Tested first on the unpublished theme 158206558305 (role checked before every write; heading style needed !important). US, es, AU on mobile and desktop: row after the hero, translated heading, other sections unchanged, no overflow, layout shift 0; AU empty section adds 4 px on desktop.
- Release: live index.json equal to main before commit; GitHub sync had not applied it after 200 s, so that one file was upserted by Admin and read back equal; export 6ea502a/6b98619.
- Live (role main): US desktop, es mobile, AU mobile, NZ desktop. Products: cream heart cardigans, heart-button set, burgundy ruffle cardigans, navy sprig dresses (active, no pajamas).
- Rollback: git revert 833b49b, sync-theme --apply and upsert the previous index.json (receipts/2026-11-27/home-row/index-live-before.json).
- Notes (Quality V138): /de and /es sweaters still say family (Admin translations, blocked today). Spanish home title still leads with dresses.
