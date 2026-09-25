"""Source-bound local extraction; no advertising-account interaction."""
from pathlib import Path
import collections
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent
SOURCE = Path('/Users/fsuels/.codex/attachments/14ea8a11-d015-4956-9f9f-d76e5bd5197e/Pasted text.txt')
raw = SOURCE.read_text()
lines = raw.splitlines()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

def nonempty(text):
    return [x.strip() for x in text.splitlines() if x.strip()]

def keywords(text):
    answer = []
    for line in text.splitlines():
        line = line.strip()
        if re.fullmatch(r'\[[^\n]+\]', line):
            answer.append({'text': line[1:-1], 'match_type': 'Exact', 'input': line})
        elif re.fullmatch(r'"[^\n]+"', line):
            answer.append({'text': line[1:-1], 'match_type': 'Phrase', 'input': line})
    return answer

matches = list(re.finditer(r'^\d+\. Groep (\d+) — (.+)$', raw, re.M))
groups = []
tracking = between(raw, '12. URL-opties en tracking per groep', '13. Nederlandse advertentie-extensies')
suffixes = re.findall(r'^utm_source=.+$', tracking, re.M)
assert len(matches) == len(suffixes) == 8
for i, m in enumerate(matches):
    block = raw[m.end():matches[i+1].start() if i+1 < len(matches) else raw.index('11. Campagne-uitsluitingen')]
    source_name = re.search(r'Dezelfde functie als (.+)\.', block).group(1)
    heads, desc = re.search(r'^Koppen[^\n]*\n([\s\S]+?)^Beschrijvingen[^\n]*\n([\s\S]+?)^Uitsluitingen', block, re.M).groups()
    neg_section = block.split('Uitsluitingen', 1)[1]
    positive_section = between(block, 'Positieve zoekwoorden', 'Koppen')
    groups.append({
        'number': int(m.group(1)), 'name': m.group(2), 'english_source_group': source_name,
        'source_line': raw[:m.start()].count('\n') + 1,
        'final_url': re.search(r'^https://[^\n]+', block, re.M).group(),
        'path1': re.search(r'^Path 1: (.+)$', block, re.M).group(1),
        'path2': re.search(r'^Path 2: (.+)$', block, re.M).group(1),
        'keywords': keywords(positive_section), 'headlines': nonempty(heads),
        'descriptions': nonempty(desc), 'negative_keywords': keywords(neg_section),
        'source_negative_notes': '\n'.join(x for x in nonempty(neg_section) if not x.startswith(('"', '['))),
        'negative_application_condition': 'Apply each routing exclusion when its specific destination group is active and suitable.' if i in (1,5) else None,
        'source_final_url_requires_check': 'Voorgestelde Final URL' in block,
        'final_url_live_verified': False,
        'source_final_url_suffix': suffixes[i],
        'resolved_final_url_suffix': None,
        'tracking_note': 'Source market is US; resolved suffix remains unset pending owner geographic decision and inherited tagging readback.'
    })

campaign_neg_section = between(raw, '11. Campagne-uitsluitingen', '12. URL-opties en tracking per groep')
campaign_negative_sets = {
    'dutch_phrase': keywords(between(campaign_neg_section, 'A. Nederlandse campagne-uitsluitingen — Phrase', 'B. Aanvullende Engelse')),
    'english_phrase': keywords(between(campaign_neg_section, 'B. Aanvullende Engelse campagne-uitsluitingen — Phrase', 'C. Tijdelijke')),
    'temporary_exact': keywords(between(campaign_neg_section, 'C. Tijdelijke assortimentbeperkingen — Exact', 'D. Wat niet')),
}
callouts = nonempty(between(raw, 'Eén regel per veld:', 'Alle zes teksten'))
sitelink_section = between(raw, 'Gebruik de Nederlandse Final URL van de bijbehorende groep.', 'Alle sitelinktitels')
sl = nonempty(sitelink_section)
assert len(sl) == 32
sitelinks = []
for i in range(8):
    header, title, description1, description2 = sl[i*4:(i+1)*4]
    sitelinks.append({'key': header, 'text': title, 'description1': description1,
                      'description2': description2, 'final_url': groups[i]['final_url']})
mapping = []
for row in nonempty(between(raw, 'Advertentiegroep\tVoorgestelde sitelinks', 'Koppel Familieshirts')):
    group_name, values = row.split('\t')
    mapping.append({'ad_group': group_name, 'sitelink_keys': values.split('; ')})
