#!/usr/bin/env python3
"""Build exact local review handoff; no release, credentials, or network access."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def value_sha(value):
    return hashlib.sha256(value.encode()).hexdigest() if value is not None else None

def key(row):
    return row['resourceId'], row['locale'], row['key']

def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

manifest = read(HERE / 'remaining_manifest.json')
original_keys = {key(r) for r in read(HERE / 'baseline.json')['rows']}
raw_cache, seen, candidates, inverses, bindings = {}, set(), [], [], []
for artifact in manifest['artifacts']:
    if artifact['status'] != 'INDEPENDENT_REVIEW_PASS_REQUIRES_LIVE_GUARDS':
        continue
    path = HERE / artifact['path']
    assert sha(path) == artifact['sha256']
    for row in read(path)['rows']:
        ident = key(row)
        assert ident not in seen
        seen.add(ident)
        assert row['locale'] != 'en' and row.get('marketId') is None
        raw_path = HERE.parent / row['rawFile'] if row.get('rawFile') else HERE / 'linked_metaobjects_before.json'
        if raw_path not in raw_cache:
            data = read(raw_path)['data']['translatableResourcesByIds']['nodes']
            raw_cache[raw_path] = {r['resourceId']: r for r in data}
        resource = raw_cache[raw_path][row['resourceId']]
        source = next(x for x in resource['translatableContent'] if x['key'] == row['key'] and x['locale'] == 'en')
        assert source['value'] == row['source'] and source['digest'] == row['sourceDigest'], ident
        # Inspect explicit row locale+market, never trust a query alias alone.
        current = []
        for alias, values in resource.items():
            if not alias.startswith('tr_'):
                continue
            for value in values:
                if value['locale'] == row['locale'] and value['key'] == row['key'] and value.get('market') is None and value not in current:
                    current.append(value)
        assert len(current) <= 1, (ident, 'conflicting explicit locale rows')
        assert (current[0] if current else None) == row['before'], (ident, 'before mismatch')
        assert isinstance(row['value'], str) and row['value'].strip()
        record = {**row, 'preparedArtifact': artifact['path'], 'preparedArtifactSHA256': artifact['sha256'],
                  'localReviewStatus': artifact['status'], 'valueSHA256': value_sha(row['value']),
                  'sourceSHA256': value_sha(row['source']), 'expectedBeforeValueSHA256': value_sha(row['before']['value'] if row['before'] else None),
                  'originalFlag': ident in original_keys}
        candidates.append(record)
        inverses.append({'resourceId': row['resourceId'], 'locale': row['locale'], 'key': row['key'], 'marketId': None,
                         'sourceDigest': row['sourceDigest'], 'beforeMetadata': row['before'],
                         'value': row['before']['value'] if row['before'] else None,
                         'operation': 'translationsRegister' if row['before'] else 'translationsRemove',
                         'expectedCurrentValueSHA256': value_sha(row['value']), 'requiresFreshSourceAndCurrentValueGuard': True})
        bindings.append({'resourceId': row['resourceId'], 'locale': row['locale'], 'key': row['key'],
                         'rawFile': str(raw_path.relative_to(HERE.parent)), 'sourceDigest': row['sourceDigest'],
                         'valueSHA256': value_sha(row['value']), 'explicitLocaleAndGlobalMarketBinding': 'PASS'})

assert len(candidates) == 1899
assert sum(r['originalFlag'] for r in candidates) == 1879
assert sum(r['key'] == 'body_html' for r in candidates) == 230
review_files = ['sv_final_independent_review.json', 'ru_final_independent_review.json',
                'sv-bodies/blue_daisy_independent_review_v2.json', 'ru-bodies/other_body_independent_review_v2.json',
                'ru-bodies/option_fields_independent_review_v2.json', 'sv-bodies/short_fields_independent_review_v2.json']
reviews, reviewed_files = [], set()
for name in review_files:
    path = HERE / name
    result = read(path)
    assert result['status'].startswith('PASS_WITH_LIMITS')
    files = result.get('files', [{'path': result.get('candidateFile'), 'sha256': result.get('candidateSHA256')}])
    for f in files:
        target = Path(f['path'])
        target = target if target.is_absolute() else HERE / target
        assert sha(target) == f['sha256'], f
        reviewed_files.add(str(target.relative_to(HERE)))
    reviews.append({'path': name, 'sha256': sha(path), 'status': result['status']})
assert all(r['preparedArtifact'] in reviewed_files for r in candidates)
write('prepared_remaining_candidates.json', {'status': 'LOCAL_CANDIDATES_NOT_APPLIED', 'rows': candidates})
write('prepared_remaining_inverse.json', {'status': 'EXACT_INVERSES_REQUIRE_FRESH_GUARDS', 'rows': inverses})
result = {'status': 'PASS_LOCAL_BINDINGS_RELEASE_NOT_RUN', 'candidateFields': len(candidates), 'originalFields': 1879, 'extraFields': 20,
          'independentlyReviewedBodyFields': 230, 'independentlyReviewedNonBodyFields': 1669, 'pendingIndependentReviewFields': 0,
          'inverseRegisterCount': sum(r['operation'] == 'translationsRegister' for r in inverses),
          'inverseRemoveCount': sum(r['operation'] == 'translationsRemove' for r in inverses),
          'sourceSnapshots': [{'path': str(p.relative_to(HERE.parent)), 'sha256': sha(p)} for p in sorted(raw_cache)],
          'independentReviewReceipts': reviews,
          'outputs': [{'path': n, 'sha256': sha(HERE / n)} for n in ['prepared_remaining_candidates.json', 'prepared_remaining_inverse.json', 'remaining_manifest.json']],
          'bindings': bindings,
          'limits': ['Raw source and before comparison uses frozen local snapshots, not current live Shopify state.',
                     'Explicit row locale and global market checked for every candidate; alias alone never accepted.',
                     'No release performed; parent owns fresh digest/current-before validation, final authorization, application and public verification.',
                     'All 918 held original fields remain outside this candidate file. No ads, negatives, handles, prices, inventory or English source edits.']}
write('prepared_remaining_checks.json', result)
print({k: result[k] for k in ['status', 'candidateFields', 'originalFields', 'extraFields', 'independentlyReviewedBodyFields', 'inverseRegisterCount', 'inverseRemoveCount']})
