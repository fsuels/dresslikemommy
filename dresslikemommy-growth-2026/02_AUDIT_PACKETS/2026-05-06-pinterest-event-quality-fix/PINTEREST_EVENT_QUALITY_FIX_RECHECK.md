# Pinterest Event Quality Fix/Recheck

Generated: 2026-05-06

## Scope

Owner request:

- Wait/recheck Google Ads Remarketing policy status later today.
- In parallel, fix Pinterest event-quality gaps, especially Checkout click ID and purchase/product/value parameters.

Guardrails preserved:

- No Pinterest campaigns created, enabled, or funded.
- No Google Ads campaign status, budget, conversion-goal, audience, product-scope, or feed edits.
- No duplicate theme-level Pinterest tag.
- No custom Pinterest CAPI token/code in theme, custom pixel, or repo.
- No Shopify product/feed edits.

## Official Guidance Used

- Shopify recommends app pixels from integrated marketing/data apps when available because they provide higher security and automatic updates: https://help.shopify.com/en/manual/promoting-marketing/pixels
- Pinterest Tag documentation says checkout event data should include dynamic `value`, `currency`, `event_id`, and line-item product data for product-level context: https://developers.pinterest.com/docs/track-conversions/pinterest-tag/
- Pinterest Conversions API documentation says `event_id` is used for deduplicating API and tag events, `event_source_url` can include `epik`, and `user_data.click_id` should use the `_epik` cookie for coverage: https://developers.pinterest.com/docs/track-conversions/track-conversions-in-the-api/
- Pinterest CAPI setup guidance recommends dual Tag + CAPI integration and deduplication parameters, with events shared close to real time: https://help.pinterest.com/en-gb/business/article/getting-started-with-the-conversions-api
- Shopify App Store listing for the Pinterest app states the app tracks performance with the Pinterest Tag and improves tracking/performance with the Pinterest Tag and API for Conversions: https://apps.shopify.com/pinterest

## Pinterest Ads Readback

Live UI: `https://ads.pinterest.com/advertiser/549756244483/conversions/health/`

Readback:

- Account/site: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Event Quality updated: `5/4/2026`
- Event source: `Conversions API` and `Pinterest Tag`
- Date range available: `Last 14 days`, `Last 1 day`
- Event quality score: `Fair`

Top action items:

1. `Product ID` in `Add Payment Info`
2. `Click ID` in `Checkout`
3. `Email` in `Add to Cart`

Details opened in Pinterest Ads:

- `Product ID` / `Add Payment Info`: coverage `0%`, issue `Product ID not set up`.
- `Click ID`: coverage `0%` for `Checkout`, `Add to Cart`, `Initiate Checkout`, `Add Payment Info`, `Page Visit`, `Search`, and `View Category`.
- `Email` / `Add to Cart`: coverage `5%`, issue `Low Email coverage`.
- Duplicate-event health shows `Event ID` in good health for `Page Visit` and `View Category`.

Events overview readback:

- `PageVisit`: `Api · Tag`, `19,656`, last received `5/6/2026 06:53am UTC`
- `ViewCategory`: `Api · Tag`, `4,131`, last received `5/6/2026 05:06am UTC`
- `AddToCart`: `Api · Tag`, `679`, last received `5/6/2026 05:28am UTC`
- `InitiateCheckout`: `Api · Tag`, `118`, last received `5/6/2026 05:29am UTC`
- `Search`: `Api · Tag`, `40`, last received `5/2/2026 07:07am UTC`
- `Checkout`: `Api · Tag`, `23`, last received `5/6/2026 05:29am UTC`
- `AddPaymentInfo`: `Api · Tag`, `21`, last received `5/6/2026 05:29am UTC`

Campaign gate:

- Reporting dashboard still showed `0 campaigns`, `0 currently being served`, `$0.00` spend in the prior Pinterest gate.
- Because no Pinterest campaigns are serving, most site events will naturally lack a real Pinterest ad click cookie. This explains why `Click ID` coverage can be `0%` even when events are otherwise firing.

## Fresh Storefront/Checkout Diagnostic

Test:

- Cleared cart.
- Loaded product URL with synthetic Pinterest click parameter:
  `https://www.dresslikemommy.com/products/red-resort-mommy-and-me-set?epik=dlm_test_20260506T105635Z&utm_source=pinterest&utm_medium=test_events&utm_campaign=pinterest_event_quality_recheck_20260506`
