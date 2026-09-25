#!/usr/bin/env python3
"""Extract supplied Norwegian copy; local files only, no network or account actions."""
from pathlib import Path
import collections
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/fsuels/.codex/attachments/48c79e0e-ee53-4382-a0b4-44728a7ac77c/Pasted text.txt')
text = SOURCE.read_text()


def between(start, end, source=text):
    return source.split(start, 1)[1].split(end, 1)[0].strip()


def lines(source):
    return [line.strip() for line in source.splitlines() if line.strip()]


def keywords(source):
    return [{'text': line[1:-1], 'match_type': 'Exact' if line[0] == '[' else 'Phrase'}
            for line in lines(source) if re.fullmatch(r'\[.+\]|"[^"]+"', line)]


def keyword_block(items):
    return '\n'.join('[' + k['text'] + ']' if k['match_type'] == 'Exact' else '"' + k['text'] + '"' for k in items)


def write_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def normalized(value):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFC', value).casefold()))


groups = []
section_matches = list(re.finditer(r'^\d+\. Gruppe (\d+) — (.+)$', text, flags=re.M))
for i, match in enumerate(section_matches):
    end = section_matches[i + 1].start() if i + 1 < len(section_matches) else text.index('11. Kampanjenegativer')
    section = text[match.end():end]
    head = re.search(r'^Overskrifter[^\n]*\n', section, re.M)
    desc = re.search(r'^Beskrivelser[^\n]*\n', section, re.M)
    neg = re.search(r'^Negative søkeord[^\n]*\n', section, re.M)
    name = match[2]
    suffix_section = text.split('12. URL-innstillinger og sporing per gruppe', 1)[1].split(f'{i+1}. {name}\n', 1)[1]
    suffix = re.search(r'^utm_source=bing[^\n]+', suffix_section, re.M)[0]
    group = {
        'index': int(match[1]), 'name': name,
        'source_english_name': re.search(r'Tilsvarer (.+)\.', section)[1],
        'source_line': text[:match.start()].count('\n') + 1,
        'final_url': re.search(r'https://www\.dresslikemommy\.com/[^\s]+', section)[0],
        'path_1': re.search(r'Path 1: (.+)', section)[1],
        'path_2': re.search(r'Path 2: (.+)', section)[1],
        'positive_keywords': keywords(section[section.index('Positive søkeord\n'):head.start()]),
        'headlines': lines(section[head.end():desc.start()]),
        'descriptions': lines(section[desc.end():neg.start()]),
        'negative_keywords': keywords(section[neg.end():]),
        'source_final_url_suffix': suffix,
        'candidate_final_url_suffix': suffix.replace('dlm_ms_us_nb_search_202609', 'dlm_ms_no_nb_search_202609'),
        'final_url_suffix': None,
        'final_url_suffix_status': 'CANDIDATE_PREPARED_NOT_APPLIED_INHERITANCE_CHECK_REQUIRED',
        'tracking_template': '', 'custom_parameters': {},
        'tracking_application_condition': 'Candidate uses Norway NO | NB. Root must inspect manual/automatic and inherited UTM settings before applying; final_url_suffix remains null until that check. Source attachment UTM retains historical US.',
        'language': 'Norwegian', 'language_code': 'NB',
        'ad_format': 'Responsive Search Ad', 'ad_group_type': 'Standard', 'pins': [],
        'image_text_pairs': None,
        'source_notes': [line for line in lines(section[neg.end():]) if not re.fullmatch(r'\[.+\]|"[^"]+"', line)],
        'requires_live_landing_verification': True,
        'negative_routing_condition': 'Corresponding specialist groups active and suitable before these Exact exclusions serve traffic.' if i + 1 in (2, 6) else None,
        'negative_routing_condition_explicit_in_attachment': i + 1 in (2, 6),
    }
    groups.append(group)

campaign_nb = keywords(between('A. Norske kampanjenegativer — Phrase', 'B. Supplerende engelske kampanjenegativer — Phrase'))
campaign_en = keywords(between('B. Supplerende engelske kampanjenegativer — Phrase', 'C. Midlertidige sortimentsbegrensninger — Exact'))
campaign_exact = keywords(between('C. Midlertidige sortimentsbegrensninger — Exact', 'D. Ord som ikke utelukkes automatisk'))
callouts = lines(between('Én linje per felt:', 'Alle seks er innenfor'))
sitelink_lines = lines(between('Bruk den norske Final URL-en til den tilsvarende gruppen.', 'Titlene og beskrivelseslinjene'))
assert len(sitelink_lines) == 32, len(sitelink_lines)
sitelinks = []
for i in range(8):
    heading, title, d1, d2 = sitelink_lines[i*4:i*4+4]
    assert heading == title
    sitelinks.append({'text': title, 'description_1': d1, 'description_2': d2,
                     'final_url': groups[i]['final_url'], 'source_group_index': i+1})
