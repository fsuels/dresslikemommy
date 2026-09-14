import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import test from 'node:test';
import { runInContext } from 'node:vm';

const require = createRequire(import.meta.url);
const { JSDOM } = require(process.env.DLM_TEST_JSDOM_PATH || '/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');
const parseLocale = (text) => JSON.parse(text.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, ''));
const md5 = (value) => createHash('md5').update(value).digest('hex');
const sourceBefore = JSON.parse(read('./source-before.json'));
const mainMetadata = JSON.parse(read('./main-files-metadata.json'));
const renderedMain = JSON.parse(read('../../2026-09-11-google-ads-signup-tag/ongoing/root_landing_qa/ROOT_RENDERED.json'));
const runtimePath = 'assets/product-desktop-ux-20260513-ruler-sync.js';
const runtime = read(`../candidate/${runtimePath}`);
const section = read('../candidate/sections/main-product.liquid');
const confidenceSnippet = read('../candidate/snippets/pdp-purchase-confidence.liquid');
const mainConfidenceSnippet = read('./source/main/snippets/pdp-purchase-confidence.liquid');
const beforeText = read('./rollback/locales/ro.json');
const before = parseLocale(beforeText);
const proposed = parseLocale(read('./proposed/locales/ro.json'));
const mainRo = parseLocale(read('./source/main/locales/ro.json'));
const confidencePath = 'products.purchase_confidence.';

// Independent expected source/translation pairs; do not read the generated change report as the oracle.
const translations = {
  security_details_body: [
    'Payments are encrypted and processed securely by our payment providers. We do not store your full card number.',
    'Plățile sunt criptate și procesate în siguranță de furnizorii noștri de servicii de plată. Nu stocăm numărul complet al cardului.',
  ],
  privacy_link_label: ['View privacy policy', 'Vezi politica de confidențialitate'],
  returns_details_label: ['Return policy', 'Politica de retur'],
  returns_full_link_label: ['View full return policy', 'Vezi politica completă de retur'],
  security_headline: ['Secure checkout', 'Finalizare securizată a comenzii'],
  security_summary: [
    'Encrypted payment. Major cards and express checkout options accepted.',
    'Plată criptată. Sunt acceptate principalele carduri și opțiunile de plată expres.',
  ],
  security_details_label: ['Payment & privacy', 'Plată și confidențialitate'],
};

const guidanceKeys = ['chooseRoleStep', 'chooseOptionsStep', 'chooseRoleCta', 'addCurrentPiece', 'readyToAdd'];
const guidance = {
  ro: ['Alege pentru cine este această piesă', 'Alege mărimea și opțiunile', 'Alege un membru al familiei', 'Adaugă această piesă în coș', 'Gata de adăugat'],
  en: ['Choose who this piece is for', 'Choose size and options', 'Choose a family member', 'Add this piece to bag', 'Ready to add'],
  es: ['Elige para quién es esta pieza', 'Elige talla y opciones', 'Elige un familiar', 'Añadir esta pieza al carrito', 'Listo para añadir'],
  ja: ['この服を着る方を選んでください', 'サイズとオプションを選んでください', '着る方を選んでください', 'この商品をカートに追加', 'カートに追加できます'],
  ar: ['اختر من سيرتدي هذه القطعة', 'اختر المقاس والخيارات', 'اختر فردًا من العائلة', 'أضف هذه القطعة إلى السلة', 'جاهزة للإضافة'],
};

function leaves(value, path = '', out = {}) {
  if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) leaves(child, path ? `${path}.${key}` : key, out);
  } else {
    out[path] = value;
  }
  return out;
}

function filesBelow(directory, prefix = '') {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const relative = prefix + entry.name;
    return entry.isDirectory()
      ? filesBelow(new URL(`${entry.name}/`, directory), `${relative}/`)
      : [relative];
  }).sort();
}

function runtimeHarness(locale) {
  const dom = new JSDOM('<!doctype html><html><body></body></html>', { runScripts: 'outside-only' });
  dom.window.document.documentElement.lang = locale;
  dom.window.fetch = () => { throw new Error('Network is forbidden in this local regression'); };
  // Execute the complete existing V7 asset, not a copied label map or reconstructed helper.
  runInContext(runtime, dom.getInternalVMContext(), { filename: runtimePath });
  return { api: dom.window, close: () => dom.window.close() };
}

