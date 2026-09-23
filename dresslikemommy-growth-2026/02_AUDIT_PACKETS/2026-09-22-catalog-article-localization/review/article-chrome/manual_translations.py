"""Manually authored article UI translations, in explicit source-key order."""
KEYS = '''breadcrumbs_label author_credential contents_label contents_aria_label recommended_products written_by author_bio shop_look compare_title compare_body continue_reading more_from inline_cta_text inline_cta_label shop_collection shop_collections build_look guide_caption read_before_shop view_all_guides'''.split()
COPY = {}
def add(locale, text):
    values=text.strip().splitlines()
    assert len(values)==len(KEYS),(locale,len(values))
    COPY[locale]=dict(zip(KEYS,values))
add('en.default', '''breadcrumbs
Family Fashion Editor
In this article
Table of contents
Recommended products from this guide
Written by
Dress Like Mommy's editorial team builds practical shopping guides for family matching outfits, mommy and me looks, daddy and me outfits, swimwear, pajamas, and photo-ready seasonal styles.
Shop the look
Ready to compare matching outfits?
Browse the core collections for mommy and me outfits, daddy and me styles, family matching sets, and vacation-ready swimwear.
Continue reading
More from {{ journal }}
Ready to shop the looks from this guide?
Shop matching collections
Shop the collection
Shop the collections
Build the look from this guide
Read {{ title }} before you shop.
Read the guide before you shop
View all guides''')
add('ar', '''مسار التنقل
محرّر أزياء الأسرة
في هذا المقال
جدول المحتويات
منتجات موصى بها من هذا الدليل
بقلم
يُعدّ فريق التحرير في Dress Like Mommy أدلة تسوّق عملية للإطلالات العائلية المتناسقة، وأزياء الأم وطفلها، وأزياء الأب وطفله، وملابس السباحة، والبيجامات، والإطلالات الموسمية المناسبة للتصوير.
تسوّق الإطلالة
هل أنت مستعد لمقارنة الإطلالات المتناسقة؟
تصفّح المجموعات الأساسية لأزياء الأم وطفلها، وأزياء الأب وطفله، والأطقم العائلية المتناسقة، وملابس السباحة المناسبة للعطلات.
تابع القراءة
المزيد من {{ journal }}
هل أنت مستعد لتسوّق الإطلالات الواردة في هذا الدليل؟
تسوّق مجموعات الأزياء المتناسقة
تسوّق المجموعة
تسوّق المجموعات
نسّق إطلالتك من هذا الدليل
اقرأ {{ title }} قبل التسوّق.
اقرأ الدليل قبل التسوّق
عرض جميع الأدلة''')
add('cs', '''Drobečková navigace
Redaktor rodinné módy
V tomto článku
Obsah článku
Doporučené produkty z tohoto průvodce
Autor článku
Redakce Dress Like Mommy připravuje praktické nákupní průvodce sladěnými rodinnými outfity, oblečením pro maminky a děti, oblečením pro tatínky a děti, plavkami, pyžamy a sezónními styly vhodnými na focení.
Nakupujte tento styl
Chcete porovnat sladěné outfity?
Prohlédněte si hlavní kolekce oblečení pro maminky a děti, stylů pro tatínky a děti, sladěných rodinných souprav a plavek na dovolenou.
Pokračovat ve čtení
Další články: {{ journal }}
Chcete nakupovat outfity z tohoto průvodce?
Prohlédnout sladěné kolekce
Prohlédnout kolekci
Prohlédnout kolekce
Sestavte si outfit podle tohoto průvodce
Před nákupem si přečtěte {{ title }}.
Před nákupem si přečtěte průvodce
Zobrazit všechny průvodce''')
add('da', '''Brødkrummenavigation
Redaktør for familiemode
I denne artikel
Indholdsfortegnelse
Anbefalede produkter fra denne guide
Skrevet af
Redaktionen hos Dress Like Mommy laver praktiske shoppingguider til matchende familietøj, mor og barn-looks, far og barn-outfits, badetøj, pyjamasser og sæsonens styles til fotografering.
Shop looket
Klar til at sammenligne matchende outfits?
Se de vigtigste kollektioner med mor og barn-outfits, far og barn-styles, matchende familiesæt og badetøj til ferien.
Læs videre
Mere fra {{ journal }}
Klar til at shoppe lookene fra denne guide?
Se matchende kollektioner
Se kollektionen
Se kollektionerne
Skab looket fra denne guide
Læs {{ title }}, før du shopper.
Læs guiden, før du shopper
Se alle guider''')
add('de', '''Brotkrümelnavigation
Redakteur für Familienmode
In diesem Artikel
Inhaltsverzeichnis
Empfohlene Produkte aus diesem Ratgeber
Geschrieben von
Das Redaktionsteam von Dress Like Mommy erstellt praktische Einkaufsratgeber für Familienoutfits im Partnerlook, Looks für Mama und Kind, Outfits für Papa und Kind, Bademode, Schlafanzüge und saisonale Styles für Fotos.
Den Look shoppen
Bereit, Outfits im Partnerlook zu vergleichen?
Entdecken Sie die wichtigsten Kollektionen mit Outfits für Mama und Kind, Styles für Papa und Kind, aufeinander abgestimmten Familiensets und Bademode für den Urlaub.
Weiterlesen
Weitere Artikel: {{ journal }}
Bereit, die Looks aus diesem Ratgeber zu shoppen?
Partnerlook-Kollektionen entdecken
Die Kollektion entdecken
Die Kollektionen entdecken
Den Look aus diesem Ratgeber zusammenstellen
Lesen Sie vor dem Einkauf {{ title }}.
Lesen Sie den Ratgeber vor dem Einkauf
Alle Ratgeber ansehen''')
add('el', '''Διαδρομή πλοήγησης
Συντάκτης οικογενειακής μόδας
Σε αυτό το άρθρο
Πίνακας περιεχομένων
Προτεινόμενα προϊόντα από αυτόν τον οδηγό
Συντάχθηκε από
Η συντακτική ομάδα του Dress Like Mommy δημιουργεί πρακτικούς οδηγούς αγορών για ασορτί οικογενειακά σύνολα, εμφανίσεις για μαμά και παιδί, σύνολα για μπαμπά και παιδί, μαγιό, πιτζάμες και εποχιακά στιλ κατάλληλα για φωτογραφίες.
Αγοράστε την εμφάνιση
Είστε έτοιμοι να συγκρίνετε ασορτί σύνολα;
Περιηγηθείτε στις βασικές συλλογές με σύνολα για μαμά και παιδί, στιλ για μπαμπά και παιδί, ασορτί οικογενειακά σετ και μαγιό για διακοπές.
Συνεχίστε την ανάγνωση
Περισσότερα από το {{ journal }}
Είστε έτοιμοι να αγοράσετε τις εμφανίσεις αυτού του οδηγού;
Δείτε τις ασορτί συλλογές
Δείτε τη συλλογή
Δείτε τις συλλογές
Δημιουργήστε την εμφάνιση αυτού του οδηγού
Διαβάστε το {{ title }} πριν ψωνίσετε.
Διαβάστε τον οδηγό πριν ψωνίσετε
Δείτε όλους τους οδηγούς''')
add('es', '''Ruta de navegación
Editor de moda familiar
En este artículo
Índice
Productos recomendados de esta guía
Escrito por
El equipo editorial de Dress Like Mommy crea guías de compra prácticas sobre conjuntos a juego para la familia, looks para mamá e hijos, conjuntos para papá e hijos, ropa de baño, pijamas y estilos de temporada ideales para las fotos.
Compra el look
¿Quieres comparar conjuntos a juego?
Explora las colecciones principales de conjuntos para mamá e hijos, estilos para papá e hijos, conjuntos familiares a juego y ropa de baño para las vacaciones.
Sigue leyendo
Más de {{ journal }}
¿Quieres comprar los looks de esta guía?
Explora las colecciones a juego
Explora la colección
Explora las colecciones
Crea el look de esta guía
Lee {{ title }} antes de comprar.
Lee la guía antes de comprar
Ver todas las guías''')
add('fi', '''Murupolku
Perhemuodin toimittaja
Tässä artikkelissa
Sisällysluettelo
Tämän oppaan suositellut tuotteet
Kirjoittaja
Dress Like Mommyn toimitus laatii käytännöllisiä ostosoppaita koko perheen yhteensopivista asuista, äidin ja lapsen tyyleistä, isän ja lapsen asuista, uima-asuista, pyjamista ja kuvauksiin sopivista kausityyleistä.
Osta tämä tyyli
Haluatko vertailla yhteensopivia asuja?
Tutustu keskeisiin mallistoihin: äidin ja lapsen asut, isän ja lapsen tyylit, koko perheen yhteensopivat asusetit ja lomalle sopivat uima-asut.
Jatka lukemista
Lisää julkaisusta {{ journal }}
Haluatko ostaa tämän oppaan asuja?
Tutustu yhteensopiviin mallistoihin
Tutustu mallistoon
Tutustu mallistoihin
Kokoa tämän oppaan tyyli
Lue {{ title }} ennen ostoksia.
Lue opas ennen ostoksia
Katso kaikki oppaat''')
add('fr', '''Fil d’Ariane
Rédacteur mode familiale
Dans cet article
Sommaire
Produits recommandés dans ce guide
Rédigé par
L’équipe éditoriale de Dress Like Mommy crée des guides d’achat pratiques sur les tenues familiales assorties, les looks maman-enfant, les tenues papa-enfant, les maillots de bain, les pyjamas et les styles de saison adaptés aux séances photo.
Acheter ce look
Prêt à comparer des tenues assorties ?
Parcourez les principales collections de tenues maman-enfant, de styles papa-enfant, d’ensembles familiaux assortis et de maillots de bain pour les vacances.
Poursuivre la lecture
Autres articles : {{ journal }}
Prêt à acheter les looks de ce guide ?
Découvrir les collections assorties
Découvrir la collection
Découvrir les collections
Composer le look de ce guide
Lisez {{ title }} avant de faire vos achats.
Lisez le guide avant de faire vos achats
Voir tous les guides''')
add('he', '''נתיב ניווט
עורך אופנת המשפחה
במאמר הזה
תוכן העניינים
מוצרים מומלצים מהמדריך הזה
נכתב על ידי
צוות העריכה של Dress Like Mommy יוצר מדריכי קנייה שימושיים לתלבושות משפחתיות תואמות, למראה מתואם לאמא ולילדים, לתלבושות לאבא ולילדים, לבגדי ים, לפיג׳מות ולסגנונות עונתיים שמתאימים לצילומים.
קנו את פריטי הלבוש
רוצים להשוות תלבושות תואמות?
עיינו בקולקציות המרכזיות של תלבושות לאמא ולילדים, סגנונות לאבא ולילדים, סטים משפחתיים תואמים ובגדי ים לחופשה.
המשך קריאה
עוד מתוך {{ journal }}
רוצים לקנות את התלבושות מהמדריך הזה?
גלו קולקציות תואמות
גלו את הקולקציה
גלו את הקולקציות
הרכיבו את התלבושת מהמדריך הזה
קראו את {{ title }} לפני הקנייה.
קראו את המדריך לפני הקנייה
לכל המדריכים''')
add('hi', '''नेविगेशन पथ
परिवार के फ़ैशन संपादक
इस लेख में
विषय-सूची
इस गाइड के सुझाए गए उत्पाद
लेखक
Dress Like Mommy की संपादकीय टीम परिवार के मैचिंग कपड़ों, माँ और बच्चों के लुक, पिता और बच्चों के कपड़ों, स्विमवियर, पजामों और तस्वीरों के लिए उपयुक्त मौसमी स्टाइल के लिए व्यावहारिक शॉपिंग गाइड तैयार करती है।
यह लुक खरीदें
क्या आप मैचिंग कपड़ों की तुलना करना चाहते हैं?
माँ और बच्चों के कपड़ों, पिता और बच्चों के स्टाइल, परिवार के मैचिंग सेट और छुट्टियों के लिए स्विमवियर के मुख्य कलेक्शन देखें।
आगे पढ़ें
{{ journal }} से और लेख
क्या आप इस गाइड के लुक खरीदना चाहते हैं?
मैचिंग कलेक्शन देखें
कलेक्शन देखें
कलेक्शन देखें
इस गाइड का लुक तैयार करें
खरीदारी से पहले {{ title }} पढ़ें।
खरीदारी से पहले गाइड पढ़ें
सभी गाइड देखें''')
add('it', '''Percorso di navigazione
Redattore di moda per la famiglia
In questo articolo
Indice
Prodotti consigliati in questa guida
Scritto da
La redazione di Dress Like Mommy crea guide pratiche all’acquisto di outfit coordinati per la famiglia, look mamma e bambino, outfit papà e bambino, costumi da bagno, pigiami e stili stagionali adatti alle foto.
Acquista il look
Vuoi confrontare gli outfit coordinati?
Esplora le collezioni principali di outfit mamma e bambino, stili papà e bambino, completi coordinati per la famiglia e costumi da bagno per le vacanze.
Continua a leggere
Altri articoli da {{ journal }}
Vuoi acquistare i look di questa guida?
Scopri le collezioni coordinate
Scopri la collezione
Scopri le collezioni
Crea il look di questa guida
Leggi {{ title }} prima di fare acquisti.
Leggi la guida prima di fare acquisti
Vedi tutte le guide''')
add('ja', '''パンくずリスト
ファミリーファッション編集者
この記事の内容
目次
このガイドのおすすめ商品
執筆者
Dress Like Mommyの編集チームは、家族のおそろいコーデ、ママと子どものコーデ、パパと子どものコーデ、水着、パジャマ、写真撮影にぴったりの季節のスタイルについて、実用的なお買い物ガイドを作成しています。
このコーデを購入
おそろいコーデを比べてみませんか？
ママと子どものコーデ、パパと子どものスタイル、家族のおそろいセット、バカンス向け水着の主要コレクションをご覧ください。
続きを読む
{{ journal }}の他の記事
このガイドのコーデを購入しませんか？
おそろいコレクションを見る
コレクションを見る
コレクション一覧を見る
このガイドのコーデを組み合わせる
お買い物の前に「{{ title }}」をお読みください。
お買い物の前にガイドを読む
すべてのガイドを見る''')
add('ko', '''탐색 경로
패밀리 패션 에디터
이 글의 내용
목차
이 가이드의 추천 상품
작성자
Dress Like Mommy 편집팀은 가족 시밀러룩, 엄마와 아이의 스타일, 아빠와 아이의 의상, 수영복, 잠옷, 사진 촬영에 어울리는 계절별 스타일을 위한 실용적인 쇼핑 가이드를 만듭니다.
이 스타일 쇼핑하기
시밀러룩을 비교해 보시겠어요?
엄마와 아이의 의상, 아빠와 아이의 스타일, 가족 시밀러룩 세트, 휴가용 수영복의 주요 컬렉션을 둘러보세요.
계속 읽기
{{ journal }}의 다른 글
이 가이드의 스타일을 쇼핑해 보시겠어요?
시밀러룩 컬렉션 보기
컬렉션 보기
컬렉션 둘러보기
이 가이드의 스타일 완성하기
쇼핑하기 전에 {{ title }} 가이드를 읽어 보세요.
쇼핑하기 전에 가이드 읽기
모든 가이드 보기''')
add('nl', '''Broodkruimelpad
Redacteur gezinsmode
In dit artikel
Inhoudsopgave
Aanbevolen producten uit deze gids
Geschreven door
De redactie van Dress Like Mommy maakt praktische koopgidsen voor bijpassende gezinsoutfits, looks voor moeder en kind, outfits voor vader en kind, badmode, pyjama’s en seizoensstijlen die geschikt zijn voor foto’s.
Shop de look
Klaar om bijpassende outfits te vergelijken?
Bekijk de belangrijkste collecties met outfits voor moeder en kind, stijlen voor vader en kind, bijpassende gezinssets en badmode voor op vakantie.
Verder lezen
Meer uit {{ journal }}
Klaar om de looks uit deze gids te shoppen?
Bekijk bijpassende collecties
Bekijk de collectie
Bekijk de collecties
Stel de look uit deze gids samen
Lees {{ title }} voordat je gaat shoppen.
Lees de gids voordat je gaat shoppen
Bekijk alle gidsen''')
add('no', '''Brødsmulenavigasjon
Redaktør for familiemote
I denne artikkelen
Innholdsfortegnelse
Anbefalte produkter fra denne guiden
Skrevet av
Redaksjonen i Dress Like Mommy lager praktiske handleguider for matchende familieantrekk, stiler for mor og barn, antrekk for far og barn, badetøy, pysjamaser og sesongens stiler som passer til fotografering.
Handle stilen
Klar til å sammenligne matchende antrekk?
Se hovedkolleksjonene med antrekk for mor og barn, stiler for far og barn, matchende familiesett og badetøy til ferien.
Les videre
Mer fra {{ journal }}
Klar til å handle stilene fra denne guiden?
Se matchende kolleksjoner
Se kolleksjonen
Se kolleksjonene
Sett sammen stilen fra denne guiden
Les {{ title }} før du handler.
Les guiden før du handler
Se alle guider''')
add('pl', '''Ścieżka nawigacji
Redaktor mody rodzinnej
W tym artykule
Spis treści
Produkty polecane w tym poradniku
Autor tekstu
Redakcja Dress Like Mommy tworzy praktyczne poradniki zakupowe dotyczące dopasowanych strojów rodzinnych, stylizacji dla mamy i dziecka, strojów dla taty i dziecka, strojów kąpielowych, piżam i sezonowych stylizacji odpowiednich do zdjęć.
Kup tę stylizację
Chcesz porównać dopasowane stroje?
Przejrzyj główne kolekcje strojów dla mamy i dziecka, stylizacji dla taty i dziecka, dopasowanych zestawów rodzinnych i strojów kąpielowych na wakacje.
Czytaj dalej
Więcej artykułów: {{ journal }}
Chcesz kupić stylizacje z tego poradnika?
Zobacz dopasowane kolekcje
Zobacz kolekcję
Zobacz kolekcje
Stwórz stylizację z tego poradnika
Przed zakupem przeczytaj {{ title }}.
Przed zakupem przeczytaj poradnik
Zobacz wszystkie poradniki''')
add('pt-BR', '''Caminho de navegação
Editor de moda para a família
Neste artigo
Índice
Produtos recomendados neste guia
Escrito por
A equipe editorial da Dress Like Mommy cria guias práticos de compras sobre looks combinando para a família, looks de mãe e filhos, roupas de pai e filhos, moda praia, pijamas e estilos da estação adequados para fotos.
Compre o look
Quer comparar looks combinando?
Explore as principais coleções de roupas de mãe e filhos, estilos de pai e filhos, conjuntos combinando para a família e moda praia para as férias.
Continue lendo
Mais de {{ journal }}
Quer comprar os looks deste guia?
Explore as coleções combinando
Explore a coleção
Explore as coleções
Monte o look deste guia
Leia {{ title }} antes de comprar.
Leia o guia antes de comprar
Ver todos os guias''')
add('ro', '''Traseu de navigare
Redactor de modă pentru familie
În acest articol
Cuprins
Produse recomandate în acest ghid
Scris de
Echipa editorială Dress Like Mommy creează ghiduri practice de cumpărături pentru ținute asortate de familie, stiluri pentru mamă și copil, ținute pentru tată și copil, costume de baie, pijamale și stiluri de sezon potrivite pentru fotografii.
Cumpără această ținută
Vrei să compari ținute asortate?
Explorează colecțiile principale de ținute pentru mamă și copil, stiluri pentru tată și copil, seturi asortate de familie și costume de baie pentru vacanță.
Continuă lectura
Mai multe din {{ journal }}
Vrei să cumperi ținutele din acest ghid?
Descoperă colecțiile asortate
Descoperă colecția
Descoperă colecțiile
Creează ținuta din acest ghid
Citește {{ title }} înainte de cumpărături.
Citește ghidul înainte de cumpărături
Vezi toate ghidurile''')
add('ru', '''Навигационная цепочка
Редактор семейной моды
В этой статье
Содержание
Рекомендуемые товары из этого руководства
Автор
Редакция Dress Like Mommy составляет практические руководства по выбору семейных комплектов в едином стиле, образов для мамы и ребёнка, нарядов для папы и ребёнка, купальников, пижам и сезонных образов для фотосъёмок.
Купить этот образ
Хотите сравнить наряды в едином стиле?
Посмотрите основные коллекции нарядов для мамы и ребёнка, образов для папы и ребёнка, семейных комплектов в едином стиле и купальников для отпуска.
Читать дальше
Другие статьи: {{ journal }}
Хотите купить наряды из этого руководства?
Посмотреть коллекции в едином стиле
Посмотреть коллекцию
Посмотреть коллекции
Создайте образ из этого руководства
Перед покупкой прочитайте {{ title }}.
Прочитайте руководство перед покупкой
Посмотреть все руководства''')
add('sv', '''Brödsmulenavigering
Redaktör för familjemode
I den här artikeln
Innehållsförteckning
Rekommenderade produkter från den här guiden
Skriven av
Redaktionen på Dress Like Mommy tar fram praktiska shoppingguider för matchande familjekläder, stilar för mamma och barn, kläder för pappa och barn, badkläder, pyjamasar och säsongens stilar som passar för fotografering.
Shoppa stilen
Vill du jämföra matchande kläder?
Utforska de viktigaste kollektionerna med kläder för mamma och barn, stilar för pappa och barn, matchande familjeset och badkläder för semestern.
Läs vidare
Mer från {{ journal }}
Vill du shoppa stilarna från den här guiden?
Se matchande kollektioner
Se kollektionen
Se kollektionerna
Skapa stilen från den här guiden
Läs {{ title }} innan du handlar.
Läs guiden innan du handlar
Se alla guider''')
assert len(COPY)==21
if __name__ == '__main__':
    import json
    print(json.dumps(COPY,ensure_ascii=False,indent=2))
