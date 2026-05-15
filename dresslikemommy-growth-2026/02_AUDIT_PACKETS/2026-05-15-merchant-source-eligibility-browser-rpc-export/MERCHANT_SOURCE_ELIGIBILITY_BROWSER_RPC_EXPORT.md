# Merchant Source / Eligibility Browser RPC Export

Generated: 2026-05-15T05:51:13

Mode: read-only Merchant Center browser RPC export. No Merchant, Ads, Shopify, Pinterest, feed, product, product-group, bid, budget, status, capacity, or conversion writes were made.

## Export Summary

| Export | Rows | Strict approved | Paid-cohort rows | Paid-cohort strict approved | Key source/currency |
| --- | ---: | ---: | ---: | ---: | --- |
| `us_es_source_10627981690` | 5412 | 4910 | 5158 | 4770 | `{"10627981690": 5412}` |
| `ca_en_eligibility` | 0 | 0 | 0 | 0 | `{}` |
| `gb_en_eligibility` | 0 | 0 | 0 | 0 | `{}` |
| `au_en_eligibility` | 0 | 0 | 0 | 0 | `{}` |

## Interpretation

- This browser RPC export complements the browser-downloaded TSV packet in `2026-05-15-merchant-source-all-products-export-attempt`: the TSV proves the full `351,007` row all-products denominator, while this RPC export adds `source_id` and raw status fields.
- `US/es` source `10627981690` is present with `5,412` rows and `4,910` strict-approved product-list rows, but current issue-export evidence still blocks repair/build decisions.
- CA/en, GB/en, and AU/en remain absent: the same full product-list snapshot contains `0` English CAD/GBP/AUD rows, so these markets are not Shopping-build-ready from Merchant feed evidence.
- The paid-cohort columns in this RPC CSV are item-id joins against local paid eligibility; use the TSV packet's target paid-label count (`772` `US/es` rows) and the issue/classification packets for repair prioritization.

## Decision Boundary

- This export is evidence only. It does not approve Merchant repair, capacity requests, Shopping campaign creation, feed/title changes, product-group changes, bid/budget/status changes, or conversion-goal changes.
- Treat `US/es` source `10627981690` separately from CA/en, GB/en, and AU/en English currency eligibility.
- Any live Merchant repair or paid-media mutation still needs an exact owner approval packet.

## Files

- `all_products_sanitized`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_all_products_browser_rpc_sanitized.csv`
- `us_es_source_10627981690`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_us_es_source_10627981690.csv`
- `ca_en_eligibility`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_ca_en_eligibility.csv`
- `gb_en_eligibility`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_gb_en_eligibility.csv`
- `au_en_eligibility`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_au_en_eligibility.csv`
- `summary`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_source_eligibility_browser_rpc_summary.json`
