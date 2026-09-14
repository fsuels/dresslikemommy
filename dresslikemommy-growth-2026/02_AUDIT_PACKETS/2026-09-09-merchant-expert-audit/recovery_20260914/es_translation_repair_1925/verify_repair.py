"""Verify the exact reviewed Spanish translation operation and its readback."""
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = pathlib.Path('/Users/fsuels/.config/dresslikemommy/merchant-evidence/20260914-es-translation-repair')

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def nodes(value):
    return {r['resourceId']: r for r in value['data']['translatableResourcesByIds']['nodes']}

proposal = read(ROOT / 'proposal.json')
review = read(ROOT / 'independent_prewrite_review.json')
before = read(PRIVATE / 'before.json')
fresh = read(PRIVATE / 'prewrite_final.json')
variables = read(ROOT / 'register.variables.json')
assert review['verdict'] == 'PASS_WITH_LIMITS', review['verdict']
assert review['reviewed_proposal_sha256'] == sha(ROOT / 'proposal.json')
assert sha(ROOT / 'proposal.json') == '8f4fee9765c5b4ec4a5943955959c51d55ec4c4da2e85c8b2f89b2295f1241e6'
assert nodes(before) == nodes(fresh), 'Source or Spanish translations changed before write'
assert not fresh['data']['translatableResourcesByIds']['pageInfo']['hasNextPage']
resources = nodes(fresh)
changes = {(c['resourceId'], c['key']): c for c in proposal['changes']}
blocked = {(c['resourceId'], c['key']) for c in proposal['blocked']}
assert len(changes) == 25 and len(blocked) == 1 and not (set(changes) & blocked)
outdated = {(rid, x['key']) for rid, resource in resources.items() for x in resource['translations'] if x['outdated']}
assert outdated == set(changes) | blocked
assert blocked == {('gid://shopify/Product/7227378925665', 'body_html')}
submitted = {}
for i in range(10):
    rid = variables['resource' + str(i)]
    for field in variables['translations' + str(i)]:
        key = (rid, field['key'])
        assert key not in submitted
        source = next(x for x in resources[rid]['translatableContent'] if x['key'] == field['key'])
        expected = changes[key]
        assert field == {'locale': 'es', 'key': expected['key'], 'value': expected['value'], 'translatableContentDigest': source['digest']}
        assert source['digest'] == expected['sourceDigest']
        assert not re.search(r'alicdn|alibaba|aliexpress|1688|taobao|tmall|admin\.shopify\.com|REDACTED_SOURCE_URL', field['value'], re.I)
        submitted[key] = field
assert set(submitted) == set(changes)

result = {
    'action': proposal['action'],
    'validatedAt': datetime.now(timezone.utc).isoformat(),
    'phase': sys.argv[1],
    'productsTargeted': 10,
    'fieldsTargeted': 25,
    'blockedFields': 1,
    'proposalSha256': sha(ROOT / 'proposal.json'),
    'reviewSha256': sha(ROOT / 'independent_prewrite_review.json'),
    'querySha256': sha(ROOT / 'register.graphql'),
    'variablesSha256': sha(ROOT / 'register.variables.json'),
    'privateBeforeSha256': sha(PRIVATE / 'before.json'),
    'privatePrewriteSha256': sha(PRIVATE / 'prewrite_final.json'),
    'sourceObservedAt': fresh['observedAt'],
    'sourceCompletedAt': fresh['completedAt'],
    'sourceDrift': False,
    'exactScopeVerified': True,
}
if sys.argv[1] == 'prewrite':
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(fresh['completedAt'].replace('Z', '+00:00'))).total_seconds()
    assert age < 600, f'Fresh guard too old: {age}s'
    result['guardAgeSeconds'] = age
    result['status'] = 'PASS_READY_FOR_EXACT_AUTHORIZED_WRITE'
elif sys.argv[1] == 'after':
    after = read(PRIVATE / 'after.json')
    actual = nodes(after)
    assert set(actual) == set(resources)
    assert not after['data']['translatableResourcesByIds']['pageInfo']['hasNextPage']
    unchanged = 0
    for rid, original in resources.items():
        assert actual[rid]['translatableContent'] == original['translatableContent'], 'English source drift'
        old_fields = {x['key']: x for x in original['translations']}
        new_fields = {x['key']: x for x in actual[rid]['translations']}
        assert set(old_fields) == set(new_fields)
        for key, old in old_fields.items():
            new = new_fields[key]
            if (rid, key) in changes:
                assert new == {'key': key, 'value': changes[(rid, key)]['value'], 'locale': 'es', 'outdated': False}
            else:
                assert old == new, 'Untargeted Spanish field drift'
                unchanged += 1
    result.update(status='VERIFIED_25_EXACT_SPANISH_CHANGES', privateAfterSha256=sha(PRIVATE / 'after.json'), afterCompletedAt=after['completedAt'], unchangedSpanishFields=unchanged, EnglishResourcesUnchanged=11, blockedTropicalBodyUnchanged=True)
else:
    raise ValueError('Expected prewrite or after')
(ROOT / (sys.argv[1] + '_verification.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(result, ensure_ascii=False))
