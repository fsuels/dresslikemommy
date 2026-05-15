# Merchant All-Products Source Eligibility Readback

Generated: `2026-05-15T05:42:46`

Mode: read-only Merchant Center browser download and local parsing. No external write occurred.

## Export

- Downloaded zip: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/browser-all-products-ready-download/products_2026-05-15_05-37-44.zip`
- TSV member: `products_2026-05-15_05-37-44.tsv`
- Total product rows: `351007`
- Source-id status: the TSV does not include `source_id`; `US/es` source `10627981690` remains tied by adjacent live source/detail readback, not by this TSV column.
- Approval-status status: the TSV does not include approved/disapproved destination status; decisions below fail closed.

## Target Market Summary

| Market | Language | Expected currency | Rows | In stock | Paid-cohort rows | Issue-export paid rows | Top feed labels | Decision |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `US` | `es` | `USD` | `5412` | `5301` | `772` | `53` | `US: 5412` | Rows exist in the all-products export, but US/es stays blocked by current issue-export and over-capacity evidence; export lacks source_id so source 10627981690 remains inferred from source/detail readback. |
| `CA` | `en` | `CAD` | `0` | `0` | `0` | `0` | `` | No CA/en rows appeared in the current all-products export; this market is not Shopping-build-ready from Merchant feed evidence. |
| `GB` | `en` | `GBP` | `0` | `0` | `0` | `0` | `` | No GB/en rows appeared in the current all-products export; this market is not Shopping-build-ready from Merchant feed evidence. |
| `AU` | `en` | `AUD` | `0` | `0` | `0` | `0` | `` | No AU/en rows appeared in the current all-products export; this market is not Shopping-build-ready from Merchant feed evidence. |

## Decisions

- `US/es`: rows exist, but the market remains blocked by the current issue export and over-capacity evidence. Do not build or repair from this packet alone.
- `CA/en`, `GB/en`, `AU/en`: no rows appeared in the current all-products export, and no CAD/GBP/AUD feed labels appeared. These markets are not Merchant Shopping-ready from current feed evidence.
- The next safe action is not a Shopping campaign build; it is a feed/source availability unblock or another authoritative Merchant export proving target rows exist.

## Outputs

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/merchant_all_products_source_eligibility_summary.json`
- Market summary CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/merchant_all_products_target_eligibility_summary.csv`
- Target paid-cohort rows CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/merchant_all_products_target_paid_cohort_rows.csv`
