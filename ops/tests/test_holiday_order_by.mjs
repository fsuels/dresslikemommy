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

test('Halloween 2026: 12-16 days gives Thu Oct 15, arriving by Sat Oct 31', () => {
  const api = load();
  const result = api.orderByFor('halloween', '12-16 days', new Date(2026, 8, 26, 21, 30));
  assert.equal(result.holiday, 'halloween');
  assert.deepEqual(ymd(result.cutoff), [2026, 10, 15, 4]);
  assert.ok(latestArrival(result.cutoff, 16) <= new Date(2026, 9, 31));
  assert.equal(api.message('halloween', result.cutoff, 'en'), 'Order by Thu, Oct 15 for estimated Halloween arrival');
});

test('Christmas 2026 targets Dec 24: cutoff Tue Dec 8', () => {
  const api = load();
  const result = api.orderByFor('christmas', '12-16 days', new Date(2026, 9, 20));
  assert.deepEqual(ymd(result.cutoff), [2026, 12, 8, 2]);
  assert.ok(latestArrival(result.cutoff, 16) <= new Date(2026, 11, 24));
  // The next day would miss Christmas Eve.
  assert.ok(latestArrival(new Date(2026, 11, 9), 16) > new Date(2026, 11, 24));
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
  assert.deepEqual(ymd(api.orderByFor('halloween', '10-20 days', today).cutoff), [2026, 10, 11, 0]);
  assert.deepEqual(ymd(api.orderByFor('halloween', '12-16 天', today).cutoff), [2026, 10, 15, 4]);
  assert.deepEqual(ymd(api.orderByFor('halloween', '12–16 jours', today).cutoff), [2026, 10, 15, 4]);
});

test('cutoff day still shows; the day after hides', () => {
  const api = load();
  assert.ok(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 15, 23, 59)));
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 16, 0, 1)), null);
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 9, 31)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 11, 9)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 11, 26)), null);
});

test('per-holiday lead: Christmas opens 90 days before its cutoff, Halloween 60', () => {
  const api = load();
  // Christmas cutoff Tue Dec 8 2026: opens Wed Sep 9 (90 days), hidden Sep 8.
  assert.ok(api.orderByFor('christmas', '12-16 days', new Date(2026, 8, 27)));
  assert.ok(api.orderByFor('christmas', '12-16 days', new Date(2026, 8, 9)));
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 8, 8)), null);
  assert.equal(api.orderByFor('christmas', '12-16 days', new Date(2026, 5, 1)), null);
  // Halloween cutoff Thu Oct 15 2026: opens Sun Aug 16 (60 days), hidden Aug 15.
  assert.ok(api.orderByFor('halloween', '12-16 days', new Date(2026, 7, 16)));
  assert.equal(api.orderByFor('halloween', '12-16 days', new Date(2026, 7, 15)), null);
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
  assert.equal(api.pickOrderBy(both, '12-16 days', new Date(2026, 9, 20)).holiday, 'christmas');
  assert.equal(api.pickOrderBy(['Summer'], '12-16 days', new Date(2026, 9, 10)), null);
  assert.equal(api.pickOrderBy(CHRISTMAS_TAGS, '12-16 days', new Date(2026, 8, 26)).holiday, 'christmas');
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
  assert.equal(line.children[0].text + line.children[1].textContent + line.children[2].text, 'Order by Thu, Oct 15 for estimated Halloween arrival');
  // A second pass is a no-op because the estimate paragraph is marked.
  assert.equal(api.render(HALLOWEEN_TAGS, tree.root, today), 0);
  assert.equal(tree.container.children.length, 2);

  const other = makeTree();
  assert.equal(api.render(['Summer'], other.root, today), 0);
  assert.equal(other.container.children.length, 1);

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
  assert.equal(api.render(CHRISTMAS_TAGS, open.root, new Date(2026, 8, 27)), 1);
  assert.equal(open.container.children.length, 0, 'no extra line is inserted next to the strip');
  assert.equal(open.slot.attrs.get('data-dlm-holiday-order-by'), 'christmas');
  assert.equal(open.slot.hidden, false);
  assert.equal(open.text.textContent, '');
  const [before, date, after] = open.text.children;
  assert.equal(before.text + date.textContent + after.text, 'Order by Tue, Dec 8 for estimated Christmas arrival');

  const closed = makeStrip();
  assert.equal(api.render(CHRISTMAS_TAGS, closed.root, new Date(2026, 11, 9)), 0);
  assert.equal(closed.slot.hidden, true);
  assert.equal(closed.container.children.length, 0);

  const released = makeStrip();
  api.releaseSlots({ querySelectorAll: () => [released.slot, open.slot] });
  assert.equal(released.slot.hidden, true);
  assert.equal(open.slot.hidden, false, 'a filled slot stays visible');
});
