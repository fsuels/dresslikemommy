from pathlib import Path
import json,hashlib,re,html,importlib.util,collections
P=Path(__file__).parent;PACK=P.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fsha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
inputs=['review/product-remainder-review/held_sunshine16_candidate.json']
rawcache={};rows=[];checks=[];pairs={};joins={};numeric=0
for name in inputs:
 f=PACK/name;rr=json.loads(f.read_text())['rows']
 for r in rr:
  src=r.get('sourceValue',r.get('source'));raw=PACK/'products'/r['rawFile'];raw=raw if raw.is_file() else PACK/r['rawFile']
  if str(raw)not in rawcache:rawcache[str(raw)]=json.loads(raw.read_text())['data']['translatableResourcesByIds']['nodes']
  n=next(x for x in rawcache[str(raw)]if x['resourceId']==r['resourceId']);s=next(x for x in n['translatableContent']if x['key']==r['key']and x['locale']=='en')
  alltr=[t for k,v in n.items()if k.startswith('tr_')for t in v]+n.get('translations',[])
  tr=[x for x in alltr if x['locale']==r['locale']and x['key']==r['key']and x.get('market')is None];before=tr[0]if tr else None
  errors=[]
  if src!=s['value']:errors.append('source_mismatch')
  if r['sourceDigest']!=s['digest']:errors.append('digest_mismatch')
  if r['before']!=before:errors.append('before_mismatch')
  v=m.verify_text(src,r['value'],r['locale']);errors+=v['errors']
  checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'sourceSHA256':sha(src),'beforeSHA256':sha(before['value'])if before else None,'valueSHA256':sha(r['value']),'candidateFile':name,'candidateFileSHA256':fsha(f),'rawFile':str(raw.relative_to(PACK)),'rawFileSHA256':fsha(raw),'errors':errors,'structure':v})
  ident=r['resourceId'].split('/')[-1]+':'+r['locale'];rows.append(r)
  def seg(t):return[html.unescape(x).strip()for x in re.split(r'(<[^>]+>)',t)if x.strip()and not x.startswith('<')]
  ss,tt=seg(src),seg(r['value']);assert len(ss)==len(tt),(ident,len(ss),len(tt))
  for s,t in zip(ss,tt):
   if s==t and re.fullmatch(r'[\d\s.,%/×x–—−+()\-]+',s):numeric+=1;continue
   pairs.setdefault((r['locale'],s,t),[]).append(ident)
  for tag in re.findall(r'<(?:p|li)\b[^>]*>.*?</(?:p|li)>',r['value'],re.S):
   if'<a 'in tag or'<strong'in tag or'<b>'in tag:
    t=html.unescape(re.sub('<[^>]+>',' ',tag));t=re.sub(r'\s+',' ',t).strip();joins.setdefault((r['locale'],t),[]).append(ident)
pp=[{'i':i,'locale':loc,'source':s,'target':t,'tuples':list(dict.fromkeys(ids))}for i,((loc,s,t),ids)in enumerate(pairs.items())]
write('product16_checks.json',{'status':'PASS'if not any(x['errors']for x in checks)else'FAILED','rows':checks,'exactUnchangedNumericCells':numeric})
write('product16_pairs.json',pp);write('product16_inline.json',[{'i':i,'locale':loc,'text':s,'tuples':ids}for i,((loc,s),ids)in enumerate(joins.items())]);write('product16_candidates_frozen_copy.json',{'rows':rows})
print({'products':len(rows),'pairs':len(pp),'pairChars':sum(len(x['source'])+len(x['target'])for x in pp),'localePairs':dict(collections.Counter(x['locale']for x in pp)),'numericExactSkipped':numeric,'joins':len(joins),'errors':[(r['resourceId'],r['locale'],r['errors'])for r in checks if r['errors']]})
