class CartRemoveButton extends HTMLElement {
  constructor() {
    super();

    this.addEventListener('click', (event) => {
      event.preventDefault();
      const cartItems = this.closest('cart-items') || this.closest('cart-drawer-items');
      cartItems.updateQuantity(this.dataset.index, 0);
    });
  }
}

customElements.define('cart-remove-button', CartRemoveButton);

// Keep cart AJAX endpoints locale-aware so translated sections render in the active language.
const getLocaleAwareRoute = (path) => {
  if (typeof path !== 'string' || path.length === 0) return path;
  if (!path.startsWith('/')) return path;

  const shopifyRoutes = window.Shopify && window.Shopify.routes;
  const shopifyRoot = shopifyRoutes && typeof shopifyRoutes.root === 'string' ? shopifyRoutes.root : '/';
  if (!shopifyRoot || shopifyRoot === '/') return path;

  const normalizedRoot = shopifyRoot.endsWith('/') ? shopifyRoot.slice(0, -1) : shopifyRoot;
  if (!normalizedRoot || normalizedRoot === '/') return path;
  if (path === normalizedRoot || path.indexOf(`${normalizedRoot}/`) === 0) return path;

  return `${normalizedRoot}${path}`;
};

const localizedCartRoutes = {
  cart_add_url: getLocaleAwareRoute(routes.cart_add_url),
  cart_change_url: getLocaleAwareRoute(routes.cart_change_url),
  cart_update_url: getLocaleAwareRoute(routes.cart_update_url),
  cart_url: getLocaleAwareRoute(routes.cart_url),
};

class CartItems extends HTMLElement {
  constructor() {
    super();
    this.lineItemStatusElement =
      document.getElementById('shopping-cart-line-item-status') || document.getElementById('CartDrawer-LineItemStatus');

    const debouncedOnChange = debounce((event) => {
      this.onChange(event);
    }, ON_CHANGE_DEBOUNCE_TIMER);

    this.addEventListener('change', debouncedOnChange.bind(this));
  }

  cartUpdateUnsubscriber = undefined;

  connectedCallback() {
    this.cartUpdateUnsubscriber = subscribe(PUB_SUB_EVENTS.cartUpdate, (event) => {
      if (event.source === 'cart-items') {
        return;
      }
      this.onCartUpdate();
    });
  }

  disconnectedCallback() {
    if (this.cartUpdateUnsubscriber) {
      this.cartUpdateUnsubscriber();
    }
  }

  onChange(event) {
    this.updateQuantity(
      event.target.dataset.index,
      event.target.value,
      document.activeElement.getAttribute('name'),
      event.target.dataset.quantityVariantId
    );
  }

  onCartUpdate() {
    if (this.tagName === 'CART-DRAWER-ITEMS') {
      fetch(`${localizedCartRoutes.cart_url}?section_id=cart-drawer`)
        .then((response) => response.text())
        .then((responseText) => {
          const html = new DOMParser().parseFromString(responseText, 'text/html');
          const selectors = ['cart-drawer-items', '.cart-drawer__footer'];
          for (const selector of selectors) {
            const targetElement = document.querySelector(selector);
            const sourceElement = html.querySelector(selector);
            if (targetElement && sourceElement) {
              targetElement.replaceWith(sourceElement);
            }
          }
        })
        .catch((e) => {
          console.error(e);
        });
    } else {
      fetch(`${localizedCartRoutes.cart_url}?section_id=main-cart-items`)
        .then((response) => response.text())
        .then((responseText) => {
          const html = new DOMParser().parseFromString(responseText, 'text/html');
          const sourceQty = html.querySelector('cart-items');
          this.innerHTML = sourceQty.innerHTML;
        })
        .catch((e) => {
          console.error(e);
        });
    }
  }

  getSectionsToRender() {
    return [
      {
        id: 'main-cart-items',
        section: document.getElementById('main-cart-items').dataset.id,
        selector: '.js-contents',
      },
      {
        id: 'cart-icon-bubble',
        section: 'cart-icon-bubble',
        selector: '.shopify-section',
      },
      {
        id: 'cart-live-region-text',
        section: 'cart-live-region-text',
        selector: '.shopify-section',
      },
      {
        id: 'main-cart-footer',
        section: document.getElementById('main-cart-footer').dataset.id,
        selector: '.js-contents',
      },
    ];
  }

