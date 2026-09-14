# Analytics and SEO baseline — 2026-09-05

Status: `LIVE_VERIFIED` within the report scopes below. Confidence: high in displayed metrics; medium in diagnosis; actual profit and attribution remain unverified.

This is a bounded read-only audit by the analytics lane. It updates evidence only. The parent owns shared command-layer integration, approvals, and live changes.

## Sources and freshness

- Shopify connector verified Dress Like Mommy / www.dresslikemommy.com, USD, timezone reported EDT. Readbacks: September 5, approximately 18:39–18:50 EDT. Aggregate sales reports do not certify paid/non-cancelled order truth.
- GA4: account 88409806, property 330266838, Chrome test tab 475224120. Traffic acquisition, All Users, purchase selected for Key events. Property timezone and currency configuration were not inspected. UI displays dollars.
- Search Console: URL-prefix property https://www.dresslikemommy.com/, Chrome test tab 475224114. Web Search, unfiltered dimensions. Performance last updated “6 hours ago”; index report last updated August 27.
- GSC periods are August 7–September 3 versus July 10–August 6, Pacific Time. Shopify comparison aligned to those date labels still disagrees directionally; its timezone is EDT. Clicks and sessions differ by definition, attribution and coverage. [Google date/dimension definitions](https://support.google.com/webmasters/answer/17011259).

## Sales versus traffic

| Shopify metric | Aug 8–Sep 4 | Jul 11–Aug 7 |
|---|---:|---:|
| Orders | 8 | 16 |
| Gross sales | $734.99 | $1,065.00 |
| Sales reversals | $0 | -$136.71 |
| Net sales | $734.99 | $928.29 |
| Total sales, including shipping | $760.97 | $955.46 |
| Reported AOV | $91.873 | $66.562 |
| Sessions | 10,393 | 3,545 |
| Cart sessions | 114 | 169 |
| Checkout-entry sessions | 25 | 75 |
| Completed-checkout sessions | 8 | 14 |
| Session conversion | 0.077% | 0.395% |

Orders halved; net sales fell 20.8%; sessions rose 193.2%. The higher AOV is good, but eight orders do not establish a durable improvement.

| Longer Shopify window | Orders | Net sales | Total sales | AOV |
|---|---:|---:|---:|---:|
| Jun 7–Sep 4, 2026 | 47 | $3,616.78 | $3,708.90 | $79.861 |
| Mar 9–Jun 6, 2026 | 70 | $4,042.55 | $4,094.73 | $62.434 |
| Sep 5, 2025–Sep 4, 2026 | 166 | $10,904.48 | $11,088.13 | $69.648 |

Daily: September 3 and 4 each had zero orders/revenue. September 5, partial at readback, had one order/$54.47. Paid attribution, campaign CPA and ROAS cannot be established from these aggregate store figures; root must join the Ads/Pinterest lane. Today improved against yesterday in total sales only.

## What explains the traffic rise?

| Shopify segment, last/prior 28d | Sessions | Cart sessions | Completed checkout |
|---|---:|---:|---:|
| Desktop | 8,545 / 2,008 | 15 / 28 | 0 / 3 |
| Mobile | 1,832 / 1,529 | 99 / 139 | 8 / 11 |
| Direct | 8,679 / 2,082 | 29 / 57 | 4 / 8 |
| Google search referrer | 987 / 1,260 | 78 / 99 | 3 / 5 |
| Unrecognized “trafficheap” referrer | 508 / 0 | 0 / 0 | 0 / 0 |

The surge is concentrated in desktop/direct, with almost no incremental buying activity. The owner does not recognize trafficheap. This supports investigating unwanted traffic, referral spam, crawlers and attribution loss; it does not prove bots or a purchased-traffic campaign. Mobile conversion also fell, so removing suspicious visits would not resolve every concern.

## Measurement gap

GA4 recorded five purchase key events/$432.20 revenue for Aug 8–Sep 4, versus Shopify eight orders/$734.99 net: aggregate gaps of 37.5% and 41.2%. Over 90 days, GA4 had 36 purchases/$2,612.69 versus Shopify 47/$3,616.78. Reconcile transaction IDs, payment/cancellation status, timestamps, consent, currency and value before calling the gap entirely lost tracking.

GA4 28d Organic Search: 878 sessions, 76.2% engagement, three purchases/$211.28. Unassigned: 1,204 sessions, four engaged sessions, 1-second average engagement, zero purchases. Paid Search: 180 sessions, zero purchases/value. Its all-event “key event rate” includes view_item and other diagnostics; it is not purchase CVR.

GA4 90d Organic Shopping: 150 sessions/four purchases/$401.86, absent in the last-28d displayed rows. Parent should connect this with Merchant/free-listing health. Paid Search: one purchase/$151.46 over 90d, not sufficient scale evidence. Displayed channel-session rows sum above displayed total sessions; retain row and total provenance and do not force additive attribution.

Historical PROB-2026-05-20-GA4-SHOPIFY-PURCHASE-PARITY says SOLVED, but its body documents undercounting and an unresolved repair. Reopen/reclassify through the parent. Non-US purchase currency and duplication remain unproven in this audit.

## Preserve the organic assets; concentrate improvements

GSC clicks increased 911 vs 812 (+12.2%), impressions approximately 41.5K vs 33.9K. CTR decreased 2.2% vs 2.4%, position 19.2 vs 17.8. This supports improving existing demand capture, not deleting the localization work.

1. **Denmark first for overseas validation.** GSC 101 vs 75 clicks; /da/collections/dresses 37 vs 26; /da 30 vs 9. Queries include “mor datter tøj” (7 clicks/93 impressions) and “mor og datter kjole” (7/82). Shopify shipping-country sales: four orders/$444.73 net in 90d; 13/$847.88 in 365d. Audit Danish collection-to-PDP-to-checkout and localized purchase measurement; prepare native-reviewed exact/phrase candidates with verified CPC feasibility.
2. **Improve commercial paths from successful Greek content.** /el/blogs/news/mommy-and-me-matching-outfit-ideas generated 66 vs 35 clicks; Greece 113 vs 73. Link relevant currently purchasable products only after content/landing inspection. Three Greek orders produced $126.61 net after $69.73 reversals in 90d: clicks are not profit proof.
3. **Preserve Norwegian and Dutch dress collections.** /no/collections/dresses 40 vs 29 clicks; /nl/collections/dresses 22 vs 29. No Norwegian shipping-country orders appeared in 90/365d results. Diagnose local checkout/offer fit before paid expansion.
4. **Triage valuable missing URLs, not every exclusion.** Index report: 8,784 404s, 5,038 crawled-not-indexed, 12 server errors. Many sampled 404s are variant/country URLs. Separate active canonical pages with demand from obsolete URLs; no blanket redirects or mass indexing. Alternate canonicals (6,263), redirects and deliberate exclusions are not automatically errors.

GSC overview strengths: 173 mobile URLs rated good, none poor; 76 valid product snippets and merchant listings, zero invalid in those coverage samples. This is limited coverage, not whole-store certification.

## Products and economic decision

Current Admin ACTIVE status confirmed for Skyfade (7536992976993; three orders/$239.31 net in 90d), cream chiffon beach dresses (7227438530657; two/$123.96), green stripe swim trunks (7510790996065; two/$119.62), Sunshine Stripe (7545279512673; one/$118.95) and Vintage Cottage pajamas (7533081133153; one/$101.97). Current status alone does not prove seasonal fit, market availability, landed cost or paid landing quality. Blank product-ID rows represent seven orders/$410.47 net and cannot become ad targets without a valid join.

Owner clarification: roughly 50% covers costs except marketing/returns; 30% profit target. For pretax booked revenue after discounts B, actual non-ad costs C net of recoveries, actual refunds R and ad spend A: profit = B − R − C − A. If starting with realized net revenue N already reduced by refunds, use N − C − A; **do not subtract refunds twice**. State whether margin is divided by B or N.

365d sales reversals were $657.25, 5.685% of gross less discounts; 90d $136.71, 3.642%. Reversals include refunds, cancellations and edits, and are not net return loss. [Shopify definitions](https://shopify.dev/docs/api/shopifyql/latest/schemas/sales_revenue/sales). As an illustrative booked-revenue scenario only, 50% cost + 30% profit + 5.685% reversal reserve leaves 14.315% for ads (~699% ROAS). At 650%, only 4.615% remains for return loss. Country/product costs and recovery data must settle the real threshold.

The $0.15 cap alone cannot assure profit: at $70 AOV and 650% ROAS it requires about 1.39% paid conversion; at 700%, 1.5%. Observed organic or mixed-traffic CVR is not a paid forecast. Keep one owner per intent/market/language/landing. The parent’s initial $50 exposure is a test envelope, with later $500+ scaling conditional on verified return-adjusted economics and exact authority.

## Handoff

Next action: reconcile recent Shopify paid/noncancelled orders with GA4 and Ads purchase records, starting with the 8-vs-5 window, while the parent advances Danish landing/keyword proof. This protects the next spend decision without discarding functioning organic assets.

- authority_context: read-only analytics/SEO assignment; authoritative control STALE_READBACK_REQUIRED, approved_external_scope NONE; parent owns newly clarified budget interpretation.
- decision_changing_evidence: transaction/value/currency parity; actual market contribution costs and returns; qualified campaign economics.
- if_evidence_supports_recommendation: bounded test, daily Shopify-linked purchases/value/CPA/ROAS, then scale packet.
- if_evidence_opposes_recommendation: repair measurement/landing or narrow/reroute; no automated scale.
- independent_verifier: parent-designated marketing safety reviewer; verifier_independence: DID_NOT_BUILD_OR_EXECUTE.
- material_decision: launch/scale recommendation requires independent review; no live change executed.
- Stop conditions: authentication, account ambiguity, permissions, billing, unsafe disclosures, or settings/write controls outside exact authority.
- Continuation: use ops/prompts/paid-growth-ai-army-continuation-prompt.md with this packet and the parent’s new anchor.

Files: analytics_shopify_aggregates.json; analytics_shopify_additional_aggregates.json; analytics_ga4_gsc_readback.json; this report. Browser actions changed report views/date/event filters only.

