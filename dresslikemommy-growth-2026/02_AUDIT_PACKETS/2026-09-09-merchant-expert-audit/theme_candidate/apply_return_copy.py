from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
THEME = ROOT / 'theme'
copy = json.loads((ROOT / 'return_copy.json').read_text())
keys = ['returns_headline', 'returns_summary', 'returns_eligible', 'returns_exclusions', 'returns_damaged', 'returns_shipping']
identity = json.loads((ROOT / 'baseline_identity.json').read_text())
assert set(copy) == {entry['locale'] for entry in identity['data']['shopLocales']}
for locale, values in copy.items():
    filename = ('en.default' if locale == 'en' else locale) + '.json'
    path = THEME / 'locales' / filename
    text = path.read_text()
    for key, value in zip(keys[:4], values[:4]):
        pattern = r'("' + key + r'"\s*:\s*)"(?:[^"\\]|\\.)*"'
        text, count = re.subn(pattern, lambda m: m.group(1) + json.dumps(value, ensure_ascii=False), text)
        assert count == 1, (filename, key, count)
    pattern = r'(?m)^(\s*)"returns_exclusions": [^\n]+\n'
    def append(m):
        return m.group(0) + ''.join(m.group(1) + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False) + ',\n' for k, v in zip(keys[4:], values[4:]))
    text, count = re.subn(pattern, append, text)
    assert count == 1, filename
    path.write_text(text)
    data = json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', text, count=1, flags=re.S))
    assert all(data['products']['purchase_confidence'][key] == value for key, value in zip(keys, values))

confidence = THEME / 'snippets/pdp-purchase-confidence.liquid'
text = confidence.read_text()
fallbacks = dict(zip(keys[:4], copy['en'][:4]))
for key, value in fallbacks.items():
    variable = 'pc_' + key
    pattern = r"(assign " + variable + r" = )'[^'\n]*'(?! \|)"
    text, count = re.subn(pattern, lambda m: m.group(1) + "'" + value + "'", text)
    assert count == 1, key
confidence.write_text(text)

modal = THEME / 'snippets/pdp-policy-modals.liquid'
text = modal.read_text()
text = re.sub(r"(?m)^\s*assign dpm_return_(?:title|line_[1-5]|full_link) = '[^'\n]*'\n", '', text)
old = "  endif\n-%}\n\n<style>"
assert text.count(old) == 1
new = "  endif\n  assign dpm_close_label = 'accessibility.close' | t\n"
mapping = [('title', 'returns_headline'), ('line_1', 'returns_summary'), ('line_2', 'returns_eligible'), ('line_3', 'returns_exclusions'), ('line_4', 'returns_damaged'), ('line_5', 'returns_shipping'), ('full_link', 'returns_full_link_label')]
new += ''.join("  assign dpm_return_" + variable + " = 'products.purchase_confidence." + key + "' | t\n" for variable, key in mapping)
new += '-%}\n\n<style>'
text = text.replace(old, new)
modal.write_text(text)

manifest = []
for path in sorted((ROOT / 'baseline').rglob('*')):
    if not path.is_file(): continue
    rel = path.relative_to(ROOT / 'baseline')
    before, after = path.read_bytes(), (THEME / rel).read_bytes()
    manifest.append({'filename': str(rel), 'baseline_md5': hashlib.md5(before).hexdigest(), 'baseline_sha256': hashlib.sha256(before).hexdigest(), 'candidate_sha256': hashlib.sha256(after).hexdigest(), 'changed': before != after})
(ROOT / 'file_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Qualified return copy applied to all 21 published locales and both snippets.')
