from pathlib import Path
import json,hashlib,importlib.util,copy,re,html
P=Path(__file__).parent;PACK=P.parents[2]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fsha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=json.loads((P/'selected_candidate.json').read_text())['rows']
selection=json.loads((P/'selection.json').read_text())
corrections=[
 ('559652503649','löst stickad','ledig stickad',3,'SOURCE_MODIFIER_PRECISION','Loose modifies the garment; the original Swedish describes an open/loose knit construction. Ledig stickad retains the relaxed garment meaning without inferring knit construction.'),
 ('559653486689','Jackor med teddyfoder','Jackor i fårskinnsimitation',3,'UNSUPPORTED_FEATURE','Faux shearling names an imitation material; the original Swedish specifically asserts a teddy lining.'),
 ('559661908065','– tropiskt mönster i 100 % bomull','– i 100 % bomull med tropiskt mönster',2,'MODIFIER_ATTACHMENT','100% cotton describes the shirts, not the tropical print.'),
 ('559662268513','Matchande randigt T-shirtset med slipsmotiv','Matchande T-shirtset med randigt slipsmotiv',3,'MODIFIER_ATTACHMENT','Striped describes the tie motif, not the whole T-shirt set.'),
 ('559662301281','Matchande strandklänning och skjortset med blått tropiskt blommönster för familjen','Matchande set med strandklänning och skjorta med blått tropiskt blommönster för familjen',2,'SET_GRAMMAR','The coordinated set consists of a dress and a shirt; the original Swedish instead separates a dress from a shirt set.'),
 ('559662792801','Sommarbadshorts för pappa &amp; son','Strandshorts för pappa &amp; son till sommaren',2,'UNSUPPORTED_USE','Summer beach shorts does not specifically assert swimwear. Strandshorts preserves the stated beach use.'),
 ('559662792801','Sommarbadshortsen för pappa &amp; son','Strandshortsen för pappa &amp; son till sommaren',1,'UNSUPPORTED_USE','Apply the same beach-shorts correction with the definite plural form required in the prose sentence.')
]
byid={r['resourceId']:copy.deepcopy(r) for r in rows};proposals=[]
for suffix,old,new,count,kind,reason in corrections:
 rid='gid://shopify/Article/'+suffix;r=byid[rid]
 assert r['value'].count(old)==count,(suffix,old,r['value'].count(old))
 r['value']=r['value'].replace(old,new)
 proposals.append({'resourceId':rid,'locale':'sv','key':'body_html','old':old,'new':new,'expectedOccurrences':count,'kind':kind,'reason':reason})
changed={x['resourceId'] for x in proposals};assert len(changed)==6
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
allfinal=[];checks=[]
for original in rows:
 r=byid[original['resourceId']]
 check=m.verify_text(r['sourceValue'],r['value'],'sv');assert not check['errors'],(r['resourceId'],check)
 if r['resourceId']in changed:
  r['valueSHA256']=sha(r['value'])
  r['reason']='Independent full source-to-target Swedish review; exact product-reference wording corrections. Complete source content and markup preserved.'
 checks.append({'resourceId':r['resourceId'],'locale':'sv','key':'body_html','sourceDigest':r['sourceDigest'],'originalValueSHA256':sha(original['value']),'proposedValueSHA256':sha(r['value']),'changed':r['resourceId'] in changed,'structure':check})
 allfinal.append(r)
