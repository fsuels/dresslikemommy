# Independent consent preservation review — September 9, 2026

Confidence: H for source identity and the narrow local repair; M for runtime readiness.

**Current verdict: PASS_WITH_EXPLICIT_OPEN_GATES for the unpublished source and final receipt consistency, with root-reported bounded preview QA passed. CSS v1's contrast failure is corrected and read back in v2. Managed-dialog translation and Pinterest receiver accuracy remain open; the isolated test session's original blank consent was not restored. This is not a complete live Pinterest repair or a publication-ready certification.** The reviewer did not author the worker's theme patch, regression tests, or root's upload transform. No browser, credential, consent-state, event, Shopify, or canonical command-layer write was performed by this reviewer. Only this review artifact was created. Later reviews below supersede earlier pending statements; earlier sections preserve the actual sequence of checks and corrections.

## Scope and source identity

Root reports a fresh Shopify Admin read identifying `gid://shopify/OnlineStoreTheme/133290917985` as MAIN, with that theme and two existing drafts retaining the old suppression code. The reviewer independently checked the supplied before-state bytes, but did not repeat the Admin request or certify the account's current state independently.

- Before-state: `/private/tmp/dlm-pinterest-consent-live-before-20260909.liquid`.
- Before MD5: `cc22c0b1bae1461d872aed1bbf4944fd`.
- Before SHA-256: `39962e58bdfa8ede189a82071ef5d2b164b66f7ec8b0a0f8de9e9e623dc00a49`.
- Candidate SHA-256: `d5817734bb7db97f5352cd34bcb724c310db2a49dc9ace165f2a036fb06d77ab`.

Ten independent byte/patch assertions passed against [CONSENT_SOURCE_PARITY.json](CONSENT_SOURCE_PARITY.json): the candidate equals the complete saved live theme plus precisely the two edits in [consent-preferences-fix.patch](consent-preferences-fix.patch). Three preferences selectors are removed from the CSS hide rule and the same three from the JavaScript deletion array. `content_for_header` remains present exactly once. All other theme bytes, automatic-banner predicates, consent API loading, existing fallback behavior, and tracking integration are preserved.

Relevant candidate source: [CSS rule](/Users/fsuels/Projects/dresslikemommy/layout/theme.liquid:420), [deletion list](/Users/fsuels/Projects/dresslikemommy/layout/theme.liquid:431), and [observer](/Users/fsuels/Projects/dresslikemommy/layout/theme.liquid:448).

## Verification actually run

- Inspected the worker's [regression suite](/Users/fsuels/Projects/dresslikemommy/ops/scripts/test_privacy_preferences_preservation.mjs), then executed it with bundled Node: **15 tests passed, zero failed**. Its fixture explicitly limits itself to independently mounted body descendants; it does not claim real Shopify DOM ancestry or consent/event behavior.
- Re-ran that same suite in memory with only its theme input changed to the saved old live source: **10 passed, five failed as expected**. The failures cover CSS suppression, initial preferences, later-opened preferences, predicate-error preferences preservation, and the DOMContentLoaded path. This demonstrates that the suite detects the original defect. An initial result parser assumed TAP while Node selected its default reporter; specifying TAP corrected that diagnostic-only issue.
- Ran a separate reviewer-owned in-memory harness: **16 assertions passed**. Old code removes standalone preferences immediately and on later insertion. The candidate retains them, preserves unrelated controls, retains the existing automatic-banner removal, and preserves required-banner/sale-region behavior.
- The independent adversarial fixture models preferences nested inside a banner wrapper. The candidate still loses those preferences when their ancestor is removed. This establishes why real ancestry is a material gate; it is not evidence that Shopify actually uses that ancestry.

## Remaining customer journey and live gates

