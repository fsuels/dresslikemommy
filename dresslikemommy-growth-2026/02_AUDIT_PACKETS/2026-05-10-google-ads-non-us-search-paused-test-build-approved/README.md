# Google Ads Non-US Search Paused Test Build - Approved

Created: 2026-05-10 00:10 EDT

Current result: `PARTIAL_9_APPLIED_REMAINING_BLOCKED_BY_FR_STALE_PREVIEW_BE_THROTTLE_IT_STILL_IN_PROGRESS_PREVIEW_NO_LIVE_SPEND`

Scope: exact owner-approved paused Google Search TEST BUILD for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.

Approval received in current chat:

`APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.`

Canonical source artifacts:

- Held full CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- Split CSV manifest: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/manifest.json`
- Split CSVs: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/`

Stop conditions:

- Any preview/import path would create or edit US campaign `23827590655`.
- Any preview/import path touches PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product scope, feed label, product group, conversion goals, or existing budgets/bids/statuses.
- Any campaign, ad group, ad, or keyword would be enabled.
- Any CPC cap exceeds `$0.20`.
- Presence-only location targeting cannot be verified or set safely within the approved paused-build scope.
- Google Ads access, login, CAPTCHA, verification, file upload, or preview result cannot be read back cleanly.

Evidence folders:

- `raw/before-readbacks/`
- `raw/preview/`
- `raw/after-readbacks/`
- `working/`

Session report:

- `GOOGLE_ADS_NON_US_SEARCH_PAUSED_TEST_BUILD_APPROVED_PARTIAL_REPORT.md`

2026-05-10 continuation:

- Applied and read back paused Search campaigns for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, and `ES`.
- All 9 final readbacks are paused, Search, presence-only, content/YouTube off, and on approved split budgets.
- `FR` is not created: preview validated once, but a stale apply attempt produced `completed with errors` / `no changes`; later fresh FR preview stuck at `0` changes.
- `BE` is not created: upload preview blocked by Google Ads upload throttling.
- `IT` is not created: preview stayed in progress at `0` changes / `0` success / `0` errors after bounded waits and still showed in-progress on the 02:05 EDT recheck; no apply was clicked.
- `PL`, `CZ`, `RO`, `PT`, and `GR` remain absent and untouched.
- Next unresolved countries: `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`.
