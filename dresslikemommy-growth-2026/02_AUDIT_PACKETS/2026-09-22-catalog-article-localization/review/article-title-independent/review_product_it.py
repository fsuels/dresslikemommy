# -*- coding: utf-8 -*-
import copy
import hashlib
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
load = lambda path: json.loads(path.read_text())
file_sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
sha = lambda value: hashlib.sha256(value.encode()).hexdigest()
plain = lambda value: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value))).strip()
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
input_file = ROOT / 'review/product-title-completeness-b/candidate_it_v1.json'
work_file = ROOT / 'review/product-title-completeness/worklist_it.json'
rows = load(input_file)['rows']
work = {r['i']: r for r in load(work_file)['rows']}

corrections = {
    870: ('Abiti lunghi floreali coordinati per mamma e bambino con spalline sul retro | DLM', 'English Mommy & Me and current body refer to children without establishing a daughter; preserve the generic child audience.'),
    1510: ('Set di T-shirt papà e io - un affettuoso legame tra padre e bambino | DLM', 'English Father-Child is generic; bambino avoids interpreting figlio specifically as son.'),
    2990: ('Pigiami in garza mamma e bambino "Peter Rabbit" - completo a maniche lunghe', 'English Mommy and Me and current body say little ones/Child, so do not narrow to daughters.'),
    3290: ('Set coordinato per la famiglia "Trail Plaid" - camicia con cappuccio per ripararsi dal sole e pantaloncini cargo', 'Sun shirt concerns sun coverage, not just lightweight construction; current body expressly supports easy sun coverage, without any UV or UPF claim.'),
}
extra_evidence = {
    1170: 'Available in a variety of vibrant prints, including lemon, floral, and abstract patterns',
    3290: 'the lightweight hooded shirt for easy sun coverage',
    830: 'Matching set for mother and daughter, ideal for casual outings, photoshoots, or vacations.',
    890: 'these dresses offer effortless style for both mom and daughter.',
    2670: 'Coordinating mother and daughter sets',
    2750: 'Girls 1–2Y / 3–4Y / 5–6Y and Mother One Size',
    2930: 'Picture-perfect matching pajamas for mom and daughter',
    3130: 'A picture-perfect matching cami dress for mom and daughter',
    3190: 'A coastal-ready matching set for mom and daughter',
    3970: 'Pick matching pieces for mom and daughter',
}
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
    if row['i'] in corrections:
        value, reason = corrections[row['i']]
        target['beforeCandidateValue'] = row['value']
        target['value'] = value
        target['valueSHA256'] = sha(value)
        target['independentCorrectionReason'] = reason
    if row['i'] in extra_evidence:
        quote = extra_evidence[row['i']]
        assert quote in plain(body['value']), row['i']
        target['supportingSourceDigests'] = {'body_html': body['digest']}
        target['independentSupportingSourceEvidence'] = {'resourceId': row['resourceId'], 'bodyValueSHA256': sha(body['value']), 'exactQuoteNormalizedWhitespace': quote}
        if row['i'] == 1170:
            target['independentEvidenceRepair'] = 'Pri... → prints is established by this exact current body quote; attachment fills the author metadata omission without changing target wording.'
    target['independentReviewStatus'] = 'PASS_COMPLETE_TITLE_MEANING_AND_SOURCE_BINDINGS'
    target['reviewStatus'] = 'INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    target['independentInputFile'] = str(input_file.relative_to(ROOT))
    target['independentInputFileSHA256'] = file_sha(input_file)
    target['requiresFreshLiveSourceAndBeforeGuard'] = True
    reviewed.append(target)
    if row['i'] in corrections or row['i'] == 1170:
        proposals.append(copy.deepcopy(target))
    checks.append({'i': row['i'], 'resourceId': row['resourceId'], 'locale': 'it', 'key': 'title', 'sourceDigestBeforeRawAndWorklistBinding': 'PASS', 'attachedBodyDigestAndQuotes': 'PASS', 'meaning': 'PASS_WITH_WORDING_CORRECTION' if row['i'] in corrections else 'PASS'})
assert len(reviewed) == len({r['i'] for r in reviewed}) == 79
dump('product_it79_reviewed.json', {'rows': reviewed})
dump('product_it79_corrections.json', {'wordingCorrections': 4, 'missingContextAttachmentRepairs': 1, 'rows': proposals})
dump('product_it79_checks.json', {'status': 'PASS', 'candidateTitlesReviewed': 79, 'wordingCorrections': 4, 'missingContextAttachmentRepairs': 1, 'checks': checks, 'limitation': 'Independent review covers all79 proposed corrections. Producer owns retained141 and held18 dispositions. No external state changed; fresh supporting-body digest and source/current-before guards required.'})
print(json.dumps({'reviewed': len(reviewed), 'wordingCorrections': len(corrections), 'missingEvidenceRepaired': 1, 'checks': 'PASS'}))
