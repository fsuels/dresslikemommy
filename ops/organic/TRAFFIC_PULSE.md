# Traffic Pulse: real organic traffic, tracked daily

Owner, 2026-10-01: "We need to continually monitor real progress of traffic. SEO traffic! actual traffic that we care about."

This file is the scoreboard for every organic lane: engine articles, SEO rewrites, translations and new listings. The `traffic-pulse` routine appends one row per day. It runs the Shopify analytics connector (ShopifyQL) for sessions and Chrome (test profile) for weekly Search Console totals. Shopify days use the store timezone.

**What counts:** sessions whose `referrer_source = 'search'` (Google, Bing, DuckDuckGo, Yahoo, Ecosia) are organic, because paid ads have been off since 2026-09-28. Direct and unknown sessions are not counted: bots and ad tails inflate them.

**Read it like this:**
- **Headline:** the 7-day average of organic search sessions per day, against the previous 7 days and the same week last year.
- **Money:** search sessions → add-to-cart → completed checkout, and orders whose referrer is search.
- A single day means little. Act on 7-day trends only.

## Baseline (CEO, 2026-10-01 from Shopify analytics)

- **Search sessions per week:**
  - Same weeks of 2025: about 100–120.
  - 2026-08-31 → 09-14: 300–340.
  - Week of 09-21: 789, inflated by the last paid-ad days (09-25 → 09-28 spike: 91 / 156 / 298 / 126).
- **Clean organic days after ads ended:** 09-29 = 77, 09-30 = 73. The 09-10 → 09-24 average was about 50 per day.
  - So organic search is up about 50% on mid-September and about 3× on last year.
  - Treat 2 days as EXPECTED, not proven, until a full clean week exists (first: 09-29 → 10-05).
- **Funnel (last 14 days, Google organic only):** 1,128 sessions → 58 add-to-cart (5.1%) → 3 completed checkouts (0.27%).
  - Bing 59, DuckDuckGo 78 and Yahoo 44 sessions produced 0 carts.
  - Orders in the last 30 days: 12 total ($653). Google search accounts for 5 ($248); the other 7 have no referrer ($405).
- **Top organic landing pages (last 7 days):** /collections/new-women-outfits 56, mommy-and-me 47, dresses 47, pajamas 43, home 37, smocked-dress product 25, /it mommy-and-me 24, /it pajamas 21, swimsuits 20.
  - Blog articles barely appear yet. The best is /el mommy-and-me guide with 9. The 74 articles are young and need weeks to rank, so judge them from 2026-10-22 on.
- **Search Console (3 months to 2026-09-29):** 2.85K clicks, 139K impressions, CTR 2.1%, average position 16.9. See `GSC_STRIKING_DISTANCE.md`.

## Latest verdict (2026-10-06)

- **DOWN on paper, UP on clean days:** 7-day organic avg 76.7/day (09-29 → 10-05) vs 122.1 the prior 7 (-37%), but the prior week holds the paid-ad spike (91 / 156 / 298 / 126). This is the first full clean week: 77, 73, 61, 63, 76, 82, 105 (537 total); 10-05's 105 is the highest clean day. Clean week avg 76.7 vs 62.8 for 09-20 → 09-24 (+22%). Still EXPECTED, not proven; next week's comparison will be clean vs clean.
- **Search funnel (6 rows with data, 09-30 → 10-05):** 460 sessions → 31 carts → 3 checkouts. 10-05: 105 sessions → 4 carts → 0 checkouts, 0 search orders (1 order, $65.98, no referrer).
- **Top landing pages (7d, to 10-05):** / 34, /it/collections/mommy-and-me 17 (4 carts), /collections/swimsuits 15 (1 cart), /blogs/news/family-christmas-photo-outfits-2026 12 (0 carts), /it/collections/pajamas 10.
- **What moved:** cause unknown for 10-05's jump to 105. The Christmas photo-outfits article holds 12 sessions with 0 carts, and /el/ and /he/ blog articles show 7 and 6, so the articles keep getting search traffic. GSC not due (Tuesday).
- **Recommended action:** add internal links and a collection CTA from the Christmas photo-outfits article to the matching-sets collections to turn its traffic into carts (it has not converted yet); and the owner should fix Chrome access to Search Console so the Monday GSC row can run.

## Daily rows (newest last)

Columns: date | search sessions | google | bing+ddg+yahoo | carts from search | checkouts from search | orders (search / all) | 7d avg search/day | vs prev 7d | note

| date | search | google | other engines | carts | checkouts | orders s/all | 7d avg | vs prev 7d | note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-29 | 77 | | | | | | 124.7 | +135% | first clean day after paid ads ended; 7d window still holds the paid-ad spike (09-25 → 09-28) |
| 2026-09-30 | 73 | 71 | 2 | 3 | 1 | 1 / 1 | 126.0 | +118% | the 1 search order was $23.99; 7d avg still inflated by the paid tail; clean days 09-29 + 09-30 avg 75 vs 53 for 09-15 → 09-24 |
| 2026-10-01 | 61 | 59 | 2 | 3 | 0 | 0 / 0 | 126.0 | +110% | no orders from any source; 7d window (09-25 → 10-01) still holds the paid tail; clean days 09-29 → 10-01 avg 70.3 vs 55.1 for 09-16 → 09-24 |
| 2026-10-02 | 63 | 56 | 7 | 6 | 0 | 0 / 0 | 122.0 | +86% | no orders from any source; 7d window (09-26 → 10-02) still holds the paid tail (156 / 298 / 126); clean days 09-29 → 10-02 avg 68.5 vs 58.3 for 09-17 → 09-24 |
| 2026-10-03 | 76 | 73 | 3 | 10 | 1 | 1 / 1 | 110.6 | +38% | search order $51.98 (only order of the day); 7d window (09-27 → 10-03) still holds 298 / 126; clean days 09-29 → 10-03 avg 70.0 vs 60.1 for 09-18 → 09-24 |
| 2026-10-04 | 82 | 76 | 6 | 5 | 1 | 1 / 2 | 79.7 | -29% | search order $116.57, other order $68.98 (no referrer); 7d window (09-28 → 10-04) drops the 298 spike, prev 7d (09-21 → 09-27) still holds the paid tail; clean days 09-29 → 10-04 avg 72.0 vs 61.3 for 09-19 → 09-24 (+17%); GSC skipped: Chrome signed in as the wrong account, no access to the property |
| 2026-10-05 | 105 | 97 | 8 | 4 | 0 | 0 / 1 | 76.7 | -37% | other engines = duckduckgo 5 + yahoo 2 + yandex 1; only order was $65.98 with no referrer; first full clean week (09-29 → 10-05) avg 76.7 vs 62.8 for 09-20 → 09-24 (+22%); prev 7d (09-22 → 09-28) still holds the paid tail; highest clean day so far |

## Weekly Search Console rows (Mondays)

| week ending | clicks 7d | impressions 7d | CTR | avg pos | clicks 28d | impressions 28d | note |
|---|---|---|---|---|---|---|---|
