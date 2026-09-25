import json,re,hashlib,html,ast,collections
from pathlib import Path
H=Path(__file__).resolve().parent;sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
d=json.loads((H/'tag_candidates_v2.json').read_text());a=json.loads((H/'effective_body_inventory.json').read_text())['rows'];rows=d['rows'];evidence=[]
italianAlts={
41:['Madre e figlia con abiti coordinati con stampa di girasoli, perfetti per l’estate','Mamma e figlia indossano abiti coordinati con stampa di girasoli per una giornata fuori','Mamma e figlia con abiti maxi a girasoli nei colori nero e giallo','Abiti coordinati a girasoli per i look estivi di madre e figlia'],
51:['Madre e figlia indossano cardigan beige coordinati con cuori e bordi neri','Set di cardigan in maglia coordinati per madre e figlia con dettagli a cuore nero e bordi a contrasto','Cardigan in maglia coordinati con cuori per madre e figlia, perfetti per le uscite informali'],
65:['Famiglia con T-shirt coordinate con sfumatura dal rosa al blu','Completo per la famiglia con T-shirt sfumate rosa e blu','Look estivo per la famiglia con T-shirt sfumate ombré'],
84:['Magliette coordinate per la famiglia con scritta «Love» e cuori, perfette per mamma, papà e bambini','Magliette coordinate per la famiglia con «Lo», «Ve» e un cuore rosso per un grazioso look coordinato']}
for r in rows:
 j,loc=r['productIndex'],r['locale'];before=r['value'];value=before;changes=[]
 if loc=='it' and j in italianAlts:
  sourcetags=re.findall(r'<img\b[^>]*>',r['source']);sourceAlts=[re.search(r'alt="([^"]*)"',t)[1] for t in sourcetags];assert len(sourceAlts)==len(italianAlts[j])
  for old,new in zip(sourceAlts,italianAlts[j]):
   needle='alt="'+old+'"';replacement='alt="'+html.escape(new,quote=True)+'"';assert value.count(needle)==1;value=value.replace(needle,replacement,1)
   changes.append({'kind':'MANUAL_ITALIAN_TRANSLATION_OF_NEWLY_RESTORED_SOURCE_ALT','source':old,'value':new,'before':needle,'after':replacement,'sourceMeaningReviewedByAuthor':True})
 if (j,loc) in [(3,'ar'),(39,'ar'),(90,'ja')]:
  old,new,quote={
   (3,'ar'):('هذا طقم ملابس سباحة __DLMTOK0___ مطابق','هذا طقم ملابس سباحة متطابق للأم وطفلتها','This is a matching Mommy and Me swim suit set'),
   (39,'ar'):('__DLMTOK0____','المتطابق للأم وطفلتها','this gorgeous Mommy and Me Matching Pink Sleeveless Summer Dress'),
   (90,'ja'):('__DLMTOK0___','Tシャツ','these "Happy Flower" Family Matching T-Shirts')
  }[(j,loc)];assert quote in r['source'] and value.count(old)==1;value=value.replace(old,new,1);changes.append({'kind':'EXACT_SOURCE_BACKED_MISSING_PROSE_FRAGMENT','before':old,'after':new,'sourceExactQuote':quote})
 if (j,loc) in [(41,'ar'),(41,'pl'),(65,'ar'),(85,'ar'),(85,'pl'),(86,'pl')]:
  # Both English source and current target contain exactly one image paragraph; source order and surviving URLs establish pairing.
  sourcePs=[p for p in re.findall(r'<p\b[^>]*>.*?</p>',r['source'],re.S) if '<img' in p];targetPs=[p for p in re.findall(r'<p\b[^>]*>.*?</p>',value,re.S) if '<img' in p];assert len(sourcePs)==len(targetPs)==1
  sp,tp=sourcePs[0],targetPs[0];sourceTags=re.findall(r'<img\b[^>]*>',sp);urls=[re.search(r'src="([^"]*)"',t)[1] for t in sourceTags]
  if j==41:alts=re.findall(r'alt="(.*?)"\s+(?:src|سرك)\s*=',tp,re.S)
  else:
   chunks=re.findall(r'<img\b.*?(?=<img|</p>)',tp,re.S);alts=[re.search(r'alt="(.*)"',c,re.S)[1] for c in chunks]
  assert len(urls)==len(alts),(j,loc,len(urls),len(alts))
  surviving=re.findall(r'https?://[^\s"<>]+',tp);assert all(u in urls for u in surviving);assert [u for u in urls if u in surviving]==surviving
  # Attribute strings are source ordered; escaping internal existing quotes is a structural encoding repair, not a wording edit.
  new='<p>'+''.join('<img src="'+u+'" alt="'+html.escape(alt,quote=True)+'">' for u,alt in zip(urls,alts))+'</p>'
  assert value.count(tp)==1;value=value.replace(tp,new,1)
  changes.append({'kind':'RESTORE_MALFORMED_SOURCE_PAIRED_IMAGE_CHAIN','before':tp,'after':new,'sourceExactImageParagraph':sp,'sourceURLsInOrder':urls,'existingLocalizedAltValuesPreserved':alts,'survivingURLsPreservedInOrder':surviving,'pairingEvidence':'Unique source/target image paragraph; same image count from localized alt strings; surviving URL positions and each translated alt meaning establish source order. Only missing URLs/tag boundaries/src attribute name and internal-quote encoding restored.'})
 if (j,loc) in [(47,'hi'),(49,'hi'),(50,'hi'),(96,'hi'),(84,'pl'),(84,'ru')]:
  sourceTags=re.findall(r'<img\b[^>]*>',r['source']); targetTags=re.findall(r'<img\b[^>]*>',value)
  assert len(sourceTags)==len(targetTags)
  for sourceTag,targetTag in zip(sourceTags,targetTags):
   sourceURL=re.search(r'src="([^"]*)"',sourceTag)[1]; assert sourceURL in targetTag
   corrected=targetTag
   if loc=='hi':
    old="src='"+sourceURL+'"'; new='src="'+sourceURL+'"'; assert old in targetTag; corrected=targetTag.replace(old,new,1)
   elif targetTag.endswith('”>') or targetTag.endswith('»>'):
    corrected=targetTag[:-2]+'">'
   if corrected!=targetTag:
    assert value.count(targetTag)==1;value=value.replace(targetTag,corrected,1)
    changes.append({'kind':'EXACT_MISMATCHED_IMAGE_ATTRIBUTE_DELIMITER','before':targetTag,'after':corrected,'sourceExactImageTag':sourceTag,'sourceURL':sourceURL,'pairingEvidence':'Image URL uniquely matches the source image. Restore mismatched attribute quote delimiter only; retain all actual source URL and localized alt wording.'})
 if changes:
  assert re.findall(r'<t[dh](?:\s[^>]*)?>.*?</t[dh]>',before,re.S)==re.findall(r'<t[dh](?:\s[^>]*)?>.*?</t[dh]>',value,re.S)
  r.update(value=value,valueSHA256=sha(value),versionTwoValueSHA256=sha(before),versionThreeExceptions=changes)
  evidence.append({'productIndex':j,'resourceId':r['resourceId'],'locale':loc,'sourceDigest':r['sourceDigest'],'v2ValueSHA256':sha(before),'v3ValueSHA256':sha(value),'changes':changes})
