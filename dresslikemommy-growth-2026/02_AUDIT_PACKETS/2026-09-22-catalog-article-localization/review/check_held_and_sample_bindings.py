#!/usr/bin/env python3
"""Independent frozen hold binding and sample manifest only; no external writes."""
from pathlib import Path
import hashlib,json,collections
H=Path(__file__).resolve().parent;P=H.parent;R=P/'products/remaining';B=P/'products'
def read(p):return json.loads(p.read_text())
def key(r):return r['resourceId'],r['locale'],r['key']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base={key(r):r for r in read(R/'baseline.json')['rows']};manifest=read(R/'remaining_manifest.json');cache={};bindings=[]
for entry in manifest['fieldLedger']:
 if entry['status']!='PRECISE_SOURCE_OR_TABLE_HOLD':continue
 r=base[key(entry)];p=B/r['rawFile']
 if p not in cache:cache[p]={n['resourceId']:n for n in read(p)['data']['translatableResourcesByIds']['nodes']}
 n=cache[p][r['resourceId']];s=next(s for s in n['translatableContent'] if s['key']==r['key'] and s['locale']=='en')
 assert s['value']==r['source'] and s['digest']==r['sourceDigest']
 before=[]
 for a,ts in n.items():
  if a.startswith('tr_'):
   for t in ts:
    if t['key']==r['key'] and t['locale']==r['locale'] and t.get('market') is None and t not in before:before.append(t)
 assert len(before)<=1 and (before[0] if before else None)==r['before']
 bindings.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':s['digest'],'rawFile':str(p.relative_to(P)),'rawSHA256':sha(p),'holdEvidence':str((R/entry['artifact']).relative_to(P)),'holdEvidenceSHA256':sha(R/entry['artifact']),'bindingReviewCode':'EXACT_SOURCE_DIGEST_EXPLICIT_LOCALE_GLOBAL_BEFORE_PASS'})
assert len(bindings)==918
rows=read(R/'prepared_remaining_candidates.json')['rows'];seen=set();sample=[]
for r in rows:
 if r['key']=='body_html':continue
 k=(r['preparedArtifact'],r['locale'])
 if k in seen:continue
 seen.add(k);sample.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'source':r['source'],'value':r['value'],'candidateFile':r['preparedArtifact'],'candidateFileSHA256':r['preparedArtifactSHA256'],'verdict':'MEANING_SAMPLE_PASS'})
assert len(sample)==122
res={'status':'PASS_WITH_LIMITS','heldFrozenSourceBeforeBindingFields':918,'sampledMeaningPairs':122,'sampleRule':'First nonbody row for each selected final artifact/locale pair, including all 20 locales and known cream/color/type risks. Every listed source/value pair manually read by independent reviewer.','samples':sample,'heldBindings':bindings,'limits':['Sample review supplements, not replaces, the six full independent meaning receipts for the final 1899 remaining fields.','No cached_cohort_candidate or remaining_cached_candidates file is authorized by this evidence; only selected final candidate filenames and exact hashes in the qualified index.','The hold itself may be source ambiguity, a demonstrated mismatch or a claim review trigger; it is not automatically proof the source is false.','Frozen baseline binding is not a fresh live source check.']}
(H/'held_bindings_and_meaning_samples.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print({'heldBindings':len(bindings),'meaningSamples':len(sample),'status':'PASS'})
