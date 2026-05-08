# Profit Growth Execution Sprint

Date: 2026-05-06

## Scope

Owner asked for aggressive but controlled marketing execution across the website, Google Ads, Pinterest, and growth planning.

This sprint used subagents for read-only CRO, paid-media, and feed/SEO audits, then made local theme/CRO and landing-page quality changes. Live ad platforms were read back only. No live campaign status, budget, bid, product scope, product group, feed label, conversion goal, Merchant Center, Shopify product, Pinterest campaign, or theme publish action was changed.

## Local CRO and Landing-Quality Changes

- Added matching-set clarity beside the product Add to Cart flow for matching products:
  - Reuses existing translated `products.product.matching_set.heading` and `copy` strings.
  - Explains that shoppers choose one size per family member and each selection adds a separate item.
- Added the shipping-options trust item into the PDP trust strip near Add to Cart.
- Changed paid-facing homepage trust language from blanket free-shipping claims to checkout-safe shipping language:
  - `Shipping options shown at checkout`
  - `secure checkout`
  - `helpful sizing support`
- Removed unsupported/operator-facing homepage copy such as `Lead with...`, `newest 19`, and `$100+` express-shipping threshold language in the key English/Spanish/French/German/Danish paid-readiness surfaces.
- Added SEO alias handling for paid nonbrand landing handles so these URLs inherit strong existing collection SEO:
  - `/collections/mother-daughter-matching-dresses`
  - `/collections/daddy-and-me`
  - `/collections/family-pajamas`

## Live Readbacks

### Google Ads

Account: `399-097-6848 dresslikemommy.com`

Date range visible in UI: `Last 7 days`, `Apr 29 - May 5, 2026`.

`DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` / `23802638621`
- Status: `Enabled`
- Budget: `$20.00/day`
- Type: `Shopping`
- Optimization score: `61.6%`
- Clicks: `81`
- Impressions: `3,906`
- Avg CPC: `$0.23`
- Cost: `$18.58`
- Conversions: `0.00`
- Products tab still shows visible products as `Eligible (limited)` with `Missing age group`.

`DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` / `23805046526`
- Status: enabled campaign row in campaign readback.
- Budget: `$2.00/day`
- Bid strategy status: `Bid strategy learning`
- Type: `Search`
- Clicks: `9`
- Impressions: `10`
- Avg CPC: `$0.14`
- Cost: `$1.30`
- Conversions: `0.00`
- Ads tab: two active RSAs read `Eligible / Average`; one old RSA remains `Paused / Poor`.

`DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506` / `23827590655`
- Status: `Paused`
- Budget: `$2.00/day`
- Type: `Search`
- Manual CPC posture from prior packet remains the launch control.
- Ads tab: RSAs still `Paused` and `Pending`, with campaign/ad groups paused.
- No live nonbrand spend.

`Remarketing - Cart Abandoners & Checkout Starters` / `23609373008`
- Status: `Paused`
- Budget: `$1.00/day`
- Type: `Display`
- Clicks/impressions/cost/conversions: `0`
- Ads tab with `Ad status: All` still shows old removed clickbait-policy RDAs, plus the clean non-removed RDA reading `Not eligible / Campaign is paused`.

### Pinterest

Advertiser: `Dress Like Mommy | Matching Family Outfits`

- Event Quality page still reads `Fair`.
- Health score updated timestamp still reads `5/4/2026`.
- Visible issues remain:
  - `Product ID` in `Add Payment Info`
  - `Click ID` in `Checkout`
  - `Email` in `Add to Cart`
- Interpretation: Shopify official Pinterest app pixel is now set to Always On and checkout pixel blocking was fixed earlier, but Pinterest's quality score has not refreshed enough to justify live Pinterest spend.

## Decisions

- Do not enable Pinterest spend yet.
- Do not enable the paused nonbrand Search rebuild while RSAs still read `Pending`.
- Do not enable Remarketing until a fresh readback filters/ignores removed ads and confirms the active non-removed RDA path is clean.
- Do not keep judging Standard Shopping only by historical Apr 29-May 5 CPC because child bids were lowered previously and the UI date range did not switch to May 6 only. Still, the campaign remains the highest current waste-risk surface because it shows spend, `0.00` conversions, and visible live Merchant `Missing age group` limitations.
- Treat the live Merchant age-group limitation as the next feed-quality repair gate, not a product-scope expansion.

## Exact Approval Gates Prepared

### Publish Local CRO Theme Changes

