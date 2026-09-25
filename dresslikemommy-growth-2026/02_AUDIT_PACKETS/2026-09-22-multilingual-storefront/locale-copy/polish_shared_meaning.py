from pathlib import Path
import json
P=Path(__file__).parent
keys=['storefront.journal.spotlight_title','storefront.journal.spotlight_body','storefront.menu.family_description','storefront.callout.matching_couples_t_shirts.callout_title','storefront.callout.matching_couples_t_shirts.callout_body','storefront.callout.new_pajama_drop.callout_title','storefront.home_title','storefront.home_description']
rows={
'ar':'''ملابس سباحة عائلية بإطلالة أنيقة في الصور
استعن بأدلة ملابس السباحة لمقارنة موديلات الأم وابنتها وملابس السباحة العائلية المتناسقة وملابس الشاطئ قبل التسوق.
ابدأ بالملابس العائلية المتناسقة، ثم اكتشف ملابس العطلات العائلية المتناسقة وملابس السباحة أو القمصان المتناسقة للأب وطفله.
قارن القمصان المتناسقة للأزواج هنا، ثم اكتشف المزيد من الإطلالات المتناسقة
قارن تصاميم القمصان المتناسقة للأزواج هنا، ثم اكتشف الملابس العائلية المتناسقة لمزيد من الخيارات.
ملابس نوم متناسقة جديدة في مجموعة مختارة واحدة
فساتين للأم وابنتها | ملابس عائلية متناسقة
تسوق فساتين الأم وابنتها والملابس المتناسقة للأم وطفلها وللعائلة للصور والعطلات واللحظات اليومية.''',
'cs':'''Rodinné plavky, které na fotografiích vypadají elegantně
Před nákupem porovnejte pomocí průvodců plavkami modely pro maminku a dceru, sladěné rodinné plavky a plážové oblečení.
Začněte sladěnými rodinnými outfity a pak objevujte oblečení na rodinnou dovolenou, sladěné plavky nebo košile pro tatínka a dítě.
Porovnejte zde trička pro páry a pak objevte další sladěné outfity
Porovnejte zde motivy sladěných triček pro páry a poté si prohlédněte rodinné oblečení pro další možnosti.
Nová sladěná pyžama v jednom přehledném výběru
Šaty pro maminku a dceru | Sladěné rodinné oblečení
Nakupujte šaty pro maminku a dceru, sladěné oblečení pro maminku a dítě i celou rodinu na focení, dovolenou a běžné dny.''',
'de':'''Familienbademode, die auf Fotos stilvoll aussieht
Vergleichen Sie mit den Bademode-Ratgebern Badeanzüge für Mutter und Tochter, abgestimmte Familienbademode und Strandoutfits vor dem Kauf.
Entdecken Sie zuerst Familienoutfits im Partnerlook und danach passende Urlaubsoutfits, Bademode oder Hemden für Papa und Kind.
Vergleichen Sie T-Shirts für Paare und entdecken Sie weitere Partnerlooks
Vergleichen Sie hier die Motive der Partner-T-Shirts und entdecken Sie Familienoutfits für weitere passende Looks.
Neue Pyjamas im Partnerlook in einer übersichtlichen Auswahl
Kleider für Mutter und Tochter | Familienoutfits im Partnerlook
Entdecken Sie Kleider für Mutter und Tochter sowie Partnerlooks für Mama und Kind und die ganze Familie für Fotos, Urlaub und Alltag.''',
'el':'''Οικογενειακά μαγιό για κομψές εμφανίσεις στις φωτογραφίες
Χρησιμοποιήστε τους οδηγούς μαγιό για να συγκρίνετε μαγιό για μαμά και κόρη, ταιριαστά οικογενειακά μαγιό και ρούχα παραλίας πριν από τις αγορές σας.
Ξεκινήστε με ταιριαστά οικογενειακά σύνολα και έπειτα δείτε σύνολα διακοπών, μαγιό ή πουκάμισα για μπαμπά και παιδί.
Συγκρίνετε εδώ μπλουζάκια για ζευγάρια και ανακαλύψτε περισσότερες ταιριαστές εμφανίσεις
Συγκρίνετε εδώ τα σχέδια στα ταιριαστά μπλουζάκια για ζευγάρια και δείτε οικογενειακά σύνολα για περισσότερες επιλογές.
Νέες ταιριαστές πιτζάμες συγκεντρωμένες σε μία επιλογή
Φορέματα για μαμά και κόρη | Ταιριαστά οικογενειακά σύνολα
Αγοράστε φορέματα για μαμά και κόρη, ταιριαστά ρούχα για μαμά και παιδί και οικογενειακά σύνολα για φωτογραφίες, διακοπές και καθημερινές στιγμές.''',
'es':'''Bañadores familiares que quedan elegantes en las fotos
Consulta las guías de moda de baño para comparar bañadores de madre e hija, modelos familiares a juego y ropa de playa antes de comprar.
Empieza por los conjuntos familiares a juego y descubre después ropa para vacaciones en familia, bañadores o camisas a juego para papá y peques.
Compara camisetas para parejas y descubre más conjuntos a juego
Compara aquí los diseños de camisetas a juego para parejas y descubre conjuntos familiares para encontrar más estilos.
Pijamas nuevos a juego reunidos en una selección
Vestidos para madre e hija | Conjuntos familiares a juego
Compra vestidos para madre e hija, ropa a juego para mamá y peques y conjuntos familiares para fotos, vacaciones y momentos cotidianos.''',
'fi':'''Tyylikkäältä kuvissa näyttävät perheen uima-asut
Vertaa uima-asujen oppaiden avulla äidin ja tyttären uimapukuja, yhteensopivia perheen uima-asuja ja ranta-asuja ennen ostamista.
Tutustu ensin yhteensopiviin perheasuihin ja sitten perheen loma-asuihin, uima-asuihin tai isän ja lapsen paitoihin.
Vertaa pariskuntien T-paitoja ja tutustu muihin yhteensopiviin asuihin
Vertaa pariskuntien yhteensopivien T-paitojen kuvioita täällä ja tutustu perheasuihin löytääksesi lisää tyylejä.
Uudet yhteensopivat pyjamat yhdessä selkeässä valikoimassa
Äidin ja tyttären mekot | Yhteensopivat perheasut
Osta äidin ja tyttären mekkoja sekä äidin ja lapsen ja koko perheen yhteensopivia asuja kuvauksiin, lomalle ja arkeen.''',
'fr':'''Des maillots de bain familiaux élégants sur les photos
Consultez les guides de maillots de bain pour comparer les modèles mère-fille, les maillots familiaux assortis et les tenues de plage avant vos achats.
Commencez par les tenues familiales assorties, puis découvrez les tenues de vacances, les maillots de bain ou les chemises assorties pour papa et enfant.
Comparez les t-shirts pour couples, puis découvrez d’autres tenues assorties
Comparez ici les motifs des t-shirts assortis pour couples, puis explorez les tenues familiales pour découvrir davantage de styles.
De nouveaux pyjamas assortis réunis dans une sélection
Robes mère-fille | Tenues familiales assorties
Découvrez des robes mère-fille, des tenues assorties pour maman et enfant et des vêtements familiaux pour les photos, les vacances et le quotidien.''',
'hi':'''तस्वीरों में सलीकेदार दिखने वाले पारिवारिक स्विमवियर
खरीदारी से पहले स्विमवियर गाइड की मदद से माँ-बेटी के स्विमसूट, परिवार के मैचिंग स्विमसूट और समुद्र तट के कपड़ों की तुलना करें।
परिवार के मैचिंग कपड़ों से शुरू करें, फिर छुट्टियों के लिए पारिवारिक कपड़े, मैचिंग स्विमसूट या पिता और बच्चे की मैचिंग शर्ट देखें।
जोड़ों की मैचिंग टी-शर्ट की तुलना करें, फिर और मैचिंग लुक देखें
यहाँ जोड़ों की मैचिंग टी-शर्ट के डिज़ाइन की तुलना करें और अधिक शैलियों के लिए परिवार के मैचिंग कपड़े देखें।
नए मैचिंग पायजामे, एक ही चुनिंदा संग्रह में
माँ-बेटी की ड्रेस | परिवार के मैचिंग कपड़े
फ़ोटो, छुट्टियों और रोज़मर्रा के पलों के लिए माँ-बेटी की ड्रेस, माँ और बच्चे के मैचिंग कपड़े और पूरे परिवार के मैचिंग कपड़े खरीदें।''',
'it':'''Costumi da bagno per la famiglia eleganti in foto
Consulta le guide ai costumi da bagno per confrontare modelli madre-figlia, costumi coordinati per la famiglia e abbigliamento da spiaggia prima dell’acquisto.
Parti dai look coordinati per la famiglia e scopri poi outfit per le vacanze, costumi da bagno o camicie coordinate per papà e bambini.
Confronta le t-shirt per coppie e scopri altri look coordinati
Confronta qui le fantasie delle t-shirt coordinate per coppie, poi scopri gli outfit per la famiglia per trovare altri stili.
Nuovi pigiami coordinati riuniti in una selezione
Abiti per mamma e figlia | Look coordinati per la famiglia
Acquista abiti per mamma e figlia, look coordinati per mamma e bambini e abbigliamento per tutta la famiglia per foto, vacanze e momenti quotidiani.''',
'ja':'''写真映えする家族のおそろい水着
購入前に水着ガイドを参考に、ママと娘の水着、家族のおそろい水着、ビーチコーデを比較しましょう。
まず家族のおそろいコーデを見てから、バケーション用コーデ、おそろい水着、パパと子どものシャツもチェックしましょう。
カップルのおそろいTシャツを比較して、ほかのおそろいコーデもチェック
ここでカップルのおそろいTシャツのデザインを比較し、家族のおそろいコーデでほかのスタイルも探しましょう。
新作のおそろいパジャマをひとつのセレクションに
ママと娘のおそろいワンピース | 家族のおそろいコーデ
写真撮影、バケーション、日常のひとときに、ママと娘のワンピース、ママと子どもや家族のおそろいコーデをお選びください。''',
'nl':'''Familiebadkleding die stijlvol staat op foto's
Gebruik de badkledinggidsen om moeder-dochterbadkleding, bijpassende gezinsbadkleding en strandoutfits te vergelijken voordat je koopt.
Begin met bijpassende gezinsoutfits en ontdek daarna vakantieoutfits, bijpassende badkleding of overhemden voor papa en kind.
Vergelijk T-shirts voor koppels en ontdek meer bijpassende outfits
Vergelijk hier de ontwerpen van bijpassende T-shirts voor koppels en ontdek gezinsoutfits voor meer stijlen.
Nieuwe bijpassende pyjama’s samen in één selectie
Jurken voor moeder en dochter | Bijpassende gezinsoutfits
Shop jurken voor moeder en dochter en bijpassende kleding voor mama en kind en het hele gezin voor foto's, vakanties en dagelijkse momenten.''',
'no':'''Familiebadetøy som ser stilfullt ut på bilder
Bruk badetøyguidene til å sammenligne badedrakter til mor og datter, matchende familiebadetøy og strandantrekk før du handler.
Start med matchende familieantrekk og utforsk deretter ferieantrekk, matchende badetøy eller skjorter til pappa og barn.
Sammenlign T-skjorter til par og utforsk flere matchende antrekk
Sammenlign motivene på matchende T-skjorter til par her, og utforsk familieantrekk for flere stiler.
Nye matchende pysjamaser samlet i ett utvalg
Kjoler til mor og datter | Matchende familieantrekk
Kjøp kjoler til mor og datter og matchende klær til mamma og barn og hele familien til bilder, ferier og hverdagsøyeblikk.''',
'pl':'''Rodzinne stroje kąpielowe, które elegancko wyglądają na zdjęciach
Przed zakupem skorzystaj z poradników o strojach kąpielowych, aby porównać modele dla mamy i córki, dopasowane stroje rodzinne i ubrania na plażę.
Zacznij od dopasowanych strojów rodzinnych, a potem odkryj ubrania na wakacje, stroje kąpielowe lub koszule dla taty i dziecka.
Porównaj T-shirty dla par i odkryj więcej dopasowanych stylizacji
Porównaj tutaj wzory dopasowanych T-shirtów dla par, a potem przejrzyj stroje rodzinne, aby znaleźć więcej stylów.
Nowe dopasowane piżamy zebrane w jednym miejscu
Sukienki dla mamy i córki | Dopasowane stroje rodzinne
Kupuj sukienki dla mamy i córki oraz dopasowane ubrania dla mamy i dziecka i całej rodziny do zdjęć, na wakacje i codzienne chwile.''',
'pt-BR':'''Moda praia em família que fica elegante nas fotos
Use os guias de moda praia para comparar modelos de mãe e filha, trajes de banho combinando em família e roupas de praia antes de comprar.
Comece pelos looks combinando em família e depois explore roupas de férias, moda praia ou camisas combinando para pai e criança.
Compare camisetas para casais e descubra mais looks combinando
Compare aqui as estampas das camisetas combinando para casais e explore os looks de família para encontrar mais estilos.
Novos pijamas combinando reunidos em uma seleção
Vestidos para mãe e filha | Looks combinando em família
Compre vestidos para mãe e filha, roupas combinando para mãe e criança e looks para toda a família para fotos, férias e momentos do dia a dia.''',
'ro':'''Costume de baie pentru familie care arată elegant în fotografii
Folosește ghidurile de costume de baie pentru a compara modele pentru mamă și fiică, costume asortate pentru familie și ținute de plajă înainte de cumpărare.
Începe cu ținute asortate pentru familie, apoi descoperă haine de vacanță, costume de baie asortate sau cămăși pentru tată și copil.
Compară tricouri pentru cupluri și descoperă mai multe ținute asortate
Compară aici imprimeurile tricourilor asortate pentru cupluri, apoi descoperă ținute de familie pentru mai multe stiluri.
Pijamale asortate noi, reunite într-o singură selecție
Rochii pentru mamă și fiică | Ținute asortate pentru familie
Cumpără rochii pentru mamă și fiică, haine asortate pentru mamă și copil și ținute de familie pentru fotografii, vacanțe și momente de zi cu zi.''',
'ru':'''Семейные купальники для стильных фотографий
Перед покупкой сравните с помощью гидов по купальникам модели для мамы и дочки, парные семейные купальники и пляжные наряды.
Начните с парных семейных нарядов, а затем посмотрите одежду для отпуска, парные купальники или рубашки для папы и ребёнка.
Сравните футболки для пар и посмотрите другие парные образы
Сравните здесь рисунки на парных футболках для двоих, а затем посмотрите семейные наряды, чтобы найти другие стили.
Новые парные пижамы в одной подборке
Платья для мамы и дочки | Парные семейные наряды
Выбирайте платья для мамы и дочки, парную одежду для мамы и ребёнка и всей семьи для фотографий, отпуска и повседневных моментов.''',
'sv':'''Familjebadkläder som ser stilfulla ut på bilder
Använd badklädesguiderna för att jämföra baddräkter för mamma och dotter, matchande familjebadkläder och strandkläder innan du handlar.
Börja med matchande familjekläder och utforska sedan semesterkläder, matchande badkläder eller skjortor för pappa och barn.
Jämför T-shirts för par och upptäck fler matchande outfits
Jämför motiven på matchande T-shirts för par här och utforska familjekläder för fler stilar.
Nya matchande pyjamasar samlade i ett urval
Klänningar för mamma och dotter | Matchande familjekläder
Köp klänningar för mamma och dotter samt matchande kläder för mamma och barn och hela familjen för foton, semester och vardagsstunder.'''
}
changes=[]
for l,strings in rows.items():
 v=strings.splitlines();assert len(v)==len(keys),(l,len(v));f=P/f'shared_candidate_{l}.json';o=json.loads(f.read_text())
 for k,s in zip(keys,v):changes.append([l,k,o[k],s]);o[k]=s
 f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
(P/'shared_meaning_corrections.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('Manually corrected',len(changes),'high-visibility semantic values')
