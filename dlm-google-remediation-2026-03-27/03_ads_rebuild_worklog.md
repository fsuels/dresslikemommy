# Ads Rebuild Worklog

Status: no ads deployment changes made in this inventory pass.

## Local evidence captured

- Active Google-related runtime references are limited to:
  - storefront GTM container loading in `layout/theme.liquid`
  - storefront fallback GA4 configuration in `layout/theme.liquid`
  - checkout GTM loader reference file in `ops/customer-events/ga4-checkout-ecommerce-pixel.js`
- No active local code/deployment hits were found for:
  - `GT-PJ5D7RB`
  - `AW-853411529`
  - `googleadservices.com`

## External dependencies still to review

- GTM container workspace contents for `GTM-5QVH4W3`
- Shopify Web Pixels
- Google Ads account tag/linker configuration
- Any app-managed or channel-managed Google tag injections

## Phase 1 repo status

Updated: 2026-03-27 16:42:14 EDT

- Removed duplicate Google runtime code from `layout/theme.liquid`.
- Neutralized the repo-stored Google custom-pixel deployment file at `ops/customer-events/ga4-checkout-ecommerce-pixel.js`.
- Remaining Ads-governance dependencies are now primarily browser/admin-side:
  - remove legacy checkout Ads snippets
  - remove GTM Google tags / linker if no longer needed
  - confirm the Google & YouTube app is the only active Google deployment path
