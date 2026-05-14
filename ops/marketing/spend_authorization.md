# Spend Authorization

Status: `APPROVED_ACTIVE`
Last updated: 2026-05-14
Approval source: owner message in current Codex session authorizing spend within the set limits as long as it respects the sales/ROAS goals.

This file defines the active bounded standing authority model. It is active only inside the limits and quality gates below.

## Business Goal

- Grow as many profitable Dress Like Mommy sales as possible across Google Ads and Pinterest.
- Target about `650% ROAS`.
- Avoid wasted spend and preserve tight test controls.

## Active Bounded Authority

Head of Growth may:

- Operate within a total daily paid-media cap of `$80/day`.
- Enable only green-gated rows in `ops/marketing/action_queue.md`.
- Start new/test campaigns only up to `$5/day` per campaign.
- Pause or reduce clear waste when spend/search-term/conversion evidence justifies it.
- Add exact negatives from search-term evidence.
- Execute bounded proactive optimizations only when the row is green-gated, fresh readback is saved, the Marketing Safety Reviewer checklist passes, and the action protects the `650% ROAS` goal.
- Keep all actions logged in `decision_log.md`, `daily_scorecard.md`, and `ops/AGENT_WORKLOG.md`.

## Quality Gates Before Any Proactive Live Action

All must pass before an operator may use this authority:

- The exact campaign/ad group/ad/keyword/product group/feed/source/product/surface is named in `action_queue.md`.
- Fresh before-state readback is saved or summarized in the command layer.
- The action stays under `$80/day` total and `$5/day` new/test campaign cap.
- Campaign/keyword/product/ad/landing scope is active, public, purchasable, not stale, not seasonally mismatched, and not supplier-leaking.
- Search campaigns have bid strategy, keyword match type, ad/RSA status, ad strength, Quality Score or quality-column gap, search terms, geo, device, landing route, and measurement state checked where available.
- Shopping/Pinterest actions have product/feed/source, product groups, photos/images, titles, prices, availability, landing page, and measurement state checked where available.
- High-intent/low-waste economics, anti-cannibalization ownership, and `expert_growth_playbook_2026.md` source-backed strategy are checked where relevant.
- The action is expected to improve profitable sales, CPA, conversion value, or path to `650% ROAS`; vanity metrics alone are not enough.
- Reviewer outcome is `PASS` or `PASS_WITH_GATES` and required gates are satisfied before the live write.

## Still Requires Fresh Approval

Even if bounded authority is approved, fresh explicit action-time approval is still required for:

- Billing or account-access changes.
- Conversion goals or attribution settings.
- PMax.
- Unresolved remarketing.
- Merchant feed/source/product-scope/feed-label/product-group changes.
- Shopify product, price, discount, policy, page, translation, inventory, or channel changes.
- Pinterest catalog/source/product-group/tag/CAPI changes outside the named approved paused draft path.
- Native-language ads or keywords without signoff.
- Spend above the total or per-campaign caps.
- Bid, budget, status, or launch actions when quality gates are incomplete, evidence is stale, or expected sales/ROAS impact is unclear.
- Any destructive action or action with unclear rollback.

## Activation Record

Activated by owner message on 2026-05-14 authorizing spend within the set limits as long as it respects the goals. The operative limits remain:

- Total daily paid-media cap: `$80/day`.
- New/test campaign cap: `$5/day` per campaign.
- Goal guardrail: maximize profitable sales while targeting about `650% ROAS`.
- Quality guardrail: no proactive live action without fresh readback, quality review, and command-layer logging.

## Current Effect

Because status is `APPROVED_ACTIVE`, Head of Growth and assigned channel operators may proactively execute green-gated bounded actions inside the limits above without asking the owner again. They must not use this as authority for out-of-bounds surfaces or incomplete-quality actions.
