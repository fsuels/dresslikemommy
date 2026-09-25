import json,re
from pathlib import Path
P=Path(__file__).parent;a=json.loads((P/'de_review_pairs.json').read_text());out=[];counts={}
patterns=[('bestseller',r'This (.+) is one of our bestsellers for a reason\. The fabric is soft, the fit is flattering for all body types, and it washes beautifully even after dozens of cycles\.',r'Das Modell „(.+)“ zählt nicht ohne Grund zu unseren Bestsellern\. Der Stoff ist weich, der Schnitt schmeichelt jedem Figurtyp und es übersteht selbst Dutzende Waschgänge hervorragend\.'),('practical',r'The (.+) combines timeless style with everyday practicality\. Parents love the quality construction, and kids love how comfortable it feels\.',r'Das Modell „(.+)“ verbindet zeitlosen Stil mit Alltagstauglichkeit\. Eltern schätzen die hochwertige Verarbeitung, und Kinder lieben das bequeme Tragegefühl\.'),('recommend',r"We can't stop recommending the (.+)\. It's the kind of piece that gets compliments every single time you wear it out\.",r'Wir können das Modell „(.+)“ gar nicht oft genug empfehlen\. Es ist eines dieser Stücke, für die du jedes Mal Komplimente bekommst, wenn du es außer Haus trägst\.')]
for r in a:
 rr=dict(r)
 for name,s,t in patterns:
  sm=re.fullmatch(s,r['source']);tm=re.fullmatch(t,r['target'])
  if sm and tm:
   rr['source']=sm.group(1);rr['target']=tm.group(1);rr['template']=name;counts[name]=counts.get(name,0)+1;break
 out.append(rr)
(P/'de_compact_pairs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(counts)
import sys
lo,hi=map(int,sys.argv[1:])
for r in out[lo:hi]:print(str(r['i'])+(' ['+r['template']+']' if 'template'in r else '')+' '+r['source']+' => '+r['target'])
