"""Build exact local FAQ release and rollback artifacts; no network or Git writes."""
from pathlib import Path
import json
import re
import hashlib
import difflib

P = Path(__file__).resolve().parent
FROZEN = P.parent / 'faq-inline-jquery-20260914'
PAGE = 'gid://shopify/Page/161933381'
EXPECTED_BEFORE = '3ef790830a524e2b2f03585b218d4d679bb97d4bc88554e937b32da6bdebb943'
EXPECTED_AFTER = 'c2797437bb4ec0296fbbc5b9ac85f4ea7a4275e7cfd00e5ddf8c5e6ce5dfe0ff'

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def write_json(name, obj):
    (P / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

inventory = json.loads((P / 'inventory-before.json').read_text())['data']
assert inventory['shop']['id'] == 'gid://shopify/Shop/15571635'
assert inventory['page']['id'] == PAGE and inventory['page']['handle'] == 'faqs'
assert not inventory['markets']['pageInfo']['hasNextPage']
assert all(not m['webPresences']['pageInfo']['hasNextPage'] for m in inventory['markets']['nodes'])
before_en = inventory['page']['body']
after_en = (FROZEN / 'page-proposed.html').read_bytes().decode()
assert sha(before_en) == EXPECTED_BEFORE and sha(after_en) == EXPECTED_AFTER
source_fields = inventory['translatableResource']['translatableContent']
assert next(x['digest'] for x in source_fields if x['key'] == 'body_html') == EXPECTED_BEFORE
style = re.search(r'<style>.*?</style>', after_en, re.S).group()
legacy_scripts = re.findall(r'<script>.*?</script>', before_en, re.S)
expected_handler = re.search(r'onclick="([^"]*)"', before_en).group(1)
pattern = re.compile(r'<div class="question-answer-block">\s*(<h3>\s*)<a class="ask" onclick="([^"]*)">([^<]+)</a>(\s*</h3>)\s*<div class="answer" style="display: none; font-size: 16px;">(.*?)</div>\s*</div>', re.S)

def transform(source):
    scripts = re.findall(r'<script>.*?</script>', source, re.S)
    # Script contents may have different line endings; substantive code must match.
    assert [s.replace('\r\n','\n') for s in scripts] == [s.replace('\r\n','\n') for s in legacy_scripts]
    stripped = re.sub(r'<script>.*?</script>', '', source, flags=re.S)
    matches = list(pattern.finditer(stripped))
    assert len(matches) == 8 and all(m.group(2) == expected_handler for m in matches)
    def disclosure(m):
        h3start, _, label, h3end, answer = m.groups()
        return ('<details class="question-answer-block" name="dlm-faq">\n'
                f'<summary class="ask">{h3start}{label}{h3end}</summary>\n'
                f'<div class="answer" style="font-size: 16px;">{answer}</div>\n</details>')
    out = pattern.sub(disclosure, stripped)
    assert out.count('<div id="page-content">') == 1
    out = out.replace('<div id="page-content">', '<div id="page-content">\n' + style, 1)
    assert not re.search(r'<script|onclick=|jQuery|display: none;', out)
    answers_before = [m.group(5) for m in matches]
    answers_after = re.findall(r'<div class="answer" style="font-size: 16px;">(.*?)</div>', out, re.S)
    assert answers_before == answers_after
    anchors = lambda x: re.findall(r'<a\b[^>]*href=[^>]*>.*?</a>', x, re.S)
    assert anchors(source) == anchors(out)
    ids = lambda x: re.findall(r'\bid="([^"]*)"', x)
    assert ids(source) == ids(out)
    return out, [m.group(3) for m in matches], [sha(x) for x in answers_before], len(anchors(source))

for d in ['before', 'candidates', 'diffs']:
    (P / d).mkdir(exist_ok=True)
(P / 'before/en.html').write_bytes(before_en.encode())
(P / 'candidates/en.html').write_bytes(after_en.encode())
qualified = []
unqualified = []
missing = []
translation_records = []
scope_reads = []
for path in sorted(P.glob('translations-before-*.json')):
    read = json.loads(path.read_text())
    scope_reads.append({'scope': read['scope'], 'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    resource = read['data']['translatableResource']
    assert resource['resourceId'] == PAGE
    for locale in inventory['shopLocales']:
        records = resource['t_' + locale['locale'].replace('-', '_')]
        for t in records:
            assert t['locale'] == locale['locale'] and (t['market'] or {}).get('id') == read['scope']['id']
            translation_records.append(t)
        bodies = [t for t in records if t['key'] == 'body_html']
        assert len(bodies) <= 1
        if not bodies:
            missing.append({'locale': locale['locale'], 'marketId': read['scope']['id'], 'primary': locale['primary'], 'other_keys': [t['key'] for t in records]})
            continue
        t = bodies[0]
        key = locale['locale'] + ('__' + read['scope']['id'].split('/')[-1] if read['scope']['id'] else '')
        (P / f'before/{key}.html').write_bytes(t['value'].encode())
        try:
            out, labels, answer_hashes, links = transform(t['value'])
        except AssertionError:
            unqualified.append({'locale': t['locale'], 'marketId': read['scope']['id'], 'before_sha256': sha(t['value']), 'reason': 'Source structure or legacy script does not exactly qualify; no candidate/update.'})
            continue
        (P / f'candidates/{key}.html').write_bytes(out.encode())
        (P / f'diffs/{key}.patch').write_text(''.join(difflib.unified_diff(t['value'].splitlines(True), out.splitlines(True), fromfile=f'{key}.before', tofile=f'{key}.candidate')))
        qualified.append({'locale': t['locale'], 'marketId': read['scope']['id'], 'key': 'body_html', 'source_path': f'before/{key}.html', 'candidate_path': f'candidates/{key}.html', 'before_sha256': sha(t['value']), 'candidate_sha256': sha(out), 'source_digest_before': EXPECTED_BEFORE, 'required_source_digest_at_registration': EXPECTED_AFTER, 'before_outdated': t['outdated'], 'before_updatedAt': t['updatedAt'], 'labels': labels, 'answer_fragment_sha256': answer_hashes, 'links': links, 'preservation': 'Exact eight answer HTML fragments, labels, href anchors and IDs; no business wording changes.'})

page_vars = {'id': PAGE, 'page': {'body': after_en}}
translations_vars = {'resourceId': PAGE, 'translations': []}
rollback_translations = {'resourceId': PAGE, 'translations': []}
for item in qualified:
    t = {'locale': item['locale'], 'key': 'body_html', 'value': (P / item['candidate_path']).read_bytes().decode(), 'translatableContentDigest': EXPECTED_AFTER}
    rollback = {**t, 'value': (P / item['source_path']).read_bytes().decode()}
    if item['marketId']:
        t['marketId'] = rollback['marketId'] = item['marketId']
    translations_vars['translations'].append(t)
    rollback_translations['translations'].append(rollback)
write_json('page-update.variables.json', page_vars)
write_json('translations-register.variables.expected.json', translations_vars)
write_json('rollback-page.variables.json', {'id': PAGE, 'page': {'body': before_en}})
write_json('rollback-translations.variables.expected.json', rollback_translations)
manifest = {'action': 'TA06-FAQ-NATIVE-DISCLOSURE-RELEASE-20260914', 'shop': inventory['shop'], 'page_id': PAGE, 'english_before_sha256': EXPECTED_BEFORE, 'english_candidate_sha256': EXPECTED_AFTER, 'enabled_locales': [l['locale'] for l in inventory['shopLocales']], 'market_scope_reads': scope_reads, 'translation_records_total': len(translation_records), 'qualified': qualified, 'unqualified': unqualified, 'missing_body_records': missing, 'protected_page_fields': {k:v for k,v in inventory['page'].items() if k not in ['body','updatedAt']}, 'protected_translatable_source': [x for x in source_fields if x['key'] != 'body_html'], 'protected_translation_records': [t for t in translation_records if t['key'] != 'body_html'], 'expected_metadata_changes': ['Page updatedAt and derived bodySummary; body source value/digest', 'Registered existing body translations updatedAt and outdated=false. Before outdated=true is not semantic correctness; all wording remains unreviewed.'], 'rollback_order': ['Read exact current source/translation values; do not overwrite drift.', 'If translated repairs applied, restore only changed exact prior translation values under the freshly read current body digest while guard equals expected candidate.', 'Restore English before body only under guard equals expected candidate; its source change makes restored translation staleness flags outdated again.', 'Read all protected fields/identities and buyer behavior.'], 'no_new_records': True, 'english_operation_input_keys': ['id','page.body'], 'translation_operation_input_keys': ['resourceId','translations.locale','translations.key','translations.value','translations.translatableContentDigest','optional translations.marketId'], 'release_status': 'PREPARED_FOR_INDEPENDENT_REVIEW'}
write_json('release-source-manifest.json', manifest)
print(json.dumps({'qualified_locales': [x['locale'] for x in qualified], 'unqualified': unqualified, 'global_missing': [m for m in missing if not m['marketId']], 'translation_records_total':len(translation_records)}, ensure_ascii=False, indent=2))
