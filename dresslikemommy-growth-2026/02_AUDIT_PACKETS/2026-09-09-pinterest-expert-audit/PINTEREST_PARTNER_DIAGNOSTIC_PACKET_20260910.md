# Pinterest managed-integration diagnostic packet

Prepared September 10, 2026. **DRAFT — NOT SENT.** No support conversation, permission request, pixel change, or synthetic platform event was created. This packet records a receiving-data discrepancy; it does not establish a Pinterest or Shopify software defect.

## Observed discrepancy

The correct Dress Like Mommy advertiser's Event Quality screen, updated September 9, rates both Tag and Conversions API Web **Fair** in the one-day and fourteen-day views inspected. In the fourteen-day CAPI view, Product ID coverage is **0% for AddPaymentInfo**, while Checkout, AddToCart, and InitiateCheckout are **100%**. PageVisit is **28%** and marked good health. Coverage does not establish a successful catalog match.

Click ID coverage is **0% for all seven displayed CAPI event types**. Email coverage is 5% for AddToCart and 57% for AddPaymentInfo. These percentages do not prove a configuration defect: traffic without a genuine Pinterest click ID or available customer identifier can legitimately lack those fields. The completed organic Pin's actual Visit site route retained all four UTMs but contained no `epik`; it cannot test click-ID capture.

The sole visible active tag already has automatic enhanced match enabled, with all displayed options selected. A generic enrollment banner contradicts the actual enabled setting and should not trigger another enrollment or installation.

## Source evidence and limits

The current captured Shopify Pinterest app script contains a `payment_info_submitted` → `AddPaymentInfo` mapping and derives product IDs from checkout line-item variants. Eleven extracted-handler fixture assertions passed. The browser source also reads genuine URL `epik`, requests cookie/storage retention, and forwards browser `pd.epik`. Source presence and isolated fixtures do not prove successful event delivery or the partner's server-side forwarding.

Shopify permits a nullable checkout-line-item variant. That is a possible missing-product-ID input, not an observed explanation for this account. The source does not expose the managed CAPI implementation. The absence of literal `click_id` in browser code does not prove a missing CAPI field.

## September10 planned supported test (inspection completed September11)

This September10 plan was executed for Test/permissions/privacy on September11; its full acceptance remains gated as recorded below. The plan was to open the existing Shopify Pinterest app pixel under **Settings → Customer events** and inspect **Test**, **View permissions**, and **View customer privacy** as available. Preserve the existing settings. Capture only event names, timestamp/window, whether a product ID is present, whether a genuine click identifier is present, callback errors, and consent state. Do not retain customer values, tokens, cookies, full event payloads, payment details, or signed feed links.

Compare Tag and CAPI for the same event type and reporting window; explicitly read Tag AddPaymentInfo Product ID coverage, which remains unverified. A natural, properly consented customer event is required for purchase/order/deduplication proof. Do not submit payment, manufacture an order, invent identifiers, or install another sender for the test.

If a corresponding valid browser event contains a product ID while the receiving CAPI event lacks it, ask the integration provider which supported repair addresses that observed mismatch. Also ask how the managed integration preserves genuine Pinterest click IDs through the Shopify customer journey. There is no reviewed merchant-facing CAPI field-mapping editor in the currently available documentation. The connector's missing read scopes do not establish missing permissions in the installed app.

## Acceptance criteria

- Supported diagnostics identify the cause or the provider confirms the mapping behavior and remediation.
- The exact changed setting or implementation is read back; event receipt is checked after the platform's reporting refresh.
- Product-ID coverage and actual catalog matching are evaluated separately.
- A genuine completed order is counted once, with matching identity, quantities, discounts, purchased-item value, and currency; browser/server deduplication is established.
- Consent refusal/revocation and genuine click continuity are checked without fabricated customer data.

September10 checkpoint: **MANAGED_INTEGRATION_DIAGNOSIS_REQUIRED**. The then-current native click failure was not evidence of authentication or missing permissions. The September11 checkpoint below supersedes that access state.

Evidence: [native health](NATIVE_HEALTH_20260910.json), [independent source review](TRACKING_MAPPING_REVIEW_20260910.md), [organic click receipt](SUNSHINE_EXECUTION_20260910.json).

Documentation: [Shopify app-pixel diagnostics](https://help.shopify.com/en/manual/promoting-marketing/pixels/app-pixels), [Shopify payment event schema](https://shopify.dev/docs/api/web-pixels-api/standard-events/payment_info_submitted), [Pinterest CAPI fields](https://developers.pinterest.com/docs/track-conversions/track-conversions-in-the-api/), [Pinterest enhanced match](https://help.pinterest.com/en/business/article/enhanced-match).


## September 11 supported-test update

**Still DRAFT — NOT SENT.** Native Customer events inspection confirms the installed Pinterest app is Connected with Server/Web, Always on data access, marketing+analytics required purposes and sale-opt-out exclusion. No permission or setting was changed. Official Pixel Helper launched successfully after scoped Computer Use recovery. Green page_viewed and product_viewed dots establish local callback success; product input includes the expected Sunshine IDs,21.99USD, and product/vendor/type fields. This is not the payment event or Pinterest CAPI receipt.

Consent acceptance remains **CONFLICTED**. After Decline, fresh product navigation initially showed Pixel is awaiting consent. Automatic review rejected Give consent; it was not retried. Later Loaded/green callbacks were observed without a verified consent transition. Two user-changed-app interruptions then stopped native work; test tab remains open, cart0 last verified, final stored choice unknown and cleanup incomplete. Do not present refusal/revocation as passed, the rejected click as executed, or any receiver-side defect as established.

Next exact test, only after explicit temporary test-consent approval and stable native access: verify a visible path back to Decline first; inspect the Shopify helper for this existing Pinterest pixel with ordinary page/product actions, then restore Decline and verify the settled reload. Capture only non-personal field presence and status. If Shopify's consent control affects other installed pixels, disclose that scope before granting; do not change privacy configuration or manufacture events. Separately read Tag14d AddPaymentInfo Product ID coverage against the same-window CAPI metric. Neither a helper green dot nor a subsequent source read substitutes for receiving-side proof.

Evidence: [September11 receipt](SHOPIFY_PIXEL_NATIVE_20260911.json), [independent documented helper meanings](PIXEL_HELPER_INTERPRETATION_20260911.md). The initial awaiting-to-loaded sequence requires a controlled repeat before attributing a cause or requesting a provider repair.
