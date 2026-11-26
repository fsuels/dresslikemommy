import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const liquid = readFileSync(new URL('../../sections/main-product.liquid', import.meta.url), 'utf8');

function extract(name, nextName) {
  const start = liquid.indexOf(`function ${name}(`);
  const end = liquid.indexOf(`function ${nextName}(`, start);
  assert.ok(start > 0 && end > start, `${name} found`);
  return liquid.slice(start, end);
}

function covers(controlRects, { height = 812, width = 375, bar = 68 } = {}) {
  const mediaContainer = {
    querySelectorAll: () => controlRects.map((r) => ({ getBoundingClientRect: () => ({ width: 30, height: 30, ...r }) })),
  };
  const context = { mediaContainer, sticky: { offsetHeight: bar }, window: { innerHeight: height, innerWidth: width }, document: { documentElement: {} } };
  vm.runInNewContext(`${extract('stickyCoversGalleryControls', 'toggleStickyVisibility')}; result = stickyCoversGalleryControls();`, context);
  return context.result;
}

test('first screen at 375x812: counter ends at y=736, bar starts at 744, so the bar shows', () => {
  assert.equal(covers([{ left: 299, right: 367, top: 710, bottom: 736 }, { left: 8, right: 44, top: 420, bottom: 456 }]), false);
});

test('a counter under the bar keeps the bar hidden', () => {
  assert.equal(covers([{ left: 299, right: 367, top: 760, bottom: 786 }]), true);
});

test('controls of other slides (off to the side) and collapsed controls are ignored', () => {
  assert.equal(covers([{ left: 706, right: 737, top: 770, bottom: 801 }, { left: 10, right: 40, top: 770, bottom: 800, width: 0, height: 0 }]), false);
});

test('the bar condition no longer depends on the gallery being scrolled past, and stays off for desktop', () => {
  const toggle = extract('toggleStickyVisibility', 'getOptionNameFromGroup');
  assert.doesNotMatch(toggle, /mediaIsInViewport/);
  assert.match(toggle, /mobileMedia\.matches/);
  assert.match(toggle, /!atcIsInViewport/);
});

test('two prices are split on the middle dot into stacked lines', () => {
  const fn = extract('setStickyPriceText', 'syncStickyPrice');
  const made = [];
  const stickyPrice = {
    textContent: '',
    children: [],
    classList: { toggle(name, on) { this.on = on; } },
    appendChild(node) { this.children.push(node.textContent); },
  };
  const context = {
    stickyPrice,
    document: { createElement: () => { const n = { className: '', textContent: '' }; made.push(n); return n; } },
  };
  vm.runInNewContext(`${fn}; setStickyPriceText('Kids from $37.99 · Adults from $49.99');`, context);
  assert.deepEqual(stickyPrice.children, ['Kids from $37.99', 'Adults from $49.99']);
  assert.equal(stickyPrice.classList.on, true);
  vm.runInNewContext(`${fn}; setStickyPriceText('$49.99');`, context);
  assert.equal(stickyPrice.textContent, '$49.99');
  assert.equal(stickyPrice.classList.on, false);
});
