from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).parent;PACK=P.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fsha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
names=['product60','product20','product16','article16'];rows=[];index=[];corrections=[];checks=[];boundary=[]
for name in names:
 f=P/f'{name}_reviewed_candidates.json';rr=json.loads(f.read_text())['rows'];cc=json.loads((P/f'{name}_corrections.json').read_text())['rules'];corrections+=cc
 rawchecks=json.loads((P/f'{name}_checks.json').read_text())['rows'];assert all(not r['errors']for r in rawchecks)
 for r,c in zip(rr,rawchecks):
  assert fsha(PACK/c['candidateFile'])==c['candidateFileSHA256'];assert fsha(PACK/c['rawFile'])==c['rawFileSHA256'];assert sha(r.get('sourceValue',r.get('source')))==c['sourceSHA256'];assert sha(r['value'])==r['valueSHA256']
  original=json.loads((P/f'{name}_candidates_frozen_copy.json').read_text())['rows'][len([x for x in index if x['batch']==name])]
  assert r['before']==original['before'];assert r['sourceDigest']==original['sourceDigest'];assert re.findall('<[^>]+>',r['value'])==re.findall('<[^>]+>',original['value'])
  # Ensure translation repairs do not introduce new run-together adjacent inline
  # boundaries: for every changed text token preserve leading/trailing whitespace.
  ta=re.split(r'(<[^>]+>)',original['value']);tb=re.split(r'(<[^>]+>)',r['value']);assert len(ta)==len(tb)
  for a,b in zip(ta,tb):
   if a==b or a.startswith('<'):continue
   assert re.match(r'^\s*',a).group()==re.match(r'^\s*',b).group();assert re.search(r'\s*$',a).group()==re.search(r'\s*$',b).group()
  changed=r['value']!=original['value'];index.append({'batch':name,'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'sourceSHA256':c['sourceSHA256'],'beforeValueSHA256':c['beforeSHA256'],'valueSHA256':r['valueSHA256'],'candidateFile':str(f.relative_to(PACK)),'candidateFileSHA256':fsha(f),'candidateRowIndex':len([x for x in index if x['batch']==name]),'authorCandidateFile':c['candidateFile'],'authorCandidateFileSHA256':c['candidateFileSHA256'],'rawFile':c['rawFile'],'rawFileSHA256':c['rawFileSHA256'],'disposition':'QUALIFIED_WITH_EXACT_CORRECTIONS'if changed else'QUALIFIED_UNCHANGED','requiresFreshLiveSourceAndBeforeGuard':True});rows.append(r)
assert len(rows)==112 and len({(r['resourceId'],r['locale'],r['key'])for r in rows})==112
write('qualified_release_index.json',{'status':'112_INDEPENDENTLY_REVIEWED_QUALIFIED_CANDIDATES','rows':index});write('product96_reviewed_candidates.json',{'status':'96_INDEPENDENTLY_REVIEWED_PRODUCT_BODIES','rows':[r for r in rows if '/Product/'in r['resourceId']]})
write('MANIFEST.json',{'status':'COMPLETE_LOCAL_INDEPENDENT_REVIEW','productBodies':96,'articleBodies':16,'totalBodies':112,'sourceBeforeDigestRawMarkupNumericChecks':'PASS_ALL112','unchangedRows':sum(r['disposition']=='QUALIFIED_UNCHANGED'for r in index),'correctedProductRows':sum(r['disposition']!='QUALIFIED_UNCHANGED'and'/Product/'in r['resourceId']for r in index),'correctedArticleRows':sum(r['disposition']!='QUALIFIED_UNCHANGED'and'/Article/'in r['resourceId']for r in index),'productCorrectionOccurrences':sum('/Product/'in r['resourceId']for r in corrections),'articleCorrectionOccurrences':sum('/Article/'in r['resourceId']for r in corrections),'files':[{ 'file':str((P/f'{n}_reviewed_candidates.json').relative_to(PACK)),'sha256':fsha(P/f'{n}_reviewed_candidates.json'),'rows':len(json.loads((P/f'{n}_reviewed_candidates.json').read_text())['rows'])}for n in names]+[{'file':str((P/'product96_reviewed_candidates.json').relative_to(PACK)),'sha256':fsha(P/'product96_reviewed_candidates.json'),'rows':96},{'file':str((P/'qualified_release_index.json').relative_to(PACK)),'sha256':fsha(P/'qualified_release_index.json'),'rows':112}],'scope':'Original frozen author candidates, current English source, and all external systems untouched. Parent is sole integration/Git/live-write owner. Existing source-policy dispositions belong to parent; no new approval gates introduced.','correctionFiles':[str((P/f'{n}_corrections.json').relative_to(PACK))for n in names]})
print(json.dumps({k:v for k,v in json.loads((P/'MANIFEST.json').read_text()).items()if k not in['files','scope','correctionFiles']},indent=2))
