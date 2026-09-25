#!/usr/bin/env python3
import hashlib,html,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent.parent/'tooling'))
import offline_translation as ot
BASE=json.loads((HERE/'body_baseline.json').read_text())['rows']
partial={(r['resourceId'],r['locale']):r for r in json.loads((HERE/'body_label_partial_candidates.json').read_text())['rows']}
group=sys.argv[1];values=json.loads((HERE/('blue_daisy_values_'+group+'.json')).read_text());indices=values.pop('sourceIndices')
rows=[];checks=[]
def norm(v):return re.sub(r'\s+',' ',html.unescape(v)).strip()
for r in BASE:
 if not r['resourceId'].endswith('/7577248596065') or r['locale'] not in values:continue
 assert len(values[r['locale']])==len(indices)
 original=r['before']['value']
 outside=re.sub(r'<table\b.*?</table>','[TABLE]',original,flags=re.S)
 nodes=[norm(t) for t in re.split('<[^>]+>',outside) if norm(t)]
 assert len(nodes)==26,(r['locale'],len(nodes))
 lookup={nodes[i]:v for i,v in zip(indices,values[r['locale']])}
 after=partial.get((r['resourceId'],r['locale']),{}).get('value',original)
 chunks=re.split(r'(<[^>]+>)',after);patches=[]
 for i in range(0,len(chunks),2):
  t=norm(chunks[i])
  if t not in lookup:continue
  v=lookup[t];patches.append({'before':t,'after':v})
  chunks[i]=re.match(r'^\s*',chunks[i]).group()+html.escape(v,quote=False)+re.search(r'\s*$',chunks[i]).group()
 after=''.join(chunks)
 assert len(patches)==18,(r['locale'],'missing source-correspondent text patch',len(patches))
 checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'sourceCheck':ot.verify_text(r['source'],after,r['locale']),'beforeAfterHtmlTagsAndAttributesIdentical':ot.Shape(original).events==ot.Shape(after).events,'beforeAfterNumericCellsAndUnitsIdentical':ot.table_facts(ot.Shape(original),r['locale'])==ot.table_facts(ot.Shape(after),r['locale'])})
 rows.append({**r,'value':after,'marketId':None,'method':'manual_remaining_English_prose_and_mixed_size_label_translation','textNodePatches':patches,'scopeNote':'Translation-only merchant reservation released by owner. Existing source statements, including chart/vendor-reference guidance, translated faithfully; English source cleanup excluded. Numeric cell values and attributes preserved.'})
name='blue_daisy_'+group;f=HERE/(name+'_candidate.json');f.write_text(json.dumps({'status':'PENDING_INDEPENDENT_PARENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
(HERE/(name+'_checks.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
(HERE/(name+'_rollback.json')).write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'action':'restore','value':r['before']['value']} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checks':checks},ensure_ascii=False))
