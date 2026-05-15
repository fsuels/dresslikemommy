# Marketing Safety Review Log

Last updated: 2026-05-15 09:45 EDT

Use this log for reviewer outcomes or simulated checklist runs. Keep entries short and tied to evidence.

## 2026-05-15 - Pinterest feed grouping guard readback

Reviewer verdict: `FAIL_EXPECTED_APPROVAL_REQUIRED_NO_LAUNCH`

Checked:

- `check_pinterest_feed_grouping.py --report-only --strict` scanned `3` current snapshots.
- The result is `3` expected FAIL snapshots and `0` ERROR snapshots.
- The Pinterest exact item-ID import still exposes `30` duplicate-parent clusters without `item_group_id`.
- Two Merchant sanitized exports still show `69` duplicate market x language buckets each, worst `96x`.
- `FIX_LANDED_FRESHNESS_MARKER.txt` is placeholder-only and does not contain the attest phrase.

Required gates/fixes:

- Do not launch Pinterest, save broad product groups, or mark the feed fixed from filter payload counts alone.
- Owner approval is required for the master all-markets grouping phrase or per-market phrases.
- If the Shopify Pinterest channel UI lacks the grouping toggle, use Path B grouped TSV generation/import only under separate exact approval.
- Strict guard mode can be attested only after per-market 24h re-sync and clean after-state readbacks.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/AUTOMATION_FEED_GROUPING_QUEUE_WIRING_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/CROSS_MARKET_VARIANT_DUPLICATION_DIAGNOSIS.md`
- `ops/scripts/check_pinterest_feed_grouping.py`

Safest next sales-moving action:

- Apply the owner-approved all-markets grouping fix, then read back grouped per-market catalog output before final Pinterest launch review.

## 2026-05-15 - Merchant post-prune after-export guard

Reviewer verdict: `FAIL_CLOSED_SHOPPING_BLOCKED`

Checked:

- Shopify-side cleanup report says only the `52` approved first-pass `International` regions were removed, leaving `21` regions and preserving separate priority markets plus duplicate `CA`/`AU`.
- Fresh Merchant browser-RPC export still has `351,007` rows.
- After-export guard failed with `199,684` remaining first-pass removal rows.
- Target rows remain absent: Canada English `0`, Canada French `0`, GB English `0`.

Required gates/fixes:

- Do not repeat the same Shopify region prune.
- Do not build Canada/GB Shopping or change campaigns/product groups from absent rows.
- Next valid path is Google & YouTube/Merchant publishing sync/control readback or delayed re-export until the after-export guard passes and target rows exist.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/SHOPIFY_INTERNATIONAL_REGION_PRUNE_EXECUTION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_POST_SHOPIFY_REGION_PRUNE_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`

Safest next sales-moving action:

- Read back the Google & YouTube/Merchant publishing controls or wait for propagation, then rerun `build_merchant_capacity_execution_guard.py --after-export` on a fresh export before any Shopping build.

## 2026-05-15 - Pinterest exact group import readback

Reviewer verdict: `HOLD_NO_LAUNCH_PRODUCTS_ZERO`

Checked:

- Exact item-ID import readback reports filter payload counts Mommy & Me `201`, Family Matching `103`, Pajamas `29`.
- Group detail pages still show `0` selected/products, empty previews, `Promote` disabled, and a 24-hour update message.

Required gates/fixes:

- Do not launch, save broad fallback groups, or rely on the imported filter payload alone.
- Fresh readback must show usable exact product counts before final launch review.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/PINTEREST_EXACT_PRODUCT_GROUP_IMPORT_READBACK.md`

Safest next sales-moving action:

- Re-read the exact product groups after Pinterest resolves the import; launch only if counts and max `$5/day` / `$0.15` CPC gates still pass.

## 2026-05-15 - Merchant capacity live-execution approval packet

Reviewer verdict: `PASS_WITH_EXACT_APPROVAL_AND_PREVIEW_GATES`

Checked:

- Packet generation was local/read-only and made no external calls or writes.
- The packet ties the Merchant `41` exact preview rows and Shopify `52/73` first-pass `International` region removals into one action-time approval phrase.
- It preserves USA English `5,491`, USA Spanish `5,412`, separate Canada/United Kingdom/Eurozone/Australia markets, Europe-later groups, duplicate `CA`/`AU` hold rows, and all hold-review rows.
- It requires a fresh Merchant all-products export and after-export guard before Canada English/French or GB English Shopping can be considered.

Required gates/fixes:

- Do not use the packet as live authority unless the exact approval phrase is present in the current session.
- Do not save if the authenticated platform preview cannot reconcile to both `merchant_capacity_platform_preview_acceptance.csv` and `shopify_international_region_prune_preview.csv`.
- Do not delete products, change product data, request capacity, or mutate campaigns/product groups/bids/budgets/statuses/conversions.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_CAPACITY_LIVE_EXECUTION_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_live_execution_checklist.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_live_execution_packet_summary.json`

Safest next sales-moving action:

- Get the exact approval phrase, reconcile the live preview to both guard CSVs, then run the scoped cleanup and after-export guard in an authenticated account-capable session.

## 2026-05-15 - Merchant browser RPC source/status addendum

Reviewer verdict: `PASS_WITH_GATES_SOURCE_CONFIRMED_NO_REPAIR`

Checked:

- Browser RPC export was read-only and stored no cookies, tokens, or request headers.
- The sanitized product-list snapshot captured `351,007` rows, matching the all-products denominator.
- `US/es` source `10627981690` has `5,412` rows; `4,910` have strict-approved raw product-list status.
- CA/en, GB/en, and AU/en still have `0` English CAD/GBP/AUD rows.

Required gates/fixes:

- Do not use raw product-list status to override current issue-export/capacity blockers.
- Use the TSV packet's target paid-label count for paid-cohort sizing and the issue/classification packets for repair priority.
- No Merchant repair, feed/source, campaign, product-group, bid, budget, status, capacity, or conversion action is justified without exact approval.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/MERCHANT_SOURCE_ELIGIBILITY_BROWSER_RPC_EXPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-eligibility-browser-rpc-export/merchant_source_eligibility_browser_rpc_summary.json`

Safest next sales-moving action:

- Keep Shopping decisions blocked; pursue either CA/GB/AU feed availability proof or a narrow owner-approved `US/es` repair/capacity/source packet.

## 2026-05-15 - Merchant all-products source eligibility export

Reviewer verdict: `PASS_WITH_GATES_NO_SHOPPING_BUILD`

Checked:

- Merchant all-products download was read-only; no upload, source sync, product edit, campaign, budget, bid, status, product-group, conversion, or billing write occurred.
- `US/es` row presence is real (`5,412` rows / `772` paid-cohort rows), but current issue-export and capacity evidence still block Shopping build or repair authority.
- CA/en, GB/en, and AU/en have `0` rows and no expected currency/feed-label proof in the current all-products export.
- The TSV lacks `source_id` and approved/disapproved destination status, so decisions fail closed.

Required gates/fixes:

- Do not create Shopping campaigns, product groups, feed/title edits, product-scope changes, capacity requests, bids, budgets, statuses, or conversion changes from this export.
- For CA/GB/AU, obtain feed/source availability proof before any Shopping build packet.
- For `US/es`, use a narrow owner-approved repair/capacity/source packet only after source/approval proof is sufficient.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/MERCHANT_ALL_PRODUCTS_SOURCE_ELIGIBILITY_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-source-all-products-export-attempt/merchant_all_products_source_eligibility_summary.json`

Safest next sales-moving action:

- Route Shopping work to feed/source availability unblocks and conversion/landing analysis, while CPC forecast remains parked until Basic Access approval.

## 2026-05-15 - Pinterest live launch CPC and category-scope gate

Reviewer verdict: `BLOCKED_NO_BROAD_PRODUCT_GROUP_LAUNCH`

Checked:

- Owner approved launch for advertiser `549756244483` using the refreshed `333` clean scope, max `$5/day`, and hard max `$0.15` CPC.
- Live UI can enforce `$0.15` CPC only with `Pin clicks` optimization plus `Custom` bidding; ROAS optimization forces Pinterest Performance+ bidding and disables custom CPC.
- Product-group selector did not expose exact `333` / custom-label groups; it exposed broad groups such as `All Products`, broad Family Matching, Mommy & Me, and Pajamas groups.

Required gates/fixes:

- Do not publish broad groups unless a current readback proves every included product is active, sellable, source-clean, and inside the approved scope.
- Use exact category product groups: Mommy & Me `201`, Family Matching `103`, Pajamas `29`, and Daddy & Me/father-inclusive only after active clean feed proof.
- If creating/exposing Pinterest product groups is required, get exact approval for that object mutation first.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-live-launch-cpc-scope-blocker/PINTEREST_LIVE_LAUNCH_CPC_SCOPE_BLOCKER.md`

Safest next sales-moving action:

- Create or expose exact active-clean Pinterest category product groups, then launch only with max `$5/day` and max `$0.15` CPC after final review.

## 2026-05-15 - US Shopping item export and clicked PDP readback

Reviewer verdict: `PASS_NO_LIVE_WRITE_ACTION`

Checked:

- Authenticated Standard Shopping product export was read-only and joined through the public-clean/held scope classifier.
- Parser found `0` title/feed approval candidates.
- Clicked-PDP public readback passed `26/26` fetches and found `0` source-blocked clicked handles.
- Conversion value remained `$0.00`, so clicks are learning evidence but not ROAS proof.

Required gates/fixes:

- Do not change titles, feed attributes, product groups, bids, budgets, statuses, negatives, product scope, campaigns, or theme files from this evidence alone.
- Continue with current Merchant `US/es` source export and CA/GB/AU English Shopping eligibility readbacks.
- Convert only a proven narrow mismatch or clean product-expansion opportunity into an exact owner approval packet before any live write.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/US_SHOPPING_AUTH_EXPORT_JOIN_PREP.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-pdp-readback/STANDARD_SHOPPING_CLICKED_PDP_PUBLIC_READBACK.md`

Safest next sales-moving action:

- Run read-only Merchant/feed eligibility for `US/es`, then CA/GB/AU English Shopping, while Pinterest remains approval-gated and GB/CA/AU Search CPC remains Basic-Access gated.

## 2026-05-14 - Authenticated GB/CA/AU CPC validation attempt

Reviewer verdict: `BLOCKED_NO_PASS_ROWS`

Checked:

- Existing authenticated Google Ads access was used; no generic access blocker was opened.
- Keyword Planner accepted the `72` exact/phrase inputs, but exported context stayed `United States`, `All languages`, `Broad`, `Maximize conversions`.
- Parser consumed the real Google UTF-16/TSV exports and returned `0` `PASS_015_CPC_GATE` rows.

Required gates/fixes:

