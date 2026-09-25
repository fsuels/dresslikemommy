import json,pathlib,hashlib,re,html
P=pathlib.Path(__file__).resolve().parent; PACK=P.parent.parent
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
loads=lambda p:json.loads(p.read_text())
allrows={r['i']:r for locale in ['ar','cs','da','de','el','es','fi','fr','he','hi'] for r in loads(P/f'worklist_{locale}.json')['rows']}
contexts=loads(P.parent/'product-title-completeness-b/source_body_context.json')
resolution=loads(P.parent/'product-title-completeness-b/shared_source_context_resolution.json')
resolved={r['productIndex']:r for r in resolution['rows']}; opaque={r['productIndex']:r for r in resolution['held']}
manual={}
for p in sorted(P.glob('manual_*.json')):
 for k,v in loads(p).items():
  assert int(k) not in manual,(p,k)
  manual[int(k)]=(v,p.name)
rows=[]; checks=[]; holds=[]
for i,(value,file) in sorted(manual.items()):
 r=dict(allrows[i]);idx=i//20
 if idx in [2,26,42,87,130]:
  holds.append(dict(r,proposedValue=value,reason='Source title/body ambiguity or contradiction; root disposition needed. Translation-only changes preserve no invented completion.'));continue
 body=contexts[idx]['body']; plain=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',body['value']))).strip()
 r.update({'productIndex':idx,'source':r['sourceValue'],'value':value,'valueSHA256':sha(value),'expectedBeforeValueSHA256':sha(r['effectiveBeforeValue']),'reason':'Manual full-title source-to-target review: correct residual English, missing garment information, mistranslation or printed-text identity.','authorMap':file,'requiresFreshLiveSourceAndBeforeGuard':True,'supportingSourceDigests':{'body_html':body['digest']},'supportingSourceBodySHA256':sha(body['value']),'supportingSourceQuoteNormalizedWhitespace':plain[:min(len(plain),3500)],'bodyContextFile':'review/product-title-completeness-b/source_body_context.json','independentMeaningReview':'PENDING'})
 if idx in resolved:r['resolvedClippedConceptEvidence']=resolved[idx]
 if idx in opaque:r['unresolvedSourceSuffix']=opaque[idx]['reason'];r['sourceSuffixHandling']='Translate confirmed complete source concepts; retain ellipsis without inventing missing qualifier.'
 failures=[]
 if value==r['effectiveBeforeValue']:failures.append('UNCHANGED')
 if not value or '<'in value:failures.append('INVALID_TITLE')
 if r['sourceSHA256']!=sha(r['sourceValue']):failures.append('SOURCE_HASH')
 if sha((PACK/r['rawFile']).read_text())!=r['rawFileSHA256']:failures.append('RAW_FILE_HASH')
 if r['before'] and r['before']['value']!=r['effectiveBeforeValue']:failures.append('BEFORE_VALUE')
 if r['overlayApplied'] and r['before'] is not None:failures.append('FABRICATED_OVERLAY_BEFORE')
 rows.append(r);checks.append({'i':i,'tuple':[r['resourceId'],r['locale'],'title',None],'failures':failures})
maxidx=max(manual)//20
name=f'candidate_000_{maxidx:03d}.json'
(P/name).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(P/f'checks_000_{maxidx:03d}.json').write_text(json.dumps({'candidateFile':name,'candidateSHA256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'rows':len(rows),'checks':checks,'failureCount':sum(bool(r['failures'])for r in checks)},ensure_ascii=False,indent=2)+'\n')
(P/f'holds_000_{maxidx:03d}.json').write_text(json.dumps(holds,ensure_ascii=False,indent=2)+'\n')
print(name,len(rows),'holds',len(holds),'failures',sum(bool(r['failures'])for r in checks),'SHA',hashlib.sha256((P/name).read_bytes()).hexdigest())
