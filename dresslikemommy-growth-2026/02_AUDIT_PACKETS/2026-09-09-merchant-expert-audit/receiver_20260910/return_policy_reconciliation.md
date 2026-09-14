Confidence: H for current Shopify source; the cause and age of Merchant’s incorrect detection remain UNKNOWN.

The published [legacy return-policy page](https://www.dresslikemommy.com/pages/return-policy) currently states **30 days from delivery**, not 15. Fresh schema-validated Shopify read at **September 10, 2026, 18:49:51 UTC** identified Shop 15571635, Dress Like Mommy, and Page 161929989. The page is published; its published date is October 23, 2016 and last update April 28, 2026, 06:57:45 UTC.

Official Refund Policy 14695685 also states 30 days. The two HTML bodies have identical normalized visible text and HTML event structure. Their only differences are two formatting newlines. Eligibility, swimwear/intimates/Final Sale/gift-card exclusions, exchanges, damage handling, refund timing and shipping-cost terms match. Therefore **no page-body correction is needed**.

No Shopify redirect record matched `/pages/return-policy`; both filtered result connections completed pagination. This proves the stored page/redirect state, not a full HTTP redirect trace. Public web retrieval corroborates 30 days but reports a three-week-old crawl; the current finding rests on the fresh Shopify read. The separate canonical-policy web open was unavailable, and its current body was obtained through Shopify.

The root-observed Merchant suggestion for 15 days and ten countries is inconsistent with current source content. Stale or incorrect extraction is plausible; this read cannot identify the precise cause or certify Merchant acceptance.

Exact UTF-8 body bindings:

- Page, 2,636 bytes: `6f63f061500595080c381f33b3bccc90264b13f7bc2f7d6ebbf3770a170f44b5`
- Official refund policy, 2,634 bytes: `a0e7f90e201df7169edf00073d48b47aa58afc69ae7b6003ee8b93720e58d7fb`

Terms §6 separately classifies all sale and personalized items as final sale, broader than the refund policy’s explicitly marked Final Sale exclusion. Its return-postage exception (“unless we made an error”) also differs from the refund policy’s damage/defect exception. These conflicts are recorded without a Terms rewrite or legal-precedence judgment.

[Machine payload](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/receiver_20260910/return_policy_reconciliation.json) includes exact before bodies, a byte-identical no-op candidate/rollback, query/schema receipts and **20/20 passing checks**. No mutation is proposed or executed. The local documentation helper failed to connect; structured documentation search and both query validators succeeded.

Next owner action: review Merchant’s suggestion against the verified 30-day policy rather than accepting 15 days, preserving the policy exceptions.

Continuation: “Use this source evidence to reconcile the Merchant return-policy suggestion; leave the already-matching page unchanged and track the separate Terms conflict.”