- Do not create a `GREEN` live action row.
- Retry through Google Ads API KeywordPlan forecast or a UI path with explicit GB/CA/AU, exact/phrase, keyword-level max `$0.15` proof.
- Do not upload/apply/add keywords, change bids/statuses/budgets, or add negatives from the invalid US/Broad export.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-authenticated-gb-ca-au-cpc-validation/AUTHENTICATED_GB_CA_AU_CPC_VALIDATION_ATTEMPT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-authenticated-gb-ca-au-cpc-validation/saved_keywords_stats_parser_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-authenticated-gb-ca-au-cpc-validation/all_keywords_forecast_parser_summary.json`

Safest next sales-moving action:

- API-backed or correctly scoped UI-backed GB/CA/AU exact/phrase max `$0.15` forecast export; if still unavailable, continue Standard Shopping authenticated item export or Pinterest paused draft lane.

## 2026-05-14 - P0 blocker board cleanup

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Solved account-access protocol and Pinterest access readback rows were not left as active P0 blockers.
- The remaining P0 is an exact authenticated Google Ads / Keyword Planner validation gate, not live upload authority.
- Pinterest remains no-write unless the approved paused draft spec and stop conditions are followed.

Required gates/fixes:

- Do not upload/apply/add keywords, change bids/statuses/budgets, or add negatives until authenticated `$0.15` CPC rows parse as `PASS_015_CPC_GATE` and a fresh `GREEN` action row exists.
- Do not reopen generic account-access P0 blockers without completing `ops/ACCOUNT_ACCESS_PROTOCOL.md`.

Evidence:

- `ops/marketing/blocker_board.md`
- `ops/marketing/action_queue.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-current-p0-blocker-fix/PINTEREST_EXISTING_DRAFT_CHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/GB_CA_AU_CPC_VALIDATION_DECISION_KIT.md`

Safest next sales-moving action:

- Authenticated `$0.15` CPC validation for the canonical 36-row GB/CA/AU packet.

## 2026-05-14 - Account access recovery protocol

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local protocol and operating-doc edits only.
- No password, token, cookie, recovery code, or secret value was written to files or evidence.
- Account access and live write authority remain separate: authenticated access does not authorize spend, product/feed changes, campaign changes, or credential mutations.

Risks:

- Future agents may still face MFA, CAPTCHA, account chooser ambiguity, or permission prompts that require owner action.
- Current-session credentials cannot be made durable in the repo; only the protocol and secure non-repo source rules can be durable.

Required gates/fixes:

- Complete `ops/ACCOUNT_ACCESS_PROTOCOL.md` before declaring any account blocked.
- Use `ACCESS_RECOVERY_REQUIRED`, `MFA_OR_CAPTCHA_REQUIRED`, `PERMISSION_REQUIRED`, or `ACCOUNT_SWITCH_REQUIRED` instead of generic P0 access blockers unless the access is required for the next approved action and the ladder has failed.
- Do not save or persist owner credentials.

Evidence:

- `ops/ACCOUNT_ACCESS_PROTOCOL.md`
- `ops/BROWSER_SUBAGENT_COORDINATION.md`
- `ops/marketing/AGENTS.md`
- `AGENTS.md`

Safest next sales-moving action:

- Start the next authenticated Ads/Pinterest/Merchant readback by claiming the existing authenticated tab/session first, then run the already-prepared read-only validation/export tasks.

## 2026-05-14 - US Shopping seasonal related-product filter local fix

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local theme edit only in `snippets/buy-box-similar-styles.liquid`.
- Public source-context readback separated the dynamic swim-trunks stale seasonal blocker from the sequin lace supplier/source vendor blocker.
- Theme Check returned `[]`.

Risks:

- This is not live on Shopify until an approved scoped theme sync occurs.
- The sequin lace PDP supplier/source leak is Shopify injected `product.vendor` data and still needs product-data approval or exclusion; the related-product filter does not fix that handle.

Required gates/fixes:

- Do not include the swim-trunks held rows in paid export/use until the local theme change is live-synced and public source readback shows `0` stale seasonal hits.
- Do not edit Shopify product/vendor/source fields, Merchant feeds, Ads, budgets, bids, statuses, conversion goals, or product groups without the exact approval gate.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-seasonal-related-filter/US_SHOPPING_SEASONAL_RELATED_FILTER_LOCAL_FIX.md`
- `snippets/buy-box-similar-styles.liquid`

Safest next sales-moving action:

- Run authenticated Standard Shopping item-level export from the public-clean scope, and separately request scoped live theme sync only if the owner wants the swim-trunks held rows eligible later.

## 2026-05-14 - Automation capability mismatch plus Merchant capacity local diagnosis

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local capability inventory only: shell, repo writes, network, Playwright MCP, Chrome DevTools MCP visibility, Computer Use visibility, GitHub MCP visibility, and OpenAI docs MCP.
- Repo-local/read-only Merchant capacity diagnosis from already-saved evidence plus current command-layer state.
- No external writes, no blocker closure without proof, and no Merchant/Shopping recommendation that exceeds approval boundaries.

Risks:

- Authenticated Merchant and Pinterest account-surface readbacks are not equivalent in this runtime because Chrome DevTools is profile-locked and Computer Use interactive access is not granted.
- The current capacity warning is real, but the exact paid-cohort intersection is still unproven; Standard Shopping still had `17` impressions yesterday, so the warning could be broad account noise.

Required gates/fixes:

