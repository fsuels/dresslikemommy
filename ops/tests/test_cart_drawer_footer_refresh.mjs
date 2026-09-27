import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const cartSource = readFileSync(new URL('../../assets/cart.js', import.meta.url), 'utf8');
const drawerMarkup = readFileSync(new URL('../../snippets/cart-drawer.liquid', import.meta.url), 'utf8');

// Selectors the drawer refresh swaps after a cart change made outside the drawer.
function refreshSelectors() {
  const body = cartSource.slice(cartSource.indexOf('onCartUpdate() {'), cartSource.indexOf('getSectionsToRender() {'));
  const match = body.match(/const selectors = \[([^\]]+)\]/);
  assert.ok(match, 'onCartUpdate declares its refresh selectors');
  return [...match[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
}

// Markup of the element a selector points at in the drawer snippet (div nesting only).
function elementMarkup(selector) {
  let start;
  if (selector.startsWith('#')) start = drawerMarkup.search(new RegExp(`<\\w+[^>]*\\bid="${selector.slice(1)}"`));
  else if (selector.startsWith('.')) start = drawerMarkup.search(new RegExp(`<\\w+[^>]*\\bclass="(?:[^"]*\\s)?${selector.slice(1)}(?:\\s[^"]*)?"`));
  else start = drawerMarkup.indexOf(`<${selector}`);
  if (start < 0) return null;
  const tag = drawerMarkup.slice(start + 1).match(/^[\w-]+/)[0];
  const tokens = new RegExp(`<${tag}\\b|</${tag}>`, 'g');
  tokens.lastIndex = start;
  let depth = 0;
  for (let token; (token = tokens.exec(drawerMarkup)); ) {
    depth += token[0].startsWith('</') ? -1 : 1;
    if (depth === 0) return drawerMarkup.slice(start, tokens.lastIndex);
  }
  return null;
}

test('every selector the drawer refresh swaps exists in the cart drawer markup', () => {
  const selectors = refreshSelectors();
  assert.ok(selectors.length > 0);
  for (const selector of selectors) {
    assert.ok(elementMarkup(selector), `${selector} must exist in snippets/cart-drawer.liquid`);
  }
});

test('the refreshed footer contains the total, Check out and the express wallets', () => {
  const footerSelector = refreshSelectors().find((selector) => selector !== 'cart-drawer-items');
  const footer = elementMarkup(footerSelector);
  assert.ok(footer, 'a footer selector is refreshed');
  assert.match(footer, /class="totals__total-value"/);
  assert.match(footer, /id="CartDrawer-Checkout"/);
  assert.match(footer, /class="cart-drawer__dynamic-checkout-buttons[\s"]/);
  assert.match(footer, /content_for_additional_checkout_buttons/);
});

function fakeElement(name, { classes = [] } = {}) {
  const classSet = new Set(classes);
  return {
    name,
    replacedWith: null,
    replaceWith(next) {
      this.replacedWith = next;
    },
    classList: {
      contains: (value) => classSet.has(value),
      toggle: (value, force) => (force ? classSet.add(value) : classSet.delete(value)),
    },
  };
}

async function runDrawerRefresh({ pageEmpty, freshEmpty }) {
  const liveItems = fakeElement('live items');
  const liveFooter = fakeElement('live footer');
  const liveDrawer = fakeElement('live drawer', { classes: pageEmpty ? ['is-empty'] : [] });
  let walletChecks = 0;
  liveDrawer.ensureExpressCheckoutButtons = () => {
    walletChecks += 1;
  };
  const freshItems = fakeElement('fresh items');
  const freshFooter = fakeElement('fresh footer');
  const freshDrawer = fakeElement('fresh drawer', { classes: freshEmpty ? ['is-empty'] : [] });
  const live = new Map([
    ['cart-drawer-items', liveItems],
    ['#CartDrawer-Footer', liveFooter],
    ['cart-drawer', liveDrawer],
  ]);
  const fresh = new Map([
    ['cart-drawer-items', freshItems],
    ['#CartDrawer-Footer', freshFooter],
    ['cart-drawer', freshDrawer],
  ]);
  const definitions = new Map();
  const requests = [];
  const context = vm.createContext({
    URL,
    console,
    HTMLElement: class {},
    customElements: { define: (name, definition) => definitions.set(name, definition), get: (name) => definitions.get(name) },
    window: { location: { origin: 'https://dresslikemommy.com', pathname: '/fr/products/a' }, Shopify: { routes: { root: '/fr/' } } },
    document: {
      readyState: 'loading',
      getElementById: () => null,
      querySelector: (selector) => live.get(selector) || null,
      querySelectorAll: () => [],
      addEventListener: () => {},
    },
    localStorage: { getItem: () => null, setItem: () => {} },
    routes: { cart_add_url: '/cart/add', cart_change_url: '/cart/change', cart_update_url: '/cart/update', cart_url: '/cart' },
    PUB_SUB_EVENTS: { cartUpdate: 'cart-update' },
    subscribe: () => () => {},
    DOMParser: class {
      parseFromString() {
        return { querySelector: (selector) => fresh.get(selector) || null };
      }
    },
    fetch: (url) => {
      requests.push(url);
      return Promise.resolve({ text: () => Promise.resolve('<cart-drawer></cart-drawer>') });
    },
  });
  vm.runInContext(cartSource, context, { filename: 'assets/cart.js' });
  const CartItems = definitions.get('cart-items');
  const drawerItems = Object.create(CartItems.prototype);
  Object.defineProperty(drawerItems, 'tagName', { value: 'CART-DRAWER-ITEMS' });
  drawerItems.onCartUpdate();
  await new Promise((resolve) => setTimeout(resolve, 0));
  return { requests, liveItems, liveFooter, liveDrawer, freshItems, freshFooter, walletChecks };
}

test('a cart change outside the drawer swaps in the fresh footer and re-checks the wallets', async () => {
  const run = await runDrawerRefresh({ pageEmpty: false, freshEmpty: false });
  assert.deepEqual(run.requests, ['/fr/cart?section_id=cart-drawer']);
  assert.equal(run.liveItems.replacedWith, run.freshItems);
  assert.equal(run.liveFooter.replacedWith, run.freshFooter);
  assert.equal(run.walletChecks, 1);
  assert.equal(run.liveDrawer.classList.contains('is-empty'), false);
});

test('the drawer empty state follows the fresh cart after an outside change', async () => {
  const filled = await runDrawerRefresh({ pageEmpty: true, freshEmpty: false });
  assert.equal(filled.liveDrawer.classList.contains('is-empty'), false);
  const emptied = await runDrawerRefresh({ pageEmpty: false, freshEmpty: true });
  assert.equal(emptied.liveDrawer.classList.contains('is-empty'), true);
});
