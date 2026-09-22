# Microsoft purchase tracking audit — current-task verification

September 22, 2026. Task 01a0c97b-e223-72b0-898d-185234f116b4.
Confidence: H for inspected settings and reports; M for diagnosis of missing attribution.
Outcome: PARTIAL. Purchase events are reaching Microsoft, but exact order/value/currency, deduplication and paid-click attribution are not certified. No production repair or support message was sent.

## What passed

Fresh native reads in this task's in-app browser (browser 2, user tabs 1 Microsoft, 2 Shopify, 3 GA4) confirmed account477439/customer770182, store dresslikemommy-com, and GA4 property330266838.

All nine current nondeleted campaigns use the checked account-default conversion setting and exactly one selected Purchase goal: ShopifyCheckoutCompleteEventTracking. Six were Enabled and three Paused in the current campaign table. No campaign-level override was found. Advanced URL options show no settings applied in all nine; Canada additionally had blank tracking-template and final-suffix fields when expanded. Ad/ad-group/keyword URL overrides were not exhaustively inspected.

| Campaign | ID | Observed status | Purchase goal selection |
|---|---|---|---|
| US English | 506254907 | Enabled | Account default, one Purchase goal |
| Canada English | 506255071 | Enabled | Account default, one Purchase goal |
| Europe English | 506255284 | Enabled | Account default, one Purchase goal |
| UK English | 506255081 | Enabled | Account default, one Purchase goal |
| Australia English | 506255076 | Enabled | Account default, one Purchase goal |
| Latinos Spanish | 506255080 | Enabled | Account default, one Purchase goal |
| Germany German | 506254908 | Paused | Account default, one Purchase goal |
| Netherlands Dutch | 506255078 | Paused | Account default, one Purchase goal |
| France and Canada French | 506255077 | Paused | Account default, one Purchase goal |

The purchase goal uses Action Equals purchase, ShopifyImport UET36005151, variable value with USD0 fallback, Count All, 30-day click window, 1-day view-through window, Last click attribution, and auto-bidding inclusion Yes. Legacy destination-URL purchases and add-to-cart remain excluded from primary bidding/conversion metrics. No field was edited or saved in the goal editor; Cancel closed it.

Account settings freshly show MSCLKID auto-tagging and UTM auto-tagging checked, Replace all existing tags selected, and blank account tracking template/final URL suffix. The reporting view already includes Spend, Revenue, Conversions, CPA and ROAS.

Shopify's native Microsoft Channel pixel page shows Web, Optimized selected and Access on; its visible activity log contains June2 data access granted. Declared permission requires analytics and marketing and respects data-sale opt-out. No privacy setting was changed. This replaces the earlier connector-only pixel visibility limitation for these native fields; it does not grant read_pixels or prove runtime consent.

## Current result windows

At approximately 14:18 UTC, Microsoft campaign report for September19–22 Eastern displayed 175 clicks, USD23.74 spend, 8,488 impressions, zero attributed conversions and zero reported revenue. Search totals: 51 clicks/USD6.10; Audience:124/USD17.64. September22 is partial; these are a dated snapshot, not frozen current totals.

The UET receiver for September19–22 displayed two Custom purchase events, with GoalValue, Currency, PageType and ProductId parameter names. No actual per-event values or order identifier were exposed. The earlier same-day packet documented three receiver purchases in the overlapping September17–22 window; that wider receiver count was not reread here. Do not join orders and receiver hits by count.

Fresh Shopify read through 14:22:01UTC (10:22:01EDT) returns the same three qualifying PAID/non-test/noncancelled orders since September17, with exhausted order and journey pagination:

| Order creation | Shopify subtotal/total USD | Checkout amount/currency | Recorded Shopify source |
|---|---:|---|---|
| September18 | 64.98 | USD64.98 | Direct |
| September19 | 66.98 | USD66.98 | Direct |
| September22 | 68.20 | AUD96.00 | Google / SEO |

Total USD200.16. No refunds recorded. No captured order journey contains UTMs, msclkid or gclid. Direct is unresolved and cannot establish or exclude earlier Microsoft influence.

Fresh GA4 September17–22 read at approximately14:28–14:30UTC shows 160 bing/cpc sessions with zero purchase key events/revenue. The Transactions report shows three transaction rows, one ecommerce purchase per row: USD64.98 and USD66.98 Direct, USD68.36 data-not-available. Total USD200.32. The earlier same-day packet independently matched full Shopify and GA4 identifiers; this refresh reread rows/amounts/source but did not redo that private identifier join. The USD0.16 newest-order difference is real; FX timing is possible, not proven. Current-day attribution remains provisional. The purchase metric was explicitly selected; other key events are not sales.

## Proven defect and unresolved verification

1. Independent public-source fetch at14:21:26UTC confirmed the installed publisher is byte-identical to the earlier audited version (8,917 bytes; SHA256 bdf85b114cb9d9ef5c790dee198f38dd8032c46bc13bdf7ca9f4ee034abc7f29). Its click-ID cookie API call incorrectly includes expiry text in the cookie-name argument. A90-day localStorage fallback exists, so actual ad-credit loss has not been established.
2. Current UET begin_checkout consent tooltip reports0% signal presence in its rolling7day EEA/UK/Switzerland sample; product and cart show Missing. Purchase Healthy explicitly says no regional sample. Neither signal presence nor this label certifies correct consent handling.
3. Installed purchase code sends Shopify checkout subtotal and matching currency. It does not send explicit order identity or full item price/quantity details. Optional field absence alone does not explain zero conversions, but this UI cannot establish exact amount acceptance or single delivery. Subtotal differs from full payment when shipping/tax/duties apply; they happen to agree in this three-order cohort.
4. The old custom replacement was independently retested and still fails two cross-tab counterexamples. No duplicate sender or historical purchase replay was introduced.

