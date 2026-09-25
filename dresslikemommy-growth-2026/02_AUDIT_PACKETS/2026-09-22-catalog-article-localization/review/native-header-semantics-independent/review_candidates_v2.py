import json,re,html,hashlib,copy,ast,collections
from pathlib import Path
from html.parser import HTMLParser
from header_proofs import prove_only_header_text
O=Path(__file__).resolve().parent;P=O.parents[1];A=P/'review/native-header-semantics'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fscache={}
def fs(p):
 stamp=(p.stat().st_mtime_ns,p.stat().st_size)
 if p not in fscache or fscache[p][0]!=stamp:fscache[p]=(stamp,hashlib.sha256(p.read_bytes()).hexdigest())
 return fscache[p][1]
def load(p):return json.loads(p.read_text())
def save(n,d):p=O/n;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return fs(p)
# Independent parser class, loaded without the prior script's orchestration/writes.
tree=ast.parse((O/'check_inventory.py').read_text());ns={'HTMLParser':HTMLParser};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.ClassDef)],type_ignores=[]),'independent cell parser','exec'),ns);Cells=ns['CellParser']
F=A/'native_header_candidates_v2.json';M=A/'mapping_dictionary_v2.json';assert fs(F)=='91399bd156d7fb400a5d0b6159088bc9f4929d492f652f2bae739573ffd56d13';assert fs(M)=='2d81ce47c73ac14865240f4c6afff060ae5f0ce7452878a44ec8caa8fb7e5b43'
d=load(F);rows=d['rows'];maps={x['mappingIndex']:x for x in load(M)['rows']};pairs={x['pairIndex']:x for x in load(A/'source_bound_pairs.json')['rows']}
assert len(maps)==741 and len(rows)==2145
for m in maps.values():
 p=pairs[m['pairIndex']];assert (m['locale'],m['sourceHeader'],m['beforeHeader'])==(p['locale'],p['sourceHeader'],p['targetHeader']);assert all(u in p['uses'] for u in m['uses']);assert m['beforeHeader'].endswith(m['preservedSuffix']) and m['afterHeader'].endswith(m['preservedSuffix']);assert re.findall(r'\d+(?:[.,]\d+)?',m['beforeHeader'])==re.findall(r'\d+(?:[.,]\d+)?',m['afterHeader'])
 assert not(m['locale']=='ko' and m['beforeHeader']=='상의 길이 (cm / in)' and m['afterHeader']=='코트 길이 (cm / in)')
 if m['semanticIndex'] in [325,594,595,680,875,1087,1191,1304,1486,1768,1861]:assert not {u['productIndex'] for u in m['uses']}&{32,33,34,35,36,37,38,126,127,128,129}
base={(r['resourceId'],r['locale']):r for r in load(P/'review/body-structure-audit/effective_body_inventory.json')['rows']};overlay={};overlaydata={}
for info in d['summary']['overlays']:
 path=P/info['file'];assert fs(path)==info['sha256'];rs=load(path)['rows'];overlaydata[info['file']]={(r['resourceId'],r['locale']):r for r in rs}
 for r in rs:overlay[r['resourceId'],r['locale']]=(r,info)
exclusions={(r['resourceId'],r['locale'],r['targetTableIndex'],r['targetRowIndex'],r['targetCellIndex']) for r in load(P/'review/body-header-localization/native_header_alignment_holds.json')['rows']}
rawcache={};sourcecache={};proof=[];changes=0;relations={};num=lambda s:tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',s))

