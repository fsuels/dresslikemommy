# ROAS Guardrail Refresh

Date: 2026-05-07 EDT / 2026-05-08 UTC

Lane: ROAS / economics guardrails

Mode: local analysis only. No external systems opened or changed.

## Scope

This refresh tightens practical 650% ROAS rules for:

- Standard Shopping
- US nonbrand Search
- paused international Search
- Pinterest test candidates

It does not authorize any live spend, campaign enablement, paused import, budget edit, bid edit, status change, product-scope change, product-group change, feed-label change, conversion-goal edit, Merchant upload, Shopify product-data edit, Pinterest draft, or Pinterest spend.

Business-model constraint: Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. Platform availability and catalog labels are treated only as channel salability diagnostics, not physical-inventory claims.

## Evidence Used

- `AGENTS.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/AGENT_COORDINATION.md`
- `ops/BROWSER_SUBAGENT_COORDINATION.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- `ops/AGENT_WORKLOG.md`
- `dresslikemommy-growth-2026/00_MASTER/MASTER_RULES.md`
- `dresslikemommy-growth-2026/00_MASTER/DECISION_LOG.md`
- `dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-28-paid-spend-product-economics.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics/ROAS_ECONOMICS_GUARDRAILS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics/cpc_cvr_cpa_model.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/roas-economics/country_budget_implications.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-standard-shopping-cost-control-review/STANDARD_SHOPPING_COST_CONTROL_REVIEW.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-aggressive-controlled-growth-build/AGGRESSIVE_CONTROLLED_GROWTH_BUILD_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/ads-gate/GOOGLE_ADS_IMPORT_GATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/pinterest/PINTEREST_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/measurement/MEASUREMENT_REPORTING_REFRESH.md`

## Core Economics

| Metric | Planning Value | Conservative Value | Notes |
|---|---:|---:|---|
| AOV | `$70.00` | `$63.25` | `$70` is the current sprint planning assumption; `$63.25` is the older master benchmark. |
| Target ROAS | `6.50x` / `650%` | `6.67x` | Older rule uses a stricter 15% CAC cap. |
| Max CPA / CAC | `$10.77` | `$9.49` | Use `$10.77` as the planning ceiling and `$9.49-$10.50` when return, duty, translation, or tracking risk is present. |
| All-in non-marketing cost | `$35.00` | `$31.63` | Existing rule: product cost, shipping, and fees are modeled as 50% of selling price. |
| Contribution after target CPA, before returns/chargebacks | `$24.23` | `$22.14` | Returns, chargebacks, reships, customer-service drag, and duties friction still come out after this. |
| Ad spend share of revenue | `15.38%` | `15.00%` | `1 / 6.5` for the target, older master rule used 15%. |

Practical interpretation:

- `650% ROAS` means every `$1.00` of ad spend needs about `$6.50` in attributed revenue.
- At `$70` AOV, a purchase should cost no more than about `$10.77` in ad spend.
- At 50% all-in non-marketing cost, 650% ROAS still leaves about `$24.23` contribution before returns and chargebacks.
- The old `$9.49` CAC benchmark remains the conservative rule for weak-trust, international, stale-tracking, or higher-return situations.

## CPC And CVR Thresholds

| CPC | Purchase CVR Needed For 650% ROAS At `$70` AOV | Use |
|---:|---:|---|
| `$0.04` | `0.37%` | Economically forgiving Shopping click if query/product quality is clean. |
| `$0.05` | `0.46%` | Still safe for low-bid Shopping or discovery only. |
| `$0.08` | `0.74%` | Good lower-CPC international discovery ceiling. |
| `$0.10` | `0.93%` | Viable cold-test cap if traffic is high intent. |
| `$0.12` | `1.11%` | Good ceiling for lower-CPC EU/discovery campaigns. |
| `$0.15` | `1.39%` | Current US nonbrand and international Search packet cap. |
| `$0.20` | `1.86%` | Upper edge for clean Search tests; too high for weak cold traffic. |
| `$0.25` | `2.32%` | Expensive unless conversion quality is already proven. |

Rule of thumb: do not pay `$0.20` for unproven cold traffic unless the landing page, query intent, and early purchase CVR can plausibly clear about `1.86%`.

## Surface Rules

### Standard Shopping

Current known state:

- Live/eligible campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, campaign `23802638621`.
- Budget readback: `$20/day`.
- Scope remains `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- Catch-all `Everything else in "All products"` remains excluded.
- 2026-05-06 readback before cost control showed `81` clicks, `$18.58` cost, `$0.23` avg CPC, and `0.00` purchase conversion value.
- Approved cost-control change lowered included child product-group base bids from `$0.05` to `$0.04`, with budget/status/scope/goals unchanged.

Guardrail:

