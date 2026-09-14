# Microsoft Shopify app tracking — support request draft

Status: LOCAL DRAFT, NOT SENT. No customer/order identifiers, authentication material or browser cookies are included. Refresh the exact installed version before submitting this as a current defect report.

Subject: Shopify UET36005151 — supported click-ID cookie repair and regional consent validation

Our Dress Like Mommy Shopify store uses Microsoft Advertising account477439/customer770182 and UET36005151 through strict app pixel931561569, client2997493. Please confirm the supported app update path and how to inspect consent acceptance for its proprietary shop-wpa event stream.

In the deployed bundle inspected September9,2026, version5ee93563fe31b11d2d65e2f09a5229dc, updateMsclkid includes expiry text in the cookie-name argument. An isolated reproduction of the installed setter produced a malformed assignment of the form msclkid; expires=<date>=<clickid>. A separate90-day localStorage fallback is present, so we have not established actual attribution loss. Please confirm whether the currently supported app release has corrected this and which release/version should be installed. The inspected source SHA256 is bdf85b114cb9d9ef5c790dee198f38dd8032c46bc13bdf7ca9f4ee034abc7f29.

The September11 seven-day regional diagnostics showed pageview consent-signal coverage27% and view_item0%; purchase Healthy explicitly had no EEA/UK/Switzerland sample. These dated observations do not prove a current regional purchase failure. Please provide the supported validation method for Page Load, product and purchase events from shop-wpa, including how Shopify permission grants and revocations reach the Microsoft receiver. We want to preserve the declared analytics/marketing/sale-of-data requirements and avoid duplicate event senders or unconditional consent.

The inspected purchase publisher maps checkout subtotal and currency to purchase-event value/currency. We need to verify those received values, retained click attribution and behavior if the checkout callback repeats, using a genuine order and privacy-appropriate identifiers. Please identify the supported diagnostic path rather than requiring an unsupported worker edit.

The Shopify Microsoft app/home returned technical loading errors during the September11 check, after its normal retry and safe home fallback. No authentication or source-specific cause is established. Microsoft Ads remains authenticated; the two newly prepared U.S./German campaigns are Paused pending measurement and launch qualification.

Evidence available: dated public configuration and source receipts, isolated setter/purchase fixtures, native regional diagnostic readback, and exact saved goal configuration. A redacted trace can be supplied after a permitted genuine session produces the relevant events. We have not placed a test order or sent customer data with this draft.

## Local references

- [Independent source findings](../microsoft_tracking_independent_review.md)
- [Consent assessment](../microsoft_consent_assessment.md)
- [Regional diagnostic interpretation](../receiver-20260911-1930/consent_diagnostic_independent_review.json)
- [Current saved campaign checkpoint](READBACK.md)
