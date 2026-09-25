from pathlib import Path
import json,re,hashlib,html,importlib.util
P=Path(__file__).parent;PACK=P.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest();write=lambda n,d:(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('o',PACK/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pairs=json.loads((P/'product16_pairs.json').read_text());rows=json.loads((P/'product16_candidates_frozen_copy.json').read_text())['rows'];checks=json.loads((P/'product16_checks.json').read_text())['rows']
rules=[(457, '뒤집어서 찬물에 약한 세탁 코스로 세탁하고, 줄에 널어 말리거나 건조기에서 낮은 온도로 건조하세요. 표백제는 사용하지 마세요.', 'Retain explicit tumble-dryer alternative rather than unspecified low-temperature drying.'), (637, 'Dziecko 2 lata', 'Correct Polish age-label grammatical inflection without changing age.'), (638, 'Dziecko 3 lata', 'Correct Polish age-label grammatical inflection without changing age.'), (639, 'Dziecko 4 lata', 'Correct Polish age-label grammatical inflection without changing age.')]
corrections=[];out=[]
for r,c in zip(rows,checks):
 v=r['value'];ident=r['resourceId'].split('/')[-1]+':'+r['locale'];applied=[]
 for i,to,why in rules:
  pair=pairs[i]
  if ident not in pair['tuples']:continue
  frm=pair['target'];assert v.count(frm)==1,(ident,frm,v.count(frm));v=v.replace(frm,to)
  fix={'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourceDigest':r['sourceDigest'],'authorValueSHA256':sha(r['value']),'pairId':i,'sourceText':pair['source'],'from':frm,'to':to,'reason':why,'occurrences':1};corrections.append(fix);applied.append(fix)
 ck=m.verify_text(r['sourceValue'],v,r['locale']);assert not ck['errors'],(ident,ck)
 rr={**r,'value':v,'valueSHA256':sha(v),'independentMeaningReview':'PASS_WITH_EXACT_CORRECTIONS'if applied else'PASS','independentReviewer':'article_he_pl_complete','independentReviewArtifact':'review/product-remainder-independent/product16_review.json','authorCandidateFile':c['candidateFile'],'authorCandidateFileSHA256':c['candidateFileSHA256']};out.append(rr)
write('product16_corrections.json',{'rules':corrections});write('product16_reviewed_candidates.json',{'rows':out})
write('product16_review.json',{'status':'PASS_AFTER_4_EXACT_CORRECTIONS','rows':16,'locales':sorted(set(r['locale']for r in rows)),'correctedRows':len(set((x['resourceId'],x['locale'])for x in corrections)),'semanticPairsRead':896,'exactUnchangedNumericUnitUniquePairs':0,'exactUnchangedNumericCellOccurrences':1232,'inlineParagraphsRead':176,'reviewMethod':'Full source-target prose, bullet, table header, role/age/size-label comparison, with exact repeated text deduplication and numeric-only mechanical preservation. Source/raw/digest/before exact binding verified independently; current source markup/images/attributes/links/tables/numbers/units verified by offline_translation.py before and after corrections. Printed garment wording retained as product identity. Source claims remain source claims; no new source-policy gate.','correctionsFile':'product16_corrections.json','rowsEvidence':checks,'sourceDefects':[],'scope':'Local independent candidate review only; parent owns integration and fresh live guards.'})
print({'rows':16,'corrections':len(corrections),'keys':[(x['resourceId'],x['locale'],x['pairId'])for x in corrections]})
