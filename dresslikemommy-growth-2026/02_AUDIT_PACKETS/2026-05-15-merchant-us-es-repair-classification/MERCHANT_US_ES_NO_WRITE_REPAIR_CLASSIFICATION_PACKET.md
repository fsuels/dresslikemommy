# Merchant US/es No-Write Repair Classification Packet

Generated: `2026-05-15T05:26:11`

Mode: local/read-only classification from the current Merchant issue export. No external write occurred.

## Source

- Current classified issue rows: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_target_issue_rows.csv`
- Prior readback packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md`

## Summary

- Market/language: `US` / `es`
- Issue rows classified: `1453`
- Unique issue items: `354`
- Paid-cohort issue items: `53`
- Paid-cohort attribute-repair candidates: `3`

## Repair Scope By Issue

| Issue | Rows | Unique items | Paid-cohort items | Action class |
|---|---:|---:|---:|---|
| Missing age group | 432 | 216 | 1 | attribute_repair_candidate |
| Missing color | 202 | 101 | 2 | attribute_repair_candidate |
| Missing gender | 86 | 43 | 2 | attribute_repair_candidate |
| Missing product image | 3 | 1 | 0 | image_or_feed_recheck_required |
| Missing size | 10 | 5 | 0 | attribute_repair_candidate |
| Over capacity for Shopping ads (outside of CSS program) | 708 | 354 | 53 | capacity_scope_decision_required |
| Product page unavailable | 12 | 4 | 0 | landing_or_product_status_recheck_required |

## Paid-Cohort Priority Items

Top rows below are the first `15` paid-cohort items from the current issue export. Use the full CSV for exact row handling.

| Item ID | Issue rows | Issue titles |
|---|---:|---|
| `shopify_US_7107978395745_41493652963425` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108009197665_41493704310881` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108125753441_41493913829473` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108938039393_41496456364129` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108942397537_41496468619361` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108948820065_41496491524193` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108953604193_41496508694625` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7108958519393_41496524718177` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109072257121_41496915574881` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109084807265_41496962760801` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109119705185_41497069289569` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109123670113_41497082822753` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109267947617_41497323634785` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109267947617_41497323995233` | 2 | Over capacity for Shopping ads (outside of CSS program) |
| `shopify_US_7109267947617_41497324159073` | 2 | Over capacity for Shopping ads (outside of CSS program) |

## Decision

`US/es` is not Shopping-build-ready. The current issue export proves live blockers, but it is not safe repair authority because it lacks `source_id` and full active approved-product state.

Do not repair by stale May 8 files, sample-clear rows, or concept copy. The next safe step is a current full all-products/source export for source `10627981690`, with country, language, feed label, currency, product status, active/approved state, paid-cohort intersection, and source timestamp.

## Approval Packet For Future Repair

Use this only after the full source/all-products export confirms exact affected rows:

`I approve a no-spend Merchant US/es repair preflight for source 10627981690 limited to the exact current paid-cohort rows proven by the full export, covering only age_group, color, gender, size, page/image availability, and capacity decision analysis. Do not change campaign status, budget, bids, product groups, feed scope, source scope, conversion settings, billing, Shopify customer-visible copy, or Pinterest/Google Ads campaign objects. Save before/after readbacks and stop on any additional approval, account, policy, or destructive prompt.`

## Output Files

- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-us-es-repair-classification/merchant_us_es_repair_scope_by_issue.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-us-es-repair-classification/merchant_us_es_paid_cohort_priority_items.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-us-es-repair-classification/merchant_us_es_repair_classification_summary.json`
