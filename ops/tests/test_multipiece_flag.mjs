import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const flag = readFileSync(new URL('../../snippets/dlm-multipiece-flag.liquid', import.meta.url), 'utf8');
const note = readFileSync(new URL('../../snippets/dlm-pdp-piece-note.liquid', import.meta.url), 'utf8');
const code = (text) => text.replace(/\{%-?\s*comment\s*-?%\}[\s\S]*?\{%-?\s*endcomment\s*-?%\}/g, '');

// Mirrors the Liquid probe: handle and tags only, hyphens as spaces, lower case.
const words = code(flag).match(/assign mpf_words = '([^']*)'/)[1].split(',');
const detect = (product) => {
  const probe = ` ${product.handle.replace(/-/g, ' ')} ${product.tags.join(' ').replace(/-/g, ' ')} `.toLowerCase() + ' ';
  return words.some((w) => probe.includes(w));
};

test('detection never reads translated fields', () => {
  for (const text of [code(flag), code(note)]) {
    assert.doesNotMatch(text, /product\.title|product\.type/);
  }
});

test('non-English fixtures: translated title and type do not matter', () => {
  const swimEs = { handle: 'mom-child-matching-two-piece-swimsuit', title: 'Bañadores a juego de mamá e hija', type: 'Trajes de baño', tags: ['Swimsuits'] };
  const swimDe = { handle: 'abstract-print-mommy-and-me-swimsuits', title: 'Passende Badeanzüge', type: 'Bademode', tags: ['Swimsuits'] };
  const pajamasIt = { handle: 'blue-gingham-collar-mommy-and-me-pajamas', title: 'Pigiami coordinati', type: 'Pigiami', tags: ['Pajamas', 'Two-Piece Pajama Set'] };
  const bikini = { handle: 'pink-wrap-mommy-and-me-bikini-set', title: 'Set bikini', type: 'Costumi', tags: ['two-piece swimsuit'] };
  const nordic = { handle: 'nordic-yoke-family-matching-sweaters', title: 'Jerséis a juego', type: 'Jerséis', tags: ['Sweaters', 'Family Sweaters', 'Matching Family Sweaters', 'Nordic Yoke'] };
  for (const p of [swimEs, swimDe, pajamasIt, bikini]) assert.equal(detect(p), true, p.handle);
  assert.equal(detect(nordic), false);
});
