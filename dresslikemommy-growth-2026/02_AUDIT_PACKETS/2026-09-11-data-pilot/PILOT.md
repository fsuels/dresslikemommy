# Dress Like Mommy — small Data pilot

Prepared September 11, 2026. Existing records only; no live reads, account changes, new infrastructure or plugin installation.

**Result: the saved data supports a reproducible sales/funnel baseline, but cannot support a product/market profit ranking or contribution after advertising.** The smallest useful continuation is completion of an existing order-cost join, not a new dashboard platform.

The requested preparation is complete. Analysis used Codex, the Data Exploration/Data Validation skills and standard-library Python. **The newly announced OpenAI Data plugin was not run or benchmarked.** This packet is a ready input and acceptance test for that later comparison.

## Question and fixed scope

Question: which products and markets generated positive contribution after advertising, and which conclusions remain uncertain?

Use **August 10–September 8 inclusive: 30 complete dates in America/New_York**, captured September 9 at 16:44:25 UTC. This is the latest located saved exact-30-day aggregate baseline, not the latest live reporting window. USD follows the saved store/report context; the primary MONEY cells do not carry an explicit ISO code and do not establish settlement currency. No post-release lift is measured: the September 10 article and Pin were released after this baseline ended.

Authoritative source: [saved Shopify baseline](../2026-09-09-organic-growth/shopify_baseline.json). Exact input hashes, periods, grain and inclusion decisions for ten files are recorded in [source_inventory.json](source_inventory.json). The search was bounded to relevant existing packets; absence here is not proof that a provider lacks the data.

## Reconciled baseline

| Measure | Recorded result | Interpretation |
|---|---:|---|
| Orders in sales report | 10 | Aggregate report count; full-window payment/cancellation/test eligibility not audited |
| Net merchandise sales | $821.44 | Discounts and sales reversals both zero in this source |
| Shipping charged to customers | $25.98 | Revenue; not the cost of delivery |
| Total sales including shipping | $847.42 | $821.44 + $25.98 + $0 tax |
| Sessions | 4,896 | QA/bot exclusions not independently established |
| Sessions with cart additions | 115 | 2.348856% of sessions |
| Sessions reaching checkout | 27 | 23.478261% of cart sessions |
| Sessions completing checkout | 10 | 0.204248% of sessions; not independently verified retained orders |

Four order-referrer groups sum to 10 orders and $847.42. All four device groups sum to 4,896 sessions, 115 cart sessions and 10 completed-checkout sessions. The equality between ten reported orders and ten completed sessions is a cross-check, not a transaction-level join.

Useful descriptive findings:

- Mobile has 1,980 sessions, 99 cart sessions and all 10 observed completed-checkout sessions. Desktop has 2,899 sessions, 16 cart sessions and zero recorded completions. This supports keeping mobile buyer verification relevant; it does not prove a desktop defect or justify a current campaign change.
- The Google search-labeled session group has 1,096 sessions and five completed-checkout sessions. That label does not establish organic-only acquisition or incremental sales.
- One unknown-source traffic group has 508 sessions and no recorded carts or completed checkouts. Investigate source quality before treating more visits as growth; this alone does not prove bot traffic.
- Top-15 session referrers cover 4,889 sessions, leaving **7** outside the list. Top-12 session countries cover 4,146 sessions and eight completions, leaving **750 sessions and 2 completions** outside the list. These subsets are not whole-store totals, and session country is not buyer shipping market.

Machine-readable results: [analysis.json](analysis.json), [metrics.csv](metrics.csv). Unknown financial outputs are null/blank, never zero.

## What other existing sources can and cannot contribute

| Source group | Useful evidence | Why it cannot close this 30-day profit question |
|---|---|---|
| Six selected historical baskets | Actual provider components total CNY1,551.13; recorded USD fees total $23.86; $595.54 − $23.86 = $571.68 in payout allocations | Selected from a 90-day population. Sanitized rows omit order dates/private mappings; actual USD provider settlements are null. Funding scenarios do not establish realized FX or profit. |
| Recent two-order checkpoints | Order-status, quantities and product/basket matching; separate native-currency fees | Rolling window overlaps the baseline. Repeated heartbeat copies are not additional sales. Full delivered and acquisition costs remain unresolved. |
| Existing Shopify/GA4 reconciliation | 28-day and 90-day purchase matching summaries | Cannot re-window aggregate summaries to these 30 dates; private transaction-level inputs were outside this task's scope. |
| Italian campaign cost readback | Historical campaign spending and reported purchase value | 90-day totals plus one separate day; not daily all-account spend. Attribution and order truth remain distinct. |
| April margin/CAC pack | Historical order/line structure and a reusable field map | Annual window outside this pilot; all 7,324 variant costs follow half-current-price modeling. The 50% expense assumption is not actual cost. |
| September 11 Microsoft planning analytics | More recently captured Shopify data | August sales covers 31 days; session data covers 90 days. Freshness does not make incompatible dates comparable. |

