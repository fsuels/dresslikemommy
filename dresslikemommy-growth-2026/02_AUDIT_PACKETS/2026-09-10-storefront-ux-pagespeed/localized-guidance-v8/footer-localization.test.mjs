import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const packet = path.dirname(dir);
const candidate = path.join(packet, 'candidate');
const proposal = path.join(dir, 'proposed');
const before = fs.readFileSync(path.join(candidate, 'sections/footer.liquid'), 'utf8');
const proposed = fs.readFileSync(process.env.DLM_FOOTER_SOURCE || path.join(proposal, 'sections/footer.liquid'), 'utf8');
const parseLocale = (locale, overlay = true) => {
  const relative = path.join('locales', `${locale === 'en' ? 'en.default' : locale}.json`);
  const file = overlay && fs.existsSync(path.join(proposal, relative)) ? path.join(proposal, relative) : path.join(candidate, relative);
  return JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\s*\/\*[\s\S]*?\*\/\s*/, ''));
};
const expected = [
  ['ro', 'secțiuni.titluri_subsol.informații_companie', 'company_info'],
  ['ro', 'secțiuni.titluri_subsol.ajutor_suport', 'help_support'],
  ['ro', 'asistență_clienți', 'customer_care'],
  ['nl', 'secties.voettekst_koppen.bedrijfsinformatie', 'company_info'],
  ['nl', 'secties.voettekst_koppen.hulp_ondersteuning', 'help_support'],
  ['de', 'Abschnitte.Fußzeilen_Überschriften.Unternehmensinformationen', 'company_info'],
  ['de', 'Abschnitte.Footer_Überschriften.Hilfe_Support', 'help_support'],
  ['el', 'τμήματα.υποσέλιδο_επικεφαλίδες.πληροφορίες_εταιρείας', 'company_info'],
  ['el', 'τμήματα.υποσέλιδο_επικεφαλίδες.εξυπηρέτηση_πελατών', 'customer_care'],
  ['fi', 'sections.footer_headings.asiakaspalvelu', 'customer_care'],
];

// Execute the production alias-case assignments, not a separately maintained
// alias table. Full Shopify Liquid/rendered verification remains a separate gate.
function applyProductionAlias(source, input) {
  const block = source.match(/{%- case footer_heading_lookup -%}([\s\S]*?){%- endcase -%}/)?.[1];
  assert.ok(block, 'Production alias case exists');
  assert.match(source, /assign footer_block_heading_prefix = footer_block_heading \| slice: 0, 2/);
  assert.match(source, /if footer_block_heading_prefix == 't:' -%}\s*{%- assign footer_heading_lookup = footer_heading_lookup \| remove_first: 't:' \| strip/);
  const inputHeading = input.trim();
  const lookup = (inputHeading.startsWith('t:') ? inputHeading.slice(2).trim() : inputHeading).toLowerCase();
  const rules = [...block.matchAll(/{%- when '([^']+)' -%}\s*{%- assign footer_block_heading = '([^']+)' -%}/g)];
  assert.equal(rules.length, (block.match(/{%- when /g) || []).length, 'Every production alias branch is covered');
  return rules.find(([, alias]) => alias === lookup)?.[2] ?? inputHeading;
}

test('frozen V7 local source and all ten failure cases are unchanged', () => {
  assert.equal(crypto.createHash('sha256').update(before).digest('hex'), 'bf94102671a334dde28a87bb97e22c942c805ddd1633673cabec847594b32bc8');
  for (const [, alias] of expected) {
    assert.equal(applyProductionAlias(before, alias), alias);
    assert.equal(applyProductionAlias(before, `t:${alias}`), `t:${alias}`);
  }
  assert.deepEqual(parseLocale('nl', false).sections.footer_headings, { company_info: 'Company info', help_support: 'Help & support', customer_care: 'Customer care' });
  assert.deepEqual(parseLocale('ro-RO', false).sections.footer_headings, parseLocale('nl', false).sections.footer_headings);
});

for (const [, alias, key] of expected) {
  test(`canonical alias: ${alias}`, () => {
    for (const input of [alias, alias.toLowerCase(), `t:${alias}`, ` t:${alias} `]) {
      assert.equal(applyProductionAlias(proposed, input), `t:sections.footer_headings.${key}`);
    }
  });
}

test('canonical alias resolution uses native parent-owned locale overlays and existing Romanian data', () => {
  const english = parseLocale('en').sections.footer_headings;
  for (const [locale, alias, key] of expected) {
    const result = applyProductionAlias(proposed, alias);
    const resolved = result.slice(2).split('.').reduce((value, part) => value?.[part], parseLocale(locale));
    assert.ok(resolved && resolved !== english[key], `${locale}.${key} requires native display data`);
    assert.doesNotMatch(resolved, /translation missing|[._]/i);
  }
  assert.deepEqual(parseLocale('ro').sections.footer_headings, { company_info: 'Informații despre companie', help_support: 'Ajutor și asistență', customer_care: 'Serviciu clienți' });
  assert.deepEqual(parseLocale('ro-RO').sections.footer_headings, parseLocale('ro').sections.footer_headings);
});

test('holdout: Danish aliases and canonical translation inputs retain their existing paths', () => {
  for (const input of [
    'sektioner.fodtekst_overskrifter.firma_info',
    't:sections.footer_headings.kundeservice',
    't:sections.footer_headings.company_info',
    't:sections.footer_headings.help_support',
    't:sections.footer_headings.customer_care',
  ]) assert.equal(applyProductionAlias(proposed, input), applyProductionAlias(before, input));
});

test('holdout: English, Spanish, French, Dutch and intentional custom headings are unchanged', () => {
  for (const input of [
    'Company info', 'Help & support', 'Customer care',
    'Información de la empresa', 'Ayuda y soporte', 'Atención al cliente',
    "Informations sur l'entreprise", 'Aide et assistance', 'Service client',
    'Klantenservice', 'Kundendienst', 'βοήθεια & υποστήριξη',
    'Contact: us', '<em>Our story</em>', 't:custom.footer.gifts',
  ]) assert.equal(applyProductionAlias(proposed, input), applyProductionAlias(before, input));
});

test('only the bounded alias case changes; disclosure, consent and all other logic remain byte-identical', () => {
  const removeCase = source => source.replace(/{%- case footer_heading_lookup -%}[\s\S]*?{%- endcase -%}/, '{% alias case %}');
  assert.equal(removeCase(proposed), removeCase(before));
});
