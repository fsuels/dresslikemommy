const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {clone, environment} = require('./native-size-guide-harness.cjs');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'native-size-guide-lavender-fixture.json'), 'utf8'));

test('reviewed Lavender source matches all nine native sizes with unchanged measurements', () => {
  const record = clone(fixture), original = JSON.stringify(record), env = environment(record);
  let matched = 0;
  for (const input of env.inputs) {
    env.select(input.value);
    const result = env.render(), label = input.value.replace(/cm$/, '');
    const row = fixture.tables[0].rows.find(row => row[0] === label);
    assert.ok(result.match, input.value); matched++;
    assert.deepEqual(Array.from(result.match.row), row);
    assert.equal(result.selected.rawValue, input.value);
    assert.ok(result.html.includes(input.value));
  }
  assert.equal(matched, 9); assert.equal(JSON.stringify(record), original);
  env.select('100cm'); env.ctx.selectedUnitSystem = 'imperial';
  assert.ok(env.render().html.includes('>24.8</strong>'));
  env.ctx.syncNativeSizeGuideTooltips();
  assert.equal(env.inputs.filter(input => input.nextElementSibling.querySelector('[data-native-size-tooltip]')).length, 9);
});

test('Lavender centimeter alias does not broaden to other handles, sizes, roles or qualifiers', () => {
  const other = clone(fixture); other.handle = 'another-product';
  let env = environment(other), count = 0;
  for (const input of env.inputs) { env.select(input.value); if (env.render().match) count++; }
  assert.equal(count, 3, 'only the literal adult rows remain matched on another product');
  for (const size of ['90cm', '101cm', '105cm', '160cm', '100 cm', '100-110cm', 'Child 100cm', 'Mother 100cm', '100cm Tall', '100cm Extended']) {
    const record = clone(fixture); record.variants[0].option1 = size;
    env = environment(record); env.select(size); assert.equal(env.render().match, null, size);
  }
  for (const sourceLabel of ['100 Tall', 'Child 100', '100-110', '100 cm']) {
    const record = clone(fixture); record.tables[0].rows.find(row => row[0] === '100')[0] = sourceLabel;
    env = environment(record); env.select('100cm'); assert.equal(env.render().match, null, sourceLabel);
  }
});

test('Lavender numeric alias requires one explicit source cm height interval containing that exact size', () => {
  for (const mode of ['no-unit', 'unknown-unit', 'wrong-range', 'reversed-range', 'no-range', 'empty-range', 'wrong-parts', 'two-height-columns']) {
    const record = clone(fixture), table = record.tables[0], row = table.rows.find(row => row[0] === '100');
    if (mode === 'no-unit') table.headers[3] = 'Height';
    if (mode === 'unknown-unit') table.headers[3] = 'Height (unknown/in)';
    if (mode === 'wrong-range') row[3] = '105-115 / 41.3-45.3';
    if (mode === 'reversed-range') row[3] = '105-95 / 41.3-37.4';
    if (mode === 'no-range') row[3] = '100 / 39.4';
    if (mode === 'empty-range') row[3] = '—';
    if (mode === 'wrong-parts') row[3] = '95-105';
    if (mode === 'two-height-columns') { table.headers.push('Height (cm/in)'); table.rows.forEach(row => row.push(row[3])); }
    const env = environment(record); env.select('100cm'); assert.equal(env.render().match, null, mode);
  }
});

test('Lavender canonicalized duplicate source rows remain ambiguous even when values agree', () => {
  for (const conflict of [false, true]) {
    const record = clone(fixture), row = clone(record.tables[0].rows.find(row => row[0] === '100'));
    row[0] = '100cm'; if (conflict) row[1] = '999 / 393.3';
    record.tables[0].rows.push(row);
    const env = environment(record); env.select('100cm'); assert.equal(env.render().match, null);
  }
});
