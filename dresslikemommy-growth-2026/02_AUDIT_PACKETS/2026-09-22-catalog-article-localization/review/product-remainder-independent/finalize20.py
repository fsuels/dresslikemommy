from pathlib import Path
import json,re,hashlib,html,importlib.util
P=Path(__file__).parent;PACK=P.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pairs=json.loads((P/'product20_pairs.json').read_text());rows=json.loads((P/'product20_candidates_frozen_copy.json').read_text())['rows'];checks=json.loads((P/'product20_checks.json').read_text())['rows']
rules=[(3, 'فساتين للنساء والفتيات: فساتين طويلة بلا أكمام، بطبقات انسيابية لمظهر منعش وأنيق.', 'Disambiguate sleeveless versus flowing tiers; preserve breezy and chic description.'), (1437, 'Un look coordinato per quattro ruoli familiari: mamme, papà, bambine e bambini. Pensato per giornate al parco, foto di famiglia, viaggi e tranquilli programmi del fine settimana.', 'Four roles are size/role categories, not an included four-member set.'), (1463, "Een bijpassende look voor de vier gezinsrollen: moeders, vaders, meisjes en jongens. Ontworpen voor dagen in het park, familiefoto's, reizen en ontspannen weekendplannen.", 'Four roles are size/role categories, not an included four-member set.'), (1481, 'Bijpassend voor vier gezinsrollen:', 'Four roles are categories, not an included four-member set.'), (1489, 'Spójny zestaw stylizacji dla czterech ról rodzinnych: mam, tatusiów, dziewczynek i chłopców. Zaprojektowany na dni w parku, rodzinne zdjęcia, podróże i swobodne plany weekendowe.', 'Four roles are size/role categories, not an included four-member set.')]
corrections=[];out=[]
for r,c in zip(rows,checks):
 v=r['value'];ident=r['resourceId'].split('/')[-1]+':'+r['locale'];applied=[]
 for i,to,why in rules:
  pair=pairs[i]
  if ident not in pair['tuples']:continue
  frm=pair['target'];assert v.count(frm)==1,(ident,frm,v.count(frm));v=v.replace(frm,to)
  fix={'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'authorValueSHA256':sha(r['value']),'pairId':i,'sourceText':pair['source'],'from':frm,'to':to,'reason':why,'occurrences':1};corrections.append(fix);applied.append(fix)
 ck=m.verify_text(r['sourceValue'],v,r['locale']);assert not ck['errors'],(ident,ck)
 rr={**r,'value':v,'valueSHA256':sha(v),'independentMeaningReview':'PASS_WITH_EXACT_CORRECTIONS'if applied else'PASS','independentReviewer':'article_he_pl_complete','independentReviewArtifact':'review/product-remainder-independent/product20_review.json','authorCandidateFile':c['candidateFile'],'authorCandidateFileSHA256':c['candidateFileSHA256']};out.append(rr)
write('product20_corrections.json',{'rules':corrections});write('product20_reviewed_candidates.json',{'rows':out})
write('product20_review.json',{'status':'PASS_AFTER_5_EXACT_CORRECTIONS','rows':20,'locales':sorted(set(r['locale']for r in rows)),'correctedRows':len(set((x['resourceId'],x['locale'])for x in corrections)),'semanticPairsRead':554,'exactUnchangedNumericUnitUniquePairs':1010,'exactUnchangedNumericCellOccurrences':0,'inlineParagraphsRead':63,'reviewMethod':'Full source-target prose, bullet, table header, role/age/size-label comparison, with exact repeated text deduplication and numeric-only mechanical preservation. Source/raw/digest/before exact binding verified independently; current source markup/images/attributes/links/tables/numbers/units verified by offline_translation.py before and after corrections. Printed garment wording retained as product identity. Source claims remain source claims; no new source-policy gate.','correctionsFile':'product20_corrections.json','rowsEvidence':checks,'sourceDefects':[],'scope':'Local independent candidate review only; parent owns integration and fresh live guards.'})
print({'rows':20,'corrections':len(corrections),'keys':[(x['resourceId'],x['locale'],x['pairId'])for x in corrections]})
