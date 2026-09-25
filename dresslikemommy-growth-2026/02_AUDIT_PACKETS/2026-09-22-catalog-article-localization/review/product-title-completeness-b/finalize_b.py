import json,hashlib,re,html,collections
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[1]
locales=['it','ja','ko','nl','no','pl','pt-BR','ro','ru','sv']
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
filesha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
work={loc:json.loads((B/f'review/product-title-completeness/worklist_{loc}.json').read_text())['rows'] for loc in locales}
ctx=json.loads((H/'source_body_context.json').read_text())
frags=[];newkeys=set();base=[];checks=[];rawcache={}
for line in (H/'manual_fragments.tsv').read_text().splitlines():
 loc,n,value=line.split('\t',2);j=int(n);r=work[loc][j];assert value!=r['effectiveBeforeValue'];assert j not in [2,22,87,130]
 k=(r['resourceId'],loc,'title');assert k not in newkeys;newkeys.add(k)
 p=B/f'review/product-title-completeness/worklist_{loc}.json'
 c=dict(r,productIndex=j,source=r['sourceValue'],value=value,valueSHA256=sha(value),expectedBeforeValueSHA256=r['expectedEffectiveBeforeValueSHA256'],reviewStatus='AUTHOR_PENDING_INDEPENDENT_MEANING_REVIEW',reason='Repair known title meaning/localization while retaining the exact unresolved source fragment and ellipsis; no guessed completion or English source edits.',requiresFreshLiveSourceAndBeforeGuard=True,requiresFreshEffectiveBeforeObject=bool(r['overlayApplied']),inputWorklistFile=str(p.relative_to(B)),inputWorklistFileSHA256=filesha(p),clippedFragmentPolicy='Root clarified: incomplete source alone is not a hold. Translate known words; preserve unresolved literal fragment. Confirmed factual conflicts remain separate.')
 frags.append(c)
(H/'candidate_fragments_v1.json').write_text(json.dumps({'status':'AUTHOR_PENDING_INDEPENDENT_REVIEW','rows':frags},ensure_ascii=False,indent=2)+'\n')
for loc in locales:base.extend(json.loads((H/f'candidate_{loc}_v1.json').read_text())['rows'])
assert len(base)==829
allrows=base+frags;bykey={(r['resourceId'],r['locale'],'title'):r for r in allrows};assert len(bykey)==len(allrows)
ledger=[]
for loc in locales:
 for j,r in enumerate(work[loc]):
  p=B/r['rawFile'];assert filesha(p)==r['rawFileSHA256']
  if p not in rawcache:
   raw=json.loads(p.read_text());rawcache[p]={n['resourceId']:n for n in raw['data']['translatableResourcesByIds']['nodes']}
  node=rawcache[p][r['resourceId']];s=next(v for v in node['translatableContent'] if v['key']=='title');b=next((v for v in node.get('tr_'+loc.replace('-','_'),[]) if v['key']=='title'),None)
  assert s['value']==r['sourceValue'] and s['digest']==r['sourceDigest'];assert b==r['rawBefore'],(loc,j,'raw_before');assert sha(s['value'])==r['sourceSHA256']
  assert (sha(r['effectiveBeforeValue']) if r['effectiveBeforeValue'] is not None else None)==r['expectedEffectiveBeforeValueSHA256']
  if r['overlayApplied']:assert r['before'] is None and filesha(B/r['overlaySourceFile'])==r['overlaySourceFileSHA256']
  else:assert r['before']==r['rawBefore']
  k=(r['resourceId'],loc,'title');c=bykey.get(k)
  reason=({2:'Title says bikini, current body says one-piece.',22:'Title says two-piece, current body says one-piece.',87:'Title says sun/cloud/plant but current body describes LOVE/heart; conflicting source.',130:'Title says cotton-silk, current body specifies cotton/viscose.'}).get(j)
  assert not (c and reason)
  status='CORRECTION_AUTHORED_PENDING_INDEPENDENT_REVIEW' if c else 'HELD_CONFIRMED_SOURCE_CONFLICT' if reason else 'FULL_TITLE_MANUALLY_READ_RETAINED'
  if c:
   assert c['sourceDigest']==s['digest'] and c['source']==s['value'] and c['valueSHA256']==sha(c['value'])
   assert re.findall(r'\d+',c['source'])==re.findall(r'\d+',c['value']),(loc,j,'numeric drift')
   assert not re.search(r'__DLMTOK|<[^>]+>',c['value'])
   if c.get('supportingSourceDigests'):
    bd=next(v for v in node['translatableContent'] if v['key']=='body_html');assert c['supportingSourceDigests']=={'body_html':bd['digest']}
    bt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',bd['value']))).strip()
    for field in ['clippedConceptEvidence','additionalBodyEvidence']:
     if c.get(field):assert c[field]['exactQuoteNormalizedWhitespace'] in bt and c[field]['bodyValueSHA256']==sha(bd['value'])
  ledger.append(dict(productIndex=j,resourceId=r['resourceId'],locale=loc,key='title',sourceValue=s['value'],sourceDigest=s['digest'],effectiveBeforeValue=r['effectiveBeforeValue'],expectedEffectiveBeforeValueSHA256=r['expectedEffectiveBeforeValueSHA256'],overlayApplied=r['overlayApplied'],status=status,holdReason=reason,proposedValue=c['value'] if c else None,sourceIncomplete=bool(re.search(r'\.\.\.',s['value'])),candidateFile='candidate_fragments_v1.json' if k in newkeys else f'candidate_{loc}_v1.json' if c else None))
