from pathlib import Path
import json, hashlib, sys
from datetime import datetime, timezone

ROOT=Path('/Users/fsuels/Projects/dresslikemommy')
P=Path(__file__).parent
phase=sys.argv[1]
readpath=P/(sys.argv[2] if len(sys.argv)>2 else phase+'-readback.json')
fresh=json.loads(readpath.read_text()); data=fresh['data']
scope=json.loads((P/'scope.json').read_text())
prior=json.loads((ROOT/scope['before_actual527_binding']['path']).read_text())
baseline=json.loads((ROOT/scope['fresh_preparation_readback']['path']).read_text())['data']
target=scope['target']['filename']; bodytarget='assets/theme-inline-body-static-07.css'
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def md5(b):return hashlib.md5(b).hexdigest()
def check(n,v,detail=None):checks.append({'name':n,'pass':bool(v),**({'detail':detail} if detail is not None else {})})
check('scope_hash',sha((P/'scope.json').read_bytes())=='1084a7106666602dda98aff3237a8bd48e9ba5700eeb384c92f001af335a88c9')
for key,v in scope.items():
 if isinstance(v,dict) and 'path' in v and 'sha256' in v:check('bound_'+key,sha((ROOT/v['path']).read_bytes())==v['sha256'])
claim=next(l for l in (ROOT/'ops/AGENT_COORDINATION.md').read_text().splitlines() if l.startswith('| Website UX and PageSpeed audit |'))
check('exact_current_claim',sha(claim.encode())=='f76d9910fef3a882e7cf4f98d85daa0da90325477d1550d760a90e61dc19200a')
before=Path(scope['file']['rollbackPath']).read_bytes();after=Path(scope['file']['candidatePath']).read_bytes()
for which,b in [('before',before),('after',after)]:
 for label,result in [('Sha256',sha(b)),('Md5',md5(b)),('Bytes',len(b))]:check(which+label,result==scope['file'][which+label])
for name,b in [('variables',after),('rollback',before)]:
 v=json.loads((ROOT/scope[name]['path']).read_text())
 check(name+'_exact_one_TEXT_target',v['themeId']=='gid://shopify/OnlineStoreTheme/137888792673' and len(v['files'])==1 and v['files'][0]['filename']==target and v['files'][0]['body']['type']=='TEXT' and v['files'][0]['body']['value'].encode()==b)
for name,count,role,ident in [('current',525,'MAIN',133290917985),('candidate',527,'UNPUBLISHED',137888792673)]:
 obj=data[name];base=baseline[name]
 check(name+'_identity_role',obj['id']==f'gid://shopify/OnlineStoreTheme/{ident}' and obj['role']==role)
 check(name+'_processing_clear',obj['processing'] is False and obj['processingFailed'] is False)
 check(name+'_complete_pages',not obj['inventory']['pageInfo']['hasNextPage'] and not obj['selected']['pageInfo']['hasNextPage'])
 inv={f['filename']:f for f in obj['inventory']['nodes']};bi={f['filename']:f for f in base['inventory']['nodes']}
 check(name+'_unique_complete_inventory',len(inv)==len(obj['inventory']['nodes'])==count and set(inv)==set(bi))
 changed=sorted(k for k in bi if inv.get(k)!=bi[k]);expected=[target] if phase=='after' and name=='candidate' else []
 check(name+'_only_expected_inventory_delta',changed==expected,changed)
 meta=['id','name','role','updatedAt','processing','processingFailed']
 if phase=='after' and name=='candidate':meta.remove('updatedAt')
 check(name+'_protected_metadata',all(obj[k]==base[k] for k in meta))
 selected={f['filename']:f for f in obj['selected']['nodes']};oldsel={f['filename']:f for f in base['selected']['nodes']}
 check(name+'_two_selected_targets',set(selected)=={target,bodytarget} and len(obj['selected']['nodes'])==2)
 for fn in [target,bodytarget]:
  b=selected[fn]['body']['content'].encode();want=after if fn==target and phase=='after' and name=='candidate' else oldsel[fn]['body']['content'].encode()
  check(name+'_'+fn+'_exact',b==want,{'sha256':sha(b),'md5':md5(b),'bytes':len(b)})
  check(name+'_'+fn+'_record_agrees',all(selected[fn][k]==inv[fn][k] for k in ['filename','checksumMd5','size','updatedAt']))
 if name=='candidate':
  bad=[]
  for f in prior['files']:
   b=(ROOT/f['sourcePath']).read_bytes();r=inv.get(f['filename'])
   if sha(b)!=f['sha256'] or md5(b)!=f['md5'] or len(b)!=f['bytes']:bad.append(f['filename']+':prior_source')
   want=after if phase=='after' and f['filename']==target else b
   if not r or r['checksumMd5']!=md5(want) or int(r['size'])!=len(want):bad.append(f['filename']+':live_inventory')
  check('all527_source_bytes_bound',len(prior['files'])==527 and not bad,bad)
if phase=='after':check('candidate_saved_timestamp_advanced',data['candidate']['updatedAt']>baseline['candidate']['updatedAt'])
receipt={'phase':phase,'checkedAtUtc':datetime.now(timezone.utc).isoformat(),'readbackPath':str(readpath.relative_to(ROOT)),'readbackSha256':sha(readpath.read_bytes()),'receivedAtUtc':fresh['receivedAtUtc'],'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks)}
(P/('AFTER_GUARDS.json' if phase=='after' else 'PREWRITE_GUARDS.json')).write_text(json.dumps(receipt,indent=2)+'\n')
if phase=='after' and not receipt['failed']:
 source=P/'source'/target;source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(data['candidate']['selected']['nodes'][next(i for i,f in enumerate(data['candidate']['selected']['nodes']) if f['filename']==target)]['body']['content'].encode())
 files=[]
 for f in prior['files']:
  r=dict(f)
  if r['filename']==target:r.update(sourcePath=str(source.relative_to(ROOT)),sha256=sha(source.read_bytes()),md5=md5(source.read_bytes()),bytes=len(source.read_bytes()),source='ACTUAL critical head CSS read back after exact single save')
  files.append(r)
 actual={'status':'ACTUAL_AFTER_READBACK_VERIFIED','observedAt':fresh['receivedAtUtc'],'candidateId':137888792673,'candidateName':data['candidate']['name'],'role':data['candidate']['role'],'savedAt':data['candidate']['updatedAt'],'mainId':133290917985,'main525FilesAndMetadataPreserved':True,'totalFiles':527,'preservedPriorFiles':526,'successorFiles':[target],'parentBindingSha256':scope['before_actual527_binding']['sha256'],'finalModuleSha256':prior['finalModuleSha256'],'files':files,'afterReadback':{'path':str(readpath.relative_to(ROOT)),'sha256':sha(readpath.read_bytes())},'publication':'HOLD pending actual critical CSS browser acceptance; candidate save only','retainedAcceptance':prior['retainedAcceptance']}
 (P/'ACTUAL_527_SOURCE_BINDING.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'phase':phase,'passed':receipt['passed'],'failed':receipt['failed'],'failedChecks':[c for c in checks if not c['pass']]}))
sys.exit(bool(receipt['failed']))
