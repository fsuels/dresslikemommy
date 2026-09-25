"""Offline exact text-node selection, no provider fallback."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import json,re,hashlib
B=Path(__file__).resolve().parent
class Spans(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False);self.s=s;self.spans=[];self.lines=[0]
  for i,c in enumerate(s):
   if c=='\n':self.lines.append(i+1)
  self.feed(s);self.close()
 def absolute(self):
  line,col=self.getpos();return self.lines[line-1]+col
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:raise ValueError('Raw block requires review')
  a=self.absolute();self.spans.append((a,a+len(self.get_starttag_text())))
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):
  a=self.absolute();self.spans.append((a,self.s.index('>',a)+1))
 def handle_comment(self,text):
  a=self.absolute();self.spans.append((a,self.s.index('-->',a)+3))
 def handle_decl(self,text):
  a=self.absolute();self.spans.append((a,self.s.index('>',a)+1))
def parts(s):
 out=[];start=0
 for a,b in Spans(s).spans:
  if a>start:out.append((False,s[start:a]))
  out.append((True,s[a:b]));start=b
 if start<len(s):out.append((False,s[start:]))
 assert ''.join(v for _,v in out)==s
 return out
def norm(s):return re.sub(r'\s+',' ',unescape(s)).strip()
def neutral(s):
 return not re.search(r'[A-Za-z]',s) or bool(re.fullmatch(r'[\d\s.,/()\-–+%:;]*[\d\s.,/()\-–+%:;A-Za-z]*',s) and re.fullmatch(r'(?:[\d\s.,/()\-–+%:;]|cm|in|kg|lbs|lb|mm|XL|XXL|XXXL|S|M|L|XS|XXS|4XL|5XL)+',s)) or s in {'Dress Like Mommy','dresslikemommy.com','DLM','Instagram','Pinterest'}
if __name__=='__main__':
 rows=json.loads((B/'selected_baseline.json').read_text())['rows'];items=[];index={};retained=[];exceptions=[]
 for r in rows:
  ss={norm(s) for tag,s in parts(r['source']) if not tag and s.strip()}
  for tag,s in parts(r['baseValue']):
   if tag or not s.strip():continue
   n=norm(s)
   if neutral(n):continue
   if n not in ss:
    retained.append({'resourceId':r['resourceId'],'text':s.strip()});continue
   if n not in index:index[n]=str(len(items)+1);items.append({'id':index[n],'source':n,'resources':[]})
   if r['resourceId'] not in items[int(index[n])-1]['resources']:items[int(index[n])-1]['resources'].append(r['resourceId'])
 (B/'segments.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n');(B/'retained_existing_nodes.json').write_text(json.dumps(retained,ensure_ascii=False,indent=2)+'\n');print('segments',len(items),'words',sum(len(x['source'].split()) for x in items),'retained',len(retained))
