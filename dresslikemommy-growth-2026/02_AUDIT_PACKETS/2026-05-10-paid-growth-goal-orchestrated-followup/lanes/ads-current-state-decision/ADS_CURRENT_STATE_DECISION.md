# Ads Current State Decision

Date: 2026-05-10

Scope: Worker A local reconciliation only. No Google Ads, browser, API, tracker, worklog, coordination, Merchant, Shopify, Pinterest, theme, or measurement writes were made.

## Executive State

The correct current Google Ads non-US Search infrastructure state is:

- Built/read back clean: 12 paused non-US Search campaigns.
- Absent/uncreated: `RO`, `PT`, `GR`.
- Parked: `FR`, `BE`.
- Live spend/enablement: none.

The current durable anchor is `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-ro-parked-preview-not-visible`.

Do not use the older `2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight` packet as the current Ads state. It contains stale claims from before `IT`, `PL`, and `CZ` were completed and before `RO` was rechecked/parked as stale-not-visible.

## Current Campaign List

| Country | Current state | Campaign ID | Budget | Required interpretation |
|---|---:|---:|---:|---|
| `GB` | Built/read back clean | `23838895360` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `CA` | Built/read back clean | `23834423669` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `AU` | Built/read back clean | `23834424182` | `$2/day` | Paused Search, presence-only, content/YouTube off |
| `CH` | Built/read back clean | `23834425358` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `DK` | Built/read back clean | `23838969244` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `DE` | Built/read back clean | `23834427575` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `NL` | Built/read back clean | `23829110118` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `SE` | Built/read back clean | `23838970036` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `ES` | Built/read back clean | `23829133584` | `$1/day` | Paused Search, presence-only, content/YouTube off |
| `IT` | Built/read back clean | `23829232530` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |
| `PL` | Built/read back clean | `23829238698` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |
| `CZ` | Built/read back clean | `23829253812` | `$1/day` | Paused Search, presence-only after narrow repair, content/YouTube off |
| `RO` | Absent/uncreated; parked after stale/not-visible preview | none | n/a | Fresh owner direction required before retrying or skipping |
| `PT` | Absent/uncreated; unattempted after RO parked | none | n/a | Fresh owner direction required if continuing after/around RO |
| `GR` | Absent/uncreated; unattempted after RO parked | none | n/a | Fresh owner direction required if continuing after/around RO |
| `FR` | Parked | none | n/a | Requires fresh non-stale completed `88/88 # OK` preview plus no-duplicate readback |
| `BE` | Parked | none | n/a | Retry only after upload-throttle cooldown and no in-progress upload row |

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/PAID_GROWTH_BROWSER_RECOVERY_AND_REMAINING_SEARCH_PREFLIGHT_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-cz-ro-pt-gr-paused-search-build/PAID_GROWTH_CZ_RO_PT_GR_PAUSED_SEARCH_BUILD_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/PAID_GROWTH_RO_PT_GR_SEARCH_CONTINUATION_REPORT.md`
- `ops/AGENT_WORKLOG.md`
- `ops/AGENT_COORDINATION.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`

## What The Stale Decision Pack Got Wrong

The packet `2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/` is not current for Ads state.

Stale claims to avoid:

- It says only 9 of 17 non-US Search countries were created and that `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR` were still unresolved/absent. Later evidence supersedes this: `IT`, `PL`, and `CZ` are now built/read back clean, moving the state to 12 of 17.
- It suggests a resume order of `PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE`. That is obsolete. `PL`, `CZ`, and `IT` are already complete and must not be re-uploaded.
- It describes `IT` as a pending/in-progress preview decision. Later browser recovery applied and read back `IT` clean as campaign `23829232530`.
- It describes `PL` as a future fresh upload. Later browser recovery applied and read back `PL` clean as campaign `23829238698`.
- It describes `CZ` as not yet built. Later CZ/RO/PT/GR build work applied and read back `CZ` clean as campaign `23829253812`.
- It does not include the later `RO` result: immediate recheck was `PREVIEW_IN_PROGRESS_ERROR_0`, then reload plus 90-second poll returned `PREVIEW_FILE_NOT_VISIBLE`, and RPC readbacks found `RO`, `PT`, and `GR` absent.

The stale packet can remain useful only as historical context for why a decision artifact existed. It should not be used to pick the next Ads action.

Stale packet paths inspected:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/owner-decision-pack/OWNER_DECISION_PACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/browser-readback-bulk-uploads/BROWSER_READBACK_BULK_UPLOADS.md`

## Current Next Ads Options

The broad paused non-US Search `TEST BUILD` approval was already given on 2026-05-10. However, because the current `RO` path ended in a stale/not-visible preview, the next Ads action needs fresh owner direction for which branch to take.

Option A: retry `RO`.

- Before upload: confirm no `RO` campaign exists and no `RO` bulk-upload preview/apply is in progress.
- Upload only `RO_intl_search_paused_draft_web_bulk.csv`.
- Preview, download, and validate exactly `88/88 # OK`.
- Apply only if clean.
- Read back `RO` as paused Search, presence-only, content/YouTube off, CPC at or below `$0.20`.
- Do not touch `PT`, `GR`, `FR`, or `BE` until `RO` completes cleanly or is parked again.

