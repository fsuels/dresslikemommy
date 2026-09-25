from pathlib import Path
import json,importlib.util,hashlib,collections,re
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('off',P.parents[2]/'tooling/offline_translation.py');o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
rows=json.loads((P/'candidates_complete.json').read_text())['rows'];base={r['resourceId']:r for r in json.loads((P/'baseline.json').read_text())['rows']}
source_holds={
 '7227630649441':'SOURCE_MEASUREMENT_CONFLICT: source pairs 50 kg with 100 lbs, 57.5 kg with 115 lbs, 62.5 kg with 125 lbs and 67.5 kg with 135 lbs. Preserved faithfully; requires source owner correction.',
 '7229128441953':'SOURCE_SIZE_EXTRAPOLATION_AND_REFUND_PROMISE: unpublished larger child measurements inferred from next size; unconditional swap/refund wording needs source-owner resolution. Four-role wording corrected to roles, no pack quantity invented.',
 '7497751986273':'SOURCE_PACK_QUANTITY_CONTRADICTION: says each set includes both mother and daughter, then says order one set separately for each. Source owner must confirm contents.',
 '7502791671905':'SOURCE_OPERATOR_COPY: customer body says list each SKU by its age group. Source cleanup must precede rebind; translation faithfully preserves it.'}
reports=[];ready=[];held=[]
for r in rows:
 a,b=o.Shape(r['source']),o.Shape(r['value']);bf=o.Shape(r['before']['value']) if r['before'] else None
 assert all(r[k]==base[r['resourceId']][k] for k in ['source','sourceDigest','before'])
 assert [e for e in a.events if e[0]!='comment']==[e for e in b.events if e[0]!='comment']
 assert len(a.tables)==len(b.tables)
 differences=[];numeric=[];unitdiff=[]
 af,bfacts=o.table_facts(a,'en'),o.table_facts(b,'ru')
 for ti,(at,bt) in enumerate(zip(a.tables,b.tables)):
  assert len(at['rows'])==len(bt['rows'])
  for ri,(ar,br) in enumerate(zip(at['rows'],bt['rows'])):
   assert len(ar)==len(br)
   for ci,(ac,bc) in enumerate(zip(ar,br)):
    av,bv=af[ti][ri][ci],bfacts[ti][ri][ci]
    if av!=bv:
     d={'table':ti,'row':ri,'cell':ci,'source':ac['text'],'candidate':bc['text'],'sourceNumbers':av[2],'candidateNumbers':bv[2],'sourceUnits':dict(av[3]),'candidateUnits':dict(bv[3])};differences.append(d)
     if av[2]!=bv[2] or av[4]!=bv[4]:numeric.append(d)
     elif av[3]!=bv[3]:unitdiff.append(d)
 notes=[]
 if any(e[0]=='comment' for e in a.events) and a.events!=b.events:notes.append('Only HTML comments differ from English source; all non-comment tag/attribute events equal. Existing translated comments preserved unchanged.')
 if unitdiff:notes.append('Exact header-cell review: source cm/in equals Russian см/дюйм; source kg/lbs equals Russian кг/фунты. Shared detector omits slash-separated in and plural фунты. Units semantically identical; no table number or size change waived.')
 if r['resourceId'].split('/')[-1] in ['7502770045025','7502793179233']:notes.append('Extra detected cm comes from Russian abbreviation см. meaning see in size-guide prose; not a measurement. Table facts identical.')
 blockers=[]
 if numeric:blockers.append('INHERITED_SIZE_LABEL_MISMATCH: current Russian age/size cells differ materially from current source. New translation preserves current numeric cells as mandated; cannot release unchanged table.')
 if r['resourceId'].split('/')[-1] in source_holds:blockers.append(source_holds[r['resourceId'].split('/')[-1]])
 report={'resourceId':r['resourceId'],'locale':'ru','key':'body_html','sourceDigest':r['sourceDigest'],'beforeGuard':'EXACT_LOCAL_BASELINE','valueSHA256':r['valueSHA256'],'strictSourceFindings':r['sourceComparisonFindings'],'tableCellDifferences':differences,'inheritedNumericMismatchCellCount':len(numeric),'nonCommentMarkupAndAttributes':'PASS','notes':notes,'blockers':blockers,'disposition':'HOLD' if blockers else 'AUTHOR_PASS_REQUIRES_INDEPENDENT_MEANING_REVIEW'}
 reports.append(report);(held if blockers else ready).append(r)
nochange=[]
for pid in ['7545279512673','7545279840353','7670724329569','7670744842337']:
 r=base['gid://shopify/Product/'+pid];nochange.append({k:r[k] for k in ['resourceId','locale','key','source','sourceDigest','before']}|{'disposition':'NO_ENGLISH_PROSE_GAP_NAMED_LABELS_PRESERVED','reason':'Remaining English is a product/design or collection proper name in existing Russian prose. Broader Russian meaning repairs are separate proposals.'})
for name,data in [('final_adjudication.json',{'status':'OFFLINE_AUTHOR_REVIEW_ONLY','inspected':118,'boundRowsPresentIn514RowBaseline':118,'statisticalNamedLabelRowsIncluded':2,'completeDrafts':112,'readyForIndependentReview':len(ready),'heldComplete':len(held),'noChangeNamedLabels':4,'malformedMarkupHolds':2,'reports':reports,'limitations':['No live source freshness read; root must rebind.', 'Author semantic review is not independent verification.', 'Exact existing attributes including any English alt text preserved.', 'Raw numeric table cells are preserved from before; stale source-relative age cells held explicitly.']}),('release_ready_for_peer_review.json',{'status':'AUTHOR_REVIEWED_NOT_APPLIED','rows':ready}),('held_complete_candidates.json',{'status':'DO_NOT_APPLY_PENDING_SOURCE_OR_TABLE_RESOLUTION','rows':held}),('no_change_dispositions.json',{'rows':nochange})]:
 (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'ready':len(ready),'held':len(held),'inheritedNumeric':sum(bool(r['inheritedNumericMismatchCellCount']) for r in reports),'sourceHolds':source_holds,'readySHA256':hashlib.sha256((P/'release_ready_for_peer_review.json').read_bytes()).hexdigest()}))
