# Pinterest GB/CA/AU Local Scope Readiness

Date: 2026-05-12

Decision: `LOCAL_READINESS_PACKET_CREATED_NO_ACCOUNT_WRITES`

## Executive Verdict

GB, CA, and AU are not Pinterest account-ready. They are the first non-US Pinterest local-packet candidates after US because they are English-first markets and the Google Ads/checkout infrastructure is strongest, but there is no country-specific Pinterest catalog/source/product-group readback for any of them.

The right growth path is:

1. Finish the already-approved paused US Pinterest draft after authenticated Ads Manager access is restored.
2. Build one non-US local Pinterest scope packet at a time, starting `GB`, then `CA`, then `AU`.
3. Do not create Pinterest account objects for GB/CA/AU until exact approval names the paused-only action and live readbacks prove the country source/scope.

## Current Proven Pinterest Baseline

| Item | Current evidence |
|---|---|
| Advertiser | `549756244483` |
| Catalog | `3041764155561548387` |
| Allowed US EN Shopify source/feed profile | `3041760867124595727` |
| Failed sitemap source to avoid | `3041760916127467912` |
| Clean US scope | `342` EN-US rows |
| US scope split | `210` Mommy & Me, `103` Family Matching, `29` Pajamas |
| US exclusions | `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401` |
| Current Pinterest campaigns in prior readback | `0` campaigns, `0` serving, `$0.00` spend |
| Event Quality | `Fair`; owner later instructed not to keep looping on tags as a launch-prep blocker |

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-controlled-measurement-pinterest-build/CONTROLLED_MEASUREMENT_PINTEREST_BUILD_REPORT.md`

## GB/CA/AU Readiness Matrix

| Market | Locale posture | Current Pinterest account readiness | Reusable local templates | Stop condition |
|---|---|---|---|---|
| GB | `en-GB` English-first | `NOT_BUILT_NO_SCOPE_READBACK` | Non-US naming/product-group/copy templates | Stop if no GB source/feed profile or if country targeting cannot read GB-only |
| CA | `en-CA` English-first; French-Canada later only by explicit decision | `NOT_BUILT_NO_SCOPE_READBACK` | Non-US naming/product-group/copy templates | Stop if no CA source/feed profile or if setup mixes US/CA |
| AU | `en-AU` English-first | `NOT_BUILT_NO_SCOPE_READBACK` | Non-US naming/product-group/copy templates | Stop if no AU source/feed profile or if item URLs/prices cannot prove AU presentment |

Reusable templates:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/pinterest_non_us_market_readiness_matrix.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/pinterest_non_us_object_naming_template.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/pinterest_non_us_product_group_template.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/pinterest_non_us_copy_country_gate_template.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade/pinterest_multilingual_keyword_interest_quality_plan.csv`

## Exact Next Safe Action

Build `GB` local scope proof first, without account writes:

- Read Pinterest Ads Manager source/catalog UI/API in a logged-in controllable browser.
- Prove whether a GB/country-specific source or item scope exists.
- Capture source ID, source status, row count, diagnostics, item URL/presentment if exposed, and available product-group filters.
- Prove whether Mommy & Me / Family Matching / Pajamas can be filtered without source/feed/feed-label/product-data mutation.
- Stop if the UI requires catalog source changes, tag/CAPI changes, audience creation, budget/bid/status activation, or any product/feed mutation.

## Approval Gate

Any Pinterest GB/CA/AU account write still requires fresh exact owner approval naming:

- Market.
- Campaign/ad group/ad/product-group scope.
- Paused-only status.
- Budget/bid fields required by Pinterest but not activated.
- Catalog/source/product-group behavior.
- Explicit no live spend and no catalog source, tag, CAPI, audience, Shopify product, Merchant, Google Ads, or feed changes.

## Guardrails Preserved

No Pinterest account writes, campaign/draft/product-group/catalog/audience/tag/CAPI/feed changes, live spend, Ads changes, Merchant changes, Shopify product-data changes, conversion-goal changes, budget/bid/status changes, payment/order/refund/cancel, credential/account/billing edits, or destructive filesystem actions were made in this local packet.
