# Marketing Safety Reviewer Checklist

Last updated: 2026-07-23

Run or simulate this checklist before any non-ops file edit, any external write, any blocker reclassification, or any spend/budget/bid/status/feed/product/conversion recommendation.

## Required Inputs

- Proposed action or recommendation.
- Files/surfaces/accounts affected.
- Approval source, if any.
- Evidence paths and readback timestamps.
- Expected local change, live change, or no-write outcome.
- Rollback or next unblock path.

## Material Decision Challenge Contract

Use this compact contract before a material decision: any paid-media spend/status/budget/bid action, live feed/product/conversion write, blocker reclassification, durable command-layer rule change, or costly/irreversible action. Routine reversible repo-local edits still use the checklist below but do not need a ceremonial contract.

Freeze these fields before execution:

1. `decision_id`, `as_of`, and evidence grade (`LIVE_VERIFIED`, `REPO_EVIDENCE`, or `INFERENCE`).
2. Exact decision and measured baseline.
3. Three explicit options: proposed action, status quo, and one credible alternative.
4. Predicted outcome and the single assumption most likely to invalidate it.
5. Numeric or observable success criterion, kill criterion, decision window, and maximum cost/exposure.
6. Approval boundary and smallest rollback.
7. Evidence that would change the decision.
8. A named verifier who did not build or execute the action.
9. One recommended next action.
10. After the window: resolved outcome, evidence, and durable learning.

The builder may prepare the contract, but may not self-certify the verifier field. A decision remains `UNRESOLVED` until a separate linked outcome record with dated evidence is appended to `decision_log.md`. The frozen prediction must not be rewritten; corrections append `AMENDMENT` or `SUPERSEDES`.

## Checklist

| Check | Pass condition | Reviewer notes |
|---|---|---|
| Approval boundary | Fresh exact action-time approval exists, or action is repo-local/read-only/paused-review-only. |  |
| External-write risk | Action does not mutate Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or live theme publish state unless approval covers it. |  |
| Spend authority | `spend_authorization.md` is `APPROVED_ACTIVE` for bounded authority, or the session has exact approval; otherwise no spend/status/budget/bid action. |  |
| Bounded proactive action | If using `APPROVED_ACTIVE`, the action is green-gated, inside `$80/day` total and `$5/day` new/test caps, quality-checked, and expected to improve profitable sales or path to `650% ROAS`. |  |
| Supplier/source URLs | No `1688`, `detail.1688.com`, `alibaba`, `aliexpress`, source URL, vendor URL, or supplier identifier reaches public HTML, analytics attributes, feed-visible data, ad copy, product copy, tags, or customer-visible metafields. |  |
| Active/public/purchasable scope | Product/landing scope is currently active, public, purchasable, in-stock/salable for the relevant channel, and not draft/inactive/unpublished/excluded/unavailable. |  |
| Seasonal/category fit | Campaign, keyword, creative, landing page, and event layer match shopper intent and the current calendar. |  |
| Expert source alignment | Recommendation follows `expert_growth_playbook_2026.md` and cites the relevant source-backed standard when strategy is material. |  |
| Full quality attention | Bid strategy, keyword/search-term quality, Quality Score or missing quality readback, ad/RSA quality, product/photo fit, landing page, measurement, and sales/ROAS path were checked where relevant. |  |
| Keyword and negative discipline | Keyword selection criteria, expansion criteria, negative-keyword evidence, and watchlist-vs-upload distinction are documented; no negative or keyword change is made from guesswork. |  |
| High-intent / low-waste economics | Keywords, products, audiences, and creatives are selected for buying intent, plausible CPC/CPA, product fit, and path to about `650% ROAS`; cheap low-intent traffic is rejected. |  |
| Anti-cannibalization | Query/product/audience ownership is clear across Search, Shopping, Pinterest, remarketing, countries, languages, campaigns, and ad groups; no duplicate or self-competing structure is introduced. |  |
| Day 1 action clock | Sales/ROAS are checked daily; zero impressions after 24 hours triggers same-day diagnosis and high-intent long-tail or auction-entry planning. |  |
| Repo-known vs live-verified | Historical repo evidence is labeled as repo-known/stale unless a current readback proves live state. |  |
| Semantic freshness control | `current_marketing_state.md` has an authoritative control block; stale mode is fail-closed, contains no `GREEN` queue row, and permits only read-only reconciliation. |  |
| Frozen material-decision contract | Material action has baseline, three options, prediction, invalidating assumption, success/kill criteria, window, maximum exposure, approval, rollback, and evidence that would change the decision. |  |
| Independent verification | A reviewer who did not build or execute the action verifies the frozen contract and after-state; unresolved outcome is not presented as success. |  |
| Decision/outcome linkage | A material decision has a stable `decision_id`; its observed result is a separate linked `outcome_id`, and the original prediction/success/kill/window fields remain frozen. |  |
| Learning evidence | A routine durable rule is supported by two independent observed-outcome events; repeated policy/prompt copies are not counted as recurrence. A single-event exception is limited to high-severity spend, customer-truth, publication, credential, destructive-action, or approval-scope failures. |  |
| Blocker classification | Any blocker close/downgrade/upgrade maps to `ops/PROBLEM_TRACKER.md` status, fixed criteria, evidence, and next action. |  |
| Audit-only drift | The outcome creates a sales-moving next action, approval packet, blocker removal, controlled build, or exact unblock step. |  |
| Operator cockpit | `operator_cockpit.md` will be updated before stopping/compacting with current goal, local/live changes, blockers, next 3 tasks, assumptions, and risks. |  |

## Verdict Format

```text
Reviewer verdict: PASS | PASS_WITH_GATES | BLOCK
Decision ID:
Decision status: NOT_MATERIAL | FROZEN_UNRESOLVED | RESOLVED
Independent verifier:
Checked:
- ...
Risks:
- ...
Required gates/fixes:
- ...
Evidence:
- ...
Safest next sales-moving action:
- ...
```

## Stop Conditions

- Missing or ambiguous approval for a live write.
- Account login, CAPTCHA, billing, account switcher, policy, destructive, or unsaved-change prompt.
- Supplier/source URL leak on any public or feed-visible surface.
- Attempt to use stale evidence for a live spend/status/feed/product/conversion decision.
- Product scope includes inactive, draft, unpublished, unavailable, excluded, or not-currently-read-back products.
- Strategy recommendation lacks high-intent/low-waste economics, anti-cannibalization owner, or a source-backed reason.
