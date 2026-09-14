from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
copies = json.loads((ROOT / 'inactive_return_copy.json').read_text())
sources = json.loads((ROOT / 'inactive_locale_source.json').read_text())
assert {f['filename'] for f in sources['files']} == {'locales/' + locale + '.json' for locale in copies}
parse = lambda text: json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', text, count=1, flags=re.S))
for locale, values in copies.items():
    path = ROOT / 'theme/locales' / (locale + '.json')
    text = path.read_text()
    before = parse(text)
    assert 'returns_damaged' not in before['products']['purchase_confidence']
    assert 'returns_shipping' not in before['products']['purchase_confidence']
    pattern = r'(?m)^(\s*)"returns_exclusions": [^\n]+\n'
    def append(m):
        return m.group(0) + ''.join(m.group(1) + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False) + ',\n' for k, v in zip(['returns_damaged', 'returns_shipping'], values))
    text, count = re.subn(pattern, append, text)
    assert count == 1, locale
    after = parse(text)
    assert after['products']['purchase_confidence'].pop('returns_damaged') == values[0]
    assert after['products']['purchase_confidence'].pop('returns_shipping') == values[1]
    assert after == before, locale
    path.write_text(text)
print('Only two new keys added to each of 14 inactive locale files; existing contents and locale status preserved.')
