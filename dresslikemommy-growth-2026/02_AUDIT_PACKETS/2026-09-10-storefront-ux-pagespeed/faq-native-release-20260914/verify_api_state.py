"""Compare independent API reads with frozen before values and exact candidates."""
from pathlib import Path
import json
import hashlib
import argparse
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--phase', choices=['preflight', 'page', 'final'], required=True)
args = parser.parse_args()

def read(name):
    return json.loads((P / name).read_text())

def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()

manifest = read('release-source-manifest.json')
before = read('inventory-before.json')['data']
after = read('inventory-' + args.phase + '.json')['data']
expected_body = (P / ('before/en.html' if args.phase == 'preflight' else 'candidates/en.html')).read_bytes().decode()
checks = {
    'shop_identity_and_domain_unchanged': before['shop'] == after['shop'],
    'protected_page_fields_unchanged': all(after['page'][k] == value for k, value in manifest['protected_page_fields'].items()),
    'page_body_exact': after['page']['body'] == expected_body,
    'enabled_locale_configuration_unchanged': before['shopLocales'] == after['shopLocales'],
    'market_configuration_unchanged': before['markets'] == after['markets'],
    'source_identity_exact': after['translatableResource']['resourceId'] == manifest['page_id'],
    'nonbody_source_fields_unchanged': [x for x in after['translatableResource']['translatableContent'] if x['key'] != 'body_html'] == manifest['protected_translatable_source'],
}
source = next(x for x in after['translatableResource']['translatableContent'] if x['key'] == 'body_html')
checks['source_body_value_and_digest_exact'] = source['value'] == expected_body and source['digest'] == sha(expected_body)
checks['no_unexpected_source_keys'] = [x['key'] for x in before['translatableResource']['translatableContent']] == [x['key'] for x in after['translatableResource']['translatableContent']]

def records(resource):
    result = {}
    for key, values in resource.items():
        if key.startswith('t_'):
            for item in values:
                identity = (item['locale'], (item['market'] or {}).get('id'), item['key'])
                assert identity not in result
                result[identity] = item
    return result

translation_results = []
qualified = {(x['locale'], x['marketId'], x['key']): x for x in manifest['qualified']}
for entry in manifest['market_scope_reads']:
    suffix = entry['scope']['id'].split('/')[-1] if entry['scope']['id'] else 'global'
    # Page checkpoint only needs the global records immediately before registration.
    if args.phase == 'page' and suffix != 'global':
        continue
    original = read('translations-before-' + suffix + '.json')
    latest = read('translations-' + args.phase + '-' + suffix + '.json')
    assert latest['scope'] == original['scope']
    old = records(original['data']['translatableResource'])
    new = records(latest['data']['translatableResource'])
    checks['translation_identities_' + suffix] = set(old) == set(new)
    for identity, prior in old.items():
        actual = new.get(identity)
        assert actual is not None, identity
        target = qualified.get(identity) if args.phase == 'final' else None
        expected = (P / target['candidate_path']).read_bytes().decode() if target else prior['value']
        preserved_metadata = all(actual[k] == prior[k] for k in prior if k not in (['value','updatedAt','outdated'] if target else []))
        value_matches = actual['value'] == expected
        metadata_expected = (actual['outdated'] is False and actual['updatedAt'] is not None) if target else preserved_metadata
        translation_results.append({'locale':identity[0], 'marketId':identity[1], 'key':identity[2], 'value_sha256':sha(actual['value'] or ''), 'expected_value_exact':value_matches, 'protected_metadata_exact':preserved_metadata, 'expected_metadata_state':metadata_expected, 'changed':bool(target)})
checks['all_translation_values_and_protected_metadata'] = all(x['expected_value_exact'] and x['protected_metadata_exact'] and x['expected_metadata_state'] for x in translation_results)
result = {'observedAt':datetime.now(timezone.utc).isoformat(),'phase':args.phase,'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'page_body_sha256':sha(after['page']['body']),'source_digest':source['digest'],'translation_records_checked':len(translation_results),'translation_records':translation_results,'expected_metadata_note':'Registered body translations become outdated=false without certifying existing business wording or semantic freshness.'}
(P / ('api-verification-' + args.phase + '.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'translation_records'},indent=2))
assert all(checks.values()), [k for k,v in checks.items() if not v]
