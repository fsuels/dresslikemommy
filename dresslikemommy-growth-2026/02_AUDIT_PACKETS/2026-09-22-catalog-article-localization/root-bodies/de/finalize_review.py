from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
import json,hashlib,re,importlib.util
P=Path(__file__).resolve().parent; root=P.parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
rows=json.loads((P/'candidate_all_complete.json').read_text())['rows'];baseline=json.loads((P.parent/'de_baseline.json').read_text());inventory=json.loads((root/'articles/inventory.json').read_text())
spec=importlib.util.spec_from_file_location('offline',root/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[]
for r,b in zip(rows,baseline):
 assert all(r[k]==b[k] for k in ['resourceId','locale','key','sourceValue','sourceDigest','before'])
 assert r['locale']=='de' and r['key']=='body_html'
 result=m.verify_text(r['sourceValue'],r['value'],'de');assert not result['errors']
 checks.append({'resourceId':r['resourceId'],'locale':'de','key':'body_html','sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['sourceValue'].encode()),'valueSHA256':sha(r['value'].encode()),'baselineBinding':'PASS','structuralCheck':result,'sourceClaimFlagCount':len(r['sourceClaimReview']),'authorLanguageReview':'PASS_FULL_TEXT_NODES_AND_ASSEMBLED_LINK_JOIN_REVIEW'})
assert len(rows)==57
write('final_field_checks.json',{'status':'PASS_AUTHOR_AND_OFFLINE_STRUCTURE','count':57,'fields':checks})
(P/'final_batches').mkdir(exist_ok=True)
for start in range(0,len(rows),5):
 i=start//5+1
 write('final_batches/batch_'+str(i).zfill(2)+'.json',{'status':'AUTHOR_REVIEWED_PARENT_REVIEW_REQUIRED','rows':rows[start:start+5]})
 write('final_batches/checks_'+str(i).zfill(2)+'.json',checks[start:start+5])
# Supersede early first-batch draft with the author-reviewed assembled version.
write('candidate_batch_01.json',{'status':'AUTHOR_REVIEWED_PARENT_REVIEW_REQUIRED','rows':rows[:5]})
write('checks_batch_01.json',checks[:5])
clock={'inventoryObservedAt':inventory.get('observedAt'),'baselineSnapshotPath':str(P.parent/'de_baseline.json'),'baselineSHA256':sha((P.parent/'de_baseline.json').read_bytes()),'baselineFileModifiedAt':datetime.fromtimestamp((P.parent/'de_baseline.json').stat().st_mtime,timezone.utc).isoformat(),'candidateReviewedAt':datetime.now(timezone.utc).isoformat(),'freshness':'Offline source-bound candidate only; root must verify current source/digest/before/publication before mutation.'}
write('source_clocks.json',clock)
write('author_review.json',{'status':'PASS_AUTHOR_REVIEW_NOT_INDEPENDENT_OR_LIVE','locale':'de','articleBodies':57,'distinctSourceTextNodes':1241,'manualNodes':975,'exactTemplateNodes':266,'checks':'All source text translated without summaries; HTML events and attributes, links, numbers, units and source baseline binding verified for every field. Reviewed concatenated prose; corrected two inline-link spaces, singular dress agreement, one resource-specific adjective case, and nested quote typography. Brand names and literal garment slogans retain English where source identifies printed designs.','sourceClaimFlags':'Retained exactly as review annotations, not automatically treated as false or as permission gates. Parent owns pending source-truth resolution and release choice.','sourceClaimAnnotatedArticles':sum(bool(r['sourceClaimReview']) for r in rows),'independentReview':'NOT_RUN_BY_AUTHOR','liveWrites':0,'providerCalls':0,'gitWrites':0,'sourceClocks':clock})
manifest={str(f.relative_to(P)):sha(f.read_bytes()) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='manifest_sha256.json'}
write('manifest_sha256.json',manifest)
print(json.dumps({'articles':57,'checksFailed':sum(bool(x['structuralCheck']['errors']) for x in checks),'batches':12,'claimAnnotated':sum(bool(r['sourceClaimReview']) for r in rows),'files':len(manifest)}))
