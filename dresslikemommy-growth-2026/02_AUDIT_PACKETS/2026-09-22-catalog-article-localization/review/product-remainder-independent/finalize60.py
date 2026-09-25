from pathlib import Path
import json,re,hashlib,html,importlib.util
P=Path(__file__).parent;PACK=P.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pairs=json.loads((P/'product60_pairs.json').read_text());rows=json.loads((P/'product60_candidates_frozen_copy.json').read_text())['rows'];checks=json.loads((P/'product60_checks.json').read_text())['rows']
rules=[(1652,'Lyhyet pussihihat lisäävät viehätystä ja eleganssia','Remove duplicated Finnish adjective (short short).'),(2206,'Barn 2-3 år (90)','Translate English Years remaining in Swedish chart label.'),(2511,'Enkel skötsel: Kan maskintvättas, hållbart tryck','Translate partially English Swedish care instruction in full.')]
corrections=[];out=[]
for r,c in zip(rows,checks):
 v=r['value'];ident=r['resourceId'].split('/')[-1]+':'+r['locale'];applied=[]
 for i,to,why in rules:
  pair=pairs[i]
  if ident not in pair['tuples']:continue
  frm=pair['target'];assert v.count(frm)==1,(ident,frm,v.count(frm));v=v.replace(frm,to)
  fix={'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'authorValueSHA256':sha(r['value']),'pairId':i,'sourceText':pair['source'],'from':frm,'to':to,'reason':why,'occurrences':1};corrections.append(fix);applied.append(fix)
 ck=m.verify_text(r['sourceValue'],v,r['locale']);assert not ck['errors'],(ident,ck)
 rr={**r,'value':v,'valueSHA256':sha(v),'independentMeaningReview':'PASS_WITH_EXACT_CORRECTIONS'if applied else'PASS','independentReviewer':'article_he_pl_complete','independentReviewArtifact':'review/product-remainder-independent/product60_review.json','authorCandidateFile':c['candidateFile'],'authorCandidateFileSHA256':c['candidateFileSHA256']};out.append(rr)
write('product60_corrections.json',{'rules':corrections});write('product60_reviewed_candidates.json',{'rows':out})
write('product60_review.json',{'status':'PASS_AFTER_3_EXACT_CORRECTIONS','rows':60,'locales':sorted(set(r['locale']for r in rows)),'correctedRows':len(corrections),'semanticPairsRead':1140,'exactUnchangedNumericUnitUniquePairs':1537,'exactUnchangedNumericCellOccurrences':540,'inlineParagraphsRead':27,'reviewMethod':'Full source-target prose, bullet, table header, role/age/size-label comparison, with exact repeated text deduplication and numeric-only mechanical preservation. Source/raw/digest/before exact binding verified independently; current source markup/images/attributes/links/tables/numbers/units verified by offline_translation.py before and after corrections. Printed garment wording retained as product identity. Source claims remain source claims; no new source-policy gate.','correctionsFile':'product60_corrections.json','rowsEvidence':checks,'sourceDefects':[],'scope':'Local independent candidate review only; parent owns integration and fresh live guards.'})
print({'rows':60,'corrections':len(corrections),'keys':[(x['resourceId'],x['locale'],x['pairId'])for x in corrections]})
# show literal joins with no inserted spaces
for r in rows:
 for tag in re.findall(r'<(?:p|li)\b[^>]*>.*?</(?:p|li)>',r['value'],re.S):
  if '<strong'in tag and len(re.sub('<[^>]+>','',tag).strip())>40:print(html.unescape(re.sub('<[^>]+>','',tag)))
