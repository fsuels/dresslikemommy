# Google Ads Import Gate

Subagent scope: Google Ads paused import gate only. I did not open Google Ads, import anything, create campaigns, enable/pause campaigns, change budget, bid, status, product scope, product group, feed label, PMax, Standard Shopping, or conversion goals. No live Ads writes were made.

## Prior Packet Verified

Prior local packet:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/`

Verified files:

- `manifest.json`
- `GOOGLE_ADS_INTL_SEARCH_INFRASTRUCTURE_PLAN.md`
- `SUBAGENT_HANDOFF.md`
- `campaign_structure.csv`
- `country_tier_plan.csv`
- `keyword_plan.csv`
- `negative_keyword_plan.csv`
- `rsa_copy_pack.csv`
- `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`
- `manual_qa/approval_gate.md`
- `manual_qa/intl_search_pre_import_qa.csv`

## Local Packet Readiness

The prior packet exists and is locally ready as a paused import draft, subject to approval and action-time readbacks.

Evidence from `manifest.json` and CSV validation:

- Existing US template campaign: `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506`
- Existing US template campaign ID: `23827590655`
- Proposed non-US campaigns: `17`
- Countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `GR`, `PT`
- Web bulk rows: `1666`
- Row mix: `17` campaigns, `204` ad groups, `612` keywords, `629` negative keywords, `204` ads
- Campaign status rows: all `Paused`
- Ad group status rows: all `Paused`
- Keyword status rows: all `Paused`
- Ad status rows: all `Paused`
- Network: `Google search`
- Bid strategy: `Manual CPC`
- Keyword match types: `306` exact, `306` phrase, `0` broad
- Max default CPC found: `$0.15`
- CPC values above `$0.20`: `0`
- Campaigns with non-paused status: `0`
- Ad groups with non-paused status: `0`
- Keywords with non-paused status: `0`
- Ads with non-paused status: `0`

## Approval Phrase Status

Status: `NOT APPROVED IN THIS SUBAGENT TASK`.

The user instructed this lane to verify the gate only and explicitly said not to import or make live Ads writes. The exact approval phrase required by the prior packet is:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

Without that exact action-time approval, even paused campaign creation/import remains blocked because it is a live Google Ads write.

## Required Readbacks Before Any Approved Import

Before applying any approved paused import, the parent/orchestrator should run just-in-time Google Ads readbacks confirming:

- Existing US nonbrand campaign `23827590655` still exists and remains paused.
- No duplicate US nonbrand campaign will be created.
- Standard Shopping is not touched.
- PMax and Remarketing are not touched.
- Conversion goals are not edited.
- Bulk upload preview returns zero errors before apply.
- Imported objects will remain paused-only.
- Country targeting is one country per campaign.
- Location option is presence-only.
- Network remains Google Search only, with no Display/Search Partners.
- Manual CPC and every default max CPC remain at or below `$0.20`.
- Keywords remain exact/phrase only.
- Campaign negatives are present.

## Next Safe Action

Do not import yet. The next safe action is for the parent/orchestrator to either:

1. Keep this lane parked until the owner gives the exact approval phrase above, or
2. If exact approval is given later, perform pre-import readbacks and a Google Ads bulk-upload preview only; apply the paused import only after the preview is clean and the approval still clearly covers the action.

No live spend, enablement, PMax, Standard Shopping, product-scope, feed-label, product-group, bid/budget/status, or conversion-goal action is authorized by this lane report.
