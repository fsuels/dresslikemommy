# Free traffic that leads to buying customers
Prepared September 9, 2026. Confidence: H in captured Shopify totals; M in strategy; L in forecasts. Additional distribution budget: USD 0. Time, existing software and fulfillment still cost money.

## Decision
Concentrate on **existing organic search demand, free Google product listings and Pinterest**. Add a small photographer-referral experiment after the guide is useful. Consented email can improve conversion/retention within existing capacity; it is not automatically new-customer acquisition.

Run a **30-day pilot from first approved publication**. Initial content audience: US English; preserve Danish dresses as first localized follow-through and Dutch as next search test. This is evidence-led, not proof of market profitability. Existing Merchant and Pinterest owners retain live accounts and prepared releases.

## Current evidence
ShopifyQL, August 10–September 8 inclusive, America/New_York timezone, captured September 9. [Exact queries/results](shopify_baseline.json).

| Signal | Observed | Implication |
|---|---|---|
| Whole store | 4,896 sessions; 115 cart sessions; 27 checkout-entry sessions; 10 completed checkouts; 0.204% completion/session ratio | Attract buying intent and improve the shopping path. |
| Google search referrer | 1,096 sessions; 76 carts ; 11 checkout entries; 5 completed checkouts | Strongest observed buying source. Referrer classification alone does not prove unpaid attribution. |
| DuckDuckGo search referrer | 54 sessions; 4 carts; 1 completed checkout | Preserve normal search discoverability; sample too small to rank channel quality. |
| Unrecognized trafficheap | 508 sessions; 0 carts/checkout entries | Existing traffic-quality investigation stays open. Bots or purchased traffic are not proven. |
| Mobile | 1,980 sessions; 99 carts; all 10 completed checkouts | Verify promoted mobile routes. Desktop zero completions does not prove broken checkout. |
| Denmark | 96 sessions; 2 completed checkouts | Preserve Danish opportunity; two events are not a stable conversion estimate. |
| Social | Facebook 69 sessions / 0 carts; Pinterest 3 sessions / 1 cart / 0 completions | Pinterest is an experiment, not established revenue. |
| Sales | 10 reported orders; USD 821.44 net sales; USD 847.42 including shipping | Revenue is not retained profit; payment/cancellation/cost/attribution still need reconciliation. |

Search categories show 6 of 10 completed checkouts, not 6 proven incrementally acquired organic customers. The new 30-day totals cannot be directly compared to the historical 28-day report. Source top 15 leaves 7 sessions outside the extract; country top 12 leaves 750. Product order counts are not additive unique orders.

Saved GSC exact-page evidence, **August 7–September 3**, all countries/devices: Danish dresses 37 clicks / 568 impressions / position 7.2; Dutch 22 / 723 / 16.1; English pajamas 3 / 307 / 34.3. This is dated, not a fresh GSC read today. Existing DA/NL release is prepared and authorized; preserve its manual publication gate. Pajamas are a longer-term relevance opportunity, not a near-page-one quick win.

## Ranked channels
| Priority | Strategy and buyer intent | Concrete execution | Effort / timing | Owner |
|---|---|---|---|---|
| 1 | Capture existing search demand | Finish the already-prepared DA/NL release. Add item/size/quantity/timing guidance and two verified dress examples to one existing family-photo guide. Keep URLs and untagged internal links. | 2–3 initial hours; about 1 hour/week. Search needs recrawling and weeks to assess. | Root content; TA-06 retains its release owner. |
| 2 | Free Google product listings | Existing Merchant task proves actual offer receipt, free-listing eligibility, accurate size/wearer grouping and landing/price/shipping agreement. Track product clicks through paid orders. | Existing account task; platform processing timing unknown. | Merchant 513 owner. Online products only; no physical store/stock claim. |
| 3 | Product-linked Pinterest | Existing Sunshine Pin first. Then six distinct posts linking to the guide, Rainbow or Pastel Bloom, with honest separate-piece disclosure and tracked links. | At most three total Pins/week, counting Sunshine, with P1–P6 spread over three weeks; about 1–2 hours/week with existing imagery. Distribution is uncertain. | Current Pinterest owner; native identity/duplicate/asset/link checks. |
| 4 | Photographer resource referrals | Offer the original planner to five individually selected family photographers with client outfit guides. Optional shopping links; useful with existing wardrobes. | About 1 hour/week; acceptance unknown. | Exact recipients/messages require authorization. |
| 5 | Consented email | Two short drafts help subscribers choose a look and each person's piece, within existing sender capacity. | 30–60 minutes per approved send. | Sender/consent/quota qualification first. |

