# Powder Blue Option Translation Polish

Date: 2026-05-19 EDT

Product: `7535944368225` / `powder-blue-mommy-and-me-set`

## Scope

Only the newly introduced piece selector was translated:

- Product option `Type`
- Product option value `Top`
- Product option value `Pants`

No body copy, title, SEO, product status, handle, prices, variants, inventory, images, theme files, feeds, campaigns, analytics, billing, or credentials were changed.

## Before Readback

- `Type` had inherited stale size-option translations such as Spanish `Talla` and German `Größe`, all marked `outdated=true`.
- `Top` had no option-value translations.
- `Pants` had no option-value translations.

## Change Made

Registered Shopify translations for all 20 published non-primary locales:

`ar`, `cs`, `da`, `de`, `el`, `es`, `fi`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `nl`, `no`, `pl`, `pt-BR`, `ro`, `ru`, `sv`.

Total translations registered: `60`.

## Admin Translation Readback

GraphQL translatable-resource readback passed:

- Resources checked: `3`
- Locale checks: `60`
- Missing translations: `0`
- Outdated translations: `0`

Sample values:

| Locale | Type | Top | Pants |
|---|---|---|---|
| `es` | `Tipo` | `Top` | `Pantalones` |
| `fr` | `Type` | `Haut` | `Pantalon` |
| `de` | `Typ` | `Top` | `Hose` |
| `pt-BR` | `Tipo` | `Top` | `Calça` |
| `ar` | `النوع` | `توب` | `بنطال` |
| `ja` | `タイプ` | `トップス` | `パンツ` |

## Storefront Samples

- `/es/products/powder-blue-mommy-and-me-set`: rendered `Tipo`, `Top`, `Pantalones`.
- `/fr/products/powder-blue-mommy-and-me-set`: rendered `Type`, `Haut`, `Pantalon`.
- `/de/products/powder-blue-mommy-and-me-set`: rendered `Typ`, `Top`, `Hose`.
- `/pt/products/powder-blue-mommy-and-me-set`: rendered `Tipo`, `Top`, `Calça` with `html lang="pt-BR"`.

`/pt-br/...` and `/pt-BR/...` returned `404`; the active Portuguese storefront route is `/pt/...`.

## Evidence Files

- `translation_plan.json`
- `translation_register_results.json`
- `translation_readback_all_locales.json`
- `storefront_es.html`
- `storefront_fr.html`
- `storefront_de.html`
- `storefront_pt_casecheck.html`

## Residual Risk

These are concise machine-assisted commerce-label translations for short option labels. They are appropriate for storefront utility labels, but they were not reviewed by native speakers.
