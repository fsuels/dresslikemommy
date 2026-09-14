/* ============================================================================
 * Dress Like Mommy — GA4 Custom Pixel (Shopify Customer Events)
 * ----------------------------------------------------------------------------
 * WHERE THIS RUNS:
 *   Shopify Admin -> Settings -> Customer events -> Add custom pixel -> paste
 *   the entire contents of this file -> Save -> Connect.
 *
 * SIGNATURE:
 *   Shopify invokes the Custom Pixel code with the sandbox globals
 *     { analytics, browser, init, customerPrivacy }
 *   already available as top-level identifiers. We do NOT wrap this file in a
 *   function — we use those identifiers directly, which is what Shopify's
 *   Custom Pixel docs prescribe.
 *
 *   - `analytics`  : subscribe / publish bus.
 *   - `browser`    : promise-based cookie + localStorage shims.
 *   - `init`       : page context AT LOAD TIME, including
 *                      init.context.document, init.context.window,
 *                      init.data, AND init.customerPrivacy (consent snapshot).
 *   - `customerPrivacy` or `api.customerPrivacy`: consent-update subscription
 *                      surface exposed by Shopify's Web Pixels Standard API.
 *
 *   Live consent updates arrive via `customerPrivacy.subscribe(
 *   "visitorConsentCollected", ...)`. Some Custom Pixel examples expose that
 *   object through `api.customerPrivacy`, so this file supports both shapes.
 *
 * WHY MEASUREMENT PROTOCOL (not gtag.js):
 *   Shopify Custom Pixels run inside a sandboxed iframe on a different origin
 *   than the storefront. The sandbox does NOT give scripts access to
 *   window.dataLayer, the parent storefront DOM, or first-party storefront
 *   cookies. gtag.js is fragile in this environment — it cannot reliably read
 *   the GA4 _ga client_id and on the new Checkout Extensibility thank-you page
 *   it is the exact failure mode that produced "0 GA4 transactions yesterday"
 *   for store dresslikemommy.com on 2026-05-14.
 *
 *   GA4 Measurement Protocol is the controllable payload path, but from a
 *   browser sandbox it must be sent as a beacon / no-CORS POST. A normal
 *   `fetch()` with `Content-Type: application/json` triggers a CORS preflight
 *   against google-analytics.com and is blocked before GA4 can record it.
 *   We construct the event payload from Shopify Customer Events `event.data`
 *   and send it to https://www.google-analytics.com/mp/collect with the
 *   property's API secret.
 *
 * CLIENT ID — IMPORTANT EXPECTATION:
 *   `browser.cookie.get('_ga')` reads cookies on the SANDBOX origin, not the
 *   storefront. The storefront's `_ga` cookie (set by any browser-side gtag.js
 *   or by Google Analytics auto-collection) is therefore typically NOT visible
 *   here. We try it anyway (cheap, harmless), then fall back to a stable UUID
 *   persisted in `browser.localStorage` under `dlm_ga4_client_id`. In practice
 *   that fallback is the expected source. This is documented behavior; it is
 *   not a bug. Reports stay attributed correctly because the fallback is
 *   stable per browser.
 *
 *   If you ever decide to seed a matching client_id, do it from the storefront
 *   theme (where `_ga` IS readable) via a thin App Proxy that writes the value
 *   into a queryable surface the pixel can read. Out of scope for v1.
 *
 * IDS (from the owner-provided context):
 *   GA4 Measurement ID:  G-N4EQNK0MMB
 *   GA4 Property ID:     330266838  (informational only — MP uses Measurement ID)
 *
 * WHAT YOU MUST FILL IN BEFORE CONNECTING:
 *   __GA4_API_SECRET__   ->  Create in GA4 Admin -> Data streams -> (Web stream
 *                            for dresslikemommy.com) -> Measurement Protocol
 *                            API secrets -> Create -> copy "Secret value".
 *                            Replace the placeholder only in Shopify's Custom
 *                            Pixel editor or a non-repo temporary copy. Never
 *                            commit the real secret to this repository.
 *
 * CONSENT:
 *   - Initial snapshot: `init.customerPrivacy.analyticsProcessingAllowed`.
 *   - Live updates: `customerPrivacy.subscribe("visitorConsentCollected", ...)`
 *   - We cache the last-known value and re-check on every dispatch.
 *   - If consent is unknown OR denied, the event is dropped (not queued).
 *
 * DEDUPLICATION:
 *   The `purchase` event sends transaction_id = the BARE NUMERIC Shopify order
 *   id (we strip `gid://shopify/Order/`), so it matches the form the
 *   GA4-imported Ads conversion uses and the form the companion
 *   `pixels/google-ads-custom-pixel.js` sends as `oid`. Cross-system dedup
 *   then works at the platform layer.
 *
 * TODO (v2 — out of scope here):
 *   When a Shopify `orders/refunded` webhook fires server-side, POST a GA4
 *   Measurement Protocol `refund` event with the same `transaction_id` and
 *   the refunded `value`/`items[]`. That keeps revenue/ROAS accurate after
 *   refunds. v1 does not handle refunds; documented in pixels/README.md.
 *
 * DEBUGGING:
 *   - Every dispatch logs `[DLM GA4 Pixel] dispatch ...` to the DevTools
 *     console (the sandbox supports console.log).
 *   - To force DebugView mode for a session, set DLM_FORCE_DEBUG_VIEW = true,
 *     Save, walk the funnel, then set back to false.
 *   - To validate payload shape outside the browser sandbox, POST a captured
 *     payload to /debug/mp/collect from a server/local shell. Browser-side
 *     validation may be blocked by the same CORS rules as collect.
 * ========================================================================== */

