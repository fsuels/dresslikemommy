# North Star Lane Board

Generated: 2026-05-10
Scope: local-only synthesis for the parent/orchestrator after the measurement and Ads branch gates. Source files read: `ops/GROWTH_NORTH_STAR.md`, `ops/PROBLEM_TRACKER.md`, and latest `ops/AGENT_WORKLOG.md` entries.

## Current Frame

The North Star is not more traffic by itself. It is a controlled paid-growth machine that increases sales and profit, keeps ROAS disciplined around the owner's target, avoids wasted clicks, proves measurement before scaling, and uses parallel lanes without conflicting writes.

Current guardrail posture:

- Allowed now: local analysis, read-only packet prep, browser/read-only account checks by the parent when available, and owner-approved paused-build only.
- Not allowed by inference: live spend, campaign enablement, budget increases, product-scope/feed-label/product-group changes, conversion-goal changes, PMax or remarketing enablement, Merchant uploads, Pinterest live writes, Shopify product-data/theme writes, checkout payment, order, refund, cancelation, credential changes, or destructive filesystem actions.
- Non-US live-spend-ready markets remain `0` until the purchase-event currency/value measurement gate is closed or explicitly accepted by the owner.

## Moving / Done

| Lane | State | Parent meaning |
|---|---|---|
| North Star operating model | Done and current | Growth work should keep moving toward trusted measurement, healthy catalog, conversion-ready pages, controlled Google/Pinterest infrastructure, explicit economics, and coordinated parallel agents. |
| Paused non-US Search infrastructure | `12` campaigns built and read back clean | `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, and `CZ` exist as paused Search campaigns, presence-only, content/YouTube off, no live spend. Do not re-upload these countries. |
| Ads CSV guardrails | Moving | Remaining split files for unresolved countries have repeatedly passed local guardrails: paused statuses, low CPC controls, no protected-campaign rows, and no stale beach URL rows. |
| Measurement gate definition | Done, still open | The exact gap is clear: storefront/cart/checkout currency proof does not prove the official Shopify Google & YouTube app's non-US `purchase` event currency/value on thank-you/order-status. |
| Merchant US/en age_group | Solved | Paid-cohort `US` / `en` `Missing age group` count is `0`; do not redo Shopify age_group edits or blind source refreshes. |
| Localized storefront readiness | Mostly solved for paused infrastructure | Shipping clarity, localized pages, checkout-to-shipping QA, collection grids, and localized PDP size charts have recent solved readbacks. These support paused infrastructure, not live spend by themselves. |
| Beach URL mitigation | Local mitigation done | Ads held packet removed all Vacation Family rows tied to the stale beach/Christmas metadata handle; Shopify SEO/social repair remains approval-gated. |
| First-enable scorecard | Local artifact exists | Latest packet has a first-enable/economics scorecard and weekly scorecard template. It is planning evidence only, not approval to enable. |

## Active Solving

| Lane | Status | Next safe motion |
|---|---|---|
| Non-US purchase currency/value measurement | `OWNER_APPROVAL_REQUIRED_FOR_PURCHASE_EVENT_PROOF` | Parent should run browser-enabled Tag Assistant, GA4 DebugView/Realtime, and Google Ads readbacks if available. If no genuine non-US purchase can prove the path, request exact owner approval for one controlled low-value test purchase/refund/cancel procedure. |
| Ads branch after `RO` preview failure | `PARTIAL_12_APPLIED_RO_STALE_PREVIEW_NOT_VISIBLE_PT_GR_ABSENT_FR_STALE_PREVIEW_BE_THROTTLE` | Parent needs fresh owner direction: retry `RO` with a new one-country preview after no-in-progress/no-campaign readback, or skip/park `RO` and continue one country at a time with `PT`, then `GR`. |
| `FR` and `BE` paused Search | Parked | `FR` needs a fresh non-stale completed `88/88 # OK` preview and no-duplicate readback. `BE` remains last after upload-throttle cooldown. |
| Native-language copy gate | `PARTIALLY_MITIGATED_LOCAL_OPTIONS_READY__OWNER_DECISION_REQUIRED` | Decide whether first paused builds stay English-first, use reviewed localized copy, or stage localized copy as a second build. No Ads import/edit without exact approval. |
| Merchant / Pinterest / beach gates | Consolidated, not fixed live | Keep approval-ready packets current. Do not perform Merchant source repair, Pinterest paused draft/live write, or Shopify SEO/social metadata edit without exact owner approval. |

