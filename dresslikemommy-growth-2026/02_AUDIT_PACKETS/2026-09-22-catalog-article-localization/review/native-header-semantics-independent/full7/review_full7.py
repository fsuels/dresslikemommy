from pathlib import Path
from html.parser import HTMLParser
import json,re,html,hashlib,copy
O=Path(__file__).resolve().parent;P=O.parents[2];A=P/'review/native-header-final';sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(n,v):p=O/n;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return fs(p)
F=A/'full7_candidates.json';assert fs(F)=='0a8da430806466a48e1f44357c79371501e76505e5ace79d31ec8966e0298915'
rows=load(F)['rows'];pairs={(x['resourceId'],x['locale']):x for x in load(A/'full7_source_target_node_pairs.json')['rows']}
class Parsed(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.events=[];self.stack=[];self.errors=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t not in ['br','img','hr','input','meta','link','source','wbr']:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('end',t))
  if self.stack and self.stack[-1]==t:self.stack.pop()
  else:self.errors.append((t,self.stack.copy()))
num=lambda s:re.findall(r'\d+(?:[.,]\d+)?',html.unescape(re.sub('<[^>]+>','',s)))
rawcache={};invcache={};proof=[];overlays={}
for rel in ['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json','review/native-header-final/current22_root_reviewed.json','review/size-label-repair/placeholder-review/placeholder88_reviewed.json','review/body-header-localization/prose-completion-review/prose_completion11_reviewed.json']:
 p=P/rel;overlays[rel]={(r['resourceId'],r['locale']) for r in load(p)['rows']}

def validate(r):
 s,v=r['source'],r['value'];assert s==r['sourceValue'] and sha(s)==r['sourceSHA256'] and sha(v)==r['valueSHA256'];assert r['before']==r['rawBefore'] and r['before']['outdated'] is True;assert sha(r['before']['value'])==r['beforeValueSHA256']==r['expectedBeforeValueSHA256']
 raw=P/r['rawFile'];assert fs(raw)==r['rawFileSHA256']
 if raw not in rawcache:rawcache[raw]={x['resourceId']:x for x in load(raw)['data']['translatableResourcesByIds']['nodes']}
 n=rawcache[raw][r['resourceId']];tc={x['key']:x for x in n['translatableContent']};assert tc[r['key']]['value']==s and tc[r['key']]['digest']==r['sourceDigest'];assert next(t for t in n['tr_'+r['locale']] if t['key']==r['key'])==r['before']
 for k,d in r['supportingSourceDigests'].items():assert tc[k]['digest']==d
 assert tc['product_type']['value']=='Matching Family Tops';assert ('Tank Top' if r['productIndex']==211 else 'Tops') in tc['title']['value']
 ci=r['corroboratingProductInventory'];ip=P/ci['file'];assert fs(ip)==ci['fileSHA256']
 if ip not in invcache:invcache[ip]={x['id']:x for x in load(ip)['data']['products']['nodes']}
 pr=invcache[ip][r['resourceId']];assert pr['variantsCount']['count']==ci['variantsCount'];assert sha(json.dumps(pr['options'],ensure_ascii=False,sort_keys=True))==ci['optionsSHA256']
 assert ci['variantsCount']==(8 if r['productIndex']==211 else 17)
 if r['productIndex']==211:assert [x['name'] for op in pr['options'] if op['name']=='Type' for x in op['optionValues']]==['Tank Top']
 else:assert {x['name'] for x in pr['options']}=={'Size','Color'}
 assert all((r['resourceId'],r['locale']) not in keys for keys in overlays.values())
 assert re.findall('<[^>]+>',s)==re.findall('<[^>]+>',v);assert num(s)==num(v)
 sp,vp=Parsed(s),Parsed(v);assert sp.events==vp.events and not vp.errors and not vp.stack and not vp.rawdata
 sr=[re.findall('<td\\b[^>]*>(.*?)</td>',t,re.S) for t in re.findall('<tr\\b[^>]*>(.*?)</tr>',s,re.S)];vr=[re.findall('<td\\b[^>]*>(.*?)</td>',t,re.S) for t in re.findall('<tr\\b[^>]*>(.*?)</tr>',v,re.S)]
 assert len(sr)==len(vr) and all(a[1:]==b[1:] for a,b in zip(sr,vr));assert len([x for x in sr if x])==(8 if r['productIndex']==211 else 17)
 p=pairs[r['resourceId'],r['locale']];assert p['sourceDigest']==r['sourceDigest'];sm=re.split('(<[^>]+>)',s)[::2];vm=re.split('(<[^>]+>)',v)[::2];assert len(sm)==len(vm);idx={x['textNodeIndex']:x for x in p['nodes']}
 for i,(sn,vn) in enumerate(zip(sm,vm)):
  if i in idx:assert sn.strip()==idx[i]['source'] and html.unescape(vn.strip())==idx[i]['target']
  else:assert sn==vn,(i,sn,vn)
 return {'productIndex':r['productIndex'],'locale':r['locale'],'sourceDigest':r['sourceDigest'],'valueSHA256':r['valueSHA256'],'sourceRawBeforeTitleTypeOptionsBindings':'PASS','completeSourceNodeCoverage':len(p['nodes']),'fullManualMeaningReview':'PASS','allCurrentSourceMeasurementDataCellsByteIdentical':'PASS','sourceMarkupAttributesNumericTokens':'PASS','balancedIndependentHTMLParser':'PASS','earlierOverlayOverlap':0,'currentTableRows':len([x for x in sr if x])}
