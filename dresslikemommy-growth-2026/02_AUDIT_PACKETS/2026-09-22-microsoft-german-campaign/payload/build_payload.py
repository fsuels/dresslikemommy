#!/usr/bin/env python3
"""Parse supplied text deterministically; never accesses Microsoft or the network."""
from pathlib import Path
import collections
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/fsuels/.codex/attachments/0bc36da9-e705-401b-a9d9-1494bb739b5a/Pasted text.txt')
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

def write_text(name, source):
    (ROOT / name).write_text(source.rstrip() + '\n')

groups = []
section_matches = list(re.finditer(r'^\d+\. Gruppe (\d+) — (.+)$', text, flags=re.M))
for i, match in enumerate(section_matches):
    end = section_matches[i+1].start() if i+1 < len(section_matches) else text.index('11. Kampagnenweite')
    section = text[match.end():end]
    head = re.search(r'^Titel[^\n]*\n', section, re.M)
    desc = re.search(r'^Beschreibungen[^\n]*\n', section, re.M)
    neg = re.search(r'^Negative Keywords[^\n]*\n', section, re.M)
    name = match[2]
    # Each suffix is followed immediately by the next numbered group, not a blank line.
    suffix_line = re.search(r'^utm_source=bing[^\n]+', text.split('12. URL-Optionen und Tracking je Gruppe',1)[1].split(f'{i+1}. {name}\n',1)[1], re.M)[0]
    group = {
        'index': int(match[1]),
        'name': name,
        'source_english_name': re.search(r'Entspricht (.+)\.', section)[1],
        'final_url': re.search(r'https://www\.dresslikemommy\.com/[^\s]+', section)[0],
        'path_1': re.search(r'Path 1: (.+)', section)[1],
        'path_2': re.search(r'Path 2: (.+)', section)[1],
        'positive_keywords': keywords(section.split('Positive Keywords\n',1)[1][:head.start()-section.index('Positive Keywords\n')-len('Positive Keywords\n')]),
        'headlines': lines(section[head.end():desc.start()]),
        'descriptions': lines(section[desc.end():neg.start()]),
        'negative_keywords': keywords(section[neg.end():]),
        'final_url_suffix': suffix_line.replace('dlm_ms_us_de_search_202609', 'dlm_ms_de_de_search_202609'),
        'tracking_template': '',
        'custom_parameters': {},
        'ad_format': 'Responsive Search Ad',
        'ad_group_type': 'Standard',
        'language': 'German',
        'pins': [],
        'image_text_pairs': None,
        'source_notes': lines(section[neg.end():])[len(keywords(section[neg.end():])):],
        'requires_live_landing_verification': True,
    }
    groups.append(group)

campaign_negative_de = keywords(between('A. Deutsche Kampagnennegative — Phrase', 'B. Ergänzende englische Kampagnennegative — Phrase'))
campaign_negative_en = keywords(between('B. Ergänzende englische Kampagnennegative — Phrase', 'C. Vorläufige Sortimentsausschlüsse — Exact'))
campaign_negative_exact = keywords(between('C. Vorläufige Sortimentsausschlüsse — Exact', 'D. Was nicht automatisch ausgeschlossen wird'))
callouts = lines(between('Eine Zeile pro Feld:', 'Alle sechs Texte'))

# The supplied paste repeats every sitelink title once as a heading. The repeated
# heading is excluded from actual title/description fields, with an explicit check.
sitelink_lines = lines(between('Als Zieladresse jeweils die deutsche Final URL der entsprechenden Gruppe verwenden.', 'Die Texte erfüllen die Grenzen'))
assert len(sitelink_lines) == 32
sitelinks = []
for i in range(8):
    heading, title, d1, d2 = sitelink_lines[i*4:i*4+4]
    assert heading == title
    sitelinks.append({'text': title, 'description_1': d1, 'description_2': d2, 'final_url': groups[i]['final_url'], 'source_group_index': i+1})
association_rows = lines(between('Anzeigengruppe\tVorgeschlagene Sitelinks', 'Den Sitelink „Familienpullover“'))
snippet_rows = lines(between('Gruppe\tÜberschrift\tWerte', '14. Bilderweiterungen'))
for group in groups:
    association = next(row.split('\t',1)[1] for row in association_rows if row.split('\t',1)[0] == group['name'])
    group['sitelinks'] = association.split('; ')
    snippet = next(row.split('\t') for row in snippet_rows if row.split('\t',1)[0] == group['name'])
    group['structured_snippet'] = {'header': snippet[1], 'values': snippet[2].split(' · ')}

