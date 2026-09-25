#!/usr/bin/env python3
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'));import offline_translation as ot
review=json.loads((HERE/'sv-bodies/blue_daisy_independent_review.json').read_text());fixes={(r['resourceId'],r['locale']):r for r in review['rows']}
checks=[];manifest=[]
for group in 'abc':
 oldname=f'blue_daisy_{group}_candidate.json';f=HERE/oldname
 assert hashlib.sha256(f.read_bytes()).hexdigest()==next(r['sha256'] for r in review['files'] if r['path']==oldname)
 d=json.loads(f.read_text())
 for r in d['rows']:
  old=r['value'];fix=fixes[(r['resourceId'],r['locale'])];assert hashlib.sha256(old.encode()).hexdigest()==fix['candidateValueSHA256']
  v=old
  for patch in fix['exactTextReplacements']:
   assert v.count(patch['beforeText'])==patch['expectedOccurrences'];v=v.replace(patch['beforeText'],patch['value'])
  assert 'up to' not in v
  assert ot.Shape(old).events==ot.Shape(v).events
  assert ot.table_facts(ot.Shape(old),r['locale'])==ot.table_facts(ot.Shape(v),r['locale'])
  r['value']=v;r['reviewRepair']={'reviewPath':'sv-bodies/blue_daisy_independent_review.json','exactTableTextPatches':fix['exactTextReplacements'],'measurementValuesAndUnitAbbreviationsUnchanged':True}
  checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'exactRequestedTextReplacements':True,'oldToV2HtmlAttributesTableNumbersAndUnitsIdentical':True,'sourceCheck':ot.verify_text(r['source'],v,r['locale']),'inheritedUnitOrSpelledAgeParserLimit':fix['normalizationExplanation']})
 d['supersedes']={'path':oldname,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'reason':'Independent reviewer found two measurement-limit words still English; v2 localizes those words only.'}
 out=HERE/f'blue_daisy_{group}_candidate_v2.json';out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');manifest.append({'path':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'fields':len(d['rows']),'rollbackPath':f'blue_daisy_{group}_rollback.json'})
(HERE/'blue_daisy_v2_checks.json').write_text(json.dumps({'rows':checks,'files':manifest,'status':'EXACT_REPAIR_APPLIED_PENDING_INDEPENDENT_REREVIEW'},ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest))
