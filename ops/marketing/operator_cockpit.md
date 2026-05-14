# Marketing Operator Cockpit

Last updated: 2026-05-14
Owner view: human-friendly command dashboard for paid-growth execution.

Open the one-screen browser dashboard at `ops/marketing/operator_cockpit.html`.
Render and open it with:

```bash
python3.13 ops/scripts/open_marketing_cockpit.py
```

Regenerate it without opening after changing command-layer state with:

```bash
python3.13 ops/scripts/render_marketing_cockpit.py
```

## Current Goal

Provide a human-friendly paid-growth cockpit where the owner can pick Google Ads or Pinterest, click into a campaign, and quickly see what is active, when it became active, today/yesterday metrics, whether the test is learning, how many paid-growth sales and ROAS it produced, how keywords/negatives were chosen, how the strategy follows 2026 expert standards, who owns daily optimization, what assumptions are being tested, what would trigger improvement, evidence, blockers, and the next decision deadline.

## Success Measure

Maximize profitable Dress Like Mommy paid-growth sales across Google Ads and Pinterest while targeting about `650% ROAS`. The dashboard must make clear whether each campaign is producing purchases, revenue, conversion value, CPA, and ROAS evidence, or whether it is only producing early learning signals.

Current paid-growth posture:

- Keep execution sales-moving: live readbacks, approved controlled actions, paused-ready builds, blocker removals, or exact unblock actions.
- Bounded spend authority is now active while `ops/marketing/spend_authorization.md` says `APPROVED_ACTIVE`: total paid-media cap `$80/day`, new/test campaign cap `$5/day`, quality-gated proactive actions only.
- Agents and subagents are responsible for monitoring progress and executing green-gated bounded actions without waiting for the owner when the action is inside approved limits and supports the `650% ROAS` goal.
- Starting 2026-05-14, each day without sales growth, usable learning, or a sales-moving improvement is a failure signal. By tomorrow, active lanes must answer: sales, revenue, CPA, ROAS, and what changed to get closer to `650% ROAS`.

## Expert Strategy Standard

Run Day 1 growth discipline: daily sales/ROAS check, high-intent low-waste traffic, no self-cannibalization, same-day action for zero impressions after 24 hours, and fast bounded improvement toward `650% ROAS`.

Detailed source-backed standard lives in `ops/marketing/expert_growth_playbook_2026.md`: Google/Pinterest/OpenAI/Anthropic practices, keyword economics, channel roles, daily optimization clocks, specialist personas, and rookie-mistake blockers.

## Done Today

- Reconciled stopped-session state before editing.
- Preserved existing local supplier/source URL sanitizer changes and command-layer reconciliation changes.
- Added a Codex-native read-only `marketing_safety_reviewer` agent.
- Added reviewer checklist, review log, assumption log, and this cockpit.
- Added a self-contained browser dashboard generated from the command layer.
- Added a clickable Campaign Explorer for Google Ads and Pinterest with active/running state, keywords/targeting, ads/creative quality, strategy reasoning, evidence, and deadlines/next checks.
- Upgraded the Campaign Explorer into a proactive test monitor with activation time, latest readback freshness, today/yesterday metric slots, test clock, assumptions, improvement triggers, and next decision rules.
- Added explicit success measurement framing: maximize profitable sales at about `650% ROAS`, with target CPA and conversion-value proof before scale decisions.
- Activated bounded spend authority and clarified that agents must proactively monitor and act inside approved caps only after quality gates pass.
- Added keyword-selection criteria, negative-keyword criteria, daily optimization owner, and continuous-improvement loop sections so campaigns cannot be created and forgotten.
- Added a 2026 expert growth playbook so future agents use source-backed keyword, negative, bidding, Shopping, Pinterest, CRO, measurement, anti-cannibalization, and agent-persona standards.
- Added Day 1 growth urgency: tomorrow's scorecard must answer sales and ROAS, and a zero-impression campaign after 24 hours now triggers same-day diagnosis and high-buyer-intent long-tail action planning.
- Updated marketing operating docs so future agents update this cockpit before stopping or compacting.

## Local Changes

