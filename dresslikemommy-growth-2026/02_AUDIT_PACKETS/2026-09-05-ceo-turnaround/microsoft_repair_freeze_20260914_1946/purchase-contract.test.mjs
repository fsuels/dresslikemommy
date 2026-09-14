import test from 'node:test';
import assert from 'node:assert/strict';
import { createPurchaseContract, privacyAllowsTracking } from './purchase-contract.mjs';

// Synthetic fixtures only. No SDK, fetch, account identifiers or real orders.
const ALLOWED = { analyticsProcessingAllowed: true, marketingAllowed: true, saleOfDataAllowed: true };
const DENIED = { analyticsProcessingAllowed: false, marketingAllowed: false, saleOfDataAllowed: false };
const START = 1_800_000_000_000;
const DAY = 86_400_000;
function event(id = 'gid://shopify/Order/TEST-ONE', amount = 47.25, currency = 'EUR') {
  return {
    name: 'checkout_completed', id: 'SYNTHETIC-CUSTOMER-EVENT-ID',
    data: { checkout: {
      order: { id }, currencyCode: currency, totalPrice: { amount, currencyCode: currency },
      subtotalPrice: { amount: 40, currencyCode: currency },
      totalTax: { amount: 4, currencyCode: currency },
      discountsAmount: { amount: 5, currencyCode: currency },
      email: 'synthetic@example.invalid', token: 'SYNTHETIC-DO-NOT-FORWARD',
    } },
    context: { window: { location: { href: 'https://example.invalid/checkout?token=SYNTHETIC' } } },
  };
}
function memoryStore() {
  const values = new Map();
  return {
    values, reads: 0, writes: 0,
    async getItem(key) { this.reads += 1; return values.get(key) ?? null; },
    async setItem(key, value) { this.writes += 1; values.set(key, value); return value; },
  };
}
function setup(options = {}) {
  const storage = options.storage ?? memoryStore();
  const calls = [];
  const contract = createPurchaseContract({
    shopHost: 'example.invalid', environment: 'test', tagId: '00000000',
    initialPrivacy: ALLOWED, storage, now: () => START,
    enqueue: (...args) => { calls.push(args); return 'queued'; },
    ...options,
  });
  contract.markPrivacySourceReady();
  return { contract, storage, calls };
}
function storedRecord(storage) { return JSON.parse([...storage.values.values()][0]).entries[0]; }
function deferred() {
  let resolve;
  const promise = new Promise((finish) => { resolve = finish; });
  return { promise, resolve };
}

test('explicit permission is required for every declared purpose; preferences are not substituted', () => {
  for (const value of [undefined, null, {}, DENIED]) assert.equal(privacyAllowsTracking(value), false);
  for (const purpose of Object.keys(ALLOWED)) {
    for (const invalid of [undefined, null, false, 'true', 1]) {
      assert.equal(privacyAllowsTracking({ ...ALLOWED, [purpose]: invalid }), false);
    }
  }
  assert.equal(privacyAllowsTracking({ ...ALLOWED, preferencesProcessingAllowed: false }), true);
});

test('denied event uses no storage or queue and is not replayed after grant', async () => {
  const { contract, calls, storage } = setup({ initialPrivacy: DENIED });
  assert.equal(contract.canInitializeTransport(), false);
  assert.equal((await contract.purchase(event())).status, 'DEFINITELY_UNSENT');
  contract.updatePrivacy(ALLOWED);
  assert.equal(contract.canInitializeTransport(), true);
  assert.equal(storage.reads, 0); assert.equal(storage.writes, 0); assert.equal(calls.length, 0);
});

test('privacy subscription readiness is mandatory even when initial permissions allow', async () => {
  const { contract, calls, storage } = setup();
  contract.invalidatePrivacySource();
  assert.equal(contract.canInitializeTransport(), false);
  await contract.purchase(event());
  assert.equal(storage.reads, 0); assert.equal(calls.length, 0);
});

