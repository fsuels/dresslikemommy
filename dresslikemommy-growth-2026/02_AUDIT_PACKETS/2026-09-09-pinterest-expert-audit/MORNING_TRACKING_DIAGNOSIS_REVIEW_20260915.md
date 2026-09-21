# Pinterest tracking diagnosis review — September 15, 2026

Confidence: M. **CAUSE_UNKNOWN; read-only catalog prerequisite check recommended.** Reviewed only `DAILY_TRACKING_READBACK_20260914.json`, `TRACKING_MAPPING_REVIEW_20260910.md` and official documentation. No current account replay, credential access, event generation or external mutation; only this review was written.

The September 14 receipt reports Tag AddPaymentInfo Product ID coverage 100% with low catalog match, versus CAPI coverage 0%, over a 14-day window updated September 12. Exact affected IDs and numeric match rate are unknown. The sample download timed out once; no file receipt proves delivery. Pinterest documents separate coverage/issue samples and 14-day versus one-day views; changed windows are not causal evidence. [Event Quality Score](https://help.pinterest.com/en/business/article/eqs)

**Adversarial challenge:** a parent product ID is not automatically wrong because a catalog also contains variant IDs. September 10 demonstrated a browser mapping to `variant.product.id`, not current server payloads or accepted catalog membership. Pinterest distinguishes catalog `id` from parent `item_group_id`; the reviewed public documentation does not establish this diagnostic's exact group-ID fallback or market-matching algorithm. Preserve both literal namespaces rather than rewrite them from inference. [Catalog fields](https://help.pinterest.com/en/business/article/before-you-get-started-with-catalogs)

**One least-invasive step executable without affected-event IDs:** root reads the currently linked Pinterest catalog's source and market inventory, recording catalog/source identity, country/language/currency, latest successful ingestion, submitted/accepted counts and issue summaries. Keep ingestion and distribution status separate. Then choose one known current product as a control and record its accepted `id`, `item_group_id` and source/market alongside its known Shopify parent/variant IDs. This can reveal a stale/empty source or namespace prerequisite; a passing control cannot clear the affected cohort. No download retry, sync, upload or catalog repair is needed. [Catalog diagnostics](https://help.pinterest.com/en/business/article/catalog-diagnostics), [Source country/language](https://help.pinterest.com/en/business/article/data-source-ingestion)

Evidence needed before choosing a repair:

- **Sender ID:** an actual affected literal ID, event time/source and matching product identity, compared with accepted catalog `id`/group values. Check parent-versus-variant, prefixes and formatting; a difference alone is not proof without the supported matching rule.
- **Missing/stale catalog:** the same product/ID in the submitted source versus Pinterest's accepted rows, with ingestion timestamps and row errors. An ad-distribution rejection alone does not establish an absent catalog ID.
- **Market case:** the affected event's non-personal storefront locale/currency context and the same product's source/market mappings. Currency alone does not identify country. Localization differences require evidence of relevance to the diagnostic before blaming them. [Catalog localization](https://help.pinterest.com/en/business/article/localize-your-catalog)
- **CAPI omission:** paired legitimate Tag/server-event metadata and event identity. Reported 0% does not distinguish missing, empty or invalid payload fields. CAPI product metadata is recommended for AddPaymentInfo but optional for request acceptance; changing catalog rows cannot correct a missing/malformed server field. [CAPI product parameters](https://developers.pinterest.com/docs/track-conversions/track-conversions-in-the-api/)

No sender rewrite, reinstall, consent retry or repair is justified yet. App-pixel callback success is not Pinterest receiver acceptance, and server pixels remain consent-governed. [Shopify app-pixel diagnostics](https://help.shopify.com/en/manual/promoting-marketing/pixels/app-pixels)

## September 15 saved-receipt after-review

**PASS_WITH_LIMITS — 32/32 checks passed.** Independently compared `MORNING_OPERATOR_RECEIPT_20260915.json`, `MORNING_RAINBOW_SOURCE_20260915.json` and `N2_NATIVE_EXECUTION_20260914.json`; no live replay.

All six schedule IDs match yesterday's receipt. N2's board/date/time match its saved detail. Current weekday, ordering and 168.5-hour P4-to-N2 spacing are consistent with the three-Pin limit. Yesterday's N2 execution receipt does not individually repeat P2–P6 times, so it alone cannot prove their historical timing preservation.

The English source is populated: 4,924 successful, zero failed, 277 warnings. This completes that prerequisite check, not the affected-event join. The 21-row decrease is correctly unassigned to a cause. The separate 99.98% display and empty issue table remain qualified; neither proves warnings cleared.

Rainbow's parent/control-variant IDs match its eight-variant Shopify source. ACTIVE does not prove sale availability. The two-value filter's 19 count with zero rendered rows identifies neither accepted literal ID nor market; it is not a zero-product result. Tag 100% coverage does not prove catalog agreement; CAPI 0% leaves missing/empty/invalid server fields unseparated.

The three outbound clicks and beta zero-revenue/checkout display retain aggregate-source limits, without asserting Shopify sales absence or profit improvement. No material overclaim or data correction found. Treat P2's “not yet due” as conditional on intended New York timing; start its first complete-date cohort only after publication is verified. Do not repeat unchanged source/control probes. Only this review was updated.
