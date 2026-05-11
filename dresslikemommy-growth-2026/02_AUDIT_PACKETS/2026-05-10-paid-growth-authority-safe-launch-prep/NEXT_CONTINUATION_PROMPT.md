# Next Continuation Prompt

Use the canonical prompt at `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the operating prompt.

Latest anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-authority-safe-launch-prep`

Continue the Dress Like Mommy paid-growth sprint from the latest worklog/problem-tracker state. The owner gave broad authority to get everything ready and start advertising only when the setup is clean. Do not start live spend until all hard launch gates pass for the exact first spend unit.

Start by reading:

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md`
- `ops/AGENT_COORDINATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/PAID_GROWTH_AUTHORITY_SAFE_LAUNCH_PREP_REPORT.md`

Priority order:

1. Close `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`. Observe a genuine non-US purchase event if available. If a real transaction is required, request exact owner approval for a controlled low-value non-US test purchase/refund/cancel. Do not enter payment or create an order without that exact action-time approval.
2. For the first Google Ads launch candidate, repeat just-in-time readbacks for campaign `23838895360` and ad group `Mommy & Me Dresses - Exact`: paused Search, `$2/day`, Manual CPC, `$0.15`, GB presence-only, content/YouTube off, account-default purchase conversion, no product/feed/PMax/Shopping changes.
3. If measurement and readbacks pass, enable only the exact GB campaign/ad group unit described in the authority packet, and immediately start the first 14-day monitoring template. Do not enable broader country sets.
4. Continue paused infrastructure only after readbacks: wait for Google Ads upload throttle cooldown, confirm no in-progress RO/FR/BE upload row and no RO campaign, then retry one-country `RO` preview only. Do not stack `PT`/`GR` behind unresolved `RO`.
5. Keep Pinterest non-US account writes gated. Use the local non-US templates only as operator prep. US Pinterest remains the only local-template-ready Pinterest path, and Event Quality remains a live-spend gate.

Guardrails:

- No PMax enablement.
- No Standard Shopping change.
- No Merchant upload/source edit/sync.
- No Shopify live product-data change.
- No conversion-goal, product-scope, feed-label, product-group, budget, bid, or status change except the single exact first-enable action after all hard gates pass.
- No payment/order/refund/cancel without exact action-time approval for that transaction path.

End by updating `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and a new `AGENT_CONTINUITY_ANCHOR`.
