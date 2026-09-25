#!/usr/bin/env python3
"""Human-authored fashion-context corrections for the 17 owned locales; local only."""
from manual_repairs import put,source,edits,HERE
import json

# The source uses 'drop' to mean new arrivals, 'matching' for coordinated clothing,
# and 'sizing support' for clothing-size help. These explicit meanings avoid literal mistranslation.
copy={
'ar':['وصل حديثًا من البيجامات','الأم والطفل','الأب والطفل','ملابس عائلية متناسقة','تسوق ملابس الأم والطفل','تسوق ملابس الأب والطفل','تسوق ملابس عائلية متناسقة','مساعدة في اختيار المقاس','هل تبحث عن تنسيق يناسب المناسبة؟','تسوق بيجامات جديدة','تصفح أحدث البيجامات'],
'cs':['Nové pyžamové přírůstky','Maminka a dítě','Tatínek a dítě','Sladěné rodinné oblečení','Nakupujte oblečení pro maminku a dítě','Nakupujte oblečení pro tatínka a dítě','Nakupujte sladěné rodinné oblečení','Pomoc s výběrem velikosti','Hledáte sladěné oblečení pro tuto příležitost?','Nakupujte nová pyžama','Prohlédněte si nová pyžama'],
'de':['Neue Pyjamas','Mama und Kind','Papa und Kind','Partnerlooks für die Familie','Mama-und-Kind-Looks kaufen','Papa-und-Kind-Looks kaufen','Partnerlooks für die Familie kaufen','Hilfe bei der Größenwahl','Auf der Suche nach dem passenden Look für den Anlass?','Neue Pyjamas kaufen','Neue Pyjamas entdecken'],
'el':['Νέες αφίξεις σε πιτζάμες','Μαμά και παιδί','Μπαμπάς και παιδί','Ασορτί οικογενειακά ρούχα','Αγοράστε ρούχα για μαμά και παιδί','Αγοράστε ρούχα για μπαμπά και παιδί','Αγοράστε ασορτί οικογενειακά ρούχα','Βοήθεια στην επιλογή μεγέθους','Ψάχνετε το κατάλληλο ασορτί σύνολο για την περίσταση;','Αγοράστε νέες πιτζάμες','Δείτε τις νέες αφίξεις σε πιτζάμες'],
'es':['Novedades en pijamas','Mamá y peque','Papá y peque','Ropa a juego para la familia','Comprar ropa para mamá y peque','Comprar ropa para papá y peque','Comprar ropa a juego para la familia','Ayuda para elegir la talla','¿Buscas el conjunto a juego adecuado para la ocasión?','Comprar pijamas nuevos','Ver las novedades en pijamas'],
'fi':['Uudet pyjamat','Äiti ja lapsi','Isä ja lapsi','Yhteensopivat perheasut','Osta äidin ja lapsen asuja','Osta isän ja lapsen asuja','Osta yhteensopivia perheasuja','Apua koon valintaan','Etsitkö tilaisuuteen sopivia yhteensopivia asuja?','Osta uusia pyjamia','Tutustu uusiin pyjamiin'],
'fr':['Nouveautés pyjamas','Maman et enfant','Papa et enfant','Tenues assorties pour la famille','Acheter des tenues maman et enfant','Acheter des tenues papa et enfant','Acheter des tenues assorties pour la famille','Aide au choix de la taille','Vous cherchez les tenues assorties adaptées à l’occasion ?','Acheter les nouveaux pyjamas','Découvrir les nouveautés pyjamas'],
'hi':['नए पजामा संग्रह','माँ और बच्चा','पिता और बच्चा','परिवार के लिए मेल खाते कपड़े','माँ और बच्चे के कपड़े खरीदें','पिता और बच्चे के कपड़े खरीदें','परिवार के लिए मेल खाते कपड़े खरीदें','सही साइज़ चुनने में मदद','क्या आप इस अवसर के लिए सही मेल खाते कपड़े ढूँढ रहे हैं?','नए पजामे खरीदें','नए पजामा संग्रह देखें'],
'it':['Novità pigiami','Mamma e bambino','Papà e bambino','Abbigliamento coordinato per la famiglia','Acquista abbigliamento mamma e bambino','Acquista abbigliamento papà e bambino','Acquista abbigliamento coordinato per la famiglia','Aiuto nella scelta della taglia','Cerchi il coordinato giusto per l’occasione?','Acquista i nuovi pigiami','Scopri le novità pigiami'],
'ja':['新作パジャマ','ママと子ども','パパと子ども','家族のおそろいコーデ','ママと子どものおそろい服を見る','パパと子どものおそろい服を見る','家族のおそろい服を見る','サイズ選びをサポート','そのシーンにぴったりのおそろいコーデをお探しですか？','新作パジャマを見る','新作パジャマのコレクションを見る'],
'nl':['Nieuwe pyjama’s','Moeder en kind','Vader en kind','Bijpassende gezinsoutfits','Shop kleding voor moeder en kind','Shop kleding voor vader en kind','Shop bijpassende gezinsoutfits','Hulp bij het kiezen van de maat','Zoek je de juiste bijpassende outfits voor de gelegenheid?','Shop nieuwe pyjama’s','Bekijk de nieuwe pyjama’s'],
'no':['Nye pysjamaser','Mamma og barn','Pappa og barn','Matchende familieantrekk','Kjøp klær til mamma og barn','Kjøp klær til pappa og barn','Kjøp matchende familieantrekk','Hjelp med å velge størrelse','Leter du etter matchende antrekk til anledningen?','Kjøp nye pysjamaser','Se de nye pysjamasene'],
'pl':['Nowości wśród piżam','Mama i dziecko','Tata i dziecko','Dopasowane stroje rodzinne','Kup ubrania dla mamy i dziecka','Kup ubrania dla taty i dziecka','Kup dopasowane stroje rodzinne','Pomoc w wyborze rozmiaru','Szukasz pasujących strojów na tę okazję?','Kup nowe piżamy','Zobacz nowe piżamy'],
'pt-BR':['Novidades em pijamas','Mãe e criança','Pai e criança','Roupas combinando para a família','Comprar roupas para mãe e criança','Comprar roupas para pai e criança','Comprar roupas combinando para a família','Ajuda para escolher o tamanho','Procurando a combinação certa para a ocasião?','Comprar novos pijamas','Ver as novidades em pijamas'],
'ro':['Noutăți la pijamale','Mamă și copil','Tată și copil','Ținute asortate pentru familie','Cumpără haine pentru mamă și copil','Cumpără haine pentru tată și copil','Cumpără ținute asortate pentru familie','Ajutor pentru alegerea mărimii','Cauți ținutele asortate potrivite pentru această ocazie?','Cumpără pijamale noi','Descoperă noutățile la pijamale'],
'ru':['Новинки пижам','Мама и ребёнок','Папа и ребёнок','Одежда для всей семьи в едином стиле','Купить одежду для мамы и ребёнка','Купить одежду для папы и ребёнка','Купить семейную одежду в едином стиле','Помощь в выборе размера','Ищете подходящие комплекты для этого случая?','Купить новые пижамы','Посмотреть новинки пижам'],
'sv':['Nya pyjamasar','Mamma och barn','Pappa och barn','Matchande familjekläder','Handla kläder för mamma och barn','Handla kläder för pappa och barn','Handla matchande familjekläder','Hjälp att välja storlek','Letar du efter rätt matchande kläder för tillfället?','Handla nya pyjamasar','Se de nya pyjamasarna']}
keys=['New Pajama Drop','Mommy & Me','Daddy & Me','Family Matching','Shop Mommy & Me','Shop Daddy & Me','Shop Family Matching','Helpful sizing support','Need the right match for the moment?','Shop New Pajamas','Browse the New Pajama Drop']
for l,values in copy.items():
    for s,v in zip(keys,values):put(l,s,v,'Human-authored clothing-context disambiguation')

