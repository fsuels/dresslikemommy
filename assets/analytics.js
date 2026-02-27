window.dataLayer = window.dataLayer || [];

(function () {
  if (window.__dlmAnalyticsInitialized) return;
  window.__dlmAnalyticsInitialized = true;

  var state = {
    productData: null,
    productDataLoaded: false,
    viewItemPushed: false,
    viewedListKeys: {},
    listViewObserver: null,
    listMutationObserver: null,
    cartSnapshot: {},
    cartSnapshotLoaded: false,
    taxonomyCacheByVariantId: {},
    lastViewCartSignature: '',
    lastCheckoutTimestamp: 0,
  };

  function safeParseJSON(input) {
    try {
      return JSON.parse(input);
    } catch (e) {
      return null;
    }
  }

  function normalizeText(value) {
    if (value === null || value === undefined) return '';
    return String(value).trim();
  }

  function parseNumber(value) {
    if (value === null || value === undefined || value === '') return null;
    var parsed = typeof value === 'number' ? value : parseFloat(value);
    if (!Number.isFinite(parsed)) return null;
    return parsed;
  }

  function parseMoney(value, forceCents) {
    var parsed = parseNumber(value);
    if (parsed === null) return null;

    if (forceCents) return parsed / 100;

    if (Math.abs(parsed) > 1000 && Math.floor(parsed) === parsed) {
      return parsed / 100;
    }

    return parsed;
  }

  function parsePositiveInteger(value, fallback) {
    var parsed = parseInt(value, 10);
    if (!Number.isFinite(parsed) || parsed <= 0) return fallback || 0;
    return parsed;
  }

  function getExperimentContext() {
    try {
      var cfg = window.experimentConfig || {};
      var enabled = !!cfg.enabled;
      var flags = [];
      if (cfg.flags && typeof cfg.flags === 'object' && !Array.isArray(cfg.flags)) {
        for (var key in cfg.flags) {
          if (!Object.prototype.hasOwnProperty.call(cfg.flags, key)) continue;
          if (cfg.flags[key]) flags.push(key);
        }
      } else if (Array.isArray(cfg.flags)) {
        flags = cfg.flags;
      }
      return {
        experiments_enabled: enabled,
        experiment_flags: flags,
      };
    } catch (e) {
      return {};
    }
  }

  function pushToDataLayer(payload) {
    if (!payload || typeof payload !== 'object') return;
    try {
      var experimentContext = getExperimentContext();
      window.dataLayer.push(Object.assign({}, experimentContext, payload));
    } catch (e) {
      // no-op
    }
  }

  function getCurrency() {
    var meta = document.querySelector('meta[property="og:price:currency"]');
    if (meta && normalizeText(meta.content)) return normalizeText(meta.content);

    if (
      window.Shopify &&
      window.Shopify.currency &&
      normalizeText(window.Shopify.currency.active)
    ) {
      return normalizeText(window.Shopify.currency.active);
    }

    return 'USD';
  }

  function cleanObject(input) {
    var output = {};
    Object.keys(input).forEach(function (key) {
      var value = input[key];
      if (value === undefined || value === null || value === '') return;
      output[key] = value;
    });
    return output;
  }

  function getSubcategory2Token(subcategory2) {
    var normalized = normalizeText(subcategory2);
    if (!normalized) return '';

    var pieces = normalized.split(/[|,>\/]/);
    for (var i = 0; i < pieces.length; i += 1) {
      var token = normalizeText(pieces[i]);
      if (token) return token;
    }

    return '';
  }

  function normalizeVariant(rawVariant) {
    if (!rawVariant || typeof rawVariant !== 'object') return null;

    var hasPrice =
      rawVariant.price !== undefined && rawVariant.price !== null && rawVariant.price !== '';
    var price = hasPrice
      ? parseMoney(rawVariant.price, false)
      : parseMoney(rawVariant.price_cents, true);

    return {
      id: normalizeText(rawVariant.id),
      title: normalizeText(rawVariant.title),
      sku: normalizeText(rawVariant.sku),
      price: price,
      barcode: normalizeText(rawVariant.barcode),
    };
  }

  function normalizeProductData(rawData) {
    if (!rawData || typeof rawData !== 'object' || Array.isArray(rawData)) return null;

    var variants = [];
    if (Array.isArray(rawData.variants)) {
      variants = rawData.variants.map(normalizeVariant).filter(Boolean);
    }

    var hasPrice = rawData.price !== undefined && rawData.price !== null && rawData.price !== '';
    var normalizedPrice = hasPrice
      ? parseMoney(rawData.price, false)
      : parseMoney(rawData.price_cents, true);

    var selectedVariantId =
      normalizeText(rawData.selected_variant_id) ||
      normalizeText(rawData.selected_or_first_variant_id) ||
      normalizeText(rawData.current_variant_id) ||
      (variants[0] && variants[0].id) ||
      '';

    return {
      id: normalizeText(rawData.id),
      title: normalizeText(rawData.title),
      handle: normalizeText(rawData.handle),
      vendor: normalizeText(rawData.vendor),
      category1: normalizeText(rawData.category1),
      subcategory: normalizeText(rawData.subcategory),
      subcategory2: normalizeText(rawData.subcategory2),
      type: normalizeText(rawData.type),
      style: normalizeText(rawData.style),
      pattern: normalizeText(rawData.pattern),
      price: normalizedPrice,
      selectedVariantId: selectedVariantId,
      variants: variants,
    };
  }

  function buildFallbackProductData() {
    var ogTitle = document.querySelector('meta[property="og:title"]');
    var ogPrice = document.querySelector('meta[property="og:price:amount"]') || document.querySelector('meta[property="product:price:amount"]');
    var category1Meta = document.querySelector('meta[name="custom-category1"]');
    var subcategoryMeta = document.querySelector('meta[name="custom-subcategory"]');
    var typeMeta = document.querySelector('meta[name="custom-type"]');
    var styleMeta = document.querySelector('meta[name="custom-style"]');
    var patternMeta = document.querySelector('meta[name="custom-pattern"]');
    var handleMatch = window.location.pathname.match(/\/products\/([^/?#]+)/);

    return {
      id: '',
      title: normalizeText(ogTitle && ogTitle.content),
      handle: handleMatch && handleMatch[1] ? normalizeText(handleMatch[1]) : '',
      vendor: '',
      category1: normalizeText(category1Meta && category1Meta.content),
      subcategory: normalizeText(subcategoryMeta && subcategoryMeta.content),
      subcategory2: '',
      type: normalizeText(typeMeta && typeMeta.content),
      style: normalizeText(styleMeta && styleMeta.content),
      pattern: normalizeText(patternMeta && patternMeta.content),
      price: parseMoney(ogPrice && ogPrice.content, false),
      selectedVariantId: '',
      variants: [],
    };
  }

  function loadProductData() {
    if (state.productDataLoaded) return state.productData;
    state.productDataLoaded = true;

    var rawData = null;

    var analyticsScript = document.querySelector('script[id^="ProductAnalyticsData-"]');
    if (analyticsScript) {
      rawData = safeParseJSON(analyticsScript.textContent);
    }

    if (!rawData) {
      var secondaryScript = document.querySelector('script[id^="AnalyticsProductJSON-"]');
      if (secondaryScript) {
        rawData = safeParseJSON(secondaryScript.textContent);
      }
    }

    if (!rawData) {
      var legacyScript = document.querySelector('script[id^="ProductJSON-"]');
      if (legacyScript) {
        rawData = safeParseJSON(legacyScript.textContent);
      }
    }

    state.productData = normalizeProductData(rawData);

    if (!state.productData && window.location.pathname.indexOf('/products/') !== -1) {
      state.productData = buildFallbackProductData();
    }

    return state.productData;
  }

  function getSelectedVariantId() {
    var selectedIdInput = document.querySelector('form[action*="/cart/add"] [name="id"]');
    return normalizeText(selectedIdInput && selectedIdInput.value);
  }

  function getVariantById(productData, variantId) {
    if (!productData || !Array.isArray(productData.variants) || !productData.variants.length) return null;

    var desiredId = normalizeText(variantId) || normalizeText(productData.selectedVariantId);
    if (!desiredId) return productData.variants[0];

    for (var i = 0; i < productData.variants.length; i += 1) {
      if (normalizeText(productData.variants[i].id) === desiredId) {
        return productData.variants[i];
      }
    }

    return productData.variants[0];
  }

  function buildBaseItem(attributes) {
    var typeValue = normalizeText(attributes.type);
    var subcategory2Value = normalizeText(attributes.subcategory2);

    return cleanObject({
      item_id: normalizeText(attributes.productId) || normalizeText(attributes.variantId),
      item_name: normalizeText(attributes.title),
      item_brand: normalizeText(attributes.vendor),
      item_variant: normalizeText(attributes.variant),
      price: parseNumber(attributes.price),
      currency: getCurrency(),
      item_category: normalizeText(attributes.category1),
      item_category2: normalizeText(attributes.subcategory),
      item_category3: typeValue || getSubcategory2Token(subcategory2Value),
      item_category4: normalizeText(attributes.style),
      item_category5: normalizeText(attributes.pattern),
      item_type: typeValue,
      custom_category1: normalizeText(attributes.category1),
      custom_subcategory: normalizeText(attributes.subcategory),
      custom_type: typeValue,
      custom_style: normalizeText(attributes.style),
      custom_pattern: normalizeText(attributes.pattern),
      product_handle: normalizeText(attributes.handle),
    });
  }

  function buildEcommerceItem(productData, variantId) {
    if (!productData) return null;

    var variant = getVariantById(productData, variantId);
    var resolvedPrice = variant && variant.price !== null ? variant.price : productData.price;
    var resolvedVariant =
      (variant && variant.sku) ||
      (variant && variant.title) ||
      (variant && variant.id) ||
      normalizeText(variantId);

    return buildBaseItem({
      productId: productData.id || (variant && variant.id) || '',
      variantId: variant && variant.id,
      title: productData.title,
      vendor: productData.vendor,
      variant: resolvedVariant,
      price: resolvedPrice,
      category1: productData.category1,
      subcategory: productData.subcategory,
      subcategory2: productData.subcategory2,
      type: productData.type,
      style: productData.style,
      pattern: productData.pattern,
      handle: productData.handle,
    });
  }

  function getRequestedQuantity() {
    var quantityInput = document.querySelector(
      'product-form .quantity__input, form[action*="/cart/add"] .quantity__input'
    );
    var quantity = parseInt(quantityInput && quantityInput.value, 10);
    return Number.isFinite(quantity) && quantity > 0 ? quantity : 1;
  }

  function roundToTwo(value) {
    return Math.round(value * 100) / 100;
  }

  function buildEcommercePayload(items) {
    var normalizedItems = Array.isArray(items) ? items.filter(Boolean) : [];
    var total = 0;

    for (var i = 0; i < normalizedItems.length; i += 1) {
      var item = normalizedItems[i];
      var price = parseNumber(item.price);
      var quantity = parsePositiveInteger(item.quantity, 1);
      if (price !== null) {
        total += price * quantity;
      }
    }

    var payload = {
      currency: getCurrency(),
      items: normalizedItems,
    };

    if (normalizedItems.length) {
      payload.value = roundToTwo(total);
    }

    return payload;
  }

  function getCartUpdateEventName() {
    return (
      (typeof PUB_SUB_EVENTS !== 'undefined' && PUB_SUB_EVENTS && PUB_SUB_EVENTS.cartUpdate) ||
      (window.PUB_SUB_EVENTS && window.PUB_SUB_EVENTS.cartUpdate) ||
      'cart-update'
    );
  }

  function getListContainer(element) {
    if (!element || !element.closest) return null;
    return element.closest('[id^="shopify-section-"], .shopify-section, section, [data-section-id], [data-id]');
  }

  function getListContext(element) {
    var container = getListContainer(element);

    var listId = normalizeText(
      container &&
        (container.getAttribute('id') ||
          container.getAttribute('data-section-id') ||
          container.getAttribute('data-id') ||
          container.getAttribute('data-analytics-list-id'))
    );
    if (!listId) listId = 'catalog';

    var listName = normalizeText(container && container.getAttribute('data-analytics-list-name'));
    if (!listName && container) {
      var heading = container.querySelector('h1, h2, h3');
      listName = normalizeText(heading && heading.textContent);
    }
    if (!listName) listName = listId;

    return {
      container: container,
      item_list_id: listId,
      item_list_name: listName,
    };
  }

  function getCardIndex(card, listContext) {
    if (!card) return 1;
    var container = (listContext && listContext.container) || card.parentElement;
    if (!container) return 1;

    var cards = container.querySelectorAll('[data-analytics-product-card="true"]');
    for (var i = 0; i < cards.length; i += 1) {
      if (cards[i] === card) return i + 1;
    }
    return 1;
  }

  function buildCardItem(card, listContext) {
    if (!card) return null;

    var price = parseMoney(card.getAttribute('data-analytics-price-cents'), true);
    var item = buildBaseItem({
      productId: card.getAttribute('data-analytics-product-id'),
      variantId: card.getAttribute('data-analytics-variant-id'),
      title: card.getAttribute('data-analytics-title'),
      vendor: card.getAttribute('data-analytics-vendor'),
      variant: card.getAttribute('data-analytics-variant'),
      price: price,
      category1: card.getAttribute('data-analytics-category1'),
      subcategory: card.getAttribute('data-analytics-subcategory'),
      subcategory2: card.getAttribute('data-analytics-subcategory2'),
      type: card.getAttribute('data-analytics-type'),
      style: card.getAttribute('data-analytics-style'),
      pattern: card.getAttribute('data-analytics-pattern'),
      handle: card.getAttribute('data-analytics-handle'),
    });

    if (!item || !item.item_name) return null;

    item.index = getCardIndex(card, listContext);
    return item;
  }

  function getCardTrackingKey(card, listContext) {
    var productId = normalizeText(card && card.getAttribute('data-analytics-product-id'));
    var handle = normalizeText(card && card.getAttribute('data-analytics-handle'));
    var listId = normalizeText(listContext && listContext.item_list_id);
    return [productId || handle, listId].join('|');
  }

  function pushViewItemList(card) {
    if (!card) return;

    var listContext = getListContext(card);
    var key = getCardTrackingKey(card, listContext);
    if (!key || state.viewedListKeys[key]) return;

    var item = buildCardItem(card, listContext);
    if (!item) return;

    state.viewedListKeys[key] = true;
    pushToDataLayer({
      event: 'view_item_list',
      ecommerce: {
        item_list_id: listContext.item_list_id,
        item_list_name: listContext.item_list_name,
        items: [item],
      },
    });
  }

  function observeProductCards(root) {
    var source = root || document;
    var cards = source.querySelectorAll
      ? source.querySelectorAll('[data-analytics-product-card="true"]')
      : [];

    if (!cards.length) return;

    if (!('IntersectionObserver' in window)) {
      for (var j = 0; j < cards.length; j += 1) {
        pushViewItemList(cards[j]);
      }
      return;
    }

    if (!state.listViewObserver) {
      state.listViewObserver = new IntersectionObserver(
        function (entries, observer) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            if (entry.intersectionRatio < 0.4) return;

            pushViewItemList(entry.target);
            observer.unobserve(entry.target);
          });
        },
        { threshold: [0.4] }
      );
    }

    for (var i = 0; i < cards.length; i += 1) {
      state.listViewObserver.observe(cards[i]);
    }
  }

  function initProductListTracking() {
    observeProductCards(document);

    if (!('MutationObserver' in window) || !document.body) return;

    state.listMutationObserver = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (!mutation.addedNodes || !mutation.addedNodes.length) return;

        for (var i = 0; i < mutation.addedNodes.length; i += 1) {
          var node = mutation.addedNodes[i];
          if (!node || node.nodeType !== 1) continue;
          observeProductCards(node);
        }
      });
    });

    state.listMutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  function initSelectItemTracking() {
    document.addEventListener('click', function (event) {
      var target = event.target;
      if (!target || !target.closest) return;

      var link = target.closest('a[href]');
      if (!link) return;

      var card = link.closest('[data-analytics-product-card="true"]');
      if (!card) return;

      var listContext = getListContext(card);
      var item = buildCardItem(card, listContext);
      if (!item) return;

      pushToDataLayer({
        event: 'select_item',
        ecommerce: {
          item_list_id: listContext.item_list_id,
          item_list_name: listContext.item_list_name,
          items: [item],
        },
      });
    });
  }

  function cacheTaxonomyFromItem(item, variantId) {
    var key = normalizeText(variantId);
    if (!key || !item) return;

    state.taxonomyCacheByVariantId[key] = cleanObject({
      item_category: item.item_category,
      item_category2: item.item_category2,
      item_category3: item.item_category3,
      item_category4: item.item_category4,
      item_category5: item.item_category5,
      item_type: item.item_type,
      custom_category1: item.custom_category1,
      custom_subcategory: item.custom_subcategory,
      custom_type: item.custom_type,
      custom_style: item.custom_style,
      custom_pattern: item.custom_pattern,
      product_handle: item.product_handle,
    });
  }

  function buildCartRowItem(row) {
    if (!row) return null;

    var variantId = normalizeText(row.getAttribute('data-variant-id'));
    var productId = normalizeText(row.getAttribute('data-product-id'));
    var lineKey = normalizeText(row.getAttribute('data-line-key'));
    var quantity = parsePositiveInteger(row.getAttribute('data-quantity'), 1);

    var quantityInput = row.querySelector && row.querySelector('input.quantity__input');
    if (quantityInput) {
      quantity = parsePositiveInteger(quantityInput.value, quantity);
    }

    var item = buildBaseItem({
      productId: productId,
      variantId: variantId,
      title: row.getAttribute('data-item-name'),
      vendor: row.getAttribute('data-item-brand'),
      variant: row.getAttribute('data-item-variant') || variantId,
      price: parseMoney(row.getAttribute('data-price-cents'), true),
      category1: row.getAttribute('data-category1'),
      subcategory: row.getAttribute('data-subcategory'),
      subcategory2: row.getAttribute('data-subcategory2'),
      type: row.getAttribute('data-type'),
      style: row.getAttribute('data-style'),
      pattern: row.getAttribute('data-pattern'),
      handle: row.getAttribute('data-product-handle'),
    });

    if (!item || !item.item_name) return null;

    cacheTaxonomyFromItem(item, variantId);

    return {
      key: lineKey || variantId || productId,
      quantity: quantity,
      variantId: variantId,
      item: item,
    };
  }

  function snapshotHasEntries(snapshot) {
    return !!snapshot && Object.keys(snapshot).length > 0;
  }

  function getCartSnapshotFromDom() {
    var rows = document.querySelectorAll('[data-cart-item="true"]');
    var snapshot = {};

    for (var i = 0; i < rows.length; i += 1) {
      var rowItem = buildCartRowItem(rows[i]);
      if (!rowItem || !rowItem.key) continue;

      if (snapshot[rowItem.key]) {
        snapshot[rowItem.key].quantity += rowItem.quantity;
      } else {
        snapshot[rowItem.key] = rowItem;
      }
    }

    return snapshot;
  }

  function buildCartSnapshotFromEventData(cartData) {
    var snapshot = {};
    if (!cartData || !Array.isArray(cartData.items)) return snapshot;

    for (var i = 0; i < cartData.items.length; i += 1) {
      var cartItem = cartData.items[i];
      if (!cartItem) continue;

      var variantId = normalizeText(cartItem.variant_id || cartItem.id);
      var productId = normalizeText(cartItem.product_id || cartItem.id);
      var lineKey = normalizeText(cartItem.key) || variantId || productId;
      var priceCents =
        cartItem.final_price !== undefined && cartItem.final_price !== null
          ? cartItem.final_price
          : cartItem.price;
      var cachedTaxonomy = state.taxonomyCacheByVariantId[variantId] || {};

      var item = cleanObject(
        Object.assign(
          {
            item_id: productId || variantId,
            item_name: normalizeText(cartItem.product_title || cartItem.title),
            item_brand: normalizeText(cartItem.vendor),
            item_variant:
              normalizeText(cartItem.sku) ||
              normalizeText(cartItem.variant_title) ||
              variantId,
            price: parseMoney(priceCents, true),
            currency: getCurrency(),
          },
          cachedTaxonomy
        )
      );

      if (!item.item_name) continue;

      snapshot[lineKey] = {
        key: lineKey,
        quantity: parsePositiveInteger(cartItem.quantity, 1),
        variantId: variantId,
        item: item,
      };

      cacheTaxonomyFromItem(item, variantId);
    }

    return snapshot;
  }

  function buildEcommerceFromSnapshot(snapshot) {
    var items = [];

    Object.keys(snapshot || {}).forEach(function (key) {
      var entry = snapshot[key];
      if (!entry || !entry.item) return;

      var item = Object.assign({}, entry.item);
      item.quantity = parsePositiveInteger(entry.quantity, 1);
      items.push(item);
    });

    return buildEcommercePayload(items);
  }

  function buildCartSignature(snapshot) {
    var parts = [];

    Object.keys(snapshot || {})
      .sort()
      .forEach(function (key) {
        var entry = snapshot[key];
        if (!entry || !entry.item) return;
        parts.push(
          [
            normalizeText(entry.item.item_id),
            normalizeText(entry.item.item_variant),
            parsePositiveInteger(entry.quantity, 1),
          ].join(':')
        );
      });

    return parts.join('|');
  }

  function setCartSnapshot(snapshot) {
    state.cartSnapshot = snapshot || {};
    state.cartSnapshotLoaded = true;
  }

  function refreshCartSnapshot(eventData) {
    var fromDom = getCartSnapshotFromDom();
    if (snapshotHasEntries(fromDom)) {
      setCartSnapshot(fromDom);
      return fromDom;
    }

    var fromEvent = buildCartSnapshotFromEventData(eventData && eventData.cartData);
    setCartSnapshot(fromEvent);
    return fromEvent;
  }

  function pushRemoveFromCartDiff(previousSnapshot, nextSnapshot) {
    if (!snapshotHasEntries(previousSnapshot)) return;

    Object.keys(previousSnapshot).forEach(function (key) {
      var previousEntry = previousSnapshot[key];
      if (!previousEntry || !previousEntry.item) return;

      var previousQty = parsePositiveInteger(previousEntry.quantity, 0);
      var nextEntry = nextSnapshot[key];
      var nextQty = nextEntry ? parsePositiveInteger(nextEntry.quantity, 0) : 0;
      if (nextQty >= previousQty) return;

      var removedQty = previousQty - nextQty;
      var removedItem = Object.assign({}, previousEntry.item, { quantity: removedQty });
      var ecommerce = buildEcommercePayload([removedItem]);

      pushToDataLayer({
        event: 'remove_from_cart',
        ecommerce: ecommerce,
      });
    });
  }

  function pushViewCartEvent(context, eventData) {
    var snapshot = state.cartSnapshotLoaded ? state.cartSnapshot : refreshCartSnapshot(eventData);
    if (!snapshotHasEntries(snapshot)) {
      snapshot = buildCartSnapshotFromEventData(eventData && eventData.cartData);
    }
    if (!snapshotHasEntries(snapshot)) return;

    var signature = [normalizeText(context), buildCartSignature(snapshot)].join('|');
    if (signature === state.lastViewCartSignature) return;
    state.lastViewCartSignature = signature;

    pushToDataLayer({
      event: 'view_cart',
      cart_context: context,
      ecommerce: buildEcommerceFromSnapshot(snapshot),
    });
  }

  function pushBeginCheckoutEvent(source, eventData) {
    var now = Date.now();
    if (now - state.lastCheckoutTimestamp < 400) return;
    state.lastCheckoutTimestamp = now;

    var snapshot = state.cartSnapshotLoaded ? state.cartSnapshot : refreshCartSnapshot(eventData);
    if (!snapshotHasEntries(snapshot) && eventData && eventData.cartData) {
      snapshot = buildCartSnapshotFromEventData(eventData.cartData);
    }

    var ecommerce = snapshotHasEntries(snapshot)
      ? buildEcommerceFromSnapshot(snapshot)
      : { currency: getCurrency() };

    pushToDataLayer({
      event: 'begin_checkout',
      checkout_source: normalizeText(source),
      ecommerce: ecommerce,
    });
  }

  function pushViewItemOnce() {
    if (state.viewItemPushed) return;

    var productData = loadProductData();
    var item = buildEcommerceItem(productData, getSelectedVariantId());
    if (!item || !item.item_name) return;

    state.viewItemPushed = true;
    pushToDataLayer({
      event: 'view_item',
      ecommerce: buildEcommercePayload([item]),
    });
  }

  function pushAddToCartEvent(variantId, quantity) {
    var productData = loadProductData();
    var item = buildEcommerceItem(productData, variantId || getSelectedVariantId());

    if (!item) {
      pushToDataLayer({ event: 'add_to_cart' });
      return;
    }

    item.quantity = parsePositiveInteger(quantity, 1);

    pushToDataLayer({
      event: 'add_to_cart',
      ecommerce: buildEcommercePayload([item]),
    });
  }

  function initProductAddToCartTracking() {
    if (typeof subscribe !== 'function') return;

    try {
      subscribe(getCartUpdateEventName(), function (eventData) {
        if (!eventData || eventData.source !== 'product-form') return;

        var quantity = parseInt(eventData.quantity, 10);
        if (!Number.isFinite(quantity) || quantity <= 0) {
          quantity = getRequestedQuantity();
        }

        pushAddToCartEvent(eventData.productVariantId || eventData.variantId, quantity);
      });
    } catch (e) {
      // no-op
    }
  }

  function initCartStateTracking() {
    refreshCartSnapshot();

    if (window.location.pathname.indexOf('/cart') === 0) {
      pushViewCartEvent('cart_page');
    }

    var cartDrawer = document.querySelector('cart-drawer');
    if (cartDrawer && 'MutationObserver' in window) {
      var drawerObserver = new MutationObserver(function () {
        if (!cartDrawer.classList.contains('active')) return;

        setTimeout(function () {
          refreshCartSnapshot();
          pushViewCartEvent('cart_drawer');
        }, 50);
      });

      drawerObserver.observe(cartDrawer, {
        attributes: true,
        attributeFilter: ['class'],
      });
    }

    if (typeof subscribe !== 'function') return;

    try {
      subscribe(getCartUpdateEventName(), function (eventData) {
        var previousSnapshot = state.cartSnapshotLoaded
          ? Object.assign({}, state.cartSnapshot)
          : {};
        var nextSnapshot = refreshCartSnapshot(eventData);

        pushRemoveFromCartDiff(previousSnapshot, nextSnapshot);
      });
    } catch (e) {
      // no-op
    }
  }

  function initHeroAnalytics() {
    var hero = document.querySelector('[data-hero-id="family-fit"]');
    if (!hero) return;

    var sectionId = hero.getAttribute('data-hero-section');
    var heroId = 'family_fit';
    var video = hero.querySelector('[data-hero-video]');

    if (video && 'IntersectionObserver' in window) {
      var viewed = false;
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (viewed) return;
            if (entry.isIntersecting && entry.intersectionRatio >= 0.6) {
              viewed = true;
              pushToDataLayer({
                event: 'hero_video_view',
                heroId: heroId,
                sectionId: sectionId,
              });
              observer.disconnect();
            }
          });
        },
        { threshold: [0.6] }
      );
      observer.observe(video);
    }
  }

  function initHomepageCtaTracking() {
    document.addEventListener('click', function (event) {
      var button = event.target && event.target.closest && event.target.closest('[data-cta-id]');
      if (!button) return;

      var scope = button.getAttribute('data-cta-scope') || '';
      pushToDataLayer({
        event: 'homepage_cta_click',
        ctaId: button.getAttribute('data-cta-id'),
        ctaScope: scope,
        ctaText: normalizeText(button.textContent),
        destination: button.getAttribute('href') || '',
        productHandle: button.getAttribute('data-product-handle') || '',
      });

      if (scope === 'hero') {
        var heroElement = button.closest('[data-hero-id]');
        pushToDataLayer({
          event: 'hero_cta_click',
          heroId: heroElement ? heroElement.getAttribute('data-hero-id') : 'family_fit',
          sectionId: heroElement ? heroElement.getAttribute('data-hero-section') : undefined,
          ctaId: button.getAttribute('data-cta-id'),
          ctaText: normalizeText(button.textContent),
        });
      }
    });
  }

  function initCheckoutTracking() {
    document.addEventListener('click', function (event) {
      var target = event.target;
      if (!target || !target.closest) return;

      var checkoutTarget = target.closest('[name="checkout"]');
      if (!checkoutTarget) return;

      var source =
        normalizeText(checkoutTarget.id) ||
        normalizeText(checkoutTarget.getAttribute('form')) ||
        normalizeText(checkoutTarget.className);

      pushBeginCheckoutEvent(source);
    });
  }

  function initCartErrorTracking() {
    if (typeof subscribe !== 'function') return;

    try {
      subscribe(getCartUpdateEventName(), function (eventData) {
        if (!eventData || !eventData.errors) return;

        var errorMessage = normalizeText(eventData.errors);
        if (!errorMessage) return;

        pushToDataLayer({
          event: 'cart_update_error',
          error_message: errorMessage,
          error_type: normalizeText(eventData.error_type) || 'unknown',
          source: normalizeText(eventData.source),
        });
      });
    } catch (e) {
      // no-op
    }
  }

  function initSearchTracking() {
    document.addEventListener('submit', function (event) {
      var form = event.target;
      if (!form) return;

      var searchInput = form.querySelector('input[type="search"]');
      if (!searchInput) return;

      var query = normalizeText(searchInput.value);
      if (!query) return;

      pushToDataLayer({
        event: 'search_submit',
        search_term: query,
      });
    });

    if (window.location.pathname.indexOf('/search') === 0) {
      var searchResults = document.querySelectorAll('[data-analytics-product-card="true"]');
      var performedSearch = window.location.search.indexOf('q=') !== -1;

      if (performedSearch && (!searchResults || !searchResults.length)) {
        pushToDataLayer({
          event: 'search_no_results',
        });
      }

      document.addEventListener('click', function (event) {
        var target = event.target;
        if (!target || !target.closest) return;

        var link = target.closest('a[href]');
        if (!link) return;

        var card = link.closest('[data-analytics-product-card="true"]');
        if (!card) return;

        var listContext = getListContext(card);
        var item = buildCardItem(card, listContext);
        if (!item) return;

        pushToDataLayer({
          event: 'search_result_click',
          item_id: normalizeText(item.item_id),
          item_name: normalizeText(item.item_name),
          search_source: 'search_page',
        });
      });
    }
  }

  function init404Tracking() {
    if (window.location.pathname !== '/404' && window.location.pathname !== '/404.html' && window.location.pathname.indexOf('/404') !== 0) {
      return;
    }

    pushToDataLayer({
      event: 'page_404_view',
      page_path: window.location.pathname,
    });

    document.addEventListener('click', function (event) {
      var target = event.target;
      if (!target || !target.closest) return;

      var link = target.closest('a[href]');
      if (!link) return;

      var href = normalizeText(link.getAttribute('href'));
      if (!href) return;

      pushToDataLayer({
        event: '404_recovery_click',
        recovery_link: href,
      });
    });
  }

  function initContactFormTracking() {
    var contactForm = document.getElementById('ContactForm');
    if (!contactForm) return;

    contactForm.addEventListener('submit', function () {
      pushToDataLayer({
        event: 'contact_form_submit',
      });
    });

    var successMessage = document.querySelector('.form-status-list.form__message');
    if (successMessage && successMessage.textContent.indexOf('success') !== -1) {
      pushToDataLayer({
        event: 'contact_form_success',
      });
    }

    var errorMessage = document.querySelector('.form-status.caption-large[role="alert"]');
    if (errorMessage) {
      pushToDataLayer({
        event: 'contact_form_error',
        has_error: true,
      });
    }
  }

  function onDocumentReady() {
    pushViewItemOnce();
    initHeroAnalytics();
    initHomepageCtaTracking();
    initProductListTracking();
    initSelectItemTracking();
    initCartStateTracking();
    initSearchTracking();
    init404Tracking();
    initContactFormTracking();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onDocumentReady, { once: true });
  } else {
    onDocumentReady();
  }

  initProductAddToCartTracking();
  initCheckoutTracking();
  initCartErrorTracking();
})();
