# Pinterest Parent Campaign Audit Verification - 2026-05-28

Scope: read-only verification of the pasted audit for Pinterest campaign `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520` / campaign ID `626758581530`, using the existing Chrome `test` profile and open authenticated Pinterest, Shopify Admin, and GA4 surfaces.

No external write occurred. No Pinterest campaign, ad group, budget, bid, product group, source, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM setting was changed.

## Verdict

The audit's core bottom line is verified: the campaign is not bringing measurable sales and is at `0` Pinterest Checkout ROAS, not the `650%` target.

The pasted ad group numbers for `2026-05-12` through `2026-05-25` are verified at the active ad group level:

| Entity | Spend | Impressions | Pin clicks | Outbound clicks | Checkout conversions | Checkout value | Checkout ROAS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049` | `$59.32` | `46,191` | `564` | `549` | `0` | `$0.00` | `0` |

Derived checks:

- Pin-click CTR: about `1.22%` (`564 / 46,191`).
- Outbound CTR: about `1.19%` (`549 / 46,191`).
- Outbound-to-pin-click rate: about `97.3%`.
- Cost per outbound click: about `$0.108`.

## Important Corrections

- The `$59.32` spend figure is the active ad group row, not the full campaign row for the same visible date range. Campaign reporting for `2026-05-12` through `2026-05-25` showed campaign-level spend around `$67.40`, `50,369` impressions, `620` pin clicks, `605` outbound clicks, and still `0` Checkout conversions/value/ROAS. The campaign-vs-ad-group discrepancy needs Pinterest reporting reconciliation before finance summaries use the smaller number.
- Current live state is later than the pasted `2026-05-25` audit. In the rolling Pinterest view through `2026-05-27`, the same campaign showed `$87.69` spend, `65,934` impressions, `827` pin clicks, `805` outbound clicks, `0` Checkout conversions, and `0` Checkout ROAS.
- The live edit readback showed the current max CPC bid as `0.10`, not the older `$0.15` stored in older command-layer notes.
- The exact start date was not independently proven from a campaign settings start timestamp in this pass. Delivery clearly exists in the reporting window; treat the pasted "started 05/18" line as plausible but not verified from the captured readback.

## Current Campaign Settings Readback

- Campaign objective: `Catalog sales`.
- Campaign status: `Active`.
- Budget type: daily.
- Daily budget: `10.00`.
- Schedule: `Run continuously`.
- Optimization score surfaced a recommendation to raise daily budget to at least `$20.00`; this was not accepted.

## Current Ad Group Settings Readback

- Ad group: `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520`.
- Ad group ID: `2680090331049`.
- Status: `Active`.
- Format: Shopping ad.
- Destination: Website.
- CTA: `Shop now`.
- URL tracking: `None`.
- Optimization: `Pin clicks`.
- Bidding: `Custom`.
- Maximum CPC bid: `0.10`.
- Targeting: all U.S., all genders, all ages, all languages, all devices, browse and search placements.

Selected product groups are nonzero and point to the intended parent source:

| Product group | ID | In-stock count | Data source |
|---|---:|---:|---|
| `DLM_PIN_US_PARENT_MOMMY_AND_ME_99_20260520` | `4673019642885` | `99` | `DLM US Paid Parent Collection Intent 2026-05-20` |
| `DLM_PIN_US_PARENT_FAMILY_MATCHING_77_20260520` | `4673019642929` | `77` | `DLM US Paid Parent Collection Intent 2026-05-20` |
| `DLM_PIN_US_PARENT_DADDY_AND_ME_34_20260520` | `4673019642938` | `34` | `DLM US Paid Parent Collection Intent 2026-05-20` |

This supersedes the earlier zero-count product-group blocker for this active ad group.

## Shopify Order Truth

Read-only Shopify Admin API aggregate checks were run without printing credentials or customer PII.

For `2026-05-12T00:00:00Z` through `<2026-05-26T00:00:00Z`:

- Orders fetched: `18`.
- Non-cancelled, non-test orders: `14`.
- Aggregate revenue: `$771.56`.
- Orders with source/journey/UTM/campaign signals matching Pinterest, `pin.it`, campaign `626758581530`, ad group `2680090331049`, or `DLM_PIN_US_PARENT_COLLECTIONS`: `0`.

For `2026-05-12T00:00:00Z` through `<2026-05-29T00:00:00Z`:

- Orders fetched: `20`.
- Non-cancelled, non-test orders: `16`.
- Aggregate revenue: `$885.13`.
- Orders with the same Pinterest/campaign/ad-group signals: `0`.

Shopify truth therefore supports the "no Pinterest-attributed sales" conclusion. It does not by itself prove that the Pinterest Checkout event is broken; it can also mean the campaign produced no purchases.

## GA4 Context

GA4 `Key event attribution paths` for `2026-04-30` through `2026-05-27` showed revenue in the property overall, but `Organic Social` and `Paid Shopping` rows visible in that report showed `$0.00` purchase revenue. This corroborates weak social/paid-shopping revenue in the broad report, but it is not an exact campaign-level Pinterest proof.

## Recommended Action

Do not scale or follow Pinterest's budget-increase recommendation. The campaign has spent enough with `0` Checkout conversions and `0` Shopify Pinterest-attributed orders that the next sales-moving action is a spend-safety pause/hold decision before deeper optimization.

Suggested exact approval phrase if the owner wants Codex to make the live pause:

```text
APPROVE PINTEREST SPEND-SAFETY PAUSE ONLY: pause campaign 626758581530 / DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520 after the May 28 readback showing active delivery, $87.69 spend through May 27, 805 outbound clicks, 0 Checkout conversions, $0 Checkout value, and 0 Shopify Pinterest-attributed orders; do not change budget, bid, product groups, sources, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or any other campaign. Capture before/after status and cost readbacks.
```

After the spend-safety state is no longer leaking money, investigate tracking and landing fit in this order:

1. Pinterest Events Manager / tag and Checkout event readback.
2. PDP landing/deep-link spot checks for the three product groups.
3. Shopify order attribution and UTM propagation from Pinterest click-throughs.
4. Creative/product-fit review only after the attribution and landing checks do not explain the zero-order result.
