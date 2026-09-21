"""Exact, source-bound guards for the reviewed Navy 3XL consistency correction."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PRIVATE = Path('/Users/fsuels/.config/dresslikemommy/merchant-evidence/20260915-navy-size-consistency')
GID = 'gid://shopify/Product/7670609346657'
KEYS = {'body_html', 'meta_description'}

def read(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def resource(data):
    rows = data['translatableResourcesByIds']['nodes']
    assert len(rows) == 1 and rows[0]['resourceId'] == GID
    assert not data['translatableResourcesByIds']['pageInfo']['hasNextPage']
    return rows[0]

def exact_recipe(old, locale, key):
    if key == 'body_html':
        removed = []
        def remove(match):
            row = match.group(0)
            first = re.search(r'<td\b[^>]*>(.*?)</td>', row, re.S | re.I)
            if first and re.search(r'\b3XL\b', re.sub(r'<[^>]*>', '', first.group(1))):
                removed.append(row)
                return ''
            return row
        new = re.sub(r'<tr\b[^>]*>.*?</tr>', remove, old, flags=re.S | re.I)
        assert len(removed) == 2, (locale, len(removed))
        assert old.count('3XL') == 3 and new.count('3XL') == 1
        new = new.replace('3XL', '2XL')
        if locale == 'fr':
            assert new.count('Echaque') == 1
            new = new.replace('Echaque', 'Chaque')
        return new
    assert key == 'meta_description' and old.count('3XL') == 1
    return old.replace('3XL', '2XL')

def protect(data):
    assert data['shop'] == {'id': 'gid://shopify/Shop/15571635', 'myshopifyDomain': 'dresslikemommy-com.myshopify.com'}
    product = data['product']
    assert product['id'] == GID and product['status'] == 'ACTIVE'
    assert product['handle'] == 'navy-sprig-mommy-and-me-dresses' and product['onlineStoreUrl']
    assert len(product['variants']['nodes']) == 24
    for connection in ['variants', 'metafields', 'resourcePublicationsV2']:
        assert not product[connection]['pageInfo']['hasNextPage']
    for variant in product['variants']['nodes']:
        assert all('3XL' not in x['value'] for x in variant['selectedOptions'])
    assert len(product['metafields']['nodes']) == 27
    assert len(product['resourcePublicationsV2']['nodes']) == 9
    return resource(data)

phase = sys.argv[1]
assert phase in {'source-prewrite', 'source-after', 'translations-prewrite', 'after'}
before = read(PRIVATE / 'before.json')
fresh = read(PRIVATE / 'prewrite.json')
assert before['data'] == fresh['data'], 'Current source differs from proposal source'
r = protect(fresh['data'])
old_pairs = {('en', x['key']): x['value'] for x in r['translatableContent'] if x['key'] in KEYS}
for name, fields in r.items():
    if name.startswith('l_'):
        for field in fields:
            if field['key'] in KEYS:
                old_pairs[(field['locale'], field['key'])] = field['value']
assert len(old_pairs) == 42
proposal = read(ROOT / 'proposal.json')
candidate = {(x['locale'], x['key']): x['value'] for x in proposal['changes']}
assert len(candidate) == len(proposal['changes']) == 42
assert set(candidate) == set(old_pairs)
for pair, old in old_pairs.items():
    assert candidate[pair] == exact_recipe(old, *pair), 'Unexpected edit: ' + str(pair)
    assert '3XL' not in candidate[pair]
    assert not re.search(r'https?://[^\s\"<>]*(?:alicdn|1688\.com|admin\.shopify\.com)', candidate[pair], re.I)
review = read(ROOT / 'independent_prewrite_review.json')
assert review['verdict'] == 'PASS_WITH_LIMITS'
assert review['reviewed_proposal_sha256'] == sha(ROOT / 'proposal.json')
variables = read(ROOT / 'update_english.variables.json')
assert variables == {'product': {'id': GID, 'descriptionHtml': candidate[('en', 'body_html')], 'seo': {'description': candidate[('en', 'meta_description')]}}}
assert review['reviewed_english_query_sha256'] == sha(ROOT / 'update_english.graphql')
assert review['reviewed_english_variables_sha256'] == sha(ROOT / 'update_english.variables.json')
assert review['reviewed_translation_query_sha256'] == sha(ROOT / 'update_translations.graphql')
overrides = read(ROOT / 'market_overrides_before.json')
assert overrides['complete'] and len(overrides['reads']) == 6
for entry in overrides['reads']:
    assert not entry['data']['translatableResourcesByIds']['pageInfo']['hasNextPage']
    for res in entry['data']['translatableResourcesByIds']['nodes']:
        assert res['resourceId'] == GID
        assert len([k for k in res if k.startswith('l_')]) == 21
        assert not any(v for k, v in res.items() if k.startswith('l_'))
report = {'action': 'TA07-NAVY-SIZE-CONSISTENCY-20260914', 'phase': phase, 'validatedAt': datetime.now(timezone.utc).isoformat(), 'proposalSha256': sha(ROOT / 'proposal.json'), 'independentPrewriteReviewSha256': sha(ROOT / 'independent_prewrite_review.json'), 'fieldsTargeted': 42, 'productVariantsProtected': 24, 'privateBeforeSha256': sha(PRIVATE / 'before.json'), 'privatePrewriteSha256': sha(PRIVATE / 'prewrite.json')}
if phase == 'source-prewrite':
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(fresh['completedAt'].replace('Z', '+00:00'))).total_seconds()
    assert 0 <= age < 600
    report.update(status='PASS_EXACT_ENGLISH_WRITE_READY', sourceAgeSeconds=age)
else:
    english = read(PRIVATE / 'after_english.json')
    protect(english['data'])
    expected = copy.deepcopy(fresh['data'])
    expected['product']['descriptionHtml'] = candidate[('en', 'body_html')]
    expected['product']['seo']['description'] = candidate[('en', 'meta_description')]
    mirrored = 0
    for old, actual in zip(expected['product']['metafields']['nodes'], english['data']['product']['metafields']['nodes']):
        if (old['namespace'], old['key']) == ('global', 'description_tag'):
            assert old['id'] == actual['id'] and actual['value'] == candidate[('en', 'meta_description')]
            assert actual['compareDigest'] and actual['compareDigest'] != old['compareDigest']
            old['value'] = actual['value']
            old['compareDigest'] = actual['compareDigest']
            mirrored += 1
    assert mirrored == 1
    er = resource(expected)
    actual_source = {x['key']: x for x in resource(english['data'])['translatableContent']}
    for field in er['translatableContent']:
        if field['key'] in KEYS:
            new = actual_source[field['key']]
            assert new['value'] == candidate[('en', field['key'])]
            assert new['digest'] and new['digest'] != field['digest'] and new['locale'] == field['locale']
            field['value'], field['digest'] = new['value'], new['digest']
    for name, fields in er.items():
        if name.startswith('l_'):
            for field in fields:
                if field['key'] in KEYS:
                    field['outdated'] = True
    assert expected == english['data'], 'English write changed unapproved state'
    report.update(englishFieldsVerified=2, sourceDigestsRefreshed=2, protectedVariantRecordsUnchanged=24, protectedOtherMetafieldsUnchanged=26, existingTranslationValuesUnchangedAfterEnglish=100, sourceAfterCompletedAt=english['completedAt'], privateAfterEnglishSha256=sha(PRIVATE / 'after_english.json'))
    if phase in {'translations-prewrite', 'after'}:
        values = read(ROOT / 'update_translations.variables.json')
        assert set(values) == {'resourceId', 'translations'} and values['resourceId'] == GID
        submitted = {(x['locale'], x['key']): x for x in values['translations']}
        assert len(submitted) == len(values['translations']) == 40
        assert set(submitted) == {pair for pair in candidate if pair[0] != 'en'}
        for pair, field in submitted.items():
            assert field == {'locale': pair[0], 'key': pair[1], 'value': candidate[pair], 'translatableContentDigest': actual_source[pair[1]]['digest']}
        binding = read(ROOT / 'independent_translation_binding_review.json')
        assert binding['verdict'] == 'PASS_WITH_LIMITS'
        assert binding['reviewed_variables_sha256'] == sha(ROOT / 'update_translations.variables.json')
        assert binding['reviewed_query_sha256'] == sha(ROOT / 'update_translations.graphql')
        report['translationVariablesSha256'] = sha(ROOT / 'update_translations.variables.json')
        report['translationBindingReviewSha256'] = sha(ROOT / 'independent_translation_binding_review.json')
        if phase == 'translations-prewrite':
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(english['completedAt'].replace('Z', '+00:00'))).total_seconds()
            assert 0 <= age < 600
            report.update(status='PASS_EXACT_40_TRANSLATION_WRITE_READY', sourceAgeSeconds=age)
        else:
            after = read(PRIVATE / 'after.json')
            final = copy.deepcopy(english['data'])
            for name, fields in resource(final).items():
                if name.startswith('l_'):
                    for field in fields:
                        pair = (field['locale'], field['key'])
                        if pair in submitted:
                            field['value'], field['outdated'] = candidate[pair], False
            assert final == after['data'], 'Final write changed unapproved state'
            protect(after['data'])
            report.update(status='VERIFIED_42_FIELDS_ALL_21_LANGUAGES', afterCompletedAt=after['completedAt'], privateAfterSha256=sha(PRIVATE / 'after.json'), existingTranslationsUpdated=40, untargetedTranslationsPreserved=60, untargetedEnglishFieldsPreserved=4)
    else:
        report['status'] = 'VERIFIED_2_ENGLISH_FIELDS_TRANSLATIONS_PENDING'
(ROOT / (phase + '_verification.json')).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
