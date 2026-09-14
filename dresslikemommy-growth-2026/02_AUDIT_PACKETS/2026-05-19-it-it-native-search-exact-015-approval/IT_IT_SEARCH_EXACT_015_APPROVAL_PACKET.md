# IT_IT Native Search Exact $0.15 Approval Packet

Date: 2026-05-19

## Recommendation

Prepare a tiny Italy / Italian native Google Search exact-match test. This packet is exact-only and uses Manual CPC at a hard `$0.15` max CPC. It does not reuse or modify the existing Italy English campaign shell.

This is a controlled native-language auction-entry test, not a scale build.

## Source Data

Primary source:

- `../2026-05-19-multimarket-search-forecast-organization/it_it_launch_candidates.csv`
- `../2026-05-19-multimarket-search-forecast-organization/low_top_015_priority_joined_decision_rows.csv`
- `../2026-05-19-multimarket-search-forecast-organization/winning_market_localized_landing_readback_corrected.csv`

API filters used in source forecast:

- Client account: `399-097-6848`
- Geo: Italy, geo target `2380`
- Language: Italian, language `1004`
- Network: Google Search
- Forecast bid: `max_cpc_bid_micros=150000` (`$0.15`)
- Candidate match types in source: exact and phrase
- Launch match type in this packet: exact only

Decision summary:

- `9` exact keywords are included for launch.
- `9` phrase rows are explicit holdouts.
- `0` broad keywords are included.
- Existing Italy Search campaign readback is English-language (`languageConstants/1000`), so this native Italian packet is separate scope.

## Live Write Boundary

This packet is local and review-only until the owner gives fresh action-time approval.

Do not:

- Upload/apply the campaign.
- Enable spend.
- Add keywords, ads, negatives, bids, budgets, statuses, or campaign settings in Google Ads.
- Change conversion goals, Merchant feeds, Shopify products, Pinterest, billing, or credentials.
- Enable broad match, phrase match, AI Max, Performance Max, Dynamic Search Ads, Search Partners, Display expansion, or automated bidding.

## Campaign Settings

Campaign name:

`DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`

Recommended launch state:

- If building for review only: create as `PAUSED`.
- If owner explicitly approves live test: create as `ENABLED`.

Core settings:

- Campaign type: Search only
- Network: Google Search only
- Search Partners: off
- Display Network: off
- Location: Italy
- Location option: presence only, not presence-or-interest
- Language: Italian
- Budget: `$5.00/day` maximum
- Bidding: Manual CPC
- Max CPC: `$0.15`
- Enhanced CPC: off at launch
- Conversion goal: purchase only
- Conversion value rule: product revenue/subtotal only, excluding shipping and tax
- Final URL expansion / automatically created assets / AI Max: off
- EU political ads setting: does not contain EU political advertising

## Launch Keywords

Use only these exact-match rows at launch:

| Ad group | Keyword | Match | Final URL | Forecast clicks | Forecast avg CPC | Historical low top bid |
|---|---|---:|---|---:|---:|---:|
| Family Matching | `[abiti coordinati famiglia]` | exact | `https://www.dresslikemommy.com/it/collections/matching-outfits?country=IT` | 0.631 | `$0.059` | `$0.113` |
| Pajamas | `[pigiami coordinati]` | exact | `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 0.441 | `$0.030` | `$0.070` |
| Pajamas | `[pigiami famiglia]` | exact | `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 3.093 | `$0.041` | `$0.135` |
| Pajamas | `[pigiami famiglia coordinati]` | exact | `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 1.934 | `$0.089` | `$0.040` |
| Pajamas | `[pigiami mamma e figlia]` | exact | `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 8.658 | `$0.078` | `$0.095` |
| Pajamas | `[pigiami mamma figlia]` | exact | `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 0.841 | `$0.150` | `$0.128` |
| Swimwear | `[costumi famiglia]` | exact | `https://www.dresslikemommy.com/it/collections/family-swimsuits?country=IT` | 1.841 | `$0.034` | `$0.149` |
| Mommy & Me Dresses | `[abiti mamma e figlia]` | exact | `https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT` | 0.739 | `$0.080` | `$0.093` |
| Mommy & Me Dresses | `[abiti mamma figlia]` | exact | `https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT` | 1.890 | `$0.085` | `$0.086` |