- New local command-layer files under `ops/marketing/`.
- New project-scoped Codex reviewer agent under `.codex/agents/`.
- New local one-screen dashboard `ops/marketing/operator_cockpit.html`.
- New local renderer `ops/scripts/render_marketing_cockpit.py`.
- New campaign detail source `ops/marketing/campaign_explorer.json` for Google Ads and Pinterest click-through panels.
- Campaign detail source now includes test-clock and improvement-trigger fields so zero-impression or zero-learning tests are diagnosed at deadlines instead of quietly sitting.
- Campaign detail source now explains whether keywords are truly proving smart from daily data, how negatives are selected from search-term evidence, and which agent owns daily action.
- Campaign detail source now includes expert-source standard, anti-cannibalization rules, and keyword economics/low-waste tests.
- Campaign detail source now treats T+24 zero impressions as an action trigger, not a passive hold.
- New expert standard file: `ops/marketing/expert_growth_playbook_2026.md`.
- `ops/marketing/spend_authorization.md` now records `APPROVED_ACTIVE` bounded authority from the owner message.
- Local docs/prompts updated to require reviewer use before risky decisions.
- Existing stopped-session local sanitizer patch remains in place and was not rewritten.

## Live Changes

- None in this pass.
- No live Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme publish write occurred.

## Current Blockers

- Active paid Search landing supplier/source URL leak is locally fixed but still requires approved live theme sync/readback before expansion.
- Merchant US/es age_group needs a current exact all-row readback before closure or repair.
- Merchant Shopping Ads capacity warning needs read-only impact diagnosis for the paid cohort and Standard Shopping.
- Pinterest Ads Manager remains blocked by authenticated controllable access.
- GB/CA/AU exact Search have already crossed the T+24 zero-impression line in saved evidence; the next monitor must diagnose serving and evaluate high-intent long-tail/auction-entry actions instead of waiting passively.
- Standard Shopping has impressions but no clicks/cost/conversion evidence from the latest command-layer readback.
- Bounded spend authority is active, but current campaign changes still need fresh readback and quality gates before any proactive live write.
- Daily optimization ownership is now required: agents must monitor, diagnose, act inside approved caps when gates pass, and keep the dashboard current.

## Next 3 Tasks

1. Run today's sales/ROAS readback and fresh today/yesterday Google Ads and Shopping metrics plus keyword quality, ad/RSA, landing, product/photo, and measurement diagnostics.
2. Because GB/CA/AU crossed T+24 with zero impressions in saved evidence, run same-day serving diagnosis and prepare/execute only green-gated bounded long-tail or auction-entry actions inside approved caps.
3. Build a high-buyer-intent long-tail candidate map for GB/CA/AU that avoids self-cannibalization, then continue blocker removal for paid-landing sanitizer sync, Merchant readbacks, and Pinterest access.

## Assumptions

- The stopped-session supplier/source URL sanitizer patch is intentional and should be preserved.
- The May 14 command-layer live reconciliation and paid-landing local handoff entries are current repo evidence, but live platform decisions still need fresh readbacks where noted.
- The user wants agents to act proactively inside approved paid-media caps once quality gates pass, but out-of-scope writes still need fresh exact approval.
- The current exact GB/CA/AU keyword set is a controlled starter hypothesis, not proof of the final smartest keywords; source-backed daily search-term and ROAS evidence must decide expansions, negatives, bid changes, or pauses.
- 2026 source-backed best practice favors controlled high-intent tests until conversion value, landing quality, and search-term data justify broader automation or scale.
- The owner wants aggressive AI-speed growth, which means faster daily evidence loops, long-tail ideation, bounded execution, and next-day sales/ROAS review inside guardrails; it does not mean unsafe broadening or unapproved external writes.

## Risks / Approval Needed

- Publishing the sanitizer to the live Shopify theme is an external write not automatically covered by paid-media spend authority.
- Merchant feed/source/product-scope/product-group actions require fresh exact approval.
- Pinterest object creation, campaign/ad group/product group changes, budget/bid/status changes, or catalog/source/tag/CAPI writes require approval and authenticated access.
- Any spend/budget/bid/status/feed/product/conversion recommendation must pass the reviewer checklist and cite current evidence.
