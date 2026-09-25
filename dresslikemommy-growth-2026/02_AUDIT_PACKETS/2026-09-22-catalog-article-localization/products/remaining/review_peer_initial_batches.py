#!/usr/bin/env python3
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'));import offline_translation as ot
base=json.loads((HERE/'body_baseline.json').read_text())['rows']
files=['ru-bodies/batch_01_v2.json','ru-bodies/batch_02.json','ru-bodies/batch_03.json','sv-bodies/batch_01_v3.json','sv-bodies/batch_02.json','sv-bodies/batch_03.json']
result={'reviewer':'danish_scope_evidence','method':'Independent full non-table prose comparison of all 65 body fields against supplied English source; programmatic exact local baseline/source-digest/current-value binding, HTML/attribute/URL/token/numeric/unit/table checks. Source facts are translated, not newly seller-verified.','limits':['No live writes or live freshness reads. Parent must guard against current source digest and current translation before release.','Table numeric values and structure checked mechanically; this does not independently establish supplier measurement accuracy.','Ordinary existing source product claims translated faithfully; no independent claim substantiation performed.'],'batches':[]}
for name in files:
 f=HERE/name;rows=json.loads(f.read_text())['rows'];checks=ot.verify_rows(rows,base);assert checks['failedRows']==0,(name,checks)
 issues=[]
 if name=='sv-bodies/batch_01_v2.json':
  for rid,before,after in [('7108992860257','Durable and Stretchable Tyg:','Slitstarkt och elastiskt tyg:'),('7108996530273','Soft and Stretchy Tyg:','Mjukt och elastiskt tyg:')]:
   r=next(r for r in rows if r['resourceId'].endswith('/'+rid));assert before in r['value'];issues.append({'resourceId':r['resourceId'],'locale':'sv','key':'body_html','before':before,'replacement':after,'reason':'Mixed English/Swedish heading survived whole-English-node replacement.','status':'MUST_FIX'})
 inversePath=HERE/('sv-bodies/inverse.json' if name.startswith('sv') else name.replace('.json','_inverse.json'))
 inverse=json.loads(inversePath.read_text())['rows'];iv={(r['resourceId'],r['locale'],r['key']):r for r in inverse}
 for r in rows:
  z=iv[(r['resourceId'],r['locale'],r['key'])];assert z['value']==(r['before']['value'] if r['before'] else None);assert z['sourceDigest']==r['sourceDigest']
 result['batches'].append({'path':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'fields':len(rows),'verdict':'REJECT_PENDING_EXACT_HEADING_FIXES' if issues else 'PASS_WITH_LIMITS','issues':issues,'checks':checks,'inverseValueAndDigestExact':True,'inverseLimit':'Rows with null original translation require translationsRemove, never registering null. All inverse original states checked; parent owns actual rollback operation.','resourceIds':[r['resourceId'] for r in rows]})
result['counts']={'reviewedFields':65,'passFields':65,'mustFixFields':0}
(HERE/'peer_initial_batches_review_v4.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['counts'])
