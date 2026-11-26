import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../assets/dlm-holiday-order-by.js', import.meta.url), 'utf8');

function load({ locale = 'en' } = {}) {
  const document = {
    readyState: 'complete',
    documentElement: { lang: locale },
    body: {},
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener() {},
  };
  const context = {
    document,
    Intl,
    Date,
    Math,
    Array,
    Number,
    String,
    Shopify: { locale },
    location: { pathname: '/' },
  };
  context.window = context;
  vm.runInNewContext(source, context);
  return context.DLMHolidayOrderBy;
}

const ymd = (date) => [date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getDay()];
const HALLOWEEN_TAGS = ['Fall', 'Ghost', 'Halloween', 'Halloween Pajamas', 'Pumpkin'];
const CHRISTMAS_TAGS = ['Christmas', 'Christmas Sweaters', 'Family Christmas Sweaters', 'Holiday', 'Winter'];

// Mirrors dlm-delivery-dates.js addDays so the invariant is checked independently.
function latestArrival(cutoff, maxDays) {
  const date = new Date(cutoff.getFullYear(), cutoff.getMonth(), cutoff.getDate() + maxDays);
  if (date.getDay() === 0) date.setDate(date.getDate() + 1);
  return date;
}

test('Halloween 2026: 12-16 days plus the 5-day worst-case buffer gives Sat Oct 10, arriving by Sat Oct 31', () => {
  const api = load();
  const result = api.orderByFor('halloween', '12-16 days', new Date(2026, 8, 26, 21, 30));
  assert.equal(result.holiday, 'halloween');
  assert.deepEqual(ymd(result.cutoff), [2026, 10, 10, 6]);
  assert.ok(latestArrival(result.cutoff, 21) <= new Date(2026, 9, 31));
  assert.equal(api.message('halloween', result.cutoff, 'en'), 'Order by Sat, Oct 10 for estimated Halloween arrival');
});

test('Christmas 2026 targets Dec 23 like the card line: cutoff Wed Dec 2 (policy handling up to 5 business days, carrier transit up to 14 days)', () => {
  const api = load();
  const result = api.orderByFor('christmas', '12-16 days', new Date(2026, 10, 25));
  assert.deepEqual(ymd(result.cutoff), [2026, 12, 2, 3]);
  assert.ok(latestArrival(result.cutoff, 21) <= new Date(2026, 11, 23));
  // The next day would miss Dec 23.
  assert.ok(latestArrival(new Date(2026, 11, 3), 21) > new Date(2026, 11, 23));
  // Worst case: ships after 5 business days (7 calendar days), then 14 days in transit.
  assert.ok(new Date(2026, 11, 2 + 7 + 14) <= new Date(2026, 11, 23));
});

test('Sunday roll: Halloween 2027 is a Sunday, so the cutoff moves back a day', () => {
  const api = load();
  const cutoff = api.computeCutoff(new Date(2027, 9, 31), 16);
  // Fri Oct 15 + 16 = Sun Oct 31, which rolls to Mon Nov 1 (too late).
  assert.deepEqual(ymd(cutoff), [2027, 10, 14, 4]);
  assert.deepEqual(ymd(latestArrival(cutoff, 16)), [2027, 10, 30, 6]);
});

test('the cutoff follows the window upper bound, not a hardcoded 16', () => {
  const api = load();
  const today = new Date(2026, 8, 26);
  assert.deepEqual(ymd(api.orderByFor('halloween', '10-20 days', today).cutoff), [2026, 10, 6, 2]);
  assert.deepEqual(ymd(api.orderByFor('halloween', '12-16 天', today).cutoff), [2026, 10, 10, 6]);
  assert.deepEqual(ymd(api.orderByFor('halloween', '12–16 jours', today).cutoff), [2026, 10, 10, 6]);
});

test('cutoff day still shows; the day after hides', () => {
  const api = load();
  assert.ok(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 10, 23, 59)));
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 11, 0, 1)), null);
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 31)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 11, 3)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 11, 26)), null);
});

test('per-holiday lead: Christmas opens 14 days before its cutoff, Halloween 60', () => {
  const api = load();
  // Christmas cutoff Wed Dec 2 2026: opens Wed Nov 18 (14 days), hidden Nov 17.
  assert.ok(api.orderByFor('christmas', '12-16 days', new Date(2026, 11, 2)));
  assert.ok(api.orderByFor('christmas', '12-16 days', new Date(2026, 10, 18)));
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 10, 17)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 5, 1)), null);
  // Halloween cutoff Sat Oct 10 2026: opens Tue Aug 11 (60 days), hidden Aug 10.
  assert.ok(api.orderByFor('halloween', '12-16 days', new Date(2026, 7, 11)));
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 7, 10)), null);
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 5, 1)), null);
});

