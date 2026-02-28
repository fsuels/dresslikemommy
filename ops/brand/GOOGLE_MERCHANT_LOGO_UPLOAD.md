# Google Merchant Logo Upload Pack

This folder contains Merchant-ready logos prepared for Dress Like Mommy.

## Files to upload

- Rectangular logo (2:1): `ops/brand/dlm-merchant-rectangular-1200x600.png`
- Square logo (1:1): `ops/brand/dlm-merchant-square-1000x1000.png`

## Validation snapshot

- `dlm-merchant-rectangular-1200x600.png`
  - Format: PNG
  - Dimensions: `1200x600`
  - Ratio: `2.0`
  - Size: `285,400` bytes (`~0.27 MB`)
- `dlm-merchant-square-1000x1000.png`
  - Format: PNG
  - Dimensions: `1000x1000`
  - Ratio: `1.0`
  - Size: `205,606` bytes (`~0.20 MB`)

Both are under 5 MB and match the required aspect ratios.

## Merchant Center upload steps

1. Open Merchant Center.
2. Go to `Business info` (or `Tools and settings` -> `Business info` depending on UI version).
3. Open `Branding` / `Logo`.
4. Upload:
   - Rectangular slot: `dlm-merchant-rectangular-1200x600.png`
   - Square slot: `dlm-merchant-square-1000x1000.png`
5. Save changes.
6. Return to `Products` -> `Diagnostics` and recheck after sync/review.

## If issue persists after upload

Update Shopify brand assets too (Google can read from connected brand data):

1. Shopify Admin -> `Settings` -> `Brand`.
2. Replace both logo variants with the same two files above.
3. Save and let the Google & YouTube app re-sync.

## Search Console association path (if needed)

If Merchant Center asks to associate Search Console:

1. Open Google Search Console for your verified property.
2. Go to `Settings` -> `Associations`.
3. Add association for Merchant Center account.

