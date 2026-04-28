# LOCAL_SHOPIFY_EXPORT_DESCRIPTION_v2

Generated: 2026-04-28
Mode: local dry-run only. No deploy. No Shopify writes.

## Source Evidence

- Current theme repository at `/Users/fsuels/Projects/dresslikemommy`.
- Existing local Shopify export: `dresslikemommy-growth-2026/01_EXPORTS_RAW/SHOPIFY/2026-04-28_LOCAL_SHOPIFY_EXPORT_raw.json`.
- Existing local v1 analysis CSVs under `dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/`.
- Existing live digest map: `ops/content/shopify-live-digest-map.json`.

## Generated Files

- `2026-04-28_LOCAL_SHOPIFY_PACKET_v2.md`
- `2026-04-28_LOCAL_SHOPIFY_EXPORT_DESCRIPTION_v2.md`
- `2026-04-28_LOCAL_SHOPIFY_ARTIFACTS/`

## Artifact Notes

All artifacts are local-only. Dry-run diffs are patch text for review, not applied changes. CSVs are analysis/export files only and must not be uploaded without explicit owner approval.

Key counts:

- Active products read from local export: 335
- Active variants read from local export: 7324
- Policy copy hits: 2547
- Missing unit-cost rows: 5928
- Missing SKU rows: 1604
- Missing barcode/GTIN rows: 5897
- Missing color/size/gender/age_group defect rows: 388
- Custom-label rows: 7324

## Privacy And Safety

No customer PII, tokens, secrets, or credentials were exported. No Shopify Admin mutation was run. No live theme/page/feed write was run.

## Verification

- Local source files were scanned for requested terms.
- Existing local Shopify export JSON was parsed successfully.
- Generated CSVs were written with headers.
- Theme Check was run separately in this session and passed with 251 files inspected and no offenses.
