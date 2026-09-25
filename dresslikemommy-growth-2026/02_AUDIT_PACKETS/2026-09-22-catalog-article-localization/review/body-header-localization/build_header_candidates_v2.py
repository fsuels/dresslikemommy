import json,pathlib,hashlib,re,html,collections,copy
from html.parser import HTMLParser
O=pathlib.Path(__file__).resolve().parent;P=O.parents[1]
J=lambda p:json.loads(p.read_text());sha=lambda s:hashlib.sha256(s.encode()).hexdigest();fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
I=P/'review/body-structure-audit/effective_body_inventory.json';S=P/'review/article-title-independent/body_structure375_reviewed.json';M=O/'proposed_language_mappings_v3.json';N=O/'native_mapping_supplement.json';B=O/'native_header_bound_occurrences.json'
assert fs(S)=='f8ae9d61b29a01f6628edf21cbf84421efd9c893f7d40f1e86c13538818ac501'
assert fs(M)=='adc34f1212e462433764b2518b0344acac1dd9f64094cfe7f643dfdee332a1cf'
base=J(I)['rows'];struct={(r['resourceId'],r['locale']):r for r in J(S)['rows']}
maps={(r['locale'],r['beforeLabel']):r for r in J(M)['rows']}
native=collections.defaultdict(list)
for r in J(B)['rows']:native[(r['resourceId'],r['locale'])].append(r)
HP=re.compile(r'(<th(?:\s[^>]*)?>)(.*?)(</th\s*>)',re.S|re.I)
plain=lambda s:' '.join(html.unescape(re.sub('<[^>]*>',' ',s)).split())
class Locate(HTMLParser):
 def __init__(self,v):
  super().__init__(convert_charrefs=False);self.lines=[0];self.lines.extend(m.end() for m in re.finditer('\n',v));self.ti=-1;self.ri=-1;self.ci=-1;self.inside=False;self.cells={};self.feed(v)
 def handle_starttag(self,t,a):
  if t=='table':self.ti+=1;self.ri=-1;self.inside=True
  elif t=='tr' and self.inside:self.ri+=1;self.ci=-1
  elif t in ['th','td'] and self.inside:
   self.ci+=1
   if t=='th':line,col=self.getpos();self.cells[(self.ti,self.ri,self.ci)]=self.lines[line-1]+col
 def handle_endtag(self,t):
  if t=='table':self.inside=False
class Parse(HTMLParser):
 def __init__(self,v):super().__init__(convert_charrefs=False);self.events=[];self.data=[];self.feed(v)
 def handle_starttag(self,t,a):self.events.append(('start',t,a))
 def handle_endtag(self,t):self.events.append(('end',t))
 def handle_startendtag(self,t,a):self.events.append(('empty',t,a))
 def handle_data(self,d):self.data.append(d)
 def handle_entityref(self,n):self.data.append('&'+n+';')
 def handle_charref(self,n):self.data.append('&#'+n+';')
