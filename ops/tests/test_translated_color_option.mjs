import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const liquid = readFileSync(new URL('../../snippets/product-variant-picker.liquid', import.meta.url), 'utf8');
const js = readFileSync(new URL('../../assets/product-desktop-ux-20260513-ruler-sync.js', import.meta.url), 'utf8');

const listed = liquid.match(/assign dlm_color_names = '([^']*)'/)[1].split(',').filter(Boolean);
const jsLabels = [...js.match(/var COLOR_OPTION_LABELS = \[([\s\S]*?)\];/)[1].matchAll(/'([^']+)'/g)].map((m) => m[1].toLowerCase());
const isColor = (name) => listed.includes(name.toLowerCase().trim());

test('translated colour option names are recognised (non-English fixtures)', () => {
  for (const name of ['Farbe', 'Barva', 'Kleur', 'Färg', 'Väri', 'Kolor', 'Цвет', 'Χρώμα', 'צבע', 'रंग', 'カラー', '色', '색상', 'Farve', 'Farge', 'Culoare']) {
    assert.equal(isColor(name), true, name);
  }
});

test('the Liquid list covers every colour label the builder script knows (except the English ones matched by substring)', () => {
  for (const label of jsLabels) {
    if (['color', 'colour', 'couleur', 'لون'].includes(label)) continue;
    assert.ok(listed.includes(label), label);
  }
});

test('size and type names are not mistaken for colour', () => {
  for (const name of ['Größe', 'Size', 'Taille', 'Typ', 'Type']) assert.equal(isColor(name), false, name);
});