Root initially observed that the isolated public product page and Privacy policy offered no cookie/preferences entry point and that no dialog rendered in that existing session. A later root-owned runtime check opened the real preferences modal through `privacyBanner.showPreferences()`: `.shopify-pc__prefs` was a direct BODY child; its overlay/dialog descendants had no banner-wrapper ancestor. Both SDK scripts were loaded. Root recorded `shouldShowBanner=false`, `saleOfDataRegion=true`, all explicit consent values blank, and processing-allowed flags true, then closed the dialog without choosing consent. This clears the ancestor-deletion concern for that observed runtime, not every future preview or consent state. These are root-owned observations, not this reviewer's browser replay. Shopping country/currency are not used as evidence of the detected privacy region. The missing customer-visible reopen control remains confirmed by root.

**Preserving nodes alone cannot repair a missing user entry point.** Shopify's current Cookie Banner API documents `privacyBanner.showPreferences().then(...)` for opening the initialized banner's preferences UI. It requires the `storefront-banner.js` integration; loading only `consent-tracking-api` does not supply that UI. The hosted storefront should reuse its existing integration after checking availability. A user-initiated preferences control can call that method; opening preferences must not automatically grant or revoke consent. The separate custom-storefront example accepts explicit storefront configuration and is not a reason to add tokens or a second banner loader here. [Shopify Cookie Banner API](https://shopify.dev/docs/api/customer-privacy#showing-the-preferences-modal)

Root must verify the new customer-visible preferences entry point on the exact candidate preview, including keyboard/mobile usability and persistence of the previously observed correct ancestry. Accept/reject, reload, reopening, revocation, and resulting pixel permissions remain separate end-to-end checks; no changes to shared browser cookies or consent are authorized for this reviewer. The selector patch deliberately leaves the existing predicate-exception fallback unchanged; it is not a general rewrite of privacy behavior. No purchase accuracy, Tag/CAPI deduplication, consent compliance, or Pinterest traffic result is certified by these tests.

The parity record reports connector restrictions on MAIN writes and publication. This review grants no external authority and recommends no alternate write path around that restriction. Root owns the currently permitted preview and promotion path, fresh before/after readback, and rollback snapshot.

**Next action:** resolve the supported, customer-visible preferences entry point in a permitted theme preview, then verify the actual dialog before any live promotion.

## Unpublished staging method review

**PASS for the proposed isolated staging method; the new footer/21-locale/JavaScript candidate is pending independent payload review.** The latest user request authorizes this reversible preview work. Duplicating the freshly read MAIN theme into a new unpublished theme respects the connector's restriction on MAIN writes and publication. Existing drafts and other operators' changes must be preserved.

Execution conditions are target and readback checks, not another owner-approval request:

1. Root captures fresh MAIN `133290917985` identity and the current theme file baseline. Use the returned new theme ID from duplication; never infer an ID or reuse either existing draft. Read back that it differs from MAIN and has role `UNPUBLISHED` before any file upsert.
2. Before upsert, bind the frozen, independently reviewed file list and hashes to that exact clone. Confirm the clone's baseline matches the fresh MAIN source. Apply only the consent candidate; do not upload the dirty local theme tree or unrelated locale edits.
3. Inspect mutation errors, await a reported upsert job if present, and independently read every changed file back. Confirm the clone remains unpublished, each body matches its intended hash, and MAIN plus unrelated files remain unchanged. A concurrent source change requires reconciliation rather than assuming this clone remains current.
4. Rollback is leaving the clone unpublished or restoring its affected files from the saved clone before-state. No MAIN rollback, theme publication, existing-draft replacement, consent/cookie change, or permission workaround is included.

Shopify documents `themeDuplicate` as returning `newTheme` and `userErrors`; `themeFilesUpsert` targets an explicit theme ID, can overwrite named files, and may return a job. The actual connector's validated schema and access response remain controlling. [themeDuplicate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/themeDuplicate), [themeFilesUpsert](https://shopify.dev/docs/api/admin-graphql/latest/mutations/themeFilesUpsert)

## Customer-visible entry point source review

**PASS for the new component logic and isolated footer additions. Locale-completeness and live-based upload payload review remain pending the 35-locale amendment.** This is not approval to upload the complete dirty local footer or locale files.

Inspected [cookie-preferences.js](/Users/fsuels/Projects/dresslikemommy/assets/cookie-preferences.js), [cookie-preferences.css](/Users/fsuels/Projects/dresslikemommy/assets/cookie-preferences.css), the footer's two asset tags and new control, the two added translation keys, and the new tests appended to `ops/scripts/test_privacy_preferences_preservation.mjs`. There is no separate new test file. The consent scope is the new component/CSS, isolated footer additions, the existing selector repair, and precisely two keys per locale. Existing Spanish footer changes and Danish/Dutch product-copy edits are outside this review's upload scope.

The visible native button is outside the policy-visibility conditional, declares a dialog, and associates a uniquely identified, polite localized status. Both translated strings are escaped in Liquid. The component only calls the existing `privacyBanner.showPreferences()` in response to a click; it adds no SDK loader, consent write, cookie/storage access, tracking dispatch, or network client. The custom element is defined once. API failures and a 10-second no-dialog timeout enable retry. Shopify retains modal focus; the opening Promise is not mistaken for a close signal. Observed closure restores focus only when focus would otherwise be stranded in the removed dialog/body, and does not take it from another control. Disconnect cleanup handles a late error safely.

Reviewer-executed source checks at this stage:

- Updated combined regression suite: **28 passed, zero failed**; JavaScript syntax check passed.
- Separate reviewer-owned synthetic component harness: **19 assertions passed**, including loading the script twice, connecting twice, two complete open/close cycles, expected focus return, preserving deliberately moved focus, one listener after reconnect, and no automatic API opening.
- Parsed all 35 storefront locale files: at the initial review, exactly the 21 published locales contained the 42 new nonempty strings. This proved published-locale presence only, not Shopify theme validation.

Root subsequently ran Shopify Theme Check and reported **28 MatchingTranslations errors** because the same two keys were absent in 14 unpublished locale files, with no other offenses. That is an actual outstanding validation failure for the initial 21-only candidate. The agreed correction adds only those two keys to all 35 existing locale files; it does not activate a language. The final source candidate and 39-file live-based payload must be checked after this amendment. Earlier 28-test success does not override that Theme Check failure.

Reviewed asset SHA-256 values:

- `assets/cookie-preferences.js`: `8b1326af0bdb4acd67b2de8016b627666211c328b1fce2d5a6b6c9047d3375f7`.
- `assets/cookie-preferences.css`: `0e07eeef86980290498ccaf6a51707b823892c59a3934ef5382c25f82ef2b248`.

Native focus behavior, mobile rendering, translated wrapping/RTL presentation, and repeated opening still require the exact unpublished preview. No additional blocking component-code finding was identified; the explicitly failed locale-completeness check and pending payload isolation remain the current source/staging gates.

## Final 39-file payload review

**PASS_EXACT_39_FILE_PAYLOAD_PARITY. No blocking source or payload finding remains for this exact unpublished-theme upsert and after-state readback.** This is neither a MAIN write nor theme publication. Root reports the new theme is `UNPUBLISHED`, `processing=false`, its 37 existing file baselines match MAIN, and both new asset paths are absent. Root also captured the other existing themes' affected-file baselines. Those account readbacks remain root-owned; the reviewer independently verified the supplied source/payload artifacts below.

- Source MAIN: `gid://shopify/OnlineStoreTheme/133290917985`.
- Only allowed upload target: `gid://shopify/OnlineStoreTheme/137880666209`.
- Upload: `/private/tmp/dlm-consent-preview-upload-20260909.json`.
- Upload file SHA-256: `c966c81d8fe3d8adfbd1a17f69e440186f06b5bafb0b935be95ccca780fd7508`.
- Complete source snapshot: `/private/tmp/dlm-consent-live-complete-before-20260909.json`, recorded `2026-09-09 18:35:47 UTC`; file SHA-256 `f0f6520d74e77652f6a13a2f5879f9aac08791b6cc80f7140122279d46343e65`.
- [CONSENT_PREVIEW_MANIFEST.json](CONSENT_PREVIEW_MANIFEST.json) SHA-256: `8278669b5218665aebffb1145776a82e71c965e1619d735520df6c829d50f71a`.
- Total decoded UTF-8 theme-file payload: 3,581,766 bytes across 39 unique TEXT files.

Independent full-payload assertions passed:

1. All 37 saved API `checksumMd5` values match their actual before-state bodies. Payload and manifest each contain exactly 39 unique paths: those 37 existing files plus the two reviewed new assets. No extra file, traversal path, or alternate target is present.
2. Every file's after MD5, SHA-256 and byte length matches the frozen manifest; every existing-file before MD5 matches the snapshot.
3. For all 35 locale files, removing only `sections.footer.cookie_preferences` and `sections.footer.cookie_preferences_unavailable` restores the complete original JSON tree. Removing the exact two textual additions also restores the complete original bytes. Thus unrelated Danish/Dutch edits, other translations and formatting were not imported. The two strings match the reviewed local candidate, including the 21 published languages. No locale activation is part of this payload.
4. Removing only the two consent asset tags and the exact reviewed preferences-control block from the candidate footer restores the complete live-before footer bytes. The existing unrelated Spanish footer edits were not imported.
5. Layout equals the saved live layout plus exactly the two selector-list changes. JS and CSS equal the previously reviewed source and the asset hashes recorded above.
6. [consent-preview-complete.patch](consent-preview-complete.patch) equals an independently reconstructed full before/after diff.
7. The full parsed execution payload at `/private/tmp/dlm-consent-functions-payload-20260909.json` equals the frozen upload JSON exactly. Its serialized file SHA-256 is `8e0c7f894cd8363c558101bff31247ee217e21279cbd720adf09d4e2c2d5a19d`; the different serialization hash does not change the 39 file bodies or target.

After the 35-locale amendment, the reviewer re-ran the final regression suite: **28 passed, zero failed**, now including all 35 locale files and the 21 published subset. Root reports final standard Shopify Theme Check exit **0**; the reviewer separately parsed `/private/tmp/dlm-consent-theme-check-final-20260909.json` and confirmed **`[]`, zero offenses**. The earlier 28 missing-translation errors are resolved in this final candidate.

Remaining verification is post-upsert role/hash readback plus the actual unpublished preview's control, close/reopen, focus, mobile, localization and RTL behavior. MAIN and the other drafts must retain their captured baselines. This payload review performs no consent choice, shared-cookie mutation, purchase event, campaign action, or publication, and does not certify end-to-end Pinterest consent or conversion tracking.

## Staged source after-state receipt review

**PASS_STAGED_SOURCE_RECEIPT_CONSISTENCY.** Independently parsed [CONSENT_PREVIEW_AFTER.json](CONSENT_PREVIEW_AFTER.json), [CONSENT_PREVIEW_BEFORE.json](CONSENT_PREVIEW_BEFORE.json), the final manifest, and the frozen upload. The after-state receipt was recorded at `2026-09-09 18:47:11 UTC`.

- All 39 unique after-state receipt MD5 values equal both the manifest and freshly calculated MD5 values of the reviewed payload bodies. The frozen upload SHA-256 remains `c966c81d8fe3d8adfbd1a17f69e440186f06b5bafb0b935be95ccca780fd7508`.
- New target remains exactly `137880666209`, role `UNPUBLISHED`, `processing=false`, `processingFailed=false`. Before clone parity records 37 matching existing files with both new assets absent.
- All three original theme identities and roles match the before receipt: MAIN `133290917985`, unpublished `137782591585`, unpublished `137850814561`. The after receipt records the same scoped 37-file count and successful preservation for each. This covers the captured files, not an independently re-audited complete theme manifest.
- The initial large request returned HTTP 413. Root reports a separate unchanged-state read before retrying the identical reviewed file set in ten sequential smaller batches through the same connector. The saved after receipt consistently records 39 total files, zero user errors and zero unfinished jobs. This is a transport-size correction, not a different write target or permission workaround.
- The receipt records zero MAIN writes, publications, Pins, and paid spend.

Evidence boundary: root performed the external API reads and reports exact equality of all 39 full returned body strings to the execution payload, plus preservation of the original themes' scoped source bodies/roles. The saved after receipt contains file hashes and preservation results rather than those raw after-body strings. This reviewer independently establishes receipt/payload consistency and does not claim a separate API replay or independent raw-body comparison after upload.

Receipt SHA-256 values: AFTER `ec42bd7f718161e667da585e9f198fb8bc0048a37c9b013709d97c9bf7c837b2`; BEFORE `f71c8f7ee70e5df87fc72ae4037f847f34e761e2b26f01f9802a858461fec125`.

**Remaining gate:** root-owned rendered QA on the exact unpublished preview. Source staging is verified at the stated evidence levels; storefront consent outcomes, publication readiness, and Pinterest measurement accuracy remain outside this after-receipt verdict.

## Rendered v1 contrast failure and bounded CSS amendment

Root's actual preview QA found the new button nearly invisible: computed text `rgba(18,18,18,.95)` on a footer background `rgb(26,26,26)`. The configured foreground variable remained dark despite the customized dark footer. **This is an observed contrast failure, not covered by prior source or synthetic test passes.** Only `assets/cookie-preferences.css` is assigned for the v2 correction; the original 39-file payload and receipt remain preserved.

Root separately reports successful actual preview checks for desktop opening/closing with focus return, keyboard Return reopening, no automatic consent choice, decline-all persistence after reload, accept-all followed by saving marketing-only rejection, and a usable 390px mobile dialog. These are root-owned rendered/consent observations. Original blank-consent cleanup is planned, not yet confirmed in the evidence supplied to this reviewer.

CSS v2 requires independent source review and an exact one-file staging amendment, followed by root's measured contrast of at least 4.5:1, mobile/Arabic wrapping and focus verification. The correction must affect only the new control/status styles, retain visible keyboard focus, and avoid importing other footer or locale changes. Awaiting the candidate; no CSS v2 source or after-state pass is claimed yet.

## CSS v2 source and single-file amendment review

**PASS for exactly `assets/cookie-preferences.css` on unpublished theme `137880666209`.** Reviewed the actual CSS, its complete diff against the saved v1 payload, and [CONSENT_CSS_V2.json](CONSENT_CSS_V2.json). This supersedes the preceding pending-source statement; it does not clear the observed rendered failure until root verifies the deployed preview.

- Before MD5: `b5a42a92b98f19380c86815797b816af`.
- After MD5: `c5fcad430f9e542b7bc5a87226e28e9d`.
- After SHA-256: `e2b78b61877ea1ebcac30dd9faa3ae2ab834283e3aa1aecd28ced984bd5b7515`.
- New file size: 669 UTF-8 bytes.

The three-class button/status selector has higher specificity than the observed two-class `.footer .link` rule. It supplies solid `#ccc` text, `1.4rem` font size, `1.5` line height and wrapping. The button retains its `4.4rem` minimum target height and gains `max-width:100%` with normal wrapping. Hover/focus-visible text is white. The change adds no outline removal, hidden state, opacity, pointer-event suppression, or global footer rule; JS is unchanged at the independently reviewed hash.

Using the standard sRGB relative-luminance calculation, solid `#ccc` on the observed `#1a1a1a` background is **10.8375:1**; white is **17.4043:1**. These are independently calculated expected ratios for the specified colors, not a claim about the actual computed cascade. Root still owns measured rendered contrast, readable mobile Spanish/Arabic wrapping, focus visibility and consent-session cleanup.

The v2 Theme Check artifact `/private/tmp/dlm-consent-theme-check-css-v2-20260909.json` independently parses as `[]`, zero offenses. The original frozen 39-file v1 payload retains its prior SHA-256; the amendment replaces only this CSS file and leaves the other 38 file bodies frozen. Retain the original v1 CSS as the exact rollback body. A CSS v2 after-state readback remains required before any visual-success claim.

## Final CSS v2 and bounded runtime handoff review

**PASS_WITH_EXPLICIT_OPEN_GATES.** Independently reviewed [CONSENT_CSS_V2_AFTER.json](CONSENT_CSS_V2_AFTER.json) and [CONSENT_RUNTIME_QA.json](CONSENT_RUNTIME_QA.json) against the reviewed CSS source, amendment, identities, computed contrast and stated limitations. No external API or UI replay was performed by this reviewer.

The first CSS after-read was correctly classified as conflicted: new checksum metadata accompanied the old 235-byte body. Root obtained a separate second read with the exact 669-byte body and matching checksum, without repeating the write. The final receipt's MD5/SHA-256/byte size match the independently reviewed CSS. Its recorded rendered values are `rgb(204,204,204)`, 14px text and 44px target height on `rgb(26,26,26)`. Independently recalculated contrast is 10.8375478:1, consistent with the reported 10.8375:1 and above 4.5:1. This clears the specific v1 contrast failure at the root-observed preview.

Root's 11-entry runtime record is internally consistent: real dialog open/close with focus return, Return-key reopening, decline/reload/reopening, accept then granular marketing rejection with persistence, 390px mobile usability/no horizontal overflow, and English/Arabic/Spanish footer-label rendering passed for their observed scope. Arabic's new button was 143.5px wide and 44px high. This is rendered evidence for those sampled routes, not all 21 published languages.

The following limits must survive the owner handoff:

- **OPEN:** the Shopify-managed dialog remained English on an Arabic route despite the Arabic footer label and `Shopify.locale=ar`. Inspect the supported Shopify privacy configuration before claiming complete multilingual consent behavior.
- **NOT VERIFIED:** Pinterest network/receiver acceptance, post-deduplication behavior and order parity. Source installation and Shopify processing flags do not establish those results.
- **CLEANUP PARTIAL:** root exited the browser preview to the existing MAIN page, reset the viewport, returned to English/US with cart zero, and closed the temporary tab. This was browser navigation, not a theme rollback or publication. Original blank consent was not restored: `legacy_tracking_consent` was absent before and after the choices, so a no-op deletion did not reset consent. No essential/authentication cookie was cleared.
- **TEST-SESSION STATE:** the isolated in-app session remains `analytics=no`, `marketing=no`, `preferences=no`, sale-of-data unset; analytics/marketing processing flags are false. Root reports no storewide privacy setting or Chrome-consent change. Future tracking checks must account for this declined test-session state rather than misclassifying expected suppression as a new tag defect.
- **NATIVE ACCESS:** the latest root observation is `MAC_LOCKED`, with owner unlock already requested. It supersedes the earlier account-switch diagnosis for the current Pinterest access step. No additional owner request is created by this review.
- **UNPUBLISHED:** new theme remains the staging target. MAIN, public Pins, campaigns and spend were not changed by this work according to the scoped receipts. This review does not grant publication authority.

Final receipt SHA-256 values: CSS v2 AFTER `52bc76e06cfa840a92849104d37c4fe977d3ff1ae540cc70bffe76243565e221`; runtime QA `c8e1caaf40599ebec630749c8ac92e9db3e6fac51d99db49dbe9782819f590ce`.

No additional blocking source finding was identified in this final receipt review. Continue from the recorded owner-access gate, preserve the exact unpublished candidate and test-session state, and close the explicit managed-dialog and Pinterest measurement gaps before reporting full completion.
