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
- Ran fresh read-only GB/CA/AU Ads monitor: stale search-term filters were removed, keyword/RSA/final URL checks passed, Quality Score columns were visible, and current keywords show `Eligible (Limited)` below first-page estimates around `$0.65-$0.74`; owner hard `$0.15` CPC cap means those head terms and close variants are rejected as action rows.
- Re-read the active GB/CA/AU PDP final URLs from public source after the sanitizer handoff: current PDP final URLs now have `0` supplier/source-domain hits and `0` URL-like brand attributes across two header/cache variants. Collection-route preflight found only `mommy-and-me`, `family-matching`, and `pajamas` clean; `matching-dresses`, `swimsuits`, `vacation`, and `daddy-and-me` rows are held.
- Rerouted GB/CA/AU keyword rows away from dirty/broken collection routes: matching-dress wedding-guest rows now use clean `mommy-and-me`; vacation/family/daddy rows now use clean `family-matching` or `mommy-and-me`; swimwear rows now use clean `family-swimsuits`. `36` GB/CA/AU `GREEN` rows are now clean-route/CPC-validation-ready.
- Prepared the exact authenticated CPC validation packet for clean-route GB/CA/AU long-tail rows: `36` rows (`GB=12`, `CA=12`, `AU=12`), `/collections/family-swimsuits` passed fresh GB/CA/AU public route readbacks with `200` and `0` supplier/url-brand hits, and all rows remain `NO_UPLOAD` until authenticated `$0.15` validation passes.
- Built the US Standard Shopping query/title diagnosis packet: yesterday's Shopping terms had `0` clicks/cost, so no negatives or product-group edits are justified. The packet maps visible terms to paid-cohort candidates, checks US public collection routes, and defines the authenticated item-level export needed before any title/feed approval packet.
- Public-preflighted the US Shopping query/title candidate PDPs: `10/10` unique handles returned `200`, `8/10` were source-clean, and the authenticated export scope is now narrowed to `18` public-clean candidate rows. `5` rows are held for public source/stale-copy issues and `1` row needs title-fit review.
- Prepared the held-PDP repair/exclusion packet for US Shopping: `6` held/review rows across `3` handles were rechecked publicly; `3` rows stay excluded until supplier/source-clean, `2` stay excluded until stale seasonal copy is clean, and `1` source-clean weak-fit row can enter export only if item-level impressions prove relevance.
- Locally fixed the US Shopping swim-trunks stale seasonal related-card blocker: source context showed the `Christmas` hits came from related-product cards, so `snippets/buy-box-similar-styles.liquid` now skips Christmas/Santa/Xmas recommendations unless the current PDP is seasonal. The row remains excluded until approved live theme sync and public readback.
- Prepared the US Shopping authenticated export join prep: generated a read-only export template, handle-level public-clean scope, summary, and `run_us_shopping_auth_export_join_prep.py` so a future account-capable session can join item-level export rows to the public-clean scope and keep held rows out of title/feed decisions.
- Corrected the blocked GB/CA/AU packet and `keyword_universe.csv`: removed lazy close-head variants as proposed actions and replaced them with market-specific long-tail validation candidates that still require clean route proof and `$0.15` CPC validation before upload.
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
- Current active PDP sanitizer readback passed; existing stopped-session local sanitizer patch remains in place and was not rewritten.
- New keyword command files: `ops/marketing/keyword_strategy.md`, `ops/marketing/keyword_scoring_rubric.md`, and `ops/marketing/keyword_universe.csv`.
- New US Shopping diagnosis packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-query-title-diagnosis/`.
- New US Shopping held-PDP repair packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-held-pdp-repair-packet/`.
- New US Shopping seasonal related-product filter packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-seasonal-related-filter/`.
- New US Shopping authenticated export join prep packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/`.
- New integration guard: `ops/scripts/audit_marketing_command_integration.py` and generated report `ops/marketing/command_layer_integration_audit.md`.
- New broad continuity guard: `ops/scripts/check_continuity_integrity.py`.
- `ops/AGENT_WORKLOG_utf8.md` is now explicitly `HISTORICAL_DO_NOT_USE`; unique historical session titles were compared and summarized in the canonical worklog.

