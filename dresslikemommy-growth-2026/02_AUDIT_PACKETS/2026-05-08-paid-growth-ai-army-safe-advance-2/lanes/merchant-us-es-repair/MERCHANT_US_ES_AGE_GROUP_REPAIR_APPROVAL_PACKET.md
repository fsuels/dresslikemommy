# Merchant US/es Age Group Repair Approval Packet

Prepared: 2026-05-09

Problem ID: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Mode: local/read-only approval packet only. This subagent did not access external accounts and did not upload Merchant feeds, click sync/refresh/update, edit a source, edit Shopify data, change ads, or change paid-feed/campaign settings.

Write scope honored: only this lane directory.

## Executive Decision

Status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`.

The original paid-cohort `US` / `en` / `United States` `Missing age group` blocker is solved and should not be reworked. The remaining issue is a separate Spanish-language US surface:

- Merchant Center account: `124884876`
- Source path: `10627981690` / `Shopify App API`
- Feed label: `US`
- Language: `es`
- Country: `United States`
- Issue: `Missing age group`
- Exact affected paid-cohort count: `625` item IDs / `1,250` rows
- Traffic split: `625` `Shopping ads` rows and `625` `Free listings` rows
- Current status: `ELIGIBLE_LIMITED` / `SEVERITY_DEMOTED`

No live repair should be attempted without fresh exact owner approval that names source `10627981690`, the `US/es/United States` surface, the selected repair path, preflight readbacks, and post-readbacks.

## Evidence Chain

1. Exact Merchant export after US/en repair:
   - Report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/MERCHANT_AGE_GROUP_EXACT_EXPORT_READBACK_REPORT.md`
   - Summary: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-summary-2026-05-08-0252.json`
   - Context breakdown: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`
   - Result: paid-cohort `US/en/United States` `Missing age group` count is `0`, down from prior exact `623`.

2. Local US/es diagnosis:
   - Report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/merchant-us-es/MERCHANT_US_ES_AGE_GROUP_DIAGNOSIS.md`
   - Summary: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-safe-followup/lanes/merchant-us-es/merchant_us_es_age_group_summary.json`
   - Result: remaining paid-cohort age_group rows are only `US/es/United States`: `625` IDs / `1,250` rows. All `625` affected IDs have local derived age_group values.

