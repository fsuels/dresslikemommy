import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const src = readFileSync(new URL('../../assets/product-desktop-ux-20260513-ruler-sync.js', import.meta.url), 'utf8');
const sticky = src.slice(src.indexOf('function initDesktopStickyAtc'), src.indexOf('function isVisibleGroup'));

test('desktop sticky bar hides while the matching-set builder or the buy button is on screen', () => {
  assert.match(sticky, /desktopMedia\.matches && !buttonInView && !\(isMatchingSet && builderInView\)/);
  assert.match(sticky, /observe\(matchingSetBuilder\)/);
});

test('desktop sticky bar no longer carries the builder instruction sentence', () => {
  assert.doesNotMatch(sticky, /data-matching-set-copy/);
});