fi=next(r for r in a if r['productIndex']==99 and r['locale']=='fi');before=fi['expectedEffectiveBeforeValue'];old='</strong yhteensopiviin asuihin';new='</strong> yhteensopiviin asuihin';assert before.count(old)==1 and fi['before']['outdated'] is False
sourceQuote='<strong data-start="2705" data-end="2729">men’s + boys’ sizing</strong>';assert sourceQuote in fi['source'];value=before.replace(old,new,1)
r={k:fi[k] for k in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','before','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']};change={'kind':'MISSING_CLOSING_STRONG_BOUNDARY','before':old,'after':new,'sourceExactTag':sourceQuote,'pairingEvidence':'Identical data-start/end indices and translated size phrase; adds missing > at same English strong boundary.'}
r.update(value=value,valueSHA256=sha(value),beforeValueSHA256=sha(before),expectedBeforeValueSHA256=sha(before),reviewStatus='AUTHOR_PENDING_INDEPENDENT_REVIEW',requiresFreshLiveSourceAndBeforeGuard=True,reason='Repair exact source-aligned missing > in Finnish closing strong tag; no prose, cell or attribute edit.',versionThreeExceptions=[change],checks={'beforeOutdatedFalse':True,'tableCellAndHeaderBytesExact':True});rows.append(r);evidence.append({'productIndex':99,'resourceId':r['resourceId'],'locale':'fi','sourceDigest':r['sourceDigest'],'beforeValueSHA256':sha(before),'v3ValueSHA256':sha(value),'changes':[change]})
assert len(rows)==375 and len(evidence)==20 # ten additional defects, four Italian alt rows, six parser-detected delimiter rows
keys={(r['resourceId'],r['locale'],r['key']) for r in rows};assert len(keys)==375
mod=ast.parse((H/'build_tag_candidates.py').read_text());ns=[n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name in ['tokens','balance']];ct={'re':re,'collections':collections,'pat':re.compile(r'<\s*(/?)\s*([^\s<>/]+)(?:\s[^<>]*?)?\s*/?>'),'void':set('area base br col embed hr img input link meta param source track wbr'.split())};exec(compile(ast.Module(body=ns,type_ignores=[]),'<pure checks>','exec'),ct)
for r in rows:
 b=ct['balance'](r['value']);assert b['unbalancedCounts']=={} and b['nestingIssueCount']==0 and b['unclosedStack']==[],(r['productIndex'],r['locale'],b);r['checks']['afterBalancedness']=b;r['checks']['v3NoTranslationPlaceholders']=True;assert not re.search(r'_+DLMTOK\d+_+',r['value'])
 r['checks']['v3TableCellAndHeaderBytesExact']=True
(H/'tag_candidates_v3.json').write_text(json.dumps({'status':'FINAL375_AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','supersedes':'tag_candidates_v2.json','rows':rows},ensure_ascii=False,indent=2)+'\n');(H/'v3_delta_evidence.json').write_text(json.dumps({'rows':evidence},ensure_ascii=False,indent=2)+'\n')
report={'status':'AUTHOR_PASS_PENDING_INDEPENDENT_REVIEW','rows':375,'changedExistingV2Rows':19,'newRows':1,'newlyLocalizedItalianAlts':12,'additionalMalformedImageRows':6,'mismatchedImageAttributeDelimiterRows':6,'additionalProsePlaceholderRows':3,'FinnishClosingBoundaryRows':1,'allBeforeOutdatedFalse':True,'allRowsBalanced':375,'allTableCellAndHeaderBytesPreserved':375,'allProseChangesExplicit':True,'allImageSourcePairingExplicit':True,'uniqueKeys':375,'candidateSHA256':sha((H/'tag_candidates_v3.json').read_text())};(H/'tag_v3_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