- Mark the account-surface gap explicitly as `AUTOMATION_CAPABILITY_MISMATCH`.
- Do not downgrade or close the Merchant capacity blocker from local evidence alone.
- Next Merchant action must be an authenticated read-only product-level intersection against the `780`-row `us_test_ready` / `paid_eligible` cohort.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-capability-merchant-capacity-diagnosis/AUTOMATION_CAPABILITY_AND_MERCHANT_CAPACITY_DIAGNOSIS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/merchant-product-issues-export/raw/product-issues-browser-export/diagnostics_page_text_before_download_priority.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/standard-shopping-readback/raw/01_productgroups_initial.txt`

Safest next sales-moving action:

- Use an authenticated Merchant session to prove whether the capacity warning touches the live paid cohort; keep the next independent sales-moving lanes active meanwhile.

## 2026-05-14 - Reviewer/cockpit implementation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local implementation of `marketing_safety_reviewer`, cockpit, assumption log, checklist, review log, marketing guide updates, Head of Growth instruction update, team registry update, prompt log update, and worklog anchor.
- Stopped-session dirty changes before editing, including supplier/source URL sanitizer changes and May 14 marketing command-layer updates.
- Spend authorization boundary.

Risks:

- Existing paid-landing sanitizer is still local only; live paid landing remains blocked for expansion until approved theme sync and public readback.
- Existing dirty worktree includes unrelated theme and command-layer changes that this implementation must preserve.

Required gates/fixes:

- Do not publish the sanitizer or mutate external marketing systems without fresh explicit approval.
- Keep `spend_authorization.md` at `PENDING_OWNER_APPROVAL` unless owner approves activation.

Evidence:

- `git status --short`
- `ops/AGENT_WORKLOG.md` latest anchors, especially `2026-05-14-paid-landing-vendor-source-sanitizer-local`
- `ops/marketing/current_marketing_state.md`
- `ops/marketing/spend_authorization.md`

Safest next sales-moving action:

- Seek scoped approval for live theme sync of the sanitizer files, or continue read-only Merchant/Pinterest unblock work if approval is unavailable.

## 2026-05-14 - Campaign explorer dashboard implementation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard and command-layer edits only: `campaign_explorer.json`, cockpit renderer, cockpit source, prompt log, marketing guide, and worklog anchor.
- Campaign details are sourced from saved repo evidence and are labeled when stale, blocked, or not live-verified.
- No supplier/source URL domains are exposed in the human dashboard data.
- Spend authorization boundary remains unchanged.

Risks:

- Google Ads and Pinterest facts shown in the campaign explorer are saved readback evidence, not a fresh live read performed during this UI-only pass.
- Pinterest remains not active from this plan because authenticated controllable Ads Manager access is blocked.
- Ad strength for GB/CA/AU exact Search is `Pending`; zero-data campaigns must not be optimized from assumptions.

Required gates/fixes:

- Do not change budgets, bids, statuses, keywords, ads, product groups, feed/product scope, or Pinterest objects without fresh explicit approval and fresh before/after readbacks.
- Keep `campaign_explorer.json` current after every material live readback or decision.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `ops/marketing/current_marketing_state.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/LIVE_RECONCILIATION_REPORT.md`

Safest next sales-moving action:

- Obtain scoped approval for live theme sync/readback of the paid-landing sanitizer, or continue read-only Merchant/Pinterest unblock lanes if approval is unavailable.

## 2026-05-14 - Proactive test monitor dashboard upgrade

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard/data/doc updates only; no platform surfaces or live account writes.
- Active campaign monitor fields now distinguish saved readback evidence from fresh-readback gaps.
- Zero-impression tests now show activation time, T+24/T+72/T+7d clock, assumptions, and improvement triggers.

Risks:

- Today 2026-05-14 Google Ads metrics are not live-read in this UI pass; the cockpit labels them as fresh readback needed.
- Any bid, budget, status, keyword, ad, product group, feed, conversion, or Pinterest object change still needs fresh explicit approval.

Required gates/fixes:

- Run fresh read-only live metrics before any optimization recommendation.
- Treat T+72 zero-impression state as a diagnosis/approval-packet trigger, not proof that a live change is already approved.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `GB_CA_AU_FIRST_72H_OPTIMIZATION_PLAN.md`
- `final_success_summary.json`

Safest next sales-moving action:

- Fresh read-only monitor for today/yesterday GB/CA/AU metrics and Shopping/Pinterest blockers, then decide whether a T+72 zero-impression diagnosis packet is needed.

## 2026-05-14 - Success measure, bid strategy, and full attention checklist

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local dashboard/data/doc updates only; no platform surfaces or live account writes.
- Success measurement is now explicit: maximize profitable sales while targeting about `650% ROAS`, with CPA/ROAS/conversion-value proof before scale.
- Campaign detail now distinguishes Manual CPC from Maximize Clicks and explains why the saved strategy was chosen.
- Full attention checklist now covers bidding, keyword quality/Quality Score, search terms, RSA/ad quality, landing page, product/photo fit, measurement, and decision discipline.

Risks:

- Quality Score columns and today metrics were not live-read in this UI pass; the cockpit labels them as required readbacks.
- Any bid strategy change, including Maximize Clicks, is a live campaign write and still needs fresh exact approval.

Required gates/fixes:

- Run fresh read-only quality/metric readbacks before any bid, budget, keyword, ad, landing, product-group, or scale/pause recommendation.
- Keep final success tied to profitable sales and about `650% ROAS`; do not treat clicks, CTR, or ad strength as the final win condition.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `ops/marketing/operator_cockpit.html`
- `ops/marketing/daily_scorecard.md`
- `ops/marketing/AGENTS.md`

Safest next sales-moving action:

- Fresh read-only monitor for today/yesterday metrics plus keyword quality/ad/landing diagnostics, then prepare a T+72 serving-diagnosis packet if GB/CA/AU remain zero-impression.

## 2026-05-14 - Bounded proactive spend authority activation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Owner authorized spending within the set limits as long as actions respect the sales/ROAS goals.
- `spend_authorization.md` now says `APPROVED_ACTIVE` with `$80/day` total paid-media cap and `$5/day` new/test campaign cap.
- Agent rules now require proactive monitoring and green-gated bounded action when quality gates pass.
- Excluded surfaces remain excluded: billing, conversion goals, PMax, unresolved remarketing, Merchant feed/source/product-scope changes, Shopify product/price/discount/policy/theme publish, unreviewed native-language ads, and actions above caps.

Risks:

- Active authority can be misused if agents skip quality checks or treat diagnostic metrics as final success.
- Current GB/CA/AU and Shopping data still do not justify an immediate bid/budget/status write without fresh readback and quality diagnostics.
- Paid-media spend authority does not automatically approve live Shopify theme sanitizer sync or Merchant/Pinterest catalog/source writes.

Required gates/fixes:

- Use authority only for green-gated rows in `action_queue.md`.
- Before any live action, save before-state readback, check bid strategy, keyword/search-term quality, Quality Score or missing quality columns, ad/RSA quality, product/photo fit, landing page, measurement, blockers, and path to profitable sales at about `650% ROAS`.
- Save after-state readback and update command-layer files.

Evidence:

- Owner message in current session.
- `ops/marketing/spend_authorization.md`
- `ops/marketing/action_queue.md`
- `ops/marketing/AGENTS.md`

Safest next sales-moving action:

- Fresh read-only monitor today/yesterday metrics and quality diagnostics, then execute only green-gated bounded actions if gates pass; otherwise document the exact blocker or diagnosis packet.

## 2026-05-14 - Keyword discipline and continuous improvement ownership

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Campaign Explorer now records keyword selection criteria, negative-keyword criteria, daily optimization owner, and continuous improvement loop.
- GB/CA/AU exact keywords are labeled as a controlled starter hypothesis, not guaranteed-smart final keywords.
- Negative watchlist is labeled `watch_only_not_uploaded`; actual negative uploads require search-term evidence.
- Agents now have explicit responsibility for daily monitoring, action triggers, and dashboard continuity.

Risks:

- Without fresh search-term and quality readbacks, keyword quality cannot be proven today.
- Bounded authority should not turn watchlist terms into negatives without evidence.

Required gates/fixes:

- Daily Google Ads monitor must include keyword/search-term quality, Quality Score or missing quality-column readback, ad/RSA quality, landing/product/photo fit, conversion value, CPA, and ROAS.
- Expand, pause, or negative-match only from daily data and green-gated reviewer-cleared decisions.

Evidence:

- `ops/marketing/campaign_explorer.json`
- `gb_ca_au_negative_watchlist.csv`
- `GB_CA_AU_1700_ZERO_DATA_DECISION_UPDATE.md`
- `GB_CA_AU_1721_ZERO_DATA_DECISION_UPDATE.md`

Safest next sales-moving action:

- Run the daily read-only Google Ads monitor and record whether the current keywords are producing impressions, qualified search terms, clicks, conversions, and progress toward `650% ROAS`.

## 2026-05-14 - 2026 expert playbook, personas, and anti-cannibalization

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local strategy/dashboard/agent updates only; no platform surfaces or live account writes.
- `expert_growth_playbook_2026.md` cites Google Ads Help, Pinterest Business, OpenAI, and Anthropic sources for match types, search-term evidence, negatives, Target ROAS readiness, Quality Score, landing/ad quality, creative/clickthrough fit, and agent guardrails.
- Campaign Explorer now exposes expert source standard, keyword economics/low-waste test, and anti-cannibalization rules.
- Agent personas now require senior specialist ownership instead of passive audit behavior.

Risks:

- Source-backed strategy still needs fresh live campaign/account data before any actual optimization.
- Broad/automated strategies are not rejected forever, but they remain gated until purchase value, landing quality, and search-term evidence justify them.

Required gates/fixes:

- Before any live recommendation, run the reviewer checklist, save fresh readbacks, and prove high-intent/low-waste economics, no self-cannibalization, and path to about `650% ROAS`.
- Do not treat this playbook as live-write approval.

Evidence:

- `ops/marketing/expert_growth_playbook_2026.md`
- `ops/marketing/campaign_explorer.json`
- `ops/marketing/reviewer_checklist.md`
- `.codex/agents/*.toml`

Safest next sales-moving action:

- Run the fresh daily Google Ads/Shopping read-only monitor and use the playbook rubric to decide whether GB/CA/AU need serving diagnosis, keyword expansion, negatives, bid review, landing repair, or continued hold.

## 2026-05-14 - Day 1 growth urgency and 24-hour zero-impression rule

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local command-layer and agent instruction updates only; no platform surfaces or live account writes.
- Owner directive that each day without growing sales is a failure signal and that zero impressions after one day requires action.
- Current saved GB/CA/AU evidence already shows T+24 zero-impression state, so the command layer now treats same-day diagnosis and long-tail/auction-entry planning as due.

Risks:

- Aggressive growth language could be misread as permission to skip approval, quality, measurement, or live-readback gates.
- Long-tail candidates still require evidence, landing fit, no self-cannibalization, and reviewer pass before live upload or bid/status action.

Required gates/fixes:

- Tomorrow's scorecard must report sales, revenue, CPA, ROAS, progress, and exact next action.
- Any live keyword, bid, budget, ad, status, or campaign change must remain inside `APPROVED_ACTIVE` caps or fresh exact approval and pass reviewer gates.

Evidence:

- Owner message in current session.
- `ops/marketing/expert_growth_playbook_2026.md`
- `ops/marketing/action_queue.md`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Run the Day 1 sales/ROAS monitor and GB/CA/AU zero-impression diagnosis, then build high-buyer-intent long-tail candidates with exact anti-cannibalization ownership and landing fit.

## 2026-05-14 - GB/CA/AU Day 1 keyword strategy repair

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local/read-only keyword strategy repair for active GB/CA/AU exact Search campaigns.
- Official Google Ads docs for Target ROAS math/traffic limits, low-search-volume behavior, exact/phrase/broad match controls, Quality Score components, and ad/landing relevance.
- Market/language candidate maps for GB English-UK, CA English-Canada with French-Canada gated separately, and AU English-Australia.
- No live keyword, ad, negative, bid, budget, status, campaign, feed, product, conversion, or theme write.

Risks:

- Latest Ads metrics are saved `2026-05-14 05:34 EDT` readbacks for reporting day `2026-05-13`; a fresh live monitor is still needed before any live action.
- CA/AU search-term pages remain non-actionable while the stale `Keyword: "human hair wigs"` filter is present.
- Active paid landing expansion still depends on approved live sanitizer sync/readback.

Required gates/fixes:

- Fresh before-state Google Ads readback with CA/AU filters clear, Quality Score/RSA/final URL checks, and current metrics.
- Reviewer pass for any exact keyword/ad/bid/status action.
- Live paid landing supplier/source sanitizer readback before traffic expansion.
- After-state readback and command-layer logging for any future live action.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/GB_CA_AU_DAY1_ZERO_IMPRESSION_KEYWORD_STRATEGY_REPAIR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/gb_ca_au_high_intent_candidate_map.csv`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Run the fresh read-only GB/CA/AU monitor and, only if gates pass, prepare an exact-scope bounded action packet for market-language long-tail exact/phrase rows or auction-entry changes.

## 2026-05-14 - Fresh GB/CA/AU Ads monitor and landing gate

Reviewer verdict: `BLOCK`

Checked:

- Fresh read-only Google Ads CDP/RPC/UI monitor for GB, CA, and AU.
- Search-term filter-chip removal only; no Ads entity mutation.
- Quality Score/Exp. CTR/ad relevance/landing page experience columns present in keyword UI.
- RSA/ad status and final URLs through read-only RPC and UI captures.
- Public GB/CA/AU landing source sanitizer readback.

Risks:

- All active final URLs still expose `[source-host-redacted]` in `data-analytics-vendor`, which violates paid-landing and supplier/source guardrails.
- The active exact keywords are `Eligible (Limited)` because `$0.15` max CPC is below first-page estimates around `$0.65-$0.74`; raising bids into generic head terms would be risky without a clean landing and conversion-value proof.
- Search terms are filter-clean now but still empty/no terms, so no negative action is justified.

Required gates/fixes:

- Scoped live theme sanitizer sync/readback must pass on GB/CA/AU final URLs before any keyword, bid, status, or traffic expansion.
- Rerun fresh Ads monitor and reviewer gate after landing is live-clean.
- Keep the exact-scope action packet `BLOCKED_DO_NOT_UPLOAD_OR_APPLY` until gates pass.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/FRESH_GB_CA_AU_ADS_MONITOR_AND_GATE_REVIEW.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Safest next sales-moving action:

- Get approval for scoped live theme sanitizer sync/readback, then rerun the GB/CA/AU monitor and only then decide whether the blocked long-tail exact packet can become a bounded live action.

## 2026-05-14 - $0.15 CPC long-tail packet correction

Reviewer verdict: `BLOCK_WITH_CORRECTION`

Checked:

- Owner hard CPC correction: clicks above `$0.15` are not acceptable for the current active Search repair.
- Fresh keyword UI readback showing active head terms below first page at `$0.65-$0.74`.
- Blocked packet rows that still proposed close head variants.
- Repo-local packet/doc correction only; no Ads or Shopify external write.

Risks:

- Close head variants can look localized while still entering the same expensive auction.
- Product-specific long tails may have low search volume; they still require read-only planner/keyword UI validation before upload.
- Live landing supplier/source URL leak still blocks traffic expansion.

Required gates/fixes:

- No bid above `$0.15`.
- No upload of `[mummy and me dresses]`, `[mommy and me dresses canada]`, `[mummy and me dresses australia]`, or other close-head variants as "long tail."
- Candidate rows must be market-specific, buyer-moment/product-specific, landing-fit, and validated at `$0.15` before live action.
- Live sanitizer readback must pass before any traffic expansion.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/CPC_015_LONG_TAIL_CORRECTION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-fresh-gb-ca-au-ads-monitor/exact_scope_bounded_action_packet_blocked.csv`

Safest next sales-moving action:

- Sync/read back the live landing sanitizer after explicit approval, then validate only the corrected long-tail candidates at `$0.15` before any bounded upload.

## 2026-05-14 - Expert keyword factory criteria

Reviewer verdict: `PASS_LOCAL`

Checked:

- Repo-local criteria file only; no platform or live account write.
- Hard `$0.15` CPC cap and `650% ROAS` math.
- Large local universe plus small validated live batch rule.
- Fix-now rule for mistakes found during execution.

Risks:

- A big local universe still needs actual Keyword Planner/keyword UI validation before live use.
- A clean keyword list cannot overcome the live landing supplier/source leak by itself.

Required gates/fixes:

- Live uploads require clean landing readback, `$0.15` CPC validation, reviewer pass, exact row scope, and after-state readback.
- For unapproved live writes, produce the exact smallest approval packet instead of stopping at a passive blocker.

Evidence:

- `ops/marketing/keyword_factory_015_cpc_criteria.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Safest next sales-moving action:

- After landing sanitizer approval/sync, build the large local keyword universe and validate the highest-scoring exact rows at `$0.15` before upload.

## 2026-05-14 - US primary keyword correction

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner correction that US is the biggest market.
- Current command layer: US live lane is Standard Shopping; GB/CA/AU are active Search keyword repair lanes.
- Repo-local criteria/doc updates only.

Risks:

- Operators may mistake non-US Search urgency for overall market priority.
- Shopping does not accept manual keywords, so US keyword work must feed title/feed/query/product diagnostics and future Search/Pinterest packets.

Required gates/fixes:

- Keep US first in keyword universe generation.
- Do not mutate Shopping feed/product groups/titles/bids/status without approval.
- Do not upload US Search rows without `$0.15` validation, clean landing, reviewer pass, and after-state readback plan.

Evidence:

- `ops/marketing/us_primary_keyword_lane.md`
- `ops/marketing/keyword_factory_015_cpc_criteria.md`
- `ops/marketing/campaign_explorer.json`

Safest next sales-moving action:

- Build the US-first local keyword universe and use it to diagnose Standard Shopping query/product/title fit, while keeping live writes gated.

## 2026-05-14 - Proactive action/results mandate

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner directive that results and actions matter more than monitor loops.
- Repo-local durable operating-doc updates only.
- No live account or production write.

Risks:

- Action language could be misread as permission to skip approval gates.
- Monitoring still matters when it produces a decision or proves no action is currently valid.

Required gates/fixes:

- Fix immediately when local/read-only or current approval covers the action.
- For unapproved live writes, prepare the exact smallest approval packet and keep other safe work moving.
- Every monitor/readback must end in a concrete result category, not vague observation.

Evidence:

- `AGENTS.md`
- `ops/marketing/AGENTS.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/marketing/expert_growth_playbook_2026.md`

Safest next sales-moving action:

- Use the next live/read-only finding to either fix now, execute an approved bounded action, or produce the exact approval packet.

## 2026-05-14 - Action-biased keyword universe and scoring rubric

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner requested the expert model: large local keyword universe, small validated live batches.
- New files are local docs/data only: `keyword_strategy.md`, `keyword_scoring_rubric.md`, and `keyword_universe.csv`.
- No live Google Ads, Shopify, Merchant, Pinterest, GA4/GTM, billing, bid, budget, status, keyword, ad, feed, product, conversion, or theme write occurred.
- CSV validation passed: `105` rows, `60` US, `15` GB, `15` CA, `15` AU; scores sum correctly and thresholds match the rubric.

Risks:

- Future operators could mistake `GREEN` for upload-ready instead of validation-ready.
- Landing and CPC gates still block GB/CA/AU live expansion.

Required gates/fixes:

- Before live use: active-product fit, clean landing route, `$0.15` CPC validation, anti-cannibalization owner, reviewer pass, exact `action_queue.md` row, and after-state readback plan.
- `YELLOW` rows stay local unless used as a bounded phrase-discovery repair; `RED` rows are not paid-Search upload candidates.

Evidence:

- `ops/marketing/keyword_strategy.md`
- `ops/marketing/keyword_scoring_rubric.md`
- `ops/marketing/keyword_universe.csv`
- `ops/marketing/spend_authorization.md`

Safest next sales-moving action:

- Validate top US `GREEN` rows against Standard Shopping queries/product titles and validate GB/CA/AU `GREEN` rows only after the paid landing sanitizer is live-clean.

## 2026-05-14 - Command-layer integration guard

Reviewer verdict: `PASS_LOCAL`

Checked:

- Owner identified side documents without follow-up as a critical process failure.
- Added `ops/scripts/audit_marketing_command_integration.py`.
- Generated `ops/marketing/command_layer_integration_audit.md`.
- Initial audit found `4` risks; current rerun reports `25` tracked files and `0` side-document risks.

Risks:

- The guard only covers files under `ops/marketing/`; audit packets and broader `ops/` history remain evidence stores and still need normal tracker/worklog discipline.

Required gates/fixes:

- Any new `ops/marketing/` artifact must be registered, action-linked, continuity-logged, or marked generated/archive.
- Future closeouts must run the audit when command-layer files are created or materially changed.

Evidence:

- `ops/scripts/audit_marketing_command_integration.py`
- `ops/marketing/command_layer_integration_audit.md`
- `ops/marketing/AGENTS.md`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Keep using `action_queue.md`, `current_marketing_state.md`, and `operator_cockpit.md` as the execution surfaces; do not let new strategy docs bypass them.

## 2026-05-14 - Post-sanitizer landing and collection-route preflight

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Active GB/CA/AU Search PDP final URLs were read public-only with two header/cache variants.
- Supplier/source-domain and URL-like brand attribute counts are now `0` on the current active PDP final URLs.
- Top keyword-universe collection routes were preflighted before treating long-tail candidates as ready for live validation.
- `keyword_universe.csv` row-level `live_action` holds were updated for routes that failed route cleanliness.
- No live Google Ads, Shopify Admin, Shopify theme push, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, keyword, feed, product, conversion, or destructive write occurred.

Risks:

- A clean current PDP final URL does not make collection-routed keyword rows upload-ready.
- `/collections/matching-dresses` and `/collections/swimsuits` still expose raw Shopify product JSON supplier vendors.
- `/collections/vacation` returns `404`.
- `/collections/daddy-and-me` has Christmas pattern metadata hits that may be a paid-landing mismatch.
- Authenticated `$0.15` CPC validation is still missing for clean-route rows.

Required gates/fixes:

- Validate only clean-route rows (`mommy-and-me`, `family-matching`, `pajamas`) in authenticated Google Ads/Keyword Planner at max `$0.15`.
- Keep blocked routes held until repaired, rerouted, or excluded.
- Do not edit Shopify product/vendor/source metadata without fresh explicit approval.
- Do not upload/apply/add keywords, raise bids, change budgets/statuses, or add negatives until exact row scope, fresh readback, reviewer pass, and after-state readback plan exist.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-paid-landing-post-sanitizer-readback/PAID_LANDING_POST_SANITIZER_AND_COLLECTION_PREFLIGHT.md`
- `ops/marketing/keyword_universe.csv`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Run authenticated `$0.15` CPC/auction validation for clean-route GB/CA/AU `GREEN` rows only.

## 2026-05-14 - GB/CA/AU keyword route reroute

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local `keyword_universe.csv` reroute only; no Google Ads, Shopify Admin, live theme, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or destructive write.
- Public source readbacks for `/collections/mommy-and-me`, `/collections/family-matching`, and `/collections/pajamas` across GB/CA/AU.
- CSV parse/count validation after reroute.
- Supplier leak source diagnosis: Shopify automatic `window.ShopifyAnalytics.meta` product JSON, not the sanitized theme `data-analytics-*` attributes.

Risks:

- Reroute improves route cleanliness but is not upload approval.
- Some rerouted rows use broader clean routes, so active-product/product-fit review still matters before live action.
- `/collections/swimsuits` remains supplier-leaking and no clean swim-specific route was proven.
- Authenticated `$0.15` CPC validation is still missing because this automation runtime has an account-surface capability mismatch.

Required gates/fixes:

- Validate only the `31` clean-route GB/CA/AU `GREEN` rows in authenticated Google Ads/Keyword Planner at max `$0.15`.
- Keep `5` swimwear rows held until a clean swim-specific route exists or product/vendor-source repair is approved and read back.
- Do not upload/apply/add keywords, raise bids, change budgets/statuses, or add negatives until exact row scope, fresh readback, reviewer pass, and after-state readback plan exist.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-paid-landing-post-sanitizer-readback/GB_CA_AU_KEYWORD_ROUTE_REROUTE_REPORT.md`
- `ops/marketing/keyword_universe.csv`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Run authenticated `$0.15` CPC/auction validation for the `31` clean-route GB/CA/AU `GREEN` rows.
## 2026-05-14 - GB/CA/AU 31-row CPC validation packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local packet generation only; no Google Ads, Shopify Admin, live theme, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or destructive write.
- Exact scope: `31` clean-route GB/CA/AU `GREEN` rows (`GB=11`, `CA=10`, `AU=10`) from `ops/marketing/keyword_universe.csv`.
- Included public routes rechecked across GB/CA/AU: `/collections/mommy-and-me`, `/collections/family-matching`, and `/collections/pajamas`; `9/9` returned `200` and `0` supplier/url-brand hits.
- Account-surface limitation recorded as `AUTOMATION_CAPABILITY_MISMATCH`: no Google Ads API env keys, no `google.ads.googleads` package, and no usable authenticated GUI path in this automation runtime.

Risks:

- Packet readiness is not CPC validation and not upload approval.
- Some rows may still fail Keyword Planner/UI auction entry at `$0.15`, duplicate live intent, or show low-search-volume behavior.
- Swimwear remains excluded because `/collections/swimsuits` still leaks supplier vendors.

Required gates/fixes:

- Validate `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-packet/gb_ca_au_31_clean_route_cpc_validation_rows.csv` in authenticated Google Ads/Keyword Planner at max `$0.15`.
- Only rows that pass may become a small exact-match action row after fresh Ads readback, anti-cannibalization review, reviewer pass, and after-state readback plan.
- Do not upload/apply/add keywords, raise bids, change budgets/statuses, or add negatives from this packet alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-packet/GB_CA_AU_31_CLEAN_ROUTE_CPC_VALIDATION_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-packet/gb_ca_au_31_clean_route_cpc_validation_summary.json`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Run authenticated `$0.15` CPC/auction validation for the exact packet rows, then promote only passed rows through the green-gated action queue.

## 2026-05-14 - GB/CA/AU swim-route unblock and 36-row CPC packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local keyword reroute and packet generation only; no Google Ads, Shopify Admin, live theme, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or destructive write.
- Public source readback for `/collections/family-swimsuits` across GB/CA/AU and two header variants.
- Exact scope now: `36` clean-route GB/CA/AU `GREEN` rows (`GB=12`, `CA=12`, `AU=12`) from `ops/marketing/keyword_universe.csv`.
- `/collections/swimsuits` remains excluded because it still leaks supplier vendors through Shopify automatic product JSON.

Risks:

- Packet readiness is not CPC validation and not upload approval.
- Some rows may still fail Keyword Planner/UI auction entry at `$0.15`, duplicate live intent, or show low-search-volume behavior.
- Product PDPs under the swim collection were not individually approved for paid traffic in this run.

Required gates/fixes:

- Validate `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv` in authenticated Google Ads/Keyword Planner at max `$0.15`.
- Only rows that pass may become a small exact/phrase action row after fresh Ads readback, anti-cannibalization review, reviewer pass, and after-state readback plan.
- Do not upload/apply/add keywords, raise bids, change budgets/statuses, or add negatives from this packet alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/GB_CA_AU_SWIM_ROUTE_UNBLOCK_AND_36_ROW_CPC_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_swim_route_unblock_summary.json`
- `ops/marketing/action_queue.md`

Safest next sales-moving action:

- Run authenticated `$0.15` CPC/auction validation for the 36-row packet, then promote only passed rows through the green-gated action queue.

## 2026-05-14 - US Standard Shopping query/title diagnosis

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local Standard Shopping diagnosis only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Current visible yesterday Shopping search terms have `0` clicks and `$0.00` cost, so no negative keyword or product-group action is justified.
- Packet maps the three visible terms to paid-cohort candidates and keeps title/feed repair behind authenticated item-level export proof.
- Public route checks passed for `/collections/mommy-and-me`, `/collections/family-matching`, `/collections/pajamas`, `/collections/family-swimsuits`, and `/collections/daddy-and-me`; `/collections/vacation` and `/collections/matching-dresses` stay held.

Risks:

- Candidate mappings are local hypotheses, not proof that those exact items received impressions.
- Title/feed edits could mutate Shopify/Merchant production data and require fresh exact approval if later proven needed.

Required gates/fixes:

- Run authenticated read-only product-item export for campaign `23802638621`.
- Join item IDs/titles/performance to `us_shopping_query_title_candidates.csv`.
- Prepare a narrow title/feed approval packet only if export proof shows a mismatch.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-query-title-diagnosis/US_STANDARD_SHOPPING_QUERY_TITLE_DIAGNOSIS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-query-title-diagnosis/us_shopping_query_title_summary.json`

Safest next sales-moving action:

- Authenticated item-level Shopping export, then title/feed approval packet only for proven mismatches.

## 2026-05-14 - US Shopping public PDP fit preflight

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public storefront readback only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Candidate scope came from the existing `24`-row US Shopping query/title diagnosis.
- Preflight checked `10` unique PDP handles across two public header variants and wrote an `18`-row public-clean scope for authenticated item export.

Risks:

- Public PDP fit does not prove which products or titles actually received Standard Shopping impressions.
- Held candidate rows may still be viable after a separate public-source/title-fit repair, but should not drive title/feed repair decisions now.

Required gates/fixes:

- Run authenticated read-only item-level Shopping export for campaign `23802638621`.
- Join item IDs/titles/performance first to `us_shopping_auth_export_public_clean_scope.csv`.
- Prepare a narrow title/feed approval packet only if export proof shows a mismatch.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-public-pdp-fit-preflight/US_SHOPPING_PUBLIC_PDP_FIT_PREFLIGHT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-public-pdp-fit-preflight/us_shopping_public_pdp_fit_preflight_summary.json`

Safest next sales-moving action:

- Authenticated item-level Shopping export against the public-clean scope; no product/feed/title write until proof exists.

## 2026-05-14 - US Shopping held PDP repair packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public storefront readback only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Rechecked only the `6` held/review rows from the prior US Shopping public PDP fit preflight.
- Packet splits rows into supplier/source repair required, stale seasonal-copy repair required, and weak-fit/export-only-if-proven-relevant.

Risks:

- The supplier/stale public-source issues may require Shopify product-data, theme, or metadata repair, which is outside paid-media bounded authority and needs exact approval.
- The weak-fit row is source-clean, but using it for title/feed repair without item-level impression proof would still be overreach.

Required gates/fixes:

- Keep excluded rows out of authenticated export/title decisions unless repaired and publicly read back clean.
- Run authenticated item-level Shopping export first; only the weak-fit row may be considered if the export proves meaningful item-level impressions for that query.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-held-pdp-repair-packet/US_SHOPPING_HELD_PDP_REPAIR_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-held-pdp-repair-packet/us_shopping_held_pdp_repair_summary.json`

Safest next sales-moving action:

- Authenticated item-level Shopping export against the public-clean scope, while preserving the held-PDP repair packet as the exact repair/exclusion gate.

## 2026-05-14 - US Shopping authenticated export join prep

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local script/report/template generation only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Existing public-clean scope from `us_shopping_auth_export_public_clean_scope.csv`: `18` rows across `7` handles.
- Existing held-PDP repair rows: `6` rows across `3` handles.
- Generated join prep report, template, handle-level scope, and JSON summary.

Risks:

- No authenticated export was available in this automation runtime, so the packet is not item-level proof.
- Export rows without a product URL or handle cannot be safely joined; future operator must include or add the Shopify handle before decision use.
- Title-signal heuristics are review triggers only, not authority to edit Shopify/Merchant/feed data.

Required gates/fixes:

- Run authenticated read-only Standard Shopping product-item export for campaign `23802638621`.
- Include item ID, product title, product group/custom labels, impressions, clicks, cost, query/search term where available, conversion value, and product URL or handle.
- Run `python3.13 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/run_us_shopping_auth_export_join_prep.py --export-csv /path/to/authenticated-export.csv`.
- Prepare a title/feed approval packet only for proven item-level mismatches after the join; do not make direct product/feed/title edits.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/US_SHOPPING_AUTH_EXPORT_JOIN_PREP.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-auth-export-join-prep/us_shopping_auth_export_join_prep_summary.json`

Safest next sales-moving action:

- Run the authenticated read-only export and then the join script; convert only proven mismatches into a narrow owner approval packet.

## 2026-05-14 - US Shopping seasonal related filter live-sync approval packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local approval/readback packet only; no live Shopify theme, Shopify Admin, Google Ads, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, title, conversion, or destructive write.
- Scope is exactly one live theme snippet: `snippets/buy-box-similar-styles.liquid`.
- The affected swim-trunks rows remain excluded until exact owner approval, snippet sync, and after-state public source readback pass.

Risks:

- Live theme sync can affect the related-product recommendation surface beyond the one PDP, even though the existing local logic is intentionally narrow.
- The two swim-trunks rows still need authenticated Shopping item-level proof before they influence title/feed decisions.

Required gates/fixes:

- Obtain the exact approval phrase in `US_SHOPPING_SEASONAL_RELATED_FILTER_LIVE_SYNC_APPROVAL_PACKET.md`.
- Before push, public-read back the swim-trunks PDP source with both `Accept: text/html` and `Accept: */*`.
- Push only `snippets/buy-box-similar-styles.liquid`.
- After push, public-read back the same PDP and require `0` supplier/source-domain hits and `0` `Christmas`/`Santa`/`Xmas` stale seasonal hits before considering the two rows repaired.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-seasonal-live-sync-approval/US_SHOPPING_SEASONAL_RELATED_FILTER_LIVE_SYNC_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-seasonal-live-sync-approval/us_shopping_seasonal_live_sync_approval_summary.json`