test('unparseable windows hide the line', () => {
  const api = load();
  const today = new Date(2026, 8, 26);
  for (const value of ['a few days', '', null, '16-12 days', '0 days', '120-130 days']) {
    assert.equal(api.orderByFor('halloween', value, today), null, String(value));
    assert.equal(api.pickOrderBy(HALLOWEEN_TAGS, value, today), null, String(value));
  }
});

test('holiday detection uses exact holiday tags and ignores lookalikes', () => {
  const api = load();
  assert.deepEqual([...api.detectHolidays(HALLOWEEN_TAGS)], ['halloween']);
  assert.deepEqual([...api.detectHolidays(CHRISTMAS_TAGS)], ['christmas']);
  assert.deepEqual([...api.detectHolidays(['Christmas Pajamas', 'Reindeer'])], ['christmas']);
  assert.deepEqual([...api.detectHolidays('Fall, halloween pajamas')], ['halloween']);
  assert.deepEqual([...api.detectHolidays(['Holiday', 'beach holiday outfit', 'Winter', 'Fall', 'Ghost'])], []);
  assert.deepEqual([...api.detectHolidays(['Halloweenish'])], []);
  assert.deepEqual([...api.detectHolidays(null)], []);
  assert.deepEqual([...api.detectHolidays([])], []);
});

test('pickOrderBy returns the earliest open holiday for the product', () => {
  const api = load();
  const both = ['Halloween', 'Christmas'];
  assert.equal(api.pickOrderBy(both, '12-16 days', new Date(2026, 9, 10)).holiday, 'halloween');
  assert.equal(api.pickOrderBy(both, '12-16 days', new Date(2026, 10, 25)).holiday, 'christmas');
  assert.equal(api.pickOrderBy(['Summer'], '12-16 days', new Date(2026, 9, 10)), null);
  assert.equal(api.pickOrderBy(CHRISTMAS_TAGS, '12-16 days', new Date(2026, 10, 25)).holiday, 'christmas');
  assert.equal(api.pickOrderBy(CHRISTMAS_TAGS, '12-16 days', new Date(2026, 7, 1)), null);
});

test('every language says estimated and keeps the date slot; unknown falls back to English', () => {
  const api = load();
  const published = ['en', 'es', 'fr', 'de', 'it', 'nl', 'pt', 'da', 'sv', 'no', 'pl', 'cs', 'fi', 'ro', 'el', 'ja', 'ko', 'ru', 'ar', 'he', 'hi'];
  for (const lang of [...published, 'hu', 'tr', 'zh', 'zh-hant']) {
    const copy = api.copy[lang];
    assert.ok(copy, lang);
    for (const key of ['halloween', 'christmas']) {
      assert.equal(copy[key].split('{date}').length, 2, `${lang} ${key}`);
      assert.doesNotMatch(copy[key], /guarant/i, `${lang} ${key}`);
    }
  }
  assert.match(api.copy.en.halloween, /estimated/);
  assert.equal(api.languageKey('pt-BR'), 'pt');
  assert.equal(api.languageKey('nb'), 'no');
  assert.equal(api.languageKey('zh-TW'), 'zh-hant');
  assert.equal(api.languageKey('xx'), 'en');
  assert.equal(api.languageKey(undefined), 'en');
  const cutoff = new Date(2026, 9, 15);
  assert.match(api.message('halloween', cutoff, 'it'), /^Ordina entro .*ott.* prima di Halloween$/);
  assert.match(api.message('halloween', cutoff, 'de'), /Okt/);
  assert.match(api.message('halloween', cutoff, 'xx-invalid!!'), /Oct/);
});

