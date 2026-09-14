# Existing GA4 pixel: exact helper repair for owner review

2026-09-06. **Prepared and independently reviewed; NOT SAVED to Shopify.**

Target: Dress Like Mommy Shopify custom pixel `111181921`, **DLM GA4 Measurement Protocol**, measurement `G-N4EQNK0MMB`, GA4 property `330266838`. Current Disconnect control is visible. The proposal replaces only `getClientId`'s cookie-truncation branch with two statements that store and return the full cookie. It does not claim to explain or recover the three missing purchases.

## Bound source and exact change

The full installed editor contents were read using the documented browser clipboard API after selecting and copying the Code textbox. Only fingerprints and the credential-free helper are saved here. The original clipboard was empty and was restored to empty. No code was pasted or saved, no event was sent, and no external tracking/configuration change occurred.

| Editor-copy representation, UTF-8 SHA-256 | Fingerprint |
| --- | --- |
| Current complete source, 10,697 JavaScript code units | `5aa1a3e64a256511f09e1eddc2445982fa8d1872588d9a0860f571f800a726b5` |
| Proposed complete source, 10,496 code units | `6f552b8a71090701fe93c7468012d2911bd1ad869dfb42f65b4bc27b643f484c` |

The 644-unit installed helper occurs exactly once and matches [the saved before fragment](installed_ga4_get_client_id_before.js). The [candidate](installed_ga4_get_client_id_candidate.js) and [exact patch](installed_ga4_get_client_id.patch) preserve its stored/generated fallback. Complete-source prefix and suffix are unchanged. The inverse helper replacement restores the exact full-source before hash.

The unchanged isolated test reproduces **four expected failures and three passing holdouts** against the installed helper; the candidate passes **7/7**. Node syntax checking of the candidate helper passes. Independent [helper review](installed_ga4_helper_review.md) supports exact owner review, with release gates. Whole-buffer parsing inside CUA returned `EvalError` for both versions; neither script was invoked and no alternate evaluator was attempted. That check is unavailable, not evidence of a candidate syntax error.

## Save and rollback gate

The current command layer requires fresh exact approval for production tracking changes. Approval of this packet would cover **one helper repair and code/configuration after-state readback**, not campaign spending, consent changes, synthetic purchases, historical-event replay or a tracking-stack migration.

Immediately before an approved save, re-copy the live editor and require the exact current hash above. Keep that raw before-state privately in the same tool session until verification completes. Reconstruct the candidate from the freshly read source and the exact helper patch; never use the repository's whole template or persist its embedded credentials. Stop on a hash mismatch, missing authority, unexpected prompt or changed target.

After one approved save, reopen/read the Code textbox and require the proposed full-source hash plus the existing connected state and configuration. If an unintended change appears, preserve evidence and use only the retained exact before-state under the approved rollback scope. For a later isolated rollback, require the exact candidate hash, replace only the candidate helper with the recorded original, and verify the original full hash. Stop for unrelated source drift.

## Effectiveness and next decision

The [no-purchase validation contract](installed_pixel_validation_plan.md) separates source binding, identity choice, dispatch and an attributable Analytics receipt. The public 429 challenge still prevents the live check; a code save cannot be called restored purchase capture or successful attribution. Existing truncated stored IDs can persist when the cookie is unavailable. No actual margin, sales uplift or new paid authority is established.

The full-editor read gap is resolved; fresh approval, source freshness at save and permitted live validation remain. Reuse `installed_ga4_binding_readback.json`, the helper test receipt, independent review and `installed_ga4_binding_checks.json`. Do not repeat the completed order join, pixel inventory or stream mapping.

The single current owner priority remains the Italian paid/unfulfilled-item resolution. One exact-order search of the verified business mailbox returned zero results and no further page; this does not establish that no outside remedy occurred. The existing owner question remains pending. See [the mail receipt](italian_resolution_mail_evidence.md). No customer message or financial action is authorized by this packet. Existing Google support approval and its validation gate, organic-release work and all nine paid-control fields remain unchanged.

Continuation: use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` and the latest CEO-turnaround anchor in the existing command layer.
