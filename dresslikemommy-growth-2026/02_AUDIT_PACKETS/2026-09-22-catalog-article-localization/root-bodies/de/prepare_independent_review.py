from pathlib import Path
from html.parser import HTMLParser
import json,importlib.util,hashlib,sys
P=Path(__file__).resolve().parent;root=P.parent.parent
class Spans(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=False);self.s=s;self.spans=[];self.lines=[0]+[i+1 for i,c in enumerate(s) if c=='\n'];self.feed(s)
 def off(self):l,c=self.getpos();return self.lines[l-1]+c
 def handle_starttag(self,t,a):s=self.off();self.spans.append((s,s+len(self.get_starttag_text())))
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
 def handle_endtag(self,t):s=self.off();self.spans.append((s,self.s.index('>',s)+1))
 def handle_comment(self,d):s=self.off();self.spans.append((s,self.s.index('-->',s)+3))
def text(s):
 o=[];st=0
 for a,b in Spans(s).spans:
  if s[st:a].strip():o.append(s[st:a].strip())
  st=b
 if s[st:].strip():o.append(s[st:].strip())
 return o
if __name__=='__main__':
 locale=sys.argv[1];f=root/('root-bodies/he-pl/pl_candidate_v2.json' if locale=='pl' else 'root-bodies/de/ru_remaining_review_input.json')
 rows=json.loads(f.read_text())['rows'];pairs=[];by_pair={};checks=[]
 spec=importlib.util.spec_from_file_location('offline',root/'tooling/offline_translation.py');off=importlib.util.module_from_spec(spec);spec.loader.exec_module(off)
 for r in rows:
  a=text(r['sourceValue']);b=text(r['value']);check=off.verify_text(r['sourceValue'],r['value'],locale)
  checks.append({'resourceId':r['resourceId'],'textNodeCounts':[len(a),len(b)],**check})
  if len(a)!=len(b):continue
  for s,t in zip(a,b):
   pair=(s,t)
   if pair not in by_pair:by_pair[pair]=len(pairs);pairs.append({'source':s,'value':t,'articleIds':[]})
   pairs[by_pair[pair]]['articleIds'].append(r['resourceId'])
 (P/(locale+'_review_pairs.json')).write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
 (P/(locale+'_review_checks_initial.json')).write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'locale':locale,'bodies':len(rows),'uniquePairs':len(pairs),'structuralFailures':[x for x in checks if x['errors']],'alignmentMismatches':[x for x in checks if x['textNodeCounts'][0]!=x['textNodeCounts'][1]]}))
