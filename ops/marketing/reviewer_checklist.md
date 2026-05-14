# Marketing Safety Reviewer Checklist

Last updated: 2026-05-14

Run or simulate this checklist before any non-ops file edit, any external write, any blocker reclassification, or any spend/budget/bid/status/feed/product/conversion recommendation.

## Required Inputs

- Proposed action or recommendation.
- Files/surfaces/accounts affected.
- Approval source, if any.
- Evidence paths and readback timestamps.
- Expected local change, live change, or no-write outcome.
- Rollback or next unblock path.

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
| Blocker classification | Any blocker close/downgrade/upgrade maps to `ops/PROBLEM_TRACKER.md` status, fixed criteria, evidence, and next action. |  |
| Audit-only drift | The outcome creates a sales-moving next action, approval packet, blocker removal, controlled build, or exact unblock step. |  |
| Operator cockpit | `operator_cockpit.md` will be updated before stopping/compacting with current goal, local/live changes, blockers, next 3 tasks, assumptions, and risks. |  |

## Verdict Format

```text
Reviewer verdict: PASS | PASS_WITH_GATES | BLOCK
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
