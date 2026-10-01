// Tests for the "Complete the family" cart upsell.
// - Pure helpers in assets/dlm-complete-family.js.
// - The role alias table in snippets/dlm-complete-family.liquid, which decides
//   which family role a (translated) variant option value belongs to and so
//   which roles are missing from the cart. It must stay unambiguous and in
//   sync with ROLE_DEFINITIONS in the PDP builder.
// Run: node --test ops/tests/test_complete_family.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.join(here, '..', '..');
const cf = require(path.join(repo, 'assets', 'dlm-complete-family.js'));
const snippet = readFileSync(path.join(repo, 'snippets', 'dlm-complete-family.liquid'), 'utf8');

function memoryStorage(initial = {}) {
  const data = { ...initial };
  return {
    data,
    getItem: (key) => (Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null),
    setItem: (key, value) => {
      data[key] = String(value);
    },
  };
}

const throwingStorage = {
  getItem() {
    throw new Error('SecurityError');
  },
  setItem() {
    throw new Error('QuotaExceededError');
  },
};

test('pickRememberedIndex matches the remembered size loosely and skips the placeholder', () => {
  const sizes = ['', 'S', 'M', 'L', '2XL'];
  assert.equal(cf.pickRememberedIndex(sizes, 'M'), 2);
  assert.equal(cf.pickRememberedIndex(sizes, '  m '), 2);
  assert.equal(cf.pickRememberedIndex(['', '2 Years', '10 Years'], '10  years'), 2);
  assert.equal(cf.pickRememberedIndex(sizes, 'XXXL'), -1);
  assert.equal(cf.pickRememberedIndex(sizes, ''), -1);
  assert.equal(cf.pickRememberedIndex(null, 'M'), -1);
});

test('size memory is per role, session-only and never throws', () => {
  const store = memoryStorage();
  assert.equal(cf.rememberSize(store, 'father', 'L'), true);
  assert.equal(store.data['dlm:lastSize:father'], 'L');
  assert.equal(cf.readRememberedSize(store, 'father'), 'L');
  assert.equal(cf.readRememberedSize(store, 'mother'), '');
  assert.equal(cf.rememberSize(store, 'uncle', 'L'), false, 'unknown role is ignored');
  assert.equal(cf.rememberSize(store, 'child', '   '), false, 'blank size is ignored');
  assert.equal(cf.rememberSize(throwingStorage, 'child', '4 Years'), false);
  assert.equal(cf.readRememberedSize(throwingStorage, 'child'), '');
  assert.equal(cf.readRememberedSize(null, 'child'), '');
});

test('buildAddBody adds exactly one piece of one real variant with the host sections', () => {
  const drawerSections = [
    { id: 'CartDrawer', section: 'cart-drawer', selector: '.drawer__inner' },
    { id: 'cart-icon-bubble', section: 'cart-icon-bubble', selector: '.shopify-section' },
  ];
  assert.deepEqual(cf.buildAddBody('48843307548769', drawerSections, '/products/jolly-crew-family-matching-pajamas'), {
    items: [{ id: 48843307548769, quantity: 1 }],
    sections: 'cart-drawer,cart-icon-bubble',
    sections_url: '/products/jolly-crew-family-matching-pajamas',
  });
  assert.deepEqual(cf.buildAddBody(48843307548769, [], '/cart'), { items: [{ id: 48843307548769, quantity: 1 }] });
  assert.equal(cf.buildAddBody('', drawerSections, '/'), null);
  assert.equal(cf.buildAddBody('abc', drawerSections, '/'), null);
  assert.equal(cf.buildAddBody('-5', drawerSections, '/'), null);
  assert.equal(cf.buildAddBody('1.5', drawerSections, '/'), null);
});

test('uniqueSectionIds dedupes the cart page sections and respects the 5-section limit', () => {
  const cartPage = [
    { id: 'main-cart-items', section: 'template--1__cart-items', selector: '.js-contents' },
    { id: 'main-cart-title', section: 'template--1__cart-items', selector: '#main-cart-title' },
    { id: 'cart-icon-bubble', section: 'cart-icon-bubble', selector: '.shopify-section' },
    { id: 'cart-live-region-text', section: 'cart-live-region-text', selector: '.shopify-section' },
    { id: 'main-cart-footer', section: 'template--1__cart-footer', selector: '#main-cart-footer-subtotal' },
  ];
  assert.deepEqual(cf.uniqueSectionIds(cartPage), [
    'template--1__cart-items',
    'cart-icon-bubble',
    'cart-live-region-text',
    'template--1__cart-footer',
  ]);
  assert.equal(cf.uniqueSectionIds(['a', 'b', 'c', 'd', 'e', 'f', 'a']).length, 5);
  assert.deepEqual(cf.uniqueSectionIds([null, '', { section: '' }, ' x ']), ['x']);
});

