Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as canonical. Read it first, then read `AGENTS.md`, `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/PROBLEM_SOLVING_PROTOCOL.md`, `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the latest worklog entries.

Continue from:

`AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-readonly-us-es-au-followup`

Do not redo US/en age_group fixes. Do not redo the AU `429` probe unless an action-time readback is required for live spend/enablement. Preserve all no-spend/no-live-write guardrails: no live spend, no campaign enablement, no campaign/budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads/source syncs/source edits, no Shopify live product-data changes, no Pinterest draft/campaign/tag/CAPI/product-group/audience/budget/bid writes, no checkout payment/order, no theme publish, and no credential changes without fresh exact approval.

Current state:

- Merchant US/en age_group remains solved: exact paid-cohort `US/en/United States` Missing age group count is `0`.
- `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` is now `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`: read-only Merchant product-detail RPC confirmed source `10627981690` has affected `US` / `es` / `United States` items still missing effective `n:age_group`. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`.
- `PROB-2026-05-08-AU-CHECKOUT-429` is solved: isolated Chrome AU checkout-to-shipping passed with AUD, Standard `0.00 AUD`, Express API `18.24 AUD`, checkout UI Standard/Express/AUD visible, no `429`, no payment, and no order. Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/au-checkout-readonly/AU_ISOLATED_CHECKOUT_TO_SHIPPING.md`.
- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` remains `OWNER_APPROVAL_REQUIRED`: Event Quality is still `Fair`; clean Pinterest scope is `342` EN-US rows with `4` exclusions.

Next best actions, in order:

1. If owner approves, run only the narrow Merchant US/es age_group repair review for source `10627981690`, with pre/post readbacks and no broad source/feed/product/Ads changes.
2. If owner instead wants growth infrastructure first, use a separate exact approval gate for paused non-US Google Search build only; do not duplicate or edit US campaign `23827590655`.
3. Use a separate exact approval gate for paused US Pinterest drafts only from the clean `342` rows and `4` exclusions, or for a narrow Event Quality repair; do not bundle it with Google Ads or Merchant.
4. Keep ROAS/economics/creative/reporting lanes moving locally while approval-gated live lanes wait.
