"""Run only after root final release; asserts all152 exact source-bound receipts before updating owned report."""
import collections,copy,datetime,hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2];load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();key=lambda r:(r['resourceId'],r['locale'],r['key'])
p=R/'review/final_remaining_dispositions.json';d=load(p);orig=copy.deepcopy(d);w=load(R/'review/native-header-final/reclassified150_worklist.json')['rows'];work={key(r):r for r in w};assert len(work)==150
eligible150=set(work)
original846=load(R/'review/article-title-independent/product_source_disposition846.json')['rows']
extra={key(r):r for r in original846 if r['resourceId']=='gid://shopify/Product/7229128441953' and r['locale'] in ['ru','sv'] and r['key']=='body_html'}
assert len(extra)==2 and not set(extra)&eligible150
work.update(extra);required152=set(work)
inv=load(R/'review/body-structure-audit/effective_body_inventory.json')['rows']
aux={key(r):dict(r,sourceValue=r['source']) for r in inv if r['productIndex'] in [164,206] and r['locale']=='fi'}
assert len(aux)==2 and not set(aux)&{key(r) for r in original846}
work.update(aux)
records=collections.defaultdict(list);cohortfields=collections.defaultdict(set);evidence={}
for f in sorted((R/'releases').glob('*.json')):
 if not re.fullmatch(r'.*_\d{4}\.json',f.name):continue
 q=load(f)
 if q.get('afterExactValueAndCurrentGuard')!='PASS':continue
 assert q['beforeSourceAndTranslationGuard']=='PASS' and q['publicationGuard']=='PASS'
 for alias,obj in q['mutation'].items():
  rid=q['resourceIds'][int(alias[1:])]
  for x in obj.get('translations',[]):
   assert x.get('outdated') is False
   k=(rid,x['locale'],x['key']);vsha=sha(x['value']);record={'file':str(f.relative_to(R)),'cohort':q['cohort'],'status':'EXACT_AFTER_AND_CURRENT_PASS','valueSHA256':vsha};records[k].append(record);cohortfields[q['cohort']].add((k,vsha))
 evidence[str(f.relative_to(R))]=fs(f)
qualified_full={}
for mf in sorted((R/'review').glob('catalogProductFull*_root_manifest.json')):
 m=load(mf);cf=Path(m['input']).resolve();assert fs(cf)==m['inputSHA256'];a=load(cf);a=a['rows'] if isinstance(a,dict) else a
 for r in a:
  k=key(r)
  if k not in work:continue
  assert r['sourceDigest']==work[k]['sourceDigest'] and r['sourceValue']==work[k]['sourceValue'];matches=[z for z in records[k] if z['valueSHA256']==sha(r['value']) and z['cohort'].startswith('catalogProductFull')];assert matches,('full body lacks completed exact receipt',k)
  if k in qualified_full:assert qualified_full[k]['valueSHA256']==sha(r['value'])
  qualified_full[k]={'candidateFile':str(cf.relative_to(R)),'candidateSHA256':fs(cf),'sourceDigest':r['sourceDigest'],'valueSHA256':sha(r['value']),'receipts':matches}
 evidence[str(mf.relative_to(R))]=fs(mf);evidence[str(cf.relative_to(R))]=fs(cf)
assert required152<=set(qualified_full),('full152 not all published',len(set(qualified_full)&required152),152)
# Narrow native fixes resolve only their original occurrence, never unrelated source facts.
current=load(R/'review/native-header-final/current22_candidates.json')['rows'];currentkeys=set()
for r in current:
 k=key(r);assert any(z['valueSHA256']==sha(r['value']) for z in records[k]),('native19 missing exact receipt',k);currentkeys.add(k)
resolved=copy.deepcopy(d.get('resolvedAfterInitialSnapshot',[]));rows=[]
for r in d['rows']:
 k=key(r);remaining=[]
 for issue in r['issues']:
  done=(k in qualified_full and (issue.get('originalGroup') in ['source_access_copy','selector_draft','operator_instruction','extrapolated_sizes'] or issue['category'] in ['OUTDATED_BODY_ENGLISH_HEADER_OCCURRENCE','NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW','OUTDATED_BODY_QZ_PLACEHOLDER'])) or (k in currentkeys and issue['category']=='NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW')
  if done:resolved.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'issue':issue,'resolution':'COMPLETE_CURRENT_SOURCE_TRANSLATION_EXACT_RECEIPT' if k in qualified_full else 'EXACT_NATIVE_HEADER_TEXT_REPAIR_RECEIPT','proof':qualified_full.get(k) or {'candidateFile':'review/native-header-final/current22_candidates.json','receipts':records[k]}})
  else:remaining.append(issue)
 if remaining:
  r['issues']=remaining;r['verifiedWrites']=records[k];r['narrowWritesResolveSourceFacts']=False;rows.append(r)
