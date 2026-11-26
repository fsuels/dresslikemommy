import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../assets/dlm-option-roles.js', import.meta.url), 'utf8');
const document = { readyState: 'complete', querySelector: () => null, addEventListener() {} };
const ctx = { document, window: {} };
ctx.window = ctx;
vm.runInNewContext(source, ctx);
const api = ctx.DLMOptionRoles;

function group() {
  const attrs = new Map();
  return { attrs, setAttribute: (k, v) => attrs.set(k, v) };
}

test('roles come from the untranslated names, so any storefront language works (nl and hu fixtures)', () => {
  // The visible names are "Maat"/"Kleur" and "Méret"/"Szín"; the primary-language JSON says Size/Color.
  for (const visible of [['Maat', 'Kleur'], ['Méret', 'Szín']]) {
    const groups = visible.map(group);
    assert.equal(api.mark(groups, [{ name: 'Size' }, { name: 'Color' }]), 2);
    assert.deepEqual(groups.map((g) => g.attrs.get('data-option-role')), ['size', 'color']);
  }
});

test('a Type option stays untouched and a count mismatch marks nothing', () => {
  const groups = [group(), group()];
  api.mark(groups, [{ name: 'Size' }, { name: 'Type' }]);
  assert.equal(groups[1].attrs.get('data-option-role'), 'other');
  const odd = [group()];
  assert.equal(api.mark(odd, [{ name: 'Size' }, { name: 'Color' }]), 0);
  assert.equal(odd[0].attrs.has('data-option-role'), false);
});

test('picker also finds size options by their values (Dutch fixture) and the CSS hides the roles', () => {
  const liquid = readFileSync(new URL('../../snippets/product-variant-picker.liquid', import.meta.url), 'utf8');
  assert.match(liquid, /render 'dlm-facet-size-group', label: dlm_ov/);
  const group = readFileSync(new URL('../../snippets/dlm-facet-size-group.liquid', import.meta.url), 'utf8');
  assert.ok(group.includes(',volwassene') || group.includes(',volwassen,'), 'Dutch adult word known');
  assert.ok(group.includes(',kinderen,') || group.includes(',kind,'), 'Dutch child word known');
  const css = readFileSync(new URL('../../assets/component-product-desktop-ux.css', import.meta.url), 'utf8');
  assert.match(css, /data-option-role="size"/);
  assert.match(css, /data-option-role="color"/);
});
