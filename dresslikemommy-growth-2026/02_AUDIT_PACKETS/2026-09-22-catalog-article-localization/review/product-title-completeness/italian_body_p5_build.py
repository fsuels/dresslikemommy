import json,pathlib,re,hashlib
P=pathlib.Path(__file__).resolve().parent;PACK=P.parent.parent
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
r=json.loads((P/'worklist_ar.json').read_text())['rows'][5];raw=PACK/r['rawFile'];node=next(n for n in json.loads(raw.read_text())['data']['translatableResourcesByIds']['nodes']if n['resourceId']==r['resourceId']);source=next(x for x in node['translatableContent']if x['key']=='body_html');before=next(x for x in node['tr_it']if x['key']=='body_html')
rules=[
('Design elegante con scollo alto:','Elegante design a collo alto con allacciatura dietro il collo:','Elegant High-Neck Halter Design:',1),
('top allacciato a collo alto','top a collo alto con allacciatura dietro il collo','high-neck halter top swimsuits',1),
('i pantaloni a vita alta','gli slip a vita alta','The high-waisted bottoms',1),
('Cravatta regolabile:','Laccio regolabile dietro il collo:','Adjustable Neck Tie:',1),
('la cravatta regolabile','il laccio regolabile dietro il collo','the adjustable neck tie',1),
('con scollo alto e scollo alto','a collo alto con allacciatura dietro il collo','High-Neck Halter Swimsuit Set',2),
('Il top allacciato al collo','Il top a collo alto con allacciatura dietro il collo','The high-neck halter top',1),
('Abbinato a pantaloni a vita alta','Abbinato a slip a vita alta','Paired with high-waisted bottoms',1),
('Il laccio regolabile della cavezza','Il laccio regolabile dietro il collo',"The halter's adjustable tie",1)
]
value=before['value'];evidence=[]
for old,new,quote,count in rules:
 assert value.count(old)==count,(old,value.count(old));assert quote in source['value'],quote
 value=value.replace(old,new);evidence.append({'beforeText':old,'afterText':new,'occurrences':count,'exactEnglishSourceQuote':quote})
candidate={'resourceId':r['resourceId'],'locale':'it','key':'body_html','marketId':None,'sourceValue':source['value'],'source':source['value'],'sourceDigest':source['digest'],'sourceSHA256':sha(source['value']),'before':before,'expectedBeforeValueSHA256':sha(before['value']),'value':value,'valueSHA256':sha(value),'rawFile':r['rawFile'],'rawFileSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'reason':'Repair public-observed Italian neck-tie/animal-halter/bikini-bottom mistranslations and duplicated high-neck wording against exact English; preserve every HTML token, link, image, measurement, and all other text.','requiresFreshLiveSourceAndBeforeGuard':True,'changes':evidence,'inheritedSourceLimitations':['Raw Italian before already contains malformed translated table tags and a duplicate source fallback chart; unchanged by this bounded text-only patch.','Fallback chart headings retain English in raw before; separate existing repair state belongs to root.'],'independentMeaningReview':'PENDING'}
tags=lambda s:re.findall(r'<[^>]*>',s)
nums=lambda s:re.findall(r'\d+(?:[.,]\d+)?',re.sub('<[^>]*>',' ',s))
checks={'sourceDigestAndSHA':source['digest']==sha(source['value']),'exactRawBefore':candidate['before']==before,'tagsAttributesCommentsIdenticalToBefore':tags(value)==tags(before['value']),'allNumbersIdenticalToBefore':nums(value)==nums(before['value']),'tableTailIdenticalToBefore':value[value.index('<table'):]==before['value'][before['value'].index('<table'):],'substitutions':sum(x['occurrences']for x in evidence),'newTextOnlyChangedAtNineExactRules':True,'freshLiveReadback':'NOT_RUN_SUBAGENT_LOCAL_ONLY','independentFullNodeMeaningReview':'PENDING'}
f=P/'italian_body_p5_candidate.json';f.write_text(json.dumps([candidate],ensure_ascii=False,indent=2)+'\n');checks['candidateSHA256']=hashlib.sha256(f.read_bytes()).hexdigest();(P/'italian_body_p5_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');print(json.dumps(checks))