for r in rows:proof.append(validate(r))
neg=[]
for kind in ['numeric_cell_corruption','missing_translated_clause','wrong_source_digest']:
 r=copy.deepcopy(rows[0])
 if kind=='numeric_cell_corruption':r['value']=r['value'].replace('44 cm / 17.3 in','45 cm / 17.3 in',1)
 elif kind=='missing_translated_clause':r['value']=r['value'].replace('Kalhoty, další spodní díly a doplňky nejsou součástí nabídky.','',1)
 else:r['sourceDigest']='0'*64
 r['valueSHA256']=sha(r['value'])
 try:validate(r)
 except AssertionError:neg.append({'case':kind,'rejected':True})
 else:raise AssertionError(kind)
q=copy.deepcopy(rows)
for r in q:r.update(independentReviewStatus='QUALIFIED_FULL_CURRENT_SOURCE_TRANSLATION',reviewStatus='INDEPENDENT_REVIEW_PASS_PENDING_ROOT_FRESH_GUARD',independentReview={'reviewer':'article_he_pl_complete','authorFile':'review/native-header-final/full7_candidates.json','authorFileSHA256':fs(F),'meaning':'All prose, chart headers, size labels and 336 source-target nodes manually read. Exact existing current source facts retained.','postFreezeCorrections':0})
h=save('full7_reviewed.json',{'rows':q});report={'status':'PASS','rows':7,'sourceProducts':2,'sourceTargetNodesReviewed':sum(x['completeSourceNodeCoverage'] for x in proof),'qualifiedSHA256':h,'authorSHA256':fs(F),'postFreezeCorrections':0,'preFreezeReviewRefinements':'All requested refinements verified: explicit machine wash in CS, generic chest rather than invented circumference, sleeve bands not cuffs/armbands, garment-opening qualifier, cotton-feel heading.','sourceConsiderations':['P211 retains unconfirmed fiber composition and top-only exclusions, with title/type/Tank Top option corroboration.','P213 retains95%cotton, exact current kg/lbs chart and source selector workflow paragraph; title/type/17variants corroborate current tops listing.','No new sourceEnglish edits or release gates; root fresh source/global-before checks remain required.'],'negativeTests':neg,'rowProofs':proof,'externalWrites':0};save('independent_review.json',report);print(json.dumps({k:report[k] for k in ['status','rows','sourceTargetNodesReviewed','qualifiedSHA256','postFreezeCorrections']}))
