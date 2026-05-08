# Ads International Search Approval Gate Validation

Date: 2026-05-08
Mode: local/read-only; no Google Ads account access or write

## Result

The local international Search packet remains mechanically valid as paused non-US infrastructure:

- `17` non-US Search campaigns: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `GR`, `PT`.
- `1,666` web-bulk rows:
  - `17` campaigns.
  - `204` ad groups.
  - `612` exact/phrase keywords.
  - `629` negatives.
  - `204` paused RSAs.
- All applicable importable status fields are `Paused`.
- All actions are `Add`.
- Max CPC values are `$0.10`, `$0.12`, or `$0.15`; `0` rows exceed `$0.20`.
- URL scan found `0` missing `country=` params, `0` wrong-host URLs, and `0` ES/IT/RO/PT bare language-only URL risks.
- Forbidden surface scan found `0` PMax, Standard Shopping, product-scope, product-group, feed-label, custom-label, or conversion-goal edit rows.
- Claim scan found no inventory, warehouse, local-stock, store-pickup, same-day/next-day, or guaranteed-delivery claims in importable rows.

## Fix Applied Locally

The previous approval gate was too broad because it included `US` and bundled Pinterest draft language into the Google Ads import gate. The gate was corrected in:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/manual_qa/approval_gate.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/build_intl_search_packet.py`.

Corrected approval wording:

`APPROVE PAUSED NON-US GOOGLE SEARCH BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT DUPLICATE OR EDIT EXISTING US NONBRAND CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES, NO PINTEREST CHANGES.`

## Residual Risk

This is not launch approval. Import/create of even paused Google Ads campaigns remains a live account write and requires exact owner approval plus just-in-time readbacks.

