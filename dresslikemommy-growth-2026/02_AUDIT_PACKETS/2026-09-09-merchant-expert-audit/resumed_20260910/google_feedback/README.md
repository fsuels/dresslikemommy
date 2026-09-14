# Shopify Google-app feedback refresh

Confidence: H for the Shopify readback and comparison; receiving Merchant/source identity remains UNKNOWN. **VERIFIED read-only refresh; no product, channel, source, or account mutation.**

The validated Shopify Admin connector query ran from **2026-09-10 00:29:17 to 00:29:37 UTC** against Shop15571635. Five sequential pages returned 50/50/50/50/40 products: all 240 unique ACTIVE product IDs match the prior cohort, with terminal `hasNextPage=false`. All 14 coverage/comparison checks passed. The prior snapshot was captured September9 at 16:42:45 UTC.

| Feedback cohort | Prior | Current |
|---|---:|---:|
| Generated September8–9 | 232 | 163 |
| Historical June4 | 6 | 6 |
| No feedback | 2 | 71 |

Exactly **69 records disappeared; none appeared; all 169 retained records are unchanged**. The two previously absent records remain absent. No returned feedback was generated after the prior capture; the latest retained generation timestamp is September9 at 09:42:09 UTC. “Recent” retains the original September8 cutoff for comparison and does not mean freshly generated during this refresh. Absence is not approval or evidence of a completed re-review.

Overlapping messages on the September8–9 cohort:

| Message | Prior products | Current products |
|---|---:|---:|
| Unclaimed website | 232 | 163 |
| Pending initial review | 232 | 163 |
| Missing age group | 159 | 104 |
| Missing color | 41 | 41 |
| Missing gender | 37 | 37 |
| Missing size | 1 | 1 |
| Personalized advertising: personal hardships | 96 | 71 |

The six June4 records still contain missing age group5, missing gender1 and unavailable product page4. No September8–9 unavailable-page message is present. Across all dates, missing attributes total age109/color41/gender38/size1. These counts overlap and are not a count of disapproved offers.

The schema and response expose App1780363, titled Google & YouTube, feedback generation time, state, message text and a Shopify product editor link. Every retained detail has `REQUIRES_ACTION`. Neither ResourceFeedback nor AppFeedback exposes a receiving Merchant account or data-source ID; the link identifies the app and product only. Country and marketing-method strings inside messages do not establish current Merchant513 eligibility. These records must not be reported as current disapprovals in Merchant513.

A local exact-ID join places 68 disappearances in the completed identifier-repair cohort and one outside it (Product7607764287585). The swim/dress market-join products were already feedback-absent. This association does not establish why feedback disappeared.

No exact source-field mutation is justified by feedback alone. Missing-size Product7535944368225 is identified, but the correct consumed size value and receiving-source mapping are not exposed. Any repair proposal needs a fresh field/variant read, grounded replacement, exact scope, before-state, inverse payload and independent after-readback; do not infer values or resubmit products from these old messages.

**Next action:** obtain the owner-ready exact Merchant513 source/diagnostic readback already gated in the parent task. It resolves receiving-source uncertainty before treating these messages as Merchant repair targets. No browser, credentials, Merchant API workaround or native-control attempt occurred in this lane.

Evidence: [query](feedback_query.graphql), [current rows and page receipts](product_feedback_current.json), [schema](feedback_schema.json), [comparison and checks](comparison.json), [cohort association](cohort_relation.json). Only new files within this folder were written. Continuation: reconcile exact receiving Merchant/source evidence with these dated Shopify feedback rows.
