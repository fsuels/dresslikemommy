# Measurement Repair Execution Readback - 2026-05-15

Status: `PARTIAL_EXECUTION_GOOGLE_ADS_NATIVE_ACTION_CREATED__SHOPIFY_GA4_BROWSER_WRITES_BLOCKED`

## Goal

Repair the broken paid-growth measurement path so Shopify orders can be evaluated correctly in Google Ads, GA4, and Pinterest.

The immediate business problem is that Shopify orders and GA4/Google Ads purchase reporting diverged badly. The Google & YouTube app pixel is still present on the storefront, but GA4 purchase reporting is not trustworthy enough for paid-growth decisions.

## Actions completed

### Google Ads native purchase conversion action

Created a new Google Ads website conversion action through Google Ads API v22.

Readback:

- Customer: `399-097-6848`
- Resource: `customers/3990976848/conversionActions/7612074463`
- Name: `Purchase - Shopify Custom Pixel native`
- Type: `WEBPAGE`
- Category: `PURCHASE`
- Status: `ENABLED`
- Primary for goal: `false` (Secondary during validation)
- Include in conversions metric: `false`
- Counting type: `MANY_PER_CLICK` (Every conversion)
- Value settings:
  - default value: `0`
  - default currency: `USD`
  - always use default value: `false`
- Click-through lookback: `30`
- View-through lookback: `1`
- Attribution model: `GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN`

The conversion ID and label were read back from the tag snippets and written only to a non-repo install copy:

- `/Users/fsuels/.config/dresslikemommy/pixels/google-ads-custom-pixel.install.js`

The repo template still keeps placeholders:

- `pixels/google-ads-custom-pixel.js`

### Shopify public storefront pixel readback

Fetched `https://www.dresslikemommy.com/` and inspected the Shopify Web Pixels config.

Readback:

- Web Pixels Manager present: yes
- Google & YouTube app pixel still present: yes
- GA4 measurement ID in app pixel config: `G-N4EQNK0MMB`
- Google Ads tag ID in app pixel config: `AW-853411529`
- Pinterest app pixel present: yes (`tagID` present)
- Custom Pixel install visible on public storefront: no configured custom pixel was visible in the fetched `webPixelsConfigList`

Interpretation:

- The old Google & YouTube app pixel is still active.
- The new repo Custom Pixels are not yet live in Shopify Customer events.
- Pinterest tag/app pixel exists, but this does not prove catalog grouping or purchase/event quality.

## Blocked live actions

### Shopify Custom Pixel paste/connect

Blocked because browser automation hit Shopify login, Chrome DevTools profile was locked, and Computer Use timed out before reading Chrome.

Current safe state:

- No Shopify Customer events Custom Pixel was pasted, saved, connected, disconnected, or toggled by this automation pass.

Next unblock:

- Use an authenticated Shopify Admin browser session to paste/connect:
  - `pixels/ga4-custom-pixel.js` after replacing the GA4 secret only inside Shopify or a non-repo temp copy.
  - `/Users/fsuels/.config/dresslikemommy/pixels/google-ads-custom-pixel.install.js` for the native Ads pixel.

### GA4 Measurement Protocol API secret

Blocked because the available `gcloud` token returns `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT` for GA4 Admin API. The Google Ads OAuth refresh token is scoped only to `https://www.googleapis.com/auth/adwords`, so it cannot create GA4 API secrets.

Current safe state:

- No GA4 Measurement Protocol API secret was created.
- No GA4 setting was changed.

Next unblock:

- Use an authenticated GA4 browser session for property `330266838`, or provide a current-session OAuth path with GA4 Admin edit scope, then create the Measurement Protocol API secret and install the GA4 Custom Pixel.

### Google & YouTube app pixel GA4 toggle

Blocked because this is a Shopify Admin UI action and requires authenticated browser access.

Current safe state:

- Google & YouTube channel/app pixel remains connected.
- Merchant Center feed path remains untouched.

Next unblock:

- In Shopify Admin -> Settings -> Customer events -> App pixels -> Google & YouTube, disable only the GA4 analytics sub-toggle if the UI exposes it separately. Do not disconnect the Google & YouTube sales channel.

### Pinterest measurement/catalog

Public storefront readback shows the Pinterest app pixel/tag is present. However, Pinterest catalog correctness is still blocked by the existing all-market feed grouping issue: generated grouped feeds pass locally, but upstream/live-equivalent snapshots still fail until the live channel/source is repaired and read back.

Current safe state:

- No Pinterest campaign, catalog, source, product group, tag, CAPI, budget, bid, or status write occurred.

Next unblock:

- First finish measurement install/readback for Ads/GA4.
- Then apply the owner-approved Pinterest feed grouping path only with exact before/after source/catalog readback.

## Verification run

- Google Ads conversion action `validateOnly=true` mutate: passed.
- Google Ads conversion action create: passed.
- Google Ads conversion action readback: passed.
- Non-repo Google Ads install copy syntax check: passed with `node --check`.
- Shopify Admin API credential probe: passed for shop `Dress Like Mommy`.
- GA4 Admin API probe: blocked with `ACCESS_TOKEN_SCOPE_INSUFFICIENT`.
- Chrome DevTools: blocked by profile lock.
- Computer Use Chrome state: timed out.
- Playwright Shopify Admin: redirected to Shopify login.

## Guardrails

- No spend was enabled.
- No campaign budget, bid, status, product group, feed source, Shopify product, Pinterest catalog/campaign, order, payment, refund, billing, or credential write occurred.
- Google Ads write was limited to creating one Secondary website purchase conversion action for validation.
- Real conversion ID/label values were not written to tracked repo files.

## Next action

Resume from an authenticated Shopify Admin and GA4 browser session. Install the two Custom Pixels, verify with GA4 DebugView/Realtime and Google Ads diagnostics, and only then consider promoting the native Ads action from Secondary to Primary.
