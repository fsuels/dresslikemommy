# Ads Branch Decision

Date: 2026-05-10

Scope: local-only decision support for the parent/orchestrator. No browser, Google Ads, network, live account, tracker, worklog, coordination, script, prompt, theme, Merchant, Shopify, Pinterest, GA4/GTM, budget, bid, status, conversion, payment, order, or other file write was made.

## Current True Ads State

The current non-US Search infrastructure state is `12 built / 3 absent / 2 parked`.

Built, read back clean, and still paused:

| Country | Campaign ID | Budget | State |
|---|---:|---:|---|
| `GB` | `23838895360` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `CA` | `23834423669` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `AU` | `23834424182` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `CH` | `23834425358` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `DK` | `23838969244` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `DE` | `23834427575` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `NL` | `23829110118` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `SE` | `23838970036` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `ES` | `23829133584` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `IT` | `23829232530` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |
| `PL` | `23829238698` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |
| `CZ` | `23829253812` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |

Absent/uncreated:

- `RO`
- `PT`
- `GR`

Parked:

- `FR`: requires a fresh non-stale completed `88/88 # OK` preview plus no-duplicate readback.
- `BE`: remains last after Google Ads upload-throttle cooldown and no in-progress upload/apply row.

Do not use `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/` as current Ads state. It predates `IT`, `PL`, and `CZ` completion and the later `RO` stale/not-visible recheck.

## Why RO/PT/GR Cannot Proceed Yet

The broad paused non-US Google Search `TEST BUILD` approval was already given on 2026-05-10, so the parent should not request that same broad approval again. The current blocker is narrower: the next Ads branch is ambiguous after the `RO` path failed to resolve cleanly.

Evidence says:

- `RO` pre-apply readback was absent.
- `RO` preview initially remained in progress with `Error count 0`.
- A later existing-preview recheck returned `PREVIEW_IN_PROGRESS_ERROR_0`.
- A reload plus 90-second poll then returned `PREVIEW_FILE_NOT_VISIBLE` for `RO_intl_search_paused_draft_web_bulk.csv`.
- Fresh RPC absent readbacks found `RO`, `PT`, and `GR` all `found=false`.
- `PT` and `GR` were intentionally not attempted because the one-country-at-a-time guard blocks stacking new uploads behind unresolved `RO`.

That leaves two valid paths, and neither is implied by the old approval:

1. Retry `RO` with a fresh one-country preview after confirming no in-progress row and no RO campaign.
2. Skip/park `RO` and continue one country at a time with `PT`, then `GR`.

Because those paths have different business/coverage consequences, the parent needs fresh owner branch direction before touching Google Ads.

## Latest User Message Approval Check

The latest user message does **not** contain enough exact approval to retry `RO` or skip `RO`.

It explicitly scopes this worker to local-only reporting, says no external browser, no Google Ads, no network, and no live writes, and gives ownership only of this file. It is a request for decision support, not action-time approval for either branch.

## Exact Approval Options

Recommended Option A: retry `RO` once with a clean new one-country path.

`APPROVE RETRY RO PAUSED GOOGLE SEARCH TEST BUILD ONLY: FIRST CONFIRM NO RO CAMPAIGN EXISTS AND NO RO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN UPLOAD ONLY RO_intl_search_paused_draft_web_bulk.csv, PREVIEW, DOWNLOAD, AND VALIDATE 88/88 # OK; APPLY ONLY IF CLEAN; READ BACK THE RO CAMPAIGN AS PAUSED SEARCH, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH PT, GR, FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

Option B: skip/park `RO` and continue with `PT`, then `GR`.

`APPROVE SKIP RO FOR NOW AND CONTINUE PAUSED GOOGLE SEARCH TEST BUILD WITH PT THEN GR ONLY: KEEP RO ABSENT/PARKED; FIRST CONFIRM NO PT/GR CAMPAIGN EXISTS AND NO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN PROCESS PT ONE COUNTRY AT A TIME, AND ONLY AFTER PT READBACK PASSES PROCESS GR; PREVIEW, DOWNLOAD, VALIDATE 88/88 # OK BEFORE APPLYING EACH; KEEP ALL NEW CAMPAIGNS/AD GROUPS/KEYWORDS/ADS PAUSED, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

Later, separate options:

- `FR` should remain parked until a fresh non-stale completed `88/88 # OK` preview plus no-duplicate readback exists.
- `BE` should remain last until upload-throttle cooldown and no in-progress upload/apply row are confirmed.

## Recommendation

Ask the owner for one of the two exact branch approvals above. I recommend Option A first: retry `RO` once through a fresh one-country preview after no-in-progress/no-campaign readback, because it preserves the intended approved country set and keeps the one-country control discipline intact. If `RO` stalls, errors, disappears again, or fails readback, park it with evidence and use Option B only after the owner gives the skip wording.

Before any non-US enablement, keep `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` open until the purchase-event currency/value path is proven.

## Evidence Read

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md`
- `ops/AGENT_COORDINATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/lanes/ads-current-state-decision/ADS_CURRENT_STATE_DECISION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/PAID_GROWTH_GOAL_ORCHESTRATED_FOLLOWUP_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/PAID_GROWTH_RO_PT_GR_SEARCH_CONTINUATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/ro/RO_PREVIEW_RECHECK_ATTEMPTS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/RO_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/PT_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/GR_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/csv-guardrail-revalidation/CSV_GUARDRAIL_REVALIDATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-cz-ro-pt-gr-paused-search-build/PAID_GROWTH_CZ_RO_PT_GR_PAUSED_SEARCH_BUILD_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/PAID_GROWTH_BROWSER_RECOVERY_AND_REMAINING_SEARCH_PREFLIGHT_REPORT.md`
