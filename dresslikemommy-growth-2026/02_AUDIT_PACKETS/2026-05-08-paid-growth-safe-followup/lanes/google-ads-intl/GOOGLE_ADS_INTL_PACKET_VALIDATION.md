# Google Ads Intl Search Packet Validation

Date: 2026-05-08

Lane: Google Ads non-US international Search local packet validation

Source packet validated: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/`

Output folder: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/google-ads-intl/`

Status: PASS for local-only paused-build readiness, still gated for any Google Ads write.

No Google Ads UI/API, Merchant, Shopify, Pinterest, campaign import, campaign creation, campaign edit, budget, bid, status, product-scope, feed-label, product-group, or conversion-goal write was made.

## Validation Method

- Read `summary.json`, `manifest.json`, `manual_qa/approval_gate.md`, `campaign_structure.csv`, and the web-bulk upload file.
- Independently parsed `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv` with Python `csv.DictReader`.
- Checked row counts, row types, actions, status fields, campaign IDs, campaign names, countries, networks, bidding, CPC ceilings, keyword match types, final URLs, localized URL paths, and forbidden terms in the importable web-bulk file.
- Ran a broader supporting-file text scan for guardrail references so documentation-only mentions would not be mistaken for importable edits.

## Confirmed Counts

Importable web-bulk rows: `1,666`

Row type counts:

- Campaign: `17`
- Ad group: `204`
- Keyword: `612`
- Negative keyword: `629`
- Ad: `204`

Per-campaign structure is consistent across all 17 campaigns:

- Campaign rows: `1`
- Ad groups: `12`
- Positive keywords: `36`
- Campaign negatives: `37`
- Responsive search ads: `12`

Supporting source-file line counts match the packet manifest shape:

- `campaign_structure.csv`: 17 data rows
- `keyword_plan.csv`: 612 data rows
- `negative_keyword_plan.csv`: 629 data rows
- `rsa_copy_pack.csv`: 204 data rows
- `final_url_mapping.csv`: 102 data rows, equal to 17 countries x 6 product themes
- `manual_qa/intl_search_pre_import_qa.csv`: 9 QA rows

## Pause and Add-Only Controls

All web-bulk rows are `Action=Add`.

Paused status checks:

- Campaign rows: `17 / 17` paused
- Ad group rows: `204 / 204` paused
- Keyword rows: `612 / 612` paused
- Ad rows: `204 / 204` paused

Negative keyword rows are campaign-level add rows and do not carry a serving status field.

## Country and US Duplication Checks

Validated non-US countries:

`AU`, `BE`, `CA`, `CH`, `CZ`, `DE`, `DK`, `ES`, `FR`, `GB`, `GR`, `IT`, `NL`, `PL`, `PT`, `RO`, `SE`

Findings:

- `US` country code appears in zero importable campaign names.
- Importable `Campaign ID`, `Ad group ID`, `Keyword ID`, and `Ad ID` fields are all blank, so the file is create-only and does not target existing entities.
- The existing US nonbrand campaign ID `23827590655` appears zero times in the importable web-bulk CSV.
- The existing US campaign name `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506` appears zero times in the importable web-bulk CSV.
- Supporting files mention `23827590655` only as a guardrail telling the next operator not to duplicate or edit it.

## Bidding, Network, and Match-Type Checks

Campaign rows:

- Campaign type: `Search`
- Networks: `Google search`
- Bid strategy type: `Manual CPC`
- Languages: `en`
- Target CPA: blank
- Target ROAS: blank
- Campaign subtype: blank
- Inventory type: blank

CPC checks:

- Minimum default max CPC observed: `$0.10`
- Maximum default max CPC observed: `$0.15`
- Result: PASS, max CPC is under the `$0.20` approval ceiling and matches the expected `$0.15` maximum.

Positive keyword match types:

- Exact match: `306`
- Phrase match: `306`
- Broad match positives: `0`

Campaign negative match types:

- Broad match negatives: `374`
- Exact match negatives: `170`
- Phrase match negatives: `85`

## URL and Localization Checks

Final URL rows checked: `816`, made of `612` keyword URLs plus `204` ad URLs.

Results:

- Missing `country=` parameter: `0`
- Mismatched `country=` parameter: `0`
- Bare language-only product paths for `/es`, `/it`, `/ro`, or `/pt`: `0`
- Localized path failures for ES/IT/RO/PT: `0`

Samples:

- GB: `https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=GB`
- ES: `https://www.dresslikemommy.com/es/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=ES`
- IT: `https://www.dresslikemommy.com/it/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=IT`
- RO: `https://www.dresslikemommy.com/ro/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=RO`
- PT: `https://www.dresslikemommy.com/pt/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=PT`

## Forbidden-Row Scan

Importable web-bulk CSV scan result: PASS.

Zero importable hits for:

- PMax / Performance Max
- Standard Shopping / Shopping campaign
- Product scope, custom labels, listing groups, product partitions, product groups
- Feed labels
- Conversion-goal edits or account-default conversion-goal text
- Existing US campaign ID `23827590655`
- Existing US campaign name `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506`

Supporting-file nuance:

- `campaign_structure.csv` contains the non-import guidance text `No edits; inherit account-default Purchases after readback`.
- `manual_qa/intl_search_pre_import_qa.csv` contains guardrail rows mentioning PMax and conversion-goal edits as prohibited.
- These are not importable web-bulk edit rows.

## Required Approval Wording

Do not import, preview-create, create, enable, upload, or edit anything in Google Ads from this packet until the owner gives this exact action-time approval:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

## Preview and Readback Checklist

Before any paused import or import preview:

- Confirm action-time owner approval exactly matches the wording above.
- Confirm existing US nonbrand campaign `23827590655` still exists and remains paused.
- Confirm the import file contains no `US` campaign rows and no nonblank existing entity IDs.
- Confirm Standard Shopping, PMax, Remarketing, product scope, feed labels, product groups, and conversion goals are not selected or edited in the workflow.
- Run Google Ads bulk import preview only; proceed no further if preview returns errors or unexpected edits.

Immediately after any future owner-approved paused build:

- Read back all 17 new campaigns as paused.
- Read back ad groups, keywords, and RSAs as paused.
- Confirm one country per campaign and presence-only location targeting.
- Confirm Google Search only, no Display/Search Partners, no PMax, no AI Max.
- Confirm Manual CPC and all default max CPC values are at or below `$0.20`.
- Confirm exact/phrase positive keywords only and campaign negatives present.
- Confirm the existing US campaign `23827590655` was not edited or duplicated.
- Confirm no Standard Shopping, product-scope, feed-label, product-group, or conversion-goal changes occurred.
- Confirm landing, shipping, checkout, Merchant/catalog, policy/ad review, tracking, and economics gates pass before any separate enable approval.

## Residual Risks

- This validation is local-file and CSV-based only; it did not perform a Google Ads account preview or account readback.
- Presence-only location targeting must be read back in Google Ads after an approved paused build because the web-bulk file carries country locations, while the UI/account setting must still be verified.
- Policy/ad-review, landing-page quality, Merchant/catalog health, tracking, and country-level ROAS math remain live-spend gates.
