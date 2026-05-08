# Problem Tracker

Purpose: track live problems from discovery through attempts, learning, solution, verification, and closure.

Protocol: `ops/PROBLEM_SOLVING_PROTOCOL.md`

## Active Summary

| Problem ID | Priority | Status | Owner | Surface | Current Next Action | Fixed Criteria | Evidence |
|---|---|---|---|---|---|---|---|
| `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` | `P2` | `ACTIVE_DIAGNOSE_READONLY` | Next Merchant/growth agent | Merchant Center `124884876`; paid-cohort item IDs in `US` feed label / `es` language / `United States` country | Read-only identify the `US/es` source/feed path and decide whether a targeted source refresh or US/es supplemental age_group source is the safe fix; do not upload/sync/edit without fresh exact owner approval | Fresh export confirms `0` paid-cohort `US/es` `Missing age group` rows, or the `US/es` surface is proven inactive/excluded from paid serving with no product/feed/conversion changes | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/` |
| `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` | `P1` | `OWNER_APPROVAL_REQUIRED` | Next Pinterest/growth agent | Pinterest advertiser `549756244483`; event quality and campaign readiness | Get exact owner approval for a paused US-only draft using the clean `342`-row scope / `4` exclusions, or approve a narrow event-quality repair path; do not add duplicate tracking blindly | Event Quality improves or owner-approved paused draft proceeds with documented `Fair` risk and no duplicate tag/CAPI regression; live spend remains separately gated | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/` and `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-orchestrated-safe-advance/lanes/pinterest/` |

## Recently Solved

