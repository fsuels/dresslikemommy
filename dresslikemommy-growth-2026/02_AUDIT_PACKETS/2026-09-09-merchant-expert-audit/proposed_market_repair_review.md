# Independent prewrite review: two-product market repair

Current status: the latest conditional six-join release below supersedes the initial hold when its explicit source-body and target-readback conditions pass. Earlier sections preserve the review history.

Date: 2026-09-09. Reviewer: merchant_standards_review. `DID_NOT_BUILD_OR_EXECUTE=true`. Confidence: H for scope and demonstrated defects; M for downstream eligibility. **Verdict: HOLD_AS_PROPOSED until the concrete product-data defects below are contained. Current owner authorization is sufficient; another permission request is not the missing step.**

## Scope and publication semantics: PASS

Reviewed root's `market_repair_before.json` at `2026-09-09T16:49:37.686Z` and separate `market_inventory.json`. Products `7109517770849` (27 variants) and `7227374534753` (21) are ACTIVE, available to Google and Online Store, and excluded from exactly these existing market publications:

| Market | Publication | Catalog |
|---|---|---|
| Eurozone | 77105660001 | 6880723041 |
| International | 77105823841 | 910622817 |
| United States | 77106053217 | 6881083489 |

Each catalog contains 238 of 240 active products. Existing catalogs are ACTIVE; no hold/exclude marker or known intentional exclusion was found. The historical exclusion reason remains UNKNOWN, not proven accidental. The owner's explicit all-products/all-served-markets request supports restoring these six joins, subject to product truth.

