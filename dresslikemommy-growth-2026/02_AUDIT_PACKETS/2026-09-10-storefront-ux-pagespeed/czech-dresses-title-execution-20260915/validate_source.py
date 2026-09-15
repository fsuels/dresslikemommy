from pathlib import Path
import json,hashlib,sys,re
from datetime import datetime, timezone
ROOT=Path('/Users/fsuels/Projects/dresslikemommy')
PACKET=Path(__file__).parent
PREP=ROOT/'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/czech-dresses-title-successor-20260915'
SCOPE=ROOT/'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/theme_czech_heading_scope_20260915.json'
phase=sys.argv[1]
fresh_path=PACKET/(sys.argv[2] if len(sys.argv)>2 else ('action-time-readback.json' if phase=='before' else 'after-readback.json'))
fresh=json.loads(fresh_path.read_text())
data=fresh['data']
baseline=json.loads((PREP/'fresh-source-readback.json').read_text())['data']
scope=json.loads(SCOPE.read_text())
checks=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),**({'detail':detail} if detail is not None else {})})
def sha(b): return hashlib.sha256(b).hexdigest()
def md5(b): return hashlib.md5(b).hexdigest()
def parse(b): return json.loads(re.sub(r'^\s*/\*.*?\*/\s*','',b.decode(),count=1,flags=re.S))
def leaves(v,p=()):
 if isinstance(v,dict):
  return {q:z for k,x in v.items() for q,z in leaves(x,p+(k,)).items()}
 if isinstance(v,list):
  return {q:z for k,x in enumerate(v) for q,z in leaves(x,p+(str(k),)).items()}
 return {p:v}
for key,v in scope.items():
 if isinstance(v,dict) and 'path' in v and 'sha256' in v:
  check('frozen_'+key,sha((ROOT/v['path']).read_bytes())==v['sha256'])
claim=next(l for l in (ROOT/'ops/AGENT_COORDINATION.md').read_text().splitlines() if l.startswith('| Website UX and PageSpeed audit |'))
check('current_exact_claim',sha(claim.encode())=='455ee259533045ff733d90d0e219c4b44ca53e491dc07339ddb398d0569e3213')
check('scope_sha',sha(SCOPE.read_bytes())=='c2363cd16ddb14b9fdcc64574bb6e0b0174e95aeaf8063478ae85cf09a032f85')
before=(ROOT/scope['before']['path']).read_bytes(); after=(ROOT/scope['candidate']['path']).read_bytes()
bl=leaves(parse(before)); al=leaves(parse(after))
delta=[list(k) for k in set(bl)|set(al) if bl.get(k)!=al.get(k)]
key=('sections','collection_seo','display_titles','dresses')
check('one_of_783_leaves',len(bl)==len(al)==783 and delta==[list(key)],{'changed':delta,'leaves':len(bl)})
check('exact_values',bl[key]=='Šaty pro mámu a já' and al[key]=='Šaty pro maminku a dceru')
old=b'"dresses": "'+'Šaty pro mámu a já'.encode()+b'"'
new=b'"dresses": "'+'Šaty pro maminku a dceru'.encode()+b'"'
check('every_other_byte_preserved',before.count(old)==1 and before.replace(old,new,1)==after)
check('longer_metadata_title_preserved',bl[('sections','collection_seo','meta_titles','dresses')]==al[('sections','collection_seo','meta_titles','dresses')]=='Šaty pro mámu a já | matka dcera')
variables=json.loads((ROOT/scope['variables']['path']).read_text())
inverse=json.loads((ROOT/scope['rollback']['path']).read_text())
check('one_text_file_target',variables['themeId']=='gid://shopify/OnlineStoreTheme/137888792673' and len(variables['files'])==1 and variables['files'][0]['filename']=='locales/cs.json' and variables['files'][0]['body']['type']=='TEXT')
check('payload_exact',variables['files'][0]['body']['value'].encode()==after)
check('inverse_exact',inverse['themeId']==variables['themeId'] and len(inverse['files'])==1 and inverse['files'][0]['filename']=='locales/cs.json' and inverse['files'][0]['body']['type']=='TEXT' and inverse['files'][0]['body']['value'].encode()==before)
prior=json.loads((ROOT/scope['before_full_source_binding']['path']).read_text())
expected=json.loads((ROOT/scope['expected_after_source_binding']['path']).read_text())
for name,count,role,idpart in [('current',525,'MAIN','133290917985'),('candidate',527,'UNPUBLISHED','137888792673')]:
 obj=data[name]; base=baseline[name]
 check(name+'_identity_and_role',obj['id']=='gid://shopify/OnlineStoreTheme/'+idpart and obj['role']==role and obj['name']==base['name'])
 check(name+'_processing',obj['processing'] is False and obj['processingFailed'] is False)
 check(name+'_complete_pages',not obj['inventory']['pageInfo']['hasNextPage'] and not obj['selected']['pageInfo']['hasNextPage'])
 inv={f['filename']:f for f in obj['inventory']['nodes']}; bi={f['filename']:f for f in base['inventory']['nodes']}
 check(name+'_complete_unique_inventory',len(inv)==count and len(obj['inventory']['nodes'])==count and set(inv)==set(bi),{'files':len(inv)})
 changed=[k for k in bi if inv.get(k)!=bi[k]]
 check(name+'_record_preservation',changed==([] if phase=='before' or name=='current' else ['locales/cs.json']),{'changed':changed})
 meta=['id','name','role','updatedAt','processing','processingFailed']
 if phase=='after' and name=='candidate': meta.remove('updatedAt')
 check(name+'_metadata_preserved',all(obj[k]==base[k] for k in meta))
 selected=obj['selected']['nodes']
 check(name+'_selected_file',len(selected)==1 and selected[0]['filename']=='locales/cs.json')
 body=selected[0]['body']['content'].encode()
 target=before if phase=='before' or name=='current' else after
 if name=='current':
  check('main_czech_body_preserved',sha(body)=='b0e9378a0be73c287b7c361eb279b768d89087d839d584dd1ff0512d89557e6c')
 else:
  check('candidate_czech_body_exact',body==target,{'sha256':sha(body),'md5':md5(body),'bytes':len(body)})
  check('candidate_selected_inventory_agreement',all(selected[0][k]==inv['locales/cs.json'][k] for k in ['filename','checksumMd5','size','updatedAt']))
  binding=prior if phase=='before' else expected
  problems=[]
  for f in binding['files']:
   raw=(ROOT/f['sourcePath']).read_bytes(); rec=inv.get(f['filename'])
   if sha(raw)!=f['sha256'] or md5(raw)!=f['md5'] or len(raw)!=f['bytes'] or rec is None or rec['checksumMd5']!=f['md5'] or int(rec['size'])!=f['bytes']:
    problems.append(f['filename'])
  check('all_527_source_files_hash_and_inventory_match',len(binding['files'])==527 and not problems,{'files':len(binding['files']),'mismatches':problems})