## Live Changes

- None in this pass.
- No live Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme publish write occurred.

## Current Blockers

- Active paid Search PDP supplier/source URL leak is currently solved by public source readback for GB/CA/AU. Future collection-route expansion is unblocked for the current GB/CA/AU validation set: `matching-dresses`, `vacation`, `daddy-and-me`, and swimwear rows were rerouted to clean collection routes. `/collections/swimsuits` itself still leaks raw Shopify product JSON supplier vendors and remains excluded.
- Merchant US/es age_group needs a current exact all-row readback before closure or repair.
- Merchant Shopping Ads capacity warning is current and account-level, but exact paid-cohort impact is still unresolved because the authenticated Merchant Chrome/account path is unavailable in this automation runtime.
- Pinterest Ads Manager remains blocked by authenticated controllable access.
- GB/CA/AU exact Search have fresh read-only Ads checks done: stale search-term filters are cleared, search terms are still empty, keyword/RSA/final URLs are enabled/country-qualified, and keyword UI shows auction-entry pressure. Live Ads action is blocked by the hard `$0.15` CPC validation gate. The exact authenticated validation packet is ready at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv`, with `36` clean-route rows and no upload authority.
- Standard Shopping has impressions but no clicks/cost/conversion evidence from the latest command-layer readback. US is still the primary market; keyword work applies through Shopping query/title/product/feed diagnostics and future US Search/Pinterest packets.
- US Standard Shopping query/title proof is now the next read-only Shopping action: local candidate mapping is ready, but item-level product/title performance export is required before any title/feed/product-group decision.
- The next US Shopping export should use the join prep at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/US_SHOPPING_AUTH_EXPORT_JOIN_PREP.md`, starting from the public-clean scope at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-public-pdp-fit-preflight/us_shopping_auth_export_public_clean_scope.csv`, not the full candidate list as a title/feed repair basis.
- Held US Shopping PDP rows have exact repair/exclusion gates now: supplier rows stay out of paid decisions until product/vendor source data is repaired and read back clean; the swim-trunks stale seasonal row has a local theme fix ready but still needs approved live sync/readback; the one source-clean weak-fit row needs authenticated item-level impression proof before it can influence title/feed decisions.
- Bounded spend authority is active, but current campaign changes still need fresh readback and quality gates before any proactive live write.
- Daily optimization ownership is now required: agents must monitor, diagnose, act inside approved caps when gates pass, and keep the dashboard current.
- Monitoring cannot be the deliverable. Every monitor/readback must end in `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- Side documents are now a tracked process defect. Current audit result: 25 tracked command-layer files, 0 side-document risks.
- Alternate worklogs are not current state. The only active worklog is `ops/AGENT_WORKLOG.md`; `ops/AGENT_WORKLOG_utf8.md` is historical evidence only.

## Next 3 Tasks

1. Run authenticated Google Ads/Keyword Planner validation for `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv` at max `$0.15`, then prepare an exact bounded action row only if auction-entry feasibility passes.
2. Run authenticated read-only Standard Shopping item-level export for campaign `23802638621`, include product URL/handle where possible, then run `python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/run_us_shopping_auth_export_join_prep.py --export-csv /path/to/authenticated-export.csv`; keep the held-PDP repair packet rows excluded unless repaired/read back clean, the local seasonal related filter is approved/live-synced/read back clean for swim-trunks rows, or item-level proof warrants the weak-fit row.
3. Use an authenticated Merchant session to intersect the live Shopping capacity warning against the `780`-row `us_test_ready` / `paid_eligible` cohort and to obtain a fresh exact US/es export/readback.

