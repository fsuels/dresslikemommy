#!/usr/bin/env python3
"""Independent final Russian structural/inverse checks; never calls a network."""
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

def clean(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    # Diagnostic-only unit equivalence, not a candidate edit. 'in' after slash
    # is omitted by the shared checker; Russian plural pounds is also missing.
    for before, after in [('cm/in', 'cm/inch'), ('см/дюйм', 'cm/inch'), ('кг/фунты', 'kg/lbs')]:
        text = text.replace(before, after)
    # These two exact prose phrases use см. = see, not cm. No table relaxation.
    text = text.replace('для точного выбора см. руководство по размерам', 'для точного выбора смотрите руководство по размерам')
    return text.replace('см. таблицу размеров', 'смотрите таблицу размеров')

path = 'ru-bodies/release_ready_for_peer_review.json'
candidates = rows(path)
baseline = {ot.key(r): r for r in rows('body_baseline.json')}
inverse = {ot.key(r): r for r in rows('ru-bodies/inverses_complete.json')}
assert len(candidates) == 93 == len({ot.key(r) for r in candidates})
reports, final_inverse = [], []
for row in candidates:
    base, inv = baseline[ot.key(row)], inverse[ot.key(row)]
    assert all(row[k] == base[k] for k in ['source', 'sourceDigest', 'before'])
    assert inv['value'] == (row['before']['value'] if row['before'] else None)
    assert inv['sourceDigest'] == row['sourceDigest']
    strict = ot.verify_text(row['source'], row['value'], 'ru')['errors']
    adjusted = ot.verify_text(clean(row['source']), clean(row['value']), 'ru')['errors']
    assert not adjusted, (row['resourceId'], adjusted)
    markup_baseline = row['before']['value'] if row['before'] else row['source']
    assert ot.Shape(row['value']).events == ot.Shape(markup_baseline).events
    visible = '\n'.join(ot.Shape(row['value']).text)
    residues = re.findall(r'\b(?:up to|approximately|years?|mother|father|child|size|height|weight|sleeve|waist|bust|length|fabric|care)\b', visible, re.I)
    assert not residues, (row['resourceId'], residues)
    reports.append({'resourceId': row['resourceId'], 'locale': 'ru', 'key': row['key'],
                    'valueSHA256': ot.sha(row['value']), 'sourceDigest': row['sourceDigest'],
                    'localBindingAndInverse': 'PASS', 'strictSourceFindings': strict,
                    'normalizedDiagnostic': 'PASS', 'markupBaseline': 'existing translation' if row['before'] else 'English source for missing translation',
                    'meaningReview': 'PASS_WITH_LIMITS'})
    final_inverse.append({'resourceId': row['resourceId'], 'locale': 'ru', 'key': row['key'],
                          'sourceDigest': row['sourceDigest'], 'value': inv['value'],
                          'beforeMetadata': row['before'], 'expectedCurrentValueSHA256': ot.sha(row['value']),
                          'operation': 'translationsRegister' if row['before'] else 'translationsRemove',
                          'requiresFreshSourceAndCurrentValueGuard': True})

inverse_path = 'ru_final_reviewed_inverse.json'
(HERE / inverse_path).write_text(json.dumps({'rows': final_inverse}, ensure_ascii=False, indent=2) + '\n')
result = {
    'status': 'PASS_WITH_LIMITS', 'reviewer': 'danish_scope_evidence', 'reviewedFields': len(reports),
    'candidateFile': path, 'candidateSHA256': sha(path), 'inverseFile': inverse_path, 'inverseSHA256': sha(inverse_path),
    'authorAdjudicationSHA256': sha('ru-bodies/final_adjudication.json'),
    'method': 'Independent full visible-prose comparison across all final author batches (112 drafts), with acceptance limited to the 93 source-qualified rows. Reused already-read source text only on exact equality. Recomputed exact local source/digest/before and inverse binding, HTML/attributes, per-cell measurements/units/size codes, numbers, URLs and residue checks. Earlier per-batch reviews retained.',
    'diagnosticNormalizations': [
        'Ignore HTML comments only when comparing source structure; all candidate comment/tag/attribute events remain exactly equal to before, or source if translation was missing.',
        'cm/in and Russian см/дюйм normalized in-memory to cm/inch; Russian кг/фунты to kg/lbs. Equivalent header units only; numbers unchanged.',
        'Two exact Russian prose phrases use см. as abbreviation for see, not centimetres; diagnostic normalization removes this false unit token.'
    ],
    'strictErrorCounts': dict(collections.Counter(e for r in reports for e in r['strictSourceFindings'])),
    'strictPassCount': sum(not r['strictSourceFindings'] for r in reports),
    'reports': reports,
    'limits': [
        'No live read or write. Parent must guard fresh source digest and exact current before value before release.',
        'Nineteen completed drafts with substantive source/table issues and two malformed existing bodies remain held; four borrowed-name no-change fields excluded.',
        'The corrected four-role wording in held Product 7229128441953 batch_06_v2 was independently checked as exactly the two requested phrase replacements; the source size-extrapolation/refund problem remains held.',
        'Existing quoted slogans, design names, technical units and image alt attributes preserved; no native-speaker or full-catalog certification.',
        'Source product and measurement claims are translated faithfully, not independently supplier-verified.'
    ]
}
(HERE / 'ru_final_independent_review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'fields': len(reports), 'strictPass': result['strictPassCount'], 'sha256': sha('ru_final_independent_review.json')}))
