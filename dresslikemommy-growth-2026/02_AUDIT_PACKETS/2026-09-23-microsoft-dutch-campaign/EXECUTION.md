# Dutch Microsoft campaign — content verified, completion blocked

Confidence: H for the saved fields and native keyword reconciliation; account restriction root cause is UNKNOWN. Overall status: PARTIAL_CONTENT_VERIFIED__ACCOUNT_RESTRICTION_BLOCKED.

Current user request authorizes completion/localization of existing `DLM | MS | NL | NL | Search | 202609`, campaign506255078, Microsoft account477439/customer770182, using US English506254907 as read/copy-only source. Owner explicitly confirmed Netherlands. Campaign remains Paused; no activation or billing change is authorized or performed. Standing paid scope NONE remains unchanged.

## Verified saved result

- Netherlands only, people in targeted locations, Dutch. Fresh target/source settings both USD10/day, Maximize Clicks with USD0.20 cap. Earlier USD20/EnhancedCPC notes were superseded by settled source/target readbacks; no monetary change was made. AI Max, text customization, URL expansion and dynamic search ads are off. Schedule is all days; inherited measurement fields remain unchanged.
- Eight Dutch group names/languages and all group geography/URL/network settings read back. Seven groups Paused; original Matching outfits voor moeder en dochter1275435292107598 remains Draft. Dresses uses Microsoft sites and select traffic; seven others entire network. Source Dresses and FamilyShirts settings explicitly matched these exceptions.
- Eight saved RSAs: all120headlines,32descriptions,8URLs,16paths and8NL-coded suffixes reopened and compared:184fields, zero differences. URLs use `/nl/`, including corrected `/nl/collections/family-sweaters`. Pending review is not approval.
- Native positive export:276rows, all144 intended Dutch Exact/Phrase tuples present, zero duplicates. All132 inherited English extras are Paused. Dutch144 are Enabled beneath the Paused campaign.
- Native campaign-negative export:202rows exactly match all202intended terms/match types, zero missing/extra/duplicates. No shared negative lists applied.
- Native group-negative export:196rows, all45intended present, zero missing/duplicates;151obsolete English extras remain. Counts intended by group6/8/6/0/6/11/0/8. Cleanup manifest includes every extra row.
- Eight Dutch campaign sitelinks with both descriptions and `/nl/` URLs read back;32group associations reconciled exactly. Six Dutch campaign callouts, no group overrides. Eight Dutch group snippets fully read back.
- Final86image associations:76Dutch-captioned copies retain exact original image identities;10captionless associations preserved. No English-captioned associations remain in this target. Source has81associations; five additional captionless images were already in the target's original generic group. Source/shared assets were not edited.
- Exact thumbnail crop comparison:75of76localized images match source; one sweater crop differs, detailed below. Do not claim complete crop parity.
- Eight public Dutch collection URLs returned HTTP200 with Dutch pages and products. Netherlands/EUR checkout behavior was NOT verified; public responses used US/USD default context.

## Concrete remaining blockers and work

Microsoft rejected the attempted original group's Draft → Paused status save with: “This campaign can’t be edited because it belongs to an inactive account. Activate the account if you want to update this campaign.” Business writes stopped. Source US campaign still showed Enabled, so the message does not establish the root cause or global account inactivity. The owner has been asked to inspect/resolve the restriction. No activation, account switching or billing attempt was made.

After owner resolution: fresh-read exact target and finish group1275435292107598 as Paused without activating campaign. Then request concrete action-time confirmation for permanent removal of132paused English positive keywords plus151obsolete group negatives (283total). No permanent keyword deletion has been attempted. Full exact144/202/45 export reconciliation is required after cleanup.

One crop requires source parity: target image extension8864942647875 / source8864942551975, sweater group1276534807763903, image1274334030342589_167FN7IVVLFWYCM. Source ROI [0,0.2857,1,0.8483]; target ROI [0,0.219,1,0.7816]. Original image identity/caption are correct. Native recrop was inspected but canceled without saving because exact mapping was unclear. Reuse the existing target asset; do not duplicate it or guess a crop.

## Evidence and resume

`native/positive_keywords_20260923.csv`, `campaign_negatives_20260923.csv`, and `group_negatives_20260923.csv` are received native files, validated for exact campaign identity. Four aggregate/footer rows in the positive report are excluded from276keyword rows. `native/keyword_export_reconciliation.json` contains full-tuple set comparisons and file hashes; `obsolete_keyword_cleanup_rows.json` preserves all283cleanup candidates. `native/content_readback_20260923.json` is explicitly a root UI-readback summary, not an independent raw asset export. Non-keyword form/maps remain in active CUA state. `live_progress.json` is the machine checkpoint. Payload parser must not be rerun without reapplying owner Netherlands override.

IAB2originaltab1 is preserved; temporary same-browser workingtab2 restored input and is marked for continuation. No unsaved editor. Do not rebuild or repeat Copy/Paste. Earlier browser-blocked checkpoint is retained in `native/earlier_execution_checkpoint.md` as superseded history.

Canonical continuation: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`; anchor `2026-09-23-microsoft-dutch-content-verified-account-blocked`. Next owner action is resolve the observed Microsoft account restriction; root can then resume exactly the saved target.

Machine handoff: authority_source=CURRENT_USER_EXACT_CAMPAIGN_COMPLETION; uncertainty_branch=MICROSOFT_ACCOUNT_REJECTION; independent_verifier=dutch_payload_saved_keyword_exports; external_business_writes=TARGET_LOCALIZATION_ONLY; complete=false.

Independent saved-keyword review: PASS_WITH_GATES; all desired tuples present, zero duplicates, exact283cleanup rows, no desired tuple in cleanup. All16generic mother/daughter outfit keywords report Draft ad group; one paused English cleanup candidate is Disapproved. Numeric IDs are bound by root browser observations; exports contain campaign/group names only. Cockpit render,25-file integration audit(0risks),strictcontinuity10checks and scoped diff check passed. See native/independent_keyword_review.json and verification_checks_20260923.json.