NUM=re.compile(r'\d+(?:[.,]\d+)?')
TAGS=re.compile(r'<[^>]*>');TD=re.compile(r'<td(?:\s[^>]*)?>.*?</td\s*>',re.S|re.I)
mask=lambda v:HP.sub(lambda m:m[1]+'[UNCHANGED_HEADER_TEXT_SCOPE]'+m[3],v)
rows=[];checks=[];applied=[];held=[];overlaydelta=[]
for r in base:
 k=r['resourceId'],r['locale'];sr=struct.get(k);v=sr['value'] if sr else r['expectedEffectiveBeforeValue']
 if sr:
  assert sr['sourceDigest']==r['sourceDigest'] and sr['source']==r['source']
  assert sr['expectedBeforeValueSHA256']==r['expectedEffectiveBeforeValueSHA256'],k
  assert sr['valueSHA256']==sha(v)
  old=collections.Counter(plain(m[2]) for m in HP.finditer(r['expectedEffectiveBeforeValue']));new=collections.Counter(plain(m[2]) for m in HP.finditer(v))
  if old!=new:overlaydelta.append({'resourceId':k[0],'locale':k[1],'addedHeaders':list((new-old).elements()),'removedHeaders':list((old-new).elements())})
 effective_outdated=False if sr or r['overlayApplied'] else r['rawBefore']['outdated']
 nbypos={}
 if native.get(k):
  assert all(n['beforeValueSHA256']==sha(v) for n in native[k]),k
  loc=Locate(v)
  for n in native[k]:
   assert not n['effectiveOutdated']
   pos=loc.cells[(n['targetTableIndex'],n['targetRowIndex'],n['targetCellIndex'])]
   nbypos[pos]=n
 changes=[];pieces=[];last=0
 for hi,m in enumerate(HP.finditer(v)):
  label=plain(m[2]);mapping=maps.get((r['locale'],label));n=nbypos.get(m.start())
  if not(mapping or n):continue
  if mapping and n:assert mapping['proposedLabel']==n['proposedLabel']
  after=mapping['proposedLabel'] if mapping else n['proposedLabel']
  if n:assert label==n['beforeLabel']
  if effective_outdated:
   held.append({'resourceId':k[0],'locale':k[1],'productIndex':r['productIndex'],'headerIndex':hi,'beforeLabel':label,'proposedLabel':after,'reason':'EFFECTIVE_BODY_OUTDATED_REQUIRES_COMPLETE_BODY_REVIEW','sourceDigest':r['sourceDigest'],'beforeValueSHA256':sha(v)})
   continue
  assert '<' not in m[2] and '<' not in after and '>' not in after
  prefix=re.match(r'\s*',m[2]).group();suffix=re.search(r'\s*$',m[2]).group();newinner=after
  if '&mdash;' in m[2]:newinner=newinner.replace('—','&mdash;')
  newinner=prefix+newinner+suffix
  assert NUM.findall(m[2])==NUM.findall(newinner),(k,label,after)
  newcell=m[1]+newinner+m[3]
  pieces.append(v[last:m.start()]);pieces.append(newcell);last=m.end()
  c={'resourceId':k[0],'locale':k[1],'productIndex':r['productIndex'],'headerIndex':hi,'cellStart':m.start(),'cellEnd':m.end(),'beforeCellHTML':m[0],'afterCellHTML':newcell,'beforeLabel':label,'afterLabel':after,'mappingLane':'ROOT_REVIEWED_ENGLISH_OR_ORTHOGRAPHY' if mapping else 'ROOT_REVIEWED_NATIVE_CORRUPTION_WITH_SOURCE_COLUMN_EVIDENCE','beforeCellSHA256':sha(m[0]),'afterCellSHA256':sha(newcell),'nativeSourceCells':n['qualifiedSourceCells'] if n else None}
  changes.append(c)
 if not changes:continue
 pieces.append(v[last:]);value=''.join(pieces)
 a=Parse(v);b=Parse(value)
 ck={'resourceId':k[0],'locale':k[1],'headerCellsChanged':len(changes),'sourceSHA256Pass':sha(r['source'])==r['sourceSHA256'],'beforeValueSHA256':sha(v),'valueSHA256':sha(value),'rawBeforeValueSHA256':sha(r['rawBefore']['value']) if r['rawBefore'] else None,'nonHeaderBytesExact':mask(v)==mask(value),'tagBytesExact':TAGS.findall(v)==TAGS.findall(value),'independentHTMLParserTagAttributeEventsExact':a.events==b.events,'allNumericTokensExact':NUM.findall(v)==NUM.findall(value),'allDataCellsExact':TD.findall(v)==TD.findall(value),'headerCountExact':len(list(HP.finditer(v)))==len(list(HP.finditer(value))),'finalReviewedStructuralOverlayApplied':bool(sr),'priorVerifiedBodyOverlayApplied':r['overlayApplied']}
 assert all(ck[x] for x in ['sourceSHA256Pass','nonHeaderBytesExact','tagBytesExact','independentHTMLParserTagAttributeEventsExact','allNumericTokensExact','allDataCellsExact','headerCountExact']),ck
 ovfile=str(S.relative_to(P)) if sr else r['overlayFile'];ovsha=fs(S) if sr else r['overlayFileSHA256'];needsfresh=bool(sr or r['overlayApplied'])
 candidate={'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'key':'body_html','marketId':None,'source':r['source'],'sourceValue':r['source'],'sourceDigest':r['sourceDigest'],'sourceSHA256':r['sourceSHA256'],'before':None if needsfresh else r['before'],'rawBefore':r['rawBefore'],'rawFile':r['rawFile'],'rawFileSHA256':r['rawFileSHA256'],'value':value,'valueSHA256':sha(value),'beforeValueSHA256':sha(v),'expectedBeforeValueSHA256':sha(v),'expectedEffectiveBeforeValueSHA256':sha(v),'expectedEffectiveBeforeValue':v,'overlayApplied':needsfresh,'overlayFile':ovfile,'overlayFileSHA256':ovsha,'overlaySourceFile':ovfile,'overlaySourceFileSHA256':ovsha,'requiresFreshEffectiveBeforeObject':needsfresh,'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'ROOT_REVIEWED_LABEL_DICTIONARY_AND_NATIVE_SOURCE_BINDINGS; GENERATED_CANDIDATE_PENDING_INDEPENDENT_PARITY_REVIEW','reason':'Change only reviewed table-header text. Preserve all prose, data cells, numbers, unit symbols, HTML tags and attributes. Exact final independently reviewed375 structural overlay applied first where overlapping.','onlineStoreUrl':r['onlineStoreUrl'],'mappingFile':str(M.relative_to(P)),'mappingFileSHA256':fs(M),'nativeMappingFile':str(N.relative_to(P)),'nativeMappingFileSHA256':fs(N),'appliedHeaderCells':len(changes),'checks':ck}
 rows.append(candidate);checks.append(ck);applied+=changes
