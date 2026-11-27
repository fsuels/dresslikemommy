import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const read = (path) => readFileSync(new URL(`../../${path}`, import.meta.url), 'utf8');
const windowSource = read('snippets/hero-season-window.liquid');
const copySource = read('snippets/hero-seasonal-copy.liquid');
const bannerSource = read('sections/hero-banner.liquid');

// Run the real `if mmdd ...` lines of the snippet for an MMDD number.
function windowEdition(mmdd) {
  const body = windowSource.slice(windowSource.indexOf('{%- liquid'));
  const lines = body.split('\n').map((line) => line.trim());
  let result = '';
  let matched = false;
  let pendingTest = null;
  for (const line of lines) {
    const test = line.match(/^(?:if|elsif) (.+)$/);
    if (test) {
      pendingTest = test[1].replace(/\band\b/g, '&&').replace(/\bor\b/g, '||');
      continue;
    }
    const echo = line.match(/^echo '([a-z_]+)'$/);
    if (echo && pendingTest !== null && !matched) {
      if (new Function('mmdd', `return ${pendingTest};`)(mmdd)) {
        result = echo[1];
        matched = true;
      }
    }
  }
  return result;
}

const mmdd = (iso) => Number(iso.slice(5, 7)) * 100 + Number(iso.slice(8, 10));

test('window selection at every boundary', () => {
  const cases = {
    '2026-11-26': '',
    '2026-12-02': '', // Christmas copy until the end of Dec 2
    '2026-12-03': 'winter_photos',
    '2026-12-25': 'winter_photos',
    '2026-12-26': 'new_year',
    '2026-12-31': 'new_year',
    '2027-01-01': 'new_year',
    '2027-01-10': 'new_year',
    '2027-01-11': 'valentines',
    '2027-02-14': 'valentines',
    '2027-02-15': 'everyday', // season-free hero until Aug 31
    '2027-03-01': 'everyday',
    '2027-06-01': 'everyday',
    '2027-08-31': 'everyday',
    '2027-09-01': '', // Halloween & winter edit (own copy and art)
    '2027-10-15': '',
    '2026-10-20': '',
  };
  for (const [date, expected] of Object.entries(cases)) {
    assert.equal(windowEdition(mmdd(date)), expected, date);
  }
  // A date that did not parse (mmdd 0) must not select a window.
  assert.equal(windowEdition(0), '');
});

const LANGS = ['es', 'fr', 'de', 'it', 'nl', 'pt', 'da', 'sv', 'no', 'pl', 'cs', 'ja', 'ko', 'ru', 'ar', 'he', 'hi', 'el', 'ro', 'fi'];

