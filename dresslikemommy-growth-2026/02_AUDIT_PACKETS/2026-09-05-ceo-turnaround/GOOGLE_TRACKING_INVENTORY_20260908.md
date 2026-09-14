# Google tracking inventory — September 8, 2026

## Latest native readback — tracking still requires receiver proof

Anchor `2026-09-08-ceo-turnaround-merchant-link-cleanup-product-coverage` supersedes the earlier blank-window gate and zero-mutation checkpoint. Merchant **513542500** and Shopify's saved link remain verified, with www.dresslikemommy.com Verified/Claimed. Two exact non-spend repairs are IMPLEMENTED and LIVE_VERIFIED: remove only the inaccessible **Ads3990976848 → Merchant513542500** catalog link; turn Shopify local retail inventory sync **Off**, persisted after reload/reopen. Merchant now has two linked services, Shopify and the existing Business Profile; no accepted Ads link remains visible. This does not prove all historical Ads spending stopped.

Fresh Shopify coverage: **240 ACTIVE products /4,945 variants; 240/240 published to both Online Store and Google & YouTube;21 published locales**. No bulk product publication is missing. Merchant's sole provided Content API source **10014302986**, US/en, still showed **0 products / no update timestamp**. Submission, received offers and approvals are not verified. International automatic sync is On;19 grouped current country/language rows include DK da/en, DE/AT de/en and CZ cs/en. The51 warnings comprise31 unsupported countries and20 language entries; their aggregate semantics remain unresolved and do not prove all non-English disabled. Preserve current Markets and verify actual localized offers before changing combinations.

Owner-selected Ads manager **7001079966** has no directly linked clients. Existing operating candidate **6509972886** is listed as setup in progress under the current Google identity;4683483813 is absent from that list. Inspect650's direct role/setup and link it under700 if qualified, then connect the operating customer to Shopify/Merchant. A manager cannot connect directly to Merchant. Ads/GA4 setup is optional for free product synchronization. GA4330266838/G-N4EQNK0MMB remains disconnected from the app; current tags/custom senders and purchase receipt still require verification before exact retirement. No further account creation is indicated.

Chrome View → Exit Full Screen restored visible capture, tables and controls through normal UI. A later separate native call reported the Mac locked and automatic unlock unsuccessful. Current single owner action: **unlock the Mac and leave Chrome test open**; the request is pending. Do not repeat the obsolete bring-window-forward request. Resume product-status/error and first-offer checks, imported shipping/returns, then Ads/GA4 linking. Paid control remains NONE; goal objective and original four-hour heartbeat are preserved. Evidence: merchant_513542500_execution_20260908.json and MERCHANT_ALL_ACTIVE_COVERAGE_20260908.json in the existing CEO packet.


Confidence: M. Stage: DIAGNOSE / HANDOFF. Prepared by tracking_inventory for root integration; no production writes. This packet is evidence for the existing command layer, not new authority or a replacement harness.

**Recommendation:** use the existing Google & YouTube app as the Google tracking owner, preserve GA4 property `330266838` and its history, bind the verified replacement Ads/Merchant identities, then disconnect only the duplicate or obsolete Google senders identified by fresh source and receiver checks. No current evidence qualifies deleting a pixel or an account today from this lane.

## Current-source proof and capability gate

The validated Shopify connector queries returned store `15571635`, Dress Like Mommy, `dresslikemommy-com.myshopify.com`, and published theme `133290917985` (`dresslikemommy/main`). Current-session readbacks completed by 18:08:33 UTC. Both requested-file pages and MAIN-theme pages were complete.

- `layout/theme.liquid`: source checksum MD5 `cc22c0b1bae1461d872aed1bbf4944fd`; no literal Google destination IDs, UA ID, gtag call, or Google tag loader found. It loads `assets/analytics.js`, supplies site-language context, and preserves `content_for_header`.
- `assets/analytics.js`: source checksum MD5 `350ac72d8869394475ad0d8fc994cc80`; no literal Google destination IDs, Google endpoint, gtag, fetch, or sendBeacon call. It pushes local ecommerce/navigation events to `dataLayer`; this is not independently a Google sender.
- These two source reads do not inspect rendered app injection, app embeds, all referenced snippets, checkout settings, GTM container contents, or Google receivers. Absence here does not prove absence elsewhere.
- `appInstallations` validated but execution returned **access denied**. That field was stopped without retry, reauthentication or alternate access. Independent permitted shop/theme reads succeeded.
- Current public schema exposes app-owned `webPixel { id settings }`, not `customPixel`/`customPixels` source/status inventory. No pixel settings or secrets were requested.

