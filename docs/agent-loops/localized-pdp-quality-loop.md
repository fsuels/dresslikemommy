# Localized PDP Quality Loop

Use this loop after every Shopify listing create/update and before treating any active product as ready for international shoppers or paid traffic.

## Goal

Every published localized PDP should feel native enough for a shopper to buy: product title, body, size chart, option names, matching-set builder, trust blocks, policy summaries, reviews, footer headings, and related-product surfaces should not leak obvious English or raw translation keys.

The existing listing localization gates protect Shopify product translations and size-chart row coverage. This loop adds a storefront-level shopper readback so a product cannot pass only because the table exists while the visible PDP still says things like `Choose size`, `Secure checkout`, `Customer Reviews`, or `translation missing`.

## Read First

1. `AGENTS.md`
2. `VISION.md`
3. `docs/agent-loops/product-listing-localization-loop.md`
4. `docs/agent-loops/ui-browser-verification-loop.md`
5. Relevant `ops/AGENT_COORDINATION.md` rows and problem-tracker entries

## Inputs

- Product handle or a small batch of handles.
- Target locales to verify. Use all published non-primary Shopify locales for final listing closeout; use a smaller locale slice only for triage.
- Product status and surface:
  - Draft listing: Admin API translation repairs can be part of the listing workflow if the original listing scope approved product writes.
  - Active/live listing: product translation writes, product data writes, and theme deploys require fresh explicit owner approval.
  - Theme locale or Liquid/JS fixes: local edits are allowed, but live theme publish/deploy still requires approval and readback.

## Repair Order

1. For a normal listing create/update, run the same synchronous closeout that the generated listing runner is required to invoke:

```bash
/usr/bin/python3 ops/scripts/finalize_shopify_listing_localization.py --handles <handle>
```

The closeout forces the new product through translation immediately with `--min-age-seconds 0`, audits the full product before and after size-chart repair, runs strict size-chart and variant mapping gates, and writes `ops/listings/<handle>-localization-closeout.json`. Use the individual commands below only to diagnose a failed closeout.

2. Require the Admin full-product translation audit to pass before size-chart repair. Missing localized bodies must return to the translation poll; never seed an English/source body with translated labels and count it as localized.

3. Repair and verify localized size-chart coverage:

```bash
python3.13 ops/scripts/repair_localized_product_size_charts.py --handles <handle> --execute
python3.13 ops/scripts/repair_localized_product_size_charts.py --handles <handle> --fail-on-missing
python3.13 ops/scripts/audit_localized_size_chart_variant_mapping.py --handles <handle> --fail-on-unmatched
```

4. Run the public storefront language-smoke audit:

```bash
python3.13 ops/scripts/audit_localized_pdp_language_leakage.py --handles <handle> --locales es,fr,de,it,pt-BR,ro --fail-on-issues
```

5. Classify every issue:

- Product translation: title, body HTML, SEO text, product option names, option values, product metafield value.
- Theme locale key: Liquid string from `locales/*.json`, missing key, hardcoded English fallback, footer/header/menu/policy copy.
- Runtime JS copy: matching-set builder, sticky CTA, size guide, review headings, customer photo strip.
- Third-party app/widget: review widget, app-injected strings, external block not controlled by Shopify translations.
- Acceptable proper noun: brand, payment method, product name, country/currency, SKU, or measurement unit.

6. Fix the narrowest owning layer:

- Use Shopify `translationsRegister` via existing product translation scripts for product-owned text.
- Add or correct locale JSON keys for theme-owned text.
- Prefer generated `snippets/product-page-copy-map.liquid` or existing locale-driven data attributes for runtime JS copy.
- For app/widget text that cannot be translated in theme code, document the app setting or owner action needed.

7. Re-run the Admin and public audits for the same handles/locales until they pass or the remaining public findings are classified as allowed proper nouns or app-gated.

## Storefront Readback

For the final closeout, verify at least:

- Desktop PDP for each locale.
- Mobile/narrow PDP for the highest-risk locale, usually Spanish first.
- Exact product route, for example `/es/products/<handle>`.
- Option picker labels, matching-set builder text, trust block, size guide, product details, reviews widget, footer, and related styles.

Do not claim localized PDP quality passed unless a public-route readback or browser check actually ran.

## Pass Criteria

The loop passes when all are true:

- Product translation poll completed without blocking errors.
- `audit_shopify_product_translation_completeness.py --fail-on-issues` reports zero missing, outdated, source-equal, or source-language product-body findings.
- `repair_localized_product_size_charts.py --fail-on-missing` returns `products_with_missing_locale_size_chart=0`, `planned_translation_count=0`, and `error_count=0`.
- `audit_localized_size_chart_variant_mapping.py --fail-on-unmatched` returns `unmatched_variant_locale_count=0`.
- Public localized PDP language audit returns zero unclassified issues for the target locales.
- Browser readback shows no obvious English leftovers, `translation missing`, raw translation-key text, missing size rows, or broken mobile layout.
- Any remaining app-controlled strings are documented with the exact app surface and next owner action.

## Stop Conditions

Stop and report instead of writing when:

- The product is active/live and the repair would mutate Shopify product translations, product data, theme files on the live theme, app settings, feeds, or paid surfaces without fresh approval.
- A localized page shows checkout, login, CAPTCHA, account, policy, payment, billing, permission, or destructive prompts.
- The audit detects supplier/source URLs or source markers in public text.
- A third-party review/widget setting is required and no app/admin access is already approved.

## Handoff

Record:

- Handles/locales audited.
- Commands run and pass/fail results.
- Issues fixed by layer: product translations, theme locale keys, runtime JS copy, app/widget.
- Remaining app/approval gates.
- Whether the product is draft, active, unpublished, or published to channels.
- Next best action before publish or paid traffic.
