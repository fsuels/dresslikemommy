# Microsoft purchase tracking audit

September22,2026. Confidence:H for observed configuration and order/report facts; M for attribution diagnosis. Overall outcome: PARTIAL — purchase collection works for observed GA4 orders; Microsoft end-to-end paid-purchase attribution is not certified.

## What the sales evidence shows

| Order date, New York | Shopify value | Shopify journey | Matched GA4 purchase value | GA4 attribution |
|---|---:|---|---:|---|
| Sep18 | USD64.98 | Direct | USD64.98 | Direct |
| Sep19 | USD66.98 | Direct | USD66.98 | Direct |
| Sep22 | AUD96.00 / USD68.20 shop money | Google SEO | USD68.36 | Data not available |

All three distinct Shopify order IDs were reconciled to GA4 transaction IDs privately using independently computed full-ID fingerprints and equal lengths. No raw identifiers are saved. Orders are PAID/non-test/noncancelled and all query pages exhausted. Shopify cutoff14:01:52UTC. GA4 reporting is intraday plus daily, with missing/unprocessed attribution warning. Today's Google-origin purchase has arrived but its GA4 source is not yet resolved; this may change during processing. The USD0.16 value discrepancy is verified; FX timing is a possible explanation, not a proved cause.

For the user's Sep19–22 window:2Shopify orders/USD135.18; Microsoft174clicks/USD23.60 spend/0reported purchases/0reported revenue. For the extended Sep17–22 first-click window:3orders/USD200.16; Microsoft211clicks/USD28.04; GA4160bing/cpc sessions with0purchase revenue. These are overlapping windows. Do not compute Microsoft ROAS from all-store sales.

None of the captured Shopify journeys has Microsoft UTMs or msclkid. Direct attribution cannot rule out prior Microsoft influence, cross-device traffic or tracking loss. The current evidence therefore neither proves Microsoft generated these sales nor proves that its zero is correct.

## What passed and what remains open

Verified: GA4 received all three identified recent purchases; GA4 records bing/cpc traffic; Microsoft UET is active and receives purchase events; purchase action/tag/value/count/window settings match; MSCLKID and UTM auto-tagging are enabled. Microsoft receives3purchase events Sep17–22 and2Sep19–22, but no order-level receiver join is available.

Open defects/limits:

1. The installed Microsoft Shopify publisher still contains the malformed click-ID cookie-setting call. Its90day localStorage fallback means actual attribution loss is not established. This app-managed bundle cannot be repaired by editing its downloaded copy or adding a theme snippet.
2. Native regional checkout/product/cart consent diagnostics remain Missing; begin_checkout has0%signal presence in its rolling7day regional sample. Purchase Healthy merely has no regional sample. A historical denied-session standard-page defect is documented; current source/aggregate evidence does not prove isolated purchase-sandbox failure.
3. Exact Microsoft purchase value/currency/order identity and deduplication are unverified. The app sends checkout subtotal in checkout currency; newest order should be checked against AUD96.00, not assumed USD68.20.
4. Shopify connector cannot read the app-pixel object without read_pixels; no scope expansion attempted. Public deployed source was freshly verified independently.

## Concrete next action

Request a supported correction and precise receiver diagnostics from Microsoft on existing case7108824779, using SUPPORT_ADDENDUM.md. This is the narrow next step because the unresolved source is publisher-managed and no safe corrective goal setting was found. An earlier custom replacement failed cross-tab duplicate/reservation tests and must not be deployed. Support contact is not yet authorized in this task; draft is LOCAL_NOT_SENT.

Acceptance after a supported correction: inspect granted/denied/withdrawn standard-page and app-pixel consent, follow one genuine consented Microsoft-attributed order from legitimate click ID to checkout, verify exactly one purchase with its subtotal/currency/items, and read back the Microsoft conversion/revenue after reporting latency. No fabricated click ID or historical purchase replay. A paid test purchase or privacy/data-sharing expansion requires its own explicit scope and user-performed payment.

No live settings were changed. Files in this packet are audit artifacts only. Existing shared canonical and account owners remain unchanged; this packet is an integration handoff for TA-15 / PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH, not a competing action queue.

## Evidence

- MICROSOFT_READBACK.md: live native goal/tagging/report/consent evidence.
- SHOPIFY_READBACK.md: schema-validated live order/journey read and reconciliation.
- GA4_READBACK.md: live acquisition, transactions, property timezone/currency and processing limitations.
- SOURCE_REFRESH.md and public_source_refresh.json: unchanged installed publisher source.
- Microsoft primary documentation: [UET and goals](https://learn.microsoft.com/en-us/advertising/guides/universal-event-tracking?view=bingads-13), [UET field and MSCLKID definitions](https://github.com/MicrosoftDocs/Advertising/blob/main/advertising/msa-help/hlp_BA_CONC_UET_FAQ_2.md). Receiving an event and attributing an ad conversion are separate checks.

## Continuity and review

task_stage: HANDOFF
next_action_id: READ_ONLY_MARKETING_RECONCILIATION
authority_context: CURRENT_USER_READ_ONLY_DIAGNOSIS; EXTERNAL_SCOPE_NONE
source_live_evidence_as_of: 2026-09-22T14:10:00Z (approximate end of Microsoft observations; source-specific clocks retained above)
live_state_mode: STALE_READBACK_REQUIRED (inherited command-layer control; this narrow audit does not refresh global paid authority)
effective_approval_policy: FRESH_ACTION_TIME_APPROVAL_REQUIRED
approved_external_scope: NONE
decision_depends_on_uncertain_state: true
material_decision: NOT_MATERIAL — diagnosis and unsent support draft only; no paid/status/privacy/conversion change proposed for execution.
decision_changing_evidence: Exact Microsoft receiver order/currency/legitimate-click trace or supported corrected publisher release.
if_evidence_supports_recommendation: Obtain correction and run the acceptance checks; do not claim success at submission.
if_evidence_opposes_recommendation: Preserve correct publisher settings, investigate processing or actual attribution source rather than duplicating senders.
independent_verifier: /root/audit_verifier — PASS_WITH_GATES / evidence PASS_WITH_LIMITS.
verifier_independence: DID_NOT_BUILD_OR_EXECUTE

Continue through the existing [canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md); retain this dated audit and existing TA-15 owner. No shared chronology/control edits were made because another active parent holds their sole write claim.

Verification: bundled Python strict continuity check returned CONTINUITY_OK; scoped git diff --check passed. No code behavior was changed, so software regression tests were not applicable. These checks validate repository continuity, not tracking operation.

Independent review found no substantive arithmetic or attribution correction. It reviewed retained summaries/source consistency, not fresh live replay; private full-ID reconciliation cannot be rerun from these sanitized artifacts. Source-specific cutoffs and processing differ. Existing TA-15 ownership and separate campaign pause/budget decisions remain unchanged.
