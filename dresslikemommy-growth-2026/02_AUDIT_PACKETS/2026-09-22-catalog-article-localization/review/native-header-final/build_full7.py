# -*- coding: utf-8 -*-
"""Full current-source body reconstruction, not a partial outdated-field refresh."""
import copy,difflib,hashlib,html,json,re
from html.parser import HTMLParser
from pathlib import Path
from full7_manual import TEXT
H=Path(__file__).resolve().parent;R=H.parents[1]
load=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dump=lambda f,d:(H/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
source_texts=load(H/'full7_source_texts.json')
inv={(r['productIndex'],r['locale']):r for r in load(R/'review/body-structure-audit/effective_body_inventory.json')['rows']}
overlays=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_v2.json','review/size-label-repair/candidate_all156.json','review/size-label-repair/placeholder-review/placeholder88_reviewed.json','review/body-structure-audit/prose_completion11_candidates_v1.json','review/native-header-final/current22_candidates.json']
overlaykeys={f:{(r['resourceId'],r['locale']) for r in load(R/f)['rows']} for f in overlays}
products={}
for p in sorted((R/'products').glob('inventory_page_*.json')):
 for n in load(p)['data']['products']['nodes']:
  if n['id'] in {r['resourceId'] for k,r in inv.items() if k in TEXT}:products[n['id']]={'file':str(p.relative_to(R)),'fileSHA256':fs(p),'product':n}
roles={'cs':{'Mother':'Maminka','Father':'Tatínek'},'fi':{'Mother':'Äiti','Father':'Isä'},'ro':{'Mother':'Mamă','Father':'Tată'},'sv':{'Mother':'Mamma','Father':'Pappa'}}
def label(s,l):
 m=re.fullmatch(r'(Mother|Father) (S|M|L|XL|[2-5]XL)',s)
 if m:return roles[l][m[1]]+' '+m[2]
 m=re.fullmatch(r'Child (\d+(?:-\d+)?) Years',s)
 if m:
  age=m[1]
  return {'cs':'Dítě '+age+(' roky' if '-' not in age and 2<=int(age)<=4 else ' let'),'fi':'Lapsi '+age+' vuotta','ro':'Copil '+age+' ani','sv':'Barn '+age+' år'}[l]
 return None
class Parse(HTMLParser):
 def __init__(self,v):super().__init__(convert_charrefs=False);self.events=[];self.stack=[];self.errors=[];self.feed(v);self.close();assert not self.rawdata
 def handle_starttag(self,t,a):
  self.events.append((t,a))
  if t not in {'br','img','hr','input','meta','link','source','wbr'}:self.stack.append(t)
 def handle_endtag(self,t):
  self.events.append(('/'+t,[]))
  if not self.stack or self.stack[-1]!=t:self.errors.append((t,self.stack.copy()))
  else:self.stack.pop()
 def handle_startendtag(self,t,a):self.handle_starttag(t,a)
def tableproof(v):
 out=[]
 for t in re.findall(r'<table\b.*?</table>',v,re.S):
  grid=[]
  for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',t,re.S):grid.append([html.unescape(re.sub('<[^>]*>','',c[1])).strip() for c in re.findall(r'<(td|th)\b[^>]*>(.*?)</\1>',row,re.S)])
  out.append({'headers':grid[0],'dataRows':len(grid)-1,'firstDataRow':grid[1],'lastDataRow':grid[-1],'allNumericTokens':re.findall(r'\d+(?:[.,]\d+)?',t)})
 return out
def validate(r):
 s=r['sourceValue'];v=r['value'];mapping=dict(zip(source_texts[str(r['productIndex'])],TEXT[r['productIndex'],r['locale']]))
 pieces=re.split('(<[^>]+>)',s);pairs=[]
 for i in range(0,len(pieces),2):
  full=pieces[i];t=full.strip()
  if not t:continue
  tr=mapping.get(t)
  if tr is None:tr=label(t,r['locale'])
  if tr is None:
   assert not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',t)),('untranslated_source',t)
   continue
  prefix=len(full)-len(full.lstrip());suffix=len(full)-len(full.rstrip())
  pieces[i]=full[:prefix]+html.escape(tr,quote=False)+(full[len(full)-suffix:] if suffix else '')
  pairs.append({'textNodeIndex':i//2,'source':t,'target':tr})
 expected=''.join(pieces);assert expected==v
 assert re.findall(r'<[^>]*>',s)==re.findall(r'<[^>]*>',v)
 assert re.findall(r'\d+(?:[.,]\d+)?',s)==re.findall(r'\d+(?:[.,]\d+)?',v)
 assert re.findall(r'https?://[^\s<>"\']+',s)==re.findall(r'https?://[^\s<>"\']+',v)
 a,b=Parse(s),Parse(v);assert a.events==b.events and not b.errors and not b.stack
 sr=[re.findall(r'<td\b[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr\b[^>]*>(.*?)</tr>',s,re.S)]
 vr=[re.findall(r'<td\b[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr\b[^>]*>(.*?)</tr>',v,re.S)]
 assert len(sr)==len(vr)
 assert all(a[1:]==b[1:] for a,b in zip(sr,vr)), 'all current source measurement cells exact'
 assert sha(v)==r['valueSHA256'] and sha(s)==r['sourceSHA256']
 return pairs
rows=[];pairs=[];checks=[];table_diffs=[];corroboration=[]
for (index,l),translated in TEXT.items():
 original=inv[index,l];s=original['source'];before=original['before'];assert before['outdated'] is True
 assert len(translated)==len(source_texts[str(index)])
 for f,keys in overlaykeys.items():assert (original['resourceId'],l) not in keys,(f,index,l)
 p=R/original['rawFile'];assert fs(p)==original['rawFileSHA256'];n=next(n for n in load(p)['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==original['resourceId'])
 rawsource=next(t for t in n['translatableContent'] if t['key']=='body_html');rawbefore=next(t for t in n['tr_'+l] if t['key']=='body_html' and not t['market'])
 assert rawsource['value']==s and rawsource['digest']==original['sourceDigest'] and rawbefore==before
 supporting={t['key']:t for t in n['translatableContent'] if t['key'] in ('title','product_type')}
 assert supporting['product_type']['value']=='Matching Family Tops'
 assert 'Tank Top' in supporting['title']['value'] if index==211 else 'Tops' in supporting['title']['value']
 pi=products[original['resourceId']];prod=pi['product'];assert prod['variantsCount']['count']==(8 if index==211 else 17)
 if index==211:assert [v['name'] for op in prod['options'] if op['name']=='Type' for v in op['optionValues']]==['Tank Top']
 else:assert {op['name'] for op in prod['options']}=={'Size','Color'}
 mapping=dict(zip(source_texts[str(index)],translated));parts=re.split('(<[^>]+>)',s)
 for i in range(0,len(parts),2):
  full=parts[i];t=full.strip();tr=mapping.get(t)
  if tr is None:tr=label(t,l)
  if tr is not None:
   prefix=len(full)-len(full.lstrip());suffix=len(full)-len(full.rstrip());parts[i]=full[:prefix]+html.escape(tr,quote=False)+(full[len(full)-suffix:] if suffix else '')
 value=''.join(parts)
 r={'productIndex':index,'resourceId':original['resourceId'],'locale':l,'key':'body_html','marketId':None,'source':s,'sourceValue':s,'sourceDigest':rawsource['digest'],'sourceSHA256':sha(s),'before':before,'rawBefore':before,'rawFile':original['rawFile'],'rawFileSHA256':original['rawFileSHA256'],'beforeValueSHA256':sha(before['value']),'expectedBeforeValueSHA256':sha(before['value']),'value':value,'valueSHA256':sha(value),'supportingSourceDigests':{k:v['digest'] for k,v in supporting.items()},'corroboratingProductInventory':{'file':pi['file'],'fileSHA256':pi['fileSHA256'],'id':prod['id'],'optionNames':[x['name'] for x in prod['options']],'variantsCount':prod['variantsCount']['count'],'optionsSHA256':sha(json.dumps(prod['options'],ensure_ascii=False,sort_keys=True))},'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'AUTHOR_COMPLETE_FULL_SOURCE_TRANSLATION_PENDING_INDEPENDENT_FULL_REVIEW','reason':'Full current English source translated, including all prose and current tables. P211 obsolete two-piece claims and pants chart replaced by exact top-only source; P213 obsolete jin weights replaced by exact current kg/lbs values. No current English fact, measurement, HTML attribute or source workflow uncertainty is changed. Raw outdated:true field requires full-body review, not partial refresh.'}
 nodepairs=validate(r);rows.append(r);pairs.append({'productIndex':index,'resourceId':r['resourceId'],'locale':l,'sourceDigest':r['sourceDigest'],'nodes':nodepairs})
 table_diffs.append({'productIndex':index,'resourceId':r['resourceId'],'locale':l,'oldTables':tableproof(before['value']),'newCurrentSourceTables':tableproof(s),'valueTables':tableproof(value),'proof':'Every current-source measurement cell after first size label is byte-identical in target. Old chart data only removed/replaced because absent from current English. No conversion recomputed.'})
 corroboration.append({'productIndex':index,'locale':l,'resourceId':r['resourceId'],'sourceTitle':supporting['title'],'sourceType':supporting['product_type'],'productInventory':pi,'assessment':'Source211 top-only is corroborated by title, type and Tank Top option. Source213 tops are corroborated by title, type and actual17size/color variants; source-selector draft text refers to upstream supplier selector, remains literal, and is not silently rewritten or treated as actual current storefront options.'})
 (H/f'full7_{index}_{l}_old_to_new.diff').write_text(''.join(difflib.unified_diff(before['value'].splitlines(True),value.splitlines(True),fromfile='raw translated before',tofile='full current source translation')))
 checks.append({'productIndex':index,'locale':l,'sourceDigestRawBeforeBinding':'PASS','completeSourceTextNodeCoverage':'PASS','currentSourceMeasurementCellsByteIdentical':'PASS','allCurrentSourceNumericTokensExact':'PASS','sourceHTMLTagsAttributesURLsImagesExact':'PASS','standardHTMLParserBalanced':'PASS','plannedOverlayOverlap':0,'oldChartReplacementRequired':True,'translatedNodes':len(nodepairs)})
assert len(rows)==7
# Meaningful corruption checks protect full-table source reconstruction.
neg=[]
for name,mut in [('measurement_changed',lambda r:r.update(value=r['value'].replace('44 cm / 17.3 in','45 cm / 17.3 in',1))),('source_node_omitted',lambda r:r.update(value=r['value'].replace(TEXT[211,'cs'][19],'',1)))]:
 bad=copy.deepcopy(rows[0]);prior=bad['value'];mut(bad);assert bad['value']!=prior
 try:validate(bad)
 except AssertionError:neg.append({'case':name,'status':'REJECTED'})
 else:raise AssertionError('corrupt full body passed')
dump('full7_candidates.json',{'rows':rows});dump('full7_source_target_node_pairs.json',{'rows':pairs});dump('full7_old_new_table_proof.json',{'rows':table_diffs});dump('full7_title_type_options_corroboration.json',{'rows':corroboration});dump('full7_checks.json',{'status':'PASS_AUTHOR_FULL_SOURCE_RECONSTRUCTION_PENDING_INDEPENDENT_REVIEW','candidateRows':7,'candidateSHA256':fs(H/'full7_candidates.json'),'rows':checks,'mutationTests':neg,'sourceWorkflowNotesPreserved':True,'unknownFiberNotInvented':True,'externalWrites':0})
print(json.dumps({'rows':7,'candidateSHA256':fs(H/'full7_candidates.json'),'sourceNodes':sum(len(x['nodes']) for x in pairs)}))