/* eslint-disable no-undef */

// ===== CONFIG =============================================================
const GA4_MEASUREMENT_ID    = "G-N4EQNK0MMB";
const GA4_API_SECRET        = "__GA4_API_SECRET__"; // <-- replace before Save
const DLM_FORCE_DEBUG_VIEW  = false; // set true to flag every event as debug
const DLM_USE_MP_VALIDATION = false; // set true to POST to /debug/mp/collect
const CLIENT_ID_STORAGE_KEY = "dlm_ga4_client_id";
const SESSION_STORAGE_KEY   = "dlm_ga4_session";
const SESSION_TIMEOUT_MS    = 30 * 60 * 1000; // GA4 default

// ===== EARLY GUARDS =======================================================
if (!GA4_API_SECRET || GA4_API_SECRET.indexOf("__") === 0) {
  console.warn("[DLM GA4 Pixel] API secret not configured — pixel disabled.");
} else {
  installPixel();
}

function installPixel() {
  const MP_ENDPOINT = DLM_USE_MP_VALIDATION
    ? "https://www.google-analytics.com/debug/mp/collect"
    : "https://www.google-analytics.com/mp/collect";

  // ===== CONSENT CACHE =====================================================
  // Seed from the init snapshot Shopify hands the pixel, then keep refreshing
  // it whenever the consent-updated event fires.
  let consentCache = (() => {
    try { return init?.customerPrivacy || null; } catch (_) { return null; }
  })();

  subscribePrivacyUpdates((event) => {
    try {
      const updated =
        event?.customerPrivacy ||
        event?.data?.customerPrivacy ||
        null;
      if (updated) consentCache = updated;
    } catch (_) { /* no-op */ }
  });

  function subscribePrivacyUpdates(callback) {
    try {
      const privacyApi =
        (typeof customerPrivacy !== "undefined" && customerPrivacy) ||
        (typeof api !== "undefined" && api?.customerPrivacy) ||
        null;
      if (privacyApi?.subscribe) {
        privacyApi.subscribe("visitorConsentCollected", callback);
        return;
      }
    } catch (_) { /* no-op */ }

    // Legacy/fallback shape observed in some Shopify Custom Pixel builds.
    try {
      if (analytics?.subscribe) {
        analytics.subscribe(
          "customer_privacy_consent_preferences_updated",
          callback
        );
      }
    } catch (_) { /* no-op */ }
  }

  function coercePrivacyFlag(value) {
    if (typeof value === "boolean") return value;
    if (typeof value === "function") {
      try {
        const result = value();
        if (typeof result === "boolean") return result;
      } catch (_) { /* no-op */ }
    }
    return null;
  }

  function analyticsAllowed() {
    try {
      const cp = consentCache;
      if (!cp) return false;
      const analyticsFlag = coercePrivacyFlag(cp.analyticsProcessingAllowed);
      if (analyticsFlag !== null) return analyticsFlag;
      // Fallback: some stores only expose the marketing flag; analytics
      // processing is generally allowed when marketing is allowed.
      const marketingFlag = coercePrivacyFlag(cp.marketingAllowed);
      if (marketingFlag !== null) return marketingFlag;
    } catch (_) { /* no-op */ }
    return false;
  }

  // ===== STORAGE WRAPPERS ==================================================
  // browser.localStorage / browser.cookie are the only persistence APIs the
  // Shopify pixel sandbox exposes. They are PROMISE-based.
  const storage = {
    async get(key) {
      try {
        if (typeof browser !== "undefined" && browser.localStorage) {
          return await browser.localStorage.getItem(key);
        }
      } catch (_) { /* no-op */ }
      return null;
    },
    async set(key, value) {
      try {
        if (typeof browser !== "undefined" && browser.localStorage) {
          await browser.localStorage.setItem(key, value);
        }
      } catch (_) { /* no-op */ }
    }
  };

  const cookies = {
    async get(name) {
      try {
        if (typeof browser !== "undefined" && browser.cookie) {
          // NOTE: reads sandbox-origin cookies, NOT storefront cookies. See
          // the file-header note on client_id behavior.
          return await browser.cookie.get(name);
        }
      } catch (_) { /* no-op */ }
      return null;
    }
  };

  // ===== CLIENT ID =========================================================
  async function getClientId() {
    // Best-effort: try the sandbox-visible _ga cookie. Almost always null in
    // current Shopify builds because the storefront _ga is on a different
    // origin. Kept for forward-compat — if a future Shopify release exposes
    // cross-origin _ga the pixel auto-upgrades to a matching client_id.
    const ga = await cookies.get("_ga");
    if (ga && typeof ga === "string") {
      // Format: GA1.1.<client_id>.<creation_ts>
      const parts = ga.split(".");
      if (parts.length >= 4) {
        const candidate = parts.slice(2, parts.length - 1).join(".");
        if (candidate) {
          await storage.set(CLIENT_ID_STORAGE_KEY, candidate);
          return candidate;
        }
      }
    }
    const stored = await storage.get(CLIENT_ID_STORAGE_KEY);
    if (stored) return stored;
    // GA4-compatible shape: <random10>.<unix_seconds>.
    const fresh = `${Math.floor(Math.random() * 1e10)}.${Math.floor(Date.now() / 1000)}`;
    await storage.set(CLIENT_ID_STORAGE_KEY, fresh);
    return fresh;
  }

  // ===== SESSION ID (30 min rolling window) ================================
  async function getSession() {
    const now = Date.now();
    let session;
    try {
      const raw = await storage.get(SESSION_STORAGE_KEY);
      if (raw) session = JSON.parse(raw);
    } catch (_) { session = null; }
    if (!session || !session.id || (now - session.last) > SESSION_TIMEOUT_MS) {
      session = {
        id: String(Math.floor(now / 1000)),
        number: (session?.number || 0) + 1,
        last: now
      };
    } else {
      session.last = now;
    }
    await storage.set(SESSION_STORAGE_KEY, JSON.stringify(session));
    return session;
  }

  // ===== UTIL: bare numeric order id ========================================
  // Shopify exposes order id as either a numeric string or
  // `gid://shopify/Order/<numeric>`. Normalize to bare numeric so this matches
  // the GA4-imported Ads conversion (which uses the numeric order id) AND the
  // companion Ads pixel's `oid` value.
  function bareOrderId(rawId) {
    if (!rawId) return "";
    const s = String(rawId);
    const m = s.match(/(\d+)\s*$/);
    return m ? m[1] : s;
  }

  // ===== ITEMS MAPPING =====================================================
  // checkout_completed shape: event.data.checkout.lineItems[] where each line
  // exposes { id, title, quantity, variant: { id, sku, title, price{amount,currencyCode},
  //   product: { id, title, type, vendor, untranslatedTitle } } }
  function buildItemsFromLines(lineItems) {
    if (!Array.isArray(lineItems)) return [];
    return lineItems.map((li, idx) => {
      const merchandise = li?.merchandise || {};
      const v = li?.variant || merchandise?.productVariant || merchandise || {};
      const product = v.product || {};
      const price = Number(
        v.price?.amount ??
        li.finalLinePrice?.amount ??
        0
      );
      // PRIMARY: variant.id (stable numeric). FALLBACK: variant.sku. Then product.id.
      const itemId = String(
        v.id || v.sku || product.id || `line_${idx}`
      );
      const out = {
        item_id: itemId,
        item_name: String(product.title || v.title || li.title || "Unknown"),
        index: idx,
        price,
        quantity: Number(li.quantity || 1)
      };
      if (v.title)      out.item_variant  = String(v.title);
      if (product.vendor) out.item_brand   = String(product.vendor);
      if (product.type)   out.item_category = String(product.type);
      if (v.sku)        out.item_sku      = String(v.sku);
      return out;
    });
  }

  // Single-item shape used by product_viewed.
  function buildSingleItem(productVariant) {
    if (!productVariant) return [];
    const v = productVariant;
    const product = v.product || {};
    const price = Number(v.price?.amount ?? 0);
    return [{
      item_id: String(v.id || v.sku || product.id || "unknown"),
      item_name: String(product.title || v.title || "Unknown"),
      item_variant: String(v.title || ""),
      item_brand: String(product.vendor || ""),
      item_category: String(product.type || ""),
      item_sku: String(v.sku || ""),
      price,
      quantity: 1
    }];
  }

  // ===== DISPATCH ==========================================================
  async function send(eventName, params, contextOverrides = {}) {
    try {
      const clientId = await getClientId();
      const session  = await getSession();

      const event = {
        name: eventName,
        params: {
          ...params,
          session_id: session.id,
          session_number: session.number,
          engagement_time_msec: 100
        }
      };
      if (DLM_FORCE_DEBUG_VIEW) event.params.debug_mode = 1;

      const body = {
        client_id: clientId,
        events: [event],
        ...contextOverrides
      };

      const url =
        `${MP_ENDPOINT}?measurement_id=${encodeURIComponent(GA4_MEASUREMENT_ID)}` +
        `&api_secret=${encodeURIComponent(GA4_API_SECRET)}`;

      console.log("[DLM GA4 Pixel] dispatch", eventName, params);

      const payload = JSON.stringify(body);

      if (DLM_USE_MP_VALIDATION) {
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: payload,
          keepalive: true
        });
        const text = await res.text();
        console.log("[DLM GA4 Pixel] MP validation response", res.status, text);
        return;
      }

      // Shopify Custom Pixels run from an opaque/null-origin sandbox. GA4 MP
      // does not return CORS headers for browser preflights, so production
      // dispatch must avoid non-safelisted request headers and must not try to
      // read the response. Prefer sendBeacon for checkout navigation survival;
      // fall back to no-cors fetch when the sandbox does not expose it.
      let beaconQueued = false;
      try {
        if (typeof navigator !== "undefined" && navigator.sendBeacon) {
          const blob = new Blob([payload], { type: "text/plain;charset=UTF-8" });
          beaconQueued = navigator.sendBeacon(url, blob);
        }
      } catch (_) { beaconQueued = false; }

      if (!beaconQueued) {
        await fetch(url, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "text/plain;charset=UTF-8" },
          body: payload,
          keepalive: true,
          credentials: "omit"
        });
      }
    } catch (err) {
      console.warn("[DLM GA4 Pixel] dispatch failed", eventName, err);
    }
  }

  // ===== SUBSCRIBE: Shopify Customer Events ================================

  // 1) page_view
  analytics.subscribe("page_viewed", async (event) => {
    if (!analyticsAllowed()) return;
    const ctx = event.context || {};
    const doc = ctx.document || {};
    const win = ctx.window || {};
    await send("page_view", {
      page_location: win.location?.href,
      page_title:    doc.title,
      page_referrer: doc.referrer
    });
  });

  // 2) view_item
  analytics.subscribe("product_viewed", async (event) => {
    if (!analyticsAllowed()) return;
    const variant = event.data?.productVariant;
    const items = buildSingleItem(variant);
    const value = items[0]?.price || 0;
    await send("view_item", {
      currency: variant?.price?.currencyCode || "USD",
      value,
      items
    });
  });

  // 3) add_to_cart
  analytics.subscribe("product_added_to_cart", async (event) => {
    if (!analyticsAllowed()) return;
    const line = event.data?.cartLine;
    const items = buildItemsFromLines(line ? [line] : []);
    const value = items.reduce((acc, it) => acc + (it.price * it.quantity), 0);
    await send("add_to_cart", {
      currency:
        line?.merchandise?.price?.currencyCode ||
        line?.cost?.totalAmount?.currencyCode ||
        "USD",
      value,
      items
    });
  });

  // 4) begin_checkout
  analytics.subscribe("checkout_started", async (event) => {
    if (!analyticsAllowed()) return;
    const checkout = event.data?.checkout || {};
    const items = buildItemsFromLines(checkout.lineItems);
    await send("begin_checkout", {
      currency:
        checkout.currencyCode ||
        checkout.totalPrice?.currencyCode ||
        "USD",
      value: Number(checkout.totalPrice?.amount || checkout.subtotalPrice?.amount || 0),
      coupon: (checkout.discountApplications || [])
        .map((d) => d?.title || d?.code).filter(Boolean).join(",") || undefined,
      items
    });
  });

  // 5) purchase  <-- THE EVENT THAT IS CURRENTLY MISSING IN GA4
  analytics.subscribe("checkout_completed", async (event) => {
    if (!analyticsAllowed()) return;
    const checkout = event.data?.checkout || {};
    const order    = checkout.order || {};
    const items    = buildItemsFromLines(checkout.lineItems);
    const currency =
      checkout.currencyCode ||
      checkout.totalPrice?.currencyCode ||
      "USD";
    await send("purchase", {
      transaction_id: bareOrderId(order.id || checkout.token || ""),
      value:    Number(checkout.totalPrice?.amount || 0),
      tax:      Number(checkout.totalTax?.amount || 0),
      shipping: Number(checkout.shippingLine?.price?.amount || 0),
      currency,
      coupon: (checkout.discountApplications || [])
        .map((d) => d?.title || d?.code).filter(Boolean).join(",") || undefined,
      items
    });
  });

  // 6) search
  analytics.subscribe("search_submitted", async (event) => {
    if (!analyticsAllowed()) return;
    const term =
      event.data?.searchResult?.query ||
      event.data?.searchResult?.searchTerm ||
      "";
    await send("search", { search_term: String(term) });
  });

  console.log("[DLM GA4 Pixel] subscribed to Shopify Customer Events");
}
