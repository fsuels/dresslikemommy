from pathlib import Path
import difflib, hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / 'theme_candidate'
OLD = ROOT.parent.parent / '2026-09-05-ceo-turnaround'
BASE, THEME = ROOT / 'baseline', ROOT / 'theme'
parse = lambda value: json.loads(re.sub(r'^\s*/\*[\s\S]*?\*/\s*', '', value))
md5 = lambda value: hashlib.md5(value).hexdigest()
sha = lambda value: hashlib.sha256(value).hexdigest()
assert sha((PRIOR / 'candidate_files.json').read_bytes()) == '1ac332a2a99ce5ae66dc9f0485f476631457acd52b594b73134f086c433d8a6b'
source = json.loads((ROOT / 'merge_source_readback.json').read_text())
draft = {f['filename']: f for f in source['data']['prior']['files']['nodes']}
source_paths = {
    'assets/cart.js': 'cart_draft_candidate/assets/cart.js',
    'assets/product-desktop-ux-20260513-ruler-sync.js': 'danish_runtime_candidate.js',
    'locales/da.json': 'traffic_live_theme_release/locales/da.json',
    'locales/nl.json': 'draft_nl_description_candidate.json',
}
proof = {'base_candidate_sha256': sha((PRIOR / 'candidate_files.json').read_bytes()), 'prior_theme_id': source['data']['prior']['id'], 'source_capture': source['captured_at_utc'], 'sources': [], 'seo_changes': []}
for filename, old_path in source_paths.items():
    body = (OLD / old_path).read_bytes()
    assert md5(body) == draft[filename]['checksumMd5'], filename
    assert len(body) == int(draft[filename]['size']), filename
    saved = ROOT / 'reviewed_prior' / filename
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_bytes(body)
    proof['sources'].append({'filename': filename, 'source_path': str(OLD / old_path), 'current_draft_md5': draft[filename]['checksumMd5'], 'saved_sha256': sha(body), 'bytes': len(body)})

# The reviewed cart changes only its recently-viewed IIFE; all other bytes remain MAIN.
cart_before = (BASE / 'assets/cart.js').read_bytes()
assert cart_before == (OLD / 'cart_draft_before/assets/cart.js').read_bytes()
cart_after = (ROOT / 'reviewed_prior/assets/cart.js').read_bytes()
matcher = difflib.SequenceMatcher(None, cart_before.splitlines(True), cart_after.splitlines(True), autojunk=False)
changed = [op for op in matcher.get_opcodes() if op[0] != 'equal']
assert changed and all(380 <= a <= b <= 448 for _, a, b, _, _ in changed)
assert cart_before[:15233] == cart_after[:15233]
assert cart_before[-4168:] == cart_after[-4168:]
(THEME / 'assets/cart.js').write_bytes(cart_after)
proof['cart_preservation'] = {'main_md5': md5(cart_before), 'candidate_md5': md5(cart_after), 'exact_reviewed_body': True, 'unchanged_prefix_bytes': 15233, 'unchanged_suffix_bytes': 4168}

def flatten(value, prefix=''):
    output = {}
    for key, entry in value.items():
        path = f'{prefix}.{key}' if prefix else key
        output.update(flatten(entry, path) if isinstance(entry, dict) else {path: entry})
    return output

for locale in ['da', 'nl']:
    filename = f'locales/{locale}.json'
    before = flatten(parse((BASE / filename).read_text()))
    old = flatten(parse((ROOT / 'reviewed_prior' / filename).read_text()))
    delta = {key: value for key, value in old.items() if before.get(key) != value}
    assert set(delta) == {'sections.collection_seo.meta_titles.dresses', 'sections.collection_seo.meta_descriptions.dresses'}
    text = (THEME / filename).read_text()
    current = flatten(parse(text))
    for key, value in delta.items():
        assert current[key] == before[key], (filename, key)
        old_literal, new_literal = json.dumps(before[key], ensure_ascii=False), json.dumps(value, ensure_ascii=False)
        assert text.count(old_literal) == 1
        text = text.replace(old_literal, new_literal, 1)
        proof['seo_changes'].append({'file': filename, 'key': key, 'before': before[key], 'after': value})
    (THEME / filename).write_text(text)

copies = json.loads((ROOT / 'shipping_copy.json').read_text())
assert len(copies) == 35
for locale, copy in copies.items():
    filename = f'locales/{locale}.json'
    text = (THEME / filename).read_text()
    data = parse(text)
    assert 'shipping_checkout' not in data['products']['purchase_confidence']
    text, n = re.subn(r'("purchase_confidence": \{\n)', lambda match: match[0] + '      "shipping_checkout": ' + json.dumps(copy, ensure_ascii=False) + ',\n', text)
    assert n == 1 and parse(text)['products']['purchase_confidence']['shipping_checkout'] == copy
    (THEME / filename).write_text(text)

filename = THEME / 'snippets/pdp-purchase-confidence.liquid'
text = filename.read_text()
text = re.sub(r'^\{%- comment -%\}[\s\S]*?\{%- endcomment -%\}', '{%- comment -%}\n  Purchase confidence: localized shipping options, qualified returns and secure checkout.\n  Destination and currency reflect the current Shopify localization.\n{%- endcomment -%}', text, count=1)
text = re.sub(r'  # CRO: standardized delivery window[\s\S]*?  assign pc_window =[^\n]*\n', '', text, count=1)
text = text.replace('pc_shipping_info_url', 'pc_shipping_policy_url').replace("'pages/shipping-info'", "'policies/shipping-policy'").replace("'/pages/shipping-info'", "'/policies/shipping-policy'")
text = re.sub(r"  if pc_country_code != blank\n    assign pc_shipping_policy_url =[^\n]*\n  endif\n", '', text, count=1)
text = text.replace("  assign pc_country_code = localization.country.iso_code | default: ''\n", '')
text = re.sub(r'  # Estimate line[\s\S]*?(?=  # "Ships to)', "  assign pc_shipping_checkout = 'products.purchase_confidence.shipping_checkout' | t\n  if pc_shipping_checkout == blank or pc_shipping_checkout contains 'translation missing'\n    assign pc_shipping_checkout = 'See shipping options at checkout.'\n  endif\n\n", text, count=1)
text, n = re.subn(r'      <p\n        class="dlm-pc-row__estimate"[\s\S]*?      </p>', '      <p class="dlm-pc-row__estimate">{{ pc_shipping_checkout }}</p>', text, count=1)
assert n == 1
text = text.replace('        <p>{{ pc_shipping_details_body }}</p>', '        <p>{{ pc_shipping_details_body }}</p>\n        <p><a class="dlm-pc-link" href="{{ pc_shipping_policy_url }}">{{ pc_shipping_details_label }}</a></p>', 1)
assert not any(s in text for s in ['12-16', 'pc_window', 'pc_estimate_template', 'dlm-shipping-card-date', 'data-delivery-estimate-row', 'data-delivery-window'])
filename.write_text(text)
proof['shipping'] = {'new_key': 'products.purchase_confidence.shipping_checkout', 'locale_count': 35, 'removed_target_id': 'dlm-shipping-card-date', 'shipping_policy_path': '/policies/shipping-policy', 'country_currency_preserved': True}
proof['consent_status'] = 'NOT_INTEGRATED_PENDING_ROOT_FINAL_PASS'
(ROOT / 'merge_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'verified_prior_sources': len(proof['sources']), 'seo_keys': len(proof['seo_changes']), 'shipping_locales': len(copies), 'cart_exact_reviewed': True, 'consent_integrated': False}))