See [sanitized receipt](google_tracking_inventory_20260908_source.json) and [validated queries](google_tracking_inventory_20260908_queries.graphql). Raw theme bodies were reduced transiently to the allowlisted facts above, not saved.

## Sender / receiver / decision map

| Surface | Destination and evidence | Decision |
|---|---|---|
| GA4 receiver | Account `88409806`, property `330266838`, stream `4030905738` / `G-N4EQNK0MMB`: Sept 6 saved native mapping | **KEEP property/history.** Current access and app-linked stream need readback. Receiver preservation does not require retaining every sender. |
| GA4 custom sender `111181921`, DLM GA4 Measurement Protocol | Sept 6 connected source sends to `G-N4EQNK0MMB` via MP. Exact repaired source SHA-256 `6f552b8a71090701fe93c7468012d2911bd1ad869dfb42f65b4bc27b643f484c` survived reload | **HOLD now; conditional DISCONNECT after replacement verification.** Preserve completed helper repair and rollback. Sender-specific ingestion remains unproven. Never paste the repo template over live code. |
| Native Ads custom sender `111214689` | Sept 6 connected; destination action/ID not proven by inspected current packet. Repo template uses placeholders | **HOLD; conditional DISCONNECT** when fresh installed source identifies obsolete/duplicate action and the app replacement is verified. Saved source has a consent-branch concern; no unlawful dispatch was proven. |
| Google & YouTube app pixel | Sept 6 “Server Web” / optimized access observed; precise connected state and current destinations unverified | **KEEP app; preferred replacement sender.** Read linked product IDs and Manage tags/conversion mappings. Merchant/feed and tracking are separate capabilities. |
| GA4 → old Ads link | Sept 5 completed GA4 link to Ads `3990976848`; original account access unresolved | **PRESERVE history; HOLD link change.** Verify new link and goals before retiring obsolete linkage; do not delete historical account or conversion records. |
| `AW-18164235932` | Sept 4 tag-sharing email; customer/action ownership unknown | **HOLD.** Neither install nor remove from this ID alone; it is not a customer-account ID. |
| `G-T03LX978J0` | No source mapping in the inspected current/saved tracking evidence | **UNKNOWN.** Do not assume it is a replacement or the retained property's stream. |
| MAIN layout / analytics asset | Fresh API source as above | **KEEP.** Do not delete `dataLayer`, analytics asset or Shopify `content_for_header` as an “old tag.” |

Saved mapping: [purchase diagnosis](PURCHASE_CAPTURE_DIAGNOSIS_AND_REPAIR.md). Completed repair: [receipt](pixel_repair_execution.json), [independent review](pixel_repair_execution_review.md), [release](LIVE_PIXEL_AND_SUNSHINE_REPAIRS.md). Older “not saved” statements are superseded only for that exact helper repair.

**New identity leads are historical, not live truth.** A local September 8 17:30 history summary reports Shopify Merchant `5849297181` and Ads `4683483813` were connected, then the user disconnected Google Business Profile, Merchant and Ads; final captured Ads setup was incomplete. It reports Merchant access denied and an unrelated accessible `truehairwigs` Merchant `513542500`. The registry also contains `5849532286` as an earlier candidate. Exclude the unrelated account. Root/merchant lane must reconcile these candidates against the actual current connection UI before choosing any target. Provenance: `/Users/fsuels/.codex/memories/extensions/skysight/resources/2026-09-08T17-30-00-MJry-10min-memory-summary.md`, lines 13–40; registry `MEMORY.md`, Task 5 under paid-growth continuity. Note timestamps are approximate; this was not a fresh session replay.

## Proposed cutover and acceptance

