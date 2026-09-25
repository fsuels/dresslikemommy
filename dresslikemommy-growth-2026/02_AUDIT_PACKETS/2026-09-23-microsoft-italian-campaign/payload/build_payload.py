#!/usr/bin/env python3
"""Extract the user supplied Italian campaign; does not perform external writes."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/fsuels/.codex/attachments/491f8936-0314-4f98-8415-2d8b45840f3d/Pasted text.txt')
raw = SOURCE.read_text()
lines = raw.splitlines()


def extract_rows(text):
    rows = []
    for line in text.splitlines():
        value = line.strip()
        if re.fullmatch(r'\[.+\]', value):
            rows.append({'text': value[1:-1], 'match': 'Exact'})
        elif re.fullmatch(r'".+"', value):
            rows.append({'text': value[1:-1], 'match': 'Phrase'})
    return rows


def between(text, first, last):
    return text.split(first, 1)[1].split(last, 1)[0]


def nonblank(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def ui(rows):
    return '\n'.join(f'[{r["text"]}]' if r['match'] == 'Exact' else f'"{r["text"]}"' for r in rows) + ('\n' if rows else '')


group_pattern = re.compile(r'^\d+\. Gruppo (\d+) — (.+)$', re.M)
matches = list(group_pattern.finditer(raw))
groups = []
tracking_text = between(raw, '12. Opzioni URL e tracciamento per gruppo', '13. Estensioni in italiano')
tracking_suffixes = re.findall(r'^utm_source=.*$', tracking_text, re.M)
for n, match in enumerate(matches):
    end = matches[n + 1].start() if n + 1 < len(matches) else raw.index('11. Esclusioni della campagna')
    block = raw[match.end():end]
    ad_start = block.index('\nTitoli')
    desc_start = block.index('\nDescrizioni')
    neg_start = block.index('\nEsclusioni')
    headline_text = block[ad_start:desc_start].split('\n', 2)[2]
    description_text = block[desc_start:neg_start].split('\n', 2)[2]
    positives = extract_rows(between(block, 'Parole chiave positive', '\nTitoli'))
    negative_text = block[neg_start:]
    negatives = extract_rows(negative_text)
    group = {
        'index': int(match[1]),
        'name': match[2],
        'source_name': re.search(r'Equivalente a (.+)\.', block)[1],
        'url': re.search(r'https://www\.dresslikemommy\.com/it/collections/[^\s]+', block)[0],
        'path1': re.search(r'^Path 1: (.+)$', block, re.M)[1],
        'path2': re.search(r'^Path 2: (.+)$', block, re.M)[1],
        'keywords': positives,
        'headlines': nonblank(headline_text),
        'descriptions': nonblank(description_text),
        'negatives': negatives,
        'negative_instructions_verbatim': negative_text.strip(),
        'source_lines': {'start': raw[:match.start()].count('\n') + 1, 'end': raw[:end].count('\n')},
        'tracking': {
            'tracking_template': '',
            'custom_parameters': {},
            'final_url_suffix_supplied_us_market': tracking_suffixes[n],
            'final_url_suffix_candidate_it_market': tracking_suffixes[n].replace('dlm_ms_us_it_search_202609', 'dlm_ms_it_it_search_202609'),
            'final_url_suffix': tracking_suffixes[n].replace('dlm_ms_us_it_search_202609', 'dlm_ms_it_it_search_202609'),
            'gate': 'Italy/Italian confirmed by user via parent; verify manual UTMs do not duplicate automatic or inherited parameters before applying.',
        },
        'copy_source_exists_in_parent_native_readback': int(match[1]) != 6,
        'serving_status': 'Paused during configuration',
    }
    # Preserve exact supplied routing rows in full while exposing their conditional nature.
    for negative in negatives:
        negative['conditional'] = negative['match'] == 'Exact'
        if negative['conditional']:
            negative['condition_provenance'] = 'EXPLICIT_SOURCE' if group['index'] in [2, 6] else 'INFERRED_FROM_SPECIFIC_GROUP_ROUTING__SOURCE_HAS_NO_EXPLICIT_GATE_IN_GROUP_3'
            t = negative['text']
            if any(x in t for x in ['papà', 'papa', 'padre']):
                destination = 5
            elif any(x in t for x in ['maglioni', 'felpe', 'cardigan']):
                destination = 8
            elif 'pigiami' in t:
                destination = 4
            elif 'costumi' in t:
                destination = 7
            elif any(x in t for x in ['abiti', 'vestiti']):
                destination = 1
            else:
                destination = 3
            negative['routing_destination_group_index'] = destination
            negative['condition'] = 'Use when destination group is active and eligible; validate before activation.'
    group['destination_gate'] = 'Public destination verification required before activation.'
    if int(match[1]) == 8:
        group['destination_gate'] = 'Explicit source gate: family-sweaters destination was not retrieved; verify before activation or associated sitelink activation.'
    groups.append(group)

campaign_block = between(raw, '11. Esclusioni della campagna', '12. Opzioni URL e tracciamento per gruppo')
campaign_it = extract_rows(between(campaign_block, 'A. Esclusioni italiane — Phrase', 'B. Esclusioni inglesi complementari — Phrase'))
campaign_en = extract_rows(between(campaign_block, 'B. Esclusioni inglesi complementari — Phrase', 'C. Restrizioni temporanee di assortimento — Exact'))
campaign_exact = extract_rows(between(campaign_block, 'C. Restrizioni temporanee di assortimento — Exact', 'D. Termini da non escludere automaticamente'))
for row in campaign_it:
    row.update(section='Italian Phrase', supplied_language_category='it')
for row in campaign_en:
    row.update(section='Complementary English Phrase', supplied_language_category='en')
for row in campaign_exact:
    row.update(section='Temporary assortment Exact', supplied_language_category='it', removal_gate='Verify actual merchandise combinations and purchasable sizes before removing.')
campaign_negatives = campaign_it + campaign_en + campaign_exact

extensions = between(raw, '13. Estensioni in italiano', '14. Estensioni immagine')
callouts = nonblank(between(extensions, 'Una riga per campo:', 'Tutti i sei testi'))
sitelink_text = between(extensions, 'Usa come destinazione il Final URL italiano del gruppo corrispondente.', 'I testi rispettano i limiti')
sitelink_lines = nonblank(sitelink_text)
sitelinks = []
for i in range(8):
    heading, text, desc1, desc2 = sitelink_lines[i * 4:(i + 1) * 4]
    assert heading == text
    sitelinks.append({'index': i + 1, 'group_index': i + 1, 'text': text, 'description1': desc1, 'description2': desc2, 'url': groups[i]['url'], 'activation_gate': groups[i]['destination_gate']})
association_text = between(extensions, 'Gruppo\tSitelink proposti', 'Non attivare il sitelink')
associations = []
for line in nonblank(association_text):
    group_name, links = line.split('\t')
    group = next(g for g in groups if g['name'] == group_name)
    texts = links.split('; ')
    associations.append({'group_index': group['index'], 'group_name': group_name, 'sitelink_indices': [next(s['index'] for s in sitelinks if s['text'] == name) for name in texts], 'sitelink_texts': texts})
snippet_text = extensions.split('Gruppo\tIntestazione\tValori', 1)[1]
snippets = []
for line in nonblank(snippet_text):
    group_name, header, values = line.split('\t')
    group = next(g for g in groups if g['name'] == group_name)
    snippets.append({'group_index': group['index'], 'group_name': group_name, 'header': header, 'values': values.split(' · ')})

payload = {
    'artifact_status': 'LOCAL_PAYLOAD_ONLY__NOT_APPLIED',
    'source': {'path': str(SOURCE), 'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'line_count': len(lines)},
    'campaign': {
        'name_requested': 'DLM | MS | IT | IT | Search | 202609',
        'name_supplied': 'DLM | MS | US | IT | Search | 202609',
        'name_resolved': 'DLM | MS | IT | IT | Search | 202609',
        'market_requested': 'IT', 'market_supplied': 'US', 'market_resolved': 'IT',
        'location_resolved': 'Italy',
        'identity_status': 'RESOLVED_USER_CONFIRMED_ITALY_ITALIAN__PARENT_REPORTED',
        'language': 'Italian', 'language_code': 'it',
        'location_intent': 'People in your targeted locations',
        'campaign_type': 'Search', 'campaign_goal_supplied': 'Drive conversions',
        'ad_group_type': 'Standard', 'ad_format': 'Responsive Search Ad',
        'status_during_configuration': 'Paused',
        'headlines_descriptions_pinning': 'None initially',
        'budget': 10, 'budget_currency': 'USD', 'budget_type': 'Daily', 'bidding_strategy': 'Maximize Clicks', 'max_cpc': 0.20, 'max_cpc_currency': 'USD',
        'source_native_readback_parent_report': {'group_count': 7, 'daily_budget_usd': 10, 'bidding_strategy': 'Maximize Clicks', 'max_cpc_usd': 0.20, 'independently_verified_by_payload_agent': False},
        'budget_gate': 'Parent reports user accepted preserved source USD10/day, Maximize Clicks with USD0.20 max CPC for the paused copy. This does not authorize activation.',
        'resolved_decisions': ['User explicitly selected Italy/Italian and IT|IT name via parent instruction.', 'Preserve source USD10/day Maximize Clicks USD0.20 cap as accepted via parent instruction.', 'Keep the campaign paused during configuration.'],
        'source_name': 'DLM | MS | US | EN | Search | 202609',
        'do_not_enable_automatically': ['AI Max', 'Broad Match', 'URL expansion'],
        'tracking_gate': 'No new UET or duplicated purchase goal. Check inherited and ad-level URL settings before applying manual suffix.',
    },
    'groups': groups,
    'campaign_negatives': campaign_negatives,
    'campaign_negative_language_policy': 'Supplied plan intentionally includes 84 complementary English Phrase rows and English loanwords in group negatives. Confirm consistency with user request to translate everything; do not silently omit or translate source-specific mixed-query protection.',
    'campaign_negative_application': 'Campaign-level entries only; never modify shared lists for other language campaigns.',
    'callouts': callouts,
    'sitelinks': sitelinks,
    'sitelink_associations': associations,
    'snippets': snippets,
    'images': {'photos': 'Reuse same source images; actual source associations require parent readback.', 'caption_pairs_advertised': 160, 'caption_pairs_supplied': 0, 'captions': [], 'status': 'MISSING_FROM_PASTED_ATTACHMENT', 'gate': 'Do not invent absent image descriptions. Caption translation requires actual existing captions and visual/source-image correspondence; preserve shared English assets.'},
    'conditional_gates': [
        'All 27 Exact group routing negatives are preserved. The attachment explicitly gates 19 rows in groups 2 and 6 on destination groups being active and eligible; the same operational gate for 8 group-3 routing rows is an inference and is labeled per row.',
        '13 Exact campaign assortment restrictions are provisional: retain unless product/size evidence supports removal.',
        'Family-sweaters URL and its sitelink require explicit destination verification.',
        'Mommy & Me Outfits is absent from the 7-group native source inventory supplied by parent; eighth group needs separately determined copy/creation method.',
        'The 160 image-caption pairs advertised by the pasted document are absent; no inferred values included.',
        'Supplied complementary English negatives are literal source content, not automatically an all-Italian final-language policy.',
        'Local literal checks do not substitute for native negative keyword conflict report or editorial approval.',
    ],
}

issues = []
checks = []
def check(name, condition, details=None):
    checks.append({'check': name, 'pass': bool(condition), 'details': details})
    if not condition:
        issues.append(name)

check('group count', len(groups) == 8, len(groups))
check('positive count', sum(len(g['keywords']) for g in groups) == 144, [len(g['keywords']) for g in groups])
check('Italian phrase negatives', len(campaign_it) == 112, len(campaign_it))
check('English phrase negatives', len(campaign_en) == 84, len(campaign_en))
check('Exact campaign negatives', len(campaign_exact) == 13, len(campaign_exact))
check('group negatives', sum(len(g['negatives']) for g in groups) == 49, [len(g['negatives']) for g in groups])
check('headlines', sum(len(g['headlines']) for g in groups) == 120)
check('descriptions', sum(len(g['descriptions']) for g in groups) == 32)
check('callouts', len(callouts) == 6)
check('sitelinks', len(sitelinks) == 8)
check('associations', len(associations) == 8 and all(len(a['sitelink_indices']) == 4 for a in associations))
check('snippets', len(snippets) == 8)
check('resolved Italy Italian identity', payload['campaign']['market_resolved'] == 'IT' and payload['campaign']['language_code'] == 'it' and payload['campaign']['name_resolved'] == 'DLM | MS | IT | IT | Search | 202609')
check('accepted preserved paused settings', payload['campaign']['budget'] == 10 and payload['campaign']['budget_currency'] == 'USD' and payload['campaign']['budget_type'] == 'Daily' and payload['campaign']['bidding_strategy'] == 'Maximize Clicks' and payload['campaign']['max_cpc'] == 0.20 and payload['campaign']['status_during_configuration'] == 'Paused')
check('selected Italy UTM suffixes', all('utm_campaign=dlm_ms_it_it_search_202609&' in g['tracking']['final_url_suffix'] and g['tracking']['final_url_suffix'] == g['tracking']['final_url_suffix_candidate_it_market'] and 'utm_campaign=dlm_ms_us_it_search_202609&' in g['tracking']['final_url_suffix_supplied_us_market'] for g in groups))
check('source contains no image-caption pairs', payload['images']['caption_pairs_supplied'] == 0, 'Missing source content is an unresolved gate, not successful image completion.')

def dupes(rows):
    return [list(k) for k, v in Counter((r['text'].casefold(), r['match']) for r in rows).items() if v > 1]

check('campaign negative duplicates', not dupes(campaign_negatives), dupes(campaign_negatives))
lengths = []
for g in groups:
    check(f'group {g["index"]} positive duplicates', not dupes(g['keywords']), dupes(g['keywords']))
    check(f'group {g["index"]} negative duplicates', not dupes(g['negatives']), dupes(g['negatives']))
    check(f'group {g["index"]} fields', len(g['headlines']) == 15 and len(g['descriptions']) == 4)
    for field, limit in [('headlines', 30), ('descriptions', 90)]:
        for i, value in enumerate(g[field], 1):
            lengths.append({'kind': field, 'group_index': g['index'], 'index': i, 'length': len(value), 'limit': limit, 'text': value})
    for field in ['path1', 'path2']:
        lengths.append({'kind': field, 'group_index': g['index'], 'length': len(g[field]), 'limit': 15, 'text': g[field]})
    check(f'group {g["index"]} italian URL', g['url'].startswith('https://www.dresslikemommy.com/it/collections/'))
for i, text in enumerate(callouts, 1):
    lengths.append({'kind': 'callout', 'index': i, 'length': len(text), 'limit': 25, 'text': text})
for s in sitelinks:
    for field, limit in [('text', 25), ('description1', 35), ('description2', 35)]:
        lengths.append({'kind': 'sitelink_' + field, 'index': s['index'], 'length': len(s[field]), 'limit': limit, 'text': s[field]})
for snippet in snippets:
    for i, text in enumerate(snippet['values'], 1):
        lengths.append({'kind': 'snippet_value', 'group_index': snippet['group_index'], 'index': i, 'length': len(text), 'limit': 25, 'text': text})
violations = [v for v in lengths if v['length'] > v['limit']]
check('all character limits', not violations, violations)

def normalized(value):
    return ' '.join(re.findall(r'\w+', value.casefold()))

conflicts = []
for g in groups:
    for p in g['keywords']:
        positive = normalized(p['text'])
        for scope, negatives in [('campaign', campaign_negatives), ('group', g['negatives'])]:
            for neg in negatives:
                negative = normalized(neg['text'])
                hit = positive == negative if neg['match'] == 'Exact' else f' {negative} ' in f' {positive} '
                if hit:
                    conflicts.append({'group_index': g['index'], 'positive': p, 'negative': neg, 'scope': scope})
check('literal positive/negative conflicts', not conflicts, conflicts)
report = {
    'status': 'PASS_LOCAL_EXTRACTION' if not issues else 'FAIL_LOCAL_EXTRACTION',
    'source_sha256': payload['source']['sha256'],
    'checks': checks, 'failed_checks': issues,
    'counts': {'groups': len(groups), 'keywords': sum(len(g['keywords']) for g in groups), 'headlines': sum(len(g['headlines']) for g in groups), 'descriptions': sum(len(g['descriptions']) for g in groups), 'campaign_phrase_negatives': len(campaign_it) + len(campaign_en), 'campaign_exact_negatives': len(campaign_exact), 'group_phrase_negatives': sum(r['match'] == 'Phrase' for g in groups for r in g['negatives']), 'group_exact_negatives': sum(r['match'] == 'Exact' for g in groups for r in g['negatives']), 'sitelinks': len(sitelinks), 'group_sitelink_associations': sum(len(a['sitelink_indices']) for a in associations), 'callouts': len(callouts), 'snippets': len(snippets), 'image_caption_pairs': 0},
    'field_lengths': lengths,
    'literal_conflicts': conflicts,
    'unresolved_gates': payload['conditional_gates'],
    'limitations': ['Source-content extraction, not native state verification.', 'Literal word-sequence filter is not the Microsoft semantic matcher.', 'Source 144 match-sequence assertion is preserved but no actual English keyword export was provided to this agent for independent sequence parity.'],
}

(ROOT / 'payload.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
ui_root = ROOT / 'ui'
ui_root.mkdir(exist_ok=True)
for g in groups:
    slug = f'{g["index"]:02d}'
    (ui_root / f'{slug}_keywords.txt').write_text(ui(g['keywords']))
    (ui_root / f'{slug}_negatives_complete_plan.txt').write_text(ui(g['negatives']))
    (ui_root / f'{slug}_negatives_phrase.txt').write_text(ui([r for r in g['negatives'] if r['match'] == 'Phrase']))
    (ui_root / f'{slug}_negatives_exact_conditional.txt').write_text(ui([r for r in g['negatives'] if r['match'] == 'Exact']))
    (ui_root / f'{slug}_headlines.txt').write_text('\n'.join(g['headlines']) + '\n')
    (ui_root / f'{slug}_descriptions.txt').write_text('\n'.join(g['descriptions']) + '\n')
    (ui_root / f'{slug}_ad.json').write_text(json.dumps(g, ensure_ascii=False, indent=2) + '\n')
(ui_root / 'campaign_negatives_complete_plan.txt').write_text(ui(campaign_negatives))
(ui_root / 'campaign_negatives_italian_phrase.txt').write_text(ui(campaign_it))
(ui_root / 'campaign_negatives_english_phrase.txt').write_text(ui(campaign_en))
(ui_root / 'campaign_negatives_exact_provisional.txt').write_text(ui(campaign_exact))
(ui_root / 'callouts.txt').write_text('\n'.join(callouts) + '\n')
ui_ready = {
    'artifact_status': payload['artifact_status'],
    'campaign': payload['campaign'],
    'groups': [{
        'index': g['index'], 'name': g['name'], 'source_name': g['source_name'],
        'url': g['url'], 'path1': g['path1'], 'path2': g['path2'],
        'keywords_text': ui(g['keywords']),
        'headlines': g['headlines'], 'descriptions': g['descriptions'],
        'negatives_text': ui(g['negatives']),
        'negatives_phrase_text': ui([r for r in g['negatives'] if r['match'] == 'Phrase']),
        'negatives_exact_conditional_text': ui([r for r in g['negatives'] if r['match'] == 'Exact']),
        'final_url_suffix': g['tracking']['final_url_suffix'],
        'tracking_template': '', 'custom_parameters': {},
    } for g in groups],
    'campaign_negatives_text': ui(campaign_negatives),
    'callouts': callouts, 'sitelinks': sitelinks,
    'sitelink_associations': associations, 'snippets': snippets,
    'conditional_gates': payload['conditional_gates'],
}
(ROOT / 'ui_ready.json').write_text(json.dumps(ui_ready, ensure_ascii=False, separators=(',', ':')) + '\n')

summary = ['# Italian campaign payload — local extraction', '', f'Status: **{report["status"]}**. This folder contains source extraction and UI paste files only; no native account writes or activation.', '', '| Group | Positive rows | Group negatives |', '|---|---:|---:|']
summary += [f'| {g["index"]}. {g["name"]} | {len(g["keywords"])} | {len(g["negatives"])} |' for g in groups]
summary += ['', 'Counts: 144 positives; 120 headlines; 32 descriptions; 196 campaign Phrase negatives (112 Italian + 84 complementary English); 13 provisional campaign Exact negatives; 49 group negatives (22 Phrase + 27 conditional Exact); 8 sitelinks, 32 group associations, 6 callouts, 8 snippets.', '', f'Local validation: {sum(c["pass"] for c in checks)}/{len(checks)} checks pass, {len(violations)} length violations, {len(conflicts)} literal conflicts. Match/text duplicates are checked per scope. Native editorial eligibility and negative conflict report remain separate.', '', '## Unresolved gates', '']
summary += ['- ' + gate for gate in payload['conditional_gates']]
summary += ['', '## Resolved settings', '', 'Parent reports explicit user selection of Italy/Italian: `DLM | MS | IT | IT | Search | 202609`. Preserve USD10/day, Maximize Clicks, USD0.20 max CPC in the paused copy. All eight selected suffixes use `utm_campaign=dlm_ms_it_it_search_202609`; supplied US originals remain provenance. No activation authority is inferred.', '', '## Files', '', '- `payload.json`: full extracted payload, source hash/line ranges, source names, conditional row metadata, extensions and supplied/candidate/selected tracking.', '- `ui_ready.json`: compact UI-ready groups with multiline keyword and negative strings, ad field arrays, selected Italy suffixes, campaign settings and extensions.', '- `validation.json`: counts, checks, full character lengths and limitations.', '- `ui/01..08_keywords.txt`: source Exact/Phrase syntax, one row per line.', '- `ui/01..08_negatives_complete_plan.txt`: all group negatives; conditional rows are not omitted.', '- `ui/01..08_negatives_exact_conditional.txt`: isolated routing rows for gate-aware handling.', '- `ui/campaign_negatives_*.txt`: complete and split campaign lists.', '- `ui/01..08_headlines.txt`, `descriptions.txt`, `ad.json`: ad-entry fields.', '- `build_payload.py`: deterministic extractor; rerunning regenerates only this owned folder.', '', 'The attachment advertises downloadable ZIP/Excel/image-caption files but provides no downloadable URLs or actual caption pairs. The claimed 40 sample-query tests and spreadsheet/ZIP validations cannot be reproduced from the pasted content; they are not adopted as performed checks.', '', 'Parent owns native source inventory, external writes/readbacks, authoritative coordination/worklog updates and independent review.']
(ROOT / 'README.md').write_text('\n'.join(summary) + '\n')
print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed_checks': issues, 'counts': report['counts']}, ensure_ascii=False))
if issues:
    raise SystemExit(1)