## Assumptions

- The current active PDP supplier/source sanitizer readback passed; the stopped-session sanitizer patch is intentional and should be preserved.
- The May 14 command-layer live reconciliation and paid-landing local handoff entries are current repo evidence, but live platform decisions still need fresh readbacks where noted.
- The user wants agents to act proactively inside approved paid-media caps once quality gates pass, but out-of-scope writes still need fresh exact approval.
- The current exact GB/CA/AU keyword set is a controlled starter hypothesis, not proof of the final smartest keywords; source-backed daily search-term and ROAS evidence must decide expansions, negatives, bid changes, or pauses.
- 2026 source-backed best practice favors controlled high-intent tests until conversion value, landing quality, and search-term data justify broader automation or scale.
- The owner wants aggressive AI-speed growth, which means faster daily evidence loops, long-tail ideation, bounded execution, and next-day sales/ROAS review inside guardrails; it does not mean unsafe broadening or unapproved external writes.
- The owner expects proactive fixes and improvements, not bureaucracy. Local/read-only mistakes should be fixed immediately; currently approved live mistakes should be fixed with before/after readback; unapproved live fixes should become exact approval packets.
- GB/CA/AU long-tail candidate rows are `review_only_not_uploaded`; the exact next validation scope is packetized at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/GB_CA_AU_SWIM_ROUTE_UNBLOCK_AND_36_ROW_CPC_PACKET.md`, but it is not a live-account instruction until fresh Ads readback, reviewer, route-level landing proof, `$0.15` CPC validation, and approval/bounded-authority gates pass.
- The fresh monitor made the stale search-term filter problem better, not the traffic problem: filters are clear now, but no search terms exist and auction-entry economics still block action until clean-route rows validate at `$0.15`.
- `keyword_universe.csv` is a local universe, not a live upload artifact; `GREEN` rows still need active-product, route cleanliness, `$0.15` CPC, reviewer, and after-state gates.
- US Shopping title/feed candidates are local hypotheses until an authenticated item-level export proves which product titles received impressions and whether a mismatch exists.
- Public-clean US Shopping PDP rows are still only export candidates; they are not proof of item-level demand or approval for title/feed edits.
- Held US Shopping PDP rows are exclusion/repair gates, not hidden export candidates.
- The auth-export join prep is a safety harness for the next read-only export, not proof of item-level demand and not approval to edit product/feed/title data.
- The local seasonal related-product filter is not live. It cannot make the swim-trunks PDP paid-eligible until a scoped live theme sync and public source readback pass.
- If an artifact is not wired into `AGENTS.md`, an action surface, and continuity logs, it is not progress; it is a side-document risk.
- If a prompt, packet, digest, or memory names an older anchor, resolve latest state from `ops/AGENT_WORKLOG.md` and the command layer instead.
- If this automation runtime cannot use the authenticated Chrome/account path, treat Merchant/Pinterest account readbacks as capability-mismatched and hand off the exact authenticated next step instead of claiming parity.

## Risks / Approval Needed

- Shopify product/vendor/source metadata or theme changes for blocked collection routes are external writes not automatically covered by paid-media spend authority.
- Scoped live theme sync for `snippets/buy-box-similar-styles.liquid` needs approval before it can clear the swim-trunks held rows.
- Merchant feed/source/product-scope/product-group actions require fresh exact approval.
- Pinterest object creation, campaign/ad group/product group changes, budget/bid/status changes, or catalog/source/tag/CAPI writes require approval and authenticated access.
- Any spend/budget/bid/status/feed/product/conversion recommendation must pass the reviewer checklist and cite current evidence.
- Any GB/CA/AU keyword expansion must keep language and market ownership clear: no French-Canada terms in the active English-Canada campaign, no duplicated exact keywords across live ad groups, no pajama/swim/beach intent routed to a dress PDP, no close-head-term "long tail", and no CPC above `$0.15`.
