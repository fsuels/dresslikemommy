# Google Ads International Search URL Hold Validation

Local-only held variant for `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`. No external account writes were made.

## Source

- Source web bulk CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`
- Source final URL mapping: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/final_url_mapping.csv`
- Blocked product: `7227378892897` / `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`
- Held theme/ad groups: `Vacation Family - Exact`, `Vacation Family - Phrase`

## Outputs

- Filtered import candidate CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- Removed rows CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/removed_rows_vacation_family_hold.csv`
- Filtered final URL mapping CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/final_url_mapping_vacation_family_hold_filtered.csv`
- Hold list CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/final_url_hold_list.csv`
- Validation JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/validation.json`

## Row Counts

Source total rows: `1666`  
Filtered total rows: `1496`  
Removed total rows: `170`

### Source By Record Type

| Key | Count |
|---|---:|
| `Campaign` | 17 |
| `Ad group` | 204 |
| `Keyword` | 612 |
| `Negative keyword` | 629 |
| `Ad` | 204 |

### Filtered By Record Type

| Key | Count |
|---|---:|
| `Campaign` | 17 |
| `Ad group` | 170 |
| `Keyword` | 510 |
| `Negative keyword` | 629 |
| `Ad` | 170 |

### Removed By Record Type

| Key | Count |
|---|---:|
| `Ad group` | 34 |
| `Keyword` | 102 |
| `Ad` | 34 |

### Removed By Ad Group

| Key | Count |
|---|---:|
| `Vacation Family - Exact` | 85 |
| `Vacation Family - Phrase` | 85 |

## Statuses In Filtered Candidate

| Status field | Value | Count |
|---|---|---:|
| `Campaign status` | `Paused` | 17 |
| `Campaign status` | `(blank)` | 1479 |
| `Ad group status` | `(blank)` | 1326 |
| `Ad group status` | `Paused` | 170 |
| `Keyword status` | `(blank)` | 357 |
| `Keyword status` | `Paused` | 1139 |
| `Ad status` | `(blank)` | 1326 |
| `Ad status` | `Paused` | 170 |

## CPC

- Maximum CPC found in filtered candidate: `$0.15`
- Unique CPC raw values: `0.10, 0.12, 0.15`
- At or below `$0.15`: `PASS`
- At or below `$0.20`: `PASS`

## Forbidden Row Checks In Filtered Candidate

| Check | Pattern | Hits | Pass |
|---|---|---:|---|
| `bad_handle` | `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` | 0 | PASS |
| `us_campaign_id_23827590655` | `23827590655` | 0 | PASS |
| `pmax` | `PMax` | 0 | PASS |
| `performance_max` | `Performance Max` | 0 | PASS |
| `standard_shopping` | `Standard Shopping` | 0 | PASS |
| `shopping_ads` | `Shopping ads` | 0 | PASS |
| `product_scope` | `product scope` | 0 | PASS |
| `feed_label` | `feed label` | 0 | PASS |
| `product_group` | `product group` | 0 | PASS |
| `conversion_goal` | `conversion goal` | 0 | PASS |

## Pass/Fail Gates

| Gate | Result |
|---|---|
| `removed_exact_expected_shape` | PASS |
| `filtered_total_expected_shape` | PASS |
| `no_bad_handle_in_filtered_bulk` | PASS |
| `no_us_campaign_23827590655` | PASS |
| `no_pmax` | PASS |
| `no_standard_shopping` | PASS |
| `no_product_scope_feed_label_product_group_conversion_goal_rows` | PASS |
| `all_campaigns_other_themes_preserved` | PASS |
| `all_mapping_bad_handle_rows_held` | PASS |

Overall validation: `PASS`

## Notes

- Campaign rows and non-`Vacation Family` themes remain in the filtered candidate.
- Removed rows are exactly the ad groups, keywords, and ads belonging to `Vacation Family - Exact` and `Vacation Family - Phrase` across the 17 non-US campaigns.
- The held final URL mapping rows explain the blocked handle, product ID, and problem ID so this URL can be repaired or replaced before any future approved import.
