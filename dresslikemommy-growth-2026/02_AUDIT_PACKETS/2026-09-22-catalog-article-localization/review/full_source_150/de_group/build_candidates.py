# -*- coding: utf-8 -*-
"""Rebuild complete translated HTML from exact current source, with source/raw checks."""
import copy,difflib,hashlib,html,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from manual_common import COMMON
from manual_translations import TEXT
H=Path(__file__).resolve().parent;R=H.parents[2]
load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dump=lambda f,d:(H/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
SRC=load(H/'source_texts.json');WORK=load(H/'worklist44.json')['rows']
ROLES={'cs':('Dítě','Maminka','Tatínek'),'da':('Barn','Mor','Far'),'el':('Παιδί','Μαμά','Μπαμπάς'),'fi':('Lapsi','Äiti','Isä'),'no':('Barn','Mor','Far'),'ro':('Copil','Mamă','Tată')}
def trans(t,l,p):
 a=SRC[str(p)]
 if t in a and a.index(t) in TEXT[p,l]:return TEXT[p,l][a.index(t)]
 if t in COMMON[l]:return COMMON[l][t]
 m=re.fullmatch(r'(.+)( \((?:cm|in|kg|lbs|/)+\))',t)
 if m and m[1] in COMMON[l]:return COMMON[l][m[1]]+m[2]
 m=re.fullmatch(r'(Mother|Father) (S|M|L|XL|[2-5]XL)',t)
 if m:return ROLES[l][1 if m[1]=='Mother' else 2]+' '+m[2]
 m=re.fullmatch(r'Child (\d+(?:-\d+)?) Years',t)
 if m:
  age=m[1];suf={'cs':(' roky' if age=='1-2' or '-' not in age and 2<=int(age)<=4 else ' let'),'da':' år','el':' ετών','fi':' vuotta','no':' år','ro':' ani'}[l]
  return ROLES[l][0]+' '+age+suf
 m=re.fullmatch(r'Up to (.+)',t)
 if m:return {'cs':'Až ','da':'Op til ','el':'Έως ','fi':'Enintään ','no':'Opptil ','ro':'Până la '}[l]+m[1]
 if re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',t)):raise AssertionError(('missing_translation',p,l,t))
 return None
class Parse(HTMLParser):
 def __init__(self,v):
  super().__init__(convert_charrefs=False);self.events=[];self.stack=[];self.errors=[];self.feed(v);self.close();assert not self.rawdata
 def handle_starttag(self,t,a):
  self.events.append((t,a))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('/'+t,[]))
  if not self.stack or self.stack[-1]!=t:self.errors.append((t,self.stack.copy()))
  else:self.stack.pop()
 def handle_startendtag(self,t,a):self.events.append((t,a))
