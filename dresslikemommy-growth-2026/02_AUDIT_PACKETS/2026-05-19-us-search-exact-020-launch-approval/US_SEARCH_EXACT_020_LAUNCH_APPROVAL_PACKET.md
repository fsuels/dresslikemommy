# US Search Exact $0.20 Launch Approval Packet

Date: 2026-05-19

## Recommendation

Launch a tiny United States Google Search exact-match test from the API-proven `$0.20` winners.

This is a sales-learning test, not a scale build. The goal is to enter auctions cheaply, protect spend, and learn whether purchase-only ROAS can work before expanding match types or automation.

## Source Data

Primary source:

- `../2026-05-18-search-keyword-planner-us-020/google_ads_api_us_search_joined_decision_rows.csv`
- `../2026-05-18-search-keyword-planner-us-020/google_ads_api_us_search_forecast_rows.csv`
- `../2026-05-18-search-keyword-planner-us-020/google_ads_api_us_search_historical_rows.csv`

API filters:

- Client account: `399-097-6848`
- Geo: United States, geo target `2840`
- Language: English, language `1000`
- Network: Google Search
- Match types in source table: `26` exact, `3` phrase
- Forecast bid: `max_cpc_bid_micros=200000` (`$0.20`)
- Forecast period: `2026-05-20` through `2026-06-18`

Decision summary:

- `8` exact keywords are launch-priority.
- `2` exact keywords are micro-test-only.
- `19` rows forecast zero clicks at the `$0.20` cap and stay out of launch.
- `0` keywords have historical low top-of-page bid at or below `$0.20`, so this launch should expect constrained / lower-position delivery.

## Live Write Boundary

This packet is local and review-only until the owner gives fresh action-time approval.

Do not:

- Upload/apply the campaign.
- Enable spend.
- Add keywords, ads, negatives, bids, budgets, statuses, or campaign settings in Google Ads.
- Change conversion goals, Merchant feeds, Shopify products, Pinterest, billing, or credentials.
- Enable broad match, AI Max, Performance Max, Dynamic Search Ads, Search Partners, or Display expansion.

## Campaign Settings

Campaign name:

`DLM_US_SEARCH_EXACT_020_TEST_20260519`

Recommended launch state:

- If building for review only: create as `PAUSED`.
- If owner explicitly approves live test: create as `ENABLED`.

Core settings:

- Campaign type: Search only
- Network: Google Search only
- Search Partners: off
- Display Network: off
- Locations: United States
- Location option: presence only, not presence-or-interest
- Language: English
- Budget: `$5.00/day` maximum
- Bidding: Manual CPC if available; otherwise Maximize Clicks with bid limit
- Max CPC: `$0.20`
- Enhanced CPC: off at launch
- Conversion goal: purchase only
- Conversion value rule: product revenue/subtotal only, excluding shipping and tax
- Final URL expansion / automatically created assets / AI Max: off

## Launch Keywords

Use only these rows at launch:

| Ad group | Keyword | Match | Final URL | Forecast clicks | Forecast avg CPC | Launch note |
|---|---|---:|---|---:|---:|---|
| Pajamas | `[mommy and me pajamas]` | exact | `https://www.dresslikemommy.com/collections/pajamas` | 221.39 | `$0.135` | Priority |
| Pajamas | `[matching family pajamas]` | exact | `https://www.dresslikemommy.com/collections/pajamas` | 29.15 | `$0.111` | Priority |
| Pajamas | `[mommy and me pajama set]` | exact | `https://www.dresslikemommy.com/collections/pajamas` | 3.02 | `$0.120` | Priority |
| Swim & Beach Looks | `[mommy and me swimsuits]` | exact | `https://www.dresslikemommy.com/collections/family-swimsuits` | 191.66 | `$0.149` | Priority |
| Swim & Beach Looks | `[matching family swimsuits]` | exact | `https://www.dresslikemommy.com/collections/family-swimsuits` | 142.08 | `$0.145` | Priority |
| Family Vacation & Beach Outfits | `[matching family vacation outfits]` | exact | `https://www.dresslikemommy.com/collections/matching-family-vacation-outfits` | 6.76 | `$0.150` | Priority |
| Family Vacation & Beach Outfits | `[family cruise outfits]` | exact | `https://www.dresslikemommy.com/collections/matching-family-vacation-outfits` | 3.80 | `$0.139` | Priority |
| Daddy & Me Shirts | `[daddy and me shirts]` | exact | `https://www.dresslikemommy.com/collections/daddy-and-me` | 2.97 | `$0.133` | Watch closely; page is source-clean but includes hidden Christmas-pattern swim attributes |

Upload/helper file:

- `us_search_exact_020_launch_keywords.csv`

## Holdout Rows

Do not launch:

- The `19` rows marked `hold_no_click_forecast_at_020`.
- The `2` rows marked `micro_test_only`, unless the owner explicitly approves a tiny probe later:
  - `[mother daughter bathing suits]`
  - `[family outfits for beach photos]`

Reason:

- This campaign is designed to learn from the forecastable exact rows first. Zero-click rows add management noise without improving short-term sales learning.

## Negative Keywords

Apply the account, campaign, and ad group negatives in:

