"""Independent structural/source verification; semantic review is recorded separately."""
import json, re, hashlib
from pathlib import Path
from html.parser import HTMLParser

BASE=Path(__file__).resolve().parents[2]
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def num(s):return re.findall(r'\d+(?:\.\d+)?',s)
def units(s):return re.findall(r'\b(?:cm|in|kg|lbs)\b',s)
class Cells(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.cells=[];self.cell=None;self.tables=0
 def handle_starttag(self,t,a):
  if t=='table':self.tables+=1
  if t in ('td','th'):
   assert self.cell is None
   self.cell=[t,a,'']
 def handle_endtag(self,t):
  if t in ('td','th'):
   assert self.cell is not None
   assert self.cell[0]==t
   self.cells.append(self.cell);self.cell=None
 def handle_data(self,s):
  if self.cell is not None:self.cell[2]+=s
def preservation(source,target):
 assert re.findall(r'<[^>]+>',source)==re.findall(r'<[^>]+>',target),'source markup changed'
 assert num(source)==num(target),'source numeric sequence changed'
 assert not re.search(r'QZ\d|QX\d|\dQXZ',target),'placeholder remains'
 a,b=Cells(),Cells();a.feed(source);b.feed(target)
 assert a.cell is None and b.cell is None
 assert a.tables==b.tables and len(a.cells)==len(b.cells),'cell structure'
 for x,y in zip(a.cells,b.cells):
  assert x[:2]==y[:2] and num(x[2])==num(y[2]) and units(x[2])==units(y[2]),'cell measurements or units'
  if x[0]=='td' and re.fullmatch(r'[\s\d.,/\-–—%]*(?:(?:cm|in|kg|lbs)[\s\d.,/\-–—%]*)*',x[2]):
   assert x[2]==y[2],'numeric-only measurement cell modified'
 return {'tables':a.tables,'cells':len(a.cells)}
def verify(rows):
 rawcache={};out=[]
 for r in rows:
  p=BASE/r['rawFile']
  if p not in rawcache:
   rawcache[p]=(hashlib.sha256(p.read_bytes()).hexdigest(),json.loads(p.read_text())['data']['translatableResourcesByIds']['nodes'])
  rawhash,nodes=rawcache[p];assert rawhash==r['rawFileSHA256']
  n=next(n for n in nodes if n['resourceId']==r['resourceId']);ss={x['key']:x for x in n['translatableContent']}
  assert r['source']==r['sourceValue']==ss[r['key']]['value']
  assert r['sourceDigest']==ss[r['key']]['digest'] and sha(r['source'])==r['sourceSHA256']
  assert sha(r['value'])==r['valueSHA256']
  rb=next(t for t in n['tr_'+r['locale'].replace('-','_')] if t['key']==r['key'] and not t.get('market'))
  assert rb==r['rawBefore']
  for k,d in r.get('supportingSourceDigests',{}).items():assert ss[k]['digest']==d
  out.append({'resourceId':r['resourceId'],'locale':r['locale'],**preservation(r['source'],r['value'])})
 assert len({(r['resourceId'],r['locale'],r['key']) for r in rows})==len(rows)
 probes=[];s=rows[0]['source'];v=rows[0]['value']
 for label,bad in [('dropped-first-tag',re.sub(r'<[^>]+>','',v,count=1)),('changed-number',re.sub(r'\d','9',v,count=1)),('introduced-token',v+' QZ012QZ0')]:
  try:preservation(s,bad)
  except AssertionError:probes.append(label)
  else:raise AssertionError('corruption not rejected '+label)
 return {'checks':out,'rawFiles':len(rawcache),'negativeProbesRejected':probes}
