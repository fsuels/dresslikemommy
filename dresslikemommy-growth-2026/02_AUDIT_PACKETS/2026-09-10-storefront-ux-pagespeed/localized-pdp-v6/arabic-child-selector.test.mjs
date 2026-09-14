import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import test from 'node:test';
import { runInContext } from 'node:vm';

const require = createRequire(import.meta.url);
const { JSDOM } = require(process.env.DLM_TEST_JSDOM_PATH || '/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const assetName = 'assets/product-desktop-ux-20260513-ruler-sync.js';
const candidate = readFileSync(new URL(`../candidate/${assetName}`, import.meta.url), 'utf8');
const snapshot = JSON.parse(readFileSync(new URL('./before.json', import.meta.url), 'utf8'));
const repairRoot = new URL('../../2026-09-10-together-heart-source-repair/', import.meta.url);
const product = JSON.parse(readFileSync(new URL('after.json', repairRoot), 'utf8')).source.product;
const plan = JSON.parse(readFileSync(new URL('plan.json', repairRoot), 'utf8'));
const englishSizes = product.options.find((option) => option.name === 'Size').values;
const arabic = plan.rows.find((row) => row.locale === 'ar');
const digest = (text, algorithm = 'sha256') => createHash(algorithm).update(text).digest('hex');
const plain = (value) => JSON.parse(JSON.stringify(value));

// Reconstruct only the three exact edits; the frozen MD5 binds this to the captured original asset.
function originalSource() {
  let source = candidate;
  const inverse = [
    [", 'اطفال', 'للأولاد']", ", 'اطفال']"],
    ["  if (/(^|-)kid(-|$)/.test(text)) return 'child';\n", ''],
    ["  // A generic KID token fills a missing role without replacing explicit role labels.\n  if (skuRoleKey && skuRoleKey !== 'child') {", '  if (skuRoleKey) {'],
  ];
  for (const [changed, original] of inverse) {
    assert.equal(source.split(changed).length - 1, 1, 'Expected exactly one scoped edit');
    source = source.replace(changed, original);
  }
  assert.equal(digest(source, 'md5'), '1d3544d25d247e50b862a089c9249e9a');
  return source;
}
const baseline = originalSource();

function harness(source, locale, body = '') {
  const dom = new JSDOM(`<!doctype html><html lang="${locale}"><body>${body}</body></html>`, {
    url: `https://dresslikemommy.com/${locale}/products/together-heart-family-matching-sweaters`,
    runScripts: 'outside-only',
  });
  dom.window.fetch = () => { throw new Error('Network is forbidden in this regression'); };
  runInContext(source, dom.getInternalVMContext(), { filename: assetName });
  return { dom, api: dom.window, close: () => dom.window.close() };
}

function fixture(api) {
  const table = api.document.querySelector('#size-chart');
  const parsed = api.parseSizeGuideTable(table);
  assert.equal(parsed.rows.length, 14);
  const labels = parsed.rows.map((row) => row[0]);
  // API IDs/SKUs/prices/colors remain exact. Size labels come from the captured locale table.
  // Availability=true isolates classification; a separate check covers unavailable variants.
  const data = {
    options: product.options.map((option) => ({ name: option.name })),
    variants: product.variants.nodes.map((variant) => {
      const size = variant.selectedOptions.find((option) => option.name === 'Size').value;
      const color = variant.selectedOptions.find((option) => option.name === 'Color').value;
      const sizeIndex = englishSizes.indexOf(size);
      assert.notEqual(sizeIndex, -1);
      return {
        id: variant.id.split('/').pop(),
        sku: variant.sku,
        price: Math.round(Number(variant.price) * 100),
        available: true,
        option1: labels[sizeIndex],
        option2: color,
        option3: null,
        title: `${labels[sizeIndex]} / ${color}`,
      };
    }),
  };
  return { data, table, parsed };
}

function summary(groups) {
  return plain(groups.map((group) => ({
    role: group.roleKey,
    offers: group.options.length,
    sizes: new Set(group.options.map((option) => option.fullLabel)).size,
  })));
}

test('baseline reconstruction matches the captured preview source and exact product', () => {
  const file = snapshot.data.preview.source.nodes.find((node) => node.filename === assetName);
  assert.equal(file.checksumMd5, digest(baseline, 'md5'));
  assert.equal(product.id, 'gid://shopify/Product/7672336646241');
  assert.equal(product.variants.nodes.length, 98);
  assert.equal(product.variants.nodes.filter((variant) => /-KID-/.test(variant.sku)).length, 49);
});

test('original code reproduces 49 missing Arabic child offers before and after body repair', () => {
  for (const bodyKey of ['before_body', 'after_body']) {
    const h = harness(baseline, 'ar', arabic[bodyKey]);
    try {
      const { data, parsed } = fixture(h.api);
      assert.equal(data.variants[0].option1, 'للأولاد عمر سنتين');
      assert.equal(data.variants[0].id, '46512187113569');
      assert.equal(data.variants[0].price, 2499);
      assert.deepEqual(summary(h.api.buildRoleGroups(data, {}, true)), [{ role: 'adult', offers: 49, sizes: 7 }]);
      assert.equal(h.api.buildSizeGuideGroups(parsed).length, 0);
    } finally { h.close(); }
  }
});

test('patched actual code preserves all 98 offers and their IDs, prices, labels, colors and availability', () => {
  const h = harness(candidate, 'ar', arabic.after_body);
  try {
    const { data } = fixture(h.api);
    data.variants[0].available = false;
    const before = JSON.stringify(data);
    const groups = h.api.buildRoleGroups(data, {}, true);
    assert.deepEqual(summary(groups), [
      { role: 'child', offers: 49, sizes: 7 },
      { role: 'adult', offers: 49, sizes: 7 },
    ]);
    const offers = groups.flatMap((group) => group.options);
    assert.deepEqual(plain(offers.map((offer) => offer.id).sort()), data.variants.map((variant) => variant.id).sort());
    for (const variant of data.variants) {
      const offer = offers.find((item) => item.id === variant.id);
      assert.equal(offer.price, variant.price);
      assert.equal(offer.fullLabel, variant.option1);
      assert.equal(offer.axes.Color, variant.option2);
      assert.equal(offer.available, variant.available);
      const group = groups.find((item) => item.options.includes(offer));
      assert.equal(group.roleKey, /-KID-/.test(variant.sku) ? 'child' : 'adult');
    }
    const availableGroups = h.api.buildRoleGroups(data, {}, false);
    assert.equal(availableGroups.flatMap((group) => group.options).length, 97);
    assert.equal(JSON.stringify(data), before);
  } finally { h.close(); }
});

test('two seven-row guides retain the supplied measurements and all 140 source table cells', () => {
  for (const bodyKey of ['before_body', 'after_body']) {
    const h = harness(candidate, 'ar', arabic[bodyKey]);
    try {
      const { table, parsed } = fixture(h.api);
      const tableBefore = table.outerHTML;
      const cellsBefore = [...table.querySelectorAll('tbody td')].map((cell) => cell.textContent);
      const parsedBefore = JSON.stringify(parsed);
      assert.equal(cellsBefore.length, 140);
      const groups = h.api.buildSizeGuideGroups(parsed);
      assert.deepEqual(plain(groups.map((group) => [group.key, group.rows.length])), [['child', 7], ['adult', 7]]);
      for (const group of groups) {
        const offset = group.key === 'child' ? 0 : 7;
        group.rows.forEach((row, index) => {
          group.headers.forEach((header, column) => {
            if (column === 0) return;
            const sourceColumn = parsed.headers.findIndex((source) => source.raw === header.raw);
            assert.notEqual(sourceColumn, -1);
            assert.equal(row[column], parsed.rows[index + offset][sourceColumn]);
          });
        });
      }
      assert.equal(table.outerHTML, tableBefore);
      assert.deepEqual([...table.querySelectorAll('tbody td')].map((cell) => cell.textContent), cellsBefore);
      assert.equal(JSON.stringify(parsed), parsedBefore);
    } finally { h.close(); }
  }
});

test('Arabic alias requires the existing whole prefix or suffix boundary', () => {
  const h = harness(candidate, 'ar');
  try {
    for (const label of ['للأولاد عمر سنتين', 'للأولاد عمر 6-7 سنوات', 'للأولاد عمر 9-10 سنوات', 'للأولاد ٣ سنوات', 'للأولاد-3 سنوات', 'عمر 3 سنوات ' + 'للأولاد']) {
      const parsed = h.api.parseRoleFromSizeLabel(label);
      assert.equal(parsed?.key, 'child', label);
      assert.equal(parsed.fullLabel, label);
    }
    for (const label of ['للأولاد', 'للأولادية 3 سنوات', 'غيرللأولاد 3 سنوات', 'مقاس للأولادية', 'KIDNEY 3']) {
      assert.equal(h.api.parseRoleFromSizeLabel(label), null, label);
    }
  } finally { h.close(); }
});

test('KID SKU fallback is token-bounded and existing specific SKU precedence is unchanged', () => {
  const h = harness(candidate, 'ar');
  const old = harness(baseline, 'ar');
  try {
    for (const sku of ['DLM-THRT-KID-KID2Y-WHT', 'KID-2Y', 'DLM-THRT-KID', 'dlm-thrt-kid-2y']) {
      assert.equal(h.api.inferRoleKeyFromSku(sku), 'child', sku);
    }
    for (const sku of ['DLM-KIDNEY-2Y', 'DLM-SKID-2Y', 'DLM-KIDD-2Y', 'DLM-KID2Y-WHT', '', null]) {
      assert.equal(h.api.inferRoleKeyFromSku(sku), '', String(sku));
    }
    for (const token of ['GRL', 'BOY', 'MOM', 'DAD', 'BABY', 'ADULT']) {
      const sku = `DLM-KID-${token}-S`;
      assert.equal(h.api.inferRoleKeyFromSku(sku), old.api.inferRoleKeyFromSku(sku), sku);
    }
    const options = [{ name: 'Size' }, { name: 'Color' }];
    const unrecognized = { sku: 'DLM-THRT-KID-KID2Y-WHT', option1: 'المقاس الخاص', option2: 'White' };
    assert.equal(old.api.getRoleInfoForVariant(unrecognized, options, 0), null);
    assert.equal(h.api.getRoleInfoForVariant(unrecognized, options, 0).key, 'child');
  } finally { h.close(); old.close(); }
});

test('generic KID fallback preserves recognized adult, boy, girl, baby and unisex roles', () => {
  const h = harness(candidate, 'en');
  const old = harness(baseline, 'en');
  const options = [{ name: 'Size' }, { name: 'Color' }];
  try {
    for (const label of ['Mother S', 'Father M', 'Girl 3 Years', 'Boy 3 Years', 'Baby 6 Months', 'Child 3 Years', 'Adult S', 'الولد 3 سنوات', 'البنت 3 سنوات', 'للكبار S']) {
      const variant = { sku: 'DLM-HOLDOUT-KID-S-WHT', option1: label, option2: 'White' };
      assert.deepEqual(plain(h.api.getRoleInfoForVariant(variant, options, 0)), plain(old.api.getRoleInfoForVariant(variant, options, 0)), label);
    }
    for (const [sku, expected] of [['DLM-HOLDOUT-BOY-3Y', 'boy'], ['DLM-HOLDOUT-GRL-3Y', 'girl']]) {
      assert.equal(h.api.getRoleInfoForVariant({ sku, option1: 'للأولاد عمر 3 سنوات' }, options, 0).key, expected);
    }
  } finally { h.close(); old.close(); }
});

test('all 20 other captured locale role and guide outputs remain unchanged', async (t) => {
  const holdouts = plan.rows.filter((row) => row.locale !== 'ar');
  assert.equal(holdouts.length, 20);
  for (const row of holdouts) {
    await t.test(row.locale, () => {
      const h = harness(candidate, row.locale, row.after_body);
      const old = harness(baseline, row.locale, row.after_body);
      try {
        const actual = fixture(h.api);
        const previous = fixture(old.api);
        const groups = h.api.buildRoleGroups(actual.data, {}, true);
        const priorGroups = old.api.buildRoleGroups(previous.data, {}, true);
        assert.equal(groups.flatMap((group) => group.options).length, 98);
        assert.deepEqual(plain(groups), plain(priorGroups));
        assert.deepEqual(plain(h.api.buildSizeGuideGroups(actual.parsed)), plain(old.api.buildSizeGuideGroups(previous.parsed)));
        assert.equal(actual.table.outerHTML, previous.table.outerHTML);
      } finally { h.close(); old.close(); }
    });
  }
});