unchanged=[r for r in allfinal if r['resourceId']not in changed];corrected=[r for r in allfinal if r['resourceId']in changed]
write('qualified_unchanged_rows.json',{'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS','rows':unchanged})
write('corrected_proposed_rows.json',{'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS_AFTER_EXACT_CORRECTIONS','rows':corrected})
write('reviewed_all_55_proposed.json',{'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS','rows':allfinal,'limits':'Local translation review only. Root must use current source/before guards and verify registration/live rendering.'})
write('correction_proposals.json',{'status':'EXACT_CORRECTION_PROPOSALS','rules':proposals,'changedBodies':len(changed),'replacements':sum(x['expectedOccurrences']for x in proposals),'checks':checks})
# Freeze qualified exact rows in the same fields used by the root release index.
qualified=[]
for r in allfinal:
 candidate=P/('corrected_proposed_rows.json' if r['resourceId']in changed else'qualified_unchanged_rows.json')
 raw=Path(r['rawFile']);raw=raw.resolve() if raw.is_file() else PACK/raw
 assert raw.is_file(),raw
 qualified.append({'resourceId':r['resourceId'],'locale':'sv','key':'body_html','marketId':None,'source':r['sourceValue'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['sourceValue']),'before':r['before'],'expectedBeforeValueSHA256':None if r['before']is None else sha(r['before']),'value':r['value'],'valueSHA256':sha(r['value']),'rawFile':str(raw.relative_to(PACK)),'rawFileSHA256':fsha(raw),'candidateFile':str(candidate.relative_to(PACK)),'candidateFileSHA256':fsha(candidate),'bindingReviewCode':'EXACT_EN_SOURCE_OPAQUE_DIGEST_EXPLICIT_LOCALE_GLOBAL_MISSING_PASS','meaningReviewCode':'INDEPENDENT_FULL_SOURCE_TARGET_PROSE_PASS_AFTER_EXACT_CORRECTION' if r['resourceId']in changed else'INDEPENDENT_FULL_SOURCE_TARGET_PROSE_PASS','structureReviewCode':'EXACT_HTML_ATTRIBUTES_URLS_NUMBERS_TABLES_PASS','requiresFreshLiveSourceAndBeforeGuard':True})
write('qualified_release_index.json',{'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS','rows':qualified,'limits':'Root-owned current source/before guard and external application/live verification remain separate.'})
review={'status':'INDEPENDENT_TRANSLATION_REVIEW_PASS_AFTER_SIX_BODY_CORRECTIONS','selectedBodies':55,'alreadyReviewedBodiesExcluded':12,'originalCandidatesPassUnchanged':49,'correctedProposedBodies':6,'exactCorrectionRules':len(proposals),'correctedOccurrences':sum(x['expectedOccurrences']for x in proposals),'uniqueSourceTargetTextPairsReviewed':982,'uniqueAssembledLinkedParagraphsReviewed':184,'exactRepeatedBoilerplatePairsReviewed':122,'method':'Read every unique source-target text pair, including complete prose, headings, list entries, CTA/title fragments; read all unique assembled linked paragraphs for grammar across inline boundaries. Exact repeated boilerplate was displayed compactly only after full source/target boilerplate validation; each variable product title was reviewed. Compare original complete rows against raw English body, opaque digest and global sv before; re-run HTML/attrs/URLs/numbers/table/placeholder invariants after every proposed correction.','structureAndRawBinding':selection,'corrections':proposals,'sourceAmbiguities':[{'resourceId':'gid://shopify/Article/559662399585','source':'Mother Daughter Stripe Holiday Dress','target':'Randig semesterklänning för mamma och dotter','disposition':'Accepted English holiday can mean vacation; article Thanksgiving context may suggest a festive dress but does not establish product title intent. No invented feature or source rewrite.'}],'sourceClaimDisposition':'All source marketing, quality, testing, free-shipping, commercial and year assertions remain faithfully translated. Their underlying truth was not independently verified in this translation review. They are not translation omissions or drift and do not create new approval holds. Organic Halloween owner reservation is archived per root clarification; no owner hold applied.','limits':['HTML attribute text is preserved exactly as required, including existing English alt/title strings. Scope covers visible body text nodes.','Existing incomplete English product-title fragments and quoted garment slogans/brands are preserved or appropriately localized; no missing suffix facts invented.','Raw export binding proves the frozen source/before snapshot, not current live state. Root owns current guards, registration, main integration and public verification.'],'inputCandidateFiles':selection['candidateFiles'],'checksFile':'correction_proposals.json','qualifiedReleaseIndex':'qualified_release_index.json','externalWrites':False,'originalAuthorCandidatesModified':False}
write('independent_review.json',review)
outputs=['qualified_unchanged_rows.json','corrected_proposed_rows.json','reviewed_all_55_proposed.json','qualified_release_index.json','correction_proposals.json','independent_review.json']
write('MANIFEST.json',{'status':'COMPLETE_LOCAL_INDEPENDENT_REVIEW','selectedBodies':55,'unchangedBodies':49,'correctedProposedBodies':6,'rootIntegrationIndex':'qualified_release_index.json','files':[{'file':x,'SHA256':fsha(P/x)}for x in outputs]})
print({'status':review['status'],'selected':55,'unchanged':49,'corrected':6,'rules':len(proposals),'occurrences':sum(x['expectedOccurrences']for x in proposals),'allChecksPass':all(not c['structure']['errors']for c in checks)})
