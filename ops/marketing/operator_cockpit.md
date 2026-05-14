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
- Repaired active GB/CA/AU keyword strategy locally: the three generic exact keywords are now explicitly only starter controls, with GB English-UK, CA English-Canada/French-Canada-gated, and AU English-Australia long-tail intent maps saved as review-only candidates.
- Ran fresh read-only GB/CA/AU Ads monitor: stale search-term filters were removed, keyword/RSA/final URL checks passed, Quality Score columns were visible, and current keywords show `Eligible (Limited)` below first-page estimates around `$0.65-$0.74`; owner hard `$0.15` CPC cap means those head terms and close variants are rejected as action rows. Live landing sanitizer still failed, so the bounded action packet is blocked/not uploadable.
- Corrected the blocked GB/CA/AU packet: removed lazy close-head variants as proposed actions and replaced them with market-specific long-tail validation candidates that still require landing-clean and `$0.15` CPC validation before upload.
- Added the `$0.15` CPC keyword factory criteria: build a big local universe fast, score it, then promote only validated market/landing/economics-safe batches into live packets.
- Corrected the keyword factory to be US-first. US is the biggest market; GB/CA/AU are expansion Search repair lanes, not a replacement for US keyword intelligence.
- Added the proactive action mandate: results over monitor loops. If a mistake, broken state, underperforming path, or clear improvement is visible, agents must fix it when safe/approved, or prepare the smallest exact approval packet and keep another safe lane moving.
- Created the action-biased keyword operating system: `keyword_strategy.md`, `keyword_scoring_rubric.md`, and a 105-row `keyword_universe.csv` seed with US first, market-language adaptation, `GREEN/YELLOW/RED` thresholds, and no live-upload authority.
- Added the command-layer integration guard: initial audit found 4 side-document risks and current audit now passes with 25 tracked files / 0 risks. New `ops/marketing/` artifacts must be registered, action-linked, logged, or marked generated/archive before they count as complete.
- Added the broad continuity integrity guard: `ops/scripts/check_continuity_integrity.py --strict` now blocks stale prompt anchors, unquarantined alternate worklogs, spend-authority disagreements, stale cockpit HTML, failed marketing integration audits, missing worklog anchors, and AGENTS/CLAUDE drift.
- Added an explicit automation capability inventory and Merchant capacity local diagnosis: shell/repo writes/network/Playwright MCP are usable, but authenticated Chrome/account surfaces are not equivalent in this runtime because Chrome DevTools is profile-locked and Computer Use interactive access is not granted. Merchant capacity warning is current, but exact paid-cohort intersection still needs an authenticated read-only Merchant session.

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
- Campaign detail source now includes market/language-specific active keyword strategy for GB, CA, and AU, with localized vocabulary, candidate themes, landing-fit gates, negative watchlists, and no-cannibalization ownership.
- Fresh monitor packet added at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/` with a blocked exact-scope bounded action packet.
- New expert standard file: `ops/marketing/expert_growth_playbook_2026.md`.
- New local packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-capability-merchant-capacity-diagnosis/AUTOMATION_CAPABILITY_AND_MERCHANT_CAPACITY_DIAGNOSIS.md`.
- `ops/marketing/spend_authorization.md` now records `APPROVED_ACTIVE` bounded authority from the owner message.
- Local docs/prompts updated to require reviewer use before risky decisions.
- Existing stopped-session local sanitizer patch remains in place and was not rewritten.
- New keyword command files: `ops/marketing/keyword_strategy.md`, `ops/marketing/keyword_scoring_rubric.md`, and `ops/marketing/keyword_universe.csv`.
- New integration guard: `ops/scripts/audit_marketing_command_integration.py` and generated report `ops/marketing/command_layer_integration_audit.md`.
- New broad continuity guard: `ops/scripts/check_continuity_integrity.py`.
- `ops/AGENT_WORKLOG_utf8.md` is now explicitly `HISTORICAL_DO_NOT_USE`; unique historical session titles were compared and summarized in the canonical worklog.

## Live Changes

- None in this pass.
- No live Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme publish write occurred.

## Current Blockers

