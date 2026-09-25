from pathlib import Path
import json
P=Path(__file__).parent
rows=json.loads((P/'home_category_existing.json').read_text())
keys=list(rows['en'])
values={
'ar':'''تسوق حسب الفئة
تسوق حسب المناسبة
الشحن القياسي مشمول
إطلالات متناسقة للحظات العائلية
ملابس سهلة التنسيق للصور والرحلات والاحتفالات
مساعدة في اختيار المقاس
تنسيق ملابس العائلة بسهولة
نرد خلال يوم عمل واحد
أنا وأمي
ملابس عائلية متناسقة
ملابس نوم
فساتين متناسقة
ملابس سباحة
أنا وأبي
العطلات
أيام التصوير
أعياد الميلاد
أيام الشاطئ
اختيارات محبوبة للأم وابنتها
إطلالات متناسقة للجميع
أطقم ناعمة لليالٍ مريحة
فساتين جاهزة للتصوير
إطلالات سباحة لأيام الشاطئ
لحظات متناسقة للأب وطفله
إطلالات للمنتجع طوال الرحلة
مصممة للصور العائلية
ملابس لطيفة للاحتفالات
تصاميم متناسقة للأيام المشمسة
الأكثر محبة
المفضل للعطلات
اختيار لمناسبات الربيع
ملابس نوم جديدة
تسوق هذه الإطلالة
تسوق ملابس النوم الجديدة
تسوق فساتين الأم وابنتها لحضور حفلات الزفاف
تسوق ملابس عائلية متناسقة للعطلات
تصفح الفساتين المتناسقة لمناسبات الربيع
تصفح ملابس النوم الجديدة''',
'cs':'''Nakupovat podle kategorie
Nakupovat podle příležitosti
Standardní doprava je zahrnuta v ceně
Sladěné oblečení pro rodinné chvíle
Snadno kombinovatelné oblečení na focení, výlety a oslavy
Pomoc s výběrem velikosti
Sladění rodinného oblečení snadno
Odpovídáme do 1 pracovního dne
Maminka a já
Sladěné rodinné oblečení
Pyžama
Sladěné šaty
Plavky
Tatínek a já
Dovolená
Focení
Narozeniny
Dny na pláži
Oblíbené kousky pro maminku a dceru
Sladěné oblečení pro všechny
Měkké soupravy pro útulné večery
Šaty připravené na focení
Plavky na dny u moře
Sladěné chvíle tatínka a dítěte
Oblečení do letoviska na celou dovolenou
Pro rodinné portréty
Roztomilé oblečení na oslavy
Sladěné styly do slunečných dnů
Nejoblíbenější
Oblíbené na dovolenou
Tip na jarní události
Nová pyžama
Nakupovat tento outfit
Nakupovat nová pyžama
Nakupovat šaty pro maminku a dceru na svatbu
Nakupovat sladěné rodinné oblečení na dovolenou
Prohlédnout sladěné šaty na jarní události
Prohlédnout nová pyžama''',
'el':'''Αγορές ανά κατηγορία
Αγορές ανά περίσταση
Περιλαμβάνεται η τυπική αποστολή
Ταιριαστές εμφανίσεις για οικογενειακές στιγμές
Εύκολα σύνολα για φωτογραφίες, ταξίδια και γιορτές
Βοήθεια με τα μεγέθη
Εύκολοι συνδυασμοί για όλη την οικογένεια
Απαντάμε εντός 1 εργάσιμης ημέρας
Μαμά κι εγώ
Ταιριαστά οικογενειακά σύνολα
Πιτζάμες
Ταιριαστά φορέματα
Μαγιό
Μπαμπάς κι εγώ
Διακοπές
Φωτογραφίσεις
Γενέθλια
Μέρες στην παραλία
Αγαπημένες επιλογές για μαμά και κόρη
Συνδυασμένες εμφανίσεις για όλους
Απαλά σετ για άνετες νύχτες
Φορέματα έτοιμα για φωτογραφίες
Μαγιό για μέρες στην παραλία
Ταιριαστές στιγμές για μπαμπά και παιδί
Εμφανίσεις διακοπών για όλο το ταξίδι
Για οικογενειακά πορτρέτα
Γλυκά σύνολα για γιορτές
Ταιριαστά στυλ για τον ήλιο
Τα πιο αγαπημένα
Αγαπημένη επιλογή διακοπών
Πρόταση για ανοιξιάτικες εκδηλώσεις
Νέες πιτζάμες
Αγοράστε αυτή την εμφάνιση
Αγοράστε νέες πιτζάμες
Αγοράστε φορέματα για μαμά και κόρη ως καλεσμένες σε γάμο
Αγοράστε ταιριαστά οικογενειακά σύνολα διακοπών
Δείτε ταιριαστά φορέματα για ανοιξιάτικες εκδηλώσεις
Δείτε τις νέες πιτζάμες''',
'fi':'''Osta kategorian mukaan
Osta tilaisuuden mukaan
Vakiotoimitus sisältyy hintaan
Yhteensopivia asuja perheen yhteisiin hetkiin
Helppoja asuja kuvauksiin, matkoille ja juhliin
Apua koon valintaan
Perheen asujen yhteensovitus helposti
Vastaamme yhden arkipäivän kuluessa
Äiti ja minä
Yhteensopivat perheasut
Pyjamat
Yhteensopivat mekot
Uima-asut
Isä ja minä
Loma
Kuvauspäivät
Syntymäpäivät
Rantapäivät
Äidin ja tyttären suosikit
Yhteensopivia asuja kaikille
Pehmeitä settejä viihtyisiin iltoihin
Mekkoja valokuviin
Uima-asuja rantapäiviin
Isän ja lapsen yhteisiä asuhetkiä
Loma-asuja koko matkalle
Perhekuvia varten
Suloisia juhla-asuja
Yhteensopivia tyylejä aurinkoisiin päiviin
Rakastetuimmat
Lomasuosikki
Valinta kevään juhliin
Uudet pyjamat
Osta tämä asu
Osta uusia pyjamia
Osta äidin ja tyttären mekkoja häävieraille
Osta yhteensopivia perheen loma-asuja
Selaa yhteensopivia mekkoja kevään juhliin
Selaa uusia pyjamia''',
'he':'''קנייה לפי קטגוריה
קנייה לפי אירוע
משלוח רגיל כלול במחיר
לבוש תואם לרגעים משפחתיים
לבוש נוח לתמונות, לטיולים ולחגיגות
עזרה בבחירת מידה
התאמת לבוש משפחתי בקלות
מענה בתוך יום עסקים אחד
אמא ואני
לבוש משפחתי תואם
פיג׳מות
שמלות תואמות
בגדי ים
אבא ואני
חופשה
ימי צילום
ימי הולדת
ימים בחוף
פריטים אהובים לאמא ולבת
לבוש מתואם לכולם
סטים רכים ללילות נעימים
שמלות מוכנות לצילום
בגדי ים לימים בחוף
רגעים תואמים לאבא ולילד
לבוש לנופש לכל הטיול
לצילומי דיוקן משפחתיים
לבוש מתוק לחגיגות
סגנונות תואמים לימים שטופי שמש
הכי אהובים
מועדף לחופשה
בחירה לאירועי האביב
פיג׳מות חדשות
קנו את הלוק הזה
קנו פיג׳מות חדשות
קנו שמלות לאמא ולבת כאורחות בחתונה
קנו לבוש משפחתי תואם לחופשה
עיינו בשמלות תואמות לאירועי האביב
עיינו בפיג׳מות החדשות''',
'hi':'''श्रेणी के अनुसार खरीदें
अवसर के अनुसार खरीदें
मानक शिपिंग शामिल है
परिवार के खास पलों के लिए मैचिंग कपड़े
फ़ोटो, यात्राओं और उत्सवों के लिए आसानी से पहनने योग्य कपड़े
साइज़ चुनने में मदद
परिवार के लिए मैचिंग कपड़े चुनना आसान
1 कार्यदिवस में जवाब देते हैं
माँ और मैं
परिवार के मैचिंग कपड़े
पायजामे
मैचिंग ड्रेस
स्विमसूट
पापा और मैं
छुट्टियाँ
फ़ोटो के दिन
जन्मदिन
समुद्र तट के दिन
माँ-बेटी की पसंदीदा शैलियाँ
सबके लिए मेल खाते कपड़े
आरामदायक रातों के लिए मुलायम सेट
फ़ोटो के लिए तैयार ड्रेस
समुद्र तट के दिनों के लिए स्विमवियर
पिता और बच्चे के मैचिंग पल
पूरी यात्रा के लिए रिज़ॉर्ट लुक
पारिवारिक फ़ोटो के लिए बने
उत्सव के लिए प्यारे कपड़े
धूप वाले दिनों के लिए मैचिंग शैलियाँ
सबसे पसंदीदा
छुट्टियों का पसंदीदा
वसंत के आयोजनों के लिए खास चुनाव
नए पायजामे
यह लुक खरीदें
नए पायजामे खरीदें
शादी में मेहमान बनकर जाने के लिए माँ-बेटी की ड्रेस खरीदें
छुट्टियों के लिए परिवार के मैचिंग कपड़े खरीदें
वसंत के आयोजनों के लिए मैचिंग ड्रेस देखें
नए पायजामे देखें''',
'it':'''Acquista per categoria
Acquista per occasione
Spedizione standard inclusa
Look coordinati per i momenti in famiglia
Outfit facili da abbinare per foto, viaggi e feste
Aiuto nella scelta della taglia
Coordinare i look di famiglia è facile
Rispondiamo entro 1 giorno lavorativo
Mamma e io
Look coordinati per la famiglia
Pigiami
Abiti coordinati
Costumi da bagno
Papà e io
Vacanze
Giornate di foto
Compleanni
Giornate in spiaggia
I preferiti per mamma e figlia
Look coordinati per tutti
Completi morbidi per notti confortevoli
Abiti pronti per le foto
Costumi per le giornate in spiaggia
Momenti coordinati per papà e figli
Look da resort per tutto il viaggio
Pensati per i ritratti di famiglia
Dolci outfit per le feste
Stili coordinati pronti per il sole
I più amati
Preferito per le vacanze
Scelta per gli eventi primaverili
Nuovi pigiami
Acquista questo look
Acquista i nuovi pigiami
Acquista abiti da invitate a un matrimonio per mamma e figlia
Acquista outfit coordinati per le vacanze in famiglia
Scopri abiti coordinati per gli eventi primaverili
Scopri i nuovi pigiami''',
'ja':'''カテゴリーから探す
シーンから探す
通常配送料込み
家族のひとときにおそろいコーデ
写真撮影、旅行、お祝いに着やすいコーデ
サイズ選びをサポート
家族のおそろいコーデを手軽に
1営業日以内に返信
ママとおそろい
家族でおそろい
パジャマ
おそろいワンピース
水着
パパとおそろい
バケーション
写真撮影
誕生日
ビーチの日
ママと娘のお気に入り
みんなで楽しむおそろいコーデ
くつろぎの夜に柔らかなセット
写真映えするワンピース
ビーチで楽しむ水着コーデ
パパと子どものおそろい時間
旅の間ずっと楽しめるリゾートコーデ
家族写真のために
お祝いにぴったりのかわいいコーデ
晴れた日に楽しむおそろいスタイル
みんなのお気に入り
バケーションのお気に入り
春のイベントにおすすめ
新作パジャマ
このコーデを購入
新作パジャマを購入
ママと娘の結婚式お呼ばれワンピースを購入
家族でおそろいのバケーションコーデを購入
春のイベント向けおそろいワンピースを見る
新作パジャマを見る''',
'ko':'''카테고리별 쇼핑
상황별 쇼핑
일반 배송비 포함
가족의 순간을 위한 커플룩
사진 촬영, 여행, 기념일에 편하게 입는 옷
사이즈 선택 도움
쉽게 맞추는 패밀리룩
영업일 기준 1일 이내 답변
엄마와 나
패밀리룩
파자마
커플 원피스
수영복
아빠와 나
휴가
사진 촬영일
생일
해변 나들이
엄마와 딸의 인기 스타일
모두를 위한 맞춤 코디
포근한 밤을 위한 부드러운 세트
사진에 잘 어울리는 원피스
해변 나들이용 수영복 코디
아빠와 아이의 커플룩 순간
여행 내내 즐기는 리조트룩
가족사진을 위한 스타일
기념일을 위한 사랑스러운 옷
햇살 가득한 날의 커플 스타일
많이 사랑받는 스타일
휴가용 인기 스타일
봄 행사 추천
새로운 파자마
이 코디 쇼핑하기
새로운 파자마 쇼핑하기
엄마와 딸의 결혼식 하객 원피스 쇼핑하기
휴가용 패밀리룩 쇼핑하기
봄 행사용 커플 원피스 둘러보기
새로운 파자마 둘러보기''',
'nl':'''Shop op categorie
Shop op gelegenheid
Standaardverzending inbegrepen
Bijpassende looks voor familiemomenten
Makkelijke outfits voor foto's, reizen en feesten
Hulp bij het kiezen van de maat
Bijpassende gezinsoutfits, eenvoudig gemaakt
Antwoord binnen 1 werkdag
Mama en ik
Bijpassende gezinsoutfits
Pyjama's
Bijpassende jurken
Badkleding
Papa en ik
Vakantie
Fotodagen
Verjaardagen
Stranddagen
Favorieten voor moeder en dochter
Bijpassende looks voor iedereen
Zachte sets voor knusse nachten
Jurken klaar voor de foto
Zwemlooks voor stranddagen
Bijpassende momenten voor vader en kind
Resortlooks voor de hele reis
Gemaakt voor familieportretten
Lieve feestoutfits
Bijpassende stijlen voor zonnige dagen
Meest geliefd
Vakantiefavoriet
Keuze voor lente-evenementen
Nieuwe pyjama's
Shop deze look
Shop nieuwe pyjama's
Shop jurken voor moeder en dochter als bruiloftsgasten
Shop bijpassende gezinsoutfits voor de vakantie
Bekijk bijpassende jurken voor lente-evenementen
Bekijk de nieuwe pyjama's''',
'no':'''Handle etter kategori
Handle etter anledning
Standardfrakt er inkludert
Matchende antrekk for familiestunder
Enkle antrekk til bilder, reiser og feiringer
Hjelp med størrelser
Matchende familieantrekk gjort enkelt
Vi svarer innen 1 virkedag
Mamma og meg
Matchende familieantrekk
Pysjamaser
Matchende kjoler
Badetøy
Pappa og meg
Ferie
Fotodager
Bursdager
Stranddager
Favoritter til mor og datter
Samstemte antrekk til alle
Myke sett for koselige kvelder
Kjoler klare for bilder
Badetøy til stranddager
Matchende øyeblikk for far og barn
Ferieantrekk til hele reisen
Laget for familieportretter
Søte antrekk til feiringer
Matchende stiler for solfylte dager
Mest elsket
Feriefavoritt
Valg til vårens arrangementer
Nye pysjamaser
Kjøp dette antrekket
Kjøp nye pysjamaser
Kjøp kjoler til mor og datter som bryllupsgjester
Kjøp matchende familieantrekk til ferien
Se matchende kjoler til vårens arrangementer
Se de nye pysjamasene''',
'pl':'''Kupuj według kategorii
Kupuj według okazji
Standardowa dostawa w cenie
Dopasowane stroje na rodzinne chwile
Wygodne stylizacje do zdjęć, na wyjazdy i uroczystości
Pomoc w wyborze rozmiaru
Łatwe dopasowanie strojów dla rodziny
Odpowiadamy w ciągu 1 dnia roboczego
Mama i ja
Dopasowane stroje rodzinne
Piżamy
Dopasowane sukienki
Stroje kąpielowe
Tata i ja
Wakacje
Dni zdjęciowe
Urodziny
Dni na plaży
Ulubione modele dla mamy i córki
Dopasowane stylizacje dla każdego
Miękkie komplety na przytulne noce
Sukienki gotowe do zdjęć
Stroje kąpielowe na plażę
Wspólne chwile taty i dziecka w dopasowanych strojach
Stylizacje do kurortu na cały wyjazd
Stworzone do rodzinnych portretów
Urocze stroje na uroczystości
Dopasowane stylizacje na słoneczne dni
Najbardziej lubiane
Wakacyjny faworyt
Wybór na wiosenne wydarzenia
Nowe piżamy
Kup tę stylizację
Kup nowe piżamy
Kup sukienki dla mamy i córki na wesele
Kup dopasowane rodzinne stroje na wakacje
Zobacz dopasowane sukienki na wiosenne wydarzenia
Zobacz nowe piżamy''',
'pt-BR':'''Comprar por categoria
Comprar por ocasião
Frete padrão incluído
Looks combinando para momentos em família
Roupas práticas para fotos, viagens e comemorações
Ajuda para escolher o tamanho
Looks combinando em família sem complicação
Respondemos em até 1 dia útil
Mamãe e eu
Looks combinando em família
Pijamas
Vestidos combinando
Moda praia
Papai e eu
Férias
Dias de fotos
Aniversários
Dias de praia
Favoritos para mãe e filha
Looks coordenados para todos
Conjuntos macios para noites aconchegantes
Vestidos prontos para as fotos
Moda praia para dias à beira-mar
Momentos combinando entre pai e filho
Looks de resort para toda a viagem
Feitos para retratos de família
Roupas encantadoras para comemorar
Estilos combinando para dias de sol
Mais amados
Favorito para as férias
Escolha para eventos de primavera
Novos pijamas
Comprar este look
Comprar novos pijamas
Comprar vestidos para mãe e filha como convidadas de casamento
Comprar looks combinando para férias em família
Ver vestidos combinando para eventos de primavera
Ver os novos pijamas''',
'ro':'''Cumpără după categorie
Cumpără după ocazie
Livrare standard inclusă
Ținute asortate pentru momente în familie
Ținute ușor de purtat la fotografii, călătorii și sărbători
Ajutor pentru alegerea mărimii
Ținute asortate în familie, fără efort
Răspundem în termen de 1 zi lucrătoare
Mama și eu
Ținute asortate pentru familie
Pijamale
Rochii asortate
Costume de baie
Tata și eu
Vacanță
Zile de fotografii
Aniversări
Zile la plajă
Preferatele pentru mamă și fiică
Ținute coordonate pentru toți
Seturi moi pentru nopți confortabile
Rochii pregătite pentru fotografii
Ținute de baie pentru zile la plajă
Momente asortate pentru tată și copil
Ținute de vacanță pentru întreaga călătorie
Create pentru portrete de familie
Ținute drăgălașe pentru sărbători
Stiluri asortate pentru zile însorite
Cele mai îndrăgite
Favoritul vacanței
Alegere pentru evenimentele de primăvară
Pijamale noi
Cumpără această ținută
Cumpără pijamale noi
Cumpără rochii pentru mamă și fiică invitate la nuntă
Cumpără ținute asortate pentru vacanța în familie
Vezi rochii asortate pentru evenimentele de primăvară
Vezi noile pijamale''',
'ru':'''Покупки по категориям
Покупки по поводу
Стандартная доставка включена
Парные образы для семейных моментов
Удобные наряды для фотографий, поездок и праздников
Помощь с выбором размера
Семейные образы — это просто
Отвечаем в течение 1 рабочего дня
Мама и я
Семейные образы
Пижамы
Парные платья
Купальники
Папа и я
Отпуск
Фотосессии
Дни рождения
Дни на пляже
Любимые модели для мамы и дочки
Сочетающиеся образы для всех
Мягкие комплекты для уютных ночей
Платья для красивых фотографий
Купальные образы для пляжа
Парные образы для папы и ребёнка
Курортные образы на всю поездку
Для семейных портретов
Милые наряды для праздников
Парные образы для солнечных дней
Самые любимые
Любимый выбор для отпуска
Выбор для весенних мероприятий
Новые пижамы
Купить этот образ
Купить новые пижамы
Купить платья для мамы и дочки на свадьбу в качестве гостей
Купить парные семейные наряды для отпуска
Посмотреть парные платья для весенних мероприятий
Посмотреть новые пижамы''',
'sv':'''Handla efter kategori
Handla efter tillfälle
Standardfrakt ingår
Matchande kläder för familjestunder
Enkla outfits för foton, resor och firanden
Hjälp med storlekar
Matchande familjekläder på ett enkelt sätt
Vi svarar inom 1 arbetsdag
Mamma och jag
Matchande familjekläder
Pyjamasar
Matchande klänningar
Badkläder
Pappa och jag
Semester
Fotodagar
Födelsedagar
Stranddagar
Favoriter för mamma och dotter
Samordnade outfits för alla
Mjuka set för mysiga kvällar
Klänningar redo för foton
Badkläder för stranddagar
Matchande stunder för pappa och barn
Semesterkläder för hela resan
För familjeporträtt
Söta kläder för firanden
Matchande stilar för soliga dagar
Mest älskade
Semesterfavorit
Val för vårens evenemang
Nya pyjamasar
Köp den här looken
Köp nya pyjamasar
Köp klänningar för mamma och dotter som bröllopsgäster
Köp matchande familjekläder för semestern
Se matchande klänningar för vårens evenemang
Se de nya pyjamasarna'''
}
for l,s in values.items():
 v=s.splitlines();assert len(v)==len(keys),(l,len(v));rows[l]=dict(zip(keys,v))
for l,v in {'es':'Envío estándar incluido','fr':'Livraison standard incluse','de':'Standardversand inklusive','da':'Standardfragt inkluderet'}.items():rows[l]['trust-free-shipping']=v
assert len(rows)==21
(P/'home_category_translations.json').write_text(json.dumps({l:{'sections.home_category_copy.'+k.replace('-','_'):v for k,v in a.items()} for l,a in rows.items()},ensure_ascii=False,indent=2)+'\n')
print('home translation matrix',len(rows),'locales',len(keys),'keys')
