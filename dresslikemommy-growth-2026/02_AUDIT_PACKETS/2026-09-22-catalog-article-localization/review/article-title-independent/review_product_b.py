# -*- coding: utf-8 -*-
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
REVIEWED = {
    'ja': {'count': 55, 'corrections': {}, 'extraEvidence': {1171: 'Available in a variety of vibrant prints, including lemon, floral, and abstract patterns'}},
    'ko': {'count': 35, 'corrections': {}, 'extraEvidence': {}},
}

locale = sys.argv[1]
manual = REVIEWED[locale]
input_file = ROOT / ('review/product-title-completeness-b/candidate_' + locale + '_v1.json')
work_file = ROOT / ('review/product-title-completeness/worklist_' + locale + '.json')
rows = load(input_file)['rows']
work = {r['i']: r for r in load(work_file)['rows']}
reviewed, proposals, checks = [], [], []
for row in rows:
    inv = work[row['i']]
    for key in ['resourceId', 'locale', 'key', 'marketId', 'sourceValue', 'sourceDigest', 'sourceSHA256', 'rawBefore', 'effectiveBeforeValue', 'expectedEffectiveBeforeValueSHA256', 'overlayApplied', 'overlaySourceFile', 'overlaySourceFileSHA256', 'rawFile', 'rawFileSHA256', 'before']:
        assert row[key] == inv[key], (row['i'], key)
    assert row['inputWorklistFileSHA256'] == file_sha(work_file)
    assert row['sourceSHA256'] == sha(row['sourceValue'])
    assert row['valueSHA256'] == sha(row['value'])
    assert row['expectedBeforeValueSHA256'] == sha(row['effectiveBeforeValue'])
    assert row['rawFileSHA256'] == file_sha(ROOT / row['rawFile'])
    raw = load(ROOT / row['rawFile'])
    node = next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId'] == row['resourceId'])
    title = next(t for t in node['translatableContent'] if t['key'] == 'title')
    body = next(t for t in node['translatableContent'] if t['key'] == 'body_html')
    assert title['value'] == row['sourceValue'] and title['digest'] == row['sourceDigest']
    if row.get('supportingSourceDigests'):
        assert row['supportingSourceDigests']['body_html'] == body['digest']
    evidence = row.get('clippedConceptEvidence')
    if evidence:
        assert evidence['resourceId'] == row['resourceId']
        assert evidence['supportingSourceDigests']['body_html'] == body['digest']
        assert evidence['bodyValueSHA256'] == sha(body['value'])
        assert evidence['exactQuoteNormalizedWhitespace'] in plain(body['value']), row['i']
    target = copy.deepcopy(row)
    if row['i'] in manual['corrections']:
        value, reason = manual['corrections'][row['i']]
        target['beforeCandidateValue'] = row['value']
        target['value'] = value
        target['valueSHA256'] = sha(value)
        target['independentCorrectionReason'] = reason
    if row['i'] in manual['extraEvidence']:
        quote = manual['extraEvidence'][row['i']]
        assert quote in plain(body['value'])
        target['supportingSourceDigests'] = {'body_html': body['digest']}
        target['independentSupportingSourceEvidence'] = {'resourceId': row['resourceId'], 'bodyValueSHA256': sha(body['value']), 'exactQuoteNormalizedWhitespace': quote}
        target['independentEvidenceRepair'] = 'Clipped concept is established by this exact current body quote; attach the missing supporting source clock.'
    target['independentReviewStatus'] = 'PASS_COMPLETE_TITLE_MEANING_AND_SOURCE_BINDINGS'
    target['reviewStatus'] = 'INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    target['independentInputFile'] = str(input_file.relative_to(ROOT))
    target['independentInputFileSHA256'] = file_sha(input_file)
    target['requiresFreshLiveSourceAndBeforeGuard'] = True
    reviewed.append(target)
    if row['i'] in manual['corrections'] or row['i'] in manual['extraEvidence']:
        proposals.append(copy.deepcopy(target))
    checks.append({'i': row['i'], 'resourceId': row['resourceId'], 'locale': locale, 'key': 'title', 'sourceDigestBeforeRawWorklistBodyBindings': 'PASS', 'meaning': 'PASS_WITH_WORDING_CORRECTION' if row['i'] in manual['corrections'] else 'PASS'})
assert len(reviewed) == len({r['i'] for r in reviewed}) == manual['count']
prefix = 'product_' + locale + str(len(reviewed))
dump(prefix + '_reviewed.json', {'rows': reviewed})
dump(prefix + '_corrections.json', {'wordingCorrections': len(manual['corrections']), 'missingContextAttachmentRepairs': len(manual['extraEvidence']), 'rows': proposals})
dump(prefix + '_checks.json', {'status': 'PASS', 'reviewed': len(reviewed), 'qualified': len(reviewed), 'wordingCorrections': len(manual['corrections']), 'missingContextAttachmentRepairs': len(manual['extraEvidence']), 'held': 0, 'checks': checks, 'limitation': 'All proposed corrections independently read; producer owns retained/source-held dispositions. Root must freshly verify source/current before and supporting body digests before release.'})
print(json.dumps({'locale':locale,'qualified':len(reviewed),'wordingCorrections':len(manual['corrections']),'evidenceRepairs':len(manual['extraEvidence']),'held':0}))