- Active paid Search landing supplier/source URL leak is locally fixed but still requires approved live theme sync/readback before expansion; fresh 08:17 public GB/CA/AU source readback still fails on `detail.1688.com` in `data-analytics-vendor`.
- Merchant US/es age_group needs a current exact all-row readback before closure or repair.
- Merchant Shopping Ads capacity warning is current and account-level, but exact paid-cohort impact is still unresolved because the authenticated Merchant Chrome/account path is unavailable in this automation runtime.
- Pinterest Ads Manager remains blocked by authenticated controllable access.
- GB/CA/AU exact Search have fresh read-only Ads checks done: stale search-term filters are cleared, search terms are still empty, keyword/RSA/final URLs are enabled/country-qualified, and keyword UI shows auction-entry pressure. Live Ads action is blocked by the landing sanitizer failure and by the hard `$0.15` CPC gate for head/near-head terms. A local scored long-tail universe exists for validation, not upload.
- Standard Shopping has impressions but no clicks/cost/conversion evidence from the latest command-layer readback. US is still the primary market; keyword work applies through Shopping query/title/product/feed diagnostics and future US Search/Pinterest packets.
- Bounded spend authority is active, but current campaign changes still need fresh readback and quality gates before any proactive live write.
- Daily optimization ownership is now required: agents must monitor, diagnose, act inside approved caps when gates pass, and keep the dashboard current.
- Monitoring cannot be the deliverable. Every monitor/readback must end in `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- Side documents are now a tracked process defect. Current audit result: 25 tracked command-layer files, 0 side-document risks.
- Alternate worklogs are not current state. The only active worklog is `ops/AGENT_WORKLOG.md`; `ops/AGENT_WORKLOG_utf8.md` is historical evidence only.

## Next 3 Tasks

1. Get approval for scoped live theme sanitizer sync/readback, then prove GB/CA/AU final URL source/DOM has zero supplier/source URL hits.
2. Use an authenticated Merchant session to intersect the live Shopping capacity warning against the `780`-row `us_test_ready` / `paid_eligible` cohort and to obtain a fresh exact US/es export/readback.
3. Validate top `GREEN` rows from `keyword_universe.csv` against active products, clean landing routes, and Keyword Planner/keyword UI at max CPC `$0.15`; do not raise bids or upload close-head variants.

## Assumptions

- The stopped-session supplier/source URL sanitizer patch is intentional and should be preserved.
- The May 14 command-layer live reconciliation and paid-landing local handoff entries are current repo evidence, but live platform decisions still need fresh readbacks where noted.
- The user wants agents to act proactively inside approved paid-media caps once quality gates pass, but out-of-scope writes still need fresh exact approval.
- The current exact GB/CA/AU keyword set is a controlled starter hypothesis, not proof of the final smartest keywords; source-backed daily search-term and ROAS evidence must decide expansions, negatives, bid changes, or pauses.
- 2026 source-backed best practice favors controlled high-intent tests until conversion value, landing quality, and search-term data justify broader automation or scale.
- The owner wants aggressive AI-speed growth, which means faster daily evidence loops, long-tail ideation, bounded execution, and next-day sales/ROAS review inside guardrails; it does not mean unsafe broadening or unapproved external writes.
- The owner expects proactive fixes and improvements, not bureaucracy. Local/read-only mistakes should be fixed immediately; currently approved live mistakes should be fixed with before/after readback; unapproved live fixes should become exact approval packets.
- GB/CA/AU long-tail candidate rows are `review_only_not_uploaded`; they are not live-account instructions until fresh readback, reviewer, landing, `$0.15` CPC validation, and approval/bounded-authority gates pass.
- The fresh monitor made the stale search-term filter problem better, not the traffic problem: filters are clear now, but no search terms exist and the live landing still blocks traffic expansion.
- `keyword_universe.csv` is a local universe, not a live upload artifact; `GREEN` rows still need active-product, landing, `$0.15` CPC, reviewer, and after-state gates.
- If an artifact is not wired into `AGENTS.md`, an action surface, and continuity logs, it is not progress; it is a side-document risk.
- If a prompt, packet, digest, or memory names an older anchor, resolve latest state from `ops/AGENT_WORKLOG.md` and the command layer instead.
- If this automation runtime cannot use the authenticated Chrome/account path, treat Merchant/Pinterest account readbacks as capability-mismatched and hand off the exact authenticated next step instead of claiming parity.

## Risks / Approval Needed

- Publishing the sanitizer to the live Shopify theme is an external write not automatically covered by paid-media spend authority.
- Merchant feed/source/product-scope/product-group actions require fresh exact approval.
- Pinterest object creation, campaign/ad group/product group changes, budget/bid/status changes, or catalog/source/tag/CAPI writes require approval and authenticated access.
- Any spend/budget/bid/status/feed/product/conversion recommendation must pass the reviewer checklist and cite current evidence.
- Any GB/CA/AU keyword expansion must keep language and market ownership clear: no French-Canada terms in the active English-Canada campaign, no duplicated exact keywords across live ad groups, no pajama/swim/beach intent routed to a dress PDP, no close-head-term "long tail", and no CPC above `$0.15`.