Safest next sales-moving action:

- In an owner-approved theme session, execute the one-snippet live sync and before/after public source readbacks; otherwise keep the swim-trunks rows excluded.

## 2026-05-14 - GB/CA/AU 36-row CPC public route refresh

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public storefront readback only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Exact source scope was the existing `36`-row GB/CA/AU CPC validation packet.
- Checked `12` unique market/route URLs with `24` fetches across browser-like and cache-busted header variants.

Risks:

- This is not Google Ads/Keyword Planner CPC or auction-entry proof.
- `/collections/family-matching` redirects cleanly to `/collections/matching-outfits`; not a landing-cleanliness blocker, but future live packets should avoid unnecessary redirects by using canonical URLs after CPC validation.

Required gates/fixes:

- Run authenticated read-only Google Ads/Keyword Planner validation at max CPC `$0.15`.
- Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass and after-state readback.
- No upload/apply/add keyword/bid/status/budget/negative action from public route proof alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/GB_CA_AU_36_ROW_CPC_PUBLIC_ROUTE_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-public-refresh/gb_ca_au_36_row_public_route_readback_summary.json`

Safest next sales-moving action:

- Authenticated `$0.15` CPC validation for the exact 36-row packet; then canonicalize passing final URLs before any live action row.

## 2026-05-14 - GB/CA/AU 36-row CPC canonical URL packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local CSV/report generation plus public storefront readback only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Exact source scope was the existing `36`-row GB/CA/AU CPC validation packet.
- Converted only redirecting `/collections/family-matching` final URLs to the canonical `/collections/matching-outfits` destination.
- Checked `12` unique market/route URLs with `24` fetches across browser-like and cache-busted header variants.

Risks:

- This is not Google Ads/Keyword Planner CPC or auction-entry proof.
- Canonical public route proof does not authorize any live keyword, bid, status, budget, or negative change.

Required gates/fixes:

- Run authenticated read-only Google Ads/Keyword Planner validation at max CPC `$0.15` using the canonical CSV.
- Promote only pass rows through a fresh `GREEN` action-queue row with reviewer pass and after-state readback.
- No upload/apply/add keyword/bid/status/budget/negative action from public route proof alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/GB_CA_AU_36_ROW_CPC_CANONICAL_URL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-36-row-cpc-canonical-url-packet/gb_ca_au_36_canonical_url_packet_summary.json`

