Confidence: H for the Shopify readbacks; end-to-end Google synchronization is not yet verified.

The correct first implementation path is the existing Google & YouTube app's automatic sync. Its actual Product sync and Countries and languages settings still require an account-bound native read. This phase made **no external changes** and created no recurring sync job or duplicate feed.

| Control | Verified state | Action |
| --- | --- | --- |
| Current ACTIVE source | 240 parents, 4,945 exact variants; all 240 parents available to Google and Online Store at September 10 15:46 UTC | Preserve the current publication coverage and earlier product repairs. |
| New-product inclusion in market catalogs | International, Eurozone and United States: enabled | Already configured; no flag change needed. |
| Unattached Estonia catalog | Automatic inclusion enabled, no associated markets | Preserve it; this is not evidence of a fourth served catalog. |
| Google publication flag | autoPublish false; forward catalog lookup binds it to AppCatalog 7676067937 | This does not establish that the Google app's automatic sync is off. Candidate API change was validated syntactically but **NOT RUN**; its suitability and target-specific support are unestablished. |
| Google app Product sync | UNKNOWN | Read current mode and Merchant account binding; set automatic sync if needed. |
| Countries and languages / future countries | UNKNOWN | Configure every actually served, supported combination and automatic future-country sync. |
| Merchant received offers and free-listing eligibility | UNKNOWN | Reconcile real source IDs, language, feed label, country coverage, processing time, errors and status. |

The desired lifecycle is:

- A product becomes ACTIVE and available on Online Store and Google: create its relevant offers.
- Product, variant, price, availability or supported translation changes: refresh the same offers.
- A product becomes DRAFT/ARCHIVED, loses required publication, or is deleted: withdraw its corresponding offers and verify that Google stops serving them.
- Reactivation: restore eligible offers without a manual Google archive blocking restoration.
- Markets and languages change: reconcile current Shopify availability, shipping, supported Google targeting and actual source coverage.

Google documents continuing product sync after updates and a separate future-country option. That option does not certify every future language. Shopify's app coverage table is narrower than Google's general language support. Reuse the existing 65-country / 21-language matrix; verify uncovered cells before adding maintained primary sources. Do not create 1,365 duplicate country-language feeds. See [Google's sync controls](https://support.google.com/merchants/answer/13693394?hl=en) and [language support](https://support.google.com/merchants/answer/160637?hl=en).

Use Shopify's lifecycle as the normal source of truth. Merchant UI archiving persists across uploads and requires manual restoration, which conflicts with automatic reactivation. A removed product also needs receiving-side verification; no guaranteed withdrawal time has been established. See [Google's archive behavior](https://support.google.com/merchants/answer/160541?hl=en).

Only if a real publication gap is observed should an existing Shopify Flow be configured for Product created and Product status updated, preserving draft status and scheduled launches. Only actual missing translated offers justify an additional maintained primary source. The repository has no current Google lifecycle publisher to enable; its Merchant workflow produces diagnostics, while the existing feed host is Pinterest-specific.

Evidence and review: [source baseline](../menu_completion_20260910/shopify_source/README.md), [current catalog receipt](catalog_snapshot.json), [official lifecycle research](official_lifecycle.md), [API candidate review](preflight_review.md), [existing code inventory](code_inventory.md), [exact desired configuration](lifecycle_setup.json).

Next action: complete the existing selected-tab confirmation so the root can inspect Merchant 513542500 and the connected Google app. No native retry or account workaround occurred in this phase. The earlier automatic approval review rejected selecting native Chrome because it could expose unrelated private content.

Continuation: follow [the canonical continuation prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md), using this lifecycle packet and the latest Merchant anchor. Do not repeat product repairs or publish the superseded theme.