test('render inserts one line after the estimate paragraph and skips non-holiday products', () => {
  const makeTree = () => {
    const container = {
      children: [],
      insertBefore(node, ref) {
        const index = ref ? this.children.indexOf(ref) : -1;
        this.children.splice(index < 0 ? this.children.length : index, 0, node);
      },
    };
    const attrs = new Map();
    const host = {
      parentNode: container,
      nextSibling: null,
      hasAttribute: (n) => attrs.has(n),
      setAttribute: (n, v) => attrs.set(n, v),
    };
    container.children.push(host);
    const element = { parentNode: host, getAttribute: () => '12-16 days' };
    return { container, root: { querySelectorAll: () => [element] } };
  };
  const document = {
    readyState: 'complete',
    documentElement: { lang: 'en' },
    body: {},
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener() {},
    createElement: () => ({
      children: [],
      style: {},
      attrs: {},
      setAttribute(n, v) { this.attrs[n] = v; },
      appendChild(child) { this.children.push(child); },
    }),
    createTextNode: (text) => ({ text }),
  };
  const sandbox = { document, Intl, Date, Math, Array, Number, String, Shopify: { locale: 'en' }, location: { pathname: '/' } };
  sandbox.window = sandbox;
  vm.runInNewContext(source, sandbox);
  const api = sandbox.DLMHolidayOrderBy;
  const today = new Date(2026, 8, 26);

  const tree = makeTree();
  assert.equal(api.render(HALLOWEEN_TAGS, tree.root, today), 1);
  assert.equal(tree.container.children.length, 2);
  const line = tree.container.children[1];
  assert.equal(line.attrs['data-dlm-holiday-order-by'], 'halloween');
  assert.equal(line.children[0].text + line.children[1].textContent + line.children[2].text, 'Order by Sat, Oct 10 for estimated Halloween arrival');
  // A second pass is a no-op because the estimate paragraph is marked.
  assert.equal(api.render(HALLOWEEN_TAGS, tree.root, today), 0);
  assert.equal(tree.container.children.length, 2);

  const other = makeTree();
  assert.equal(api.render(['Summer'], other.root, today), 0);
  assert.equal(other.container.children.length, 1);

  // A card that already prints the Christmas estimate gets no second line.
  const card = makeTree();
  card.container.querySelector = (sel) => (sel === '[data-dlm-christmas-order-by]' ? {} : null);
  assert.equal(api.render(CHRISTMAS_TAGS, card.root, new Date(2026, 10, 25)), 0);
  assert.equal(card.container.children.length, 1);

  const late = makeTree();
  assert.equal(api.render(HALLOWEEN_TAGS, late.root, new Date(2026, 9, 16)), 0);
  assert.equal(late.container.children.length, 1);
});

test('value-strip slot is filled in place, or hidden when no line applies', () => {
  const makeText = () => ({
    textContent: 'stale',
    children: [],
    appendChild(child) { this.children.push(child); },
  });
  const makeStrip = () => {
    const attrs = new Map();
    const text = makeText();
    const slot = {
      hidden: false,
      attrs: new Map(),
      hasAttribute(n) { return this.attrs.has(n); },
      setAttribute(n, v) { this.attrs.set(n, v); },
      querySelector: (sel) => (sel === '[data-dlm-holiday-text]' ? text : null),
    };
    const strip = { querySelector: (sel) => (sel === '[data-dlm-holiday-slot]' ? slot : null) };
    const container = { children: [], insertBefore(node) { this.children.push(node); } };
    const host = { parentNode: container, nextSibling: null, hasAttribute: (n) => attrs.has(n), setAttribute: (n, v) => attrs.set(n, v) };
    const element = {
      parentNode: host,
      getAttribute: () => '12-16 days',
      closest: (sel) => (sel === '[data-dlm-value-strip]' ? strip : null),
    };
    return { slot, text, container, root: { querySelectorAll: () => [element] } };
  };
  const document = {
    readyState: 'complete',
    documentElement: { lang: 'en' },
    body: {},
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener() {},
    createElement: () => ({ textContent: '' }),
    createTextNode: (text) => ({ text }),
  };
  const sandbox = { document, Intl, Date, Math, Array, Number, String, Shopify: { locale: 'en' }, location: { pathname: '/' } };
  sandbox.window = sandbox;
  vm.runInNewContext(source, sandbox);
  const api = sandbox.DLMHolidayOrderBy;

  const open = makeStrip();
  assert.equal(api.render(CHRISTMAS_TAGS, open.root, new Date(2026, 10, 25)), 1);
  assert.equal(open.container.children.length, 0, 'no extra line is inserted next to the strip');
  assert.equal(open.slot.attrs.get('data-dlm-holiday-order-by'), 'christmas');
  assert.equal(open.slot.hidden, false);
  assert.equal(open.text.textContent, '');
  const [before, date, after] = open.text.children;
  assert.equal(before.text + date.textContent + after.text, 'Order by Wed, Dec 2 for estimated Christmas arrival');

  const closed = makeStrip();
  assert.equal(api.render(CHRISTMAS_TAGS, closed.root, new Date(2026, 11, 8)), 0);
  assert.equal(closed.slot.hidden, true);
  assert.equal(closed.container.children.length, 0);

  const released = makeStrip();
  api.releaseSlots({ querySelectorAll: () => [released.slot, open.slot] });
  assert.equal(released.slot.hidden, true);
  assert.equal(open.slot.hidden, false, 'a filled slot stays visible');
});