test('checkout total is unchanged; no double discount, cent conversion, URL or personal field forwarding', async () => {
  const { contract, calls, storage } = setup();
  const outcome = await contract.purchase(event());
  assert.deepEqual(outcome, { status: 'QUEUED_UNCONFIRMED', reason: 'QUEUED_UNCONFIRMED', receiverReceipt: 'NOT_OBSERVED' });
  const [name, payload] = calls[0];
  assert.equal(name, 'purchase'); assert.equal(payload.revenue_value, 47.25); assert.equal(payload.currency, 'EUR');
  assert.equal(payload.ecomm_pagetype, 'purchase');
  assert.match(payload.transaction_id, /^[a-f0-9]{64}$/);
  assert.equal(payload.event_id, `purchase_${payload.transaction_id}`);
  assert.deepEqual(Object.keys(payload).sort(), ['currency', 'ecomm_pagetype', 'event_id', 'revenue_value', 'transaction_id']);
  assert.doesNotMatch(JSON.stringify([payload, outcome, [...storage.values.values()]]), /TEST-ONE|synthetic@|DO-NOT-FORWARD|checkout\?/);
});

test('zero and fractional amounts are preserved without assuming two currency decimal places', async () => {
  const { contract, calls } = setup();
  await contract.purchase(event('ZERO', 0, 'USD'));
  await contract.purchase(event('JPY', 1000, 'JPY'));
  await contract.purchase(event('KWD', 1.234, 'KWD'));
  assert.deepEqual(calls.map(([, payload]) => [payload.revenue_value, payload.currency]), [[0, 'USD'], [1000, 'JPY'], [1.234, 'KWD']]);
});

test('invalid event identity, amount, and currency are discarded before storage', async () => {
  const fixtures = [];
  fixtures.push({ ...event(), name: 'checkout_started' });
  for (const id of [null, '', ' padded ', 42]) fixtures.push(event(id));
  const missingId = event(); delete missingId.data.checkout.order.id; fixtures.push(missingId);
  for (const amount of [null, '47.25', -1, NaN, Infinity]) fixtures.push(event('BAD', amount));
  for (const currency of [null, 'eur', 'US', 'USD ', 3]) fixtures.push(event('BAD', 10, currency));
  const mismatch = event(); mismatch.data.checkout.currencyCode = 'USD'; fixtures.push(mismatch);
  const missingMoney = event(); delete missingMoney.data.checkout.totalPrice; fixtures.push(missingMoney);
  const { contract, storage, calls } = setup();
  for (const fixture of fixtures) assert.equal((await contract.purchase(fixture)).status, 'DEFINITELY_UNSENT');
  assert.equal(storage.reads, 0); assert.equal(calls.length, 0);
});

test('concurrent calls and changed Shopify event IDs for one order enqueue once in one instance', async () => {
  const { contract, calls } = setup();
  const first = event(); const second = event(); second.id = 'DIFFERENT-SYNTHETIC-EVENT';
  const outcomes = await Promise.all([contract.purchase(first), contract.purchase(second)]);
  assert.equal(calls.length, 1);
  assert.deepEqual(outcomes.map(({ status }) => status), ['QUEUED_UNCONFIRMED', 'SUPPRESSED']);
});

test('snapshot protects pending value and order identity from later input mutation', async () => {
  const { contract, calls } = setup();
  const input = event(); const pending = contract.purchase(input);
  input.data.checkout.totalPrice.amount = 999; input.data.checkout.order.id = 'MUTATED';
  await pending;
  assert.equal(calls[0][1].revenue_value, 47.25);
  assert.equal((await contract.purchase(event())).status, 'SUPPRESSED');
});

test('reload suppresses the same order and distinct orders remain distinct', async () => {
  const storage = memoryStore(); const first = setup({ storage });
  await first.contract.purchase(event());
  const second = setup({ storage });
  assert.equal((await second.contract.purchase(event())).status, 'SUPPRESSED');
  await second.contract.purchase(event('DISTINCT'));
  assert.equal(second.calls.length, 1);
  assert.notEqual(first.calls[0][1].transaction_id, second.calls[0][1].transaction_id);
});

