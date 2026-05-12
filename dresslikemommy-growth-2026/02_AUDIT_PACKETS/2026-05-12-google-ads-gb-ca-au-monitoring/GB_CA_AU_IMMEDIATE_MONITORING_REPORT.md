# GB/CA/AU Immediate Google Ads Monitoring Report

Date: 2026-05-12

## Scope

Read-only monitor pass for the first English-first live Search cohort:

- `GB` campaign `23838895360`
- `CA` campaign `23834423669`
- `AU` campaign `23834424182`

No Google Ads, Merchant, Pinterest, Shopify, feed, product-scope, conversion-goal, budget, bid, or status writes were made in this monitoring pass.

## Authoritative Status Readback

RPC status/safety checks passed:

| Market | Campaign | Campaign Status | Enabled Ad Group | Budget | Network | Geo | Conversion Override |
|---|---:|---|---|---:|---|---|---|
| `GB` | `23838895360` | `Enabled` | `194138528537` / `Mommy & Me Dresses - Exact` | `$2/day` | Search only; content/YouTube off | Presence-only | None |
| `CA` | `23834423669` | `Enabled` | `196679079575` / `Mommy & Me Dresses - Exact` | `$2/day` | Search only; content/YouTube off | Presence-only | None |
| `AU` | `23834424182` | `Enabled` | `198852670520` / `Mommy & Me Dresses - Exact` | `$2/day` | Search only; content/YouTube off | Presence-only | None |

Each campaign has exactly one enabled ad group and nine paused ad groups.

## Serving Blocker Found

The visible Google Ads campaign page for each campaign showed:

- Campaign status: `Enabled`
- Serving/status: `Not eligible`
- Explanation: `All keywords are paused, All ads are paused`
- Reporting range visible at capture time: `Last 7 days`, `May 5 - 11, 2026`
- Visible current-row metrics: `$0.00` cost, `0.00` conversion/value style metrics, and no meaningful fresh serving data yet

This means the campaign and exact ad group shells are enabled, but traffic is still not serving because the inner keywords and responsive search ad in each exact ad group remain paused. That state matches the prior exact approvals, which named campaign and ad group status only.

## Exact Inner Scope From Split Files

Each enabled exact ad group has:

- `3` paused exact-match keywords:
  - `mommy and me dresses`
  - `mother daughter dresses`
  - `mom and daughter matching outfits`
- `1` paused responsive search ad
- Country-qualified final URLs for that market

## Read-Only Inner Entity Discovery

A follow-up read-only RPC discovery found the exact paused keyword/ad entities that would need the next owner approval. No mutate RPCs were sent.

| Market | Ad Group ID | Paused Keyword Criterion IDs | Paused RSA Ad ID | URL Check |
|---|---:|---|---:|---|
| `GB` | `194138528537` | `299141671628`, `301154335636`, `301154336396` | `808406712704` | `?country=GB` |
| `CA` | `196679079575` | `299141671628`, `301154335636`, `301154336396` | `808294804728` | `?country=CA` |
| `AU` | `198852670520` | `299141671628`, `301154335636`, `301154336396` | `808328767090` | `?country=AU` |

Discovery checks passed for each market: exactly `3` paused keyword criteria, exactly `1` paused ad, and all final URLs country-qualified.

## Evidence

- Monitor script: `monitor_gb_ca_au_readonly_cdp.py`
- Inner discovery script: `discover_gb_ca_au_inner_entities_readonly_cdp.py`
- Summary: `raw/monitoring_summary.json`
- Inner discovery summary: `raw/inner-entity-discovery/inner_entity_discovery_summary.json`
- RPC readbacks: `raw/rpc/GB/`, `raw/rpc/CA/`, `raw/rpc/AU/`
- UI captures: `raw/ui/GB/`, `raw/ui/CA/`, `raw/ui/AU/`
- Safety checks: `raw/checks/GB/monitor_checks.json`, `raw/checks/CA/monitor_checks.json`, `raw/checks/AU/monitor_checks.json`

## Next Unblock Action

To make the three exact Search tests actually eligible to serve, get fresh exact action-time approval to enable only:

- In `GB` campaign `23838895360`, ad group `Mommy & Me Dresses - Exact`: the 3 listed exact-match keywords and 1 responsive search ad.
- In `CA` campaign `23834423669`, ad group `Mommy & Me Dresses - Exact`: the 3 listed exact-match keywords and 1 responsive search ad.
- In `AU` campaign `23834424182`, ad group `Mommy & Me Dresses - Exact`: the 3 listed exact-match keywords and 1 responsive search ad.

Do not change budgets, bids, product scope, feed, Merchant, Pinterest, conversion goals, other campaigns, other ad groups, phrase keywords, broad keywords, ads outside the named exact ad groups, PMax, Standard Shopping, Shopify product data, or billing.

Suggested exact approval:

`APPROVE ENABLE GB CA AU EXACT SEARCH INNER ENTITIES ONLY: IN CAMPAIGN 23838895360 AD GROUP Mommy & Me Dresses - Exact, CAMPAIGN 23834423669 AD GROUP Mommy & Me Dresses - Exact, AND CAMPAIGN 23834424182 AD GROUP Mommy & Me Dresses - Exact, ENABLE ONLY THE 3 EXACT-MATCH KEYWORDS mommy and me dresses, mother daughter dresses, mom and daughter matching outfits AND THE 1 RESPONSIVE SEARCH AD IN EACH NAMED AD GROUP; KEEP ALL OTHER AD GROUPS, ADS, KEYWORDS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, CONVERSION GOALS, PMAX, STANDARD SHOPPING, SHOPIFY PRODUCT DATA, AND BILLING UNCHANGED.`
