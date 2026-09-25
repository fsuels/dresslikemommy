from pathlib import Path
from collections import Counter
import hashlib, importlib.util, json
P=Path(__file__).resolve().parent; R=P.parent.parent
rows=json.loads((P/'retained96_worklist.json').read_text())['rows']
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
separates={
'ar':'Golden Daisy – قطع متناسقة للأم وابنتها',
'cs':'Golden Daisy – sladěné samostatné kousky pro maminku a dceru',
'da':'Golden Daisy – matchende enkeltdele til mor og datter',
'el':'Golden Daisy – ασορτί μεμονωμένα κομμάτια για μαμά και κόρη',
'fi':'Golden Daisy – yhteensopivat erilliset vaatekappaleet äidille ja tyttärelle',
'he':'Golden Daisy – פריטי לבוש נפרדים ותואמים לאמא ולבת',
'hi':'Golden Daisy – माँ और बेटी के लिए अलग-अलग मैचिंग परिधान',
'ja':'Golden Daisy – ママと娘のお揃いセパレートアイテム',
'ko':'Golden Daisy – 엄마와 딸을 위한 매칭 단품 의류',
'nl':'Golden Daisy – bijpassende losse kledingstukken voor moeder en dochter',
'no':'Golden Daisy – matchende enkeltplagg til mor og datter',
'pl':'Golden Daisy – pasujące oddzielne elementy garderoby dla mamy i córki',
'pt-BR':'Golden Daisy – peças avulsas combinando para mãe e filha',
'ro':'Golden Daisy – piese separate asortate pentru mamă și fiică',
'ru':'Golden Daisy — отдельные сочетающиеся вещи для мамы и дочки',
'sv':'Golden Daisy – matchande separata plagg för mamma och dotter',
}
seo={
'Family Matching Bikini Sets - Floral Print | Dress Like Mommy':{
'fr':'Ensembles de bikinis assortis pour la famille – Imprimé floral | Dress Like Mommy',
'it':'Set di bikini coordinati per la famiglia – Stampa floreale | Dress Like Mommy',
'ja':'家族でお揃いのビキニセット – 花柄 | Dress Like Mommy',
'pl':'Rodzinne komplety bikini w pasującym stylu – Kwiatowy nadruk | Dress Like Mommy'},
'Family Matching Button-Down Shirts - Floral Print | Dress Like Mommy':{
'ar':'قمصان متناسقة بأزرار للعائلة – طبعة زهور | Dress Like Mommy',
'it':'Camicie coordinate con bottoni per la famiglia – Stampa floreale | Dress Like Mommy',
'ja':'家族でお揃いのボタン付きシャツ – 花柄 | Dress Like Mommy',
'nl':'Bijpassende overhemden met knopen voor het gezin – Bloemenprint | Dress Like Mommy'},
'Family Matching Button-Down Shirts - Navy Floral | Dress Like Mommy':{
'ar':'قمصان متناسقة بأزرار للعائلة – نقشة زهور باللون الكحلي | Dress Like Mommy',
'it':'Camicie coordinate con bottoni per la famiglia – Motivo floreale blu navy | Dress Like Mommy',
'ja':'家族でお揃いのボタン付きシャツ – ネイビーの花柄 | Dress Like Mommy',
'nl':'Bijpassende overhemden met knopen voor het gezin – Marineblauw bloemenmotief | Dress Like Mommy',
'pl':'Rodzinne pasujące koszule zapinane na guziki – Granatowy motyw kwiatowy | Dress Like Mommy'},
'Family Matching Button-Down Shirts - Green Floral | Dress Like Mommy':{
'it':'Camicie coordinate con bottoni per la famiglia – Motivo floreale verde | Dress Like Mommy',
'ja':'家族でお揃いのボタン付きシャツ – グリーンの花柄 | Dress Like Mommy',
'pl':'Rodzinne pasujące koszule zapinane na guziki – Zielony motyw kwiatowy | Dress Like Mommy'},
}
out=[];checks=[]
for r in rows:
 if r['key']=='body_html':continue
 old=r['before']['value'];new=old
 if r['key']=='product_type':
  if r['locale']=='nl':
   new='Zwemkleding';reason='Dutch Badpakken narrows the generic current Swimwear category to one-piece suits; use the full generic category.'
  else:reason='Full equivalent swimwear category reviewed in this mother/child swimsuit context; re-register identical value against current source digest to clear outdated metadata.'
 elif r['key']=='title':
  assert r['source']=='Golden Daisy Mommy & Me Matching Separates';new=separates[r['locale']];reason='Translate the complete current title, restoring explicit matching coordination and separate garments while preserving the Golden Daisy design name.'
 else:
  new=seo[r['source']][r['locale']];reason='Replace older SEO wording with a complete equivalent of current source: preserve family coordination, garment, floral/color qualifier and Dress Like Mommy brand; do not retain stale extra attributes or omitted current terms.'
 check=v.verify_text(r['source'],new,r['locale']);assert not check['errors'],(r,check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']}
 rr.update(sourceValue=r['source'],value=new,reason=reason,marketId=None,independentReview='SOURCE_MEANING_REVIEWED_BY_AUTHOR_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'disposition':'IDENTICAL_EQUIVALENT_REFRESH' if new==old else 'FULL_SOURCE_TRANSLATION_CORRECTION','meaning':'AUTHOR_REVIEW_PASS','preservation':check,'sourceSHA256':hashlib.sha256(r['source'].encode()).hexdigest(),'beforeSHA256':hashlib.sha256(old.encode()).hexdigest(),'valueSHA256':hashlib.sha256(new.encode()).hexdigest()})
assert len(out)==72
for name,d in [('retained_short72_candidate.json',{'rows':out}),('retained_short72_checks.json',{'counts':dict(Counter(c['disposition'] for c in checks)),'fields':checks,'limits':'Offline complete-source review only. Root must independently review, fresh-read source and before, publish and verify.'})]:
 (P/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'counts':dict(Counter(c['disposition'] for c in checks))}))