assert len(ledger)==2380
(H/'coverage_all_2380.json').write_text(json.dumps({'status':'FULL2380_MANUAL_TITLE_READ_COMPLETE','sourcePolicy':'Incomplete source alone does not block known-word repair; unresolved source fragment retained. Actual contradictions held. Candidates are authorship only; independent reviewer/root guard required.','counts':dict(collections.Counter(x['status'] for x in ledger)),'rows':ledger},ensure_ascii=False,indent=2)+'\n')
report={'status':'PASS','fullManualTitles':2380,'baseCandidates':len(base),'fragmentCandidates':len(frags),'allAuthoredCandidates':len(allrows),'heldConflictTuples':40,'exactRawSourceDigestBeforeBindings':2380,'rawFileHashesVerified':len(rawcache),'numericTokensPreserved':len(allrows),'candidateKeysUnique':len(bykey),'overlayInputsPreserved':sum(r['overlayApplied'] for a in work.values() for r in a),'release':'NOT RUN by subagent; parent sole release authority.','files':[{'file':p.name,'rows':len(json.loads(p.read_text())['rows']),'sha256':filesha(p)} for p in sorted(H.glob('candidate_*_v1.json'))]}
(H/'final_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(H/'FINAL_REPORT.md').write_text(f'''# B product-title completion\n\nAll 2,380 frozen effective titles were individually read: 238 products in each of it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv.\n\nAuthored {len(allrows)} corrections: 829 in ten frozen base batches and {len(frags)} additional source-fragment corrections in candidate_fragments_v1.json. These batches are disjoint. Existing root overlays are preserved as expected-effective-before values; their null before object requires a fresh full object from root, not an absent-translation assumption.\n\n40 tuples remain held for demonstrated current English contradictions across four products: indices 2 (bikini/one-piece), 22 (two-piece/one-piece), 87 (sun/cloud/plant versus LOVE/heart), 130 (cotton-silk/cotton-viscose). These include the four pre-existing RU/SV missing-title holds. Source clipping alone is no longer a hold. Unknown literal source fragments remain visible where their completion cannot be evidenced.\n\nValidation: all 2,380 raw-source/digest/raw-before/effective-before bindings and raw hashes pass; all {len(allrows)} proposed values preserve numeric tokens and carry unique resource/locale/key tuples. Body-supported expansions verify the exact current English body digest and exact normalized quote. Full manual meaning review remains independently owned by de/hepl agents; their reviewed copies supersede authored copies for release. No API, Git, browser, live, or canonical state writes were made in this lane.\n''')
print(json.dumps(report,ensure_ascii=False))
