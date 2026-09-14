# Google tag migration — September 9, 2026

Owner: root task 01a086fc-0bf7-71a2-ba21-aa3564fafe30. Stage: HANDOFF. Configuration migration and exact duplicate cleanup VERIFIED; reopened wizard progress is CONFLICTED and non-actionable. The final resumed result below supersedes the earlier blocked handoff.

## Scope and before-state

The current user explicitly requests completion of the migration notice in the open Shopify Google & YouTube tab, including removal of duplicate tags. This is fresh, narrow integration authority; full-paid authority remains NONE. Existing broader Google task 01a08223-036e-7fa3-8961-ecd297163fb5 was observed idle before this cutover. Root owns the existing Chrome test Shopify migration tab and a separate Customer events inventory tab. Other claims and settings remain preserved.

LIVE_VERIFIED in native Chrome during this session:

- Store: Dress Like Mommy, admin path /store/dresslikemommy-com.
- The Google & YouTube Overview displays the exact migration notice. Merchant 513542500 shows zero products and no linked Ads account; no Merchant or Ads action is included here.
- Migration wizard: 1 of 3 tasks completed; existing Google account step complete; one detected tag G-N4EQNK0MMB, named dresslikemommy.com - GA4 Destination; one GA4 destination G-N4EQNK0MMB. Migrate checkbox initially clear; migration buttons disabled.
- Warning: code-based GA4 custom dimensions and metrics will not migrate. Standard sitewide ecommerce measurement is offered.
- The wizard's Review tags link opened Google tag account 6056111167/container 93018894. It shows G-N4EQNK0MMB and GT-PJ5D7RB, with the sole displayed destination dresslikemommy.com - GA4. Existing diagnostic: some pages are not tagged.
- No authentication, new permission, terms or billing step encountered. No external mutation yet.

## Frozen decision

Decision ID: DLM-DEC-2026-09-09-GA4-TAG-MIGRATION. Proposed action: migrate the one verified existing GA4 destination through the supported app, confirm persisted configuration, then disconnect only freshly identified duplicate GA4 emitters with reversible UI controls. Keep the existing property/history. Status quo leaves the warning and legacy checkout compatibility risk. Alternative manual app tag entry has the same destination but bypasses useful detected-tag review.

Prediction: the wizard can install the retained GA4 tag without creating a new account, changing paid campaigns, or affecting other integrations. Invalidating evidence: unexpected destination, permission/terms gate, unsupported critical privacy setting, or failed persisted readback. Success: app confirms migration and exact tag persists; every duplicate action has before/after connection proof. Purchase ingestion/value/currency/deduplication is a distinct acceptance check and cannot be claimed from setup alone. No synthetic purchase or payment is authorized.

Rollback: preserve custom pixel source and reconnect only an exact disconnected sender if replacement checks fail; remove only the newly added app tag through its normal Manage tags flow when needed. Never delete pixels or GA4 history. Any rollback must avoid leaving both senders indefinitely enabled. Maximum financial exposure: zero new spend, purchases or billing actions.

Independent verifier: tag_migration_review, read-only, DID_NOT_BUILD_OR_EXECUTE. Preliminary verdict PASS_WITH_GATES for the verified GA4 migration; receiver and duplicate evidence remain to be collected. Historical source differences include custom item_sku/session_number and purchase totalPrice versus the app's discounted merchandise value; do not claim unchanged report semantics.

Official sources: https://support.google.com/tagmanager/answer/15642481 ; https://support.google.com/analytics/answer/16108370 ; https://support.google.com/tagmanager/answer/16091176 .

## Execution and result

At approximately 16:32 UTC root selected G-N4EQNK0MMB and clicked Migrate selected tags. Subsequent native readback: 2 of 3 tasks completed, Review and migrate Google tags step complete, Remove duplicate tags step incomplete, with an Ok acknowledgement. This proves the migration step was saved; final completion and duplicate cleanup remain pending.

Fresh Customer events inventory has eight entries: custom GA4 111181921, custom Ads 111214689, Facebook/Instagram, Google & YouTube 1780363, Judge.me, Microsoft, Pinterest and TikTok. GA4 editor shows Disconnect DLM GA4 Measurement Protocol and installed code const GA4_MEASUREMENT_ID = G-N4EQNK0MMB. Its source remains untouched; API secret was not emitted or persisted. The Ads custom pixel is not qualified for removal by this GA4 migration alone.

Native control recovered from a user-selected tab change by reacquiring Chrome with cua.getApp as requested by the tool. An earlier attempt to refresh the stale binding was rejected by automatic review; no action was forced. A blank screenshot and stale disabled-button view resolved through normal Chrome View > Exit Full Screen; the enabled migration button was then freshly observed before clicking. No access/security configuration was changed.

