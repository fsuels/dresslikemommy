import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('./theme/assets/cart.js', import.meta.url), 'utf8');
const skyfade = {
  url: '/products/skyfade-family-matching-set',
  title: 'Skyfade Family Matching Set | Dress Like Mommy',
  image: 'https://cdn.shopify.com/skyfade.jpg',
  price: '131.0', // Previously cached DKK amount, without a currency field.
};

function runCart({
  history = [skyfade],
  rawStorage = JSON.stringify(history),
  root = '/da/',
  pathname = '/da/cart',
  surfaces = ['Drawer', 'Page'],
  readyState = 'complete',
  meta = {},
  storageThrows = false,
} = {}) {
  let stored = rawStorage;
  const elements = new Map();
  const events = new Map();
  const subscriptions = new Map();
  const definitions = new Map();
  const writes = [];
  const addSurface = (surface) => {
    elements.set(`Cart${surface}-RecentlyViewed`, { style: { display: 'none' } });
    elements.set(`Cart${surface}-RecentlyViewedGrid`, { innerHTML: '' });
  };
  surfaces.forEach(addSurface);
  elements.set('main-cart-items', { dataset: { id: 'cart-items-section' } });
  elements.set('main-cart-footer', { dataset: { id: 'cart-footer-section' } });

  const context = vm.createContext({
    URL,
    HTMLElement: class {},
    customElements: {
      define: (name, definition) => definitions.set(name, definition),
      get: (name) => definitions.get(name),
    },
    window: {
      location: { origin: 'https://dresslikemommy.com', pathname },
      Shopify: { routes: { root } },
    },
    document: {
      readyState,
      getElementById: (id) => elements.get(id) || null,
      querySelector: (selector) => meta[selector] || null,
      addEventListener: (name, callback) => {
        events.set(name, [...(events.get(name) || []), callback]);
      },
    },
    localStorage: {
      getItem: () => {
        if (storageThrows) throw new Error('Storage unavailable');
        return stored;
      },
      setItem: (key, value) => {
        if (storageThrows) throw new Error('Storage unavailable');
        assert.equal(key, 'dlm_recently_viewed');
        stored = value;
        writes.push(value);
      },
    },
    routes: {
      cart_add_url: '/cart/add',
      cart_change_url: '/cart/change',
      cart_update_url: '/cart/update',
      cart_url: '/cart',
    },
    PUB_SUB_EVENTS: { cartUpdate: 'cart-update' },
    subscribe: (name, callback) => {
      subscriptions.set(name, [...(subscriptions.get(name) || []), callback]);
      return () => {};
    },
    // Any unexpected network request is a failure; history cards must stay local.
    fetch: () => assert.fail('Recently viewed cards must not fetch cached prices'),
  });
  vm.runInContext(source, context, { filename: 'assets/cart.js' });

  return {
    elements,
    definitions,
    writes,
    stored: () => stored,
    html: (surface) => elements.get(`Cart${surface}-RecentlyViewedGrid`)?.innerHTML || '',
    addSurface,
    domReady: () => (events.get('DOMContentLoaded') || []).forEach((callback) => callback()),
    cartUpdated: () => (subscriptions.get('cart-update') || []).forEach((callback) => callback({ source: 'cart-items' })),
  };
}

for (const surface of ['Drawer', 'Page']) {
  test(`${surface}: a cached DKK amount never appears as dollars or any stale price`, () => {
    const page = runCart({ surfaces: [surface] });
    assert.match(page.html(surface), /Skyfade Family Matching Set/);
    assert.match(page.html(surface), /href="\/da\/products\/skyfade-family-matching-set"/);
    assert.doesNotMatch(page.html(surface), /131|\$|upsell-price|cross-sell-price/);
    assert.equal(page.elements.get(`Cart${surface}-RecentlyViewed`).style.display, '');
  });
}

for (const [priorUrl, root, expected] of [
  ['/da/products/skyfade-family-matching-set', '/fr/', '/fr/products/skyfade-family-matching-set'],
  ['/fr/products/skyfade-family-matching-set', '/da/', '/da/products/skyfade-family-matching-set'],
  ['/da/products/skyfade-family-matching-set', '/', '/products/skyfade-family-matching-set'],
  ['/da/products/skyfade-family-matching-set', '/da/', '/da/products/skyfade-family-matching-set'],
  ['/fr-ca/products/skyfade-family-matching-set?currency=CAD&country=CA', '/da', '/da/products/skyfade-family-matching-set'],
]) {
  test(`switch from ${priorUrl} to ${root} keeps exactly the current locale`, () => {
    const page = runCart({ root, history: [{ ...skyfade, url: priorUrl }] });
    for (const surface of ['Drawer', 'Page']) {
      assert.ok(page.html(surface).includes(`href="${expected}"`));
      assert.doesNotMatch(page.html(surface), /currency=|country=/);
    }
  });
}

