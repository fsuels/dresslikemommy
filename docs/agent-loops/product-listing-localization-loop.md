# Product Listing And Localization Loop

Use this loop for Shopify listing creation or updates from vendor pages, screenshots, size charts, product images, or dropship source material.

## Read First

1. `AGENTS.md`
2. `VISION.md`
3. `ops/prompts/START-HERE.md`
4. `ops/prompts/shopify-listing-master-prompt.md`
5. `ops/prompts/shopify-listing-from-1688.md`
6. Relevant `ops/AGENT_COORDINATION.md` rows and problem-tracker entries

## Safety Defaults

- New listing work is draft-first.
- Do not set products `ACTIVE`.
- Do not publish to Online Store, Google & YouTube, Facebook & Instagram, Pinterest, TikTok, or any other sales channel unless the owner explicitly requests a separate live publish step.
- Do not write vendor/source URLs, supplier domains, offer IDs, `1688`, `Alibaba`, or similar source markers into customer-visible or feed-visible Shopify data.
- Treat the size chart as the source of truth for variants and measurements.

## Build

- Create or update the idempotent runner under `ops/scripts/create-<shortcode>-<slug>.sh`.
- Save local listing notes, body HTML, CSV backup, verify JSON, size-chart JSON, and image evidence under the existing `ops/listings/` and `uploads/<slug>/` conventions.
- Use existing price/cost, tag, metafield, and category rules from the canonical listing prompt.
- Halt before any Admin API write if variant count, option axes, size rows, or category evidence is inconsistent.

## Validate

Use the exact commands required by the listing prompt for the touched product. Common gates include:

```bash
python3 ops/scripts/validate_listing_variant_model.py --size-chart <size-chart.json> --derived <derived.json> --vendor-evidence <detail-evidence.json>
/usr/bin/python3 ops/scripts/finalize_shopify_listing_localization.py --handles <handle>
python3.13 ops/scripts/audit_localized_pdp_language_leakage.py --handles <handle> --locales <all-published-non-primary-locales> --fail-on-issues
```

The generated `create-<shortcode>-<slug>.sh` runner must invoke `finalize_shopify_listing_localization.py` itself after the create/update heredoc. Do not leave the closeout as a manual follow-up. The command translates the new product immediately with `--min-age-seconds 0`, runs the full-product audit before and after size-chart repair, runs strict size-chart and variant mapping readbacks, writes `ops/listings/<handle>-localization-closeout.json`, and exits nonzero on failure.

Also re-query Shopify and confirm:

- Product remains `DRAFT` unless explicitly approved otherwise.
- Variant count and SKUs match the derived model.
- Prices and Cost per item match the active rule.
- Size tables and localized body HTML preserve row coverage.
- The Admin translation completeness audit reports no missing, outdated, source-equal, or English/source-language product-body translations.
- Public localized PDP routes do not leak obvious English copy or raw translation keys; use `docs/agent-loops/localized-pdp-quality-loop.md` when this gate fails.
- No source/vendor tokens leaked into Shopify data or generated artifacts.

## Done

The loop is done when the product is verified in Shopify Admin, the generated runner's localization closeout report says `status=passed`, the full-product translation gate passes for every published non-primary locale, size-chart/variant gates pass, public localized PDP language-smoke checks pass or have documented app/approval gates, source-leak checks pass, and the handoff names exactly what the owner should review before any future publish step.
