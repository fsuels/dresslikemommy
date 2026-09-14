import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const filename = 'assets/product-desktop-ux-20260513-ruler-sync.js';
const reviewed = fs.readFileSync(path.join(root, 'reviewed_prior', filename), 'utf8');
let current = fs.readFileSync(path.join(root, 'theme', filename), 'utf8');
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
function slice(text) {
  const start = text.indexOf('var UI_LABELS_BY_LOCALE = {');
  const end = text.indexOf('\nvar GUIDE_MEASUREMENT_TOKENS', start);
  if (start < 0 || end < 0) throw Error('Dictionary boundary missing');
  const context = vm.createContext({});
  vm.runInContext(text.slice(start, end), context);
  return { start, end, dictionary: context.UI_LABELS_BY_LOCALE, block: text.slice(start, end) };
}
const old = slice(reviewed), before = slice(current);
const keys = ['chooseRoleStep', 'chooseOptionsStep', 'chooseRoleCta', 'addCurrentPiece', 'readyToAdd'];
const allowedChanges = {
  addCurrentPiece: 'Læg denne vare i indkøbskurven',
  readyToAdd: 'Klar til at lægge i kurven',
};
let changes = [];
const block = before.block.replace(/(  da: \{\n)([\s\S]*?)(  \},)/, (all, open, body, close) => {
  for (const key of keys) {
    const value = old.dictionary.da[key];
    if (value !== before.dictionary.da[key]) {
      if (allowedChanges[key] !== value) throw Error('Unapproved Danish conflict: ' + key);
      const pattern = new RegExp(`(    ${key}: )[^\\n]+`);
      if (!pattern.test(body)) throw Error('Missing Danish key: ' + key);
      body = body.replace(pattern, (_, prefix) => prefix + JSON.stringify(value) + ',');
      changes.push({ key, before: before.dictionary.da[key], after: value });
    }
  }
  return open + body + close;
});
current = current.slice(0, before.start) + block + current.slice(before.end);
const after = slice(current);
for (const [locale, labels] of Object.entries(before.dictionary)) for (const [key, value] of Object.entries(labels)) {
  const expected = locale === 'da' && Object.hasOwn(allowedChanges, key) ? allowedChanges[key] : value;
  if (after.dictionary[locale][key] !== expected) throw Error('Unexpected dictionary delta: ' + locale + '.' + key);
}
for (const key of keys) if (after.dictionary.da[key] !== old.dictionary.da[key]) throw Error('Prior reviewed Danish value lost: ' + key);
if (changes.length !== 2) throw Error('Unexpected override count');
fs.writeFileSync(path.join(root, 'theme', filename), current);
fs.writeFileSync(path.join(root, 'danish_merge_proof.json'), JSON.stringify({ source_sha256: sha(reviewed), candidate_sha256: sha(current), preserved_prior_keys: keys, overrides: changes, other_dictionary_entries_unchanged: true, functional_javascript_unchanged_from_revision3: true }, null, 2) + '\n');
console.log('Verified five prior Danish values; only two explicit dictionary overrides changed from revision 3.');