1. Bind store, connected Google identity, Ads customer, Merchant account, GA4 property/stream and Google tag destinations from one current window. Capture settings before-state and exact rollback. No replacement GA4 property is justified merely because Ads is new.
2. Configure the app's exact Google destinations under root's current authority. Google supports one connected account per product type; manual tag migration is distinct from account linking. Prefer app-managed measurement because official guidance recommends it for Shopify checkout and warns about custom-pixel Google tagging limitations. This recommendation does not establish the cause of historical missing MP purchases. [Google migration guidance](https://support.google.com/analytics/answer/15642481?hl=en), [custom-pixel limitations](https://support.google.com/analytics/answer/16000892).
3. In a bounded transition, verify the app emitter then disconnect the exact superseded Google custom/tag senders; retain reversible configuration, no indefinite duplicate collection. Verify retained app receipt after each change. Preserve non-Google integrations and diagnostic-only code. Do not blindly execute the stale README Phase 3 native-pixel promotion/pause recipe. [Google duplicate removal](https://support.google.com/analytics/answer/16424072).
4. Required acceptance: one actual, authorized completed purchase must match privately across Shopify callback, selected sender, GA4 receiver and intended Ads action: nonempty stable `transaction_id`, actual `value`, explicit ISO currency and items. GA4 value must reconcile discounted merchandise; tax/shipping are separate. Confirm no second counted purchase on order-status revisit. No fabricated purchase, forced attribution ID, replay of old orders, or agent payment. A natural future order may supply proof. One order establishes a bounded journey, not complete coverage. [GA4 purchase specification](https://developers.google.com/analytics/devguides/collection/ga4/reference/events#purchase).
5. Verify page/product/cart/checkout paths and consent before/after grant and refusal, preserving the current privacy policy. Denied-consent behavior must match the intended consent mode, including any legitimate consent pings; do not infer all network requests must disappear. Confirm no unauthorized storage/user-data send. Audit banner-to-Shopify Customer Privacy integration. [Shopify migration checks](https://help.shopify.com/en/manual/promoting-marketing/pixels/pixel-migration).
6. Exactly one verified purchase action should own bidding for a sale. Check campaign/custom-goal overrides: a Secondary action in a custom goal can still be used for bidding. Do not assume transaction-ID dedup works across distinct actions. [Google primary/secondary rules](https://support.google.com/google-ads/answer/11461796?hl=en), [transaction IDs](https://support.google.com/google-ads/answer/6386790?hl=en).
7. A queued beacon, HTTP 2xx or validation success is not GA4 ingestion proof; debug validation events never enter reports. A GA4 purchase may have no Ads attribution without an eligible real ad interaction. Compare consistent timezone/window/currency and respect reporting delay. [MP transport](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference), [MP validation](https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events).
8. Refunds/cancellations and Ads conversion adjustments remain unproven; browser purchase tracking does not establish retained revenue/profit. Define their receiver reconciliation before treating gross platform ROAS as net performance. Preserve the existing private parity cohort; no new customer/order export was made.

Success remains profitable purchases at about 650% ROAS, not setup completion. CPA = spend / verified purchases; ROAS = comparable verified conversion value / spend; actual allowable CPA depends on verified basket costs and margin. Current paid purchases since yesterday, revenue, CPA and ROAS were **not refreshed** in this bounded inventory. No high-intent economics, anti-cannibalization or scale decision can be certified from tag activity.

## Handoff and checks

- `source_live_evidence_as_of: 2026-09-08 current session, completed by 18:08:33 UTC; Shopify source only`
- `live_state_mode: STALE_READBACK_REQUIRED` (full paid control; only the named Shopify sources were refreshed)
- `effective_approval_policy: CURRENT_OWNER_MIGRATION_INSTRUCTION_ROOT_INTEGRATION_REQUIRED`
- `approved_external_scope: NONE_FOR_THIS_READ_ONLY_SUBAGENT`
- `decision_depends_on_uncertain_state: true`
- `material_decision: MATERIAL`
- `decision_changing_evidence: exact current app/customer-event destinations and receiver purchase proof`
- `if_evidence_supports_recommendation: root may perform the reviewed bounded app cutover and retire proven duplicates under current authority`
- `if_evidence_opposes_recommendation: stop deletion, retain verified sender and revise exact destination mapping`
- `independent_verifier: root-assigned marketing safety reviewer; review pending`
- `verifier_independence: DID_NOT_BUILD_OR_EXECUTE`

Three connector validations passed; bundled skill validator passed for inventory query. The local docs-search script first failed from broken system Node, then fetch failed under bundled Node; official web docs supplied the independent fallback. API inventory was denied only at appInstallations; two independent source reads passed. `python3.13` was absent; bundled Python parsed the sanitized receipt and passed four scoped assertions plus whitespace/sensitive-query checks on all three artifacts. `git diff --check` exited 0 but does not cover these new untracked files; the explicit file checks do. No browser calls, setting edits, events, account connections or deletions occurred. Parent owns canonical state/worklog and final checks.

**One next action:** root obtains the current Google & YouTube connected-service and Manage tags/conversion mapping, because it selects the correct replacement accounts and distinguishes obsolete senders from the retained GA4 history.

Continuation: use [canonical prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md), latest relevant anchor `2026-09-07-ceo-turnaround-meow-search-identity` plus this current inventory and root's newer integration anchor, if created.
