import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../assets/dlm-size-chart-link.js', import.meta.url), 'utf8');

function el() {
  const attrs = new Map();
  const node = {
    children: [], className: '', textContent: '', nextElementSibling: null,
    setAttribute(k, v) { attrs.set(k, String(v)); },
    getAttribute: (k) => (attrs.has(k) ? attrs.get(k) : null),
    hasAttribute: (k) => attrs.has(k),
    appendChild(c) { this.children.push(c); c.parentNode = this; },
  };
  node.classList = { add(c) { node.className += ' ' + c; } };
  return node;
}

test('ruler icon gets a translated visible label and one helper line under the first size row (Spanish fixture)', () => {
  const icon = el();
  icon.setAttribute('aria-label', 'Ver talla de Adultos');
  const row = el();
  const parent = el();
  row.parentNode = parent;
  parent.insertBefore = (node) => { row.nextElementSibling = node; node.parentNode = parent; };
  const wrapper = el();
  wrapper.setAttribute('data-size-chart-icon-label', 'Tabla de tallas');
  wrapper.setAttribute('data-size-guide-compare-hint', 'Abre la tabla completa más abajo.');
  const card = el();
  card.closest = () => wrapper;
  card.querySelector = (s) => (s === '[data-pdp-fit-inline-trigger]' ? icon : s === '.product-matching-set__size-row' ? row : null);
  const document = {
    readyState: 'complete',
    querySelector: (s) => (s === '[data-dlm-size-helper]' ? row.nextElementSibling : wrapper),
    querySelectorAll: (s) => (s === '.product-matching-set' ? [{}] : s === '[data-instance-card]' ? [card] : []),
    createElement: () => el(),
    addEventListener() {},
  };
  const ctx = { document, MutationObserver: undefined };
  ctx.window = ctx;
  vm.runInNewContext(source, ctx);
  assert.equal(icon.children.length, 1);
  assert.equal(icon.children[0].textContent, 'Tabla de tallas');
  assert.equal(icon.getAttribute('aria-label'), 'Tabla de tallas: Ver talla de Adultos');
  assert.equal(row.nextElementSibling.textContent, 'Abre la tabla completa más abajo.');
  vm.runInNewContext(source, ctx);
  assert.equal(icon.children.length, 1, 'a second scan adds nothing');
});
