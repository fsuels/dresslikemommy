# Dress Like Mommy: profitable growth through December 31, 2026

**Status: audit and local preparation; live launch remains gated.** This plan is grounded in the September 5 account, Shopify and public readbacks. It is not a forecast or a claim that sales have already improved. Active task status belongs in `ops/marketing/action_queue.md`; this dated packet preserves the decision and its evidence.

## Objective and owner decisions

Maximize profitable sales before year-end. Preserve a 30% profit target; owner estimates 50% of each sale covers all costs except marketing and returns, leaving 20% for those two categories. Respect CPC <= USD 0.15. USD 50 is an initial marketing test amount, with willingness to fund USD 500 or more when profitable results justify it. Because the first answer did not distinguish daily from total, use 50 total as a temporary exposure planning safeguard and bind each exact amount/window at launch. It is not a permanent ceiling. The million-dollar aspiration is not yet a supported year-end forecast.

## What the evidence says

| Evidence | Meaning and limits | Keep or change |
|---|---|---|
| Shopify Aug 8–Sep 4: 8 orders,$734.99 merchandise net,$760.97 total; prior 28 days 16 orders,$928.29 net | Sales weakened despite10,393 vs 3,545 sessions. Aggregate orders are not yet paid/noncancelled order truth. | Prioritize qualified acquisition and buyer conversion. |
| Desktop 8,545 sessions / 0 completed checkouts; mobile 1,832 / 8; direct 8,679; unrecognized trafficheap 508 / 0 carts / 0 completed | Strong quality/attribution investigation signal; not proof of bots. Mobile conversion also declined. | Investigate sources and consent/attribution; no blind country/referrer blocking. |
| GSC Aug 7–Sep 3: 911 clicks vs 812; about 41.5K impressions; CTR 2.2% vs 2.4% | Organic demand exists. Different dates/timezone/definitions from Shopify prevent a naive parity comparison. | Keep localized SEO infrastructure; improve pages already earning impressions. |
| Denmark 4 orders / $444.73 net in 90 days, 13 orders in 365 days; GSC 101 clicks; US 26 orders / $2,112.18 net in 90 days | US is the largest sales base; Denmark is an overseas validation candidate with both demand and orders. Small samples do not prove CPC or profitability. | Validate one Danish buyer path while preparing one US control. |
| GA4 28 days 5 purchases / $432.20 displayed (currency configuration unverified) vs Shopify 8 orders / USD 734.99 net; 90 days 36 vs 47 | Aggregate discrepancy needs transaction, status, time, consent and currency reconciliation. Channel rows also do not sum to GA4 total. | Reopen the falsely closed parity problem; do not scale on GA4 totals. |
| Golden Daisy selection/cart/hosted checkout worked; caption and cart-count issues remain | Checkout is not universally broken. No payment placed; mobile winner/destination path needs its own check. | Preserve the flow; release the existing small corrections through isolated preview. |
| Spanish/French mixed copy and unsupported numerical trust claims; 17 public page attempts, 16 HTTP 200, 1 rate-limited | Translation presence is not language quality. This is a sample, not full-store clearance. | Repair exact customer-facing strings and high-demand pages first. |
| Pinterest paused / $0 recent spend; source 210 ingested; detailed event quality Fair;420 catalog rows organic-limited by stale data | Infrastructure is reusable; source ingestion and received Checkout events do not establish attributed sales. | Keep organic opportunity; diagnose exact stale/source/attribution scope before paid relaunch. |
| Ads operating account unavailable; Merchant explicit noaccess | No current Google spend or feed eligibility conclusion is possible. | Restore app/account access; the same documented identity is already signed in. Do not treat manager zeros as business results. |

Evidence: `analytics_seo_audit.md` and three aggregate JSON files; `google_audit_report.md`, `google_campaign_buildsheet.json`; `cro_audit_report.md`, public scan and existing patch manifest; `pinterest_merchant_readback.md`. Account windows and exclusions are retained in those reports. Known CRO synthetic cart/checkout events approximately 22:35–22:43 UTC September 5 must not become sales/learning outcomes.

## Socratic decision tests

