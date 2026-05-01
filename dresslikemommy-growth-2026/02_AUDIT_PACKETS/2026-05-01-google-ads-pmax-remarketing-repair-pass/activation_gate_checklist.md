# Activation Gate Checklist - PMax And Remarketing

## Applies To

- `PMax: Shopping ads (United States)`
- `PMax: USA Google Shopping T-Shirts`
- `Remarketing - Cart Abandoners & Checkout Starters`

## Global Gates

- Campaign is still paused before gate starts.
- Budget readback is exact and owner-approved.
- Conversion action readback confirms purchase value, currency, transaction ID, and deduplication.
- No supplier/source URLs appear in feed-visible or customer-visible product fields.
- Location targeting is United States with presence-only option where available.
- URL suffix/tracking is present or intentionally documented.
- Rollback trigger and rollback owner decision are documented.

## PMax Specific Gates

- Correct Merchant Center is `124884876 - Dresslikemommy`.
- Product scope is non-overlapping with Standard Shopping and any other PMax.
- Product cohort has exact count, item IDs/export, clean eligibility, and no supplier/source-domain exposure.
- Product economics prove the test can meet CAC/ROAS constraints.
- Final URL expansion is off or URL allowlisted to safe `/collections/` and `/products/` paths.
- Brand exclusion/brand traffic plan is documented so PMax does not cannibalize Brand Search.
- Asset group copy is product-specific and claim-safe.
- Audience signals and search themes are present.
- Ad strength is not `Poor`.

## Remarketing Specific Gates

- Existing clickbait-limited ads are paused or replaced.
- New responsive display ads are eligible or pending review without clickbait policy errors.
- Cart/checkout audiences are eligible or the campaign remains blocked.
- Past purchasers/converters are excluded.
- Dynamic remarketing/feed linkage is verified or intentionally held.
- Frequency/content controls are documented.
- Optimized targeting/audience expansion posture is documented.

## Current Gate Result

`BLOCKED_NOT_READY_TO_ENABLE`

Reason:
- PMax Shopping United States has wrong/no-product source risk.
- PMax T-Shirts lacks verified T-shirt-only product economics and has weak assets.
- Remarketing has policy-limited ads and ineligible audiences.

