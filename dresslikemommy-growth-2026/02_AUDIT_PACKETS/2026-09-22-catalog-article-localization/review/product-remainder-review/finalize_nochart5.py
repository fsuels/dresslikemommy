# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,html,importlib.util,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
rows=[r for r in json.loads((P/'translation_only_held_worklist.json').read_text())['rows'] if r['priorHoldArtifact']=='body_source_holds.json']
manual={}
for line in (P/'nochart_manual.tsv').read_text().splitlines():
 locale,index,value=line.split('\t',2)
 if locale=='ja':value=value.replace('4つ','四つ').replace('1つ','一つ')
 manual[locale,int(index)]=value
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
out=[];checks=[]
for r in rows:
 parts=re.split('(<[^>]*>)',r['source']);n=0
 for i,old in enumerate(parts):
  if not old.strip() or old.startswith('<'):continue
  val=manual[r['locale'],n];n+=1;lead=old[:len(old)-len(old.lstrip())];trail=old[len(old.rstrip()):];parts[i]=lead+html.escape(val,quote=False)+trail
 assert n==26
 value=''.join(parts);check=v.verify_text(r['source'],value,r['locale']);assert not check['errors'],(r['locale'],check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']};rr.update(sourceValue=r['source'],value=value,marketId=None,reason='Translate complete current source body and remove the obsolete translated-only chart by reconstructing the source HTML exactly. Preserve separate-item selection, included/excluded pieces, all sizes and care.',independentReview='FULL_AUTHOR_REVIEW_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'meaning':'FULL_SOURCE_AUTHOR_REVIEW_PASS','sourcePreservation':check,'allSourceNodes':26,'sourceSHA256':hashlib.sha256(r['source'].encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest()})
for name,data in [('held_nochart5_candidate.json',{'rows':out}),('held_nochart5_checks.json',{'fields':checks,'limit':'Complete translation from supplied current English source; no source facts edited. Root owns live freshness, independent review and publication.'})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'preservationFailures':0}))
