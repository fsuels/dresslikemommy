# Pinterest Spend-Safety Pause Execution - 2026-05-29

## Scope

- Approved live action: pause only Pinterest campaign `626758581530` / `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- Advertiser: `549756244483`.
- Approval basis: May 28 zero-return readback showing active delivery, `$87.69` spend through `2026-05-27`, `805` outbound clicks, `0` Checkout conversions, `$0` Checkout value, and `0` Shopify Pinterest-attributed orders.
- Explicit exclusions honored: no budget, bid, product group, source/feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or other campaign change.

## Before-State Readback

- Time: `2026-05-29 11:44 EDT`.
- Pinterest reporting filter: campaign ID `626758581530`, objective `Catalog sales`, date range `2026-05-18` through `2026-05-29`, time zone `UTC`.
- UI row readback: campaign status `Active`; campaign switch checked/on.
- Campaign name readback: `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520`.
- UI spend readback for the filtered row: `$105.00`.
- UI campaign objective/ID readback: `Catalog sales, ID: 626758581530`.
- Screenshot: `pinterest-before-pause-626758581530.png`.
- API campaign metadata before the pause read back `status=ACTIVE`, `summary_status=RUNNING`, `objective_type=CATALOG_SALES`, and `daily_spend_cap=10000000` micro-USD.

## Action Taken

- Toggled only the campaign-level active switch for campaign `626758581530`.
- Pinterest displayed an early-pause warning. The current owner prompt explicitly approved the pause, so `Pause anyway` was clicked.

## After-State Readback

- Time: `2026-05-29 11:45 EDT`.
- UI row readback: campaign status `Paused`; campaign switch unchecked/off.
- UI campaign name/ID still read back as `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520` / `626758581530`.
- UI spend readback for the filtered row remained `$105.00`.
- Screenshot: `pinterest-after-pause-626758581530.png`.
- Independent authenticated Pinterest API readback:
  - `status=PAUSED`
  - `summary_status=PAUSED`
  - `objective_type=CATALOG_SALES`
  - `daily_spend_cap=10000000` micro-USD (`$10.00`)
  - Spend metric for `2026-05-18` through `2026-05-29`: `105.002796`
  - Total impressions: `75011`
  - Total pin/clickthrough metric: `1002`

## Result

The approved spend-safety pause is complete. Campaign `626758581530` is paused and should no longer continue delivery from the previously active parent campaign lane.

Next valid sales-moving work is read-only diagnosis before any relaunch: Pinterest Events Manager Checkout/tag readback, then 5-10 ad/PDP deep-link checks, then Shopify/Pinterest UTM attribution propagation.
