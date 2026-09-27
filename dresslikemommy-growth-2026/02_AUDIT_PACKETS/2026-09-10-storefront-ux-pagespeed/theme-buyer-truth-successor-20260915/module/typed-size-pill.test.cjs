const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const fixtures = JSON.parse(fs.readFileSync(path.join(__dirname, 'typed-size-pill-fixtures.json')));
const originalFixtureBytes = JSON.stringify(fixtures);
const harnessPath = path.join(__dirname, 'buyer-truth.test.cjs');
const prefix = fs.readFileSync(harnessPath, 'utf8').split("for (const locale of ['en', 'fr', 'ar']) {")[0];
const sandbox = {require, console, __dirname};
vm.runInNewContext(prefix + '\nthis.production = {environment, tableDom, declaration};', sandbox);
const afterHarness = sandbox.production;
const copy = value => JSON.parse(JSON.stringify(value));

function environment(product, production = afterHarness) {
  const tables = product.tables.map(t => production.tableDom(t, t.heading));
  const env = production.environment('en', tables);
  if (typeof env.ctx.measurementDetailsKey !== 'function') {
    vm.runInContext(production.declaration('measurementDetailsKey'), env.ctx);
  }
  env.ctx.productData = {options: product.options, variants: product.variants.map(v => ({...v, available: true, price: Math.round(Number(v.price) * 100)}))};
  env.ctx.roleGroupsCache = env.ctx.buildRoleGroups(env.ctx.productData, {}, true, {skipTypeFilter: true});
  return env;
}

function matches(product, production) {
  const {ctx} = environment(product, production);
  const cases = [];
  for (const group of ctx.roleGroupsCache) for (const option of group.options) {
    const inst = {roleKey: group.roleKey || group.key, groupKey: group.key, axisSelections: option.axes || {}, sizeLabel: option.sizeLabel};
    const context = ctx.getMeasurementContextForInstance(group, inst, option);
    const match = ctx.findMeasurementsForOption(group, option, context);
    cases.push({role: group.roleKey || group.key, size: option.sizeLabel, axes: option.axes, context, match});
  }
  return {ctx, cases};
}
function product(handle) { return copy(fixtures.find(p => p.handle === handle)); }
function choose(result, role, type, size) {
  const found = result.cases.find(c => c.role === role && c.axes.Type === type && c.size === size);
  assert.ok(found, `${role}/${type}/${size}`);
  return found.match;
}
function fields(match) {
  assert.ok(match);
  return Object.fromEntries(Array.from(match.headers).slice(1).map((header, i) => [header.raw || header.label, match.row[i + 1]]));
}

test('source-backed typed charts cover every intended variant and preserve controls', () => {
  const expected = {
    'fresh-blue-plaid-family-matching-set': 25,
    'red-resort-mommy-and-me-set': 10,
    'golden-daisy-mommy-and-me-set': 21,
    'ivory-cascade-mommy-and-me-set': 11,
    'rainbow-stripe-family-matching-set': 12,
    'geometric-blue-family-matching-set': 11,
  };
  for (const [handle, count] of Object.entries(expected)) {
    const result = matches(product(handle), afterHarness);
    assert.equal(result.cases.filter(c => c.match).length, count, handle);
  }
  assert.equal(JSON.stringify(fixtures), originalFixtureBytes);
});

test('Golden Daisy keeps exact prefixed measurements and rejects unqualified garment measurements', () => {
  const fixture = product('golden-daisy-mommy-and-me-set');
  fixture.tables[0].headers.push('Waist (cm)', 'Hip (cm)', 'Garment Length (cm)');
  fixture.tables[0].rows.forEach(r => r.push('999', '888', '777'));
  const result = matches(fixture, afterHarness);
  const top = fields(choose(result, 'girl', 'Top', '2 Years'));
  const pants = fields(choose(result, 'girl', 'Pants', '2 Years'));
  assert.equal(top['Top Chest/Bust (cm)'], '67');
  assert.equal(top['Top Length (cm)'], '37');
  assert.equal(top['Top Hip (cm)'], '71');
  assert.equal(top['Top Waist (cm)'], '67');
  assert.equal(pants['Pants Length (cm)'], '46');
  assert.equal(pants['Pants Waist (cm)'], '42');
  assert.ok(!Object.keys(top).some(k => /pants/i.test(k)));
  assert.ok(!Object.keys(pants).some(k => /top/i.test(k)));
  for (const values of [top, pants]) {
    assert.ok(!Object.values(values).some(v => ['999', '888', '777'].includes(v)));
  }
  const youngest = fields(choose(result, 'girl', 'Pants', '1-2 Years'));
  assert.equal(youngest['Pants Length (cm)'], '42');
  assert.equal(youngest['Pants Waist (cm)'], '40');
  const girl = result.ctx.roleGroupsCache.find(g => (g.roleKey || g.key) === 'girl');
  const sample = girl.options.find(o => o.axes.Type === 'Top');
  const synthetic = {...sample, sizeLabel: '1-2 Years', fullLabel: 'Girl 1-2 Years'};
  assert.equal(result.ctx.findMeasurementsForOption(girl, synthetic, {garmentKey: 'top', ambiguous: false}), null,
    'guidance without any Top metric does not become Top measurements');
});

