# Current sales, campaign candidates and margin evidence

Read September 5 EDT / September 6, 2026 UTC. **The sales reconciliation is complete for the fixed windows below. Actual net profit remains unverified because invoice-backed fulfillment costs are missing.** No account, campaign, tracking, product or billing setting changed.

Both Shopify and GA4 were freshly verified as USD / America/New_York. Shopify shop15571635 is Dress Like Mommy / www.dresslikemommy.com; GA4 is account88409806/property330266838. Root read Shopify orders, lines, refunds and current variant costs; the independent Analytics lane read the existing Chrome test Transactions reports. September5 partial-day activity is excluded.

## The actual purchase gap

| Measure | Aug8–Sep4,28 complete days | Jun7–Sep4,90 complete days |
|---|---:|---:|
| Shopify orders before exclusions | 8 | 47 |
| Paid, noncancelled Shopify orders | 8 | 45 |
| Cancelled, refunded orders | 0 | 2 |
| Test orders | 0 | 0 |
| Retained merchandise sales, USD | 734.99 | 3,616.78 |
| Total sales including shipping, USD | 760.97 | 3,708.90 |
| GA4 purchase transactions | 5 | 36 |
| GA4 purchase revenue, USD, rounded once | 432.20 | 2,612.69 |
| Retained paid orders matched to GA4 | 5 | 34 |
| Retained paid orders missing from GA4 | 3 | 11 |
| Merchandise sales on those missing orders, USD | 302.44 | 1,141.26 |

All **36 GA4 transaction IDs matched Shopify uniquely**, with no unmatched IDs, duplicates, ambiguous matches or local-calendar-date mismatches. GA4 includes both cancelled/refunded orders. Therefore the correct retained-sales comparison is34 matched versus45 paid orders, rather than treating all36 GA4 events as retained purchases. The two cancellations explain why Shopify's gross order count exceeds paid/noncancelled orders; they do not explain the11 missing paid orders.

For the recent28d, the five matched Shopify orders contain USD432.55 merchandise, and the three missing orders contain USD302.44: together they reconcile exactly to USD734.99. GA4's full-precision matched value is USD432.204968, a difference of negative USD0.345032. Over90d the36 matched Shopify purchases originally contained USD2,612.23 merchandise, versus GA4 USD2,612.691065, a difference of positive USD0.461065. All13 individual differences exceeding one cent involve non-USD customer presentment currencies. Currency conversion is a plausible explanation, but original event parameters and settlement exchange rates were not verified. Do not fabricate a conversion rule or force source values to agree.

The three missing recent orders are two US orders and one Danish order. In Shopify their recorded last visits are DuckDuckGo SEO, Google SEO and direct. This proves missing order coverage in the GA4 report; it does not prove consent behavior, a specific pixel defect, or the channel that caused each sale. GA4 separately flags missing session data and a session_start/ad_user_data sequencing diagnostic. That is a platform diagnostic requiring a read-only implementation trace before any tracking repair. `(not set)` campaign values can be normal for non-campaign traffic; they are not individually proof of failure.

## What remains useful from the old sold-product test

Existing Google Shopping candidate campaign: **23867953136**, eight products and19 exact historical variants. Current Admin readback finds all19 variants available for sale and all eight products ACTIVE. This does not verify Merchant eligibility, live landing quality, current campaign scope or spend authority.

| Old candidate | Orders90d /28d | Merchandise USD90d /28d | Current selling countries |
|---|---:|---:|---|
| Lavender floral-applique dresses | 0 /0 | 0 /0 | None observed |
| Green Tropical Leaf swim shorts | 1 /1 | 47.83 /47.83 | Denmark |
| Ivory Dot dresses | 0 /0 | 0 /0 | None observed |
| Pink Lace Garden dresses | 0 /0 | 0 /0 | None observed |
| Polka Dot dresses | 1 /0 | 68.00 /0 | Czechia |
| Blue Tie-Dye Butterfly dresses | 0 /0 | 0 /0 | None observed |
| Powder Blue set | 0 /0 | 0 /0 | None observed |
| Ivory Cascade set | 0 /0 | 0 /0 | None observed |

