# First 14 Day Monitoring Rules

Date: 2026-05-10

Mode: local-only monitoring prep. No campaign was enabled.

## Economics

- Target ROAS: `650%` / `6.5x`
- Working AOV: `$70`
- Working gross margin: `50%`
- Target CPA at 6.5x ROAS: `$10.77`
- First GB max CPC: `$0.15`
- Breakeven CVR at `$0.15` CPC: `1.39%`

## Review Cadence

| Time from launch | Required readback | Allowed action |
|---|---|---|
| T+2h | Campaign/ad group status, location, spend sanity | Roll back only if wrong geo, wrong unit, or unexpected spend/settings change |
| T+24h | Impressions, clicks, cost, CPC, conversions, value, search terms, locations, devices, policy | Observe only unless policy/geo/guardrail failure |
| T+72h | Same as T+24h plus zero-purchase thresholds | If spend >= `$16` with 0 purchases, pause the ad group |
| T+7d | CVR, CPA, ROAS, search-term quality, product/page notes | Keep, pause, or extend learning window; no scale without approval |
| T+14d | Confirm repeatability if week 1 looked good | Propose next unit; do not auto-scale |

## Kill Rules

- `$8` spend and 0 purchases: warning; inspect terms/geo/device.
- `$16` spend and 0 purchases: hard pause the active ad group.
- `$24` spend and 0 purchases: kill that configuration; do not relaunch same structure.
- Any non-GB click on a GB-only test: pause immediately.
- Any budget/bid/conversion/product/feed/PMax/Shopping drift: pause the active ad group and investigate.

## Scale Rules

Do not scale from impressions, CTR, cheap CPC, saves, carts, checkout starts, or one weak purchase alone. Scaling requires purchase value proof, CPA near or below `$10.77`, no measurement anomalies, and fresh approval.