Owner direction required:

`APPROVE RETRY RO PAUSED GOOGLE SEARCH TEST BUILD ONLY: FIRST CONFIRM NO RO CAMPAIGN EXISTS AND NO RO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN UPLOAD ONLY RO_intl_search_paused_draft_web_bulk.csv, PREVIEW, DOWNLOAD, AND VALIDATE 88/88 # OK; APPLY ONLY IF CLEAN; READ BACK THE RO CAMPAIGN AS PAUSED SEARCH, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH PT, GR, FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

Option B: skip/park `RO` and proceed with `PT`, then `GR`.

- Keep `RO` absent/parked.
- Confirm no `PT`/`GR` campaign exists and no bulk-upload preview/apply is in progress.
- Process `PT` one country at a time.
- Only after `PT` readback passes, process `GR`.
- For each: preview, download, validate exactly `88/88 # OK`, apply only if clean, then read back paused Search/presence-only/content-off/YouTube-off/CPC <= `$0.20`.

Owner direction required:

`APPROVE SKIP RO FOR NOW AND CONTINUE PAUSED GOOGLE SEARCH TEST BUILD WITH PT THEN GR ONLY: KEEP RO ABSENT/PARKED; FIRST CONFIRM NO PT/GR CAMPAIGN EXISTS AND NO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN PROCESS PT ONE COUNTRY AT A TIME, AND ONLY AFTER PT READBACK PASSES PROCESS GR; PREVIEW, DOWNLOAD, VALIDATE 88/88 # OK BEFORE APPLYING EACH; KEEP ALL NEW CAMPAIGNS/AD GROUPS/KEYWORDS/ADS PAUSED, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

Option C: handle `FR` later.

- `FR` remains parked.
- Do not use stale/inherited rows.
- Next `FR` action must start with fresh no-duplicate readback, then a fresh non-stale completed preview validating `88/88 # OK`, then apply/readback only if clean.
- Owner direction should explicitly name `FR` if choosing this path.

Option D: handle `BE` last.

- `BE` remains parked after the Google Ads upload throttle.
- Wait for throttle cooldown and confirm no in-progress upload/apply row.
- Use a fresh one-country upload only; do not apply an old throttled row.
- Owner direction should explicitly name `BE` if choosing this path.

## Blocked Or Prohibited Actions

Do not:

- Re-upload or re-apply completed countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Apply stale pending rows or any row that is not a fresh validated `88/88 # OK`.
- Apply, discard, upload, retry, or sequence `RO`/`PT`/`GR`/`FR`/`BE` without fresh owner direction for the branch being taken.
- Enable campaigns, ad groups, ads, or keywords.
- Start live spend.
- Change budgets, bids, campaign status, conversion goals, product scope, feed labels, product groups, or Merchant/feed data.
- Touch US campaign `23827590655`.
- Touch Standard Shopping, PMax, Brand Search, Remarketing, Merchant, Shopify product data, Pinterest, theme files, GA4/GTM, account/billing, credentials, checkout payment, orders, refunds, or CAPTCHA/verification flows.
- Treat cart/checkout currency evidence as proof of non-US `purchase` event value/currency. `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` remains open before any non-US enablement.

## Evidence Details

Key current-state reports:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/PAID_GROWTH_RO_PT_GR_SEARCH_CONTINUATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/ro/RO_PREVIEW_RECHECK_ATTEMPTS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/ro/existing_preview_recheck_status.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/RO_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/PT_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/campaign-absent-readbacks/GR_campaign_rpc/initial_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/csv-guardrail-revalidation/CSV_GUARDRAIL_REVALIDATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/measurement-gate-recheck/PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-cz-ro-pt-gr-paused-search-build/PAID_GROWTH_CZ_RO_PT_GR_PAUSED_SEARCH_BUILD_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/PAID_GROWTH_BROWSER_RECOVERY_AND_REMAINING_SEARCH_PREFLIGHT_REPORT.md`

Prior built-campaign evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/raw/remaining-readback/IT_campaign_rpc/final_validated_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/raw/remaining-readback/PL_campaign_rpc/final_validated_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/after-readbacks/CZ_campaign_rpc/final_validated_summary.json`

Stale/reference-only packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/owner-decision-pack/OWNER_DECISION_PACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/browser-readback-bulk-uploads/BROWSER_READBACK_BULK_UPLOADS.md`

## Final Worker A Conclusion

Current correct Ads state is `12 built / 3 absent / 2 parked`:

- Built: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Absent: `RO`, `PT`, `GR`.
- Parked: `FR`, `BE`.

The next owner decision is not "continue from PL" and not "apply old IT/FR rows." It is whether to retry `RO` with a fresh one-country preview after no-in-progress/no-campaign readback, or skip/park `RO` and proceed `PT` then `GR` one at a time. `FR` and `BE` remain later, separately gated work.
