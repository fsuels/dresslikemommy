import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const source = path.resolve(root, '../../2026-09-09-microsoft-ads-rebuild/buy_button_locale_replacements.json');
const payload = fs.readFileSync(source);
if (crypto.createHash('sha256').update(payload).digest('hex') !== '2f9860735c8d0948fec437adb377dd93545edae8c86626b90fe72bb8abd6698e') throw new Error('Reviewed payload drift');
const replacements = JSON.parse(payload);
const asset = path.join(root, 'theme/assets/product-desktop-ux-20260513-ruler-sync.js');
let text = fs.readFileSync(asset, 'utf8');
const start = text.indexOf('var UI_LABELS_BY_LOCALE = {');
const end = text.indexOf('\nvar GUIDE_MEASUREMENT_TOKENS', start);
let block = text.slice(start, end);
const ctx = vm.createContext({});
vm.runInContext(block, ctx);
const existing = ctx.UI_LABELS_BY_LOCALE;
const added = [];
const preserved = [];
for (const [locale, labels] of Object.entries(replacements)) {
  const missing = [];
  for (const [key, value] of Object.entries(labels)) {
    if (Object.hasOwn(existing[locale] || {}, key)) {
      if (existing[locale][key] !== value) throw new Error(`Existing value conflicts: ${locale}.${key}`);
      preserved.push(`${locale}.${key}`);
    } else {
      missing.push(`    ${key}: ${JSON.stringify(value)},`);
      added.push(`${locale}.${key}`);
    }
  }
  if (!missing.length) continue;
  if (existing[locale]) {
    const pattern = new RegExp(`(  ${locale}: \\{\\n)([\\s\\S]*?)(  \\},)`);
    if (!pattern.test(block)) throw new Error(`Missing dictionary source: ${locale}`);
    block = block.replace(pattern, (_, open, contents, close) => open + contents + missing.join('\n') + '\n' + close);
  } else {
    block = block.replace(/\n};$/, `\n  ${locale}: {\n${missing.join('\n')}\n  },\n};`);
  }
}
const checked = vm.createContext({});
vm.runInContext(block, checked);
for (const [locale, labels] of Object.entries(replacements)) for (const [key, value] of Object.entries(labels)) {
  if (checked.UI_LABELS_BY_LOCALE[locale]?.[key] !== value) throw new Error(`Integration failed: ${locale}.${key}`);
}
for (const [locale, labels] of Object.entries(existing)) for (const [key, value] of Object.entries(labels)) {
  if (checked.UI_LABELS_BY_LOCALE[locale]?.[key] !== value) throw new Error(`Existing dictionary changed: ${locale}.${key}`);
}
text = text.slice(0, start) + block + text.slice(end);
fs.writeFileSync(asset, text);
fs.writeFileSync(path.join(root, 'selector_copy_integration.json'), JSON.stringify({ source_sha256: crypto.createHash('sha256').update(payload).digest('hex'), added, preserved, conflicts: [] }, null, 2) + '\n');
console.log(JSON.stringify({ added: added.length, preserved: preserved.length, conflicts: 0 }));
