# Independent local-inventory repair review

**PASS_WITH_GATES.** Confidence: M until fresh modal and persistence readbacks resolve the app's load-integrity risk.

The user's explicit request to fix this Google app settings page covers the proposed reversible correction: turn Off automatic sync in **Retail locations**, then Save once. DLM has no physical retail store ([AGENTS.md](/Users/fsuels/Projects/dresslikemommy/AGENTS.md:14)); the operator supplied the physical-retail requirements from [Google](https://support.google.com/merchants/answer/13709335?hl=en) and [Shopify](https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/shopping-on-google/local-inventory). This review made no external call.

Before writing, root must verify Merchant 124884876, the exact modal, current On and initially disabled Save. After the single toggle, Save must apply only local-retail automatic sync. Preserve the fulfillment location itself and all online-product, country/language, shipping, conversion and account-ID settings. No address should be retained. Normal tool confirmation remains binding; no generic Continue is needed.

The generic error toast and notification count changing 3-of-3→0-of-3 without edits indicate unreliable loading, not verified setting changes. Stop before Save if backend/auth errors prevent a concrete state. After saving, reopen/reload and require persisted Off; do not trust a success toast alone. Capture any error/uncertain persistence as unverified, stop, and do not repeat the write.

Risk: local retail distribution may cease, consistent with the business model. Rollback is the same control On only if a verified unintended outcome warrants it after a fresh state check; no automatic rollback on ambiguous errors.

This verdict does not certify channel restoration: Google permissions and Overview Inactive may remain unresolved. Only this review file was written.