Upload/helper file:

- `it_it_search_exact_015_launch_keywords.csv`

## Holdout Rows

Do not launch phrase or broad rows in this packet.

Phrase holdout file:

- `it_it_search_exact_015_holdout_keywords.csv`

Reason:

- The exact rows are sufficient for first auction-entry learning.
- Phrase rows could cannibalize exact rows and expand query waste before Italian search-term quality is proven.

## Negative Keywords

Apply only the campaign and ad-group negatives in:

- `it_it_search_exact_015_negative_keywords.csv`

Negative policy:

- Keep brand terms negative in this nonbrand native campaign.
- Block Italian and English DIY, pattern, secondhand, marketplace, wholesale, support, toy/costume, and irrelevant terms.
- Use ad-group cross-negatives to keep pajamas, swimwear, dresses, and family matching separated.

## RSA Assets

Use the RSA assets in:

- `it_it_search_exact_015_rsa_assets.csv`

RSA launch rules:

- One RSA per ad group at launch.
- Italian ad copy only.
- Do not mention free shipping, returns, discounts, inventory, warehouse, local stock, or guaranteed delivery unless verified at action time.
- Do not imply a physical retail store.

## Landing Page Readback

Public localized landing checks from the corrected multimarket packet:

| URL | Status | Supplier/source hits | Collection-grid signal | Title |
|---|---:|---:|---|---|
| `https://www.dresslikemommy.com/it/collections/matching-outfits?country=IT` | 200 | 0 | True | Abiti coordinati per la famiglia / Mamma e Me |
| `https://www.dresslikemommy.com/it/collections/pajamas?country=IT` | 200 | 0 | True | Pigiami Mamma e Me - Pigiami Coordinati per Famiglia / Vestiti Come Mamma – Dress Like Mommy |
| `https://www.dresslikemommy.com/it/collections/family-swimsuits?country=IT` | 200 | 0 | True | Costumi da bagno coordinati per la famiglia / Costumi da bagno per famiglie |
| `https://www.dresslikemommy.com/it/collections/mommy-and-me?country=IT` | 200 | 0 | True | Mamma e Me Abiti / Abiti, Costumi da bagno e Set abbinati |

Landing decision:

- IT localized collection URLs are acceptable for this packet.
- They must be re-read before any live write if more than 24 hours have passed or product/archive state changes.

## Measurement Rules

ROAS formula:

`ROAS = product_subtotal_conversion_value / ad_spend`

Target:

`650% ROAS = 6.5x`

Required conversion rate at `$0.15` CPC:

`required_CVR = (6.5 * 0.15) / subtotal_AOV = 0.975 / subtotal_AOV`

Examples:

- If subtotal AOV is `$50`, required CVR is `1.95%`.
- If subtotal AOV is `$75`, required CVR is `1.30%`.
- If subtotal AOV is `$100`, required CVR is `0.98%`.

Do not use these examples as actual AOV. Use real Shopify subtotal AOV when judging performance.

## Validate-Only And Readback Requirements

Before any live write:

1. Run `execute_it_it_search_exact_015_live.py --validate-only` with the approved Google Ads API config.
2. Save before-state readback JSON from the script.
3. Confirm validate-only passed.
4. Confirm after-state readback still shows no live campaign unless `--execute` was intentionally approved.
5. Run reviewer checks against this packet.

For live execution after fresh approval only:

1. Re-run before-state readback and refuse if the campaign already exists.
2. Run validate-only first.
3. Execute only if validate-only passes.
4. Save after-state readback JSON.
5. Confirm campaign, budget, geo, language, networks, Manual CPC, max CPC, exact keywords, negatives, RSAs, AI Max off, Search Partners off, Display off, and purchase goal state.

