from pathlib import Path
import json, hashlib, sys
from datetime import datetime, timezone
ROOT=Path('/Users/fsuels/Projects/dresslikemommy')
PACKET=Path(__file__).parent
phase=sys.argv[1]
readpath=PACKET/(sys.argv[2] if len(sys.argv)>2 else ('before-readback.json' if phase=='before' else 'after-readback.json'))
fresh=json.loads(readpath.read_text()); data=fresh['data']
scope=json.loads((PACKET/'scope.json').read_text()); target=scope['target']['filename']
prior=json.loads((ROOT/scope['before_full_source_binding']['path']).read_text())
baseline=json.loads((ROOT/prior['afterReadback']['path']).read_text())['data']
checks=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def md5(b): return hashlib.md5(b).hexdigest()
def check(name,ok,detail=None): checks.append({'name':name,'pass':bool(ok),**({'detail':detail} if detail is not None else {})})
check('scope_sha',sha((PACKET/'scope.json').read_bytes())=='ac78a5e36449fd49bb956c93deb248ca24ad42b9971c6bee32c274f0fd82098d')
for key,v in scope.items():
 if isinstance(v,dict) and 'path' in v and 'sha256' in v: check('frozen_'+key,sha((ROOT/v['path']).read_bytes())==v['sha256'])
claim=next(l for l in (ROOT/'ops/AGENT_COORDINATION.md').read_text().splitlines() if l.startswith('| Website UX and PageSpeed audit |'))
check('current_exact_claim',sha(claim.encode())=='5394bed4a599e611da1623126e10ad7353edabc5c08807bde507a7bc3824253e')
before=Path(scope['exact_change']['rollbackPath']).read_bytes(); after=Path(scope['exact_change']['candidatePath']).read_bytes()
for which,body in [('before',before),('after',after)]:
 for label,result in [('Sha256',sha(body)),('Md5',md5(body)),('Bytes',len(body))]:check(which+'_'+label,result==scope['exact_change'][which+label])
variables=json.loads((ROOT/scope['variables']['path']).read_text()); inverse=json.loads((ROOT/scope['rollback']['path']).read_text())
for name,var,body in [('forward',variables,after),('inverse',inverse,before)]:
 check(name+'_one_exact_text_file',var['themeId']=='gid://shopify/OnlineStoreTheme/137888792673' and len(var['files'])==1 and var['files'][0]['filename']==target and var['files'][0]['body']['type']=='TEXT' and var['files'][0]['body']['value'].encode()==body)
for name,count,role,idpart in [('current',525,'MAIN','133290917985'),('candidate',527,'UNPUBLISHED','137888792673')]:
 obj=data[name]; base=baseline[name]
 check(name+'_identity_role_name',obj['id']=='gid://shopify/OnlineStoreTheme/'+idpart and obj['role']==role and obj['name']==base['name'])
 check(name+'_not_processing',obj['processing'] is False and obj['processingFailed'] is False)
 check(name+'_complete_pages',not obj['inventory']['pageInfo']['hasNextPage'] and not obj['selected']['pageInfo']['hasNextPage'])
 inv={f['filename']:f for f in obj['inventory']['nodes']}; bi={f['filename']:f for f in base['inventory']['nodes']}
 check(name+'_complete_unique_inventory',len(inv)==count and len(obj['inventory']['nodes'])==count and set(inv)==set(bi))
 changed=sorted(k for k in bi if inv.get(k)!=bi[k]); expected=[] if phase=='before' or name=='current' else [target]
 check(name+'_preserved_records',changed==expected,{'changed':changed})
 meta=['id','name','role','updatedAt','processing','processingFailed']
 if phase=='after' and name=='candidate':meta.remove('updatedAt')
 check(name+'_preserved_metadata',all(obj[k]==base[k] for k in meta))
 nodes=obj['selected']['nodes']; check(name+'_selected_one_target',len(nodes)==1 and nodes[0]['filename']==target)
 body=nodes[0]['body']['content'].encode(); required=after if phase=='after' and name=='candidate' else before
 check(name+'_target_exact_body',body==required,{'sha256':sha(body),'md5':md5(body),'bytes':len(body)})
 check(name+'_selected_inventory_agree',all(nodes[0][k]==inv[target][k] for k in ['filename','checksumMd5','size','updatedAt']))
 if name=='candidate':
  mismatches=[]
  for f in prior['files']:
   raw=(ROOT/f['sourcePath']).read_bytes(); rec=inv.get(f['filename'])
   if sha(raw)!=f['sha256'] or md5(raw)!=f['md5'] or len(raw)!=f['bytes']:mismatches.append(f['filename']+': prior source')
   expected_body=after if phase=='after' and f['filename']==target else raw
   if rec is None or rec['checksumMd5']!=md5(expected_body) or int(rec['size'])!=len(expected_body):mismatches.append(f['filename']+': inventory')
  check('all_527_sources_and_records_bound',len(prior['files'])==527 and not mismatches,{'mismatches':mismatches})
if phase=='after':check('candidate_saved_timestamp_increased',data['candidate']['updatedAt']>baseline['candidate']['updatedAt'])
receipt={'phase':phase,'checkedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceReadback':str(readpath.relative_to(ROOT)),'sourceSha256':sha(readpath.read_bytes()),'sourceReceivedAtUtc':fresh['receivedAtUtc'],'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks)}
out=PACKET/('ACTION_TIME_GUARDS.json' if phase=='before' else 'AFTER_GUARDS.json');out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
if phase=='after' and not receipt['failed']:
 source=PACKET/'source'/target;source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(data['candidate']['selected']['nodes'][0]['body']['content'].encode())
 files=[]
 for f in prior['files']:
  record=dict(f)
  if f['filename']==target:record.update({'sourcePath':str(source.relative_to(ROOT)),'sha256':sha(source.read_bytes()),'md5':md5(source.read_bytes()),'bytes':len(source.read_bytes()),'source':'ACTUAL mobile-heading CSS read back after exact one-file save'})
  files.append(record)
 actual={'status':'ACTUAL_AFTER_READBACK_VERIFIED','observedAt':fresh['receivedAtUtc'],'candidateId':137888792673,'candidateName':data['candidate']['name'],'role':data['candidate']['role'],'savedAt':data['candidate']['updatedAt'],'mainId':133290917985,'main525FilesAndMetadataPreserved':True,'totalFiles':527,'preservedPriorFiles':526,'successorFiles':[target],'parentBindingSha256':scope['before_full_source_binding']['sha256'],'finalModuleSha256':prior['finalModuleSha256'],'files':files,'afterReadback':{'path':str(readpath.relative_to(ROOT)),'sha256':sha(readpath.read_bytes())},'publication':'HOLD pending actual browser/cold-load acceptance; UNPUBLISHED save only','retainedAcceptance':scope['retained_acceptance']}
 (PACKET/'ACTUAL_527_SOURCE_BINDING.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':receipt['passed'],'failed':receipt['failed'],'failedChecks':[c for c in checks if not c['pass']],'sourceReceivedAtUtc':fresh['receivedAtUtc']}))
sys.exit(bool(receipt['failed']))
