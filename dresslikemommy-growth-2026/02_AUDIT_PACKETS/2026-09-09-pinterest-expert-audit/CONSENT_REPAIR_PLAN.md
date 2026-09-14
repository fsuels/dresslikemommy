# Consent repair preview — frozen decision

- Decision: `DLM-DEC-2026-09-09-CONSENT-PREFERENCES-PREVIEW`; frozen September 9, 2026 at18:29UTC, before external staging.
- Objective: make the existing Shopify privacy preferences reachable and keep its dialog intact, without changing the app pixel installation or automatically setting consent.
- Baseline: fresh MAIN theme133290917985 and two existing drafts retain three preferences selectors in both a hide rule and a deletion list. MAIN layout MD5 `cc22c0b1bae1461d872aed1bbf4944fd`. Fresh footer/policy render has no preferences entry. Actual SDK opens its dialog as a direct BODY child. Fifteen local tests pass; five regress against the saved baseline.
- Options: create one isolated unpublished repair preview; retain the present inaccessible control; or remove the complete banner suppression customisation. Choose the isolated minimal repair because it preserves unrelated banner policy and makes the customer journey reviewable.
- Prediction: one new unpublished theme contains only the two selector-list edits, one footer preferences button and its supporting code, and two new translation keys in each of21publishedlocales. Existing theme sources remain intact; button activation opens the existing dialog without automatically granting or declining consent.
- Most likely invalidating assumption: the preview lacks Shopify's existing banner SDK, or its actual dialog lifecycle differs from the tested behavior.
- Success: exact candidate bytes read back from the new UNPUBLISHED ID, no userErrors/unfinished job, source parity for MAIN and the two existing drafts, visible desktop/mobile/localized footer and user-initiated dialog behavior.
- Kill conditions: wrong theme/account/role, source drift, unrelated payload changes, missing/rejected SDK without usable feedback, review failure, blocked mutation or unexpected permission/publish step.
- Window/exposure: this execution checkpoint, at most one new unpublished theme and zero advertising spend; no production publication.
- Authority: owner's current “fix everything” instruction covers this reversible repair preview. Existing full-paid control remains NONE. The connector forbids live/MAIN file writes and theme publication; neither will be attempted through a different path.
- Before-state: exact23file MAIN manifest in `/private/tmp/dlm-consent-live-before-20260909.json`; original layout also saved separately. Bind final file checksums and returned new theme ID before upsert. Do not import unrelated local footer or DA/NL changes.
- Verification/rollback: independently review candidate; compare clone to MAIN before upload; read every uploaded file after completion; re-read original themes. Keep preview unpublished if any check fails. Restore only its affected files from captured before-state if a proven staging defect requires rollback; preserve all existing drafts.
- Independent verifier: `/root/consent_diagnosis`, did not build or execute. Staging method PASS; final candidate bytes still require review.
- Evidence that changes the decision: fresh source drift, real preview lifecycle failure, missing translation, or unsupported Shopify SDK initialization.
- Next action: finish independent candidate review, then stage and verify the isolated preview. Live promotion is a separate owner action in Shopify Admin because of the connector boundary.

The exact outcome will be appended after execution; this prediction remains frozen. This packet is evidence, not a competing command layer. Continue through the [canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md).

## Amendment — theme validation, before file upload

Standard Shopify Theme Check found28 MatchingTranslations errors and no other offenses: the two new keys were absent from14additional, unpublished theme locales. The repair now adds the same two keys to all35existing locale files,39theme files total. The21published locales remain unchanged in publication status. This is additive translation coverage only. Fresh MAIN and the new clone each return37existing affected files; the two consent assets are absent. Complete before-state is `/private/tmp/dlm-consent-live-complete-before-20260909.json`. Both existing drafts are snapshotted separately for checksum preservation. Final review and a repeated theme check must pass before upload; no published-language or paid authority changes.
