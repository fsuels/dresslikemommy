import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const packet = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const theme = process.env.AUDIT_THEME_DIR || path.join(packet, 'candidate');
const source = fs.readFileSync(path.join(theme, 'sections/footer.liquid'), 'utf8');
const locales = Object.fromEntries(['en', 'es', 'da'].map(locale => [
  locale,
  JSON.parse(fs.readFileSync(path.join(theme, 'locales', locale === 'en' ? 'en.default.json' : `${locale}.json`), 'utf8').replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '')),
]));
const aliases = new Map([...source.matchAll(
  /when '([^']+)' -%}\s*{%- assign footer_block_heading = 't:([^']+)'/g,
)].map(([, alias, key]) => [alias, key]));
const defaults = new Map([
  ['COMPANY INFO', 'company_info'],
  ['HELP & SUPPORT', 'help_support'],
  ['CUSTOMER CARE', 'customer_care'],
]);
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');

// Contract fixtures use the real alias map and locale files. They do not replace
// Shopify's Liquid renderer; theme syntax and browser rendering are checked separately.
function headingContract(input, locale, menuTitle = '', translations = {}) {
  let heading = input.trim();
  if (!heading) return '';
  const lookup = (heading.startsWith('t:') ? heading.slice(2).trim() : heading).toLowerCase();
  if (aliases.has(lookup)) heading = `t:${aliases.get(lookup)}`;
  let translationKey = '';
  if (heading.startsWith('t:')) translationKey = heading.slice(2).trim();
  else if (defaults.has(heading.toUpperCase())) translationKey = `sections.footer_headings.${defaults.get(heading.toUpperCase())}`;
  if (translationKey) {
    heading = translations[translationKey] ?? translationKey.split('.').reduce((value, key) => value?.[key], locales[locale])
      ?? `Translation missing: ${locale}.${translationKey}`;
  }
  for (let attempt = 1; attempt <= 2; attempt++) {
    const check = heading.replace(/<[^>]*>/g, '').trim().toLowerCase();
    const invalid = !check || check.startsWith('translation missing:')
      || check.startsWith('sections.footer_headings.') || check.startsWith('sektioner.fodtekst_overskrifter.')
      || heading.includes('translation_missing') || (translationKey !== '' && heading === translationKey);
    if (!invalid) break;
    heading = attempt === 1 ? escape(menuTitle.trim()) : '';
  }
  return heading;
}

test('production source binds aliases, strict prefixes, validation and nonempty heading output', () => {
  assert.deepEqual([...aliases], [
    ['sektioner.fodtekst_overskrifter.firma_info', 'sections.footer_headings.company_info'],
    ['sections.footer_headings.kundeservice', 'sections.footer_headings.customer_care'],
  ]);
  assert.doesNotMatch(source, /footer_block_heading contains 't:'/);
  assert.match(source, /elsif footer_block_heading_prefix == 't:'/);
  assert.match(source, /capture footer_resolved_heading/);
  for (const [variable, prefix] of [
    ['error', 'translation missing:'],
    ['key', 'sections.footer_headings.'],
    ['alias', 'sektioner.fodtekst_overskrifter.'],
  ]) {
    assert.ok(source.includes(`assign footer_heading_${variable}_prefix = footer_heading_check | slice: 0, ${prefix.length}`));
    assert.ok(source.includes(`footer_heading_${variable}_prefix == '${prefix}'`));
  }
  assert.match(source, /footer_resolved_heading contains 'translation_missing'/);
  assert.match(source, /footer_translation_key != blank and footer_resolved_heading == footer_translation_key/);
  assert.match(source, /for footer_heading_attempt in \(1\.\.2\)/);
  assert.match(source, /footer_resolved_heading = block\.settings\.menu\.title \| default: '' \| strip \| escape/);
  assert.match(source, /if footer_resolved_heading != blank -%}\s*<h2 class="footer-block__heading inline-richtext">{{ footer_resolved_heading }}<\/h2>/);
});

test('observed Danish alias inputs resolve to readable Danish headings', () => {
  for (const prefix of ['', 't:']) {
    assert.equal(headingContract(`${prefix}sektioner.fodtekst_overskrifter.firma_info`, 'da'), 'Virksomhedsoplysninger');
    assert.equal(headingContract(`${prefix}sections.footer_headings.kundeservice`, 'da'), 'Kundeservice');
  }
});

for (const [locale, expected] of Object.entries({
  en: ['Company info', 'Help & support', 'Customer care'],
  es: ['Información de la empresa', 'Ayuda y soporte', 'Atención al cliente'],
  da: ['Virksomhedsoplysninger', 'Hjælp og support', 'Kundeservice'],
})) {
  test(`${locale}: all three canonical keys and standard default labels retain localized headings`, () => {
    [...defaults].forEach(([label, key], index) => {
      assert.equal(headingContract(`t:sections.footer_headings.${key}`, locale), expected[index]);
      assert.equal(headingContract(label, locale), expected[index]);
    });
  });
}

test('intentional custom literal, rich text and valid custom translation survive', () => {
  for (const locale of ['en', 'es', 'da']) {
    assert.equal(headingContract('Contact: us', locale), 'Contact: us');
    assert.equal(headingContract('<em>Our story</em>', locale), '<em>Our story</em>');
  }
  assert.equal(headingContract('t:custom.footer.gifts', 'da', '', { 'custom.footer.gifts': 'Gaveguider' }), 'Gaveguider');
});

test('unknown keys and missing-translation output fall back to an escaped valid menu title', () => {
  for (const value of [
    't:custom.footer.absent',
    'sections.footer_headings.absent',
    'sektioner.fodtekst_overskrifter.absent',
    'Translation missing: da.sections.footer_headings.kundeservice',
    '<span class="translation_missing">Absent</span>',
  ]) assert.equal(headingContract(value, 'da', 'Hjælp & kontakt'), 'Hjælp &amp; kontakt');
  assert.equal(headingContract('t:custom.footer.echoed', 'da', 'Hjælp', { 'custom.footer.echoed': 'custom.footer.echoed' }), 'Hjælp');
});

test('unusable fallback omits the heading and intentional blank settings stay blank', () => {
  for (const menu of ['', 'Translation missing: da.bad', 'sections.footer_headings.absent']) {
    assert.equal(headingContract('t:custom.footer.absent', 'da', menu), '');
  }
  assert.equal(headingContract(' ', 'da', 'Hjælp'), '');
});
