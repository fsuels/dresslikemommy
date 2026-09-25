#!/usr/bin/env python3
"""Read-only reconciliation of frozen local translation evidence; writes this review directory only."""
from pathlib import Path
import collections,datetime,hashlib,json
HERE=Path(__file__).resolve().parent
PACKET=HERE.parent
PRODUCTS=PACKET/'products'
REM=PRODUCTS/'remaining'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vsha(v):return hashlib.sha256(v.encode()).hexdigest() if v is not None else None
def ident(r):return r['resourceId'],r['locale'],r['key']
def write(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
raw_cache={}
def raw_resource(r):
 name=r.get('rawFile') or r.get('evidenceFile') or 'remaining/linked_metaobjects_before.json'
 path=PRODUCTS/name
 if path not in raw_cache:
  raw_cache[path]={n['resourceId']:n for n in read(path)['data']['translatableResourcesByIds']['nodes']}
 return raw_cache[path][r['resourceId']],path

def bind(r):
 n,path=raw_resource(r)
 s=[s for s in n['translatableContent'] if s['key']==r['key'] and s['locale']=='en']
 assert len(s)==1,('ambiguous source',ident(r))
 assert s[0]['value']==r['source'],('source mismatch',ident(r))
 digest=r.get('sourceDigest',r.get('translatableContentDigest'))
 assert s[0]['digest']==digest,('digest mismatch',ident(r))
 before=[]
 for alias,vs in n.items():
  if alias.startswith('tr_'):
   for t in vs:
    if t['locale']==r['locale'] and t['key']==r['key'] and t.get('market') is None and t not in before:before.append(t)
 assert len(before)<=1,('conflicting locale records',ident(r))
 assert (before[0] if before else None)==r['before'],('before mismatch',ident(r))
 for key,dig in r.get('supportingSourceDigests',{}).items():
  assert any(s['key']==key and s['digest']==dig and s['locale']=='en' for s in n['translatableContent']),('supporting digest mismatch',ident(r),key)
 value=r.get('value',r.get('after'))
 assert isinstance(value,str) and value.strip()
 assert r['locale']!='en' and r.get('marketId') is None
 return {'resourceId':r['resourceId'],'productId':r.get('productId'),'locale':r['locale'],'key':r['key'],'marketId':None,'source':r['source'],'sourceDigest':digest,'sourceSHA256':vsha(r['source']),'before':r['before'],'expectedBeforeValueSHA256':vsha(r['before']['value'] if r['before'] else None),'value':value,'valueSHA256':vsha(value),'rawFile':str(path.relative_to(PACKET)),'rawFileSHA256':sha(path),'supportingSourceDigests':r.get('supportingSourceDigests',{}),'bindingReviewCode':'EXACT_EN_SOURCE_OPAQUE_DIGEST_EXPLICIT_LOCALE_GLOBAL_BEFORE_PASS'}

manifest=read(REM/'remaining_manifest.json')
reviewed={}
receipts=[]
for receipt in manifest['independentReviewReceipts']:
 p=REM/receipt['path'];assert sha(p)==receipt['sha256']
 d=read(p);assert d['status'].startswith('PASS_WITH_LIMITS')
 files=d.get('files',[{'path':d.get('candidateFile'),'sha256':d.get('candidateSHA256')}])
 for f in files:
  q=Path(f['path']);q=q if q.is_absolute() else REM/q
  assert sha(q)==f['sha256'],str(q)
  reviewed[str(q.relative_to(REM))]={'path':str(p.relative_to(PACKET)),'sha256':sha(p),'status':d['status']}
 receipts.append({'path':str(p.relative_to(PACKET)),'sha256':sha(p),'status':d['status']})
for artifact in manifest['artifacts']:
 assert sha(REM/artifact['path'])==artifact['sha256'],artifact['path']

cohorts=[('option_cohort_candidate.json','ROOT_INDEPENDENT_OPTION_LEXICON_MEANING_PASS'),('simple_copy_cohort_candidate.json','INDEPENDENT_SIMPLE_APPAREL_DICTIONARY_MEANING_PASS'),('german_titles_cohort_candidate.json','INDEPENDENT_GERMAN_TITLE_MEANING_PASS'),('remaining/prepared_remaining_candidates.json','PRIOR_INDEPENDENT_MEANING_RECEIPT_HASH_BOUND')]
original=read(PRODUCTS/'CANDIDATE_MANIFEST.json')
for f in original['cohorts']:assert sha(PRODUCTS/f['file'])==f['sha256']
option_review=read(PRODUCTS/'option_cohort_root_review.json')
assert option_review['status']=='PASS' and option_review['candidateSha256']==sha(PRODUCTS/'option_cohort_candidate.json')
simple_dict=read(PRODUCTS/'simple_copy_dictionary.json')
hold_indices={20,29,39,40}
german=read(PRODUCTS/'german_titles_cohort_candidate.json')['rows']
hold_ids={ident(german[i]):i for i in hold_indices}
corrected={20:'Passendes T-Shirt- und Babybody-Set für Vater und Baby mit „Player 1“ und „Player 2“ … | DLM',29:'T-Shirt-Set mit Batteriemotiv – „Super Tired“ für die Eltern … | DLM',39:'Regenbogen-T-Shirts mit „Beautiful“-Schriftzug und buntem Sonnenmotiv | DLM',40:'T-Shirts mit „Eternal“-Schriftzug und buntem Herzmotiv | DLM'}
reasons={20:'The bound English body explicitly assigns a T-shirt to dad and an onesie to baby; the candidate calls both T-shirts.',29:'The body identifies Super Tired as actual printed text. Preserve the literal English slogan instead of translating it into an audience description.',39:'The body identifies Beautiful as actual printed text; retain the literal slogan and translate the surrounding garment description.',40:'The body identifies Eternal as actual printed text; retain the literal slogan and translate the surrounding garment description.'}
qualified=[];new_holds=[];proposals=[];seen=set();all_rows=[];cohort_summary=[]
for filename,meaning in cohorts:
 p=PRODUCTS/filename;d=read(p);rows=d['rows'];count=0
 for row in rows:
  k=ident(row);assert k not in seen,('duplicate',k);seen.add(k)
  record=bind(row);record.update({'candidateFile':str(p.relative_to(PACKET)),'candidateFileSHA256':sha(p),'meaningReviewCode':meaning,'requiresFreshLiveSourceAndBeforeGuard':True})
  if filename.startswith('remaining/'):
   a=row['preparedArtifact'];assert a in reviewed
   assert row['preparedArtifactSHA256']==sha(REM/a)
   source_rows=read(REM/a)['rows'];matching=[r for r in source_rows if ident(r)==k]
   assert len(matching)==1 and matching[0]['value']==record['value']
   record['selectedCandidateFile']=str((REM/a).relative_to(PACKET));record['selectedCandidateFileSHA256']=sha(REM/a);record['meaningReviewReceipt']=reviewed[a]
  elif filename=='simple_copy_cohort_candidate.json':
   dictionary_index=[k.casefold() for k in simple_dict['sourceKeys']].index(row['source'].casefold())
   assert row['value']==simple_dict[row['locale']][dictionary_index]
  elif filename=='option_cohort_candidate.json':
   record['meaningReviewReceipt']={'path':'products/option_cohort_root_review.json','sha256':sha(PRODUCTS/'option_cohort_root_review.json'),'status':'PASS'}
  if k in hold_ids:
   i=hold_ids[k];new_holds.append({**record,'disposition':'INDEPENDENT_REVIEW_CORRECTION_REQUIRED','reason':reasons[i]})
   proposal={**record,'value':corrected[i],'valueSHA256':vsha(corrected[i]),'replacesUnreleasedCandidateValue':record['value'],'reason':reasons[i],'status':'PROPOSED_BY_REVIEWER_REQUIRES_ROOT_INDEPENDENT_APPROVAL'}
   proposals.append(proposal)
  else:qualified.append(record);count+=1
  all_rows.append(record)
 cohort_summary.append({'candidateFile':str(p.relative_to(PACKET)),'sha256':sha(p),'fields':len(rows),'qualified':count,'held':len(rows)-count})

ledger=manifest['fieldLedger'];assert len({ident(r) for r in ledger})==len(ledger)
existing_holds=[r for r in ledger if r['status']=='PRECISE_SOURCE_OR_TABLE_HOLD']
nochange=[r for r in ledger if r['status']=='REVIEWED_NO_CHANGE']
for r in existing_holds+nochange:
 assert ident(r) not in seen,('candidate vs noncandidate overlap',ident(r))
existing_holds=[{**r,'evidenceFile':str((REM/r['artifact']).relative_to(PACKET)),'evidenceSHA256':sha(REM/r['artifact']),'disposition':r['status']} for r in existing_holds]
assert len(existing_holds)==918 and len(nochange)==107
language=read(REM/'language_review_dispositions.json')
assert len(language['rows'])==337 and len({ident(r) for r in language['rows']})==337
ql={ident(r):r for r in qualified};hl={ident(r):r for r in existing_holds+new_holds};nc={ident(r):r for r in nochange}
language_reconciled=[]
for r in language['rows']:
 n,path=raw_resource(r);s=next(t for t in n['translatableContent'] if t['key']==r['key'] and t['locale']=='en')
 assert s['digest']==r['sourceDigest'] and vsha(s['value'])==r['sourceSHA256']
 tr=[t for a,vs in n.items() if a.startswith('tr_') for t in vs if t['key']==r['key'] and t['locale']==r['locale'] and t.get('market') is None]
 assert tr and all(vsha(t['value'])==r['currentSHA256'] for t in tr)
 k=ident(r)
 final='QUALIFIED_CANDIDATE' if k in ql else 'PRECISE_HOLD' if k in hl else 'REVIEWED_NO_CHANGE' if k in nc else 'TRIAGE_FALSE_POSITIVE_ONLY' if r['disposition']=='WRONG_LANGUAGE_FALSE_POSITIVE_NO_CHANGE' else 'UNRESOLVED'
 assert final!='UNRESOLVED',r
 language_reconciled.append({**r,'reconciledDisposition':final})

# These receipts are a point-in-time observation, not a substitute for final live readback.
released=set();receipt_errors=[];receipt_files=[]
for p in sorted(PRODUCTS.glob('option_release_batch_*.json')):
 d=read(p);receipt_files.append({'path':str(p.relative_to(PACKET)),'sha256':sha(p)})
 for alias,m in d.get('mutation',{}).items():
  if m.get('userErrors'):receipt_errors.append({'file':p.name,'alias':alias,'errors':m['userErrors']});continue
  idx=int(alias[1:]);rid=d['ids'][idx]
  for t in m.get('translations',[]):
   k=(rid,t['locale'],t['key'])
   if k in ql and t['value']==ql[k]['value'] and t.get('outdated') is False:released.add(k)
 for r in d.get('mismatches',[]):receipt_errors.append({'file':p.name,'mismatch':r})
assert not receipt_errors,receipt_errors
for r in qualified:r['observedMutationReceiptAtReview']='MATCHING_SUCCESS_RECEIPT_EXISTS' if ident(r) in released else 'NOT_SEEN_IN_OPTION_RECEIPTS'

limits=['All source/current-before comparisons use frozen local snapshots. Fresh live source digest and exact translation before guard remain mandatory.', 'Existing independent meaning reviews are attributed, hash-bound evidence; this reviewer independently reread all 569 simple-copy rows by exact dictionary mapping and all 50 German titles, and did not pretend to re-author/re-review every long body.', 'The four reviewer proposals are deliberately excluded until root independently accepts them.', 'Exact translated product facts do not independently establish supplier truth. 918 recorded source/chart/claim holds remain held.', 'Mutation receipt count is only a point-in-time partial-release observation, not a live public acceptance result.', 'No live write, provider, browser, Git, canonical, source, price, status, handle, inventory, or ad changes by this lane.']
write('qualified_product_release_index.json',{'status':'QUALIFIED_LOCAL_INDEX_REQUIRES_FRESH_ROOT_GUARDS','generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fields':len(qualified),'resources':len({r['resourceId'] for r in qualified}),'rows':qualified,'limits':limits})
write('held_product_ledger.json',{'fields':len(existing_holds)+len(new_holds),'existingSourceAndChartHolds':existing_holds,'newIndependentMeaningHolds':new_holds,'limits':limits})
write('german_title_correction_proposals.json',{'status':'FOUR_SOURCE_BOUND_PROPOSALS_PENDING_ROOT_INDEPENDENT_REVIEW','rows':proposals})
write('retained_product_ledger.json',{'rows':nochange,'outdatedMetadataEvidence':{'path':'products/remaining/no_change_outdated_metadata.json','sha256':sha(REM/'no_change_outdated_metadata.json'),'fields':len(read(REM/'no_change_outdated_metadata.json')['rows'])}})
write('language_flag_reconciliation.json',{'allFlags':337,'inputDispositions':language['byDisposition'],'reconciledCounts':dict(collections.Counter(r['reconciledDisposition'] for r in language_reconciled)),'rows':language_reconciled})
result={'status':'PASS_RECONCILIATION_WITH_FOUR_NEW_MEANING_HOLDS','allSelectedFields':len(all_rows),'qualifiedFields':len(qualified),'heldFields':len(existing_holds)+len(new_holds),'retainedNoChangeFields':len(nochange),'duplicateCandidateRows':0,'sourceDigestBeforeBindingErrors':0,'allSelectedLocaleCounts':dict(collections.Counter(r['locale'] for r in all_rows)),'cohorts':cohort_summary,'independentReviewReceipts':receipts,'frozenRawFiles':len(raw_cache),'languageFlags':337,'languageReconciledCounts':dict(collections.Counter(r['reconciledDisposition'] for r in language_reconciled)),'observedSuccessfulOptionReceiptFields':len(released),'receiptFiles':receipt_files,'limits':limits}
write('product_release_reconciliation.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['independentReviewReceipts','receiptFiles','limits','allSelectedLocaleCounts']},ensure_ascii=False,indent=2))