Catalog inclusion and channel publication jointly control customer availability; this is a real storefront availability expansion. Publication changes do not require price changes. [Shopify catalog semantics](https://help.shopify.com/en/manual/markets/customizations/catalogs) The proposed product-specific publish/unpublish operations are appropriate and reversible. Current docs state that parent publication changes preserve variant-specific publication state; the connector's inspected ProductVariant schema does not expose those newer publication fields. Do not claim all 48 variants are independently publication-verified. [Publishing semantics](https://shopify.dev/docs/apps/build/sales-channels/product-publishing)

## Concrete defects discovered before release

1. **43 of 48 nonempty barcodes fail GTIN checks:** 25/27 on `7109517770849`, 18/21 on `7227374534753`. Computed from the full root snapshot using valid-length checks and GS1 alternating 3/1 modulo-10 calculation; four positive/negative control cases passed. The other five pass checksum only, which does not prove manufacturer assignment. [GS1 algorithm](https://www.gs1.org/services/how-calculate-check-digit-manually) Google requires accurate identifiers and directs merchants to leave unknown assigned identifiers blank, never invent replacements. Correct or remove demonstrably invalid values with an exact before/after record; do not manufacture check digits or infer `identifier_exists=false`. [Google identifier requirements](https://support.google.com/merchants/answer/160161)
2. **Six supplier-hosted image URLs remain in `7109517770849`'s description.** Expanding availability would expose this known source-leak defect in additional market contexts. Preserve the images/content through approved rehosting or another reviewed correction before publication. The exact body SHA-256 observed was `ae53f8ef97b7723ea3d4fe902478e50dccb019ec4d30c5430e61ccbb72cfc9a4`. Root's repo snapshot also needs redaction, retaining exact rollback privately under project hygiene rules. No source URLs are repeated here.

## Paid scope and required readback

The six joins do not mutate campaign settings, bids, budgets or tracking. Root reports a fresh 16:32 native checkpoint with Merchant 513 at zero offers and no linked Ads. This supports the bounded path, but neither unchanged settings nor this review establishes zero indirect spend: existing consumers can react to changed product availability. Do not enlarge campaigns or countries to complete this repair.

After data corrections and refreshed preconditions, recheck the six false joins and exact target bindings; preserve non-target publications, prices, variants and all other fields. Execute only the intended joins, recording per-product errors and partial success. Independently read six true joins, catalog counts expected at 240, unchanged nine app publications per product, and unchanged non-target data. Rollback removes only joins actually added, preserving later unrelated edits.

Verify representative localized selected-variant product/cart paths and subsequently Merchant's received offers and free-listing eligibility. Shopify publication success alone cannot close the broader audit. Next action: contain the proven identifier/source defects, then return the refreshed packet for release review.

## Containment amendment: PASS; publication remains separate

Independently reconciled `barcode_containment_plan.json`: exactly 25+18 invalid variants; updates contain only ID and empty barcode; all 43 inverse values match the before-state; five checksum-valid variants remain untouched; four checksum controls pass. Two calls are not jointly atomic: inspect each result and read back successful changes before any retry. Preserve every other variant/product field and identifier flag.

Rehosting the six existing images through the structured upload tool is within current correction authority. Verify each hosted copy is accessible and preserves the original visual content. Replace only the six exact source URLs in primary/affected translated bodies; retain all images, copy, tables and alt values. Snapshot locale values and use current translation digests. Keep exact source URLs private. New permissions are unnecessary. Missing identifiers, five unverified values and Merchant receipt remain explicit gaps.

## Extended invalid-GTIN containment: prewrite PASS

Reviewed 2026-09-09 after both canary readbacks. Current owner correction authority covers clearing the frozen **1,065 checksum-invalid barcodes across 68 products**. No additional owner permission or substantive eligibility blocker was identified for this exact containment. Publication and image repair remain separate.

Independently recomputed all 4,945 raw audit rows: 1,108 invalid, 3,712 empty, 125 checksum-valid but manufacturer-unverified; zero classification mismatches or duplicate variant IDs. Every parent is ACTIVE. The 43 canary rows and 1,065 remaining rows partition the invalid set exactly. Frozen `identifier_audit.json` SHA-256: `397405435b058e0c7d04be5c286cf1e05e843df3ace78b4e4a9fcbb462ffdf87`.

Independently compared both complete canary variant connections: all 43 targets became null; five valid-checksum values and every other shared product, variant and publication field matched. Description preservation is root-attested against its private snapshot, not independently rehashed by this reviewer.

Execution conditions:

- Refresh each product and compare exact IDs, ACTIVE status and original target barcodes against the frozen cohort. Stop on unexplained drift; exclude valid/empty rows, including duplicates whose validity is unproven.
- Change only target barcode values, with partial updates disabled. Calls are atomic per product, not across the cohort. Record each success/error; do not replay successful products blindly.
- Read complete variant connections after each success. Require target nulls and exact preservation of all other queried fields, including SKU, prices, options and inventory settings. Preserve MPN/custom-product/identifier flags.
- Keep exact inverse values; any rollback must account for subsequent changes. Stop on readback mismatch before continuing.

This removes demonstrably invalid submitted identifiers without inventing replacements, consistent with [Google identifier guidance](https://support.google.com/merchants/answer/160161). It does not verify manufacturer assignment, Merchant receipt, free-listing eligibility, traffic, profit or zero indirect paid impact. **Next action:** execute and independently read back this exact frozen cohort.

## Conditional six-join release

2026-09-09. `DID_NOT_BUILD_OR_EXECUTE=true`. **CONDITIONAL RELEASE**, within the owner's explicit all-products/all-served-markets correction request. No additional owner permission is required. Scope: products `7109517770849` and `7227374534753`, each into existing publications `77105660001`, `77105823841`, `77106053217`; six joins only.

The 43 invalid barcodes have passed independent comparison. Keep the five checksum-valid but manufacturer-unverified values unchanged; proving every retained identifier's provenance is not a new release prerequisite. `image_verification.md` releases the six hosted images for exact reference replacement. Four blocked direct-source comparisons limit fidelity claims, but the verifier found no visible content blocker.

Before publication:

1. Complete and read back the exact six-reference substitution in the source body and all 20 affected locale bodies. Compare each body to its private original after only the approved substitutions; preserve copy, tables, image order, alt values and other translation keys. Check rendered hosted images and current translation digests. No remaining known source references in these bodies.
2. Refresh both ACTIVE products, 27/21 complete variants, availability, existing Google/Online Store and other app publications; preserve prices, inventory settings and other fields. Reconfirm no new hold/exclusion evidence and the exact ACTIVE catalog/publication bindings. Capture the six current joins and catalog counts; stop on unexplained drift.
3. Use only these product/publication pairs, with an inverse for joins actually added. Inspect each mutation/error separately; do not blindly repeat a partial success.

After publication, independently read all six joins true, expected catalog counts 240 when the refreshed baseline remains 238, unchanged app publications and non-target fields. Verify representative selected-variant localized product/cart paths. Preserve subsequent unrelated edits in any rollback.

Fresh native Merchant receipt/country/eligibility checks remain necessary to close the broader audit, not additional prerequisites for this Shopify-only repair absent a concrete contradiction. No campaign, budget, country creation or tracking change is included. Zero indirect paid impact is not certified. **Next:** finish exact body readback, then execute these six joins.

## Source-body release precondition: independently VERIFIED

2026-09-09. `DID_NOT_BUILD_OR_EXECUTE=true`. **PASS:** the source-image correction precondition for the conditional six-join release is satisfied.

Compared the private before-state, `image_src_replacement_plan.json`, `image_rehosting_after.json` and the ordered hosting manifest. Independently verified exactly six approved reference replacements in each of 21 source/locale bodies: **126 substitutions**, with every other body byte unchanged. The source retains eight image tags. All 20 locale bodies read `outdated=false`; all non-body translatable records, other locale fields and body metadata match their before-state. Each original source reference occurred once per body and none remains in the corrected bodies. Plan and readback bodies match exactly. The private snapshot remains mode 0600; no supplier URLs were printed or persisted by this reviewer.

After-evidence SHA-256: `5a33f4af3a1ed643afc03c36a8daa3159f2b86d1a0bb75a2528229bd3ab2efcb`.

The separate image-content release remains supported by `image_verification.md`. This translation comparison does not independently reproduce root's broader full-product non-body preservation assertion. Root will refresh both products, all 48 variants and all three publication bindings before adding the six joins; the existing target/drift and after-readback conditions remain applicable. No additional approval or substantive blocker arose.

**Next:** complete the fresh Shopify target snapshot and execute only the six reviewed joins; then independently verify publication results and preserved fields.
