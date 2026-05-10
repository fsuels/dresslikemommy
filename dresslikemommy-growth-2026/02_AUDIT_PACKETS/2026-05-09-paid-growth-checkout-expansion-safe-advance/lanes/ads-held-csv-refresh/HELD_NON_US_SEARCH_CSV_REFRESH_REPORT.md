# Held Non-US Search CSV Refresh

Date: 2026-05-09

Source CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`

Scope: local/read-only validation only. No Google Ads browser/account was opened. No import, preview, upload, campaign creation, enablement, budget/bid/status change, product-scope/feed-label/product-group change, conversion-goal change, Merchant edit, Shopify edit, Pinterest edit, or live spend action was performed.

## Result

Overall result: `PASS_LOCAL_ONLY_APPROVAL_GATED`

- Data rows: `1496`
- Header columns: `95`
- Actions: `Add=1496`
- Campaigns: `17`
- Locations: `17`
- Entity counts: `Campaign=17`, `Ad group=170`, `Keyword=510`, `Negative keyword=629`, `Ad=170`
- Final URL rows checked: `680`
- Final URL country params: `40` rows each for `AU`, `BE`, `CA`, `CH`, `CZ`, `DE`, `DK`, `ES`, `FR`, `GB`, `GR`, `IT`, `NL`, `PL`, `PT`, `RO`, and `SE`
- CPC values observed: `$0.10`, `$0.12`, `$0.15`; cap checked: `<= $0.20`
- Budget values observed on new paused campaign rows: `$1.00/day`, `$2.00/day`
- Existing entity ID columns: all blank for `Campaign ID`, `Ad group ID`, `Keyword ID`, and `Ad ID`

## Guardrail Checks

| Check | Hits / failures | Result |
|---|---:|---|
| All importable entity statuses paused | `0` failures | `PASS` |
| CPC above `$0.20` or invalid | `0` | `PASS` |
| Budget rows above `$2.00` or invalid | `0` | `PASS` |
| Non-Add actions | `0` | `PASS` |
| Existing entity IDs populated | `0` | `PASS` |
| US campaign `23827590655` | `0` | `PASS` |
| `PMax` / Performance Max text | `0` | `PASS` |
| Standard Shopping text | `0` | `PASS` |
| Product scope, feed label, product group, Merchant text | `0` | `PASS` |
| Conversion goal text | `0` | `PASS` |
| `Vacation Family` text | `0` | `PASS` |
| Bad beach handle text | `0` | `PASS` |
| Product ID `7227378892897` | `0` | `PASS` |
| Bare localized `/es`, `/it`, `/ro`, `/pt` final URLs without `country=` | `0` | `PASS` |
| Live enablement words | `0` | `PASS` |
| Budget-increase wording | `0` | `PASS` |

Negative keyword rows do not carry a status column in this web-bulk export and were counted separately from importable paused entities.

## Campaign And Location Counts

| Campaign | Location | Rows | Campaign | Ad group | Keyword | Negative keyword | Ad |
|---|---|---:|---:|---:|---:|---:|---:|
| `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Australia | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Belgium | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Canada | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Switzerland | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Czechia | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Germany | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Denmark | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Spain | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | France | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | United Kingdom | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Greece | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Italy | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Netherlands | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Poland | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Portugal | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Romania | 88 | 1 | 10 | 30 | 37 | 10 |
| `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Sweden | 88 | 1 | 10 | 30 | 37 | 10 |

## Preview/Import Preflight Checklist

This checklist is for a future parent/orchestrator only. It does not grant approval and must not be treated as permission to import.

1. Get the canonical `TEST BUILD` approval wording exactly:

```text
APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.
```

2. Before preview/import, re-run this local CSV validation against the exact file that will be uploaded.
3. Confirm the selected file is the held `1496`-row CSV, not the older `1666`-row CSV that still included Vacation Family rows.
4. Confirm all importable entities are paused and all ID columns are blank.
5. Confirm the bad beach handle, product ID `7227378892897`, and `Vacation Family` text remain absent.
6. Confirm no US campaign `23827590655`, PMax, Standard Shopping, product-scope, feed-label, product-group, conversion-goal, Merchant, Shopify, Pinterest, theme, enablement, bid-increase, or budget-increase rows exist.
7. Use Google Ads upload preview only after approval; do not apply the preview until the preview row counts and entity types match this report.
8. After any approved preview/import, read back that every created Campaign, Ad group, Keyword, and Ad is still paused, CPC is still `<= $0.20`, and no live spend can accrue.
9. Live spend remains separately blocked. Enabling any campaign requires a new exact approval after checkout, Merchant/Pinterest/tracking, economics, and landing-page gates are cleared.

## Residual Risks

- This is local CSV validation only; it does not prove Google Ads upload preview compatibility or account-side policy eligibility.
- The packet is suitable only for paused non-US Search infrastructure. It is not a live-spend packet.
- `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, and `GR` still need no-payment checkout-to-shipping QA before live spend.
- The beach/vacation product metadata problem remains unresolved on Shopify; this held CSV mitigates Ads import risk by excluding the affected rows rather than fixing the product URL.

## Account-Write Confirmation

No account writes were made. No Google Ads, Merchant Center, Shopify Admin, Pinterest, GA4/GTM, theme, feed, product, campaign, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, import, preview, upload, or enablement action was performed.
