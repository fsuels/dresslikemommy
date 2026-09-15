"""Build only the three approved sizing paragraph replacements from guarded bodies."""
from pathlib import Path
import hashlib, html, json, re
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
REPO = P.parents[3]
O = REPO / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-organic-growth/daily-operation-20260914/sizing-localization-20260914'
def read(path): return json.loads(path.read_text())
def sha(value): return hashlib.sha256(value.encode()).hexdigest()
inv = read(P/'inventory-before.json')['data']
answers = read(P/'answers.json')
routes = read(O/'ROUTES.json')
routes['en'] = {'article': read(O/'EXECUTION_HANDOFF.json')['target']['url']}
organic_manifest = read(O/'SOURCE_MANIFEST.json')
for name in ['EXECUTION_HANDOFF.json','FINAL_READBACK.json','ROUTES.json','PUBLIC_VERIFICATION.json']:
    assert hashlib.sha256((O/name).read_bytes()).hexdigest() == organic_manifest['files'][name], name
guide = read(P/'guide-source-before.json')['data']
assert guide['article']['id'] == 'gid://shopify/Article/559700574305'
assert guide['article']['isPublished'] is True
assert sha(guide['article']['body']) == 'c1c3ca1fa58097d25857d12fb361f82ac60ae7d45f5545a717ca9a6ab04aea88'
assert sha(inv['page']['body']) == 'c2797437bb4ec0296fbbc5b9ac85f4ea7a4275e7cfd00e5ddf8c5e6ce5dfe0ff'
assert inv['page']['id'] == 'gid://shopify/Page/161933381'
assert inv['page']['isPublished'] is True
assert not inv['markets']['pageInfo']['hasNextPage']
assert all(not x['webPresences']['pageInfo']['hasNextPage'] for x in inv['markets']['nodes'])
before_global = read(P/'translations-before-global.json')['data']['translatableResource']
records = [r for k, rows in before_global.items() if k.startswith('t_') for r in rows]
body_records = {r['locale']: r for r in records if r['key']=='body_html'}
assert set(answers) == {'en'} | set(body_records)
assert len(body_records) == 17
assert len(records) == 36
for loc in body_records:
    actual = next(r for r in guide['translatableResource']['t_'+loc.replace('-','_')] if r['key']=='body_html')
    assert actual['value'].encode() == (O/'locales'/loc/'candidate.html').read_bytes(), loc
    assert actual['outdated'] is False, loc
(P/'candidates').mkdir(exist_ok=True)
(P/'diffs').mkdir(exist_ok=True)
manifest = {
 'schema':'dlm.faq_sizing_truth_candidates.v1',
 'built_at_utc':datetime.now(timezone.utc).isoformat(),
 'action_id':'TA06-FAQ-SIZING-TRUTH-20260914',
 'page_id':inv['page']['id'],
 'source_body_sha256':sha(inv['page']['body']),
 'question_labels_changed':0,
 'per_body_replaced_paragraphs':3,
 'native_disclosure_controls_per_body':8,
 'guide_source_manifest_sha256':hashlib.sha256((O/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
 'guide_routes_source':str(O/'ROUTES.json'),
 'protected_page_fields':{k:v for k,v in inv['page'].items() if k not in ['body','updatedAt']},
 'protected_translatable_source':[x for x in inv['translatableResource']['translatableContent'] if x['key']!='body_html'],
 'qualified':[],
 'market_scope_reads':[{'scope':read(x)['scope'],'file':x.name} for x in sorted(P.glob('translations-before-*.json'))],
 'limits':['Three repaired answers only; other legacy business and policy wording is unreviewed.','No missing translations are created; pl/ru/sv retain English body fallback.','Existing FAQ ar/he LTR layout is preserved; no full RTL claim.','Native-language human review has not been performed.']
}
detail_re = re.compile(r'<details\b[^>]*>[\s\S]*?</details>')
p_re = re.compile(r'<p\b[^>]*>[\s\S]*?</p>')
for loc, parts in answers.items():
    before = (P/'before'/f'{loc}.html').read_bytes().decode()
    assert before == (inv['page']['body'] if loc=='en' else body_records[loc]['value'])
    assert len(parts)==4 and parts[0].count('{guide}')==1
    link = '<a href="'+html.escape(routes[loc]['article'],quote=True)+'">'+html.escape(parts[1])+'</a>'
    replacement = [html.escape(parts[0]).replace('{guide}',link),html.escape(parts[2]),html.escape(parts[3])]
    details=list(detail_re.finditer(before))
    assert len(details)==8,loc
    edits=[]
    for index,(section,paragraph) in enumerate([(1,1),(1,4),(7,1)]):
        d=details[section]
        paragraphs=list(p_re.finditer(d.group()))
        item=paragraphs[paragraph]
        previous=paragraphs[paragraph-1].group()
        assert '<strong>' in previous and '</strong>' in previous,(loc,section,paragraph)
        assert not '<strong>' in item.group(),(loc,section,paragraph)
        start,end=d.start()+item.start(),d.start()+item.end()
        new='<p>'+replacement[index]+'</p>'
        edits.append({'start':start,'end':end,'before':item.group(),'after':new,'question_html':previous,'section_index':section,'paragraph_index':paragraph})
    candidate=before
    for e in reversed(edits): candidate=candidate[:e['start']]+e['after']+candidate[e['end']:]
    # Reconstruct both bodies with approved paragraphs removed, proving all other bytes are retained.
    original_mask=before
    for e in reversed(edits): original_mask=original_mask[:e['start']]+'<APPROVED_SIZING_PARAGRAPH>'+original_mask[e['end']:]
    candidate_mask=candidate
    for e in edits:
        assert candidate_mask.count(e['after'])==1,(loc,'ambiguous candidate paragraph')
        candidate_mask=candidate_mask.replace(e['after'],'<APPROVED_SIZING_PARAGRAPH>',1)
    assert original_mask==candidate_mask,(loc,'unrelated-byte drift')
    assert re.findall(r'<summary[\s\S]*?</summary>',before)==re.findall(r'<summary[\s\S]*?</summary>',candidate)
    assert candidate.count('<details')==8 and candidate.count('<summary')==8
    assert candidate.count('<script')==0 and 'onclick=' not in candidate
    assert len(re.findall(r'href=',candidate))==len(re.findall(r'href=',before)),loc
    (P/'candidates'/f'{loc}.html').write_bytes(candidate.encode())
    (P/'diffs'/f'{loc}.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    manifest['qualified'].append({'locale':loc,'marketId':None,'key':'body' if loc=='en' else 'body_html','before_path':f'before/{loc}.html','candidate_path':f'candidates/{loc}.html','before_sha256':sha(before),'candidate_sha256':sha(candidate),'unchanged_content_sha256':sha(original_mask),'guide_url':routes[loc]['article'],'edits_path':f'diffs/{loc}.json'})
(P/'release-source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','bodies':len(manifest['qualified']),'exact_paragraph_changes':54,'unchanged_controls':144,'unchanged_question_labels':True,'other_content_exact':True,'global_translation_records':len(records),'protected_titles':len(records)-17},indent=2))
