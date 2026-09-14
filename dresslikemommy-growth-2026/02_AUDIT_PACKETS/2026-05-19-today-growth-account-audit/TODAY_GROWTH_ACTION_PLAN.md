# Today Growth Action Plan

Generated: `2026-05-20T03:45:00Z`
Mode: read-only Google Ads API audit plus campaign-specialist subagent review. No live write occurred from this packet.

## Executive Decision

The account does not need more guessing today. It needs three controlled actions:

1. Fix the only channel currently getting nonbrand Google traffic: US Standard Shopping.
2. Give Search a real auction-entry path without breaking the `$0.15` CPC ceiling.
3. Keep Pinterest capped and read-only until the current-active feed ingestion finishes.

## Current Live Google Ads Readback

Readback source: `google_ads_campaigns_today.csv`, `google_ads_campaigns_last_30_days.csv`, `google_ads_bid_strategy_current.csv`.

### Campaigns With Traffic

| Campaign | Today | Last 30 days | Current issue |
|---|---:|---:|---|
| `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | `1088` impressions / `24` clicks / `$4.45` cost / `$0.00` value | `6146` impressions / `134` clicks / `$26.19` cost / `$0.00` value | Traffic exists but PDP message quality is weak; clicked PDP title cleanup is the best today action. |
| `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | `0` impressions / `$0.00` cost | `33` impressions / `26` clicks / `$2.50` cost / `$0.00` value | Brand defense is cheap enough; do not scale. |

### Search Campaigns With Zero Impressions

| Campaign | Status | Bid strategy | Budget | Diagnosis |
|---|---|---|---:|---|
| `DLM_US_SEARCH_EXACT_020_TEST_20260519` | `ENABLED` / `LEARNING` | Maximize Clicks / `$0.15` ceiling | `$5/day` | Newly launched, exact-only, no auction entry yet. Hold until T+24; do not add broad. |
| `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506` | `ENABLED` / `LEARNING` | Maximize Clicks / `$0.15` ceiling | `$5/day` | Older US nonbrand shell still zero; do not add more spend until overlap is cleaned. |
| `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519` | `ENABLED` / `ELIGIBLE` | Manual CPC | `$5/day` | Exact-only tiny scope; phrase holdouts already forecast below `$0.15` and are the next controlled volume unlock. |
| `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `ENABLED` / `ELIGIBLE` | Manual CPC | `$2/day` | Current head terms are below first page; forecast found 6 GB rows that can enter below `$0.15`. |
| `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `ENABLED` / `ELIGIBLE` | Manual CPC | `$2/day` | Forecast retry found `0` nonzero CA rows at `$0.15`; do not expand today. |
| `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `ENABLED` / `ELIGIBLE` | Manual CPC | `$2/day` | Forecast retry found `0` nonzero AU rows at `$0.15`; do not expand today. |

## Recommended Today Actions

### Action 1 - Execute Clicked-PDP Title Cleanup

This is the highest-confidence sales improvement because Shopping is the only Google campaign currently delivering real nonbrand traffic.

Use the existing packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-title-conversion-approval/STANDARD_SHOPPING_CLICKED_TITLE_CONVERSION_APPROVAL_PACKET.md`
- It covers `12` clicked PDPs with literal ellipses in visible H1s, representing `64/65` clicked Shopping clicks and `$13.96/$14.17` spend in the prior evidence.

Do not change Shopping bids, product groups, feed, conversion goals, or budget before this cleanup.

### Action 2 - GB Search Auction-Entry Repair

The paced Google Ads API forecast found only GB pass rows at the `$0.15` cap:

| Market | Match | Keyword | Forecast clicks | Avg CPC |
|---|---|---|---:|---:|
| GB | exact | `mummy and me pyjamas` | `0.4842` | `$0.110027` |
| GB | phrase | `mummy and me pyjamas` | `0.4842` | `$0.110027` |
| GB | exact | `matching family holiday outfits` | `3.0702` | `$0.074135` |
| GB | phrase | `matching family holiday outfits` | `3.5447` | `$0.081748` |
| GB | exact | `family matching pyjamas` | `3.9858` | `$0.105314` |
| GB | phrase | `family matching pyjamas` | `3.9858` | `$0.105314` |

Recommended write, after exact approval:

- Add only these 6 GB keywords.
- Use new tightly themed GB ad groups, not the existing Mommy-only ad group.
- Keep campaign Google Search only, Search Partners off, Display off, AI Max off, no broad.
- Keep max CPC ceiling/bids at `$0.15`.
- Keep daily budget unchanged at `$2/day` unless the owner explicitly approves more.

### Action 3 - IT Search Controlled Volume Unlock

The IT exact campaign has `0` impressions so far, and the held phrase rows were already forecast below the `$0.15` cap. Recommended write, after exact approval:

- Add the 9 held IT phrase rows from `it_it_search_exact_015_holdout_keywords.csv`.
- Keep existing ad groups, RSAs, negatives, budget, geo, language, and Search-only settings.
- Switch IT from Manual CPC to Maximize Clicks only if the `$0.15` ceiling is set in the same validated operation.
- No broad match.

### Action 4 - Do Not Expand CA/AU Today

The fresh 72-row forecast retry produced `0` nonzero CA rows and `0` nonzero AU rows at `$0.15`.

Do not spend build time or account writes there today. Keep them as read-only / next candidate factory lanes.

### Action 5 - Pinterest Hold

Pinterest is serving, but current-active feed ingestion was still processing in the last repo-known readback. Do not change Pinterest bid, budget, product groups, keywords, ads, or audiences until source `3041760873378113572` completes and exact product groups read back clean.

## Exact Approval Needed

### Google Ads Growth Unlock Approval

`I approve the Google Ads Today Growth Unlock exactly as specified in TODAY_GROWTH_ACTION_PLAN.md: add only the six GB forecast-passing exact/phrase keywords at max $0.15 CPC in tightly themed GB ad groups, add only the nine IT phrase holdout keywords from it_it_search_exact_015_holdout_keywords.csv, optionally switch IT to Maximize Clicks only with a $0.15 CPC ceiling in the same validated operation, keep Google Search only, no Search Partners, no Display, no AI Max, no broad match, no budget increases, no conversion-goal changes, no Shopping changes, no Merchant changes, no Shopify changes, no Pinterest changes, and capture validate-only plus before/after readbacks.`

### Shopify Clicked-PDP Cleanup Approval

Use the exact phrase in:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-title-conversion-approval/STANDARD_SHOPPING_CLICKED_TITLE_CONVERSION_APPROVAL_PACKET.md`

## Evidence Files

- `google_ads_campaigns_today.csv`
- `google_ads_campaigns_last_7_days.csv`
- `google_ads_campaigns_last_30_days.csv`
- `google_ads_ad_groups_last_30_days.csv`
- `google_ads_keywords_last_30_days.csv`
- `google_ads_search_terms_last_30_days_top200.csv`
- `google_ads_bid_strategy_current.csv`
- `gb_ca_au_36_api_forecast_rows_retry_015.csv`
- `gb_ca_au_36_api_forecast_summary_retry_015.json`
