# GB/CA/AU 17:21 Zero-Data Decision Update

Date: `2026-05-12`
Readback window:

- Status/safety monitor: `2026-05-12T17:20:41-04:00`
- Performance/search-term route probe: `2026-05-12T17:21:23-04:00`

## Scope

Read-only monitor for the already-approved live exact Search micro-cohort:

| Market | Campaign | Exact ad group |
|---|---|---|
| `GB` | `23838895360` | `194138528537` |
| `CA` | `23834423669` | `196679079575` |
| `AU` | `23834424182` | `198852670520` |

## Safety Readback

All three markets passed the safety checks:

- Campaign status: `Enabled`.
- Overview status: `Eligible`.
- Budget: `$2.00/day`.
- Search only.
- Presence-only location targeting.
- No campaign conversion-goal override.
- Exactly `1` enabled ad group: `Mommy & Me Dresses - Exact`.
- `9` other ad groups remain paused per market.

Evidence:

- `../2026-05-12-google-ads-gb-ca-au-monitoring/raw/monitoring_summary.json`
- `../2026-05-12-google-ads-gb-ca-au-monitoring/raw/rpc/`
- `../2026-05-12-google-ads-gb-ca-au-monitoring/raw/ui/`

## Performance Readback

The fresh campaign/ad group/keyword page captures still show no actionable performance data:

| Market | Clicks | Impressions | Cost | Conversions | Conversion value |
|---|---:|---:|---:|---:|---:|
| `GB` | `0` | `0` | `$0.00` | `0.00` | `0.00` |
| `CA` | `0` | `0` | `$0.00` | `0.00` | `0.00` |
| `AU` | `0` | `0` | `$0.00` | `0.00` | `0.00` |

Search-term route result:

- Direct `/aw/searchterms` still returns `404`.
- Direct `/aw/search-terms` still returns `404`.
- Working route remains `/aw/keywords/searchterms`.
- The working search-term page still has the stale unrelated filter `Keyword: "human hair wigs"`.
- No attributable GB/CA/AU search term was visible or actionable.

Evidence:

- `../2026-05-12-google-ads-gb-ca-au-monitoring/raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary.json`
- `../2026-05-12-google-ads-gb-ca-au-monitoring/raw/perf-search-term-probe/`

## Decision

No live optimization edit is justified yet.

Do not make any of these from the current evidence:

- Negative keyword edit.
- Keyword pause or expansion.
- Bid edit.
- Budget edit.
- Campaign/ad group/ad/keyword status edit.
- ROAS or CPA conclusion.
- Expansion to another enabled market based on performance.

Next action is a later timed read-only monitor after impressions/clicks/search terms populate, or a fresh owner-approved action if the owner wants to change the experiment before data appears.

## Guardrails

No Google Ads write occurred. No upload, preview, import, apply, enable, pause, budget, bid, negative keyword, product/feed, Merchant, Pinterest, Shopify, conversion-goal, payment/order/refund/cancel, credential/account/billing, or destructive action occurred.