  updateQuantity(line, quantity, name, variantId) {
    this.enableLoading(line);

    // Save item data before removal for undo functionality
    const isRemoval = parseInt(quantity) === 0;
    let removedItemData = null;
    if (isRemoval) {
      const quantityElement = document.getElementById(`Quantity-${line}`) || document.getElementById(`Drawer-quantity-${line}`);
      if (quantityElement) {
        removedItemData = {
          variantId: quantityElement.dataset.quantityVariantId,
          quantity: parseInt(quantityElement.getAttribute('value')) || 1,
          line: line
        };
      }
    }

    const body = JSON.stringify({
      line,
      quantity,
      sections: this.getSectionsToRender().map((section) => section.section),
      sections_url: window.location.pathname,
    });

    fetch(`${localizedCartRoutes.cart_change_url}`, { ...fetchConfig(), ...{ body } })
      .then((response) => {
        return response.text();
      })
      .then((state) => {
        const parsedState = JSON.parse(state);
        const quantityElement =
          document.getElementById(`Quantity-${line}`) || document.getElementById(`Drawer-quantity-${line}`);
        const items = document.querySelectorAll('.cart-item');

        if (parsedState.errors) {
          quantityElement.value = quantityElement.getAttribute('value');
          // Map common Shopify error patterns to user-friendly messages
          let errorMessage = parsedState.errors;
          if (typeof parsedState.errors === 'string') {
            errorMessage = parsedState.errors;
            // Provide specific, actionable error messages
            if (errorMessage.toLowerCase().includes('sold out') || errorMessage.toLowerCase().includes('out of stock')) {
              errorMessage = 'This item is sold out. Please try a different quantity.';
            } else if (errorMessage.toLowerCase().includes('maximum') || errorMessage.toLowerCase().includes('max')) {
              const match = errorMessage.match(/(\d+)/);
              if (match) {
                errorMessage = `You can add a maximum of ${match[1]} of this item to your cart.`;
              } else {
                errorMessage = 'You\'ve reached the maximum quantity for this item.';
              }
            } else if (errorMessage.toLowerCase().includes('minimum') || errorMessage.toLowerCase().includes('min')) {
              const match = errorMessage.match(/(\d+)/);
              if (match) {
                errorMessage = `This item requires a minimum of ${match[1]} to be added.`;
              } else {
                errorMessage = 'This item requires a minimum quantity.';
              }
            } else if (errorMessage.toLowerCase().includes('inventory')) {
              errorMessage = 'Not enough inventory available. Please try a smaller quantity.';
            } else if (errorMessage.toLowerCase().includes('unavailable')) {
              errorMessage = 'This item is temporarily unavailable. Please try again soon.';
            }
          } else if (parsedState.description) {
            errorMessage = parsedState.description;
          }
          this.updateLiveRegions(line, errorMessage);
          return;
        }

        this.classList.toggle('is-empty', parsedState.item_count === 0);
        const cartDrawerWrapper = document.querySelector('cart-drawer');
        const cartFooter = document.getElementById('main-cart-footer');

        if (cartFooter) cartFooter.classList.toggle('is-empty', parsedState.item_count === 0);
        if (cartDrawerWrapper) cartDrawerWrapper.classList.toggle('is-empty', parsedState.item_count === 0);

        this.getSectionsToRender().forEach((section) => {
          const elementToReplace =
            document.getElementById(section.id).querySelector(section.selector) || document.getElementById(section.id);
          elementToReplace.innerHTML = this.getSectionInnerHTML(
            parsedState.sections[section.section],
            section.selector
          );
        });
        const updatedValue = parsedState.items[line - 1] ? parsedState.items[line - 1].quantity : undefined;
        let message = '';
        if (items.length === parsedState.items.length && updatedValue !== parseInt(quantityElement.value)) {
          if (typeof updatedValue === 'undefined') {
            message = window.cartStrings.error;
          } else {
            // Provide a clearer message about why the quantity was adjusted
            const requestedQty = parseInt(quantityElement.value);
            if (updatedValue < requestedQty) {
              message = `Only ${updatedValue} available — we've updated your quantity.`;
            } else {
              message = window.cartStrings.quantityError.replace('[quantity]', updatedValue);
            }
          }
        }
        this.updateLiveRegions(line, message);

        const lineItem =
          document.getElementById(`CartItem-${line}`) || document.getElementById(`CartDrawer-Item-${line}`);
        if (lineItem && lineItem.querySelector(`[name="${name}"]`)) {
          cartDrawerWrapper
            ? trapFocus(cartDrawerWrapper, lineItem.querySelector(`[name="${name}"]`))
            : lineItem.querySelector(`[name="${name}"]`).focus();
        } else if (parsedState.item_count === 0 && cartDrawerWrapper) {
          trapFocus(cartDrawerWrapper.querySelector('.drawer__inner-empty'), cartDrawerWrapper.querySelector('a'));
        } else if (document.querySelector('.cart-item') && cartDrawerWrapper) {
          trapFocus(cartDrawerWrapper, document.querySelector('.cart-item__name'));
        }

        // Show undo toast when an item is removed
        if (isRemoval && removedItemData && removedItemData.variantId) {
          this.showUndoToast(removedItemData);
        }

        publish(PUB_SUB_EVENTS.cartUpdate, { source: 'cart-items', cartData: parsedState, variantId: variantId });
      })
      .catch((error) => {
        this.querySelectorAll('.loading__spinner').forEach((overlay) => overlay.classList.add('hidden'));
        const errors = document.getElementById('cart-errors') || document.getElementById('CartDrawer-CartErrors');
        // Differentiate error types with specific, actionable messaging
        if (error instanceof TypeError) {
          if (error.message === 'Failed to fetch' || error.message.includes('fetch')) {
            errors.textContent = 'Unable to update cart — please check your internet connection and try again.';
          } else {
            errors.textContent = 'Something went wrong updating your cart. Please refresh the page and try again.';
          }
        } else if (error instanceof SyntaxError) {
          errors.textContent = 'Server error updating cart. Please refresh and try again.';
        } else {
          errors.textContent = window.cartStrings.error || 'Unable to update cart. Please try again.';
        }
      })
      .finally(() => {
        this.disableLoading(line);
      });
  }