| Problem ID | Priority | Status | Closed | Surface | Result | Evidence |
|---|---|---|---|---|---|---|
| `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT` | `P1` | `SOLVED_READBACK_PASSED_US_EN` | 2026-05-08 | Merchant Center `124884876`; paid-cohort US/en `Missing age group` diagnostics | Fresh read-only product-issues export downloaded and reconciled; paid-cohort `US` / `en` / `United States` `Missing age group` count is `0`, down from prior exact `623` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/` |
| `PROB-2026-05-08-MERCHANT-LOCAL-INVENTORY` | `P0` | `SOLVED_READBACK_PASSED` | 2026-05-08 | Merchant Center `124884876`; physical-store local inventory diagnostics | Removed active physical-store `Local inventory ads` add-on; `Free local listings` was already inactive; diagnostics showed `Great, all your prioritized fixes are resolved` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-local-inventory-addons-removal/MERCHANT_LOCAL_INVENTORY_ADDONS_REMOVAL_REPORT.md` |
| `PROB-2026-05-08-PINTEREST-CATALOG-337-346` | `P1` | `SUPERSEDED_BY_SAFER_PATH` | 2026-05-08 | Pinterest EN-US catalog proof for US paused draft scope | Re-resolved 5 stale rows, built clean 342-row scope, excluded 4 unresolved variants | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md` |

## Detailed Problem Records

### `PROB-2026-05-08-MERCHANT-AGE-GROUP-EXACT-EXPORT`

Priority: `P1`

Status: `SOLVED_READBACK_PASSED_US_EN`

Owner/session: Codex current session, 2026-05-08.

Surface: Merchant Center account `124884876`; paid-cohort US/en products; source `Shopify App API`; dedicated supplemental source `upload_paid_cohort_age_group_only.txt` / source `10651516446`.

Exact symptom:
- Merchant paid-cohort `Missing age group` had previously remained at `623` rows after Shopify-side variant metafield repair.
- Later source/sample readback improved materially, but exact CSV export did not materialize in the latest run.

Business impact:
- Paid growth is less clean while Merchant diagnostics may still contain old age-group issues.
- This should not freeze other lanes, but it must be verified to completion.

Definition of fixed:
- A fresh exact product-issues export/API readback confirms `0` paid-cohort US/en `Missing age group` rows, or any remaining rows are isolated to known unmatched/deleted/offline offers and have a concrete repair/ignore reason.

Attempt log:

| Time | Attempt | Result | Evidence |
|---|---|---|---|
| 2026-05-07 | Shopify ProductVariant `mm-google-shopping.age_group` repair for all `780` paid-cohort variants | Shopify readback/dry-run showed all `780` already correct, but Merchant diagnostics remained stale | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-merchant-feed-refresh-age-group-recheck/` |
| 2026-05-08 | Source-refresh path/readback after owner-approved Merchant source-refresh solution | Sample US/en timestamp advanced to `2026-05-08T05:55:06+00:00`; sample no longer showed `Missing age group` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-source-refresh-approved-action/` |
| 2026-05-08 | Dedicated age_group-only source readback | Source existed, last updated `May 8, 2026 1:55 AM`, `780` updated products, `771` matched, `9` `Offer does not exist`, attributes recognized | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-dedicated-supplemental-repair/` |
| 2026-05-08 | Exact product-issues CSV download attempt | Download did not materialize; do not treat this as solved mathematically until a later export/API readback confirms | Worklog anchor `2026-05-08-merchant-source-refresh-approved-action` |
| 2026-05-08 02:36 EDT | `DLM-MERCHANT-US-ExactExportVerifier` local artifact audit | No current exact count found. Latest exact CSVs are stale May 7 exports with `623` paid-cohort US/en `Missing age group` IDs; May 8 post-refresh folder has no product_issues CSV; source/sample/visible diagnostics improved; API probes remain blocked by insufficient local OAuth scopes | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-orchestrated-safe-advance/lanes/merchant/MERCHANT_AGE_GROUP_EXACT_EXPORT_VERIFICATION_PATH.md` |
| 2026-05-08 02:51 EDT | Read-only Merchant exact export retry on prioritized/all diagnostics URLs | Merchant showed `Great, all your prioritized fixes are resolved`; no CSV downloaded because the full product-issues table/export was hidden behind the read-only `View all issues` control | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/raw/product-issues-browser-export/download_attempt_summary_priority.json` |
| 2026-05-08 02:52 EDT | Read-only Merchant exact export after clicking only `View all issues`, then the product-issues download button and ready-download notification | Export downloaded as `product_issues_2026-05-08_01-58-05.csv` with `33,620` rows. Reconciliation against the `780` paid-cohort IDs showed paid-cohort `US` / `en` / `United States` `Missing age group` count `0`, delta `-623`; sample item no longer affected | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-summary-2026-05-08-0252.json` |
| 2026-05-08 02:53 EDT | Context breakdown of remaining paid item-ID age_group rows | Remaining paid item-ID age_group rows are `625` unique item IDs / `1,250` rows only in `US` feed label, `es` language, `United States`, split `625` Shopping ads and `625` Free listings. Opened new follow-up `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`; do not confuse it with the solved US/en blocker | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json` |

Failed or ruled-out paths:
- Repeating Shopify age_group edits is ruled out unless fresh readback proves a regressed Shopify value.
- Blind source refresh/re-upload loops are ruled out.
- Local inventory fixes are unrelated to age_group and must not be mixed into this problem.
- The remaining `US/es` age_group rows are a separate follow-up problem, not evidence that the old `US/en` blocker remains.

Current next action:
- Closed for the original US/en paid-growth gate. Continue the separate `US/es` read-only diagnosis in `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`.

Approval/credential/platform gates:
- Merchant API/Content API product-issues path has previously failed with insufficient OAuth scopes.
- Any Merchant source refresh, supplemental upload, feed/source edit, Shopify product data edit, product-scope/feed-label/product-group change, or Ads/Pinterest spend work still requires fresh exact owner approval.

Parallel work to continue:
- Paused Google Search infrastructure, Pinterest paused drafts/gates, localization QA, ROAS guardrails, creative packs, and reporting readbacks.

### `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Priority: `P2`

Status: `ACTIVE_DIAGNOSE_READONLY`

Owner/session: Next Merchant/growth agent.

Surface: Merchant Center account `124884876`; paid-cohort item IDs in feed label `US`, language `es`, country `United States`.

