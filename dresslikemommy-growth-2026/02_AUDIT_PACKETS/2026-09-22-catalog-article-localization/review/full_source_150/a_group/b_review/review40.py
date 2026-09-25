from pathlib import Path
from html.parser import HTMLParser
import json,re,html,hashlib,copy,collections,importlib.util
O=Path(__file__).resolve().parent;P=O.parents[3];B=P/'review/full_source_150/b_group'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
input_file=B/'candidates40_v2.json';assert fs(input_file)=='ec959b2f84d1180d2c15371a0b3a4f0e0ccf02ead2071e0af751083cdf340869'
rows=copy.deepcopy(load(input_file)['rows']);pairs=load(B/'node_pairs40_v2.json')['rows']
ix={(r['productIndex'],r['locale']):r for r in rows}
pp={(r['productIndex'],r['locale'],r['nodeIndex']):r for r in pairs if r['kind']=='prose'}
corrections=[]
def edit(p,l,node,target,reason):
 q=pp[p,l,node];assert q['target']!=target
 corrections.append({'productIndex':p,'locale':l,'resourceId':ix[p,l]['resourceId'],'kind':'prose','nodeIndex':node,'source':q['source'],'old':q['target'],'new':target,'reason':reason})
# Restore precise physical care methods without changing temperatures.
for p,n in [(211,9),(213,9),(214,9),(215,10),(220,9)]:
 old=pp[p,'ar',n]['target'];new=old.replace('قلبها إلى الداخل','قلبها على الوجه الداخلي').replace('قلبه إلى الداخل','قلبه على الوجه الداخلي')
 edit(p,'ar',n,new,'Make inside-out orientation explicit; retain the exact source washing/drying/ironing instructions.')
for p,n in [(211,9),(213,9),(214,9),(215,10),(219,9),(220,9)]:
 old=pp[p,'ko',n]['target'];new=old.replace('자연 건조','걸어서 건조')
 edit(p,'ko',n,new,'Source specifies line drying; generic natural drying omitted the hanging method.')
edit(216,'ko',5,pp[216,'ko',5]['target'].replace('크로셰은','크로셰는'),'Correct Korean topic-particle agreement after a vowel-ending noun.')
edit(215,'hi',6,'डेज़ी की कढ़ाई है और साथ में आइवरी रंग की चौड़े पायंचों वाली पैंट है, जिस पर उसी रंग का फूलों वाला कटवर्क है।','Fix case agreement and bind tonal floral cutwork unambiguously to the ivory wide-leg pants; preserve the split inline sentence.')
edit(221,'hi',7,'भरे हुए घेर वाली परतदार ट्यूल की आकृति, खींचकर पहनने वाली कमर और माँ तथा बच्चे दोनों के लिए गोल घूमने पर लहराने वाला आकार।','Full describes the layered silhouette rather than density; twirling is rotation rather than walking around.')
edit(211,'he',3,pp[211,'he',3]['target'].replace('גופייה בהירה','גופייה בצבע עז'),'Bright in this vivid-red design means vibrant, not a light-colored garment.')
edit(214,'he',23,pp[214,'he',23]['target'].replace('אדום בהיר','אדום עז'),'Preserve vivid bright red rather than asserting a light shade of red.')
edit(213,'ja',23,pp[213,'ja',23]['target'].replace('袖のストライプ、','袖のストライプ柄の帯、'),'Restore striped sleeve bands, preserving both the band detail and stripe pattern.')
edit(213,'he',23,pp[213,'he',23]['target'].replace('פסי השרוולים','הרצועות המפוספסות שעל השרוולים'),'Restore striped sleeve bands, preserving both the band detail and stripe pattern.')
# A unit-labelled age format avoids invalid Arabic year agreement at 2/12 and ranges.
seen=set()
for q in pairs:
 if q['kind']=='td' and q['locale']=='ar' and re.fullmatch(r'Child [0-9-]+ Years',q['source']):
  k=(q['productIndex'],q['source']);
  if k in seen:continue
  seen.add(k);n=re.search(r'[0-9-]+',q['source'])[0]
  corrections.append({'productIndex':q['productIndex'],'locale':'ar','resourceId':q['resourceId'],'kind':'td','source':q['source'],'old':q['target'],'new':'طفل — العمر بالسنوات: '+n,'reason':'Use a grammatical unit-labelled age; exact role, age numerals and year unit remain unchanged.'})