test('MAIN source assertions bind to the five captured text files; its runtime remains metadata-only', () => {
  assert.equal(mainMetadata.themeId, 'gid://shopify/OnlineStoreTheme/133290917985');
  assert.equal(mainMetadata.role, 'MAIN');
  assert.equal(mainMetadata.files.length, 5);
  for (const file of mainMetadata.files) {
    assert.equal(file.bodyType, 'OnlineStoreThemeFileBodyText');
    assert.equal(md5(read(`./source/main/${file.filename}`)), file.checksumMd5);
    const metadata = sourceBefore.data.main.files.nodes.find((node) => node.filename === file.filename);
    assert.equal(metadata.checksumMd5, file.checksumMd5);
  }
  const mainRuntime = mainMetadata.runtime.find((file) => file.filename === runtimePath);
  assert.equal(mainRuntime.bodyType, 'OnlineStoreThemeFileBodyUrl');
  assert.equal(mainRuntime.checksumMd5, '61ded53111ee5002eb5c37b42a2c4b3f');
  assert.equal(existsSync(new URL(`./source/main/${runtimePath}`, import.meta.url)), false);
  assert.notEqual(md5(runtime), mainRuntime.checksumMd5, 'Different checksums do not reveal MAIN runtime contents');
});

test('V7 runtime/data assets and PDP data-generating templates remain byte-identical to preview metadata', () => {
  assert.equal(sourceBefore.data.preview.id, 'gid://shopify/OnlineStoreTheme/137888792673');
  assert.equal(sourceBefore.data.preview.role, 'UNPUBLISHED');
  const assets = sourceBefore.data.preview.files.nodes.filter((file) => file.filename.startsWith('assets/') && /\.(?:js|json)$/.test(file.filename));
  assert.equal(assets.length, 44);
  const templates = [
    'sections/main-product.liquid',
    'snippets/product-desktop-ux.liquid',
    'snippets/pdp-purchase-confidence.liquid',
    'snippets/product-page-copy-map.liquid',
  ];
  for (const file of [...assets, ...templates.map((filename) => sourceBefore.data.preview.files.nodes.find((item) => item.filename === filename))]) {
    assert.ok(file, 'Captured template exists');
    const body = readFileSync(new URL(`../candidate/${file.filename}`, import.meta.url));
    assert.equal(md5(body), file.checksumMd5, `${file.filename} remains V7`);
  }
  assert.equal(md5(runtime), '522339c5825769c499e1ad1488b8a138');
  assert.match(section, /<script src="\{\{ 'product-desktop-ux-20260513-ruler-sync\.js' \| asset_url \}\}" defer="defer"><\/script>/);
});

test('V8 proposal contains six locale overlays and the separately-owned footer only', () => {
  assert.deepEqual(filesBelow(new URL('./proposed/', import.meta.url)), [
    'locales/de.json', 'locales/el.json', 'locales/fi.json', 'locales/nl.json',
    'locales/ro-RO.json', 'locales/ro.json', 'sections/footer.liquid',
  ]);
  assert.equal(read('../candidate/locales/ro.json'), beforeText);
  const file = sourceBefore.data.preview.files.nodes.find((item) => item.filename === 'locales/ro.json');
  assert.equal(md5(beforeText), file.checksumMd5);
});

for (const locale of ['ro', 'ro-RO', 'en', 'es', 'ja', 'ar']) {
  test(`existing V7 runtime resolves ${locale} and returns its five exact guidance labels`, () => {
    const h = runtimeHarness(locale);
    const root = locale === 'ro-RO' ? 'ro' : locale;
    try {
      assert.equal(h.api.getLocaleRoot(), root);
      assert.deepEqual(guidanceKeys.map((key) => h.api.uiLabel(key, 'UNEXPECTED FALLBACK')), guidance[root]);
    } finally {
      h.close();
    }
  });
}

test('Romanian locale normalization and existing dynamic-label/fallback behavior remain intact', () => {
  const h = runtimeHarness(' RO_ro ');
  try {
    assert.equal(h.api.getLocaleRoot(), 'ro');
    assert.equal(h.api.uiLabel('chooseRoleStep'), guidance.ro[0]);
    assert.equal(h.api.uiLabel('addRole', '', { role: 'Mamă & Copil' }), '+ Adaugă Mamă & Copil');
    assert.equal(h.api.uiLabel('unlistedLabel', 'Detalii {role}', { role: 'Copil' }), 'Detalii Copil');
    h.api.document.documentElement.lang = '';
    assert.equal(h.api.getLocaleRoot(), 'en');
    assert.equal(h.api.uiLabel('chooseOptionsStep'), guidance.en[1]);
  } finally {
    h.close();
  }
});

for (const [key, [english, romanian]] of Object.entries(translations)) {
  test(`Romanian ${key} preserves the captured source meaning and uses the existing translation binding`, () => {
    assert.equal(before.products.purchase_confidence[key], english);
    assert.equal(mainRo.products.purchase_confidence[key], english);
    assert.equal(proposed.products.purchase_confidence[key], romanian);
    const binding = `'${confidencePath}${key}' | t`;
    assert.ok(confidenceSnippet.includes(binding), `V7 consumes ${binding}`);
    assert.ok(mainConfidenceSnippet.includes(binding), `MAIN source consumes ${binding}`);
  });
}

