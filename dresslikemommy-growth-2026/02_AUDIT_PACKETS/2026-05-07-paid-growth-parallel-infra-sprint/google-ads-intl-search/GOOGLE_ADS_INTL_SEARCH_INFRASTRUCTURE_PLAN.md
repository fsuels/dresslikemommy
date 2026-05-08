# Google Ads International Search Infrastructure Packet

Date: 2026-05-07

Scope: local-only planning and build artifacts for segmented paused country Search tests. No Google Ads UI/API, campaign creation, budget, bid, status, keyword, conversion-goal, Standard Shopping, PMax, Remarketing, Merchant, or Shopify writes were made.

## Template Read

- Existing paused US nonbrand rebuild: `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506` / campaign `23827590655`.
- Template controls preserved: Search only, paused only, Manual CPC, exact/phrase keywords, shared campaign negatives, claim-safe RSAs.
- This packet does not create or duplicate a US campaign; it clones the structure locally for non-US country shells.

## Country Tier Plan

- US: existing paused campaign remains the governed template; no duplicate build.
- Priority English import candidates after owner approval and action-time readbacks: GB, CA, AU.
- High-value watchlist paused shells: CH and DK, English-only until local route/shipping QA passes.
- Broader ecommerce paused English shells: DE, NL, SE, FR, BE, ES, IT.
- Lower-CPC discovery paused English shells: PL, CZ, RO, GR, PT.
- Local-language keyword/RSA variants are intentionally held until the localization/shipping QA lane clears each route.

## Build Summary

- Proposed non-US campaigns: `17`.
- Ad groups per campaign: `12`.
- Keywords per campaign: `36`.
- Campaign negatives per campaign: `37`.
- RSAs per campaign: `12`.
- Total web-bulk rows: `1666`.
- Status everywhere: `Paused`.
- Bid strategy: `Manual CPC`.
- CPC caps: `$0.10` to `$0.15`; none above `$0.20`.
- Networks: Google Search only.
- Initial languages: `en` only.

## Import Readiness

These are local draft artifacts. Importing even paused campaigns is a live Google Ads write and needs the exact owner approval gate below. After any approved import, read back campaign status, location option/presence, networks, budget, bid caps, keywords, negatives, RSAs, policy/ad review, and conversion-goal inheritance before any enablement discussion.

Exact approval gate required before live paused campaign creation:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

## Files

- `country_tier_plan.csv`
- `campaign_structure.csv`
- `keyword_plan.csv`
- `negative_keyword_plan.csv`
- `rsa_copy_pack.csv`
- `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`
- `manual_qa/intl_search_pre_import_qa.csv`
- `manual_qa/approval_gate.md`
- `manifest.json`

## Residual Risks

- English-only targeting outside English-first markets is conservative but may have limited reach and conversion quality.
- Local-language campaigns need separate localized keyword and RSA packs after route, shipping, returns/duties, checkout, and catalog eligibility QA.
- Google Ads bulk import field support can drift; first live step must be preview-only with zero-error readback before apply.
- Presence-only location option may require UI/API confirmation after import because the template CSV does not encode it reliably.
- Paused budgets are draft shell settings only; enablement requires a separate country-level economics decision.
