# Entry pages with organic visits and no add-to-cart (2026-11-27)

Read-only diagnosis. Nothing changed in the store, theme or git.
Data: `_DATA.md` (Shopify analytics, organic only, 13-26 Nov, 14 days). Live look: built-in browser, phone viewport 375x812, country switched from Spain to United States with the store's selector and restored to Spain at the end. 13 page loads, about 10 s apart, no 429/403, no verification page. No add to cart, no forms, no checkout.

## 1. Landing pages and cart rate

Store-wide organic cart rate: 220 carts / 2,805 sessions = 7.8%.
Only 6 pages reach 25 sessions, so the list goes down to 18 sessions to get 8 pages. Caution: at 18-22 sessions, zero carts happens by chance about 1 time in 5 even on an average page. Only swimsuits (40/0, chance about 4%) and /collections/sweaters (30/0, about 9%) are clearly below normal.

| Landing page | Sessions | Carts | Cart rate | Checkouts / orders | Group |
| --- | --- | --- | --- | --- | --- |
| / (English home) | 80 | 5 | 6.3% | 0 / 0 | worst |
| /collections/swimsuits | 40 | 0 | 0% | 0 / 0 | worst |
| /collections/sweaters | 30 | 0 | 0% | 0 / 0 | worst |
| /sv/collections/dresses | 22 | 0 | 0% | - | worst |
| /sv (Swedish home) | 21 | 1 | 4.8% | - | worst |
| /no/collections/dresses | 18 | 0 | 0% | - | worst |
| /collections/family-sweaters | 18 | 1 | 5.6% | - | worst |
| /it/collections/matching-outfits | 18 | 1 | 5.6% | - | worst |
| /products/nordic-yoke-family-matching-sweaters | 46 | 7 | 15.2% | 3 / 1 | best |
| /cs/collections/matching-family-christmas-outfits | 35 | 6 | 17.1% | 1 / 0 | best |
| /products/christmas-reindeer-family-matching-sweaters | 16 | 4 | 25.0% | - | best |
| /ro/collections/matching-family-christmas-outfits (not used as a model) | 28 | 10 | 35.7% | 0 / 0 | high carts, no checkouts |
| Others: it Christmas 22/2, nl dresses 20/2, jolly-crew 18/3, grapevine 17/4, reindeer-row 16/1 | | | | | |

No blog article reached 18 sessions, so all 8 are store pages.

## 2. Page by page (US shopper, phone)

### / (English home), 80 sessions, 5 carts
- Search Console baseline: Google sends "mommy and me outfits" (919 impressions) and "mommy and me dresses" (165) to the home page.
- Above the fold: the order-by line "Order by Wed, Dec 2 for estimated Christmas arrival", a dark "Christmas Edition" hero with a family-pajama photo, and buttons for Christmas sweaters and Christmas pajamas. Products start right below (Nordic Yoke first).
- Nothing mom-and-daughter until the "Matching family sets" block, about 3,000 px down (page is 7,800 px).
- Nothing broken. The order-by line is clear and correct.
- **Likely reason: intent mismatch.** A "mommy and me outfits" searcher lands on a whole-family Christmas pajama page. Mom-and-daughter is not visible in the first screens.

### /collections/swimsuits, 40 sessions, 0 carts
- Title and H1 match ("Mommy and Me Swimsuits"); 31 products, none sold out in the first rows, prices from $19.99 (sale from $29.99), mother-and-daughter beach photos.
- Filters (Price, Color, Size, Type) are present; no order-by line (none is needed); no reviews on cards.
- The page works. It is the end of November: northern shoppers are not buying swimwear. Southern-hemisphere visitors (Australia 124 organic sessions) are possible but not visible in the data.
- **Likely reason: seasonality.** The page is fine; demand is off-season. Do not spend effort on it now; recheck in spring.

