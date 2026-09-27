const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'native-size-guide-fixture.json')));
const repo = path.resolve(__dirname, '../../../../..');
const harnessPath = path.join(__dirname, 'buyer-truth.test.cjs');
const sourceLine = "const source = fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');";
const prefix = fs.readFileSync(harnessPath, 'utf8').split("for (const locale of ['en', 'fr', 'ar']) {")[0].replace(sourceLine, 'const source = providedSource;');
const clone = value => JSON.parse(JSON.stringify(value));

class Node {
  constructor(tag = 'span', attrs = {}) { this.tagName = tag.toUpperCase(); this.attrs = {...attrs}; this.children = []; this.listeners = {}; this.style = {}; this.textContent = ''; this.innerHTML = ''; }
  getAttribute(name) { return Object.hasOwn(this.attrs, name) ? this.attrs[name] : null; }
  setAttribute(name, value) { this.attrs[name] = String(value); }
  removeAttribute(name) { delete this.attrs[name]; }
  hasAttribute(name) { return Object.hasOwn(this.attrs, name); }
  appendChild(child) { this.children.push(child); child.parent = this; return child; }
  remove() { if (this.parent) this.parent.children = this.parent.children.filter(child => child !== this); }
  querySelector(selector) { const match = selector.match(/^\[([^\]]+)\]$/); return match ? this.children.find(child => child.hasAttribute(match[1])) || null : null; }
  addEventListener(name, handler) { (this.listeners[name] ||= []).push(handler); }
  getBoundingClientRect() { return {left: this.left || 20, width: this.tagName === 'LABEL' ? 100 : 240}; }
}
class Snapshot extends Node {
  set innerHTML(value) {
    this.html = value; this.nodes = {};
    if (!value || !value.includes('data-matching-size-guide-metrics-toggle')) return;
    this.nodes['[data-matching-size-guide-metrics-toggle]'] = new Node('button', {'aria-expanded': value.match(/aria-expanded="([^"]+)"/)[1]});
    this.nodes['[data-matching-size-guide-metrics]'] = new Node('div', /data-matching-size-guide-metrics hidden/.test(value) ? {hidden: 'hidden'} : {});
    const label = new Node(); label.textContent = value.match(/data-matching-size-guide-metrics-toggle-label>([^<]+)/)[1];
    this.nodes['[data-matching-size-guide-metrics-toggle-label]'] = label;
  }
  get innerHTML() { return this.html; }
  querySelector(selector) { return this.nodes[selector] || null; }
}

function load() {
  const source = fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
  const css = fs.readFileSync(path.join(repo, 'assets/component-product-desktop-ux-ruler-sync.css'), 'utf8');
  const sandbox = {require, console, __dirname: path.dirname(harnessPath), providedSource: source};
  vm.runInNewContext(prefix + '\nthis.production={environment,tableDom,declaration};', sandbox);
  return {...sandbox.production, source, css};
}
function environment(record = clone(fixture)) {
  const production = load();
  const tables = record.tables.map(table => production.tableDom(table, table.heading));
  const env = production.environment('en', tables), ctx = env.ctx;
  const extra = ['getCurrentVariantSelects', 'getCurrentSizeSelect', 'findSizeGuideSelect', 'normalizeNativeGuideSizeLabel',
    'getNativeRadioGuideContext', 'getNativeRadioGuideState', 'getNativeRadioStateForInput', 'getNativeRadioGuideRow',
    'syncNativeSizeGuideTooltips', 'getSelectedSizeState', 'getGuideRowEntries', 'getSelectedGuideRowEntry',
    'getSelectedGuideMatch', 'getSelectedGuideRowLabel', 'formatSelectedGuideDisplay', 'renderSelectedGuideSnapshot'];
  vm.runInContext(extra.filter(name => new RegExp('function ' + name + '\\(').test(production.source)).map(name => production.declaration(name)).join('\n'), ctx);
  const productData = {options: clone(record.options), variants: record.variants.map(v => ({...v, available: v.available !== false, price: Math.round(Number(v.price) * 100)}))};
  const sizeIndex = productData.options.findIndex(option => option.name === 'Size');
  const inputs = record.variants.map((variant, index) => {
    const label = new Node('label', {for: 'native-size-' + index, class: 'existing-class'});
    label.textContent = String(variant['option' + (sizeIndex + 1)] || '');
    const input = {id: 'native-size-' + index, value: label.textContent, checked: index === 0, disabled: false,
      attrs: {name: 'Size', form: 'product-form-fixture', type: 'radio', 'aria-label': 'existing-' + index}, nextElementSibling: label,
      getAttribute(name) { return Object.hasOwn(this.attrs, name) ? this.attrs[name] : null; },
      setAttribute() { throw new Error('Native radio attributes must not be written'); },
      removeAttribute() { throw new Error('Native radio attributes must not be removed'); },
      dispatchEvent() { throw new Error('Native radio events must not be synthesized'); }};
    return input;
  });
  const color = {id: 'native-color', value: 'white', checked: true, disabled: false, attrs: {name: 'Color', type: 'radio'}, getAttribute(name) { return this.attrs[name] || null; }, nextElementSibling: new Node('label', {for: 'native-color'})};
  const picker = {querySelectorAll(selector) {
    assert.ok(['input[type="radio"]', 'input[type="radio"]:checked'].includes(selector));
    const all = inputs.concat(color); return selector.endsWith(':checked') ? all.filter(input => input.checked) : all;
  }};
  const snapshot = new Snapshot('div', {hidden: 'hidden'});
  ctx.document.getElementById = id => id === 'variant-selects-fixture' ? picker : null;
  ctx.document.createElement = tag => new Node(tag);
  ctx.window.innerWidth = 1024;
  Object.assign(ctx, {productData, productHandle: record.handle, selectedUnitSystem: 'metric', snapshot,
    snapshotLabel: 'Your size details', compareHintLabel: 'Compare the original chart', unitToggleLabel: 'Size chart units',
    groups: [], parsed: tables.length ? ctx.parseSizeGuideTable(tables[0]) : null,
    sizeGuideRoot: {querySelectorAll() { return []; }, querySelector() { return null; }}});
  function select(value) { inputs.forEach(input => { input.checked = input.value === value; }); }
  function state() { return ctx.getSelectedSizeState(); }
  function render() { const selected = state(); const match = ctx.getSelectedGuideMatch(selected); ctx.renderSelectedGuideSnapshot(match, selected); return {selected, match, html: snapshot.innerHTML}; }
  return {...env, production, record, ctx, inputs, picker, snapshot, select, state, render};
}
module.exports = {fixture, clone, environment, load};
