# Listing Localization Workflow Automation Readback

Date: 2026-07-23

## Outcome

The normal Shopify listing creation workflow now has a synchronous localization closeout. A generated listing runner is not allowed to exit successfully after creating or updating a product until the product passes the full translation, localized size-chart, and variant-row mapping gates.

## Required Runner Footer

Every future generated `ops/scripts/create-<shortcode>-<slug>.sh` runner must call:

```bash
/usr/bin/python3 "$ROOT/ops/scripts/finalize_shopify_listing_localization.py" --handles "<handle>"
```

The requirement is part of the canonical listing prompt, quick-start instructions, 1688 listing instructions, and product-listing localization loop.

## Synchronous Closeout

`ops/scripts/finalize_shopify_listing_localization.py` performs these steps in order:

1. Full-product translation refresh with `--min-age-seconds 0 --execute --force-refresh`.
2. Full-product Admin translation audit with `--fail-on-issues`.
3. Localized size-chart repair.
4. Second full-product Admin translation audit after the deterministic repair.
5. Strict localized size-chart audit with `--fail-on-missing`.
6. Strict variant-to-localized-size-row audit with `--fail-on-unmatched`.

Any nonzero step stops the closeout, leaves the listing workflow failed, identifies the exact failed step, and writes evidence to `ops/listings/<handle>-localization-closeout.json`. A successful closeout writes `status=passed`.

The immediate `--min-age-seconds 0` override closes the defect that allowed a brand-new listing to be deferred by the background worker's normal five-minute stabilization delay.

## Second Safety Net

The installed `com.dresslikemommy.shopify-product-translations` LaunchAgent continues checking for newly created products every five minutes with `--force-refresh --execute`. This covers products created outside the canonical generated listing runner.

The background worker is not accepted as the normal workflow's closeout evidence. A standard listing run still needs its synchronous per-handle report.

## Regression Protection

- `ops/tests/test_finalize_shopify_listing_localization.py` verifies the six-step order, immediate new-product override, live force refresh, strict audits, and canonical workflow references.
- `ops/scripts/check_continuity_integrity.py --strict` now fails if the closeout script is missing, loses required translation/audit stages, or is removed from any canonical listing workflow file.

## Verification

- `python3.13 -m py_compile ops/scripts/finalize_shopify_listing_localization.py ops/tests/test_finalize_shopify_listing_localization.py ops/scripts/check_continuity_integrity.py` passed.
- `python3.13 ops/tests/test_finalize_shopify_listing_localization.py` passed.
- `python3.13 ops/scripts/finalize_shopify_listing_localization.py --handles future-listing-example --print-plan` produced the expected six-step plan without Shopify reads or writes.
- `python3.13 ops/scripts/check_continuity_integrity.py --strict` passed and included `PASS listing_localization_workflow`.
- Targeted `git diff --check` passed.

## Boundary

This closeout guarantees current product-owned translations and localized size/variant integrity across every published non-primary Shopify locale. New products remain drafts in the normal workflow, so public-route browser verification happens after a separate publish step. Shared theme/runtime and third-party widget localization remain storefront-level concerns rather than product translation fields.

