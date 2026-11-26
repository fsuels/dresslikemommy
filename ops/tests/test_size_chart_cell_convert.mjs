import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../assets/product-desktop-ux-20260513-ruler-sync.js', import.meta.url), 'utf8');
const start = source.indexOf('function convertMetricChartCell');
const end = source.indexOf('function isEmptyChartCell');
const ctx = {};
vm.runInNewContext(source.slice(start, end) + '\nthis.f = convertMetricChartCell;', ctx);
const f = ctx.f;

test('cm values and ranges', () => {
  assert.equal(f('70 cm', 'cm'), '27.6 in');
  assert.equal(f('42–60 cm', 'cm'), '16.5–23.6 in');
  assert.equal(f('86', 'cm'), '33.9');
});
test('decimal comma is kept', () => {
  assert.equal(f('61,5 cm', 'cm'), '24,2 in');
});
test('kg to lbs', () => {
  assert.equal(f('10-15 kg', 'kg'), '22-33.1 lbs');
});
test('unrecognised cells fail safe', () => {
  assert.equal(f('S/M', 'cm'), null);
  assert.equal(f('70 cm / 27 in', 'cm'), null);
  assert.equal(f('70 kg', 'cm'), null);
});
