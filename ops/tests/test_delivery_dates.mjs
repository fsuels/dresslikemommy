import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../assets/dlm-delivery-dates.js', import.meta.url), 'utf8');

function makeElement(windowValue, text) {
  const attributes = new Map([['data-dlm-delivery-window', windowValue]]);
  return {
    textContent: text,
    getAttribute: (name) => (attributes.has(name) ? attributes.get(name) : null),
    setAttribute: (name, value) => attributes.set(name, value),
    hasAttribute: (name) => attributes.has(name),
  };
}

function load({ elements = [], locale = 'en' } = {}) {
  const document = {
    readyState: 'complete',
    documentElement: { lang: locale },
    body: {},
    querySelectorAll: () => elements.filter((el) => !el.hasAttribute('data-dlm-delivery-rendered')),
    querySelector: () => elements.find((el) => !el.hasAttribute('data-dlm-delivery-rendered')) || null,
    addEventListener() {},
  };
  const context = { document, Intl, Date, Array, Number, String, Shopify: { locale } };
  context.window = context;
  vm.runInNewContext(source, context);
  return context.DLMDeliveryDates;
}

const localDay = (date) => [date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getDay()];

test('12-16 days from Saturday Sep 26 2026 lands Thu Oct 8 to Mon Oct 12', () => {
  const api = load();
  const range = api.computeWindow('12-16 days', new Date(2026, 8, 26, 21, 30));
  assert.deepEqual(localDay(range.from), [2026, 10, 8, 4]);
  assert.deepEqual(localDay(range.to), [2026, 10, 12, 1]);
  assert.match(api.formatWindow(range, 'en'), /^Thu, Oct 8\s*–\s*Mon, Oct 12$/);
});

test('an estimate that lands on Sunday rolls to Monday', () => {
  const api = load();
  const range = api.computeWindow('12-16 days', new Date(2026, 8, 25));
  assert.deepEqual(localDay(range.from), [2026, 10, 7, 3]);
  assert.deepEqual(localDay(range.to), [2026, 10, 12, 1]);
});

test('localized day windows parse the same numbers', () => {
  const api = load();
  for (const value of ['12-16 يومًا', '12-16 天', '12–16 jours']) {
    const range = api.computeWindow(value, new Date(2026, 8, 26));
    assert.deepEqual(localDay(range.to), [2026, 10, 12, 1], value);
  }
});

test('unparseable windows keep the Liquid fallback text', () => {
  const fallback = makeElement('a few days', 'a few days');
  const good = makeElement('12-16 days', '12-16 days');
  const api = load({ elements: [fallback, good] });
  assert.equal(api.computeWindow('a few days'), null);
  assert.equal(api.computeWindow('16-12 days'), null);
  assert.equal(fallback.textContent, 'a few days');
  assert.notEqual(good.textContent, '12-16 days');
  assert.match(good.textContent, /\d/);
  assert.ok(good.hasAttribute('data-dlm-delivery-rendered'));
});

test('dates follow the storefront locale', () => {
  const api = load();
  const range = api.computeWindow('12-16 days', new Date(2026, 8, 26));
  assert.match(api.formatWindow(range, 'it'), /ott/);
  assert.match(api.formatWindow(range, 'da'), /okt/);
  assert.match(api.formatWindow(range, 'not a locale!!'), /Oct/);
});
