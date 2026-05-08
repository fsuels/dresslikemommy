# Ads Intl Country URL Packet Refresh

Generated: 2026-05-08

Lane: `ADS-INTL`

Scope: local-only refresh of the existing international Search packet from `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/`.

## Guardrail Result

PASS. No Google Ads UI/API, Merchant Center, Shopify Admin, Pinterest, feed, product data, product scope, product group, feed-label, conversion-goal, budget, bid, status, import, enable, pause, or live-spend action was taken.

All changes are local files inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/`

## What Changed

- Copied the prior local-only international Search packet into this lane.
- Refreshed final URLs in the copied `keyword_plan.csv`, `rsa_copy_pack.csv`, and `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`.
- Replaced collection final URLs with country-qualified product URLs.
- Used the 2026-05-08 proven localized country pattern for ES/IT/RO/PT:
  - `https://www.dresslikemommy.com/es/products/<handle>?country=ES`
  - `https://www.dresslikemommy.com/it/products/<handle>?country=IT`
  - `https://www.dresslikemommy.com/ro/products/<handle>?country=RO`
  - `https://www.dresslikemommy.com/pt/products/<handle>?country=PT`
- Kept English-only, not-yet-localized markets on base product routes with `country=<ISO_COUNTRY>`, for example:
  - `https://www.dresslikemommy.com/products/<handle>?country=GB`
- Added `final_url_mapping.csv` so the product handle and final URL template for every country/theme pair are reviewable before any future preview-only import.

## URL Change Counts

- Keyword final URLs changed: `612`
- RSA final URLs changed: `204`
- Web bulk final URLs changed: `816`
- Final URL mapping rows: `102`

## Validation Counts

- Campaigns: `17`
- Ad groups: `204`
- Positive keywords: `612`
- Campaign negatives: `629`
- RSAs: `204`
- Web bulk rows: `1666`

## Validation Results

- Validation status: `PASS`
- Errors: `0`
- Campaign status rows: all `Paused`
- Ad group status rows: all `Paused`
- Keyword status rows: all `Paused`
- RSA/ad status rows: all `Paused`
- Max CPC: `0.15`, so `0` rows exceed `$0.20`
- Positive keyword match types: exact/phrase only
- No PMax rows
- No Standard Shopping rows
- No product-scope rows
- No product-group rows
- No feed-label edit rows
- No conversion-goal edit rows
- ES/IT/RO/PT final URLs use localized product paths plus `country=<ISO>`
- No bare `/es`, `/it`, `/ro`, or `/pt` product final URLs without country parameters were found

## Files Produced

- `refresh_country_urls.py`
- `country_tier_plan.csv`
- `campaign_structure.csv`
- `keyword_plan.csv`
- `negative_keyword_plan.csv`
- `rsa_copy_pack.csv`
- `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`
- `final_url_mapping.csv`
- `manifest.json`
- `summary.json`
- `manual_qa/approval_gate.md`
- `manual_qa/intl_search_pre_import_qa.csv`

## Residual Risks

- This is still not approval to import, create, preview, or enable anything in Google Ads.
- Country-qualified product URL behavior was browser-proven for ES/IT/RO/PT product landings; other markets still need their own country/currency/checkout readbacks before spend.
- English-only campaigns outside English-first countries may have limited reach and conversion quality.
- Any future Google Ads step must begin with exact owner approval, then preview-only import validation, then just-in-time readbacks before applying.