source_remaining={key(r) for r in rows if any(i.get('originalGroup') for i in r['issues'])};assert len(source_remaining)==443
sanity_file=R/'review/full_source_150/b_group/remaining445_sanity.json';sanity=load(sanity_file);sanityrows={key(r):r for r in sanity['rows']};assert len(sanityrows)==445 and source_remaining<=set(sanityrows)
for r in rows:
 k=key(r)
 if k in source_remaining:
  x=sanityrows[k];assert r['sourceDigest']==x['sourceDigest'];r['refinedSourceDisposition']={'classification':x['classification'],'sanityGroup':x['sanityGroup'],'evidencePath':str(sanity_file.relative_to(R))}
d['refinedRemaining443Assessment']={'evidencePath':str(sanity_file.relative_to(R)),'SHA256':fs(sanity_file),'counts':dict(collections.Counter(sanityrows[k]['classification'] for k in source_remaining)),'groupCounts':sanity['expected443AfterTwoReceipts'],'remainingPolicyOnly':0,'note':'Read-only source-evidence review distinguishes explicit conflicts, design mismatches, ambiguous purchased unit and unknown derived measurements; not blanket permission holds.'}
evidence[str(sanity_file.relative_to(R))]=fs(sanity_file)

articles={key(r) for r in rows if any(i['category'] in ['ARTICLE_SHIPPING_SCOPE_CONFLICT','ARTICLE_SUN_PROTECTION_CLAIM_EVIDENCE_MISSING','OBSOLETE_50_DOLLAR_SHIPPING_THRESHOLD'] for i in r['issues'])};title={key(r) for r in rows if any(i['category']=='TITLE_SAME_PRODUCT_FACT_CONFLICT' for i in r['issues'])};assert len(articles)==142 and len(title)==80
counts=collections.Counter(i['category'] for r in rows for i in r['issues']);assert counts['NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW']==2-len(set(qualified_full)&set(aux)) and counts['OUTDATED_BODY_ENGLISH_HEADER_OCCURRENCE']==0 and counts['OUTDATED_BODY_QZ_PLACEHOLDER']==0
root_cohort_files={
 'catalogProductStructure375':'review/article-title-independent/body_structure375_reviewed.json',
 'catalogProductHeaders2028':'review/body-header-localization/header_candidates_root_reviewed.json',
 'catalogProductSize156':'review/size-label-repair/candidate_root_reviewed156.json',
 'catalogProductPlaceholder88':'review/size-label-repair/placeholder-review/placeholder88_root_bound.json',
 'catalogProductProse11':'review/body-header-localization/prose-completion-review/prose_completion11_root_bound.json'}
archive=load(R/'release_review_archives/manifest.json');archive_map={x['originalReviewPath']:x for x in archive['files']}
for co in d['plannedCohorts']:
 if 'candidateFile' not in co:continue
 co['candidateFile']=root_cohort_files[co['cohortLabel']];cf=R/co['candidateFile'];assert fs(cf)==archive_map[co['candidateFile']]['uncompressedSHA256'];co['candidateSHA256']=fs(cf);co['archiveFile']=archive_map[co['candidateFile']]['archivePath'];evidence[co['candidateFile']]=fs(cf)
 a=load(cf)['rows'];n=sum(any(z['valueSHA256']==sha(r['value']) and z['cohort']==co['cohortLabel'] for z in records[key(r)]) for r in a);assert n==len(a),('root-bound cohort lacks exact receipt',co['cohortLabel'],n,len(a));co.update(exactMatchingCandidateReceiptRows=n,status='COMPLETE_EXACT_RECEIPTS')
