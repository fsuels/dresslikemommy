# Paid Spend Product Economics

Date: 2026-04-28
Mode: operating rule for growth, product eligibility, and paid-spend decisions.

## Operator Rule

- All-in non-marketing cost is basically 50% of selling price.
- That 50% includes product cost, shipping, and fees.
- The remaining deductions after that are marketing cost, returns, and chargebacks.
- Any product or collection with low AOV or unknown cost should be excluded from paid spend until the economics are known or improved.

## Current Benchmark

| Metric | Value | Formula |
| --- | ---: | --- |
| AOV | $63.25 | Operator-provided current AOV |
| All-in non-marketing cost | $31.63 | $63.25 x 50% |
| Max CAC | $9.49 | $63.25 x 15% |
| Required ROAS | 6.67 | $63.25 / $9.49 |
| Contribution after max CAC, before returns/chargebacks | $22.14 | $63.25 x 35% |

## Paid Eligibility Gate

- Include only products/collections with known selling price, known or operator-approved cost basis, and enough AOV to support the CAC target.
- Exclude unknown-cost items from paid campaigns and feed scale labels.
- Exclude low-AOV products unless they can be bundled, cross-sold, or repriced so the product can still support a realistic CAC.
- Use 6.67 ROAS as the minimum paid-spend guardrail at the current margin/CAC assumption.

## Notes

- This is a planning rule, not a Shopify writeback.
- Recompute max CAC whenever AOV changes: `max_cac = AOV * 0.15`.
- Recompute required ROAS if the marketing cap changes: `required_roas = 1 / marketing_spend_pct`.
