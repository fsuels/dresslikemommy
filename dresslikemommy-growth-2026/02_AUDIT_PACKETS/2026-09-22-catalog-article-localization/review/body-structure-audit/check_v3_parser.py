import json,re,hashlib,collections
from html.parser import HTMLParser
from pathlib import Path
H=Path(__file__).resolve().parent
class Check(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.issues=[];self.tags=[];self.attrs=[]
 def handle_starttag(self,tag,attrs):
  self.tags.append(tag);self.attrs.append((tag,attrs))
  if tag not in 'area base br col embed hr img input link meta param source track wbr'.split():self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in 'area base br col embed hr img input link meta param source track wbr'.split():return
  if self.stack and self.stack[-1]==tag:self.stack.pop()
  else:self.issues.append((tag,self.stack[-5:]));self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)] if tag in self.stack else self.stack
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs);self.handle_endtag(tag)
def check(s):
 p=Check();p.feed(s);p.close();return p
v=json.loads((H/'tag_candidates_v3.json').read_text())['rows'];inv=json.loads((H/'effective_body_inventory.json').read_text())['rows'];m={(x['resourceId'],x['locale']):x for x in v};errors=[];remaining=[];sources={}
for r in v:
 p=check(r['value']);assert not p.issues and not p.stack,(r['productIndex'],r['locale'],p.issues,p.stack)
 assert not p.rawdata,(r['productIndex'],r['locale'],p.rawdata)
for r in inv:
 p=check(m.get((r['resourceId'],r['locale']),{}).get('value',r['expectedEffectiveBeforeValue']) or '')
 if p.issues or p.stack or p.rawdata:remaining.append({'productIndex':r['productIndex'],'locale':r['locale'],'resourceId':r['resourceId'],'issues':p.issues,'stack':p.stack,'parserUnconsumed':p.rawdata})
 if r['productIndex'] not in sources:
  q=check(r['source']);sources[r['productIndex']]={'issues':q.issues,'stack':q.stack,'parserUnconsumed':q.rawdata}
summary={'status':'PASS_375_CANDIDATES','candidateSHA256':hashlib.sha256((H/'tag_candidates_v3.json').read_bytes()).hexdigest(),'candidateRowsParsed':375,'candidateStrictParserFailures':0,'fullScopeRowsParsed':4760,'remainingFullScopeParserIssues':len(remaining),'sourceParserIssueProducts':[k for k,x in sources.items() if x['issues'] or x['stack'] or x['parserUnconsumed']],'remaining':remaining}
(H/'v3_standard_parser_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='remaining'}));print(json.dumps(remaining[:5],ensure_ascii=False))
