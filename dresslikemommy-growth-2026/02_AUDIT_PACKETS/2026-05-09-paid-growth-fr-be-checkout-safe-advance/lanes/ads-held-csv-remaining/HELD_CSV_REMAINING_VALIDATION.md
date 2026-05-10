# Worker C Held CSV Remaining-Market Validation

- Generated: 2026-05-09T01:52:10
- Source CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- Lane: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-fr-be-checkout-safe-advance/lanes/ads-held-csv-remaining`
- Scope: local-only validation for checkout-pending countries `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR`.
- No Google Ads UI/account access, preview, import, upload, or live write was performed.

## Status

`PASS_LOCAL_ONLY_APPROVAL_GATED`: the held CSV remains locally valid for the seven remaining checkout-pending country campaigns. It is still not approved for live preview/import and does not make any market live-spend-ready.

## File-Level Readback

- Data rows: `1496`
- Header columns: `95`
- Campaigns: `17`
- Row types: `{'Campaign': 17, 'Ad group': 170, 'Keyword': 510, 'Negative keyword': 629, 'Ad': 170}`
- Actions: `{'Add': 1496}`
- CPC values found: `[0.1, 0.12, 0.15]`; rows over `$0.20`: `0`
- Existing ID hits: `{'Campaign ID': 0, 'Ad group ID': 0, 'Keyword ID': 0, 'Ad ID': 0}`

## Focus-Country Coverage

| Country | Rows | Campaign | Ad groups | Keywords | Negatives | Ads | Final URLs | URL country-param result |
|---|---:|---|---:|---:|---:|---:|---:|---|
| NL | 88 | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| FR | 88 | `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| BE | 88 | `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| SE | 88 | `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| PL | 88 | `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| CZ | 88 | `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |
| GR | 88 | `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 10 | 30 | 37 | 10 | 40 | PASS |

All seven focus countries have exactly `88` rows each: `1` campaign, `10` ad groups, `30` positive keywords, `37` negative keywords, and `10` ads. Each has `40` final URL rows with the matching `country=<ISO>` parameter.

## Guardrail Results

- `PASS` `total_data_rows`: `1496 data rows`
- `PASS` `campaign_count`: `17 campaigns`
- `PASS` `all_actions_add`: `{'Add': 1496}`
- `PASS` `all_importable_entities_paused`: `0 non-paused Campaign/Ad group/Keyword/Ad rows`
- `PASS` `ids_blank`: `{'Campaign ID': 0, 'Ad group ID': 0, 'Keyword ID': 0, 'Ad ID': 0}`
- `PASS` `cpc_cap_at_or_below_0_20`: `[0.1, 0.12, 0.15]`
- `PASS` `remaining_country_coverage`: `{'NL': 88, 'FR': 88, 'BE': 88, 'SE': 88, 'PL': 88, 'CZ': 88, 'GR': 88}`
- `PASS` `remaining_country_url_params`: `{'NL': {'missing': 0, 'wrong': 0}, 'FR': {'missing': 0, 'wrong': 0}, 'BE': {'missing': 0, 'wrong': 0}, 'SE': {'missing': 0, 'wrong': 0}, 'PL': {'missing': 0, 'wrong': 0}, 'CZ': {'missing': 0, 'wrong': 0}, 'GR': {'missing': 0, 'wrong': 0}}`
- `PASS` `no_vacation_family_or_bad_beach_handle_or_product`: `{'Vacation Family': 0, 'matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set': 0, '7227378892897': 0, 'Christmas': 0, 'Xmas': 0}`
- `PASS` `no_us_campaign_23827590655`: `{'23827590655': 0, 'US campaign name': 0}`
- `PASS` `no_forbidden_entity_types_or_surfaces`: `{}`

## Forbidden-Change Scan

- `0` hits for `Vacation Family`.
- `0` hits for bad beach handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`.
- `0` hits for product ID `7227378892897`.
- `0` hits for `Christmas` / `Xmas` in this CSV.
- `0` hits for US campaign ID `23827590655` or the known US nonbrand campaign name.
- `0` forbidden row/entity type hits for PMax, Standard Shopping, Shopping/product groups, feed labels, conversion goals, Merchant, or asset/listing/product-partition rows.

## Residual Gates

- This is local evidence only. Any Google Ads preview/import/upload still requires the exact owner approval gate from the canonical paid-growth prompt.
- The seven countries remain checkout-pending for live spend readiness; this report only validates that their paused CSV rows are structurally safe in the held packet.
- No Standard Shopping, PMax, Merchant, Pinterest, Shopify, product-scope, feed-label, product-group, conversion-goal, budget, bid, or status live changes were made.

## Raw Evidence

- `held_csv_remaining_validation_raw.json`
- `held_csv_remaining_country_summary.csv`
- `held_csv_remaining_check_results.csv`