test('PDP card, cart and drawer line (liquid snippet) use the same policy buffer as the value-strip line', async () => {
  const { readFileSync } = await import('node:fs');
  const liquid = readFileSync(new URL('../../snippets/christmas-order-by.liquid', import.meta.url), 'utf8');
  const api = load();
  assert.equal(api.policyHandlingBufferDays, 5);
  assert.match(liquid, /assign cob_max = cob_max \| plus: cob_extra \| plus: 5/);
});

// Independent worst-case check against the shipping policy: the parcel leaves within 5 business
// days after payment, then carrier transit is at most 14 days (YunExpress registered air mail
// quotes 7-14; published in the Product structured data). Arrival on a
// Sunday rolls to Monday like the estimate does.
function policyWorstArrival(order, transitMax = 14) {
  const d = new Date(order.getFullYear(), order.getMonth(), order.getDate());
  let business = 0;
  while (business < 5) {
    d.setDate(d.getDate() + 1);
    if (d.getDay() !== 0 && d.getDay() !== 6) business += 1;
  }
  d.setDate(d.getDate() + transitMax);
  if (d.getDay() === 0) d.setDate(d.getDate() + 1);
  return d;
}

test('Christmas cutoff is the latest order day whose policy worst case still arrives by Dec 23', () => {
  const api = load();
  const cutoff = api.orderByFor('christmas', '12-16 days', new Date(2026, 10, 25)).cutoff;
  const target = new Date(2026, 11, 23);
  // Every order day from Nov 1 up to the cutoff arrives by Dec 23 in the worst case...
  for (let d = new Date(2026, 10, 1); d <= cutoff; d.setDate(d.getDate() + 1)) {
    assert.ok(policyWorstArrival(d) <= target, `order ${d.toDateString()} arrives ${policyWorstArrival(d).toDateString()}`);
  }
  // ...and the next day does not (Wed Dec 2 -> Dec 23, Thu Dec 3 -> Dec 24).
  assert.deepEqual(ymd(cutoff), [2026, 12, 2, 3]);
  assert.deepEqual(ymd(policyWorstArrival(new Date(2026, 11, 2))), [2026, 12, 23, 3]);
  assert.deepEqual(ymd(policyWorstArrival(new Date(2026, 11, 3))), [2026, 12, 24, 4]);
});

test('worst case by weekday: dispatch takes at most 7 calendar days', () => {
  for (let i = 0; i < 7; i += 1) {
    const order = new Date(2026, 11, 1 + i);
    const dispatchOnly = policyWorstArrival(order, 0);
    const days = Math.round((dispatchOnly - order) / 86400000);
    assert.ok(days <= 7 && days >= 5, `${order.toDateString()} dispatch in ${days} days`);
  }
});

test('structured data publishes handling 1-5 and transit from the per-country carrier map (US 7-14)', () => {
  const liquid = readFileSync(new URL('../../snippets/jsonld-seo.liquid', import.meta.url), 'utf8');
  const map = readFileSync(new URL('../../snippets/dlm-transit-map.liquid', import.meta.url), 'utf8');
  assert.match(liquid, /assign schema_handling_max = schema_handling_max \| plus: 2/);
  assert.match(liquid, /render 'dlm-transit-map', country: shipping_country_code/);
  assert.match(liquid, /schema_transit_range != blank and schema_delivery_min >= 1/);
  assert.match(map, /US:7-14\|/);
  assert.doesNotMatch(map, /AU:/);
});

function fakeBanner(windowValue = '12-16 days') {
  const attrs = { 'data-dlm-christmas-window': windowValue };
  const text = {
    textContent: '',
    children: [],
    appendChild(child) { this.children.push(child); },
  };
  const banner = {
    hidden: false,
    attrs,
    getAttribute: (n) => attrs[n] ?? null,
    setAttribute: (n, v) => { attrs[n] = v; },
    hasAttribute: (n) => n in attrs,
    querySelector: (sel) => (sel === '[data-dlm-holiday-text]' ? text : null),
  };
  const textOf = () => text.children.map((c) => c.text ?? c.textContent).join('');
  return { banner, textOf };
}

