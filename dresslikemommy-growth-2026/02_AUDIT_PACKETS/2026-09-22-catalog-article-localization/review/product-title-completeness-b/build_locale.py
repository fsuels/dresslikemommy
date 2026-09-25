import json,re,hashlib,sys,html
from pathlib import Path
H=Path(__file__).resolve().parent;B=H.parents[1]
loc=sys.argv[1]
P=B/f'review/product-title-completeness/worklist_{loc}.json';a=json.loads(P.read_text())['rows']
ctx=json.loads((H/'shared_source_context_resolution.json').read_text());byctx={r['productIndex']:r for r in ctx['rows']}
body=json.loads((H/'source_body_context.json').read_text());held={r['productIndex']:r['reason'] for r in ctx['held']}
fix={int(line.split('\t',1)[0]):line.split('\t',1)[1] for line in (H/f'manual_{loc}.tsv').read_text().splitlines() if line}
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
manifest=json.loads((B/'review/product-title-completeness/WORKLIST_MANIFEST.json').read_text());m=next(m for m in manifest['localeFiles'] if m['file']==P.name);assert m['sha256']==hashlib.sha256(P.read_bytes()).hexdigest()
cs=[];ledger=[]
for j,r in enumerate(a):
 assert sha(r['sourceValue'])==r['sourceSHA256'] and (sha(r['effectiveBeforeValue']) if r['effectiveBeforeValue'] is not None else None)==r['expectedEffectiveBeforeValueSHA256']
 assert r['resourceId']==body[j]['resourceId']
 reason=('SOURCE_CONFLICT_TWO_PIECE_TITLE_VS_ONE_PIECE_BODY' if j==22 else None) or r.get('sourceProductConflict') or ('Existing missing-title source hold' if r['existingMissingTitleHold'] else held.get(j))
 if j in fix:
  assert not reason,(j,reason)
  value=fix[j];assert value!=r['effectiveBeforeValue']
  assert '<' not in value and '>' not in value and '\n' not in value
  support=byctx.get(j)
  c=dict(r,productIndex=j,source=r['sourceValue'],value=value,valueSHA256=sha(value),expectedBeforeValueSHA256=r['expectedEffectiveBeforeValueSHA256'],reviewStatus='AUTHOR_PENDING_INDEPENDENT_MEANING_REVIEW',reason='Full manual source/effective title review: repair untranslated generic garment copy, malformed grammar, mistranslated garment/design/relationship or literal printed name; preserve complete observed source facts and seller style names.',requiresFreshLiveSourceAndBeforeGuard=True,requiresFreshEffectiveBeforeObject=bool(r['overlayApplied']),inputWorklistFile=str(P.relative_to(B)),inputWorklistFileSHA256=m['sha256'])
  if support:c['supportingSourceDigests']=support['supportingSourceDigests'];c['clippedConceptEvidence']=support
  # Preserve full body digest for all manually checked body-context-dependent printed/garment fixes as well.
  if j in [49,69,71,74,75,76,78,79,80,81,89,90,92,94,159,164,165,179,180,192,198,212]:
   c['supportingSourceDigests']={'body_html':body[j]['body']['digest']}
   t=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',body[j]['body']['value']))).strip()
   c['additionalBodyEvidence']={'bodyValueSHA256':sha(body[j]['body']['value']),'exactQuoteNormalizedWhitespace':t[:t.find(' Size Chart') if ' Size Chart' in t else min(len(t),1000)],'note':'Current source visible-text evidence. No body or English source edits; exact body digest guarded.'}
  cs.append(c);status='CORRECTION_AUTHORED_PENDING_INDEPENDENT_REVIEW'
 elif reason:status='HELD_SOURCE_CLARIFICATION';value=None
 else:status='FULL_TITLE_MANUALLY_READ_RETAINED';value=None
 ledger.append({'productIndex':j,'resourceId':r['resourceId'],'locale':loc,'key':'title','sourceValue':r['sourceValue'],'sourceDigest':r['sourceDigest'],'effectiveBeforeValue':r['effectiveBeforeValue'],'expectedEffectiveBeforeValueSHA256':r['expectedEffectiveBeforeValueSHA256'],'overlayApplied':r['overlayApplied'],'status':status,'holdReason':reason,'proposedValue':value})
assert len(a)==238 and len(fix)==len(cs)
(H/f'candidate_{loc}_v1.json').write_text(json.dumps({'status':'AUTHOR_REVIEW_COMPLETE_PENDING_INDEPENDENT_MEANING_AND_FRESH_EFFECTIVE_BEFORE','locale':loc,'rows':cs},ensure_ascii=False,indent=2)+'\n')
(H/f'coverage_{loc}.json').write_text(json.dumps({'status':'FULL238_MANUAL_TITLE_READ','locale':loc,'rows':ledger},ensure_ascii=False,indent=2)+'\n')
print(loc,{'read':len(a),'candidates':len(cs),'held':sum(r['status']=='HELD_SOURCE_CLARIFICATION' for r in ledger),'retained':sum(r['status']=='FULL_TITLE_MANUALLY_READ_RETAINED' for r in ledger),'sha256':hashlib.sha256((H/f'candidate_{loc}_v1.json').read_bytes()).hexdigest()})
