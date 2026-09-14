# Google Shopping Parent-Outfit Remaining Eligibility Repair Or Exclusion Approval Packet

Generated: `2026-05-21T10:14:00Z`

Mode: approval packet only. This file does not authorize any write by itself.

## Why This Packet Exists

The read-only eligibility diagnostic found that the parent-outfit gate is still blocked after the approved TSV refresh:

- Gate remains `4,390 / 4,531` ready rows.
- Missing expected rows remain `141`.
- Ready-row label mismatches are `0`.
- Ready-row image mismatches are `0`.
- Bad catchall units are `0`.
- All V2 Shopping campaigns and the old test campaign remain paused.

The `141` missing rows now split into exact repair targets:

- `70` Ads-visible offer IDs with blank/not-ready labels.
- `71` Ads-absent offer IDs.

The eligibility diagnostic also found `20` expected rows that are `OUT_OF_STOCK` and carry the non-campaign error `not_eligible_out_of_stock`. Inventory changes are not part of the approved scope, so these rows need exclusion from strict paid-ready eligibility until stock state changes, or a separate exact inventory/source decision.

## Evidence To Read First

- `GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_DIAGNOSTIC_20260521.md`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_remaining_blocker_split_20260521.json`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_gate_missing_ads_visible_blank_or_not_ready_20260521.csv`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_gate_missing_ads_absent_20260521.csv`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_out_of_stock_expected_items_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_summary_20260521.json`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T095240Z.json`
- `merchant_source_10663204023_after_approved_tsv_refresh_20260521T093710Z.json`

## Proposed Narrow Repair Or Exclusion Scope

If approved, perform only these bounded actions:

1. Exclusion/spec handling for only the `20` current `OUT_OF_STOCK` expected offer IDs:
   - Do not change Shopify inventory.
   - Do not change product titles, prices, handles, body, SEO, images, options, variants, or publications.
   - Mark them out of the strict paid-ready included gate until they read `IN_STOCK`, or build the equivalent local/spec exclusion needed so the gate does not require out-of-stock rows to be eligible.

2. Supplemental label/image repair for only the `70` Ads-visible blank/not-ready expected offer IDs:
   - Use the existing approved parent-outfit label/image values only.
   - Preserve non-parent rows.
   - Preserve known non-label attributes such as `age_group`.
   - Do not reset broad Merchant sources.
   - Do not broaden beyond the exact `70` item IDs unless a readback proves the smallest source requires preserving surrounding non-parent rows.

3. Primary-source presence repair for only the `71` Ads-absent expected offer IDs:
   - Use the narrowest Google & YouTube / Merchant / Shopify Admin control surface that can make those exact offer IDs appear.
   - Do not trigger a broad account sync unless a current UI/API readback proves no narrow control exists and the owner gives separate approval for that broader action.
   - Do not recreate products.
   - Do not change Shopify product identity or merchandising fields.

4. Wait for processing, then rerun the read-only gate:

```bash
/tmp/dlm-google-ads-venv/bin/python dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/run_google_shopping_parent_outfit_merchant_feed_gate.py
```

Report:

- expected rows after approved exclusion/spec handling;
- ready rows;
- missing expected rows;
- image mismatches;
- label mismatches;
- bad catchalls;
- campaign paused readback;
- old test campaign paused readback;
- whether the `20` out-of-stock rows are excluded or still included.

## Approval Phrase

If approved, paste this exact phrase:

```text
Approve Google Shopping parent-outfit remaining eligibility repair/exclusion only: keep all Shopping V2 campaigns paused and keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused; exclude or hold out only the 20 current OUT_OF_STOCK expected offer IDs from strict paid-ready eligibility without changing Shopify inventory; refresh or update only the minimal approved supplemental label/image overlay needed for the 70 Ads-visible blank-label expected offer IDs; repair only the narrow Google & YouTube/Merchant primary-source presence for the 71 Ads-absent expected offer IDs; preserve non-parent rows and known non-label attributes such as age_group; do not change Shopify titles/prices/handles/body/SEO/inventory/publications, Google & YouTube broad account settings, Merchant feeds/sources outside the narrow approved rows/source, Google Ads campaigns/product groups/budgets/bids/statuses/conversions/billing, or trigger broad account sync; wait for processing and rerun the counts/images/no-catchall gate; no activation discussion until the gate passes and separate activation approval is given.
```

## Still Blocked Without Separate Approval

- No Shopping campaign activation or unpause.
- No budget, bid, status, product-group, conversion, campaign, or billing changes.
- No Merchant source reset, broad source refresh, or broad account sync.
- No Shopify title, price, handle, body, SEO, inventory, publication, option, image, or unrelated variant changes.
- No product recreation.
- No activation discussion until the gate passes and the owner gives separate activation approval.

## Stop Conditions

Stop and report before writing if any control surface requires:

- broad Google & YouTube account sync;
- product recreation;
- Merchant source reset affecting non-parent or unrelated rows;
- campaign/ad group/product group/status/budget/bid/conversion changes;
- billing, credential, account switcher, MFA, CAPTCHA, policy, or permission prompts;
- a Shopify product-data mutation outside the exact presence repair.
