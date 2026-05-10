# Merchant US/es Age Group Diagnosis

Generated: 2026-05-08 03:03 EDT

Lane: Merchant US/es age_group diagnosis for `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`.

Scope: local/read-only artifact diagnosis only. No Merchant upload, source sync, source edit, Shopify product edit, Google Ads/Pinterest write, budget/bid/status/product-scope/feed-label/product-group/conversion-goal change, checkout payment/order, spend, or enablement was made.

## Current Status

Status: `US_ES_SPANISH_US_SURFACE_STILL_HAS_MISSING_AGE_GROUP`.

The original paid-growth blocker for current `US` / `en` / `United States` paid cohort rows remains cleared in the exact export. The remaining age_group issue is isolated to a separate Spanish-language US context:

- Feed label: `US`
- Language: `es`
- Country: `United States`
- Issue: `Missing age group`
- Unique paid-cohort item IDs: `625`
- Rows: `1,250`
- Traffic split: `625` `Shopping ads` rows and `625` `Free listings` rows
- Item status: `ELIGIBLE_LIMITED` for all `1,250` rows
- Issue severity: `SEVERITY_DEMOTED` for all `1,250` rows
- Click potential: `1,244` `Low`, `6` `Available soon`

## What We Can Prove

1. The exact product-issues export contains no paid-cohort `US` / `en` / `United States` `Missing age group` rows.
2. The same export contains `625` paid-cohort item IDs with `Missing age group` only in `US` / `es` / `United States`.
3. Every one of the `625` US/es affected IDs exists in the local age_group review/upload artifact, so local derived age_group values exist for these IDs:
   - `adult`: `284`
   - `kids`: `216`
   - `toddler`: `123`
   - `infant`: `2`
4. The dedicated supplemental source `10651516446` / `upload_paid_cohort_age_group_only.txt` is documented as joined to `Shopify App API (US, English)`, with feed label `US` and content language `en`.
5. Source processing for `10651516446` recognized `n:age_group`, updated `780` rows, matched `771`, and showed `9` `Offer does not exist` rows.
6. The US/en sample product detail after the source landed contains effective `n:age_group` and no longer lists `Missing age group`; it lists only the separate local-inventory add-on issue.
7. Readback probes show the Spanish US item is a separate Shopify App API row/source path:
   - US/en sample row: source `10627623003` / `Shopify App API`, feed label `US`, language `en`, last updated `2026-05-08T05:55:06+00:00`, labels `paid_eligible` and `us_test_ready`.
   - US/es sample row: source `10627981690` / `Shopify App API`, feed label `US`, language `es`, last updated between `2026-05-04T20:09:48+00:00` and `2026-05-07T19:26:38+00:00` in sampled artifacts, labels either old/empty and not `paid_eligible` + `us_test_ready`.

## Likely Source Path

Most likely path: `Shopify App API` source `10627981690`, feed label `US`, language `es`.

Reasoning:

- The exact export's remaining paid-cohort age_group rows are exactly `US` / `es` / `United States`.
- Sample source probes for affected IDs expose a distinct `US` / `es` `Shopify App API` row under source `10627981690`.
- The existing dedicated age_group source is explicitly `US` / `en` and joined to `Shopify App API (US, English)`, so it plausibly repaired only the English US source path.
- The US/en processed sample now contains `n:age_group`, while the US/es export rows still report missing age group.

## Serving Risk Assessment

Current US/en Standard Shopping serving risk: `LOW / NOT THE CURRENT US_EN GATE`.

Evidence:

- Exact export count for paid-cohort `US` / `en` / `United States` `Missing age group` is `0`.
- US/en sample product detail contains `n:age_group`.
- US/en sample row has the current paid-targeting labels `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- US/es sample rows are distinct source rows and do not show the current paid-targeting label pair in the inspected readbacks.

Spanish-language US risk: `ACTIVE DIAGNOSTIC / DO NOT USE FOR PAID TESTING YET`.

Evidence:

- The exact export marks the affected US/es rows under both `Shopping ads` and `Free listings`.
- All affected rows are `ELIGIBLE_LIMITED` and `SEVERITY_DEMOTED`, so this looks like a visibility/ranking limitation, not a disapproval.
- Because the traffic type includes `Shopping ads`, Spanish-language US Shopping usage should remain gated until this is fixed or a fresh readback proves it cleared.

## Attempts

### Attempt 1 - Exact Export Reconciliation

Inputs:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/raw/product-issues-browser-export/product_issues_2026-05-08_01-58-05.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-dedicated-supplemental-repair/age_group_only_upload_review.csv`

Result:

- Export rows: `33,620`
- Paid cohort item IDs: `780`
- Paid-cohort `Missing age group`, any context: `1,250` rows / `625` unique IDs
- Paid-cohort `US` / `en` / `United States`: `0` rows / `0` unique IDs
- Paid-cohort `US` / `es` / `United States`: `1,250` rows / `625` unique IDs
- All `625` US/es affected IDs are present in the age_group-only upload/review files.

### Attempt 2 - Source And Report Artifact Inspection

Inputs:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-dedicated-supplemental-repair/join_input_requests_new_source_details.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-dedicated-supplemental-repair/new_source_processing_report_rpc.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/source-detail-processing-readback/source_detail.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/readback-after-timestamp-advance/browser-source-readback/merchant_exact_label_readback_refresh_check.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/raw/browser-source-readback-us-es-sample/merchant_exact_label_readback_refresh_check.json`

Result:

- Dedicated supplemental source `10651516446` is `US` / `en`, used in `Shopify App API (US, English)`.
- The source accepted `age group` / `n:age_group` and matched most paid-cohort IDs.
- The US/en product detail readback shows effective `n:age_group`.
- The US/es product-list readback shows a separate `Shopify App API` source ID `10627981690`.

## Ruled-Out Or Failed Paths

- Not a repeat Shopify ProductVariant age_group data problem based on current local evidence: all `625` affected US/es IDs already have derived age_group values in the local review/upload file.
- Not a remaining US/en exact-export blocker: current paid-cohort US/en exact count is `0`.
- Not explained by the dedicated source's `9` unmatched rows: the visible unmatched examples can account for only a small subset, while the US/es issue affects `625` IDs. The source is also joined to `US` / `en`, not `US` / `es`.
- Not safe to fix live in this subagent lane: any Merchant source creation/upload/sync/source edit or Shopify product-data change is outside the current guardrails and requires owner action-time approval.

## Next Gate

Next read-only gate:

1. In Merchant, inspect at least one affected item detail with `language=es`, `feedLabel=US`, and source `10627981690`.
2. Confirm whether the US/es processed product data lacks `n:age_group` while US/en contains it.
3. Inspect source/settings details for `10627981690` to confirm whether there is a joinable Spanish US source path.

Next live-fix approval gate:

- Any live fix requires fresh explicit owner approval because it would likely require a Merchant source action for the US/es source path, a Merchant upload, a source sync/update, or a Shopify data/channel action.
- Do not reuse the US/en dedicated source action as approval for US/es.

Fixed criteria:

- Fresh exact product-issues export or equivalent readback shows `0` paid-cohort `Missing age group` rows for feed label `US`, language `es`, country `United States`.
- At least one affected US/es product detail readback shows effective `n:age_group`.
- US/en paid labels and Standard Shopping scope remain unchanged.

## Files Produced

- `MERCHANT_US_ES_AGE_GROUP_DIAGNOSIS.md`
- `merchant_us_es_age_group_summary.json`
- `merchant_us_es_age_group_sample.csv`
