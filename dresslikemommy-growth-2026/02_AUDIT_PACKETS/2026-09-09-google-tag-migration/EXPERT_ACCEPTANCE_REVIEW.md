# Independent GA4 acceptance review

Confidence: H. Verdict: **PASS for the scoped transport findings, with receiver, purchase and theme-release limits retained**.

Reviewed `GA4_EXPERT_ACCEPTANCE_20260910.json`, its Markdown report, and prior `CLEANUP_VERIFICATION.json`. This is an independent review of the operator's retained evidence, not a new browser observation or receiver test. The reviewer did not execute migration, alter settings, generate events, or modify shared canonical files.

The records correctly separate the initial UNPUBLISHED137881223265 session from MAIN133290917985 after Exit preview. Preview consent-control results do not establish that the repair is published. MAIN page_view, view_item and begin_checkout have positive HTTP204 observations with truncated capture windows; complete counts are not asserted. The complete add_to_cart window records one matching USD39.99, quantity1, variant44047096348769 event.

The final denied MAIN reload's 488-event, untruncated window supports zero observed Google requests only within that bounded window. Final fresh MAIN cart0 supports cleanup, even though the removal occurred on the preview theme. The cart recurrence is linked to PROB-2026-09-06-CART-RETURN-DISPLAY; its cause remains a hypothesis. These limits are stated appropriately.

HTTP204 is not GA4 report ingestion. Receiver acceptance, genuine purchase identity/value/currency/deduplication and custom-field equivalence remain unverified. The zero-order cutoff result includes the dated final 2026-09-10T00:44:40Z recheck. Prior duplicate cleanup remains verified; the wizard counter conflict is preserved.

The requested clarification is verified: all three item-bearing `main_events` now use the observed app key `sku`, their SKU values are preserved, and none retains an `item_sku` field. Legacy `item_sku`, session-number and purchase-value equivalence remain explicitly false in `custom_field_acceptance`.

No correction remains for this review's scope. No additional live test or production change is required by this review. This verdict does not authorize or certify the separate theme release.