Exact symptom:
- The 2026-05-08 exact product-issues export shows the original paid-cohort `US/en/United States` `Missing age group` count is `0`.
- The same export still shows `625` paid-cohort item IDs with `Missing age group` only in `US/es/United States`, duplicated across `Shopping ads` and `Free listings` for `1,250` rows.

Business impact:
- This does not reopen the solved US/en Standard Shopping blocker, but it could affect Spanish-language US Shopping/free-listing eligibility or future Spanish-language paid tests.

Definition of fixed:
- A fresh exact export confirms `0` paid-cohort `US/es/United States` `Missing age group` rows, or the `US/es` surface is proven inactive/excluded from paid serving with no product/feed/conversion changes.

Attempt log:

| Time | Attempt | Result | Evidence |
|---|---|---|---|
| 2026-05-08 02:52 EDT | Exact product-issues export context reconciliation | `625` paid item IDs / `1,250` rows remain only in `US/es/United States`; `US/en/United States` is `0` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json` |
| 2026-05-08 02:53 EDT | Read-only sample source/label probe for affected item `shopify_US_7227630649441_41872775020641` | Script exposed the US/en `Shopify App API` row with timestamp `2026-05-08T05:55:06+00:00` and clean labels, but did not expose the US/es source row; more targeted US/es source readback is needed | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/raw/browser-source-readback-us-es-sample/merchant_exact_label_readback_refresh_check.json` |

Failed or ruled-out paths:
- Repeating Shopify `mm-google-shopping.age_group` edits is ruled out unless a fresh Shopify readback proves regression.
- Blind Merchant source refresh, supplemental upload, feed/source edit, product-scope/feed-label/product-group change, or Shopify product edit is ruled out without fresh exact owner approval.
- Local inventory fixes are unrelated and must not be mixed into this issue.

Current next action:
- Read-only identify the US/es Merchant source/feed path and whether a targeted US/es source refresh or supplemental age_group source is the safe fix.
- If a live fix is needed, prepare exact owner approval wording before any upload/sync/edit.

Approval/credential/platform gates:
- Merchant source refresh/sync, supplemental upload, feed/source edit, Shopify product-data edit, Google Ads product-scope/feed-label/product-group/conversion-goal change, and any spend/enablement require fresh exact owner approval.
- API product-status diagnostics still require properly scoped read-only Merchant credentials outside the repo if browser export/source readback is insufficient.

Parallel work to continue:
- Owner-approved paused non-US Google Search shell build or owner-approved paused Pinterest US draft build, plus GB/CA/AU no-payment checkout QA and ROAS/creative/reporting work.

### `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Priority: `P1`

Status: `OWNER_APPROVAL_REQUIRED`

Owner/session: Next Pinterest/growth agent.

Surface: Pinterest advertiser `549756244483`; official Shopify Pinterest app pixel/CAPI; Event Quality; paused campaign/draft readiness.

Exact symptom:
- Pinterest Event Quality reads `Fair`.
- API proof shows official Tag and CAPI are alive, but gaps remain around click ID, product ID in AddPaymentInfo, and email in AddToCart.

Business impact:
- Pinterest spend should remain gated or explicitly accepted with risk until measurement quality is understood.

Definition of fixed:
- Event Quality improves after platform/app refresh and traffic, or owner approves a specific path: paused US draft creation with `Fair` risk documented, or a narrow tracking repair that avoids duplicate tags/CAPI.

Attempt log:

| Time | Attempt | Result | Evidence |
|---|---|---|---|
| 2026-05-06 | Official Shopify Pinterest pixel set to `Always on` / share all events | Checkout diagnostic showed official Pinterest event emitted successfully and blocked events count dropped to `0` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-pinterest-event-quality-fix/` |
| 2026-05-08 | Fresh Pinterest API/readback | Tag and CAPI timestamps were fresh; Event Quality still `Fair`; Verified Merchant and Automatic Enhanced Match passed; Enhanced Match error remained | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/` |
| 2026-05-08 | Catalog proof repair | Old `337/346` blocker superseded by clean `342`-row scope and 4 exclusions | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/` |
| 2026-05-08 02:40 EDT | `DLM-PINTEREST-EventCatalog-DraftGate` local gate audit | Verified older `337` resolved / `9` excluded draft solution is superseded by clean `342` resolved / `4` excluded scope. Exact paused-draft approval wording prepared; Event Quality `Fair` remains a live-spend gate, not a blocker to approved paused draft creation | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-orchestrated-safe-advance/lanes/pinterest/PINTEREST_342_SCOPE_DRAFT_GATE.md` |

