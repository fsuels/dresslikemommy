# Standard Shopping Cost-Control Review

Verified: 2026-05-06, America/New_York

## Approval

Owner approval phrase:

`APPROVE STANDARD SHOPPING COST CONTROL REVIEW: READ BACK SEARCH TERMS, PRODUCTS, CPC, AND SPEND FIRST; LOWER MAX CPC CAP TO $0.20 OR LESS ONLY IF READBACK CONFIRMS NO PURCHASE VALUE; KEEP BUDGET, PRODUCT SCOPE, FEED LABELS, PRODUCT GROUPS, CONVERSION GOALS, AND CAMPAIGN STATUS UNCHANGED.`

## Campaign

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Date range readback: Apr 29-May 5, 2026
- Campaign status before edit: Enabled / Eligible
- Budget before edit: `$20.00/day`
- Campaign type: Shopping
- Bid strategy type: Manual CPC

## Required Readback Before Any Edit

Campaign-level readback:

- Clicks: `81`
- Impressions: `3,906`
- CTR: `2.07%`
- Avg CPC: `$0.23`
- Cost: `$18.58`
- Conversions: `0.00`
- Conversion value: `0.00`
- Conversion value / cost: `0.00`

Search-term readback:

| Search term | Match type | Clicks | Impr. | Avg CPC | Cost | Conversions |
|---|---|---:|---:|---:|---:|---:|
| mommy and me dresses | Exact match | 13 | 481 | `$0.23` | `$2.99` | `0.00` |
| matching sibling outfits | Exact match | 3 | 12 | `$0.23` | `$0.70` | `0.00` |
| mommy and me outfits | Exact match | 3 | 101 | `$0.25` | `$0.75` | `0.00` |
| family matching outfits | Exact match | 2 | 38 | `$0.24` | `$0.48` | `0.00` |
| matching mom and me dresses | Exact match | 2 | 5 | `$0.25` | `$0.50` | `0.00` |
| matching mother baby outfits | Exact match | 2 | 1 | `$0.22` | `$0.44` | `0.00` |
| mom and daughter matching dresses | Exact match | 2 | 36 | `$0.23` | `$0.45` | `0.00` |
| mommy and baby matching dress | Exact match | 2 | 4 | `$0.23` | `$0.46` | `0.00` |
| mother and daughter dresses | Exact match | 2 | 12 | `$0.24` | `$0.48` | `0.00` |
| mother daughter pajamas | Exact match | 2 | 1 | `$0.25` | `$0.50` | `0.00` |

Search-term totals:

- Visible search terms: `58` clicks, `2,457` impressions, `$0.23` avg CPC, `$13.60` cost, `0.00` conversions.
- Other search terms: `23` clicks, `1,449` impressions, `$0.22` avg CPC, `$4.98` cost, `0.00` conversions.
- Campaign total: `81` clicks, `3,906` impressions, `$0.23` avg CPC, `$18.58` cost, `0.00` conversions.

Product readback:

- Top visible products all read `0.00` conversions and `0.00` conversion value.
- Product issue pattern: visible top products were `Eligible (limited)` with `Missing age group`.
- Product count readback: `1 - 10 of 771`.

Product-group readback before edit:

| Product group | Max CPC before | Clicks | Cost | Avg CPC | Conversions |
|---|---:|---:|---:|---:|---:|
| `daddy_me` | `$0.05` | 3 | `$0.68` | `$0.23` | `0.00` |
| `family_matching` | `$0.05` | 3 | `$0.70` | `$0.23` | `0.00` |
| `mommy_me` | `$0.05` | 34 | `$7.63` | `$0.22` | `0.00` |
| `pajamas` | `$0.05` | 6 | `$1.42` | `$0.24` | `0.00` |
| `swimsuits` | `$0.05` | 35 | `$8.15` | `$0.23` | `0.00` |
| `Everything else in "us_test_ready"` | `$0.05` | 0 | `$0.00` | `—` | `0.00` |
| `Everything else in "All products"` | Excluded | 0 | `$0.00` | `—` | `0.00` |

Gate decision: the approved condition was met. The campaign had cost and CPC above the target posture, with `0.00` primary purchase conversions and `0.00` conversion value.

## Live Change Made

Changed only product-group Max CPC bids from `$0.05` to `$0.04`:

- `All products > us_test_ready > daddy_me`
- `All products > us_test_ready > family_matching`
- `All products > us_test_ready > mommy_me`
- `All products > us_test_ready > pajamas`
- `All products > us_test_ready > swimsuits`
- `All products > us_test_ready > Everything else in "us_test_ready"`

Rationale:

- The visible product-group max CPC was `$0.05`, but realized average CPC was about `$0.22-$0.24`, likely because existing bid adjustments are multiplying the base Shopping bids.
- Lowering `$0.05` to `$0.04` is the smallest clean reduction that targets an effective ceiling near `$0.20` while preserving product scope.

## Final Readback

Final product-group readback after save and page reload:

| Product group | Final Max CPC | Product scope status |
|---|---:|---|
| `daddy_me` | `$0.04` | Still included |
| `family_matching` | `$0.04` | Still included |
| `mommy_me` | `$0.04` | Still included |
| `pajamas` | `$0.04` | Still included |
| `swimsuits` | `$0.04` | Still included |
| `Everything else in "us_test_ready"` | `$0.04` | Still included, 0 clicks |
| `Everything else in "All products"` | Excluded | Still excluded |

Final campaign row readback:

- Campaign status: Enabled / Eligible
- Budget: `$20.00/day`
- Campaign type: Shopping
- Campaign ID: `23802638621`
- Date-range historical metrics still show `$0.23` avg CPC because the change is not retroactive.

## Unchanged Surfaces

No changes were made to:

- Campaign budget
- Campaign status
- Campaign product structure / product-group subdivisions
- Feed labels
- Product scope / inventory filter
- Merchant Center
- Shopify
- Conversion goals
- Conversion actions
- Brand Search
- PMax
- Remarketing
- Pinterest

## Next Monitoring Rule

Monitor the next 24-72 hours of new clicks only. Historical Apr 29-May 5 CPC will not change retroactively. If new clicks still average above `$0.20` with no purchase value, the next smallest move would be a separate approval to lower the active child product-group bids again from `$0.04` to `$0.03` or pause the test.

## Decision

`STANDARD_SHOPPING_COST_CONTROL_COMPLETED__BASE_PRODUCT_GROUP_BIDS_LOWERED_FROM_0_05_TO_0_04__BUDGET_STATUS_SCOPE_GOALS_UNCHANGED`
