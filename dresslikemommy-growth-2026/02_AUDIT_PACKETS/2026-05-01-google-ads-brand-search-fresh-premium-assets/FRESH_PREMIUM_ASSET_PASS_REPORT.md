# Brand Search Fresh Premium Asset Pass

Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` / `23805046526`

Decision: `FRESH_PREMIUM_ASSETS_UPLOAD_READY_PENDING_OWNER_APPROVAL`

## What Changed

- Superseded the prior reused-image recommendation set.
- Created a fresh-from-scratch premium image asset set for Brand Search.
- Kept the logo asset tied to the official Dress Like Mommy brand mark; do not invent a replacement logo for live ads.
- Preserved proof-backed price assets from current storefront/product readbacks.
- Deferred promotion assets because no current storefront-visible promo code or percent/amount-off offer was verified.

## Recommended Image / Logo Assets

Upload-ready files live in `recommended-assets/`:

- `dress-like-mommy-official-logo-square-1200.png`
- `mommy-me-boardwalk-square-1200.jpg`
- `mommy-me-boardwalk-landscape-1200x628.jpg`
- `family-garden-square-1200.jpg`
- `family-garden-landscape-1200x628.jpg`
- `family-coastal-landscape-1200x628.jpg`

Manifest:

- `fresh_premium_asset_upload_manifest.csv`

Visual QA:

- `fresh-premium-assets-contact-sheet.jpg`

## Expert Guardrails

- The image assets are new AI-generated creative, not old website/theme/product images.
- The image assets contain no text overlay, no logo overlay, no supplier/source references, and no unsupported promotional claims.
- The creative is category-representative, not exact-SKU photography. Before live upload, owner should approve that this representation is acceptable for the storefront assortment.
- The official logo export is intentionally not a new invented logo. Brand Search ROI depends on instant brand recognition and storefront consistency.

## Price Assets

Price rows copied into this packet:

- `price_asset_upload_rows.csv`
- `product_price_evidence.csv`

Recommended rows remain proof-backed:

- Mommy & Me Outfits: from `$16.99`
- Matching Dresses: from `$26.99`
- Family Matching Sets: from `$19.99`
- Matching Swimwear: from `$14.99`
- Family Matching Tees: from `$16.99`

## Promotion Asset

Do not create a promotion asset yet.

Reason: no current storefront-visible promo code or percent/amount-off offer was verified. Free standard shipping is real, but should stay as callout/copy unless the Google Ads promotion workflow supports it and policy proof is reviewed at upload time.

Evidence:

- `promotion_asset_decision.csv`

## Live Google Ads Status

No live Google Ads changes were made in this pass.

Reason: uploading/associating Google Ads assets creates live ad creative that can be shown to shoppers, so it needs owner action-time approval after review of the new creative set. The campaign budget, bidding, conversion goals, keywords, negatives, audiences, and other campaigns were not touched.

## Next Exact Approval

If the owner wants these uploaded, the clean approval phrase is:

`APPROVE UPLOAD BRAND SEARCH FRESH IMAGE LOGO AND PRICE ASSETS ONLY; KEEP BUDGET AT $5/DAY; NO PROMOTION ASSET`