The primary baseline also contains a **90-day top-products report**. It is explicitly excluded from 30-day product ranking. Adding its product order counts would risk counting the same order more than once.

## Minimum data contract for a profit answer

[required_fields.csv](required_fields.csv) specifies seven datasets, their grain, missing fields and validation rules. The important requirements are:

1. Eligible orders and lines for the exact window, joined through protected aliases to exact products, variants and quantities. Private order IDs and alias mappings remain outside repository artifacts.
2. Actual item/service/freight/duty charges and credits; payment fees; settled currencies and supported FX allocations. Count each expense or recovery once. Shopify shipping revenue is not carrier cost.
3. Complete daily campaign/account spend for the same reporting window and currency basis, with deduplicated purchase attribution and an explicit unattributed bucket.
4. A stated refund/dispute/return maturity cutoff. An as-of contribution calculation is not final retained profit.

Working definition for this pilot: **contribution after advertising = consistently defined net merchandise revenue + retained shipping revenue − actual variable fulfillment costs − processing/FX fees − other nonduplicated variable losses − advertising cost.** Tax collected is excluded. Do not subtract refunds again if already reflected in the revenue basis. Allocated fixed overhead is separate from contribution and is required for an all-in profit claim.

ROAS requires explicitly attributed revenue divided by matching advertising cost; CPA requires that cost divided by qualified attributed purchases. Missing spend, uncertain attribution, or a zero denominator yields an unavailable result, not a fabricated ratio. No product allocation rule is assumed for account-level spending.

## Acceptance test and decision

The frozen evaluation criteria for a later Data-plugin run are:

| Criterion | Expected behavior |
|---|---|
| Baseline fidelity | Return 10 reported orders, $821.44 net merchandise, $847.42 total sales, 4,896 sessions and 0.204248% completion/session ratio |
| Correct aggregation | Reconcile devices/order referrers; preserve top-N residuals; do not join session and order aggregates as individual transactions |
| Period discipline | Exclude 90-day products, 28-day reconciliation, rolling checkpoints and August 31-day sales from this 30-day calculation |
| Financial discipline | Withhold profit rankings, CPA and ROAS until costs, currency and attribution are adequately matched |
| Evidence and execution | Cite source paths/date/filter definitions; no account changes, installation, public sharing or invented data |

**Preparation validation:** 45 schema, period, arithmetic, coverage and unknown-value checks pass. Reproduce without modifying output:

```bash
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-data-pilot/reproduce.py --check
```

This establishes a reference answer and exposes known limits. It does not measure the new plugin's accuracy, reporting time savings, new purchases or profit lift. A later run passes only if it satisfies every criterion above; a plausible-looking profit figure from these incomplete inputs is a failure.

Alternative considered: purchase/connect a warehouse and build another dashboard. Existing local records already support the descriptive analysis, while the unresolved expense/attribution joins would remain. Keep using the existing cockpit and records until those inputs support a useful financial decision. No durable workflow or prompt rule is changed by this pilot.

**One next evidence action within this pilot:** continue existing **TA-16**, obtaining actual item/service/freight/duty and settlement charges for the already recorded fulfilled Rainbow basket, using its existing protected mapping. This is a small, identifiable cost gap; even after it is filled, attribution and return maturity must be resolved before claiming retained profit. Do not repeat completed cost-source discovery for the separate six historical baskets. Global owner priorities and other operators' claims remain unchanged.

## Authority, review and continuity

- `task_stage`: `HANDOFF`
- `source_live_evidence_as_of`: `2026-06-01` (inherited authoritative control; not the pilot snapshot date)
- `pilot_saved_source_as_of`: `2026-09-09T16:44:25.080Z`
- `live_state_mode`: `STALE_READBACK_REQUIRED`
- `effective_approval_policy`: `FRESH_ACTION_TIME_APPROVAL_REQUIRED`
- `approved_external_scope`: `NONE`
- `decision_depends_on_uncertain_state`: `true`
- `decision_changing_evidence`: complete period-bound order, actual cost, settlement and campaign attribution joins
- `if_evidence_supports_recommendation`: validate the completed basket and repeat the bounded profit analysis through the existing cost/measurement lanes
- `if_evidence_opposes_recommendation`: retain unavailable financial outputs and correct the exact missing or conflicting input
- `material_decision`: `NOT_MATERIAL` (local preparation; no spend, launch, blocker reclassification or permanent rule change)
- `independent_verifier`: `data_pilot_verifier`
- `verifier_independence`: `DID_NOT_BUILD_OR_EXECUTE`

Review verdict is recorded in [independent_review.json](independent_review.json). Source files and existing order cohorts remain unchanged. This packet is a dated evidence artifact, not a new command layer. Remove only this packet and its added continuity references to reverse the local preparation; preserve all pre-existing work.

Continue using [the canonical growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md), with anchor `2026-09-11-read-only-data-pilot` and this packet as evidence. Current scope remains existing-records analysis; later live evidence collection must follow the existing task/account owners and authority.
