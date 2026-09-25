#!/usr/bin/env python3
"""Close peer field dispositions without changing any author artifact."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read(path):
    return json.loads((HERE / path).read_text())

def rows(path):
    return read(path)['rows']

def key(row):
    return row['resourceId'], row['locale'], row['key']

def write(path, data):
    (HERE / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

base = {key(r): r for r in rows('body_baseline.json')}
ru = []
for report in read('ru-bodies/final_adjudication.json')['reports']:
    if report['disposition'] == 'HOLD':
        ru.append({**base[key(report)], 'disposition': 'HOLD_SOURCE_OR_TABLE', 'reviewEvidence': report,
                   'remainingWork': 'Resolve the exact listed source/measurement mismatch before translating or clearing the outdated flag.'})
for report in rows('ru-bodies/inherited_blockers.json'):
    ru.append({**base[key(report)], 'disposition': 'HOLD_MALFORMED_HTML', 'reviewEvidence': report,
               'remainingWork': 'Normalize malformed translated tags and reconcile the retained chart against exact current source measurements; do not silently replace numbers.'})
nochange = []
for report in rows('ru-bodies/no_change_dispositions.json'):
    if report['resourceId'].split('/')[-1] in ['7545279512673', '7545279840353']:
        assert report['before']['outdated'] is True
        ru.append({**base[key(report)], 'disposition': 'HOLD_CHANGED_SOURCE_CHART',
                   'reviewEvidence': {'noEnglishProseGap': True, 'outdated': True, 'reason': 'No English prose gap does not resolve changed source measurements. Existing Russian has the same stale Sunshine/Raglan chart issue held in other locales.', 'authorAcknowledged': True},
                   'remainingWork': 'Compare current source and existing Russian table cells, then reconcile current seller-backed options/measurements before registering any refreshed translation.'})
    else:
        nochange.append(report)
assert len(ru) == 23 and len(nochange) == 2
write('ru_body_final_holds.json', {'status': 'PRECISE_FIELD_HOLDS_NOT_RELEASE_CANDIDATES', 'rows': ru})
write('ru_body_final_no_change.json', {'status': 'REVIEWED_NAMED_LABEL_FALSE_POSITIVES', 'rows': nochange})

source_issues = rows('sv-bodies/new_source_blockers.json')
table_reviews = {key(r): r for r in rows('sv-bodies/existing_table_structure_proposals.json')}
sv = []
for row in rows('sv-bodies/blocked_fields.json'):
    issues = [r for r in source_issues if key(r) == key(row)]
    table = table_reviews.get(key(row))
    assert issues or table, key(row)
    sv.append({**row, 'disposition': 'HOLD_SOURCE_OR_MEASUREMENT', 'sourceIssues': issues,
               'tableReview': table, 'remainingWork': 'Resolve the exact source contradiction or listed table-cell/age mismatch; preserve current numeric cells until the source owner reconciles measurements.'})
for row in rows('sv-bodies/legacy_image_hold_candidates.json'):
    sv.append({**base[key(row)], 'disposition': 'HOLD_LEGACY_IMAGE_VARIANCE',
               'reviewEvidence': row['existingVarianceReview'],
               'authoredDraftArtifact': 'sv-bodies/legacy_image_hold_candidates.json',
               'remainingWork': 'Source owner decides whether the listed obsolete image tags should become br tags as in current source; body prose candidate already authored.'})
assert len(sv) == 25
write('sv_body_final_holds.json', {'status': 'PRECISE_FIELD_HOLDS_NOT_RELEASE_CANDIDATES', 'rows': sv})
print({'RussianHolds': len(ru), 'RussianNoChange': len(nochange), 'SwedishHolds': len(sv)})
