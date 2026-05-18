# `pixels/` — Shopify Custom Pixels for GA4 + Google Ads

This directory holds the two Shopify Customer Events scripts that replace the broken purchase tracking on `www.dresslikemommy.com`.

| File | Purpose | Where it runs | Endpoint it hits |
| --- | --- | --- | --- |
| `ga4-custom-pixel.js` | Sends `page_view`, `view_item`, `add_to_cart`, `begin_checkout`, `purchase`, `search` to GA4 | Shopify Custom Pixel sandbox | `https://www.google-analytics.com/mp/collect` |
| `google-ads-custom-pixel.js` | Sends a native Google Ads conversion on every completed checkout | Shopify Custom Pixel sandbox | `https://www.googleadservices.com/pagead/conversion/<AW_ID>/` |

The install runbook is `docs/tracking-setup.md`. Read it before pasting either script into Shopify. The tracked files are templates only: leave placeholder IDs/secrets in the repo, and replace them only in Shopify's Custom Pixel editor or a non-repo temporary copy.

## Why these are Custom Pixels (and not theme code)

The new Shopify Checkout Extensibility thank-you page does **not** allow arbitrary `<script>` injection. The Customer Events API (`analytics.subscribe(...)`) inside a Custom Pixel is the only first-party path to fire analytics on the thank-you page in 2026. Theme-level `gtag` snippets and `additional_scripts.liquid` no longer execute on the checkout/thank-you steps, which is why the existing Google & YouTube App pixel has been silently missing `purchase` events.

## Why Measurement Protocol for GA4 (not gtag.js in the sandbox)

The Custom Pixel sandbox:

- Cannot access `window.dataLayer`, the parent storefront DOM, or first-party storefront cookies directly. It exposes only `browser.cookie` and `browser.localStorage` (both promise-based).
- Has a strict CSP that often blocks 3rd-party script loaders in practice — gtag.js is the canonical example of a script that "sometimes works" inside the sandbox depending on the Shopify build and the consent-mode shim.
- Survives best when the pixel uses beacon / no-CORS requests to known endpoints.

So `ga4-custom-pixel.js` constructs the GA4 Measurement Protocol payload itself and POSTs it with `navigator.sendBeacon(...)`, falling back to `fetch(..., { mode: "no-cors" })`. Do not change this to a normal JSON `fetch()`: the Shopify sandbox has an opaque/null origin, and GA4's MP endpoint does not allow the browser preflight, so ordinary JSON fetches fail before GA4 receives the event. We persist a client ID and rolling session ID via `browser.localStorage` so GA4 can stitch the pixel's own events across visits. The sandbox usually cannot read the storefront `_ga` cookie, so do not expect the GA4 client ID to match older theme/app-tag sessions.

## Why a direct conversion beacon for Google Ads (not gtag.js either)

Same sandbox constraint. The legacy image-pixel form of the Ads conversion request is a GET to `googleadservices.com/pagead/conversion/<AW_ID>/?label=...&value=...&oid=...`. `google-ads-custom-pixel.js` builds that URL directly and fires it with `fetch(..., { mode: "no-cors", credentials: "include", keepalive: true })`. The current template also starts an image backup beacon with the same `oid` / `transaction_id` so a sandbox transport miss is easier to detect and Google Ads can dedupe duplicate same-action fires by order ID.

Because the sandbox cannot read the storefront `_gcl_aw` linker cookie, the pixel captures `gclid`, `gbraid`, and `wbraid` from consented `page_viewed` URLs and stores them in `browser.localStorage` for 90 days. If the buyer arrived from a Google ad URL, those click IDs are attached to the purchase beacon. If no click ID exists, the conversion still fires with value/currency/order ID, but Ads attribution may be modeled or absent. This is a v1 bridge, not the full Google Ads API upload path.

## Native Ads diagnostic mode

The native Ads template intentionally leaves sanitized diagnostic logging on. The logs are there because a completed Shopify order did not appear in the native Google Ads action after delayed API/UI readback, so the next live Customer Events edit must prove three separate gates:

1. `checkout_completed` was received by the custom pixel.
2. Shopify Customer Privacy allowed the conversion to fire.
3. The pixel attempted `googleadservices.com/pagead/conversion/<AW_ID>/` with `value`, `currency`, `oid`, and `transaction_id`.

The diagnostic logs do not print the conversion label, full conversion URL, click IDs, checkout token, email, phone, or address. If `init.customerPrivacy` / `api.customerPrivacy` is unavailable or has unknown flags, the template trusts Shopify's pixel-level permission gate rather than silently dropping the purchase. Explicit `marketingAllowed: false` still blocks firing.

