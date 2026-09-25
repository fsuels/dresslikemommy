import json,re,html,hashlib,collections,ast,runpy
from pathlib import Path
from html.parser import HTMLParser
H=Path(__file__).resolve().parent;B=H.parents[1];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();norm=lambda s:' '.join(html.unescape(s).split())
module=ast.parse((H/'inventory.py').read_text());ns={'HTMLParser':HTMLParser,'re':re,'unicodedata':__import__('unicodedata')};ev=ast.parse((B/'review/body-header-localization/native_header_evidence.py').read_text());exec(compile(ast.Module(body=[x for x in ev.body if isinstance(x,ast.ClassDef)],type_ignores=[]),'parser','exec'),ns);Tables=ns['Tables'];exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='aligned'],type_ignores=[]),'align','exec'),ns);ns['nums']=lambda s:tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',__import__('unicodedata').normalize('NFKC',s)))
class CellSpans(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.s=s;self.offsets=[0];self.offsets.extend(m.end() for m in re.finditer('\n',s));self.ti=-1;self.ri=-1;self.ci=-1;self.inside=False;self.active=None;self.cells={};self.feed(s)
 def pos(self):l,c=self.getpos();return self.offsets[l-1]+c
 def handle_starttag(self,t,a):
  if t=='table':self.ti+=1;self.ri=-1;self.inside=True
  elif t=='tr' and self.inside:self.ri+=1;self.ci=-1
  elif t in ['th','td'] and self.inside:
   self.ci+=1;self.active=(self.ti,self.ri,self.ci);self.cells[self.active]={'tag':t,'start':self.pos()+len(self.get_starttag_text())}
 def handle_endtag(self,t):
  if t in ['th','td'] and self.active is not None:self.cells[self.active]['end']=self.pos();self.active=None
  elif t=='table':self.inside=False;self.active=None
raw=json.loads((B/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows'];rawmap={(r['resourceId'],r['locale']):r for r in raw};effective={k:{'value':r['expectedEffectiveBeforeValue'],'files':([{'file':r['overlayFile'],'sha256':r['overlayFileSHA256']}] if r['overlayApplied'] else [])} for k,r in rawmap.items()}
files=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json','review/size-label-repair/candidate_root_reviewed156.json','review/size-label-repair/placeholder-review/placeholder88_root_bound.json','review/body-header-localization/prose-completion-review/prose_completion11_root_bound.json','review/native-header-final/current22_root_reviewed.json','review/native-header-semantics-independent/full7/full7_reviewed.json']
filechecks=[];mismatches=[]
for rel in files:
 p=B/rel;fs=hashlib.sha256(p.read_bytes()).hexdigest();rs=json.loads(p.read_text())['rows'];filechecks.append({'file':rel,'sha256':fs,'rows':len(rs)})
 for r in rs:
  k=r['resourceId'],r['locale'];old=effective[k]['value'];assert r['sourceDigest']==rawmap[k]['sourceDigest'];exp=r.get('expectedEffectiveBeforeValue')
  if exp is None and r.get('before'):exp=r['before']['value']
  expectedsha=r.get('expectedEffectiveBeforeValueSHA256') or r.get('beforeValueSHA256')
  if expectedsha and sha(old or '')!=expectedsha:mismatches.append({'file':rel,'key':k,'effectiveSHA256':sha(old or ''),'expectedSHA256':expectedsha,'reason':'Earlier complete value may already contain reviewed changes; latest root-verified full overlay is authoritative.'})
  effective[k]={'value':r['value'],'files':effective[k]['files']+[{'file':rel,'sha256':fs,'valueSHA256':sha(r['value'])}]}
excludes={(r['resourceId'],r['locale'],r['targetTableIndex'],r['targetRowIndex'],r['targetCellIndex']) for r in json.loads((B/'review/body-header-localization/native_header_alignment_holds.json').read_text())['rows']}
full7={(r['resourceId'],r['locale']) for r in json.loads((B/files[-1]).read_text())['rows']}
mp=json.loads((H/'mapping_dictionary_v1.json').read_text());by=collections.defaultdict(list);held=[];superseded=[]
for m in mp['rows']:
 for u in m['uses']:
  k=u['resourceId'],u['locale']
  if k in full7:superseded.append({**u,'mappingIndex':m['mappingIndex'],'disposition':'SUPERSEDED_BY_INDEPENDENT_FULL7'});continue
  if u['effectiveOutdated']:held.append({**u,'mappingIndex':m['mappingIndex'],'reason':'OUTDATED_TRUE_REQUIRES_FULL_SOURCE_BODY_REVIEW'});continue
  by[k].append((m,u))
rows=[];checks=[];cellledger=[];failures=[]
for k,uses in by.items():
 r=rawmap[k];before=effective[k]['value'];v=before;parser=CellSpans(before);tar=Tables().get(before);src=Tables().get(r['source']);patches=[];seen=set()
 for m,u in uses:
  ck=u['targetTableIndex'],u['targetRowIndex'],u['targetCellIndex'];assert (*k,*ck) not in excludes;assert ck not in seen;seen.add(ck)
  if len(tar)<=ck[0] or len(tar[ck[0]]['rows'])<=ck[1] or len(tar[ck[0]]['rows'][ck[1]])<=ck[2]:failures.append({'key':k,'mappingIndex':m['mappingIndex'],'reason':'LATEST_OVERLAY_CHANGED_TABLE_COORDINATE'});continue
  cell=tar[ck[0]]['rows'][ck[1]][ck[2]]
  if cell['text']==m['afterHeader']:superseded.append({**u,'mappingIndex':m['mappingIndex'],'disposition':'ALREADY_CORRECTED_BY_LATER_REVIEWED_OVERLAY'});continue
  if cell['text']!=m['beforeHeader']:failures.append({'key':k,'mappingIndex':m['mappingIndex'],'reason':'LATEST_OVERLAY_CHANGED_HEADER','newHeader':cell['text'],'oldHeader':m['beforeHeader']});continue
  matches=[]
  for sm in u['sourceMatches']:
   st=src[sm['sourceTableIndex']];proof=ns['aligned'](st,tar[ck[0]])
   if proof and st['rows'][sm['sourceRowIndex']][sm['sourceCellIndex']]['text']==m['sourceHeader']:matches.append({**sm,'latestOverlayAlignmentEvidence':proof})
  assert matches,('lost alignment',k,ck)
  span=parser.cells[ck];inner=before[span['start']:span['end']]
  if '<' in inner:failures.append({'key':k,'mappingIndex':m['mappingIndex'],'reason':'INLINE_HEADER_MARKUP_REQUIRES_SEPARATE_EXACT_TEXT_PATCH','inner':inner});continue
  assert norm(inner)==m['beforeHeader'];stripped=inner.strip();leading=inner[:len(inner)-len(inner.lstrip())];trailing=inner[len(inner.rstrip()):];suffix=m['preservedSuffix'];sufmatch=re.search(r'\s*[（(][^()（）]*[)）]\s*$',stripped) if suffix else None
  rawsuffix=sufmatch.group(0) if sufmatch else '';aftercore=m['afterHeader'][:-len(suffix)] if suffix else m['afterHeader'];new=leading+html.escape(aftercore,quote=False)+rawsuffix+trailing
  assert norm(new)==m['afterHeader'],(new,m)
  patch={'mappingIndex':m['mappingIndex'],'tableIndex':ck[0],'rowIndex':ck[1],'cellIndex':ck[2],'start':span['start'],'end':span['end'],'beforeHTML':inner,'afterHTML':new,'sourceHeader':m['sourceHeader'],'beforeHeader':m['beforeHeader'],'afterHeader':m['afterHeader'],'reason':m['reason'],'exactSourceMatches':matches,'unitAndQualifierSuffixBytesPreserved':rawsuffix}
  patches.append(patch);cellledger.append({'resourceId':k[0],'locale':k[1],'productIndex':r['productIndex'],**patch})
 for p in sorted(patches,key=lambda p:p['start'],reverse=True):assert v[p['start']:p['end']]==p['beforeHTML'];v=v[:p['start']]+p['afterHTML']+v[p['end']:]
 if not patches:continue
 # All bytes outside declared header text spans must be identical; reverse reconstruction is exact.
 reconstruction=v
 shift=0
 for p in sorted(patches,key=lambda p:p['start']):
  pos=p['start']+shift;assert reconstruction[pos:pos+len(p['afterHTML'])]==p['afterHTML'];shift+=len(p['afterHTML'])-len(p['beforeHTML'])
 clean=lambda s:re.sub(r'<th\b[^>]*>[\s\S]*?</th\s*>','<TH_TEXT_EXCLUDED>',s,flags=re.I)
 assert clean(before)==clean(v)
 assert re.findall(r'<[^>]*>',before)==re.findall(r'<[^>]*>',v)
 assert re.findall(r'<td\b[^>]*>[\s\S]*?</td\s*>',before,re.I)==re.findall(r'<td\b[^>]*>[\s\S]*?</td\s*>',v,re.I)
 assert r['sourceDigest']==sha(r['source'])==r['sourceSHA256']
 out={z:r[z] for z in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']};out.update({'marketId':None,'sourceValue':r['source'],'before':None,'expectedEffectiveBeforeValue':before,'expectedEffectiveBeforeValueSHA256':sha(before),'expectedBeforeValueSHA256':sha(before),'beforeValueSHA256':sha(before),'value':v,'valueSHA256':sha(v),'plannedBeforeDependencies':effective[k]['files'],'requiresFreshEffectiveBeforeObject':True,'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'AUTHOR_SOURCE_COLUMN_BOUND_NATIVE_HEADER_REPAIR_PENDING_INDEPENDENT_REVIEW','reason':'Only the declared current-source-bound localized header text is changed. All other text, every td measurement/size cell, HTML tags, attributes, URLs and existing units are byte-identical. Exact source column shape and numeric correspondence independently retained.','headerRepairs':patches})
 rows.append(out);checks.append({'resourceId':k[0],'locale':k[1],'patches':len(patches),'sourceDigestSHA256Pass':True,'nonHeaderBytesExact':True,'allHTMLTagsAndAttributesExact':True,'allTDCellsExact':True,'allUnitSuffixBytesExact':True,'currentOnly':True,'excludesNative31Pass':True})
# All recorded source raw page hashes remain bound; no connector is used.
rawchecks=[]
for rel,want in sorted({(r['rawFile'],r['rawFileSHA256']) for r in rows}):
 actual=hashlib.sha256((B/rel).read_bytes()).hexdigest();assert actual==want;rawchecks.append({'file':rel,'sha256':actual,'pass':True})
summary={'status':'AUTHOR_CHECKS_PASS_PENDING_INDEPENDENT_MEANING_REVIEW','bodies':len(rows),'headerRepairs':len(cellledger),'locales':dict(collections.Counter(x['locale'] for x in rows)),'outdatedHeldOccurrences':len(held),'supersededOccurrences':len(superseded),'remainingApplicationFailures':len(failures),'rawFilesBound':len(rawchecks),'overlayBeforeMismatches':len(mismatches),'overlays':filechecks}
for name,obj in [('native_header_candidates_v1.json',{'summary':summary,'rows':rows}),('candidate_checks_v1.json',{'summary':summary,'checks':checks,'rawFileBindings':rawchecks,'overlayBeforeMismatches':mismatches}),('native_header_cell_ledger_v1.json',{'rows':cellledger}),('outdated_hold_ledger.json',{'rows':held}),('superseded_occurrences.json',{'rows':superseded}),('application_failures.json',{'rows':failures})]:(H/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False));print('candidate SHA',hashlib.sha256((H/'native_header_candidates_v1.json').read_bytes()).hexdigest())
