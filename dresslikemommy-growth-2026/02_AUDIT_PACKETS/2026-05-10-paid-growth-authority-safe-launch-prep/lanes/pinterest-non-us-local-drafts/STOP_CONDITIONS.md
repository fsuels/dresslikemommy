# Pinterest Non-US Stop Conditions

Generated: 2026-05-10

Mode: local-only safety file. This is not an approval to act in Pinterest.

Stop immediately if any future non-US Pinterest operator sees one of these conditions.

## Approval And Account-Action Stops

- No exact parent/owner approval exists for the named market and named action.
- Approval text does not explicitly name any required initial budget, bid, or status fields.
- The UI requires `Create`, `Save`, `Publish`, `Launch`, `Promote`, `Enable`, `Apply`, `Upload`, `Sync`, or any equivalent account write outside the approval.
- The UI requires any campaign, ad group, ad, product group, audience, budget, bid, status, catalog source, feed, tag, CAPI, Shopify, Merchant, Google Ads, GA4/GTM, theme, product-data, or live-spend change.

## Source And Catalog Stops

- No country-specific Pinterest catalog/source/feed profile is visible and read back.
- The selected source is the blocked failed sitemap source `3041760916127467912`.
- The selected source is only the proven US EN source `3041760867124595727` and the operator cannot prove it is valid for the target non-US market.
- The source/feed profile, locale, item URL, price, availability diagnostic, or row count differs from the local packet and cannot be reconciled.
- Product groups cannot be filtered without changing feed labels, product data, source settings, or Merchant data.
- The clean scope cannot be counted and saved as local evidence before account action.
- Exclusions are unknown, overlap the clean scope, or include active catalog rows without a documented reason.

## Country And Language Stops

- Country targeting cannot be read back as the single intended country.
- A market's language split is unresolved (`CH`, `BE`, or `PT` in particular).
- Native-language copy has not passed native review for a native-copy market.
- Landing pages show mixed-language, stale policy, stale product metadata, wrong currency, or wrong country presentment for the intended market.
- The product URL points to the known beach/Vacation Family stale metadata blocker or any other held URL without a clean public readback.

## Measurement And Spend Stops

- Event Quality is `Fair` or worse and the operator is attempting live spend.
- Pinterest Tag/CAPI freshness is stale or missing.
- A second Pinterest pixel/tag/CAPI path is present or proposed.
- The operator is asked to add a duplicate theme tag, custom CAPI, or Customer Events pixel without a separate exact repair approval and dedupe proof.
- The account shows unexpected currently-serving campaigns, active ads, live product groups, or non-zero spend before the intended operation.

## Business-Model And Claim Stops

- Copy implies a physical store, warehouse, local inventory, on-hand stock, guaranteed availability, same-day/fast delivery, guaranteed delivery, unsupported free shipping, discounts, reviews, bestseller status, or urgency.
- The setup requires local inventory ads, pickup, store inventory, or physical-store claims.
- The setup would mutate Shopify product data, product labels, catalog/feed labels, product scope, product groups, Merchant source data, conversion goals, or Google Ads structure.

## Recovery Path

When a stop condition triggers:

1. Take no account action.
2. Capture the exact observed blocker in the parent packet.
3. Name the exact next unblock action.
4. Route unrelated safe work to another lane rather than treating the blocked market as a sprint-wide stop.
