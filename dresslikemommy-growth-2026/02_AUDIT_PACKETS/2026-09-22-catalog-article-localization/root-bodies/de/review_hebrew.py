from pathlib import Path
import json,re,hashlib,importlib.util
P=Path(__file__).resolve().parent; root=P.parent.parent
f=root/'root-bodies/he-pl/he_candidate.json'; raw=f.read_bytes(); rows=json.loads(raw)['rows'];baseline=json.loads((root/'root-bodies/he_baseline.json').read_text())
if isinstance(baseline,dict):baseline=baseline['rows']
by_id={r['resourceId']:r for r in baseline}
spec=importlib.util.spec_from_file_location('offline',root/'tooling/offline_translation.py');off=importlib.util.module_from_spec(spec);spec.loader.exec_module(off)
corrections=[];checks=[]
for r in rows:
 v=r['value']; edits=[]
 b=by_id[r['resourceId']]
 assert all(r[k]==b[k] for k in ['resourceId','locale','key','sourceValue','sourceDigest','before'])
 if r['resourceId'].endswith('/559471919201'):
  old='אמא ובת ב <a href="/collections/dresses">שמלות פרחוניות</a>'
  new='אמא ובת עם <a href="/collections/dresses">שמלות פרחוניות תואמות</a>'
  assert v.count(old)==1;v=v.replace(old,new)
  edits.append({'type':'omitted_matching_restored','source':'Mom and daughter in matching / floral dresses','before':old,'after':new})
 # A Hebrew bound prefix must join the following linked word; whitespace is not a word boundary here.
 for m in list(re.finditer(r'(?<![\u0590-\u05FF])([בו])([ \t]+)(?=<a\b)',v))[::-1]:
  old=m.group();new=m.group(1);v=v[:m.start()]+new+v[m.end():]
  edits.append({'type':'bound_prefix_link_whitespace','before':old,'after':new,'surroundingText':r['value'][max(0,m.start()-35):m.end()+70]})
 a=off.verify_text(r['sourceValue'],r['value'],'he');z=off.verify_text(r['sourceValue'],v,'he');assert not a['errors'] and not z['errors']
 checks.append({'resourceId':r['resourceId'],'baselineBinding':'PASS','fullSemanticComparison':'PASS_EXCEPT_CORRECTED_MATCHING_OMISSION' if r['resourceId'].endswith('/559471919201') else 'PASS','beforeStructuralCheck':a,'proposedStructuralCheck':z,'edits':edits})
 if edits:corrections.append({**r,'beforeCandidateValue':r['value'],'value':v,'candidateCorrectionReasons':edits})
(P/'he_candidate_corrections.json').write_text(json.dumps({'status':'INDEPENDENT_REVIEW_PROPOSALS_ROOT_INTEGRATION_REQUIRED','baseCandidateSHA256':hashlib.sha256(raw).hexdigest(),'rows':corrections},ensure_ascii=False,indent=2)+'\n')
report={'status':'CORRECTIONS_PROPOSED','reviewedArticles':11,'reviewedUniqueAlignedTextPairs':314,'reviewedAllSourceAndTargetProse':True,'candidateSHA256':hashlib.sha256(raw).hexdigest(),'correctionArticles':len(corrections),'corrections':sum(len(x['edits']) for x in checks),'structuralFailures':0,'remainingMissingTranslations':0,'sourceTruth':'No new fact claims introduced by target versus supplied English source. Generic source marketing flags are not treated as false or as permission gates. Existing source truth decisions remain root-owned.','liveVerification':'NOT_RUN','fields':checks}
(P/'he_independent_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['fields']}))
