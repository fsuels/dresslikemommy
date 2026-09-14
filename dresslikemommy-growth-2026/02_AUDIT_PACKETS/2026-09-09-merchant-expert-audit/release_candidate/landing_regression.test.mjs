import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire('/tmp/dlm-merchant-landing-validation-20260909/package.json');
const { JSDOM } = require('jsdom');
const root = path.dirname(fileURLToPath(import.meta.url));
const code = fs.readFileSync(path.join(root, 'theme/assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
const shippingCopy = JSON.parse(fs.readFileSync(path.join(root, 'shipping_copy.json'), 'utf8'));
const consentCopy = JSON.parse(fs.readFileSync(path.join(root, 'consent_locale_copy.json'), 'utf8'));
const seoChanges = JSON.parse(fs.readFileSync(path.join(root, 'merge_proof.json'), 'utf8')).seo_changes;
function normalizeReviewedReleaseAdditions(before, after, filename) {
  const locale = path.basename(filename, '.json');
  assert.equal(after.products.purchase_confidence.shipping_checkout, shippingCopy[locale]);
  assert.equal(Object.hasOwn(before.products.purchase_confidence, 'shipping_checkout'), false);
  delete after.products.purchase_confidence.shipping_checkout;
  for (const [key, value] of Object.entries(consentCopy[locale])) {
    assert.equal(after.sections.footer[key], value);
    assert.equal(Object.hasOwn(before.sections.footer, key), false);
    delete after.sections.footer[key];
  }
  for (const change of seoChanges.filter(change => change.file === filename)) {
    const keys = change.key.split('.');
    const target = keys.slice(0, -1).reduce((value, key) => value[key], after);
    assert.equal(target[keys.at(-1)], change.after);
    target[keys.at(-1)] = change.before;
  }
}
const defaultPrice = '<div class="price price--large price--range" data-price-current-text="$20.00 – $30.00" data-price-variant-id="100"><div class="price__container"><div class="price__regular"><span class="price-item price-item--regular">$20.00 – $30.00</span></div><small class="unit-price hidden"><span class="price-item"><span></span><span>/</span><span></span></span></small></div></div>';

function data(selected = null, currency = 'USD') {
  return {
    currency,
    selected_variant_id: selected,
    default_price_html: defaultPrice,
    options: [{ name: 'Size', position: 1 }, { name: 'Color', position: 2 }, { name: 'Pattern', position: 3 }],
    variants: [
      { id: 101, available: true, price: 3000, price_text: '$30.00', option1: 'Mother S', option2: 'Red', option3: 'Solid' },
      { id: 102, available: true, price: 3100, price_text: '$31.00', option1: 'Mother S', option2: 'Blue', option3: 'Floral' },
      { id: 201, available: true, price: 2000, price_text: '$20.00', option1: 'Child 6 Years', option2: 'Red', option3: 'Solid' },
      { id: 202, available: true, price: 2200, price_text: '$22.00', option1: 'Child 6 Years', option2: 'Blue', option3: 'Floral' },
      { id: 203, available: false, price: 2100, price_text: '$21.00', option1: 'Child 8 Years', option2: 'Red', option3: 'Solid' },
      { id: 204, available: true, price: 2300, price_text: '$23.00', option1: 'Child 6 Years', option2: 'Blue', option3: 'Solid' },
    ],
  };
}

function setup(product = data(), lang = 'en') {
  const dom = new JSDOM(`<!doctype html><html lang="${lang}"><body><main id="MainProduct-fixture"><div class="product__info-container--matching-set"><div id="price-fixture">${defaultPrice}</div><form id="product-form-fixture"><input name="id" value="101"></form><div id="variant-selects-fixture"></div><div id="fixture-wrapper"><section data-matching-set-builder hidden><div data-matching-set-roles></div><div data-matching-set-summary hidden><p data-matching-set-empty-copy></p><div data-matching-set-chips hidden></div><strong data-matching-set-total hidden></strong></div><button data-matching-set-add-button disabled>Add</button><p data-matching-set-status hidden></p></section></div></div></main><cart-drawer></cart-drawer></body></html>`, { url: 'https://fixture.invalid/products/family?variant=' + product.selected_variant_id, runScripts: 'outside-only', pretendToBeVisual: true });
  const { window } = dom;
  const observers = [];
  const NativeMutationObserver = window.MutationObserver;
  window.MutationObserver = class extends NativeMutationObserver {
    constructor(callback) { super(callback); observers.push(this); }
  };
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  const requests = [];
  window.fetch = async (url, config) => {
    requests.push({ url, entries: Array.from(config.body.entries()) });
    return { ok: true, json: async () => ({ sections: {} }) };
  };
  const drawer = window.document.querySelector('cart-drawer');
  drawer.getSectionsToRender = () => [{ id: 'cart-drawer' }];
  drawer.renderContents = () => {};
  window.eval(code);
  window.initMatchingSetBuilder(window.document.getElementById('fixture-wrapper'), 'fixture', product);
  const query = selector => window.document.querySelector(selector);
  const selected = selector => Array.from(window.document.querySelectorAll(selector)).map(node => node.textContent.trim());
  const click = selector => { const button = query(selector); assert.ok(button, selector); assert.equal(button.disabled, false, selector); button.click(); };
  return { dom, window, query, selected, click, requests, close: () => { observers.forEach(observer => observer.disconnect()); window.close(); } };
}

test('explicit child link selects its role, size, every axis and exactly quantity one', async () => {
  const f = setup(data(202));
  try {
    assert.deepEqual(f.selected('[data-select-role-group].is-selected'), ['Child']);
    assert.equal(f.query('[data-instance-pill].is-selected').getAttribute('data-size-label'), '6 Years');
    assert.deepEqual(f.selected('[data-instance-axis].is-selected'), ['Blue', 'Floral']);
    assert.equal(f.query('[data-qty-value]').textContent, '1');
    assert.equal(f.query('#price-fixture .price-item--regular').textContent, '$22.00');
    f.click('[data-matching-set-add-button]');
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.deepEqual(f.requests[0].entries.filter(([key]) => key.startsWith('items[')), [['items[0][id]', '202'], ['items[0][quantity]', '1']]);
  } finally { f.close(); }
});

test('explicit adult link remains adult with correct price and axes', () => {
  const f = setup(data(101));
  try {
    assert.deepEqual(f.selected('[data-select-role-group].is-selected'), ['Mother']);
    assert.equal(f.query('[data-instance-pill].is-selected').getAttribute('data-size-label'), 'S');
    assert.deepEqual(f.selected('[data-instance-axis].is-selected'), ['Red', 'Solid']);
    assert.equal(f.query('#price-fixture .price').getAttribute('data-price-variant-id'), '101');
    assert.equal(f.query('[data-matching-set-add-button]').disabled, false);
  } finally { f.close(); }
});

for (const missing of [null, '', 999999, 'invalid']) {
  test(`missing or invalid link ${JSON.stringify(missing)} preserves empty adult default and range`, () => {
    const f = setup(data(missing));
    try {
      assert.deepEqual(f.selected('[data-select-role-group].is-selected'), ['Mother']);
      assert.equal(f.query('[data-instance-pill].is-selected'), null);
      assert.equal(f.query('[data-instance-axis].is-selected'), null);
      assert.equal(f.query('[data-matching-set-add-button]').disabled, true);
      assert.ok(f.query('#price-fixture .price--range'));
    } finally { f.close(); }
  });
}

test('unavailable explicit variant is visible, priced and cannot be added', async () => {
  const f = setup(data(203));
  try {
    assert.deepEqual(f.selected('[data-select-role-group].is-selected'), ['Child']);
    assert.equal(f.query('[data-instance-pill].is-selected').getAttribute('data-size-label'), '8 Years');
    assert.equal(f.query('[data-instance-pill].is-selected').disabled, true);
    assert.equal(f.query('#price-fixture .price-item--regular').textContent, '$21.00');
    assert.equal(f.query('[data-matching-set-add-button]').disabled, true);
    assert.match(f.query('[data-matching-set-add-button]').textContent, /Out of stock/);
    f.query('[data-matching-set-add-button]').dispatchEvent(new f.window.MouseEvent('click', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.equal(f.requests.length, 0);
    assert.equal(f.query('[data-matching-set-summary]').hidden, true);
  } finally { f.close(); }
});

test('shopper changing role clears the linked price and never reseeds the deep link', () => {
  const f = setup(data(202));
  try {
    f.click('[data-select-role-group="mother"]');
    assert.equal(f.query('[data-instance-pill].is-selected'), null);
    assert.ok(f.query('#price-fixture .price--range'));
    f.click('[data-select-role-group="child"]');
    assert.equal(f.query('[data-instance-pill].is-selected'), null);
    assert.equal(f.query('[data-instance-axis].is-selected'), null);
    assert.equal(f.query('[data-matching-set-add-button]').disabled, true);
  } finally { f.close(); }
});

test('changing axes refreshes the price and clearing an axis returns to the range', () => {
  const f = setup(data(202));
  try {
    f.click('[data-axis-name="Pattern"][data-axis-value="Solid"]');
    assert.equal(f.query('#price-fixture .price').getAttribute('data-price-variant-id'), '204');
    assert.equal(f.query('#price-fixture .price-item--regular').textContent, '$23.00');
    f.click('[data-axis-name="Pattern"][data-axis-value="Solid"]');
    assert.ok(f.query('#price-fixture .price--range'));
    assert.equal(f.query('[data-matching-set-add-button]').disabled, true);
  } finally { f.close(); }
});

test('quantity and legacy change rerenders preserve shopper choices without reseeding', () => {
  const f = setup(data(202));
  try {
    f.click('[data-qty-action="inc"]');
    f.window.document.getElementById('variant-selects-fixture').dispatchEvent(new f.window.Event('change'));
    assert.equal(f.query('[data-qty-value]').textContent, '2');
    assert.deepEqual(f.selected('[data-instance-axis].is-selected'), ['Blue', 'Floral']);
    f.click('[data-instance-pill].is-selected');
    f.window.document.getElementById('variant-selects-fixture').dispatchEvent(new f.window.Event('change'));
    assert.equal(f.query('[data-instance-pill].is-selected'), null);
    assert.equal(f.query('[data-matching-set-add-button]').disabled, true);
  } finally { f.close(); }
});

test('server-formatted EUR and JPY values survive without USD conversion', () => {
  for (const [currency, lang, expected] of [['EUR', 'de', '22,00 €'], ['JPY', 'ja', '¥3,100']]) {
    const fixture = data(202, currency);
    fixture.variants.find(v => v.id === 202).price_text = expected;
    const f = setup(fixture, lang);
    try { assert.equal(f.query('#price-fixture .price-item--regular').textContent, expected); }
    finally { f.close(); }
  }
});

test('server money entities decode once while preserving spaces, ampersands and text controls', () => {
  const cases = [
    ['22,00&nbsp;€', '22,00\u00a0€'],
    ['22,00&nbsp €', '22,00\u00a0 €'],
    ['22,00&#160;€', '22,00\u00a0€'],
    ['22,00&#x202f;€', '22,00\u202f€'],
    ['22,00\u00a0€ / 22,00\u202f€', '22,00\u00a0€ / 22,00\u202f€'],
    ['R&amp;D & fee &unknown;', 'R&D & fee &unknown;'],
    ['22,00 &amp;nbsp; €', '22,00 &nbsp; €'],
    ['22,00&#x9;€&#10;EUR', '22,00\t€\nEUR'],
    ['22,00&#13;€', '22,00\r€'],
    ['22,00&#0;€', '22,00\ufffd€'],
  ];
  for (const [encoded, expected] of cases) {
    const product = data(202, 'EUR');
    product.variants.find(v => v.id === 202).price_text = encoded;
    const f = setup(product, 'de');
    try {
      assert.equal(f.query('#price-fixture .price-item--regular').textContent, expected);
      assert.equal(f.query('#price-fixture .price').getAttribute('data-price-current-text'), expected);
      assert.equal(f.query('#price-fixture .price').getAttribute('data-price-variant-id'), '202');
    } finally { f.close(); }
  }
});

test('unit-price entities decode with the existing numeric reference quantity and unit', () => {
  const product = data(202, 'EUR');
  Object.assign(product.variants.find(v => v.id === 202), {
    unit_price_text: '4,40&#160;€', unit_price_reference_value: 100, unit_price_reference_unit: 'g',
  });
  const f = setup(product, 'de');
  try {
    assert.equal(f.query('.unit-price').hidden, false);
    assert.equal(f.query('.unit-price .price-item > span:first-child').textContent, '4,40\u00a0€');
    assert.equal(f.query('.unit-price .price-item > span:last-child').textContent, '100g');
    assert.equal(f.query('#price-fixture .price').getAttribute('data-price-variant-id'), '202');
  } finally { f.close(); }
});

test('decoding money text never creates markup or executes an encoded event handler', () => {
  const product = data(202, 'EUR');
  product.variants.find(v => v.id === 202).price_text = '&lt;img src=x onerror=alert(1)&gt; <em>22,00 €</em>';
  const f = setup(product);
  try {
    assert.equal(f.query('#price-fixture .price-item--regular').textContent, '<img src=x onerror=alert(1)> <em>22,00 €</em>');
    assert.equal(f.query('#price-fixture img, #price-fixture script, #price-fixture em'), null);
    assert.equal(f.requests.length, 0);
    assert.equal(f.query('[data-matching-set-add-button]').disabled, false);
  } finally { f.close(); }
});

test('an asynchronous stale Dawn price replacement is reconciled without a mutation loop', async () => {
  const f = setup(data(202));
  try {
    const price = f.query('#price-fixture');
    price.innerHTML = '<div>Old adult price $30</div>';
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.equal(f.query('#price-fixture .price-item--regular').textContent, '$22.00');
    const stable = price.innerHTML;
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.equal(price.innerHTML, stable);
  } finally { f.close(); }
});

test('all 21 published locales preserve scoped returns plus exact reviewed release additions', () => {
  const copies = JSON.parse(fs.readFileSync(path.join(root, 'return_copy.json'), 'utf8'));
  const parse = text => JSON.parse(text.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, ''));
  const keys = ['returns_headline', 'returns_summary', 'returns_eligible', 'returns_exclusions', 'returns_damaged', 'returns_shipping'];
  for (const [locale, values] of Object.entries(copies)) {
    const filename = 'locales/' + (locale === 'en' ? 'en.default' : locale) + '.json';
    const before = parse(fs.readFileSync(path.join(root, 'baseline', filename), 'utf8'));
    const after = parse(fs.readFileSync(path.join(root, 'theme', filename), 'utf8'));
    normalizeReviewedReleaseAdditions(before, after, filename);
    for (let i = 0; i < keys.length; i++) {
      assert.equal(after.products.purchase_confidence[keys[i]], values[i]);
      delete before.products.purchase_confidence[keys[i]];
      delete after.products.purchase_confidence[keys[i]];
    }
    assert.deepEqual(after, before, locale);
    assert.ok(after.accessibility.close, locale);
  }
});

test('reviewed selector dictionaries preserve English and all existing entries', () => {
  const f = setup();
  try {
    const replacements = JSON.parse(fs.readFileSync(path.resolve(root, '../../2026-09-09-microsoft-ads-rebuild/buy_button_locale_replacements.json'), 'utf8'));
    replacements.da.addCurrentPiece = 'Læg denne vare i indkøbskurven';
    replacements.da.readyToAdd = 'Klar til at lægge i kurven';
    for (const [locale, labels] of Object.entries(replacements)) {
      f.window.document.documentElement.lang = locale === 'pt' ? 'pt-BR' : locale;
      for (const [key, value] of Object.entries(labels)) assert.equal(f.window.uiLabel(key, 'unexpected fallback'), value, `${locale}.${key}`);
    }
  } finally { f.close(); }
});

test('inactive locale parity preserves existing text with exact return, shipping and consent additions', () => {
  const copies = JSON.parse(fs.readFileSync(path.join(root, 'inactive_return_copy.json'), 'utf8'));
  const parse = text => JSON.parse(text.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, ''));
  for (const [locale, values] of Object.entries(copies)) {
    const filename = 'locales/' + locale + '.json';
    const before = parse(fs.readFileSync(path.join(root, 'baseline', filename), 'utf8'));
    const after = parse(fs.readFileSync(path.join(root, 'theme', filename), 'utf8'));
    normalizeReviewedReleaseAdditions(before, after, filename);
    for (const [index, key] of ['returns_damaged', 'returns_shipping'].entries()) {
      assert.equal(Object.hasOwn(before.products.purchase_confidence, key), false);
      assert.equal(after.products.purchase_confidence[key], values[index]);
      delete after.products.purchase_confidence[key];
    }
    assert.deepEqual(after, before, locale);
  }
  const filenames = fs.readdirSync(path.join(root, 'theme/locales')).filter(name => name.endsWith('.json') && !name.endsWith('.schema.json'));
  assert.equal(filenames.length, 35);
  for (const filename of filenames) {
    const dict = parse(fs.readFileSync(path.join(root, 'theme/locales', filename), 'utf8')).products.purchase_confidence;
    assert.ok(dict.returns_damaged && dict.returns_shipping, filename);
  }
});