- Added variant `44116578467937`.
- Clicked checkout.
- Stopped on checkout contact page; no payment or order was submitted.

Result:

- Checkout opened successfully.
- Browser cookies after the test contained `_pin_unauth` only; no `_epik` cookie was present from the synthetic parameter.
- This synthetic test cannot prove real Pinterest ad-click `click_id` handling because Pinterest docs specify the `_epik` cookie generated from ad clicks, and the account has no campaigns currently serving.

Shopify source event evidence:

- Shopify emitted `checkout_started`.
- The source payload had `products_count = 1`.
- Product payload included:
  - `variant_id = 44116578467937`
  - `product_id = 7545373130849`
  - `product_gid = gid://shopify/Product/7545373130849`
  - `name = Red Resort Mommy and Me Set - Tee and Skirt`
  - `price = 28.99`
  - `sku = DLM-RRES-GRL-SET-KID4Y-REDWHT`
  - `quantity = 1`
- Value payload included:
  - `subtotal_value = 28.99`
  - `currency = USD`
- Consent flags visible in the Shopify source event:
  - `analytics_allowed = true`
  - `marketing_allowed = true`
  - `sale_of_data_allowed = true`

Pinterest app pixel evidence:

- Pinterest app pixel ID in Shopify Web Pixels Manager: `22577249`
- Pinterest app ID: `3009811`
- Pinterest tag configuration: `{"tagID":"2620007050621"}`
- The Pinterest app pixel registered on:
  - storefront product page
  - cart page
  - checkout page
- On checkout, Shopify emitted:
  - `web_pixels_manager_subscriber_event_blocked`
  - `event_name = checkout_started`
  - `pixel_id = 22577249`
- The Pinterest app pixel's live data-sharing transform showed:
  - `protectedCustomerApprovalScopes = read_customer_address, read_customer_email, read_customer_name, read_customer_personal_data, read_customer_phone`
  - `dataSharingControls = []`

Interpretation:

- The product/value data exists in Shopify's checkout source event.
- The official Pinterest app pixel is present and registered, but at least the `checkout_started` event is blocked for the Pinterest app in the current live data-sharing state.
- The clean first fix is to change the official Pinterest app pixel in Shopify Customer Events to `Always on` / `share all events`, then rerun the checkout test and Pinterest Event Quality recheck.
- This is not a theme-code fix. Adding a second Pinterest tag or client-side CAPI token would create duplication and token/privacy risk.

## Shopify Admin Blocker

Attempted Shopify Admin UI:

- URL: `https://admin.shopify.com/store/dresslikemommy-com/settings/customer_events`
- Result: browser was not logged into Shopify Admin and showed the Shopify login screen.

Shopify Admin API readback:

- Stored local Admin API token loaded successfully.
- `appByHandle(handle: "pinterest-4")` read back:
  - app ID `gid://shopify/App/3009811`
  - title `Pinterest`
  - handle `pinterest-4`
  - developer `PINTEREST inc`
  - install URL `https://dresslikemommy-com.myshopify.com/admin/apps/pinterest-4`
- The Admin GraphQL API available to this token did not expose a safe mutation for app-pixel data-sharing controls. This appears to require Shopify Admin UI access.

## Required Approval

Safe approval phrase requested from owner:

`APPROVE PINTEREST EVENT QUALITY FIX: IN SHOPIFY CUSTOMER EVENTS, SET ONLY THE OFFICIAL PINTEREST APP PIXEL TO ALWAYS ON / SHARE ALL EVENTS; KEEP OFFICIAL PINTEREST APP TAG+CAPI ONLY; NO CUSTOM PIXEL, NO THEME PINTEREST TAG, NO CAPI TOKEN, NO CAMPAIGN OR SPEND CHANGES.`

After approval/login:

1. Open Shopify Admin > Settings > Customer events.
2. Open the official `Pinterest` app pixel.
3. Change only its data setting to `Always on` / `share all events` if that exact control is available.
4. Save.
5. Rerun the same storefront-to-checkout diagnostic.
6. Confirm the Pinterest app pixel no longer emits `web_pixels_manager_subscriber_event_blocked` for checkout-start/payment/purchase-adjacent events.
7. Recheck Pinterest Event Quality after Pinterest refreshes the health score.