association_rows = lines(between('Annonsegruppe\tForeslåtte nettstedkoblinger', 'Ikke sett nettstedkoblingen'))
snippet_rows = lines(between('Gruppe\tOverskrift\tVerdier', '14. Bildeutvidelser'))
for group in groups:
    association = next(row.split('\t', 1)[1] for row in association_rows if row.split('\t', 1)[0] == group['name'])
    group['sitelinks'] = association.split('; ')
    snippet = next(row.split('\t') for row in snippet_rows if row.split('\t', 1)[0] == group['name'])
    group['structured_snippet'] = {'header': snippet[1], 'values': snippet[2].split(' · ')}

# Preserve all routing exclusions, including conditional Exact rows. The recipient
# map is derived from exact source phrases, with documented Norwegian ASCII forms.
def ascii_norwegian(value):
    return normalized(value).replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')


for group in groups:
    group['negative_routing_assignments'] = []
    for negative in group['negative_keywords']:
        if negative['match_type'] != 'Exact':
            continue
        recipients = [other['index'] for other in groups if other['index'] != group['index'] and any(
            ascii_norwegian(negative['text']) == ascii_norwegian(pos['text']) for pos in other['positive_keywords'])]
        group['negative_routing_assignments'].append({
            'negative': negative, 'recipient_group_indices': recipients,
            'evidence_type': 'INFERRED_FROM_SOURCE_KEYWORD_MATCH',
            'condition_explicit_in_attachment': group['negative_routing_condition_explicit_in_attachment'],
            'launch_check': 'Read back recipient targeting, status, landing suitability and negative conflicts before enabling traffic.'
        })

payload = {
    'artifact_type': 'LOCAL_REVIEW_PAYLOAD_NOT_LIVE_STATE',
    'source_file': str(SOURCE), 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_note': 'Literal extraction from supplied attachment. No external/account/landing-page read in this delegated lane.',
    'campaign': {
        'name': 'DLM | MS | NO | NB | Search | 202609', 'campaign_id': None, 'location': 'Norway',
        'user_requested_name': 'DLM | MS | NB | NB | Search | 202609',
        'attachment_name': 'DLM | MS | US | NB | Search | 202609',
        'attachment_location': 'United States',
        'target_identity_status': 'NORWAY_NO_NB_SEPARATE_NEW_PAUSED_COPY_AUTHORIZED_BY_PARENT_CURRENT_SCOPE',
        'creation_plan': 'Create a separate new paused copy of source campaign 506254907 for Norway / Norwegian Bokmål NO | NB; target campaign ID remains null until created and read back.',
        'excluded_campaigns': [{'campaign_id': '506256099', 'owner': 'Polish campaign task',
                                'verified_state_reported_by_parent': 'Owner confirmed renamed PL | PL and Paused.',
                                'instruction': 'Permanently excluded from this Norwegian task; no Norwegian writes.'}],
        'language': 'Norwegian', 'language_code': 'NB',
        'location_intent': 'People in your targeted locations',
        'type': 'Search', 'goal': 'Drive conversions', 'setup_status': 'Paused',
        'budget': 10, 'budget_currency': 'USD', 'budget_period': 'Daily',
        'bidding_strategy': 'Maximize Clicks', 'maximum_cpc': 0.20, 'maximum_cpc_currency': 'USD',
        'maximum_cpc_enabled': True,
        'budget_and_bid_note': 'Parent current native source readback verified USD10/day and Maximize Clicks with checked USD0.20 cap. Preserve as source monetary baseline for paused copying only; no activation or spend increase inferred.',
        'monetary_evidence_source': 'Parent supplied current native source readback; this local payload lane did not access account.',
        'tracking_template': '',
        'negative_keywords': campaign_nb + campaign_en + campaign_exact,
        'negative_keyword_subsets': {'norwegian_phrase': campaign_nb, 'supplemental_english_phrase': campaign_en, 'provisional_catalog_exact': campaign_exact},
        'provisional_catalog_exact_condition': 'Supplied temporary assortment exclusions; no new inventory/size-combination check was provided.',
        'callouts': callouts, 'callout_assignment': 'Campaign-level shared across all eight groups.',
        'sitelinks': sitelinks,
    },
    'ad_groups': groups,
    'authority_correction_provenance': [
        {'sequence': 1, 'source': 'Original user request', 'record': 'Requested DLM | MS | NB | NB | Search | 202609 and Norwegian localization.'},
        {'sequence': 2, 'source': 'Supplied attachment', 'record': 'Specifies US | NB / United States. Attachment source text and hash have not been changed.'},
        {'sequence': 3, 'source': 'Parent owner readback', 'record': 'Campaign506256099 belongs exclusively to Polish task, renamed PL | PL and Paused; permanently excluded from Norwegian writes.'},
        {'sequence': 4, 'source': 'Latest user correction relayed by parent', 'quote': 'in that case you need to do Norwegian with language norsk with instructions I gave you',
         'parent_scope_resolution': 'Norway / Norwegian Bokmål, NO | NB, separate new paused source copy. Effective payload country/name follow this current parent scope; historical attachment remains US.'},
    ],
    'image_assets': {'requested_policy': 'Preserve copied source images; do not invent or substitute pictures.',
                     'declared_pairs': 160, 'provided_pairs': 0, 'text_pairs': None,
                     'status': 'MISSING_ATTACHMENT_CONTENT',
                     'note': 'Paste references downloadable ZIP/Excel/caption files but includes no file links or actual caption/alt-text pairs. Cannot validate or apply 320 absent fields.'},
    'unresolved': [
        'Separate new Norwegian target campaign ID remains unknown until parent creates and reads back the authorized NO | NB paused copy. Campaign506256099 remains permanently excluded.',
        'Candidate NO | NB final URL suffixes are prepared but not applied or verified against inherited/automatic tracking; effective suffix remains null pending parent inheritance readback.',
        '160 image-caption pairs are referenced but absent.',
        'Live /no/ landing readiness, including family-tops, not verified here; attachment historical claims are not fresh proof.',
        'Source phrase/exact order and source images require root current-account reconciliation.',
    ],
    'preservation_decisions': ['Keep explicit 84 supplemental English campaign negatives and supplied English group negatives per root instruction; no extra language-only exclusion invented.',
                              'Keep all 54 group negatives in paused review payload, including conditional Exact entries; recipient eligibility remains launch check.',
                              'Eighth Mommy & Me Outfits group is explicitly requested by attachment; parent reports native source has seven groups. Do not pretend all eight are present in source.'],
}