test('composite sets retain their complete original measurement rows', () => {
  for (const [handle, role, type, size] of [
    ['fresh-blue-plaid-family-matching-set', 'girl', 'Top & Skirt Set', '1-2 Years'],
    ['red-resort-mommy-and-me-set', 'girl', 'Two-Piece Set', '4 Years'],
  ]) {
    const fixture = product(handle), result = matches(fixture, afterHarness);
    const match = choose(result, role, type, size);
    const table = fixture.tables[0];
    const original = table.rows.find(row => row[0] === 'Child ' + size);
    const expected = Object.fromEntries(table.headers.slice(1).map((h, i) => [h, original[i + 1]])
      .filter(([, value]) => value && !/^[—–-]+$/.test(value)));
    assert.deepEqual(fields(match), expected, handle);
  }
});

test('exact garment, size, role, selected type, and conflicting-row guards remain in force', () => {
  const fresh = product('fresh-blue-plaid-family-matching-set');
  const result = matches(fresh, afterHarness), ctx = result.ctx;
  const girl = ctx.roleGroupsCache.find(g => (g.roleKey || g.key) === 'girl');
  const sample = girl.options.find(o => o.axes.Type === 'Top & Skirt Set');
  assert.equal(ctx.findMeasurementsForOption(girl, sample, {garmentKey: 'topSkirtSet', ambiguous: true}), null);
  assert.equal(ctx.findMeasurementsForOption(girl, {...sample, sizeLabel: '17 Years', fullLabel: 'Girl 17 Years'}, {garmentKey: 'topSkirtSet'}), null);
  assert.equal(ctx.findMeasurementsForOption({roleKey: 'father', key: 'father'}, sample, {garmentKey: 'topSkirtSet'}), null);
  assert.equal(ctx.findMeasurementsForOption(girl, sample, {garmentKey: 'pants'}), null);

  const conflicting = copy(fresh.tables[0]);
  conflicting.id = 'size-chart-copy';
  conflicting.rows[0][4] = '999 cm / 393.3 in';
  fresh.tables.push(conflicting);
  assert.equal(choose(matches(fresh, afterHarness), 'girl', 'Top & Skirt Set', '1-2 Years'), null);

  const mismatched = product('fresh-blue-plaid-family-matching-set');
  mismatched.tables[0].heading = 'Size Chart — Top & Pants Set';
  assert.equal(choose(matches(mismatched, afterHarness), 'girl', 'Top & Skirt Set', '1-2 Years'), null);

  const two = product('red-resort-mommy-and-me-set');
  two.tables.push(copy(two.tables[0]));
  assert.equal(choose(matches(two, afterHarness), 'girl', 'Two-Piece Set', '4 Years'), null);

  const wrong = matches(product('rainbow-stripe-family-matching-set'), afterHarness);
  assert.ok(wrong.cases.filter(c => c.context.garmentKey === 'shorts').every(c => !c.match),
    'standalone Shirt chart must not become Shorts');
});

test('explicit Top/Pants split rejects headers naming both components', () => {
  const fixture = product('golden-daisy-mommy-and-me-set');
  fixture.tables[0].headers.push('Top/Pants Length (cm)');
  fixture.tables[0].rows.forEach(row => row.push('777'));
  const result = matches(fixture, afterHarness);
  assert.equal(result.cases.filter(c => c.match).length, 21);
  for (const c of result.cases) {
    const values = fields(c.match);
    assert.ok(!Object.keys(values).some(k => /top\/pants/i.test(k)));
    assert.ok(!Object.values(values).includes('777'));
  }
});

test('Top and Skirt complete set rejects garment headers outside its components', () => {
  const fixture = product('fresh-blue-plaid-family-matching-set');
  fixture.tables[0].headers.push('Cardigan Length (cm)', 'Top/Cardigan Length (cm)');
  fixture.tables[0].rows.forEach(row => row.push('888', '889'));
  const result = matches(fixture, afterHarness);
  assert.equal(result.cases.filter(c => c.match).length, 25);
  for (const c of result.cases.filter(c => c.axes.Type === 'Top & Skirt Set')) {
    const values = fields(c.match);
    assert.ok(!Object.keys(values).some(k => /cardigan/i.test(k)));
    assert.ok(!Object.values(values).some(value => value === '888' || value === '889'));
  }
  const child = fields(choose(result, 'girl', 'Top & Skirt Set', '1-2 Years'));
  assert.equal(child['Skirt Length (cm/in)'], '23.5 cm / 9.3 in');
  assert.equal(child['Garment Length (cm/in)'], '32 cm / 12.6 in');
});

test('new typed entries reject adult qualifiers and combined sizes without exact source labels', () => {
  const result = matches(product('fresh-blue-plaid-family-matching-set'), afterHarness);
  const group = result.ctx.roleGroupsCache.find(g => (g.roleKey || g.key) === 'mother');
  const option = group.options.find(o => o.axes.Type === 'Top & Skirt Set' && o.sizeLabel === 'S');
  assert.ok(option);
  for (const size of ['S/M', 'S Tall']) {
    const altered = {...option, sizeLabel: size, fullLabel: 'Mother ' + size};
    assert.equal(result.ctx.findMeasurementsForOption(group, altered, {garmentKey: 'topSkirtSet'}), null, size);
  }
});
