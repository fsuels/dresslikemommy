// OFFLINE REPAIR CANDIDATE. No SDK, network, installation or automatic subscription.
// Integrating this module does not disconnect or repair Shopify's installed app.

const PURPOSES = ['analyticsProcessingAllowed', 'marketingAllowed', 'saleOfDataAllowed'];
const STATES = new Set(['reserved', 'definitely_unsent', 'queued_unconfirmed', 'delivery_uncertain']);
const DAY = 86_400_000;
const HEX = /^[a-f0-9]{64}$/;

export function privacyAllowsTracking(privacy) {
  return PURPOSES.every((purpose) => privacy?.[purpose] === true);
}

function privacySnapshot(privacy) {
  return Object.fromEntries(PURPOSES.map((purpose) => [purpose, privacy?.[purpose] === true]));
}

export async function sha256(value) {
  const bytes = new TextEncoder().encode(value);
  const hash = await globalThis.crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, '0')).join('');
}

function result(status, reason = status) {
  // No order IDs, amounts, URLs or customer fields in diagnostic results.
  return { status, reason, receiverReceipt: 'NOT_OBSERVED' };
}

function readPurchase(event) {
  if (event?.name !== 'checkout_completed') return { error: 'WRONG_EVENT' };
  const checkout = event?.data?.checkout;
  const orderId = checkout?.order?.id;
  if (typeof orderId !== 'string' || orderId.length === 0 || orderId.trim() !== orderId) {
    return { error: 'MISSING_OR_INVALID_ORDER_ID' };
  }
  const total = checkout?.totalPrice;
  if (typeof total?.amount !== 'number' || !Number.isFinite(total.amount) || total.amount < 0) {
    return { error: 'INVALID_TOTAL' };
  }
  if (typeof total.currencyCode !== 'string' || !/^[A-Z]{3}$/.test(total.currencyCode)) {
    return { error: 'INVALID_CURRENCY' };
  }
  if (checkout.currencyCode != null && checkout.currencyCode !== total.currencyCode) {
    return { error: 'CURRENCY_CONFLICT' };
  }
  return { orderId, value: total.amount, currency: total.currencyCode };
}

function decodeLedger(raw, maximumRecords, now) {
  if (raw === null) return { version: 1, entries: [] };
  if (typeof raw !== 'string' || raw.length > maximumRecords * 512 + 100) throw new Error('ledger');
  const ledger = JSON.parse(raw);
  if (ledger?.version !== 1 || !Array.isArray(ledger.entries) || ledger.entries.length > maximumRecords) {
    throw new Error('ledger');
  }
  const keys = new Set();
  for (const entry of ledger.entries) {
    if (typeof entry?.key !== 'string' || typeof entry?.fingerprint !== 'string'
      || !HEX.test(entry.key) || !HEX.test(entry.fingerprint) || !STATES.has(entry?.state)
      || !Number.isSafeInteger(entry?.createdAt) || entry.createdAt < 0 || entry.createdAt > now
      || !Number.isSafeInteger(entry?.updatedAt) || entry.updatedAt < entry.createdAt || entry.updatedAt > now
      || keys.has(entry.key)) throw new Error('ledger');
    keys.add(entry.key);
  }
  return ledger;
}

