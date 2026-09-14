Confidence: H for the local evidence gap; current installed Microsoft/Meta behavior remains UNKNOWN.

No qualified purchase-tracking patch is supported. The bounded scan of **256 local JS/CJS/Liquid/JSON files** in `pixels`, theme directories and `agent-backend` found no UET/Meta sender, catalog-ID mapping or matching purchase-parameter implementation. No patch or artificial reproducer was created; existing source and production were untouched.

The [pixel README](../../../pixels/README.md:11) explicitly identifies the GA4/Google Ads files as templates. [Local analytics code](../../../assets/analytics.js:115) pushes dataLayer events, including [begin_checkout](../../../assets/analytics.js:952). Neither that queue nor the [theme language context](../../../layout/theme.liquid:304) establishes a Microsoft/Meta consumer or a completed-purchase sender.

The [March26 runtime record](../../../ops/AGENT_WORKLOG.md:8540) names UET tag **36005151** and Meta pixel **547553035448852** in Shopify web-pixel configuration. The [April29 source review](../../../ops/AGENT_WORKLOG.md:24700) found no hardcoded `fbq`/`uetq`. These are dated recorded observations, not current installation or payload proof. The current saved [purchase-capture receipt](purchase_capture_current_readback.json) documents Google integrations only; it cannot prove Microsoft/Meta is absent.

The [prior UET review](microsoft_uet_purchase_source_review.md) remains valid: 98 conversions/value98 does not prove hardcoded1, missing revenue, fallback use, or duplicate events. Meta value/currency, browser/server event identity, and catalog content-ID mapping remain unverified. Tag36000629 is a UET tag, not the Smart goal ID.

The saved GA4 helper repair and Microsoft goal163000100 Include-in-Conversions repair are completed scopes. Neither was reapplied or reinterpreted as full purchase validation.

**Next action:** after normal native access returns, root should bind the existing Shopify Microsoft/Meta app integrations to their current IDs and inspect already-existing purchase diagnostics for value, currency, event identity and catalog mapping. No synthetic purchase, new pixel, consent/account change or duplicate-goal edit follows from this inventory. If the installed source/diagnostics is unavailable, retain UNKNOWN.

The [structured inventory](cross_platform_tracking_source_20260907.json) records exact scope, source hashes and checks. No browser/API/event calls occurred. Local runtime tests were not applicable without an implementation candidate. Continue with the installed-payload readback; it is the first evidence that could justify a useful tracking repair.
