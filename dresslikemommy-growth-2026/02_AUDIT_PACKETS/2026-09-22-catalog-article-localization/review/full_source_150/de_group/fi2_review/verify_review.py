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

A=R/'review/full_source_150/a_group/final_fi2'
assert fs(A/'candidates2.json')=='e87b61e0fdda686c3fc0c5b2d6d6a05305451d982e39ad1fb3a774f158d5bf71'
rr=load(A/'candidates2.json')['rows'];pairs=load(A/'node_pairs2.json')['rows'];ev=load(A/'source_correspondence_evidence.json')['rows'];checks=[];corrections=[];tables=[]
for r,p,e in zip(rr,pairs,ev):
 assert r['productIndex']==p['productIndex']==e['productIndex'];rawp=R/r['rawFile'];assert fs(rawp)==r['rawFileSHA256'];n=next(n for n in load(rawp)['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==r['resourceId']);sc={x['key']:x for x in n['translatableContent']};bef=next(x for x in n['tr_fi'] if x['key']=='body_html' and not x['market']);assert r['sourceValue']==sc['body_html']['value'] and r['sourceDigest']==sc['body_html']['digest'] and bef==r['rawBefore']
 assert r['before'] is None and r['beforeValueSHA256']==sha(r['expectedEffectiveBeforeValue'])==r['expectedBeforeValueSHA256']
 for k,digest in r['supportingSourceDigests'].items():assert digest==sc[k]['digest']
 for dep in r['plannedBeforeDependencies']:assert fs(R/dep['file'])==dep['sha256']
 assert (r['plannedBeforeDependencies'][-1]['valueSHA256'] if r['plannedBeforeDependencies'] else sha(bef['value']))==sha(r['expectedEffectiveBeforeValue'])
 ep=R/e['optionsEvidence']['file'];assert fs(ep)==e['optionsEvidence']['sha256'];epn=next(x for x in load(ep)['data']['products']['nodes'] if x['id']==r['resourceId']);assert epn==e['optionsEvidence']['product']
 if r['productIndex']==206:
  old='Sopii selkeästi farkkujen, valkoisten housujen tai neutraalinväristen shortsien kanssa tai kerrokseksi takin alle.'
  new='Sopii hyvin farkkujen, valkoisten housujen tai neutraalinväristen shortsien kanssa tai kerrokseksi takin alle.'
  assert r['value'].count(old)==1;r['value']=r['value'].replace(old,new);r['valueSHA256']=sha(r['value']);q=next(x for x in p['nodes'] if x['target']==old);q['target']=new
  corrections.append({'productIndex':206,'resourceId':r['resourceId'],'locale':'fi','key':'body_html','source':q['source'],'beforeCandidateText':old,'reviewedText':new,'reason':'Natural Finnish for clothing pairing; selkeästi means clearly and is an unnatural literal rendering of cleanly here. Meaning and garment list preserved.'})
 count=check(r,p['nodes']);r['independentReview']={'reviewer':'article_de_complete','fullMeaningAndCompleteSourceNodes':'PASS','sourceScopeQualifiers':'PASS','measurementsAndHTML':'PASS','titleTypeAndOptionsCorroboration':'PASS','rootMustBindCurrentLiveBefore':True}
 checks.append({'productIndex':r['productIndex'],'locale':'fi','sourceRawBeforeAndDigestBinding':'PASS','sourceNodes':len(p['nodes']),'sourceHTMLAttributesURLsNumericTokens':'PASS','exactNonlabelMeasurementCells':count,'standardParserBalanced':'PASS','titleTypeOptionsBinding':'PASS','rootFreshLiveGuardRequired':True})
 table=lambda v:[[re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',z,re.S) for z in re.findall(r'<tr\b[^>]*>(.*?)</tr>',x,re.S)] for x in re.findall(r'<table\b.*?</table>',v,re.S)]
 st,bt,vt=table(r['sourceValue']),table(r['expectedEffectiveBeforeValue']),table(r['value']);assert len(bt)==len(st)+1
 tables.append({'productIndex':r['productIndex'],'sourceTables':st,'beforeTables':bt,'candidateTables':vt,'decision':'Remove exactly the obsolete target-only table; current source table structure and measurements preserved.','sourceTableCount':len(st),'beforeTableCount':len(bt),'targetTableCount':len(vt)})
assert len(rr)==2 and sum(len(x['nodes']) for x in pairs)==73
for mode in ['unit','omission']:
 bad=copy.deepcopy(rr[1]);bad['value']=bad['value'].replace('kg','g',1) if mode=='unit' else bad['value'].replace(html.escape(pairs[1]['nodes'][1]['target'],quote=False),'',1);bad['valueSHA256']=sha(bad['value'])
 try:check(bad,pairs[1]['nodes'])
 except AssertionError:pass
 else:raise AssertionError('negative probe accepted '+mode)
dump('fi2_reviewed.json',{'rows':rr});dump('node_pairs_reviewed.json',{'rows':pairs});dump('corrections.json',{'rows':corrections});dump('table_proof.json',{'rows':tables});dump('checks.json',{'status':'PASS_INDEPENDENT_FULL_SOURCE_MEANING_AND_PRESERVATION_REVIEW','candidateRows':2,'candidateSHA256':fs(H/'fi2_reviewed.json'),'sourceNodes':73,'rows':checks,'corrections':len(corrections),'negativeTests':['unit_change_rejected','complete_source_clause_omission_rejected'],'sourceEnglishChanged':False,'externalWrites':0})
print(json.dumps({'qualified':2,'sourceNodes':73,'corrections':len(corrections),'SHA256':fs(H/'fi2_reviewed.json')}))
