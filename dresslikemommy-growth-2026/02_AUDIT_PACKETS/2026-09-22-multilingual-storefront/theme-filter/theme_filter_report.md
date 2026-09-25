Confidence: H for source classification equivalence and local JavaScript behavior; M for Shopify-rendered locale templates until parent live verification.

IMPLEMENTED in two source files:
- assets/daddy-me-collection-filter.js: classify existing analyticsHandle instead of translated analyticsTitle; select existing locale count wording through Intl.PluralRules; use localized other when a category is absent; avoid identical count text writes.
- snippets/collection-breadcrumbs.liquid: expose escaped count templates from products.facets.product_count_simple plural keys. Missing translation diagnostics are omitted from attributes.

snippets/card-product.liquid is byte-identical to baseline; its existing escaped data-analytics-handle already supplies the required source field. No product, collection membership, routing target, price, or inventory edits.

VERIFIED: 12 actual-IIFE regression tests pass. Coverage includes 100 source collection memberships (64 parent, 13 tees, 23 shirts), all 21 published locales, current English full snapshots, 23 observed Danish titles, tee exclusions, 0/1/plural counts using available locale keys, missing-template behavior, locale path/query preservation, observer idempotence, and replacement card metadata.

Fresh Shopify Admin fixture query passed structured schema validation and the Admin skill validator; all three collection pages returned hasNextPage=false. The original English title rule and source-handle rule yield identical cohorts: 24 parent shirts, 0 tee-collection shirts, and 23 shirt-collection shirts. Source memberships are not market-visible product counts.

VERIFIED: node --check and git diff --check passed. Shopify CLI Theme Check was run against one fixed theme snapshot, then rerun with our two files restored to baseline: outputs exactly identical, 3051 offenses (3048 MatchingTranslations, 3 TranslationKeyExists), none in our two files. The snapshot includes parallel locale work in progress; these counts are not a final release assertion.

BLOCKED: required Liquid skill validator cannot load @shopify/theme-check-common. The installed Shopify CLI was the independent validation fallback. No dependency installation or skill modification was attempted.

NOT RUN: public rendered candidate verification or release (parent owns these). Worker IAB was unavailable; no personal Chrome tabs were touched. Parent should verify rendered data-daddy-count-* attributes, visible count text and stable analyticsHandle across representative localized routes, including he/no once locale owner supplies their missing count keys.

Remaining limits: handles can be intentionally renamed; future source-handle changes should recheck the English cohort. This preserves the current tee inverse rule, including its existing non-shirt interpretation on the parent collection. It does not change pagination or market availability. Missing count translations leave the server text untouched rather than inventing an English replacement.

Evidence: source_collections_readback.json, before_manifest.json, candidate_manifest.json, regression.test.mjs, regression_output.txt, validation_summary.json, baseline_theme_check.json, candidate_theme_check.json.