if phase=='after':
 check('candidate_saved_after_before',data['candidate']['updatedAt']>baseline['candidate']['updatedAt'])
 actual={'status':'ACTUAL_AFTER_READBACK_VERIFIED' if all(c['pass'] for c in checks) else 'FAILED',
 'observedAt':fresh['receivedAtUtc'],'candidateId':137888792673,'candidateName':data['candidate']['name'],'role':data['candidate']['role'],'savedAt':data['candidate']['updatedAt'],
 'mainId':133290917985,'main525FilesAndMetadataPreserved':all(c['pass'] for c in checks if c['name'].startswith(('current_','main_'))),
 'totalFiles':527,'preservedPriorFiles':526,'successorFiles':['locales/cs.json'],'parentBindingSha256':scope['before_full_source_binding']['sha256'],
 'finalModuleSha256':prior['finalModuleSha256'],'files':expected['files'],
 'afterReadback':{'path':str(fresh_path.relative_to(ROOT)),'sha256':sha(fresh_path.read_bytes())},
 'publication':'UNPUBLISHED only; no MAIN write or Git push. Owner Admin publication remains pending.',
 'retainedAcceptance':'Prior accepted buyer-truth source and all additive post-publication cases remain applicable.'}
 for f in actual['files']:
  if f['filename']=='locales/cs.json': f['source']='ACTUAL one-string Czech H1 successor independently read back'
 if all(c['pass'] for c in checks): (PACKET/'ACTUAL_527_SOURCE_BINDING.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
receipt={'phase':phase,'checkedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceReadback':str(fresh_path.relative_to(ROOT)),'sourceReadbackSha256':sha(fresh_path.read_bytes()),'sourceReceivedAtUtc':fresh['receivedAtUtc'],'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks)}
out=PACKET/('ACTION_TIME_GUARDS.json' if phase=='before' else 'AFTER_GUARDS.json')
out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'phase':phase,'passed':receipt['passed'],'failed':receipt['failed'],'sourceReceivedAtUtc':fresh['receivedAtUtc'],'failedChecks':[c for c in checks if not c['pass']],'receipt':str(out)},ensure_ascii=False))
sys.exit(bool(receipt['failed']))
