from pathlib import Path
import json,re,html,hashlib,runpy,importlib.util,copy
from html.parser import HTMLParser
O=Path(__file__).resolve().parent;P=O.parents[3]
load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
W=load(O/'worklist.json')['rows'];S=load(O/'source_texts.json');T=runpy.run_path(str(O/'manual.py'))['TEXT'];rows=[];pairs=[];evidence=[]
files=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json','review/size-label-repair/candidate_root_reviewed156.json','review/size-label-repair/placeholder-review/placeholder88_root_bound.json','review/body-header-localization/prose-completion-review/prose_completion11_root_bound.json','review/native-header-final/current22_root_reviewed.json','review/native-header-semantics-independent/full7/full7_reviewed.json','review/native-header-semantics-independent/native_header2145_reviewed.json']
overlays=[]
for f in files:
 d=load(P/f);rr=d if isinstance(d,list) else d['rows'];overlays.append((f,{(r['resourceId'],r['locale'],r['key']):r for r in rr}))
for w in W:
 pi=w['productIndex'];ss=S[str(pi)];tt=T[pi];assert len(ss)==len(tt);dictionary=dict(zip(ss,tt));parts=re.split('(<[^>]+>)',w['source']);nodes=[]
 for i in range(0,len(parts),2):
  old=parts[i];v=html.unescape(old).strip()
  if not v:continue
  new=dictionary.get(v)
  if new is None:
   m=re.fullmatch(r'Child ([0-9-]+) Years',v)
   if m:new='Lapsi '+m[1]+' vuotta'
   elif re.fullmatch(r'Adult (S|M|L|XL|2XL|3XL)',v):new=v.replace('Adult','Aikuinen')
  if new is None:assert not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',v));continue
  lead=len(old)-len(old.lstrip());trail=len(old)-len(old.rstrip());parts[i]=old[:lead]+html.escape(new,quote=False)+(old[-trail:] if trail else '');nodes.append({'textNodeIndex':i//2,'source':v,'target':new})
 value=''.join(parts);effective=w['expectedEffectiveBeforeValue'];deps=[]
 for f,om in overlays:
  ov=om.get((w['resourceId'],'fi','body_html'))
  if ov:
   assert ov['sourceDigest']==w['sourceDigest'];effective=ov['value'];deps.append({'file':f,'sha256':fs(P/f),'valueSHA256':sha(effective)})
 raw=load(P/w['rawFile']);n=next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==w['resourceId']);sc={x['key']:x for x in n['translatableContent']}
 r={k:w[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']};r.update({'marketId':None,'sourceValue':w['source'],'before':None,'expectedEffectiveBeforeValue':effective,'expectedEffectiveBeforeValueSHA256':sha(effective),'beforeValueSHA256':sha(effective),'expectedBeforeValueSHA256':sha(effective),'plannedBeforeDependencies':deps,'value':value,'valueSHA256':sha(value),'requiresFreshEffectiveBeforeObject':True,'requiresFreshLiveSourceAndBeforeGuard':True,'supportingSourceDigests':{k:sc[k]['digest'] for k in ['title','product_type']},'reviewStatus':'AUTHOR_FULL_CURRENT_SOURCE_COMPLETE_PENDING_ROOT_INDEPENDENT_REVIEW','reason':'Full current-source Finnish replacement resolves stale chart/prose. Remove obsolete target-only chart, preserve every current English source tag/attribute, measurement value/unit/blank cell and stated garment scope. No source edits.'});rows.append(r);pairs.append({'productIndex':pi,'resourceId':w['resourceId'],'locale':'fi','nodes':nodes})
 invs=[]
 for ip in sorted((P/'products').glob('inventory_page_*.json')):
  for x in load(ip)['data']['products']['nodes']:
   if x['id']==w['resourceId']:invs.append({'file':str(ip.relative_to(P)),'sha256':fs(ip),'product':x})
 assert len(invs)==1
 evidence.append({'productIndex':pi,'titleSource':sc['title'],'productTypeSource':sc['product_type'],'optionsEvidence':invs[0],'sourceTables':len(re.findall(r'<table\b',w['source'])),'expectedBeforeTables':len(re.findall(r'<table\b',effective)),'candidateTables':len(re.findall(r'<table\b',value)),'obsoleteTargetOnlyTablesRemoved':len(re.findall(r'<table\b',effective))-len(re.findall(r'<table\b',value)),'unresolvedSourceConflicts':[],'decision':'P164 separately selected Shirt/Shorts and56 variants corroborate both garment size runs; current English has no table.' if pi==164 else 'P20613 size variants exactly match current13-row Child/Adult table; current source has no hip/waist columns. Tiny heart patch at chest pocket is not a heart-shaped pocket.'})
spec=importlib.util.spec_from_file_location('guard',P/'review/full_source_150/verify_full_source_candidates.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);check=m.verify(rows)
class Parser(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.stack=[];self.events=[];self.feed(s);self.close();assert not self.stack and not self.rawdata
 def handle_starttag(self,t,a):
  self.events.append(('start',t,a))
  if t not in ['meta','br','img','hr','input','link','wbr','source','area','base','col','embed','param','track']:self.stack.append(t)
 def handle_endtag(self,t):self.events.append(('end',t));assert self.stack and self.stack.pop()==t
for r in rows:assert Parser(r['source']).events==Parser(r['value']).events
candidate=O/'candidates2.json';assert not candidate.exists();candidate.write_text(json.dumps({'rows':rows},ensure_ascii=False,indent=2)+'\n')
for f,d in [('node_pairs2.json',{'rows':pairs}),('source_correspondence_evidence.json',{'rows':evidence}),('checks2.json',{'status':'AUTHOR_PASS_PENDING_ROOT_INDEPENDENT_REVIEW','candidateSHA256':fs(candidate),'fullyTranslatedNodes':sum(len(x['nodes']) for x in pairs),'exactSourceMarkupAndStandardParser':'PASS','sourceEnglishChanged':False,'rootFreshSourceAndBeforeGuardRequired':True,**check})]:
 q=O/f;assert not q.exists();q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(candidate.relative_to(P)),'sha256':fs(candidate),'rows':len(rows),'textNodes':sum(len(x['nodes']) for x in pairs),'tableCounts':[(x['productIndex'],x['sourceTables'],x['expectedBeforeTables'],x['candidateTables']) for x in evidence]}))