test('identity is stable and namespaced by shop, environment and tag', async () => {
  const outcomes = [];
  for (const options of [{}, {}, { shopHost: 'another.invalid' }, { environment: 'production' }, { tagId: '00000001' }]) {
    const { contract, calls } = setup(options); await contract.purchase(event()); outcomes.push(calls[0][1]);
  }
  assert.deepEqual(outcomes[0], outcomes[1]);
  assert.equal(new Set(outcomes.map((payload) => payload.transaction_id)).size, 4);
});

test('same order with changed value or currency requires reconciliation', async () => {
  const { contract, calls } = setup();
  await contract.purchase(event());
  assert.equal((await contract.purchase(event(undefined, 48))).reason, 'ORDER_VALUE_CONFLICT');
  assert.equal((await contract.purchase(event(undefined, 47.25, 'USD'))).reason, 'ORDER_VALUE_CONFLICT');
  assert.equal(calls.length, 1);
});

test('revocation and regrant during async read invalidate the original consent ticket', async () => {
  const storage = memoryStore(); const entered = deferred(); const finish = deferred();
  storage.getItem = async () => { entered.resolve(); await finish.promise; return null; };
  const { contract, calls } = setup({ storage }); const pending = contract.purchase(event());
  await entered.promise; contract.updatePrivacy(DENIED); contract.updatePrivacy(ALLOWED); finish.resolve();
  assert.equal((await pending).reason, 'CONSENT_CHANGED_DURING_READ');
  assert.equal(storage.writes, 0); assert.equal(calls.length, 0);
});

test('revocation during reservation prevents enqueue; a reload holds the unresolved reservation', async () => {
  const storage = memoryStore(); const write = storage.setItem.bind(storage);
  const entered = deferred(); const finish = deferred();
  storage.setItem = async (...args) => { await write(...args); entered.resolve(); await finish.promise; };
  const { contract, calls } = setup({ storage }); const pending = contract.purchase(event());
  await entered.promise; contract.updatePrivacy(DENIED); finish.resolve();
  assert.equal((await pending).reason, 'CONSENT_CHANGED_AFTER_RESERVATION');
  assert.equal(calls.length, 0); assert.equal(storedRecord(storage).state, 'reserved');
  assert.equal((await setup({ storage }).contract.purchase(event())).reason, 'EXISTING_RESERVED');
});

test('storage rejection before reserve, ambiguous reserve write, and corrupt data cannot send', async () => {
  const variants = [
    { getItem: async () => { throw new Error('synthetic'); }, setItem: async () => {} },
    { getItem: async () => null, setItem: async () => { throw new Error('synthetic'); } },
    { getItem: async () => '{corrupt', setItem: async () => {} },
  ];
  for (const storage of variants) {
    const { contract, calls } = setup({ storage });
    assert.equal((await contract.purchase(event())).status, 'DEFINITELY_UNSENT');
    assert.equal((await contract.purchase(event('SECOND'))).reason, 'STORAGE_UNCERTAIN');
    assert.equal(calls.length, 0);
  }
});

test('array-coerced ledger key or fingerprint is corruption, never a fresh order', async () => {
  for (const field of ['key', 'fingerprint']) {
    const storage = memoryStore(); await setup({ storage }).contract.purchase(event());
    const [storageKey, raw] = [...storage.values.entries()][0];
    const ledger = JSON.parse(raw); ledger.entries[0][field] = [ledger.entries[0][field]];
    storage.values.set(storageKey, JSON.stringify(ledger));
    const { contract, calls } = setup({ storage });
    assert.equal((await contract.purchase(event())).reason, 'STORAGE_OR_CLOCK_UNAVAILABLE');
    assert.equal(calls.length, 0);
  }
});

test('stalled storage has bounded admission and all admitted calls settle by deadline', { timeout: 2000 }, async () => {
  const storage = memoryStore(); const entered = deferred(); let reads = 0;
  storage.getItem = () => { reads += 1; entered.resolve(); return new Promise(() => {}); };
  const { contract, calls } = setup({ storage, maximumPending: 2, operationDeadlineMs: 100 });
  const first = contract.purchase(event()); await entered.promise;
  const rest = Array.from({ length: 250 }, (_, index) => contract.purchase(event(`PENDING-${index}`)));
  const outcomes = await Promise.all([first, ...rest]);
  assert.equal(outcomes.filter(({ reason }) => reason === 'PENDING_LIMIT_REACHED').length, 249);
  assert.equal(outcomes[0].reason, 'OPERATION_DEADLINE_EXPIRED');
  assert.equal(outcomes[1].reason, 'STORAGE_UNCERTAIN');
  assert.equal(reads, 1); assert.equal(calls.length, 0);
  assert.equal((await contract.purchase(event('LATER'))).reason, 'STORAGE_UNCERTAIN');
});

