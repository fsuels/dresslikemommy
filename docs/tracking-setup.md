# Tracking Setup — GA4 + Google Ads via Shopify Custom Pixels

**Owner:** Frank ([owner email redacted])
**Store:** [www.dresslikemommy.com](https://www.dresslikemommy.com) (handle `dresslikemommy-com`)
**Last updated:** 2026-05-17
**Why this exists:** Shopify's `Google & YouTube` App pixel is not firing `purchase` events into GA4 on the new Checkout Extensibility thank-you page. GA4 showed 0 transactions for 2026-05-14 against a real Shopify order #9490 ($158.91), and last-7-day GA4 purchases (3) are off by ~10x vs Shopify (≈28 orders / 30d). Because the primary Google Ads Purchase conversion is GA4-imported, Ads conversion data is also empty. We are replacing the broken path with two self-owned Shopify Custom Pixels.

This doc is the install runbook the browser session will follow. Read it top-to-bottom before clicking anything.

## 0. Decisions already locked

The four operating-mode choices have been made and the code in `pixels/` reflects them. Do not change these mid-install:

- **GA4 transport:** Measurement Protocol payloads sent from the Shopify pixel sandbox by `navigator.sendBeacon(...)`, with `fetch(..., { mode: "no-cors" })` fallback. Do not use ordinary JSON `fetch()` from the browser sandbox; GA4's MP endpoint blocks the CORS preflight before events arrive. gtag.js is unreliable inside the Shopify pixel sandbox; the controlled MP payload is the repair path.
- **Ads transport:** Direct conversion beacon to `googleadservices.com/pagead/conversion/<AW_ID>/`, using the legacy image-pixel URL shape. Avoids the gtag script-load failure mode in the sandbox. The pixel also captures `gclid`, `gbraid`, and `wbraid` from consented page URLs and persists them for 90 days in the Shopify pixel sandbox.
- **Deduplication:** Use the same bare numeric Shopify order ID in GA4 `transaction_id` and Ads `oid`/`transaction_id`. Google Ads deduplicates duplicate fires inside one conversion action, but not reliably across two separate actions, so the GA4-imported action must move to Secondary or Paused once the native action validates. (Detail in `pixels/README.md`.)
- **Google & YouTube app pixel:** Disable only the GA4 portion if the app exposes it as a separate toggle. Keep the Merchant Center product feed intact. If GA4 cannot be cleanly separated, document the tradeoff and keep G&YT GA4 on with `transaction_id` dedup as a fallback.

## 1. Create the new Google Ads website conversion action

Goal: produce the `AW-XXXXXXXXXX` Conversion ID and `xxxxxxxxxxxxxxxx` Conversion Label that get pasted into `pixels/google-ads-custom-pixel.js`.

1. Sign into Google Ads at [https://ads.google.com](https://ads.google.com) with access to customer ID **399-097-6848** (MCC **700-107-9966**).
2. Top right account picker → confirm you are on `399-097-6848` (dresslikemommy.com), not the MCC.
3. Left nav → **Goals** → **Conversions** → **Summary**.
4. Click the blue **+ New conversion action** button.
5. Choose **Website**.
6. Enter the domain `www.dresslikemommy.com` and click **Scan**. Let the scan finish; ignore the existing GA4-imported action result.
7. Below the scan results click **+ Add a conversion action manually**.
8. Fill in exactly:
   - **Goal and action optimization:** `Purchase` (under the "Sales" group). This is the goal category Google uses for bidding and reporting.
   - **Conversion name:** `Purchase — Shopify Custom Pixel (native)`. The "(native)" suffix makes it easy to tell apart from the GA4-imported action `dresslikemommy.com - GA4 (web) purchase`.
   - **Value:** `Use different values for each conversion` → leave default value blank (the pixel always sends the real `value`).
   - **Count:** `Every`. Every purchase is a distinct sale.
   - **Click-through conversion window:** `30 days`.
   - **Engaged-view conversion window:** `3 days` (default).
   - **View-through conversion window:** `1 day` (default).
   - **Include in "Conversions":** **No** (Secondary) for the first 48h validation window. This lets you watch the native action in `All conversions` and Diagnostics without double-counting the main `Conversions` column while the existing GA4-imported purchase action remains Primary. After validation, switch native to Primary and move the GA4-imported action to Secondary or Paused.
   - **Attribution model:** `Data-driven` (default; falls back to last-click if not enough volume).
9. Click **Done**, then **Save and continue**.
10. On the **Tag setup** screen choose **Use Google tag manually using code that you paste yourself**.
11. Copy the two values shown:
    - **Conversion ID** — looks like `AW-1234567890`.
    - **Conversion label** — looks like `abcDEFghiJKLmnoPQR`.
12. Click **Done**. You do NOT need to install the tag on the site — the Shopify Custom Pixel will fire the conversion directly.

Keep those two values out of the repo. When you install the pixel, paste a copy of `pixels/google-ads-custom-pixel.js` into Shopify's Custom Pixel code editor, then replace `__AW_CONVERSION_ID__` and `__AW_CONVERSION_LABEL__` inside the Shopify editor before saving. If you prepare a temporary local copy, put it outside this repository and do not commit it.

## 2. Create the GA4 Measurement Protocol API secret

Goal: produce the secret string that gets pasted into `pixels/ga4-custom-pixel.js`.

1. Sign into GA4 at [https://analytics.google.com](https://analytics.google.com). Confirm you are on the property `dresslikemommy.com - GA4` (property ID **330266838**, Measurement ID **G-N4EQNK0MMB**).
2. Bottom left **Admin** (gear icon).
3. Property column → **Data streams**.
4. Click the web data stream for `www.dresslikemommy.com`.
5. Scroll to **Events** section → **Measurement Protocol API secrets** → **Create**.
6. Nickname it `Shopify Custom Pixel` and click **Create**.
7. Copy the **Secret value** (long random string). It is only shown once — copy now.

Keep the secret value out of the repo. When you install the pixel, paste a copy of `pixels/ga4-custom-pixel.js` into Shopify's Custom Pixel code editor, then replace `__GA4_API_SECRET__` inside the Shopify editor before saving. If you prepare a temporary local copy, put it outside this repository and do not commit it.

## 3. Install the GA4 Custom Pixel in Shopify

1. Sign into Shopify Admin → store `dresslikemommy-com`.
2. **Settings** → **Customer events**.
3. **Add custom pixel** → name: `DLM GA4 (Measurement Protocol)`.
4. Permission: **Customer privacy** → check **Permission required** and require **Analytics** permission for this pixel. Keep **Marketing** unchecked unless your legal/consent posture requires both analytics and marketing for GA4 collection. Under **Data sale**, choose **Data collected does not qualify as data sale** unless your legal/compliance setup says otherwise.
5. Paste the entire contents of `pixels/ga4-custom-pixel.js` into the **Code** editor.
6. Confirm the line `const GA4_API_SECRET = "..."` contains your real secret and not `__GA4_API_SECRET__`.
7. Click **Save**.
8. Top right status banner → **Connect**. The pixel must show status **Connected**.

## 4. Install the Google Ads Custom Pixel in Shopify

1. Same screen: **Settings** → **Customer events** → **Add custom pixel**.
2. Name: `DLM Google Ads (native conversion)`.
3. Permission: **Customer privacy** → **Permission required** and require **Marketing** permission for this pixel. Requiring **Analytics** too is optional; the pixel falls back to analytics consent only if Shopify does not expose a marketing-specific flag.
4. Paste the entire contents of `pixels/google-ads-custom-pixel.js`.
5. Confirm `AW_CONVERSION_ID` and `AW_CONVERSION_LABEL` are real values, not `__AW_*__`.
6. **Save** → **Connect**. Status must read **Connected**.

You should now see two rows in **Custom pixels**, both Connected:
- `DLM GA4 (Measurement Protocol)`
- `DLM Google Ads (native conversion)`

## 5. Disable the GA4 portion of the Google & YouTube app pixel

We want to remove the duplicate GA4 path without breaking the Merchant Center product feed (which the same Google & YouTube channel powers).

1. Shopify Admin → **Settings** → **Customer events** → **App pixels** tab.
2. Click the row `Google & YouTube`.
3. Look for a sub-toggle named something like **Send analytics events to Google Analytics 4** or **Connect Google Analytics**.
   - **If present:** turn it **off**. Keep **Send conversion events to Google Ads** untouched for now (the new native pixel handles purchases; leaving G&YT Ads enabled as a belt-and-suspenders backup is acceptable for the short validation window — turn it off after step 7 below if the native action is clean).
   - **If the app does not let you disconnect GA4 separately from Ads/Merchant:** stop. Do **not** disconnect the whole G&YT channel. Document the limitation in the worklog and proceed — the GA4 Custom Pixel will simply double-report (with `transaction_id` dedup, GA4 itself will collapse the duplicates after up to ~24h).
4. Save.

**Important:** do **not** remove or disconnect the Google & YouTube **sales channel** itself. That channel is the source of truth for the Merchant Center product feed (`Shopify App API` source, `124884876` Merchant Center, source ID `10627623003`). Removing the channel would break Shopping ads serving.

## 6. Verification checklist (run in this order)

Before placing a test order, do the static checks. Then place one real test order.

### 6a-urgent. Native Ads Customer Events diagnostic/fix gate

After order `#9494`, Google Ads still showed no native action entries even though the action configuration was correct. Before another paid test, use the approval packet below to update only the native Ads custom pixel:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-18-google-ads-native-customer-events-diagnostic-fix/SHOPIFY_CUSTOMER_EVENTS_NATIVE_ADS_DIAGNOSTIC_FIX_PACKET.md`

The prepared Ads pixel now logs three sanitized checkpoints:

- `checkout_completed received`
- the consent decision and reason
- the conversion attempt with `value`, `currency`, `oid`, and `transaction_id`

The logs are intentionally redacted: do not paste raw conversion labels, full conversion URLs, click IDs, checkout tokens, email, phone, or address into repo notes.

### 6a. Static checks (no money moved)

- [ ] In the Shopify GA4 Custom Pixel editor, `GA4_API_SECRET` is not the placeholder.
- [ ] In the Shopify Google Ads Custom Pixel editor, neither `AW_CONVERSION_ID` nor `AW_CONVERSION_LABEL` is the placeholder.
- [ ] Shopify → Customer events → both Custom pixels show **Connected**.
- [ ] Google Ads → Goals → Conversions → the new `Purchase — Shopify Custom Pixel (native)` action exists with status `Unverified` (will flip to `Recording conversions` after the first real fire) and `Include in "Conversions"` is **No** until validation is complete.
- [ ] Storefront DevTools console on a product page shows `[DLM GA4 Pixel] dispatch page_view` / `view_item` and does **not** show `Access to fetch at 'https://www.google-analytics.com/mp/collect...' has been blocked by CORS policy` or `[DLM GA4 Pixel] dispatch failed`.

### 6b. GA4 DebugView dry run (no order)

1. In `pixels/ga4-custom-pixel.js`, temporarily set `DLM_FORCE_DEBUG_VIEW = true` and **Save** in Shopify Admin. (You will revert this before going to production.)
2. Open [www.dresslikemommy.com](https://www.dresslikemommy.com) in a private Chrome window.
3. In GA4 left nav → **Admin** → **DebugView**.
4. Browse: home → a product page → click **Add to cart** → open cart → click **Checkout** → **stop at the shipping step**, do not pay.
5. DebugView should show events appearing in real time:
   - `page_view`
   - `view_item` (with `value`, `currency: USD`, `items[].item_id`)
   - `add_to_cart`
   - `begin_checkout`
6. If any event is missing or `value` is 0, capture the DevTools console and stop — fix before placing the real test order.
7. Set `DLM_FORCE_DEBUG_VIEW = false` and Save again.

### 6c. Real test order (end-to-end)

1. Place a real order on `www.dresslikemommy.com` for the lowest-priced product. Use a card you can refund. Do not use a Shopify "test mode" / Bogus Gateway order — Custom Pixels behave differently in test mode and you want the production thank-you page.
2. Within 60 seconds:
   - GA4 → **Reports** → **Realtime** → confirm a `purchase` event with the right `value` and `transaction_id` (= Shopify order id).
   - GA4 → **Admin** → **DebugView** (works if you are the buyer and have the GA Debugger extension) — confirm event params.
   - DevTools Network panel on the thank-you page → filter `googleadservices.com` → confirm a GET to `/pagead/conversion/<AW_ID>/?...&label=<LABEL>&value=<VALUE>&oid=<ORDER_ID>&transaction_id=<ORDER_ID>`. Because the request uses `mode: "no-cors"`, Chrome may show it as opaque rather than exposing a readable response body.
   - If the buyer session originally landed from a Google ad URL, the same request should include at least one of `gclid`, `gbraid`, or `wbraid`. Do not fabricate a fake click ID on the real test order; just verify the field is present when the real landing URL provided it.
3. Within ~3 hours:
   - Google Ads → **Goals** → **Conversions** → click `Purchase — Shopify Custom Pixel (native)` → **Diagnostics** → confirm the order id appears under recent conversions.
4. Within 24 hours:
   - GA4 → **Reports** → **Monetization** → **Ecommerce purchases** → confirm the order shows up once with the correct revenue.
   - Google Ads → **Campaigns** column set including `Conversions` → confirm the conversion attributes to the right campaign.
5. Refund the test order in Shopify. (Refunds will currently NOT propagate to GA4/Ads — that's a known limitation of pure client-side purchase tracking. If refund accuracy matters, follow up with a Measurement Protocol `refund` event triggered from a Shopify webhook; out of scope for this install.)

### 6d. Google Ads Tag Assistant (optional but recommended)

1. Install the Tag Assistant Chrome extension.
2. Visit [https://tagassistant.google.com](https://tagassistant.google.com) → **Add domain** → `www.dresslikemommy.com`.
3. Walk through the checkout in the Tag Assistant-instrumented tab.
4. On the thank-you page Tag Assistant should report a Google Ads conversion fired with the right `AW-ID/label`, `value`, `currency`, and `transaction_id`. If the test path did not begin from a real Google ad click, attribution diagnostics may show limited or no click attribution even though the conversion request fired.

## 7. After 48h: prune the duplicate

Once you have at least 48h of native-pixel data with order counts and revenue matching Shopify within ±5%:

1. Google Ads → Goals → Conversions → `Purchase — Shopify Custom Pixel (native)` → **Settings** → **Include in "Conversions"** → **Yes**.
2. Google Ads → Goals → Conversions → `dresslikemommy.com - GA4 (web) purchase` → **Settings** → **Include in "Conversions"** → **No** (Secondary). Wait 24h.
3. If reporting still looks correct, pause the GA4-imported action: same screen → **Status** → **Pause**.
4. (Optional, only if step 5 above left the G&YT Ads sub-toggle on) Shopify → Customer events → App pixels → Google & YouTube → turn off **Send conversion events to Google Ads**.
5. Confirm Smart Bidding strategies on active campaigns are now pointed at the new native action. If any campaign is still bidding to the old GA4-imported conversion only, switch its conversion goals to use account-default goals (the new native action will be the default once it is the only active Primary).

## 8. Rollback plan

If something breaks at any step:

- **Pixel emits no events / DebugView empty:**
  1. Shopify → Customer events → click the broken Custom Pixel → **Disconnect**.
  2. The Google & YouTube app pixel is still active and will continue powering whatever tracking it powered before. The state pre-install is recoverable in full.
- **Native Ads conversion under- or over-reports:**
  1. Re-enable the GA4-imported action (`Include in "Conversions"` → **Yes**) immediately.
  2. Pause the native action.
  3. Investigate via Tag Assistant + DevTools network logs from the test order.
- **Merchant Center feed breaks:**
  1. This pixel work does NOT touch the Merchant feed source. If feed errors appear, the cause is elsewhere — do not blame the pixel install.
  2. If the G&YT channel was accidentally disconnected, reconnect from Shopify → Sales channels.
- **Worst case (any of the above causes business pain):**
  1. Disconnect both Custom Pixels.
  2. Re-enable any G&YT GA4 toggles you turned off.
  3. Re-enable the GA4-imported Ads conversion action as Primary.
  4. State is restored to the broken-but-stable baseline this work is replacing.

## 9. Reference IDs

- GA4 Measurement ID: `G-N4EQNK0MMB`
- GA4 property ID: `330266838`
- GA4 property name: `dresslikemommy.com - GA4`
- Google Ads customer ID: `399-097-6848`
- Google Ads MCC: `700-107-9966`
- Shopify domain: `www.dresslikemommy.com`
- Shopify store handle: `dresslikemommy-com`
- Merchant Center account: `124884876` (do not modify during this work)
- Files: `pixels/ga4-custom-pixel.js`, `pixels/google-ads-custom-pixel.js`, `pixels/README.md`