optional_copy_edits = [
    {'group_index': 1, 'field': 'descriptions', 'index_1_based': 3, 'source': groups[0]['descriptions'][2], 'suggestion': 'Mama-und-ich-Kleider für Urlaub, Geburtstag und Fotos. Findet euren nächsten Partnerlook.', 'reason': 'German compound hyphenation; source keyword text remains unchanged.'},
    {'group_index': 4, 'field': 'descriptions', 'index_1_based': 3, 'source': groups[3]['descriptions'][2], 'suggestion': 'Mama-und-ich-Schlafanzüge mit Shorts oder langer Hose. Vergleicht eure Muster und Maße.', 'reason': 'German compound hyphenation.'},
    {'group_index': 6, 'field': 'headlines', 'index_1_based': 12, 'source': groups[5]['headlines'][11], 'suggestion': 'Partnerlook zum Geburtstag', 'reason': 'More idiomatic than Zusammen zum Geburtstag passen.'},
    {'group_index': 6, 'field': 'descriptions', 'index_1_based': 3, 'source': groups[5]['descriptions'][2], 'suggestion': 'Mama-und-ich-Outfits für Fotos, Geburtstage und Urlaub. Vergleicht Modelle und Größen.', 'reason': 'German compound hyphenation.'},
    {'group_index': 7, 'field': 'descriptions', 'index_1_based': 3, 'source': groups[6]['descriptions'][2], 'suggestion': 'Mama-und-ich-Bademode mit Blumen und Rüschen. Vergleicht eure Lieblingsprints und Maße.', 'reason': 'German compound hyphenation.'},
    {'group_index': 7, 'field': 'headlines', 'index_1_based': 9, 'source': groups[6]['headlines'][8], 'suggestion': 'Vergleicht eure Maße', 'reason': 'Avoids the awkward phrase eure beiden Maße.'},
]
payload = {
    'artifact_type': 'LOCAL_REVIEW_PAYLOAD_NOT_LIVE_STATE',
    'source_file': str(SOURCE),
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_note': 'Extracted from supplied attachment. External state not inspected in this delegated lane.',
    'explicit_override': 'Current user target DE | DE overrides attachment US | DE: Germany, German, revised campaign UTM.',
    'campaign': {
        'name': 'DLM | MS | DE | DE | Search | 202609',
        'location': 'Germany',
        'language': 'German',
        'location_intent': 'People in your targeted locations',
        'type': 'Search',
        'goal': 'Drive conversions',
        'setup_status': 'Paused',
        'budget': None,
        'bidding_strategy': None,
        'budget_and_bid_note': 'Read live reference; source provides no numeric authorized budget or bid.',
        'tracking_template': '',
        'negative_keywords': campaign_negative_de + campaign_negative_en + campaign_negative_exact,
        'negative_keyword_subsets': {'german_phrase': campaign_negative_de, 'supplemental_english_phrase': campaign_negative_en, 'provisional_catalog_exact': campaign_negative_exact},
        'callouts': callouts,
        'sitelinks': sitelinks,
    },
    'ad_groups': groups,
    'optional_copy_edits_not_applied': optional_copy_edits,
    'image_assets': {'policy': 'Retain reference campaign images, subject to live asset mapping. No source image text pairs or actual images are supplied in this attachment.', 'supplied_image_text_pairs': 0, 'claimed_image_text_pairs': 160, 'pairs': None},
    'limitations': [
        'Missing advertised downloadable ZIP, Excel, 160 caption/alt pairs and 40 example-query cases; no links or actual material supplied.',
        'Group Exact negatives route intent only if matching destination ad groups are active and eligible. A negative does not guarantee routing.',
        'Family-sweaters URL explicitly unverified by source. All localized landing pages and checkout need current verification.',
        'Source campaign geographic settings conflict with current user target and are explicitly overridden.',
        'Literal matching validation does not emulate Microsoft semantic matching, close variants, editorial approval or live inherited exclusions.',
        'Text preservation does not verify product availability, styles, sizing, delivery or return claims.',
        'UTM suffixes must be checked against inherited, ad-level and sitelink-level tracking to avoid duplicate or stale English campaign tags.',
        'No keyword demand, CPC, conversion or sales evidence accompanies this source.'
    ],
}

errors = []
counts = {'groups':len(groups), 'positive_keywords':sum(len(g['positive_keywords']) for g in groups), 'headlines':sum(len(g['headlines']) for g in groups), 'descriptions':sum(len(g['descriptions']) for g in groups), 'campaign_german_phrase_negatives':len(campaign_negative_de), 'campaign_english_phrase_negatives':len(campaign_negative_en), 'campaign_exact_negatives':len(campaign_negative_exact), 'group_negatives':sum(len(g['negative_keywords']) for g in groups), 'sitelinks':len(sitelinks), 'callouts':len(callouts), 'structured_snippets':len(groups), 'supplied_image_text_pairs':0}
expected = dict(groups=8, positive_keywords=144, headlines=120, descriptions=32, campaign_german_phrase_negatives=136, campaign_english_phrase_negatives=82, campaign_exact_negatives=12, group_negatives=49, sitelinks=8, callouts=6, structured_snippets=8)
for field, value in expected.items():
    if counts[field] != value: errors.append({'type':'count', 'field':field, 'expected':value,'actual':counts[field]})

length_rows=[]
def length_check(scope, field, value, limit):
    length_rows.append({'scope':scope,'field':field,'text':value,'length':len(value),'limit':limit,'pass':len(value)<=limit})
    if len(value)>limit: errors.append(length_rows[-1])