d['plannedCohorts']=[co for co in d['plannedCohorts'] if co.get('cohortLabel')!='full_source150']
d['plannedCohorts'].append({'cohortLabel':'full_source150','plannedRows':150,'exactMatchingCandidateReceiptRows':150,'status':'COMPLETE_EXACT_SOURCE_BOUND_RECEIPTS','note':'Full current-source replacements, not partial label writes; includes source uncertainty/workflow qualifications.'})
d['limitations']=[('Final offline receipt reconciliation after all154 full-source bodies (152 original fields plus2 separate Finnish fields) completed.' if set(aux)<=set(qualified_full) else 'Interim offline receipt reconciliation: all152 original full-source fields verified; separate Finnish2 awaiting release receipts.'),'Not a new full-catalog audit or an independent fresh live verification; exact root release after-state receipts are the evidence.','Root owns source decisions, public release, Gitmain synchronization and public checks.']
d['reconciliationStatus']='FINAL_COMPLETED_AUTHORIZED_TRANSLATION_REPAIRS_WITH_EXPLICIT_SOURCE_RESIDUALS' if set(aux)<=set(qualified_full) else 'INTERIM_FI2_RELEASE_PENDING'
d['snapshotAtUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['rows']=rows;d['resolvedAfterInitialSnapshot']=resolved;d['sourceQualifiedFull150']=[{'resourceId':k[0],'locale':k[1],'key':k[2],**v} for k,v in qualified_full.items() if k in eligible150];d['additionalFullCurrentSourceBodies']=[{'resourceId':k[0],'locale':k[1],'key':k[2],'original846Overlap':k in extra,**v} for k,v in qualified_full.items() if k not in eligible150];d['counts'].update(originalProductFieldsStillOpen=443,originalProductFullyResolvedByCurrentSourceBodies=152,originalProductResolvedTotal=403,originalArticleFieldsStillOpen=142,titleSourceConflictWatches=80,outdatedHeaderOccurrences=0,outdatedHeaderBodies=0,nativeHeaderOccurrences=counts['NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW'],nativeHeaderBodies=counts['NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW'],outdatedQZBodies=0,uniqueRemainingTuplesIncludingEnglishLinkSources=len(rows));d['receiptCohortCounts']={k:len(v) for k,v in cohortfields.items()};d['evidenceFileSHA256'].update(evidence)
d['counts']['originalProductBodyFieldsWithPartialWrites']=sum(r['key']=='body_html' and bool(r['verifiedWrites']) and any(i.get('originalGroup') for i in r['issues']) for r in rows)
d.pop('supersedingScopedUpdates',None)
d['remainingOriginalProductFieldsByKey']=dict(collections.Counter(r['key'] for r in rows if any(i.get('originalGroup') for i in r['issues'])));d['remainingIssueCounts']=dict(counts)
d['countingNotes'] = list(dict.fromkeys(d['countingNotes'] + ['Reclassified150 full bodies plus2 qualified-guidance RU/SV bodies are source/digest-bound and exact-receipt verified; original595 is reduced to443. Draft/internal-source wording is preserved as source copy, not a translation hold.','161 prior outdated-header occurrences across41 bodies and six QZ fields are fully resolved through complete source translations; do not count them again.','Native31 resolves22 exact label repairs plus7 full-body translations; the two additional FI full-source replacements resolve legacy chart correspondence only when exact completed receipts are present.','443 is a remaining source-evidence ledger classification, not443 blanket permission gates. Later specific evidence may qualify additional rows.']))
d['unfinishedWorkNotANewPermissionGate']=[('Two Finnish complete-current-source replacements are independently qualified; live release receipts remain pending. They replace stale charts rather than invent missing hip measurements.' if counts['NATIVE_HEADER_TYPO_OR_DIMENSION_REVIEW'] else 'The two Finnish legacy chart gaps are resolved by complete current-source translations; original846 overlap is zero.'),'132 source-access +16 selector-draft +2 operator-copy full translations are complete with source qualifications retained. English editorial cleanup is separate.','Further precise source evidence may resolve individual residual fields; neither internal workflow wording nor outdated flags alone justify a hold.']
for group in d['sourceGroupDecisionEvidence']:group['historicalOriginal846GroupEvidence']=True
# Preserve the timestamped prior snapshot before replacing our own report.
backup=R/'review/final_remaining_dispositions_pre150_snapshot.json'
if not backup.exists():backup.write_text(json.dumps(orig,ensure_ascii=False,indent=2)+'\n')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
note_path=R/'review/final_remaining_dispositions_150_note.json';note=load(note_path);note['snapshotAtUTC']=d['snapshotAtUTC'];note['counts'].update(eligibleWithExactFullTranslationReceipts=150,eligiblePreparedButNoExactReceipt=0,eligibleFullAuthorshipOrReviewInProgress=0,originalProductFieldsNotYetFullyTranslated=443,additionalOriginalFieldsFullyTranslated=2,articleProductTitleUnion=len(source_remaining|articles|title))
for r in note['rows']:
 k=key(r);r['status']='EXACT_LIVE_FULL_TRANSLATION_RECEIPT';r['fullTranslation']=qualified_full[k]
note['notes']=list(dict.fromkeys(note['notes']+['Final update: all150 exact current-source-bound values have completed release receipts; no pending values counted live. Main final_remaining_dispositions.json now contains current deduplicated residuals.']))
note_path.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'full150Exact':150,'additionalOriginalExact':2,'originalRemaining':443,'uniqueRemainingTuples':len(rows),'SHA256':fs(p)}))