test('cart add URL stays locale-aware like assets/cart.js', () => {
  assert.equal(cf.cartAddJsUrl({ cart_add_url: '/cart/add' }, '/'), '/cart/add.js');
  assert.equal(cf.cartAddJsUrl({ cart_add_url: '/es/cart/add' }, '/es/'), '/es/cart/add.js');
  assert.equal(cf.cartAddJsUrl({ cart_add_url: '/cart/add' }, '/fr/'), '/fr/cart/add.js');
  assert.equal(cf.cartAddJsUrl(null, undefined), '/cart/add.js');
  assert.equal(cf.localeAwareRoute('/cart', '/de/'), '/de/cart');
  assert.equal(cf.localeAwareRoute('/de/cart', '/de/'), '/de/cart');
  assert.equal(cf.localeAwareRoute('https://x.test/cart', '/de/'), 'https://x.test/cart');
});

test('add responses: success needs items, errors surface Shopify text or the localized fallback', () => {
  assert.equal(cf.isAddSuccess(true, { items: [{ id: 1 }], sections: {} }), true);
  assert.equal(cf.isAddSuccess(false, { items: [] }), false);
  assert.equal(cf.isAddSuccess(true, { status: 422, message: 'Cart Error' }), false);
  assert.equal(cf.isAddSuccess(true, null), false);
  const soldOut = { status: 422, message: 'Cart Error', description: 'You can’t add more Father M to the cart.' };
  assert.equal(cf.errorText(soldOut, 'fallback'), 'You can’t add more Father M to the cart.');
  assert.equal(cf.errorText({ message: 'Cart Error' }, 'fallback'), 'Cart Error');
  assert.equal(cf.errorText({}, 'No se pudo añadir al carrito.'), 'No se pudo añadir al carrito.');
});

test('analytics event carries ids and role keys only', () => {
  assert.deepEqual(cf.analyticsEvent('add', 8123456789, 'father', 'cart'), {
    event: 'dlm_complete_family',
    action: 'add',
    product_id: '8123456789',
    role: 'father',
    surface: 'cart',
  });
  assert.equal(cf.analyticsEvent('add', 1, 'uncle', 'drawer'), null);
  assert.equal(cf.analyticsEvent('purchase', 1, 'child', 'drawer'), null);
  assert.equal(cf.analyticsEvent('open_role', 'gid://shopify/Product/42', 'child', 'elsewhere').surface, 'drawer');
  assert.equal(cf.analyticsEvent('open_role', 'gid://shopify/Product/42', 'child', 'drawer').product_id, '42');
});

test('added announcement reads "<prefix>: <role> · <size>"', () => {
  assert.equal(cf.addedMessage('Added to bag', 'Dad', 'M'), 'Added to bag: Dad · M');
  assert.equal(cf.addedMessage('Añadido al carrito', 'Infantil', ''), 'Añadido al carrito: Infantil');
  assert.equal(cf.addedMessage('', '', ''), '');
});

// --- Liquid role table -------------------------------------------------------

function parseAliasTable(source) {
  // Base table only: the two-space-indented assigns. Per-language additions
  // ('baba') sit deeper inside an if/elsif and are checked separately.
  const chunks = [...source.matchAll(/^  assign dcf_alias = (?:dcf_alias \| append: )?'([^']*)'/gm)].map((m) => m[1]);
  const table = new Map();
  const duplicates = [];
  chunks.join('').split('|').forEach((entry) => {
    if (!entry) return;
    const [alias, role] = entry.split('=');
    if (table.has(alias) && table.get(alias) !== role) duplicates.push(`${alias}: ${table.get(alias)} vs ${role}`);
    table.set(alias, role);
  });
  return { table, duplicates };
}

const { table: aliasTable, duplicates } = parseAliasTable(snippet);

// Mirror of the snippet's lookup order for one option value: first two words,
// first word, first hyphen segment, last word.
function roleOf(value) {
  const words = String(value).replace(/[():,/]/g, ' ').trim().toLowerCase().split(/\s+/).filter(Boolean);
  const candidates = [];
  if (words.length > 1) candidates.push(`${words[0]} ${words[1]}`);
  if (words.length) candidates.push(words[0]);
  if (words.length && words[0].includes('-')) candidates.push(words[0].split('-')[0]);
  if (words.length > 1) candidates.push(words[words.length - 1]);
  for (const candidate of candidates) if (aliasTable.has(candidate)) return aliasTable.get(candidate);
  return '';
}

// Mirror of the snippet's per-product decision: the option must carry at
// least two roles; then offer every role not in the cart, plus "another" kid
// or adult when that role is already there.
function missingRoles(optionValues, cartValues) {
  const roles = new Set(optionValues.map(roleOf).filter(Boolean));
  if (roles.size < 2) return [];
  const inCart = new Set(cartValues.map(roleOf).filter(Boolean));
  const offered = [];
  for (const role of cf.ROLE_KEYS) {
    if (!optionValues.some((value) => roleOf(value) === role)) continue;
    if (!inCart.has(role) || role === 'child' || role === 'adult') offered.push(inCart.has(role) ? `another ${role}` : role);
  }
  return offered;
}

