import assert from 'node:assert/strict';
import test from 'node:test';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const packet = path.dirname(fileURLToPath(import.meta.url));
const runtime = JSON.parse(fs.readFileSync(path.join(packet, 'runtime.json'), 'utf8'));
const require = createRequire(path.join(runtime.harness_path, 'package.json'));
const { Liquid } = require('liquidjs');
const organic = path.resolve(packet, '../../../2026-09-09-organic-growth');
const classification = JSON.parse(fs.readFileSync(path.join(organic, 'couples-theme-classification-readback-20260911.json'), 'utf8')).result.data;
const copy = JSON.parse(fs.readFileSync(path.join(organic, 'couples-collection-copy-20260911.json'), 'utf8')).locale_values;
const partials = path.join(runtime.harness_path, 'test-partials');
fs.mkdirSync(partials, { recursive: true });
fs.writeFileSync(path.join(partials, 'collection-seo-fallback.liquid'), "{%- case field -%}{%- when 'display_title' -%}Existing title{%- when 'hero_summary' -%}<p>Legacy hero</p>{%- when 'body_description' -%}<p>Legacy hero</p><p>Legacy body</p>{%- when 'force_theme_seo' -%}true{%- endcase -%}");
fs.writeFileSync(path.join(partials, 'collection-seo-content.liquid'), '<p>Legacy lower rich content</p>');
for (const name of ['product-image-alt', 'collection-hub-subcategory-cards', 'collection-merchandising-callout', 'style-journal-internal-links', 'faq-schema-from-html', 'icon-caret']) {
  fs.writeFileSync(path.join(partials, `${name}.liquid`), '');
}
const liquid = new Liquid({ partials, extname: '.liquid' });
const read = (stage, name) => fs.readFileSync(path.join(packet, stage, name), 'utf8');
const visibility = 'snippets/collection-grid-product-visible.liquid';
const banner = 'sections/main-collection-banner.liquid';
const seo = 'sections/main-collection-seo.liquid';
const prepare = source => source.replace(/{%\s*schema\s*%}[\s\S]*?{%\s*endschema\s*%}/g, '').replace(/{%-?\s*style\s*-?%}/g, '<style>').replace(/{%-?\s*endstyle\s*-?%}/g, '</style>');
const render = (stage, name, context) => liquid.parseAndRender(prepare(read(stage, name)), context);
const productFixture = (category, tags = [], title = 'Test item') => ({ title, handle: 'test-item', tags, metafields: { custom: { category1: category } } });
const collectionFixture = (handle, description = copy.en.body_html) => ({ id: handle === 'couples' ? 290635284577 : 123456789, handle, title: 'Preserved source title', description, metafields: { custom: {} } });
const context = (handle = 'couples', description = copy.en.body_html, show = true) => ({ collection: collectionFixture(handle, description), section: { id: 'test-section', settings: { show_collection_description: show, show_collection_image: false, color_scheme: 'scheme-1', padding_top: 20, padding_bottom: 48 } }, settings: { animations_reveal_on_scroll: false }, routes: { collections_url: '/collections' } });

test('all three approved source members reproduce hidden-before and visible-after', async () => {
  assert.equal(classification.nodes.length, 3);
  for (const node of classification.nodes) {
    const c = { collection: collectionFixture('couples'), collection_handle: 'couples', product: productFixture(node.category1.value, node.tags, node.title) };
    assert.equal((await render('before', visibility, c)).trim(), 'false', node.id);
    assert.equal((await render('proposed', visibility, c)).trim(), 'true', node.id);
  }
});

test('other collection branches retain their actual Liquid output across category and tag cases', async () => {
  const handles = ['mommy-and-me', 'mother-daughter-matching-dresses', 'dresses', 'matching-outfits', 'family-matching-outfits', 'family-sets', 'daddy-and-me', 'trunks', 'couple-matching', 'matching-couples-t-shirts', 'maternity', 'unmapped'];
  const categories = ['', 'Mommy and Me', 'Family Matching', 'Daddy and Me', 'Couples', 'Maternity'];
  const tags = [[], ['Mommy and Me'], ['Family Matching'], ['Daddy and Me'], ['Couples'], ['Maternity']];
  for (const handle of handles) for (const category of categories) for (const tagList of tags) {
    const c = { collection: collectionFixture(handle), collection_handle: handle, product: productFixture(category, tagList) };
    assert.equal(await render('proposed', visibility, c), await render('before', visibility, c), `${handle}/${category}/${tagList}`);
  }
});

