import collections
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUTHOR = ROOT / 'review/article-title-completeness'
sha = lambda value: hashlib.sha256(value.encode()).hexdigest()
file_sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
load = lambda path: json.loads(path.read_text())
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
tuple_key = lambda row: (row['resourceId'], row['locale'], row['key'])

inventory = load(AUTHOR / 'inventory.json')
by_key = {tuple_key(row): row for row in inventory['rows']}
assert len(by_key) == len(inventory['rows']) == 1340
assert len({row['resourceId'] for row in inventory['rows']}) == 67
assert len({row['locale'] for row in inventory['rows']}) == 20

# Independent complete-title meaning review, not substitutions inferred by a heuristic.
corrections = {
    413: ('Opas perheen yhteensopivaan tyyliin välikauteen', 'Transitional weather is the between-season period; vaihtelevassa säässä instead means variable weather.'),
    600: ('מדריך מידות לתלבושות תואמות: איך למצוא את המידה המתאימה לכל אחד', 'In this sizing guide, fit means the appropriate size for each wearer; גזרה instead denotes garment cut/style.'),
    717: ('Guida di stile per mamma e bambino per il ritorno a scuola', 'Mommy and Me does not restrict the child to a daughter; use the generic child term instead of figlia.'),
    1243: ('Осенний семейный стиль в едином стиле: клетка, фланель и другие идеи', 'Matching concerns the coordinated style, not exclusively a shared color palette (в единой гамме).'),
}
# Avoid the repeated "style" phrase while preserving the full source title meaning.
corrections[1243] = ('Осенние семейные образы в едином стиле: клетка, фланель и другие идеи', corrections[1243][1])

qualified, proposals, checks = [], [], []
seen = set()
for batch_name in ['candidate_batch_01.json', 'candidate_batch_02.json']:
    batch_file = AUTHOR / batch_name
    batch = load(batch_file)
    assert batch['inventoryFileSHA256'] == file_sha(AUTHOR / 'inventory.json')
    output_batch = []
    for row in batch['rows']:
        key = tuple_key(row)
        assert key not in seen
        seen.add(key)
        inv = by_key[key]
        assert row['auditId'] == inv['auditId']
        assert row['sourceValue'] == row['source'] == inv['source']
        assert row['sourceDigest'] == inv['sourceDigest']
        assert row['sourceSHA256'] == sha(row['sourceValue'])
        assert row['rawBefore'] == inv['before']
        assert row['before']['value'] == inv['effectiveValue']
        assert row['before']['key'] == row['key'] and row['before']['locale'] == row['locale']
        assert row['before'].get('market') is None and row.get('marketId') is None
        assert row['expectedBeforeValueSHA256'] == sha(row['before']['value'])
        assert row['valueSHA256'] == sha(row['value'])
        assert row['rawFile'] == inv['rawFile']
        assert row['rawFileSHA256'] == inv['rawFileSHA256'] == file_sha(ROOT / row['rawFile'])
        reviewed = copy.deepcopy(row)
        if row['auditId'] in corrections:
            value, reason = corrections[row['auditId']]
            reviewed['beforeCandidateValue'] = row['value']
            reviewed['value'] = value
            reviewed['valueSHA256'] = sha(value)
            reviewed['independentCorrectionReason'] = reason
            proposals.append(copy.deepcopy(reviewed))
        reviewed['independentReviewStatus'] = 'PASS_COMPLETE_TITLE_MEANING_AND_EXACT_FROZEN_BINDINGS'
        reviewed['independentReviewer'] = 'article_de_complete'
        reviewed['reviewStatus'] = 'INDEPENDENTLY_REVIEWED_SOURCE_BOUND'
        reviewed['requiresFreshLiveSourceAndBeforeGuard'] = True
        reviewed['independentInputFile'] = str(batch_file.relative_to(ROOT))
        reviewed['independentInputFileSHA256'] = file_sha(batch_file)
        qualified.append(reviewed)
        output_batch.append(reviewed)
        checks.append({
            'auditId': row['auditId'], 'resourceId': key[0], 'locale': key[1], 'key': key[2],
            'tupleSourceDigestBeforeAndRawFileSHA256': 'PASS',
            'fullTitleMeaningLocalizationAndOmissions': 'PASS_AFTER_PROPOSED_CORRECTION' if row['auditId'] in corrections else 'PASS',
            'targetValueSHA256': reviewed['valueSHA256'],
            'sourceMonthMeaningNote': 'January correctly localized as 1월; digit is a month rendering, not an added factual quantity.' if row['auditId'] == 813 else None,
        })
    dump(batch_name.replace('candidate_', 'reviewed_'), {'rows': output_batch})

assert len(qualified) == 175 and len(proposals) == 4
dump('qualified175_titles.json', {'status': 'INDEPENDENTLY_REVIEWED_PENDING_ROOT_SELECTION_AND_LIVE_GUARDS', 'rows': qualified})
dump('title_correction_proposals4.json', {'rows': proposals})
dump('title_checks.json', {
    'status': 'PASS', 'inventoryTuples': 1340, 'publishedArticles': 67, 'publishedLocales': 20,
    'reviewScope': 'All 175 proposed complete titles independently read against the English source. The producer owns complete reading of the other 1165 effective titles.',
    'candidateFieldsReviewed': 175, 'qualifiedWithoutCorrection': 171, 'qualifiedWithProposedCorrection': 4,
    'byLocale': dict(sorted(collections.Counter(row['locale'] for row in qualified).items())),
    'sourceBodyClaimFlags': 'No title was held merely because its article body has a source-claim flag.',
    'limitations': 'Offline snapshot review only. Root must freshly verify source/digest/publication/current before value before any release, then read back exact target.',
    'inventorySHA256': file_sha(AUTHOR / 'inventory.json'), 'checks': checks,
})
print(json.dumps({'reviewed': len(qualified), 'corrections': len(proposals), 'checks': 'PASS'}))