Eligible Google product listings can appear without payment, but enrollment does not prove received offers, eligibility or actual showing. Accurate product data supports discovery. [Google free listings](https://support.google.com/merchants/answer/13889434?hl=en), [product data and Search](https://developers.google.com/search/docs/specialty/ecommerce/share-your-product-data-with-google).

Existing Style Journal pages already cover seasons, gifts, care and sizing. Improve useful purchase steps rather than adding generic articles. Competitor collections organize around relationships/occasions, supporting this structure; web results do not establish relative rankings or conversion. [PatPat photo assortment](https://www.patpat.com/collections/matching-family-picture-perfect-outfits). [16 keyword hypotheses](content-opportunities.md) map to existing destinations.

## Deliverables and sequence
[Exact article update](PUBLICATION_REVIEW.md): a near-opening shopping planner plus replacing fixed two-week planning advice with destination-specific timing guidance. All other body content/article fields are preserved. One-page PDF: output/pdf/family-photo-outfit-planner.pdf, local only; no public download exists yet. [Distribution copy](distribution-copy.md): six Pins, one social caption, two emails, one outreach template. Pin artwork/profile qualification is not complete. [Calendar](calendar.csv) is an asset schedule; the existing action_queue.md remains the sole work queue.

Days 1–7: approved article release and live mobile/desktop readback; existing owners finish authorized DA/NL/Sunshine work. Count Sunshine as the first of at most three total Pins in week one; publish P1/P2 only after Sunshine completes and Pinterest release checks pass. Shift the schedule if its gate remains open. Obtain fresh GSC page/query/country baseline through the account owner.
Days 8–14: P3/P4/P5; approved individual photographer outreach; one consented email if capacity qualifies. Review visits, carts and genuine orders.
Days 15–21: P6, then up to two additional variations within the three-Pin weekly cap for the strongest observed qualified-visit destination. If visits bring no carts, investigate the actual buying objection before more production.
Days 22–30: compare complete windows, reconcile orders/costs and choose continue/revise/stop. Review search effects again 6–8 weeks after launch; one quiet week does not establish SEO failure.

## Measurement and decision rules
Update the existing daily_scorecard.md/action_queue.md; no second dashboard, scheduler or background publisher.

Primary outcome: distinct paid, noncancelled orders from qualified unpaid acquisition and retained contribution. Join entry tags/referrer with transaction IDs and actual channel records. Consent loss, paid misclassification, cross-device journeys and last-click bias remain limitations. No ROAS claim at zero ad spend.

Secondary funnel: outbound clicks → tagged sessions → product-detail sessions → cart → checkout → paid order. A guide visit alone is not a qualified product visit. Existing GA4 view_item coverage must be verified by the tracking owner; otherwise use Shopify source/cart/checkout aggregates and label product-detail attribution unknown.

Use utm_source,utm_medium,utm_campaign=organic_202609 and distinct utm_content on external links. Never tag internal article/navigation links. Social/Pinterest uses pinterest/social; email newsletter/email; PDF family_photo_planner/referral. No tracking settings changed.

Day 7: check links and data collection. Day 14: compare guide-first versus product-first routes on product visits and carts, not saves. Day 30:
- Continue destinations producing verified paid orders and supported positive contribution; small samples remain directional.
- At 100 tagged product-detail sessions with zero carts, inspect offer/fit/price and revise once before more posts. This is an operational threshold, not statistical proof.
- Below 100 such sessions, classify acquisition/measurement shortfall or inconclusive evidence; do not infer product rejection.
- Hold a promoted item immediately for a broken buying route or contradicted size/price/shipping/fulfillment truth.
- No paid samples, giveaways, commissions, sponsored links, tools or boosts under the free plan.

Contribution = realized net product revenue + collected shipping − actual product/fulfillment/payment/return costs not already deducted − allocated labor/software/overhead. Keep taxes/currencies consistent and never deduct refunded revenue twice. Current actual costs are incomplete, so profit stays unknown.

## Decision frame and challenge
Decision ID: DLM-DEC-2026-09-09-ORGANIC-BUYER-PILOT.
Hypothesis: existing search demand plus useful buying support and relevant distribution will produce better buying activity than generic reach.
Alternative: direct collection/PDP links remove a step and may outperform the guide. The six-Pin batch includes both, as an observational comparison, not randomized causal proof.
Success: verified publication, attributable buying funnel and supported positive contribution. Failure: no usable qualified traffic, no carts after the threshold, or unresolved product-truth defects. Deadline: day 30 from actual launch; search follow-through 6–8 weeks.
Challenge: search referrals may include paid traffic; 10mobile events are a small sample; a planner can attract nonbuyers. Preserve attribution limits and follow actual orders.
Independent verifier: separate reviewer who did not build or execute this packet; verdict/source binding in review.md. New public changes await exact scope approval; prior approvals for other releases persist.

**Single next owner action:** approve the exact family-photo article body update in PUBLICATION_REVIEW.md. It has a confirmed useful gap, two checked destinations and a rollback. Merchant/Pinterest owners continue independently. PDF upload and other channel sends are later, separate releases.

Continuation: use ops/prompts/paid-growth-ai-army-continuation-prompt.md with organic-only scope, TA-20 and anchor 2026-09-09-organic-buyer-growth-plan. Continue the prepared release and measurement; do not restart the audit, reopen held URL probes, duplicate themes/Pins or broaden paid authority.