## Validate-Only Result

Validate-only was run on 2026-05-19 with the packet executor.

Result:

- Mode: `validate_only`
- Validate-only passed: `True`
- Live mutate executed: `False`
- Operation count validated: `87`
- Before-state campaign count for `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`: `0`
- After-state campaign count for `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`: `0`
- Purchase conversion-action readback rows were captured before and after; no conversion-goal mutation occurred.

Evidence:

- `google_ads_api_it_it_execution_report_20260519T134851Z.md`
- `google_ads_api_it_it_before_readback_20260519T134851Z.json`
- `google_ads_api_it_it_after_readback_20260519T134851Z.json`

## Live Execution Result

The owner approved execution in the current session on 2026-05-19. The guarded executor reran before-state readback, validate-only, live mutate, and after-state readback.

Result:

- Mode: `execute`
- Validate-only passed: `True`
- Live mutate executed: `True`
- Operation count: `87`
- Campaign ID: `23866684201`
- Campaign status: `ENABLED`
- Campaign primary status: `ELIGIBLE`
- Campaign type: `SEARCH`
- Bidding: `MANUAL_CPC`
- Budget: `5,000,000` micros daily
- Google Search: `True`
- Search Partners/Search Network: `False`
- Display/content network: `False`
- Partner search network: `False`
- Location: `geoTargetConstants/2380`
- Language: `languageConstants/1004`
- Presence-only location targeting: `PRESENCE`
- Enhanced CPC: `False`
- AI Max: `False`
- Enabled ad groups: `4`
- Enabled exact positive keywords: `9`
- Campaign-scoped negatives: `47`
- Ad-group negatives: `19`
- Enabled RSAs: `4`

Evidence:

- `google_ads_api_it_it_execution_report_20260519T135836Z.md`
- `google_ads_api_it_it_before_readback_20260519T135836Z.json`
- `google_ads_api_it_it_after_readback_20260519T135836Z.json`

## Stop Rules

Campaign-level:

- Stop immediately if average CPC exceeds `$0.15`.
- Stop immediately if Google Ads uses Search Partners, Display, broad match, phrase match, AI Max, auto-created assets that change query scope, or any non-purchase primary optimization.
- Stop immediately if purchase conversion value includes shipping or tax.
- Stop immediately if final URLs change away from the packet.

Keyword-level:

- Add a negative immediately when a search term is DIY, marketplace, support, wholesale, secondhand, toy/costume, brand-support, or unrelated.
- Promote no new keyword until a search term has at least one purchase or strong add-to-cart/checkout evidence from separate analytics.
- Pause a keyword after either `40` clicks with `0` purchases and no strong onsite signal, or spend reaches `subtotal_AOV / 6.5` with `0` purchases.
- If a keyword has no impressions after `72` hours, keep it but do not raise CPC above `$0.15`; prepare a separate phrase-discovery packet only after owner approval.

## Approval Phrases

Paused build approval, no spend:

`Approve creating the paused Google Ads Search campaign DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519 exactly as specified in IT_IT_SEARCH_EXACT_015_APPROVAL_PACKET.md, with no enabled spend.`

Enabled live test approval:

`Approve enabling the Google Ads Search campaign DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519 exactly as specified in IT_IT_SEARCH_EXACT_015_APPROVAL_PACKET.md: Google Search only, Italy, Italian, exact match only, $5/day max budget, $0.15 max CPC, purchase-only conversion, no broad match, no phrase match, no AI Max, no PMax, no Search Partners, no Display, and no changes outside this packet.`

## Expert Verdict

Proceed only as a tight exact-only native Italian microtest after validate-only passes. Do not use the existing Italy English campaign as the native-language container. Do not add phrase rows until exact Italian search terms prove relevance and CPC discipline.
