# Actual fulfillment cost: independent core review

Confidence: H for local arithmetic; actual net margin remains UNKNOWN. **PASS for the corrected provider-component receipt, not profit or launch readiness.** Reviewed 2026-09-06 against [cost readback](actual_fulfillment_cost_readback.json) and [prior sales reconciliation](CURRENT_SALES_CANDIDATE_RECONCILIATION.md). I did not inspect the financial/provider UI or independently reproduce the private order joins.

All six Decimal totals reconcile:

| Alias | Base CNY | Adjustments CNY | Final CNY |
| --- | ---: | ---: | ---: |
| COST_01 | 435.45 | −157.48 | 277.97 |
| COST_02 | 295.29 | −6.45 | 288.84 |
| COST_03 | 260.48 | −62.71 | 197.77 |
| COST_04 | 244.22 | +0.22 | 244.44 |
| COST_05 | 374.47 | +1.27 | 375.74 |
| COST_06 | 166.00 | +0.37 | 166.37 |

Combined provider total: CNY1,551.13. COST_06 service details sum to CNY14.70. The corrected Danish note distinguishes net international shipping CNY101.07 from CNY108.07 including domestic shipping. These are historical charges, not repeat-order quotes.

Italy remains materially conflicted: canceled retail lines $32.98+$36.40=$69.38; provider-retained retail $81.87 plus cancellations equals Shopify retained merchandise $151.25. The provider’s −CNY157.48 adjustment is neither a USD refund nor proof of corrected Shopify revenue. Preserve both records; do not independently subtract cancellations or allocate mixed-basket costs to Skyfade alone. “Completed” proves neither delivery nor closed returns.

The six selected orders contain $568.94 merchandise/$595.55 shop totals, not the eight-order recent population. The prior 90-day comparison remains 45 retained Shopify orders versus 34 retained GA4 matches; all 36 GA4 purchases include two refunded orders. Starting with retained revenue prevents subtracting those refunds again. Customer shipping revenue is separate from provider freight expense; credited provider costs must not be credited twice.

At the component receipt’s capture, per-order USD settlement/rate allocation, settled fees, borne duties/VAT, unrecovered returns and other expenses were null. Later payout evidence is outside this review. Existing 50%-cost illustrations reconcile algebraically, but are estimates. With consistently defined retained USD revenue `R`, settled provider USD cost `S`, and additional non-ad USD costs `F`, the conditional ceiling is:

`CPA ≤ min(R / 6.5, 0.70R − S − F)`

Require a positive feasible ceiling; include each fee/loss once. No numerical actual-profit target exists yet.

`CNY cost / USD revenue` has currency units, not a margin percentage. Multiplying by an applicable USD/CNY rate only creates a conditional screen unless settlement is allocated. Under a common hypothetical rate and comparable cost coverage, Sunshine’s 2.055 versus Vintage’s 3.685 CNY/USD supports prioritizing Sunshine settlement validation—not declaring a winner. Preserve Vintage/Sky Blue validation; exclude Italy from clean margin ranking pending reconciliation. Single baskets and mixed products cannot establish repeatable unit economics. Campaign authority and buyer-path gates remain unchanged.

SHA256 bindings:

- Cost receipt: `85ad31625c078488b64e114febeece4a2fde8b506ee171d09cb041ef49c301a3`
- Prior reconciliation: `82f96609d1b2fafc4501100269858f1e55ee288fc15f6d103ab8329010b8e90b`

Funding extension, 2026-09-06: **PASS for the corrected conditional [funding screen](actual_fulfillment_funding_screen.json) and [CSV](actual_fulfillment_candidate_screen.csv).** All eight successful applied/received ratios reproduce USD/CNY0.16247–0.164265. Latest Amount Paid $328.53 already includes $10.16 handling. Maximum displayed-rate residual CNY0.058341 ≈USD0.009232 is compatible with separately rounded amount/fee fields, not proof of bank settlement. Seven older detail receipts were not opened by the operator.

With other missing expenses set to zero, remaining room after advertising at `R/6.5` is negative at **both** endpoints: Denmark −$6.01/−$6.36; Vintage −$5.36/−$6.03; Sky Blue −$0.28/−$0.58. All six provider-cost ranges and five usable revenue screens reconcile. Italy’s four revenue-dependent fields are now null/empty in JSON/CSV; its provider-only conversion remains conditional.

Sunshine merits settlement/buyer-path validation first. The corrected Vintage COST_HOLD covers this basket/proposed 6.5× stage, not every lower-CPA test or organic use. No funding-lot allocation, actual order settlement, actual margin or future-rate guarantee follows. Original authority gates remain intact.

- Funding SHA256: `0a43d2c5d205e1503f903d2574e3b910426291ccda1661a73adfd15806eebf88`
- CSV SHA256: `7d4fa630fcc37d9af6d15c41f487fda1d59fdba282c7914be2f4f9cbb59421fe`
