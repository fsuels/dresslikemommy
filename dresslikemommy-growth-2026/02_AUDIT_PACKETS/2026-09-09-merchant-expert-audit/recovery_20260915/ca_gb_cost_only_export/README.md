Confidence: H. This is an isolated local implementation candidate, not an active generator, feed, source, market activation or upload approval.

The candidate adds a market-scoped `shippingCostOnly` option to the actual `automation_release_v1/src/generator.js` used by the `native-holds-20260914` profile. The source generator SHA256 is `a028e2f7f3bb1f0c1f03e222e6b2a608b742f46b6a8f13cc97572885fe009c4f`. All 14 owner-profile dependencies were checked before preparation and again in the tests. Their original paths/hashes are in `dependency_bindings.json`. The profile authorizes the existing US English local publisher only; it does not authorize this addition or a CA/GB release.

Only `generator.patch` changes executable behavior. `candidate/src/generator.js` is the reviewable full candidate; collector, query, eligibility, package and fixture files are byte-identical local copies used to resolve imports. No active code, configuration, owner profile, deployment, canonical record, Shopify record or native Merchant state was changed. No credentials, real source snapshots or live feeds are in this packet. No dependencies were installed.

The exact optional market property is:

```json
{
  "shippingCostOnly": {
    "country": "CA",
    "currency": "CAD",
    "amount": "0.00",
    "verified": true,
    "evidenceSha256": "REPLACE_WITH_REVIEWED_ZERO_COST_RECEIPT_SHA256"
  }
}
```

For `gb-en`, change only `country` to `GB`, `currency` to `GBP`, and use the applicable reviewed receipt hash. The example placeholder deliberately fails validation. This is not a runnable production config. Do not copy the synthetic test evidence hash into a release. The separate `proposed_market_options.json` now binds the parent’s fresh 13:34:37.245 UTC shipping read (`482e430c12ff3ec74cfe205bb5f4fad82ea6e734f1225695af7491d9faf5abd2`, 15 coverage checks passed). It supplies exact proposed CA/GB property additions for later independent review; it contains no enabling or landing-verification flags and has not been merged into any current config.

The option accepts only `ca-en`/CA/en/CAD and `gb-en`/GB/en/GBP with source locale `en`, `market.enabled === true`, `landingContextVerified === true`, matching explicit country/currency landing query, existing eligibility holds configured, and `returnPolicy.emitLabels === false`. Those flags are prerequisites; this patch never changes them. Existing real CA/GB configurations remain disabled and unverified. Global placement, unknown keys (including ETA/service/return fields), a mismatched country/currency, any amount other than the exact string `0.00`, a nonliteral verification flag, or a malformed/all-zero receipt hash fails closed. The flag/hash binds a review reference; code cannot establish the truth, current applicability or independence of that evidence.

With valid opt-in, the TSV receives one final `shipping` column containing exactly `CA:::0.00 CAD` or `GB:::0.00 GBP` on every emitted row. No handling/transit values, return-policy label or product `returns` annotation is submitted. Existing row fields, native prices, numeric variant links, exclusions, lifecycle sets and source clocks are preserved. Diagnostics alone gain the cost-evidence reference and display limitation. Without this property, US/AU/CA/GB default results and streamed/materialized bytes remain equal to the active generator, including ordinary return-label behavior. The shared default `COLUMNS` array is unchanged.

Google documents product shipping-price precedence over account shipping settings. Omitted delivery/return annotations do **not** guarantee no display: Google may use crawled or modeled ETA information and default/website return information. This candidate does not resolve the storefront's conflicting return wording or prove delivery times. [Shipping attribute](https://support.google.com/merchants/answer/6324484), [shipping settings precedence](https://support.google.com/merchants/answer/12578516), [optional return-policy submission](https://support.google.com/merchants/answer/14011730). These primary-document findings were supplied by the parent; no web calls were made here.

Tests use only synthetic products, prices, catalogs, source clocks and verification evidence. They reuse the six actual configured hold identifiers to verify unavailable/held partitioning, complete-source-proven archival and reactivation. Coverage includes default result equality, materialized/streamed column equality, no CA/GB option leakage into US/AU, malformed/broadened settings, disabled/unverified contexts, incomplete/stale/future/changed sources, native price errors, numeric IDs, no partial feed on error and publication exclusions. The initial new test helper had a missing brace; syntax checking stopped before tests, the one-brace correction is recorded in `syntax_initial_failure.json`, and the passing initial run is retained. The final run additionally tests accidental global option placement.

Run the bounded suite from this packet with the existing runtime:

```sh
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test candidate/test/shipping-cost-only.test.mjs
```

Next: independently review the exact patch, evidence contract and test receipts. Only a subsequent explicit integration/release can bind real cost evidence, complete fresh country sources and actual published CA/GB buyer acceptance. Do not update frozen US/AU profile hashes merely to make this candidate load; a separately reviewed dependency transition is required if shared active code is later changed. Alternatively, keep its eventual country exporter isolated under its own exact reviewed dependency binding. The existing owner remains responsible for native receiving and effective shipping readback.
