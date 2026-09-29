# Organic SEO backlog seed (2026-09-28)

Author: read-only SEO analyst pass. No Shopify, git or repo writes were made except this file.
Goal: maximize FREE organic traffic. No paid ads. Dropshipping truth rules apply (no inventory, warehouse, fast-shipping, review, bestseller or guarantee claims; no pets).

Evidence labels: `GIT` = commit on `origin/main`; `LIVE` = fetched from the public site or read via the Admin API on 2026-09-28 (read-only); `WORKLOG` = an earlier session's LIVE_VERIFIED anchor, not re-read today; `INFERENCE`.

Important: the local checkout is **274 commits behind `origin/main`** (local HEAD 5d2e8a7, 2026-09-27; origin/main cb7eb4c, 2026-09-28 22:51). Everything below was read from `origin/main` (`git show origin/main:...`), not the stale working tree. Whoever executes this backlog must `git fetch` and rebase or work from a fresh checkout first.
The session scratchpad is also shared with another session (my first inventory file was overwritten); my files live in `.../scratchpad/seo_analyst/`.

Season clock (delivery is ~12-16 days, so order-by dates come first):
| Event | Date | Last order for arrival (estimate) | Days from today |
|---|---|---|---:|
| Halloween | Oct 31 | Oct 15 (already used by the theme) | 17 to cutoff |
| Thanksgiving | Nov 26 | ~Nov 8-10 | ~40 |
| Christmas | Dec 25 | ~Dec 5-8 (theme shows Dec 8) | ~70 |
| Valentine's | Feb 14, 2027 | ~Jan 25 (plan: live by Dec 5) | ~120 |
Google needs weeks to rank a new page, so pages for Christmas and Valentine's must be indexed in October and November, not December. Evidence that indexing can be fast: the Christmas photo-outfits article (published 09-27) already appears in Google results for "family christmas photo outfit ideas what to wear" one day later (WebSearch, 2026-09-28).

---

## 1. Shipped (verified in git; live status per anchors)

