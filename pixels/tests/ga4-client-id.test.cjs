const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

// Execute only the actual identity helper. No pixel initialization or transport
// can run, and every identifier below is synthetic.
const sourcePath = process.env.DLM_GA4_TEMPLATE_TEST_SOURCE ||
  path.join(__dirname, '..', 'ga4-custom-pixel.js');
const source = fs.readFileSync(sourcePath, 'utf8');
const start = source.indexOf('  async function getClientId() {');
const end = source.indexOf('  // ===== SESSION ID', start);
assert.ok(start >= 0 && end > start, 'Identity helper boundaries must exist');
const helper = source.slice(start, end);
const key = 'dlm_ga4_client_id';

async function resolve(cookie, stored) {
  const values = new Map(stored === undefined ? [] : [[key, stored]]);
  const cookieReads = [];
  const math = Object.create(Math);
  math.random = () => 0.123456789;
  const getClientId = vm.runInNewContext(`(${helper.trim()})`, {
    CLIENT_ID_STORAGE_KEY: key,
    cookies: { get: async name => { cookieReads.push(name); return cookie; } },
    storage: {
      get: async name => values.get(name),
      set: async (name, value) => values.set(name, value),
    },
    Math: math,
    Date: { now: () => 1700000000000 },
  });
  const result = await getClientId();
  assert.deepEqual(cookieReads, ['_ga']);
  return { result, saved: values.get(key) };
}

// Google MP documents the entire client-ID cookie as an accepted client_id.
// This contract deliberately does not depend on parsing a cookie's components.
for (const cookie of [
  'GA1.1.123456789.1700000000',
  'GA1.2.987654321.1700000001',
  'GA1.1.111111111.1700000002',
  'GA1.1.222222222.1700000003',
]) {
  test(`preserves the complete synthetic cookie ${cookie}`, async () => {
    const actual = await resolve(cookie, '444444444.1600000000');
    assert.equal(actual.result, cookie);
    assert.equal(actual.saved, cookie);
  });
}

test('keeps the existing stored identifier when the cookie is unavailable', async () => {
  const stored = '333333333.1600000000';
  assert.deepEqual(await resolve(null, stored), { result: stored, saved: stored });
});

test('keeps the existing stored identifier when the cookie is empty', async () => {
  const stored = '555555555.1600000000';
  assert.deepEqual(await resolve('', stored), { result: stored, saved: stored });
});

test('retains the fallback identifier behavior without a cookie or stored value', async () => {
  const actual = await resolve(undefined, undefined);
  assert.match(actual.result, /^[1-9]\d*\.[1-9]\d*$/);
  assert.equal(actual.saved, actual.result);
});
