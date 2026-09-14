Confidence: H for local reconciliation. **PASS: 31/31 checks.**

The same two baskets contain two units each. Belgium: **USD25.49 + 28.98 = 54.47**, with presentment **EUR21.95 + 24.95 = 46.90**. Current default prices total USD51.98; they are different fields, and the difference has no established cause. US shop/presentment revenue is **USD14.99 + 16.99 = 31.98**. Combined recorded shop revenue remains USD86.45.

All four saved unit costs equal current default price ×0.50, rounded half-up: **USD12 + 14** and **USD7.50 + 8.50**. This matches the existing formula and 135-variant audit; it does not establish supplier or delivered costs. See `CURRENT_SALES_CANDIDATE_RECONCILIATION.md:66` and `ops/scripts/sync_shopify_variant_costs.py:118`.

Recorded fees reconcile separately: Belgium EUR2.78; US capture USD1.42. The authorization is excluded. Actual settled USD fees for Belgium remain permission-blocked; currencies must not be added or converted into a purported settlement figure. No margin or traffic-attribution conclusion follows.

Read-only provider follow-up, each quantity **1**:

| Row | Product ID | Variant ID | Exact size/color |
|---|---|---|---|
| RECENT_01 / BE | 7229023846497 | 41878198943841 | Girl 4-5 Years / Multi Color |
| RECENT_01 / BE | 7229023846497 | 41878199107681 | Mother M / Multi Color |
| RECENT_02 / US | 7109117280353 | 41497061949537 | Child 4-5 years / Multi-Color |
| RECENT_02 / US | 7109117280353 | 41497061851233 | Mother L / Multi-Color |

Match provider status and item charges; distinguish quoted, charged and settled product/service/freight/duty costs and recoveries, with original currencies and shared charges counted once. No purchase, fulfillment, payment or refund action.

Exact source bindings—including the supplemental presentment query—and checks are in `recent_order_basket_review.json`. Only local reads and these two review files were written.
