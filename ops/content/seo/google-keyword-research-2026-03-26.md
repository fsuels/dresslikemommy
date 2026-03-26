# Google Search Console and Keyword Research

Date: 2026-03-26
Store: `dresslikemommy.com`

## Evidence And Limits
- Live URLs were taken from the store sitemap and checked on the live site in a real Chrome session.
- Google Search Console could not be used in authenticated mode in this session. The public Search Console landing page was reachable, but no verified property data for `dresslikemommy.com` was available here, so clicks, CTR, average position, and true position 5-20 opportunities could not be exported.
- Google autocomplete was pulled from the US-localized Google suggest endpoint.
- Query-level Google Trends charts returned HTTP 429 from this network. The seasonal plan below is directional and should be confirmed in Google Trends or GSC once a clean browser session is available.

## Highest-Value Keyword Families
These are relative demand and competition tiers, not absolute monthly search volumes.

| Keyword family | Relative demand | Competition | Google autocomplete evidence |
| --- | --- | --- | --- |
| `mommy and me outfits` | High | High | Strong audience modifiers: `girl`, `baby girl`, `newborn`, `valentines`, `christmas` |
| `mommy and me dresses` | High | High | Clear commercial occasions: `wedding`, `spring`, `easter`, `photoshoot` |
| `mother daughter matching dresses` | High | Medium-high | Strong event intent: `wedding`, `easter`, `birthday` |
| `family matching outfits` | Very high | Very high | Broad transactional modifiers: `christmas`, `vacation`, `easter`, `photoshoot`, `summer` |
| `family matching swimsuits` | High | Medium-high | Strong summer modifiers: `with baby`, `plus size`, `4th of july` |
| `family matching pajamas` | High | High | Strong seasonal modifiers: `christmas`, `with baby`, `with dog`, `sale` |
| `daddy and me outfits` | Medium-high | Medium | Clear family-role modifiers: `boy`, `girl`, `baby boy`, `newborn` |
| `daddy and me shirts` | Medium | Medium | Commercial long tails exist: `matching shirts`, `golf shirts`, `hawaiian shirts` |
| `daddy and me swim trunks` | Medium | Medium | Transactional variants exist: `matching swim trunks`, `matching swim shorts` |
| `matching family vacation outfits` | Medium-high | Medium | Closely related autocomplete: `matching family summer outfits`, `coordinating family vacation outfits` |
| `matching family photo outfits` | Medium-high | Medium-high | Strong occasion intent: `christmas`, `fall`, `photoshoot`, `portrait` |
| `matching family beach outfits` | Medium | Medium | Strong summer travel modifiers: `beach wear`, `beach clothes`, `beach vacation outfits` |
| `couples matching outfits` | High | Very high | Competitive lifestyle modifiers: `vacation`, `cruise`, `wedding`, `photoshoot` |
| `couples matching shirts` | Medium-high | High | Clear commercial modifiers: `funny`, `disney`, `cruise`, `christmas` |
| `family matching easter outfits` | Medium-high seasonal | Medium | Autocomplete includes `plus size`, `easter dresses`, `coordinating family easter outfits` |
| `family matching halloween outfits` | High seasonal | High | Autocomplete quickly shifts to `halloween costumes` and `costume ideas` |
| `family matching christmas outfits` | High seasonal | High | Autocomplete includes `for pictures`, `with baby`, large marketplace modifiers |

## What Looks Most Valuable
- Best broad commercial terms: `family matching outfits`, `mommy and me outfits`, `mommy and me dresses`, `family matching swimsuits`, `family matching pajamas`.
- Best intent-rich mid-tail terms: `matching family vacation outfits`, `matching family photo outfits`, `mother daughter matching swimsuits`, `daddy and me shirts`, `couples matching shirts`.
- Best long-tail product terms: `mommy and me matching bikini set`, `matching family beach outfits`, `father son matching tropical shirts`, `valentines couples matching shirts`.

## Structural SEO Risks
- Blog cannibalization is severe. The live blog sitemap currently contains `254` article URLs, including repeated year-stamped versions of the same topics:
  - `valentines-day-mommy-and-me-outfits` -> `11` versions
  - `spring-matching-outfits-for-mommy-and-me` -> `11` versions
  - `summer-matching-family-outfits` -> `11` versions
  - `halloween-family-matching-costume-ideas` -> `11` versions
  - `christmas-matching-family-pajamas` -> `9` versions
- Collection overlap is also present:
  - `daddy-and-me` and `daddy-me` are both live collection handles.
  - `couples` and `matching-couples-t-shirts` overlap and must stay differentiated by intent.
  - `matching-outfits` and `family-sets` overlap unless one owns broad family intent and the other owns vacation/beach intent.
