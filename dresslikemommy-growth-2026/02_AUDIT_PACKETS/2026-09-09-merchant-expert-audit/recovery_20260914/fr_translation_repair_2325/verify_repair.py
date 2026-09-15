"""Validate this exact French translation operation and its independent readback."""
import hashlib
import json
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PRIVATE = Path('/Users/fsuels/.config/dresslikemommy/merchant-evidence/20260914-fr-translation-repair')

def read(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def nodes(value):
    return {r['resourceId']: r for r in value['data']['translatableResourcesByIds']['nodes']}

phase = sys.argv[1]
assert phase in ('prewrite', 'after')
proposal = read(ROOT / 'proposal.json')
review = read(ROOT / 'independent_prewrite_review.json')
before = read(PRIVATE / 'before.json')
fresh = read(PRIVATE / 'prewrite_final.json')
variables = read(ROOT / 'register.variables.json')
assert review['verdict'] == 'PASS_WITH_LIMITS'
assert review['reviewed_proposal_sha256'] == sha(ROOT / 'proposal.json')
assert review['reviewed_query_sha256'] == sha(ROOT / 'register.graphql'), 'Reviewed mutation document changed'
assert review['reviewed_variables_sha256'] == sha(ROOT / 'register.variables.json'), 'Reviewed mutation values changed'
assert proposal['locale'] == 'fr' and proposal.get('marketId') is None
assert nodes(before) == nodes(fresh), 'Source or French translations changed before write'
assert before['data']['nodes'] == fresh['data']['nodes'], 'Product state changed before write'
assert fresh['data']['shop'] == {'id': 'gid://shopify/Shop/15571635', 'myshopifyDomain': 'dresslikemommy-com.myshopify.com'}
assert len(fresh['data']['nodes']) == 10 and all(p['status'] == 'ACTIVE' and p['onlineStoreUrl'] for p in fresh['data']['nodes'])
assert not fresh['data']['translatableResourcesByIds']['pageInfo']['hasNextPage']
resources = nodes(fresh)
changes = {(c['resourceId'], c['key']): c for c in proposal['changes']}
assert len(changes) == len(proposal['changes']) == 25 and not proposal.get('blocked')
outdated = {(rid, x['key']) for rid, resource in resources.items() for x in resource['translations'] if x['outdated']}
assert outdated == set(changes), 'Must repair exactly this reviewed outdated cohort'
assert len({rid for rid, key in changes}) == 10
assert all(key in {'title', 'body_html', 'product_type', 'meta_title', 'meta_description'} for rid, key in changes)
submitted = {}
for i in range(10):
    rid = variables['resource' + str(i)]
    for field in variables['translations' + str(i)]:
        key = (rid, field['key'])
        assert key not in submitted
        source = next(x for x in resources[rid]['translatableContent'] if x['key'] == field['key'])
        expected = changes[key]
        assert field == {'locale': 'fr', 'key': expected['key'], 'value': expected['value'], 'translatableContentDigest': source['digest']}
        assert source['digest'] == expected['sourceDigest']
        assert not re.search(r'alicdn|alibaba|aliexpress|1688\.com|taobao|tmall|admin\.shopify\.com|REDACTED_SOURCE_URL', field['value'], re.I)
        assert field['value'].strip()
        submitted[key] = field
assert set(submitted) == set(changes)
assert set(variables) == {key for i in range(10) for key in ('resource' + str(i), 'translations' + str(i))}
result = {
    'action': proposal['action'], 'validatedAt': datetime.now(timezone.utc).isoformat(),
    'phase': phase, 'productsTargeted': 10, 'fieldsTargeted': 25,
    'proposalSha256': sha(ROOT / 'proposal.json'),
    'reviewSha256': sha(ROOT / 'independent_prewrite_review.json'),
    'querySha256': sha(ROOT / 'register.graphql'),
    'variablesSha256': sha(ROOT / 'register.variables.json'),
    'privateBeforeSha256': sha(PRIVATE / 'before.json'),
    'privatePrewriteSha256': sha(PRIVATE / 'prewrite_final.json'),
    'sourceObservedAt': fresh['observedAt'], 'sourceCompletedAt': fresh['completedAt'],
    'sourceDrift': False, 'exactScopeVerified': True,
}
if phase == 'prewrite':
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(fresh['completedAt'].replace('Z', '+00:00'))).total_seconds()
    assert 0 <= age < 600, 'Prewrite source is outside the ten-minute window'
    result.update(guardAgeSeconds=age, status='PASS_READY_FOR_EXACT_AUTHORIZED_WRITE')
else:
    after = read(PRIVATE / 'after.json')
    actual = nodes(after)
    assert after['data']['shop'] == fresh['data']['shop']
    assert after['data']['nodes'] == fresh['data']['nodes'], 'Untargeted product identity/status/title changed'
    assert set(actual) == set(resources)
    assert not after['data']['translatableResourcesByIds']['pageInfo']['hasNextPage']
    unchanged = source_fields = 0
    for rid, original in resources.items():
        assert actual[rid]['translatableContent'] == original['translatableContent'], 'English source drift'
        source_fields += len(original['translatableContent'])
        old_fields = {x['key']: x for x in original['translations']}
        new_fields = {x['key']: x for x in actual[rid]['translations']}
        assert set(old_fields) == set(new_fields)
        for key, old in old_fields.items():
            new = new_fields[key]
            if (rid, key) in changes:
                assert new == {'key': key, 'value': changes[(rid, key)]['value'], 'locale': 'fr', 'outdated': False}
            else:
                assert old == new, 'Untargeted French field drift'
                unchanged += 1
    assert unchanged == 25 and source_fields == 60
    result.update(status='VERIFIED_25_EXACT_FRENCH_CHANGES', privateAfterSha256=sha(PRIVATE / 'after.json'),
                  afterCompletedAt=after['completedAt'], unchangedFrenchFields=unchanged,
                  unchangedEnglishFieldsAndDigests=source_fields, productIdentitiesAndStatusesUnchanged=10)
(ROOT / (phase + '_verification.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