  updateLiveRegions(line, message) {
    const lineItemError =
      document.getElementById(`Line-item-error-${line}`) || document.getElementById(`CartDrawer-LineItemError-${line}`);
    if (lineItemError) lineItemError.querySelector('.cart-item__error-text').innerHTML = message;

    this.lineItemStatusElement.setAttribute('aria-hidden', true);

    const cartStatus =
      document.getElementById('cart-live-region-text') || document.getElementById('CartDrawer-LiveRegionText');
    cartStatus.setAttribute('aria-hidden', false);

    setTimeout(() => {
      cartStatus.setAttribute('aria-hidden', true);
    }, 1000);
  }

  getSectionInnerHTML(html, selector) {
    return new DOMParser().parseFromString(html, 'text/html').querySelector(selector).innerHTML;
  }

  enableLoading(line) {
    const mainCartItems = document.getElementById('main-cart-items') || document.getElementById('CartDrawer-CartItems');
    mainCartItems.classList.add('cart__items--disabled');

    const cartItemElements = this.querySelectorAll(`#CartItem-${line} .loading__spinner`);
    const cartDrawerItemElements = this.querySelectorAll(`#CartDrawer-Item-${line} .loading__spinner`);

    [...cartItemElements, ...cartDrawerItemElements].forEach((overlay) => overlay.classList.remove('hidden'));

    // Disable checkout buttons during cart update to prevent stale-total submissions
    document.querySelectorAll('.cart__checkout-button').forEach((btn) => {
      btn.setAttribute('disabled', 'disabled');
    });

    document.activeElement.blur();
    this.lineItemStatusElement.setAttribute('aria-hidden', false);
  }

  disableLoading(line) {
    const mainCartItems = document.getElementById('main-cart-items') || document.getElementById('CartDrawer-CartItems');
    mainCartItems.classList.remove('cart__items--disabled');

    const cartItemElements = this.querySelectorAll(`#CartItem-${line} .loading__spinner`);
    const cartDrawerItemElements = this.querySelectorAll(`#CartDrawer-Item-${line} .loading__spinner`);

    cartItemElements.forEach((overlay) => overlay.classList.add('hidden'));
    cartDrawerItemElements.forEach((overlay) => overlay.classList.add('hidden'));

    // Re-enable checkout buttons after cart update completes
    document.querySelectorAll('.cart__checkout-button').forEach((btn) => {
      btn.removeAttribute('disabled');
    });
  }

