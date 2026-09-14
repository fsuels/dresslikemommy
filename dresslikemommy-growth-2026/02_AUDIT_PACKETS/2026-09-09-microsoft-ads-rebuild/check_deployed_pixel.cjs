// Offline analysis of the exact downloaded public app bundle. Network is mocked.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { webcrypto } = require('node:crypto');
const source = fs.readFileSync(path.join(__dirname, 'microsoft_deployed_app_pixel.js'), 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));
const drain = async () => { for (let i = 0; i < 12; i++) await tick(); };
const context = {
  window: { location: { href: 'https://www.dresslikemommy.com/collections/mommy-and-me', pathname: '/collections/mommy-and-me', search: '' }, screen: { width: 390, height: 844 } },
  document: { referrer: '', title: 'Offline synthetic fixture' },
  navigator: { language: 'en-US' }
};
function store() {
  const values = new Map();
  return { getItem: async key => values.get(key) ?? null, setItem: async (key, value) => values.set(key, value), removeItem: async key => values.delete(key) };
}
async function run(currency, beforePage = false, repeat = false) {
  const handlers = {}, requests = [], cookieCalls = [];
  const api = {
    settings: { ti: '36005151', endpoint: 'https://bat.bing.com/action/0' },
    init: { context },
    browser: { localStorage: store(), sessionStorage: store(), cookie: { get: async () => null, set: async (...args) => cookieCalls.push(args) } },
    analytics: { subscribe: (name, handler) => { handlers[name] = handler; } }
  };
  vm.runInNewContext(source, {
    shopify: { extend: (event, callback) => { assert.equal(event, 'WebPixel::Render'); callback(api); } },
    URLSearchParams, Date, Math, Uint8Array, crypto: webcrypto,
    fetch: async (url, options) => { requests.push({ url, method: options.method }); return { ok: true }; }
  }, { timeout: 1000 });
  const event = { id: 'offline-fixture-event', clientId: 'offline-client', context, data: { checkout: {
    order: { id: 'offline-order' }, currencyCode: currency,
    subtotalPrice: { amount: 42.50, currencyCode: currency },
    totalPrice: { amount: 52.95, currencyCode: currency },
    lineItems: [ { variant: { id: 'fixture-variant', product: { id: 'fixture-product' } } } ]
  } } };
  if (beforePage) { handlers.checkout_completed(event); await drain(); assert.equal(requests.length, 0); }
  handlers.page_viewed(event); await drain();
  if (!beforePage) { handlers.checkout_completed(event); await drain(); }
  if (repeat) { handlers.checkout_completed(event); await drain(); }
  const parsed = requests.map(r => ({ ...Object.fromEntries(new URL(r.url).searchParams), method: r.method, host: new URL(r.url).hostname }));
  const purchases = parsed.filter(r => r.ea === 'purchase');
  assert.equal(purchases.length, repeat ? 2 : 1);
  for (const p of purchases) {
    assert.equal(p.ti, '36005151'); assert.equal(p.gv, '42.5'); assert.equal(p.gc, currency);
    assert.equal(p.pagetype, 'purchase'); assert.equal(p.evt, 'custom');
    assert.equal(p.host, 'bat.bing.com'); assert.equal(p.method, 'GET');
    assert.equal(p.prodid, 'fixture-product_fixture-variant');
  }
  return { currency, beforePage, repeat, requestCount: parsed.length, purchaseCount: purchases.length,
    purchaseFields: Object.keys(purchases[0]).sort(), value: purchases[0].gv,
    consentFieldPresent: 'asc' in purchases[0] || 'ad_storage' in purchases[0],
    transactionIdPresent: ['transaction_id', 'order_id', 'event_id'].some(k => k in purchases[0]),
    cookieCalls: cookieCalls.length };
}
(async () => {
  const cases = [];
  for (const currency of ['USD','EUR','GBP','CAD','AUD','DKK','PLN','CZK','RON','JPY']) cases.push(await run(currency));
  cases.push(await run('EUR', true));
  cases.push(await run('USD', false, true));
  const report = { captured_at_utc: new Date().toISOString(), status: 'PASS', scenarios: cases.length,
    scope: 'Offline VM, downloaded deployed app bundle, synthetic fixtures and mocked fetch/storage only. No event was sent to Microsoft; no order was placed.',
    findings: ['Purchase maps subtotal to gv and currency to gc, not a constant one.', 'Purchase queues until page_viewed initializes the sender.', 'Replaying the same checkout event emits a second request in this bundle.', 'No asc/ad_storage or order/event deduplication field appears in the captured purchase payload. Shopify broker gating and receiver behavior are outside this test.'],
    limitations: ['No live receipt, attribution, browser consent or Shopify sandbox integration proof.', 'Mock cookie calls do not validate the Shopify cookie API or cross-page persistence.'], cases };
  fs.writeFileSync(path.join(__dirname, 'deployed_pixel_offline_test.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ status: report.status, scenarios: cases.length, externalRequests: 0, report: 'deployed_pixel_offline_test.json' }));
})().catch(error => { console.error(error); process.exitCode = 1; });
