# Spend Authorization

Status: `REVOKED_BY_OWNER`
Last updated: 2026-09-28
Approval source: owner chat 2026-09-28 ended all paid marketing. The 2026-05-14 `$80/day` bounded authority below is historical and void.

### OWNER DECISION — paid marketing ended (2026-09-28)

Status: `REVOKED_BY_OWNER`. The owner said in chat on 2026-09-28: "I have paused all the ads from microsoft ads, and google ads I was losing money ! I will not do any more paid marketing! from now on we will only focus in increasing sales organically FREE traffic."

- All paid media is ended: Google Ads (650-997-2886 and legacy 399-097-6848), Microsoft Ads 477439, Pinterest ads, and any other paid channel.
- No agent may enable, resume, create, rebuild, budget, bid on or re-scope any paid campaign, or propose paid spend, unless the owner reverses this in a new chat message. Historical `APPROVED_ACTIVE`, green rows, packets and heartbeats below are void.
- Still allowed: read-only checks that spend stays at $0, and pausing anything found still spending (this reduces cost and follows the owner's decision).
- Free Google/Microsoft product listings, organic Pinterest, SEO, email and other unpaid channels are NOT paid marketing; they are the growth plan now (`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-27-million-plan/README.md`).

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
- Promote only small validated keyword batches from `keyword_universe.csv`; the full local universe is never a live upload artifact.
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
- Search keyword additions have `GREEN` scoring in `keyword_universe.csv` or an equivalent reviewer-approved row, validated market language, anti-cannibalization owner, landing proof, and `$0.15` CPC feasibility. `YELLOW` rows are local unless the action is a tightly bounded phrase-discovery repair with an exact gate and after-state readback.
- Shopping/Pinterest actions have product/feed/source, product groups, photos/images, titles, prices, availability, landing page, and measurement state checked where available.
- High-intent/low-waste economics, anti-cannibalization ownership, and `expert_growth_playbook_2026.md` source-backed strategy are checked where relevant.
- The action is expected to improve profitable sales, CPA, conversion value, or path to `650% ROAS`; vanity metrics alone are not enough.
- Reviewer outcome is `PASS` or `PASS_WITH_GATES` and required gates are satisfied before the live write.

## Keyword Action Thresholds

- Build the keyword universe as large as possible locally, starting with US first, then market-adapted GB/CA/AU. Do not upload the whole universe live.
- If an enabled Search campaign or ad group has `0` impressions after 24 hours, same-day diagnosis is mandatory: status, keyword status, policy, RSA, Quality Score or gap, geo, language, final URL, landing sanitizer, bid, budget, auction entry, and search volume.
- If everything is eligible but too narrow, prepare or execute a green-gated repair with `5-20` closely related exact/phrase long-tail rows at max CPC `$0.15`; do not bid up head terms above `$0.15`.
- If exact rows are `Low search volume`, keep them local as evidence, add adjacent buyer-moment phrase variants only when green-gated, and review search terms the next day.
- With planning AOV `$70` and target ROAS `650%`, rough target CPA is `$10.77`. At about `$5.38` spend with no add-to-cart, checkout, qualified query, or other useful signal, hold/narrow/prepare pause. At about `$10.77` spend with no purchase, pause/narrow/reroute when authority and evidence allow.
- Every live Search session must produce a serving repair, negative action, keyword expansion, hold/kill/scale decision, or exact blocker/unblock action. Monitor-only is not progress unless there is genuinely no actionable data and `daily_scorecard.md` records the next decision.

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
