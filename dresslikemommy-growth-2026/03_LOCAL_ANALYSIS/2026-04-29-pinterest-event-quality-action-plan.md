# Pinterest Event Quality Action Plan

Generated: 2026-04-29
Store: dresslikemommy.com / dresslikemommy-com.myshopify.com
Pinterest ad account: 549756244483

## Verdict

The outside plan is directionally right about the four Pinterest Event Quality gaps, but its custom implementation path is not the right first move for this store.

The store already uses the official Shopify Pinterest channel/app pixel. Adding a second hand-coded Pinterest tag, a custom Shopify customer event pixel, or a client-side CAPI call would likely create duplicate events and could expose tokens or bypass the current consent architecture. The first path should be the official Pinterest app/channel plus Pinterest Ads Event Manager settings/support. A custom server-side CAPI integration should be treated as a fallback only after official-channel limits are confirmed.

## Evidence

- Pinterest Event Quality still reports `Fair`, updated 2026-04-27, with these gaps:
  - Email for `AddToCart`.
  - Click ID for `Checkout`, `AddToCart`, `InitiateCheckout`, `AddPaymentInfo`, `PageVisit`, `Search`, and `ViewCategory`.
  - Product ID for `AddPaymentInfo`.
  - Event ID for `PageVisit`.
- Pinterest Events Overview currently shows both `Api` and `Tag` sources for `PageVisit`, `ViewCategory`, `AddToCart`, `InitiateCheckout`, `Search`, `Checkout`, and `AddPaymentInfo`.
- Shopify Admin evidence confirms the official Pinterest app/channel is installed:
  - App: `Pinterest`
  - App ID: `gid://shopify/App/3009811`
  - Handle: `pinterest-4`
  - Developer: `PINTEREST inc`
  - Publication: `gid://shopify/Publication/76582879329`
  - Channel: `Pinterest`
  - Important scopes include `read_customer_events`, `read_pixels`, `write_pixels`, `read_product_feeds`, and `write_product_feeds`.
- Live storefront Web Pixels Manager has a Pinterest app pixel:
  - Type: `APP`
  - Runtime: `STRICT`
  - `apiClientId`: `3009811`
  - `tagID`: `2620007050621`
  - `dataSharingState`: `optimized`
  - Privacy purposes: `ANALYTICS`, `MARKETING`, `SALE_OF_DATA`
- Pinterest Ads tag page shows:
  - Tag name: `conversion_tracker (2620007050621)`
  - Latest event: Apr 29, 2026 02:15 UTC
  - Automatic enhanced match: `Enabled`
- Shopify Pinterest app marketing settings show:
  - Ad account: `549756244483`
  - Pinterest tag and Conversions API are automatically set up for the store.
  - Pinterest tag for Shopify: `2620007050621`
- Theme code has no hand-rolled `pintrk(...)` call. `layout/theme.liquid` initializes `window.dataLayer` and lazy-loads `assets/analytics.js`; `assets/analytics.js` emits GA4-style dataLayer events only.
- Theme code does not own hosted checkout events such as `payment_info_submitted`, `checkout_completed`, or payment-step CAPI payloads.
- Shopify consent policy readback confirms EEA/UK-style opt-in regions and US state sale-of-data opt-out regions are configured. Shopify's privacy banner gate is present in `layout/theme.liquid`.

## Decisions

1. Keep the official Pinterest Shopify channel as the source of truth.
2. Do not add a duplicate theme-level Pinterest tag.
3. Do not put a Pinterest CAPI token in theme JavaScript, Shopify custom pixel JavaScript, or any repo file.
4. Do not build a Shopify Function for Pinterest CAPI. Shopify Functions are not the right server-to-server transport for this job.
5. Do not create a custom CAPI backend unless Pinterest support or official-app testing proves the Shopify Pinterest channel cannot pass the required fields.

## Action Plan

### Phase 1 - Official Integration Verification

Status: mostly completed in this pass.

- Confirm the Pinterest Shopify app is connected to ad account `549756244483`.
- Confirm the live tag ID is `2620007050621`.
- Confirm Pinterest Tag and Conversions API are automatically set up by the Shopify app.
- Confirm Automatic Enhanced Match is enabled in Pinterest Ads Manager.
- Confirm the live storefront still loads the Pinterest app pixel through Shopify Web Pixels Manager.

### Phase 2 - Event Quality Re-test

Run this before any custom development.

- In Pinterest Ads Manager, open Conversions -> Test events.
- Use a real browser session from a Pinterest click URL when possible, so an `epik` value or `_epik` cookie exists.
- Trigger:
  - Page visit
  - Product view
  - Collection/view category
  - Search
  - Add to cart
  - Initiate checkout
  - Add payment info
  - Checkout/purchase
- Verify whether the received `Api` and `Tag` events include:
  - Matching `event_id` for PageVisit.
  - `click_id` when the session has an `epik`/`_epik` value.
  - Hashed email where the user is logged in or has supplied checkout/contact email and consent allows sharing.
  - `content_ids` on `AddPaymentInfo`.

### Phase 3 - Escalate Through Official Channels If Gaps Persist

If Test Events still show missing fields while the official app is active, open a Pinterest/Shopify support ticket with this exact evidence:

- Shopify app `Pinterest` is installed and connected.
- App pixel tag ID is `2620007050621`.
- Pinterest Ads Manager says Automatic Enhanced Match is enabled.
- Pinterest Shopify app says Tag and Conversions API are automatically set up.
- Event Quality gaps remain for Click ID, AddToCart email, AddPaymentInfo product ID, and PageVisit event ID.
- Events Overview shows `Api + Tag` for the affected events.

Ask whether the official Shopify Pinterest integration currently supports:

- Passing `_epik`/`epik` into CAPI `user_data.click_id`.
- Deduplicating PageVisit by sharing the same `event_id` between Tag and CAPI.
- Passing checkout line item IDs on `AddPaymentInfo`.
- Passing hashed email for AddToCart when Shopify customer/contact email is available and consent permits it.

### Phase 4 - Custom Backend Only If Official App Cannot Fix It

Build this only if Phase 3 proves the official app cannot provide the fields.

Requirements:

- A real server-side app/proxy endpoint holds the Pinterest CAPI token.
- The browser/customer-event pixel never contains the CAPI token.
- Consent is checked before sending marketing identifiers or hashed email.
- Browser tag and server event share a generated UUID for deduplication.
- `_epik`/`epik` is captured only when consent permits and sent as `user_data.click_id`.
- Emails are lowercased, trimmed, SHA-256 hashed, and sent only as hashes.
- `payment_info_submitted` uses Shopify checkout line items to populate `custom_data.content_ids`.
- The official Pinterest app's duplicate browser/server events must be disabled, scoped, or proven deduped before custom events go live.

## Current Recommendation

Do not ship custom Pinterest code today. The strongest, lowest-risk next action is a controlled Pinterest Test Events pass using the current official Shopify Pinterest integration, followed by support escalation if the same fields are missing in real event payloads.

## Rollback

No live settings or theme code were changed by this plan. If a later custom integration is built, rollback must include disabling that custom pixel/backend route and returning event ownership to the official Shopify Pinterest channel.