- `us_search_exact_020_negative_keywords.csv`

Important negative policy:

- Keep brand terms negative in this nonbrand campaign so brand protection and nonbrand learning stay separate.
- Keep marketplace and DIY terms blocked.
- Keep support terms blocked.
- Add search-term negatives daily during the first three days if spend appears.

## RSA Assets

Use the RSA assets in:

- `us_search_exact_020_rsa_assets.csv`

RSA launch rules:

- One RSA per ad group at launch.
- Do not pin headlines unless Google policy/clarity requires it.
- Do not mention free shipping, returns, discounts, inventory, warehouse, local stock, or guaranteed delivery unless verified at action time.
- Do not imply a physical retail store.

## Landing Page Readback

Public landing checks performed on 2026-05-19:

| URL | Status | Result |
|---|---:|---|
| `https://www.dresslikemommy.com/collections/pajamas` | 200 | Pajama intent match; no supplier/source host hits in scan |
| `https://www.dresslikemommy.com/collections/family-swimsuits` | 200 | Swim intent match; no supplier/source host hits in scan |
| `https://www.dresslikemommy.com/collections/matching-family-vacation-outfits` | 200 | Vacation intent match; no supplier/source host hits in scan |
| `https://www.dresslikemommy.com/collections/daddy-and-me` | 200 | Daddy intent match and no supplier/source host hits; watch because hidden product attributes include `Christmas` on swim products |

Recommended landing decision:

- Launch Pajamas, Swim, and Vacation as priority.
- Launch Daddy & Me only as a watch-tier ad group, or hold it if the owner wants the cleanest possible first test.

## Measurement Rules

ROAS formula:

`ROAS = product_subtotal_conversion_value / ad_spend`

Target:

`650% ROAS = 6.5x`

Required conversion rate at `$0.20` CPC:

`required_CVR = (6.5 * 0.20) / subtotal_AOV = 1.30 / subtotal_AOV`

Examples:

- If subtotal AOV is `$50`, required CVR is `2.60%`.
- If subtotal AOV is `$75`, required CVR is `1.73%`.
- If subtotal AOV is `$100`, required CVR is `1.30%`.

Do not use these examples as actual AOV. Use real Shopify subtotal AOV when judging performance.

## Stop Rules

Campaign-level:

- Stop immediately if average CPC exceeds `$0.20`.
- Stop immediately if Google Ads uses Search Partners, Display, broad match, AI Max, auto-created assets that change query scope, or any non-purchase primary optimization.
- Stop immediately if purchase conversion value includes shipping or tax.
- Stop immediately if final URLs change away from the packet.

Keyword-level:

- Add a negative immediately when a search term is DIY, marketplace, support, wholesale, secondhand, toy/costume, brand-support, or unrelated.
- Promote no new keyword until a search term has at least one purchase or strong add-to-cart/checkout evidence from separate analytics.
- Pause a keyword after either:
  - `40` clicks with `0` purchases and no strong onsite signal, or
  - spend reaches `subtotal_AOV / 6.5` with `0` purchases.
- If a keyword has no impressions after `72` hours, keep it but do not raise CPC above `$0.20`; add a phrase-discovery lane only after owner approval.

Ad group watch rules:

- Daddy & Me is watch-tier because the current collection page is relevant but mixed. If it spends with poor engagement or irrelevant search terms, pause that ad group first.
- Swim and Pajamas are the primary learning groups.

## Search Term Mining Rules

Daily during first three serving days:

- Pull search terms.
- Add negatives for irrelevant terms immediately.
- If a term converts and CPC is at or below `$0.20`, add it as exact in the most relevant ad group after review.
- If a term is relevant but no purchase yet, leave it as data unless it exceeds the spend/click stop rule.

Weekly:

- Review by keyword, landing page, device, and search term.
- Do not switch to broad match, AI Max, or Maximize Conversion Value until conversion tracking is proven and there is enough purchase conversion volume to avoid unstable automation.

## Approval Phrases

Paused build approval, no spend:

`Approve creating the paused Google Ads Search campaign DLM_US_SEARCH_EXACT_020_TEST_20260519 exactly as specified in US_SEARCH_EXACT_020_LAUNCH_APPROVAL_PACKET.md, with no enabled spend.`

Enabled live test approval:

`Approve enabling the Google Ads Search campaign DLM_US_SEARCH_EXACT_020_TEST_20260519 exactly as specified in US_SEARCH_EXACT_020_LAUNCH_APPROVAL_PACKET.md: Google Search only, United States, English, exact match only, $5/day max budget, $0.20 max CPC, purchase-only conversion, no broad match, no AI Max, no PMax, no Search Partners, no Display, and no changes outside this packet.`

## Expert Verdict

Proceed only with this tight exact-match launch if the owner wants a live Search test now.

The expert default is:

1. Launch Pajamas, Swim, and Vacation exact keywords first.
2. Include Daddy & Me only as a watch-tier ad group, or hold it until the collection page is cleaner.
3. Keep budget at `$5/day` and max CPC at `$0.20`.
4. Treat the first week as controlled learning, not scale.
5. Do not use broad match, AI Max, or tROAS until purchase data proves the economics.
