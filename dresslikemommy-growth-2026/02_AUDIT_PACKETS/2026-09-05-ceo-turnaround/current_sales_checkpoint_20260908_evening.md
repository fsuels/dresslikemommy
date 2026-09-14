Latest dated checkpoint (September10): September10 07:44:04–07:44:43UTC: the same2 PAID, non-test, noncancelled web orders remain, with4units/USD86.45. Zero new orders since03:39:40UTC, during the trailing24hours or after the approximate GA4 cutover; zero refund/cancellation/carrier-event delta. Rainbow has one successful2-unit recorded fulfillment; Mermaid has none.32source checks and18independent root receipt checks pass. The ninth heartbeat entry preserves all eight prior entries. Delivery, actual costs, acquisition attribution, CPA, ROAS and retained profit remain UNKNOWN.

See heartbeat_readbacks[8] in the existing JSON. Earlier September8 report is retained below as history.

Confidence: H.

**LIVE VERIFIED: no changed business evidence; no action newly qualified.** One existing structured Shopify order query refreshed the September5 00:00 through September8 15:10:23 America/New_York window (cutoff **2026-09-08 19:10:23 UTC**). Name, domain, USD shop currency and time zone matched. Order and line-item pagination completed.

The same **2 PAID, non-test, uncancelled web orders / 4 current units / USD86.45 current merchandise subtotal** remain. Total also equals USD86.45; original/current merchandise amounts and units agree. Both orders remain **UNFULFILLED**; current tax and recorded refunds remain **USD0.00**.

Since the prior September8 02:50:16 UTC cutoff—16 hours, 20 minutes, 7 seconds—there are **0 new order creations, 0 qualifying orders and USD0.00 additional current merchandise subtotal**. The trailing 24-hour window also contains zero qualifying orders. No new sales learning is established by this checkpoint.

| Country | Product ID | Current units | Current merchandise USD | Fulfillment |
|---|---|---:|---:|---|
| Belgium | Rainbow 7229023846497 | 2 | 54.47 | 1 UNFULFILLED order |
| United States | Mermaid 7109117280353 | 2 | 31.98 | 1 UNFULFILLED order |

Both saved baskets uniquely match their exact public product/variant IDs and original quantities in transient memory; all four variant selections and current quantities remain unchanged. Prior order IDs were not saved, so this is a unique basket-signature comparison, not a persisted order-ID join. Presentment is kept separate: EUR46.90 and USD31.98.

All 11 source/comparison checks pass. Monetary totals were summed in integer cents. No raw response, order/customer/transaction identifiers, exact order timestamps, personal address or contact details were saved. This report and [sanitized JSON](current_sales_checkpoint_20260908_evening.json) preserve country aggregates, public product IDs, totals/statuses and variant-match counts only. The [query](current_sales_checkpoint_20260908_evening.graphql) is byte-identical to the prior query; only its upper-bound variable advanced.

The historical Aug8–Sep4 **8-order/USD734.99 merchandise** baseline remains unrefreshed and separate from this **2-order/USD86.45** cohort. PAID denotes Shopify financial status. Paid-media attribution, acquisition cost, CPA, ROAS, actual provider expenses, delivery and retained profit are unresolved. Zero recorded refunds is only a read-time observation.

**Next:** hold this lane with evidence; the existing fulfillment and actual provider-cost reconciliation remains the prerequisite for using these baskets to qualify paid expansion. No new action was qualified. Root-reported Google/CUA policy and app-scope gates remain unchanged and were not retried.

Source: [previous checkpoint](current_sales_checkpoint_20260908.json), current validated read-only Shopify connector response. One order query, zero external writes, browser/public requests or event sends. Query validation artifact: `current-sales-checkpoint-20260908-evening-v1`, revision1, VALID.

Continue with root's existing Google connection plan and independent review of this checkpoint; do not restart the audit or infer new spend authority.