Safest next sales-moving action:

- Authenticated `$0.15` CPC validation for the canonical 36-row packet; only pass rows can become a bounded live action row.

## 2026-05-14 - GB/CA/AU CPC validation decision kit

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local Keyword Planner input/template/parser generation only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- The source scope is exactly the canonical `36`-row GB/CA/AU packet and expands it only into `72` decision rows for exact+phrase validation.
- The parser classifies authenticated forecast rows as `PASS_015_CPC_GATE`, `FAIL_015_CPC_GATE`, `LOW_VOLUME_OR_NO_AUCTION`, `POLICY_OR_DESTINATION_BLOCK`, or `MISSING_REQUIRED_FORECAST_DATA`.

Risks:

- This is not a Google Ads/Keyword Planner readback and cannot prove CPC feasibility.
- Phrase validation rows are decision candidates only; they must not become live rows unless authenticated forecast, reviewer, anti-cannibalization, and after-state gates pass.

Required gates/fixes:

- Run authenticated read-only Google Ads/Keyword Planner validation at max CPC `$0.15`.
- Export forecast/readback rows and run `validate_keyword_planner_forecast_export.py`.
- Promote only `PASS_015_CPC_GATE` rows through a fresh `GREEN` action-queue row with fresh Ads before-state readback and after-state plan.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/GB_CA_AU_CPC_VALIDATION_DECISION_KIT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/gb_ca_au_cpc_validation_decision_kit_summary.json`

Safest next sales-moving action:

- In an account-capable Ads session, validate the canonical rows and run the parser; live action remains blocked until pass rows exist.

## 2026-05-14 - Collection source cleanup approval packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public storefront source readback only; no Shopify Admin, Google Ads, Merchant, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, or destructive write.
- Exact source scope was `/collections/swimsuits` and `/collections/matching-dresses` across `US`, `GB`, `CA`, and `AU` with browser-like and generic/cache-busted header variants.
- Packet names only cleanup-or-exclude gates for product/vendor source leakage and keeps current clean GB/CA/AU CPC validation rows untouched.

Risks:

- Product/vendor source cleanup is a Shopify Admin product-data write and requires fresh owner approval.
- The packet proves public source leakage and product rows, but it does not authorize product edits or paid traffic to those routes.

Required gates/fixes:

- Keep `/collections/swimsuits` and `/collections/matching-dresses` local-only/excluded until rerouted or owner-approved product/vendor cleanup is read back with `0` supplier hits.
- Do not upload/add keyword rows, edit product/feed titles, or change product groups from this packet alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/COLLECTION_SOURCE_CLEANUP_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-collection-source-cleanup-approval/collection_source_cleanup_approval_summary.json`

Safest next sales-moving action:

- Keep the current clean-route GB/CA/AU CPC validation as the main path; use this packet only if the owner chooses to clean the remaining dirty collection routes.