length_rows, errors, duplicates, conflicts = [], [], [], []
positive_owners = collections.defaultdict(list)


def check_length(scope, field, value, limit):
    row = {'scope': scope, 'field': field, 'text': value, 'length': len(value), 'limit': limit, 'pass': len(value) <= limit}
    length_rows.append(row)
    if not row['pass']:
        errors.append(row)


def check_duplicates(scope, items):
    counts = collections.Counter((normalized(k['text']), k['match_type']) for k in items)
    duplicates.extend({'scope': scope, 'keyword': key, 'count': count} for key, count in counts.items() if count > 1)


def excludes(negative, positive):
    n, p = normalized(negative['text']), normalized(positive['text'])
    return n == p if negative['match_type'] == 'Exact' else f' {n} ' in f' {p} '


for group in groups:
    number = group['index']
    for field, limit in [('headlines', 30), ('descriptions', 90)]:
        for value in group[field]:
            check_length(group['name'], field, value, limit)
    for field in ['path_1', 'path_2']:
        check_length(group['name'], field, group[field], 15)
    for value in group['structured_snippet']['values']:
        check_length(group['name'], 'snippet_value', value, 25)
    for kind in ('positive', 'negative'):
        check_duplicates(f'group_{number}_{kind}s', group[f'{kind}_keywords'])
    for positive in group['positive_keywords']:
        positive_owners[(normalized(positive['text']), positive['match_type'])].append(number)
        for scope, negatives in [('campaign', payload['campaign']['negative_keywords']), ('group', group['negative_keywords'])]:
            for negative in negatives:
                if excludes(negative, positive):
                    conflicts.append({'group': number, 'scope': scope, 'positive': positive, 'negative': negative})
    write_json(f'group_{number:02d}.json', group)
    for kind in ('positive', 'negative'):
        (ROOT / f'group_{number:02d}_{kind}_keywords.txt').write_text(keyword_block(group[f'{kind}_keywords']) + '\n')
check_duplicates('campaign_negatives', payload['campaign']['negative_keywords'])
for link in sitelinks:
    for field, limit in [('text', 25), ('description_1', 35), ('description_2', 35)]:
        check_length('sitelink', field, link[field], limit)
