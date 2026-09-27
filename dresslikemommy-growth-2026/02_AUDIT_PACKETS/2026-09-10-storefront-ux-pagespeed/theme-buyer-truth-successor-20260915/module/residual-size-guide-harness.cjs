const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const fixtures = JSON.parse(fs.readFileSync(path.join(__dirname, 'residual-size-guide-fixtures.json')));
const repo = path.resolve(__dirname, '../../../../..');
const harnessPath = path.join(__dirname, 'buyer-truth.test.cjs');
let prefix = fs.readFileSync(harnessPath, 'utf8').split("for (const locale of ['en', 'fr', 'ar']) {")[0];
const sourceLine = "const source = fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');";
assert.ok(prefix.includes(sourceLine));
prefix = prefix.replace(sourceLine, 'const source = providedSource;');
prefix = prefix.replace('privateNames.map(name => declaration(name))', "privateNames.filter(name => source.includes('function ' + name + '(')).map(name => declaration(name))");
function harness() {
 const source = fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
 const sandbox = {require, console, __dirname: path.dirname(harnessPath), providedSource: source};
 vm.runInNewContext(prefix + '\nthis.production = {environment, tableDom, declaration};', sandbox);
 sandbox.production.isCandidate = source.includes('function indexExactSourceMeasurementRows(');
 return sandbox.production;
}
const production = harness();
const copy = value => JSON.parse(JSON.stringify(value));
function environment(product) {
 const tables = product.tables.map(t => production.tableDom(t, t.heading));
 const env = production.environment('en', tables);
 if (production.isCandidate) vm.runInContext(production.declaration('indexExactSourceMeasurementRows'), env.ctx);
 if (typeof env.ctx.getExactCompoundChartScope === 'function') vm.runInContext(production.declaration('indexExactCompoundMeasurementRows'), env.ctx);
 if (typeof env.ctx.isExactGenericRoleChart === 'function') vm.runInContext(production.declaration('indexExactGenericRoleMeasurementRows'), env.ctx);
 env.ctx.productData = {options: product.options, variants: product.variants.map(v => ({...v, available: true, price: Math.round(Number(v.price) * 100)}))};
 env.ctx.roleGroupsCache = env.ctx.buildRoleGroups(env.ctx.productData, {}, true, {skipTypeFilter: true});
 return env;
}
function matches(product) {
 const {ctx} = environment(product), cases = [];
 for (const group of ctx.roleGroupsCache) for (const option of group.options) {
  const inst = {roleKey: group.roleKey || group.key, groupKey: group.key, axisSelections: option.axes || {}, sizeLabel: option.sizeLabel};
  const context = ctx.getMeasurementContextForInstance(group, inst, option);
  const originalContext = JSON.stringify(context);
  const match = ctx.findMeasurementsForOption(group, option, context);
  assert.equal(JSON.stringify(context), originalContext, 'measurement lookup must preserve the fit selection context');
  cases.push({role: group.roleKey || group.key, size: option.sizeLabel, axes: option.axes, context, match, group, option});
 }
 return {ctx, cases, product};
}
function product(handle) { const p = fixtures.find(p => p.handle === handle); assert.ok(p, handle); return copy(p); }
function choose(result, role, axisValue, size) {
 const found = result.cases.find(c => c.role === role && Object.values(c.axes).includes(axisValue) && c.size === size);
 assert.ok(found, `${role}/${axisValue}/${size}`); return found;
}
function fields(match) {
 assert.ok(match);
 return Object.fromEntries(Array.from(match.headers).slice(1).map((header, i) => [header.raw || header.label, match.row[i + 1]]));
}
// Every retained field must be an unchanged cell from one complete source row.
// Do not combine values across different source rows to satisfy the assertion.
function assertSourceValues(result) {
 for (const c of result.cases.filter(c => c.match)) {
  const values = fields(c.match);
  const tables = c.match.sourceTable && c.match.sourceTable.record ? [c.match.sourceTable.record] : result.product.tables;
  assert.ok(tables.some(table => table.rows.some(row => Object.entries(values).every(([header, value]) => {
   const index = table.headers.indexOf(header);
   return index >= 0 && row[index] === value;
  }))), result.product.handle + '/' + c.role + '/' + c.size + ': all fields belong to one source row');
 }
}
module.exports = {assert, fixtures, copy, environment, matches, product, choose, fields, assertSourceValues};
