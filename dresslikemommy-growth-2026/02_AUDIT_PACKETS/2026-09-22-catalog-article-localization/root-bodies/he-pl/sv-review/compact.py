import json,re,sys
from pathlib import Path
P=Path(__file__).parent;a=json.loads((P/'pairs.json').read_text());out=[];counts={}
patterns=[('bestseller',r'This (.+) is one of our bestsellers for a reason\. The fabric is soft, the fit is flattering for all body types, and it washes beautifully even after dozens of cycles\.',r'Produkten (.+) är en av våra bästsäljare av goda skäl\. Tyget är mjukt, passformen är smickrande för alla kroppstyper och plagget håller sig fint i tvätten även efter dussintals tvättar\.'),('practical',r'The (.+) combines timeless style with everyday practicality\. Parents love the quality construction, and kids love how comfortable it feels\.',r'Produkten (.+) förenar tidlös stil med praktisk användning i vardagen\. Föräldrar älskar den välgjorda konstruktionen och barnen älskar hur bekväm den känns\.'),('recommend',r"We can't stop recommending the (.+)\. It's the kind of piece that gets compliments every single time you wear it out\.",r'Vi kan inte sluta rekommendera (.+)\. Det är den sortens plagg som får komplimanger varje gång du bär det ute\.')]
for r in a:
 rr=dict(r)
 for name,s,t in patterns:
  sm=re.fullmatch(s,r['source']);tm=re.fullmatch(t,r['target'])
  if sm and tm:rr['source']=sm.group(1);rr['target']=tm.group(1);rr['template']=name;counts[name]=counts.get(name,0)+1;break
 out.append(rr)
(P/'compact_pairs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(counts)
lo,hi=map(int,sys.argv[1:])
for r in out[lo:hi]:print(str(r['i'])+(' ['+r['template']+']' if'template'in r else'')+' '+r['source']+' => '+r['target'])