duplicates=[]
casefold_equivalents=[]
conflicts=[]
cross_group_overlaps=[]
positive_owners=collections.defaultdict(list)
def normalized(value):
    return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFC',value).casefold()))
def duplicate_check(scope,items):
    counts=collections.Counter((unicodedata.normalize('NFC',k['text']).strip().lower(),k['match_type']) for k in items)
    for key,count in counts.items():
        if count>1: duplicates.append({'scope':scope,'keyword':key,'count':count})
    normalized_items=collections.defaultdict(list)
    for k in items:normalized_items[(normalized(k['text']),k['match_type'])].append(k['text'])
    for key,variants in normalized_items.items():
        if len(variants)>1 and len(set(variants))>1:casefold_equivalents.append({'scope':scope,'normalized_keyword':key,'source_variants':variants,'note':'Intentional German orthographic variants preserved; Python casefold equates sharp s and ss, which is not proof of Microsoft duplicate handling.'})
def excludes(negative,positive):
    n,p=normalized(negative['text']),normalized(positive['text'])
    return n==p if negative['match_type']=='Exact' else f' {n} ' in f' {p} '

for group in groups:
    number=group['index']
    for field,limit in [('headlines',30),('descriptions',90)]:
        for value in group[field]:length_check(group['name'],field,value,limit)
    for field in ['path_1','path_2']:length_check(group['name'],field,group[field],15)
    for value in group['structured_snippet']['values']:length_check(group['name'],'snippet_value',value,25)
    duplicate_check(f'group_{number}_positives',group['positive_keywords'])
    duplicate_check(f'group_{number}_negatives',group['negative_keywords'])
    for positive in group['positive_keywords']:
        positive_owners[(normalized(positive['text']),positive['match_type'])].append(number)
        for scope,negatives in [('campaign',payload['campaign']['negative_keywords']),('group',group['negative_keywords'])]:
            for negative in negatives:
                if excludes(negative,positive):conflicts.append({'group':number,'scope':scope,'positive':positive,'negative':negative})
    write_text(f'group_{number:02d}_positive_keywords.txt',keyword_block(group['positive_keywords']))
    write_text(f'group_{number:02d}_negative_keywords.txt',keyword_block(group['negative_keywords']))
    write_text(f'group_{number:02d}_rsa.txt','\n'.join([group['name'],group['final_url'],f"Path 1: {group['path_1']}",f"Path 2: {group['path_2']}",'','HEADLINES',*group['headlines'],'','DESCRIPTIONS',*group['descriptions'],'','FINAL URL SUFFIX',group['final_url_suffix']]))
    write_json(f'group_{number:02d}.json',group)
for key,owners in positive_owners.items():
    if len(set(owners))>1:cross_group_overlaps.append({'keyword':key,'groups':owners})
duplicate_check('campaign_negatives',payload['campaign']['negative_keywords'])
for s in sitelinks:
    length_check(s['text'],'sitelink_title',s['text'],25)
    length_check(s['text'],'sitelink_description_1',s['description_1'],35)
    length_check(s['text'],'sitelink_description_2',s['description_2'],35)
for value in callouts:length_check('campaign','callout',value,25)
for edit in optional_copy_edits:length_check(f"optional_group_{edit['group_index']}",edit['field'],edit['suggestion'],30 if edit['field']=='headlines' else 90)

validation = {'result':'PASS_LOCAL_WITH_DOCUMENTED_LIMITATIONS' if not errors and not duplicates and not conflicts else 'FAIL', 'counts':counts, 'errors':errors, 'within_scope_duplicate_keyword_entries':duplicates, 'casefold_equivalent_variants':casefold_equivalents, 'cross_group_duplicate_positive_entries':cross_group_overlaps, 'literal_positive_negative_conflicts':conflicts, 'validation_scope':'Python Unicode length, counts, lowercased exact duplicate detection, casefold/token-normalized literal phrase/exact exclusions; no platform, network or semantic validation.', 'length_checks':length_rows, 'per_group_counts':[{'index':g['index'],'name':g['name'],'positive':len(g['positive_keywords']),'negative':len(g['negative_keywords']),'headlines':len(g['headlines']),'descriptions':len(g['descriptions'])} for g in groups]}
write_json('campaign_payload.json',payload)
write_json('validation.json',validation)
write_text('campaign_negative_keywords.txt',keyword_block(payload['campaign']['negative_keywords']))
write_text('campaign_negative_keywords_phrase.txt',keyword_block(campaign_negative_de+campaign_negative_en))
write_text('campaign_negative_keywords_exact_provisional.txt',keyword_block(campaign_negative_exact))
write_text('callouts.txt','\n'.join(callouts))
write_json('sitelinks.json',sitelinks)
write_json('optional_copy_edits_not_applied.json',optional_copy_edits)
print(json.dumps({'result':validation['result'],'counts':counts,'errors':errors,'duplicates':duplicates,'conflicts':conflicts,'path':str(ROOT)},ensure_ascii=False,indent=2))
assert not errors and not duplicates and not conflicts
