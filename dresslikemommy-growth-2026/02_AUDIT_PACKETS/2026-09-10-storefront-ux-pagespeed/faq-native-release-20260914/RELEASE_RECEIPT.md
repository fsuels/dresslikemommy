# FAQ repair released and verified

Confidence: H for the bounded functional repair. Status: **LIVE_FUNCTIONAL_PASS_WITH_LIMITS**.

The FAQ sizing answer and seven other answer groups now open through native browser controls on the published storefront. The repair is live in English and all 17 existing translated FAQ bodies. No business wording or links were rewritten.

## Exact scope and chronology

- Action: `TA06-FAQ-NATIVE-DISCLOSURE-RELEASE-20260914`.
- Store: `gid://shopify/Shop/15571635`, Dress Like Mommy, `dresslikemommy-com.myshopify.com`.
- Page: `gid://shopify/Page/161933381`, handle `faqs`, public URL https://www.dresslikemommy.com/pages/faqs.
- Parent plan SHA256: `a02d2b2634029f149a876973531aa1c46bd89d86b54933af049a1340605961ba`.
- Fresh action-time source and all existing translation values matched the reviewed before snapshots.
- `pageUpdate` changed only the English body at `2026-09-14T23:30:04Z`. Returned no user errors. Independent query then confirmed the exact candidate body and new source digest, and all 36 translation records still unchanged.
- A normal public English Sizing activation succeeded before the translated updates.
- `translationsRegister` updated only 17 existing global `body_html` records at `23:30:50–51Z`, using the newly read exact source digest. Returned no user errors.
- Two mutation calls total; no retries, duplicate writes, rollbacks, newly created translation records, theme changes, or Git changes.

Exact English before SHA256: `3ef790830a524e2b2f03585b218d4d679bb97d4bc88554e937b32da6bdebb943`.

Exact released English body and source digest: `c2797437bb4ec0296fbbc5b9ac85f4ea7a4275e7cfd00e5ddf8c5e6ce5dfe0ff`.

## Content and identity preservation

Inventory covered 21 enabled locales in the global scope and six markets: 147 locale/scope combinations. There were 17 translated bodies and 19 translated titles. No market-specific FAQ translation records existed. All existing translated bodies individually qualified for the same mechanical defect repair.

Updated locales: `ar`, `cs`, `da`, `de`, `el`, `es`, `fi`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `nl`, `no`, `pt-BR`, `ro`.

Polish and Russian had translated titles but no translated body. Swedish had neither. These absences remain unchanged; their live routes use the repaired English body. No new translated wording was created. The Portuguese locale's observed public route is `/pt/`.

Every repaired source retains its original eight answer fragments, labels, headings, IDs and links. The repair removes the two obsolete page scripts and eight broken inline handlers per body, substitutes native disclosures and supplies scoped markers/focus/touch-target styling. Across English and the 17 translated bodies, 144 broken answer controls were repaired.

Final independent API queries matched the exact English and all 17 translated candidates. All 36 record identities/values were reconciled, including the 19 untouched translated titles. Page title, handle, original publication date/status, template, creation date, non-body source fields, enabled locales, market configuration and absent records remained unchanged.

Expected metadata changes: the page update timestamp and source body/digest changed. Each registered body translation now has a new update timestamp and `outdated=false`; all 17 were previously `outdated=true`. This automatic registration metadata does **not** certify the preserved translation wording or business claims as current or accurate.

## Live buyer checks

- English: 36 recorded checks cover all eight answers opening and closing at desktop 1280x720 and mobile 390x844, Enter/Space interaction, keyboard access to the Sizing Page link, visible focus and control geometry.
- All 20 other language routes: exact eight control labels found, normal sizing-answer opening and closing verified at 390px, with no horizontal overflow or newly captured console errors. This covers every repaired translated body and the three English fallback routes.
- Post-release console read: zero warnings or errors.
- All measured controls meet the 44px minimum target height and remain within the document width. Desktop, mobile, Arabic and Hebrew screenshots were visually inspected.
- The same pre-existing left-to-right page direction remains on Arabic and Hebrew routes. Their native answer access and narrow overflow checks passed; full right-to-left layout acceptance is not claimed.

The checks used tagged operator URLs (`dlm_qa=faq-native-release-20260914`). Exclude those visits from acquisition/conversion reporting. No tracking setting or analytics filter was changed. No purchase, revenue, conversion uplift or PageSpeed score claim is made. Safari/Firefox-specific device execution was not run.

## Other state and cleanup

Final theme readback at `23:36:04Z` still shows MAIN `133290917985` and reviewed candidate `137888792673` as `UNPUBLISHED`, with their prior update timestamps unchanged. This page release does not publish the theme or clear separate numeric-variant/country/currency theme acceptance gates.

Task-owned IAB1/tab7 was closed and the temporary viewport reset to the starting 1280x720 size. Cart stayed empty. User tabs and the organic owner's IAB2/tab1 and Article559700574305 were not used. No country selector was operated. The browser country changed from AU/AUD (through the Norwegian route at 23:34:31) to CA/CAD (Portuguese route at 23:34:41). Cause is unverified; the latest state was left in place to avoid overriding a peer selection, and the Merchant owner was notified.

The frozen diagnostic's 23 artifacts remain unchanged. All release evidence is in this disjoint successor packet. Parent owns shared claim, queue, problem, worklog and other canonical integration.

## Residual issues and next action

Existing sizing statements conflict over ordered EU/US sizes and automatic Asian-size substitution. Existing payment-processing, operations/location, response, fulfillment, tracking and cancellation statements still require an authoritative factual review. These were preserved, not silently corrected. Missing Polish/Russian/Swedish body translations and Arabic/Hebrew page direction are separate remaining UX gaps.

Parent next action: integrate this live FAQ receipt into TA-06 and retain the existing exact theme owner-publication gate. The functional FAQ repair no longer needs to remain a draft or be repeated. Continue factual wording and remaining localization work as separately bounded changes so important business information is not guessed or overwritten.

Continuation: “Continue TA-06 from the live FAQ release receipt; preserve the released Page161933381 bodies and address the remaining verified wording/localization gaps under exact source review.”

Rollback files contain the exact prior English and translated bodies. A rollback is permitted only for records actually changed, after fresh current-value/source-digest guards: restore changed translations first under the current source digest, then restore English if its body still matches the released candidate. Never overwrite intervening edits. No rollback was needed.

## Evidence map

- `release-source-manifest.json`: per-locale exact source/candidate hashes, protected fields, missing records and rollback boundaries.
- `independent-before-review.json`: independent source, operation, digest and rollback review.
- `mutation-chronology.json` and `mutation-01/02` receipts: exact supported API operations and results.
- `inventory-final.json`, `translations-final-*.json`, `api-verification-final.json`: independent after-state source data and comparisons.
- `browser-live-verification.json`, per-route receipts, `browser-final-cleanup.json`, four screenshots: published buyer checks and limits.
- `independent-after-review.json`: separate raw-source and browser-receipt verification.
- `VALIDATION.json`: final bounded checks; frozen manifest binds final artifacts.
