# Brand Search Paused Cleanup And Activation Gate

Date: 2026-04-30

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`

Campaign ID: `23805046526`

## Decision

`BRAND_SEARCH_ACTIVATION_GATE_PASSED_AWAITING_EXPLICIT_OWNER_ENABLE_APPROVAL_AT_1_USD_PER_DAY`

No enable action was taken.

Exact approval phrase required before enabling:

`APPROVE ENABLE BRAND SEARCH AT $1.00/DAY NOW`

## Owner-Approved Paused Cleanup Applied

1. Bidding was changed from `Maximize conversion value` to `Maximize clicks`.
2. A maximum CPC bid limit was enabled and set to `0.20`.
3. Location option was changed from `Presence or interest` to `Presence: People in or regularly in your included locations`.

The campaign remained paused and stayed at `$1.00/day`.

## Activation Gate Readback

| Gate | Readback | Status |
|---|---:|---|
| Campaign status | `Paused` | Pass |
| Budget | `$1.00/day` | Pass |
| Campaign type | Search | Pass |
| Network | Google Search Network only | Pass |
| Conversion goal | Account-default: Purchases | Pass |
| Bid strategy | Maximize clicks | Pass |
| CPC guardrail | Max CPC cap `0.20` | Pass |
| Location | United States | Pass |
| Location option | Presence only | Pass |
| Language | English | Pass |
| AI Max | Not enabled | Pass |
| Text customization / Final URL expansion | Off | Pass |
| Automatically created assets | Off | Pass |
| Broad match keywords | Off | Pass |
| Cost / clicks / impressions | `$0.00`, `0`, `0` | Pass |

## Ads, Keywords, And Negatives

- Ads: two responsive search ads are present, one in `Brand - Exact` and one in `Brand - Phrase`; both are paused because the campaign is paused. No policy block was observed in the ads readback.
- Keywords: the prior live audit captured the brand exact and phrase keyword structure. No keyword expansion or match-type broadening was performed in this cleanup pass.
- Negatives: change history shows `190` negative phrase and `63` negative exact keywords from the original Google Ads Editor build. I did not bulk delete negatives because that can remove intentional protections and because the campaign has no search-term data yet.

## Recommendations Not Applied In This Pass

- Brand list enforcement: held because the setting currently shows `Limiting to: 0 brand lists`; adding the wrong brand list can prevent all brand serving. This can be handled after a verified Dress Like Mommy brand list exists.
- Extra RSAs and campaign-level assets: held because they require copy/claim review. Existing ads are sufficient for a low-dollar controlled activation gate, but assets should be expanded before any meaningful scale.
- Campaign URL suffix: held because purchase measurement already passed through Google Ads and GA4. UTMs can still be added later for analytics hygiene.
- Negative keyword pruning: held until real search-term data exists or a full negative export is reviewed.

## Rollback / Stop Triggers If Enabled Later

Pause Brand Search immediately if any of these occur:

- Any non-brand search-term theme appears.
- Any non-US traffic appears.
- Ads become disapproved or limited by policy.
- Cost exceeds `$3` before confirming qualified brand traffic.
- Purchase value, currency, or transaction ID tracking regresses.
- Average CPC materially exceeds the intended low-CPC brand-protection posture.
- The owner asks to stop.

## PMax And Remarketing Status

PMax and Remarketing were not edited or enabled. They remain blocked until their structural repair work is completed and separately activation-gated.

## Evidence

- Structured readback: `raw/brand_cleanup_structured_readback.json`
- Bidding guardrail: `raw/brand_bidding_cpc_cap_inputs.json`
- Location option: `raw/brand_location_presence_radios.json`
- Settings text: `raw/brand_settings_after_cleanup_summary.txt`
- Ads readback: `raw/brand_ads_after_cleanup_readback.txt`
- Keywords readback: `raw/brand_keywords_after_cleanup_readback.txt`
- Change history: `change-history/brand_change_history_after_brand_cleanup.txt`
- Screenshots: `screenshots/`
