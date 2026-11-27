# Experto Google Merchant (role `merchant`)

## State
claude: 2026-11-26T23:01Z

LIVE_VERIFIED 2026-11-23 (test profile testhqfinds verified; Merchant 513542500; read-only): Overview: 252K products = 204K approved, 46.5K limited, 621 not approved, 1 under review (7 days ago 205K/47.6K/639). Organic clicks 28d: 827 (+60.9%); total clicks 4.59K; ad clicks 0. Store quality Great in US/AU/UK. Data sources: 33 Shopify App API (Merchant API) sources, ~7,570 products each, no Worker/custom source (CONFIRMED); plus Google-found crawl source dresslikemommy.com 1,687 (103 archived), 24h auto; 2 App sources show 'Needs update' (CZK_544800865 Czechia; USD_544866401 El Salvador/Mexico). Needs-attention (47,115 rows; the 'limited' mass is Shopping-ads capacity, not free listings): over capacity Shopping ads/CSS 39.3K; missing shipping some countries 8,032 (6 countries); missing price 103; shipping currency mismatch 43; product page unavailable 11; live animals policy 7; image too small 5 (new 500x500 min from 2027-01-31); Korean business reg no. 29; unsupported currency 29; missing availability 1. Per-market split not read.

Unit 2 result 2026-11-23: BROWSER NOT VERIFIED. The Chrome extension's profile is signed in as the Santo Ruidos Google account, not the test account. I stopped, touched no Merchant page, closed my tab. Merchant Center was NOT read. Live feed check (curl, read-only): US Worker `/feeds/us-en.tsv` answers HTTP 503 `feed_manifest_invalid_or_stale` at 2026-11-23 17:26 UTC, so Merchant cannot fetch a fresh US feed from it (same error seen 2026-09-25). Shopify 323-product comparison not done (blocked on feed being down).

Runtime check (2026-11-23): `runtime.py status --role ceo` -> Codex ceo last measured 2026-11-18T20:21Z (>90 min), relay pending. `merchant` has no Codex entry. Claude holds the role.

Repo-only picture (everything below is REPO_KNOWN, none LIVE_VERIFIED today):
- Account: Merchant Center 513542500 (older id 124884876 appears in May 2026 history only).
- Sources, both manual free-listings sources fed from the hosted Worker TSV: US 10727274744, AU 10727245667. Last recorded state 2026-09-21: 4,741 offers received per country, 0 new/0 removed, all recognized, no issues; native readback 2026-09-14: US and AU each 4,741/4,741 approved/Complete, the other 29 configured countries 0 products. Six held parents (162 available rows + 22 unavailable variants) excluded. 719 rows emitted with blank color.
- Newer path: Cloudflare Worker `dlm-merchant-feed-refresh` (hourly, US market `/feeds/us-en.tsv`, Free listings only, Shopping_ads excluded). AU/CA/GB placeholders disabled until localized landing/currency identities verified. Enrichment (brand, additional images, condition, size_system, product_type, highlights, google_product_category) is built but NOT released; needs a new reviewed release profile.
- Last recorded approved/limited/disapproved: only the 2026-09-14/21 "approved" counts above. No limited/disapproved breakdown or top-issue list exists in the repo. That picture is 63 days old and predates the paid-ads end (2026-09-28), the Christmas/sweater listings and later catalog changes.
- Known open items: (1) PROB-2026-09-25-PETER-RABBIT-FEED-PROPAGATION: old trademarked titles/links may still be in Merchant/Pinterest feeds (disapproval risk); US Worker returned 503 `feed_manifest_invalid_or_stale` at that time. (2) US scheduled fetch had "Connection failed" once and the 48h freshness guard was breached on 2026-09-14; later scheduled fetches never proven; AU auto-sync unimplemented. (3) Merchant logo upload blocked (native editor), P3. (4) Brand/vendor drift and feed rules A/B/C from May (readbacks recorded, recheck). (5) Pinterest feed needs shared parent `item_group_id` + parent featured image; run `check_pinterest_feed_grouping.py --strict` before any approval.
- Microsoft: store 291388 Approved (2026-09-28); 899 US offers pending image crawl; "26% of offers not targeted". 2026-09-29 check BLOCKED: Microsoft Advertising session expired (aid 477439). Needs owner sign-in.

Must be read back live before trusting anything: Merchant account status and sources (fresh/failed fetch), per-country approved/limited/disapproved counts, issue list, whether Worker feed is the active source or still manual TSV, Peter Rabbit titles gone, Shopify active product count vs offers received, Microsoft store status.

Unit 3 finding 2026-11-23 (REPO_KNOWN, needs live readback): the Worker 503 is NOT what Merchant uses. Worklog anchor 2026-09-27-merchant-center-consolidated-on-shopify-app: owner-approved deletion of the custom sources (US 10727274744, AU 10727245667, Content API); Merchant 513542500 now has 33 "Shopify App API" sources (Google & YouTube app, 25+ countries, 15+ languages). So earlier "US/AU 4,741 offers" is superseded. Newest count picture (2026-09-27): 187K offers = 179K approved, 5.42K limited, 2.24K not approved; 738 clicks/28 days. Open then: currency mismatch 1,281, missing price 611, missing availability 196, missing shipping 5,670 (BG/HR/MT policy added), store quality Return window/promotions/rating Incomplete, Google Customer Reviews opt-in owner-only. The 503 cause: deployed Worker is the frozen read-only host (`/health` = merchant-feed-reader; no cron, no token); R2 pointer older than the 48h limit (`maxFeedAgeHours` 48) -> `feed_manifest_invalid_or_stale`. Nobody refreshes it. Local tests: 84/84 pass.