test('untrusted stored text remains text and image attributes cannot break out', () => {
  const title = '<img src=x onerror="alert(1)"> & Mom\'s <script>alert(2)</script>';
  const page = runCart({ history: [{ ...skyfade, title, image: 'https://cdn.shopify.com/a.jpg?q=" onerror="alert(3)&x=1' }] });
  for (const surface of ['Drawer', 'Page']) {
    assert.match(page.html(surface), /&lt;img src=x onerror=&quot;alert\(1\)&quot;&gt;/);
    assert.match(page.html(surface), /&amp; Mom&#39;s &lt;script&gt;/);
    assert.doesNotMatch(page.html(surface), /<script|<img src=x|" onerror="/);
    assert.match(page.html(surface), /src="https:\/\/cdn\.shopify\.com\/a\.jpg\?q=%22/);
    assert.match(page.html(surface), /&amp;x=1/);
  }
});

test('external, executable, invalid, and non-product links are not rendered', () => {
  const unsafeUrls = [
    'https://other.example/products/skyfade',
    '//other.example/products/skyfade',
    'javascript:alert(1)',
    'data:text/html,attack',
    '/cart',
    '/collections/family',
    '/fr/cart',
    '/products/',
    '/da/fr/products/skyfade',
    '/products/skyfade/extra',
    'http://[invalid',
    null,
  ];
  const page = runCart({ history: [...unsafeUrls.map((url) => ({ ...skyfade, title: 'Rejected card', url })), skyfade] });
  for (const surface of ['Drawer', 'Page']) {
    assert.doesNotMatch(page.html(surface), /Rejected card|other\.example|javascript:|data:text/);
    assert.equal((page.html(surface).match(/<a /g) || []).length, 1);
  }
});

test('unsafe image schemes are omitted while a valid product remains clickable', () => {
  for (const image of ['javascript:alert(1)', 'data:image/svg+xml,<svg onload="alert(1)">', 'file:///private/image.jpg', 'http://[invalid']) {
    const page = runCart({ history: [{ ...skyfade, image }] });
    for (const surface of ['Drawer', 'Page']) {
      assert.match(page.html(surface), /href="\/da\/products\//);
      assert.doesNotMatch(page.html(surface), /<img|javascript:|data:image|file:/);
    }
  }
});

test('malformed, non-array, or unavailable storage leaves the empty cart usable', () => {
  for (const rawStorage of ['{broken', '{}', 'null', '"text"', '123', '[null, 1, {}, {"url":"/products/a","title":12}]']) {
    const page = runCart({ rawStorage });
    assert.equal(page.html('Drawer'), '');
    assert.equal(page.html('Page'), '');
    assert.equal(page.elements.get('CartPage-RecentlyViewed').style.display, 'none');
  }
  assert.doesNotThrow(() => runCart({ storageThrows: true }));
});

test('a localized product visit is tracked once and its empty-cart drawer renders', () => {
  const page = runCart({
    pathname: '/fr/products/skyfade-family-matching-set',
    root: '/fr/',
    surfaces: ['Drawer'],
    history: [{ ...skyfade, url: '/da/products/skyfade-family-matching-set' }],
    meta: {
      'meta[property="og:title"]': { content: 'Ensemble familial Skyfade | Dress Like Mommy' },
      'meta[property="og:image"]': { content: 'https://cdn.shopify.com/skyfade-fr.jpg' },
      'meta[property="product:price:amount"]': { content: '17.59' },
    },
  });
  const stored = JSON.parse(page.stored());
  assert.equal(page.writes.length, 1);
  assert.equal(stored.length, 1);
  assert.equal(stored[0].url, '/products/skyfade-family-matching-set');
  assert.equal(stored[0].price, undefined);
  assert.match(page.html('Drawer'), /Ensemble familial Skyfade/);
  assert.match(page.html('Drawer'), /href="\/fr\/products\/skyfade-family-matching-set"/);
});

test('a product visit recovers from non-array history and storage denial remains harmless', () => {
  const options = {
    pathname: '/da/products/skyfade-family-matching-set',
    rawStorage: '{}',
    meta: { 'meta[property="og:title"]': { content: skyfade.title } },
  };
  assert.equal(JSON.parse(runCart(options).stored()).length, 1);
  assert.doesNotThrow(() => runCart({ ...options, storageThrows: true }));
});

test('history stays bounded, deduplicates past locales, and respects card limits', () => {
  const history = [{ ...skyfade, url: '/fr/products/skyfade-family-matching-set' }, skyfade];
  for (let index = 0; index < 8; index++) history.push({ ...skyfade, url: `/products/item-${index}` });
  const page = runCart({ history });
  assert.equal((page.html('Drawer').match(/<a /g) || []).length, 3);
  assert.equal((page.html('Page').match(/<a /g) || []).length, 4);
  assert.equal((page.html('Page').match(/href="\/da\/products\/skyfade-family-matching-set"/g) || []).length, 1);
});

test('DOM readiness and an empty-cart replacement both render history', () => {
  const loading = runCart({ readyState: 'loading' });
  assert.equal(loading.html('Drawer'), '');
  loading.domReady();
  assert.match(loading.html('Drawer'), /Skyfade Family Matching Set/);

  const replacement = runCart({ surfaces: [] });
  replacement.addSurface('Drawer');
  replacement.addSurface('Page');
  replacement.cartUpdated();
  assert.match(replacement.html('Drawer'), /Skyfade Family Matching Set/);
  assert.match(replacement.html('Page'), /Skyfade Family Matching Set/);
});

test('the existing quantity count and subtotal refresh targets stay intact', () => {
  const page = runCart();
  const sections = page.definitions.get('cart-items').prototype.getSectionsToRender.call({});
  assert.equal(sections.find((section) => section.id === 'main-cart-title').selector, '#main-cart-title');
  assert.equal(sections.find((section) => section.id === 'main-cart-footer').selector, '#main-cart-footer-subtotal');
});
