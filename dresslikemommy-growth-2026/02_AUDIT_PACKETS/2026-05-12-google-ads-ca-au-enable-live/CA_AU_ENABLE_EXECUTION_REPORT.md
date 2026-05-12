# CA/AU Google Ads Search Enable Execution Report

Date: 2026-05-12

## Approval

Owner approved:

`APPROVE ENABLE CA AND AU SEARCH CAMPAIGNS ONLY: ENABLE CAMPAIGN 23834423669 AD GROUP Mommy & Me Dresses - Exact AND CAMPAIGN 23834424182 AD GROUP Mommy & Me Dresses - Exact; KEEP EXISTING BUDGETS, BIDS, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, AND CONVERSION GOALS UNCHANGED; DO NOT ENABLE ANY OTHER CAMPAIGNS OR AD GROUPS.`

## Action Taken

Used Google Ads authenticated CDP RPC to enable only:

- `CA` campaign `23834423669` / `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
  - Enabled ad group `196679079575` / `Mommy & Me Dresses - Exact`
- `AU` campaign `23834424182` / `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
  - Enabled ad group `198852670520` / `Mommy & Me Dresses - Exact`

No other ad groups or campaigns were enabled.

## Pre-Enable Gates

Pre-enable readbacks and local split-file checks passed for both `CA` and `AU`:

- Campaign existed with the expected ID/name.
- Campaign status was `Paused`.
- Target ad group name was exactly `Mommy & Me Dresses - Exact`.
- All ad groups in each campaign were `Paused`.
- Budget was unchanged at `2000000` micros / `$2/day`.
- Google Search was on.
- Content network was off.
- YouTube was off.
- Positive and negative geo targeting were both presence-only: raw `{ "16": 18, "17": 18 }`.
- Campaign conversion-goal override was absent.
- Split CSV target-ad-group keywords were exact match and paused.
- Split CSV target-ad-group ads were paused.
- Split CSV final URLs were country-qualified for the correct market.

## Post-Enable Readback

Final post-enable readback passed:

| Market | Campaign ID | Campaign Status | Enabled Ad Group | Budget | Network | Geo |
|---|---:|---|---|---:|---|---|
| `CA` | `23834423669` | `Enabled` | `196679079575` / `Mommy & Me Dresses - Exact` | `$2/day` | Google Search only; content/YouTube off | Presence-only |
| `AU` | `23834424182` | `Enabled` | `198852670520` / `Mommy & Me Dresses - Exact` | `$2/day` | Google Search only; content/YouTube off | Presence-only |

For both markets, post-enable delta checks passed:

- `campaign_enabled`: `true`
- `target_adgroup_enabled`: `true`
- `other_adgroups_paused`: `true`
- `budget_unchanged`: `true`
- `network_unchanged`: `true`
- `geo_unchanged`: `true`
- `adgroup_set_unchanged`: `true`
- `no_campaign_conversion_override`: `true`

## Evidence

- Script: `enable_ca_au_exact_live_cdp.py`
- Approval: `raw/enable-action/approval_phrase.txt`
- CA pre-gates: `raw/pre-enable-readback/CA/pre_enable_gate_checks.json`
- AU pre-gates: `raw/pre-enable-readback/AU/pre_enable_gate_checks.json`
- CA mutation responses: `raw/enable-action/CA/`
- AU mutation responses: `raw/enable-action/AU/`
- CA post-delta: `raw/post-enable-readback/CA/post_enable_delta_checks.json`
- AU post-delta: `raw/post-enable-readback/AU/post_enable_delta_checks.json`
- Final summary: `raw/post-enable-readback/final_success_summary.json`

## Guardrails Preserved

No budget, bid, product scope, feed, Merchant, Pinterest, conversion-goal, PMax, Standard Shopping, Shopify product-data, payment/order, billing, credential, or destructive filesystem changes were made.

## Next Best Action

Monitor GB/CA/AU as the first English-first live Search cohort using the 650% ROAS guardrails. The next expansion candidates are not the rest of the built markets blindly; the smart sequence is:

1. Read back early spend/search-term/conversion signals on GB/CA/AU.
2. Restore authenticated Pinterest Ads Manager access to complete the already-approved paused US draft.
3. Prepare exact approval for the next English-first Search candidates only after deciding whether to add CH/DK or wait for first cohort data.
4. Keep ES/IT and other localized markets behind native-language and landing-page QA before live enablement.
