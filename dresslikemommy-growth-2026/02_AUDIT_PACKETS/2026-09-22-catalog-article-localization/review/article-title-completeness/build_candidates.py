import json,hashlib,sys
from pathlib import Path
H=Path(__file__).resolve().parent
inv=json.loads((H/'inventory.json').read_text());byid={r['auditId']:r for r in inv['rows']}
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
rows=[]
for line in (H/'manual_corrections.tsv').read_text().splitlines():
 if not line:continue
 i,value=line.split('\t',1);r=byid[int(i)]
 assert value and value!=r['effectiveValue']
 before=r['before'];prov={'rawFile':r['rawFile'],'rawFileSHA256':r['rawFileSHA256']}
 if r.get('rootAppliedOverlay'):
  before={'key':'title','locale':r['locale'],'market':None,'outdated':False,'value':r['effectiveValue']};prov=r['rootAppliedOverlay']
 elif r['appliedReceipts']:
  t=r['appliedReceipts'][-1];before={'key':'title','locale':r['locale'],'market':None,'outdated':False,'value':t['translation']['value']};prov=t
 elif r['selectedCandidates']:
  raise AssertionError('Pending selected title requires root reconciliation '+str(i))
 rows.append({'auditId':int(i),'resourceId':r['resourceId'],'locale':r['locale'],'key':'title','marketId':None,'handle':r['handle'],'source':r['source'],'sourceValue':r['source'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['source']),'before':before,'expectedBeforeValueSHA256':sha(before['value']) if before else None,'rawBefore':r['before'],'rawFile':r['rawFile'],'rawFileSHA256':r['rawFileSHA256'],'effectiveBeforeProvenance':prov,'value':value,'valueSHA256':sha(value),'reason':'Full current-source manual title review: correct demonstrated mixed English, semantic mistranslation, omitted title meaning or corrupted wording; preserve entire title meaning and established brand/holiday terms.','reviewStatus':'AUTHOR_PENDING_INDEPENDENT_MEANING_REVIEW','requiresFreshLiveSourceAndBeforeGuard':True})
assert len(rows)==len({(r['resourceId'],r['locale']) for r in rows})
name=sys.argv[1] if len(sys.argv)>1 else 'candidates.json'
(H/name).write_text(json.dumps({'status':'MANUALLY_AUTHORED_OFFLINE_PENDING_INDEPENDENT_REVIEW','inventoryFileSHA256':hashlib.sha256((H/'inventory.json').read_bytes()).hexdigest(),'rows':rows},ensure_ascii=False,indent=2)+'\n')
print(name,len(rows),hashlib.sha256((H/name).read_bytes()).hexdigest())
