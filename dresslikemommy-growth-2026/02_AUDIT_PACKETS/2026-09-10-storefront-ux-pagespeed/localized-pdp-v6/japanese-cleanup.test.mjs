import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { JSDOM } = require(process.env.DLM_TEST_JSDOM_PATH || '/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const dir = path.dirname(fileURLToPath(import.meta.url));
const packet = path.dirname(dir);
const theme = process.env.AUDIT_THEME_DIR || path.join(packet, 'candidate');
const snippet = fs.readFileSync(path.join(theme, 'snippets/pdp-description-copy-cleanup.liquid'), 'utf8');
const script = snippet.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'Run the actual script extracted from the candidate Liquid snippet');
const plan = JSON.parse(fs.readFileSync(path.resolve(packet, '../2026-09-10-together-heart-source-repair/plan.json'), 'utf8'));
const fixtureHashes = {
  ja: '9be752054def42be5e7a71c87dfd263853a985400e50c72184b6d44254976c3b',
  en: '3b219a9fe76d0533abcd82d36101ce3cdfb394ce6382dcf4304dc00474667bba',
  fr: '21ae3b4f070b6863e1deff06567a985a2ff3f54f5b2d23e65e3cb8b3acd2c8f6',
  ar: 'd3a7bb0bfd14250669081711a8130333bea940ebe0283d793bbe49df8003e9c3',
  ko: 'f71a1b8dd06bb020ee107e2a072c810e880d47b08ac49e710793fccfa90bc7f4',
};
const fixtures = Object.fromEntries(Object.entries(fixtureHashes).map(([locale, hash]) => {
  const body = plan.rows.find(row => row.locale === locale)?.after_body;
  assert.equal(crypto.createHash('sha256').update(body).digest('hex'), hash, `${locale} fixture is frozen`);
  return [locale, body];
}));

function run(html, locale) {
  const dom = new JSDOM(`<!doctype html><html lang="${locale}"><body><div data-product-description>${html}</div></body></html>`, {
    runScripts: 'outside-only',
    url: `https://www.dresslikemommy.com/${locale}/products/test-fixture`,
  });
  const { document } = dom.window;
  const root = document.querySelector('[data-product-description]');
  const snapshot = () => ({
    html: root.innerHTML,
    paragraphs: [...root.querySelectorAll('p')].map(node => node.innerHTML),
    tables: [...root.querySelectorAll('table')].map(node => node.outerHTML),
    listItems: [...root.querySelectorAll('li')].map(node => node.innerHTML),
    text: root.textContent,
    adminArtifacts: root.querySelectorAll('a[href*="admin.shopify.com"], meta[http-equiv], meta[content*="text/html"]').length,
  });
  const before = snapshot();
  dom.window.eval(script);
  document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
  const after = snapshot();
  dom.window.close();
  return { before, after };
}

const japaneseParagraphs = [
  'ハート柄とTogetherの文字が入った長袖クルーネックセーター。子ども用と大人用のサイズがあります。',
  '1点の選択につきセーター1着です。一人ずつサイズと色を選んでください。写真に写っているその他の衣類や小物は含まれません。',
  '胸囲、袖丈、着丈を、お手持ちのサイズが合うセーターと比べてください。ヒップとウエストの寸法は不明です。',
];
const observedJapaneseFailure = ['Together。。', '11。。。', '、、、。。'];

test('Japanese: all three saved paragraphs survive exactly, including the observed failure examples', () => {
  const result = run(fixtures.ja, 'ja');
  assert.deepEqual(result.before.paragraphs, japaneseParagraphs);
  assert.notDeepEqual(result.after.paragraphs, observedJapaneseFailure);
  assert.deepEqual(result.after.paragraphs, japaneseParagraphs);
});

for (const locale of ['ja', 'ja-JP', 'zh', 'zh-Hant', 'ko-KR']) {
  test(`${locale}: native CJK prose, fullwidth punctuation and list markup survive unchanged`, () => {
    const result = run('<p>サイズ（子ども）：１１０。 Together</p><ul><li><strong>尺寸：</strong>兒童（１１０）</li><li>가족 의류（衣類）</li></ul>', locale);
    assert.equal(result.after.html, result.before.html);
  });
}

for (const locale of ['en', 'fr', 'ar', 'ko']) {
  test(`${locale}: saved buyer paragraphs retain existing behavior`, () => {
    const result = run(fixtures[locale], locale);
    const expected = locale === 'fr'
      ? result.before.paragraphs.map(html => html.replace(/\s+([,.;:])/g, '$1'))
      : result.before.paragraphs;
    assert.deepEqual(result.after.paragraphs, expected);
  });
}

test('all five saved localized size tables remain exactly unchanged', () => {
  for (const [locale, html] of Object.entries(fixtures)) {
    const result = run(html, locale);
    assert.ok(result.before.tables.length, `${locale} has a real saved size table`);
    assert.deepEqual(result.after.tables, result.before.tables, locale);
  }
});

test('non-CJK locales retain vendor phrase and stray CJK cleanup in paragraphs and list items', () => {
  for (const locale of ['en', 'fr', 'ar', '']) {
    const result = run('<p>The vendor calls this a 四层纱布 (four-layer gauze) loungewear set.</p><ul><li><strong>Print reference:</strong> 花朵 (floral)</li></ul>', locale);
    assert.deepEqual(result.after.paragraphs, ['(four-layer gauze) loungewear set.']);
    assert.deepEqual(result.after.listItems, ['<strong>Pattern:</strong> (floral)']);
  }
});

test('native CJK locales still remove explicit English vendor-credit phrases', () => {
  for (const locale of ['ja', 'zh-Hant', 'ko']) {
    const result = run('<p>The vendor calls this a 四层纱布 (four-layer gauze).</p>', locale);
    assert.deepEqual(result.after.paragraphs, ['(four-layer gauze).']);
  }
});

test('admin-artifact and internal-label removal stay active on every tested locale', () => {
  for (const locale of ['ja', 'zh', 'ko', 'en', 'fr', 'ar']) {
    const result = run('<p>Visible copy <a href="https://admin.shopify.com/store/test/products/1">Internal link</a></p><meta http-equiv="Content-Type" content="text/html"><ul><li><strong>Chart-backed variants:</strong>Internal copy</li></ul>', locale);
    assert.equal(result.after.adminArtifacts, 0, locale);
    assert.equal(result.after.listItems.length, 0, locale);
    assert.ok(!result.after.text.includes('Internal link'), locale);
  }
});