1. **Is lack of traffic the whole problem?** No: sessions nearly tripled while orders halved. Falsifier for poor traffic quality: independently measured human visits and improved purchase counts in the same source/cohort. Until then, traffic totals are diagnostic.
2. **Are foreign markets automatically cheaper and better?** Unknown. Denmark has real demand; lower CPC, actual costs, delivery reliability and Danish purchase-flow quality remain unproven. Reject a market if it cannot meet the profit requirement, regardless of cheap visits.
3. **Can USD 0.15 clicks retain 30% profit?** Only at adequate conversion and order value. The calculator below tests that premise without inventing inputs.
4. **Should we rebuild the store or campaigns?** Not wholesale. Working checkout, existing content, verified product IDs, localized architecture and paused campaign assets should be reused after fresh checks. Existing June fixes were prepared but not fully released; more duplicate patches would not help.
5. **What would justify aggressive scale?** Reconciled paid orders, conservative return-adjusted contribution, repeatable conversion, reliable fulfillment and a measured next budget step. A cheap CPC, one order or platform-reported ROAS alone is insufficient.

## Economics and reinvestment

Let B be booked merchandise revenue after discounts, before refunds, excluding collected tax; C all actual non-ad costs net of recoveries; R refunds/extra return handling not already included in C; A ads. Profit=B−C−R−A. Costs and return loss must be disjoint: a recovery reducing C cannot reduce R again. If using net revenue already reduced by refunds, do not subtract those refunds again. State the denominator used for the 30% target. TA-03 must also reconcile the recent USD25.98 shipping-revenue split into standard versus upgrade charges, costs and refund treatment; the aggregate alone does not contradict shipping-inclusive standard pricing.

The owner's simplified planning model gives ad allowance=20%−incremental return-loss rate. Required ROAS=1/ad allowance; allowed CPA=booked AOV×ad allowance; economic CPC=allowed CPA×qualified paid conversion rate, capped at USD 0.15. Negative/unknown allowance prevents a spend recommendation.

| Illustrative return loss, not verified | Max advertising share | Required booked-revenue ROAS | CPA ceiling on $100 order |
|---:|---:|---:|---:|
| 0% |20%|5.00x|$20.00|
| 3% |17%|5.88x|$17.00|
| 5% |15%|6.67x|$15.00|
| 5.685% |14.315%|6.99x|$14.32|
| 10% |10%|10.00x|$10.00|

Keep the existing 650% ROAS discipline as a floor for campaign planning, with a stricter threshold whenever actual contribution requires it. At 650%, only 4.615% of booked revenue remains for return loss under the owner's 50% cost assumption. Annual Shopify sales reversals were 5.685% of gross less discounts, but reversals include edits/cancellations and are not cohort return losses; the table is a sensitivity analysis, not a validated reserve.

`ops/scripts/plan_marketing_economics.py` requires explicit order value, cost rate, return-loss rate, profit rate, conversion rate and CPC cap. Example only: $100 order, 50% cost, 5% return loss, 30% profit, 1% CVR gives $15 CPA / $0.15 CPC; 0.5% CVR only supports $0.075 CPC. Six decision tests cover these cases, missing inputs, invalid rates and no positive ad allowance.

Initial pilot: choose one narrow product/intent/market, not a simultaneous broad rollout. Candidate Google Search copy is built locally; existing sold-product Shopping campaign 23867953136 is a reuse candidate once current item eligibility is verified. Bind exact IDs, presence targeting, language, bid, daily exposure and cumulative stop before launch; Google average daily budgets can overdeliver, so a daily setting is not a lifetime cap. No positive bid adjustments, broad match, PMax, Display, Search Partners or unreviewed remarketing in this proposed pilot.

At T+24, zero impressions triggers eligibility/auction/volume diagnosis, not a bid increase above $0.15. Spend checkpoints at approximately half and one allowable CPA trigger review/hold when qualified signal or purchases are absent; these are capital-protection rules, not statistical proof of failure. Stop breaches immediately within exact authority; do not repeatedly reset a failing test to consume a larger budget. Assess conversion lag before declaring results mature.

Scale review can start after multiple independently verified purchases across more than one day at the required contribution/CPA, with a conservative return reserve and no attribution/fulfillment problem. A proposal of 5 paid purchases is a screening checkpoint, not statistical certification. Release the next budget in measured steps, initially 20–30% of the prior daily rate as a proposed safeguard; change one major variable at a time and recheck after 48–72 hours plus the relevant conversion lag. Faster or USD 500+ expansion remains available when order volume, uncertainty and cash exposure support an exact larger stage. Cohort profit, not the original $50, controls ambition.

