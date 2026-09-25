#!/usr/bin/env python3
"""Read captured UTF-16 Microsoft exports; write local missing-row artifacts only."""
import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKET = ROOT.parent
ui = json.loads((ROOT / 'ui_ready.json').read_text())
campaign_name = ui['campaign']['name_resolved']


def read_native(scope):
    path = PACKET / 'native' / f'{scope}_negatives_before.csv'
    raw = path.read_bytes()
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-16')), delimiter='\t'))
    expected_fields = ['Negative', 'Match type', 'Campaign'] + (['Ad group'] if scope == 'group' else [])
    assert rows and list(rows[0]) == expected_fields
    assert all(r['Campaign'] == campaign_name and r['Match type'] in ['Phrase', 'Exact'] and r['Negative'] for r in rows)
    return rows, {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'encoding': 'UTF-16', 'delimiter': 'TAB', 'header': expected_fields, 'data_rows': len(rows), 'all_rows_exact_target_name': True}


def parse_expected(text):
    rows = []
    for line in text.splitlines():
        assert re.fullmatch(r'\[.+\]|".+"', line), line
        rows.append((line[1:-1], 'Exact' if line[0] == '[' else 'Phrase'))
    return rows


def tuple_dict(pair):
    return {'text': pair[0], 'match': pair[1]}


def ui_text(rows):
    return ''.join(f'[{r[0]}]\n' if r[1] == 'Exact' else f'"{r[0]}"\n' for r in rows)


missing_dir = ROOT / 'missing_negatives'
missing_dir.mkdir(exist_ok=True)


def compare(scope, name, native_rows, expected_text, index=None):
    before = [(r['Negative'], r['Match type']) for r in native_rows]
    expected = parse_expected(expected_text)
    current_set, expected_set = set(before), set(expected)
    shared = [row for row in expected if row in current_set]
    missing = [row for row in expected if row not in current_set]
    obsolete = [row for row in before if row not in expected_set]
    duplicates = [{'text': k[0], 'match': k[1], 'occurrences': v} for k, v in Counter(before).items() if v > 1]
    assert not duplicates, duplicates
    basename = 'campaign' if scope == 'campaign' else f'{index:02d}_group'
    missing_path = missing_dir / f'{basename}_missing.txt'
    missing_path.write_text(ui_text(missing))
    result = {
        'scope': scope, 'campaign': campaign_name, 'group': name if scope == 'group' else None,
        'group_index': index, 'current': len(before), 'expected': len(expected),
        'shared_count': len(shared), 'missing_count': len(missing), 'obsolete_count': len(obsolete),
        'shared': [tuple_dict(r) for r in shared], 'missing': [tuple_dict(r) for r in missing],
        'obsolete': [tuple_dict(r) for r in obsolete], 'duplicates': duplicates,
        'current_matches': dict(Counter(r[1] for r in before)),
        'expected_matches': dict(Counter(r[1] for r in expected)),
        'missing_matches': dict(Counter(r[1] for r in missing)),
        'missing_text_file': str(missing_path),
    }
    assert result['current'] == result['shared_count'] + result['obsolete_count']
    assert result['expected'] == result['shared_count'] + result['missing_count']
    return result


campaign_rows, campaign_source = read_native('campaign')
group_rows, group_source = read_native('group')
campaign = compare('campaign', None, campaign_rows, ui['campaign_negatives_text'])
groups = [compare('group', g['name'], [r for r in group_rows if r['Ad group'] == g['name']], g['negatives_text'], g['index']) for g in ui['groups']]
assert len(group_rows) == sum(g['current'] for g in groups)
assert {r['Ad group'] for r in group_rows} == {g['name'] for g in ui['groups']}

