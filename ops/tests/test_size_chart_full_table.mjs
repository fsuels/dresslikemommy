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

// Ranges in every converter: "-", en dash, em dash, "to", unit suffixes, decimal commas.
function extractFn(name) {
  const m = src.match(new RegExp('^( *)function ' + name + '\\(', 'm'));
  assert.ok(m, name + ' exists');
  const from = m.index;
  const close = src.indexOf('\n' + m[1] + '}\n', from);
  return src.slice(from, close + m[1].length + 3);
}
const rctx = { normalizeText: (v) => String(v || '').trim().toLowerCase() };
vm.runInNewContext(
  ['roundMeasurement', 'convertRangeValue', 'normalizeGuideUnit', 'formatGuideNumericValue', 'convertGuideValueBetweenUnits', 'stripGuideTrailingUnit', 'convertGuideCellText'].map(extractFn).join('\n'),
  rctx
);

test('convertRangeValue converts both ends of every range style', () => {
  assert.equal(rctx.convertRangeValue('80–90', 'cm', 'in'), '31.5–35.4');
  assert.equal(rctx.convertRangeValue('80—90', 'cm', 'in'), '31.5—35.4');
  assert.equal(rctx.convertRangeValue('80-90', 'cm', 'in'), '31.5-35.4');
  assert.equal(rctx.convertRangeValue('80 to 90', 'cm', 'in'), '31.5 to 35.4');
  assert.equal(rctx.convertRangeValue('9–12.5 kg', 'kg', 'lbs'), '19.8–27.6');
  assert.equal(rctx.convertRangeValue('7,5', 'kg', 'lbs'), '16.5');
  assert.equal(rctx.convertRangeValue('7,5–9,5 kg', 'kg', 'lbs'), '16.5–20.9');
  assert.equal(rctx.convertRangeValue('Adult', 'cm', 'in'), null);
});

test('guide table cells convert ranges with em dash, "to" and decimal commas', () => {
  assert.equal(rctx.convertGuideCellText('80–90', 'cm', 'in'), '31.5–35.4');
  assert.equal(rctx.convertGuideCellText('80—90 cm', 'cm', 'in'), '31.5—35.4');
  assert.equal(rctx.convertGuideCellText('40 to 50', 'kg', 'lbs'), '88.2 to 110.2');
  assert.equal(rctx.convertGuideCellText('7,5 kg', 'kg', 'lbs'), '16.5');
});

test('full chart cells convert em dash, "to" and decimal commas', () => {
  assert.equal(ctx.convertMetricChartCell('80—90 cm', 'cm'), '31.5—35.4 in');
  assert.equal(ctx.convertMetricChartCell('80 to 90', 'cm'), '31.5 to 35.4');
  assert.equal(ctx.convertMetricChartCell('7,5 kg', 'kg'), '16.5 lbs');
  assert.equal(ctx.convertMetricChartCell('9–12,5 kg', 'kg'), '19.8–27.6 lbs');
});

test('age cells such as "6-12 mo" use the storefront language word for months', () => {
  const labels = src.slice(src.indexOf('var SIZE_UNIT_LABELS_BY_LOCALE = {'), src.indexOf('var UI_LABELS_BY_LOCALE'));
  const run = (lang) => {
    const c = { document: { documentElement: { lang, getAttribute: () => lang } }, normalizeText: (v) => String(v || '').trim().toLowerCase() };
    vm.runInNewContext([labels, extractFn('getLocaleRoot'), extractFn('getLocaleMap'), extractFn('localizeMonthAbbreviation')].join('\n'), c);
    return c.localizeMonthAbbreviation;
  };
  assert.equal(run('es')('6-12 mo'), '6-12 meses');
  assert.equal(run('de')('6-12 mo'), '6-12 Monate');
  assert.equal(run('fr')('6-12 mo'), '6-12 mois');
  assert.equal(run('ja')('6-12 mo'), '6-12か月');
  assert.equal(run('en')('6-12 mo'), '6-12 mo');
  assert.equal(run('es')('2-3'), '2-3');
  assert.equal(run('es')('9-12.5 kg'), '9-12.5 kg');
});
