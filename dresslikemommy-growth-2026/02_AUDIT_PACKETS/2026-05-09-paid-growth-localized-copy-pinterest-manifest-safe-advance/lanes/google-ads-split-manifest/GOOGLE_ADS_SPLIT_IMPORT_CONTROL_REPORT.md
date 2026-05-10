# Google Ads Split Import-Control Manifest

Status: `PASS_LOCAL_ONLY_APPROVAL_GATED`

## Scope

Worker A generated local-only split/import-control artifacts from the held non-US Search CSV. No Google Ads, Merchant Center, Shopify, Pinterest, campaign, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, or external-account writes were made.

Source CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
Source SHA256: `8401e29066693c4215760e0f9b09080f50d94de47f6e27300724f99ed5e0c814`

## Totals

- Total data rows: `1496`
- Campaigns: `17` non-US paused Search campaigns
- Row type counts: `{'Ad': 170, 'Ad group': 170, 'Campaign': 17, 'Keyword': 510, 'Negative keyword': 629}`
- Action counts: `{'Add': 1496}`
- Max default CPC: `$0.15`

## Per-Country Split Files

| Country | Location | Campaign | Rows | Campaign | Ad groups | Keywords | Negatives | Ads | Final URLs | Max CPC | Split CSV |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GB | United Kingdom | `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.15 | `split_csvs/GB_intl_search_paused_draft_web_bulk.csv` |
| CA | Canada | `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.15 | `split_csvs/CA_intl_search_paused_draft_web_bulk.csv` |
| AU | Australia | `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.15 | `split_csvs/AU_intl_search_paused_draft_web_bulk.csv` |
| CH | Switzerland | `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/CH_intl_search_paused_draft_web_bulk.csv` |
| DK | Denmark | `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/DK_intl_search_paused_draft_web_bulk.csv` |
| DE | Germany | `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/DE_intl_search_paused_draft_web_bulk.csv` |
| NL | Netherlands | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/NL_intl_search_paused_draft_web_bulk.csv` |
| SE | Sweden | `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/SE_intl_search_paused_draft_web_bulk.csv` |
| FR | France | `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/FR_intl_search_paused_draft_web_bulk.csv` |
| BE | Belgium | `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/BE_intl_search_paused_draft_web_bulk.csv` |
| ES | Spain | `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/ES_intl_search_paused_draft_web_bulk.csv` |
| IT | Italy | `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.12 | `split_csvs/IT_intl_search_paused_draft_web_bulk.csv` |
| PL | Poland | `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.10 | `split_csvs/PL_intl_search_paused_draft_web_bulk.csv` |
| CZ | Czechia | `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.10 | `split_csvs/CZ_intl_search_paused_draft_web_bulk.csv` |
| RO | Romania | `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.10 | `split_csvs/RO_intl_search_paused_draft_web_bulk.csv` |
| GR | Greece | `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.10 | `split_csvs/GR_intl_search_paused_draft_web_bulk.csv` |
| PT | Portugal | `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 1 | 10 | 30 | 37 | 10 | 40 | $0.10 | `split_csvs/PT_intl_search_paused_draft_web_bulk.csv` |

## Validation

| Check | Status | Detail |
|---|---:|---|
| `source_rows` | `PASS` | 1496 data rows |
| `action_add_only` | `PASS` | all rows use Action=Add |
| `no_existing_ids` | `PASS` | Campaign/Ad group/Keyword/Ad IDs are blank |
| `seventeen_non_us_campaigns` | `PASS` | 17 campaigns, codes=AU,BE,CA,CH,CZ,DE,DK,ES,FR,GB,GR,IT,NL,PL,PT,RO,SE |
| `no_us_campaign_names` | `PASS` | no campaign starts DLM_US_ |
| `campaigns_paused_search_only` | `PASS` | campaign rows are Paused Search / Google search / en |
| `all_importable_entities_paused` | `PASS` | Campaign/Ad group/Keyword/Negative keyword/Ad status fields are paused where applicable |
| `max_cpc_at_or_below_0_15` | `PASS` | max CPC found=0.15 |
| `forbidden_text_scan` | `PASS` | no US campaign id, bad beach URL/product, Vacation Family, PMax, Standard Shopping, product/feed/conversion/enablement terms |
| `no_product_feed_conversion_row_types` | `PASS` | row types=Ad, Ad group, Campaign, Keyword, Negative keyword |
| `final_urls_country_qualified` | `PASS` | every Final URL row carries country=<campaign country code> |

## Preview-Only Runbook

1. Before any Google Ads UI, Editor, API, preview, or import action, the parent/orchestrator must obtain the exact canonical paused non-US Google Search `TEST BUILD` approval from the owner.
2. Use the split file for the intended country or the full held CSV only in a preview/import validation flow. Do not enable campaigns, do not change budgets or bids, and do not touch PMax, Standard Shopping, product scope, feed labels, product groups, or conversion goals.
3. Confirm the preview shows only new paused Search entities: one paused campaign per selected country, ten paused ad groups, thirty paused positive keywords, thirty-seven paused negatives, and ten paused RSAs per country.
4. Confirm no existing campaign IDs or account entities are edited, especially US campaign `23827590655`.
5. CSV rows alone cannot prove the Google Ads location option. In the live Ads preview/readback, verify `Presence: People in or regularly in your included locations` before any launch decision.
6. After any approved paused import, perform just-in-time readbacks for status, budget, CPC, language, location, final URLs, exclusions, and conversion-goal inheritance before considering separate enablement approval.

## Residual Gate

These artifacts are import-control evidence only. They do not authorize live preview/import/build, live spend, campaign enablement, or any live-account write. Presence-only targeting remains a readback gate because it is not represented conclusively in the CSV.
