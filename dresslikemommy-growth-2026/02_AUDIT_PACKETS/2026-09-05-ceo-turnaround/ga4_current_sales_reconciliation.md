# Current GA4 purchase reconciliation

Status: `LIVE_VERIFIED_GA4_READ_ONLY`. Confidence: high in the displayed/exported data and exact cross-report join; attribution, retained profit, and original event currency remain limited. Read September 5, 2026 EDT / September 6 UTC; the first normal CSV download was timestamped 01:28:13 UTC, and the JSON records the later readback completion time. This analytics subagent owns these two sanitized evidence files; the parent owns Shopify reconciliation and shared controls.

## Identity and definitions

Existing Chrome `test` tab `475224120`, browser `2`, account `88409806`, property `330266838`, `dresslikemommy.com - GA4`. Property details visibly showed `(GMT-04:00) New York Time` and `US Dollar ($)`. Settings were read only; Save was disabled. Reporting currency is therefore verified USD and reporting timezone is America/New_York. This does **not** prove the original currency parameter sent by each purchase event or the customer's presentment currency.

Source: Reports → Life cycle → Monetization → Transactions. All Users; no comparison or report filter. Primary dimension Transaction ID. Secondary dimensions Date, Session source / medium, and Session campaign ID were read separately, using Ecommerce purchases and Purchase revenue. Normal CSV downloads preserved full numeric precision. No custom report or exploration was saved.

## Purchase totals

| Complete window, New York time | Unique transaction IDs | Ecommerce purchases | Reported purchase revenue USD | Full-precision CSV sum |
|---|---:|---:|---:|---:|
| August 8–September 4, 2026 | 5 | 5 | 432.20 | 432.204968 |
| June 7–September 4, 2026 | 36 | 36 | 2,612.69 | 2612.691065 |

These confirm the earlier GA4 aggregate figures exactly. September 5 partial activity is excluded. The 28-day report visibly covered `1-5 of 5`; the 90-day report covered `1-36 of 36` after Rows per page was set to 50. All 36 IDs appear once, with one ecommerce purchase each. All three 90-day exports have identical key sets, purchase counts, and exact revenue strings; the dated 28-day subset reproduces the five-transaction total.

Adding individually rounded UI rows gives USD432.21 for 28 days and USD2,612.68 for 90 days. Those one-cent differences result from summing rounded rows rather than rounding the exported full-precision sum. Use full precision for the private join; do not “repair” a source value to force an equality.

## Recorded acquisition

| Session source / medium | Purchases 28d | Revenue USD 28d | Purchases 90d | Revenue USD 90d |
|---|---:|---:|---:|---:|
| google / organic | 3 | 211.28 | 20 | 1,500.44 |
| (direct) / (none) | 1 | 118.95 | 6 | 370.62 |
| chatgpt.com / ai-assistant | 1 | 101.97 | 5 | 308.00 |
| google / cpc | 0 | 0.00 | 1 | 151.46 |
| yahoo / organic | 0 | 0.00 | 1 | 99.96 |
| google / product_sync | 0 | 0.00 | 1 | 66.98 |
| chatgpt.com / feed | 0 | 0.00 | 1 | 64.97 |
| uk.search.yahoo.com / referral | 0 | 0.00 | 1 | 50.24 |

Values above are rounded only for presentation. The single google / cpc transaction is dated July 23 and has session campaign ID `23866684201`. Four transactions have campaign ID text `Shopping Free Listings`, totaling USD401.86; 31 have `(not set)`, totaling USD2,059.367279 before rounding. No transaction reports session campaign ID `23867953136`. This is a recorded attribution observation; absent campaign tags cannot establish that a campaign produced no sales.

## Coverage and limitations

