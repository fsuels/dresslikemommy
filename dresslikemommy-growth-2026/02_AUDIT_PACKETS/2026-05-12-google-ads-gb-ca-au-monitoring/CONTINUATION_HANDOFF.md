# Continuation Handoff - GB/CA/AU Monitoring

Date: 2026-05-12

Latest anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-google-ads-gb-ca-au-monitoring`

Use the canonical owner-standard prompt at `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

## Current Truth

GB, CA, and AU Search campaign/ad-group shells were enabled under exact owner approvals:

- GB campaign `23838895360`, ad group `Mommy & Me Dresses - Exact`
- CA campaign `23834423669`, ad group `Mommy & Me Dresses - Exact`
- AU campaign `23834424182`, ad group `Mommy & Me Dresses - Exact`

Immediate monitoring found they are not actually serving. Google Ads UI shows:

- `Not eligible`
- `All keywords are paused, All ads are paused`

Each enabled exact ad group has:

- `3` paused exact-match keywords:
  - `mommy and me dresses`
  - `mother daughter dresses`
  - `mom and daughter matching outfits`
- `1` paused responsive search ad

Read-only inner entity discovery is complete:

| Market | Ad Group ID | Paused Keyword Criterion IDs | Paused RSA Ad ID |
|---|---:|---|---:|
| GB | `194138528537` | `299141671628`, `301154335636`, `301154336396` | `808406712704` |
| CA | `196679079575` | `299141671628`, `301154335636`, `301154336396` | `808294804728` |
| AU | `198852670520` | `299141671628`, `301154335636`, `301154336396` | `808328767090` |

Evidence: `raw/inner-entity-discovery/inner_entity_discovery_summary.json`.

## Next Exact Approval Needed

`APPROVE ENABLE GB CA AU EXACT SEARCH INNER ENTITIES ONLY: IN CAMPAIGN 23838895360 AD GROUP Mommy & Me Dresses - Exact, CAMPAIGN 23834423669 AD GROUP Mommy & Me Dresses - Exact, AND CAMPAIGN 23834424182 AD GROUP Mommy & Me Dresses - Exact, ENABLE ONLY THE 3 EXACT-MATCH KEYWORDS mommy and me dresses, mother daughter dresses, mom and daughter matching outfits AND THE 1 RESPONSIVE SEARCH AD IN EACH NAMED AD GROUP; KEEP ALL OTHER AD GROUPS, ADS, KEYWORDS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, CONVERSION GOALS, PMAX, STANDARD SHOPPING, SHOPIFY PRODUCT DATA, AND BILLING UNCHANGED.`

## Next Operator Steps After Approval

1. Pre-readback status, final URLs, campaign/ad-group status, budget, network, geo, and conversion-goal override.
2. Enable only the named inner exact keywords and RSA entities.
3. Post-readback that only those inner entities changed and that each campaign moves away from `Not eligible` or has a clear platform review/status reason.
4. Update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, `ops/AGENT_WORKLOG.md`, `AGENTS.md`, the canonical prompt, and this packet.

## Other Active Paths

- Pinterest paused US draft build remains exact-approved but blocked by authenticated Pinterest Ads Manager access in a controllable browser/session.
- RO paused Search build remains exact-approved but blocked by Google Ads file-picker/native upload path; do not re-upload completed countries.
- ES/IT native-language Search remain candidates only after native review, landing QA, exact upload/use approval, and readbacks.
