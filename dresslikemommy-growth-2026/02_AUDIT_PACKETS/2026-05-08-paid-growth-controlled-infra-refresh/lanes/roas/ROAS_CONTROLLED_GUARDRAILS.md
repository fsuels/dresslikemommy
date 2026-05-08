# ROAS Controlled Guardrails

Date: 2026-05-08
Lane: ROAS / economics subagent
Mode: local model only. No external accounts opened or changed.

## Scope

This refresh updates the operating guardrails for a `650%` ROAS target across:

- paused Search tests
- live Standard Shopping monitoring
- Pinterest US draft readiness
- country-level international test budgets

It does not authorize live spend, campaign import/create/enable/pause, budget edits, bid edits, conversion-goal edits, product-scope changes, product-group changes, feed-label changes, Merchant uploads, Shopify product-data edits, Pinterest drafts, Pinterest product groups, or Pinterest spend.

Business-model constraint preserved: Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. Availability/catalog labels are channel salability diagnostics only, not claims of stocked physical inventory.

## Evidence Used

- `AGENTS.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/AGENT_COORDINATION.md`
- `dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-28-paid-spend-product-economics.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics/ROAS_ECONOMICS_GUARDRAILS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/roas/ROAS_GUARDRAIL_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/PAID_GROWTH_PT_PRESENTMENT_URL_READBACK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/measurement/MEASUREMENT_CONTROLLED_READBACK.md`

## Core Economics

Target ROAS formula: `max CPA = revenue / 6.5`.

Prior packets use `50%` all-in non-marketing cost as the operating margin model. That means product cost, shipping, and fees consume about half of revenue before ad spend, while returns, chargebacks, reships, customer-service drag, and duties friction still need to be watched separately.

| AOV Scenario | Target ROAS | Max CPA | All-In Non-Marketing Cost At 50% | Contribution After Target CPA, Before Returns/Chargebacks | Notes |
|---:|---:|---:|---:|---:|---|
| `$63.25` | `650%` | `$9.73` | `$31.63` | `$21.90` | Older benchmark AOV. Prior conservative CAC rule was `$9.49` from a 15% cap. |
| `$70.00` | `650%` | `$10.77` | `$35.00` | `$24.23` | Current sprint planning AOV. |

Practical interpretation:

- At `$63.25` AOV, one target-CPA learning window is `$9.73`.
- At `$70.00` AOV, one target-CPA learning window is `$10.77`.
- Use `$9.49-$9.73` as the conservative decision band when tracking, localization, duties, return risk, or product mix is weaker.
- Use `$10.77` as the normal planning ceiling only when purchase value, landing page, product scope, and query quality are clean.
- The old 15% CAC cap is slightly stricter than `650%` ROAS at `$63.25`; it remains useful as a cash-control floor.

## CPC / CVR Break-Even

The attached `cpc_cvr_guardrails.csv` gives the exact thresholds for CPC values `$0.04`, `$0.10`, `$0.15`, `$0.20`, and `$0.25` across both AOV scenarios.

| CPC | CVR Needed At `$63.25` AOV | CVR Needed At `$70` AOV | Operating Read |
|---:|---:|---:|---|
| `$0.04` | `0.41%` | `0.37%` | Very low-bid Shopping can work if query/product quality is clean. |
| `$0.10` | `1.03%` | `0.93%` | Viable for cold exact/phrase testing with strong intent. |
| `$0.15` | `1.54%` | `1.39%` | Current paused Search cap; still needs real buyer intent. |
| `$0.20` | `2.06%` | `1.86%` | Upper edge; do not use for weak cold or mixed-language traffic. |
| `$0.25` | `2.57%` | `2.32%` | Expensive; only defensible after proven CVR and clean ROAS. |

## Paused Search Test Rules

Current known Search infrastructure:

- US nonbrand paused campaign `23827590655`: `$2/day`, Manual CPC, `$0.15` max CPC, exact/phrase only.
- International Search remains local-only / parked: `17` proposed non-US paused campaigns, max CPC no higher than `$0.15`, no import/create/enable/spend approval.

Activation prerequisites:

- Fresh approval and just-in-time readback.
- Campaigns are paused before any import/build.
- Google Search only, no Display expansion.
- Presence-only location targeting.
- Purchase conversion value is trusted; micro-conversions do not inflate ROAS.
- Exact/phrase positives only with strict negatives.
- Final URLs use country-qualified localized paths where proven, not bare language paths.

Budget rules if approval is later granted:

- US nonbrand: keep `$2/day`; do not scale during the first learning window.
- Priority English markets `GB`, `CA`, `AU`: `$2/day` each, `$0.15` cap.
- `CH` and `DK`: `$1-$2/day`, `$0.12-$0.15` preferred.
- Broader EU `DE`, `NL`, `SE`, `FR`, `BE`: `$1/day`, `$0.10-$0.15`.
- ES/IT/PT: `$1/day`, `$0.08-$0.12` until localized traffic proves conversion quality.
- PL/CZ/RO/GR: `$1/day`, `$0.05-$0.12`.

Kill rules:

