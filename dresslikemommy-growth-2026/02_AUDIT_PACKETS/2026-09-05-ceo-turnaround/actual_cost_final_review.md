# Final actual-cost review

Confidence: H for local numerical consistency. **PASS; no material arithmetic defect found.** Reviewed 2026-09-06. Remaining execution blockers are unresolved Italian fulfillment, conditional provider funding allocation, remaining expenses, buyer-path evidence and exact authority. I did not inspect the Shopify/provider UI, reproduce private joins, verify bank settlement or execute an external action.

The [six payout allocations](shopify_payout_fee_readback.json) reconcile exactly with Decimal:

| Alias | Converted gross USD | Processing + currency fees USD | Net allocation USD |
| --- | ---: | ---: | ---: |
| COST_01 | 164.86 | 9.16 | 155.70 |
| COST_02 | 99.96 | 3.20 | 96.76 |
| COST_03 | 47.83 | 2.39 | 45.44 |
| COST_04 | 131.94 | 4.13 | 127.81 |
| COST_05 | 101.97 | 3.26 | 98.71 |
| COST_06 | 48.98 | 1.72 | 47.26 |

Totals: **$595.54 − $23.86 = $571.68**. Allocated payout net is not proof of bank receipt, no later reversal, delivery or closed refund exposure. Italy’s API gross $164.87 and payout gross $164.86 remain distinct; the one-cent cause is not established.

All [fee-inclusive calculations](actual_cost_after_payment_fees.json) reproduce from unrounded provider costs at both funding endpoints, adding each recorded payment fee once. Merchandise revenue excludes optional shipping while full costs/fees remain included: a conservative screening choice, not an actual-margin assertion. Do not start from payout net and subtract these same fees again.

Remaining room after ads at exactly 6.5× ROAS, reserving 30% merchandise profit and setting other unknown expenses to zero:

| Basket | Low-rate / high-rate room USD |
| --- | ---: |
| Mixed US | 4.47 / 3.95 |
| Danish shorts | −8.40 / −8.75 |
| Sunshine | 21.12 / 20.68 |
| Vintage | −8.62 / −9.29 |
| Small Sky Blue | −2.00 / −2.30 |

Danish pre-ad room is already −$1.04/−$1.40. Lower CPA alone cannot restore the 30% target for this basket under these assumptions; this does not establish an actual loss. The conditional ceiling remains `min(R/6.5, 0.70R − Ck − F − E)`, with funding-lot basis and disjoint remaining expenses unresolved. Handling already included in `k` must not be added again.

Italy correctly retains null revenue-derived fields. Shopify records Paid/Partially fulfilled: two Ivory Meadow items €28.95+€31.95=€60.90 unfulfilled; provider canceled retail is $69.38. These currencies/statuses are not interchangeable refund or delivery evidence. Three fulfilled Skyfade items do not resolve the other two. Confirming external replacement/refund/customer agreement is a supported first owner priority; no customer contact or money-moving action is authorized here.

The [reconciliation’s](ACTUAL_COST_RECONCILIATION.md) Sunshine-first order is justified for expense and buyer-path validation, not as a winner: one five-unit basket cannot set expected AOV, unit freight or CPA. Vintage’s existing basket/proposed 6.5× stage remains held; lower-CPA and organic strategies are not categorically excluded. Mixed-basket costs cannot be assigned to one product. No profitable-sales lift or spend authority follows.

SHA256 bindings:

- Payout receipt: `1b1d642854e936ceb93fc14c01792b39156c6924aa39fd510147b8210e2e1b9d`
- Fee-inclusive screen: `b21386c5e256e02dfb85102dbd506d8d65bee3a7c46a6e4e8a930cb1baab970d`
- Reconciliation: `ca729998b2626e79f9cc1f75fba1c1adddd4c26e24c0e0211b680306b1c2e455`
- Provider components: `85ad31625c078488b64e114febeece4a2fde8b506ee171d09cb041ef49c301a3`
- Funding screen: `0a43d2c5d205e1503f903d2574e3b910426291ccda1661a73adfd15806eebf88`