Product membership is not exact variant membership. **Only one of the19 original variants sold in this90d window: one Green Tropical Leaf unit for USD25.39 in Denmark. There were zero observed US sales of the19 exact variants.** The second swim-short unit and both Polka Dot units used other variants. Relaunching the old US selection unchanged would therefore rely on old selection evidence. This is a reason to refresh the scope, not proof that the products cannot sell or that an unobserved campaign failed.

## Updated candidate review order

These are candidates for cost and buyer-path validation, not launch recommendations or proven winners.

| Priority | Product / market | Current evidence | What prevents a profitability claim |
|---|---|---|---|
| 1 | Vintage Cottage pajamas / US | One recent order,3 units,USD101.97; GA4 records chatgpt.com / ai-assistant | One-order sample; modeled costs; intent, landing and CPC feasibility unverified |
| 2 | Sunshine Stripe tops / US | One recent order,5 units,USD118.95; GA4 records direct | One-order sample and the same cost/launch gaps |
| 3 | Sky Blue pleated family set / US | Two90d orders,USD71.97; recent orderUSD48.98 is missing from GA4 | Purchase coverage and actual costs need resolving |
| 4 | Skyfade / Italy | Part of the sole GA4 Google CPC purchase, linked to existing Italian Search23866684201 | Shopify records organic visits; mixed basket has unresolved product identity; current ad spend unavailable |
| 5 | Green Tropical Leaf shorts / Denmark | Only original retest product with a recent sale,USD47.83 | Small sample; different market and partial variant overlap; actual costs/seasonal offer fit unknown |

Skyfade sold in three orders across the US, Italy and Romania for USD239.31 during90d, with no sale in the recent28d. The GA4 google/cpc cohort contains one matched purchase: USD151.463786 reported revenue and session campaign23866684201, versus Shopify merchandiseUSD151.25. Its product join includes Skyfade and lines without current product IDs. Shopify records Google/SEO first and last visits with no UTMs for this cohort. Preserve this attribution conflict: the purchase is real, while paid acquisition is not independently reconciled. CPA and ROAS require current Ads spend and attribution evidence; product components must not be treated as the whole acquired basket.

The recent US pajama order recorded as ChatGPT traffic is useful evidence to preserve the store's discoverability. It is not proof that this AI session generated the sale. Google free-listing labels also occur on four90d GA4 transactions, USD401.86; those labels do not establish paid campaign revenue.

Five retained orders include lines without a current product ID, totaling USD410.47 merchandise in90d; two recent orders contain USD240.13 of those lines. The earlier Shopify product report counted seven orders in the blank-ID group because its count included the two cancelled orders. Current product identity must be resolved through a supported historical join before those lines become ad targets; titles alone are not enough to invent a product/variant mapping.

## Margin findings and the cost worksheet

**All135 current variants inspected have unitCost equal to selling price ×0.50, rounded half-up.** An independent history reader also found142/142 older variant costs across the eight candidates and Skyfade using the same formula. `ops/scripts/sync_shopify_variant_costs.py:118` calculates that value; the worklog records a backfill and hourly overwriting convention at `ops/AGENT_WORKLOG.md:23675`. Whether the old hourly job is currently running was not checked. These fields are planning inputs, not supplier invoices or verified profit.

The earlier economics packet explicitly left83 shipping-cost worklist rows blank. No complete actual product/China-service/freight/duties/credit basis was found for this cohort. The owner has been asked where those charges are recorded. The linked [cost requirements](candidate_actual_cost_requirements.csv) list five candidate product-market pairs. A separate private worklist selects six relevant orders for invoice/settlement matching; actual-cost cells remain blank rather than being filled with estimates. Actual cost records must remain separate from any automatically overwritten Shopify cost field.

