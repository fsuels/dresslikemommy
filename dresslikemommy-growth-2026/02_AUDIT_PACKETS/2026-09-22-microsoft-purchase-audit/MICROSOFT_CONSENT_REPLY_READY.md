# Consent questions — reply draft

Status: DRAFT_NOT_SENT. Based on the user's pasted Microsoft email, the September 12 saved storefront consent trace and September 22 audit. No fresh consent-transition test was run for this reply. No Tag Helper screenshot pair exists in the reviewed evidence. The token-bearing file-transfer link was neither opened nor stored. Existing case 7108824779 and follow-up reference 7109193190 require linkage clarification.

## Email body

Subject: Consent evidence — case 7108824779 / reference 7109193190

Hello,

Thank you for reviewing the update. Here are the answers based on the tests completed so far:

1. **Default consent configuration:** I cannot currently confirm that `ad_storage: denied` is initialized before `bat.js` on every page. The Microsoft publisher wrapper inspected on September 12 loaded `bat.js` and queued a page-load event without an explicit consent-default command in that wrapper. We have not verified whether another component sets consent earlier across all pages.

2. **Shopify Customer Privacy API:** The API returned effective analytics and marketing permissions of `false` before and after a reload in the September 12 test (region USFL). However, correct propagation of those permissions and subsequent changes to UET is not verified. The app bundle audited again on September 22 had no explicit consent-update handling or `visitorConsentCollected` subscription. Shopify's app-pixel permission requirements are configured, but those requirements alone do not establish that Microsoft receives the correct consent signal. See [Shopify's pixel privacy documentation](https://shopify.dev/docs/api/web-pixels-api/pixel-privacy).

3. **UET Tag Helper results:** We do not currently have a completed Tag Helper test or screenshots demonstrating both `asc=denied` and `asc=granted`. The evidence we do have is from Microsoft's native **Test your tag** and a browser network trace: on September 12, the receiver showed three page-load events with **Consent Signal: Not present**. At 10:43:06.879 UTC, a standard `/action/0` page-load request for UET 36005151 had no `asc` parameter while Shopify's analytics and marketing permissions were false. This was a historical storefront-page test, not verification of the separate purchase-pixel stream.

Please identify the supported setup required for the installed Microsoft Shopify integration to pass consent correctly for both the storefront tag and the app purchase pixel, and the test procedure for each. Please also confirm the expected pre-consent behavior for this integration: your [consent documentation](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_uet_consent) allows either no events before consent or events with denied consent, depending on the implementation.

Finally, your email refers to existing case **7108824779**, while the upload link and final reference use **7109193190**. Please confirm that these references are linked and that evidence uploaded under 7109193190 will be included in the original investigation.

Thank you,
Francisco

## Internal evidence

- `../2026-09-09-microsoft-ads-rebuild/heartbeat-20260912-1038/receiver_consent_trace.json`: dated permissions, standard request and native receiver evidence; scope and capture limitations retained.
- `../2026-09-09-microsoft-ads-rebuild/heartbeat-20260912-1038/support_request_ready.md`: observed publisher-wrapper source limitations.
- `SOURCE_REFRESH.md` and `technical_review_01a0c97b.md`: September 22 app-source identity and bounded consent findings.
- Microsoft and Shopify official documentation reread for the distinction between pixel loading permissions, consent transmission and Basic/Advanced validation. No support contact, file upload, tracking deployment or consent setting change occurred in this reply-drafting step.