3. Live read-only US/es product detail readback:
   - Report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
   - Summary: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/merchant_us_es_source_detail_readback_summary.json`
   - Result: two affected US/es sample details on source `10627981690` still show `Missing age group` and lack effective `n:age_group`; one control sample on the same source has effective `n:age_group` and no `Missing age group`.

## Why US/en Is Solved And US/es Is Separate

US/en is solved because the exact all-issues Merchant export shows `0` paid-cohort `US/en/United States` `Missing age group` rows, and the cleared sample item is no longer in the US/en issue set.

The US/en repair path involved the US English source path:

- Source `10627623003` / `Shopify App API`
- Feed label `US`
- Language `en`
- Dedicated age_group-only supplemental source `10651516446` / `upload_paid_cohort_age_group_only.txt`
- Source `10651516446` was joined to `Shopify App API (US, English)`, recognized `n:age_group`, updated `780` products, matched `771`, and left `9` unmatched `Offer does not exist` rows.

US/es is separate because the remaining issue rows are only:

- Feed label `US`
- Language `es`
- Country `United States`
- Source `10627981690` / `Shopify App API`

The US/es source path is not the same as the repaired US/en source path. The read-only detail readback confirms affected US/es product details still lack effective `n:age_group`, while a control sample on source `10627981690` already has `n:age_group`. That means this is a targeted Spanish US source/data propagation problem, not a reason to redo broad Shopify age_group work or reopen the US/en Standard Shopping gate.

## Repair-Path Candidate A: US/es Age_Group-Only Supplemental Source

Candidate A is the preferred deterministic path if Merchant supports a clean preview/join for the Spanish US source.

Action after approval:

- Create or update one age_group-only supplemental source for source `10627981690` / `Shopify App API`.
- Target only feed label `US`, language `es`, country `United States`.
- Use only exact previewed affected paid-cohort item IDs, currently `625`.
- Use only columns `id` and `age_group`.
- Do not include custom labels, source URLs, product scope attributes, product groups, campaigns, prices, descriptions, shipping, inventory, or any non-age_group attribute.
- Do not touch US/en source `10627623003`, Standard Shopping, feed labels, product groups, conversion goals, budgets, bids, status, Pinterest, or Shopify product data.

Why this is safe:

- It limits the write to the missing attribute and the exact failing language/feed/country surface.
- It avoids broad source refresh side effects.
- It has a clear previewable row count and file schema.

Primary risk:

- It is still a Merchant upload/source action and must not be done without exact approval and a preview that proves the source joins to `10627981690` / `US` / `es`.

Exact owner approval text for Candidate A:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

## Repair-Path Candidate B: Source-Specific Official Refresh

Candidate B is a fallback if Merchant/Shopify exposes a clearly source-specific official refresh/sync/update-products control for source `10627981690`.

Action after approval:

- Read back source `10627981690` and at least two affected US/es product details first.
- Use exactly one clearly labeled official refresh/sync/update-products control only if it is source-specific or context-specific to source `10627981690` / `US` / `es`.
- Do not use a broad all-sources refresh.
- Do not upload a file.
- Do not edit source settings, Shopify products, labels, product scope, campaign settings, budgets, bids, or conversion goals.

Why this can be safe:

- It follows the native app/source path and may pick up already-correct source data without creating a new supplemental source.

Primary risk:

- Official refresh controls may be broader than they look and may affect more than the Spanish US source. If the UI cannot prove the action is narrow, do not use this path.

Exact owner approval text for Candidate B:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH B ONLY: READ BACK SOURCE 10627981690 AND TWO AFFECTED US/ES PRODUCT DETAILS FIRST; THEN CLICK ONE CLEARLY LABELED SOURCE-SPECIFIC OFFICIAL SHOPIFY APP API / GOOGLE & YOUTUBE REFRESH, SYNC, OR UPDATE-PRODUCTS CONTROL ONLY IF THE UI CONTEXT PROVES IT APPLIES TO SOURCE 10627981690 / FEED LABEL US / LANGUAGE ES; NO MERCHANT UPLOAD, SOURCE CREATION, PRIMARY SOURCE EDIT, SHOPIFY PRODUCT-DATA EDIT, GOOGLE ADS, PINTEREST, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; DO NOT USE A BROAD ALL-SOURCES REFRESH; READ BACK SOURCE TIMESTAMP, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

## Ruled-Out Paths

- Redoing Shopify ProductVariant `mm-google-shopping.age_group` edits: ruled out because Shopify-side paid-cohort age_group was already repaired and all `625` affected US/es IDs have local derived age_group values.
- Treating US/es as a reopened US/en blocker: ruled out because exact US/en paid-cohort count is `0`.
- Explaining the issue as the US/en dedicated source's `9` unmatched rows: ruled out because US/es affects `625` IDs and the dedicated source was joined to `US/en`, not `US/es`.
- Broad Merchant refresh/sync/update: ruled out without exact approval because it can affect unrelated sources and attributes.
- Merchant source edit without preview: ruled out.
- Shopify product-data edits: ruled out unless a fresh readback proves Shopify age_group regressed, which current evidence does not show.
- Product-scope, feed-label, product-group, Standard Shopping, PMax, conversion-goal, budget, bid, status, or live-spend changes: ruled out for this repair.
- Local inventory feed/store-pickup/physical-store repair: ruled out as a wrong surface for this dropshipping business and unrelated to age_group.

## Required Preflight Readbacks

Before any live repair:

1. Confirm coordination row is clear or parent owns a narrow active write claim for Merchant US/es age_group only.
2. Fresh exact Merchant all-issues export or equivalent readback:
   - `US/en/United States` paid-cohort `Missing age group` remains `0`.
   - `US/es/United States` count is recorded immediately before repair.
3. Product detail readback for at least two affected US/es item IDs:
   - `shopify_US_7227630649441_41872775020641` expected age_group `kids`
   - `shopify_US_7227379023969_41871522431073` expected age_group `adult`
4. Product detail readback for one control sample on source `10627981690` that already has `n:age_group`:
   - `shopify_US_7227254276193_41871113158753` expected age_group `toddler`
5. Source/path readback:
   - Source ID `10627981690`
   - Source name `Shopify App API`
   - Feed label `US`
   - Language `es`
6. Repair payload preview if Candidate A is selected:
   - Exact row count matches approved affected scope.
   - Only `id` and `age_group` columns.
   - All age_group values are one of `newborn`, `infant`, `toddler`, `kids`, `adult`.
   - No custom labels, source URLs, product scope, pricing, shipping, inventory, descriptions, titles, or campaign columns.
7. UI-context proof if Candidate B is selected:
   - Control is source-specific to `10627981690` / `US` / `es`.
   - If the control is account-wide, all-sources, all-products, or ambiguous, stop and do not click it.

## Required Post-Readbacks

After an approved repair:

1. Source/action processing readback:
   - Expected source/action timestamp advanced.
   - No parse errors.
   - For Candidate A, `age_group` / `n:age_group` is recognized.
   - Matched/unmatched counts are recorded.
2. Product detail readback for the two affected samples:
   - `Missing age group` absent.
   - Effective `n:age_group` present with the expected value.
3. Control sample readback:
   - Control item still has `n:age_group`.
   - No unexpected issue introduced.
4. Fresh exact all-issues export or equivalent:
   - Paid-cohort `US/es/United States` `Missing age group` count is `0`, or remaining rows are itemized with a new narrower problem ID.
   - Paid-cohort `US/en/United States` `Missing age group` remains `0`.
5. Label/scope integrity readback:
   - US/en sample still has `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
   - Standard Shopping product scope, feed labels, product groups, budget, bids, status, and conversion goals were not changed.