- Pause or narrow any ad group/country after about `$5` spend with weak search terms or no qualified product engagement.
- At `$9.49-$10.77` spend with `0` purchases, force a pause/narrow/owner-decision. Use `$9.49-$9.73` for weaker or international cases.
- At `$16` spend with `0` purchases, hard pause the ad group/country.
- After `2` purchases, hold or reduce if CPA is above the relevant max CPA or ROAS is below `650%`.
- Do not scale from CTR, add-to-cart, checkout starts, or cheap clicks alone.

Scale rules:

- Require at least `3` purchases in the campaign/country, clean primary purchase value, clean search terms, and no return/chargeback/duties warning.
- CPA <= `$8.75` or ROAS >= `800%`: a future owner-approved increase can be `20%-30%` every `3-7` days for new paused Search tests.
- CPA between `$8.75` and the target max CPA: hold or increase only `10%-20%`.
- CPA above target max CPA: do not scale; tighten terms, CPC, country, landing page, or pause.

## Standard Shopping Monitoring

Current known state:

- Campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` / `23802638621` remains live/eligible.
- Budget is `$20/day`.
- Scope remains `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- Catch-all `Everything else in "All products"` remains excluded.
- Included child product-group base bids were lowered to `$0.04` in the prior approved cost-control pass.

Monitoring rules:

- This ROAS lane makes no Standard Shopping edits.
- Judge new economics separately from historical clicks before the `$0.04` bid change.
- Fresh readback is required before any recommendation to change bids, budget, status, product groups, product scope, feed labels, or conversion goals.
- If post-bid-change spend reaches one target-CPA window with `0` purchases, the parent should request an owner decision: hold briefly with evidence, reduce/lower bids, or pause.
- At `$16-$20` post-bid-change spend with `0` purchases and no strong checkout evidence, recommend a hard rollback decision.
- If a product/query cluster spends about `$5` with irrelevant or low-intent traffic, recommend negatives, product exclusion, lower bid, or pause after approval.

Scale rules:

- Do not scale Standard Shopping from clicks, CTR, product eligibility, or add-to-cart signals alone.
- Consider scale only after at least `3` primary-purchase conversions from the paid cohort, ROAS at or above `650%`, clean search terms, no Merchant/source regression, and no return/chargeback warning.
- If approved later, the first Shopping scale step should be conservative: `10%-20%`, not a large jump.

## Pinterest US Draft Readiness

Current known state from latest stored evidence:

- Pinterest advertiser `549756244483`.
- Campaign baseline: `0 campaigns`, `0 currently being served`, `$0.00` spend.
- Event Quality remains `Fair`, updated `2026-05-06`.
- Tag and CAPI events are fresh in latest evidence, but quality gaps remain.
- EN Shopify source had `5,663/5,663`, `0` failed, `152` warnings.
- Separate sitemap source still failed.
- Current item proof from the later unblock packet supersedes the earlier `337/346` blocker: `342` EN-US in-stock rows are clean, with exactly `4` excluded variants.

Draft/spend rules:

- Keep Pinterest drafts/spend parked until Event Quality/catalog/item proof is refreshed and exact owner approval exists.
- Future first draft should be USA-only and should use only `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`, excluding the `4` rows in `pinterest_us_unresolved_exclusions_4.csv` unless a fresh just-in-time readback re-resolves them.
- Start at `$1/day` only after gates pass and approval is explicit.
- Translate Pinterest performance back to effective CPC, CPA, and purchase ROAS. The same max CPA math applies.
- Do not call catalog availability physical inventory; it is only channel salability.

Pinterest kill rules:

- No draft/spend if Event Quality stays stale/Fair without a parent acceptance decision, item proof is missing, USA-only targeting is not verified, or catalog source health is ambiguous.
- At `$5` spend with no qualified clicks, saves, add-to-cart, checkout, or clean product engagement, pause/rebuild targeting and creative.
- At one target-CPA window with `0` purchases, pause unless the parent explicitly approves one small retargeting window based on strong checkout evidence.
- At `$16` spend with `0` purchases, hard pause.
- Do not scale from saves, outbound clicks, or checkout starts alone.

## RO Currency Caveat

Romania now correctly presents in `RON`, not EUR, when using country-qualified URLs. RO economics should use RON local revenue and local reported value, or a documented FX-normalized value, before comparing CPA/ROAS against USD planning thresholds.

Do not compare raw RON order value to USD ad spend without currency normalization. Do not assume EUR for RO.

## Portfolio Controls

- New approved tests should add no more than `$10-$15/day` total incremental spend until first clean purchase-value readback.
- Full international discovery should stay at or below `$20/day` incremental spend until at least one country proves purchase CPA near or below target.
- Keep countries segmented so losers do not hide inside blended averages.
- PMax and Remarketing remain outside this lane.
- Use primary purchase value / cost for ROAS decisions, not stale all-conversion value that may include old micro-conversion values.

## Files In This Lane

- `ROAS_CONTROLLED_GUARDRAILS.md`
- `cpc_cvr_guardrails.csv`
- `country_budget_guardrails.csv`
- `summary.json`
