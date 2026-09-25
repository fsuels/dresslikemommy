import json,re,html,hashlib,collections,ast,unicodedata
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
module=ast.parse((B/'review/body-header-localization/native_header_evidence.py').read_text());ns={'HTMLParser':HTMLParser};exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.ClassDef)],type_ignores=[]),'<table parser>','exec'),ns);Tables=ns['Tables']
raw=json.loads((B/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows'];overlays={};files=[]
for rel in ['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json']:
 p=B/rel;fsha=hashlib.sha256(p.read_bytes()).hexdigest();rs=json.loads(p.read_text())['rows'];files.append({'file':rel,'sha256':fsha,'rows':len(rs)})
 for r in rs:overlays[r['resourceId'],r['locale']]=(r,rel,fsha)
exclude={(r['resourceId'],r['locale'],r['targetTableIndex'],r['targetRowIndex'],r['targetCellIndex']) for r in json.loads((B/'review/body-header-localization/native_header_alignment_holds.json').read_text())['rows']};assert len(exclude)==31
nums=lambda s:tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',unicodedata.normalize('NFKC',s)))
def aligned(s,t):
 if len(s['rows'])!=len(t['rows']):return None
 sh=th=None;projections=0;reordered=0
 for sr,tr in zip(s['rows'],t['rows']):
  if [(c['tag'],c['colspan'],c['rowspan']) for c in sr]!=[(c['tag'],c['colspan'],c['rowspan']) for c in tr]:return None
  if all(c['tag']=='th' for c in sr):sh,th=sr,tr;continue
  for ci,(sc,tc) in enumerate(zip(sr,tr)):
   if sc['tag']!='td' or ci==0:continue # size labels are reviewed separately; measurement columns define this match.
   sn,tn=nums(sc['text']),nums(tc['text'])
   if sn==tn:continue
   if len(sn)>1 and sorted(sn)==sorted(tn):reordered+=1;continue # exact same per-cell numbers; common RTL range reordering.
   if sh is not None and len(sh)==len(sr) and re.search(r'\((?:cm|kg)\)',th[ci]['text']) and '/' in sc['text'] and nums(sc['text'].split('/',1)[0])==tn:projections+=1;continue
   return None
 return {'rowAndCellTagSpanShapeEqual':True,'measurementNumbersPerCorrespondingCellExact':True,'sizeLabelColumnExcludedBecauseSeparateAudit':True,'reorderedWithinCellNumericMatches':reordered,'explicitMetricOnlyProjections':projections}
alluses=[];holds=[];coverage=[];cache={};usedexclude=[];effective=[]
for r in raw:
 k=r['resourceId'],r['locale'];ov=overlays.get(k);v=ov[0]['value'] if ov else r['expectedEffectiveBeforeValue'];outdated=False if ov or r['overlayApplied'] else r['rawBefore']['outdated'];source=cache.setdefault(r['resourceId'],Tables().get(r['source']));target=Tables().get(v or '');bodycount=0
 effective.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'effectiveOutdated':outdated,'value':v,'effectiveValueSHA256':sha(v or ''),'plannedOverlay':{'file':ov[1],'sha256':ov[2]} if ov else None,'sourceDigest':r['sourceDigest']})
 for ti,t in enumerate(target):
  matches=[(si,e) for si,s in enumerate(source) if (e:=aligned(s,t)) is not None]
  for ri,tr in enumerate(t['rows']):
   for ci,c in enumerate(tr):
    if c['tag']!='th':continue
    bodycount+=1;key=(r['resourceId'],r['locale'],ti,ri,ci)
    if key in exclude:usedexclude.append(key);continue
    ss=[{'sourceTableIndex':si,'sourceRowIndex':ri,'sourceCellIndex':ci,'sourceHeader':source[si]['rows'][ri][ci]['text'],'evidence':e} for si,e in matches]
    status='SOURCE_COLUMN_BOUND' if ss and len({x['sourceHeader'] for x in ss})==1 else 'SOURCE_TABLE_ALIGNMENT_OR_UNIQUE_HEADER_UNPROVED'
    use={'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'targetTableIndex':ti,'targetRowIndex':ri,'targetCellIndex':ci,'targetHeader':c['text'],'sourceHeader':ss[0]['sourceHeader'] if status=='SOURCE_COLUMN_BOUND' else None,'sourceMatches':ss,'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'effectiveValueSHA256':sha(v or ''),'effectiveOutdated':outdated,'status':status}
    (alluses if status=='SOURCE_COLUMN_BOUND' else holds).append(use)
 coverage.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'targetTables':len(target),'headerOccurrences':bodycount})
groups=collections.defaultdict(list)
for u in alluses:groups[u['locale'],u['sourceHeader'],u['targetHeader']].append(u)
summary={'scopeBodies':4760,'plannedOverlays':files,'sourceBoundHeaderOccurrences':len(alluses),'alignmentHeldHeaderOccurrences':len(holds),'excludedNative31Occurrences':len(usedexclude),'uniqueBoundSourceTargetPairs':len(groups),'effectiveOutdatedBoundOccurrences':sum(x['effectiveOutdated'] for x in alluses),'pairsByLocale':dict(collections.Counter(k[0] for k in groups))};assert len(usedexclude)==31
pairs=[{'pairIndex':i,'locale':k[0],'sourceHeader':k[1],'targetHeader':k[2],'count':len(u),'currentCount':sum(not x['effectiveOutdated'] for x in u),'outdatedCount':sum(x['effectiveOutdated'] for x in u),'uses':u} for i,(k,u) in enumerate(sorted(groups.items()))]
for name,obj in [('inventory_summary.json',summary),('source_bound_pairs.json',{'rows':pairs}),('alignment_holds.json',{'rows':holds}),('coverage4760.json',{'rows':coverage}),('effective_body_values.json',{'rows':effective})]:(H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(H/'pairs_compact.tsv').write_text('index\tlocale\tsource\ttarget\tcurrent\toutdated\n'+''.join(f"{r['pairIndex']}\t{r['locale']}\t{r['sourceHeader']}\t{r['targetHeader']}\t{r['currentCount']}\t{r['outdatedCount']}\n" for r in pairs));print(json.dumps(summary))
