# Recent Listing All-Locale Translation Repair Readback

Date: 2026-07-23

## Scope

- Shopify products created on or after `2026-06-23T00:00:00Z`.
- Six non-archived products, all created on 2026-06-29:
  - `pink-resort-ruffle-mommy-and-me-dresses`
  - `green-botanical-ruffle-mommy-and-me-dresses`
  - `ocean-bloom-mommy-and-me-dresses`
  - `red-tropical-leaf-mommy-and-me-dresses`
  - `coral-blossom-mommy-and-me-dresses`
  - `ivory-meadow-mommy-and-me-dresses`
- Twenty published non-primary locales:
  `ar`, `cs`, `da`, `de`, `el`, `es`, `fi`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `nl`, `no`, `pl`, `pt-BR`, `ro`, `ru`, and `sv`.
- Product translation values only. Product status, publication/channel scope, price, variants, inventory, theme assets, app settings, feeds, campaigns, billing, and credentials were not changed.

## Root Cause

The original Ivory Meadow listing translation poll ran before the product met the worker's minimum-age delay and processed zero products. The later narrow size-chart repair created localized `body_html` values from the English source body while translating only deterministic labels and table text. Those hybrid bodies were current in Shopify, so later normal worker runs skipped them. The first `--force-refresh` implementation also preserved existing hybrid bodies because the existing-body repair path ran before translation.

The repair now:

- refuses to create a missing localized body from the English source in the size-chart-only script;
- makes `--force-refresh` translate the full source body before deterministic repairs;
- installs the automatic worker with both `--force-refresh` and `--execute`;
- requires an Admin translation-completeness audit before the size-chart and public storefront gates;
- audits Size + Color listings instead of silently returning zero variant checks;
- maps Shopify `pt-BR` to the public `/pt` route.

## Before And After

| Readback | Before | After |
|---|---:|---:|
| Products checked | 6 | 6 |
| Published locales checked | 20 | 20 |
| Eligible Admin translation slots | 3,880 | 3,880 |
| Missing translations | 140 | 0 |
| Outdated translations | 100 | 0 |
| Product-body language issues | 120 | 0 |
| Total Admin translation issues | 360 | 0 |
| Products with Admin translation issues | 6 | 0 |

The approved execution registered `360` translation values across `18` product-owned resources: `60` values per product, with zero failures.

## Product And Size-Chart Verification

- Admin translation audit: `0` missing, `0` outdated, `0` source-equal, `0` body-language issues.
- Localized size-chart strict readback: `6` products scanned, `6` with source charts, `0` missing, `0` planned, `0` errors.
- Variant mapping readback: `1,120` variant-locale checks, `0` unmatched.
- Automatic LaunchAgent readback: installed, loaded, `--force-refresh` and `--execute` present, latest exit code `0`.

## Public Storefront Verification

- All `120` recent-product locale routes returned successfully.
- The raw public HTML audit fell from `6,493` to `5,478` findings after the product translation repair.
- The remaining raw findings are identical by locale across all six products and belong to shared theme/runtime or third-party widget surfaces, not product-owned translation bodies.
- Spanish has `36` raw findings total, all Judge.me review strings. The live browser renders the widget in Spanish.
- Live Ivory Meadow Spanish browser readback passed at desktop `1440 x 1000` and mobile `390 x 844`: `lang=es`, Spanish product description present, and none of the reported English product-body phrases present.
- Live French and Portuguese Ivory Meadow product-body samples also contained no reported English product-body phrases; Portuguese correctly resolves at `/pt` with `lang=pt-BR`.

## Quality Boundary

This repair verifies translation completeness, freshness, absence of detected source-language leakage in product-owned content, size-chart preservation, and representative rendered storefront behavior. Automated machine translation across twenty locales is not a substitute for native-editor review of literary fluency. Shared theme/runtime and widget localization findings remain a separate follow-up surface.

## Evidence Files

- `before_admin_translation_audit.json` / `.csv`
- `after_admin_translation_audit.json` / `.csv`
- `translation_dry_run_v2.jsonl`
- `translation_execute.jsonl`
- `size_chart_readback.json` / `.csv`
- `variant_mapping_readback_v2.json` / `.csv`
- `before_public_language_audit.json` / `.csv`
- `after_public_language_audit.json` / `.csv`