6. Evidence packet and problem tracker update:
   - Save before/after evidence.
   - Move `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` only when fixed criteria pass.

## Fixed Criteria

This problem is fixed only when:

- Fresh exact product-issues export or equivalent readback shows `0` paid-cohort `US/es/United States` `Missing age group` rows.
- At least two formerly affected US/es product details show effective `n:age_group` and no `Missing age group`.
- Paid-cohort `US/en/United States` remains `0`.
- US/en paid labels and Standard Shopping product scope remain unchanged.
- No Google Ads, Pinterest, Shopify product-data, product-scope, feed-label, product-group, conversion-goal, budget, bid, status, PMax, Standard Shopping, or live-spend change occurred as part of this repair.

## Parallel Lanes To Continue While Approval Is Pending

- Paused non-US Google Search infrastructure approval gate and local validation. Do not duplicate or edit existing US nonbrand campaign `23827590655`.
- Pinterest paused US draft/Event Quality gate using the clean `342`-row EN-US scope and `4` exclusions. Live spend remains separately gated.
- GB/CA visual checkout UI confirmation before spend.
- ROAS/economics guardrail refinement around `$70` AOV, `650%` target ROAS, and CPC/CVR kill rules.
- Claim-safe creative/RSA/Pinterest copy packs without unsupported shipping, inventory, review, bestseller, or promo claims.
- Reporting/readback packet work for campaign and catalog readiness.

## Parent Integration Note

Because this subagent's ownership/write scope was limited to this lane directory, this packet does not update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, or `ops/AGENT_COORDINATION.md`. The parent/orchestrator should integrate this packet into those durable files if this lane becomes the selected approval path.