test('root Couples still includes legacy correctly classified members', async () => {
  for (const product of [productFixture('Couples'), productFixture('', ['Couples'])]) {
    const c = { collection: collectionFixture('couples'), product };
    assert.equal((await render('before', visibility, c)).trim(), 'true');
    assert.equal((await render('proposed', visibility, c)).trim(), 'true');
  }
});

test('both stored paragraphs are rendered exactly for all 21 saved locales', async () => {
  assert.equal(Object.keys(copy).length, 21);
  for (const [locale, values] of Object.entries(copy)) {
    const c = context('couples', values.body_html);
    const before = await render('before', banner, c);
    const after = await render('proposed', banner, c);
    assert.ok(before.includes('Legacy hero'), locale);
    assert.ok(!before.includes(values.body_html), locale);
    assert.ok(after.includes(`<div class="collection-hero__description rte">${values.body_html}</div>`), locale);
    assert.ok(!after.includes('Legacy hero'), locale);
    assert.ok(after.includes('<h1 class="collection-hero__title">Existing title</h1>'), locale);
  }
});

test('description setting remains respected and blank source retains prior fallback', async () => {
  for (const c of [context('couples', copy.en.body_html, false), context('couples', '')]) {
    assert.equal(await render('proposed', banner, c), await render('before', banner, c));
  }
});

test('other collection banners remain byte-identical in rendered output', async () => {
  for (const handle of ['mommy-and-me', 'family-matching-outfits', 'swimsuits', 'daddy-and-me', 'couple-matching', 'matching-couples-t-shirts', 'maternity', 'unmapped']) {
    assert.equal(await render('proposed', banner, context(handle)), await render('before', banner, context(handle)), handle);
  }
});

test('only exact Couples root suppresses its obsolete lower copy', async () => {
  assert.ok((await render('before', seo, context())).includes('Legacy lower rich content'));
  assert.equal((await render('proposed', seo, context())).trim(), '');
  for (const handle of ['mommy-and-me', 'family-matching-outfits', 'swimsuits', 'daddy-and-me', 'couple-matching', 'matching-couples-t-shirts', 'maternity', 'unmapped']) {
    assert.equal(await render('proposed', seo, context(handle)), await render('before', seo, context(handle)), handle);
  }
});

test('section schemas remain byte-identical and only three source files change', () => {
  for (const name of [banner, seo]) {
    const schema = text => text.match(/{%\s*schema\s*%}([\s\S]*?){%\s*endschema\s*%}/)[1];
    assert.equal(schema(read('proposed', name)), schema(read('before', name)));
    JSON.parse(schema(read('proposed', name)));
  }
  assert.deepEqual(runtime.files, [visibility, banner, seo]);
});

test('exact collection ID controls copy behavior if its handle changes', async () => {
  const c = context('renamed-couples');
  c.collection.id = 290635284577;
  assert.ok((await render('proposed', banner, c)).includes(copy.en.body_html));
  assert.equal((await render('proposed', seo, c)).trim(), '');
  for (const handle of ['renamed-couples', 'couple-matching']) {
    const v = { collection: collectionFixture(handle), product: productFixture('Family Matching') };
    v.collection.id = 290635284577;
    assert.equal((await render('proposed', visibility, v)).trim(), 'true');
  }
});

test('same handle with a different collection ID receives no exception', async () => {
  const c = context();
  c.collection.id = 987654321;
  c.product = productFixture('Family Matching');
  for (const name of [visibility, banner, seo]) {
    assert.equal(await render('proposed', name, c), await render('before', name, c), name);
  }
});