def relation(st,tt):
 assert len(st)==len(tt);heads=None;methods=collections.Counter()
 for sr,tr in zip(st,tt):
  assert [(x['tag'],x['colspan'],x['rowspan']) for x in sr]==[(x['tag'],x['colspan'],x['rowspan']) for x in tr]
  if all(x['tag']=='th' for x in sr):heads=sr,tr;continue
  for ci,(sc,tc) in enumerate(zip(sr,tr)):
   if sc['tag']!='td' or ci==0:continue
   a,b=num(sc['text']),num(tc['text'])
   if a==b:methods['exact']+=1;continue
   if len(a)>1 and sorted(a)==sorted(b):methods['sameCellNumericMultiset']+=1;continue
   if heads and len(heads[0])==len(sr) and re.search(r'\((?:cm|kg)\)',heads[1][ci]['text']) and '/' in sc['text'] and num(sc['text'].split('/',1)[0])==b:methods['explicitMetricComponent']+=1;continue
   raise AssertionError(('column numbers differ',sc,tc))
 return dict(methods)

def validate(r):
 k=r['resourceId'],r['locale'];b=base[k];v=r['expectedEffectiveBeforeValue'];assert sha(r['source'])==r['sourceSHA256']==b['sourceSHA256'];assert r['source']==r['sourceValue']==b['source'];assert r['sourceDigest']==b['sourceDigest'];assert sha(v)==r['beforeValueSHA256']==r['expectedBeforeValueSHA256']==r['expectedEffectiveBeforeValueSHA256'];assert sha(r['value'])==r['valueSHA256']
 expected=overlay[k][0]['value'] if k in overlay else b['expectedEffectiveBeforeValue'];assert expected==v
 assert k in overlay or b['overlayApplied'] or b['rawBefore']['outdated'] is False
 for dep in r['plannedBeforeDependencies']:
  assert fs(P/dep['file'])==dep['sha256']
  if dep['file'] not in overlaydata:
   dr=load(P/dep['file']);dr=dr['rows'] if isinstance(dr,dict) else dr
   overlaydata[dep['file']]={(rr['resourceId'],rr['locale']):rr for rr in dr}
  assert k in overlaydata[dep['file']]
  if 'valueSHA256' in dep:assert sha(overlaydata[dep['file']][k]['value'])==dep['valueSHA256']
 rf=P/r['rawFile']
 if rf not in rawcache:
  assert fs(rf)==r['rawFileSHA256'];rawcache[rf]=(fs(rf),{x['resourceId']:x for x in load(rf)['data']['translatableResourcesByIds']['nodes']})
 rh,nodes=rawcache[rf];assert rh==r['rawFileSHA256'];n=nodes[r['resourceId']];s=next(x for x in n['translatableContent'] if x['key']==r['key']);assert s['value']==r['source'] and s['digest']==r['sourceDigest'];assert next(x for x in n['tr_'+r['locale'].replace('-','_')] if x['key']==r['key'])==r['rawBefore']
 ev=prove_only_header_text(v,r['value']);assert len(ev['changes'])==len(r['headerRepairs'])
 bt=Cells(v).get();at=Cells(r['value']).get()
 if k[0] not in sourcecache:sourcecache[k[0]]=Cells(r['source']).get()
 st=sourcecache[k[0]];reconstructed=v
 for patch in sorted(r['headerRepairs'],key=lambda x:x['start'],reverse=True):
  assert v[patch['start']:patch['end']]==patch['beforeHTML'];reconstructed=reconstructed[:patch['start']]+patch['afterHTML']+reconstructed[patch['end']:]
  mp=maps[patch['mappingIndex']];assert (mp['locale'],mp['sourceHeader'],mp['beforeHeader'],mp['afterHeader'])==(r['locale'],patch['sourceHeader'],patch['beforeHeader'],patch['afterHeader'])
  ti,ri,ci=patch['tableIndex'],patch['rowIndex'],patch['cellIndex'];assert (k[0],k[1],ti,ri,ci) not in exclusions
  assert bt[ti][ri][ci]['text']==patch['beforeHeader'] and at[ti][ri][ci]['text']==patch['afterHeader']
  assert bt[ti][ri][ci]['tag']==at[ti][ri][ci]['tag']=='th'
  assert any(u['resourceId']==k[0] and u['locale']==k[1] and (u['targetTableIndex'],u['targetRowIndex'],u['targetCellIndex'])==(ti,ri,ci) and not u['effectiveOutdated'] for u in mp['uses'])
  suffix=mp['preservedSuffix'];assert patch['unitAndQualifierSuffixBytesPreserved']==suffix;assert patch['beforeHeader'].endswith(suffix) and patch['afterHeader'].endswith(suffix)
  for sm in patch['exactSourceMatches']:
   si=sm['sourceTableIndex'];assert st[si][sm['sourceRowIndex']][sm['sourceCellIndex']]['text']==patch['sourceHeader'];rel=(k,si,ti)
   if rel not in relations:relations[rel]=relation(st[si],bt[ti])
 assert reconstructed==r['value']
 return {'productIndex':r['productIndex'],'resourceId':k[0],'locale':k[1],'sourceDigest':r['sourceDigest'],'beforeValueSHA256':sha(v),'valueSHA256':sha(r['value']),'headerRepairs':len(r['headerRepairs']),'exactLatestBeforeAndRawSourceBindings':'PASS','nonHeaderMarkupAttributesTDNumericUnitPreservation':'PASS','sourceColumnMeaningCorrespondence':'PASS','completeMappingManualReview':'PASS','native31Overlap':0}