headings={
'ar':'إطلالات متناسقة للحظات التي تبقى في ذاكرة العائلة',
'cs':'Sladěné oblečení pro chvíle, na které rodiny nejraději vzpomínají',
'de':'Abgestimmte Looks für die schönsten Familienerinnerungen',
'el':'Ασορτί εμφανίσεις για τις στιγμές που μένουν στη μνήμη της οικογένειας',
'es':'Looks a juego para los momentos que más recuerdan las familias',
'fi':'Yhteensopivia asuja perheiden ikimuistoisimpiin hetkiin',
'fr':'Des tenues assorties pour les moments qui restent dans la mémoire des familles',
'hi':'परिवार की सबसे यादगार पलों के लिए मेल खाते परिधान',
'it':'Look coordinati per i momenti che le famiglie ricordano di più',
'ja':'家族の大切な思い出に残る、おそろいの装い',
'nl':'Bijpassende outfits voor de momenten die gezinnen het meest bijblijven',
'no':'Matchende antrekk til øyeblikkene familier husker best',
'pl':'Dopasowane stroje na chwile, które rodziny wspominają najchętniej',
'pt-BR':'Looks combinando para os momentos que ficam na memória da família',
'ro':'Ținute asortate pentru momentele pe care familiile le țin minte cel mai bine',
'ru':'Образы в едином стиле для самых памятных семейных моментов',
'sv':'Matchande kläder för de stunder familjer minns allra mest'}
for l,v in headings.items():put(l,'Matching looks for the moments families remember most',v)

