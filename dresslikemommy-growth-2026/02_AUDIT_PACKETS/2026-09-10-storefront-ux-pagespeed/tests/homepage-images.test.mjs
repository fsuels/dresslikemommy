import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const packet = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const theme = process.env.AUDIT_THEME_DIR || path.join(packet, 'candidate');
const source = fs.readFileSync(path.join(theme, 'assets/homepage-collection-card-images.js'), 'utf8');

function image(key) {
  let src = 'https://www.dresslikemommy.com/cdn/' + key + '.jpg';
  let srcset = src + ' 640w';
  const writes = [];
  return {
    dataset: { homepageCollectionImageKey: key },
    writes,
    get currentSrc() { return src; },
    get src() { return src; },
    set src(value) { writes.push(['src', value]); src = value; },
    get srcset() { return srcset; },
    set srcset(value) { writes.push(['srcset', value]); srcset = value; },
    getAttribute(name) { return name === 'src' ? src : null; },
    removeAttribute(name) { writes.push(['remove', name]); },
  };
}

function candidate(key) {
  return { key, src: 'https://www.dresslikemommy.com/cdn/' + key + '.jpg', srcset: key + '.jpg 640w', alt: key };
}

function run(keys) {
  const images = keys.map(image);
  const cards = images.map(img => ({
    querySelector(selector) {
      if (selector === '[data-homepage-collection-image]') return img;
      if (selector === '.homepage-collection-card__image-candidates') {
        return { textContent: JSON.stringify([candidate('a'), candidate('b'), candidate('c')]) };
      }
      return null;
    },
  }));
  const events = new Map();
  const document = {
    readyState: 'complete',
    querySelectorAll(selector) { return selector === '[data-homepage-collection-card]' ? cards : []; },
    addEventListener(name, callback) { events.set(name, callback); },
  };
  vm.runInNewContext(source, { document, window: {}, Set, Math, URL }, { filename: 'homepage-collection-card-images.js' });
  return { images, reloadSection() { events.get('shopify:section:load')({ target: { ownerDocument: document } }); } };
}

test('keeps unique server images without changing requests after initial HTML has begun loading', () => {
  const page = run(['a', 'b']);
  assert.deepEqual(page.images.map(img => img.dataset.homepageCollectionImageKey), ['a', 'b']);
  assert.deepEqual(page.images.flatMap(img => img.writes), []);
});

test('still replaces a duplicate card image with a distinct available candidate', () => {
  const page = run(['a', 'a']);
  assert.equal(page.images[0].writes.length, 0);
  assert.notEqual(page.images[1].dataset.homepageCollectionImageKey, 'a');
  assert.ok(page.images[1].writes.some(([name]) => name === 'src'));
});

test('theme editor section reload does not reload already unique images', () => {
  const page = run(['a', 'b']);
  page.reloadSection();
  assert.deepEqual(page.images.flatMap(img => img.writes), []);
});
