#!/usr/bin/env python3
"""Bound final review checks; offline only. Meaning review is recorded separately."""
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'tooling'))
import offline_translation as ot

def rows(path):
    return json.loads((HERE / path).read_text())['rows']

def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()

def strip_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.S)

path = 'sv-bodies/qualified_candidates.json'
candidates = rows(path)
baseline = {ot.key(r): r for r in rows('body_baseline.json')}
inverse = {ot.key(r): r for r in rows('sv-bodies/qualified_inverse.json')}
assert len(candidates) == 99 == len({ot.key(r) for r in candidates})
reports = []
for row in candidates:
    base, inv = baseline[ot.key(row)], inverse[ot.key(row)]
    assert all(row[k] == base[k] for k in ['source', 'sourceDigest', 'before'])
    assert inv['value'] == (row['before']['value'] if row['before'] else None)
    assert inv['sourceDigest'] == row['sourceDigest']
    assert inv['expectedCurrentValueSHA256'] == ot.sha(row['value'])
    assert inv['operation'] == ('translationsRegister' if row['before'] else 'translationsRemove')
    source, target = row['source'], row['value']
    strict = ot.verify_text(source, target, 'sv')['errors']
    adjudication = 'STRICT_SOURCE_PASS'
    if strict:
        assert strict == ['html_structure_or_attributes_changed']
        clean_source, clean_target = map(strip_comments, (source, target))
        if not ot.verify_text(clean_source, clean_target, 'sv')['errors']:
            adjudication = 'EXISTING_COMMENTS_ONLY_SOURCE_DIFFERENCE'
            assert ot.Shape(row['before']['value']).events == ot.Shape(target).events
        else:
            assert row['resourceId'] == 'gid://shopify/Product/7241105670241'
            tables = lambda s: re.findall(r'<table\b.*?</table>', s, flags=re.S)
            non_table = lambda s: re.sub(r'<table\b.*?</table>', '', s, flags=re.S)
            assert len(tables(clean_source)) == len(tables(clean_target)) == 1
            assert not ot.verify_text(tables(clean_source)[0], tables(clean_target)[0], 'sv')['errors']
            assert not ot.verify_text(non_table(clean_source), non_table(clean_target), 'sv')['errors']
            assert ot.Shape(row['before']['value']).events == ot.Shape(target).events
            adjudication = 'EXISTING_TABLE_POSITION_ONLY_SOURCE_DIFFERENCE'
    visible = '\n'.join(ot.Shape(target).text)
    residues = re.findall(r'\b(?:up to|approximately|years?|mother|father|child|size|height|weight|sleeve|waist|bust|length|fabric|care)\b', visible, re.I)
    assert not residues, (row['resourceId'], residues)
    reports.append({'resourceId': row['resourceId'], 'locale': 'sv', 'key': row['key'],
                    'valueSHA256': ot.sha(target), 'sourceDigest': row['sourceDigest'],
                    'exactLocalBindingAndInverse': 'PASS', 'strictSourceFindings': strict,
                    'adjudication': adjudication, 'meaningReview': 'PASS_WITH_LIMITS'})

result = {
    'status': 'PASS_WITH_LIMITS', 'reviewer': 'danish_scope_evidence',
    'candidateFile': path, 'candidateSHA256': sha(path), 'reviewedFields': len(reports),
    'inverseFile': 'sv-bodies/qualified_inverse.json', 'inverseSHA256': sha('sv-bodies/qualified_inverse.json'),
    'authorManifestFile': 'sv-bodies/final_manifest_v2.json', 'authorManifestSHA256': sha('sv-bodies/final_manifest_v2.json'),
    'method': 'Independent full visible prose comparison of all 99 final bodies with exact English sources, including source reuse only where exact source text matches previously read source. Manual care/negation/selection/product-type meaning review; programmatic baseline/digest/before, inverse, HTML/attributes/URLs, per-cell numeric/unit/size-code and residue checks. Original review histories preserved.',
    'counts': dict(collections.Counter(r['adjudication'] for r in reports)),
    'reports': reports,
    'limits': [
        'Local candidate acceptance only. No live read or write; release owner must recheck exact source digest and current before value.',
        'Twenty-five author-held fields excluded. This review does not approve their source claims or measurement changes.',
        'Twenty-one comment-only and one existing table-position differences explicitly retained after independent component equivalence checks; no numeric mismatch waived.',
        'Existing quoted garment slogans, technical units, size codes and image alt attributes preserved. No full-catalog or native-speaker certification.',
        'Faithful rendering of source product claims does not independently establish supplier accuracy.'
    ]
}
(HERE / 'sv_final_independent_review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'count': len(reports), 'checks': result['counts'], 'sha256': sha('sv_final_independent_review.json')}))