- Judge new performance separately from pre-2026-05-06 historical clicks because the bid reduction is not retroactive.
- Fresh readback is required before any budget, bid, status, product-group, product-scope, feed-label, or conversion-goal decision.
- If new effective avg CPC remains above `$0.20` with `0` purchase value, the economics recommendation is to request approval for the next smallest action: lower included child product-group bids from `$0.04` to `$0.03`, reduce budget, or pause the test.
- If post-bid-change spend reaches `$10.77` with `0` purchases, stop treating the campaign as "still learning" without a decision. Present the owner with a pause/reduce/lower-bid choice.
- If post-bid-change spend reaches `$16-$20` with `0` purchases or no strong checkout evidence, recommend a hard rollback decision.
- If a product group, product, or query theme spends about `$5` with irrelevant terms or no qualified shopper intent, recommend negatives, product exclusion, bid reduction, or pause after approval.

Scale rule:

- Do not scale Standard Shopping from clicks, CTR, product eligibility, or add-to-cart signals alone.
- Consider scale only after at least `3` primary-purchase conversions from the paid cohort with ROAS at or above `650%`, clean search terms, no supplier/source exposure, no Merchant paid-cohort regression, and no return/chargeback warning.
- If CPA is <= `$8.75` or ROAS >= `800%`, a future owner-approved budget increase should be gradual: `10%-20%` first for this live Shopping test, not a large jump.

### US Nonbrand Search

Current known state:

- Paused campaign: `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506`, campaign `23827590655`.
- Budget: `$2/day`.
- Bid strategy: Manual CPC.
- Default max CPC: `$0.15`.
- Structure: `12` ad groups, `36` exact/phrase keywords, `37` campaign negatives, `12` paused RSAs.
- No spend yet.

Guardrail:

- Keep paused until activation readbacks confirm campaign status, location option, Google Search only, no Display/Search Partners, account-default Purchases, ad policy, exact/phrase-only keywords, negatives, and max CPC at or below `$0.15`.
- At `$0.15` CPC, the campaign needs about `1.39%` purchase CVR to hit 650% ROAS at `$70` AOV.
- Start at `$2/day` only if approved; do not raise budget for the first learning window.
- Pause or rewrite a keyword/ad group immediately if search terms show wholesale/supplier, free/cheap-only, costume/Halloween mismatch, unrelated brands/IP, adult/NSFW, generic fashion without family-matching intent, or non-shopper research intent.
- If any ad group spends `$5` with no qualified product engagement or obviously weak terms, pause/narrow it.
- If campaign or ad group spend reaches `$10.77` with `0` purchases, pause or narrow unless the owner explicitly approves one more small learning window based on clean terms.
- If spend reaches `$16` with `0` purchases, hard pause that ad group or campaign.

Scale rule:

- Do not scale before `3` purchases and clean primary purchase value.
- CPA <= `$8.75` or ROAS >= `800%`: future approval can move `$2/day` to about `$2.50-$3/day`.
- CPA `$8.75-$10.77` or ROAS `650%-800%`: hold or increase only `10%-20%` after at least `3-7` days of stable clean data.
- CPA > `$10.77`: hold, tighten terms/ads/landing page, or reduce. Do not scale.

### Paused International Search

Current known state:

- Prior local packet proposes `17` non-US paused Search campaigns.
- Countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `GR`, `PT`.
- Local packet has `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` paused RSAs, and max CPC no higher than `$0.15`.
- It has not been imported, created, enabled, or spent.
- International live spend is blocked by public localized policy/page copy, route/currency/checkout QA, catalog/readback gates, and lack of exact action-time approval.

Guardrail:

- Keep local-only until the parent gets exact approval and just-in-time readbacks.
- Do not import/create paused campaigns until the approval gate is explicit, even though they would be paused.
- Do not enable or spend internationally until public policy/page copy, localized routes, currency behavior, no-payment checkout, tracking, Merchant/Pinterest catalog health, and country-level economics pass.
- Keep country campaigns segmented. Never blend countries into one test where winners and losers hide inside averages.
- At the current `$0.15` cap, each country still needs about `1.39%` purchase CVR for 650% ROAS. That is a high bar for unproven localized traffic.

Starting economics if future approval is given:

- `GB`, `CA`, `AU`: `$2/day` max each, `$0.15` cap. Do not allow `$0.20` until CVR proof can support `1.86%+`.
- `CH`, `DK`: `$1-$2/day`, `$0.12-$0.15` preferred because duties/language/trust friction can suppress CVR.
- `DE`, `NL`, `SE`, `FR`, `BE`: `$1/day` first, `$0.10-$0.15` cap after localization and checkout QA.
- `ES`, `IT`: `$1/day`, `$0.08-$0.12` preferred until stale localized copy is fully cleared and CVR is proven.
- `PL`, `CZ`, `RO`, `GR`, `PT`: `$1/day`, `$0.05-$0.12` preferred. Cheap CPC is useful only if exact/phrase traffic remains high-intent.

Kill rule:

- Country hard stop before spend: mixed-language page, stale policy/shipping copy, unclear returns/duties, bad currency/checkout behavior, untrusted conversion value, Merchant/Pinterest catalog uncertainty, or broad/loose keywords.
- If a country spends `$5` with weak terms or no qualified product engagement, pause that country/ad group.
- If a country spends `$9.49-$10.77` with `0` purchases, pause or narrow. Use the stricter `$9.49` line when translation, duties, shipping clarity, or return risk is not clean.
- If a country spends `$16` with `0` purchases, hard pause.
- If a country gets `2` purchases but CPA is above `$10.77` or ROAS is below `650%`, hold or reduce. Do not let a blended international portfolio hide that loss.