- The Date and Session source / medium reports indicated 100% of available data. The quality panel said Unsampled report and Reporting showing daily data. No thresholding or sampling warning was observed.
- The Session campaign ID view instead indicated “mostly complete data,” while its expanded panel still said unsampled / 100% of available data. It additionally flagged **Missing session data**. The UI attributes `(not set)` values to missing session_start events, saying the stream sends event data before the ad_user_data parameter. This is GA4's diagnostic message, not an independently verified implementation root cause. The panel says changes affect future data and may take 24–48 hours to appear. No consent, tracking, or attribution change was made.
- `31/36` transaction campaign IDs are `(not set)` (86.1%). No source/medium value was missing in the three-way export join, but the campaign warning limits attribution confidence.
- Item ID was visible but disabled in the Transactions secondary-dimension selector. No item ID or transaction-to-item mapping was extracted from this report. Parent must use the private Shopify order-line join for campaign candidate product membership.
- Parent reported that all 36 GA4 IDs matched Shopify uniquely, including both refunded/cancelled orders. Thus GA4 purchases must not be treated as retained paid orders. The parent's independent Shopify evidence owns the retained-order denominators and value comparison.
- No event-level original currency, consent sequencing trace, fresh ad spend, CPA, ROAS, product cost, return recovery, or current campaign serving state was obtained in this lane.

## Decision and next action

Use the parent's private Shopify order-line join and fresh campaign costs as the basis for candidate economics. A single CPC purchase does not establish high-intent/low-waste economics, target CPA around USD10.77, 650% ROAS, or safe scaling. Self-cannibalization remains unknown without current account/query inventory.

The latest completed day, September 4, has zero GA4 purchases and USD0 purchase revenue, unchanged from September 3. The current partial day was deliberately excluded. Paid-growth CPA/ROAS are not calculable here. Today's concrete action is to complete the retained-order/candidate join, then prepare a read-only diagnosis of the session_start/ad_user_data sequence. Any production measurement repair requires exact approval.

Private handoff: the approved non-repo reconciliation directory contains the three normal original CSV exports, a date-only normalized file, a date/source normalized file, and `ga4_transactions_with_campaign_90d.csv`. All are mode `0600`; no order identifiers or personal/customer contact data are included in this report or its JSON summary. Original downloads were moved out of Downloads into that private directory. Parent received the private paths directly.

Current tab: [GA4 Transactions, 90 complete days, Session campaign ID](https://analytics.google.com/analytics/web/#/a88409806p330266838/reports/explorer?params=_u..nav%3Dmaui%26_r.explorerCard..seldim%3D%5B%22transactionId%22,%22sessionCampaignId%22%5D%26_u.dateOption%3Dlast90Days%26_u.comparisonOption%3Ddisabled%26_r.explorerCard..startRow%3D0%26_r.explorerCard..rowsPerPage%3D50&ruid=019f8def-dfd0-4785-a638-262fce4dc7be&collectionId=11131314159&r=transaction-id-report). Export menu closed; no unsaved-change prompt or pending external write. The URL uses the site's relative last90Days preset; future sessions must explicitly reselect the fixed dates above.

- authority_context: Parent-assigned read-only GA4; authoritative control `STALE_READBACK_REQUIRED`, `approved_external_scope=NONE`.
- decision_changing_evidence: Retained Shopify order/candidate join; current ad cost; original currency and event-order proof.
- if_evidence_supports_recommendation: Build a bounded test/scale packet from retained Shopify-linked purchases and current cost.
- if_evidence_opposes_recommendation: Diagnose measurement or offer; hold scale and reroute independent safe work.
- material_decision: NOT_MATERIAL; this is read-only reconciliation and decision support, not a launch/scale approval.
- independent_verifier: Parent independently read Shopify and joined transaction IDs; parent owns final integrated review.
- verifier_independence: DID_NOT_BUILD_OR_EXECUTE.
- Continuation: Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` with the parent's reconciliation anchor. Do not repeat the completed GA4 export while these fixed-window private files remain available.

Validation: CSV column schemas, 36 unique IDs, exact Date/Source/Campaign key/count/value equality, 28-day subset count/value, requested date bounds, full-precision aggregate checks, and private file permissions passed. See `ga4_current_sales_reconciliation_summary.json` for sanitized calculated data. Root owns shared continuity checks and integration.
