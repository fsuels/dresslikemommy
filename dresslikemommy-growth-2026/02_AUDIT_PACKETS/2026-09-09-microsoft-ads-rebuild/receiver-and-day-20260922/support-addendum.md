# Prepared addendum for existing Microsoft case 7108824779

Status: **LOCAL — NOT SENT**. This supplements the diagnostic already acknowledged on September 14. It is not a new support case or authorization to change the account, app, tracking, consent or campaigns. Use only the existing authenticated case channel when available; do not retry the unchanged September 21 mailbox mismatch or failed human connection.

Prepared message:

> Please add this September 22 native readback to existing service request 7108824779 for account 477439, UET 36005151 (ShopifyImport). Please preserve the existing case and diagnostic.
>
> During the 08:25–08:28 UTC readback, the UET interface showed Consent: Need Attention. The rolling seven-day EEA/UK/Switzerland diagnostics report a consent signal on 25% of page-view events and 0% of begin_checkout, add_to_cart and view_item events. Population counts are not exposed, and other regions are excluded.
>
> A Custom purchase event is received in September 22's partial day. The parameter popup lists GoalValue, Currency, PageType and ProductId, but exposes no exact values or order identity. The purchase Healthy tooltip explicitly says no EEA/UK/Switzerland events were detected. It therefore does not establish regional purchase-consent correctness.
>
> The current primary goal ShopifyCheckoutCompleteEventTracking is bound to ShopifyImport/UET 36005151 and action Equals to purchase, with variable value, USD 0.00 fallback, Count All, a 30-day click window and Last click attribution. It still shows No recent conversions. These settings were read without changes; recent reporting latency remains possible.
>
> Please provide the team's current investigation status, any supported publisher correction for the installed Shopify integration, and a way to verify standard-page and app purchase consent, a single purchase sender, exact order value/currency/items and receiver deduplication. The earlier standard denied-session defect remains the demonstrated test; an isolated app-purchase defect is not proved by these aggregate diagnostics. Please confirm whether engineering has accepted an escalation and the next update time. No account, consent, app, tracking or campaign change is authorized by this status request.

Source: [source.json](source.json). No order/customer PII, authentication material or attachment is included. This draft does not claim an email response, a support repair, or a new send.
