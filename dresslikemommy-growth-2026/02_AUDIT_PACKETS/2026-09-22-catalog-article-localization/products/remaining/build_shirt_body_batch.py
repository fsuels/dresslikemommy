#!/usr/bin/env python3
import hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
BASE=json.loads((HERE/'body_baseline.json').read_text())['rows']
parts={(r['resourceId'],r['locale']):r for r in json.loads((HERE/'body_label_partial_candidates.json').read_text())['rows']}
values=json.loads((HERE/'body_shirt_fragments_ru_sv.json').read_text())
ids={'7502770896993','7502765719649'}
rows=[];checks=[]
for r in BASE:
 if r['resourceId'].split('/')[-1] not in ids or r['locale'] not in {'ru','sv'}:continue
 after=parts.get((r['resourceId'],r['locale']),r).get('value',r['before']['value'])
 chunks=re.split(r'(<[^>]+>)',after);patches=[]
 for i in range(0,len(chunks),2):
  t=re.sub(r'\s+',' ',html.unescape(chunks[i])).strip()
  if t not in values:continue
  v=values[t][r['locale']];patches.append({'source':t,'value':v})
  chunks[i]=re.match(r'^\s*',chunks[i]).group()+html.escape(v,quote=False)+re.search(r'\s*$',chunks[i]).group()
 after=''.join(chunks)
 if r['locale']=='ru' and r['resourceId'].endswith('/7502770896993'):
  after=after.replace('100% хлопок','100% хлопка')
 check=ot.verify_text(r['source'],after,r['locale']);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'check':check})
 rows.append({**r,'value':after,'marketId':None,'method':'manual_exact_English_text_nodes_plus_reviewed_size_headers','manualTextPatches':patches,'preserved':'Original translated spans, HTML markup/attributes, URLs and numeric size cells retained.'})
f=HERE/'shirt_body_ru_sv_candidate.json';f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(HERE/'shirt_body_ru_sv_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(HERE/'shirt_body_ru_sv_rollback.json').write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
