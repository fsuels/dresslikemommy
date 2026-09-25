import re,json,html
from pathlib import Path
H=Path(__file__).resolve().parent;rs=json.loads((H/'worklist40.json').read_text())['rows'];out=[]
for r in rs[::5]:
 parts=re.split(r'(<[^>]*>)',r['source']);intable=False;nodes=[]
 for i,s in enumerate(parts):
  if s.startswith('<table'):intable=True
  elif s.startswith('</table'):intable=False
  elif not s.startswith('<') and s.strip() and not intable:
   nodes.append({'index':len(nodes),'partIndex':i,'sourceText':html.unescape(s.strip())})
 out.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'nodes':nodes})
(H/'source_prose_nodes.json').write_text(json.dumps({'rows':out},ensure_ascii=False,indent=2)+'\n')
for r in out:
 print('\nP',r['productIndex'])
 for n in r['nodes']:print(n['index'],n['sourceText'])
