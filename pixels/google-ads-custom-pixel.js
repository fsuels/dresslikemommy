/* ============================================================================
 * Dress Like Mommy - Google Ads Custom Pixel (Shopify Customer Events)
 * Shopify-validator-safe build: no ternary operators, no optional chaining,
 * no async arrow functions, no object spread.
 * ========================================================================== */

(function () {
  var AW_CONVERSION_ID = "__AW_CONVERSION_ID__";
  var AW_CONVERSION_LABEL = "__AW_CONVERSION_LABEL__";
  var CLICK_ID_STORAGE_KEY = "dlm_google_ads_click_ids";
  var CLICK_ID_TTL_MS = 90 * 24 * 60 * 60 * 1000;
  var DLM_DIAGNOSTIC_MODE = true;
  var TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE = true;
  var FIRE_IMAGE_BACKUP_BEACON = true;
  var imageBeaconRefs = [];
  var consentCache = getInitialPrivacy();

  if (!AW_CONVERSION_ID || AW_CONVERSION_ID.indexOf("__") === 0 || !AW_CONVERSION_LABEL || AW_CONVERSION_LABEL.indexOf("__") === 0) {
    safeLog("warn", "Conversion ID/Label not configured - pixel disabled", {});
    return;
  }

  var AW_ID_NUMERIC = AW_CONVERSION_ID.replace(/^AW-/i, "");
  if (!/^\d+$/.test(AW_ID_NUMERIC)) {
    safeLog("warn", "AW_CONVERSION_ID must look like AW-1234567890", {});
    return;
  }

  subscribePrivacyUpdates(function (event) {
    var updated = null;
    try {
      if (event && event.customerPrivacy) updated = event.customerPrivacy;
      if (!updated && event && event.data && event.data.customerPrivacy) updated = event.data.customerPrivacy;
      if (updated) consentCache = updated;
    } catch (err) {
      // no-op
    }
  });

  analytics.subscribe("page_viewed", function (event) {
    var decision = consentDecision();
    safeLog("log", "page_viewed received", {
      eventId: getEventId(event),
      consentAllowed: decision.allowed,
      consentReason: decision.reason,
      consentFlags: decision.flags,
      hasLocationHref: Boolean(urlFromEvent(event))
    });
    if (!decision.allowed) return;
    captureClickIdsFromPage(event);
  });

  analytics.subscribe("checkout_completed", function (event) {
    var checkout = getCheckout(event);
    var order = checkout.order || {};
    var value = Number(getNested(checkout, ["totalPrice", "amount"]) || 0);
    var currency = getNested(checkout, ["currencyCode"]);
    if (!currency) currency = getNested(checkout, ["totalPrice", "currencyCode"]);
    if (!currency) currency = "USD";
    var transactionId = bareOrderId(order.id || checkout.token || "");
    var decision = consentDecision();

    safeLog("log", "checkout_completed received", {
      eventId: getEventId(event),
      eventName: getEventName(event),
      hasCheckout: Boolean(checkout && Object.keys(checkout).length),
      hasOrderId: Boolean(order.id),
      hasCheckoutToken: Boolean(checkout.token),
      value: value,
      currency: currency,
      transactionIdPresent: Boolean(transactionId),
      consentAllowed: decision.allowed,
      consentReason: decision.reason,
      consentFlags: decision.flags
    });

    if (!decision.allowed) {
      safeLog("warn", "checkout_completed blocked by consent decision", {
        consentReason: decision.reason,
        consentFlags: decision.flags
      });
      return;
    }

    if (!transactionId) {
      safeLog("warn", "missing transaction_id/oid; conversion not sent", {
        value: value,
        currency: currency
      });
      return;
    }

    getStoredClickIds().then(function (clickIds) {
      return fireConversion(value, currency, transactionId, clickIds);
    }).catch(function (err) {
      safeLog("warn", "conversion promise failed", safeErrorPayload(err));
    });
  });

  safeLog("log", "subscribed to Shopify page_viewed + checkout_completed", {
    diagnosticMode: DLM_DIAGNOSTIC_MODE,
    imageBackupBeacon: FIRE_IMAGE_BACKUP_BEACON,
    trustShopifyPermissionGateWhenPrivacyUnavailable: TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE
  });

  function getInitialPrivacy() {
    try {
      if (typeof init !== "undefined" && init && init.customerPrivacy) return init.customerPrivacy;
    } catch (err) {
      // no-op
    }
    return null;
  }

  function subscribePrivacyUpdates(callback) {
    try {
      var privacyApi = null;
      if (typeof customerPrivacy !== "undefined" && customerPrivacy) privacyApi = customerPrivacy;
      if (!privacyApi && typeof api !== "undefined" && api && api.customerPrivacy) privacyApi = api.customerPrivacy;
      if (privacyApi && privacyApi.subscribe) privacyApi.subscribe("visitorConsentCollected", callback);
    } catch (err) {
      // no-op
    }
  }

  function coercePrivacyFlag(value) {
    if (typeof value === "boolean") return value;
    if (typeof value === "function") {
      try {
        var result = value();
        if (typeof result === "boolean") return result;
      } catch (err) {
        // no-op
      }
    }
    return null;
  }

  function consentDecision() {
    var unavailableReason = "privacy_unavailable";
    var unknownReason = "privacy_flags_unknown";
    var exceptionReason = "privacy_exception";

    if (TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE) {
      unavailableReason = "privacy_unavailable_trusting_shopify_permission_gate";
      unknownReason = "privacy_flags_unknown_trusting_shopify_permission_gate";
      exceptionReason = "privacy_exception_trusting_shopify_permission_gate";
    }

    try {
      var cp = consentCache;
      if (!cp) {
        return {
          allowed: TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE,
          reason: unavailableReason,
          flags: privacyFlags(false, null, null, null)
        };
      }

      var marketingFlag = coercePrivacyFlag(cp.marketingAllowed);
      var analyticsFlag = coercePrivacyFlag(cp.analyticsProcessingAllowed);
      var saleOfDataFlag = coercePrivacyFlag(cp.saleOfDataAllowed);
      var flags = privacyFlags(true, marketingFlag, analyticsFlag, saleOfDataFlag);

      if (marketingFlag === true) return { allowed: true, reason: "marketing_allowed", flags: flags };
      if (marketingFlag === false && analyticsFlag !== true) return { allowed: false, reason: "marketing_denied", flags: flags };
      if (analyticsFlag === true) return { allowed: true, reason: "analytics_allowed_fallback", flags: flags };
      if (analyticsFlag === false) return { allowed: false, reason: "analytics_denied", flags: flags };

      return {
        allowed: TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE,
        reason: unknownReason,
        flags: flags
      };
    } catch (err) {
      return {
        allowed: TRUST_SHOPIFY_PERMISSION_GATE_WHEN_PRIVACY_UNAVAILABLE,
        reason: exceptionReason,
        flags: privacyFlags(false, null, null, null)
      };
    }
  }

  function privacyFlags(hasPrivacySnapshot, marketingAllowed, analyticsProcessingAllowed, saleOfDataAllowed) {
    return {
      hasPrivacySnapshot: hasPrivacySnapshot,
      marketingAllowed: marketingAllowed,
      analyticsProcessingAllowed: analyticsProcessingAllowed,
      saleOfDataAllowed: saleOfDataAllowed
    };
  }

  function safeLog(level, message, payload) {
    if (!DLM_DIAGNOSTIC_MODE) return;
    try {
      var logger = console[level] || console.log;
      if (!payload) payload = {};
      logger("[DLM Ads Pixel] " + message, payload);
    } catch (err) {
      // no-op
    }
  }

  function safeErrorPayload(err) {
    var payload = { errorName: "unknown", errorMessage: "unknown" };
    try {
      if (err && err.name) payload.errorName = String(err.name);
      if (err && err.message) payload.errorMessage = String(err.message);
      if (!err || !err.message) payload.errorMessage = String(err);
    } catch (e) {
      // no-op
    }
    return payload;
  }

  function getNested(obj, path) {
    var current = obj;
    for (var i = 0; i < path.length; i += 1) {
      if (!current) return null;
      current = current[path[i]];
    }
    return current;
  }

  function getEventId(event) {
    if (event && event.id) return event.id;
    return null;
  }

  function getEventName(event) {
    if (event && event.name) return event.name;
    return "checkout_completed";
  }

  function getCheckout(event) {
    if (event && event.data && event.data.checkout) return event.data.checkout;
    return {};
  }

  function bareOrderId(rawId) {
    if (!rawId) return "";
    var s = String(rawId);
    var m = s.match(/(\d+)\s*$/);
    if (m) return m[1];
    return s;
  }

  function urlFromEvent(event) {
    if (event && event.context && event.context.window && event.context.window.location && event.context.window.location.href) {
      return event.context.window.location.href;
    }
    try {
      if (typeof init !== "undefined" && init && init.context && init.context.window && init.context.window.location && init.context.window.location.href) {
        return init.context.window.location.href;
      }
    } catch (err) {
      // no-op
    }
    return "";
  }

  var storage = {
    get: function (key) {
      try {
        if (typeof browser !== "undefined" && browser && browser.localStorage && browser.localStorage.getItem) {
          return browser.localStorage.getItem(key);
        }
      } catch (err) {
        // no-op
      }
      return Promise.resolve(null);
    },
    set: function (key, value) {
      try {
        if (typeof browser !== "undefined" && browser && browser.localStorage && browser.localStorage.setItem) {
          return browser.localStorage.setItem(key, value);
        }
      } catch (err) {
        // no-op
      }
      return Promise.resolve();
    },
    remove: function (key) {
      try {
        if (typeof browser !== "undefined" && browser && browser.localStorage && browser.localStorage.removeItem) {
          return browser.localStorage.removeItem(key);
        }
      } catch (err) {
        // no-op
      }
      return Promise.resolve();
    }
  };

  function extractClickIds(url) {
    if (!url) return null;
    try {
      var params = new URL(url).searchParams;
      var clickIds = {};
      var keys = ["gclid", "gbraid", "wbraid", "gclsrc"];
      for (var i = 0; i < keys.length; i += 1) {
        var key = keys[i];
        var value = params.get(key);
        if (value) clickIds[key] = value;
      }
      if (Object.keys(clickIds).length > 0) return clickIds;
    } catch (err) {
      // no-op
    }
    return null;
  }

  function captureClickIdsFromPage(event) {
    var clickIds = extractClickIds(urlFromEvent(event));
    if (!clickIds) return Promise.resolve();
    var payload = {};
    var keys = Object.keys(clickIds);
    for (var i = 0; i < keys.length; i += 1) payload[keys[i]] = clickIds[keys[i]];
    payload.expiresAt = Date.now() + CLICK_ID_TTL_MS;
    safeLog("log", "stored Google click id(s)", {
      hasGclid: Boolean(payload.gclid),
      hasGbraid: Boolean(payload.gbraid),
      hasWbraid: Boolean(payload.wbraid),
      hasGclsrc: Boolean(payload.gclsrc)
    });
    return storage.set(CLICK_ID_STORAGE_KEY, JSON.stringify(payload));
  }

  function getStoredClickIds() {
    return storage.get(CLICK_ID_STORAGE_KEY).then(function (raw) {
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !parsed.expiresAt || parsed.expiresAt < Date.now()) {
        return storage.remove(CLICK_ID_STORAGE_KEY).then(function () { return null; });
      }
      return {
        gclid: parsed.gclid || null,
        gbraid: parsed.gbraid || null,
        wbraid: parsed.wbraid || null,
        gclsrc: parsed.gclsrc || null
      };
    }).catch(function () {
      return null;
    });
  }

  function buildConversionUrl(value, currency, transactionId, clickIds) {
    var params = new URLSearchParams();
    params.set("label", AW_CONVERSION_LABEL);
    params.set("value", String(value));
    params.set("currency_code", currency);
    params.set("currency", currency);
    params.set("oid", transactionId);
    params.set("transaction_id", transactionId);
    params.set("send_to", AW_CONVERSION_ID + "/" + AW_CONVERSION_LABEL);
    params.set("guid", "ON");
    params.set("script", "0");

    if (clickIds) {
      if (clickIds.gclid) params.set("gclid", String(clickIds.gclid));
      if (clickIds.gbraid) params.set("gbraid", String(clickIds.gbraid));
      if (clickIds.wbraid) params.set("wbraid", String(clickIds.wbraid));
      if (clickIds.gclsrc) params.set("gclsrc", String(clickIds.gclsrc));
    }

    return "https://www.googleadservices.com/pagead/conversion/" + encodeURIComponent(AW_ID_NUMERIC) + "/?" + params.toString();
  }

  function fireImageBackupBeacon(url) {
    if (!FIRE_IMAGE_BACKUP_BEACON) return false;
    try {
      var img = new Image(1, 1);
      img.referrerPolicy = "no-referrer-when-downgrade";
      img.src = url;
      imageBeaconRefs.push(img);
      return true;
    } catch (err) {
      return false;
    }
  }

  function fireConversion(value, currency, transactionId, clickIds) {
    var url = buildConversionUrl(value, currency, transactionId, clickIds);
    safeLog("log", "Conversion request attempted", {
      endpointHost: "www.googleadservices.com",
      endpointPath: "/pagead/conversion/" + AW_ID_NUMERIC + "/",
      value: value,
      currency: currency,
      oid: transactionId,
      transactionId: transactionId,
      hasGclid: Boolean(clickIds && clickIds.gclid),
      hasGbraid: Boolean(clickIds && clickIds.gbraid),
      hasWbraid: Boolean(clickIds && clickIds.wbraid)
    });

    return fetch(url, {
      method: "GET",
      mode: "no-cors",
      credentials: "include",
      keepalive: true,
      cache: "no-store"
    }).then(function () {
      var backupStarted = fireImageBackupBeacon(url);
      safeLog("log", "conversion fetch dispatched", {
        value: value,
        currency: currency,
        oid: transactionId,
        transactionId: transactionId,
        backupStarted: backupStarted
      });
    }).catch(function (err) {
      var backupStarted = fireImageBackupBeacon(url);
      var payload = safeErrorPayload(err);
      payload.backupStarted = backupStarted;
      safeLog("warn", "conversion dispatch failed; image backup attempted", payload);
    });
  }
}());
