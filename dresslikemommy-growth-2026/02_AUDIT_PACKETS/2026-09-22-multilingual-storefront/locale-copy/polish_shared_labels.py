from pathlib import Path
import json
P=Path(__file__).parent
# Best-selling family looks; dress best sellers; resort favorite; easy sets; pool-day favorite.
rows={
'ar':['الإطلالات العائلية الأكثر مبيعًا','الفساتين الأكثر مبيعًا','المفضل للعطلات','أطقم سهلة التنسيق','المفضل لأيام المسبح'],
'cs':['Nejprodávanější rodinné outfity','Nejprodávanější šaty','Oblíbené na dovolenou','Snadno kombinovatelné soupravy','Oblíbené k bazénu'],
'de':['Die meistverkauften Familienlooks','Die meistverkauften Kleider','Urlaubsfavorit','Unkomplizierte Sets','Favorit für Pooltage'],
'el':['Τα πιο δημοφιλή οικογενειακά σύνολα σε πωλήσεις','Τα φορέματα με τις περισσότερες πωλήσεις','Αγαπημένο για διακοπές','Εύκολοι συνδυασμοί σε σετ','Αγαπημένο για μέρες στην πισίνα'],
'es':['Conjuntos familiares más vendidos','Vestidos más vendidos','Favorito para vacaciones','Conjuntos fáciles de combinar','Favorito para días de piscina'],
'fi':['Myydyimmät perheasut','Myydyimmät mekot','Lomasuosikki','Helposti yhdisteltävät setit','Suosikki allaspäiviin'],
'fr':['Les tenues familiales les plus vendues','Les robes les plus vendues','Favori des vacances','Ensembles faciles à porter','Favori pour les journées à la piscine'],
'hi':['सबसे ज़्यादा बिकने वाले पारिवारिक लुक','सबसे ज़्यादा बिकने वाली ड्रेस','छुट्टियों का पसंदीदा','आसानी से पहने जाने वाले सेट','पूल के दिनों का पसंदीदा'],
'it':['I look di famiglia più venduti','Gli abiti più venduti','Preferito per le vacanze','Completi facili da indossare','Preferito per le giornate in piscina'],
'ja':['人気のファミリーコーデ','ベストセラーのワンピース','バケーションのお気に入り','手軽に着られるセット','プールの日のお気に入り'],
'nl':['Bestverkochte gezinsoutfits','Bestverkochte jurken','Vakantiefavoriet','Makkelijk te combineren sets','Favoriet voor dagen bij het zwembad'],
'no':['Bestselgende familieantrekk','Bestselgende kjoler','Feriefavoritt','Enkle sett','Favoritt til bassengdager'],
'pl':['Najlepiej sprzedające się stroje rodzinne','Najlepiej sprzedające się sukienki','Wakacyjny faworyt','Łatwe do zestawienia komplety','Ulubiony wybór na dni przy basenie'],
'pt-BR':['Looks de família mais vendidos','Vestidos mais vendidos','Favorito para as férias','Conjuntos fáceis de combinar','Favorito para dias de piscina'],
'ro':['Cele mai vândute ținute de familie','Cele mai vândute rochii','Favoritul vacanței','Seturi ușor de combinat','Favoritul zilelor la piscină'],
'ru':['Самые продаваемые семейные образы','Самые продаваемые платья','Любимый выбор для отпуска','Простые комплекты','Любимый выбор для дней у бассейна'],
'sv':['Bästsäljande familjekläder','Bästsäljande klänningar','Semesterfavorit','Lättburna set','Favorit för pooldagar']}
keys=['storefront.menu.best_selling_family_looks','storefront.menu.dress_best_sellers','storefront.menu.resort_favorite','storefront.menu.easy_sets','storefront.menu.pool_day_favorite']
changes=[]
for l,v in rows.items():
 f=P/f'shared_candidate_{l}.json';o=json.loads(f.read_text())
 for k,t in zip(keys,v):changes.append([l,k,o[k],t]);o[k]=t
 if l=='no':o.update({'storefront.journal.about_title':'Finn guiden, og kjøp deretter det matchende antrekket','storefront.journal.newsletter_title':'Få stylingtips og 10% rabatt','storefront.collection_fallback_body_html':'<p>Se {{ title }}, og sammenlign modellene i kolleksjonen.</p><p>Åpne hver produktside for å se tilgjengelige alternativer, størrelsesguiden og produktdetaljene før du velger.</p>'})
 f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
(P/'shared_label_corrections.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