## Waiting Approval

| Gate | Approval needed |
|---|---|
| Controlled non-US purchase proof | Exact owner approval if Tag Assistant/GA4/Ads cannot prove purchase currency/value without a real transaction. |
| Ads branch decision | Fresh owner direction to retry `RO` or skip/park `RO` before moving to `PT` and `GR`; this is distinct from the already-granted broad paused TEST BUILD approval. |
| First non-US enable | Exact action-time approval after measurement proof, with market/ad group/budget/bid/runbook named. Current local recommendation path has been GB / exact-only style, but approval is still required. |
| Merchant US/es age_group | Exact approval for narrow repair of source `10627981690`, preferred age_group-only supplemental path after preview. |
| Pinterest Event Quality / paused draft | Exact approval for a paused US-only draft using the clean `342`-row scope, or a narrow event-quality repair path. |
| Beach product SEO/social metadata | Exact approval for narrow Shopify metadata repair before any paid traffic uses that handle again. |
| Native-language copy direction | Owner decision on English-first vs localized/native reviewed copy before future native-language imports. |

## Platform / Credential Pending

| Surface | Blocker |
|---|---|
| GA4 / Tag Assistant / Google Ads measurement | Requires logged-in browser/account readbacks. Local evidence cannot prove the app-fired checkout `purchase` event currency/value. |
| Google Ads RO bulk upload | Prior preview became stale/not visible. Needs live UI/browser readback before any retry or skip branch. |
| Google Ads BE bulk upload | Upload-throttle cooldown remains a platform gate; keep BE last. |
| Merchant Center | US/es fix requires account access plus exact owner approval; US/en is solved and should not be touched. |
| Pinterest | Event Quality may remain `Fair` until app/platform refresh or paid Pinterest traffic; avoid duplicate tracking fixes. |
| Shopify public probes | Rapid public probes can trigger Shopify `429`; use low-volume browser checks when needed. |

## Next Safe Parallel Actions

These lanes are safe under current guardrails because they are local, read-only prep, browser/read-only when the parent has access, or paused-build only after explicit direction.

| Rank | Lane | Output | Hard stop |
|---|---|---|---|
| 1 | Measurement readback lane | Browser-ready checklist for Tag Assistant, GA4 DebugView/Realtime, and Google Ads conversion diagnostics, including pass/fail fields for currency, value, transaction ID, and duplicate purchase detection. | Stop before any payment/order. If a real order is needed, ask for exact controlled-test approval. |
| 2 | Ads branch decision lane | One-country decision board for `RO` retry vs `RO` skip/park, then `PT`, `GR`, `FR`, `BE`; include no-duplicate checks, expected row counts, preview/apply/readback gates, and completed-country do-not-touch list. | Stop before upload/apply unless parent has fresh owner direction and is operating in the approved paused-build scope. |
| 3 | Approval packet lane | Compact owner-decision packet for Merchant US/es, Pinterest Event Quality/paused draft, beach metadata repair, and native-language copy choice, with exact approval phrases and rollback/readback criteria. | Stop before Merchant/Pinterest/Shopify/Admin/Ads writes. |
| 4 | Economics scorecard lane | Local weekly optimization template keyed to existing campaign IDs, CPC/CPA/ROAS guardrails, kill thresholds, and required columns for spend, clicks, conversions, value, search terms, products, countries, and returns risk. | Stop before changing budgets, bids, campaign status, product scope, or conversion goals. |

## Top 3 Safe Next Lanes For Parent

1. Measurement readback lane: prove or formally escalate the non-US `purchase` event currency/value gate before any enablement.
2. Ads branch decision lane: get fresh owner direction on `RO` retry vs skip/park, then proceed one country at a time only inside paused-build guardrails.
3. Approval packet lane: prepare concise approval-ready decisions for Merchant US/es, Pinterest, beach metadata, and native-language copy so blocked lanes do not stall the whole sprint.