test('alias table is unambiguous, lowercase and covers every role', () => {
  assert.deepEqual(duplicates, []);
  assert.ok(aliasTable.size > 200, `expected a multilingual table, got ${aliasTable.size}`);
  for (const [alias, role] of aliasTable) {
    assert.equal(alias, alias.toLowerCase(), `alias ${alias} must be lowercase`);
    assert.ok(cf.ROLE_KEYS.includes(role), `alias ${alias} maps to unknown role ${role}`);
  }
  for (const role of cf.ROLE_KEYS) assert.ok([...aliasTable.values()].includes(role), `no alias for ${role}`);
  assert.ok(!aliasTable.has('baba'), "'baba' is language-specific (hu baby / tr father) and added per locale");
  assert.match(snippet, /dcf_lang == 'hu'\s+assign dcf_alias = dcf_alias \| append: 'baba=baby\|'/);
  assert.match(snippet, /dcf_lang == 'tr'\s+assign dcf_alias = dcf_alias \| append: 'baba=father\|'/);
});

test('alias table agrees with ROLE_DEFINITIONS in the PDP builder', () => {
  const pdp = readFileSync(path.join(repo, 'assets', 'product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
  const block = pdp.slice(pdp.indexOf('var ROLE_DEFINITIONS = ['), pdp.indexOf('var ROLE_FIT_COPY_BY_LOCALE'));
  const defs = [...block.matchAll(/key: '(\w+)'[\s\S]*?aliases: \[([^\]]*)\]/g)];
  assert.equal(defs.length, 7);
  const mismatches = [];
  for (const [, key, list] of defs) {
    for (const [, alias] of list.matchAll(/'([^']+)'/g)) {
      const lower = alias.toLowerCase();
      if (/\s/.test(lower)) continue; // multi-word PDP aliases ("mom dress") match on their first word
      if (aliasTable.get(lower) !== key) mismatches.push(`${alias} -> ${aliasTable.get(lower) || 'missing'} (PDP: ${key})`);
    }
  }
  assert.deepEqual(mismatches, []);
});

test('missing roles for Jolly Crew pajamas (live option values, en and es)', () => {
  const en = ['Child 2 Years', 'Child 14 Years', 'Mother S', 'Mother M', 'Father S', 'Father 4XL'];
  assert.deepEqual(missingRoles(en, ['Mother M']), ['father', 'child']);
  assert.deepEqual(missingRoles(en, ['Mother M', 'Child 4 Years']), ['father', 'another child']);
  assert.deepEqual(missingRoles(en, ['Mother M', 'Father L', 'Child 4 Years']), ['another child']);
  const es = ['Infantil 2 años', 'Mamá S', 'Papá S'];
  assert.deepEqual(missingRoles(es, ['Mamá M']), ['father', 'child']);
});

test('role lookup handles adult/child sweaters, suffix roles, hyphens and non-roles', () => {
  assert.deepEqual(missingRoles(['Adult S', 'Adult M', 'Child 4Y'], ['Adult M']), ['child', 'another adult']);
  assert.equal(roleOf('S (Mom)'), 'mother');
  assert.equal(roleOf('Mother-S'), 'mother');
  assert.equal(roleOf('Bé gái 4 tuổi'), 'girl');
  assert.equal(roleOf('Trẻ em 2 tuổi'), 'child');
  assert.equal(roleOf('Baby 3 Months'), 'baby');
  assert.equal(roleOf('Red'), '');
  assert.equal(roleOf('M'), '');
  // A colour like "Baby Pink" alone yields only one role, so the snippet does
  // not treat the Color option as the family-role option.
  assert.deepEqual(missingRoles(['Baby Pink', 'Baby Blue'], ['Baby Blue']), []);
  assert.deepEqual(missingRoles(['Mother S', 'Mother M'], ['Mother S']), [], 'a mom-only product offers nothing');
});

test('single-piece notice: translated for every language and shown only for exactly 1 piece', () => {
  // Every language block (default + each case branch) defines both strings.
  const blocks = (snippet.match(/assign t_another_adult = /g) || []).length;
  assert.equal((snippet.match(/assign t_single = /g) || []).length, blocks);
  assert.equal((snippet.match(/assign t_single_hint = /g) || []).length, blocks);
  // Pieces sum line quantities, so 2 of the same kid size (siblings) count as matching.
  assert.match(snippet, /assign dcf_pieces = dcf_pieces \| plus: dcf_line\.quantity/);
  assert.match(snippet, /if dcf_pieces == 1\s+assign dcf_product_html = dcf_product_html \| append: '<p class="dlm-cf__single"/);
  // Output is escaped.
  assert.match(snippet, /assign dcf_single_e = t_single \| escape/);
  assert.match(snippet, /assign dcf_single_hint_e = t_single_hint \| escape/);
});

test('single-piece designs are listed first so max_products never hides the notice', () => {
  assert.match(snippet, /for dcf_pass in \(1\.\.2\)\s+for item in dcf_items/);
  assert.match(snippet, /if dcf_pass == 1 and dcf_qty_all != 1\s+continue/);
  // The seen-marker is set only after the pass filter, so pass 2 still visits multi-piece designs.
  assert.ok(snippet.indexOf('if dcf_pass == 1 and dcf_qty_all != 1') < snippet.indexOf("assign dcf_seen = dcf_seen | append: item.product_id"));
});
