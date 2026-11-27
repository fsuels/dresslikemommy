# Traffic Pulse: real organic traffic, tracked daily

Owner, 2026-10-01: "We need to continually monitor real progress of traffic. SEO traffic! actual traffic that we care about."

This file is the scoreboard for every organic lane: engine articles, SEO rewrites, translations and new listings. The `traffic-pulse` routine appends one row per day. It runs the Shopify analytics connector (ShopifyQL) for sessions and Chrome (test profile) for weekly Search Console totals. Shopify days use the store timezone.

**What counts:** sessions whose `referrer_source = 'search'` (Google, Bing, DuckDuckGo, Yahoo, Ecosia) are organic, because paid ads have been off since 2026-09-28. Direct and unknown sessions are not counted: bots and ad tails inflate them.

**Method correction (2026-11-26):** paid Google Ads kept spending after 09-28, so `referrer_source = 'search'` includes ad clicks. Rows from 11-23 on subtract sessions whose landing URL carries gad_, gclid, gbraid, wbraid or msclkid, or utm_medium cpc. Earlier rows include ad sessions and are not comparable.

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

## Latest verdict (2026-11-23, Experto SEO; ShopifyQL, referrer_source=search)

- **UP:** 7-day organic avg 225.4/day (11-16 → 11-22, 1,578 sessions) vs 174.7 for 11-09 → 11-15 (+29%), and vs 114.0 on 10-07 → 10-13 (about 2x in six weeks). No scheduled routine ran since 10-15, so the rise is not from new articles.
- **Funnel, 11-09 → 11-22:** 2,801 sessions → 222 carts (7.9%) → 30 reached checkout → 12 completed (0.43% of sessions). Cart-to-checkout stays the leak (13% of carts reach checkout).
- **Top 14-day landing pages (sessions / carts / reached checkout / completed):** /it/collections/mommy-and-me 132/6/0/0; / 96/8/1/0; /it/collections/matching-outfits 48/7/0/0; /products/nordic-yoke-family-matching-sweaters 43/7/3/1; /collections/swimsuits 41/0/0/0; /it/collections/pajamas 33/0/0/0; /collections/sweaters 29/0/0/0; /cs/collections/matching-family-christmas-outfits 28/7/0/0; /ro/... christmas 24/10/0/0.
- **Cart loss:** zero-cart pages with real volume: swimsuits (41), IT pajamas (33), sweaters (29), family-sweaters (18/1), pajamas (15/0), sv/no dresses and homes (about 80). Carts that never reach checkout: cs and ro Christmas collections (17 carts, 0 checkouts), IT mommy-and-me and matching-outfits (13 carts, 0).
- **Gap:** 10-14 → 11-08 rows backfilled from ShopifyQL only (no google/other split, no all-source orders). GSC not pulled yet.

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
| 2026-10-06 | 95 | 93 | 2 | 7 | 0 | 0 / 0 | 79.3 | -36% | other engines = yahoo 2; no orders from any source; 7d window (09-30 → 10-06) is fully clean, prev 7d (09-23 → 09-29) still holds the paid spike (91 / 156 / 298 / 126); clean window avg 79.3 vs 61.0 for 09-21 → 09-24 (+30%) |
| 2026-10-07 | 105 | | | | | | 83.9 | n/a | backfilled from the timeseries only (no per-engine, cart or order data for this day); prev 7d needs 09-24, which is outside this run's 16-day query |
| 2026-10-08 | 111 | | | | | | 91.0 | -28% | backfilled from the timeseries only; prev 7d (09-25 → 10-01) still holds the paid tail (91 / 156 / 298 / 126) |
| 2026-10-09 | 83 | | | | | | 93.9 | -23% | backfilled from the timeseries only; prev 7d (09-26 → 10-02) still holds 156 / 298 / 126 |
| 2026-10-10 | 114 | 111 | 3 | 6 | 0 | 0 / 0 | 99.3 | -10% | other engines = yahoo 2 + duckduckgo 1; no orders from any source; highest organic day on record since ads ended; clean window 10-04 → 10-10 avg 99.3 vs 76.7 for the first clean week 09-29 → 10-05 (+29%) |
| 2026-10-11 | 148 | | | | | | 108.7 | +36% | backfilled from the timeseries only; highest organic day since ads ended; prev 7d (09-28 → 10-04) still holds the 126 paid-tail day |
| 2026-10-12 | 121 | | | | | | 111.0 | +45% | backfilled from the timeseries only; both 7d windows fully clean (10-06 → 10-12 vs 09-29 → 10-05) |
| 2026-10-13 | 116 | 115 | 1 | 6 | 0 | 0 / 0 | 114.0 | +44% | other engines = duckduckgo 1 (1 cart); no orders from any source; clean vs clean 10-07 → 10-13 avg 114.0 vs 79.3 for 09-30 → 10-06; third straight day above 115 |
| 2026-10-14 | 114 | | | 8 | 0 | 0 / n/a | 115.3 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-15 | 111 | | | 7 | 1 | 0 / n/a | 115.3 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-16 | 125 | | | 7 | 1 | 0 / n/a | 121.3 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-17 | 120 | | | 13 | 2 | 0 / n/a | 122.1 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-18 | 128 | | | 3 | 0 | 0 / n/a | 119.3 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-19 | 136 | | | 7 | 1 | 1 / n/a | 121.4 | n/a | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-20 | 128 | | | 10 | 3 | 1 / n/a | 123.1 | +8% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-21 | 138 | | | 11 | 1 | 0 / n/a | 126.6 | +10% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-22 | 126 | | | 10 | 1 | 1 / n/a | 128.7 | +12% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-23 | 110 | | | 8 | 1 | 1 / n/a | 126.6 | +4% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-24 | 111 | | | 7 | 0 | 0 / n/a | 125.3 | +3% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-25 | 181 | | | 13 | 5 | 3 / n/a | 132.9 | +11% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-26 | 147 | | | 7 | 3 | 2 / n/a | 134.4 | +11% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-27 | 130 | | | 9 | 1 | 1 / n/a | 134.7 | +9% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-28 | 157 | | | 11 | 1 | 0 / n/a | 137.4 | +9% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-29 | 142 | | | 9 | 2 | 2 / n/a | 139.7 | +9% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-30 | 130 | | | 12 | 0 | 0 / n/a | 142.6 | +13% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-10-31 | 108 | | | 8 | 1 | 0 / n/a | 142.1 | +13% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-01 | 154 | | | 15 | 4 | 2 / n/a | 138.3 | +4% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-02 | 144 | | | 20 | 2 | 1 / n/a | 137.9 | +3% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-03 | 175 | | | 16 | 2 | 1 / n/a | 144.3 | +7% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-04 | 165 | | | 16 | 3 | 2 / n/a | 145.4 | +6% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-05 | 165 | | | 19 | 3 | 2 / n/a | 148.7 | +6% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-06 | 152 | | | 19 | 5 | 2 / n/a | 151.9 | +7% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-07 | 145 | | | 16 | 1 | 1 / n/a | 157.1 | +11% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-08 | 171 | | | 12 | 0 | 0 / n/a | 159.6 | +15% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-09 | 175 | | | 14 | 0 | 0 / n/a | 164.0 | +19% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-10 | 140 | | | 9 | 1 | 0 / n/a | 159.0 | +10% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-11 | 169 | | | 11 | 2 | 0 / n/a | 159.6 | +10% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-12 | 194 | | | 16 | 4 | 2 / n/a | 163.7 | +10% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-13 | 135 | | | 12 | 0 | 0 / n/a | 161.3 | +6% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-14 | 176 | | | 21 | 3 | 2 / n/a | 165.7 | +5% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-15 | 234 | | | 24 | 4 | 0 / n/a | 174.7 | +9% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-16 | 188 | | | 13 | 2 | 2 / n/a | 176.6 | +8% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-17 | 275 | | | 11 | 1 | 1 / n/a | 195.9 | +23% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-18 | 228 | | | 18 | 3 | 1 / n/a | 204.3 | +28% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-19 | 198 | | | 15 | 3 | 1 / n/a | 204.9 | +25% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-20 | 203 | | | 17 | 1 | 0 / n/a | 214.6 | +33% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-21 | 221 | | | 22 | 2 | 1 / n/a | 221.0 | +33% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-22 | 265 | | | 19 | 4 | 2 / n/a | 225.4 | +29% | backfilled 2026-11-23 from ShopifyQL (referrer_source=search); google/other split and all-source orders not pulled; checkouts = sessions that reached checkout, orders s = sessions that completed checkout |
| 2026-11-23 | 271 | 264 | 7 | 12 | 0 | 0 / 2 | 226.1 | +41% | ORGÁNICO REAL (sin gad_/gclid/gbraid/wbraid/msclkid/cpc); compras en sesión 0; anuncios aparte: 11 sesiones, 1 carritos |
| 2026-11-24 | 226 | 220 | 6 | 21 | 2 | 1 / 4 | 220.6 | +23% | ORGÁNICO REAL (sin gad_/gclid/gbraid/wbraid/msclkid/cpc); compras en sesión 1; anuncios aparte: 12 sesiones, 0 carritos |
| 2026-11-25 | 174 | 166 | 8 | 17 | 2 | 0 / 2 | 214.6 | +14% | ORGÁNICO REAL (sin gad_/gclid/gbraid/wbraid/msclkid/cpc); compras en sesión 0; anuncios aparte: 8 sesiones, 1 carritos |
| 2026-11-26 | 129 | 124 | 5 | 9 | 0 | 0 / 4 |  |  | ORGÁNICO REAL (sin gad_/gclid/gbraid/wbraid/msclkid/cpc); compras en sesión 0; anuncios aparte: 13 sesiones, 0 carritos; DÍA PARCIAL hasta ~19:30 hora de la tienda, sin media 7d; primer día de los cambios del 26-nov |

## Weekly Search Console rows (Mondays)

| week ending | clicks 7d | impressions 7d | CTR | avg pos | clicks 28d | impressions 28d | note |
|---|---|---|---|---|---|---|---|
