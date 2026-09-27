/*
 * "Complete the family" cart upsell: behaviour for the server-rendered block
 * from snippets/dlm-complete-family.liquid (cart drawer and /cart).
 *
 * - A role chip ("+ Dad $35.99") opens that role's inline size <select>; only
 *   one panel is open per block. The last size picked for a role in this
 *   browser session is preselected (sessionStorage, nothing leaves the page).
 * - "Add" posts ONE variant to /cart/add.js with the host's own sections
 *   (cart-drawer-items or cart-items getSectionsToRender()) and swaps them in
 *   place, exactly like Dawn's quantity update path. The drawer stays open,
 *   keeps its scroll position and focus moves back to the block.
 * - Real variant prices only (rendered by Liquid). No discounts, no urgency.
 *
 * The block sits inside Dawn's cart forms, whose <cart-items> element runs a
 * quantity update on every bubbling "change" event. The select's change is
 * therefore handled (and stopped) in the capture phase on document.
 *
 * Pure helpers are exported for node tests (ops/tests/test_complete_family.mjs).
 * ES5 only; no build step. Delegated listeners, so re-rendered markup needs
 * no re-binding.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  if (root && root.document && !root.DLMCompleteFamily) {
    root.DLMCompleteFamily = api;
    api.autoStart(root);
  }
})(typeof window !== 'undefined' ? window : this, function () {
  'use strict';

  var STORAGE_PREFIX = 'dlm:lastSize:';
  var ROLE_KEYS = ['mother', 'father', 'girl', 'boy', 'child', 'baby', 'adult'];
  var ACTIONS = { open_role: true, add: true };
  var SURFACES = { drawer: true, cart: true };
  var MAX_SECTIONS = 5; // Shopify Section Rendering API limit per request

  // ---------------------------------------------------------------------
  // Pure helpers (tested in node)
  // ---------------------------------------------------------------------

  function isRole(role) {
    return ROLE_KEYS.indexOf(String(role || '')) !== -1;
  }

  function normalizeSize(value) {
    return String(value == null ? '' : value)
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
  }

  // Index of the size to preselect, or -1. `sizes` is the list of size
  // labels in select order (index 0 may be the empty placeholder).
  function pickRememberedIndex(sizes, remembered) {
    var wanted = normalizeSize(remembered);
    if (!wanted || !sizes) return -1;
    for (var i = 0; i < sizes.length; i += 1) {
      if (normalizeSize(sizes[i]) === wanted) return i;
    }
    return -1;
  }

  function readRememberedSize(storage, role) {
    if (!storage || !isRole(role)) return '';
    try {
      return String(storage.getItem(STORAGE_PREFIX + role) || '');
    } catch (error) {
      return '';
    }
  }

  function rememberSize(storage, role, size) {
    var value = String(size == null ? '' : size).trim();
    if (!storage || !isRole(role) || !value) return false;
    try {
      storage.setItem(STORAGE_PREFIX + role, value);
      return true;
    } catch (error) {
      return false;
    }
  }

  // Accepts section ids or Dawn's {id, section, selector} descriptors.
  function uniqueSectionIds(list) {
    var out = [];
    (list || []).forEach(function (entry) {
      var id = entry && typeof entry === 'object' ? entry.section : entry;
      id = id == null ? '' : String(id).trim();
      if (id && out.indexOf(id) === -1 && out.length < MAX_SECTIONS) out.push(id);
    });
    return out;
  }

  // Body for POST /cart/add.js: exactly one piece of one real variant.
  function buildAddBody(variantId, sections, sectionsUrl) {
    var id = Number(variantId);
    if (!(id > 0) || Math.floor(id) !== id) return null;
    var body = { items: [{ id: id, quantity: 1 }] };
    var ids = uniqueSectionIds(sections);
    if (ids.length) {
      body.sections = ids.join(',');
      if (sectionsUrl) body.sections_url = String(sectionsUrl);
    }
    return body;
  }

  // Same rule as getLocaleAwareRoute() in assets/cart.js.
  function localeAwareRoute(path, rootPath) {
    if (typeof path !== 'string' || !path || path.charAt(0) !== '/') return path;
    var rootValue = typeof rootPath === 'string' ? rootPath : '/';
    if (!rootValue || rootValue === '/') return path;
    var normalized = rootValue.charAt(rootValue.length - 1) === '/' ? rootValue.slice(0, -1) : rootValue;
    if (!normalized || normalized === '/') return path;
    if (path === normalized || path.indexOf(normalized + '/') === 0) return path;
    return normalized + path;
  }

  function cartAddJsUrl(routes, rootPath) {
    var base = (routes && routes.cart_add_url) || '/cart/add';
    if (!/\.js$/.test(base)) base += '.js';
    return localeAwareRoute(base, rootPath);
  }

  // Shopify /cart/add.js errors: {status: 422, message, description}.
  function errorText(parsed, fallback) {
    if (parsed && typeof parsed.description === 'string' && parsed.description.trim()) return parsed.description.trim();
    if (parsed && typeof parsed.message === 'string' && parsed.message.trim()) return parsed.message.trim();
    return String(fallback || '');
  }

  function isAddSuccess(ok, parsed) {
    return Boolean(ok && parsed && typeof parsed === 'object' && !parsed.status && Array.isArray(parsed.items));
  }

  // dataLayer event; ids and role keys only (no PII, no prices).
  function analyticsEvent(action, productId, role, surface) {
    if (!ACTIONS[action] || !isRole(role)) return null;
    var id = String(productId == null ? '' : productId).replace(/\D/g, '');
    return {
      event: 'dlm_complete_family',
      action: action,
      product_id: id,
      role: role,
      surface: SURFACES[surface] ? surface : 'drawer'
    };
  }

  function addedMessage(prefix, roleLabel, size) {
    var what = [String(roleLabel || '').trim(), String(size || '').trim()].filter(Boolean).join(' · ');
    return [String(prefix || '').trim(), what].filter(Boolean).join(': ');
  }

  // ---------------------------------------------------------------------
  // DOM layer
  // ---------------------------------------------------------------------

  function closest(node, selector) {
    return node && node.closest ? node.closest(selector) : null;
  }

  function sessionStore(win) {
    try {
      return win.sessionStorage || null;
    } catch (error) {
      return null;
    }
  }

  function selectedOption(select) {
    return select && select.selectedIndex >= 0 ? select.options[select.selectedIndex] : null;
  }

  function autoStart(win) {
    var doc = win.document;
    if (!doc || doc.documentElement.hasAttribute('data-dlm-cf-ready')) return;
    doc.documentElement.setAttribute('data-dlm-cf-ready', '');

    function syncPanel(panel) {
      if (!panel) return;
      var select = panel.querySelector('[data-dlm-cf-select]');
      var price = panel.querySelector('[data-dlm-cf-price]');
      var add = panel.querySelector('[data-dlm-cf-add]');
      var option = selectedOption(select);
      var hasValue = Boolean(option && option.value);
      if (price) price.textContent = hasValue ? option.getAttribute('data-money') || '' : price.getAttribute('data-default') || '';
      if (add && !add.hasAttribute('aria-busy')) add.disabled = !hasValue;
    }

    function preselect(panel, role) {
      var select = panel.querySelector('[data-dlm-cf-select]');
      if (!select || select.value) return;
      var sizes = [];
      for (var i = 0; i < select.options.length; i += 1) {
        sizes.push(select.options[i].value ? select.options[i].getAttribute('data-size') || '' : '');
      }
      var index = pickRememberedIndex(sizes, readRememberedSize(sessionStore(win), role));
      if (index > 0) select.selectedIndex = index;
    }

    function pushAnalytics(action, productId, role, surface) {
      var payload = analyticsEvent(action, productId, role, surface);
      if (!payload) return;
      try {
        win.dataLayer = win.dataLayer || [];
        win.dataLayer.push(payload);
      } catch (error) {
        /* analytics is optional */
      }
    }

    function togglePanel(chip) {
      var block = closest(chip, '[data-dlm-complete-family]');
      var panel = doc.getElementById(chip.getAttribute('aria-controls') || '');
      if (!block || !panel) return;
      var opening = chip.getAttribute('aria-expanded') !== 'true';
      block.querySelectorAll('[data-dlm-cf-chip]').forEach(function (other) {
        other.setAttribute('aria-expanded', 'false');
      });
      block.querySelectorAll('[data-dlm-cf-panel]').forEach(function (other) {
        other.hidden = true;
      });
      if (!opening) return;
      var role = chip.getAttribute('data-role');
      chip.setAttribute('aria-expanded', 'true');
      panel.hidden = false;
      preselect(panel, role);
      syncPanel(panel);
      var select = panel.querySelector('[data-dlm-cf-select]');
      if (select && typeof select.focus === 'function') select.focus();
      var add = panel.querySelector('[data-dlm-cf-add]');
      pushAnalytics('open_role', add && add.getAttribute('data-product-id'), role, block.getAttribute('data-surface'));
    }

    function showError(block, message) {
      var box = block && block.querySelector('[data-dlm-cf-error]');
      if (!box) return;
      box.textContent = message || '';
      box.hidden = !message;
    }

    function announce(surface, message) {
      if (!message) return;
      // The region is part of freshly swapped markup; a short delay lets
      // assistive tech register it before the text changes.
      win.setTimeout(function () {
        var block = doc.querySelector('[data-dlm-complete-family][data-surface="' + surface + '"]');
        var region =
          (block && block.querySelector('[data-dlm-cf-status]')) ||
          doc.getElementById(surface === 'cart' ? 'cart-live-region-text' : 'CartDrawer-LiveRegionText');
        if (region) region.textContent = message;
      }, 150);
    }

    function swapSections(descriptors, htmlBySection) {
      var parser = new win.DOMParser();
      descriptors.forEach(function (descriptor) {
        var container = doc.getElementById(descriptor.id);
        var html = htmlBySection[descriptor.section];
        if (!container || typeof html !== 'string') return;
        var target = (descriptor.selector && container.querySelector(descriptor.selector)) || container;
        var parsed = parser.parseFromString(html, 'text/html');
        var source = parsed.querySelector(descriptor.selector || '.shopify-section') || parsed.querySelector('.shopify-section');
        if (source) target.innerHTML = source.innerHTML;
      });
    }

    function restoreFocus(surface, variantId) {
      var block = doc.querySelector('[data-dlm-complete-family][data-surface="' + surface + '"]');
      var target =
        (block && block.querySelector('.dlm-cf__heading')) ||
        doc.querySelector('.cart-item[data-variant-id="' + variantId + '"] .cart-item__name') ||
        doc.querySelector(surface === 'cart' ? '#main-cart-title' : '#CartDrawer .drawer__inner');
      if (!target) return;
      var drawer = surface === 'drawer' ? doc.getElementById('CartDrawer') : null;
      if (drawer && typeof win.trapFocus === 'function') {
        win.trapFocus(drawer, target);
      } else if (typeof target.focus === 'function') {
        target.focus();
      }
    }

    function publishUpdate(parsed, variantId) {
      try {
        if (typeof win.publish === 'function' && win.PUB_SUB_EVENTS && win.PUB_SUB_EVENTS.cartUpdate) {
          // source 'cart-items' is Dawn's signal that the cart sections were
          // already re-rendered (as in CartItems.updateQuantity), so cart
          // components do not fetch and replace them a second time.
          win.publish(win.PUB_SUB_EVENTS.cartUpdate, {
            source: 'cart-items',
            origin: 'dlm-complete-family',
            cartData: parsed,
            variantId: variantId
          });
        }
      } catch (error) {
        /* subscribers are optional */
      }
    }

    function submit(addButton) {
      var block = closest(addButton, '[data-dlm-complete-family]');
      var panel = closest(addButton, '[data-dlm-cf-panel]');
      if (!block || !panel || block.hasAttribute('data-busy')) return;
      var select = panel.querySelector('[data-dlm-cf-select]');
      var option = selectedOption(select);
      if (!option || !option.value) {
        if (select) select.focus();
        return;
      }

      var surface = block.getAttribute('data-surface') || 'drawer';
      var role = addButton.getAttribute('data-role') || '';
      var chip = doc.querySelector('[aria-controls="' + panel.id + '"]');
      var roleLabel = chip ? chip.getAttribute('data-role-label') : '';
      var size = option.getAttribute('data-size') || option.textContent;
      var variantId = option.value;
      var host = closest(block, 'cart-drawer-items') || closest(block, 'cart-items');
      var descriptors = [];
      if (host && typeof host.getSectionsToRender === 'function') {
        try {
          descriptors = host.getSectionsToRender() || [];
        } catch (error) {
          descriptors = [];
        }
      }
      var body = buildAddBody(variantId, descriptors, win.location.pathname);
      if (!body) return;

      var scroller = host && host.tagName === 'CART-DRAWER-ITEMS' ? host : null;
      var scrollTop = scroller ? scroller.scrollTop : 0;

      block.setAttribute('data-busy', '');
      addButton.setAttribute('aria-busy', 'true');
      addButton.disabled = true;
      showError(block, '');

      var config =
        typeof win.fetchConfig === 'function'
          ? win.fetchConfig('json')
          : { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' } };
      config.headers = config.headers || {};
      config.headers['X-Requested-With'] = 'XMLHttpRequest';
      config.body = JSON.stringify(body);

      var responseOk = false;
      var shopifyRoot = win.Shopify && win.Shopify.routes ? win.Shopify.routes.root : '/';
      win
        .fetch(cartAddJsUrl(win.routes, shopifyRoot), config)
        .then(function (response) {
          responseOk = response.ok;
          return response.json();
        })
        .then(function (parsed) {
          if (!isAddSuccess(responseOk, parsed)) {
            showError(block, errorText(parsed, block.getAttribute('data-msg-error')));
            return;
          }
          rememberSize(sessionStore(win), role, option.getAttribute('data-size'));
          pushAnalytics('add', addButton.getAttribute('data-product-id'), role, surface);
          if (!parsed.sections || !descriptors.length) {
            win.location.href = localeAwareRoute((win.routes && win.routes.cart_url) || '/cart', shopifyRoot);
            return;
          }
          try {
            swapSections(descriptors, parsed.sections);
          } catch (error) {
            // The piece is in the cart; show it on the cart page instead of a
            // misleading "could not add" message.
            win.location.href = localeAwareRoute((win.routes && win.routes.cart_url) || '/cart', shopifyRoot);
            return;
          }
          if (scroller) {
            var freshScroller = doc.querySelector('cart-drawer-items');
            if (freshScroller) freshScroller.scrollTop = scrollTop;
          }
          restoreFocus(surface, variantId);
          announce(surface, addedMessage(block.getAttribute('data-msg-added'), roleLabel, size));
          publishUpdate(parsed, variantId);
        })
        .catch(function (error) {
          showError(block, block.getAttribute('data-msg-error'));
          if (win.console) win.console.error(error);
        })
        .then(function () {
          // Only reached with the old block still in the page when the add
          // failed; after a success the block was replaced by fresh markup.
          block.removeAttribute('data-busy');
          addButton.removeAttribute('aria-busy');
          syncPanel(panel);
        });
    }

    doc.addEventListener('click', function (event) {
      var chip = closest(event.target, '[data-dlm-cf-chip]');
      if (chip) {
        event.preventDefault();
        togglePanel(chip);
        return;
      }
      var add = closest(event.target, '[data-dlm-cf-add]');
      if (add) {
        event.preventDefault();
        if (!add.disabled) submit(add);
      }
    });

    // Capture phase: runs before <cart-items>/<cart-drawer-items> see the
    // change, which they would otherwise treat as a line quantity update.
    doc.addEventListener(
      'change',
      function (event) {
        var select = closest(event.target, '[data-dlm-cf-select]');
        if (!select) return;
        event.stopPropagation();
        syncPanel(closest(select, '[data-dlm-cf-panel]'));
        var block = closest(select, '[data-dlm-complete-family]');
        if (block) showError(block, '');
      },
      true
    );
  }

  return {
    STORAGE_PREFIX: STORAGE_PREFIX,
    ROLE_KEYS: ROLE_KEYS,
    isRole: isRole,
    normalizeSize: normalizeSize,
    pickRememberedIndex: pickRememberedIndex,
    readRememberedSize: readRememberedSize,
    rememberSize: rememberSize,
    uniqueSectionIds: uniqueSectionIds,
    buildAddBody: buildAddBody,
    localeAwareRoute: localeAwareRoute,
    cartAddJsUrl: cartAddJsUrl,
    errorText: errorText,
    isAddSuccess: isAddSuccess,
    analyticsEvent: analyticsEvent,
    addedMessage: addedMessage,
    autoStart: autoStart
  };
});