  showUndoToast(removedItemData) {
    // Remove any existing toast
    const existingToast = document.querySelector('.cart-undo-toast');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.className = 'cart-undo-toast';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
      <span>Item removed</span>
      <button type="button" class="cart-undo-toast__btn">Undo</button>
    `;
    document.body.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(() => toast.classList.add('is-visible'));

    const undoBtn = toast.querySelector('.cart-undo-toast__btn');
    let undone = false;

    const removeToast = () => {
      toast.classList.remove('is-visible');
      setTimeout(() => toast.remove(), 300);
    };

    undoBtn.addEventListener('click', () => {
      if (undone) return;
      undone = true;
      // Re-add the item
      const body = JSON.stringify({
        items: [{ id: parseInt(removedItemData.variantId), quantity: removedItemData.quantity }]
      });
      fetch(`${localizedCartRoutes.cart_add_url}`, { ...fetchConfig(), ...{ body } })
        .then((response) => response.json())
        .then(() => {
          removeToast();
          // Trigger cart update
          location.reload();
        })
        .catch(() => removeToast());
    });

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      if (!undone) removeToast();
    }, 5000);
  }
}

customElements.define('cart-items', CartItems);

/* ── Recently Viewed Products — lazy: only track on product pages, only render when empty cart containers exist ── */
(function() {
  const STORAGE_KEY = 'dlm_recently_viewed';
  const MAX_ITEMS = 6;

  // Track current product page (lightweight — just localStorage write)
  if (window.location.pathname.startsWith('/products/')) {
    try {
      const titleTag = document.querySelector('meta[property="og:title"]');
      const imageTag = document.querySelector('meta[property="og:image"]');
      const priceTag = document.querySelector('meta[property="product:price:amount"]');

      if (titleTag) {
        const viewed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
        const url = window.location.pathname;
        const filtered = viewed.filter(item => item.url !== url);
        filtered.unshift({ url, title: titleTag.content || '', image: imageTag ? imageTag.content : '', price: priceTag ? priceTag.content : '', time: Date.now() });
        localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered.slice(0, MAX_ITEMS)));
      }
    } catch(e) { /* localStorage not available */ }
    return; // Exit early — no rendering needed on product pages
  }

  // Only render if empty-cart containers exist on page
  function renderRecentlyViewed() {
    const drawerContainer = document.getElementById('CartDrawer-RecentlyViewed');
    const pageContainer = document.getElementById('CartPage-RecentlyViewed');
    if (!drawerContainer && !pageContainer) return; // No containers — skip entirely

    try {
      const viewed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      if (viewed.length === 0) return;

      if (drawerContainer) {
        const drawerGrid = document.getElementById('CartDrawer-RecentlyViewedGrid');
        if (drawerGrid) {
          drawerGrid.innerHTML = viewed.slice(0, 3).map(function(item) {
            return '<a href="' + item.url + '" class="cart-drawer__upsell-item">' +
              (item.image ? '<img src="' + item.image + '" alt="" width="70" height="70" loading="lazy" class="cart-drawer__upsell-img">' : '') +
              '<div class="cart-drawer__upsell-info"><span class="cart-drawer__upsell-name">' + item.title.split(' | ')[0] + '</span>' +
              (item.price ? '<span class="cart-drawer__upsell-price">$' + item.price + '</span>' : '') +
              '</div></a>';
          }).join('');
          drawerContainer.style.display = '';
        }
      }

      if (pageContainer) {
        const pageGrid = document.getElementById('CartPage-RecentlyViewedGrid');
        if (pageGrid) {
          pageGrid.innerHTML = viewed.slice(0, 4).map(function(item) {
            return '<a href="' + item.url + '" class="cart-page__cross-sell-item">' +
              (item.image ? '<div class="cart-page__cross-sell-img-wrap"><img src="' + item.image + '" alt="" width="150" height="150" loading="lazy" class="cart-page__cross-sell-img"></div>' : '') +
              '<div class="cart-page__cross-sell-info"><span class="cart-page__cross-sell-name">' + item.title.split(' | ')[0] + '</span>' +
              (item.price ? '<span class="cart-page__cross-sell-price">$' + item.price + '</span>' : '') +
              '</div></a>';
          }).join('');
          pageContainer.style.display = '';
        }
      }
    } catch(e) { /* localStorage not available */ }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderRecentlyViewed);
  } else {
    renderRecentlyViewed();
  }
})();

/* ── Swipe-to-remove on mobile — only init on touch devices with cart items ── */
(function() {
  if (!('ontouchstart' in window)) return;
  if (!document.querySelector('.cart-item')) return; // No cart items — skip

  let startX = 0;
  let currentX = 0;
  let swiping = false;
  let currentRow = null;

  document.addEventListener('touchstart', function(e) {
    const row = e.target.closest('.cart-item');
    if (!row) return;
    startX = e.touches[0].clientX;
    currentRow = row;
    swiping = true;
  }, { passive: true });

  document.addEventListener('touchmove', function(e) {
    if (!swiping || !currentRow) return;
    currentX = e.touches[0].clientX;
    const diff = startX - currentX;
    if (diff > 10) {
      currentRow.style.transform = 'translateX(' + Math.max(-diff, -120) + 'px)';
      currentRow.style.transition = 'none';
    }
  }, { passive: true });

  document.addEventListener('touchend', function() {
    if (!swiping || !currentRow) return;
    const diff = startX - currentX;
    if (diff > 80) {
      // Swipe threshold met — remove item
      currentRow.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
      currentRow.style.transform = 'translateX(-100%)';
      currentRow.style.opacity = '0';
      const removeBtn = currentRow.querySelector('cart-remove-button button, cart-remove-button a');
      if (removeBtn) {
        setTimeout(function() { removeBtn.click(); }, 300);
      }
    } else {
      // Reset position
      currentRow.style.transition = 'transform 0.2s ease';
      currentRow.style.transform = '';
    }
    swiping = false;
    currentRow = null;
  });
})();

/* ── Delivery date calculation (10 business days — matches product page FREE Shipping) ── */
/* Only runs when .js-delivery-date elements exist (cart has items) */
(function() {
  if (!document.querySelector('.js-delivery-date')) {
    // Defer — elements may appear later when cart drawer opens
    var checkLater = function() {
      if (document.querySelector('.js-delivery-date')) initDeliveryDates();
    };
    document.addEventListener('cart:updated', checkLater);
    var drawer = document.getElementById('CartDrawer');
    if (drawer) {
      new MutationObserver(function(mutations) {
        if (document.querySelector('.js-delivery-date:empty')) initDeliveryDates();
      }).observe(drawer, { childList: true, subtree: true });
    }
    return;
  }
  initDeliveryDates();

  function initDeliveryDates() {
  function addBusinessDays(startDate, businessDays) {
    const date = new Date(startDate);
    let added = 0;
    while (added < businessDays) {
      date.setDate(date.getDate() + 1);
      const day = date.getDay();
      if (day !== 0 && day !== 6) added++;
    }
    return date;
  }

  function updateDeliveryDates() {
    const today = new Date();
    const deliveryDate = addBusinessDays(today, 10);
    const options = { month: 'short', day: 'numeric' };
    const shopifyLocale = window.Shopify && window.Shopify.locale ? window.Shopify.locale : '';
    const documentLang =
      document.documentElement && typeof document.documentElement.getAttribute === 'function'
        ? document.documentElement.getAttribute('lang') || ''
        : '';
    const activeLocale = shopifyLocale || documentLang || navigator.language || 'en-US';
    let formatted;
    try {
      formatted = new Intl.DateTimeFormat(activeLocale, options).format(deliveryDate);
    } catch (error) {
      formatted = deliveryDate.toLocaleDateString('en-US', options);
    }
    document.querySelectorAll('.js-delivery-date').forEach(function(el) {
      el.textContent = formatted;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateDeliveryDates);
  } else {
    updateDeliveryDates();
  }

  // Also update after AJAX cart updates (drawer re-renders)
  document.addEventListener('cart:updated', updateDeliveryDates);
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
      if (m.addedNodes.length) {
        const hasDate = document.querySelector('.js-delivery-date:empty');
        if (hasDate) updateDeliveryDates();
      }
    });
  });
  const cartDrawer = document.getElementById('CartDrawer');
  if (cartDrawer) observer.observe(cartDrawer, { childList: true, subtree: true });
  } /* end initDeliveryDates */
})();

if (!customElements.get('cart-note')) {
  customElements.define(
    'cart-note',
    class CartNote extends HTMLElement {
      constructor() {
        super();

        this.addEventListener(
          'input',
          debounce((event) => {
            const body = JSON.stringify({ note: event.target.value });
            fetch(`${localizedCartRoutes.cart_update_url}`, { ...fetchConfig(), ...{ body } });
          }, ON_CHANGE_DEBOUNCE_TIMER)
        );
      }
    }
  );
}