export function createPurchaseContract({
  shopHost,
  environment,
  tagId,
  initialPrivacy,
  storage,
  enqueue,
  now = Date.now,
  maximumRecords = 100,
  maximumAgeMs = 90 * DAY,
  maximumPending = 8,
  operationDeadlineMs = 5000,
}) {
  if (typeof shopHost !== 'string' || !/^[a-z0-9.-]+$/.test(shopHost)
    || !['test', 'production'].includes(environment) || !/^\d+$/.test(tagId)
    || !storage || typeof storage.getItem !== 'function' || typeof storage.setItem !== 'function'
    || typeof enqueue !== 'function' || typeof now !== 'function'
    || !Number.isSafeInteger(maximumRecords) || maximumRecords < 1 || maximumRecords > 1000
    || !Number.isSafeInteger(maximumAgeMs) || maximumAgeMs < 1
    || !Number.isSafeInteger(maximumPending) || maximumPending < 1 || maximumPending > 100
    || !Number.isSafeInteger(operationDeadlineMs) || operationDeadlineMs < 1 || operationDeadlineMs > 60_000) {
    throw new TypeError('Invalid contract configuration');
  }

  const namespace = ['dlm-uet-purchase-contract-v1', shopHost, environment, String(tagId)];
  const storageKey = namespace.join(':');
  let privacy = privacySnapshot(initialPrivacy);
  let privacyRevision = 0;
  let privacySourceReady = false;
  let serial = Promise.resolve();
  let pending = 0;
  // A storage failure makes this instance unusable for later sends. It may have
  // persisted a reservation even when the API rejected its completion promise.
  let storageUncertain = false;

  function updatePrivacy(next) {
    const snapshot = privacySnapshot(next);
    if (PURPOSES.some((purpose) => snapshot[purpose] !== privacy[purpose])) privacyRevision += 1;
    privacy = snapshot;
  }

  function consentTicket() {
    const revision = privacyRevision;
    return () => privacySourceReady && revision === privacyRevision && privacyAllowsTracking(privacy);
  }

  async function processPurchase(event, current, attempt) {
    if (storageUncertain) return result('HOLD', 'STORAGE_UNCERTAIN');
    if (!current()) return result('DEFINITELY_UNSENT', 'CONSENT_UNAVAILABLE_OR_CHANGED');
    const purchase = readPurchase(event);
    if (purchase.error) return result('DEFINITELY_UNSENT', purchase.error);

    let key;
    let fingerprint;
    try {
      key = await sha256(JSON.stringify([...namespace, 'purchase', purchase.orderId]));
      fingerprint = await sha256(JSON.stringify([purchase.value, purchase.currency]));
    } catch {
      return result('DEFINITELY_UNSENT', 'IDENTITY_UNAVAILABLE');
    }
    if (!current()) return result('DEFINITELY_UNSENT', 'CONSENT_CHANGED_DURING_IDENTITY');

    let ledger;
    let timestamp;
    try {
      const raw = await storage.getItem(storageKey);
      if (!current()) return result('DEFINITELY_UNSENT', 'CONSENT_CHANGED_DURING_READ');
      timestamp = now();
      if (!Number.isSafeInteger(timestamp) || timestamp < 0) throw new Error('clock');
      ledger = decodeLedger(raw, maximumRecords, timestamp);
    } catch {
      storageUncertain = true;
      return result('DEFINITELY_UNSENT', 'STORAGE_OR_CLOCK_UNAVAILABLE');
    }

    if (ledger.entries.some((entry) => timestamp - entry.createdAt >= maximumAgeMs)) {
      return result('HOLD', 'EXPIRED_RECORD_REQUIRES_RECONCILIATION');
    }
    const existing = ledger.entries.find((entry) => entry.key === key);
    if (existing) {
      if (existing.fingerprint !== fingerprint) return result('HOLD', 'ORDER_VALUE_CONFLICT');
      return result('SUPPRESSED', `EXISTING_${existing.state.toUpperCase()}`);
    }
    if (ledger.entries.length >= maximumRecords) return result('HOLD', 'CAPACITY_REQUIRES_RECONCILIATION');

    const entry = { key, fingerprint, state: 'reserved', createdAt: timestamp, updatedAt: timestamp };
    ledger.entries.push(entry);
    if (!current()) return result('DEFINITELY_UNSENT', 'CONSENT_CHANGED_BEFORE_RESERVATION');
    try {
      await storage.setItem(storageKey, JSON.stringify(ledger));
    } catch {
      storageUncertain = true;
      return result('DEFINITELY_UNSENT', 'RESERVATION_WRITE_UNCERTAIN');
    }
    // The SDK adapter must itself honor consent. This gate cannot control its
    // timers, delayed requests, automatic page views or other installed senders.
    if (!current()) return result('DEFINITELY_UNSENT', 'CONSENT_CHANGED_AFTER_RESERVATION');

    const payload = Object.freeze({
      transaction_id: key,
      event_id: `purchase_${key}`,
      revenue_value: purchase.value,
      currency: purchase.currency,
      ecomm_pagetype: 'purchase',
    });
    let state = 'delivery_uncertain';
    try {
      // A synchronous adapter result is an interface contract, not a Microsoft
      // receipt. `not_queued` requires proof that the adapter did not dispatch.
      attempt.dispatchInvoked = true;
      const queueResult = enqueue('purchase', payload);
      if (queueResult === 'queued') state = 'queued_unconfirmed';
      else if (queueResult === 'not_queued') state = 'definitely_unsent';
      else if (queueResult && typeof queueResult.then === 'function') {
        // An unsupported asynchronous adapter must not cause an unhandled rejection.
        Promise.resolve(queueResult).catch(() => {});
      }
    } catch {
      // A throw may occur after dispatch: retain the reservation and do not retry.
    }
    entry.state = state;
    entry.updatedAt = timestamp;
    if (!current()) return result('DELIVERY_UNCERTAIN', 'CONSENT_CHANGED_DURING_QUEUE');
    try {
      await storage.setItem(storageKey, JSON.stringify(ledger));
    } catch {
      storageUncertain = true;
      return result('DELIVERY_UNCERTAIN', 'QUEUE_STATE_WRITE_UNCERTAIN');
    }
    return result(state.toUpperCase());
  }

  return Object.freeze({
    updatePrivacy,
    // Call only after the documented visitorConsentCollected subscription succeeds.
    markPrivacySourceReady() { privacySourceReady = true; },
    invalidatePrivacySource() { privacySourceReady = false; privacyRevision += 1; },
    canInitializeTransport() { return privacySourceReady && privacyAllowsTracking(privacy); },
    purchase(event) {
      const permissionIsCurrent = consentTicket();
      // Events received without consent are discarded, never replayed on a grant.
      if (!permissionIsCurrent()) return Promise.resolve(result('DEFINITELY_UNSENT', 'CONSENT_UNAVAILABLE'));
      if (storageUncertain) return Promise.resolve(result('HOLD', 'STORAGE_UNCERTAIN'));
      if (pending >= maximumPending) return Promise.resolve(result('HOLD', 'PENDING_LIMIT_REACHED'));
      // Snapshot only the fields used by the contract before entering the queue.
      const input = {
        name: event?.name,
        data: { checkout: {
          order: { id: event?.data?.checkout?.order?.id },
          totalPrice: event?.data?.checkout?.totalPrice == null ? null : {
            amount: event.data.checkout.totalPrice.amount,
            currencyCode: event.data.checkout.totalPrice.currencyCode,
          },
          currencyCode: event?.data?.checkout?.currencyCode,
        } },
      };
      pending += 1;
      const attempt = { expired: false, dispatchInvoked: false };
      const current = () => !attempt.expired && !storageUncertain && permissionIsCurrent();
      let timer;
      const deadline = new Promise((resolve) => {
        timer = setTimeout(() => {
          attempt.expired = true;
          storageUncertain = true;
          resolve(result(attempt.dispatchInvoked ? 'DELIVERY_UNCERTAIN' : 'DEFINITELY_UNSENT', 'OPERATION_DEADLINE_EXPIRED'));
        }, operationDeadlineMs);
      });
      const work = serial.then(() => processPurchase(input, current, attempt));
      // The deadline includes time waiting in the serial queue. An expired task
      // may still complete an already-started storage write, but every later
      // dispatch check sees its invalidated ticket. The instance stays on hold.
      const next = Promise.race([work, deadline]).finally(() => {
        clearTimeout(timer);
        pending -= 1;
      });
      serial = next.catch(() => {});
      return next;
    },
  });
}