The live-edit approval packet is:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-18-google-ads-native-customer-events-diagnostic-fix/SHOPIFY_CUSTOMER_EVENTS_NATIVE_ADS_DIAGNOSTIC_FIX_PACKET.md`

## Deduplication strategy

There are three potential conversion paths from this store into Google Ads:

1. **The existing GA4-imported action** — `dresslikemommy.com - GA4 (web) purchase`. Source: Google Analytics (GA4). Currently broken because GA4 is not receiving `purchase`.
2. **The new native Ads action** — `Purchase — Shopify Custom Pixel (native)`. Source: this repo's `google-ads-custom-pixel.js`.
3. **The Google & YouTube app pixel** — Shopify's built-in pixel, which has its own GA4 + Ads conversion paths. Today it is the only thing running, and it is the thing that is silently missing purchases.

Without coordination, an order could trigger all three at once, and Google Ads would inflate `Conversions` by 2–3x. The plan:

### Phase 1 — install (Day 0)

- Native Ads pixel: live as **Secondary** at first (`Include in "Conversions"` = No) unless the owner explicitly wants to switch bidding immediately. Watch it in `All conversions` and Diagnostics during validation.
- GA4-imported Ads action: leave **as is** (still Primary) during the first validation window. The new GA4 pixel should also start feeding this action again through GA4 import, with normal GA4/Ads lag.
- G&YT app pixel: turn off only the GA4 sub-toggle if the app exposes it. Leave the Ads sub-toggle alone for now.
- GA4 Custom Pixel: live. Now GA4 is receiving `purchase` from two paths (the new pixel + whatever G&YT was sending). They share `transaction_id`, so GA4 dedupes them server-side within ~24h.

### Phase 2 — validate (Day 0 → Day 2)

For ~48h, monitor:

- GA4 → Monetization → Ecommerce purchases: order count and revenue should match Shopify orders within ±5%.
- Google Ads → Goals → Conversions → `Purchase — Shopify Custom Pixel (native)` → Diagnostics: order IDs should match Shopify within ±5%.
- Google Ads → Goals → Conversions → `dresslikemommy.com - GA4 (web) purchase`: should now also climb (because GA4 is now getting purchases) but lag the native action by 0–6h.

If counts on both Ads actions are within ±5% of each other (after the GA4 import lag), the native action is ready to promote. If counts diverge significantly, do not proceed to Phase 3 — investigate first.

### Phase 3 — prune (Day 2+)

- Google Ads → `Purchase — Shopify Custom Pixel (native)` → `Include in "Conversions"` → **Yes** (Primary).
- Google Ads → `dresslikemommy.com - GA4 (web) purchase` → `Include in "Conversions"` → **No** (Secondary). Wait 24h to confirm Smart Bidding picks up the native action.
- After 24h, set the GA4-imported action to **Paused** so it stops collecting at all. (Pause, not delete — keeping it makes rollback trivial.)
- If Smart Bidding strategies on any campaign were targeting only the GA4-imported action, retarget them to use account-default goals so they now bid to the native action.
- (Optional) Turn off the G&YT Ads sub-toggle in Shopify if it is still on. Skip if turning it off would also kill the Merchant feed.

End state: one Primary Ads conversion action, fed by one Shopify Custom Pixel. No double counting. Merchant Center feed untouched.

### Why not "run both in parallel forever with `transaction_id` dedup"

Google Ads `transaction_id` dedup works **per conversion action**, not across actions. Two distinct conversion actions firing with the same `transaction_id` will each count once — the dedup only prevents the same action from firing twice for the same order. So leaving both Primary forever would permanently double the conversions column. The clean fix is to keep exactly one action Primary at a time.

## What this does NOT cover

- **Refunds.** A `refund` in Shopify does not cancel a GA4 purchase or an Ads conversion automatically. If refund accuracy is important for ROAS, the next step is a server-side webhook (Shopify `orders/refunded`) that POSTs a `refund` event via GA4 Measurement Protocol and adjusts the Ads conversion via the Google Ads API. Out of scope here.
- **Enhanced Conversions for Ads.** Possible — would hash the buyer's email and send it with the conversion. Higher match rate, but pulls PII into the pixel, which raises consent/legal questions. Add later if Smart Bidding is starved for signal.
- **Server-side GTM.** Possible — would consolidate everything behind a single tagging server. Bigger lift; revisit only if multi-touch attribution requirements grow.
- **Cross-domain or app tracking.** Not applicable — single Shopify storefront on `www.dresslikemommy.com`.

## Quick-reference: what fires on what

| Shopify event | GA4 event (via this pixel) | Ads event (via this pixel) |
| --- | --- | --- |
| `page_viewed` | `page_view` | — |
| `product_viewed` | `view_item` | — |
| `product_added_to_cart` | `add_to_cart` | — |
| `checkout_started` | `begin_checkout` | — |
| `checkout_completed` | `purchase` (with `transaction_id`, `value`, `currency`, `tax`, `shipping`, `items[]`) | conversion (with `oid`/`transaction_id`, `value`, `currency`) |
| `search_submitted` | `search` | — |
