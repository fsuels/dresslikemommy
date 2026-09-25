import json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv={}
for p in sorted((B/'articles/raw').glob('inventory_*.json')):
 for r in json.loads(p.read_text())['data']['articles']['nodes']:
  if r['isPublished']: inv[r['id']]=r
rows=[]
for p in sorted((B/'articles/raw').glob('translations_*.json')):
 a=json.loads(p.read_text());locale=a['variables']['locale']
 for n in a['data']['translatableResourcesByIds']['nodes']:
  if n['resourceId'] not in inv: continue
  s=next(s for s in n['translatableContent'] if s['key']=='title')
  before=[t for t in n['translations'] if t['key']=='title' and t['locale']==locale and not t.get('market')]
  assert len(before)<=1
  rows.append({'resourceId':n['resourceId'],'locale':locale,'key':'title','source':s['value'],'sourceDigest':s['digest'],'before':before[0] if before else None,'effectiveValue':before[0]['value'] if before else None,'rawFile':str(p.relative_to(B)),'rawFileSHA256':sha(p),'handle':inv[n['resourceId']]['handle'],'selectedCandidates':[],'appliedReceipts':[]})
assert len(inv)==67 and len(rows)==1340
bykey={(r['resourceId'],r['locale']):r for r in rows}
selected=['articles/short_fields_candidate_01.json','articles/short_fields_candidate_02.json','root-bodies/he-pl/remaining-review/short_candidates.json','review/root_article_short3.json']
for rel in selected:
 p=B/rel;a=json.loads(p.read_text())
 for c in a['rows']:
  if c['key']!='title':continue
  k=(c['resourceId'],c['locale'])
  if k not in bykey:continue
  r=bykey[k];assert c.get('sourceValue',c.get('source'))==r['source'] and c['sourceDigest']==r['sourceDigest']
  r['selectedCandidates'].append({'file':rel,'fileSHA256':sha(p),'value':c['value']});r['effectiveValue']=c['value']
for p in sorted((B/'releases').glob('*.json')):
 if p.name.endswith('_intent.json'):continue
 a=json.loads(p.read_text())
 if 'mutation' not in a or 'resourceIds' not in a: continue
 for i,rid in enumerate(a['resourceIds']):
  if '/Article/' not in rid: continue
  m=a['mutation'].get('r'+str(i))
  if not m or m.get('userErrors'): continue
  for t in m.get('translations',[]):
   if t['key']!='title':continue
   k=(rid,t['locale'])
   if k not in bykey:continue
   r=bykey[k];r['appliedReceipts'].append({'file':str(p.relative_to(B)),'fileSHA256':sha(p),'translation':t});r['effectiveValue']=t['value']
p=B/'articles/short_fields_01_receipts.json'
for a in json.loads(p.read_text()):
 m=a['result']['data']['translationsRegister'];assert not m['userErrors']
 for t in m['translations']:
  if t['key']!='title':continue
  r=bykey[(a['resourceId'],t['locale'])];r['appliedReceipts'].append({'file':str(p.relative_to(B)),'fileSHA256':sha(p),'translation':t});r['effectiveValue']=t['value']
p=B/'review/article_titles_applied_root_overlay.json'
for c in json.loads(p.read_text()):
 r=bykey[(c['resourceId'],c['locale'])]
 assert c.get('sourceValue',c.get('source'))==r['source'] and c['sourceDigest']==r['sourceDigest']
 r['rootAppliedOverlay']={'file':str(p.relative_to(B)),'fileSHA256':sha(p),'value':c['value']}
 r['effectiveValue']=c['value']
rows.sort(key=lambda r:(r['locale'],list(inv).index(r['resourceId'])))
for i,r in enumerate(rows):r['auditId']=i
(H/'inventory.json').write_text(json.dumps({'status':'FROZEN_RAW_WITH_SELECTED_AND_SUCCESSFUL_RECEIPT_OVERLAY','publishedArticles':67,'locales':sorted({r['locale'] for r in rows}),'rows':rows},ensure_ascii=False,indent=2)+'\n')
print({'rows':len(rows),'selectedTitleRows':sum(bool(r['selectedCandidates']) for r in rows),'receiptTitleRows':sum(bool(r['appliedReceipts']) for r in rows)})
for r in rows:
 if r['locale']=='de':print(r['auditId'],r['source'],'=>',r['effectiveValue'])