Failed or ruled-out paths:
- Adding duplicate theme-level Pinterest tag or custom CAPI is ruled out without exact approval because it risks duplicate tracking and PII/credential handling.
- Waiting passively for `Fair` to become `Good` is not a solution by itself; if waiting is chosen, it needs a timed readback and a parallel draft/repair lane.

Current next action:
- Either request owner approval to create paused US-only Pinterest catalog/retargeting drafts using the proven `342`-row scope and excluding the `4` unresolved variants, or request approval for a narrow event-quality repair plan.

Approval/credential/platform gates:
- Live Pinterest draft/campaign/product-group/budget/bid/tag/CAPI writes require exact owner approval.
- Custom CAPI would require token/secret handling outside repo and a separate privacy-safe implementation plan.

Parallel work to continue:
- Google Search paused infrastructure, Merchant exact age_group verification, localization QA, ROAS/economics, creative packs, and reporting.

### `PROB-2026-05-08-MERCHANT-LOCAL-INVENTORY`

Priority: `P0`

Status: `SOLVED_READBACK_PASSED`

Owner/session: Codex, 2026-05-08.

Surface: Merchant Center account `124884876`; physical-store local inventory diagnostics.

Exact symptom:
- Merchant showed `Missing local inventory data` / `Missing inventory data for products in your physical stores` even though Dress Like Mommy has no physical store and uses dropshipping.

Business impact:
- Misleading physical-store diagnostic could lead agents into the wrong fix: creating local inventory, pickup, warehouse, or on-hand stock claims.

Definition of fixed:
- Physical-store local inventory add-ons disabled/removed, no local inventory claims created, diagnostics readback clears prioritized issue.

Attempt log:

| Time | Attempt | Result | Evidence |
|---|---|---|---|
| 2026-05-08 | Readback Merchant issue panel and add-ons | Issue panel stated no-physical-store fix was removing local add-ons; `Local inventory ads` was active, physical-store `Free local listings` was inactive | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-local-inventory-addons-removal/` |
| 2026-05-08 | Removed only active physical-store `Local inventory ads` add-on | After readback, both local add-ons showed as `Add`; neither appeared in `Your add-ons` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-local-inventory-addons-removal/` |
| 2026-05-08 | Diagnostics readback | Merchant showed `Great, all your prioritized fixes are resolved` | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-local-inventory-addons-removal/MERCHANT_LOCAL_INVENTORY_ADDONS_REMOVAL_REPORT.md` |

Failed or ruled-out paths:
- Creating local inventory feeds/store codes/pickup/local stock claims was ruled out because the business has no physical store.
- Product data edits were ruled out because the issue was a physical-store add-on problem.

Current next action:
- If cached Merchant screens still show the issue, recheck after refresh; do not create local inventory data.

Approval/credential/platform gates:
- None for the completed fix.

Parallel work to continue:
- Other paid-growth lanes.

## New Problem Template

Copy this template for every new problem:

```markdown
### `PROB-YYYY-MM-DD-SHORT-NAME`

Priority: `P1`

Status: `ACTIVE_SOLVING`

Owner/session:

Surface:

Exact symptom:

Business impact:

Definition of fixed:

Attempt log:

| Time | Attempt | Result | Evidence |
|---|---|---|---|
| YYYY-MM-DD HH:MM TZ |  |  |  |

Failed or ruled-out paths:

Current next action:

Approval/credential/platform gates:

Parallel work to continue:
```
