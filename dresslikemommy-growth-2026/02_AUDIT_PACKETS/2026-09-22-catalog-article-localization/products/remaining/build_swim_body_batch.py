#!/usr/bin/env python3
import hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
BASE=json.loads((HERE/'body_baseline.json').read_text())['rows']
parts={(r['resourceId'],r['locale']):r for r in json.loads((HERE/'body_label_partial_candidates.json').read_text())['rows']}
number=sys.argv[1]
sources={r['id']:r['sourceNodes'] for r in json.loads((HERE/('swim_batch_'+number+'_nodes.json')).read_text())}
values=json.loads((HERE/('swim_batch_'+number+'_values.json')).read_text())
rows=[];checks=[]
for r in BASE:
 id=r['resourceId'].split('/')[-1]
 if id not in values or r['locale'] not in values[id]:continue
 assert len(sources[id])==len(values[id][r['locale']])
 lookup=dict(zip(sources[id],values[id][r['locale']]))
 for s,v in list(lookup.items()):
  lookup[s.replace('Принт:','Mönster:').replace('Ткань:','Tyg:')]=v
 after=parts.get((r['resourceId'],r['locale']),r).get('value',r['before']['value'])
 chunks=re.split(r'(<[^>]+>)',after);patches=[]
 for i in range(0,len(chunks),2):
  t=re.sub(r'\s+',' ',html.unescape(chunks[i])).strip()
  if t not in lookup:continue
  v=lookup[t];patches.append({'before':t,'after':v})
  chunks[i]=re.match(r'^\s*',chunks[i]).group()+html.escape(v,quote=False)+re.search(r'\s*$',chunks[i]).group()
 after=''.join(chunks)
 check=ot.verify_text(r['source'],after,r['locale']);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'check':check})
 rows.append({**r,'value':after,'marketId':None,'method':'manual_current_English_or_mixed_label_text_nodes_plus_reviewed_size_headers','manualTextPatches':patches,'preserved':'Original translated spans, HTML markup/attributes, URLs and numeric size cells retained. Existing English source commercial/product statements translated faithfully, not independently supplier-verified.'})
name='swim_body_batch_'+number
f=HERE/(name+'_candidate.json');f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(HERE/(name+'_checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(HERE/(name+'_rollback.json')).write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