# These candidates preserve the specific family/garment intent and Exact match.
# Arbitrary obsolete-to-missing swaps are deliberately not proposed.
translation_pairs = {
    2: [
        ('family matching shirts', 'camicie coordinate famiglia'),
        ('matching shirts for family', 'camicie uguali per tutta la famiglia'),
        ('family matching tops', 'maglie coordinate famiglia'),
        ('matching family t shirts', 'magliette coordinate famiglia'),
        ('family matching sweaters', 'maglioni coordinati famiglia'),
        ('matching sweaters for family', 'maglioni uguali per tutta la famiglia'),
        ('matching family hoodies', 'felpe con cappuccio coordinate famiglia'),
        ('matching family sweatshirts', 'felpe coordinate famiglia'),
    ],
    3: [
        ('father son matching hawaiian shirts', 'camicie hawaiane coordinate papà e figlio'),
        ('daddy and me button up shirts', 'camicie con bottoni papà e figlio'),
        ('father son matching button down shirts', 'camicie abbottonate padre e figlio'),
        ('family matching sweaters', 'maglioni coordinati famiglia'),
        ('matching family hoodies', 'felpe con cappuccio coordinate famiglia'),
        ('matching family sweatshirts', 'felpe coordinate famiglia'),
    ],
}
edit_candidates = []
for index, pairs in translation_pairs.items():
    group = next(g for g in groups if g['group_index'] == index)
    for old, new in pairs:
        assert {'text': old, 'match': 'Exact'} in group['obsolete']
        assert {'text': new, 'match': 'Exact'} in group['missing']
        edit_candidates.append({'scope': 'group', 'group_index': index, 'group': group['group'], 'from': {'text': old, 'match': 'Exact'}, 'to': {'text': new, 'match': 'Exact'}, 'assessment': 'Narrow same-intent translation candidate; not a claim of equivalent Microsoft semantic matching.', 'native_edit_capability': 'NOT_VERIFIED_LOCAL_ONLY', 'execution_gate': 'Root must verify exact row and editable text control. After edit, export must prove one old tuple absent and one target tuple present without duplicates. Preserve Exact match and routing destination eligibility gate.'})


def normalize(text):
    return ' '.join(re.findall(r'\w+', text.casefold()))


literal_conflicts = []
for g in ui['groups']:
    own = next(x for x in groups if x['group_index'] == g['index'])
    for positive, _ in parse_expected(g['keywords_text']):
        for scope, negatives in [('campaign', campaign['obsolete']), ('group', own['obsolete'])]:
            for neg in negatives:
                p, n = normalize(positive), normalize(neg['text'])
                if (p == n if neg['match'] == 'Exact' else f' {n} ' in f' {p} '):
                    literal_conflicts.append({'group': g['name'], 'positive': positive, 'negative': neg, 'scope': scope})

