# Paid Growth Checkout / Merchant / Pinterest Readbacks Lane Board

Date: 2026-05-07 EDT / 2026-05-08 UTC

Parent/orchestrator: Codex current session.

Scope: read-only/local/QA only. No live spend, no campaign import/create/enable/pause, no budget, bid, status, conversion-goal, product-scope, feed-label, product-group, Merchant upload, Shopify product-data, shipping-rate, Market, payment, order, Pinterest draft, pixel/tag/CAPI, or Google & YouTube publication changes.

## Moving

| Lane | Owner | Surface | Current Action |
|---|---|---|---|
| Parent control | Parent | coordination, packet, final integration | Own approvals, lane board, final report, worklog, coordination, and AGENTS memory. |
| Checkout QA | Subagent | public storefront/cart shipping-rate endpoint | Slow ES/IT/RO/PT route/currency/no-payment checkout QA using known region fields. |
| Merchant | Subagent | Merchant Center / Shopify read-only scripts | Recheck source timestamp and product-issues path; no product/feed/source writes. |
| Pinterest | Subagent | Pinterest read-only gate | Fresh read-only gate if account/CDP access is available; no drafts/spend/writes. |
| Ads gate | Subagent | local Ads approval/import gate | Keep paused import parked; verify no approval and no live action. |

## Blocked / Guarded

| Lane | Guardrail |
|---|---|
| Checkout QA | No payment submission and no order creation. Stop on 429/CAPTCHA/bot-protection. Do not alter shipping rates or Markets. |
| Merchant | Do not repeat the Google & YouTube toggle; do not edit product data; do not create local inventory feeds. Merchant `Missing local inventory data` is not a product-data fix target for this dropshipping business. |
| Pinterest | Do not create drafts, product groups, campaigns, audiences, budgets, bids, pixels, tags, CAPI, or spend. |
| Ads | No import/create/enable without exact action-time owner approval and just-in-time readbacks. |

## Waiting On Approval

| Action | Approval |
|---|---|
| Paused Google international Search import/create | Exact approval phrase from the prior packet; preview-first only; no enable/spend. |
| Merchant official source refresh/resync | Exact source-refresh approval; read back first; no product-data edits/uploads/feed-label/campaign changes. |
| Pinterest paused US drafts | Fresh read-only gates plus exact paused-draft approval. |
| Any live spend | Separate approval after checkout, catalog/feed, tracking, and economics gates pass. |

## Done

| Lane | Result |
|---|---|
| Parent bootstrap | Required memory and latest continuation prompt read; new packet created. |
| Ads gate | Import remains parked; no live Google Ads access or writes. |
| Merchant | Partial improvement: paid-cohort US/en `Missing age group` dropped from `754` to `623`, but still not cleared; API path still scope-blocked. |
| Checkout QA | ES/IT/RO/PT route/policy/shipping-rate checks passed; currency/presentment still reads `USD` instead of expected `EUR`. |
| Pinterest | Fresh read-only gate completed; 0 campaigns/0 spend, Event Quality still `Fair`, EN catalog completed, item proof only partial. |

## Final Status

| Category | Status | Next Safe Action |
|---|---|---|
| ES/IT/RO/PT shipping routes and outbound rates | Passed with HTTP `200`, no stale limited-country copy, rates returned for all four countries. | Human/browser checkout walkthrough to shipping step only, focused on presentment currency; no payment. |
| ES/IT/RO/PT currency | Blocked; product/cart signals still `USD` while expected market currency is `EUR`. | Read-only inspect Markets/currency/presentment behavior before paid traffic. |
| Merchant age_group | Partial improvement, not cleared: `623` paid US/en item IDs still affected. | Continue read-only monitoring; do not toggle, upload, or edit products. |
| Merchant local inventory diagnostic | Not a product-data fix target; DLM has no physical store and is dropshipping. | At most read-only verify whether Local Inventory Ads / physical-store settings are enabled by mistake. |
| Pinterest | Blocked for drafts/spend; Event Quality still `Fair`, item proof partial. | Full 346-row current item proof, then owner decision on accepting Event Quality gaps for paused draft only. |
| Ads import | Parked, not approved. | Exact approval plus just-in-time readbacks and preview-only import path. |

## Next Safe Parallel Action

1. Currency/presentment lane: read-only inspect why ES/IT/RO/PT localized product and cart-rate signals remain `USD`.
2. Merchant lane: continue read-only monitoring until paid US/en `Missing age group` reaches `0` or stalls; no second toggle without approval.
3. Pinterest lane: full current 346-row US item proof; keep drafts/spend parked.
4. Ads lane: parked until exact approval; if approved, preview-first only.
5. Parent: integrate this packet into AGENTS/worklog/coordination and continue no-live-spend posture.
