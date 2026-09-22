# Microsoft UET and September 21 completed-day readback

Confidence: H for the observed native configuration and arithmetic; M for diagnosis because exact orders, consent sessions, sender identity and attribution remain unjoined.

Action: `TA15-RECEIVER-AND-DAY-20260922`. Account `477439`, customer `770182`, UET `36005151`. Native evidence: September 22, 08:25–08:28:51 UTC. This is a completed read-only operating step; the overall tracking repair and profitable-growth objective remain PARTIAL.

## Decision-changing evidence

Microsoft receives events, but a repaired purchase-measurement path is **not verified**. The September 22 partial-day receiver shows one Custom `purchase` and parameter names `GoalValue`, `Currency`, `PageType`, `ProductId`. It exposes no parameter values, exact order identity, line items or duplicate suppression. Its **Healthy** consent tooltip expressly reports no events from the EEA, UK or Switzerland; this is not a passing regional purchase-consent test.

The live regional diagnostics say 25% of page-view events and 0% of the checked `begin_checkout`, `add_to_cart`, and `view_item` events had a consent signal during the last seven days. These figures cover EEA/UK/Switzerland only. They are signal-presence diagnostics, not consent-granted percentages, legal conclusions, selected-day percentages, or isolated proof of an app-pixel defect. Denominators are unavailable. The earlier denied standard-publisher capture and the rejected cross-tab custom candidate retain their separate evidence boundaries.

The primary `ShopifyCheckoutCompleteEventTracking` goal matches action **Equals to purchase**, UET `36005151`/ShopifyImport, variable revenue with USD0.00 fallback, Count All, 30-day click window, 1-day view-through window, Last click attribution, and Yes for auto-bidding optimization. Its table says **No recent conversions**. The edit dialog was inspected and cancelled; the unchanged goal table was compared before/after. Correct configuration does not prove received value or attribution. Enhanced-conversion state was not adjudicated.

## Newly completed reporting day

September 21, Eastern Time (native account label), read at September 22 08:28 UTC:

| Surface | Spend USD | Clicks | Impressions | Reported conversions |
|---|---:|---:|---:|---:|
| Search | 2.97 | 20 | 617 | 0 |
| Audience | 4.38 | 27 | 2,649 | 0 |
| Account total | 7.35 | 47 | 3,266 | 0 |

Reported revenue is USD0.00. Audience placements account for 59.5918% of spend. Zero reported conversions does not establish zero Shopify purchases. The UI's USD0.00 CPA cell is not an economically valid CPA with zero verified acquisitions; true CPA and contribution profit remain unknown. No improvement or wasted-spend claim is made.

This replaces only the September 21 partial USD4.34/28-click snapshot. The September 15–20 snapshot retains its original source date and was not refreshed or combined here. The new date is a completed reporting day, not final attribution. Native UI warns that recent UET conversions may lag two hours.

Nine currently visible campaigns retain the same status/budget tuples as the September 21 source: US/CA/GB/Latinos/EUR/AU Enabled at USD20/day each; NL and FR&CA Paused at USD20/day; DE Paused at USD3/day. USD120/day is the configured Enabled total; USD163/day includes Paused allocations. Neither is actual spend, a hard account cap, or approval. No CPC settings were reopened; earlier US/CA USD0.20 and EUR USD0.10 readbacks keep their own dates and the owner's USD0.15 ceiling remains.

The September 21 UET table totals 776 events across five rendered event types and has no purchase row. September 22 partial totals 165 events and contains the one purchase. Chart and table totals reconcile. This does not join an event to a distinct order. Relative “last received” timestamps remain current even when Yesterday is selected, so they are not treated as exact selected-day event times.

## Scope and next action

There were zero business mutations, support sends, mailbox retries, Shopify order reads, test purchases, cart actions, billing changes or shared canonical edits. Task-owned IAB tabs1/2 were retained; the goal dialog is closed. Current control is `READ_ONLY_MARKETING_RECONCILIATION`, paid external scope `NONE`. The exact six-campaign pause decision and numeric total daily-budget/maximum30-day-loss question remain pending without repetition.

The next tracking action is a supported publisher correction through existing case **7108824779**, using [the prepared addendum](support-addendum.md) when its existing authenticated channel is available. This addendum is LOCAL and NOT SENT. The September 21 mailbox mismatch and failed human chat connection were not retried unchanged. Team consultation remains the last verified stage; no engineering escalation, email reply or repair is asserted. Preserve the rejected custom purchase implementation. After a supported correction, verify standard and app consent, a single purchase sender, exact order value/currency/items, and receiver deduplication.

The parent may use this dated receipt in its existing full-sales cycle, but order/event attribution requires explicit joining evidence. No duplicate full-sales query was issued.

Root consistency checks: 27/27 PASS. Independent saved-source review is recorded separately; it is not an independent native replay. Sources: [source.json](source.json), [readback.json](readback.json), [root-verification.json](root-verification.json).

Continuation: use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` and `TA15-RECEIVER-AND-DAY-20260922` with current controls. Do not repeat this completed snapshot without a changed date, authority, support response or measurement premise.