All raw authentication query strings, credentials, customer information and pixel secrets are excluded from this record.

Persisted app settings after migration: Settings > Additional conversion measurement settings > Google tags shows G-N4EQNK0MMB under Manually added Google tags, with Save disabled. The other installed tag is the existing Merchant GT-T5R7JFVL / MC-7BWRVJETCH for 513542500. Connected services remain Merchant and Business Profile (2); migration did not directly link an Analytics or Ads service. Manual tag configuration is supported by Google's migration workflow.

Local theme scan across layout/snippets/sections/assets/config/templates found no G-N4EQNK0MMB, GT-PJ5D7RB, GTM loader, gtag call or Google Analytics loader. This is local-source evidence only. A separate unauthenticated public-source request through Python could not resolve the domain in the sandbox; no source result or current-public absence is claimed.

Independent cutover amendment: tag_migration_review returned conditional PASS for disconnecting the exact GA4 duplicate after app-origin consented nonpurchase delivery and source coverage checks, followed by a reload/retest. This bounded reversible sequence supersedes the historical purchase-before-retirement order for the current user-requested migration. A genuine purchase remains required to certify purchase delivery, transaction identity/value/currency/items and repeat-visit deduplication. Keeping both senders indefinitely is not an acceptable substitute. Ads111214689 remains outside GA4 duplicate retirement.

At approximately 16:38 UTC, native Google Tag Assistant connected to the public homepage (US/USD, cart0, no customer form or order). It reports two Google tags: G-N4EQNK0MMB and GT-T5R7JFVL. GA4 detail: On-page gtag('config'), IDs G-N4EQNK0MMB/GT-PJ5D7RB, destination G-N4EQNK0MMB, Hits Sent > Page View. This is a live browser-dispatch observation; GA4 receiver ingestion is not yet established. Consent inspection is pending. No purchase event was generated. Browser focus changes continue to interrupt some operations; fresh native reacquisition is used rather than stale actions.

## Current handoff, approximately 16:45 UTC

IMPLEMENTED and configuration VERIFIED: one GA4 tag migration. NOT DONE: custom111181921 disconnection, duplicate-cleanup acknowledgement and Complete migration. No custom pixel code/status was changed. Existing source and reconnection path are preserved. A duplicate-collection risk remains while both the legacy GA4 sender and migrated app tag are enabled; do not describe this as a finished migration or duplicate-free setup.

At16:40 the app task inventory identified three other active tasks sharing native Chrome focus: Merchant01a08706-c63a-7e01-ba48-7777bcb1788a, Pinterest01a08704-8176-7171-b6f5-928a09d7c3f9 and Microsoft01a08703-644f-7940-8f67-9a2fa63722bb. All acknowledged a temporary migration lease. After their pause, Chrome consistently returned only All products - Merchant Center, empty AX and Screenshot unavailable. Finder AX succeeded; no current evidence establishes Mac lock, missing permissions or authentication failure. Fresh native reacquisition, one normal fullscreen shortcut, Finder opening the existing Chrome application, and reset of this task's CUA JavaScript session did not restore readable Chrome. No browser/helper restart, security changes or indirect account mutation was attempted. The native lease was released to the Merchant task next, with a request for sequential use and immediate notification if usable Chrome returns.

One next action: restore a visible, controllable normal Chrome window, then finish the exact GA4 cleanup before unrelated Google changes. Existing owner authorization persists. Resume current Tag Assistant consent and GA4 source coverage/receiver checks, disconnect only custom111181921 when qualified, reload/retest, then acknowledge cleanup and Complete migration; read back the Overview. Preserve custom Ads111214689, existing Merchant tag, all other integrations and history. No new blanket approval needed. Use the existing canonical continuation prompt and anchor2026-09-09-google-tag-migration-partial-readback.

Confidence: H on the saved app configuration and Tag Assistant dispatch; M on overall migration because cleanup, receiver, consent and genuine purchase verification remain incomplete.

Final independent review by /root/tag_migration_review: PASS for accurate partial-completion reporting; no material mismatch across this receipt, the problem entry, coordination row and TA-02 row. Reviewer did not execute/build or modify any record. No claim of complete migration, duplicate-free collection, receiver ingestion or proven purchase tracking is approved.

Final local validation: strict continuity returned CONTINUITY_OK with all ten checks passing; command-layer integration audit passed with 25 of 25 tracked documents integrated and zero side-document risks; scoped git diff --check passed. These validate the handoff records, not GA4 receipt or completed duplicate cleanup. Canonical updates are recorded in the worklog, coordination claim, problem tracker, decision/outcome log, current marketing state, TA-02 action queue, cockpit, blocker board and review log.

## Resumed execution — 2026-09-09 18:09 UTC