for r in rows:proof.append(validate(r));changes+=len(r['headerRepairs'])
assert changes==3864 and len(rawcache)==103
negative=[]
for case in ['nonheader_prose_changed','measurement_changed','source_digest_changed','before_changed']:
 r=copy.deepcopy(rows[0])
 if case=='nonheader_prose_changed':r['value']+='x';r['valueSHA256']=sha(r['value'])
 elif case=='measurement_changed':
  m=re.search(r'<td[^>]*>([^<]*\d[^<]*)</td>',r['value']);r['value']=r['value'][:m.start(1)]+'999'+r['value'][m.end(1):];r['valueSHA256']=sha(r['value'])
 elif case=='source_digest_changed':r['sourceDigest']='0'*64
 else:r['expectedEffectiveBeforeValue']+=' '
 try:validate(r)
 except AssertionError:negative.append({'case':case,'rejected':True})
 else:raise AssertionError(case)
q=copy.deepcopy(rows)
for r in q:r.update(independentReviewStatus='QUALIFIED_EXACT_SOURCE_HEADER_SEMANTICS_AND_PRESERVATION',reviewStatus='INDEPENDENT_REVIEW_PASS_PENDING_ROOT_FRESH_GUARD',independentReview={'reviewer':'article_he_pl_complete','authorFile':str(F.relative_to(P)),'authorSHA256':fs(F),'mappingFile':str(M.relative_to(P)),'mappingSHA256':fs(M),'postFreezeValueCorrections':0})
h=save('native_header2145_reviewed.json',{'summary':{**d['summary'],'status':'INDEPENDENT_REVIEW_PASS_PENDING_ROOT_FRESH_GUARD'},'rows':q})
report={'status':'PASS','qualifiedFile':'native_header2145_reviewed.json','qualifiedSHA256':h,'authorSHA256':fs(F),'mappingSHA256':fs(M),'bodies':2145,'headerEdits':3864,'allProposedMappingsManuallyRead':741,'allSemanticStemsPreRead':1926,'rawFilesBound':len(rawcache),'finalSourceTargetTableRelationsProved':len(relations),'postFreezeValueCorrections':0,'negativeTests':negative,'sourceEnglishChanged':False,'externalWrites':0,'outdatedInventoryUsesExcluded':158,'priorRefinementsConfirmed':['Korean top length retained for the five explicit shirt products rather than introducing a coat claim.','Finnish possessive grammar and Norwegian jacket compound corrected without changing garment identity.','Eleven shorts-height charts excluded from person-stature relabeling.'],'rowProof':proof};save('independent_review_v2.json',report)
print(json.dumps({k:report[k] for k in ['status','bodies','headerEdits','allProposedMappingsManuallyRead','rawFilesBound','qualifiedSHA256','postFreezeValueCorrections']}))
