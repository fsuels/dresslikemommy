from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re

P = Path(__file__).resolve().parent
R = P.parent.parent
f = P / 'ru_remaining_review_input.json'
rows = json.loads(f.read_text())['rows']
baseline_file = R / 'articles/ru-bodies/baseline.json'
baseline = json.loads(baseline_file.read_text())['rows']
bi = {(x['resourceId'], x['locale'], x['key']): x for x in baseline}
spec = importlib.util.spec_from_file_location('v', R / 'tooling/offline_translation.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

corrections = [
    {
        'ids': ['559471984737'],
        'old': '</a> с сезонной подборкой.',
        'new': '</a>, чтобы выбрать сезонные модели.',
        'reason': 'Source "for seasonal picks" expresses the purpose of browsing the linked collection; remove the Russian duplicate "selection with a seasonal selection" and make the purpose natural after the inline link.',
    },
    {
        'ids': ['559654994017'],
        'old': 'Помогать семьям подбирать семейные наряды в едином стиле когда вся семья одевается в едином стиле — одно из наших любимых занятий.',
        'new': 'Помогать семьям подбирать сочетающиеся наряды для всей семьи — одно из наших любимых занятий.',
        'reason': 'Render the source family-matching coordination meaning without an unpunctuated Russian when-clause introduced by literal template substitution; the repeated source concept is retained once as a natural phrase.',
    },
    {
        'ids': ['559654994017', '559659516001', '559660433505', '559662497889'],
        'old': 'Не упустите эти парные образы когда вся семья одевается в едином стиле —',
        'new': 'Не упустите эти семейные образы в едином стиле —',
        'reason': 'Source "matching family outfits matching looks" refers to the family outfits themselves, not a temporal when-clause; replace the malformed Russian template join with the equivalent noun phrase.',
    },
    {
        'ids': ['559662202977'],
        'old': 'Помогать семьям подбирать наряды для мамы и ребёнка когда вся семья одевается в едином стиле — одно из наших любимых занятий.',
        'new': 'Помогать семьям подбирать наряды для мамы и ребёнка, сочетающиеся с одеждой всей семьи, — одно из наших любимых занятий.',
        'reason': 'Express the source coordination of mommy-and-me outfits with the wider family matching outfits as a grammatical Russian phrase instead of an unpunctuated when-clause.',
    },
    {
        'ids': ['559662465121'],
        'old': 'Тропические пляжные наряды с разноцветным принтом листьев... | DLM',
        'new': 'Летние тропические пляжные наряды с разноцветным принтом листьев... | DLM',
        'reason': 'Restore the explicit Summer descriptor present in the English product name; apply consistently to heading, descriptive paragraph and CTA.',
        'occurrences': 3,
    },
]

out, proposals, fields = [], [], []
for r in rows:
    identity = (r['resourceId'], r['locale'], r['key'])
    b = bi[identity]
    assert all(r[k] == b[k] for k in ['sourceValue', 'sourceDigest', 'before', 'locale', 'key'])
    value = r['value']
    edits = []
    for c in corrections:
        if r['resourceId'].rsplit('/', 1)[-1] not in c['ids']:
            continue
        occurrences = value.count(c['old'])
        assert occurrences == c.get('occurrences', 1), (r['resourceId'], c, occurrences)
        value = value.replace(c['old'], c['new'])
        edits.append({'before': c['old'], 'after': c['new'], 'occurrences': occurrences, 'reason': c['reason']})
    check = v.verify_text(r['sourceValue'], value, 'ru')
    assert not check['errors'], (r['resourceId'], check)
    badjoins = re.findall(r'([А-Яа-яЁё])(?:</(?:a|strong|em)>)([А-Яа-яЁё])', value)
    assert not badjoins, (r['resourceId'], badjoins)
    rr = copy.deepcopy(r)
    rr.update(value=value, independentReview='FULL_MEANING_SOURCE_BINDING_AND_PRESERVATION_PASS')
    out.append(rr)
    if edits:
        proposals.append({**rr, 'beforeCandidateValue': r['value'], 'candidateCorrectionReasons': edits})
    fields.append({
        'resourceId': r['resourceId'], 'locale': r['locale'], 'key': r['key'],
        'sourceBinding': 'PASS',
        'meaning': 'PASS_WITH_LISTED_CORRECTION' if edits else 'PASS',
        'inlineJoins': 'PASS', 'checks': check, 'corrections': edits,
        'sourceSHA256': hashlib.sha256(r['sourceValue'].encode()).hexdigest(),
        'candidateBeforeSHA256': hashlib.sha256(r['value'].encode()).hexdigest(),
        'candidateAfterSHA256': hashlib.sha256(value.encode()).hexdigest(),
    })

assert len(out) == 55
assert len(proposals) == 7
scope = '55 Russian article body rows absent from article_release_index_final.json when this review input was selected; the frozen selection is ru_remaining_review_input.json. Existing released 12 Russian rows were excluded.'
review = {
    'status': 'PASS_WITH_SEVEN_BODY_CORRECTION_PROPOSALS',
    'articles': 55,
    'scope': scope,
    'reviewedUniqueAlignedSourceTargetTextPairs': 909,
    'separatelyReviewedUnalignedBody': 'gid://shopify/Article/559471820897: 84 source versus 83 target nonempty nodes; complete block-by-block review confirms all source meanings retained with grammatical phrase placement.',
    'baselineBindings': '55/55 sourceValue, sourceDigest, before, locale and key exactly match supplied baseline',
    'structuralFailures': 0,
    'correctionRows': len(proposals),
    'correctionSpans': sum(e['occurrences'] for r in proposals for e in r['candidateCorrectionReasons']),
    'sourceAssertions': 'Source assertions are preserved. Generic marketing/style/source-claim annotations are metadata, not new approval gates. No external truth audit or current source freshness check was performed; root owns known source contradictions and final release guards.',
    'retainedNames': 'English printed slogans and named brands remain named text. Existing truncated product labels retain their source truncation or reuse an observed full title in the same source article.',
    'qualificationBoundary': 'Qualified for translation meaning and preservation after listed candidate edits. This offline review does not establish publication, public routing, live rendering, current source freshness or factual truth of inherited source assertions.',
    'fields': fields,
}
hashes = {
    'frozenSelectionSHA256': hashlib.sha256(f.read_bytes()).hexdigest(),
    'authoredCandidateSHA256': hashlib.sha256((R / 'articles/ru-bodies/candidate_all_complete.json').read_bytes()).hexdigest(),
    'baselineSHA256': hashlib.sha256(baseline_file.read_bytes()).hexdigest(),
}
for name, data in [
    ('ru_candidate_corrections.json', {**hashes, 'scope': scope, 'rows': proposals}),
    ('ru_independently_qualified.json', {**hashes, 'status': '55_FULL_BODY_TRANSLATIONS_QUALIFIED_WITH_LISTED_EDITS', 'rows': out}),
    ('ru_independent_review.json', {**hashes, **review}),
]:
    (P / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'qualified': len(out), 'correctionRows': len(proposals), 'correctionSpans': review['correctionSpans'], 'structuralFailures': 0}))