The owner explicitly renewed completion authority. Fresh native Chrome AX worked; a normal View > Exit Full Screen action restored visible, responsive rendering. Pinterest, Merchant and Microsoft acknowledged exclusive native use for this cutover. No browser restart or permission change was needed.

Fresh pre-cutover proof: app Google tags showed saved G-N4EQNK0MMB with Save disabled and existing Merchant GT-T5R7JFVL intact. Tag Assistant expanded Consent Default showed analytics_storage, ad_storage, ad_user_data and ad_personalization granted. Its GA4 page_view hit used analytics.google.com/g/collect, destination G-N4EQNK0MMB, Shopify event marker page_viewed and cookie-consent field G111. The Consent tab separately said default not configured; this discrepancy is retained. The explicit command/hit state is evidence for this test only, not proof of affirmative visitor choice or denied-consent behavior.

Independent tag_cleanup_verifier returned PASS_WITH_GATES before the final disconnection. Fresh exact custom111181921 editor showed the matching GA4 destination, Analytics required, and Disconnect. The supported confirmation said the pixel would stop being loaded and could be reconnected. Root confirmed Disconnect once. After-state: Pixel disconnected toast, Connect DLM GA4 Measurement Protocol control, retained source and unchanged destination. Root did not edit or save pixel code.

Root navigated to Customer events and fully reloaded. The rendered inventory showed the old GA4 Web badge gray; Ads111214689 remained green Web, and Google & YouTube remained green Server/Web. All eight entries remained. A screenshot was visually inspected in the tool result; no customer or secret source screenshot was persisted.

Root reloaded the existing debug homepage once. Tag Assistant added a distinct new page group, events22-31 versus prior6-15. The isolated new page contained exactly one GA4 Page View; its hit fired on29 History Change with the same GA4 destination, standard collection endpoint, Shopify page_viewed marker and G111. This verifies replacement dispatch after legacy retirement, not backend receipt or universal deduplication.

The refreshed app Overview has no migration notice. A direct return to the previously observed wizard route initially rendered an empty embedded app; normal app entry restored the Overview. A final3/3 acknowledgement has not yet been observed or clicked in this resumed turn.

## Final resumed result

The delayed direct wizard read resolved successfully: it displays **1 of 3 tasks completed**, **No tags to migrate at this time**, and a disabled **Migrate selected tags** button. It offers Go to settings; no duplicate acknowledgement or Complete migration button is present. This is a conflicting interface progress indicator, not a failed saved-tag or pixel-status readback. Root did not click a final acknowledgement or claim a 3/3 result, and did not repeat the tag installation. Merchant confirmed it had not clicked any migration acknowledgement in its separate task.

Root returned using the wizard's back control. The loaded Overview was inspected in AX and a rendered screenshot: the migration notice is absent. The independent verifier's final verdict is PASS for configuration migration and identified duplicate cleanup, with wizard completion status CONFLICTED. Saved configuration, exact status change, one post-cleanup page-view hit and the contradictory wizard counter are retained together.

Tag Assistant debugging was stopped through its normal dialog with Keep domain enabled unchecked. Final readback says this browser is not actively debugging any domains. Native Chrome was left on Google & YouTube Overview, with no unsaved form, and released to Pinterest; Microsoft follows by their direct handoff. No account, campaign, Merchant, other pixel, consent configuration, source code, billing, purchase or payment change was made.

Current next tracking action: reconcile the next genuine Shopify purchase against GA4 receiver transaction identity, value, currency and items. No new purchase is requested or generated. This validates sales measurement separately from the completed configuration cleanup. Inspect denied-consent behavior and the documented custom-field/value differences as part of that acceptance; do not reconnect the legacy sender merely to address the wizard counter. Existing source and the verified Connect control remain the narrow rollback path if a causal replacement failure is demonstrated.

Canonical continuation: ops/prompts/paid-growth-ai-army-continuation-prompt.md, anchor 2026-09-09-google-tag-duplicate-cleanup-verified. Do not repeat migration or the completed duplicate disconnection.

Final resumed local checks: strict continuity returned CONTINUITY_OK with all10checks passing after the new anchor; command-layer integration25/25 and0risks; scoped git diff --check and structured receipt/UTF-8/whitespace validation passed. These checks validate records and continuity, not untested purchase accuracy.

Independent final consistency review passed the configuration/duplicate versus wizard/purchase boundaries. Its one clarification was applied to the current tracking checkpoint: the verified cutover explicitly supersedes older instructions to keep the legacy pixel connected until purchase proof. Historical paragraphs were preserved.

After the final clarification, one interim strict check detected the cockpit cache before its source refresh. The existing dashboard service generated the updated cache (observed0.27seconds after source), and the final strict rerun returned CONTINUITY_OK/all10PASS. No extra renderer, service or UI change was introduced.