// Split the snippet into { 'edition:key': { lang|else: text } }.
function parseCopy() {
  const entries = {};
  let ids = [];
  let langs = [];
  for (const raw of copySource.split('\n')) {
    const line = raw.trim();
    const whenId = raw.match(/^ {4}when ('[a-z_]+:[a-z_0-9]+'(?:, '[a-z_]+:[a-z_0-9]+')*)$/);
    if (whenId) {
      ids = [...whenId[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
      ids.forEach((id) => (entries[id] ||= {}));
      continue;
    }
    const whenLang = raw.match(/^ {8}when ((?:'[a-zA-Z-]+'(?:, )?)+)$/);
    if (whenLang) {
      langs = [...whenLang[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
      continue;
    }
    if (line === 'else') {
      langs = ['else'];
      continue;
    }
    const echo = line.match(/^echo (?:'([^']*)'|"([^"]*)")$/);
    if (echo && ids.length) {
      const text = echo[1] ?? echo[2];
      for (const id of ids) for (const lang of langs) entries[id][lang] = text;
    }
  }
  return entries;
}

const copy = parseCopy();
const NEW = ['winter_photos', 'new_year', 'valentines', 'everyday'];
const TEXT_KEYS = ['eyebrow', 'heading', 'subheading', 'cta_primary', 'cta_secondary'];

test('every new edition has copy in English and every snippet language', () => {
  for (const edition of NEW) {
    for (const key of TEXT_KEYS) {
      const entry = copy[`${edition}:${key}`];
      assert.ok(entry, `${edition}:${key} missing`);
      if (edition === 'everyday' && key === 'eyebrow') {
        assert.equal(entry.else, 'Dress Like Mommy');
        continue;
      }
      assert.ok(entry.else, `${edition}:${key} English missing`);
      for (const lang of LANGS) {
        const text = entry[lang] || entry[lang === 'no' ? 'nb' : lang];
        assert.ok(text && text.trim(), `${edition}:${key} ${lang} missing`);
        if (lang !== 'en') assert.notEqual(text, entry.else, `${edition}:${key} ${lang} left in English`);
      }
    }
  }
});

test('new copy makes no shipping, stock, discount, review or guarantee claims', () => {
  const banned = /guarante|ship|deliver|arriv|in stock|sale|off\b|discount|free|review|best.?sell|rated|order by|by christmas/i;
  for (const edition of NEW) {
    for (const key of TEXT_KEYS) {
      assert.doesNotMatch(copy[`${edition}:${key}`].else, banned, `${edition}:${key}`);
    }
  }
});

test('links point at the intended collections and no third link', () => {
  const links = {};
  for (const m of copySource.matchAll(/when ((?:'[a-z_]+:link_[a-z]+'(?:, )?)+)\n\s+echo '([^']*)'/g)) {
    for (const id of m[1].matchAll(/'([^']+)'/g)) links[id[1]] = m[2];
  }
  assert.equal(links['winter_photos:link_primary'], '/collections/family-sweaters');
  assert.equal(links['winter_photos:link_secondary'], '/collections/matching-family-christmas-outfits');
  assert.equal(links['new_year:link_primary'], '/collections/family-sweaters');
  assert.equal(links['new_year:link_secondary'], '/collections/matching-family-sweatshirts');
  assert.equal(links['valentines:link_primary'], '/collections/valentines-day-matching-outfits-1');
  assert.equal(links['valentines:link_secondary'], '/collections/mommy-and-me');
  assert.equal(links['everyday:link_primary'], '/collections/matching-outfits');
  assert.equal(links['everyday:link_secondary'], '/collections/mommy-and-me');
  for (const edition of NEW) assert.equal(links[`${edition}:link_tertiary`], undefined);
  assert.equal(links['christmas:link_primary'], '/collections/christmas-sweaters');
});

test('the Christmas copy is untouched and the banner wires the windows safely', () => {
  assert.equal(copy['christmas:heading'].else, 'Matching Christmas outfits for the whole family');
  assert.equal(copy['christmas:cta_primary'].else, 'Christmas Sweaters');
  assert.match(bannerSource, /render 'hero-season-window', mmdd: hero_today_mmdd/);
  assert.match(bannerSource, /if request\.design_mode and hero_preview_date\.size == 10/);
  assert.match(bannerSource, /key: 'heading', lang: hero_language_code/);
  assert.doesNotMatch(bannerSource, /edition: hero_seasonal_copy, key: '(?:eyebrow|heading|subheading|cta_[a-z]+|link_[a-z]+)'/);
});

test('the date value is numeric month * 100 + day and the art is neutral after Dec 25', () => {
  assert.match(bannerSource, /assign hero_today_month = 'now' \| date: '%m' \| plus: 0\n\s+assign hero_today_day = 'now' \| date: '%d' \| plus: 0\n\s+assign hero_today_mmdd = hero_today_month \| times: 100 \| plus: hero_today_day/);
  assert.doesNotMatch(bannerSource, /date: '%m%d'/);
  assert.match(bannerSource, /hero_copy_edition == 'christmas' or hero_copy_edition == 'winter_photos'/);
  // Month * 100 + day for the dates that matter (the same arithmetic the Liquid does).
  const value = (iso) => Number(iso.slice(5, 7)) * 100 + Number(iso.slice(8, 10));
  assert.deepEqual(['2027-01-01', '2027-01-10', '2027-01-11', '2027-02-01'].map(value), [101, 110, 111, 201]);
  assert.deepEqual(['2027-01-01', '2027-01-10', '2027-01-11', '2027-02-01'].map((d) => windowEdition(value(d))), ['new_year', 'new_year', 'valentines', 'valentines']);
});

test('Portuguese uses the February 14 name, Romanian copy fixes hold', () => {
  assert.doesNotMatch(copySource, /Namorados/);
  assert.equal(copy['valentines:eyebrow'].pt, 'Dia de São Valentim');
  assert.doesNotMatch(copy['winter_photos:subheading'].ro, /călduroase/);
  const holiday = read('assets/dlm-holiday-order-by.js');
  assert.match(holiday, /christmas: 'Comandați până pe \{date\} pentru livrarea estimată înainte de Crăciun'/);
  assert.doesNotMatch(holiday, /Comandă până \{date\}/);
});

test('the hero by month: Christmas art only to Dec 25, season-free Feb 15 to Aug 31, Halloween edit Sep 1 to Oct 15', () => {
  const art = (m) => m >= 1016 || (m >= 101 && m <= 831);
  assert.match(bannerSource, /hero_today_mmdd >= 1016 or hero_today_mmdd >= 101 and hero_today_mmdd <= 831/);
  const month = (m, d) => m * 100 + d;
  assert.equal(art(month(9, 1)), false);
  assert.equal(art(month(10, 15)), false);
  assert.equal(art(month(10, 16)), true);
  assert.equal(art(month(8, 31)), true);
});
