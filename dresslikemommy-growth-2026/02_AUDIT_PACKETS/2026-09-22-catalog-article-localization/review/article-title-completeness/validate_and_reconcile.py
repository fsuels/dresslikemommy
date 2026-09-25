import json,hashlib,re
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent;B=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fsha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((H/'inventory.json').read_text());rows=inv['rows'];cand=json.loads((H/'candidates_all.json').read_text())['rows'];byid={r['auditId']:r for r in rows};bycand={r['auditId']:r for r in cand}
assert len(rows)==len({(r['resourceId'],r['locale'],r['key']) for r in rows})==1340
assert Counter(r['locale'] for r in rows)=={x:67 for x in inv['locales']} and len(inv['locales'])==20
assert len({r['resourceId'] for r in rows})==67
b1=json.loads((H/'candidate_batch_01.json').read_text())['rows'];b2=json.loads((H/'candidate_batch_02.json').read_text())['rows'];assert b1+b2==cand
rawcache={};checks=[]
for r in rows:
 p=B/r['rawFile'];assert fsha(p)==r['rawFileSHA256']
 if p not in rawcache:rawcache[p]=json.loads(p.read_text())
 n=next(n for n in rawcache[p]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId'])
 s=next(x for x in n['translatableContent'] if x['key']=='title');assert s['value']==r['source'] and s['digest']==r['sourceDigest']
 old=[t for t in n['translations'] if t['key']=='title' and t['locale']==r['locale'] and not t.get('market')]
 assert len(old)<=1 and (old[0] if old else None)==r['before']
 assert r['effectiveValue'] is not None
 if r.get('rootAppliedOverlay'):
  prov=r['rootAppliedOverlay'];assert fsha(B/prov['file'])==prov['fileSHA256']
  match=[c for c in json.loads((B/prov['file']).read_text()) if c['resourceId']==r['resourceId'] and c['locale']==r['locale'] and c['key']=='title']
  assert len(match)==1 and match[0]['value']==r['effectiveValue'] and match[0]['sourceDigest']==r['sourceDigest']
 c=bycand.get(r['auditId'])
 if c:
  assert c['source']==r['source'] and c['sourceDigest']==r['sourceDigest'] and c['sourceSHA256']==sha(r['source'])
  assert c['before']['value']==r['effectiveValue'] and c['expectedBeforeValueSHA256']==sha(r['effectiveValue'])
  assert c['valueSHA256']==sha(c['value']) and c['value']!=r['effectiveValue']
  assert re.findall(r'\d+',c['source'])==re.findall(r'\d+',c['value']) or (c['auditId']==813 and 'January' in c['source'] and c['value'].startswith('1월') and re.findall(r'\d+',c['value'])==['1'])
  assert '<' not in c['value'] and '>' not in c['value'] and '\n' not in c['value'] and '_' not in c['value']
 checks.append({'auditId':r['auditId'],'resourceId':r['resourceId'],'locale':r['locale'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(r['source']),'frozenBeforeSHA256':sha(r['before']['value']) if r['before'] else None,'effectiveBeforeSHA256':sha(r['effectiveValue']),'effectiveBeforeOrigin':'ROOT_APPLIED_OVERLAY' if r.get('rootAppliedOverlay') else ('SUCCESSFUL_RECEIPT' if r['appliedReceipts'] else 'FROZEN_RAW'),'candidateSHA256':sha(c['value']) if c else None,'binding':'PASS'})
classes={
'MIXED_ENGLISH': [202,206,208,210,214,218,220,223,230,231,237,239,240,263,277,287,675,717,876,880,883,887,903,918,1010,1084],
'CORRUPTED_TOKEN':[1,4,7,805,808,811],
'FALSE_CUSTOM_MADE_OR_GARMENT_SHAPE':[72,120,819,846,861],
'INCORRECT_HOLIDAY_OR_HOLIDAY_VACATION':[188,298,318,817,848,992,1126],
'SWIMWEAR_CATEGORY_TOO_NARROW':[137,179,447,916,941,983,1075,1117],
'WRONG_WORD_OR_MEANING':[2,5,13,149,158,255,270,276,279,282,285,301,303,306,310,319,322,331,364,365,438,455,488,547,572,598,600,608,627,631,636,644,665,732,748,813,836,898,932,933,976,1175,1201,1211],
'OMITTED_TITLE_MEANING':[]}
assigned={i:cat for cat,ids in classes.items() for i in ids}
ledger=[]
for r in rows:
 c=bycand.get(r['auditId']);cl=assigned.get(r['auditId'],'OMITTED_TITLE_MEANING') if c else 'RETAINED_FAITHFUL_OR_NORMAL_TARGET_LANGUAGE_TERM'
 ledger.append({'auditId':r['auditId'],'resourceId':r['resourceId'],'locale':r['locale'],'source':r['source'],'reviewedValue':r['effectiveValue'],'status':'CORRECTION_AUTHORED_PENDING_INDEPENDENT_REVIEW' if c else 'MANUALLY_READ_RETAINED','findingClass':cl,'proposedValue':c['value'] if c else None,'effectiveBeforeSHA256':sha(r['effectiveValue']),'candidateSHA256':sha(c['value']) if c else None})
report={'status':'PASS_SOURCE_BINDINGS_AND_COMPLETE_AUTHOR_REVIEW_PENDING_INDEPENDENT_MEANING','publishedArticles':67,'publishedNonEnglishLocales':20,'titleTuples':1340,'authorManualReadTuples':1340,'correctionCandidates':len(cand),'retained':1340-len(cand),'byLocale':[{'locale':l,'reviewed':67,'corrections':sum(c['locale']==l for c in cand),'retained':67-sum(c['locale']==l for c in cand)} for l in inv['locales']],'appliedTitleRepairsReconciled':sum(bool(r['appliedReceipts']) or bool(r.get('rootAppliedOverlay')) for r in rows),'newCorrectionsUsingAppliedValueAsBefore':sum(c['effectiveBeforeProvenance'].get('file','').startswith(('releases/','review/article_titles_applied','articles/short_fields_01_receipts')) for c in cand),'candidateFileSHA256':fsha(H/'candidates_all.json'),'inventoryFileSHA256':fsha(H/'inventory.json'),'candidateMaxCharacters':max(len(c['value']) for c in cand),'numericSemanticException':{'auditId':813,'source':'January','target':'1월','meaning':'Exact localized month; no added measurement/year/quantity'},'findingClasses':dict(Counter(r['findingClass'] for r in ledger if r['proposedValue'])),'boundaries':['English source unchanged. No provider/API/browser/Git/canonical writes.','Existing candidate/applied repair values were reconciled against root overlay and saved successful receipts; any correction of an already repaired title is bound to its applied value, never its outdated raw value.','Ordinary target-language fashion loans and recognizable holiday names such as Black Friday, Halloween and Thanksgiving are retained. Mommy and Me is not treated as an immutable brand where mixed untranslated phrasing remains.','Coverage is title key only; body, excerpt, SEO title and live rendering are separate scopes.','Fresh live source/digest/before/publication guards and independent meaning review required before root release. Current-source title-safe repairs are not held solely on body source-policy metadata.'],'rows':checks}
(H/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(H/'coverage_ledger.json').write_text(json.dumps({'status':'ALL1340_MANUALLY_READ','rows':ledger},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','correctionCandidates','retained','appliedTitleRepairsReconciled','newCorrectionsUsingAppliedValueAsBefore','candidateMaxCharacters','findingClasses']},ensure_ascii=False,indent=2))