summary = {key: sum(g[key] for g in groups) for key in ['current', 'expected', 'shared_count', 'missing_count', 'obsolete_count']}
source_before = json.loads((PACKET / 'source_before.json').read_text())
assert len(source_before['source_groups']) == 7
family_before = next(g for g in groups if g['group_index'] == 2)
mom_before = next(g for g in groups if g['group_index'] == 6)
family_set = {(r['Negative'], r['Match type']) for r in group_rows if r['Ad group'] == family_before['group']}
mom_set = {(r['Negative'], r['Match type']) for r in group_rows if r['Ad group'] == mom_before['group']}
report = {
    'status': 'PASS_EXACT_COMPARISON_OF_CAPTURED_ROWS__EXPORT_COMPLETENESS_UNCONFIRMED',
    'campaign_id': '506256101', 'campaign_name': campaign_name,
    'native_sources': {'campaign': campaign_source, 'group': group_source},
    'expected_source': {'path': str(ROOT / 'ui_ready.json'), 'sha256': hashlib.sha256((ROOT / 'ui_ready.json').read_bytes()).hexdigest()},
    'comparison_key': ['scope', 'campaign', 'group_if_applicable', 'text_exact_case_and_accents', 'match'],
    'campaign': campaign, 'groups': groups, 'group_totals': summary,
    'captured_rows_duplicates': 0, 'captured_rows_unknown_groups': 0,
    'captured_rows_literal_positive_conflicts': literal_conflicts,
    'completeness_assessment': {
        'campaign': '106 captured data rows. No native total/footer or pagination evidence accompanies the file, so total completeness is not independently certified.',
        'group': 'Exactly 200 captured data rows across all 8 expected groups. A round 200 is not proof of truncation or completeness; fresh settled native total or all-row export readback is required.',
        'source_group_count': len(source_before['source_groups']),
        'source_negative_export_or_total_provided': False,
        'new_group_6_rows': mom_before['current'],
        'new_group_6_same_negative_tuples_as_family_outfits': family_set == mom_set,
        'seven_source_named_groups_captured_rows': len(group_rows) - mom_before['current'],
        'arithmetic_inference': '200 = 161 captured rows in the seven source-named groups + 39 rows in new Mommy & Me Outfits. The new group exactly repeats Family Matching Outfits 39 tuples. This is consistent with copying that group, but source expected total 161 is not independently established.',
    },
    'edit_feasibility': {
        'native_editability': 'NOT_RUN_NO_BROWSER_AUTHORITY_IN_THIS_LANE',
        'campaign_candidates': [],
        'campaign_reason': 'No obsolete campaign tuple has a defensible one-for-one same-intent counterpart among the missing Italian rows. Broad wholesale/free-download/brand/delivery negatives must not be arbitrarily repurposed.',
        'group_candidates': edit_candidates,
        'candidate_count': len(edit_candidates),
        'group_count_if_14_verified_text_edits_only': 200,
        'group_missing_after_14_verified_edits': 25,
        'group_obsolete_after_14_verified_edits': 176,
        'group_count_after_then_adding_remaining25': 225,
        'campaign_count_if_add_missing114_only': 220,
        'warning': 'Editing keyword text changes exclusion behavior; this is not cosmetic renaming and cannot establish semantic equivalence or eliminate unmatched extras. Missing-only files describe the original before-export; recompute or subtract completed edits before insertion.',
        'no_candidate_for_other_groups': 'Do not force unrelated generic English category rows into Italian target rows simply to preserve record count. Group 8 needs six additions because its two current tuples are both required. Groups 4 and 7 require zero target rows, so their extras have no target replacement.',
    },
    'harmful_extra_flags': [
        {'scope': 'campaign', 'terms': ['dresslikemommy', 'dresslikemommy.com'], 'match': 'Exact', 'risk': 'Directly excludes exact brand searches contrary to the supplied no-automatic-brand-exclusion plan.'},
        {'scope': 'campaign', 'terms': ['wholesale', 'bulk', 'personalized', 'custom made', 'free download', 'free downloads', 'same day delivery', 'next day delivery', 'overnight shipping'], 'match': 'Phrase', 'risk': 'Unplanned broad exclusions; supplied plan requires contextual assessment instead of automatic blocking for these intents.'},
        {'scope': 'group', 'group_indices': [2, 6], 'terms': ['shirt', 'shirts', 'tee', 'tees', 't-shirt', 't-shirts', 'pajama', 'pajamas', 'swimsuit', 'swimwear', 'bikini', 'sweater', 'cardigan', 'hoodie'], 'match': 'Phrase', 'risk': 'Broad category exclusions can suppress mixed-category English/Italian searches. The supplied routing plan uses narrow Exact entries; retain no inference that these generic extras are necessary.'},
        {'scope': 'group', 'group_index': 6, 'risk': 'Its entire 39-row inherited Family Outfits negative set is outside the 11-row Mommy & Me Outfits plan; even inherited family-shirt Exact rows route a different family intent.'},
        {'scope': 'group', 'group_indices': [4, 7], 'risk': '17 Pajama and 16 Swimsuit inherited negatives conflict with the intentionally empty group-negative plan; no replacement tuples exist.'},
        {'scope': 'all', 'risk': 'No literal block of the current 144 Italian positive strings was found among captured obsolete rows. That does not validate inherited extras or rule out harmful exclusion of broader or mixed-language search queries.'},
    ],
    'execution': 'LOCAL_ONLY_NO_EXTERNAL_WRITES',
}
(ROOT / 'native_negative_delta.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
lines = ['# Captured native negative delta', '', 'Exact tuple comparison only; native export completeness remains unconfirmed.', '', '| Scope | Current | Expected | Shared | Missing | Obsolete |', '|---|---:|---:|---:|---:|---:|']
for r in [campaign] + groups:
    lines.append(f'| {r["group"] or "Campaign"} | {r["current"]} | {r["expected"]} | {r["shared_count"]} | {r["missing_count"]} | {r["obsolete_count"]} |')
lines.extend(['', 'Group totals: 200 current, 49 expected, 10 shared, 39 missing, 190 obsolete. No duplicate captured tuples. All missing-only text files are based on these before-state exports and must be reconciled again after any edits.', '', '14 narrow Exact translation candidates exist: 8 in Family Outfits and 6 in Family Shirts. Native editability is unverified. Even if all 14 edits succeed, 25 additions and 176 unmatched group extras remain. No safe equivalent campaign replacement is identified.', '', 'Completeness: 200 group rows include all eight groups; 39 Mommy Outfits tuples exactly repeat Family Outfits. Remaining seven source-named groups account for 161 captured rows, but no source-negative total/export establishes that as complete.', '', 'Flags: exact brand negatives; broad wholesale/bulk/personalization/delivery campaign negatives; generic category Phrase negatives in broad outfit groups; all39 mismatched Mommy Outfits entries; intentionally empty Pajama/Swim negative targets. No captured obsolete row literally blocks one of the 144 supplied Italian positive strings.', '', 'No native action, deletion, status, budget, canonical file or peer artifact change was made.'])
(ROOT / 'NATIVE_NEGATIVE_DELTA.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'status': report['status'], 'campaign': {k: campaign[k] for k in ['current', 'expected', 'shared_count', 'missing_count', 'obsolete_count']}, 'groups': summary, 'edit_candidates': len(edit_candidates), 'literal_conflicts': len(literal_conflicts), 'missing_file_count': len(list(missing_dir.glob('*.txt')))}, ensure_ascii=False))