| SHA | What | Live status |
|---|---|---|
| `1f858a0` | seo.md #8 one hreflang set (22 alternates); #7 shipping policy no longer inlined on every page; home one H1; #4 canonicals `daddy-and-me`→`daddy-me`, `popular-mommy-me-1`→`mommy-and-me`; PDP copy blob 178 KB→~5-15 KB | WORKLOG LIVE_VERIFIED 09-27 |
| `d8a472e` | #3 six head-term collections (mommy-and-me, christmas-pajamas, new-women-outfits, daddy-me, swimsuits, family-pajamas): titles, meta, buyer guides in 21 languages, SEO-speak removed; #11 thin-collection noindex guard (seasonal hubs whitelisted); #9 `?variant=` noindex removed (was already absent live: D8 was STALE); #10 homepage title + stable H1 (seasonal line is h2) | WORKLOG LIVE_VERIFIED 09-27 (checklist §5 of SEO_BUILD_NOTES) |
| `c819ec1` | #1(d) Christmas redirects: 69 of 74 already target `/collections/christmas-pajamas`; 5 missing IDs recreated as 301s. Nothing to repoint | LIVE_VERIFIED 09-27 |
| `9ec0476` (record) | 15 overnight 301s: `family-christmas-pajamas`, `matching-christmas-pajamas`, `matching-family-christmas-pajamas`, `christmas-pjs`, `family-christmas-pjs`, `holiday-pajamas` → christmas-pajamas; `christmas`, `christmas-outfits`, `family-christmas-outfits`, `mommy-and-me-christmas` → matching-family-christmas-outfits; three sweater aliases → christmas-sweaters; `halloween-pajamas`, `halloween` → halloween-family-pajamas. Also 5 hidden Christmas winners published to all Markets (they were 404 in the US) | LIVE_VERIFIED 09-27 |
| `280108c` (record) | 5 archived nightgown/pajama product URLs 404→301 `/collections/pajamas` | LIVE_VERIFIED 09-27 |
| `02cf0e9` (record) | #12 blog→head-collection links applied to 46 articles (exact-anchor paragraph each) | WORKLOG 09-27, spot-check 9/9 |
| `af0871d` | Product JSON-LD `hasMerchantReturnPolicy` (30 days) and `shippingDetails.deliveryTime` (#14, partial) | LIVE_VERIFIED EN and /de; Rich Results Test not run |
| `b53040f`, `df95631`, `032d509` | #15 partial: collection filter markup slimmed (mommy-and-me 1,498→1,064 KB), country picker slimmed | LIVE_VERIFIED 09-27 |
| `4ac88af`, `1a32468` | Homepage flips to a Christmas hero on Oct 16 (Halloween cutoff Oct 15) | Not yet visible; check Oct 16 |
| `6c70aff`, `b0b82f3` (record) | GSC brief: English titles/H1/meta/guide for `couples`, `pajamas`, `family-tops`, `family-sweaters`, new `/collections/thanksgiving-family-outfits` (30 products), heart-tee product SEO title, Thanksgiving article rewrite, Grinch blocks removed from 3 posts, 6 URLs submitted in GSC | LIVE_VERIFIED 09-28 |
| `7aafd97`, `37a87db` (record) | `matching-outfits` made the Family Matching hub (rule + tag, superset of old hubs); `popular-family-matching` and English `new-women-outfits` canonical to it; `daddy-me-shirts` retitled; main menu FAMILY MATCHING → matching-outfits | LIVE_VERIFIED 09-28 |
| `5ec1df3`, `87f7db3` | Christmas cluster: cross-links between Christmas collections and a guides section; 3 Christmas guides translated into all 20 non-English locales | LIVE_VERIFIED 09-28 |
| `ad7ad94`, `36f5d48`, `516f26f` (records) | 3 new Christmas articles live (pajama guide, sweater guide, photo outfits) with own og:image, 8 then 12 more locales | LIVE_VERIFIED 09-27/28 |
| `20a17e8`, `5ba49a0` | New `siblings-matching-outfits` collection (3 products) and Siblings in the collections pill row | LIVE_VERIFIED 09-28 |
| `8a29c21`, `e937452`, `f6fcc03` | Merchant feed: color/pattern/material in descriptions, age_group/gender variant metafields (5,556 variants), brand fix | LIVE_VERIFIED 09-28 |
| `da07766`, `7ec0a83`, `ecdb3f2` | Image alt guard, image captions in structured data, alt/captions in 20 languages | WORKLOG |
| `7b5ac50`, `8e916da` | Mommy & Me swimsuit and dress copy rewrite with 20-locale titles | WORKLOG |

Also confirmed today (LIVE): live sitemap has **50 collections, 70 articles**, canonical logic in `layout/theme.liquid` (`popular-family-matching`→matching-outfits, `daddy-and-me`→daddy-me, `popular-mommy-me-1`→mommy-and-me). `robots.txt` lists the sitemap. `/llms.txt` and `/agents.md` are Shopify-generated (identical text, not store-specific).

---

## 2. Open from prior audits

Type: T = theme code, S = Shopify admin data (Admin API, agent-doable), O = owner / GSC / account action.

| # | Item (source) | Exact target | Type | Status / note |
|---|---|---|---|---|
| O1 | Mirror head-collection titles/descriptions into Shopify SEO fields (seo.md §6) | `swimsuits` (admin title still "Mother Daughter Swimsuits - Matching Swimwear"), `christmas-pajamas` ("Matching Family Christmas Pajamas \| Dress Like Mommy"), `mommy-and-me`, `daddy-me`, `family-pajamas` | S | Theme forces the right title in English, so low urgency; admin fields drive feeds, social and other locales |
| O2 | Nav/footer links to survivors only (SEO_BUILD_NOTES §6) | Menus: main menu done for FAMILY MATCHING; footer and homepage tiles unchecked | S | Verify footer and tile links do not point at `best-sellers`, `popular-*`, `new-matching-outfits` |
| O3 | Remove "Popular" wording (SEO_BUILD_NOTES §6) | `popular-mommy-me-1`, `popular-family-matching` (canonicalized), and **`best-sellers` H1 "Best Sellers" + SEO title "Best Selling Mommy and Me Outfits"**, still self-canonical and in the sitemap | T+S | Claim risk (no bestseller claims without data) and cannibalization; see backlog #7 |
| O4 | Restore or 301 the 152 lost URLs (seo.md D1, fix #2) | 152 clean English URLs, 21,682 impressions (25% of total) that left the sitemap; needs the GSC Pages export diffed against the sitemap | S (+O for the export) | Only three groups are done (74 Christmas, 15 overnight, 5 nightgown, plus the beach swimwear redirect). The rest are NOT verified. Examples: Christmas tree family tees, King/Queen family tees, mother-daughter beach swimwear |
| O5 | Breadcrumb for christmas-pajamas (#1e) | `snippets/collection-breadcrumbs.liquid` has a christmas-pajamas branch on origin/main (lines 67, 105) | T | Not re-read live; confirm Home › Family Matching › Christmas Pajamas |
| O6 | Restore Merchant free-listing health (#5) | Merchant 513542500 | O | Access now works (feed edits shipped 09-28). Still open: US Merchant feed `read_markets` scope, Google Customer Reviews opt-in, return/shipping annotations, FAMILY10 promotion (owner packet) |
| O7 | Genuine reviews and stars (#6, D6) | Judge.me past-order import; review-request emails; Google product-ratings feed | S/O | Owner packet item. Never seed or move reviews |
| O8 | Product JSON-LD remainder (#14) | `snippets/jsonld-seo.liquid`: `AggregateOffer`/`ProductGroup` variants, `shippingRate` derived not hard-coded 0, Rich Results Test | T | Return policy and deliveryTime are done |
| O9 | Page weight remainder (#15) | Header country/language SVGs (~73 KB per page), 28-30 external scripts, inline JS over 20 KB | T | Anchor `2026-09-27-ceo-sprint-collection-facet-weight-cut` next action |
| O10 | Localized head copy (#13) | Hub copy in no, da, fi, cs, ro, he for the `matching-outfits` hub; other 14 locales done | T+S | Routed to the translation lane on 09-28 |
| O11 | Non-whitelisted thin-collection noindex path (#11) | Any collection with fewer than 3 visible products | T | Never tested live (only the whitelisted `family-swimsuits`). Candidates: `jumpsuits` 4, `valentines-day-matching-outfits-1` 4, `pants` 5 all above 3; `siblings-matching-outfits` has 3 |
| O12 | Empty duplicate hubs | `family-swimsuits` (19 per admin) verified 0 products on 09-27; recheck | S | Fill or drop from sitemap |
| O13 | 28-day GSC measure | `matching-outfits` hub, head terms, couples, pajamas, tops, sweaters, Thanksgiving | O | External clock: read GSC on **2026-10-26**. Kill rule: Thanksgiving week with no gain and 0 clicks |
| O14 | GSC brief: mommy-and-me (3,700 impr, pos 51) and couples (3,380 impr, pos 41) are authority/link gaps, not copy | `/collections/mommy-and-me`, `/collections/couples` | S+O | Needs internal links from articles and off-site mentions (backlog #6, #16, #24) |
| O15 | Rules already in place (no action) | Keep seasonal products ACTIVE out of season: `ops/sourcing/CONTINUOUS-EXPANSION-WORKFLOW.md` line 143 | done | The archive-and-delete churn cause (D1) is now a documented rule |

Stale or superseded: D8 / fix #9 (`?variant=` noindex) was already absent live; the `popular-family-matching` hub choice was superseded by `matching-outfits` (`7aafd97`).

---

## 3. Live inventory (LIVE, 2026-09-28)

### 3a. Collections: 50 in the sitemap
Counts are Admin API `productsCount` (membership, inflated: `new-arrivals` reads 843 but only 301 products are ACTIVE). Use them for relative size only.

Head/hub: `matching-outfits` (family hub), `mommy-and-me`, `daddy-me` (`daddy-and-me` canonical to it), `christmas-pajamas`, `matching-family-christmas-outfits`, `christmas-sweaters`, `christmas-tops`, `thanksgiving-family-outfits`, `halloween-family-pajamas`, `valentines-day-matching-outfits-1`, `family-photo-outfits`, `matching-family-vacation-outfits`, `couples`, `matching-couples-t-shirts`, `siblings-matching-outfits`, `maternity`, `family-pajamas`, `pajamas`, `family-tops`, `family-sweaters`, `sweaters`, `family-sets`, `swimsuits`, `family-swimsuits`, `trunks`, `mother-daughter-matching-dresses`, `dresses`, `maxi-dresses`, `midi-dresses`, `mini-dresses`, `sundresses`, `formal-dresses`, `rompers`, `jumpsuits`, `tops`, `bottoms`, `leggings`, `pants`, `matching-hawaiian-outfits`, `daddy-me-shirts`, `daddy-me-t-shirts`, `fall-winter`, `new-pajama-drop`.
Duplicates/aliases still self-canonical or indexed: `best-sellers` (521, H1 "Best Sellers"), `new-matching-outfits` (522, H1 "New Mommy and Me Outfits"), `new-arrivals` (843), `popular-mommy-me-1`, `popular-family-matching`, `new-women-outfits` (canonical to matching-outfits in English only), `daddy-and-me`, and `dresses` vs `mother-daughter-matching-dresses` (both 133 members, both self-canonical; live check on `dresses` shows its own canonical).
Not in sitemap (hidden): `family-bundle-eligible`, `skirts-archived`, `matching-family-pet-outfits` (pet: leave hidden).

### 3b. Blog `news`: 70 published articles (192 more are unpublished "[Archived duplicate]" drafts, not in the sitemap)
Fresh 2026 Christmas set (3): `matching-family-christmas-pajamas-guide-2026`, `matching-family-christmas-sweaters-guide-2026`, `family-christmas-photo-outfits-2026`.
Holiday/seasonal relevant to Q4 (title; publishedAt shown in the theme):
- Thanksgiving (5): `best-matching-outfits-for-thanksgiving-dinner` (rewritten 09-28, "Matching Family Thanksgiving Outfits: Ideas for Dinner and Photos", dated 2016), `thanksgiving-family-matching-outfit-ideas`, `mommy-and-me-thanksgiving-style-guide`, `cozy-matching-outfits-for-the-thanksgiving-holiday` (dated 2019), `fall-family-photo-outfits-for-november` (dated 2018).
- Christmas/holiday (4): `christmas-matching-family-pajamas` (2025-12-04), `holiday-family-matching-outfits-complete-guide`, `black-friday-deals-top-matching-family-outfits` (dated 2017), `new-year-new-matching-looks-family-fashion`.
- Halloween (3): `halloween-family-matching-costume-ideas`, `mommy-and-me-halloween-outfits-that-are-actually-stylish` (dated 2018), `matching-family-outfits-for-pumpkin-patch-photos` (dated 2016).
- Valentine's (2): `mommy-and-me-valentines-day-outfits`, `adorable-matching-valentines-day-looks-for-the-whole-family` (dated 2016).
- Fall (about 14): `fall-family-matching-outfits`, `fall-family-photo-session-complete-matching-outfit-guide`, `autumn-matching-family-style-plaid-flannel-and-more`, `best-fall-colors-for-family-matching-looks`, `fall-festival-...`, `apple-picking-...`, `october-family-style-...`, `best-family-matching-outfits-for-harvest-season`, `pumpkin-spice-...`, `coordinating-family-outfits-for-october-events`, `mommy-and-me-fall-fashion-...`, `daddy-and-me-fall-outfit-ideas`, `transitioning-from-summer-to-fall-...`, `september-style-guide-...`.
- Evergreen: `the-complete-guide-to-family-matching-outfits`, `what-to-wear-for-family-photos-matching-outfit-ideas` (1,088 words), `matching-outfit-sizing-guide-right-fit-for-everyone`, `how-to-care-for-your-matching-family-outfits`, `mommy-and-me-matching-outfit-ideas`, `mommy-and-me-outfits-for-every-budget`, `daddy-and-me-matching-outfits-the-ultimate-guide`, `family-matching-pajamas-our-top-picks-for-cozy-nights`, `ultimate-gift-guide-matching-outfits-for-every-occasion`, `best-matching-family-outfits-for-winter`, `winter-family-photo-outfits-matching-looks-for-cold-weather`, `how-to-style-cozy-mommy-and-me-looks-in-january`.
- Spring/summer/other (about 25): Easter (3), Mother's Day (2), Father's Day (1), spring (5), summer/beach/swim (10), back-to-school (3), patriotic (1), daddy-and-me spring/summer.
**Zero live articles** on: couples/his-and-hers, maternity, siblings, cruise/Disney/vacation packing, family reunion, size conversion, "how to match without being identical". Fifteen draft articles exist in `ops/content/style-journal/articles/` (on origin/main) and are not live: `couple-matching-pajamas-holidays-anniversaries-gifts`, `matching-couple-outfits-the-complete-guide`, `matching-couple-outfits-date-night-travel-gifts`, `maternity-matching-outfits-complete-guide-for-expecting-moms`, `matching-family-cruise-outfits-what-to-pack`, `matching-family-outfits-for-disney-trips`, `family-reunion-matching-shirts-outfit-ideas`, `family-vacation-outfits-beach-cruise-resort`, `how-to-choose-mommy-and-me-matching-outfits-for-family-photos`, `daddy-and-me-*` (5). They predate the current honesty rules and product set; each needs a claims and link pass before publishing (Disney is IP-adjacent: skip).

### 3c. Critical defect found in the live blog (LIVE, Admin API + one live check)
- **55 of 70 live articles link to products that are no longer ACTIVE: 265 links, 241 distinct handles.** Live check: `/products/mother-and-daughter-matching-swimsuit` returns **404** (from `spring-break-matching-looks-for-the-whole-family`). This includes every Q4 article except the rewritten Thanksgiving post and the 3 new Christmas guides: `christmas-matching-family-pajamas` (3 dead), `holiday-family-matching-outfits-complete-guide` (7 of 7), `thanksgiving-family-matching-outfit-ideas` (7 of 7), `mommy-and-me-thanksgiving-style-guide` (7 of 7), `cozy-matching-outfits-for-the-thanksgiving-holiday` (7 of 7), `new-year-new-matching-looks-family-fashion` (9 of 9), `mommy-and-me-valentines-day-outfits` (3 of 3).
- Dead collection links: `/collections/family-matching` (6 articles, redirects), `/collections/headbands` (3 articles).
- **Unsupported claims in 60+ old articles:** "one of our bestsellers" (44 articles), "happiness guarantee" (25), "free shipping on all orders" (21; current wording is "standard shipping included"), one Disney mention.
- **Fake publish dates:** 34 articles are dated 2016-2023, but Shopify created 54 of them on 2026-03-25 (the store's own history starts in 2017). The GSC brief already showed Google serving "a blog post dated 2016". Only 5 of 70 articles have an SEO title override and 11 have a meta description override.

### 3d. Q4 2026 gap table (WebSearch, 8 queries, US)

| Query | Live page today | Gap | Who ranks (competitor type) | Demand read |
|---|---|---|---|---|
| matching family christmas pajamas | `/collections/christmas-pajamas` (17 products), guide-2026, older `christmas-matching-family-pajamas` article | Covered, but the old article competes with the new guide and has 3 dead links | Big retailers (Target, Kohl's, Hanna Andersson, PatPat, Pajamagram, Tipsy Elves, Burt's Bees), Forbes "best of" | Very high commercial; head term is unwinnable near term, win long-tail and Merchant free listings |
| family christmas photo outfit ideas | `family-christmas-photo-outfits-2026` (already appears in Google), `family-photo-outfits`, hub | Covered. Needs internal links, indexing, and a refresh in November | Photographers, Minted, Chatbooks, Kate Backdrop, blogs | High informational, strong hand-off to purchase; 9 of the top results are blogs, so the format fits |
| thanksgiving family outfits | `/collections/thanksgiving-family-outfits` (30), 5 articles | Cannibalized: 5 overlapping articles, 3 of them with 100% dead product links | Walmart, Etsy, Amazon, Target, Pinterest, Sparkle In Pink, blogs | Real but short window: order-by ~Nov 8-10 |
| mommy and me christmas dresses | **None; and 0 ACTIVE Christmas dress products** | Product gap, not a page gap. Do not build a thin "dresses" page | Etsy, Amazon, Sparkle In Pink, MatchingLook, Pinterest (product-led) | High; only servable by adding 2026 Christmas dresses (merch queue) or by targeting "mommy and me christmas outfits/pajamas/sweaters" instead |
| mommy and me christmas outfits / pajamas | Hub `matching-family-christmas-outfits`; 34 Christmas products carry the Mommy and Me tag | No mommy-and-me-specific Christmas page or article | Same retailers | Good; write one article, avoid a duplicate collection |
| matching couples christmas pajamas | `couples` collection (adult-size family sets), no article, no Christmas couples page | **Gap** | Walmart, Tipsy Elves, Fashion Nova, Pajamagram, My Couple Goal, a wedding blog | High; `couples` already has 3,380 impressions at pos 41 |
| family halloween costumes matching | `halloween-family-pajamas` (5 Halloween products), 2 articles | Covered as far as honest; costume SERP is IP characters (Toy Story, Bluey, Marvel, Mario) and costume retailers | GMA/ABC, Tipsy Elves, costume shops | Cutoff Oct 15; only the "Halloween pajamas / coordinating colors" angle is winnable |
| valentines day mommy and me outfits | `valentines-day-matching-outfits-1` (4 products), 2 older articles (one already visible: "10 Adorable Matching Looks") | Thin collection, handle ends in `-1`, 6 dead links across the two articles | Walmart, Sparkle In Pink, PatPat, MomMeMatch, Styl'd Grace | High from mid-January; needs indexing by December. 3 Valentine and 24 heart-design products exist |
| new year family pajamas / NYE | 1 article (9 dead links) | Gap, small | not searched | Low-medium |

Q4 conclusion: the missing pages are couples-Christmas, mommy-and-me-Christmas, a Valentine's hub with real products, and a cleanup of the overlapping Thanksgiving and Christmas-pajama articles. Everything else exists and is broken more than it is missing.

---

## 4. Ranked backlog (top 25)

Ranking = expected organic sessions x purchase intent x time-to-rank, weighted by the season clock. "A" marks items an agent can run unattended through the Admin API (with a claim in `ops/AGENT_COORDINATION.md`, before-state saved, readback after).

| # | Action | Target | Type | T/S/O | Why |
|---:|---|---|---|---|---|
| 1 | **Repair the 265 dead product links in 55 live articles.** Map each dead handle to the closest ACTIVE same-intent product or the best collection (Christmas→christmas-pajamas/christmas-sweaters, dresses→mother-daughter-matching-dresses, tees→family-tops, swim→swimsuits). Order: Christmas, Thanksgiving, Halloween, Valentine's, New Year first. Save `body` before-state, use `articleUpdate`, then re-register translations | `christmas-matching-family-pajamas`, `holiday-family-matching-outfits-complete-guide`, `thanksgiving-*` (3), `mommy-and-me-valentines-day-outfits`, `new-year-new-matching-looks-family-fashion`, then the remaining ~45 | S (A) | Every Q4 article sends shoppers to a 404 today; also feeds the GSC 404 count |
| 2 | **Strip unsupported claims in the same pass:** "one of our bestsellers", "happiness guarantee", "free shipping on all orders" → "standard shipping included", delete Disney mention | 44 + 25 + 21 articles, `the-complete-guide-to-family-matching-outfits` | S (A) | Truth rule; also lowers helpful-content risk |
| 3 | **Recover the 152 lost ranking URLs**: owner exports GSC Pages (16 months) or the agent reads it in the logged-in Chrome profile; diff against sitemap; 301 each to the same-intent collection (not `/collections/all`); restore any still-sourceable product | 21,682 impressions at pos 7-14 | S (+O export) | Largest proven pool of near-page-1 impressions; redirects are reversible by ID |
| 4 | **Push indexing for the Christmas cluster in GSC** (Request indexing) | `christmas-pajamas`, `christmas-sweaters`, `christmas-tops`, `matching-family-christmas-outfits`, `family-photo-outfits`, the 3 guides | O | Christmas is 31% of 2025 sales; pages must be indexed in October. Prior session already did this for 6 URLs, so the profile works |
| 5 | **Collapse Christmas-pajama article cannibalization**: 301 `christmas-matching-family-pajamas` → `matching-family-christmas-pajamas-guide-2026` (or rewrite it as a different intent, e.g. baby/toddler sizing); refresh `holiday-family-matching-outfits-complete-guide` to link the three guides | 2 articles | S (A) | One page per intent; the 2026 guide has 15 live products |
| 6 | **Couples Christmas article + `couples` collection intro**: "Matching Couples Christmas Pajamas and His-and-Hers Holiday Sets" built from the ACTIVE adult-size sets (Father/Adult sweater, pajama sets); retune the local draft `couple-matching-pajamas-holidays-anniversaries-gifts`; link from `couples`, `christmas-pajamas`, hub. Say "adult sizes of our family sets", no invented couple-only claims | new article; `couples` | S (A) | Empty SERP slot for us; `couples` has 3,380 impressions at pos 41 with no supporting article |
| 7 | **De-duplicate the mommy-and-me and dresses clusters in the theme**: canonical `new-matching-outfits`, `best-sellers`, `new-arrivals` (all 520-840-member supersets) to their head collection or noindex them; `dresses` → `mother-daughter-matching-dresses` (or the reverse, per GSC clicks); drop "Best Sellers" and "Popular" wording | `layout/theme.liquid` canonical block; collection titles | T+S | Same cannibalization that put head terms on pages 3-5 (D3); removes a bestseller claim |
| 8 | **Consolidate Thanksgiving to two pages** (collection + `best-matching-outfits-for-thanksgiving-dinner`); 301 the other three articles (`thanksgiving-family-matching-outfit-ideas`, `mommy-and-me-thanksgiving-style-guide`, `cozy-matching-outfits-for-the-thanksgiving-holiday`) and fold their best paragraphs into the survivor. Do it now: order-by ~Nov 8-10 | 3 articles | S (A) | 690 impressions at pos 30 were split across variants and an old 2016-dated post |
| 9 | **Mommy and me Christmas outfits article** ("Mommy and Me Christmas Outfits: Pajamas, Sweaters and Tops", 34 products carry the tag; state plainly that no dresses are offered) + link from `mommy-and-me`, hub, christmas-pajamas | new article | S (A) | Real query, no page; avoids a duplicate collection and an unsupported dress promise |
| 10 | **Valentine's hub**: rename/retarget `valentines-day-matching-outfits-1` (handle stays), rule = heart designs (24 active heart products, 3 Valentine), 6+ products before publishing; refresh the 2 articles; link from hub and Feb nav. Merch queue adds red/heart 2026 designs (category opp #4, live by Dec 5) | collection + 2 articles | S (A) + merch | Peak demand mid-Jan to Feb 14; needs 6+ weeks to index. Empty-collection guard applies below 3 products |
| 11 | **Fix article dates**: set `publishedAt` for the 34 articles dated 2016-2023 to Shopify `createdAt` (2026-03-25) or hide the visible date | 34 articles | S (A) or T | Fake dates are a trust and freshness defect; the GSC brief showed one served as "2016" |
| 12 | **Article SEO fields**: write `global.title_tag` (65 missing) and `description_tag` (59 missing) for the Q4 and evergreen articles, with the exact query in the title | all 70, Q4 first | S (A) | CTR on pages already at pos 8-30; cheap |
| 13 | **Kids-to-adult size conversion and matching-set sizing guide** (linkable asset): child age/height to size, "how to size a matching set for a family of 4/5/6", adult chest/waist table pulled from the store's real size charts; evergreen and quotable by AI assistants. Extend `matching-outfit-sizing-guide-right-fit-for-everyone` rather than creating a sibling | 1 article + `size-guide` page link | S (A) | Sizing is the top objection; evergreen links and citations; no claims needed |
| 14 | **Christmas product SEO fields**: verify title and meta pattern on the 41 Christmas products carry "matching family Christmas pajamas/sweaters" head terms (current pattern is good: "Christmas Reindeer Family Sweaters"); fix the 2 active products missing SEO fields | 41 products + 2 | S (A) | Product snippets and merchant listings are the best Google surface (pos 2.1) |
| 15 | **Enable/verify the AI-assistant path**: ChatGPT was the best unpaid intent source (207 sessions, 23 carts). Confirm Shopify agentic storefronts / ChatGPT channel is on (owner terms step), keep facts consistent (shipping window, returns, sizing) on policy pages, and confirm Bing has the sitemap | Shopify channels | O | ChatGPT search and Copilot draw on Bing; low effort, high intent |
| 16 | **Bing Webmaster Tools**: import from GSC, submit the sitemap, enable IndexNow if not automatic | bing.com/webmasters | O | Bing+Yahoo+DDG was 76 orders in 2024-26; Christmas pages get crawled faster |
| 17 | **Halloween refresh before Oct 15**: update the two Halloween articles and the pumpkin-patch post with live products only, link `halloween-family-pajamas`; frame as "coordinated Halloween pajamas and colors", not costumes | 3 articles | S (A) | Window closes in 17 days; costume SERP is IP and retailers, so keep to the winnable angle |
| 18 | **Family-photo hub**: title/H1/intro for `family-photo-outfits` targeting "family photo outfits" with a color-palette guide (2-3 palettes, how to mix solids and plaids for 3-8 people); link the Christmas photo article and the evergreen `what-to-wear-for-family-photos` | `family-photo-outfits` | T+S | Photo season Oct-Dec; strong informational-to-buy path, and this article type already ranks for us |
| 19 | **Siblings page and article** (`siblings-matching-outfits`, 3 products): intro/guide copy plus "Big sister little brother Christmas sweaters" article; add to nav at 3+ products (already done) | collection + article | S (A) | Zero competition on our side, small but high-conversion; supports 4-5 piece baskets |
| 20 | **Pinterest organic**: 5-10 original Pins per week using the 4-image photoshoots, each linking to a live collection or guide (Christmas pajamas, photo outfits, couples, Valentine's); boards per season | Pinterest account | O (off-site posting needs owner yes) | Visual niche; Pinterest gave 2.9k impressions in 30 days and a catalog is already ingested; long-lived Pins rank for months |
| 21 | **Judge.me past-order review import and review-request emails** | Judge.me | O | Stars lift CTR on every organic and Shopping result; theme already emits `aggregateRating` |
| 22 | **Merchant free-listing extras**: return policy and store rating, FAMILY10 promotion tag, shipping annotation | Merchant 513542500 | O | Free, on the site's best Google surface |
| 23 | **Off-site linkable asset outreach**: pitch the sizing guide and the photo-palette guide to mom bloggers/photographers and post in relevant communities. Owner approves each post; no paid placements | off-site | O | Authority is the stated gap for `mommy-and-me` (pos 51) and `couples` (pos 41) |
| 24 | **Article template**: show "Last updated", drop the fake byline dates, per-article product cards from the ACTIVE catalog so dead links cannot recur; add a scheduled check that flags any article link to a non-active product | `templates/article.json`, `snippets/style-journal-internal-links.liquid`, `ops/scripts` | T | Prevents the #1 defect from returning each time products are archived |
| 25 | **Later-season pipeline (start December)**: Lunar New Year (Feb 6; category opp #10), Easter Mar 28 (live by Jan 15), Mother's Day May 9 (live by Mar 1), Father's Day; publish the article one week after the merch goes live, not before | new articles | S | Keeps seasonal pages ACTIVE and indexed year-round per the D1 rule |

Deliberately not on the list: paid ads; pet pages (owner rule); licensed-character costume content (Grinch, Bluey, Toy Story, Peter Rabbit removed earlier); a "mommy and me Christmas dresses" collection (0 products); publishing the 15 old draft articles without a claims and link pass; removing languages (creates 404s).

## 5. Suggested execution order (AI speed)
1. Now, unattended (S): #1 and #2 in one script, then #11, #12, #5, #8, #14; save before-states, one claim, translation re-registration for changed articles.
2. Owner yes needed: #4 (GSC login is the owner's Chrome profile), #15, #16, #21, #22, #20/#23.
3. Then new content in this order: #6, #9, #18, #13, #10 (needs merch), #19.
4. Theme (one commit to `main`, then verify Shopify sync): #7, #24, O8/O9.
5. External clocks: Oct 15 (Halloween cutoff, Christmas hero flips Oct 16), Oct 26 (28-day GSC read), Nov 8-10 (Thanksgiving cutoff), Dec 5-8 (Christmas cutoff), Dec 26 (hero reverts to Halloween copy on Jan 1: needs a winter edition).

## 6. Evidence and limits
- Live checks used 12 site fetches (sitemap index, collections, blogs, agentic sitemap, atom feed, 3 collection pages, llms.txt, agents.md, robots.txt, one product URL) plus read-only Admin API queries (collections, articles, products). No writes.
- The dead-link count treats any `/products/<handle>` not in the ACTIVE set as dead; one was confirmed 404 live, the rest were not fetched individually (some may 301). `LIVE_READBACK_REQUIRED` for the exact status split before mapping.
- Demand statements come from 8 WebSearch queries (SERP composition only, no volumes). GSC numbers are quoted from the 09-28 GSC brief and `seo.md` (Feb-Apr and Jun-Sep windows).
- Product counts: 301 ACTIVE products (Admin API), 41 Christmas, 0 Christmas dresses, 5 Halloween, 3 Valentine, 24 heart designs, 3 siblings.
