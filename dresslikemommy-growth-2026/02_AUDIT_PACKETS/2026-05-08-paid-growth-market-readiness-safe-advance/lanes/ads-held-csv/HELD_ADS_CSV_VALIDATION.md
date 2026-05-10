# Held Ads CSV Validation

Source CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`

Scope: local-only validation of the safer held non-US Google Search web bulk CSV. No Google Ads import, preview, account access, campaign creation, status change, bid change, budget change, product/feed/conversion change, Merchant upload, Shopify edit, or Pinterest write was performed.

## Result

Overall result: `PASS`

- Data rows: `1496`
- Header columns: `95`
- Campaigns: `17`
- Countries/locations: `17`
- Actions: `{'Add': 1496}`
- Entity counts: `{'Ad': 170, 'Ad group': 170, 'Campaign': 17, 'Keyword': 510, 'Negative keyword': 629}`
- CPC values observed: `[0.1, 0.12, 0.15]`; cap checked: `<= $0.20`
- Final URL rows checked: `680`

## Gate Checks

| Check | Hits | Result |
|---|---:|---|
| `status_not_paused` | 0 | PASS |
| `cpc_above_or_invalid` | 0 | PASS |
| `us_campaign_23827590655_hits` | 0 | PASS |
| `forbidden_pmax_hits` | 0 | PASS |
| `forbidden_standard_shopping_hits` | 0 | PASS |
| `forbidden_product_scope_feed_label_product_group_hits` | 0 | PASS |
| `forbidden_conversion_goal_hits` | 0 | PASS |
| `vacation_family_hits` | 0 | PASS |
| `bad_beach_handle_hits` | 0 | PASS |
| `bad_product_id_7227378892897_hits` | 0 | PASS |
| `bare_localized_final_urls_without_country` | 0 | PASS |
| `live_enable_hits` | 0 | PASS |
| `budget_increase_like_hits` | 0 | PASS |

All importable Campaign, Ad group, Keyword, and Ad rows are paused. Negative keyword rows have no status column in this export and are counted separately.

## Counts By Entity And Status

| Entity | Status Counts |
|---|---|
| `Ad` | `{'Paused': 170}` |
| `Ad group` | `{'Paused': 170}` |
| `Campaign` | `{'Paused': 17}` |
| `Keyword` | `{'Paused': 510}` |

## Counts By Country

| Location | Rows | Campaigns | Row Types |
|---|---:|---:|---|
| Australia | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Belgium | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Canada | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Czechia | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Denmark | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| France | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Germany | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Greece | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Italy | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Netherlands | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Poland | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Portugal | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Romania | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Spain | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Sweden | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| Switzerland | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |
| United Kingdom | 88 | 1 | Ad:10, Ad group:10, Campaign:1, Keyword:30, Negative keyword:37 |

## Counts By Campaign

| Campaign | Location | Rows | Campaign | Ad Group | Keyword | Negative Keyword | Ad | Statuses |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Australia | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Belgium | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Canada | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Switzerland | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Czechia | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Germany | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Denmark | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Spain | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | France | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | United Kingdom | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Greece | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Italy | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Netherlands | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Poland | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Portugal | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Romania | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |
| `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | Sweden | 88 | 1 | 10 | 30 | 37 | 10 | Paused:51 |

## Budget And CPC Readback

- Campaign budget rows: `17`; all are `Action=Add` and `Campaign status=Paused`.
- Budget values observed: `['1.00', '2.00']`.
- CPC observations: `170` values, observed set `[0.1, 0.12, 0.15]`.
- CPC failures over `$0.20` or invalid values: `0`.

## URL And Exclusion Readback

- Bare localized `/es`, `/it`, `/ro`, `/pt` final URLs without `country` parameter: `0`.
- `Vacation Family` hits: `0`.
- Bad beach handle hits: `0`.
- Product ID `7227378892897` hits: `0`.

## Notes

This file is suitable only as a local validation artifact for a future approval-gated preview/import decision. It does not grant approval to import, create, enable, raise budgets/bids, or send live traffic.