Do not:

- add `pintrk` to theme code,
- add a custom Pinterest customer event pixel,
- add or store a Pinterest CAPI token,
- install a third-party tracking app without a separate duplicate-event migration plan,
- enable Pinterest spend before event quality and catalog gates are clean enough.

## Google Ads Remarketing Recheck

Campaign: `Remarketing - Cart Abandoners & Checkout Starters`

Campaign ID: `23609373008`

Recheck time: 2026-05-06 approximately 06:55 EDT

Campaign table readback:

- Status: `Paused`
- Budget: `$1.00/day`
- Campaign type: `Display`
- Clicks: `0`
- Impressions: `0`
- Cost: `$0.00`
- Conversions: `0.00`
- `Most ads limited by policy`: no longer visible in the campaign row

Ads table readback:

- Clean generic RDA remains:
  - `Dress Like Mommy Styles`
  - `Matching Family Styles From Dress Like Mommy`
  - `Shop matching looks for moms, dads, kids, and families.`
  - Status: `Not eligible`
  - Reason: `Campaign is paused`
- Five old clickbait RDAs remain visible as `Removed` rows with old `Policy (Clickbait), Campaign is paused` history.
- No campaign enablement or Google Ads edits were made.

Interpretation:

- Remarketing policy propagation looks improved at the campaign row level.
- The campaign should still remain paused until owner gives a fresh exact enable approval and one more just-in-time readback confirms only the clean active/non-removed ad is eligible except for the paused campaign state.

## Decision

`PINTEREST_EVENT_QUALITY_ROOT_CAUSE_IDENTIFIED__SHOPIFY_CUSTOMER_EVENTS_PINTEREST_APP_PIXEL_DATA_SHARING_BLOCKS_CHECKOUT_EVENT__SHOPIFY_ADMIN_LOGIN_AND_OWNER_APPROVAL_REQUIRED_FOR_FIX__REMARKETING_POLICY_ROW_CLEARED_BUT_CAMPAIGN_REMAINS_PAUSED`

## Owner-Approved Shopify Customer Events Fix

Approval received:

`APPROVE PINTEREST EVENT QUALITY FIX: IN SHOPIFY CUSTOMER EVENTS, SET ONLY THE OFFICIAL PINTEREST APP PIXEL TO ALWAYS ON / SHARE ALL EVENTS; KEEP OFFICIAL PINTEREST APP TAG+CAPI ONLY; NO CUSTOM PIXEL, NO THEME PINTEREST TAG, NO CAPI TOKEN, NO CAMPAIGN OR SPEND CHANGES.`

Action time: 2026-05-06 approximately 07:12 EDT

Shopify Customer Events pre-edit readback:

- URL: `https://admin.shopify.com/store/dresslikemommy-com/settings/customer_events`
- Page title: `Dress Like Mommy - Customer events - Shopify`
- App pixels table readback:
  - `Facebook & Instagram` = `Connected` / `Optimized`
  - `Google & YouTube` = `Connected` / `Optimized`
  - `Judge.me Reviews` = `Connected` / `Always on`
  - `Microsoft Channel` = `Connected` / `Optimized`
  - `Pinterest` = `Connected` / `Optimized`
  - `TikTok` = `Connected` / `Optimized`

Live change:

- Opened only the `Pinterest` app pixel's `Data access settings`.
- Confirmed current radio state:
  - `Optimized` = checked
  - `Always on` / `UNRESTRICTED` = available and unchecked
- Changed only the `Pinterest` app pixel to `Always on`.
- Clicked `Apply`.
- Shopify showed `Data access updated`.

Post-edit Shopify readback:

- `Pinterest` row read: `Pinterest / Connected / Always on`
- Other app pixel rows remained unchanged in the visible table.
- No custom pixel, theme tag, CAPI token, campaign, spend, product, feed, or Google Ads change was made.

## Post-Fix Storefront-To-Checkout Diagnostic

Diagnostic time: 2026-05-06 approximately 07:13 EDT / 11:13 UTC

Test path:

- Cleared cart.
- Loaded `https://www.dresslikemommy.com/products/red-resort-mommy-and-me-set?epik=dlm_after_fix_20260506111305`
- Added variant `44116578467937`.
- Entered Shopify checkout only. No payment information was entered and no order was placed.
- Cleared the test browser cart after diagnostics; cart read back `item_count = 0`.

Pinterest app pixel results:

- Pixel ID: `22577249`
- App ID: `3009811`
- Tag ID: `2620007050621`
- `web_pixels_manager_subscriber_event_blocked` for Pinterest: `0`
- Pinterest app pixel emitted successfully:
  - `product_viewed` / `SUCCESS` / storefront
  - `page_viewed` / `SUCCESS` / storefront
  - `product_added_to_cart` / `SUCCESS` / storefront
  - `checkout_started` / `SUCCESS` / checkout
  - `page_viewed` / `SUCCESS` / checkout
- Pinterest app pixel data-sharing transform now showed:
  - `dataSharingControls = ["share_all_events"]`
  - on both storefront and checkout surfaces
- Browser cookie readback now included:
  - `_pin_unauth`
  - `_epik`
  - `_derived_epik`

Shopify source checkout event still contained the required product/value data:

- `variant_id = 44116578467937`
- `product_id = 7545373130849`
- `product_gid = gid://shopify/Product/7545373130849`
- `name = Red Resort Mommy and Me Set - Tee and Skirt`
- `price = 28.99`
- `sku = DLM-RRES-GRL-SET-KID4Y-REDWHT`
- `quantity = 1`
- `subtotal_value = 28.99`
- `currency = USD`
- Consent flags:
  - `analytics_allowed = true`
  - `marketing_allowed = true`
  - `sale_of_data_allowed = true`

Interpretation:

- The live Shopify blocker found earlier is fixed for the official Pinterest app pixel.
- Checkout is no longer blocked at the Shopify Web Pixels Manager layer for Pinterest pixel `22577249`.
- Real paid-click Click ID coverage still requires actual Pinterest ad traffic; the synthetic `epik` test confirms the cookie path and data-sharing permission, not real campaign attribution.

## Pinterest Ads Recheck After Fix

Pinterest Event Quality readback:

- URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/health/`
- Account/site: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Event source: `Conversions API` + `Pinterest Tag`
- Event Quality score: `Fair`
- Health score last updated: `5/4/2026`
- Top action items shown after fix:
  1. `Product ID` in `Add Payment Info`
  2. `Email` in `Add to Cart`
  3. `Click ID` in `Checkout`

Pinterest Events Overview readback:

- URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/events-overview/`
- PageVisit: `19,659`, source `Api - Tag`, last received `5/6/2026 06:53am (UTC)`
- ViewCategory: `4,131`, source `Api - Tag`, last received `5/6/2026 05:06am (UTC)`
- AddToCart: `680`, source `Api - Tag`, last received `5/6/2026 11:13am (UTC)`
- InitiateCheckout: `119`, source `Api - Tag`, last received `5/6/2026 05:29am (UTC)`
- Search: `40`, source `Api - Tag`, last received `5/2/2026 07:07am (UTC)`
- Checkout: `23`, source `Api - Tag`, last received `5/6/2026 05:29am (UTC)`
- AddPaymentInfo: `21`, source `Api - Tag`, last received `5/6/2026 05:29am (UTC)`

Interpretation:

- Pinterest's platform health score had not refreshed after the Shopify fix because the score still used the `5/4/2026` update.
- Events Overview immediately reflected the post-fix AddToCart test at `11:13 UTC`.
- Checkout event reporting and Event Quality issue order may lag behind the live Shopify Web Pixels Manager success readback.
- No Pinterest campaign, budget, ad, product group, catalog, CAPI token, or spend change was made.

## Final Decision

`PINTEREST_SHOPIFY_APP_PIXEL_DATA_ACCESS_SET_TO_ALWAYS_ON__CHECKOUT_PIXEL_UNBLOCKED__OFFICIAL_PINTEREST_TAG_AND_CAPI_ONLY__NO_CUSTOM_PIXEL_THEME_TAG_CAPI_TOKEN_CAMPAIGN_OR_SPEND_CHANGES__PINTEREST_EVENT_QUALITY_PENDING_PLATFORM_REFRESH`
