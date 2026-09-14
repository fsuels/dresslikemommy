import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import test from 'node:test';
import { runInContext } from 'node:vm';

const require = createRequire(import.meta.url);
const { JSDOM } = require(process.env.DLM_TEST_JSDOM_PATH || '/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const sectionPath = 'sections/main-product.liquid';
const mapPath = 'snippets/product-page-copy-map.liquid';
const globalPath = 'assets/global.js';
const contextKeys = ['back_to_context', 'view_similar_styles_in', 'browse_more_from'];
const snapshot = JSON.parse(readFileSync(new URL('./before.json', import.meta.url), 'utf8'));
const digest = (value) => createHash('md5').update(value).digest('hex');
const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');
const originalSection = read(`./rollback/${sectionPath}`);
const candidateSection = read(`../candidate/${sectionPath}`);
const originalMapSource = read(`./rollback/${mapPath}`);
const candidateMapSource = read(`../candidate/${mapPath}`);
const originalGlobal = read(`./rollback/${globalPath}`);
const candidateGlobal = read(`../candidate/${globalPath}`);
const parseMap = (source) => JSON.parse(source.replace(/^\{% comment %\}[\s\S]*?\{% endcomment %\}\s*/, ''));
const originalMap = parseMap(originalMapSource);
const candidateMap = parseMap(candidateMapSource);
const locales = Object.keys(originalMap);

function sourceBetween(source, start, end) {
  assert.equal(source.split(start).length - 1, 1, `Unique production boundary: ${start}`);
  const startIndex = source.indexOf(start);
  const endIndex = source.indexOf(end, startIndex);
  assert.ok(endIndex > startIndex, `Closing production boundary: ${end}`);
  return source.slice(startIndex, endIndex);
}

function productionFunctions(source) {
  return sourceBetween(source, '    function normalize(text) {', '    function translateTextNodes(root) {')
    + sourceBetween(source, '    function applyContextTranslations() {', '    function applyProductTranslations() {');
}

const originalFunctions = productionFunctions(originalSection);
const candidateFunctions = productionFunctions(candidateSection);

// This models missing global Liquid context on a direct PDP; it is not a Liquid engine.
// The browser functions below are extracted unchanged from the actual theme files.
function directPdpCopy(map, locale) {
  return Object.fromEntries(Object.entries(map[locale]).map(([key, value]) => [
    key,
    value.replace(/\{\{\s*(?:collection|context|size|price)\s*\}\}/g, ''),
  ]));
}

function expectedLabels(locale, context) {
  const copy = originalMap[locale];
  const interpolate = (template) => template.replace(/\{\{\s*(?:collection|context)\s*\}\}/g, () => context);
  return {
    back: interpolate(copy.back_to_context),
    heading: interpolate(copy.browse_more_from),
    link: copy.view_similar_styles,
    aria: interpolate(copy.view_similar_styles_in),
    title: interpolate(copy.view_similar_styles_in),
    href: '/collections/family-tops',
  };
}

function harness(functions, copy, labels, locale = 'en') {
  const dom = new JSDOM('<!doctype html><html><body><span data-back-to-results-label></span><h2 class="buy-box-similar-styles__title"></h2><a class="product-breadcrumb__browse-link"></a></body></html>', {
    url: `https://dresslikemommy.com/${locale}/products/together-heart-family-matching-sweaters`,
    runScripts: 'outside-only',
  });
  const { document } = dom.window;
  document.documentElement.lang = locale;
  const back = document.querySelector('[data-back-to-results-label]');
  const heading = document.querySelector('h2');
  const link = document.querySelector('a');
  back.textContent = labels.back;
  heading.textContent = labels.heading;
  link.textContent = labels.link;
  link.setAttribute('aria-label', labels.aria);
  link.setAttribute('title', labels.title);
  link.setAttribute('href', labels.href);
  dom.window.copy = copy;
  dom.window.fetch = () => { throw new Error('Network is forbidden in this regression'); };
  runInContext(functions, dom.getInternalVMContext(), { filename: sectionPath });
  return {
    apply: () => runInContext('applyContextTranslations();', dom.getInternalVMContext()),
    labels: () => ({
      back: back.textContent,
      heading: heading.textContent,
      link: link.textContent,
      aria: link.getAttribute('aria-label'),
      title: link.getAttribute('title'),
      href: link.getAttribute('href'),
    }),
    childElementCount: () => back.childElementCount + heading.childElementCount + link.childElementCount,
    close: () => dom.window.close(),
  };
}

function assertLabels(actual, expected) {
  assert.deepEqual(actual, expected);
  for (const field of ['back', 'heading', 'aria', 'title']) {
    assert.doesNotMatch(actual[field], /\{\{|__CONTEXT__/, `${field} has no unresolved placeholder`);
  }
}

function globalHarness(source, locale = 'en') {
  const dom = new JSDOM('<!doctype html><html><body></body></html>', {
    url: `https://dresslikemommy.com/${locale}/products/together-heart-family-matching-sweaters`,
    runScripts: 'outside-only',
  });
  dom.window.document.documentElement.lang = locale;
  dom.window.Shopify = { locale };
  dom.window.DLM_PRODUCT_PAGE_COPY = Object.fromEntries(locales.map((key) => [key, directPdpCopy(candidateMap, key)]));
  dom.window.fetch = () => { throw new Error('Network is forbidden in this regression'); };
  // Include the real locale lookup, constants, and sanitizer with the formatter.
  // Stop before unrelated page initialization; none of this prefix runs page effects.
  const functions = sourceBetween(source, 'function getFocusableElements(container) {', 'function rememberResultsPageUrl() {');
  runInContext(functions, dom.getInternalVMContext(), { filename: globalPath });
  return {
    format: (...args) => dom.window.formatBackToResultsLabel(...args),
    close: () => dom.window.close(),
  };
}

test('frozen rollback files match the captured preview checksums', () => {
  assert.equal(snapshot.data.preview.id, 'gid://shopify/OnlineStoreTheme/137888792673');
  for (const [filename, source] of [[sectionPath, originalSection], [mapPath, originalMapSource], [globalPath, originalGlobal]]) {
    const file = snapshot.data.preview.files.nodes.find((node) => node.filename === filename);
    assert.ok(file, `${filename} was captured`);
    assert.equal(digest(source), file.checksumMd5, `${filename} rollback is exact`);
  }
  assert.equal(digest(originalGlobal), 'd8c9a52489db8532de327592e6a60f9d');
});

test('map repair changes only 105 context templates across the same 35 locales', () => {
  assert.equal(locales.length, 35);
  assert.deepEqual(Object.keys(candidateMap), locales);
  let changed = 0;
  for (const locale of locales) {
    assert.deepEqual(Object.keys(candidateMap[locale]), Object.keys(originalMap[locale]));
    for (const [key, value] of Object.entries(originalMap[locale])) {
      if (!contextKeys.includes(key)) {
        assert.equal(candidateMap[locale][key], value, `${locale}.${key} is preserved`);
        continue;
      }
      assert.equal((value.match(/\{\{\s*(?:context|collection)\s*\}\}/g) || []).length, 1);
      assert.equal(candidateMap[locale][key].split('__CONTEXT__').length - 1, 1);
      assert.equal(
        candidateMap[locale][key],
        value.replace(/\{\{\s*(?:context|collection)\s*\}\}/g, '__CONTEXT__'),
        `${locale}.${key} retains its translated words`,
      );
      changed += 1;
    }
  }
  assert.equal(changed, 105);
});

test('old snapshot fails complete-label acceptance in all 35 locales with its exact English symptom', () => {
  for (const locale of locales) {
    const h = harness(originalFunctions, directPdpCopy(originalMap, locale), expectedLabels('en', 'Family Tops'), locale);
    try {
      h.apply();
      const result = h.labels();
      assert.throws(() => assertLabels(result, expectedLabels(locale, 'Family Tops')), { name: 'AssertionError' });
      for (const field of ['back', 'heading', 'aria', 'title']) {
        assert.ok(!result[field].includes('Family Tops'), `${locale}.${field} reproduces missing context`);
      }
      assert.equal(result.href, '/collections/family-tops');
      if (locale === 'en') {
        assert.equal(result.heading, 'Browse more from ');
        assert.equal(result.aria, 'View similar styles in ');
        assert.equal(result.title, 'View similar styles in ');
        assert.equal(result.back, 'Back to ');
      }
    } finally {
      h.close();
    }
  }
});

for (const locale of locales) {
  test(`${locale}: candidate preserves the collection in translated fallback text and accessible attributes`, () => {
    const h = harness(candidateFunctions, directPdpCopy(candidateMap, locale), expectedLabels('en', 'Family Tops'), locale);
    try {
      h.apply();
      assertLabels(h.labels(), expectedLabels(locale, 'Family Tops'));
    } finally {
      h.close();
    }
  });
}

test('English labels and destination remain complete after repeated context translation', () => {
  const expected = expectedLabels('en', 'Family Tops');
  const h = harness(candidateFunctions, directPdpCopy(candidateMap, 'en'), expected);
  try {
    for (let repeat = 0; repeat < 5; repeat += 1) {
      h.apply();
      assertLabels(h.labels(), expected);
    }
  } finally {
    h.close();
  }
});

for (const [locale, context] of [['ar', 'ملابس العائلة'], ['ja', 'ファミリートップス']]) {
  test(`${locale}: already-localized native labels survive repeated application unchanged`, () => {
    const expected = expectedLabels(locale, context);
    const h = harness(candidateFunctions, directPdpCopy(candidateMap, locale), expected, locale);
    try {
      h.apply();
      h.apply();
      assertLabels(h.labels(), expected);
    } finally {
      h.close();
    }
  });

  test(`${locale}: English fallback labels retain the native collection name`, () => {
    const h = harness(candidateFunctions, directPdpCopy(candidateMap, locale), expectedLabels('en', context), locale);
    try {
      h.apply();
      assertLabels(h.labels(), expectedLabels(locale, context));
    } finally {
      h.close();
    }
  });
}

test('punctuation and markup-like collection text stay literal in text and accessible labels', () => {
  const context = 'Mom\'s & Kids (2–8) / "Family" <Tops>';
  const expected = expectedLabels('en', context);
  const h = harness(candidateFunctions, directPdpCopy(candidateMap, 'en'), expected);
  try {
    h.apply();
    assertLabels(h.labels(), expected);
    assert.equal(h.childElementCount(), 0, 'Collection text never becomes markup');
  } finally {
    h.close();
  }
});

test('literal dollar tokens fail with the old helper plus repaired map and pass with the candidate callback', () => {
  const context = "Family $& $$ $` $' Tops";
  const expected = expectedLabels('en', context);
  const old = harness(originalFunctions, directPdpCopy(candidateMap, 'en'), expected);
  const fixed = harness(candidateFunctions, directPdpCopy(candidateMap, 'en'), expected);
  try {
    old.apply();
    assert.throws(() => assertLabels(old.labels(), expected), { name: 'AssertionError' });
    assert.match(old.labels().heading, /__CONTEXT__/);
    fixed.apply();
    assertLabels(fixed.labels(), expected);
    fixed.apply();
    assertLabels(fixed.labels(), expected);
  } finally {
    old.close();
    fixed.close();
  }
});

for (const locale of ['en', 'ar', 'ja']) {
  test(`${locale}: generic labels without collection context stay complete and retain the destination`, () => {
    const generic = (copy) => ({
      back: copy.back_to_results,
      heading: copy.browse_similar_styles,
      link: copy.view_similar_styles,
      aria: copy.view_similar_styles,
      title: copy.view_similar_styles,
      href: '/collections/all',
    });
    const h = harness(candidateFunctions, directPdpCopy(candidateMap, locale), generic(originalMap.en), locale);
    try {
      h.apply();
      assertLabels(h.labels(), generic(originalMap[locale]));
    } finally {
      h.close();
    }
  });
}

test('old shared back-link formatter with the repaired map reproduces literal-dollar corruption', () => {
  const h = globalHarness(originalGlobal);
  try {
    assert.equal(h.format('Family Tops'), expectedLabels('en', 'Family Tops').back);
    const context = "Family $& $$ $` $' Tops";
    const result = h.format(context);
    assert.notEqual(result, expectedLabels('en', context).back);
    assert.match(result, /__CONTEXT__/);
  } finally {
    h.close();
  }
});

test('candidate shared formatter preserves ordinary and literal-dollar collection names in all 35 locales', () => {
  for (const locale of locales) {
    const h = globalHarness(candidateGlobal, locale);
    try {
      for (const context of ["Mom's & Kids (2–8) / Tops", "Family $& $$ $` $' Tops"]) {
        assert.equal(h.format(context), expectedLabels(locale, context).back, `${locale} preserves literal context`);
      }
      assert.equal(h.format(' \n Family\tTops \n '), expectedLabels(locale, 'Family Tops').back, `${locale} retains whitespace cleanup`);
    } finally {
      h.close();
    }
  }
});

test('shared formatter retains localized generic, existing fallback, and search labels', () => {
  for (const locale of ['en', 'ar', 'ja']) {
    const h = globalHarness(candidateGlobal, locale);
    const copy = originalMap[locale];
    try {
      for (const empty of ['', null, undefined, ' \t\n ']) {
        assert.equal(h.format(empty), copy.back_to_results, `${locale} empty input uses generic label`);
      }
      assert.equal(h.format(copy.back_to_results), copy.back_to_results);
      assert.equal(h.format(copy.back_to_search_results), copy.back_to_search_results);
      for (const search of ['Search', 'Search results', ' SEARCH\nRESULTS ']) {
        assert.equal(h.format(search), copy.back_to_search_results, `${locale} recognizes search context`);
      }
    } finally {
      h.close();
    }
  }
});