assert len({(r['resourceId'],r['locale']) for r in rows})==len(rows)
assert len({(r['resourceId'],r['locale']) for r in held})==41
out=O/'header_candidates_v2.json';out.write_text(json.dumps({'rows':rows},ensure_ascii=False,indent=2)+'\n')
manifest={'rows':len(rows),'appliedHeaderCells':len(applied),'englishAndOrthographyCells':sum(x['mappingLane'].startswith('ROOT_REVIEWED_ENGLISH') for x in applied),'nativeCorruptionCells':sum(x['mappingLane'].startswith('ROOT_REVIEWED_NATIVE') for x in applied),'outdatedBodyTuplesHeld':len({(r['resourceId'],r['locale']) for r in held}),'outdatedHeaderOccurrencesHeld':len(held),'nativeAlignmentOccurrencesHeld':len(J(O/'native_header_alignment_holds.json')['rows']),'finalReviewedStructuralOverlapBodies':sum(c['finalReviewedStructuralOverlayApplied'] for c in checks),'priorVerifiedOverlayBodies':sum(c['priorVerifiedBodyOverlayApplied'] for c in checks),'candidateFile':str(out.relative_to(P)),'candidateSHA256':fs(out),'finalReviewedStructuralFile':str(S.relative_to(P)),'finalReviewedStructuralSHA256':fs(S),'mappingFile':str(M.relative_to(P)),'mappingSHA256':fs(M),'nativeMappingFile':str(N.relative_to(P)),'nativeMappingSHA256':fs(N),'allCandidatePreservationChecksPass':True,'perLocale':dict(collections.Counter(r['locale'] for r in rows)),'externalWrites':'NONE','releaseOrder':'ROOT must verify final independently reviewed structural375 then fresh exact body-source/global-before guards before header release.'}
for n,d in [('candidate_checks_v2.json',{'rows':checks,'allPass':True}),('applied_header_cell_ledger_v2.json',{'rows':applied}),('outdated_body_holds_v2.json',{'rows':held}),('final_structural_header_reparse_v2.json',{'rows':overlaydelta}),('candidate_manifest_v2.json',manifest)]: (O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
