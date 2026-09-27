// Tests for the pure helpers in assets/dlm-family-builder.js.
// Run: node --test ops/tests/test_family_builder.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const fb = require(path.join(here, '..', '..', 'assets', 'dlm-family-builder.js'));

const mother = { variantId: '47169572929633', quantity: 1, unitPrice: 3599, roleKey: 'mother', label: 'Mother · M' };
const father = { variantId: '47169573126241', quantity: 1, unitPrice: 3599, roleKey: 'father', label: 'Father · L' };
const child = { variantId: '47169572765793', quantity: 1, unitPrice: 3299, roleKey: 'child', label: 'Child · 4-5 Years' };

test('mergeLine appends new variants and merges repeats without mutating input', () => {
  const one = fb.mergeLine([], mother);
  const two = fb.mergeLine(one, child);
  const three = fb.mergeLine(two, child);
  assert.equal(one.length, 1);
  assert.equal(two.length, 2);
  assert.equal(three.length, 2);
  assert.equal(three[1].quantity, 2);
  assert.equal(two[1].quantity, 1, 'input array untouched');
});

test('mergeLine ignores empty, zero-qty and missing-id lines and caps quantity', () => {
  assert.deepEqual(fb.mergeLine([mother], null).length, 1);
  assert.equal(fb.mergeLine([], { ...mother, quantity: 0 }).length, 0);
  assert.equal(fb.mergeLine([], { ...mother, variantId: '' }).length, 0);
  const big = fb.mergeLine([{ ...mother, quantity: 98 }], { ...mother, quantity: 5 });
  assert.equal(big[0].quantity, fb.MAX_LINE_QTY);
});

test('removeLine removes by variant id only', () => {
  const lines = [mother, father, child].reduce((acc, line) => fb.mergeLine(acc, line), []);
  const left = fb.removeLine(lines, father.variantId);
  assert.deepEqual(left.map((l) => l.roleKey), ['mother', 'child']);
  assert.equal(fb.removeLine(left, 'nope').length, 2);
});

test('family of four: totals and combined pending selection use real prices', () => {
  let lines = fb.mergeLine([], mother);
  lines = fb.mergeLine(lines, father);
  const pending = { ...child, quantity: 2 };
  const all = fb.combineWithPending(lines, pending);
  assert.deepEqual(fb.computeTotals(all), { count: 4, cents: 3599 + 3599 + 3299 * 2 });
  assert.deepEqual(fb.computeTotals(fb.combineWithPending(lines, null)), { count: 2, cents: 7198 });
});

test('items payload and request body match Shopify /cart/add.js', () => {
  const all = fb.combineWithPending(fb.mergeLine(fb.mergeLine([], mother), father), { ...child, quantity: 2 });
  const body = fb.buildRequestBody(all, ['cart-drawer', 'cart-icon-bubble'], '/products/beanie-ghost-family-matching-pajamas');
  assert.deepEqual(body, {
    items: [
      { id: 47169572929633, quantity: 1 },
      { id: 47169573126241, quantity: 1 },
      { id: 47169572765793, quantity: 2 },
    ],
    sections: 'cart-drawer,cart-icon-bubble',
    sections_url: '/products/beanie-ghost-family-matching-pajamas',
  });
  assert.deepEqual(fb.buildRequestBody([mother], [], '/x'), { items: [{ id: 47169572929633, quantity: 1 }] });
});

test('findUnavailable flags sold-out or unknown variants', () => {
  const variants = {
    [mother.variantId]: { id: 1, available: true },
    [father.variantId]: { id: 2, available: false },
  };
  const bad = fb.findUnavailable([mother, father, child], variants);
  assert.deepEqual(bad.map((l) => l.roleKey), ['father', 'child']);
});

test('nextRoleKey walks the builder order, then stays put', () => {
  const order = ['mother', 'father', 'child'];
  assert.equal(fb.nextRoleKey(order, [mother]), 'father');
  assert.equal(fb.nextRoleKey(order, [mother, father]), 'child');
  assert.equal(fb.nextRoleKey(order, [mother, father, child]), null);
  assert.equal(fb.nextRoleKey(['mother', 'child'], [child]), 'mother');
});

test('money format is learned from the shop price text', () => {
  const usd = fb.parseMoneyFormat('$32.99 USD', 3299);
  assert.equal(fb.formatMoney(13196, usd), '$131.96 USD');
  assert.equal(fb.formatMoney(123456, usd), '$1,234.56 USD');
  const eur = fb.parseMoneyFormat('32,99 €', 3299);
  assert.equal(fb.formatMoney(123456, eur), '1.234,56 €');
  const eurDot = fb.parseMoneyFormat('€1.299,00 EUR', 129900);
  assert.equal(fb.formatMoney(260000, eurDot), '€2.600,00 EUR');
  const jpy = fb.parseMoneyFormat('¥3,300', 330000);
  assert.equal(fb.formatMoney(990000, jpy), '¥9,900');
  assert.equal(fb.parseMoneyFormat('free', 3299), null);
  assert.equal(fb.parseMoneyFormat('$40.00', 3299), null, 'mismatched sample is rejected');
  assert.match(fb.formatMoney(13196, null, 'USD', 'en-US'), /131\.96/);
});