- Inventory gaps are blocking SEO on demand-rich terms:
  - `/collections/family-pajamas` rendered with `0` products in the live browser session.
  - `/collections/christmas-pajamas` rendered with `0` products.
  - `/collections/christmas-tops` rendered with `0` products.

## Public-Signal Low-Hanging Fruit
These are the first keywords to validate in GSC once access is available. They already have live landing pages, strong query-to-page fit, and manageable optimization work.

| Candidate keyword | Best URL | Why it is a strong first bet |
| --- | --- | --- |
| `family matching swimsuits` | `/collections/family-swimsuits` | Exact-match commercial collection with live inventory and aligned product set |
| `matching family vacation outfits` | `/collections/family-sets` | High-intent summer query with an existing set-focused collection that can be repositioned |
| `daddy and me shirts` | `/collections/daddy-me-t-shirts` | Exact page-to-query fit and clear autocomplete depth |
| `mommy and me matching bikini set` | product page for the floral bikini set | Product title is already close to the query and conversion intent is strong |
| `matching family photo outfits` | `/blogs/news/what-to-wear-for-family-photos-matching-outfit-ideas` | Informational query with obvious internal-link paths to commercial collections |
| `matching couple t shirts` | `/collections/matching-couples-t-shirts` or the LO VE product page | Page and products exist, but copy is under-optimized |

## Recommended Keyword Ownership Rules
- Homepage owns the brand-wide umbrella term set, not the same exact head terms as collections.
- Collections own the highest-intent transactional keywords.
- Blog posts own informational modifiers such as `ideas`, `guide`, `for photos`, `for spring photos`, and `for valentines day`.
- Product pages own design- and occasion-specific long tails.
- Consolidate seasonal blog duplicates into one evergreen hub plus one current-year refresh if a year needs to appear in the title.

Detailed page-by-page mapping: `ops/content/seo/google-keyword-map-2026-03-26.csv`

## Seasonal Calendar
Refresh or publish 6-8 weeks before the search peak, not when the holiday is already in market.

| Season | Peak search window | Refresh by | Existing pages to refresh | New page or collection to create if gap remains |
| --- | --- | --- | --- | --- |
| Valentine's Day | January to mid-February | December 15 to January 1 | `/collections/valentines-day-matching-outfits-1`, `/blogs/news/mommy-and-me-valentines-day-outfits`, couples heart-shirt products | A tighter couples Valentine's landing page if couples inventory grows |
| Easter | February to early April | January 15 to February 1 | `/blogs/news/mommy-and-me-easter-dresses-2026`, `/blogs/news/family-matching-outfits-spring-photos`, `/collections/mommy-and-me` | `/collections/family-easter-outfits` or a dedicated spring family photo collection |
| Mother's Day | April to early May | March 15 to April 1 | `/collections/mommy-and-me`, existing Mother's Day articles in the blog archive | One evergreen `/blogs/news/mothers-day-mommy-and-me-outfits` hub, redirecting older yearly duplicates |
| Summer vacation and beach | April to July | March 1 to April 15 | `/collections/family-sets`, `/collections/family-swimsuits`, `/blogs/news/mother-daughter-matching-swimsuits-complete-guide-for-summer-2026`, family beach products | A dedicated vacation outfits guide if `family-sets` is not fully repositioned |
| July 4th | Late May to early July | May 10 to May 20 | `/collections/family-swimsuits`, summer outfit articles, relevant patriotic products if stocked | `/collections/family-4th-of-july-outfits` if inventory supports it |
| Halloween | September to late October | August 15 to August 31 | Existing Halloween blog series, `/collections/matching-outfits` if no Halloween collection exists | `/collections/family-halloween-outfits` or `/collections/family-halloween-costumes` |
| Christmas and holiday pajamas | October to December | September 15 to October 1 | `/collections/christmas-pajamas`, `/collections/christmas-tops`, `/collections/family-pajamas`, Christmas pajama articles | `/collections/family-christmas-outfits` if non-pajama holiday inventory becomes meaningful |

## Recommended Next Moves
1. Connect or open authenticated Google Search Console and export queries/pages filtered to positions `5-20`, then compare against the CSV map first.
2. Pick one canonical page for each recurring seasonal intent and redirect or consolidate year-stamped duplicates.
3. Decide whether empty collections (`family-pajamas`, `christmas-pajamas`, `christmas-tops`) will be stocked. If not, noindex or redirect them instead of leaving them indexable.
4. Rework collection titles, H1s, intro copy, and internal links in this order:
   - `/collections/family-swimsuits`
   - `/collections/family-sets`
   - `/collections/daddy-me-t-shirts`
   - `/collections/matching-couples-t-shirts`
   - `/collections/mommy-and-me`