## Execution sequence and task ownership

| Window from cleared dependencies | Work and subtasks | Completion evidence |
|---|---|---|
| First 48 hours | TA-01 account access/current spend; TA-02 purchase/source reconciliation; TA-03 exact cohort margin; TA-04 isolated homepage/cart preview; TA-05 valuable 404 / 5xx classification | Correct account readbacks, paid-order join, actual cost/return worksheet, independent preview QA, scoped redirect list. |
| Days 3–7 | TA-06 existing Danish/Greek/Norwegian commercial SEO changes; TA-07 free listings; TA-08 one paid cohort/keywords/ad copy; TA-09 reviewed initial test | Published changes only after exact diff/authority; clean free-listing rows; exact campaign/readback and loss clock. |
| Weeks 2–4 | TA-10 Danish challenger; TA-11 Pinterest organic drafts; TA-12 exact source/events repair; retire failing tests and reuse winning pages/products | Country-level contribution, qualified clicks/purchases, confirmed query/landing fit, reviewed scale decision. |
| October–December | Expand proven occasion/product-country combinations; verify seasonal demand and delivered-by-date evidence before holiday promises; weekly profit/cash review | Increasing contribution dollars and repeatable purchases; actual return/fulfillment outcomes feed future allocations. |

These are execution targets, not promises of rankings, orders or account access by those dates. Do not stop independent local/SEO work while one account lane is unavailable.

## The durable operating system

Use the existing `ops/marketing/` command layer. Root owns priorities, integration and external writes. Google, analytics/SEO, CRO, Merchant/Pinterest specialists own disjoint evidence; a separate reviewer challenges material decisions. `action_queue.md` contains TA-01–13 and their subtasks/dependencies; `daily_scorecard.md` owns dated measurements; `decision_log.md` preserves frozen predictions and later outcomes; `PROBLEM_TRACKER.md` owns unresolved defects; `operator_cockpit.html` is generated from those records.

The dashboard now marks saved campaign cards as historical and collapses them when full reconciliation is incomplete. It does not reinterpret old ACTIVE labels as current status.

At every material checkpoint or context handoff: update the owning task and evidence, distinguish VERIFIED/INFERRED/UNKNOWN, record the next decision and its trigger, release only this task's claims, and append one worklog anchor. Resume via the existing canonical paid-growth prompt. No second agent memory tree, new website AI surface, or unattended spending automation was created. Reviewer badges must not infer current approval from old log text; that display defect is corrected locally in this pass.

## Danish buying-path correction

The Skyfade Danish product route is active and displayed DKK pricing, but its recently viewed cart card showed `$131.0` and linked without the Danish prefix. The new local cart change removes unreliable cached prices and preserves the current locale in validated product links. The existing quantity and subtotal corrections remain intact. Local tests and a fixture can validate this JavaScript; only an isolated live-theme preview and post-publication readback can prove the storefront is repaired.

The same product exposes an internal supplier-research sentence and several untranslated purchase labels. Prepare the exact Danish translation-resource diff after a current content digest; omit the internal research clause without inventing a fiber claim. Keep the Denmark paid pilot gated until its complete buying path is verified.

## Scope still unfinished

Google operating-account metrics and Merchant eligibility require restored app access for the already signed-in, historically documented identity. Order-level attribution, actual landed costs/return recovery, delivery performance, every SKU/locale/market, full payment methods, email retention, and legal/tax/service-policy accuracy are not fully audited. This packet cannot certify 30% realized profit or launch readiness. GA4's Ads link was tested and redirected to the manager; GA4 has no Merchant link. Support submission is already owner-authorized but NOT SUBMITTED after inconsistent email/summary validation and automatic approval-review rejection. The next owner action is only to manually correct Contact email/optional CC for a fresh readback before the approved send. Business Manager shows the documented user as Super admin, but that role does not confer the missing app permissions. The cause is unknown. See `google_access_recovery.md`; this supersedes the initial wrong-login inference.

Continuation: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, anchor `2026-09-05-ceo-turnaround-audit-harness`. Current authority and remaining gates come from the command layer, never this dated packet alone.