function loadWithBanners(banners, locale = 'en') {
  const document = {
    readyState: 'complete',
    documentElement: { lang: locale },
    body: {},
    querySelector: () => null,
    querySelectorAll: (sel) => (sel === '[data-dlm-xmas-banner]' ? banners : []),
    addEventListener() {},
    createElement: () => ({ textContent: '' }),
    createTextNode: (text) => ({ text }),
  };
  const sandbox = { document, Intl, Date, Math, Array, Number, String, Shopify: { locale }, location: { pathname: '/' } };
  sandbox.window = sandbox;
  vm.runInNewContext(source, sandbox);
  return sandbox.DLMHolidayOrderBy;
}

test('home/collection banner shows the same Wed Dec 2 line as the PDP card and is translated', () => {
  const api = loadWithBanners([]);
  const today = new Date(2026, 10, 26);
  const pdp = api.message('christmas', api.orderByFor('christmas', '12-16 days', today).cutoff, 'en');
  assert.equal(pdp, 'Order by Wed, Dec 2 for estimated Christmas arrival');
  for (const locale of ['en', 'es', 'it', 'de']) {
    const { banner, textOf } = fakeBanner();
    const bannerApi = loadWithBanners([banner], locale);
    assert.equal(bannerApi.renderBanners({ querySelectorAll: () => [banner] }, today), 1);
    const expected = bannerApi.message('christmas', bannerApi.orderByFor('christmas', '12-16 days', today).cutoff, locale);
    assert.equal(textOf(), expected);
    assert.equal(banner.hidden, false);
    assert.equal(banner.attrs['data-dlm-holiday-order-by'], 'christmas');
    assert.match(textOf(), locale === 'en' ? /Wed, Dec 2/ : /2/);
  }
});

test('home/collection banner hides after the cutoff, before the lead window, and on unparseable windows', () => {
  const api = loadWithBanners([]);
  const run = (today, windowValue) => {
    const { banner } = fakeBanner(windowValue);
    const count = api.renderBanners({ querySelectorAll: () => [banner] }, today);
    return { count, hidden: banner.hidden };
  };
  assert.deepEqual(run(new Date(2026, 11, 2), '12-16 days'), { count: 1, hidden: false });
  assert.deepEqual(run(new Date(2026, 11, 3), '12-16 days'), { count: 0, hidden: true });
  assert.deepEqual(run(new Date(2026, 10, 17), '12-16 days'), { count: 0, hidden: true });
  assert.deepEqual(run(new Date(2026, 10, 18), '12-16 days'), { count: 1, hidden: false });
  assert.deepEqual(run(new Date(2026, 10, 26), 'soon'), { count: 0, hidden: true });
});

test('one date block: no short Christmas line is added when the value strip carries the full estimate line', () => {
  const makeTree = () => {
    const attrs = new Map();
    const container = { children: [], insertBefore(node) { this.children.push(node); }, querySelector: () => null };
    const host = { parentNode: container, nextSibling: null, hasAttribute: (n) => attrs.has(n), setAttribute: (n, v) => attrs.set(n, v) };
    const strip = { querySelector: () => null };
    const element = {
      parentNode: host,
      getAttribute: () => '12-16 days',
      closest: (sel) => (sel === '[data-dlm-value-strip]' ? strip : null),
    };
    return { container, root: { querySelectorAll: () => [element] } };
  };
  const run = (stripHasFullLine) => {
    const document = {
      readyState: 'complete',
      documentElement: { lang: 'en' },
      body: {},
      querySelector: (sel) => (stripHasFullLine && sel === '[data-dlm-value-strip] [data-dlm-christmas-order-by]' ? {} : null),
      querySelectorAll: () => [],
      addEventListener() {},
      createElement: () => ({ textContent: '', style: {}, setAttribute() {}, appendChild() {} }),
      createTextNode: (text) => ({ text }),
    };
    const sandbox = { document, Intl, Date, Math, Array, Number, String, Shopify: { locale: 'en' }, location: { pathname: '/' } };
    sandbox.window = sandbox;
    vm.runInNewContext(source, sandbox);
    const tree = makeTree();
    sandbox.DLMHolidayOrderBy.render(CHRISTMAS_TAGS, tree.root, new Date(2026, 10, 25));
    return tree.container.children.length;
  };
  assert.equal(run(true), 0, 'the full line in the strip replaces the short line');
  assert.equal(run(false), 1, 'without the full line the short line is still added');
});
