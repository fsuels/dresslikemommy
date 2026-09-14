# Combined storefront release candidate — frozen revision 1

Confidence: H for exact source preservation and local checks; combined rendered acceptance remains NOT RUN.

IMPLEMENTED in the isolated `release_candidate/` folder. The Merchant revision 3 candidate is unchanged. The release uses **525 checksum-verified MAIN files**, individually matched to the current source manifest, with fresh Shopify reads for missing or different local sources. No dirty root file was accepted without its exact MAIN MD5/size match. Four fresh source reads also confirm the prior reviewed UNPUBLISHED theme **137782591585**; all four saved source bodies match its current MD5s.

The **46-file release** combines:

- Merchant revision 3’s exact linked-variant initialization, current localized prices, availability guard, qualified returns and selector translations.
- Purchase-confidence shipping text changed to a neutral checkout message in all 35 locale files. Its fixed 12–16-day value, date target and update attributes are removed. Country, currency and change-country controls remain identical, with a localized shipping-policy link.
- The exact reviewed cart improvement, four DA/NL dress SEO values, and five Danish selector labels. The two approved Danish wording differences override the later dictionary proposal; functional Merchant JavaScript is otherwise identical to revision 3.
- The independently reviewed consent control: four exact nonlocale files, including the **669-byte CSS v2**, and only two additional footer keys merged into each of 35 locales. All 39 consent source files match the final handoff hashes; no whole locale file was substituted.
- The independent structured-data correction: remove invented price-expiry data and the unconditional 30-day Offer return policy. Remove the single hidden product-FAQ render call carrying unsupported delivery copy. Offer selection, price, currency, availability, URLs, identifiers, other schema and the unused FAQ source file remain intact.

VERIFIED: 18 Merchant regressions, 28 consent regressions and 10 release integration checks pass. The exact reviewed cart remains **15 passes and one identical pre-existing quantity/subtotal fixture failure**; this is not a clean full-cart suite. Tests use synthetic DOM/source fixtures; they do not render Shopify Liquid. The shipping test includes the old date script as a positive control and verifies it cannot refill the removed target. All 46 changed files pass the Shopify Liquid skill’s Theme Check with complete source context and zero diagnostics; 44 existing baseline counterparts also pass. Three JavaScript syntax checks and whitespace validation pass. An unused variable found in the first shipping check was removed and the affected release rechecked.

Frozen [payload](release_candidate/candidate_files.json): SHA-256 `3b32bf05196772f7a1939c95f39c1f89601c54ee8bf5a36f0681e5c72c87cf60`, **4,410,277 bytes**. [Receipt](release_candidate/candidate_files_receipt.json), [full patch](release_candidate/candidate.patch), [verification](release_candidate/verification_summary.json), exact before-state and rollback bodies are included. New assets account for two of the 46 files.

Worker external writes: **zero**. Root owns independent final review and staging on existing UNPUBLISHED **137881223265**, followed by desktop/mobile and locale journeys, cart/currency checks, policy links and parsing the complete emitted JSON. The peer-observed Shopify preferences dialog still uses English on the Arabic route; that limitation remains open. No publication, shipping configuration change, locale activation or traffic/profit claim is made.

Next action: root’s hash-bound combined review, because it verifies the exact release before preview staging. Continuation: “Review release revision 1 against its receipt, then stage and verify that exact unpublished preview.”
