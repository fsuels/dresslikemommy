import re,json,html,hashlib,collections
from pathlib import Path
O=Path(__file__).resolve().parent;P=O.parents[2]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
w=json.loads((P/'review/full_source_150/original_worklist.json').read_text())['rows'];rs=[x for x in w if x['locale'] in ['es','fr','it','nl','pl','pt-BR']]
base={(r['resourceId'],r['locale']):r for r in json.loads((P/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows']}
texts={};prepared=[]
for r in rs:
 b=base[r['resourceId'],r['locale']];assert r['source']==r['sourceValue']==b['source'];assert r['sourceDigest']==b['sourceDigest'];assert r['before']==b['rawBefore'];r={**r,'productIndex':b['productIndex'],'rawFile':b['rawFile'],'rawFileSHA256':b['rawFileSHA256']};prepared.append(r)
 texts.setdefault(r['productIndex'],[])
 for t in re.split('(<[^>]+>)',r['source'])[::2]:
  t=t.strip()
  if not t or not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',t)):continue
  if re.fullmatch(r'(?:Child|Girl|Boy) \d+(?:-\d+)? Years?',t) or re.fullmatch(r'(?:Mother|Father|Adult) (?:[2-5]?XL|S|M|L)',t):continue
  if t not in texts[r['productIndex']]:texts[r['productIndex']].append(t)
(O/'source_texts.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2)+'\n');(O/'worklist38.json').write_text(json.dumps({'rows':prepared},ensure_ascii=False,indent=2)+'\n')
print('rows',len(rs),'texts',sum(map(len,texts.values())),'byproduct',{k:len(v) for k,v in texts.items()})
for r in prepared:
 def prose(s):return html.unescape(re.sub('<[^>]+>','',re.sub(r'<table\b.*?</table>','',s,flags=re.S)))
 print(r['productIndex'],r['locale'],'sourceprose',len(prose(r['source'])),'beforeprose',len(prose(r['before']['value'])))
