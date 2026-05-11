# 2026-05-10 Paid Growth Orchestrator Deep Follow-Up Packet

Purpose: continue the Dress Like Mommy paid-growth sprint as parent/orchestrator from `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-orchestrator-safe-resume`. This packet does NOT duplicate the prior orchestrator-safe-resume packet; it advances five disjoint follow-up lanes that the prior packet did not cover, so the next browser-enabled session can paste-execute apply, pre-enable measurement gates, Pinterest Event Quality repair, native-language review, and the very first non-US live enable.

Operating prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

Scope and constraints:
- This Cowork session has file/bash/Agent-subagent tools but no logged-in Google Ads / Merchant Center / Pinterest / Shopify Admin browser access. Per the canonical operating prompt's non-blocking execution rule, the parent stated this clearly and ran disjoint local read-only lanes in parallel rather than freezing the sprint.
- Standing guardrails preserved: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, no Shopify live product-data changes, no Pinterest live writes, no theme edits, no checkout payment, no order submission, no CAPTCHA/verification bypass, no credential changes.
- Goal of this packet: produce paste-ready operator artifacts that close the gap between the existing safe-resume strategy and the very first live action (per-country apply playbook, measurement gap audit, Pinterest Event Quality repair plan, native-language review checklist, and the GB first-enable runbook).

Lane index:

| Lane | Subagent | Scope | Output |
|---|---|---|---|
| A | Ads-apply-playbook | Per-country paste-ready apply playbook for the 8 unresolved paused Search countries (PL, CZ, RO, PT, GR, IT, FR, BE) with row counts, currency/budget read directly from the held CSVs, RPC readback targets, per-country preflight, and rollback procedure. | `lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md` |
| B | Measurement-conversion-gap | Audit of the cross-market conversion goal inheritance (US `Account-default: Purchases` applied to 9 non-US Search campaigns), GA4/Tag readbacks needed before any non-US enable, currency presentment risk on the `purchase` event, Pinterest Tag/CAPI dedupe state, and pre-enable measurement gate checklist. | `lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md` |
| C | Pinterest-event-quality-fix-plan | Concrete actionable plan to lift Pinterest Event Quality from `Fair` to `Good`. Maps each gap (Product ID in AddPaymentInfo, Email in AddToCart, Click ID in Checkout, Enhanced Match ERROR) to category (Shopify Pinterest official app vs Pinterest dashboard vs theme vs volume-gated), with two distinct exact-quote owner-approval phrases. | `lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md` |
| D | Native-language-review-checklist | Reviewer-facing checklist for the 14 native-language copy locale variants. Per-locale reviewer brief covering dialect, brand voice, forbidden claims, locale-specific gotchas, landing-language QA spot-checks, and recruitment options. Recommended staging order. | `lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md` |
| E | First-enable-runbook | Operator runbook for the very first non-US live enable: GB campaign `23838895360` / ad group `Mommy & Me Dresses - Exact`. Pre-enable gate checklist, exact owner-approval phrase verbatim, apply-time runbook, 24h/72h/7d review cadence, kill thresholds, rollback, and forward escalation path to CA, AU. | `lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md` |

Guardrails preserved by every lane:
- No live spend.
- No campaign enablement.
- No budget/bid/status changes.
- No PMax enable.
- No Standard Shopping changes.
- No product-scope/feed-label/product-group changes.
- No conversion-goal changes.
- No Merchant uploads.
- No Shopify live product-data changes.
- No Pinterest live writes.
- No theme edits or live theme pushes.
- No checkout payment or order submission.
- No CAPTCHA/verification bypass.
- No credential changes or account-billing actions.
- No browser/account access of any kind in this session.

Final integration: parent/orchestrator updates `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and `ops/AGENT_COORDINATION.md` with the new `AGENT_CONTINUITY_ANCHOR`. The canonical paid-growth prompt continues to be the single owner-standard prompt; only its embedded "current state to preserve" section is touched (anchor pointer + new evidence packet path) without creating a competing prompt.
