import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const theme = readFileSync(new URL('../../layout/theme.liquid', import.meta.url), 'utf8');
const visibilityClass = 'dlm-shopify-privacy-banner-visible';
const bannerSelectors = ['#shopify-pc__banner', '.shopify-pc__banner__wrapper'];
const preferenceSelectors = [
  '.shopify-pc__prefs',
  '.shopify-pc__prefs__overlay',
  '.shopify-pc__prefs__dialog',
];
const matchingScripts = [...theme.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map((match) => match[1])
  .filter((script) => script.includes(`var visibilityClass = '${visibilityClass}'`));
assert.equal(matchingScripts.length, 1, 'execute exactly one actual theme privacy-gate script');
const script = matchingScripts[0];

// The fixture models independently mounted body descendants. It cannot establish
// Shopify's live dialog ancestry, rendered visibility, consent storage, or events.
function runGate(options = {}) {
  const nodes = [];
  const classes = new Set();
  const observers = [];
  const listeners = new Map();
  const loadRequests = [];
  const append = (selectors) => selectors.map((selector) => {
    const node = {
      selector,
      isConnected: true,
      remove() { this.isConnected = false; },
    };
    nodes.push(node);
    return node;
  });
  const initialBanners = append(bannerSelectors);
  const initialPreferences = append(preferenceSelectors);
  const document = {
    documentElement: {
      classList: {
        add: (name) => classes.add(name),
        contains: (name) => classes.has(name),
      },
    },
    body: options.noBody ? null : {},
    readyState: options.loading ? 'loading' : 'complete',
    querySelectorAll: (selector) => nodes.filter((node) => node.isConnected && node.selector === selector),
    addEventListener: (name, callback, settings) => listeners.set(name, { callback, settings }),
  };
  const window = {};
  if (!options.noShopify) {
    window.Shopify = {
      customerPrivacy: options.noPrivacy ? undefined : {
        shouldShowBanner: options.shouldShowBanner ?? (() => false),
        saleOfDataRegion: options.saleOfDataRegion ?? (() => false),
      },
    };
    if (!options.noLoader) {
      window.Shopify.loadFeatures = (features, callback) => {
        loadRequests.push(features);
        callback(options.loadError);
      };
    }
  }
  class MutationObserver {
    constructor(callback) { this.callback = callback; }
    observe(target, settings) {
      assert.equal(target, document.body);
      assert.equal(settings.childList, true);
      assert.equal(settings.subtree, true);
      observers.push(this);
    }
  }
  runInNewContext(script, { window, document, MutationObserver }, { timeout: 1000 });
  return {
    classes, observers, listeners, loadRequests, initialBanners, initialPreferences, append,
    flushMutations: () => observers.forEach((observer) => observer.callback()),
  };
}

function assertConnected(nodes, expected) {
  for (const node of nodes) {
    assert.equal(node.isConnected, expected, `${node.selector} connected=${expected}`);
  }
}

test('the suppression CSS hides only automatic banner selectors', () => {
  const gateRules = [...theme.matchAll(/([^{}]+)\{([^{}]*)\}/g)]
    .filter((match) => match[1].includes(`html:not(.${visibilityClass})`));
  assert.equal(gateRules.length, 1, 'one automatic-banner suppression rule');
  const selectors = gateRules[0][1].trim().split(',').map((selector) => selector.trim());
  assert.deepEqual(selectors, bannerSelectors.map((selector) => `html:not(.${visibilityClass}) ${selector}`));
  assert.match(gateRules[0][2], /display:\s*none\s*!important/);
  assert.match(gateRules[0][2], /visibility:\s*hidden\s*!important/);
});

test('initial preferences survive while automatic banners remain suppressed', () => {
  const gate = runGate();
  assert.equal(gate.classes.has(visibilityClass), false);
  assert.equal(gate.observers.length, 1);
  assert.equal(gate.loadRequests[0][0].name, 'consent-tracking-api');
  assert.equal(gate.loadRequests[0][0].version, '0.1');
  assertConnected(gate.initialBanners, false);
  assertConnected(gate.initialPreferences, true);
});

test('preferences opened later survive the existing mutation observer', () => {
  const gate = runGate();
  const laterPreferences = gate.append(preferenceSelectors);
  const laterBanners = gate.append(bannerSelectors);
  gate.flushMutations();
  gate.flushMutations();
  assertConnected(laterPreferences, true);
  assertConnected(laterBanners, false);
  assert.equal(gate.classes.has(visibilityClass), false);
});

for (const [name, options] of [
  ['required banner', { shouldShowBanner: () => true }],
  ['sale-of-data region', { saleOfDataRegion: () => true }],
  ['missing Shopify', { noShopify: true }],
  ['missing feature loader', { noLoader: true }],
  ['feature load error', { loadError: new Error('fixture load failure') }],
  ['missing privacy API', { noPrivacy: true }],
  ['required banner with failing region lookup', { shouldShowBanner: () => true, saleOfDataRegion: () => { throw new Error('fixture'); } }],
  ['sale-of-data region with failing banner lookup', { shouldShowBanner: () => { throw new Error('fixture'); }, saleOfDataRegion: () => true }],
]) {
  test(`${name} preserves the existing visible-banner path`, () => {
    const gate = runGate(options);
    assert.equal(gate.classes.has(visibilityClass), true);
    assert.equal(gate.observers.length, 0);
    assertConnected(gate.initialBanners, true);
    assertConnected(gate.initialPreferences, true);
    const laterPreferences = gate.append(preferenceSelectors);
    gate.flushMutations();
    assertConnected(laterPreferences, true);
  });
}

test('predicate errors preserve the existing banner choice without deleting preferences', () => {
  const fail = () => { throw new Error('fixture predicate failure'); };
  const gate = runGate({ shouldShowBanner: fail, saleOfDataRegion: fail });
  assert.equal(gate.classes.has(visibilityClass), false);
  assertConnected(gate.initialBanners, false);
  assertConnected(gate.initialPreferences, true);
});

test('loading documents wait for DOMContentLoaded before applying the gate', () => {
  const gate = runGate({ loading: true });
  assert.equal(gate.loadRequests.length, 0);
  assert.equal(gate.observers.length, 0);
  assertConnected(gate.initialBanners, true);
  assertConnected(gate.initialPreferences, true);
  const listener = gate.listeners.get('DOMContentLoaded');
  assert.equal(listener.settings.once, true);
  listener.callback();
  assert.equal(gate.loadRequests.length, 1);
  assertConnected(gate.initialBanners, false);
  assertConnected(gate.initialPreferences, true);
});

test('the observer still stops suppression if the banner becomes visible', () => {
  const gate = runGate();
  gate.classes.add(visibilityClass);
  const laterNodes = gate.append([...bannerSelectors, ...preferenceSelectors]);
  gate.flushMutations();
  assertConnected(laterNodes, true);
});

test('a missing body retains the existing no-observer behavior', () => {
  const gate = runGate({ noBody: true });
  assert.equal(gate.observers.length, 0);
  assertConnected(gate.initialBanners, true);
  assertConnected(gate.initialPreferences, true);
});

const footer = readFileSync(new URL('../../sections/footer.liquid', import.meta.url), 'utf8');
const footerScript = readFileSync(new URL('../../assets/cookie-preferences.js', import.meta.url), 'utf8');
const publishedLocales = ['ar', 'cs', 'da', 'de', 'el', 'en.default', 'es', 'fi', 'fr', 'he', 'hi', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt-BR', 'ro', 'ru', 'sv'];

test('the footer offers a native translated button and an adjacent polite status outside policy visibility', () => {
  const copyright = footer.slice(footer.indexOf('<div class="footer__copyright'));
  const control = copyright.match(/<cookie-preferences\b[\s\S]*?<\/cookie-preferences>/)?.[0];
  assert.ok(control, 'preferences control belongs to the copyright area');
  assert.match(copyright.slice(0, copyright.indexOf(control)), /\{%- endif -%\}\s*$/);
  assert.match(control, /<button\s+type="button"/);
  assert.match(control, /class="link link--text footer__cookie-preferences-button"/);
  assert.match(control, /aria-haspopup="dialog"/);
  assert.match(control, /aria-describedby="CookiePreferencesStatus-\{\{ section.id \}\}"/);
  assert.match(control, /id="CookiePreferencesStatus-\{\{ section.id \}\}"[\s\S]*?role="status"[\s\S]*?aria-live="polite"/);
  for (const key of ['cookie_preferences', 'cookie_preferences_unavailable']) {
    assert.ok(control.includes(`'sections.footer.${key}' | t | escape`));
  }
  assert.equal(footer.split("'cookie-preferences.js' | asset_url").length - 1, 1);
  assert.equal(footer.split("'cookie-preferences.css' | asset_url").length - 1, 1);
});

test('both preferences messages exist in all 35 theme locales, including the 21 published locales', () => {
  const localeFiles = readdirSync(new URL('../../locales/', import.meta.url))
    .filter((name) => name.endsWith('.json') && !name.endsWith('.schema.json'));
  assert.equal(localeFiles.length, 35);
  assert.equal(publishedLocales.length, 21);
  for (const locale of publishedLocales) {
    assert.ok(localeFiles.includes(`${locale}.json`), `${locale}: published locale remains covered`);
  }
  for (const locale of localeFiles) {
    const source = readFileSync(new URL(`../../locales/${locale}`, import.meta.url), 'utf8');
    const data = JSON.parse(source.replace(/^\s*\/\*[\s\S]*?\*\//, ''));
    for (const key of ['cookie_preferences', 'cookie_preferences_unavailable']) {
      assert.equal(typeof data.sections.footer[key], 'string', `${locale}: ${key}`);
      assert.ok(data.sections.footer[key].trim(), `${locale}: ${key} is not empty`);
      assert.doesNotMatch(data.sections.footer[key], /translation missing|\{\{|<script/i);
    }
  }
});

function runFooter(options = {}) {
  const observers = [];
  const timers = new Map();
  const registry = new Map();
  const dialogs = [];
  const calls = [];
  const handlers = new Map();
  const attributes = new Map();
  let timerId = 0;
  let consentWrites = 0;
  const status = { textContent: '' };
  const button = {
    disabled: false,
    isConnected: true,
    focusCount: 0,
    addEventListener: (name, callback) => handlers.set(name, callback),
    removeEventListener: (name) => handlers.delete(name),
    setAttribute: (name, value) => attributes.set(name, value),
    removeAttribute: (name) => attributes.delete(name),
    focus() { this.focusCount += 1; document.activeElement = this; },
  };
  const document = {
    body: { isConnected: true },
    querySelectorAll(selector) {
      assert.equal(selector, '.shopify-pc__prefs__dialog, .shopify-pc__prefs');
      return dialogs.filter((dialog) => dialog.isConnected);
    },
  };
  document.activeElement = document.body;
  const api = {
    showPreferences(...args) {
      calls.push({ receiver: this, args });
      return options.onOpen?.();
    },
  };
  const window = {
    privacyBanner: options.noApi ? undefined : options.noMethod ? {} : api,
    getComputedStyle: (dialog) => ({ visibility: dialog.visibility }),
    Shopify: { customerPrivacy: { setTrackingConsent: () => { consentWrites += 1; } } },
  };
  class HTMLElement {
    constructor() { this.dataset = { unavailableMessage: 'Localized retry message' }; }
    querySelector(selector) { return selector === 'button' ? button : status; }
  }
  class MutationObserver {
    constructor(callback) { this.callback = callback; }
    observe(target) {
      assert.equal(target, document.body);
      this.active = true;
      observers.push(this);
    }
    disconnect() { this.active = false; }
  }
  runInNewContext(footerScript, {
    window, document, HTMLElement, MutationObserver,
    customElements: { get: (name) => registry.get(name), define: (name, value) => registry.set(name, value) },
    setTimeout: (callback, delay) => { assert.equal(delay, 10000); timers.set(++timerId, callback); return timerId; },
    clearTimeout: (id) => timers.delete(id),
  }, { timeout: 1000 });
  const Control = registry.get('cookie-preferences');
  const control = new Control();
  control.connectedCallback();
  return {
    control, button, attributes, status, document, window, api, calls, observers, timers,
    get consentWrites() { return consentWrites; },
    click: () => handlers.get('click')?.(),
    flushMutations: () => observers.filter((observer) => observer.active).forEach((observer) => observer.callback()),
    expireOpening: () => [...timers.values()].forEach((callback) => callback()),
    addDialog(visible = true) {
      const dialog = {
        visible, visibility: 'visible', isConnected: true, hiddenAncestor: false,
        child: { isConnected: true },
        getClientRects() { return this.visible ? [{}] : []; },
        closest() { return this.hiddenAncestor ? {} : null; },
        contains(node) { return node === this.child; },
      };
      dialogs.push(dialog);
      return dialog;
    },
  };
}

const settlePromises = () => new Promise(setImmediate);

test('connecting the footer never opens preferences or writes consent automatically', () => {
  const fixture = runFooter();
  assert.equal(fixture.calls.length, 0);
  assert.equal(fixture.consentWrites, 0);
  assert.equal(fixture.observers.length, 0);
  assert.equal(fixture.timers.size, 0);
});

for (const options of [{ noApi: true }, { noMethod: true }]) {
  test(`an unavailable ${options.noApi ? 'API' : 'method'} reports the translated status and permits retry`, () => {
    const fixture = runFooter(options);
    fixture.click();
    assert.equal(fixture.status.textContent, fixture.control.dataset.unavailableMessage);
    assert.equal(fixture.button.disabled, false);
    assert.equal(fixture.observers.length, 0);
    fixture.window.privacyBanner = fixture.api;
    fixture.click();
    assert.equal(fixture.calls.length, 1);
    assert.equal(fixture.status.textContent, '');
    assert.equal(fixture.consentWrites, 0);
  });
}

test('repeated clicks call the existing API once, with its receiver and no consent arguments', () => {
  const fixture = runFooter();
  fixture.click();
  fixture.click();
  assert.equal(fixture.calls.length, 1);
  assert.equal(fixture.calls[0].receiver, fixture.api);
  assert.equal(fixture.calls[0].args.length, 0);
  assert.equal(fixture.button.disabled, true);
  assert.equal(fixture.attributes.get('aria-busy'), 'true');
  assert.equal(fixture.consentWrites, 0);
});

test('a resolved API Promise never restores focus; an observed dialog close does', async () => {
  let fixture;
  let dialog;
  fixture = runFooter({ onOpen: () => { dialog = fixture.addDialog(); return Promise.resolve(); } });
  fixture.click();
  fixture.document.activeElement = dialog.child;
  await settlePromises();
  assert.equal(fixture.button.focusCount, 0);
  assert.equal(fixture.button.disabled, true);
  assert.equal(fixture.timers.size, 0);
  dialog.isConnected = false;
  dialog.child.isConnected = false;
  fixture.flushMutations();
  assert.equal(fixture.button.disabled, false);
  assert.equal(fixture.button.focusCount, 1);
  assert.equal(fixture.observers.some((observer) => observer.active), false);
});

test('closing a dialog does not steal focus already moved to another page control', () => {
  const fixture = runFooter();
  fixture.click();
  const dialog = fixture.addDialog();
  fixture.flushMutations();
  fixture.document.activeElement = { isConnected: true };
  dialog.visible = false;
  fixture.flushMutations();
  assert.equal(fixture.button.disabled, false);
  assert.equal(fixture.button.focusCount, 0);
});

for (const [name, onOpen] of [
  ['synchronous exception', () => { throw new Error('fixture API failure'); }],
  ['rejected Promise', () => Promise.reject(new Error('fixture API failure'))],
]) {
  test(`${name} reports the translated error, cleans up and allows retry`, async () => {
    const fixture = runFooter({ onOpen });
    fixture.click();
    await settlePromises();
    assert.equal(fixture.status.textContent, fixture.control.dataset.unavailableMessage);
    assert.equal(fixture.button.disabled, false);
    assert.equal(fixture.timers.size, 0);
    assert.equal(fixture.observers.some((observer) => observer.active), false);
    assert.equal(fixture.button.focusCount, 0);
    fixture.click();
    await settlePromises();
    assert.equal(fixture.calls.length, 2);
    assert.equal(fixture.consentWrites, 0);
  });
}

test('an API call with no visible dialog has a bounded retry path', async () => {
  const fixture = runFooter({ onOpen: () => Promise.resolve() });
  fixture.addDialog(false);
  fixture.click();
  await settlePromises();
  assert.equal(fixture.button.disabled, true);
  assert.equal(fixture.button.focusCount, 0);
  fixture.expireOpening();
  assert.equal(fixture.status.textContent, fixture.control.dataset.unavailableMessage);
  assert.equal(fixture.button.disabled, false);
  assert.equal(fixture.observers.some((observer) => observer.active), false);
});

test('a late rejection from an expired attempt cannot disrupt a newer opening', async () => {
  let rejectPrevious;
  let attempt = 0;
  const fixture = runFooter({ onOpen: () => ++attempt === 1
    ? new Promise((_resolve, reject) => { rejectPrevious = reject; }) : undefined });
  fixture.click();
  fixture.expireOpening();
  fixture.click();
  fixture.addDialog();
  fixture.flushMutations();
  rejectPrevious(new Error('old attempt'));
  await settlePromises();
  assert.equal(fixture.status.textContent, '');
  assert.equal(fixture.button.disabled, true);
  assert.equal(fixture.calls.length, 2);
});

test('removing the footer cleans up without moving focus or accepting a late error', async () => {
  let rejectOpening;
  const fixture = runFooter({ onOpen: () => new Promise((_resolve, reject) => { rejectOpening = reject; }) });
  fixture.click();
  fixture.control.disconnectedCallback();
  rejectOpening(new Error('detached'));
  await settlePromises();
  assert.equal(fixture.timers.size, 0);
  assert.equal(fixture.observers.some((observer) => observer.active), false);
  assert.equal(fixture.button.focusCount, 0);
  assert.equal(fixture.status.textContent, '');
  fixture.control.connectedCallback();
  fixture.click();
  assert.equal(fixture.calls.length, 2);
});
