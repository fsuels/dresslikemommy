# Italian GA4 native result review

Confidence: H. **PASS — internally consistent receipt; no required correction.** Reviewed 2026-09-06. This independently assesses the [sanitized operator receipt](italian_ga4_native_readback.json), not a replay of browser observations or the private transaction join.

The retained row reports one purchase/USD151.46, generic session campaign `23866684201`, native Ads customer `3990976848`, native Ads campaign name `DLM_IT_SEARCH_NATIVE_IT_EXACT_015_TEST_20260519`, and manual campaign ID `(not set)`. Native account plus campaign name supports explicit GA4 attribution of this purchase’s session. The historical name-to-ID mapping remains operator-supplied; the unavailable Ads-specific numeric ID is correctly not inferred from the generic ID. Missing manual ID does not prove absent manual tagging or exclude other touchpoints. The [frozen interpretation](italian_ga4_native_interpretation.md) remains applicable and unchanged.

The rolling June 8–September 5 result (33 purchases/USD2,281.81) is explicitly superseded. Custom June 7–September 4 restored 36/USD2,612.69 before filtering; the receipt reports those fixed dates and the same isolated row persisted after reopening. These observations are not a fresh reconciliation of every order.

The quality dialog’s 100% of available daily data establishes reported unsampled coverage, not complete event capture, all real touchpoints, or agreement with Shopify. The sanitized receipt excludes transaction identifiers; the saved, explicitly unshared exploration retains the private filter. Creating that analytical artifact is distinct from changing production measurement configuration. Its privacy and persistence observations remain operator-supplied.

Shopify’s organic journey discrepancy, independent click linkage, Google Ads conversion credit, value differences, campaign cost and actual order costs remain unresolved. No sales lift, incremental acquisition, CPA, 650% ROAS or profitability is established.

Next action: assess root’s bounded campaign-cost receipt if available; otherwise preserve the Ads access gate. No launch or measurement change is supported by this result alone.

SHA256 bindings:

- Receipt: `aed1b1e036081583014b5b34d425b5da6dd900b4a6a4369423ae15d48d1e10f4`
- Frozen interpretation: `54c5b441767a248098120394703bb112e4d054562fa50322e5f9d455dfa0a020`
