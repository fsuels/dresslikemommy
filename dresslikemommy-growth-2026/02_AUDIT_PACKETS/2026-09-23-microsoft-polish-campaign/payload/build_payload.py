#!/usr/bin/env python3
"""Extract the user's Polish attachment; local-only, no network or account writes."""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/fsuels/.codex/attachments/85bc3fa4-696d-4532-a172-4a26031897df/Pasted text.txt')
text = SOURCE.read_text(encoding='utf-8')


def between(start, end, source=text):
    return source.split(start, 1)[1].split(end, 1)[0].strip()


def lines(value):
    return [line.strip() for line in value.splitlines() if line.strip()]


def keywords(value):
    return [{'text': line[1:-1], 'match_type': 'Exact' if line[0] == '[' else 'Phrase'}
            for line in lines(value) if re.fullmatch(r'\[.+\]|"[^"]+"', line)]


def keyword_block(items):
    return '\n'.join('[' + row['text'] + ']' if row['match_type'] == 'Exact'
                     else '"' + row['text'] + '"' for row in items)


def write_json(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_text(name, value):
    (ROOT / name).write_text(value.rstrip() + ('\n' if value.strip() else ''), encoding='utf-8')


groups = []
sections = list(re.finditer(r'^\d+\. Grupa (\d+) — (.+)$', text, re.M))
for i, match in enumerate(sections):
    end = sections[i+1].start() if i+1 < len(sections) else text.index('11. Wykluczenia kampanii')
    section = text[match.end():end]
    head = re.search(r'^Nagłówki[^\n]*\n', section, re.M)
    desc = re.search(r'^Opisy[^\n]*\n', section, re.M)
    neg = re.search(r'^Wykluczenia[^\n]*\n', section, re.M)
    positive_start = section.index('Pozytywne słowa kluczowe\n') + len('Pozytywne słowa kluczowe\n')
    suffix_source = text.split('12. Opcje URL i śledzenie dla każdej grupy', 1)[1].split(f'{i+1}. {match[2]}\n', 1)[1]
    suffix = re.search(r'^utm_source=bing[^\n]+', suffix_source, re.M)[0]
    negatives = keywords(section[neg.end():])
    condition = None
    if i == 1:
        condition = 'Apply these Exact routing exclusions when the shirts and sweaters groups are active and eligible.'
    elif i == 5:
        condition = 'Apply each Exact routing exclusion only when its corresponding specific group is active and appropriate.'
    groups.append({
        'index': int(match[1]),
        'name': match[2],
        'source_english_name': re.search(r'Odpowiednik (.+)\.', section)[1],
        'source_line': text.count('\n', 0, match.start()) + 1,
        'final_url': re.search(r'https://www\.dresslikemommy\.com/[^\s]+', section)[0],
        'path_1': re.search(r'Path 1: (.+)', section)[1],
        'path_2': re.search(r'Path 2: (.+)', section)[1],
        'positive_keywords': keywords(section[positive_start:head.start()]),
        'headlines': lines(section[head.end():desc.start()]),
        'descriptions': lines(section[desc.end():neg.start()]),
        'negative_keywords': negatives,
        'negative_application_condition': condition,
        'source_final_url_suffix': suffix,
        'proposed_final_url_suffix': suffix.replace('dlm_ms_us_pl_search_202609', 'dlm_ms_pl_pl_search_202609'),
        'tracking_action': 'CONDITIONAL_ON_NATIVE_TRACKING_READBACK',
        'tracking_note': 'Do not apply the proposed suffix until manual tagging and inherited/ad/sitelink tracking are reconciled. Do not clear templates or custom parameters merely because this attachment proposes empty values.',
        'ad_format': 'Responsive Search Ad',
        'ad_group_type': 'Standard',
        'language': 'Polish',
        'proposed_pins': [],
        'image_text_pairs': None,
        'source_notes': [line for line in lines(section[neg.end():]) if not re.fullmatch(r'\[.+\]|"[^"]+"', line)],
        'requires_current_landing_verification': True,
    })

campaign_pl = keywords(between('A. Polskie wykluczenia kampanii — Phrase', 'B. Uzupełniające wykluczenia angielskie — Phrase'))
campaign_en = keywords(between('B. Uzupełniające wykluczenia angielskie — Phrase', 'C. Tymczasowe ograniczenia asortymentu — Exact'))
campaign_exact = keywords(between('C. Tymczasowe ograniczenia asortymentu — Exact', 'D. Czego nie wykluczać automatycznie'))
callouts = lines(between('Jeden wiersz do każdego pola:', 'Wszystkie sześć tekstów'))

# Every sitelink title occurs first as a heading and again as its actual field.
# Verify those repeated headings instead of mistaking them for descriptions.
sitelink_lines = lines(between('Użyj polskiego Final URL odpowiadającej grupy.', 'Tytuły i opisy linków'))
assert len(sitelink_lines) == 32, 'Unexpected sitelink section shape'
sitelinks = []
for i in range(8):
    heading, title, d1, d2 = sitelink_lines[i*4:i*4+4]
    assert heading == title, 'Sitelink heading/title mismatch'
    sitelinks.append({'text': title, 'description_1': d1, 'description_2': d2,
                     'final_url': groups[i]['final_url'], 'source_group_index': i+1})
association_rows = lines(between('Grupa\tProponowane linki do podstron', 'Nie uruchamiaj linków'))
snippet_rows = lines(between('Grupa\tNagłówek\tWartości', '14. Rozszerzenia obrazów'))
for group in groups:
    association = next(row.split('\t', 1)[1] for row in association_rows if row.split('\t', 1)[0] == group['name'])
    group['sitelinks'] = association.split('; ')
    snippet = next(row.split('\t') for row in snippet_rows if row.split('\t', 1)[0] == group['name'])
    group['structured_snippet'] = {'header': snippet[1], 'values': snippet[2].split(' · '),
                                   'native_header_label_verification': 'REQUIRED'}

payload = {
    'schema_version': 1,
    'artifact_type': 'LOCAL_PREPARATION_NOT_LIVE_STATE',
    'source_file': str(SOURCE),
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_note': 'Verbatim extraction of supplied Polish copy, keywords and extensions. No browser or external actions in this delegated lane.',
    'explicit_override': 'Parent assignment confirms current user target PL | PL supersedes attachment US | PL: Poland, Polish. Proposed manual campaign UTM changes us_pl to pl_pl only; application remains conditional.',
    'campaign': {
        'name': 'DLM | MS | PL | PL | Search | 202609',
        'native_id': None,
        'location': 'Poland',
        'language': 'Polish',
        'location_intent': 'People in your targeted locations',
        'type': 'Search',
        'attachment_goal': 'Drive conversions',
        'attachment_setup_status': 'Paused',
        'actual_status': None,
        'budget': None,
        'bidding_strategy': None,
        'settings_note': 'Native target identity, current status, budget and bidding require parent readback. This artifact neither authorizes activation nor establishes numeric budget authority.',
        'negative_keywords': campaign_pl + campaign_en + campaign_exact,
        'negative_keyword_subsets': {'polish_phrase': campaign_pl, 'supplemental_english_phrase': campaign_en,
                                     'provisional_catalog_exact': campaign_exact},
        'callouts': callouts,
        'sitelinks': sitelinks,
    },
    'ad_groups': groups,
    'image_assets': {
        'policy': 'Retain corresponding source images after parent native asset mapping. Do not invent image content or caption/alt pairs.',
        'supplied_image_text_pairs': 0,
        'claimed_image_text_pairs': 160,
        'pairs': None,
    },
    'limitations': [
        'The pasted text mentions ZIP/Excel and 160 image caption/alt pairs but contains no actual files, download URLs or image pairs. Their claimed checks cannot be reproduced.',
        'Native source-campaign match-type sequence, names, images and existing extensions have not been read in this lane.',
        'All 64 group negatives are retained, including 31 conditionally routed Exact rows in groups 2 and 6. Conditions do not justify omitting them from expected-state reconciliation.',
        'The 18 Exact catalog exclusions are provisional in the source and are not a fresh availability audit.',
        'All 84 English supplementary Phrase negatives are intentionally retained as supplied; they are exclusions, not positive keywords or language settings.',
        'Four collection URLs were unverified in the attachment: new-women-outfits, family-tops, swimsuits, family-sweaters. All eight require current verification.',
        'Literal matching does not emulate Microsoft semantic matching, close variants, account/shared inherited exclusions, editorial approval or native conflict reporting.',
        'No fresh product availability, checkout, pricing, delivery, returns, keyword demand, CPC, conversion or profit evidence is established.',
        'Proposed manual suffixes require native tracking readback to avoid replacing or duplicating inherited tagging; no UET/conversion changes are proposed.',
    ],
}

errors, duplicates, conflicts, length_rows = [], [], [], []
counts = {
    'groups': len(groups), 'positive_keywords': sum(len(g['positive_keywords']) for g in groups),
    'headlines': sum(len(g['headlines']) for g in groups), 'descriptions': sum(len(g['descriptions']) for g in groups),
    'campaign_polish_phrase_negatives': len(campaign_pl), 'campaign_english_phrase_negatives': len(campaign_en),
    'campaign_phrase_negatives': len(campaign_pl) + len(campaign_en), 'campaign_exact_negatives': len(campaign_exact),
    'campaign_total_negatives': len(payload['campaign']['negative_keywords']),
    'group_negatives': sum(len(g['negative_keywords']) for g in groups),
    'conditional_group_negatives': sum(len(g['negative_keywords']) for g in groups if g['negative_application_condition']),
    'sitelinks': len(sitelinks), 'sitelink_associations': sum(len(g['sitelinks']) for g in groups),
    'callouts': len(callouts), 'structured_snippets': len(groups), 'supplied_image_text_pairs': 0,
}
expected = dict(groups=8, positive_keywords=144, headlines=120, descriptions=32,
                campaign_polish_phrase_negatives=145, campaign_english_phrase_negatives=84,
                campaign_phrase_negatives=229, campaign_exact_negatives=18, campaign_total_negatives=247,
                group_negatives=64, conditional_group_negatives=31, sitelinks=8,
                sitelink_associations=32, callouts=6, structured_snippets=8)
for field, value in expected.items():
    if counts[field] != value:
        errors.append({'type': 'count', 'field': field, 'expected': value, 'actual': counts[field]})


def length_check(scope, field, value, limit):
    row = {'scope': scope, 'field': field, 'text': value, 'length': len(value), 'limit': limit, 'pass': len(value) <= limit}
    length_rows.append(row)
    if not row['pass']:
        errors.append(row)


def normalize(value):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFC', value).casefold()))


def duplicate_check(scope, items):
    seen = Counter((unicodedata.normalize('NFC', k['text']).strip().casefold(), k['match_type']) for k in items)
    for key, count in seen.items():
        if count > 1:
            duplicates.append({'scope': scope, 'keyword': key, 'count': count})


def excludes(negative, positive):
    n, p = normalize(negative['text']), normalize(positive['text'])
    return n == p if negative['match_type'] == 'Exact' else f' {n} ' in f' {p} '


positive_owners = defaultdict(list)
sitelink_titles = {s['text'] for s in sitelinks}
for group in groups:
    number = group['index']
    for field, limit in [('headlines', 30), ('descriptions', 90)]:
        for value in group[field]:
            length_check(group['name'], field, value, limit)
    for field in ['path_1', 'path_2']:
        length_check(group['name'], field, group[field], 15)
    for value in group['structured_snippet']['values']:
        length_check(group['name'], 'snippet_value', value, 25)
    if len(group['headlines']) != 15 or len(group['descriptions']) != 4:
        errors.append({'type': 'group_ad_field_count', 'group': number})
    if len(group['sitelinks']) != 4 or len(set(group['sitelinks'])) != 4 or not set(group['sitelinks']) <= sitelink_titles:
        errors.append({'type': 'sitelink_associations', 'group': number})
    duplicate_check(f'group_{number}_positives', group['positive_keywords'])
    duplicate_check(f'group_{number}_negatives', group['negative_keywords'])
    for positive in group['positive_keywords']:
        positive_owners[(normalize(positive['text']), positive['match_type'])].append(number)
        for scope, negatives in [('campaign', payload['campaign']['negative_keywords']), ('group', group['negative_keywords'])]:
            for negative in negatives:
                if excludes(negative, positive):
                    conflicts.append({'group': number, 'scope': scope, 'positive': positive, 'negative': negative})
    write_json(f'group_{number:02d}.json', group)
    write_text(f'group_{number:02d}_positive_keywords.txt', keyword_block(group['positive_keywords']))
    write_text(f'group_{number:02d}_negative_keywords.txt', keyword_block(group['negative_keywords']))
    write_text(f'group_{number:02d}_rsa.txt', '\n'.join([
        group['name'], group['final_url'], f"Path 1: {group['path_1']}", f"Path 2: {group['path_2']}",
        '', 'HEADLINES', *group['headlines'], '', 'DESCRIPTIONS', *group['descriptions'],
        '', 'PROPOSED FINAL URL SUFFIX - APPLY ONLY AFTER NATIVE TRACKING READBACK', group['proposed_final_url_suffix']]))
duplicate_check('campaign_negatives', payload['campaign']['negative_keywords'])
for sitelink in sitelinks:
    for field, limit in [('text', 25), ('description_1', 35), ('description_2', 35)]:
        length_check(sitelink['text'], f'sitelink_{field}', sitelink[field], limit)
for callout in callouts:
    length_check('campaign', 'callout', callout, 25)

cross_group = [{'keyword': key, 'groups': owners} for key, owners in positive_owners.items() if len(set(owners)) > 1]
validation = {
    'result': 'PASS_LOCAL_WITH_DOCUMENTED_LIMITATIONS' if not errors and not duplicates and not conflicts else 'FAIL',
    'source_sha256': payload['source_sha256'], 'counts': counts, 'errors': errors,
    'within_scope_duplicate_keyword_entries': duplicates,
    'cross_group_duplicate_positive_entries': cross_group,
    'literal_positive_negative_conflicts': conflicts,
    'discrepancies': [
        {'field': 'image_text_pairs', 'attachment_claimed': 160, 'actually_supplied': 0, 'action': 'Parent must read existing native image text or obtain actual attachment; do not fabricate.'},
        {'field': 'target_market', 'attachment': 'US', 'current_request': 'PL', 'action': 'Current explicit Poland/Polish scope wins.'},
        {'field': 'campaign_name_settings_row', 'attachment': '`DLM', 'action': 'Malformed pasted table row; use exact current user campaign name.'},
    ],
    'validation_scope': 'Counts; Unicode character lengths against attachment-stated limits; within-scope casefold duplicate tuples; token-normalized literal Phrase/Exact exclusion checks. No live or semantic matching validation.',
    'length_checks': length_rows,
    'per_group_counts': [{'index': g['index'], 'name': g['name'], 'positive': len(g['positive_keywords']),
                          'positive_exact': sum(k['match_type'] == 'Exact' for k in g['positive_keywords']),
                          'positive_phrase': sum(k['match_type'] == 'Phrase' for k in g['positive_keywords']),
                          'negative': len(g['negative_keywords']), 'negative_match_types': dict(Counter(k['match_type'] for k in g['negative_keywords'])),
                          'conditional': g['negative_application_condition'] is not None,
                          'headlines': len(g['headlines']), 'descriptions': len(g['descriptions'])} for g in groups],
}
write_json('campaign_payload.json', payload)
write_json('validation.json', validation)
write_json('sitelinks.json', sitelinks)
write_json('structured_snippets.json', [{'group_index': g['index'], 'group_name': g['name'], **g['structured_snippet']} for g in groups])
write_text('campaign_negative_keywords.txt', keyword_block(payload['campaign']['negative_keywords']))
write_text('campaign_negative_keywords_phrase.txt', keyword_block(campaign_pl + campaign_en))
write_text('campaign_negative_keywords_polish_phrase.txt', keyword_block(campaign_pl))
write_text('campaign_negative_keywords_english_phrase.txt', keyword_block(campaign_en))
write_text('campaign_negative_keywords_exact_provisional.txt', keyword_block(campaign_exact))
write_text('callouts.txt', '\n'.join(callouts))
print(json.dumps({'result': validation['result'], 'counts': counts, 'errors': errors,
                  'duplicates': duplicates, 'conflicts': conflicts, 'path': str(ROOT)}, ensure_ascii=False, indent=2))
assert not errors and not duplicates and not conflicts, 'Local payload validation failed'