snippets = []
for row in nonempty(between(raw, 'Groep\tKop\tWaarden', '14. Afbeeldingsextensies')):
    name, header, values = row.split('\t')
    snippets.append({'ad_group': name, 'header': header, 'values': values.split(' · ')})

payload = {
    'artifact_role': 'GENERATED_SOURCE_BOUND_CANDIDATE_NOT_ACCOUNT_READBACK',
    'source': {'path': str(SOURCE), 'sha256': hashlib.sha256(raw.encode()).hexdigest(),
               'lines': len(lines), 'source_text_preserved': True},
    'scope': {'target_campaign_id_from_parent': '506255078', 'english_source_campaign_id_from_parent': '506254907',
              'source_is_read_copy_only': True, 'keep_target_paused': True, 'no_live_actions_by_payload_worker': True},
    'campaign': {'requested_name': 'DLM | MS | NL | NL | Search | 202609',
                 'attachment_name': 'DLM | MS | US | NL | Search | 202609',
                 'attachment_location': 'United States', 'attachment_location_intent': 'People in your targeted locations',
                 'resolved_market': None, 'resolved_name': None, 'language': 'Dutch', 'status': 'Paused',
                 'market_status': 'OWNER_CLARIFICATION_PENDING_WITH_PARENT',
                 'ad_group_type': 'Standard', 'ad_format': 'Responsive Search Ad',
                 'budget': None, 'bidding_strategy': None,
                 'settings_note': 'Preserve freshly verified existing target/source monetary settings only under root authority; source gives no approved new amount.'},
    'ad_groups': groups, 'campaign_negative_sets': campaign_negative_sets,
    'campaign_negative_keywords': sum(campaign_negative_sets.values(), []),
    'extensions': {'callouts': callouts, 'sitelinks': sitelinks,
                   'sitelink_associations': mapping, 'structured_snippets': snippets,
                   'image_text_pairs': [],
                   'image_text_status': 'MISSING_FROM_ATTACHMENT',
                   'image_note': 'Attachment mentions 160 caption/alt pairs in downloads but supplies neither pairs nor usable links. Do not invent or equate that claim with applied assets.'},
    'source_ambiguities': [
        'User requests NL market and Dutch language; attachment explicitly retains United States and US-based utm_campaign.',
        'Campaign-settings table truncates campaign name to `DLM; complete name occurs elsewhere and is preserved as attachment_name.',
        'Temporary Exact exclusions reflect a historic assortment restriction, not a current product audit.',
        'Declared prior landing, 40-query, spreadsheet and ZIP checks are attachment assertions, not verified by this worker.',
        'Image caption download text contains no delivered caption pairs or download URLs.'
    ],
    'release_gates': ['Owner geographic clarification', 'Fresh target/source/native settings readback',
                      'Dutch landing suitability and routing conditions', 'Inherited tagging review',
                      'Native campaign and all 8 group negative reconciliation', 'Separate activation authority']
}

def norm(s):
    return tuple(re.findall(r"\w+", s.casefold()))

def duplicates(items, key):
    c = collections.Counter(key(x) for x in items)
    return [{'key': list(k) if isinstance(k, tuple) else k, 'count': v} for k,v in c.items() if v > 1]

def literal_blocks(positive, negative):
    p,n = norm(positive),norm(negative['text'])
    if negative['match_type'] == 'Exact':
        return p == n
    return any(p[i:i+len(n)] == n for i in range(len(p)-len(n)+1))

length_checks = []
for g in groups:
    for field,limit in [('headlines',30),('descriptions',90)]:
        for index,value in enumerate(g[field],1):
            length_checks.append({'scope':g['name'],'field':field,'index':index,'text':value,'length':len(value),'limit':limit,'pass':len(value)<=limit})
    for field in ['path1','path2']:
        length_checks.append({'scope':g['name'],'field':field,'text':g[field],'length':len(g[field]),'limit':15,'pass':len(g[field])<=15})
for index,value in enumerate(callouts,1):
    length_checks.append({'scope':'callouts','index':index,'text':value,'length':len(value),'limit':25,'pass':len(value)<=25})
for item in sitelinks:
    for field,limit in [('text',25),('description1',35),('description2',35)]:
        length_checks.append({'scope':item['key'],'field':field,'text':item[field],'length':len(item[field]),'limit':limit,'pass':len(item[field])<=limit})