trust={
'ar':'إطلالات متناسقة للحظات العائلية','cs':'Sladěné oblečení pro rodinné chvíle','de':'Partnerlooks für Familienmomente','el':'Ασορτί εμφανίσεις για οικογενειακές στιγμές','es':'Looks a juego para momentos en familia','fi':'Yhteensopivia asuja perheen yhteisiin hetkiin','fr':'Des tenues assorties pour les moments en famille','hi':'परिवार के खास पलों के लिए मेल खाते परिधान','it':'Look coordinati per i momenti in famiglia','ja':'家族の時間を彩るおそろいコーデ','nl':'Bijpassende outfits voor gezinsmomenten','no':'Matchende antrekk til familiestunder','pl':'Dopasowane stroje na rodzinne chwile','pt-BR':'Looks combinando para os momentos em família','ro':'Ținute asortate pentru momentele în familie','ru':'Образы в едином стиле для семейных моментов','sv':'Matchande kläder för familjens stunder'}
for l,v in trust.items():put(l,'Matching looks for family moments',v)

# Collection descriptions: faithful clothing meaning; shipping qualification explicitly approved by root.
pajama={
'ar':['<p>وصلت بيجامات جديدة. تسوق أحدث بيجامات الأم والطفل في مكان واحد.</p>','وصل حديثًا من البيجامات | بيجامات متناسقة أُضيفت حديثًا','تسوق أحدث بيجامات الأم والطفل ضمن تشكيلة واحدة. نقوش جديدة وأطقم مريحة، مع الشحن القياسي مشمولًا.'],
'cs':['<p>Právě dorazila nová pyžama. Nakupujte nejnovější pyžama pro maminku a dítě na jednom místě.</p>','Nová pyžama | Právě přidaná sladěná pyžama','Prohlédněte si nejnovější pyžama pro maminku a dítě v jednom výběru. Nové vzory, pohodlné soupravy a standardní doprava v ceně.'],
'de':['<p>Neue Pyjamas sind eingetroffen. Entdecken Sie die neuesten Mama-und-Kind-Pyjamas an einem Ort.</p>','Neue Pyjamas | Neu eingetroffene Partnerlook-Pyjamas','Entdecken Sie die neuesten Mama-und-Kind-Pyjamas in einer Auswahl. Neue Muster, gemütliche Sets und Standardversand inklusive.'],
'el':['<p>Μόλις έφτασαν νέες πιτζάμες. Αγοράστε τις πιο πρόσφατες πιτζάμες για μαμά και παιδί, όλες σε ένα μέρος.</p>','Νέες αφίξεις σε πιτζάμες | Νέες ασορτί πιτζάμες','Δείτε τις πιο πρόσφατες πιτζάμες για μαμά και παιδί σε μία συλλογή. Νέα σχέδια, άνετα σετ και κανονική αποστολή που περιλαμβάνεται.'],
'es':['<p>Acaban de llegar pijamas nuevos. Encuentra las últimas novedades en pijamas para mamá y peque en un solo lugar.</p>','Novedades en pijamas | Pijamas a juego recién añadidos','Descubre las últimas novedades en pijamas para mamá y peque en una sola selección. Nuevos estampados, conjuntos cómodos y envío estándar incluido.'],
'fi':['<p>Uusia pyjamia on juuri saapunut. Osta uusimmat äidin ja lapsen pyjamat yhdestä paikasta.</p>','Uudet pyjamat | Juuri lisätyt yhteensopivat pyjamat','Tutustu uusimpiin äidin ja lapsen pyjamiin yhdessä valikoimassa. Uusia kuvioita, mukavia settejä ja vakiotoimitus sisältyy hintaan.'],
'fr':['<p>De nouveaux pyjamas viennent d’arriver. Retrouvez toutes les nouveautés en pyjamas maman et enfant au même endroit.</p>','Nouveautés pyjamas | Pyjamas assortis tout juste ajoutés','Découvrez les derniers pyjamas maman et enfant dans une même sélection. Nouveaux imprimés, ensembles douillets et livraison standard incluse.'],
'hi':['<p>नए पजामे आ गए हैं। माँ और बच्चे के लिए सबसे नए पजामे एक ही जगह खरीदें।</p>','नए पजामा संग्रह | हाल ही में जोड़े गए मेल खाते पजामे','माँ और बच्चे के लिए नवीनतम पजामे एक ही संग्रह में देखें। नए प्रिंट, आरामदायक सेट और मानक शिपिंग शामिल है।'],
'it':['<p>Sono appena arrivati nuovi pigiami. Scopri tutte le ultime novità di pigiami mamma e bambino in un unico posto.</p>','Novità pigiami | Pigiami coordinati appena aggiunti','Scopri gli ultimi pigiami mamma e bambino in un’unica selezione. Nuove fantasie, completi comodi e spedizione standard inclusa.'],
'ja':['<p>新作パジャマが入荷しました。ママと子どもの最新のおそろいパジャマを、一か所でご覧いただけます。</p>','新作パジャマ | 新しく加わったおそろいパジャマ','ママと子どもの新作パジャマをまとめてチェック。新しい柄、心地よいセット、通常配送の送料込み。'],
'nl':['<p>Er zijn nieuwe pyjama’s binnen. Shop de nieuwste pyjama’s voor moeder en kind op één plek.</p>','Nieuwe pyjama’s | Net toegevoegde bijpassende pyjama’s','Bekijk de nieuwste pyjama’s voor moeder en kind in één selectie. Nieuwe prints, comfortabele sets en standaardverzending inbegrepen.'],
'no':['<p>Nye pysjamaser har akkurat kommet. Kjøp de nyeste pysjamasene til mamma og barn på ett sted.</p>','Nye pysjamaser | Nettopp tilføyd matchende pysjamas','Se de nyeste pysjamasene til mamma og barn i ett utvalg. Nye mønstre, behagelige sett og standardfrakt inkludert.'],
'pl':['<p>Właśnie pojawiły się nowe piżamy. Kup najnowsze piżamy dla mamy i dziecka w jednym miejscu.</p>','Nowości wśród piżam | Nowe dopasowane piżamy','Odkryj najnowsze piżamy dla mamy i dziecka w jednej kolekcji. Nowe wzory, wygodne zestawy i standardowa wysyłka w cenie.'],
'pt-BR':['<p>Acabaram de chegar novos pijamas. Encontre as últimas novidades de pijamas para mãe e criança em um só lugar.</p>','Novidades em pijamas | Pijamas combinando recém-adicionados','Confira os últimos pijamas para mãe e criança em uma só seleção. Novas estampas, conjuntos aconchegantes e frete padrão incluído.'],
'ro':['<p>Tocmai au sosit pijamale noi. Descoperă cele mai noi pijamale pentru mamă și copil într-un singur loc.</p>','Noutăți la pijamale | Pijamale asortate recent adăugate','Descoperă cele mai noi pijamale pentru mamă și copil într-o singură selecție. Imprimeuri noi, seturi confortabile și transport standard inclus.'],
'ru':['<p>У нас появились новые пижамы. Выбирайте последние новинки пижам для мамы и ребёнка в одном месте.</p>','Новинки пижам | Новые пижамы в едином стиле','Последние новинки пижам для мамы и ребёнка в одной подборке. Новые принты, уютные комплекты и стандартная доставка включена.'],
'sv':['<p>Nya pyjamasar har precis kommit in. Handla de senaste pyjamasarna för mamma och barn på ett ställe.</p>','Nya pyjamasar | Nyligen tillagda matchande pyjamasar','Se de senaste pyjamasarna för mamma och barn i ett urval. Nya mönster, mysiga set och standardfrakt ingår.']}
pj_sources=[source('<p>Fresh pajamas'), 'New Pajama Drop | Just Added Matching Pajamas',source('Shop the latest mommy-and-me')]
for l,values in pajama.items():
    for index,(s,v) in enumerate(zip(pj_sources,values)):
        put(l,s,v,'Human-authored fashion context; root-approved standard-shipping qualification' if index==2 else 'Human-authored fashion context')

if __name__=='__main__':
    (HERE/'manual_storefront_repairs_log.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    print('Local manual corrections:',len(edits))