Scale rule:

- Country scaling requires at least `3` purchases in that country, clean search terms, clean purchase value, and no return/chargeback/duties complaint.
- CPA <= `$8.75` or ROAS >= `800%`: increase `20%-30%` every `3-7` days, but keep campaign-level caps low.
- CPA `$8.75-$10.77`: increase `10%-20%` only if the next readback stays clean.
- CPA above `$10.77`: do not scale; tighten or pause.

### Pinterest Test Candidates

Current known state:

- Pinterest official app pixel is on the official path and Events Overview showed fresh Tag/API events through Checkout and AddPaymentInfo.
- Event Quality still read `Fair`, updated `5/6/2026`.
- Remaining visible action items included Product ID in Add Payment Info, Email in Add to Cart, and Click ID in Checkout.
- EN Shopify data source read as completed with `5,663 of 5,663` items and `0` failed, but a sitemap source showed `Failed` and localized sources had warnings/fail counts.
- Exact current item-level paid candidate proof was not refreshed.
- No Pinterest campaign, draft, product group, catalog, pixel/tag/CAPI, budget, bid, audience, or spend write has approval in this lane.

Guardrail:

- Keep Pinterest draft/spend blocked until Event Quality and item-level candidate proof are refreshed and the parent has explicit approval.
- If approved later, start with USA-only retargeting/catalog candidates before any broad or international Pinterest spend.
- Use `$1/day` first. Pinterest should prove purchase economics before it gets broader discovery budget.
- Since Pinterest bidding may not map cleanly to CPC, translate performance back to effective CPC, CPA, and purchase ROAS. The same 650% math applies: `$0.15` effective CPC needs about `1.39%` purchase CVR; `$0.20` needs about `1.86%`.
- Catalog availability labels must be described as catalog salability only, not physical inventory.

Kill rule:

- No draft/spend if Event Quality remains stale/fair without a parent decision, exact candidate item proof is missing, USA-only targeting is not verified, or catalog source health is ambiguous.
- If a future `$1/day` test spends `$5` with no qualified clicks, saves, add-to-cart, checkout, or clean product engagement, pause or rebuild targeting/creative.
- If spend reaches `$10.77` with `0` purchases, pause unless the parent explicitly approves one more small retargeting window with strong checkout evidence.
- If spend reaches `$16` with `0` purchases, hard pause.
- If purchase CPA exceeds `$10.77` after `2` purchases, hold or reduce. Do not scale from saves, outbound clicks, or checkout starts alone.

Scale rule:

- Scale Pinterest only from primary purchase value and clean attributed ROAS.
- Require at least `3` purchases from the tested audience/product group before scale.
- CPA <= `$8.75` or ROAS >= `800%`: raise by `20%-30%` after `3-7` days.
- CPA `$8.75-$10.77`: hold or raise only `10%-20%`.
- CPA above `$10.77` or ROAS below `650%`: do not scale.

## Portfolio Control

- New approved tests should add no more than `$10-$15/day` total incremental spend until the first clean purchase-value readback.
- Full international discovery should not exceed `$20/day` incremental spend until at least one country proves CPA near or below `$10.77`.
- Existing live Standard Shopping must not be budgeted, paused, re-enabled, product-scoped, or structurally changed by this lane.
- PMax and Remarketing stay out of this refresh. PMax remains blocked; Remarketing remains paused/policy-gated unless a separate fresh approval changes that.
- Use primary purchase value and `Conv. value / cost` for ROAS decisions. Do not use pre-cleanup `All conv. value` that may include micro-conversion value.

## Decision Rules In Plain English

- At `$70` AOV, one target-CPA learning window is about `$10.77`.
- Spending one target-CPA window with no purchases should force a decision, not passive continuation.
- Spending about `$16` with no purchases is the hard-pause zone for any narrow ad group, country, or Pinterest test.
- CPC above `$0.20` is expensive unless purchase CVR is already near `1.86%` or better.
- Scale only after purchases, clean value, clean terms, and no return/chargeback warnings.
- Cheap CPC is useful only when traffic can convert; cheap low-intent clicks are still waste.

## Residual Risks

- AOV is a working assumption. Recompute with `target_cpa = AOV / 6.5` when fresh AOV changes materially.
- The 50% all-in non-marketing cost rule is an operating model; actual returns, chargebacks, duties, reshipments, and support costs can lower contribution.
- Small budgets learn slowly, but that is intentional cash control while feed, tracking, and international readiness are still being cleaned up.
- Google Ads and Pinterest attribution can lag. Avoid overreacting to same-day ROAS, but do not let unqualified spend pass the hard caps.
- This lane did not update `ops/AGENT_WORKLOG.md` because the subagent ownership instruction allowed writes only under this lane folder.

## Files Written

- `ROAS_GUARDRAIL_REFRESH.md`
- `roas_guardrail_summary.csv`