### /collections/sweaters, 30 sessions, 0 carts
- Title "Mommy and Me & Family Matching Sweaters"; H1 on the phone is two long lines. The pills highlight "MOMMY AND ME" and "Within Mommy & Me" while the first products are whole-family sweaters (Christmas Reindeer, Nordic Yoke, Burgundy Trim daddy-and-me).
- 37 products, first rows in stock, seasonal and relevant; cards show "From $31.99" (the kids' price, nothing says "per piece").
- No Christmas order-by line on this page (the home page and product pages have it).
- It largely duplicates /collections/family-sweaters (same top products), and its intro links to family-sweaters: two pages compete for the same searches and split the visits.
- **Likely reason: a weak hub that duplicates family-sweaters.** It gives no reason to choose here (no order-by date, no price per person), and the people who clicked a sweater went on to the product page. The 0 carts are counted on this landing page, not on the product page.

### /sv/collections/dresses, 22 sessions, 0 carts (and /no/collections/dresses, 18 / 0)
- Swedish and Norwegian text is translated and reads correctly; H1 "Matchande klänningar mamma och dotter" / "Kjoler til mor og datter".
- 37 products, but only one is for winter (the heart-button cardigan and dress set, first). The rest are summer: tropical leaves, beach chiffon, sleeveless ruffles, sunflower maxi dresses.
- In late November, a Scandinavian searcher wants a Christmas or winter-party dress (the page's own guide link talks about winter and Christmas parties). The products do not match.
- Norway: 83 organic sessions and 0 checkouts overall; NOK cannot be enabled (prices in another currency and import costs at checkout are a hurdle). Sweden: 117 / 6 / 0 checkouts.
- **Likely reason: seasonality plus an assortment gap.** No winter mom-and-daughter dresses to show. Market barriers (currency, VAT) probably add to it.

### /sv (Swedish home), 21 sessions, 1 cart
- Page title (search snippet) "Klänningar för mamma och dotter | Matchande familjekläder", but the page opens with Christmas family sweaters and pajamas.
- The order-by line is shown in Swedish ("Beställ senast ons 2 dec. ..."); all text is translated.
- **Likely reason: intent mismatch** (search snippet promises dresses; page shows family Christmas knits) plus the Sweden-wide barrier above.

### /collections/family-sweaters, 18 sessions, 1 cart
- Title "Matching Family Sweaters for Christmas & the Holidays", H1 "Matching Family Sweaters"; 44 products; first row Nordic Yoke, Christmas Reindeer, Reindeer Row, Nordic Heart Reindeer (the best sellers), in stock.
- Cards show only "From $37.99" (kids' price); a family of four on Nordic Yoke is about $175, and no card says who the price is for.
- No Christmas order-by line; no reviews.
- The 44 include sweatshirts and cardigans (as planned).
- **Likely reason: weak buying cue before the click, small sample.** The page is well matched; 18 sessions with 1 cart is within normal chance. Visitors who click through to Nordic Yoke convert there.

### /it/collections/matching-outfits, 18 sessions, 1 cart
- Title "Vestiti coordinati famiglia: mamma, papà e bambini", H1 "Vestiti coordinati per la famiglia"; 193 products.
- Search Console: it ranks for "vestiti coordinati famiglia eleganti" (34 impressions, pos 9). The first 24 products are all sweaters, sweatshirts and pajamas; there is nothing "elegant" (dresses, shirts) near the top.
- Italian title word order is wrong on two cards: "Cuoricino Felpe coordinate per la famiglia", "Rombi retrò Maglioni coordinati per la famiglia".
- No order-by line; no reviews.
- **Likely reason: intent mismatch** (looking for elegant outfits, sees knits and pajamas); small sample.

## 3. What the best pages have that the worst lack

The best pages are Nordic Yoke, Christmas Reindeer and the Czech Christmas collection.
- **Clear price.** The product pages say "Kids from $31.99 · Adults from $34.99. Pick a size for each person. Priced per piece." Collection cards say only "From $31.99".
- **A date.** The product pages show "Estimated delivery: Wed, Dec 9 – Wed, Dec 16" and "order by Wed, Dec 2 to arrive by Wed, Dec 23". On collection pages the date is missing.
- **In-season intent.** A Christmas search lands on Christmas knits that are best sellers. The worst pages are off-season (swimwear, summer dresses) or the visitor wanted something else (mother-and-daughter, elegant).
- **Whole-family photos.** The best pages open on a full-width family photo (6 photos on Nordic Yoke, 3 on Christmas Reindeer), plus a sticky bar with the price and "Select size".
- No page shows reviews, best or worst, so reviews do not explain the gap.

The size choices sit about 1,040 px down on product pages (below the first phone screen) and the size chart link is about 360 px below them. That is the same on the best and worst pages and does not explain this gap.

## 4. Ranked changes (max 8)

1. **Theme change (I can do).** Show the existing Christmas order-by line ("Order by Wed, Dec 2 for estimated Christmas arrival", the same component the home page shows) on collection pages: sweaters, family-sweaters, matching-family-christmas-outfits, christmas-sweaters, matching-outfits, mommy-and-me, in all languages already translated. It expires by itself after the cutoff. Today 8 collection pages show no date at all.
2. **Theme change (I can do).** On collection cards with an adult and a kids price, show "Kids from $X · Adults from $Y" (the wording the product page already uses) instead of "From $X", or at least add "per person".
3. **Product data change (I can do).** /collections/dresses: move the heart-button cardigan and dress set plus any long-sleeve, velvet, plaid, red or Christmas dresses from mommy-and-me to the top, before the summer chiffon and beach dresses, until February. This fixes sv, no and nl dresses at once, because those pages share the collection.
4. **Product data change (I can do).** /collections/mommy-and-me and the home page: Google sends "mommy and me outfits" to the home page. Add one mom-and-daughter row ("Mommy and me Christmas", e.g. Cream Heart cardigans, heart-button set) in the first two screens of the home page, right after the Christmas hero. This is a theme section setting.
5. **Product data change (I can do).** /it/collections/matching-outfits: put 4-6 dresses and button-up shirts in the first two rows so "eleganti" searchers see them. Fix the two Italian card titles with wrong word order ("Felpe coordinate per la famiglia con cuoricino", "Maglioni coordinati per la famiglia a rombi retrò"). These titles are product translations; check that the translation lane is open first, otherwise the fix is **translation (blocked today)**.
6. **Theme change (I can do).** /collections/sweaters: the breadcrumb pills highlight "Mommy and Me" on a page whose top products are whole-family sweaters. Either put it under Family Matching, or make it the true mom-and-daughter sweater page (cardigans and mommy-and-me knits first) so it stops competing with family-sweaters.
7. **Translation (blocked today).** /sv home search title "Klänningar för mamma och dotter ...": change it to the family wording the page shows ("Matchande familjekläder och julkläder"). Leave the dresses page as the place for dress searches.
8. **Owner decision.** Swedish and Norwegian shoppers: 200 organic sessions in 14 days and 0 checkouts. Decide whether to show local currency or a "prices include VAT / duties" line for SE/NO, or stop pushing those markets. Also new photos of winter mom-and-daughter dresses: none exist in the catalogue.

Not recommended: changing swimsuits now. The page is fine and the problem is the season.

## Limits
- Small samples. 18-22 sessions with 0-1 carts is not proof of a broken page.
- Sessions are not split by country per landing page. English pages are visited from many countries; I viewed them as a US shopper only.
- The home-page order-by line was seen live, but I did not find its source file in the repo working copy. Check the live theme or uncommitted work before change 1.

## Follow-up executed (2026-11-27 ~11:13Z)
1. **US order-by line on gift collections: done, 24c6f2f.** The existing `christmas-cutoff-banner` (same text, date and cutoff script as the home page; Liquid stops it after 3 Dec, the script hides it after the cutoff) now renders under the title/intro of sweaters, family-sweaters, matching-outfits, family-matching-outfits, mommy-and-me, pajamas and family-pajamas. It is **United States only** (`us_only`); "christmas" collections keep their top banner as before; swimwear, maternity and dresses get nothing. On mobile it overrides the hero rule that hides everything but the title (`!important`, only while not `[hidden]`). Green, 400 weight, date in bold as on the home page; 23 px tall, under the H1; layout shift 0.0026.
2. **Kids/Adults starting prices on cards: done, same commit.** The keys already exist in all 35 locales (`products.product.price.group_from`, `products.facets.size_groups.child/adult`). Cards whose kids and adult sizes start at different prices, and whose shown price is the lowest kids price, read "Kids from $37.99 ~~$47.99~~" and, on the next line, "Adults from $49.99". DE: "Kinder ab €40,95 / Erwachsene ab €53,95". CA: "Kids from $55.00 CAD ~~$70.00 CAD~~ / Adults from $73.00 CAD". `dlm-price-groups` gained `output: 'amounts'`, and the product page line is unchanged. No amounts changed.
   Copy test (unpublished "gallery-test 2026-11-27", synced first): US, CA and DE, mobile and desktop. No overflow (375/375). CA and DE show no line. christmas-sweaters keeps its top banner; swimsuits shows none. Console: only the known 401s. Release: commit, 90 s, list (5 differ), apply (5), re-check 0; export 44a1016 keeps all 5 files. Live US check OK.
3. **mother-daughter-matching-dresses: sort was MANUAL, so I reordered it (Admin, collectionReorderProducts, job done).** The full previous order (135 products) is saved in `ops/category-team/state/mother-daughter-dresses-order-before-2026-11-27.json`. The collection has only one true winter piece (Heart Button cardigan + dress set, a knit). No velvet or long-sleeve dresses exist. New top 5: Heart Button, Navy Sprig (dress + cardigan), Black Bow (black, tie neck), Green Lace Garden (green, puff sleeve), Lavender floral applique (tagged Formal). The rest keep their previous order. To undo: replay the saved order with collectionReorderProducts.
