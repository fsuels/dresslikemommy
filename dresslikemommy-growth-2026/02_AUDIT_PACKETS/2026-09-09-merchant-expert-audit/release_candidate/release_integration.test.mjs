import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire('/tmp/dlm-merchant-landing-validation-20260909/package.json');
const { JSDOM } = require('jsdom');
const root = path.dirname(fileURLToPath(import.meta.url));
const read = filename => fs.readFileSync(path.join(root, filename), 'utf8');
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const md5 = value => crypto.createHash('md5').update(value).digest('hex');
const parse = value => JSON.parse(value.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, ''));
const snippet = read('theme/snippets/pdp-purchase-confidence.liquid');
const previousSnippet = fs.readFileSync(path.resolve(root, '../theme_candidate/theme/snippets/pdp-purchase-confidence.liquid'), 'utf8');
const shippingCopy = JSON.parse(read('shipping_copy.json'));
function datesScript(source) {
  const scripts = [...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].filter(match => match[1].includes('function calculateDeliveryDates()'));
  assert.equal(scripts.length, 1);
  return scripts[0][1];
}

test('the actual legacy date script cannot refill the removed confidence target', async () => {
  const script = datesScript(read('theme/layout/theme.liquid'));
  assert.equal(script, datesScript(read('baseline/layout/theme.liquid')));
  const paragraph = snippet.match(/<p class="dlm-pc-row__estimate">\{\{ pc_shipping_checkout \}\}<\/p>/)?.[0];
  assert.ok(paragraph);
  assert.doesNotMatch(snippet, /dlm-shipping-card-date|data-delivery-estimate-row|data-delivery-window|12[-–]16/);
  for (const configured of [undefined, { standard: { minBusinessDays: 12, maxBusinessDays: 16 } }]) {
    const dom = new JSDOM(`<html lang="en"><body>${paragraph.replace('{{ pc_shipping_checkout }}', shippingCopy['en.default'])}</body></html>`, { runScripts: 'outside-only' });
    try {
      dom.window.Shopify = { locale: 'en' };
      dom.window.DLM_DELIVERY_ESTIMATES = configured;
      dom.window.eval(script);
      dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
      await new Promise(resolve => setTimeout(resolve, 0));
      assert.equal(dom.window.document.querySelector('.dlm-pc-row__estimate').textContent, 'See shipping options at checkout.');
      assert.equal(dom.window.document.getElementById('dlm-shipping-card-date'), null);
    } finally { dom.window.close(); }
  }
});

test('date regression has a positive control that detects the previous rolling promise', async () => {
  const dom = new JSDOM('<html lang="en"><body><p data-delivery-estimate-row data-delivery-fallback-visible><span id="dlm-shipping-card-date" data-delivery-window="12-16 days" data-delivery-window-mode="calendar">12-16 days</span></p></body></html>', { runScripts: 'outside-only' });
  try {
    dom.window.Shopify = { locale: 'en' };
    dom.window.eval(datesScript(read('baseline/layout/theme.liquid')));
    dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
    await new Promise(resolve => setTimeout(resolve, 0));
    assert.notEqual(dom.window.document.getElementById('dlm-shipping-card-date').textContent, '12-16 days');
    assert.match(dom.window.document.getElementById('dlm-shipping-card-date').textContent, /\d/);
  } finally { dom.window.close(); }
});