def assemble(r):
 s=r['sourceValue'];p=r['productIndex'];l=r['locale'];a=re.split('(<[^>]+>)',s);pairs=[]
 for i in range(0,len(a),2):
  full=a[i];t=full.strip()
  if not t:continue
  tr=trans(t,l,p)
  if tr is None:continue
  start=len(full)-len(full.lstrip());end=len(full)-len(full.rstrip())
  a[i]=full[:start]+html.escape(tr,quote=False)+(full[-end:] if end else '')
  pairs.append({'textNodeIndex':i//2,'source':html.unescape(t),'target':tr})
 return ''.join(a),pairs
def grid(v):
 return [[[html.unescape(re.sub('<[^>]*>','',c)).strip() for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',row,re.S)] for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',t,re.S)] for t in re.findall(r'<table\b.*?</table>',v,re.S)]
def validate(r):
 s=r['sourceValue'];v=r['value'];expected,pairs=assemble(r);assert expected==v
 assert sha(v)==r['valueSHA256'] and sha(s)==r['sourceSHA256']
 assert re.findall(r'<[^>]*>',s)==re.findall(r'<[^>]*>',v),'HTML tags and every attribute byte exact'
 assert re.findall(r'\d+(?:[.,]\d+)?',s)==re.findall(r'\d+(?:[.,]\d+)?',v),'all source numbers in exact order'
 assert re.findall(r'https?://[^\s<>"\']+',s)==re.findall(r'https?://[^\s<>"\']+',v)
 a,b=Parse(s),Parse(v);assert a.events==b.events and not b.errors and not b.stack,('HTML',r['productIndex'],r['locale'],b.errors,b.stack)
 sg,vg=grid(s),grid(v);assert len(sg)==len(vg)
 cellproof=[]
 for ti,(st,vt) in enumerate(zip(sg,vg)):
  assert len(st)==len(vt)
  for ri,(sr,vr) in enumerate(zip(st,vt)):
   assert len(sr)==len(vr)
   for ci,(sc,vc) in enumerate(zip(sr,vr)):
    if ri==0:continue
    if ci==0:assert trans(sc,r['locale'],r['productIndex'])==vc
    elif sc.startswith('Up to '):assert trans(sc,r['locale'],r['productIndex'])==vc
    else:assert sc==vc,('measurement',ti,ri,ci,sc,vc)
    cellproof.append({'table':ti,'row':ri,'cell':ci,'source':sc,'target':vc,'numericAndUnitsExact':True,'localizedOnly':ci==0 or sc.startswith('Up to ')})
 return pairs,cellproof
rows=[];nodepairs=[];checks=[];proof=[];unknown=[];support=[];rawcache={}
selection=set(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else None
for w in WORK:
 p=w['productIndex'];l=w['locale']
 if (p,l) not in TEXT or selection is not None and p not in selection:continue
 rawp=R/w['rawFile'];assert fs(rawp)==w['rawFileSHA256'];raw=rawcache.setdefault(str(rawp),load(rawp));n=next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==w['resourceId']);src=next(s for s in n['translatableContent'] if s['key']=='body_html');before=next(s for s in n['tr_'+l] if s['key']=='body_html' and not s['market'])
 assert src['value']==w['sourceValue'] and src['digest']==w['sourceDigest'] and before==w['rawBefore'];assert sha(w['expectedEffectiveBeforeValue'])==w['expectedBeforeValueSHA256']
 r=copy.deepcopy(w);v,pairs=assemble(r);r.update(value=v,valueSHA256=sha(v),reviewStatus='AUTHOR_COMPLETE_PENDING_INDEPENDENT_FULL_SOURCE_REVIEW',reason='Full current-source translation of all prose, headings, roles and current chart data, including source uncertainty and workflow notes. Source markup/attributes, URLs and every numeric token preserved. Supersedes outdated translated facts and charts only to match current English.',requiresFreshLiveSourceAndBeforeGuard=True,beforeGuardNote='Exact worklist effective-before provided; root must rebind to confirmed later native-header-semantics release before mutation.')
 r['supportingSourceDigests']={k['key']:k['digest'] for k in n['translatableContent'] if k['key'] in ['title','product_type']}
 pairs,cp=validate(r);rows.append(r);nodepairs.append({'productIndex':p,'locale':l,'resourceId':r['resourceId'],'sourceDigest':r['sourceDigest'],'nodes':pairs});proof.append({'productIndex':p,'locale':l,'sourceTables':grid(r['sourceValue']),'rawBeforeTables':grid(before['value']),'valueTables':grid(v),'measurementCells':cp})
 for pair in pairs:
  if re.search(r'exact fiber|not visible|unavailable|not estimated|blocked vendor|not publish|not charted|draft|operator|remain unlisted|no dad|not supplied|no S-2XL',pair['source'],re.I):unknown.append({'productIndex':p,'locale':l,**pair,'disposition':'English qualification/workflow preserved faithfully; English editorial cleanup separate, no invented source fact.'})
 support.append({'productIndex':p,'locale':l,'titleAndType':[s for s in n['translatableContent'] if s['key'] in ['title','product_type']]})
 checks.append({'productIndex':p,'locale':l,'sourceDigestRawBeforeBinding':'PASS','fullSourceNodeCoverage':'PASS','translatedNodes':len(pairs),'HTMLTagsAttributesURLsExact':'PASS','allNumericTokensExact':'PASS','allMeasurementCellsExact':'PASS','standardParserBalanced':'PASS','sourceUncertaintyAndWorkflowTranslated':'AUTHOR_REVIEWED_IN_PAIRS'})
assert rows
name=sys.argv[1] if len(sys.argv)>1 else 'candidate_all'
dump(name+'.json',{'rows':rows});dump(name+'_node_pairs.json',{'rows':nodepairs});dump(name+'_table_proof.json',{'rows':proof});dump(name+'_unknowns.json',{'rows':unknown});dump(name+'_supporting_source.json',{'rows':support})
neg=[]
for label,fn in [('alter_current_source_measurement',lambda r:r.update(value=r['value'].replace('cm','mm',1))),('omit_complete_prose_node',lambda r:r.update(value=r['value'].replace(html.escape(nodepairs[0]['nodes'][1]['target'],quote=False),'',1)))]:
 bad=copy.deepcopy(rows[0]);prev=bad['value'];fn(bad);assert prev!=bad['value'];bad['valueSHA256']=sha(bad['value'])
 try:validate(bad)
 except AssertionError:neg.append({'case':label,'result':'REJECTED'})
 else:raise AssertionError('corruption accepted')
dump(name+'_checks.json',{'status':'PASS_AUTHOR_CHECKS_PENDING_INDEPENDENT_REVIEW','rows':checks,'candidateRows':len(rows),'candidateSHA256':fs(H/(name+'.json')),'sourceTextNodesTranslated':sum(len(x['nodes']) for x in nodepairs),'mutationTests':neg,'sourceRawFilesVerified':len(rawcache),'externalWrites':0})
print(json.dumps({'rows':len(rows),'candidate':name+'.json','candidateSHA256':fs(H/(name+'.json')),'textNodes':sum(len(x['nodes']) for x in nodepairs)}))
