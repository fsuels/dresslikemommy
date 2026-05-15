/* ============================================================================
 * Dress Like Mommy — Google Ads Custom Pixel (Shopify Customer Events)
 * ----------------------------------------------------------------------------
 * WHERE THIS RUNS:
 *   Shopify Admin -> Settings -> Customer events -> Add custom pixel -> paste
 *   the entire contents of this file -> Save -> Connect.
 *
 * WHAT IT DOES:
 *   On `checkout_completed`, fires a native Google Ads conversion that is
 *   independent of GA4. This restores Ads-side reporting after the broken
 *   GA4-imported conversion went dark (Ads conversions for last 14 days
 *   showed Purchases = 0 while Shopify had real orders).
 *
 * WHY A DIRECT BEACON INSTEAD OF gtag.js:
 *   Shopify Custom Pixels run in a sandboxed iframe with strict CSP and no
 *   access to the parent storefront window. Loading gtag.js inside the sandbox
 *   is unreliable — and the new Checkout Extensibility thank-you page is
 *   precisely where script loaders silently fail. The legacy image-pixel form
 *   of the conversion call is a GET to
 *   https://www.googleadservices.com/pagead/conversion/<AW_ID>/?...
 *   We construct that URL directly so the conversion fires whether or not the
 *   sandbox can pull a 3rd-party script. This is intentionally a v1 bridge; a
 *   later server-side Google Ads API upload can supersede it if enhanced
 *   conversions or user-provided-data matching become required.
 *
 * IDS:
 *   Google Ads customer ID:  399-097-6848
 *   Google Ads MCC:          700-107-9966
 *
 * WHAT YOU MUST FILL IN BEFORE CONNECTING:
 *   __AW_CONVERSION_ID__     ->  e.g. "AW-1234567890". From Google Ads ->
 *                                Goals -> Conversions -> click the new
 *                                website conversion action -> Tag setup ->
 *                                "Conversion ID".
 *   __AW_CONVERSION_LABEL__  ->  e.g. "abcDEFghiJKLmnoPQR". Same screen,
 *                                "Conversion label".
 *
 *   Replace placeholders only in Shopify's Custom Pixel editor or a non-repo
 *   temporary copy. Never commit real conversion IDs/labels to this repository.
 *
 * CONSENT:
 *   Gated on Shopify's Customer Privacy API:
 *     init.customerPrivacy.marketingAllowed === true, with live updates from
 *     customerPrivacy.subscribe("visitorConsentCollected", ...)
 *   (Ads conversions are a marketing/ad-personalization use case, so we read
 *   the marketing flag rather than the analytics flag used by the GA4 pixel.)
 *
 * CLICK IDS / ATTRIBUTION:
 *   The sandbox cannot read the storefront's `_gcl_aw` or Google linker
 *   cookies. Instead, on every consented `page_viewed` event we read the URL
 *   from `event.context.window.location.href`, capture `gclid`, `gbraid`, and
 *   `wbraid` query parameters, and persist them in `browser.localStorage` for
 *   90 days. On `checkout_completed`, we attach the stored click IDs to the
 *   conversion beacon. If a buyer did not arrive with one of those URL params,
 *   the conversion still fires, but Ads attribution may be modeled or absent.
 *
 * DEDUPLICATION:
 *   We pass `oid` and `transaction_id` = bare numeric Shopify order id. Google
 *   Ads deduplicates duplicate fires inside the SAME conversion action by
 *   order id. It does not reliably dedupe two different conversion actions, so
 *   after ~48h of validating the native conversion, move the GA4-imported
 *   action to Secondary or pause it (see pixels/README.md).
 *
 * DEBUGGING:
 *   - Network panel in DevTools: filter for `googleadservices.com` and confirm
 *     a request to /pagead/conversion/<AW_ID>/ on order completion.
 *   - Google Tag Assistant (https://tagassistant.google.com) on the
 *     thank-you page can confirm the conversion fires.
 *   - Google Ads -> Goals -> Conversions -> Diagnostics shows recent
 *     conversions with their transaction_id within ~3 hours.
 * ========================================================================== */

