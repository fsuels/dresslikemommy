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

## Latest verdict (2026-10-02)

- **UP** on paper: 7-day organic avg 126.0/day (09-25 → 10-01) vs 60.1 the prior 7 (+110%). That window still includes the paid-ad tail (09-25 → 09-28: 91 / 156 / 298 / 126), so it overstates. The three clean days (77, 73, 61) average 70.3, against 55.1 for 09-16 → 09-24 (about +28%), but the clean days are drifting down (77 → 73 → 61). EXPECTED, not proven, until the clean week 09-29 → 10-05 closes.
- **Search funnel (09-30 + 10-01, the only rows with data):** 134 sessions → 6 carts → 1 checkout. 10-01: 61 sessions → 3 carts → 0 checkouts, 0 orders of any source.
- **Top landing pages (7d, 09-25 → 10-01):** /collections/new-women-outfits 55, /collections/mommy-and-me 47, /collections/dresses 45, /collections/pajamas 42, / 35.
- **What moved:** cause unknown beyond the paid-ad spike fading. No blog article is in the top 10 landing pages yet (the best product page is the smocked-dress set at 24).
- **Recommended action:** watch whether the clean-day level holds near 60-70 or keeps sliding; re-read 10-06 for the first full clean week. Meanwhile push internal links from the top collections (new-women-outfits, mommy-and-me) to the best products to lift the 3/61 cart rate.

## Daily rows (newest last)

Columns: date | search sessions | google | bing+ddg+yahoo | carts from search | checkouts from search | orders (search / all) | 7d avg search/day | vs prev 7d | note

| date | search | google | other engines | carts | checkouts | orders s/all | 7d avg | vs prev 7d | note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-29 | 77 | | | | | | 124.7 | +135% | first clean day after paid ads ended; 7d window still holds the paid-ad spike (09-25 → 09-28) |
| 2026-09-30 | 73 | 71 | 2 | 3 | 1 | 1 / 1 | 126.0 | +118% | the 1 search order was $23.99; 7d avg still inflated by the paid tail; clean days 09-29 + 09-30 avg 75 vs 53 for 09-15 → 09-24 |
| 2026-10-01 | 61 | 59 | 2 | 3 | 0 | 0 / 0 | 126.0 | +110% | no orders from any source; 7d window (09-25 → 10-01) still holds the paid tail; clean days 09-29 → 10-01 avg 70.3 vs 55.1 for 09-16 → 09-24 |

## Weekly Search Console rows (Mondays)

| week ending | clicks 7d | impressions 7d | CTR | avg pos | clicks 28d | impressions 28d | note |
|---|---|---|---|---|---|---|---|