`APPROVE THEME CRO PUSH ONLY: PUSH THE LOCAL CRO/SHIPPING-CLARITY/COLLECTION-SEO CHANGES TO A THEME PREVIEW FIRST; DO NOT PUBLISH LIVE UNTIL I REVIEW THE PREVIEW; NO SHOPIFY PRODUCT, FEED, ADS, PIXEL, OR CAMPAIGN CHANGES.`

### Standard Shopping Waste Control

Use only after a fresh date-range readback confirms post-bid-change clicks/cost are still inefficient with no purchase value:

`APPROVE PAUSE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY WITH NO PRODUCT SCOPE, FEED LABEL, PRODUCT GROUP STRUCTURE, BUDGET, MERCHANT, SHOPIFY, OR CONVERSION GOAL CHANGES.`

Conservative alternative:

`APPROVE REDUCE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY TO $1/DAY WITH NO PRODUCT SCOPE, FEED LABEL, PRODUCT GROUP STRUCTURE, MERCHANT, SHOPIFY, OR CONVERSION GOAL CHANGES.`

### Merchant Age-Group Repair Readback

`APPROVE MERCHANT AGE_GROUP READBACK AND REPAIR PLAN ONLY: READ BACK PAID-COHORT AGE_GROUP, GENDER, SIZE, COLOR, ITEM_GROUP_ID, AND GOOGLE PRODUCT CATEGORY SOURCES FOR HIGHEST-CLICK LIMITED PRODUCTS; PREPARE A REPAIR PACKET; NO MERCHANT UPLOAD, FEED RULE, SHOPIFY PRODUCT, PRODUCT SCOPE, CAMPAIGN, BUDGET, BID, OR CONVERSION-GOAL CHANGES.`

### Remarketing Enable Gate

`APPROVE ENABLE REMARKETING - CART ABANDONERS & CHECKOUT STARTERS AT $1/DAY ONLY IF FRESH READBACK SHOWS THE ACTIVE NON-REMOVED AD PATH IS POLICY CLEAN; KEEP AUDIENCES, ALL CONVERTERS EXCLUSION, FEED FILTER, OPTIMIZED TARGETING OFF, BUDGET, AND CONVERSION GOALS UNCHANGED.`

### Nonbrand Search Enable Gate

Use only after RSAs clear review:

`APPROVE ENABLE DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506 AT $2/DAY; KEEP MANUAL CPC AT $0.15, EXACT/PHRASE ONLY, CURRENT NEGATIVES, US-ENGLISH TARGETING, ACCOUNT-DEFAULT PURCHASE GOALS, AND NO PMAX, SHOPPING, PRODUCT SCOPE, OR CONVERSION-GOAL CHANGES.`

### Brand Search RSA Quality Repair

`APPROVE BRAND SEARCH RSA QUALITY REPAIR ONLY: READ BACK CURRENT BRAND ADS, EDIT OR ADD BRAND SEARCH RSA TEXT TO IMPROVE AD STRENGTH, KEEP BUDGET AT OR BELOW $2/DAY, KEEP CPC CAP/BID STRATEGY/TARGETING/CONVERSION GOALS UNCHANGED, NO IMAGE/LOGO/PRICE ASSET UPLOAD.`

### Pinterest Paused Catalog Draft

Use only after Pinterest Event Quality refresh improves:

`APPROVE PINTEREST PAUSED US CATALOG TEST DRAFT ONLY: CREATE OR PREPARE PAUSED US-ONLY PRODUCT-GROUP CAMPAIGN STRUCTURE FOR MOMMY & ME, FAMILY MATCHING, AND PAJAMAS; KEEP ALL ADS PAUSED; NO LIVE SPEND, NO BROAD INTERNATIONAL TARGETING, NO PERFORMANCE+ ALL-PRODUCTS LAUNCH.`

## Verification

- `shopify theme check` passed with `261 files inspected with no offenses found`.
- `git diff --check` passed.
- JSON parse passed for:
  - `templates/index.json`
  - `locales/en.default.json`
  - `locales/es.json`
  - `locales/fr.json`
  - `locales/de.json`
  - `locales/da.json`
- Paid-facing stale-copy scan returned no matches for:
  - `Free shipping on all orders`
  - `FREE Shipping`
  - `$100+`
  - `Lead with`
  - `purchase-tracked`
  - `proving they convert`

## Decision

`LOCAL_CRO_AND_LANDING_QUALITY_PATCH_COMPLETE__LIVE_GOOGLE_ADS_PINTEREST_READBACKS_DONE__NO_LIVE_SPEND_OR_FEED_CHANGES__MERCHANT_AGE_GROUP_AND_STANDARD_SHOPPING_WASTE_CONTROL_ARE_NEXT_PROFIT_GATES`.
