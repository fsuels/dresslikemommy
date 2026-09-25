from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json
P=Path(__file__).resolve().parent;R=P.parent.parent
files=['retained_short72_candidate.json','retained_body24_candidate.json','held_ru_sv36_candidate.json','held_old15_candidate.json','held_nochart5_candidate.json','held_sunshine16_candidate.json']
def key(r):return r['resourceId'],r['locale'],r['key']
expected={key(r) for f in ['retained96_worklist.json','translation_only_held_worklist.json'] for r in json.loads((P/f).read_text())['rows']}
base={key(r):r for r in json.loads((R/'products/remaining/baseline.json').read_text())['rows']}
excluded={key(r) for f in ['qualified_product_release_index.json','root_product_release_rows.json','german_title_correction_proposals.json'] for r in json.loads((R/'review'/f).read_text())['rows']}
rows=[];seen=set();checks=[]
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
for name in files:
 for r in json.loads((P/name).read_text())['rows']:
  k=key(r);assert k not in seen and k not in excluded;seen.add(k)
  b=base[k];assert r['sourceValue']==b['source'] and all(r[z]==b[z] for z in ['resourceId','locale','key','sourceDigest','before'])
  assert r['marketId'] is None
  assert r['before'] is None or (r['before']['locale']==r['locale'] and r['before'].get('market') is None)
  check=v.verify_text(r['sourceValue'],r['value'],r['locale']);assert not check['errors'],(k,check)
  rows.append(r);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'artifact':name,'sourceBeforeBinding':'PASS','sourcePreservation':check})
assert seen==expected and len(rows)==168
write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
write('complete168_candidates.json',{'status':'AUTHOR_REVIEW_COMPLETE_ROOT_INDEPENDENT_REVIEW_AND_LIVE_GUARDS_REQUIRED','rows':rows})
write('complete168_checks.json',{'fields':checks,'missingKeys':0,'duplicateKeys':0,'qualified7887Overlap':0,'sourceBindingFailures':0,'preservationFailures':0})
write('manifest.json',{'scope':'918 original held fields plus96 retained outdated fields; four German already-corrected holds and all7887 qualified keys excluded.','authorCandidateCount':168,'retainedReview':{'fields':96,'identicalEquivalentRefreshesInFrozenAuthorVersion':35,'correctionsInFrozenAuthorVersion':61,'rootOverrideNote':'Root separately selected broader type wording for15 fields; do not override root selected copies or treat these frozen originals as latest integration choices.'},'repairedOriginalHolds':72,'remainingSourceDispositions':846,'countsByKey':dict(Counter(r['key'] for r in rows)),'files':[{'path':n,'rows':len(json.loads((P/n).read_text())['rows']),'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in files],'sourceDecisionEvidence':'source_disposition_worklist.json','releaseBoundary':'No external writes, current-source API reads, publication, Git operations or public verification performed by this lane. Root owns independent review, selected corrections, live guards and main/live release.'})
print(json.dumps({'rows':len(rows),'exactCoverage':True,'noOverlap':True,'allPreservationPass':True,'remainingSourceDispositions':846}))
