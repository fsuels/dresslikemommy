import json,re,html,hashlib,collections,pathlib
from html.parser import HTMLParser
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1];I=P/'review/body-structure-audit/effective_body_inventory.json'
rows=json.loads(I.read_text())['rows'];sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
class Tables(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tables=[];self.t=None;self.row=None;self.cell=None
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='table':self.t={'attrs':a,'rows':[]};self.tables.append(self.t)
  elif t=='tr' and self.t is not None:self.row=[];self.t['rows'].append(self.row)
  elif t in ['td','th'] and self.row is not None:self.cell={'tag':t,'colspan':a.get('colspan','1'),'rowspan':a.get('rowspan','1'),'text':''};self.row.append(self.cell)
 def handle_endtag(self,t):
  if t in ['td','th']:self.cell=None
  elif t=='tr':self.cell=None;self.row=None
  elif t=='table':self.t=None;self.row=None;self.cell=None
 def handle_data(self,s):
  if self.cell is not None:self.cell['text']+=s
 def get(self,v):
  self.feed(v)
  for t in self.tables:
   for r in t['rows']:
    for c in r:c['text']=' '.join(c['text'].split())
  return self.tables
num=lambda s:[x.replace(',', '.') for x in re.findall(r'\d+(?:[.,]\d+)?',s)]
def signature(t):
 return [( [(c['tag'],c['colspan'],c['rowspan']) for c in r], [num(c['text']) if c['tag']=='td' else [] for c in r] ) for r in t['rows']]
def aligned(s,t):
 if len(s['rows'])!=len(t['rows']):return None
 sh=th=None;projections=0
 for sr,tr in zip(s['rows'],t['rows']):
  if [(c['tag'],c['colspan'],c['rowspan']) for c in sr]!=[(c['tag'],c['colspan'],c['rowspan']) for c in tr]:return None
  if all(c['tag']=='th' for c in sr):sh=sr;th=tr;continue
  for ci,(sc,tc) in enumerate(zip(sr,tr)):
   if sc['tag']!='td':continue
   if num(sc['text'])==num(tc['text']):continue
   if sh is None or len(sh)!=len(sr):return None
   source_header=sh[ci]['text'];target_header=th[ci]['text']
   metric_only=(re.search(r'\((?:cm|kg)\)',target_header) and re.search(r'\((?:cm|kg)/',source_header))
   if not metric_only or '/' not in sc['text'] or num(sc['text'].split('/',1)[0])!=num(tc['text']):return None
   projections+=1
 return {'metricOnlySourceProjections':projections,'normalizedDecimalSeparatorsOnly':True,'allTargetDataNumericValuesMatchCorrespondingSourceComponent':True}
patterns={'cs':r'Srukáv|SDélka|Srameno|Sobjímka','de':r'Rempfohlen','es':r'HCadera|Haltura|Halto','fi':r'^Lanka','ro':r'Torace/Burt|Torace/Bupt|^Manec(?:\s|\()','sv':r'Bryst/Byst'}
# Source meaning is verified for every use before this target-only spelling/meaning proposal is qualified.
rep={
'cs':{'SDélka rukávu':'Délka rukávu','Sobjímka':'Rukáv','Srukáv':'Rukáv','Srameno':'Rameno'},
'de':{'Rempfohlenes':'Empfohlenes','Rempfohlene':'Empfohlene'},
'es':{'HCadera':'Cadera','Haltura':'Altura','Halto':'Altura'},
'fi':{'Lanka':'Lantio'},
'ro':{'Torace/Burt':'Torace/bust','Torace/Bupt':'Torace/bust','Manec':'Mânecă'},
'sv':{'Bryst/Byst':'Bröst/byst'},
}
expected={'SDélka rukávu':'Sleeve Length','Sobjímka':'Sleeve','Srukáv':'Sleeve','Srameno':'Shoulder','Rempfohlenes':'Recommended Weight','Rempfohlene':'Recommended Height','HCadera':'Hip','Haltura':'Height','Halto':'Height','Lanka':'Hip','Torace/Burt':'Chest/Bust','Torace/Bupt':'Chest/Bust','Manec':'Sleeve','Bryst/Byst':'Chest/Bust'}
uses=[];held=[]
for r in rows:
 l=r['locale']
 if l not in patterns:continue
 src=Tables().get(r['source']);tar=Tables().get(r['expectedEffectiveBeforeValue'])
 for ti,t in enumerate(tar):
  sig=signature(t);alignments={si:aligned(s,t) for si,s in enumerate(src)};matches=[si for si,a in alignments.items() if a is not None]
  for ri,tr in enumerate(t['rows']):
   for ci,c in enumerate(tr):
    h=c['text']
    if c['tag']!='th' or not re.search(patterns[l],h):continue
    prefix=next(k for k in rep[l] if k in h);new=h.replace(prefix,rep[l][prefix]);want=expected[prefix]
    sourcecells=[{'tableIndex':si,'rowIndex':ri,'cellIndex':ci,'header':src[si]['rows'][ri][ci]['text'],'alignmentEvidence':alignments[si]} for si in matches]
    # Numeric fingerprint plus source header meaning is required; no positional-only inference.
    qualified=[x for x in sourcecells if (want in x['header'] or (want=='Hip' and x['header'].startswith('Hips')))]
    success=bool(qualified) and len({x['header'] for x in qualified})==1
    obj={'resourceId':r['resourceId'],'productIndex':r['productIndex'],'locale':l,'key':'body_html','targetTableIndex':ti,'targetRowIndex':ri,'targetCellIndex':ci,'beforeLabel':h,'proposedLabel':new,'sourceCandidates':sourcecells,'qualifiedSourceCells':qualified,'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'beforeValueSHA256':r['expectedEffectiveBeforeValueSHA256'],'effectiveOutdated':False if r['overlayApplied'] else r['rawBefore']['outdated'],'rawFile':r['rawFile'],'rawFileSHA256':r['rawFileSHA256'],'overlayFile':r['overlayFile'],'overlayFileSHA256':r['overlayFileSHA256'],'tableRowCellShapeNumericFingerprintSHA256':sha(json.dumps(sig,ensure_ascii=False)),'bindingResult':'EXACT_ROW_CELL_SHAPE_WITH_NUMERIC_VALUES_MATCHED_TO_FULL_OR_EXPLICIT_METRIC_SOURCE_COMPONENT' if success else 'HOLD_TABLE_ALIGNMENT_OR_MEANING_NOT_CONFIRMED'}
    if success:uses.append(obj)
    else:held.append(obj)
groups=collections.defaultdict(list)
for x in uses:groups[(x['locale'],x['beforeLabel'],x['proposedLabel'],x['qualifiedSourceCells'][0]['header'])].append(x)
maps=[]
for (l,b,a,s),u in sorted(groups.items()):maps.append({'locale':l,'beforeLabel':b,'proposedLabel':a,'exactEnglishSourceHeader':s,'count':len(u),'currentFalseOccurrences':sum(not x['effectiveOutdated'] for x in u),'outdatedTrueOccurrences':sum(x['effectiveOutdated'] for x in u),'sourceBinding':'Every use has exact source/target table row and colspan/rowspan shape plus decimal-normalized per-cell numeric equality, or explicitly metric-only headers with exact source metric component equality; complete evidence in native_header_bound_occurrences.json.','uses':[{'resourceId':x['resourceId'],'productIndex':x['productIndex'],'targetTableIndex':x['targetTableIndex'],'targetRowIndex':x['targetRowIndex'],'targetCellIndex':x['targetCellIndex'],'sourceDigest':x['sourceDigest'],'beforeValueSHA256':x['beforeValueSHA256']} for x in u]})
for n,d in [('native_header_bound_occurrences.json',{'rows':uses}),('native_header_alignment_holds.json',{'rows':held}),('native_mapping_supplement.json',{'status':'PROPOSED_PENDING_ROOT_INDEPENDENT_REVIEW','rows':maps})]:(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(O/'native_mapping_compact.tsv').write_text('locale\tEnglish_source_header\tbefore\tafter\tcurrent\toutdated\n'+''.join(f"{x['locale']}\t{x['exactEnglishSourceHeader']}\t{x['beforeLabel']}\t{x['proposedLabel']}\t{x['currentFalseOccurrences']}\t{x['outdatedTrueOccurrences']}\n" for x in maps))
print('bound',len(uses),'held',len(held),'mappings',len(maps),'current',sum(not x['effectiveOutdated'] for x in uses),'outdated',sum(x['effectiveOutdated'] for x in uses));print('Holds',collections.Counter((x['locale'],x['beforeLabel']) for x in held));print((O/'native_mapping_compact.tsv').read_text())