## 2026-05-14 - Current P0 blocker fix readback

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Existing authenticated Pinterest Ads Manager tab for advertiser `549756244483` is controllable.
- Account/domain read back as `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Create menu exposes `Create campaign` and `Load existing campaign draft`.
- Reporting readback shows `0 campaigns`, `0 currently being served`, `$0.00` spend, and `0` impressions for `05/07/2026 - 05/14/2026`.
- CPC forecast parser now does not misclassify ordinary `Eligible (Limited)` as a policy/destination block.

Risks:

- Pinterest access does not authorize launch/spend or out-of-scope budget/bid/tag/CAPI/source/feed mutations.
- Google Ads Keyword Planner is still not accessible in the currently controllable Ads tab, which redirects to Google sign-in.
- Parser smoke tests are not Keyword Planner proof.

Required gates/fixes:

- For Pinterest, use only the approved paused US draft workflow, with before/after readbacks and no launch/live spend.
- For GB/CA/AU Search, export authenticated Keyword Planner/Ads forecast rows at max `$0.15` and run the patched parser before any live action row.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-current-p0-blocker-fix/P0_BLOCKER_FIX_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-current-p0-blocker-fix/pinterest_authenticated_reporting_readback.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-current-p0-blocker-fix/forecast_parser_smoke_summary.json`

Safest next sales-moving action:

- Build/read back the approved paused Pinterest US draft from the restored tab, or validate the GB/CA/AU 36-row packet in an authenticated Google Ads/Keyword Planner session.

## 2026-05-14 - US keyword route unblock

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local `keyword_universe.csv` reroute plus public storefront readback only.
- Exact source scope was US rows on `/collections/vacation`, `/collections/matching-dresses`, `/collections/swimsuits`, and `/collections/daddy-and-me`.
- Rerouted `23` rows to `/collections/matching-outfits`, `/collections/mommy-and-me`, and `/collections/family-swimsuits`.
- Public readback checked all replacement routes across browser-like and cache-busted header variants with `200`, `0` supplier/url-brand hits, and `0` stale seasonal/local-inventory trust hits.

Risks:

- Route cleanliness does not prove active-product fit, CPC feasibility, or paid Search demand.
- The original dirty collection routes still require owner-approved product/vendor source cleanup before they can receive paid traffic directly.

Required gates/fixes:

- Keep rerouted US rows local-only until active-product proof, authenticated `$0.15` CPC/search feasibility, reviewer pass, and a fresh `GREEN` action row exist.
- Do not upload/add keywords, change bids/budgets/status, or edit Shopify product/vendor data from this packet alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-keyword-route-unblock/US_KEYWORD_ROUTE_UNBLOCK_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-keyword-route-unblock/us_keyword_route_unblock_summary.json`

Safest next sales-moving action:

- Use the rerouted US rows only as a future validation source after the authenticated Standard Shopping export or a separate US Search feasibility packet proves product/query fit.

## 2026-05-14 - Google Ads API CPC forecast retry harness

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Repo-local read-only script/report only; no Google Ads, Merchant, Shopify Admin, live theme, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, product-group, conversion, credential, or destructive write.
- Harness reads the existing canonical `72` exact/phrase validation rows and forecasts one keyword row at a time to avoid aggregate US/Broad UI export ambiguity.
- Dry-run shows market geo targets `GB=2826`, `CA=2124`, `AU=2036`, English `1000`, Google Search only, and max CPC `150000` micros.
- Live run fails closed before any API call when `GOOGLE_ADS_CUSTOMER_ID` is unset.

Risks:

- This is not authenticated CPC proof; it is a safer execution harness for the next account-capable shell.
- Google Ads API credentials/customer access still need to be loaded outside this unattended runtime before forecast rows can be produced.

Required gates/fixes:

- Run the harness only as read-only forecast evidence in an account-capable shell.
- Run the existing parser on `google_ads_api_cpc_forecast_rows.csv`.
- Promote only real `PASS_015_CPC_GATE` rows through a fresh `GREEN` action-queue row with fresh Ads before-state readback, reviewer pass, anti-cannibalization check, and after-state readback plan.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/GOOGLE_ADS_API_CPC_FORECAST_RETRY_HARNESS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/run_google_ads_api_cpc_forecast.py`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-cpc-validation-decision-kit/google_ads_api_cpc_forecast_summary.json`

Safest next sales-moving action:

- Run the API harness in a credentialed Google Ads shell, then parse the output and create a green row only for pass rows.

## 2026-05-15 - US active-product public proof

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Read-only Outlook Basic Access watch first; no approval found as of 04:05 EDT.
- Public storefront active-product proof only; no Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, credential, or theme write.
- Exact source scope was US `GREEN` keyword-universe rows already routed to clean collection pages.
- Public readback checked `5` collection routes and sampled `51` product pages; `47` rows passed, `4` stayed held/review.

Risks:

- Public product proof is not item-level Shopping export proof and not CPC/search feasibility proof.
- The family-swimsuits route sample still surfaced non-swim products, so those specific rows stay held/review until route/product fit is better or a swim-specific product proof is produced.

Required gates/fixes:

- Keep all rows local-only until authenticated `$0.15` CPC/search feasibility, anti-cannibalization review, fresh `GREEN` action row, and after-state readback exist.
- Do not upload/add keywords, change bids/budgets/status, or edit Shopify product/vendor data from this packet.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-active-product-proof/US_ACTIVE_PRODUCT_PROOF_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-active-product-proof/us_active_product_proof_summary.json`

Safest next sales-moving action:

- Use only the `PUBLIC_ACTIVE_PRODUCT_PASS` rows as the source for a future small US Search validation packet after the GB/CA/AU P0 CPC gate clears or an account-capable US CPC path is available.

## 2026-05-15 - US Search active-product validation packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Read-only Outlook Basic Access watch first; no approval found as of 04:27 EDT.
- Repo-local/public storefront packet only; no Google Ads, Shopify Admin, Merchant, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, credential, or theme write.
- Exact source scope was `12` US `GREEN` rows with public-active product proof and canonical clean routes.
- Public route readback checked `6` route/header fetches across `matching-outfits`, `mommy-and-me`, and `pajamas`; all returned `200`, `0` redirects, `0` supplier/url-brand hits, and `0` stale/trust hits.

Risks:

- This is a forecast input, not CPC/search-feasibility proof.
- It does not replace authenticated Standard Shopping item-level export proof and does not prove live Search readiness.

Required gates/fixes:

- Keep all rows local-only until authenticated `$0.15` CPC/search feasibility, anti-cannibalization review, fresh `GREEN` action row, and after-state readback exist.
- Do not upload/add keywords, change bids/budgets/status, or add negatives from this packet.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/US_SEARCH_ACTIVE_PRODUCT_VALIDATION_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-us-search-active-product-validation-packet/us_search_active_product_validation_summary.json`

Safest next sales-moving action:

- After Basic Access approval, validate the US matrix read-only at max `$0.15`; promote only real `PASS_015_CPC_GATE` rows through a fresh green row.

## 2026-05-15 - Current Ads serving and search-term readback

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Read-only Outlook Basic Access watch first; no approval found as of 04:35 EDT.
- Existing authenticated Google Ads UI readback only; no Google Ads, Shopping, Merchant, Shopify Admin, Pinterest, GA4/GTM, billing, campaign, budget, bid, status, keyword, negative, feed, product, conversion, credential, or theme write.
- Enabled-campaign aggregate current view showed `6` impressions, `1` click, `$0.04` cost, and `0.00` conversions/value.
- Visible GB exact Search row still showed `0` impressions/clicks/cost.
- Cleared a stale search-term reporting filter and read the broader Apr 18-May 14 table: brand Search rows carried visible clicks/cost, while visible Standard Shopping rows remained `0` clicks and `$0.00` cost.

Risks:

- The current aggregate `1` click / `$0.04` signal is not campaign-attributed enough to justify optimization by itself.
- Broader date-range brand Search clicks do not validate GB/CA/AU long-tail CPC feasibility and do not prove Shopping title/feed action.

Required gates/fixes:

- Keep the GB/CA/AU CPC gate blocked until Basic Access approval or a correctly scoped authenticated UI export produces real `PASS_015_CPC_GATE` rows.
- Run authenticated Standard Shopping item-level export before any title/feed/product-group/negative decision.

Evidence:

- Google Ads UI read-only readback, 2026-05-15 04:35-04:39 EDT, client account `399-097-6848`.
- `ops/marketing/action_queue.md`
- `ops/marketing/daily_scorecard.md`

Safest next sales-moving action:

- Keep watching Basic Access and rerun the API forecast harness/parser after approval; independently run the authenticated Shopping item-level export when an export-capable session is available.

## 2026-05-15 - Pinterest paused-draft scope refresh

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public/read-only only: refreshed the already-approved Pinterest paused-draft scope before any object creation.
- Checked `32` unique product pages and `32` image URLs from the prior `342`-row Pinterest scope.
- Product pages passed `30/32`; image URLs passed `32/32`.
- Held `9` variants across `2` Mommy & Me PDPs because public source still exposes `[source-host-redacted]` / `[source-host-redacted]` supplier domains.

Risks:

- The older `342`-row scope is no longer safe as a direct paused-draft prefill unless the `9` held variants are repaired.
- This is not Pinterest write authority and does not solve tag/Event Quality or launch approval.

Required gates/fixes:

- Use `pinterest_paused_draft_refreshed_clean_scope.csv` (`333` variants) for the next paused-draft prefill.
- Keep the held `9` variants excluded unless approved product/vendor cleanup passes public source readback.
- Stop before any Pinterest budget, bid, enablement, launch, publish, audience, source, feed, tag, CAPI, or catalog mutation outside the paused spec.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/PINTEREST_PAUSED_DRAFT_SCOPE_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_scope_refresh_summary.json`

Safest next sales-moving action:

- In an account-capable session, create only the paused/draft Pinterest shell from the restored advertiser tab using the refreshed `333`-variant scope, then read back before any live launch decision.

## 2026-05-15 - Pinterest 333 paused draft build-ready packet and multilingual Shopping queue

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Built repo-local Pinterest paused/draft object packet from the refreshed `333` public-clean variants: `201` Mommy & Me, `103` Family Matching, `29` Pajamas.
- Built repo-local Google Shopping multilingual queue covering `US/en`, `US/es`, `CA/en`, `GB/en`, `AU/en`, and later native-language concept lanes.
- Confirmed both packets are no-write artifacts and do not create platform objects or mutate feeds/titles/product groups.

Risks:

- Pinterest "draft" creation is still an external account write even when paused; current-session approval is required before clicking Create/Save.
- Multilingual Shopping can become unsafe if stale Merchant exports, concept copy, or storefront language assumptions are treated as feed/title proof.

Required gates/fixes:

