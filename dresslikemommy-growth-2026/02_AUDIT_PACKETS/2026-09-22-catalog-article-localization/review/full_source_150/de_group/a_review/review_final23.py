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
inputs=[('next12_beach','47ed3309efaf54a6ff47932a4811deb989f2b89805605369a2a869ef19b30d53'),('last11','f3aa361c405e12273d91c44a416a2e913df7c1a10e169e19596bb843a75fb495')]
# Direct language review: generic construction names, no product fact or source edits.
REPLACE={
'es':{4:('Crochet ligero','Ganchillo ligero'),12:('Crochet aporta','El ganchillo aporta'),211:('El conjunto de crochet','El conjunto de ganchillo'),219:('Textura de crochet','Textura de ganchillo')},
'fr':{12:('Crochet offre','Le crochet offre')},
'it':{12:('Crochet mantiene','La lavorazione all’uncinetto mantiene')},
'nl':{12:('Crochet geeft','Haakwerk geeft'),211:('De Crochet-set','De gehaakte set')},
'pl':{12:('Crochet zachowuje','Szydełkowy splot zachowuje')},
'pt-BR':{12:('Crochet mantém','O crochê mantém')}}
rows=[];allpairs=[];checks=[];corrections=[]
for name,h in inputs:
 f=A/('candidate_'+name+'.json');assert fs(f)==h;rr=load(f)['rows'];pp={(x['resourceId'],x['locale']):x for x in load(A/('node_pairs_'+name+'.json'))['rows']}
 for original in rr:
  r=copy.deepcopy(original);p=copy.deepcopy(pp[r['resourceId'],r['locale']]);rawp=R/r['rawFile'];assert fs(rawp)==r['rawFileSHA256'];n=next(n for n in load(rawp)['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId']);src=next(x for x in n['translatableContent'] if x['key']=='body_html');bef=next(x for x in n['tr_'+r['locale'].replace('-','_')] if x['key']=='body_html' and not x['market']);assert r['sourceValue']==src['value'] and r['sourceDigest']==src['digest'] and bef==r['rawBefore'];assert sha(bef['value'])==r['beforeValueSHA256']
  if r['productIndex']==216:
   tokens=re.split('(<[^>]+>)',r['value'])
   for ni,(old,new) in REPLACE[r['locale']].items():
    q=next(x for x in p['nodes'] if x['textNodeIndex']==ni);prev=q['target'];assert prev.count(old)==1;q['target']=prev.replace(old,new)
    raw=tokens[ni*2];assert html.unescape(raw.strip())==prev
    start=len(raw)-len(raw.lstrip());end=len(raw)-len(raw.rstrip());tokens[ni*2]=raw[:start]+html.escape(q['target'],quote=False)+(raw[-end:] if end else '')
    corrections.append({'productIndex':216,'locale':r['locale'],'resourceId':r['resourceId'],'key':r['key'],'textNodeIndex':ni,'source':q['source'],'old':prev,'new':q['target'],'reason':'Crochet names the generic construction in this source. Localize the construction and natural determiner; preserve all garment facts and source uncertainty.'})
   r['value']=''.join(tokens);r['valueSHA256']=sha(r['value'])
  count=check(r,p['nodes']);r['independentReview']={'reviewer':'article_de_complete','fullMeaningAndCompleteSourceNodes':'PASS','sourceScopeQualifiersAndUncertainty':'PASS','measurementsAndHTML':'PASS','rootMustBindCurrentLiveBefore':True};rows.append(r);allpairs.append(p);checks.append({'productIndex':r['productIndex'],'locale':r['locale'],'sourceRawBeforeAndDigestBinding':'PASS','fullMeaningReview':'PASS','sourceNodes':len(p['nodes']),'sourceHTMLAttributesURLsNumericTokens':'PASS','measurementCellsExact':count,'standardParserBalanced':'PASS','rootFreshLiveGuardRequired':True})
assert len(rows)==23 and len({(r['resourceId'],r['locale']) for r in rows})==23 and len(corrections)==10
# Numeric and completeness negative cases exercise the verifier independently of authors.
for mode in ['unit','omission']:
 bad=copy.deepcopy(rows[0])
 if mode=='unit':bad['value']=bad['value'].replace('cm','mm',1)
 else:bad['value']=bad['value'].replace(html.escape(allpairs[0]['nodes'][1]['target'],quote=False),'',1)
 bad['valueSHA256']=sha(bad['value'])
 try:check(bad,allpairs[0]['nodes'])
 except AssertionError:pass
 else:raise AssertionError('corruption accepted')
dump('reviewed_final23.json',{'rows':rows});dump('reviewed_final23_node_pairs.json',{'rows':allpairs});dump('corrections_final23.json',{'rows':corrections});dump('checks_final23.json',{'status':'PASS_INDEPENDENT_FULL_MEANING_SOURCE_AND_PRESERVATION_REVIEW','candidateRows':23,'candidateSHA256':fs(H/'reviewed_final23.json'),'rows':checks,'corrections':len(corrections),'correctedFields':6,'sourceNodes':sum(x['sourceNodes'] for x in checks),'negativeTests':['unit_change_rejected','source_qualification_omission_rejected'],'externalWrites':0});print(json.dumps({'qualified':23,'corrections':len(corrections),'SHA256':fs(H/'reviewed_final23.json'),'nodes':sum(x['sourceNodes'] for x in checks)}))
