import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { setTimeout as delay } from 'node:timers/promises';
import test from 'node:test';
import { runInContext } from 'node:vm';

const require = createRequire(import.meta.url);
const { JSDOM } = require(process.env.DLM_TEST_JSDOM_PATH || '/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const candidateRoot = new URL('../candidate/', import.meta.url);
const readCandidate = (path) => readFileSync(new URL(path, candidateRoot), 'utf8');
const searchFormSource = readCandidate('assets/search-form.js');
const predictiveSource = readCandidate('assets/predictive-search.js');
const cartSource = readCandidate('assets/cart.js');
const tick = () => delay(0);

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

function searchHarness(t) {
  const dom = new JSDOM(`
    <predictive-search data-loading-text="Loading">
      <form action="/es/search">
        <input type="search" name="q" aria-expanded="false">
        <button type="reset" class="hidden">Reset</button>
        <div data-predictive-search></div>
        <span class="predictive-search-status"></span>
      </form>
    </predictive-search>
    <button id="outside">Outside</button>
  `, { url: 'https://dresslikemommy.com/es', runScripts: 'outside-only', pretendToBeVisual: true });
  t.after(() => dom.window.close());
  const { window } = dom;
  const debounced = new Map();
  const requests = [];
  window.debounce = (callback) => (...args) => debounced.set(callback, () => callback(...args));
  window.routes = { predictive_search_url: '/es/search/suggest' };
  Object.defineProperty(window.HTMLElement.prototype, 'innerText', {
    get() { return this.textContent; },
    set(value) { this.textContent = value; },
  });
  // Deliberately allow aborted responses to settle to exercise the stale-response guard too.
  window.fetch = (url, options) => {
    const request = { url, options, ...deferred() };
    requests.push(request);
    return request.promise;
  };
  runInContext(searchFormSource, dom.getInternalVMContext(), { filename: 'assets/search-form.js' });
  runInContext(predictiveSource, dom.getInternalVMContext(), { filename: 'assets/predictive-search.js' });
  const search = window.document.querySelector('predictive-search');
  const input = search.input;
  input.focus();
  function flushInput() {
    const callbacks = [...debounced.values()];
    debounced.clear();
    callbacks.forEach((callback) => callback());
  }
  function type(value, flush = true) {
    input.value = value;
    input.dispatchEvent(new window.Event('input', { bubbles: true }));
    if (flush) flushInput();
  }
  function resultMarkup(label) {
    return `<div id="shopify-section-predictive-search">
      <div id="predictive-search-results-groups-wrapper"><p class="result-label">${label}</p></div>
      <button class="predictive-search__item" data-predictive-search-search-for-text>Search for ${label}</button>
      <span data-predictive-search-live-region-count-value>1 result</span>
    </div>`;
  }
  async function respond(index, label) {
    requests[index].resolve({ ok: true, text: async () => resultMarkup(label) });
    await tick();
  }
  function key(code, type = 'keydown') {
    const event = new window.KeyboardEvent(type, { code, key: code, bubbles: true, cancelable: true });
    input.dispatchEvent(event);
    return event;
  }
  return { window, search, input, requests, type, flushInput, resultMarkup, respond, key };
}

test('a slower older query cannot overwrite the latest results', async (t) => {
  const h = searchHarness(t);
  h.type('red');
  h.type('red dress');
  assert.equal(h.requests[0].options.signal.aborted, true);
  await h.respond(1, 'red dress');
  await h.respond(0, 'red');
  assert.equal(h.search.querySelector('.result-label').textContent, 'red dress');
  assert.equal(h.input.getAttribute('aria-expanded'), 'true');
  assert.equal(new URL(h.requests[1].url, h.window.location.href).searchParams.get('q'), 'red dress');
});

test('a response body arriving during the next input debounce is discarded', async (t) => {
  const h = searchHarness(t);
  h.type('red');
  const body = deferred();
  h.requests[0].resolve({ ok: true, text: () => body.promise });
  await tick();
  h.type('blue', false);
  body.resolve(h.resultMarkup('red'));
  await tick();
  assert.equal(h.search.hasAttribute('open'), false);
  h.flushInput();
  await h.respond(1, 'blue');
  assert.equal(h.search.querySelector('.result-label').textContent, 'blue');
});

test('Escape dismisses pending results without preventing native search-input behavior', async (t) => {
  const h = searchHarness(t);
  h.type('red dress');
  assert.equal(h.key('Escape').defaultPrevented, false);
  assert.equal(h.input.value, 'red dress');
  h.key('Escape', 'keyup');
  assert.equal(h.requests[0].options.signal.aborted, true);
  await h.respond(0, 'red dress');
  assert.equal(h.search.hasAttribute('open'), false);
  assert.equal(h.input.getAttribute('aria-expanded'), 'false');
});

test('a queued input callback cannot reopen after Escape; fresh typing can', async (t) => {
  const h = searchHarness(t);
  h.type('red dress', false);
  h.key('Escape');
  h.key('Escape', 'keyup');
  h.flushInput();
  assert.equal(h.requests.length, 0);
  h.type('red dresses');
  await h.respond(0, 'red dresses');
  assert.equal(h.search.hasAttribute('open'), true);
});

test('native input clearing followed by Escape leaves no delayed dropdown', async (t) => {
  const h = searchHarness(t);
  h.type('red dress');
  h.key('Escape');
  h.type('', false);
  h.key('Escape', 'keyup');
  h.flushInput();
  await h.respond(0, 'red dress');
  assert.equal(h.input.value, '');
  assert.equal(h.search.hasAttribute('results'), false);
  assert.equal(h.search.hasAttribute('open'), false);
});

test('focusout prevents delayed reopening and refocus fetches fresh results', async (t) => {
  const h = searchHarness(t);
  h.type('red dress');
  h.window.document.getElementById('outside').focus();
  await h.respond(0, 'red dress');
  assert.equal(h.search.hasAttribute('open'), false);
  assert.equal(h.requests[0].options.signal.aborted, true);
  h.input.focus();
  assert.equal(h.requests.length, 2);
  assert.equal(h.requests[1].options.signal.aborted, false);
  await h.respond(1, 'red dress');
  assert.equal(h.search.hasAttribute('open'), true);
});

test('refocus uses the current query cache, never an older visible prefix result', async (t) => {
  const h = searchHarness(t);
  h.type('red');
  await h.respond(0, 'red');
  h.type('red dress');
  h.window.document.getElementById('outside').focus();
  await tick();
  h.input.focus();
  assert.equal(h.requests.length, 3);
  assert.equal(h.search.hasAttribute('open'), false);
  await h.respond(2, 'red dress');
  h.window.document.getElementById('outside').focus();
  await tick();
  h.input.focus();
  assert.equal(h.requests.length, 3);
  assert.equal(h.search.querySelector('.result-label').textContent, 'red dress');
  assert.equal(h.search.hasAttribute('open'), true);
});

test('query cache keeps whitespace, hyphens and object-property names distinct', async (t) => {
  const h = searchHarness(t);
  const queries = ['mother daughter', 'mother-daughter', 'mother  daughter', '__proto__', 'constructor'];
  for (const [index, query] of queries.entries()) {
    h.type(query);
    assert.equal(h.requests.length, index + 1);
    await h.respond(index, query);
    assert.equal(h.search.querySelector('.result-label').textContent, query);
  }
  for (const query of queries) {
    h.type(query);
    assert.equal(h.requests.length, queries.length);
    assert.equal(h.search.querySelector('.result-label').textContent, query);
  }
});

test('search-for label replacement is literal and skips absent or ambiguous previous terms', (t) => {
  const h = searchHarness(t);
  const element = h.window.document.createElement('span');
  element.setAttribute('data-predictive-search-search-for-text', '');
  h.search.append(element);
  const cases = [
    ['(', '(floral)', 'Search for (', 'Search for (floral)'],
    ['[', '[floral]', 'Search for [', 'Search for [floral]'],
    ['a+b', '$& dress', 'Search for a+b', 'Search for $& dress'],
    ['.', '* dress', 'Search for .', 'Search for * dress'],
    ['', 'dress', 'Search for', 'Search for'],
    [null, 'dress', 'Search for null', 'Search for null'],
    ['absent', 'dress', 'Search for blue', 'Search for blue'],
    ['Search', 'dress', 'Search for Search', 'Search for Search'],
    ['aa', 'dress', 'aaa', 'aaa'],
  ];
  for (const [previous, next, original, expected] of cases) {
    element.innerText = original;
    assert.doesNotThrow(() => h.search.updateSearchForTerm(previous, next));
    assert.equal(element.innerText, expected, JSON.stringify({ previous, next }));
  }
  element.remove();
  assert.doesNotThrow(() => h.search.updateSearchForTerm('(', 'dress'));
});

test('network, HTTP and malformed-result failures preserve normal form submission', async (t) => {
  for (const failure of ['network', 'http', 'markup']) {
    await t.test(failure, async (t) => {
      const h = searchHarness(t);
      h.type('red dress');
      h.search.predictiveSearchResults.innerHTML = '<li aria-selected="true"><a href="/products/old">Old</a></li>';
      if (failure === 'network') h.requests[0].reject(new TypeError('Failed to fetch'));
      if (failure === 'http') h.requests[0].resolve({ ok: false, status: 503 });
      if (failure === 'markup') h.requests[0].resolve({ ok: true, text: async () => '<p>Unavailable</p>' });
      await tick();
      assert.equal(h.search.hasAttribute('open'), false);
      assert.equal(h.search.hasAttribute('loading'), false);
      const submit = new h.window.Event('submit', { bubbles: true, cancelable: true });
      h.input.form.dispatchEvent(submit);
      assert.equal(submit.defaultPrevented, false);
      assert.equal(h.input.value, 'red dress');
    });
  }
});

test('AbortError and late failures do not throw or dismiss a newer success', async (t) => {
  const h = searchHarness(t);
  h.type('red');
  h.type('red dress');
  await h.respond(1, 'red dress');
  const aborted = new Error('Aborted');
  aborted.name = 'AbortError';
  h.requests[0].reject(aborted);
  await tick();
  assert.equal(h.search.hasAttribute('open'), true);
  h.type('blue');
  h.type('blue dress');
  await h.respond(3, 'blue dress');
  h.requests[2].reject(new TypeError('Failed to fetch'));
  await tick();
  assert.equal(h.search.querySelector('.result-label').textContent, 'blue dress');
  assert.equal(h.search.hasAttribute('open'), true);
});

function cartHarness(t) {
  const dom = new JSDOM(`
    <cart-items>
      <div id="main-cart-title"><h1>Tu carrito (1)</h1><a href="/es/collections/all">Seguir comprando</a></div>
      <div id="main-cart-items" data-id="cart-items-section"><div class="js-contents">
        <div class="cart-item" id="CartItem-1"><input id="Quantity-1" name="updates[]" value="1" data-quantity-variant-id="123"></div>
      </div></div>
      <p id="shopping-cart-line-item-status"></p><div id="cart-errors"></div>
    </cart-items>
    <div id="main-cart-footer" data-id="cart-footer-section"><div class="js-contents">$20</div></div>
    <div id="cart-icon-bubble">1</div><div id="cart-live-region-text"></div>
  `, { url: 'https://dresslikemommy.com/es/cart', runScripts: 'outside-only' });
  t.after(() => dom.window.close());
  const { window } = dom;
  const requests = [];
  window.Shopify = { routes: { root: '/es/' } };
  window.routes = { cart_url: '/cart', cart_change_url: '/cart/change.js', cart_add_url: '/cart/add.js', cart_update_url: '/cart/update.js' };
  window.debounce = (callback) => callback;
  window.ON_CHANGE_DEBOUNCE_TIMER = 300;
  window.PUB_SUB_EVENTS = { cartUpdate: 'cart-update' };
  window.subscribe = () => () => {};
  window.publish = () => {};
  window.fetchConfig = () => ({ method: 'POST' });
  window.cartStrings = { error: 'Unable to update', quantityError: 'Use [quantity]' };
  window.fetch = (url, options) => {
    const request = { url, options, ...deferred() };
    requests.push(request);
    return request.promise;
  };
  window.eval(cartSource);
  const cart = window.document.querySelector('cart-items');
  cart.showUndoToast = () => {};
  return { window, cart, requests };
}

test('cart quantity and removal refresh the translated title from the same section response', async (t) => {
  assert.match(readCandidate('sections/main-cart-items.liquid'), /<div id="main-cart-title" class="title-wrapper-with-link">/);
  for (const count of [2, 0]) {
    await t.test(`item_count=${count}`, async (t) => {
      const h = cartHarness(t);
      h.window.document.getElementById('Quantity-1').value = String(count);
      h.cart.updateQuantity(1, count, 'updates[]', '123');
      assert.equal(h.requests[0].url, '/es/cart/change.js');
      const requestBody = JSON.parse(h.requests[0].options.body);
      assert.equal(requestBody.sections_url, '/es/cart');
      assert.equal(requestBody.sections.filter((id) => id === 'cart-items-section').length, 2);
      const itemMarkup = count ? `<div class="cart-item" id="CartItem-1"><input name="updates[]" id="Quantity-1" value="${count}"></div>` : '';
      const state = {
        item_count: count,
        items: count ? [{ quantity: count }] : [],
        sections: {
          'cart-items-section': `<div id="main-cart-title"><h1>Tu carrito (${count})</h1><a href="/es/collections/all">Seguir comprando</a></div><div class="js-contents">${itemMarkup}</div>`,
          'cart-footer-section': `<div class="js-contents">$${count * 20}</div>`,
          'cart-icon-bubble': `<div class="shopify-section">${count}</div>`,
          'cart-live-region-text': `<div class="shopify-section">${count} artículos</div>`,
        },
      };
      h.requests[0].resolve({ text: async () => JSON.stringify(state) });
      await tick();
      assert.equal(h.window.document.querySelector('#main-cart-title h1').textContent, `Tu carrito (${count})`);
      assert.equal(h.window.document.querySelector('#main-cart-title a').getAttribute('href'), '/es/collections/all');
      assert.equal(h.window.document.querySelector('#main-cart-footer .js-contents').textContent, `$${count * 20}`);
      assert.equal(h.window.document.getElementById('cart-errors').textContent, '');
      assert.equal(h.cart.classList.contains('is-empty'), count === 0);
    });
  }
});
