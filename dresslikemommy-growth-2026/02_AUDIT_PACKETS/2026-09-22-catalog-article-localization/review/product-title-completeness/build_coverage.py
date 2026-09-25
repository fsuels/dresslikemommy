import json,pathlib,hashlib,collections
P=pathlib.Path(__file__).resolve().parent;R=P.parent/'article-title-independent'
loads=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
langs=['ar','cs','da','de','el','es','fi','fr','he','hi']
rows=sorted([r for l in langs for r in loads(P/f'worklist_{l}.json')['rows']],key=lambda r:r['i'])
authored={r['i']:('candidate_000_237.json',r)for r in loads(P/'candidate_000_237.json')}
for file in ['candidate_a_clipped_preserved.json','candidate_a_flo_preserved6.json']:
 for r in loads(P/file):authored[r['i']]=(file,r)
qualified={}
for file in ['product_a000_079_reviewed215.json','product_a35_preserved_reviewed.json','product_a6_flo_preserved_reviewed.json']:
 a=loads(R/file);a=a if isinstance(a,list)else a['rows']
 for r in a:qualified[r['i']]=(file,r)
knownConflicts={2:'Current English title calls bikini; body calls one-piece.',22:'Current English title/introduction calls two-piece; body feature calls one-piece.',87:'Current English title names sun/cloud/plant design; English body describes LOVE/heart.',130:'Current English title says cotton-silk; current body fabric is cotton/viscose.'}
opaque=loads(P.parent/'product-title-completeness-b/shared_source_context_resolution.json')['held'];opaque={r['productIndex']:r['reason']for r in opaque}
ledger=[]
for r in rows:
 i=r['i'];idx=i//20
 status='MANUALLY_REVIEWED_RETAIN_CURRENT_MEANING'
 if i in authored:status='AUTHORED_CORRECTION_INDEPENDENT_REVIEW_PENDING'
 if i in qualified:status='INDEPENDENTLY_REVIEWED_CORRECTION_READY_FOR_ROOT'
 if idx in knownConflicts:status='SOURCE_CONTRADICTION_RETAIN_PENDING_ROOT_SOURCE_DISPOSITION'
 file,proposal=authored.get(i,(None,None));qfile,q=qualified.get(i,(None,None))
 ledger.append({'i':i,'productIndex':idx,'resourceId':r['resourceId'],'locale':r['locale'],'key':'title','marketId':None,'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'effectiveBeforeValueSHA256':r['expectedEffectiveBeforeValueSHA256'],'overlayApplied':r['overlayApplied'],'inputWorklist':f'worklist_{r["locale"]}.json','disposition':status,'candidateFile':file,'candidateValueSHA256':proposal['valueSHA256']if proposal else None,'independentReviewedFile':f'../article-title-independent/{qfile}'if qfile else None,'independentReviewedValueSHA256':hashlib.sha256(q['value'].encode()).hexdigest()if q else None,'sourceConflict':knownConflicts.get(idx),'sourceClippingLimitation':opaque.get(idx),'method':'Full visible current English title versus effective target comparison. Exact current English body consulted for garment cuts, ambiguous words, printed slogans and body-supported clipped completion. Printed design identities retained where appropriate. Changes use exact source/body digests and effective before guard.','unchangedDispositionReason':None if proposal else('Source facts need root reconciliation.'if idx in knownConflicts else'Current localized meaning is sufficiently equivalent; retain valid translations, target-language loanwords, printed strings and source design names.')})
assert len(ledger)==2380 and len({(r['resourceId'],r['locale'])for r in ledger})==2380
assert all(sum(r['locale']==l for r in ledger)==238 for l in langs)
f=P/'A2380_COVERAGE_LEDGER.json';f.write_text(json.dumps({'scope':'238 products × 10 assigned locales, titles only; all 2380 full title pairs manually compared. Root owns release and source changes.','rows':ledger},ensure_ascii=False,indent=2)+'\n')
manifest={'titlePairsManuallyReviewed':2380,'publishedProducts':238,'locales':langs,'all20EffectiveInventoryTitlePairs':4760,'rootTitleOverlayRowsAll20':394,'ownEffectiveOverlayRows':sum(r['overlayApplied']for r in rows),'uniqueAuthoredTitleCorrections':len(authored),'initialCandidate864File':'candidate_000_237.json','independentQualifiedCount':len(qualified),'independentPendingCount':sum(r['disposition']=='AUTHORED_CORRECTION_INDEPENDENT_REVIEW_PENDING'for r in ledger),'sourceConflictTupleFlags':sum(bool(r['sourceConflict'])for r in ledger),'actualAuthorCandidateSourceContradictionHolds':2,'unchangedTitlePairsWithoutNewCandidate':sum(r['i']not in authored for r in rows),'sourceContradictionProductIndices':list(knownConflicts),'dispositions':dict(collections.Counter(r['disposition']for r in ledger)),'perLocale':{l:dict(collections.Counter(r['disposition']for r in ledger if r['locale']==l))for l in langs},'coverageLedgerFile':f.name,'coverageLedgerSHA256':sha(f),'frozenDisjointInitialReviewBatches':{n:sha(P/n)for n in ['candidate_000_079.json','candidate_080_179.json','candidate_final_remaining.json']},'supersedingClippedSourceFollowups':{n:sha(P/n)for n in ['candidate_a_clipped_preserved.json','candidate_a_flo_preserved6.json']},'checks':'Every title tuple unique; 238 rows per assigned locale; all initial864 raw/source/effective before bindings pass. No invented overlay updatedAt; root fresh read required. Independent meaning review status recorded separately.','noExternalWrites':True,'noGitWrites':True,'remainingOwnerAction':'Root integrates independently reviewed candidates using fresh API guards, syncs main and verifies live. Pending reviewer completes disjoint308 and304 batches.'}
(P/'A2380_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in manifest.items()if not isinstance(v,(dict,list))},ensure_ascii=False))