## Recommended next action and concrete acceptance

Use the prepared [support update](SUPPORT_UPDATE_READY.md) on existing Microsoft case7108824779 to obtain a supported publisher correction and receiver diagnostics. LOCAL_NOT_SENT. No customer details, click identifiers, credentials, attachments, new case, or account-change authorization are included. The current task does not explicitly authorize sending this message. Prior source-owner support authority is not silently transferred.

A supported correction must be read back by source/version, then verified against one genuine eligible Microsoft click and order: exactly one purchase, agreed subtotal-or-total definition, matching currency, item data as supported, goal credit, and reported revenue after latency. Standard-page and app-purchase consent must be tested separately across appropriate states. No fabricated click ID, paid self-click, synthetic live purchase or historical event replay. The user would perform any payment under a separately scoped test.

No configuration toggle found in this audit repairs publisher-managed code. A documented Microsoft custom-pixel alternative exists, but requires a reviewed replacement/cutover; adding it alongside the current app is not an accepted fix.

## Scope, operational notes and handoff

Only subordinate audit artifacts were added. Other owners retain Microsoft account and shared-canonical write claims. No campaign Save, app change, tracking deployment, consent expansion, support message, spend/status/bid change or order action occurred.

During the final campaign-settings exit, Cancel displayed an unexpected unsaved-changes prompt despite no form-field edits. A subsequent navigation already queued in the same tool invocation reached account settings; no Save or confirmation button was clicked. The prompt was gone on readback. The warning cause is UNKNOWN; no browser-side draft preservation is asserted. Future work must stop immediately on such a warning. This procedural limitation is retained separately from the observed saved settings.

The task reused only its three assigned IAB tabs. No personal-browser page was controlled. Source-specific dates and clocks remain separate. This packet is a handoff to existing TA-15 / PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH; it does not replace the shared worklog, problem tracker, cockpit or action queue, whose active parent retains sole ownership.

task_stage: HANDOFF
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
authority_context: CURRENT_USER_TRACKING_DIAGNOSIS; NO_SUPPORT_SEND_AUTHORIZATION
live_state_mode: STALE_READBACK_REQUIRED
effective_approval_policy: FRESH_ACTION_TIME_APPROVAL_REQUIRED
approved_external_scope: NONE
autonomous_action_ready: false
decision_depends_on_uncertain_state: true
material_decision: NOT_MATERIAL — read-only diagnosis and unsent technical message.
decision_changing_evidence: Exact legitimate-click/order/value receiver trace, current supported publisher correction, or a contrary source-attribution receipt.
if_evidence_supports_recommendation: Obtain supported correction and verify end to end; support submission alone is not completion.
if_evidence_opposes_recommendation: Preserve correct settings and investigate actual source/processing without duplicating senders.
independent_verifier: /root/publisher_review — PASS_WITH_LIMITS for code and final saved-evidence review; no independent live replay or new private transaction-ID join.
verifier_independence: DID_NOT_BUILD_OR_EXECUTE

Evidence: [technical review](technical_review_01a0c97b.md), [fresh orders](order_refresh_01a0c97b.md), [earlier same-day audit](REPORT.md), native observations in this task.
Final independent review: [verdict](final_review_01a0c97b.md). Strict continuity returned CONTINUITY_OK with all10 checks passing. These repository checks do not validate tracking operation. The ready support update remains unsent; an exact send-authorization question is pending in the current task.
Continuation: use the [canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md) with this packet and existing TA-15 owner.

Official sources: [Microsoft event fields](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_uet_parameters_table), [Shopify cookie API](https://shopify.dev/docs/api/web-pixels-api/standard-api/browser), [Microsoft Shopify implementation](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_proc_uet_webplatform_shopify), [Microsoft attribution mechanics](https://github.com/MicrosoftDocs/Advertising/blob/main/advertising/msa-help/hlp_BA_CONC_UETv2HowCTWorks.md).

## September 22 support-send continuation

The user subsequently explicitly authorized the prepared update for existing case 7108824779. The earlier `NO_SUPPORT_SEND_AUTHORIZATION`, unsent and permission-pending statements above describe the audit's earlier closeout, not this continuation. The approved six-paragraph message was sent once to the authenticated Microsoft live-support chat at 10:42–10:43 AM EDT. Support agent Abdul-Karmel Duba replied and read back the exact case/account/tag scope. At 10:53 AM he requested Francisco directly because he recognized AI assistance. The assistant disclosed its role, requested that the chat remain open, and handed it to the owner. Status: SENT_TO_HUMAN_SUPPORT; CASE_ATTACHMENT_BLOCKED_PENDING_OWNER_HANDOFF. No case-save confirmation, correction, release date or next update time was provided. Current receipt and exact next action: [SUPPORT_SEND_RECEIPT.md](SUPPORT_SEND_RECEIPT.md). This narrow communication authorization does not authorize any business settings changes, transfer another task's platform/canonical claim, or establish that tracking is repaired. Do not resend the six parts or duplicate the case.
