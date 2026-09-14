Confidence: H on source extraction; current URL health and recovery value remain unknown.

**No exact 404/5xx candidate rows can be recovered from this packet.** The JSON therefore contains `candidates: []`, not invented URLs or rankings. GSC was read on September 5; its index report was last updated August 27, 2026. It reported **8,784 Not found (404)** and **12 Server error (5xx)** URLs. These are historical aggregate counts.

The audit saved four strings under `sample_canonical_paths`, following a review of the first 10 of 1,000 shown 404 examples. It says many examples contained variant/country/currency parameters. These are **normalized path leads**, not preserved original example URLs or verified Google canonicals:

- `/fr/products/family-matching-hawaiian-shirt-and-floral-dress`
- `/pt/products/matching-love-heart-printing-couple-t-shirts`
- `/ru/products/couple-matching-shirts-mr-and-mrs-wedding-gift-anniversary`
- `/ru/products/parent-child-one-piece-cut-out-bowknot-bathing-suit`

Their exact original query strings and crawl dates are missing. No 5xx sample URL was recorded. None of these paths appears in the saved 10 top-page rows or four focused exact-page reports for Aug 7–Sep 3 versus Jul 10–Aug 6. Exact clicks, impressions and backlinks are **unknown**, not zero. No source-linked prior URL-recovery receipt is referenced by the scoped current reports. None can therefore be classified as truly unhandled, previously fixed, or query/locale/canonical noise.

The missing artifacts are specifically the dated **Page indexing → Not found (404) → Examples** and **Page indexing → Server error (5xx) → Examples** URL-level exports, retaining full URLs and available last-crawl dates. Subsequent priority needs exact-page performance/backlink rows and any existing exact redirect receipt. The saved aggregate counts and normalized paths cannot substitute for those rows.

Do not import the Greek empty-pajama HTTP 200 finding or later 429 rate limits into this 404/5xx list. Working performance pages and alternate-canonical exclusions are also not automatically broken routes.

Next owner action: obtain those two issue-example exports, then join their exact URLs to root's separate public-status and redirect-capability evidence. This permits a scoped recovery decision without guessing destinations or demand.

Sources: [index/readback JSON](analytics_ga4_gsc_readback.json) at `/gsc/index`; [baseline audit](analytics_seo_audit.md), indexing paragraph; [focused GSC evidence](gsc_traffic_priority.json), four exact page reports; `seo_priority_change_briefs.md` and `CEO_TURNAROUND_PLAN.md` references. [Candidate-source JSON](organic_url_recovery_candidates.json) records exact provenance, null unknowns and source hashes.

Only these two local artifacts were created. No browser, external query/write, shared-state edit or broad historical audit occurred. Validation checks exact path preservation, empty candidate rows, metric nulls and source-file hashes. Continuation: “Supply the dated 404 and 5xx Examples exports and reconcile only their exact URLs with current status and prior recovery receipts.”
