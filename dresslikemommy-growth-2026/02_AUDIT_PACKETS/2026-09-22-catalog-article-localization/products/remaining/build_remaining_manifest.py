#!/usr/bin/env python3
import collections,hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
def rows(file):
 d=json.loads((HERE/file).read_text());return d['rows'] if isinstance(d,dict) else d
def k(r):return(r['resourceId'],r['locale'],r['key'])
def sha(file):return hashlib.sha256((HERE/file).read_bytes()).hexdigest()
base=rows('baseline.json');body=rows('body_baseline.json');covered={};artifacts=[]
def add(file,status,subset=None):
 rr=rows(file);rr=rr if subset is None else [r for r in rr if subset(r)]
 artifacts.append({'path':file,'sha256':sha(file),'fields':len(rr),'status':status})
 for r in rr:
  ident=k(r)
  if ident in covered:raise ValueError(('overlapping dispositions',ident,file,covered[ident]))
  covered[ident]={'resourceId':ident[0],'locale':ident[1],'key':ident[2],'status':status,'artifact':file}
superseded={'blue_daisy_a_candidate.json','blue_daisy_b_candidate.json','blue_daisy_c_candidate.json','russian_body_label_fixes_candidate.json','swim_body_batch_1_candidate.json','option_misc_candidate.json','titles_000_067_candidate.json','titles_068_135_candidate.json','ordinary_meta_titles_candidate.json'}
review_receipts=[]; reviewed_files=set()
for name in ['sv_final_independent_review.json','ru_final_independent_review.json','sv-bodies/blue_daisy_independent_review_v2.json','ru-bodies/other_body_independent_review_v2.json','ru-bodies/option_fields_independent_review_v2.json','sv-bodies/short_fields_independent_review_v2.json']:
 d=json.loads((HERE/name).read_text());assert d['status'].startswith('PASS_WITH_LIMITS'), (name,d['status'])
 for f in d.get('files',[{'path':d.get('candidateFile'),'sha256':d.get('candidateSHA256')}]):
  p=pathlib.Path(f['path']);p=p if p.is_absolute() else HERE/p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],str(p)
  reviewed_files.add(str(p.relative_to(HERE)))
 review_receipts.append({'path':name,'sha256':sha(name),'status':d['status']})
selected=sorted({p.name for p in HERE.glob('*_candidate.json')} - superseded)
selected += sorted(f.replace('_candidate.json','_candidate_v2.json') for f in superseded)
for name in selected:
 f=HERE/name
 if f.name=='body_label_partial_candidates.json':continue
 assert f.name in reviewed_files,f.name
 add(f.name,'INDEPENDENT_REVIEW_PASS_REQUIRES_LIVE_GUARDS')
for f in ['titles_068_135_no_change.json','other_titles_no_change.json','product_types_no_change.json','option_misc_no_change.json','meta_titles_no_change.json']:
 add(f,'REVIEWED_NO_CHANGE')
for f in ['titles_000_067_held.json','titles_068_135_held.json','source_claim_holds.json','meta_titles_source_holds.json','body_source_holds.json','body_construction_source_holds.json','older_stale_table_holds.json','changed_source_chart_holds.json']:
 add(f,'PRECISE_SOURCE_OR_TABLE_HOLD')
add('older_stale_bodies_dispositions.json','REVIEWED_NO_CHANGE',lambda r:r['disposition']=='NO_LANGUAGE_REPAIR_REQUIRED')
add('ru-bodies/release_ready_for_peer_review.json','INDEPENDENT_REVIEW_PASS_REQUIRES_LIVE_GUARDS')
add('sv-bodies/qualified_candidates.json','INDEPENDENT_REVIEW_PASS_REQUIRES_LIVE_GUARDS')
add('ru_body_final_holds.json','PRECISE_SOURCE_OR_TABLE_HOLD')
add('sv_body_final_holds.json','PRECISE_SOURCE_OR_TABLE_HOLD')
add('short_fields_review_holds.json','PRECISE_SOURCE_OR_TABLE_HOLD')
add('ru_body_final_no_change.json','REVIEWED_NO_CHANGE')
missing=[r for r in base if k(r) not in covered];extra=[v for ident,v in covered.items() if ident not in set(map(k,base))]
assert not missing, len(missing)
result={'status':'COMPLETE_FIELD_DISPOSITION_LOCAL_CANDIDATES_ONLY','scope':'Original 2902 remaining flags plus explicitly discovered linked/review fields. All selected candidates have independent meaning review; release owner must guard fresh source/current value. Frozen first 5988-field cohorts excluded.','originalBaselineFields':len(base),'originalDispositionCounts':dict(collections.Counter(covered[k(r)]['status'] for r in base if k(r) in covered)),'originalUncoveredCount':len(missing),'uncovered':[{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourcePreview':r['source'][:180]} for r in missing],'extraDiscoveredFields':extra,'artifacts':artifacts,'independentReviewReceipts':review_receipts,'fieldLedger':sorted(covered.values(),key=lambda r:k(r)),'limits':['No live or source writes made by this candidate-preparation lane.','No ads, negatives, prices, handles, inventory, English source or Git mutations.','Every original field has a candidate, reviewed no-change classification, or exact source/table hold. No-change does not assert a live mutation or clearing Shopify outdated metadata.','Independent reviews bind final selected versions. Source claims and chart accuracy are not independently seller-verified; holds remain excluded.','Superseded original candidate artifacts remain preserved; only selected filenames in this manifest are current.']}
f=HERE/'remaining_manifest.json';f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print({x:result[x] for x in ['originalBaselineFields','originalDispositionCounts','originalUncoveredCount','uncovered']});print('extra',len(extra),'artifacts',len(artifacts))