Order transaction fees were returned in seven currencies: USD76.90, EUR35.04, DKK159.82, GBP2.27, RON40.35, CZK201.78 and CAD6.17 for successful sale/capture transactions on the45 retained orders. **These amounts cannot be added into a USD expense total.** The additional read-only settled-balance query was denied because the connector lacks `read_shopify_payments` / `read_shopify_payments_accounts`; no permission or billing change was attempted. Current settled fee allocation remains incomplete.

Refund transactions for the two cancelled orders report successful refunds totaling USD137.15 in Shopify's shop-money representation, versus USD136.71 of reversed original merchandise. One non-USD-presentment order accounts for the USD0.44 difference; settlement/FX causation remains unverified. Refund dollars and actual unrecovered fulfillment expense are different inputs. Do not subtract a refund again after starting from retained net revenue.

The recent USD25.98 shipping revenue is now explained: **two Priority Shipping charges of USD12.99 and six Free Standard Shipping orders**. Optional upgrades are consistent with included standard shipping. These are customer charges, not actual freight costs; no unsupported standard-shipping defect was inferred.

Under the owner's stated model, advertising plus unrecovered return loss must fit within20% of merchandise revenue to retain30% after50% other costs. For the observed USD101.97 pajama basket, that is USD20.39 before return loss; a hypothetical5% loss reserve would leave USD15.30 for ads. These are illustrative ceilings, not validated CPA targets. The existing6.5x ROAS discipline can be stricter than the no-loss calculation, and larger ad budgets remain conditional on verified contribution. Do not add payment fees again on top of an assumed50% cost bucket that already includes them.

## Decision and continuation

**Refresh the product selection; do not treat the old US test as launch-ready.** Start actual-cost validation with the recent US pajama basket, with Sunshine Stripe as a second current candidate. Preserve Italy's existing Search campaign for investigation once access returns; do not convert its single, conflicting attribution into a scale decision.

One owner action: identify the account/system or file containing actual fulfillment charges and supplier credits. It goes first because the sales-to-product match is now available, while actual costs determine whether any paid test can satisfy30% profit. The previously approved Google support submission remains NOT SUBMITTED under its existing form-validation gate; that separate approval is unchanged.

Internal queue: TA-03 actual landed-cost and settled-fee allocation; TA-02 missing-purchase/attribution diagnosis using the private matched and missing cohorts; TA-08 refresh the exact candidate scope and buyer-path/CPC evidence. No live tracking fix or launch is authorized by this report. Current full-account control remains `STALE_READBACK_REQUIRED`, `approved_external_scope=NONE`, `next_best_action=READ_ONLY_MARKETING_RECONCILIATION`.

Durable evidence: `sales_candidate_reconciliation_summary.json`, `current_sold_campaign_candidates.csv`, `current_product_sales_and_modeled_costs.csv`, `candidate_actual_cost_requirements.csv`, the GA4 report/summary and `reconciliation_readonly_queries.graphql`. `reconcile_sales_candidates.py` reproduces aggregate outputs with Decimal from the private input; it rejects ambiguous joins, incomplete pagination, unsupported refund states and changed line quantities. Normal GA4 CSVs and minimal Shopify records are outside the repo in a private mode700 directory with mode600 files. They are temporary inputs, not an indefinitely durable archive; if missing, repeat the saved fixed-window read-only queries and exports. No names, contact data, order IDs or customer identifiers appear in these aggregate outputs.

The initial unquoted ISO filter admitted one partial September5 order. The corrected quoted timestamp filter was re-read, returned47 records with no further pages and zero out-of-window rows, and is the only order set used here. All line/shipping/refund connections were checked for complete pagination. Shopify aggregate totals, original and retained amounts and all retained line totals reconcile. The separate Shopify documentation search script failed to fetch; the official connector schema/docs supplied the definitions, and both connector and local script validation passed. Schema definitions, scope failures and modeled-cost limitations are not silently replaced by guesses.

Continue via `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, the current digest and the latest relevant worklog anchor. Independent numerical/privacy review and canonical continuity checks are recorded in the final reconciliation check receipt.