for c in corrections:
 r=ix[c['productIndex'],c['locale']];parts=re.split('(<[^>]+>)',r['value']);matches=[]
 for j in range(0,len(parts),2):
  old=parts[j]
  if html.unescape(old).strip()!=c['old']:continue
  n=len(old)-len(old.lstrip());t=len(old)-len(old.rstrip());parts[j]=old[:n]+html.escape(c['new'],quote=False)+(old[-t:] if t else '');matches.append(j//2)
 assert matches,(c['productIndex'],c['locale'],c['old']);r['value']=''.join(parts);c['appliedTextNodeIndices']=matches;c['occurrences']=len(matches)

VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Parse(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.events=[];self.stack=[];self.cells=[];self.cell=None;self.prose=[];self.tables=0;self.feed(s);self.close();assert not self.stack and self.cell is None and not self.rawdata
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t not in VOID:self.stack.append(t)
  if t=='table':self.tables+=1
  if t in ('th','td'):assert self.cell is None;self.cell=[t,a,'']
 def handle_startendtag(self,t,a):self.events.append(('empty',t,a))
 def handle_endtag(self,t):
  self.events.append(('end',t));assert self.stack and self.stack[-1]==t,(t,self.stack);self.stack.pop()
  if t in ('th','td'):assert self.cell and self.cell[0]==t;self.cells.append(self.cell);self.cell=None
 def handle_data(self,s):
  if self.cell is not None:self.cell[2]+=s
  elif s.strip():self.prose.append(s.strip())
 def handle_comment(self,s):self.events.append(('comment',s))
 def handle_decl(self,s):self.events.append(('decl',s))
num=lambda s:re.findall(r'\d+(?:\.\d+)?',s)
units=lambda s:re.findall(r'\b(?:cm|in|kg|lbs)\b',s)
def preservation(source,value):
 assert re.findall(r'<[^>]+>',source)==re.findall(r'<[^>]+>',value),'raw markup'
 assert num(source)==num(value),'whole source numeric sequence'
 assert not re.search(r'QZ\d|QX\d|\dQXZ',value),'placeholder'
 a,b=Parse(source),Parse(value);assert a.events==b.events and a.tables==b.tables and len(a.cells)==len(b.cells);assert len(a.prose)==len(b.prose)
 numeric_cells=0
 for x,y in zip(a.cells,b.cells):
  assert x[:2]==y[:2] and num(x[2])==num(y[2]) and units(x[2])==units(y[2]),'cell numeric/unit'
  if x[0]=='td' and re.fullmatch(r'[\s\d.,/\-–—%]*(?:(?:cm|in|kg|lbs)[\s\d.,/\-–—%]*)*',x[2]):assert x[2]==y[2],'literal numeric cell';numeric_cells+=1
 return a,b,numeric_cells
rawcache={};overlays={};checks=[];qualified_pairs=[]
for r in rows:
 p,l=r['productIndex'],r['locale'];key=r['resourceId'],l,r['key'];r['valueSHA256']=sha(r['value'])
 rf=P/r['rawFile'];assert fs(rf)==r['rawFileSHA256']
 if rf not in rawcache:rawcache[rf]={n['resourceId']:n for n in load(rf)['data']['translatableResourcesByIds']['nodes']}
 n=rawcache[rf][r['resourceId']];ss={x['key']:x for x in n['translatableContent']};s=ss['body_html'];assert r['source']==r['sourceValue']==s['value'] and r['sourceDigest']==s['digest'];assert sha(r['source'])==r['sourceSHA256']
 rb=next(t for t in n['tr_'+l.replace('-','_')] if t['key']=='body_html' and not t.get('market'));assert rb==r['rawBefore'];effective=rb['value']
 for d in r['plannedBeforeDependencies']:
  of=P/d['file'];assert fs(of)==d['sha256']
  if of not in overlays:
   data=load(of);rr=data if isinstance(data,list) else data['rows'];overlays[of]={(x['resourceId'],x['locale'],x['key']):x for x in rr}
  ov=overlays[of][key];assert sha(ov['value'])==d['valueSHA256'];assert ov.get('sourceDigest')==r['sourceDigest'];effective=ov['value']
 assert effective==r['expectedEffectiveBeforeValue'];assert all(r[k]==sha(effective) for k in ['expectedEffectiveBeforeValueSHA256','beforeValueSHA256','expectedBeforeValueSHA256'])
 assert r['before'] is None and r['requiresFreshEffectiveBeforeObject'] and r['requiresFreshLiveSourceAndBeforeGuard']
 a,b,numeric=preservation(r['source'],r['value'])
 prose=[q for q in pairs if q['productIndex']==p and q['locale']==l and q['kind']=='prose'];table=[q for q in pairs if q['productIndex']==p and q['locale']==l and q['kind']!='prose'];assert a.prose==[q['source'] for q in prose];assert [x[2].strip() for x in a.cells]==[q['source'] for q in table]
 changed={(c['kind'],c['source'],c['old']):c['new'] for c in corrections if c['productIndex']==p and c['locale']==l}
 for q,v in zip(prose,b.prose):assert v==changed.get(('prose',q['source'],q['target']),q['target']);qualified_pairs.append({**q,'target':v})
 for q,v in zip(table,b.cells):assert v[2].strip()==changed.get((q['kind'],q['source'],q['target']),q['target']);qualified_pairs.append({**q,'target':v[2].strip()})
 cr=[c for c in corrections if c['productIndex']==p and c['locale']==l]
 r['independentReviewStatus']='QUALIFIED_FULL_CURRENT_SOURCE_MEANING_AND_PRESERVATION';r['reviewStatus']=r['independentReviewStatus'];r['independentReview']={'authorFile':str(input_file.relative_to(P)),'authorFileSHA256':fs(input_file),'proseNodesRead':len(prose),'tableNodesChecked':len(table),'correctionRules':len(cr),'correctedTextNodeOccurrences':sum(c['occurrences'] for c in cr),'sourceEnglishChanged':False,'rootFreshBeforeAndSourceGuardRequired':True}
 checks.append({'productIndex':p,'locale':l,'rawSourceDigestBeforeAndOverlayBindings':'PASS','sourceTagsAttributesCommentsParser':'PASS','allSourceNumericTokensAndTableUnits':'PASS','measurementCellsByteExact':numeric,'tables':a.tables,'completeProseNodesRead':len(prose),'completeTableNodesChecked':len(table),'correctionRules':len(cr),'correctedOccurrences':sum(c['occurrences'] for c in cr)})
assert len({(r['resourceId'],r['locale'],r['key']) for r in rows})==40
negative=[];s=rows[0]['source'];v=rows[0]['value']
for label,bad in [('drop-tag',re.sub('<[^>]+>','',v,count=1)),('alter-measurement',v.replace('96-105','96-106',1)),('drop-source-prose',re.sub(r'(<li>\s*<strong>[^<]+</strong>)[^<]+',r'\1',v,count=1)),('introduce-placeholder',v+' QZ012QZ0')]:
 try:preservation(s,bad)
 except AssertionError:negative.append(label)
 else:raise AssertionError('negative probe missed '+label)
qualified=O/'reviewed40.json';assert not qualified.exists();qualified.write_text(json.dumps({'rows':rows},ensure_ascii=False,indent=2)+'\n')
summary={'status':'QUALIFIED_40_PENDING_ROOT_FRESH_GUARDED_RELEASE','candidateFile':str(qualified.relative_to(P)),'candidateSHA256':fs(qualified),'authorFileSHA256':fs(input_file),'rows':40,'proseNodesFullyRead':sum(r['completeProseNodesRead'] for r in checks),'tableNodesSourceCompared':sum(r['completeTableNodesChecked'] for r in checks),'distinctHeaderConceptsReviewed':90,'rawFilesHashVerified':len(rawcache),'plannedOverlayFilesHashVerified':len(overlays),'correctionRules':len(corrections),'correctedOccurrences':sum(c['occurrences'] for c in corrections),'rowsWithCorrections':len({(c['productIndex'],c['locale']) for c in corrections}),'negativeProbesRejected':negative,'sourceDispositions':'All existing unknown composition, source access, workflow, exclusions and unavailable measurement qualifications translated; source English unchanged. No added approval gates.','externalWrites':0,'checks':checks}
for name,data in [('corrections.json',corrections),('reviewed_node_pairs40.json',{'rows':qualified_pairs}),('independent_review.json',summary)]:
 f=O/name;assert not f.exists();f.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},ensure_ascii=False))