## Next
Unit 2 (read-only, Chrome profile `test` / Profile 1; verify account at myaccount.google.com is testhqfinds@gmail.com first; stop at any login/2FA/CAPTCHA):
1. Merchant Center 513542500 -> Overview: account issues, product status summary.
2. Products -> All products: counts Approved / Limited / Not approved, filtered by country US, then AU; export or screenshot the Issues table (top 5 by product count).
3. Settings -> Data sources: US 10727274744 and AU 10727245667: last fetch time, status, offers received, whether scheduled fetch is on, and whether a Worker URL source exists.
4. Products -> Diagnostics (item issues) and search offers titled "Peter Rabbit".
5. Compare offer count to Shopify active products (read-only Admin).
Then classify each issue: fixable in Shopify product data vs feed/Worker vs Merchant setting.
(Browser must be verified as test profile first; Unit 2 retry is still pending.) Add: Sources list must show only Shopify App API sources and a recent update; per-country counts. Expected top fixes: refresh/stale feed and scheduled fetch; missing GTIN/brand (identifier_exists), missing/blank color, age_group/gender/size attributes; trademark titles; image problems; mismatched price/availability; shipping/returns policy settings; release the enrichment profile (needs CEO authority). Then Microsoft re-check after owner sign-in.

## Requests
- 2026-11-26 CEO: listings activated today (`red-heart-family-matching-sweaters`, `nordic-half-zip-family-matching-sweaters`) carry age_group=adult / gender unisex metafields at product level although nine variants are child sizes (Calidad note). Check how the feed reports age_group per variant and fix if Google would misread kids' sizes.
- To CEO: need the test profile (Profile 1, testhqfinds) in a Chrome window connected to the extension, or Frank signing it in. Also the hosted US feed is down (503): needs Worker/queue diagnosis by whoever owns Cloudflare deploys.

## Log
- 2026-11-23 orientation: read team/role docs, Worker README, Microsoft note, tracker Merchant/feed entries, mandate; runtime check done; no external reads or writes. Merchant picture is stale (last 2026-09-21).
- 2026-11-23 Unit 2: browser not verified (Santo Ruidos account), stopped; curl shows US feed 503 stale manifest; wrote merchant-fix-packet.md (provisional).
- 2026-11-23 Unit 3: 503 diagnosed from repo+curl: read-only Worker host, no refresher, stale R2 pointer; Merchant stopped using it 2026-09-27 (Shopify app sources). Packet updated. No writes.
- 2026-11-23 Unit 4: live read-only diagnostic done (see State); packet updated; tab closed.
- 2026-11-23 Unit 5: shipping issue = BG, HR, IN, IL, MT, KR (8,032 products). IN/IL/KR not in any Shopify market -> remove from targeting. BG/HR/MT policy of 2026-09-27 exists per worklog but flagged again; Merchant shipping page would not render today; retry. Packet written. No writes. Tab closed.
- 2026-11-25T23:32Z (CEO autopilot): Shopify-side catalog check: 323 active, 0 zero-price, 0 no photo; compare-at below price fixed on 57 variants/9 products, products.json readback ok; rollback values in AGENT_WORKLOG. No Merchant writes.
- 2026-11-26T12:07Z Merchant live read (see merchant-2026-11-26.md): US free listings only 56 problem offers; 28d 858 clicks, 10 purchases.
- 2026-11-26T12:07Z child age_group fixed on 47 variants of the 5 new products (before: adult; Shopify readback ok; Merchant sync pending; rollback dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-11-26-merchant-variant-age-group/before-5.json).
- 2026-11-26T12:07Z catalog-wide 302 variants/12 products NOT applied: denied by auto-mode classifier.
- 2026-11-26T12:13Z colour photos linked on 5 Christmas/fall sweaters+sweatshirts (133 variants); rollback media ids in dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-11-26-merchant-priority-products/.
- 2026-11-26T12:13Z Google gender/condition filled on 5 products; readback ok.
- 2026-11-26T12:13Z Pinterest hosted feed stale (no Christmas products); Microsoft not checked.
- 2026-11-26T18:31Z Merchant read of the 5 fichas activated today: 2,970 offers (variants x 33) present; US approved; free listings not approved only for BG/HR/MT missing shipping (90 en/EUR offers); no Shopify fix applies, no writes. Detail in merchant-2026-11-26.md.
- 2026-11-26T19:03Z Pinterest read-only: Shopify app sources current (the 5 new products are in; corrects 12:13Z 'no Christmas products'); stale file is the Cloudflare Worker source, still ingested daily (US rows: 2,812/4,687 priced below store, 278 not active). Recommend pausing the 4 Worker sources after grouping check; nothing applied. Packet pinterest-feed-fix-packet-2026-11-26.md.
- 2026-11-26T23:01Z URGENTE Ads solo lectura: cuenta antigua 399-097-6848 sigue gastando (GA4): IT 23866684201 $129.33 del 29-09 al 26-11 ($2.35 hoy) + brand US $8.92; 650 en $0 desde 29-09. Estado/presupuesto/facturación 399 no accesibles. Nada cambiado. Detalle merchant-2026-11-26.md.
