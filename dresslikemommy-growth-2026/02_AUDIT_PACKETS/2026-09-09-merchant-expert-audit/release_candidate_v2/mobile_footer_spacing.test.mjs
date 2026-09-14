import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire('/tmp/dlm-merchant-landing-validation-20260909/package.json');
const { JSDOM } = require('jsdom');
const root = path.dirname(fileURLToPath(import.meta.url));
const filename = 'assets/theme-inline-body-static-04.css';
const before = fs.readFileSync(path.join(root, 'baseline', filename), 'utf8');
const candidate = fs.readFileSync(path.join(root, 'theme', filename), 'utf8');
const oldSelector = 'body.template-product.sticky-mobile-atc-visible';
const newSelector = 'body.sticky-mobile-atc-visible';
const geometry = JSON.parse(fs.readFileSync(path.join(root, 'before_geometry.json'), 'utf8'));
function spacingRule(css) {
  const dom = new JSDOM(`<style>${css}</style>`);
  const matches = [];
  for (const rule of dom.window.document.styleSheets[0].cssRules) {
    if (!rule.cssRules) continue;
    for (const inner of rule.cssRules) {
      if (inner.selectorText?.includes('sticky-mobile-atc-visible')) matches.push({ media: rule.conditionText, selector: inner.selectorText, padding: inner.style.getPropertyValue('padding-bottom') });
    }
  }
  dom.window.close();
  assert.equal(matches.length, 1);
  return matches[0];
}

test('exactly one obsolete selector qualifier is removed; all declarations remain unchanged', () => {
  assert.equal(before.split(oldSelector).length - 1, 1);
  assert.equal(candidate, before.replace(oldSelector, newSelector));
  assert.equal(candidate.length, before.length - '.template-product'.length);
});

test('the actual reported body matches the amendment and reproduces the old mismatch', () => {
  const dom = new JSDOM(`<body class="${geometry.body_class}"></body>`);
  try {
    const body = dom.window.document.body;
    assert.equal(body.matches(oldSelector), false);
    assert.equal(body.matches(newSelector), true);
    body.classList.remove('sticky-mobile-atc-visible');
    assert.equal(body.matches(newSelector), false);
    body.className = 'template-product sticky-mobile-atc-visible';
    assert.equal(body.matches(oldSelector), true);
    assert.equal(body.matches(newSelector), true);
  } finally { dom.window.close(); }
});

test('CSS parses and preserves the existing749px mobile boundary and safe-area expression', () => {
  const old = spacingRule(before);
  const changed = spacingRule(candidate);
  assert.equal(old.media, 'screen and (max-width: 749px)');
  assert.equal(changed.media, old.media);
  assert.equal(changed.padding, old.padding);
  assert.equal(changed.padding, 'calc(var(--sticky-mobile-atc-offset, 8.8rem) + env(safe-area-inset-bottom))');
  assert.equal(changed.selector, newSelector);
  const maximum = Number(changed.media.match(/max-width:\s*(\d+)px/)[1]);
  for (const width of [320, 390, 749]) assert.ok(width <= maximum);
  for (const width of [750, 1024, 1440]) assert.ok(width > maximum);
});

test('existing unmodified JS supplies measured heights and removes spacing state when hidden', () => {
  const source = fs.readFileSync(path.resolve(root, '../release_candidate/theme/sections/main-product.liquid'), 'utf8');
  const start = source.indexOf('      function syncBodyOffset(isVisible) {');
  const end = source.indexOf('      function toggleStickyVisibility()', start);
  assert.ok(start >= 0 && end > start);
  const dom = new JSDOM('<body class="gradient animate--hover-default"></body>', { runScripts: 'outside-only' });
  try {
    dom.window.sticky = { offsetHeight: 80 };
    dom.window.eval(source.slice(start, end));
    for (const height of [80, 114, 148]) {
      dom.window.sticky.offsetHeight = height;
      dom.window.syncBodyOffset(true);
      assert.equal(dom.window.document.body.style.getPropertyValue('--sticky-mobile-atc-offset'), `${height}px`);
      assert.equal(dom.window.document.body.matches(newSelector), true);
    }
    dom.window.syncBodyOffset(false);
    assert.equal(dom.window.document.body.style.getPropertyValue('--sticky-mobile-atc-offset'), '');
    assert.equal(dom.window.document.body.matches(newSelector), false);
  } finally { dom.window.close(); }
});

test('root geometry predicts full reachability with measured bar height and safe-area clearance', () => {
  // Arithmetic against parent-provided geometry, not a browser layout test.
  assert.equal(geometry.cookie_button.bottom > geometry.sticky.top, true);
  for (const [barHeight, safeArea] of [[80, 0], [114, 34], [148, 34]]) {
    const padding = barHeight + safeArea;
    const expectedCookieBottomAtMaxScroll = geometry.cookie_button.bottom - padding;
    const stickyTop = geometry.viewport.height - barHeight;
    assert.ok(expectedCookieBottomAtMaxScroll < stickyTop);
  }
  assert.equal(geometry.cookie_button.bottom - 80, 724.17);
});

test('the mobile rule does not introduce a desktop or hidden-bar padding branch', () => {
  const rule = spacingRule(candidate);
  assert.equal(rule.selector, newSelector);
  const added = candidate.replace(before.replace(oldSelector, newSelector), '');
  assert.equal(added, '');
  assert.equal(candidate.split(newSelector).length - 1, 1);
  assert.equal(rule.media.includes('max-width: 749px'), true);
});
