# Measurement and actual economics readiness

Prepared September 11, 2026. `DERIVED_REVIEW / PASS_WITH_LIMITS`; existing records only. This packet is evidence for the existing command layer, not another operating system. No native access, account change, customer-data extraction or payment occurred. Root owns account execution; this lane owns only this folder.

**Decision:** configuration and published bootstrap are verified by root; next use the standard pixel helpers at owner handback. Actual maximum CAC, market profit and purchase acceptance remain unknown. The smallest financial continuation is TA-16's existing fulfilled Rainbow basket cost join; do not repeat the completed six-basket cost discovery.

## Readiness matrix

| Gate | Existing evidence | Exact remaining evidence / decision |
|---|---|---|
| Orders and markets — PARTIAL | August10–September8: 10 report orders, USD821.44 net merchandise, USD847.42 total sales. Separate June13–September10 report: 43 orders, USD3,190.41 net merchandise, USD3,256.55 total sales; 42 new/1 returning customers reported. | Complete eligible order/line population, shipping country, currency and date/timezone. Aggregate customers are not attributed acquired customers. Session country is not shipping market. Do not combine the 30-day, 90-day and selected-basket cohorts. |
| Provider costs — PARTIAL | Six historically selected baskets have actual CNY1,551.13 in provider components. | Per-order actual USD settlement/funding allocation, fees and supported FX; duty/VAT borne, later credits and return losses. Provider Completed is not delivery or settled cost. |
| Payment fees — PARTIAL | The same six baskets have USD23.86 recorded fees and USD571.68 payout allocations. Two recent baskets separately show EUR2.78 and USD1.42 fees. | Bank/settlement reconciliation and complete fee/refund/dispute coverage. Do not add currencies, count authorization plus capture twice, or treat shipping charged as freight expense. |
| All-in profit / CAC — UNKNOWN | Source components exist; old 50%-of-price variant costs and conditional funding screens are models. | Complete retained revenue R, disjoint actual variable costs V, allocated overhead/other costs H, return maturity, attributed new-customer count and matched ad cost for each market. All actual profit/CAC outputs remain null. |
| New Ads configuration — VERIFIED BY ROOT | Customer6509972886; AW-18433316477; Purchase7760272273; only Checkout completed maps to label DTaoCJG3sfQcEP2s2NVE. Full reloads and Google detector pass. Primary/Every/dynamic USD1 fallback; EC Not configured. | Fresh event/payload/receiver checks. Never substitute the fallback USD1 for order value. |
| GA4 / legacy Ads — PARTIAL | GA4 G-N4EQNK0MMB has dated non-purchase transport evidence. Legacy connected pixel111214689 uses AW-853411529/kZ_RCN-T3K0cEMmN-JYD. | Preserve both. Fresh behavioral readback must distinguish base requests from purchase conversions. Different destinations do not prove global deduplication. |
| Passive page — CAPABILITY LIMIT | Root bound MAIN133290917985, canonical URL, AW/label and retained tags; cart0, English/US/USD. Complete root capture: 576 selected events, zero visible Google requests. | Sandbox child visibility is unverified. Unsupported Target.setAutoAttach was not retried. Missing cookie/banner does not establish a consent choice; zero root requests is not tracking failure. Own tab closed. |
| Consent / purchase — OPEN | No genuine purchase was exercised during the new Ads repair; earlier GA4 consent evidence was partly preview-specific. | Clean MAIN binding, complete capture, applicable consent signals, real transaction match, dynamic values/items and receiver receipt. No blanket privacy or ingestion claim follows from tag detection. |
| Authority — HOLD SPEND | Standing control remains NONE; the exact campaign24247604341 pause question is pending. | Broad “keep working/fix everything” supports diagnosis and preparation, not an invented budget, loss allowance or answer to the pending pause question. Preserve exact action-time gates. |

## Worked existing-data table

These six aliases are a selected historical sample, not complete market cohorts. Source readbacks are dated September6; amounts are not current market cost forecasts. Actual USD provider settlement, net profit and maximum CAC are **UNKNOWN for every row**.

| Alias / shipping market | Provider CNY | Recorded fees USD | Recorded payout net USD |
|---|---:|---:|---:|
| COST_01 / IT | 277.97 | 9.16 | 155.70 |
| COST_02 / US | 288.84 | 3.20 | 96.76 |
| COST_03 / DK | 197.77 | 2.39 | 45.44 |
| COST_04 / US | 244.44 | 4.13 | 127.81 |
| COST_05 / US | 375.74 | 3.26 | 98.71 |
| COST_06 / US | 166.37 | 1.72 | 47.26 |
| Selected-sample total | 1,551.13 | 23.86 | 571.68 |