for value in callouts:
    check_length('campaign', 'callout', value, 25)

counts = {
    'groups': len(groups), 'positive_keywords': sum(len(g['positive_keywords']) for g in groups),
    'positive_exact': sum(k['match_type'] == 'Exact' for g in groups for k in g['positive_keywords']),
    'positive_phrase': sum(k['match_type'] == 'Phrase' for g in groups for k in g['positive_keywords']),
    'headlines': sum(len(g['headlines']) for g in groups), 'descriptions': sum(len(g['descriptions']) for g in groups),
    'campaign_negative_norwegian_phrase': len(campaign_nb), 'campaign_negative_english_phrase': len(campaign_en),
    'campaign_negative_provisional_exact': len(campaign_exact), 'campaign_negatives_total': len(payload['campaign']['negative_keywords']),
    'group_negatives_total': sum(len(g['negative_keywords']) for g in groups),
    'group_negative_exact': sum(k['match_type'] == 'Exact' for g in groups for k in g['negative_keywords']),
    'group_negative_phrase': sum(k['match_type'] == 'Phrase' for g in groups for k in g['negative_keywords']),
    'sitelinks': len(sitelinks), 'sitelink_associations': sum(len(g['sitelinks']) for g in groups),
    'callouts': len(callouts), 'snippets': len(groups), 'snippet_values': sum(len(g['structured_snippet']['values']) for g in groups),
    'image_text_pairs_provided': 0, 'image_text_fields_provided': 0,
}
expected = {'groups': 8, 'positive_keywords': 144, 'headlines': 120, 'descriptions': 32,
            'campaign_negative_norwegian_phrase': 138, 'campaign_negative_english_phrase': 84,
            'campaign_negative_provisional_exact': 11, 'campaign_negatives_total': 233,
            'group_negatives_total': 54, 'sitelinks': 8, 'sitelink_associations': 32, 'callouts': 6, 'snippets': 8}
for key, value in expected.items():
    if counts[key] != value:
        errors.append({'count': key, 'expected': value, 'actual': counts[key]})
for group in groups:
    if len(group['headlines']) != 15 or len(group['descriptions']) != 4:
        errors.append({'group': group['index'], 'error': 'RSA field count mismatch'})
    if any(title not in {link['text'] for link in sitelinks} for title in group['sitelinks']):
        errors.append({'group': group['index'], 'error': 'Unknown sitelink association'})
    for row in group['negative_routing_assignments']:
        if not row['recipient_group_indices']:
            errors.append({'group': group['index'], 'error': 'Unresolved Exact routing recipient', 'negative': row['negative']})

validation = {
    'result': 'PASS_LOCAL_WITH_DOCUMENTED_LIMITATIONS' if not errors and not duplicates and not conflicts else 'FAIL',
    'counts': counts, 'errors': errors, 'within_scope_duplicate_keyword_entries': duplicates,
    'cross_group_duplicate_positive_entries': [{'keyword': key, 'groups': owners} for key, owners in positive_owners.items() if len(set(owners)) > 1],
    'literal_positive_negative_conflicts': conflicts,
    'validation_scope': 'Unicode character lengths; exact match-type counts; NFC/casefold/token duplicate and literal Phrase/Exact conflict check. No Microsoft semantic, policy, account or website validation.',
    'length_checks': length_rows,
    'per_group_counts': [{'index': g['index'], 'name': g['name'], 'positive': len(g['positive_keywords']), 'negative': len(g['negative_keywords']),
                          'negative_exact': sum(k['match_type'] == 'Exact' for k in g['negative_keywords']),
                          'headlines': len(g['headlines']), 'descriptions': len(g['descriptions'])} for g in groups],
    'missing_image_text_fields_not_validated': 320,
}
write_json('campaign_payload.json', payload)
write_json('validation.json', validation)
for name, items in [('campaign_negative_keywords', payload['campaign']['negative_keywords']), ('campaign_negative_keywords_phrase', campaign_nb + campaign_en),
                    ('campaign_negative_keywords_exact_provisional', campaign_exact)]:
    (ROOT / f'{name}.txt').write_text(keyword_block(items) + '\n')
write_json('sitelinks.json', sitelinks)
(ROOT / 'callouts.txt').write_text('\n'.join(callouts) + '\n')
print(json.dumps({'result': validation['result'], 'counts': counts, 'errors': errors, 'duplicates': duplicates, 'conflicts': conflicts}, ensure_ascii=False, indent=2))
assert not errors and not duplicates and not conflicts