/* eslint-disable no-undef */
(() => {
  // ===== CONFIG =============================================================
  const AW_CONVERSION_ID    = "__AW_CONVERSION_ID__";    // "AW-XXXXXXXXXX"
  const AW_CONVERSION_LABEL = "__AW_CONVERSION_LABEL__"; // "xxxxxxxxxxxxxxxx"
  const CLICK_ID_STORAGE_KEY = "dlm_google_ads_click_ids";
  const CLICK_ID_TTL_MS = 90 * 24 * 60 * 60 * 1000;

  // ===== EARLY GUARDS =======================================================
  if (
    !AW_CONVERSION_ID ||
    AW_CONVERSION_ID.indexOf("__") === 0 ||
    !AW_CONVERSION_LABEL ||
    AW_CONVERSION_LABEL.indexOf("__") === 0
  ) {
    console.warn("[DLM Ads Pixel] Conversion ID/Label not configured — pixel disabled.");
    return;
  }
  // Strip the "AW-" prefix so we can build the conversion URL.
  const AW_ID_NUMERIC = AW_CONVERSION_ID.replace(/^AW-/i, "");
  if (!/^\d+$/.test(AW_ID_NUMERIC)) {
    console.warn("[DLM Ads Pixel] AW_CONVERSION_ID must look like 'AW-1234567890'.");
    return;
  }

  // ===== UTIL: consent ======================================================
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

  function consentAllowed() {
    try {
      const cp = consentCache;
      if (!cp) return false;
      const marketingFlag = coercePrivacyFlag(cp.marketingAllowed);
      if (marketingFlag !== null) return marketingFlag;
      // Some consent UIs only set the analytics flag; fall back to that rather
      // than dropping the conversion entirely in non-marketing-specific builds.
      const analyticsFlag = coercePrivacyFlag(cp.analyticsProcessingAllowed);
      if (analyticsFlag !== null) return analyticsFlag;
    } catch (_) { /* no-op */ }
    return false;
  }

  // ===== UTIL: sandbox storage =============================================
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
    },
    async remove(key) {
      try {
        if (typeof browser !== "undefined" && browser.localStorage) {
          await browser.localStorage.removeItem(key);
        }
      } catch (_) { /* no-op */ }
    }
  };

  function bareOrderId(rawId) {
    if (!rawId) return "";
    const s = String(rawId);
    const m = s.match(/(\d+)\s*$/);
    return m ? m[1] : s;
  }

  function urlFromEvent(event) {
    return (
      event?.context?.window?.location?.href ||
      init?.context?.window?.location?.href ||
      ""
    );
  }

  function extractClickIds(url) {
    if (!url) return null;
    try {
      const params = new URL(url).searchParams;
      const clickIds = {};
      ["gclid", "gbraid", "wbraid", "gclsrc"].forEach((key) => {
        const value = params.get(key);
        if (value) clickIds[key] = value;
      });
      return Object.keys(clickIds).length ? clickIds : null;
    } catch (_) {
      return null;
    }
  }

  async function captureClickIdsFromPage(event) {
    const clickIds = extractClickIds(urlFromEvent(event));
    if (!clickIds) return;
    const payload = {
      ...clickIds,
      capturedAt: Date.now(),
      expiresAt: Date.now() + CLICK_ID_TTL_MS
    };
    await storage.set(CLICK_ID_STORAGE_KEY, JSON.stringify(payload));
    console.log("[DLM Ads Pixel] stored Google click id(s)", {
      hasGclid: Boolean(payload.gclid),
      hasGbraid: Boolean(payload.gbraid),
      hasWbraid: Boolean(payload.wbraid),
      expiresAt: new Date(payload.expiresAt).toISOString()
    });
  }

  async function getStoredClickIds() {
    try {
      const raw = await storage.get(CLICK_ID_STORAGE_KEY);
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      if (!parsed?.expiresAt || parsed.expiresAt < Date.now()) {
        await storage.remove(CLICK_ID_STORAGE_KEY);
        return {};
      }
      return parsed;
    } catch (_) {
      return {};
    }
  }

  // ===== UTIL: fire the conversion beacon ===================================
  // This mirrors the request gtag.js generates for
  //   gtag('event', 'conversion', { send_to: 'AW-XXX/LABEL', value, currency, transaction_id });
  // The beacon is a GET to googleadservices.com/pagead/conversion/<AW_ID>/.
  async function fireConversion({ value, currency, transactionId, clickIds }) {
    try {
      const params = new URLSearchParams();
      params.set("random", String(Date.now()));
      params.set("cv", "9");                                     // conversion version
      params.set("fst", String(Date.now()));                     // first-seen timestamp
      params.set("num", "1");
      params.set("guid", "ON");
      params.set("script", "0");
      params.set("label", AW_CONVERSION_LABEL);
      if (typeof value === "number" && !Number.isNaN(value)) {
        params.set("value", String(value));
      }
      if (currency) params.set("currency_code", String(currency));
      if (currency) params.set("currency", String(currency));
      if (transactionId) params.set("oid", String(transactionId)); // order id = dedup key
      if (transactionId) params.set("transaction_id", String(transactionId));
      if (clickIds?.gclid) params.set("gclid", String(clickIds.gclid));
      if (clickIds?.gbraid) params.set("gbraid", String(clickIds.gbraid));
      if (clickIds?.wbraid) params.set("wbraid", String(clickIds.wbraid));
      if (clickIds?.gclsrc) params.set("gclsrc", String(clickIds.gclsrc));
      params.set("u_w", "0");
      params.set("u_h", "0");
      params.set("frm", "0");

      const url = `https://www.googleadservices.com/pagead/conversion/${encodeURIComponent(AW_ID_NUMERIC)}/?${params.toString()}`;

      console.log("[DLM Ads Pixel] firing conversion", {
        AW_CONVERSION_ID,
        label: AW_CONVERSION_LABEL,
        value,
        currency,
        transactionId,
        clickIds: {
          hasGclid: Boolean(clickIds?.gclid),
          hasGbraid: Boolean(clickIds?.gbraid),
          hasWbraid: Boolean(clickIds?.wbraid)
        },
        url
      });

      // fetch with keepalive ensures the request survives the thank-you-page
      // navigation. mode:'no-cors' is fine — Ads conversions don't read the
      // response body. credentials:'include' lets Google attach its gcl/dsid
      // cookies if the user already has them.
      await fetch(url, {
        method: "GET",
        mode: "no-cors",
        credentials: "include",
        keepalive: true
      });
    } catch (err) {
      console.warn("[DLM Ads Pixel] conversion dispatch failed", err);
    }
  }

  // ===== SUBSCRIBE: capture click ids =======================================
  analytics.subscribe("page_viewed", async (event) => {
    if (!consentAllowed()) return;
    await captureClickIdsFromPage(event);
  });

  // ===== SUBSCRIBE: checkout_completed ======================================
  analytics.subscribe("checkout_completed", async (event) => {
    if (!consentAllowed()) {
      console.log("[DLM Ads Pixel] marketing consent denied — skipping.");
      return;
    }
    const checkout = event.data?.checkout || {};
    const order = checkout.order || {};
    const value = Number(checkout.totalPrice?.amount || 0);
    const currency =
      checkout.currencyCode ||
      checkout.totalPrice?.currencyCode ||
      "USD";
    const transactionId = bareOrderId(order.id || checkout.token || "");
    const clickIds = await getStoredClickIds();
    await fireConversion({ value, currency, transactionId, clickIds });
  });

  console.log("[DLM Ads Pixel] subscribed to Shopify page_viewed + checkout_completed");
})();