test('a storage read that completes after timeout cannot reserve or dispatch', { timeout: 2000 }, async () => {
  const storage = memoryStore(); const entered = deferred(); const finish = deferred();
  storage.getItem = async () => { entered.resolve(); await finish.promise; return null; };
  const { contract, calls } = setup({ storage, operationDeadlineMs: 50 });
  const pending = contract.purchase(event()); await entered.promise;
  assert.equal((await pending).reason, 'OPERATION_DEADLINE_EXPIRED');
  finish.resolve(); await new Promise(setImmediate);
  assert.equal(storage.writes, 0); assert.equal(calls.length, 0);
});

test('a late reservation write is preserved after timeout and cannot dispatch', { timeout: 2000 }, async () => {
  const storage = memoryStore(); const write = storage.setItem.bind(storage);
  const entered = deferred(); const finish = deferred();
  storage.setItem = async (...args) => { entered.resolve(); await finish.promise; return write(...args); };
  const { contract, calls } = setup({ storage, operationDeadlineMs: 50 });
  const pending = contract.purchase(event()); await entered.promise;
  assert.equal((await pending).status, 'DEFINITELY_UNSENT');
  assert.equal(storage.values.size, 0);
  finish.resolve(); await new Promise(setImmediate);
  assert.equal(storedRecord(storage).state, 'reserved'); assert.equal(calls.length, 0);
  assert.equal((await setup({ storage }).contract.purchase(event())).reason, 'EXISTING_RESERVED');
});

test('timeout after a queue attempt remains delivery-uncertain and does not retry', { timeout: 2000 }, async () => {
  const storage = memoryStore(); const write = storage.setItem.bind(storage); let writes = 0;
  storage.setItem = async (...args) => {
    writes += 1; if (writes === 2) return new Promise(() => {}); return write(...args);
  };
  const { contract, calls } = setup({ storage, operationDeadlineMs: 50 });
  const outcome = await contract.purchase(event());
  assert.equal(outcome.status, 'DELIVERY_UNCERTAIN'); assert.equal(outcome.reason, 'OPERATION_DEADLINE_EXPIRED');
  assert.equal(storedRecord(storage).state, 'reserved'); assert.equal(calls.length, 1);
  assert.equal((await contract.purchase(event())).reason, 'STORAGE_UNCERTAIN');
});

test('queue exceptions are uncertain, remain recorded durably and cannot trigger blind resend', async () => {
  let attempts = 0;
  const { contract, storage } = setup({ enqueue: () => { attempts += 1; throw new Error('may have dispatched'); } });
  assert.equal((await contract.purchase(event())).status, 'DELIVERY_UNCERTAIN');
  assert.equal(storedRecord(storage).state, 'delivery_uncertain');
  assert.equal((await contract.purchase(event())).status, 'SUPPRESSED');
  assert.equal((await setup({ storage }).contract.purchase(event())).status, 'SUPPRESSED');
  assert.equal(attempts, 1);
});

test('explicit adapter non-dispatch is definitely unsent but not automatically retried', async () => {
  let attempts = 0;
  const { contract, storage } = setup({ enqueue: () => { attempts += 1; return 'not_queued'; } });
  assert.equal((await contract.purchase(event())).status, 'DEFINITELY_UNSENT');
  assert.equal(storedRecord(storage).state, 'definitely_unsent');
  assert.equal((await contract.purchase(event())).reason, 'EXISTING_DEFINITELY_UNSENT');
  assert.equal(attempts, 1);
});

