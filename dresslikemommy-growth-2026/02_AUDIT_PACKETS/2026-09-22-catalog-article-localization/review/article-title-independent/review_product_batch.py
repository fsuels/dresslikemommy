# -*- coding: utf-8 -*-
"""Bind manually reviewed corrections to frozen title worklists and body evidence."""
import copy
import hashlib
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
load = lambda path: json.loads(path.read_text())
file_sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
sha = lambda value: hashlib.sha256(value.encode()).hexdigest()
plain = lambda value: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value))).strip()
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
config_path = HERE / sys.argv[1]
config = load(config_path)
assert config['manualFullPairReviewComplete'] is True
input_file = ROOT / config['inputFile']
assert file_sha(input_file) == config['inputSHA256']
raw_rows = load(input_file)
rows = raw_rows if isinstance(raw_rows, list) else raw_rows['rows']
work = {}
for locale in {r['locale'] for r in rows}:
    f = ROOT / ('review/product-title-completeness/worklist_' + locale + '.json')
    for row in load(f)['rows']:
        work[row['i']] = (row, file_sha(f))
reviewed, proposals, held, checks = [], [], [], []
changes = config.get('changes', {})
for row in rows:
    inv, work_sha = work[row['i']]
    for key in ['resourceId', 'locale', 'key', 'marketId', 'sourceValue', 'sourceDigest', 'sourceSHA256', 'rawBefore', 'effectiveBeforeValue', 'expectedEffectiveBeforeValueSHA256', 'overlayApplied', 'overlaySourceFile', 'overlaySourceFileSHA256', 'rawFile', 'rawFileSHA256', 'before']:
        assert row[key] == inv[key], (row['i'], key)
    assert row['sourceSHA256'] == sha(row['sourceValue'])
    assert row['valueSHA256'] == sha(row['value'])
    assert row.get('expectedBeforeValueSHA256', row['expectedEffectiveBeforeValueSHA256']) == sha(row['effectiveBeforeValue'])
    assert row['rawFileSHA256'] == file_sha(ROOT / row['rawFile'])
    raw = load(ROOT / row['rawFile'])
    node = next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId'] == row['resourceId'])
    title = next(t for t in node['translatableContent'] if t['key'] == 'title')
    body = next(t for t in node['translatableContent'] if t['key'] == 'body_html')
    assert title['value'] == row['sourceValue'] and title['digest'] == row['sourceDigest']
    if row.get('supportingSourceDigests'):
        assert row['supportingSourceDigests']['body_html'] == body['digest']
    if row.get('supportingSourceBodySHA256'):
        assert row['supportingSourceBodySHA256'] == sha(body['value'])
    if row.get('supportingSourceQuoteNormalizedWhitespace'):
        assert row['supportingSourceQuoteNormalizedWhitespace'] in plain(body['value'])
    evidence = row.get('clippedConceptEvidence')
    if evidence:
        assert evidence['resourceId'] == row['resourceId']
        assert evidence['supportingSourceDigests']['body_html'] == body['digest']
        assert evidence['bodyValueSHA256'] == sha(body['value'])
        assert evidence['exactQuoteNormalizedWhitespace'] in plain(body['value'])
    target = copy.deepcopy(row)
    target['expectedBeforeValueSHA256'] = sha(row['effectiveBeforeValue'])
    target['independentInputFile'] = str(input_file.relative_to(ROOT))
    target['independentInputFileSHA256'] = file_sha(input_file)
    target['independentWorklistSHA256'] = work_sha
    hold_reason = config.get('holdIndices', {}).get(str(row['i']))
    if hold_reason:
        target['independentHoldReason'] = hold_reason
        target['independentReviewStatus'] = 'EXACT_SOURCE_CONFLICT'
        held.append(target)
        continue
    change = changes.get(str(row['i']))
    if change:
        target['beforeCandidateValue'] = row['value']
        target['value'] = change['value']
        target['valueSHA256'] = sha(change['value'])
        target['independentCorrectionReason'] = change['reason']
        if change.get('exactBodyQuote'):
            assert change['exactBodyQuote'] in plain(body['value']), row['i']
            target['supportingSourceDigests'] = {'body_html': body['digest']}
            target['independentSupportingSourceEvidence'] = {'resourceId': row['resourceId'], 'bodyValueSHA256': sha(body['value']), 'exactQuoteNormalizedWhitespace': change['exactBodyQuote']}
        proposals.append(copy.deepcopy(target))
    target['reviewStatus'] = 'INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    target['independentReviewStatus'] = 'PASS_VISIBLE_SOURCE_TITLE_MEANING_WITH_PRESERVED_UNKNOWN_FRAGMENTS'
    target['requiresFreshLiveSourceAndBeforeGuard'] = True
    reviewed.append(target)
    checks.append({'i': row['i'], 'resourceId': row['resourceId'], 'locale': row['locale'], 'sourceDigestBeforeRawWorklistBodyBindings': 'PASS', 'meaning': 'PASS_AFTER_CORRECTION' if change else 'PASS'})
assert len(rows) == len({r['i'] for r in rows}) == config['expectedCount']
prefix = config['outputPrefix']
dump(prefix + '_reviewed.json', {'rows': reviewed})
dump(prefix + '_corrections.json', {'rows': proposals})
dump(prefix + '_holds.json', {'rows': held})
dump(prefix + '_checks.json', {'reviewed': len(rows), 'qualified': len(reviewed), 'corrections': len(proposals), 'held': len(held), 'checks': checks, 'reviewConfigSHA256': file_sha(config_path), 'limitation': 'Known words translated; exact unknown clipped fragments preserved per root instruction. Root must freshly verify source/current before and all supporting body digests before release.'})
print(json.dumps({'qualified': len(reviewed), 'corrections': len(proposals), 'held': len(held), 'prefix': prefix}))