- Pinterest requires the exact approval phrase in `PINTEREST_333_PAUSED_DRAFT_BUILD_READY.md`, plus before/after advertiser/status/spend readbacks and stop conditions.
- Shopping requires authenticated read-only exports before any campaign/feed/title/product-group approval packet.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-333-paused-draft-build-ready/PINTEREST_333_PAUSED_DRAFT_BUILD_READY.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-google-shopping-multilingual-expansion-queue/GOOGLE_SHOPPING_MULTILINGUAL_EXPANSION_QUEUE.md`

Safest next sales-moving action:

- If the owner approves, create only the Pinterest paused draft objects from the restored `549756244483` advertiser tab; in parallel, run the read-only Standard Shopping and Merchant language/country exports.

## 2026-05-15 - Standard Shopping export join and clicked PDP readback

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Read-only Standard Shopping product export join for campaign `23802638621`; no Google Ads, Merchant, Shopify Admin, feed, title, product-group, bid, budget, status, conversion, Pinterest, GA4/GTM, billing, credential, or live theme write.
- Joined `767` paid-cohort rows: `65` clicks, `$14.17` cost, `$0.00` conversion value, and `0` title/feed repair candidates.
- Public-read back `27` clicked export rows across `13` unique product handles and `26` storefront fetches.
- Result: `26/26` public fetches passed and `0` clicked handles were source-blocked.

Risks:

- Historical export date range is `Apr 18-May 14, 2026`, not a same-day ROAS result.
- Clean clicked PDP source does not explain why clicks did not convert.
- The held rows still require their separate repair/readback gates before paid expansion use.

Required gates/fixes:

- Do not edit titles, feed attributes, product groups, bids, budgets, statuses, negatives, or product scope from this packet alone.
- Continue with current Merchant `US/es` source export and CA/GB/AU English eligibility readbacks before Shopping expansion.
- Use clean clicked PDPs for conversion/landing/product-fit analysis only.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-pdp-readback/STANDARD_SHOPPING_CLICKED_PDP_PUBLIC_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-shopping-readonly-export-queue/standard_shopping_products_export_summary.json`

Safest next sales-moving action:

- Run Merchant `US/es` source `10627981690` read-only export, then CA/GB/AU English country/feed eligibility readbacks; separately analyze clean clicked PDPs for conversion friction.

## 2026-05-15 - 333 Pinterest scope and Basic Access watch refresh

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Outlook connector profile is `info@dresslikemommy.com`.
- Targeted read-only searches through 05:08 EDT found no Google Ads API Basic Access approval.
- The current Pinterest paused-draft path is the refreshed `333` clean-variant scope, not the older full `342` rows.

Risks:

- Running the CPC harness before Basic Access approval will repeat the Explorer-access blocker.
- Reusing the older `342` Pinterest scope would reintroduce `9` variants from supplier-leaking public PDPs.

Required gates/fixes:

- Do not rerun the Google Ads API CPC harness until Basic Access approval is present.
- Do not create Pinterest paused/draft objects without the exact approval phrase in `PINTEREST_333_PAUSED_DRAFT_BUILD_READY.md`.

Evidence:

- Outlook read-only searches, 2026-05-15 05:08 EDT.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-333-paused-draft-build-ready/PINTEREST_333_PAUSED_DRAFT_BUILD_READY.md`

Safest next sales-moving action:

- Keep watching `info@dresslikemommy.com`; use only the `333` Pinterest scope if the paused-draft approval phrase is given.

## 2026-05-15 - Pinterest paused-draft UI attempt stopped on budget validation

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Current-session exact approval phrase was received for advertiser `549756244483` using the refreshed `333` scope, with no launch, no enablement, no spend, no budget/bid activation, no catalog/source/tag/CAPI/feed changes, and a required stop on out-of-scope writes.
- Existing authenticated Pinterest Ads Manager tab was used.
- Manual Catalog sales flow reached campaign name `DLM_PIN_US_CATALOG_333_PAUSED_20260515` and status `Paused`.
- Draft actions exposed `Save as a new draft`, but Pinterest validation blocked save because budget was blank.

Risks:

- Pinterest UI requires a valid daily budget value before saving the paused draft.
- Entering even the minimum `$1.00` daily budget is outside the current conservative no-budget/no-bid activation boundary unless explicitly approved for validation-only use.

Required gates/fixes:

- Do not retry the no-budget save path.
- Continue only if the owner approves entering the minimum `$1.00` daily budget solely to satisfy paused-draft validation while keeping the campaign paused/unpublished/no-spend, or if a no-budget API/import route is found.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-paused-draft-budget-validation-stop/PINTEREST_PAUSED_DRAFT_BUDGET_VALIDATION_STOP.md`

Safest next sales-moving action:

- Get the narrow minimum-budget paused-draft approval packet or continue independent Shopping/Merchant read-only exports.

## 2026-05-15 - Merchant Shopping issue-export readback

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Read-only/local analysis of current Merchant product-issues export and API attempt evidence.
- `US/es` issue-export state for source-readiness lane: `1,453` rows, `354` unique items, `432` Missing age group rows, `708` over-capacity rows, and `53` paid-cohort issue items.
- CA/GB/AU English country-language pairs have `0` rows in the current issue export.
- Google Ads API Basic Access watch still found no approval, so the CPC forecast harness remains parked.

Risks:

- The issue export does not include `source_id`, so it is not a source-specific all-products export for `10627981690`.
- CA/GB/AU `0` issue rows do not prove active approved product counts, feed label, currency, country availability, or paid-cohort eligibility.
- Merchant API and Content API readbacks returned 403 insufficient authentication scopes.

Required gates/fixes:

- Do not create Shopping campaigns or mutate feeds, titles, product groups, product scope, bids, budgets, statuses, or conversion settings from issue-export evidence alone.
- Build the `US/es` no-write repair/classification packet before any source/feed action.
- Capture CA/GB/AU all-products/source exports before any Shopping expansion packet.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/MERCHANT_SHOPPING_READONLY_QUEUE_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-shopping-readonly-queue-readback/merchant_shopping_readonly_queue_summary.json`

Safest next sales-moving action:

- Prepare the smallest `US/es` repair/classification packet and obtain full CA/GB/AU English all-products/source eligibility exports; rerun the CPC harness only after Basic Access approval appears.

## 2026-05-15 - Merchant US/es no-write repair classification packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Local/read-only classification of the current Merchant `US/es` issue rows.
- Output packet classifies `1,453` rows / `354` unique items / `53` paid-cohort issue items.
- Paid-cohort attribute-repair candidates are limited to `3` unique items; over-capacity still affects all `53` paid-cohort issue items.

Risks:

- The issue export does not include `source_id` or full active approved-product proof.
- Capacity, feed/source, product, title, and Shopping campaign changes are excluded surfaces without exact approval.

Required gates/fixes:

- Capture full source/all-products export for source `10627981690` before repair/build decisions.
- Do not mutate Merchant feeds, source scope, products, titles, capacity, product groups, bids, budgets, statuses, campaigns, conversions, billing, Shopify Admin, or Pinterest from this packet alone.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-us-es-repair-classification/MERCHANT_US_ES_NO_WRITE_REPAIR_CLASSIFICATION_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-us-es-repair-classification/merchant_us_es_repair_classification_summary.json`

Safest next sales-moving action:

- Run full source/all-products exports for `US/es`, CA/en, GB/en, and AU/en, then decide whether a narrow approval packet is valid.

## 2026-05-15 - Pinterest `$1.00` validation-only product-group scope stop

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Owner approval allowed `$1.00` daily budget only for paused-draft validation, with no launch, no enablement, no spend, no bid activation, and no catalog/source/tag/CAPI/feed/audience changes.
- The authenticated Pinterest selector had selected groups `0`.
- Searches for `DLM_PIN_US_SHOPPING`, `mommy_me`, and `family_matching` returned no exact groups.
- Searches for `pajamas`, `Mommy`, and `Family Matching` returned only broad groups: `Pajamas` `252`, Mommy & Me `445/1,011`, Family Matching `1,011+`, and `All Products` `5,664`.

Risks:

- Saving or adding any available broad group would exceed the approved `333` active-clean scope.
- Creating/exposing exact product groups is likely a product-group/catalog-scope action and remains outside the validation-only approval.

Required gates/fixes:

- Do not click `Add product groups`, Save, Continue, Review, Publish, Launch, or Enable from this broad-group state.
- Continue only after exact approval to create/expose product groups from existing feed attributes or after a selector readback proves exact `201/103/29` groups are already available.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-paused-draft-product-group-scope-stop/PINTEREST_PAUSED_DRAFT_PRODUCT_GROUP_SCOPE_STOP.md`

Safest next sales-moving action:

- Use the exact product-group approval packet, then continue the paused/unpublished draft only if final review shows exact scope and no launch/enablement/spend/bid activation.

## 2026-05-15 - Pinterest exact product-group approval packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Packet derives groups only from the refreshed `333` public-clean scope CSV.
- Exact required groups are Mommy & Me `201` variants / `26` products, Family Matching `103` / `7`, and Pajamas `29` / `1`.
- Father-inclusive rows are isolated as proof-only: `43` variants across `4` products.
- All `333` rows pass image, price, availability, shipping policy, return policy, and public PDP source-clean fields.

Risks:

- Product-group creation/exposure is a Pinterest object/catalog-scope mutation and needs exact approval.
- Father-inclusive rows may overlap existing groups; do not create a separate group unless the owner explicitly approves and the platform can expose it exactly.

Required gates/fixes:

- Do not save, publish, launch, or enable broad groups.
- Get exact approval to create/expose product groups from existing feed attributes only, excluding the `9` held variants.
- Final review must reconfirm max `$5/day`, max `$0.15` CPC, and exact active-clean group counts.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/PINTEREST_EXACT_PRODUCT_GROUP_UNBLOCK_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/pinterest_exact_product_group_unblock_summary.json`

Safest next sales-moving action:

- Ask for the exact approval phrase in the packet, then create/expose exact groups and launch only after the final review passes.

## 2026-05-15 - Pinterest exact product-group approved attempt stop

Reviewer verdict: `BLOCK_NO_LAUNCH`

Checked:

- Current-session owner approval matched the exact product-group packet boundary.
- The attempted UI label-filter path used existing feed attributes only: `paid_eligible`, `us_test_ready`, and `mommy_me`.
- Pinterest preview returned `0 products selected`, so the expected Mommy & Me count `201` was not met.
- Exact item-ID fallback import CSV was generated from the refreshed clean scope with `201/103/29` counts.
- Chrome file upload failed before import with `Not allowed`.

Risks:

- Launching or saving broad groups would violate the active-clean `333` scope.
- A zero-count label preview could mean Pinterest does not expose the custom-label filters on this surface, so readback counts are mandatory after any import.

Required gates/fixes:

- Use a file-upload-capable browser path.
- Import the exact item-ID CSV only.
- Read back exact groups before campaign save or launch review.
- Final review must still confirm max `$5/day`, max `$0.15` CPC, exact group scope, and no source/feed/tag/CAPI/billing/Shopify changes.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/PINTEREST_EXACT_PRODUCT_GROUP_ATTEMPT_STOP.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/pinterest_exact_product_group_item_id_import.csv`

Safest next sales-moving action:

- Enable file upload for the controlled Chrome path or use another upload-capable authenticated path, then import and read back exact counts before final launch review.

## 2026-05-15 - Pinterest exact product-group import readback

Reviewer verdict: `BLOCK_NO_LAUNCH_PRODUCTS_ZERO`

Checked:

- Current-session owner approval allowed an upload-capable exact CSV import path and final-review launch only if max `$5/day`, max `$0.15` CPC, exact scope, and no excluded changes were confirmed.
- Authenticated Chrome DevTools path imported `pinterest_exact_product_group_item_id_import.csv`.
- The three exact groups now exist.
- Edit readback confirms item-ID filter payload counts: Mommy & Me `201`, Family Matching `103`, Pajamas `29`.
- Pinterest detail pages still show `0` selected/products, empty previews, disabled `Promote`, and `This product group updates every 24 hours`.

Risks:

- A filter-payload count is not yet a launchable product-count readback.
- Launching while Pinterest shows `0` products would violate the final-review gate.

Required gates/fixes:

- Freshly read back the imported groups after Pinterest resolves the update.
- Proceed to final launch review only if usable product counts match exact active-clean scope.
- Final review must confirm max `$5/day`, max `$0.15` CPC, exact groups, and no source/feed/tag/CAPI/billing/Shopify changes.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/PINTEREST_EXACT_PRODUCT_GROUP_IMPORT_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/pinterest_exact_product_group_item_id_import.csv`

