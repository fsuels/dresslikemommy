# Merchant Shopping Read-Only Queue Readback

Generated: `2026-05-15T05:19:57`
Mode: read-only Merchant issue export analysis. No Merchant, Google Ads, Shopify, feed, title, product-group, bid, budget, status, campaign, conversion, billing, or credential write occurred.

## Source Evidence

- Current Merchant issue export: `/Users/fsuels/Downloads/product_issues_2026-05-15_05-10-59.csv` (`266318` rows, modified `2026-05-15T05:14:16`)
- Google Ads product report already downloaded: `/Users/fsuels/Downloads/Product report.csv` (modified `2026-05-15T05:04:18`)
- API attempt: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-api-attempt/merchant_center_api_diagnostics_summary.json`
- Chrome DevTools MCP was profile-locked; direct local CDP/RPC evidence paths were used where available.

## Results

| Market | Language | Issue rows | Unique items | Paid-cohort issue items | Shopping ads issue rows | Shopping disapproved rows | Top issues | Decision |
|---|---:|---:|---:|---:|---:|---:|---|---|
| US | es | 1453 | 354 | 53 | 724 | 359 | Over capacity for Shopping ads (outside of CSS program): 708 | Missing age group: 432 | Missing color: 202 | Missing gender: 86 | Product page unavailable: 12 | Missing size: 10 | Missing product image: 3 | US/es is not Shopping-build-ready from this export; current issue rows include age_group and Shopping capacity blockers. |
| CA | en | 0 | 0 | 0 | 0 | 0 |  | No current issue-export rows surfaced for this country/language, but this is not full eligibility proof. |
| GB | en | 0 | 0 | 0 | 0 | 0 |  | No current issue-export rows surfaced for this country/language, but this is not full eligibility proof. |
| AU | en | 0 | 0 | 0 | 0 | 0 |  | No current issue-export rows surfaced for this country/language, but this is not full eligibility proof. |

## Decision

- `US/es` is not ready for a Shopping build from this readback: current issue rows include `Missing age group`, `Missing color`, `Missing gender`, product-page/image issues, and the Shopping capacity warning.
- `CA/en`, `GB/en`, and `AU/en` showed `0` rows in the current issue export, which is useful but incomplete. It clears visible issue-export blockers only; it does not prove active approved product counts or feed/source availability.
- Do not create Shopping campaigns, change feed/title/product groups, alter product scope, or change budget/bid/status from this packet.

## Next Action

- Prepare a no-write `US/es` repair/classification packet from the current issue rows, starting with age_group/color/gender and page/image issues.
- Capture a full current all-products/source export for CA/GB/AU proving country, currency, feed label, active approved count, and paid-cohort intersection before any Shopping build.

## Output Files

- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_market_language_summary.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_issue_title_counts.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_target_issue_rows.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_readonly_queue_summary.json`
