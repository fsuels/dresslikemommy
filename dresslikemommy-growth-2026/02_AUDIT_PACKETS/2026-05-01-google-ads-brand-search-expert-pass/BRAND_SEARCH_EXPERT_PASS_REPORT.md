# Brand Search Expert Pass

Date: 2026-05-01

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`  
Campaign ID: `23805046526`

## Decision

`BRAND_SEARCH_EXPERT_PASS_NO_ADDITIONAL_LIVE_EDITS`

I did not apply additional live campaign edits in this pass. The external review mixed valid strategic ideas with items that are already complete, unsupported by evidence, or blocked by the current coordination guardrails.

## Current State Readback

- Brand Search is live / enabled at `$5.00/day`.
- Bid strategy remains `Maximize clicks`.
- Conversion goal remains `Account-default: Purchases`.
- Fresh ads readback shows two enabled serving RSAs:
  - `Brand - Phrase`: `Eligible / Pending`
  - `Brand - Exact`: `Eligible / Pending`
- The previously Poor Phrase RSA is not one of the enabled serving ads in the fresh readback.
- Fresh keyword readback shows core exact and phrase brand keywords eligible.
- The two low-search-volume exact keywords are already paused:
  - `[dress like mommy shop]`
  - `[dlm dresses]`
- Fresh asset readback shows campaign/account assets in scope, including sitelinks, callouts, one structured snippet, and a pending campaign business name. Image/business-logo/promotion/price asset gaps still exist.

## Conversion Readback

Read-only conversion gate packet: `conversion-readback/`

Result:

- Purchase conversion-value gate: `PASS_PURCHASE_CONVERSION_VALUE_TRACKING_VERIFIED__NO_CURRENT_AD_ATTRIBUTION`
- Exactly one primary account-level purchase action is present.
- Primary purchase action: `Google Shopping App Purchase`
- It has recent received request evidence and dynamic value evidence.
- `Purchases from google Adwords` has large historical all-conversion/value totals, but is secondary and not included in account goals.

Decision:

- Do not change conversion primaries inside this Brand Search optimization pass.
- A conversion source-of-truth change would be account-level measurement work and is explicitly blocked by the repo guardrails without separate fresh approval.

## External Review Item Decisions

| Review item | Decision | Reason |
|---|---|---|
| Fix Poor Brand-Phrase RSA | No new edit | The Poor RSA was already paused. Fresh readback shows enabled Phrase and Exact RSAs as `Eligible / Pending`, not Poor. |
| Rewrite RSAs with promo/review/social-proof claims | Not applied | Suggested claims like `WELCOME20`, `100K+ Moms`, `4.8 stars`, and weekly drops were not sufficiently proven for ad-policy-safe use in this pass. Pinning H2/H3 is also not automatically best practice because it can reduce RSA flexibility. |
| Fix conversion primaries | Deferred | Good strategic concern, but out of scope without separate explicit conversion-goal approval. Current gate shows one primary purchase action and recent request evidence. |
| Remove/soften negatives like `[free]`, `[amazon]`, `[reseller]` | Not applied | Prior audit found `0` evidence-supported prune candidates. Exact negatives like `[free]` do not block `dress like mommy free shipping`; removing protections before search-term data would add risk. |
| Add Observation audiences | Deferred | Strategically reasonable once existing eligible lists are verified. Do not upload Customer Match lists or change audience settings in this pass. |
| Add image/logo/promotion/price assets | Deferred | Image/logo gaps are real, but live association still needs a safe asset-upload workflow. Promotion/price assets require current promo/pricing proof. |
| Change customer acquisition to bid higher for new customers | Not applied | Brand Search is a defensive controlled test; no Customer Match readback supports this yet. Leave `Bid equally for new and existing customers`. |
| Pause low-search-volume keywords | Already done | Fresh keyword readback confirms both low-search-volume exact keywords are already paused. |
| Merge Exact/Phrase ad groups | Not applied | Current split is acceptable for brand-control reporting and copy separation; restructuring a live campaign without performance data would add audit noise. |
| Page feeds | Not applied | Optional, lower priority, and not needed for a controlled exact/phrase brand campaign. |
| IP exclusions | Deferred | Requires known owner/internal IPs. Do not guess or add broad exclusions. |
| Linked-account/account-level asset housekeeping | No new edit | Prior account-level asset cleanup exists; no additional live account-level changes were made here. |
| Switch to tROAS after 14 days | Future-only | Not applicable until conversion source-of-truth and 14-day performance data are stable. |

## Guardrails Confirmed

- Standard Shopping remains locked by another agent and was not touched.
- Merchant Center, feeds, Shopify Admin, GA4/GTM, Pinterest, PMax, Remarketing, budgets, bid strategy, and conversion goals were not changed.
- The Standard Shopping 48-hour deadline is 2026-05-02 19:09 EDT, so it has not passed as of this 2026-05-01 pass.

## Evidence

- Fresh live readbacks: `live-readback/`
- Conversion readback: `conversion-readback/`

## Next Best Action

Run a narrow follow-up only after choosing one of these lanes:

1. Conversion-goal source-of-truth audit/repair, with explicit approval to change account-level conversion primaries if evidence supports it.
2. Brand Search asset-enrichment pass, limited to associating policy-safe image/logo assets and adding only proof-backed promotion/price assets.
3. Brand Search monitoring after first impressions/clicks: search terms, CPC, Search Impression Share, Quality Score, ad review final state, and spend.