Safest next sales-moving action:

- Recheck exact group product counts and only then continue final launch review; do not launch or save broad groups.

## 2026-05-15 - Standard Shopping clicked title conversion approval packet

Reviewer verdict: `PASS_WITH_GATES`

Checked:

- Public/read-only conversion analysis of the `13` unique clicked Standard Shopping PDP handles.
- Source evidence: `65` clicks / `$14.17` cost / `$0.00` conversion value, `0` source-blocked clicked handles, and `0` feed-title repair candidates.
- New packet found `12/13` clicked visible H1s contain literal ellipses, covering `64` clicks / `$13.96` cost.
- Add-to-cart form, customer-photo section markup, and hidden zero-review badge behavior remained present in checked public source.

Risks:

- Shopify product title/display-title cleanup is customer-visible product data/presentation work and needs exact owner approval.
- Do not let the packet become feed-title, product-group, bid, budget, negative, status, campaign, conversion, or Merchant/Pinterest authority.

Required gates/fixes:

- Owner approval must match the packet phrase before any Shopify title/display-title cleanup.
- Before/after public readbacks must verify H1/title, add-to-cart, price, source-clean, and zero-review state.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-title-conversion-approval/STANDARD_SHOPPING_CLICKED_TITLE_CONVERSION_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-standard-shopping-clicked-title-conversion-approval/standard_shopping_clicked_title_conversion_summary.json`

Safest next sales-moving action:

- Ask for exact cleanup approval; otherwise keep observing and continue Merchant/feed eligibility work.

## 2026-05-15 - Merchant priority-market capacity fix packet

Reviewer verdict: `PASS_WITH_LIVE_READBACK_GATE`

Checked:

- Current Merchant all-products browser RPC export has `351,007` rows.
- Owner priority order is USA English and Spanish first, Canada English/French second, GB English third, Europe later.
- Current protected rows are USA English `5,491` and USA Spanish `5,412`.
- Current missing priority rows are CA/en `0`, CA/fr `0`, and GB/en `0`.
- First-pass non-priority removal candidates total `199,684` rows: Asia/Middle East `129,112`, Africa `37,511`, South America `8,818`, and non-US-USD `24,243`.

Risks:

- The cleanup must remove market/feed-country publishing scope, not Shopify products.
- Removing Europe in the first pass would violate the owner priority order because Europe is later-priority, not removal-priority.
- A live UI/API control that cannot preview the exact candidate groups is not safe to save.

Required gates/fixes:

- Read back the exact Merchant/Shopify/Google publishing control surface before any Save/Apply/Sync/Upload.
- Preserve USA English, USA Spanish, future Canada English/French, future GB English, and Europe-later groups.
- After cleanup, capture a fresh all-products export and prove total rows dropped before enabling/exporting Canada and GB rows.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_PRIORITY_MARKET_CAPACITY_FIX_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_priority_market_capacity_fix_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_removal_candidate_groups.csv`

Safest next sales-moving action:

- Use an authenticated exact-control path to prune only the listed non-priority publishing groups, then re-export Merchant products and enable/prove Canada English/French and GB English rows.

## 2026-05-15 - Merchant capacity execution guard

Reviewer verdict: `PASS_WITH_LIVE_READBACK_GATE`

Checked:

- Guard script reads the current `351,007` row sanitized Merchant RPC export and the removal-candidate CSV.
- Guard output defines `41` exact preview rows, expected first-pass removal `199,684`, expected after-first-pass floor `151,323`, protected USA English `5,491`, protected USA Spanish `5,412`, and current CA/en, CA/fr, GB/en rows all `0`.
- The generated after-export mode fails closed unless all first-pass removal groups are gone and USA English/Spanish counts do not drop.

Risks:

- This still does not authorize Save/Apply/Sync/Upload; it only defines the live preview and after-export acceptance criteria.
- A platform surface that cannot map to the CSV is not safe to mutate.

Required gates/fixes:

- Reconcile live preview to `merchant_capacity_platform_preview_acceptance.csv` before any save.
- After cleanup, run `build_merchant_capacity_execution_guard.py --after-export` on the fresh export before enabling/building Canada or GB Shopping.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_PRIORITY_MARKET_CAPACITY_EXECUTION_GUARD.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_execution_guard_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_platform_preview_acceptance.csv`

Safest next sales-moving action:

- Use an authenticated exact-control path to preview only the guard rows, then save only if USA English/Spanish and Europe-later groups are preserved.

## 2026-05-15 - Shopify Markets region prune preview

Reviewer verdict: `PASS_WITH_LIVE_READBACK_GATE`

Checked:

- Region preview reads only the sanitized Shopify Markets readback and makes no external calls.
- It confirms active market handles include `us`, `canada`, `united-kingdom`, `eu`, `australia`, and `international`.
- It classifies `52/73` `International` regions as first-pass removal candidates only when a live preview preserves priority markets, and keeps `21` regions in preserve/hold-review.
- It explicitly blocks whole-market removal, product deletion, Europe removal, duplicate `CA`/`AU` removal, and any save when the live preview cannot reconcile to the guard files.

Risks:

- Region classification is an operator checklist, not proof that Shopify Markets is the exact control surface connected to Merchant row generation.
- A live UI/API that cannot preview the exact region and feed-group effect is not safe to mutate.

Required gates/fixes:

- Reconcile authenticated preview to both `shopify_international_region_prune_preview.csv` and `merchant_capacity_platform_preview_acceptance.csv`.
- After cleanup, capture a fresh Merchant export and run the after-export guard before Canada/GB Shopping work.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_SHOPIFY_MARKETS_REGION_PRUNE_PREVIEW.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/shopify_international_region_prune_preview.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/shopify_international_region_prune_summary.json`

Safest next sales-moving action:

- Use an authenticated exact-control path to preview `International` region removals and feed-group effects, then save only if the preview preserves priority markets and matches both guard files.

## 2026-05-15 - Shopify Region Prune And Post-Prune Merchant Export

Reviewer verdict: `PASS_FOR_BOUNDED_SHOPIFY_WRITE__FAIL_FOR_SHOPPING_BUILD`

Checked:

- Shopify Admin Markets mutation touched only market handle `international`.
- Removed region count was exactly `52`; `International` region count changed from `73` to `21`.
- Required active markets stayed present: `us`, `canada`, `united-kingdom`, `eu`, `australia`, and `international`.
- Duplicate `CA` and `AU` stayed present inside `International`.
- Fresh Merchant browser-RPC export still captured `351,007` rows.
- After-export guard failed closed with `199,684` remaining first-pass removal rows.
- Canada English, Canada French, and GB English proof rows are still `0`.

Risks:

- Shopify Markets cleanup may require Google & YouTube/Merchant propagation time or a separate publishing sync/control action before Merchant rows change.
- Building Shopping now would use absent Canada/GB rows and violate the owner's gate.

Required gates/fixes:

- Do not repeat the same Shopify region prune.
- Re-export after Google/Merchant propagation or use a Google & YouTube/Merchant publishing sync/control path, then rerun the after-export guard.
- Build Shopping only after Canada English/French and GB English rows exist and the guard passes.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/SHOPIFY_INTERNATIONAL_REGION_PRUNE_EXECUTION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/MERCHANT_POST_SHOPIFY_REGION_PRUNE_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-post-shopify-region-prune-export/MERCHANT_SOURCE_ELIGIBILITY_BROWSER_RPC_EXPORT.md`

Safest next sales-moving action:

- Trigger/read back the Google & YouTube/Merchant publishing path if available, or rerun the Merchant export after propagation, then pass the guard before any Shopping build.

## 2026-05-15 - Merchant Post-Prune Paid-Cohort Intersection

Reviewer verdict: `PASS_WITH_HOLD_DECISION`

Checked:

- Local/read-only join used saved Merchant post-prune browser-RPC export, exact `780` paid cohort source, and saved Google Ads Standard Shopping product export.
- No external account write, feed edit, product edit, campaign edit, bid, budget, status, conversion, billing, credential, or destructive action occurred.
- Current Standard Shopping export IDs reconcile `767/767` to current US/en Merchant rows.
- Canada English, Canada French, GB English, and AU English remain `0` paid-cohort IDs in the saved Merchant export.
- Non-target groups still contain `51,033` duplicate paid-cohort rows across all `780` paid-cohort IDs.

Risks:

- The join is from saved exports, not a fresh account-surface readback after propagation.
- It cannot prove Canada/GB Shopping readiness because those target rows are still absent.

Required gates/fixes:

- Do not create Shopping campaigns, product groups, feed/title changes, or scope changes from this intersection.
- Continue only through Google & YouTube/Merchant publishing sync/control readback or delayed re-export, then rerun the after-export guard.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-merchant-post-prune-paid-cohort-intersection/MERCHANT_POST_PRUNE_PAID_COHORT_INTERSECTION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-merchant-post-prune-paid-cohort-intersection/merchant_post_prune_paid_cohort_intersection_summary.json`

Safest next sales-moving action:

- Use Merchant/Google publishing controls or a fresh propagation export to make the non-target duplicate rows disappear, then pass the guard before Canada/GB Shopping work.

## 2026-05-15 - Pinterest Path B Grouped Feed Generation

Reviewer verdict: `PASS_LOCAL_FALLBACK_READY__LIVE_UPLOAD_APPROVAL_REQUIRED`

Checked:

- Patched `ops/scripts/generate_pinterest_feed_grouped.py` to accept the repo's canonical Shopify credential keys without printing or persisting credentials.
- Generated local Path B grouped TSVs for `us`, `canada`, `united-kingdom`, `eu`, `australia`, and `international`.
- Each generated market feed has `6,969` rows, `326` unique parent groups, `0` missing `item_group_id`, and `0` supplier/source host hits.
- `python3.13 ops/scripts/check_pinterest_feed_grouping.py --report-only --strict` reports all `6` generated feeds PASS and the `3` upstream/live-equivalent snapshots still expected FAIL / `0` ERROR.

Risks:

- The generated feeds are local fallback artifacts only; they are not proof that the live Shopify Pinterest channel or Pinterest catalog has changed.
- Uploading/importing Path B would be a Pinterest catalog/source write and still requires separate exact owner approval plus after-state readback.

Required gates/fixes:

- Do not upload/import Path B, Save/Sync/Publish a channel setting, launch Pinterest, or attest the freshness marker without exact owner approval and post-sync readback.

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/PATH_B_GROUPED_FEED_GENERATION_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/`

Safest next sales-moving action:

- If the channel grouping toggle is unavailable, get separate exact approval to upload/import generated Path B feeds, then read back per-market grouped catalog rows after sync before launch review.
