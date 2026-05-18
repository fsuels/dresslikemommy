# Shopify Customer Events Native Ads Diagnostic Fix Packet

Date: 2026-05-18

Status: `OWNER_APPROVAL_REQUIRED_BEFORE_SHOPIFY_CUSTOMER_EVENTS_EDIT`

## Why this packet exists

Shopify order `#9494` proved the prepared checkout completed, and Google Ads readbacks proved the native action is configured correctly. Google Ads still shows no native purchase entry for the order-day window, so the next valid repair lane is Shopify Customer Events execution:

- Did `checkout_completed` arrive inside the native Ads custom pixel?
- Did the Shopify Customer Privacy state allow the pixel to fire?
- Did the installed code actually attempt the native `googleadservices.com/pagead/conversion/...` request with `value`, `currency`, `oid`, and `transaction_id`?

This packet prepares the smallest live Shopify Customer Events edit that can answer those questions.

## Current evidence

- Shopify Admin read-only order readback confirmed paid order `#9494`, total `$15.99 USD`, product `Matching Mommy & Me Two Piece Swimsuit`, variant `Child 2-3 years / Black`, quantity `1`.
- Google Ads native conversion action `7612074463`, `Purchase - Shopify Custom Pixel native`, remains `ENABLED`, `WEBPAGE`, `PURCHASE`, `primaryForGoal: true`, and `includeInConversionsMetric: true`.
- Google Ads API returned `0` native action rows for `2026-05-17` through `2026-05-18`.
- Google Ads UI Webpages/Diagnostics for the native action still showed no entries.
- A separate-browser replay of the order-status URL redirects to the storefront home and is not valid purchase proof.

## Prepared local code change

The tracked template `pixels/google-ads-custom-pixel.js` now includes:

- A sanitized `checkout_completed received` diagnostic log emitted before the consent gate.
- A structured consent decision with `consentAllowed`, `consentReason`, and privacy flags.
- A privacy fallback that trusts Shopify's pixel-level permission gate only when `init.customerPrivacy` / `api.customerPrivacy` is unavailable or missing flags. Explicit `marketingAllowed: false` still blocks firing.
- Sanitized conversion-attempt logs that do not print the conversion label, full conversion URL, click IDs, checkout token, email, phone, or address.
- A same-URL image backup beacon after the `fetch(..., { mode: "no-cors", credentials: "include", keepalive: true })` request. Both requests carry the same `oid` / `transaction_id` so Google Ads can dedupe duplicate fires inside the same conversion action.

## Exact approval phrase

Owner must approve this exact phrase before any live Shopify Customer Events edit:

`I approve updating only the Shopify Customer Events custom pixel named DLM Google Ads native conv with the prepared diagnostic/fix code from pixels/google-ads-custom-pixel.js. Do not change any other Shopify setting, product, theme, app pixel, Google Ads setting, GA4/GTM setting, Merchant/Pinterest/feed/campaign/budget/bid/status, billing, order, refund, or cancelation state.`

## Live execution steps after approval

1. Open the existing authenticated Shopify Admin tab.
2. Go to `Settings -> Customer events -> Custom pixels`.
3. Open `DLM Google Ads native conv`.
4. Copy the current live pixel code to a non-repo temporary backup. Do not write real conversion labels into tracked files.
5. Paste the prepared code from `pixels/google-ads-custom-pixel.js`.
6. Replace only:
   - `__AW_CONVERSION_ID__`
   - `__AW_CONVERSION_LABEL__`
7. Save.
8. Confirm the pixel remains `Connected`.
9. Do not edit any other custom pixel or app pixel.

## Verification plan

### No-charge verification

1. Use Shopify Pixel Helper/Test on `DLM Google Ads native conv`.
2. Confirm `page_viewed` is received and the callback succeeds.
3. Open browser console and confirm sanitized logs:
   - `[DLM Ads Pixel] subscribed to Shopify page_viewed + checkout_completed`
   - `[DLM Ads Pixel] page_viewed received`
4. Confirm there is no raw conversion label, full conversion URL, checkout token, email, phone, or address in console output.

### Owner-performed checkout verification

1. Owner performs any real payment/order step. Automation must not click Pay, place an order, refund, or cancel.
2. On the thank-you/order-status page, inspect Network for:
   - `googleadservices.com/pagead/conversion/<native-id>/...`
   - `label` present but not copied into repo notes
   - `value`
   - `currency` or `currency_code`
   - `oid`
   - `transaction_id`
3. Inspect console for:
   - `[DLM Ads Pixel] checkout_completed received`
   - `consentAllowed: true`
   - `consentReason`
   - `[DLM Ads Pixel] firing conversion`
   - `[DLM Ads Pixel] firing image backup beacon`
4. If `checkout_completed received` is absent, the issue is Shopify event delivery or the pixel not running on the completion surface.
5. If `checkout_completed received` is present but `consentAllowed` is false, the issue is Customer Privacy configuration/consent.
6. If `firing conversion` appears but the Network request is absent, the issue is sandbox transport/CSP/request dispatch.
7. If the Network request appears with purchase fields, the remaining issue is Google Ads diagnostics/attribution/readback timing.

## Stop conditions

Stop immediately if any of these appear:

- Shopify asks to disconnect/reconnect the Google & YouTube sales channel.
- Shopify prompts for destructive changes outside the named custom pixel.
- The editor shows a different pixel than `DLM Google Ads native conv`.
- The live code lacks the real Ads ID/label and the real values cannot be safely recovered from the existing editor or local non-repo copy.
- Google Ads, GA4, Merchant, Pinterest, billing, product, theme, feed, campaign, budget, bid, status, order, refund, or cancel actions are requested by the UI.

## Rollback

If the diagnostic/fix code causes unexpected behavior:

1. Reopen `DLM Google Ads native conv`.
2. Paste the non-repo temporary backup captured before the edit.
3. Save.
4. Confirm the pixel remains `Connected`.
5. Record before/after state and stop.

## References

- Shopify Web Pixels `checkout_completed` docs: https://shopify.dev/docs/api/web-pixels-api/standard-events/checkout_completed
- Shopify Web Pixels `customerPrivacy` docs: https://shopify.dev/docs/api/web-pixels-api//standard-api/customerprivacy
- Shopify custom pixel code and consent docs: https://help.shopify.com/en/manual/promoting-marketing/pixels/custom-pixels/code
- Shopify custom pixel testing docs: https://help.shopify.com/en/manual/promoting-marketing/pixels/custom-pixels/testing