test('locale lookup covers every storefront language and falls back to English', () => {
  const required = ['en', 'es', 'fr', 'de', 'it', 'nl', 'pt', 'da', 'sv', 'no', 'pl', 'cs', 'ja', 'ko', 'ru', 'ar', 'he', 'hi', 'el', 'ro', 'fi', 'hu', 'tr', 'zh'];
  const keys = Object.keys(fb.STRINGS.en);
  for (const lang of required) {
    assert.ok(fb.STRINGS[lang], `missing ${lang}`);
    for (const key of keys) {
      assert.equal(typeof fb.STRINGS[lang][key], 'string', `${lang}.${key}`);
      assert.ok(fb.STRINGS[lang][key].length > 0, `${lang}.${key} empty`);
    }
    assert.ok(fb.STRINGS[lang].addAll.includes('{count}') && fb.STRINGS[lang].addAll.includes('{total}'), `${lang}.addAll placeholders`);
    assert.ok(fb.STRINGS[lang].soldOut.includes('{item}'), `${lang}.soldOut placeholder`);
  }
  assert.equal(fb.resolveLanguage('pt-BR'), 'pt');
  assert.equal(fb.resolveLanguage('zh-CN'), 'zh');
  assert.equal(fb.resolveLanguage('nb'), 'no');
  assert.equal(fb.resolveLanguage('ro-RO'), 'ro');
  assert.equal(fb.resolveLanguage('xx'), 'en');
  assert.equal(fb.resolveLanguage(''), 'en');
  assert.equal(fb.translate('addAll', 'en', { count: 4, total: '$131.96 USD' }), 'Add all to bag (4) · $131.96 USD');
  assert.equal(fb.translate('addAll', 'de', { count: 2, total: '71,98 €' }), 'Alle in den Warenkorb (2) · 71,98 €');
  assert.equal(fb.translate('remove', 'xx'), 'Remove');
});

test('nextRoleKey also skips roles already added to the bag from this page', () => {
  const order = ['mother', 'father', 'child'];
  assert.equal(fb.nextRoleKey(order, [], ['mother']), 'father');
  assert.equal(fb.nextRoleKey(order, [father], ['mother']), 'child');
  assert.equal(fb.nextRoleKey(order, [child], ['mother', 'father']), null);
  assert.equal(fb.nextRoleKey(order, [mother], undefined), 'father', 'extra roles are optional');
});

test('roleChips offers every role the product has and flags the missing ones', () => {
  const roles = [
    { key: 'mother', label: 'Mother' },
    { key: 'father', label: 'Father' },
    { key: 'child', label: ' Child ' },
  ];
  assert.deepEqual(fb.roleChips(roles, [], mother, []), [
    { key: 'mother', label: '+ Mother', missing: false },
    { key: 'father', label: '+ Father', missing: true },
    { key: 'child', label: '+ Child', missing: true },
  ]);
  const later = fb.roleChips(roles, [mother], child, ['father']);
  assert.deepEqual(later.map((c) => c.missing), [false, false, false], 'a second child stays offered');
  assert.deepEqual(later.map((c) => c.key), ['mother', 'father', 'child'], 'builder order kept');
});

test('roleChips falls back to the plain button when a label is unknown or there is one role', () => {
  assert.deepEqual(fb.roleChips([{ key: 'mother', label: 'Mother' }], [], mother), []);
  assert.deepEqual(fb.roleChips([{ key: 'mother', label: 'Mother' }, { key: 'child', label: '' }], [], mother), []);
  assert.deepEqual(fb.roleChips(null, [], mother), []);
  const ar = fb.roleChips([{ key: 'mother', label: 'الأم' }, { key: 'child', label: 'الطفل' }], [], null);
  assert.deepEqual(ar.map((c) => c.label), ['+ الأم', '+ الطفل']);
  assert.deepEqual(ar.map((c) => c.missing), [true, true]);
});

test('chip caption reuses the existing add-another copy without its plus', () => {
  assert.equal(fb.stripLeadingPlus(fb.STRINGS.en.addAnother), 'Add another family member');
  assert.equal(fb.stripLeadingPlus('＋ 別のご家族を追加'), '別のご家族を追加');
  assert.equal(fb.stripLeadingPlus('No plus'), 'No plus');
  for (const lang of Object.keys(fb.STRINGS)) {
    const caption = fb.stripLeadingPlus(fb.STRINGS[lang].addAnother);
    assert.ok(caption.length > 0 && !caption.startsWith('+'), `${lang} caption`);
  }
});

test('isAddSuccess only matches the builder success copy', () => {
  assert.equal(fb.isAddSuccess(' Matching set added to cart. ', 'Matching set added to cart.'), true);
  assert.equal(fb.isAddSuccess('Unable to add the selected pieces. Please try again.', 'Matching set added to cart.'), false);
  assert.equal(fb.isAddSuccess('', ''), false);
  assert.equal(fb.isAddSuccess('anything', undefined), false);
});

test('cart add url keeps the locale prefix and targets the .js endpoint', () => {
  assert.equal(fb.cartAddJsUrl({ cart_add_url: '/cart/add' }), '/cart/add.js');
  assert.equal(fb.cartAddJsUrl({ cart_add_url: '/es/cart/add' }), '/es/cart/add.js');
  assert.equal(fb.cartAddJsUrl(undefined), '/cart/add.js');
});