for item in snippets:
    for value in item['values']:
        length_checks.append({'scope':item['ad_group'],'field':'structured_snippet_value','text':value,'length':len(value),'limit':25,'pass':len(value)<=25})

conflicts = []
for g in groups:
    for p in g['keywords']:
        for scope, negatives in [('campaign',payload['campaign_negative_keywords']),('own_group',g['negative_keywords'])]:
            for n in negatives:
                if literal_blocks(p['text'],n):
                    conflicts.append({'group':g['name'],'positive':p,'negative_scope':scope,'negative':n})
keyword_key = lambda x: (x['text'].casefold(),x['match_type'])
dup = {'campaign_negatives':duplicates(payload['campaign_negative_keywords'],keyword_key),
       'group_keywords':{g['name']:duplicates(g['keywords'],keyword_key) for g in groups},
       'group_negatives':{g['name']:duplicates(g['negative_keywords'],keyword_key) for g in groups}}
counts = {'ad_groups':len(groups),'positive_keywords':sum(len(g['keywords']) for g in groups),
          'positive_by_match_type':dict(collections.Counter(k['match_type'] for g in groups for k in g['keywords'])),
          'headlines':sum(len(g['headlines']) for g in groups),'descriptions':sum(len(g['descriptions']) for g in groups),
          'campaign_negative_sets':{k:len(v) for k,v in campaign_negative_sets.items()},
          'campaign_negatives':len(payload['campaign_negative_keywords']),
          'group_negatives':sum(len(g['negative_keywords']) for g in groups),
          'group_negatives_by_match_type':dict(collections.Counter(k['match_type'] for g in groups for k in g['negative_keywords'])),
          'callouts':len(callouts),'sitelinks':len(sitelinks),'sitelink_associations':sum(len(m['sitelink_keys']) for m in mapping),
          'structured_snippets':len(snippets),'delivered_image_pairs':0,
          'groups':[{'number':g['number'],'name':g['name'],'positives':len(g['keywords']),'negatives':len(g['negative_keywords']),
                     'negative_match_counts':dict(collections.Counter(k['match_type'] for k in g['negative_keywords']))} for g in groups]}
expected = {'ad_groups':8,'positive_keywords':144,'headlines':120,'descriptions':32,'campaign_negatives':202,'group_negatives':45,
            'callouts':6,'sitelinks':8,'sitelink_associations':32,'structured_snippets':8}
structural_checks = {key: counts[key] == value for key,value in expected.items()}
structural_checks['campaign_negative_set_counts'] = counts['campaign_negative_sets'] == {'dutch_phrase':111,'english_phrase':82,'temporary_exact':9}
structural_checks['each_group_rsa_fields'] = all(len(g['headlines'])==15 and len(g['descriptions'])==4 for g in groups)
structural_checks['sitelink_mapping_resolves'] = all(set(m['sitelink_keys']) <= {s['key'] for s in sitelinks} for m in mapping)
structural_checks['extensions_group_names_resolve'] = all(m['ad_group'] in {g['name'] for g in groups} for m in mapping+snippets)
duplicate_count = len(dup['campaign_negatives']) + sum(len(v) for v in dup['group_keywords'].values()) + sum(len(v) for v in dup['group_negatives'].values())
validation = {'result':'PASS_LOCAL_TEXT_EXTRACTION' if all(structural_checks.values()) and not conflicts and not duplicate_count and all(x['pass'] for x in length_checks) else 'FAIL',
              'source_sha256':payload['source']['sha256'],'counts':counts,'structural_checks':structural_checks,
              'limits_basis':'Attachment-stated RSA, path, callout and sitelink limits; snippet value check uses 25-character candidate limit, not a current API verification.',
              'length_checks':length_checks,'length_violations':[x for x in length_checks if not x['pass']],
              'duplicate_tuple_count':duplicate_count,'duplicate_checks':dup,
              'literal_conflict_count':len(conflicts),'literal_conflicts':conflicts,
              'literal_conflict_method':'Case-folded word tokens; Exact requires full token equality, Phrase contiguous token sequence. Campaign plus own group checked for each supplied positive. Does not model Microsoft semantic matching.',
              'live_readback_performed':False,'changes_to_source_dutch_copy':0}
save('campaign_payload.json',payload)
save('validation.json',validation)
(OUT/'source.txt').write_text(raw)
print(json.dumps({'result':validation['result'],'counts':counts,'length_violations':validation['length_violations'],'duplicates':duplicate_count,'conflicts':len(conflicts)},ensure_ascii=False,indent=2))
