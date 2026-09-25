# Independent semantic-review artifact builder and structural/raw verifier.
import copy,hashlib,html,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;R=H.parents[3];A=R/'review/full_source_150/a_group'
load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dump=lambda n,d:(H/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
class Parser(HTMLParser):
 def __init__(self,v):
  super().__init__(convert_charrefs=False);self.events=[];self.stack=[];self.errors=[];self.feed(v);self.close();assert not self.rawdata
 def handle_starttag(self,t,a):
  self.events.append((t,a))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('/'+t,[]))
  if not self.stack or self.stack[-1]!=t:self.errors.append(t)
  else:self.stack.pop()
 def handle_startendtag(self,t,a):self.events.append((t,a))
def check(r,pairs):
 s=r['sourceValue'];v=r['value'];assert sha(s)==r['sourceSHA256'] and sha(v)==r['valueSHA256'];assert re.findall(r'<[^>]*>',s)==re.findall(r'<[^>]*>',v)
 assert re.findall(r'\d+(?:[.,]\d+)?',s)==re.findall(r'\d+(?:[.,]\d+)?',v)
 sp=re.split('(<[^>]+>)',s);vp=re.split('(<[^>]+>)',v);assert len(sp)==len(vp);np={x['textNodeIndex']:x for x in pairs};assert len(np)==len(pairs)
 for i in range(0,len(sp),2):
  a,b=sp[i].strip(),vp[i].strip();i=i//2
  if i in np:
   assert html.unescape(a)==html.unescape(np[i]['source']),(i,a,np[i]['source'])
   assert html.unescape(b)==html.unescape(np[i]['target']),(i,b,np[i]['target'])
  else:assert a==b,('unpaired_changed_text',i,a,b)
 x,y=Parser(s),Parser(v);assert x.events==y.events and not y.errors and not y.stack
 st=re.findall(r'<table\b.*?</table>',s,re.S);vt=re.findall(r'<table\b.*?</table>',v,re.S);assert len(st)==len(vt)
 cellcount=0
 for a,b in zip(st,vt):
  sr=[re.findall(r'<td\b[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr\b[^>]*>(.*?)</tr>',a,re.S)];vr=[re.findall(r'<td\b[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr\b[^>]*>(.*?)</tr>',b,re.S)];assert len(sr)==len(vr)
  for x,y in zip(sr,vr):
   assert len(x)==len(y)
   for xc,yc in zip(x[1:],y[1:]):
    if xc.startswith('Up to '):assert re.findall(r'[0-9]+(?:\.[0-9]+)?|kg|lbs',xc)==re.findall(r'[0-9]+(?:\.[0-9]+)?|kg|lbs',yc)
    else:assert xc==yc,('measurement_changed',xc,yc)
    cellcount+=1
 return cellcount
inputs=[('first3','94ec5312e49ed5bc92f1a496eb1dbc26e9a88ae808704f11cf4715f4aebe9ba3'),('next12','4f284eef66d08cd969a3df5bbe1fc1e1504e62f8b33e784b64bcfc366c8cdb31')]
rows=[];allpairs=[];checks=[];corrections=[]
for name,h in inputs:
 f=A/('candidate_'+name+'.json');assert fs(f)==h;rr=load(f)['rows'];pp={(x['resourceId'],x['locale']):x for x in load(A/('node_pairs_'+name+'.json'))['rows']}
 for original in rr:
  r=copy.deepcopy(original);p=copy.deepcopy(pp[r['resourceId'],r['locale']]);rawp=R/r['rawFile'];assert fs(rawp)==r['rawFileSHA256'];n=next(n for n in load(rawp)['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId']);src=next(x for x in n['translatableContent'] if x['key']=='body_html');bef=next(x for x in n['tr_'+r['locale'].replace('-','_')] if x['key']=='body_html' and not x['market']);assert r['sourceValue']==src['value'] and r['sourceDigest']==src['digest'] and bef==r['rawBefore'];assert sha(bef['value'])==r['beforeValueSHA256']
  if (r['productIndex'],r['locale'])==(215,'pl'):
   old='Dziecko 1-2 lat';new='Dziecko 1-2 lata';assert r['value'].count('>'+old+'<')==1;r['value']=r['value'].replace('>'+old+'<','>'+new+'<');r['valueSHA256']=sha(r['value']);q=next(x for x in p['nodes'] if x['target']==old);q['target']=new;corrections.append({'productIndex':215,'locale':'pl','resourceId':r['resourceId'],'key':r['key'],'source':q['source'],'old':old,'new':new,'reason':'Polish age-label inflection: 1–2 uses lata; numbers and label role unchanged.','authoredValueSHA256':original['valueSHA256'],'reviewedValueSHA256':r['valueSHA256']})
  count=check(r,p['nodes']);r['independentReview']={'reviewer':'article_de_complete','fullMeaningAndCompleteSourceNodes':'PASS','sourceScopeQualifiersAndUncertainty':'PASS','measurementsAndHTML':'PASS','rootMustBindCurrentLiveBefore':True};rows.append(r);allpairs.append(p);checks.append({'productIndex':r['productIndex'],'locale':r['locale'],'sourceRawBeforeAndDigestBinding':'PASS','fullMeaningReview':'PASS','sourceNodes':len(p['nodes']),'sourceHTMLAttributesURLsNumericTokens':'PASS','measurementCellsExact':count,'standardParserBalanced':'PASS','rootFreshLiveGuardRequired':True})
assert len(rows)==15 and len({(r['resourceId'],r['locale']) for r in rows})==15
# Two negative integrity cases prevent measurements and unmatched omissions.
bad=copy.deepcopy(rows[0]);bad['value']=bad['value'].replace('kg','g',1);bad['valueSHA256']=sha(bad['value'])
try:check(bad,allpairs[0]['nodes'])
except AssertionError:pass
else:raise AssertionError('altered unit accepted')
bad=copy.deepcopy(rows[0]);q=allpairs[0]['nodes'][1];bad['value']=bad['value'].replace(html.escape(q['target'],quote=False),'',1);bad['valueSHA256']=sha(bad['value'])
try:check(bad,allpairs[0]['nodes'])
except AssertionError:pass
else:raise AssertionError('omitted source qualification accepted')
dump('reviewed_first15.json',{'rows':rows});dump('reviewed_first15_node_pairs.json',{'rows':allpairs});dump('corrections_first15.json',{'rows':corrections});dump('checks_first15.json',{'status':'PASS_INDEPENDENT_FULL_MEANING_SOURCE_AND_PRESERVATION_REVIEW','candidateRows':15,'candidateSHA256':fs(H/'reviewed_first15.json'),'rows':checks,'corrections':len(corrections),'sourceNodes':sum(x['sourceNodes'] for x in checks),'negativeTests':['unit_change_rejected','source_qualification_omission_rejected'],'externalWrites':0});print(json.dumps({'qualified':15,'corrections':len(corrections),'SHA256':fs(H/'reviewed_first15.json')}))
