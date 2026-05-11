# Non-US Purchase Measurement Read-only Continuation

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-11-paid-growth-native-rewrite-local-measurement-continuation`
Status: `READONLY_PATH_IDENTIFIED_PURCHASE_EVENT_PROOF_STILL_REQUIRED`

## Current Evidence

- Shopify has `7` sanitized non-USD order candidates since `2026-04-01` across `DKK`, `GBP`, and `CHF`.
- GA4 UI access was previously proven for account `88409806`, property `330266838`, visible property `dresslikemommy.com - GA4`.
- Google Ads conversion configuration still points to one primary purchase action with dynamic value, but this is not order-level non-US proof.
- GA4 CLI/API matching remains blocked by insufficient OAuth scopes.
- This packet added a read-only GA4 standard Events pagination probe. The second page of the GA4 Events report for `Apr 13 - May 10, 2026` showed `purchase` as row `12`, with `17` events, `16` users, and `$1,103.34` total revenue. The report still did not expose transaction ID, event currency, or order-level value, so the non-US currency/value gate remains open.

## Best Remaining Read-only Path

Use logged-in GA4 UI, not a live checkout, to attempt:

1. Date range `2026-04-01` through `2026-05-10`.
2. Filter `eventName = purchase`.
3. Pull visible/exportable dimensions: transaction ID, currency code, country, date, hour/minute if available.
4. Pull metrics: purchases, purchase revenue/total revenue, event value if available.
5. Match against sanitized Shopify candidates by timestamp window, country, currency, and value.

Strongest candidate windows:

- `2026-05-07 13:22 UTC`, `DK`, `201 DKK`
- `2026-05-04 07:29 UTC`, `DK`, `434 DKK`
- `2026-04-18 13:19 UTC`, `GB`, `24 GBP`
- `2026-04-15 19:20 UTC`, `CH`, `34 CHF`

## If Read-only UI Cannot Expose The Fields

Exact unblock options:

- Provide/refresh a read-only Google Analytics OAuth token with Analytics Data/Admin API scopes for property `330266838`; or
- Approve the controlled non-US test-purchase/refund/cancel procedure already documented in the prior packet.

No campaign can be enabled from this packet. This lane is not closed until non-US `purchase` currency/value/transaction evidence is saved.

## Additional Evidence In This Packet

- `ga4_ui_readonly_probe/ga4_events_purchase_pagination_probe_summary.json`
- `ga4_ui_readonly_probe/ga4_events_purchase_pagination_probe.png`
- `ga4_ui_readonly_probe/ga4_purchase_detail_readonly_probe_summary.json`
- `ga4_ui_readonly_probe/ga4_purchase_detail_readonly_probe.png`