Italy is additionally **CONFLICTED**: provider canceled retail lines total USD69.38, while the fixed-window Shopify merchandise total remains USD151.25. Neither canceled retail lines nor provider CNY adjustments establish a customer refund. API shop total164.87 versus payout converted gross164.86 also retains a one-cent source discrepancy. Resolve those transactions; do not silently net them. For BE and all other markets, the admitted evidence does not establish a complete actual-cost cohort. Sparse repeat-customer evidence cannot justify speculative LTV.

Use one revenue basis: `R` is merchandise after discounts/refunds plus retained shipping, excluding collected tax; `V` is disjoint actual variable costs net of evidenced recoveries; `H` is allocated overhead/other costs excluded from V. Define `CM=R−V` and permitted ads `A≤min(R/6.5, CM−H−0.30R, approved cash/loss allowance)`. Unknown/nonpositive results produce no qualified amount. First-order max CAC uses a genuine new-customer first-order cohort: `A/new_customers`; observed CAC needs matched acquisition spend. All-in profit is `R−V−H−ad_spend`. Retain unattributed orders/costs without invented allocation. Future bids also need USD0.15 CPC control and auction feasibility. These equations confer no spend approval.

## Concrete acceptance sequence

1. **Next safe check after owner handback:** Shopify Settings → Customer events → Google & YouTube app pixel → More options → Test. Inspect one app pixel at a time, then pair with standard Google Tag Assistant and the exact Ads action/GA4 receiver diagnostics. A green Pixel Helper event proves callback success, not Google ingestion. Check page/product events without a Purchase-label event; do not reconnect pixels or repeat unsupported worker attachment. [Shopify's supported test](https://help.shopify.com/en/manual/promoting-marketing/pixels/app-pixels), [Google verification](https://support.google.com/analytics/answer/16138144?hl=en), checked September11.
2. Only through the existing consent owner and authorized isolated QA context, test denied/granted/revoked transitions and restore the original state. Do not reuse a peer's unrestored test profile or retry a rejected grant. Cookieless consent-mode pings are not automatically a failure; compare signals and permitted identifiers to the actual implementation.
3. Before payment, verify one intended variant through cart/checkout entry if authorized, then remove the QA item and read cart0. Keep preview flags, actual market/currency and capture completeness explicit. No synthetic production Purchase, live-ad click or agent payment.
4. Reconcile the next genuine order using a protected transaction alias. Compare discounted merchandise value, currency, quantities and stable variant IDs with the exact new AW/label and GA4 event. Store only whitelisted summaries and equality results; private order IDs, request headers, cookies and raw payloads stay outside this packet.
5. Separate dispatch, transport response, receiver ingestion and counted attribution. Check stable transaction identity and same-action deduplication from legitimate repeat delivery or isolated test evidence; never replay a fabricated conversion into production. GA4 and Ads actions do not deduplicate each other. An organic order can prove collection; genuine paid attribution needs its own qualifying interaction.
6. Join that order to actual item/service/freight/duty, settlement and fee records; then close returns/disputes at a stated maturity cutoff. Existing TA-16 owns the Rainbow cost follow-up. Measurement readiness alone never closes profit readiness.

## Reusable artifacts and limits

[acceptance.schema.json](acceptance.schema.json) defines null-preserving evidence and gates; [acceptance.current.json](acceptance.current.json) contains exact bindings and [worked rows](existing_data.csv). [validate.py](validate.py) passes38 source/arithmetic/gate checks, including10 adverse cases. It covers the schema keywords used here; a general Draft2020-12 engine is unavailable. Default execution is read-only; `--report` writes only local validation.json. The original pilot separately passes45 checks. One reference-only heartbeat source changed during review; its hash was recaptured without changing calculations.

Sources: [existing data pilot](../../../2026-09-11-data-pilot/PILOT.md), its inventory and provider/fee files; [90-day Shopify evidence](../../../2026-09-11-google-ads-cold-start-research/EVIDENCE.json); [root repair](../../execution_receipt.json), [passive receipt](../LIVE_READBACK.json) and dated GA4 acceptance. Recent September9–11 ShopifyQL rows show0 orders; September11 is partial and aggregates do not certify the full ledger. Source hashes/scopes are retained in JSON. This lane obtained no new account evidence.
