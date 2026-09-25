from pathlib import Path
import json,hashlib,collections,re,html
P=Path(__file__).parent;PACK=P.parents[2]
fsha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
files=['articles/short_fields_candidate_01.json','articles/short_fields_candidate_02.json','root-bodies/de/candidate_all_complete.json','root-bodies/he-pl/he_candidate.json','root-bodies/he-pl/pl_candidate_v2.json','articles/ru-bodies/candidate_all_complete.json']+[str(x.relative_to(PACK))for x in sorted((PACK/'tooling/sv-bodies').glob('final_batch_*.json'))]
# Frozen original exact key bases plus the reviewed successor variants. Later files override the same key.
files+=['review/article_release_index_final.json','root-bodies/de/pl_independently_qualified.json','root-bodies/de/ru_independently_qualified.json','root-bodies/he-pl/sv-review/qualified_release_index.json']
covered={};inputs=[]
for name in files:
 f=PACK/name;a=json.loads(f.read_text());rr=a['rows']if isinstance(a,dict)else a
 for r in rr:covered[(r['resourceId'],r['locale'],r['key'])]={'path':name,'row':r}
 inputs.append({'file':name,'SHA256':fsha(f),'rows':len(rr)})
ledger=json.loads((PACK/'articles/defect_ledger.json').read_text());uncovered=[];dispositions=[];rawcache={}
for l in ledger:
 key=(l['resourceId'],l['locale'],l['key'])
 if key in covered:
  c=covered[key];assert c['row']['sourceDigest']==l['sourceDigest']
  dispositions.append({'id':l['id'],'resourceId':l['resourceId'],'locale':l['locale'],'key':l['key'],'flags':l['flags'],'disposition':'ALREADY_PREPARED_EXACT_KEY','candidateFile':c['path'],'sourceDigest':l['sourceDigest']})
  continue
 f=PACK/'articles'/l['rawFile']
 if str(f)not in rawcache:rawcache[str(f)]=json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']
 node=next(x for x in rawcache[str(f)]if x['resourceId']==l['resourceId'])
 s=next(x for x in node['translatableContent']if x['locale']=='en'and x['key']==l['key']);tr=[x for x in node['translations']if x['locale']==l['locale']and x['key']==l['key']and x.get('market')is None]
 before=tr[0]if tr else None
 assert s['digest']==l['sourceDigest']
 assert hashlib.sha256(s['value'].encode()).hexdigest()==l['sourceSha256']
 assert (hashlib.sha256(before['value'].encode()).hexdigest()if before else None)==l['translationSha256']
 uncovered.append({'ledgerId':l['id'],'resourceId':l['resourceId'],'locale':l['locale'],'key':l['key'],'sourceValue':s['value'],'sourceDigest':s['digest'],'before':before,'rawFile':str(f.relative_to(PACK)),'rawFileSHA256':fsha(f),'flags':l['flags']})
short=[x for x in uncovered if x['key']!='body_html'];bodies=[x for x in uncovered if x['key']=='body_html'];templates=[x for x in bodies if not x['resourceId'].endswith(('559471919201','559471231073'))];other=[x for x in bodies if x not in templates]
locales=[x['locale']for x in json.loads((PACK/'articles/blogs_locales_raw.json').read_text())['data']['shopLocales']if x['published']and not x['primary']]
write('prepared_coverage.json',{'scope':'499 frozen article defect-ledger rows across all 20 published non-English locales; prepared exact keys only, not proof of live application','ledgerSHA256':fsha(PACK/'articles/defect_ledger.json'),'publishedNonEnglishLocales':locales,'preparedCoveredRows':len(dispositions),'uncoveredRows':len(uncovered),'inputs':inputs,'rows':dispositions,'countsByLocale':{loc:{'totalFlagged':sum(x['locale']==loc for x in ledger),'alreadyPrepared':sum(x['locale']==loc for x in dispositions),'uncovered':sum(x['locale']==loc for x in uncovered)}for loc in locales}})
for name,rr in [('uncovered_worklist.json',uncovered),('short_worklist.json',short),('template_body_worklist.json',templates),('other_body_worklist.json',other)]:write(name,{'rows':rr})
print({'covered':len(dispositions),'uncovered':len(uncovered),'short':len(short),'templateBodies':len(templates),'otherBodies':len(other)})
for r in short:print(r['ledgerId'],r['locale'],r['key'],repr(r['sourceValue']),repr(r['before']['value']if r['before']else None))
