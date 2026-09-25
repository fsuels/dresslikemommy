from pathlib import Path
import json,re,hashlib,importlib.util
P=Path(__file__).parent;data=json.loads((P/'pl_candidate.json').read_text());original={r['resourceId']:r['value'] for r in data['rows']}
fixes={
'559471231073':[
('zacznij od <a','zacznij od kolekcji <a'),
('Dlatego <a','Dlatego kolekcje <a'),
('przejdź do <a','przejdź do artykułów <a'),
('lub przejrzyj <a','lub przejrzyj kolekcję <a')],
'559471329377':[('po codzienne inspiracje stylizacyjne.','aby codziennie czerpać inspiracje do stylizacji.')],
'559471558753':[
('Sprawdź nasze <a href="/collections/family-swimsuits">rodzinnych dopasowanych strojów kąpielowych</a>','Sprawdź nasze <a href="/collections/family-swimsuits">rodzinne dopasowane stroje kąpielowe</a>')],
'559471820897':[
('Sprawdź nasze <a href="/collections/matching-outfits">dopasowanych strojów</a> oraz <a href="/collections/family-matching">rodzinne dopasowane</a> kolekcje.','Sprawdź nasze kolekcje: <a href="/collections/matching-outfits">Dopasowane stroje</a> oraz <a href="/collections/family-matching">Dopasowane ubrania rodzinne</a>.'),
('Tematyczne dopasowane stroje — szczególnie na <a href="/collections/family-matching">rodzinne dopasowane</a> chwile','Tematyczne dopasowane stroje — szczególnie na <a href="/collections/family-matching">rodzinne chwile w dopasowanych ubraniach</a>')],
'559471919201':[
('— <a href="/collections/matching-outfits">dopasowanych strojów</a>','— <a href="/collections/matching-outfits">dopasowane stroje</a>')],
'559471984737':[
('Dopasowana <a href="/collections/dresses">sukienkach dla mamy i córki</a>','Dopasowana <a href="/collections/dresses">sukienka dla mamy i córki</a>'),
('Sprawdź nasze <a href="/collections/matching-outfits">dopasowanych strojów</a>','Sprawdź nasze <a href="/collections/matching-outfits">dopasowane stroje</a>')],
'559472050273':[
('Nasze <a href="/">Dress Like Mommy</a> kolekcje są','Nasze kolekcje <a href="/">Dress Like Mommy</a> są')]
}
audit=[]
for r in data['rows']:
 id=r['resourceId'].split('/')[-1];v=r['value']
 for old,new in fixes.get(id,[]):
  assert old in v,(id,old);v=v.replace(old,new)
 v=re.sub(r'(</a>)\s+([,.])',r'\1\2',v)
 r['value']=v
 if v!=original[r['resourceId']]:audit.append({'resourceId':r['resourceId'],'oldSHA256':hashlib.sha256(original[r['resourceId']].encode()).hexdigest(),'newSHA256':hashlib.sha256(v.encode()).hexdigest(),'contextualReplacements':fixes.get(id,[]),'closingAnchorPunctuationWhitespaceNormalized':True})
spec=importlib.util.spec_from_file_location('o',P.parent.parent/'tooling/offline_translation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base=[{**r,'source':r['sourceValue']} for r in json.loads((P.parent/'pl_baseline.json').read_text())];report=m.verify_rows(data['rows'],base);assert report['failedRows']==0,report
(P/'pl_candidate_v2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(P/'pl_first5_candidate_v2.json').write_text(json.dumps({**data,'rows':data['rows'][:5]},ensure_ascii=False,indent=2)+'\n');(P/'pl_checks_v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(P/'pl_author_inline_review.json').write_text(json.dumps({'status':'PASS_AUTHOR_INLINE_REVIEW','version':'v2','note':'Read all 63 full assembled linked paragraphs, fixed contextual Polish inflections and normalized punctuation joins. Original v1 retained. Source claims untouched. Independent semantic review still required.','changes':audit},ensure_ascii=False,indent=2)+'\n');print(report['status'],len(audit))
