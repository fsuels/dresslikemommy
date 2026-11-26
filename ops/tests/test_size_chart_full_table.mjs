import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const src = readFileSync(path.join(repo, 'assets', 'product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
const start = src.indexOf('function convertMetricChartCell');
const end = src.indexOf('// Adds a cm/in switch to a copied chart');
const ctx = {};
vm.runInNewContext(src.slice(start, end), ctx);

test('converts cm and kg values, ranges and suffixed values', () => {
  assert.equal(ctx.convertMetricChartCell('68 cm', 'cm'), '26.8 in');
  assert.equal(ctx.convertMetricChartCell('80–90 cm', 'cm'), '31.5–35.4 in');
  assert.equal(ctx.convertMetricChartCell('104', 'cm'), '40.9');
  assert.equal(ctx.convertMetricChartCell('9–12.5 kg', 'kg'), '19.8–27.6 lbs');
  assert.equal(ctx.convertMetricChartCell('40-50', 'kg'), '88.2-110.2');
});

test('refuses text it cannot convert reliably', () => {
  assert.equal(ctx.convertMetricChartCell('One size', 'cm'), null);
  assert.equal(ctx.convertMetricChartCell('68 kg', 'cm'), null);
  assert.equal(ctx.convertMetricChartCell('30 in', 'cm'), null);
});

test('detects empty cells', () => {
  for (const v of ['-', '', ' ', '–', '—']) assert.ok(ctx.isEmptyChartCell(v));
  assert.ok(!ctx.isEmptyChartCell('0'));
  assert.ok(!ctx.isEmptyChartCell('39 cm'));
});

test('removes columns that are empty in every body row but keeps real ones', () => {
  const mkRow = (vals) => {
    const row = { children: vals.map((v) => ({ textContent: v })) };
    row.removeChild = (c) => { row.children.splice(row.children.indexOf(c), 1); };
    return row;
  };
  const rows = [mkRow(['Size', 'Hip (cm)', 'Bust (cm)', 'Waist (cm)']), mkRow(['S', '-', '90 cm', '']), mkRow(['M', '-', '94 cm', '-'])];
  ctx.removeEmptyChartColumns({ querySelectorAll: () => rows });
  assert.deepEqual(rows.map((r) => r.children.map((c) => c.textContent)), [['Size', 'Bust (cm)'], ['S', '90 cm'], ['M', '94 cm']]);
});