test('unsupported async queue result is uncertain, including rejected promises', async () => {
  const { contract, storage } = setup({ enqueue: async () => { throw new Error('synthetic'); } });
  assert.equal((await contract.purchase(event())).status, 'DELIVERY_UNCERTAIN');
  assert.equal(storedRecord(storage).state, 'delivery_uncertain');
});

test('revocation during adapter invocation cannot undo a queue attempt or justify receipt', async () => {
  let control;
  const { contract, storage } = setup({ enqueue: () => { control.updatePrivacy(DENIED); return 'queued'; } });
  control = contract;
  const outcome = await contract.purchase(event());
  assert.equal(outcome.reason, 'CONSENT_CHANGED_DURING_QUEUE');
  assert.equal(outcome.receiverReceipt, 'NOT_OBSERVED');
  assert.equal(storedRecord(storage).state, 'reserved');
});

test('failed final persistence preserves the reservation and holds later sends', async () => {
  const storage = memoryStore(); const write = storage.setItem.bind(storage); let writes = 0;
  storage.setItem = async (...args) => { writes += 1; if (writes === 2) throw new Error('synthetic'); return write(...args); };
  const { contract, calls } = setup({ storage });
  assert.equal((await contract.purchase(event())).reason, 'QUEUE_STATE_WRITE_UNCERTAIN');
  assert.equal(storedRecord(storage).state, 'reserved'); assert.equal(calls.length, 1);
  assert.equal((await contract.purchase(event('SECOND'))).reason, 'STORAGE_UNCERTAIN');
});

test('capacity and expiry hold records; neither silently evicts or resends', async () => {
  const storage = memoryStore(); const first = setup({ storage, maximumRecords: 1 });
  await first.contract.purchase(event());
  assert.equal((await first.contract.purchase(event('SECOND'))).reason, 'CAPACITY_REQUIRES_RECONCILIATION');
  const expired = setup({ storage, maximumRecords: 1, now: () => START + 90 * DAY });
  assert.equal((await expired.contract.purchase(event())).reason, 'EXPIRED_RECORD_REQUIRES_RECONCILIATION');
  assert.equal((await expired.contract.purchase(event('NEW-AFTER-EXPIRY'))).reason, 'EXPIRED_RECORD_REQUIRES_RECONCILIATION');
  assert.equal(expired.calls.length, 0); assert.equal(storage.values.size, 1);
});

test('clock rollback fails closed rather than discarding a future-dated record', async () => {
  const storage = memoryStore(); await setup({ storage }).contract.purchase(event());
  const { contract, calls } = setup({ storage, now: () => START - 1 });
  assert.equal((await contract.purchase(event())).reason, 'STORAGE_OR_CLOCK_UNAVAILABLE');
  assert.equal(calls.length, 0);
});

test('known limitation: two tabs can both read an empty ledger and enqueue the same order', async () => {
  const storage = memoryStore(); const barrier = deferred(); let reads = 0;
  storage.getItem = async (key) => {
    const snapshot = storage.values.get(key) ?? null; reads += 1;
    if (reads === 2) barrier.resolve(); await barrier.promise; return snapshot;
  };
  const first = setup({ storage }); const second = setup({ storage });
  const outcomes = await Promise.all([first.contract.purchase(event()), second.contract.purchase(event())]);
  assert.deepEqual(outcomes.map(({ status }) => status), ['QUEUED_UNCONFIRMED', 'QUEUED_UNCONFIRMED']);
  assert.equal(first.calls.length + second.calls.length, 2);
  assert.equal(first.calls[0][1].event_id, second.calls[0][1].event_id);
});

test('known limitation: concurrent distinct-tab writes can lose a reservation', async () => {
  const storage = memoryStore(); const barrier = deferred(); let reads = 0;
  storage.getItem = async (key) => {
    const snapshot = storage.values.get(key) ?? null; reads += 1;
    if (reads === 2) barrier.resolve(); await barrier.promise; return snapshot;
  };
  const first = setup({ storage }); const second = setup({ storage });
  await Promise.all([first.contract.purchase(event('TAB-A')), second.contract.purchase(event('TAB-B'))]);
  assert.equal(first.calls.length + second.calls.length, 2);
  assert.equal(JSON.parse([...storage.values.values()][0]).entries.length, 1);
});
