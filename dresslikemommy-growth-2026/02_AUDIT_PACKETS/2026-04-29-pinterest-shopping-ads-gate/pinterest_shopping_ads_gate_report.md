# Pinterest Shopping Ads Gate Report

Generated: 2026-04-29T05:34:56

## Decision

`DO NOT CLICK CREATE AN AD, CREATE PRODUCT GROUPS, OR LAUNCH PINTEREST SHOPPING ADS YET.`

Pinterest status is promising and the exact item-level EN-US catalog readback passed for the current candidate rows, but the launch gate is still closed because full event/CAPI/deduplication proof, USA-only targeting proof, ROAS evidence, and explicit operator launch approval are not complete.

## Current Evidence

- Existing authenticated capture showed Pinterest catalog and conversion tracking active, 0 campaigns, 0 ads, and $0.00 spend across captured 30/90/365-day windows.
- Post-ingestion recheck showed English Warning 188 cleared and Shopify-side active Pinterest scope clean for compare-at, long description, and the shallow category fix, while non-English feed rechecks still needed another completion window.
- Item-level Pinterest catalog readback covered 346 candidate offer rows with statuses: `{"FOUND_EN_US_IN_STOCK": 346}`.
- Controlled Test Events captured PageVisit, ViewCategory, Search, and AddToCart rows with visible event IDs and no visible issue text; the pass stopped at checkout start and did not trigger AddPaymentInfo or Checkout/Purchase.
- Operator-reported current context: merchant approved, Shopify connected, Event Quality Score = Good setup, and organic Last 30 activity of 12.4K impressions, 317 engagements, and 31 saves.

## Review-Only Product Groups

| Product group | Candidate offer rows | Shopify products | Feed/PDP pass rows | Pinterest readback pass rows | Pinterest item gate |
|---|---:|---:|---:|---:|---|
| Mommy & Me | 214 | 28 | 214 | 214 | PASS_EXACT_EN_US_IN_STOCK_READBACK |
| Family Matching | 103 | 7 | 103 | 103 | PASS_EXACT_EN_US_IN_STOCK_READBACK |
| Pajamas | 29 | 1 | 29 | 29 | PASS_EXACT_EN_US_IN_STOCK_READBACK |

## Post-Gate Structure

- Campaign: `DLM_PIN_US_SHOPPING_TEST_PAID_READY`.
- Objective: Shopping/catalog sales only.
- Country targeting: United States only.
- Status: paused or draft only at creation; live launch needs separate explicit approval.
- Product groups: Mommy & Me, Family Matching, and Pajamas only.
- Include only rows with known cost, clean feed/PDP status, in-stock availability, `custom_label_0=paid_eligible`, and `custom_label_4=us_test_ready`.
- Exclude All Products, unknown-cost rows, out-of-stock rows, unverified landing pages, international targeting, and anything without exact Pinterest catalog proof.

## Gates Still Required

1. Keep the candidate set limited to rows with current `FOUND_EN_US_IN_STOCK` readback; rerun item readback if the catalog refreshes or the row set changes.
2. Verify event-level health through AddPaymentInfo and Checkout/Purchase without creating a real paid order, and confirm CAPI/tag deduplication if Pinterest exposes it.
3. Confirm the ad setup UI can target USA only before any draft is saved.
4. Keep required ROAS at or above `6.67`; there is no Pinterest paid ROAS yet because spend is `$0.00`.

## Output Files

- `candidate_offer_rows`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/pinterest_paid_ready_candidate_offer_rows.csv`
- `excluded_offer_rows`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/pinterest_excluded_paid_cohort_rows.csv`
- `gate_report`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/pinterest_shopping_ads_gate_report.md`
- `product_group_manifest`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/pinterest_product_group_manifest_review_only.csv`
- `summary`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/summary.json`