test('all35 locales use the exact neutral checkout message and no new delivery promise', () => {
  assert.equal(Object.keys(shippingCopy).length, 35);
  for (const [locale, copy] of Object.entries(shippingCopy)) {
    const dictionary = parse(read(`theme/locales/${locale}.json`));
    assert.equal(dictionary.products.purchase_confidence.shipping_checkout, copy, locale);
    assert.doesNotMatch(copy, /\d|translation missing|<|>|\{\{/i, locale);
  }
});

test('country/currency/change-country controls remain byte-identical and shipping policy is linked', () => {
  const row = text => text.match(/<p class="dlm-pc-row__action-row">[\s\S]*?<\/p>/)?.[0];
  assert.equal(row(snippet), row(previousSnippet));
  assert.match(snippet, /localization.country.name/);
  assert.match(snippet, /localization.country.currency.iso_code/);
  assert.match(snippet, /routes.root_url/);
  assert.match(snippet, /append: 'policies\/shipping-policy'/);
  assert.match(snippet, /append: '\/policies\/shipping-policy'/);
  assert.match(snippet, /href="\{\{ pc_shipping_policy_url \}\}"/);
});

test('cart is the exact prior reviewed source and all four SEO values survive the merges', () => {
  assert.equal(sha(read('theme/assets/cart.js')), 'e2fed4a6ae3abbba3b39d481dfee9eb755f623e7856b2d1c2a8747fe6c059cf7');
  const changes = JSON.parse(read('merge_proof.json')).seo_changes;
  assert.equal(changes.length, 4);
  for (const change of changes) {
    const dictionary = parse(read('theme/' + change.file));
    assert.equal(change.key.split('.').reduce((value, key) => value[key], dictionary), change.after);
  }
});

test('consent nonlocale files match final independent sources including CSSv2', () => {
  const handoff = JSON.parse(read('consent_handoff_source.json'));
  const nonlocales = handoff.files.filter(file => !file.filename.startsWith('locales/'));
  assert.equal(nonlocales.length, 4);
  for (const file of nonlocales) {
    const body = fs.readFileSync(path.join(root, 'theme', file.filename));
    assert.equal(sha(body), file.afterSha256, file.filename);
    assert.equal(md5(body), file.afterMd5, file.filename);
    assert.equal(body.length, file.bytes, file.filename);
  }
  assert.equal(fs.statSync(path.join(root, 'theme/assets/cookie-preferences.css')).size, 669);
});

test('functional Merchant JavaScript and immutable revision3 remain intact after Danish merge', () => {
  const file = 'assets/product-desktop-ux-20260513-ruler-sync.js';
  const prior = fs.readFileSync(path.resolve(root, '../theme_candidate/theme', file), 'utf8');
  let normalized = read('theme/' + file);
  for (const change of JSON.parse(read('danish_merge_proof.json')).overrides) {
    const after = `    ${change.key}: ${JSON.stringify(change.after)},`;
    assert.equal(normalized.split(after).length - 1, 1);
    normalized = normalized.replace(after, `    ${change.key}: ${JSON.stringify(change.before)},`);
  }
  assert.equal(normalized, prior);
  assert.equal(sha(fs.readFileSync(path.resolve(root, '../theme_candidate/candidate_files.json'))), '1ac332a2a99ce5ae66dc9f0485f476631457acd52b594b73134f086c433d8a6b');
});

test('structured data removes only invented expiry and universal returns while keeping exact offer behavior', () => {
  const filename = 'snippets/jsonld-seo.liquid';
  const before = read('baseline/' + filename);
  assert.equal(md5(before), 'b7935da217fb539fc8fc4b32793b7132');
  let expected = before.replace("  {%- assign price_valid_until_year = 'now' | date: '%Y' | plus: 1 -%}\n", '')
    .replace("  {%- assign price_valid_until = price_valid_until_year | append: '-12-31' -%}\n", '')
    .replace('      "priceValidUntil": {{ price_valid_until | json }},\n', '')
    .replace(/      "hasMerchantReturnPolicy": \{[\s\S]*?      \},\n/, '');
  const after = read('theme/' + filename);
  assert.equal(after, expected);
  assert.doesNotMatch(after, /price_valid_until|priceValidUntil|hasMerchantReturnPolicy/);
  for (const field of ['selected_variant_price', 'currency_code', 'selected_variant.available', 'selected_variant_offer_url', 'selected_sku_value', 'gtin8', 'gtin12', 'gtin13', 'gtin14', 'shippingDetails']) assert.ok(after.includes(field), field);
  assert.match(after, /"itemCondition": "https:\/\/schema.org\/NewCondition",\n      "shippingDetails": \{/);
});

test('only the hidden productFAQ render call is removed from the already reviewed main product', () => {
  const filename = 'sections/main-product.liquid';
  const prior = fs.readFileSync(path.resolve(root, '../theme_candidate/theme', filename), 'utf8');
  const call = "{% render 'product-faq-schema', product: product %}\n";
  assert.equal(prior.split(call).length - 1, 1);
  assert.equal(read('theme/' + filename), prior.replace(call, ''));
  assert.equal(read('theme/snippets/product-faq-schema.liquid'), read('baseline/snippets/product-faq-schema.liquid'));
});

test('complete baseline has525 independently checksum-bound original files', () => {
  const manifest = JSON.parse(read('complete_baseline_manifest.json'));
  assert.equal(manifest.files.length, 525);
  for (const file of manifest.files) {
    const body = fs.readFileSync(path.join(root, 'baseline', file.filename));
    assert.equal(md5(body), file.md5, file.filename);
    assert.equal(sha(body), file.sha256, file.filename);
    assert.equal(body.length, file.bytes, file.filename);
  }
});