test('exactly seven Romanian leaves change; every other value, number, URL, and placeholder is preserved', () => {
  const oldLeaves = leaves(before);
  const newLeaves = leaves(proposed);
  assert.deepEqual(Object.keys(newLeaves).sort(), Object.keys(oldLeaves).sort());
  const changed = Object.keys(oldLeaves).filter((key) => oldLeaves[key] !== newLeaves[key]).sort();
  assert.deepEqual(changed, Object.keys(translations).map((key) => confidencePath + key).sort());
  const restored = structuredClone(proposed);
  for (const key of Object.keys(translations)) restored.products.purchase_confidence[key] = before.products.purchase_confidence[key];
  assert.deepEqual(restored, before, 'All other JSON structure and leaves are unchanged');
  const tokens = (value) => String(value).match(/\{\{[\s\S]*?\}\}|\{[A-Za-z_][A-Za-z0-9_]*\}|https?:\/\/[^\s"'<>]+|\/policies\/[A-Za-z0-9_-]+|\d+(?:[.,]\d+)*/g) || [];
  for (const key of Object.keys(oldLeaves)) {
    assert.deepEqual(tokens(newLeaves[key]), tokens(oldLeaves[key]), `${key} preserves protected tokens`);
  }
});

test('V8 preserves V7 qualified return deadlines, conditions, exclusions, damage process, and shipping responsibility', () => {
  const facts = {
    returns_headline: 'Returul articolelor eligibile',
    returns_summary: 'Solicitați returul sau schimbul articolelor eligibile în termen de 30 de zile de la livrare.',
    returns_eligible: 'Articolele eligibile trebuie să fie nepurtate, nespălate și returnate cu etichetele atașate.',
    returns_exclusions: 'Costumele de baie, lenjeria intimă, articolele vândute fără drept de retur și cardurile cadou sunt excluse. Consultați politica integrală pentru condiții și excepții.',
    returns_damaged: 'Articol deteriorat sau defect? Contactați serviciul de asistență în termen de 7 zile și atașați fotografii.',
    returns_shipping: 'Transportul returului este plătit de client, cu excepția cazului în care articolul a sosit deteriorat sau defect.',
  };
  for (const [key, value] of Object.entries(facts)) {
    assert.equal(before.products.purchase_confidence[key], value, `${key} was already in V7`);
    assert.equal(proposed.products.purchase_confidence[key], value, `${key} is unchanged by V8`);
  }
  for (const policy of ['shipping-policy', 'refund-policy', 'privacy-policy']) {
    assert.ok(confidenceSnippet.includes(`append: 'policies/${policy}'`));
    assert.ok(confidenceSnippet.includes(`append: '/policies/${policy}'`));
  }
});

test('captured MAIN English returns differ from the qualified Romanian V7 source, not from a new V8 policy change', () => {
  const pdp = renderedMain.pages.find((page) => page.lang === 'ro' && page.url?.includes('/products/together-heart-family-matching-sweaters'));
  assert.ok(pdp);
  assert.equal(renderedMain.main_binding.theme_id, '133290917985');
  assert.equal(renderedMain.main_binding.role, 'main');
  assert.deepEqual(pdp.untranslated_buying_text, [guidance.en[0], guidance.en[1], '30-day returns & exchanges', 'Secure checkout']);
  assert.equal(mainRo.products.purchase_confidence.returns_headline, '30-day returns & exchanges');
  assert.equal(mainRo.products.purchase_confidence.returns_summary, 'This item is returnable if unworn, unwashed, and tags are attached.');
  assert.equal(mainRo.products.purchase_confidence.returns_exclusions, 'Final-sale, personalized, swimwear, and intimate items may be excluded.');
  for (const key of ['returns_headline', 'returns_summary', 'returns_eligible', 'returns_exclusions']) {
    assert.notEqual(before.products.purchase_confidence[key], mainRo.products.purchase_confidence[key]);
    assert.equal(proposed.products.purchase_confidence[key], before.products.purchase_confidence[key]);
  }
});

test('ro-RO overlay is footer-only; runtime language fallback does not imply its purchase-confidence JSON is translated', () => {
  const regionalBefore = parseLocale(read('./rollback/locales/ro-RO.json'));
  const regionalAfter = parseLocale(read('./proposed/locales/ro-RO.json'));
  assert.deepEqual(regionalAfter.products.purchase_confidence, regionalBefore.products.purchase_confidence);
  assert.equal(regionalAfter.products.purchase_confidence.returns_headline, '30-day returns & exchanges');
  assert.equal(regionalAfter.products.purchase_confidence.security_headline, 'Secure checkout');
  const restored = structuredClone(regionalAfter);
  restored.sections.footer_headings = regionalBefore.sections.footer_headings;
  assert.deepEqual(restored, regionalBefore);
});
