TEXT={}
# Exact repeated source table-label templates; source unit spellings are retained.
H={
'es':['Talla','Edad','Peso','Estatura','Pecho/busto','Manga o falda','Pantalón/shorts o -','Cadera','Cintura','Largo de la prenda'],
'fr':['Taille','Âge','Poids','Stature','Poitrine/buste','Manche ou jupe','Pantalon/short ou -','Hanches','Taille','Longueur du vêtement'],
'it':['Taglia','Età','Peso','Altezza','Petto/busto','Manica o gonna','Pantalone/shorts o -','Fianchi','Vita','Lunghezza del capo'],
'nl':['Maat','Leeftijd','Gewicht','Lichaamslengte','Borst/buste','Mouw of rok','Broek/short of -','Heup','Taille','Kledinglengte'],
'pl':['Rozmiar','Wiek','Masa ciała','Wzrost','Klatka piersiowa/biust','Rękaw lub spódnica','Spodnie/szorty lub -','Biodra','Talia','Długość odzieży'],
'pt-BR':['Tamanho','Idade','Peso','Altura','Peito/busto','Manga ou saia','Calça/shorts ou -','Quadril','Cintura','Comprimento da peça']}
def headers(l,weight=True):
 a=H[l];return a[:2]+[a[2]+(' (kg/lbs)' if weight else '')]+[x+' (cm/in)' for x in a[3:]]
TEXT[216,'es']=[
'Tejido:','Crochet ligero de punto abierto, con una sensación aireada de prenda para cubrir el bañador; la composición exacta de fibras no era visible en la página bloqueada del proveedor.',
'Estilo en familia:','Un conjunto de playa coordinado para mamá e hija, pensado para vacaciones cálidas, mañanas en el resort y fotos a juego bajo el sol.',
'Estampado:','Crochet aporta un estilo sencillo y costero con un dibujo calado de textura marcada en negro, blanco, naranja, albaricoque o verde.',
'Detalles del diseño:','Diseño sin mangas con escote en V, textura de punto abierto, detalle de canalé en la cintura y silueta de falda a juego tanto para mamá como para hija.',
'Cuidados:','Lavar a mano con agua fría, devolver suavemente la forma, secar en plano a la sombra y evitar la lejía o las superficies ásperas junto a la piscina.',
'Rango de tallas:','Niñas: Infantil 6-8 años a Infantil 10-12 años; Madre S a Madre XL.',
'Guía de tallas - Conjunto para cubrir el bañador']+headers('es',False)+[
'El conjunto de crochet para mamá e hija aporta un toque cuidado a los conjuntos de playa a juego. El top sin mangas de punto abierto y la falda dan al conjunto un aire ligero de resort, manteniendo un aspecto suave, sencillo y fácil de fotografiar.',
'Úsalo sobre el bañador para pasear por la playa, desayunar en el resort y hacer retratos de vacaciones, o combínalo con sandalias y accesorios tejidos para salidas familiares con buen tiempo. El rango respaldado por la tabla abarca tres tallas de niña y cuatro de madre, y cada variante corresponde a una fila de la tabla adjunta.',
'Características principales:','Textura de crochet de punto abierto:','El dibujo aireado aporta al conjunto su estilo costero para cubrir el bañador.',
'Mamá e hija a juego:','El mismo diseño con textura en las tallas de niña y de madre.',
'Silueta lista para la playa:','Top sin mangas con escote en V y parte inferior de tipo falda, como se muestran en la imagen del producto facilitada.',
'Tallas respaldadas por la tabla:','Las tallas de niña utilizan orientaciones de edad, estatura, busto, cintura y largo; las de madre utilizan busto, cadera y largo.',
'Cinco colores para elegir:','Elige negro, blanco, naranja, albaricoque o verde para el mismo conjunto de playa respaldado por la tabla.',
'Elige cada talla y lleva en la maleta un sencillo look de playa a juego para vuestro próximo recuerdo familiar bajo el sol.'
]
TEXT[216,'fr']=[
'Tissu :','Crochet léger à mailles ajourées, au toucher aérien d’une tenue à porter sur le maillot ; la composition exacte des fibres n’était pas visible sur la page bloquée du fournisseur.',
'En famille :','Un ensemble de plage coordonné pour mère et fille, conçu pour les vacances au soleil, les matinées au complexe hôtelier et les photos assorties par beau temps.',
'Motif :','Crochet offre un style sobre et côtier grâce à un motif ajouré texturé en noir, blanc, orange, abricot ou vert.',
'Détails du modèle :','Coupe sans manches à encolure en V, texture à mailles ajourées, détail côtelé à la taille et silhouette de jupe assortie pour la mère comme pour la fille.',
'Entretien :','Laver à la main à l’eau froide, remettre délicatement en forme, sécher à plat à l’ombre et éviter l’eau de Javel ou les surfaces rugueuses au bord de la piscine.',
'Gamme de tailles :','Filles : Enfant 6-8 ans à Enfant 10-12 ans ; Mère S à Mère XL.',
'Guide des tailles - Ensemble de plage à porter sur le maillot']+headers('fr',False)+[
'L’ensemble en crochet pour mère et fille apporte une touche soignée aux tenues de plage assorties. Le haut sans manches à mailles ajourées et la jupe créent une allure légère de vacances, tout en gardant un style doux, simple et facile à photographier.',
'Portez-le sur un maillot pour les promenades sur la plage, les petits-déjeuners au complexe hôtelier et les portraits de vacances, ou associez-le à des sandales et à des accessoires tissés pour les sorties en famille par beau temps. La gamme appuyée par le tableau couvre trois tailles pour filles et quatre pour mères, chaque variante correspondant à une ligne du tableau joint.',
'Caractéristiques principales :','Texture de crochet à mailles ajourées :','Le motif aérien donne à l’ensemble son allure côtière de tenue à porter sur le maillot.',
'Mère et fille assorties :','Le même style texturé dans les tailles pour filles et pour mères.',
'Silhouette de plage :','Haut sans manches à encolure en V et bas de type jupe présentés sur l’image du produit fournie.',
'Tailles appuyées par le tableau :','Les tailles pour filles utilisent les indications d’âge, de stature, de buste, de taille et de longueur ; les tailles pour mères utilisent celles de buste, de hanches et de longueur.',
'Cinq couleurs au choix :','Choisissez noir, blanc, orange, abricot ou vert pour le même ensemble de plage appuyé par le tableau.',
'Choisissez chaque taille et glissez dans votre valise une tenue de plage sobre et assortie pour votre prochain souvenir de famille au soleil.'
]
TEXT[216,'it']=[
'Tessuto:','Crochet leggero a maglia aperta, con la sensazione ariosa di un copricostume; la composizione esatta delle fibre non era visibile nella pagina bloccata del fornitore.',
'Stile in famiglia:','Un completo da spiaggia coordinato per mamma e figlia, pensato per vacanze al caldo, mattine al resort e foto abbinate al sole.',
'Motivo:','Crochet mantiene uno stile essenziale e marino con un motivo traforato dalla texture evidente in nero, bianco, arancione, albicocca o verde.',
'Dettagli del modello:','Linea senza maniche con scollo a V, texture a maglia aperta, dettaglio a coste in vita e silhouette con gonna abbinata sia per mamma sia per figlia.',
'Cura:','Lavare a mano in acqua fredda, ridare delicatamente la forma, asciugare in piano all’ombra ed evitare candeggina o superfici ruvide a bordo piscina.',
'Gamma di taglie:','Bambine: Bambino 6-8 anni a Bambino 10-12 anni; Madre S a Madre XL.',
'Tabella taglie - Completo copricostume']+headers('it',False)+[
'Il completo in crochet per mamma e figlia aggiunge un tocco curato ai copricostume coordinati. Il top senza maniche a maglia aperta e la gonna donano all’outfit un’aria leggera da resort, mantenendo un aspetto morbido, semplice e facile da fotografare.',
'Indossalo sopra il costume per passeggiate in spiaggia, colazioni al resort e ritratti di vacanza, oppure abbinalo a sandali e accessori intrecciati per le uscite in famiglia nella bella stagione. La gamma supportata dalla tabella comprende tre taglie da bambina e quattro da madre, con ogni variante collegata a una riga della tabella allegata.',
'Caratteristiche principali:','Texture in crochet a maglia aperta:','Il motivo arioso conferisce al completo il suo stile marino da copricostume.',
'Mamma e figlia coordinate:','Lo stesso stile lavorato nelle taglie da bambina e da madre.',
'Silhouette pronta per la spiaggia:','Top senza maniche con scollo a V e parte inferiore a gonna mostrati nell’immagine del prodotto fornita.',
'Taglie supportate dalla tabella:','Le taglie da bambina utilizzano le indicazioni di età, altezza, busto, vita e lunghezza; quelle da madre utilizzano busto, fianchi e lunghezza.',
'Cinque colori a scelta:','Scegli nero, bianco, arancione, albicocca o verde per lo stesso completo copricostume supportato dalla tabella.',
'Scegli ogni taglia e metti in valigia un look da spiaggia semplice e coordinato per il prossimo ricordo di famiglia al sole.'
]
TEXT[216,'nl']=[
'Stof:','Licht, opengewerkt haakwerk met het luchtige gevoel van een strandoutfit voor over zwemkleding; de exacte vezelsamenstelling was niet zichtbaar op de geblokkeerde leverancierspagina.',
'Voor het gezin:','Een bijpassende strandset voor moeder en dochter, voor warme vakanties, ochtenden in het resort en zonnige foto’s in dezelfde stijl.',
'Print:','Crochet geeft een eenvoudige, kustgerichte look met een opengewerkt structuurpatroon in zwart, wit, oranje, abrikoos of groen.',
'Ontwerpdetails:','Mouwloos model met V-hals, opengewerkte structuur, een geribbeld tailledetail en een bijpassend roksilhouet voor zowel moeder als dochter.',
'Wasvoorschrift:','Koud met de hand wassen, voorzichtig in model brengen, plat in de schaduw drogen en bleekmiddel of ruwe oppervlakken bij het zwembad vermijden.',
'Maatbereik:','Meisjes: Kind 6-8 jaar tot Kind 10-12 jaar; Moeder S tot Moeder XL.',
'Maattabel - Strandset voor over zwemkleding']+headers('nl',False)+[
'De Crochet-set voor moeder en dochter geeft bijpassende strandkleding een verzorgde uitstraling. De mouwloze, opengewerkte top en de rok geven de outfit een luchtige resortlook, met een zachte, eenvoudige stijl die mooi op foto’s uitkomt.',
'Draag de set over zwemkleding voor strandwandelingen, ontbijt in het resort en vakantieportretten, of combineer hem met sandalen en geweven accessoires voor gezinsuitjes bij warm weer. Het maatbereik op basis van de tabel omvat drie meisjesmaten en vier moedermaten, waarbij elke variant gekoppeld is aan een rij in de bijgevoegde tabel.',
'Belangrijkste kenmerken:','Opengewerkte haakstructuur:','Het luchtige patroon geeft de set zijn kustlook als outfit voor over zwemkleding.',
'Moeder en dochter in dezelfde stijl:','Dezelfde structuurstijl in meisjes- en moedermaten.',
'Silhouet voor het strand:','Mouwloze top met V-hals en een rok als onderstuk, zoals getoond op de aangeleverde productafbeelding.',
'Maten op basis van de tabel:','Meisjesmaten gebruiken richtlijnen voor leeftijd, lichaamslengte, buste, taille en lengte; moedermaten gebruiken buste, heup en lengte.',
'Keuze uit vijf kleuren:','Kies zwart, wit, oranje, abrikoos of groen voor dezelfde strandset op basis van de maattabel.',
'Kies elke maat en pak een eenvoudige, bijpassende strandlook in voor jullie volgende zonnige familieherinnering.'
]
TEXT[216,'pl']=[
'Materiał:','Lekki, ażurowy szydełkowy splot o przewiewnym charakterze plażowego okrycia; dokładny skład włókien nie był widoczny na zablokowanej stronie dostawcy.',
'Rodzinny styl:','Pasujący komplet plażowy dla mamy i córki, stworzony na ciepłe wakacje, poranki w kurorcie i wspólne zdjęcia w słońcu.',
'Wzór:','Crochet zachowuje prosty, nadmorski styl dzięki ażurowemu wzorowi o wyrazistej fakturze w kolorze czarnym, białym, pomarańczowym, morelowym lub zielonym.',
'Szczegóły fasonu:','Fason bez rękawów z dekoltem V, ażurowa faktura, prążkowany detal w talii i pasujący fason spódnicy zarówno dla mamy, jak i córki.',
'Pielęgnacja:','Prać ręcznie w zimnej wodzie, delikatnie przywrócić kształt, suszyć na płasko w cieniu i unikać wybielacza oraz szorstkich powierzchni przy basenie.',
'Zakres rozmiarów:','Dziewczynki: Dziecko 6-8 lat do Dziecko 10-12 lat; Mama S do Mama XL.',
'Tabela rozmiarów - Komplet plażowy na strój kąpielowy']+headers('pl',False)+[
'Szydełkowy komplet dla mamy i córki dodaje eleganckiego akcentu pasującym okryciom plażowym. Ażurowy top bez rękawów i spódnica nadają strojowi lekki, wakacyjny charakter, zachowując delikatny, prosty wygląd, który dobrze prezentuje się na zdjęciach.',
'Noś go na stroju kąpielowym podczas spacerów po plaży, śniadań w kurorcie i wakacyjnych portretów albo połącz z sandałami i plecionymi dodatkami na rodzinne wyjścia w ciepłe dni. Zakres rozmiarów potwierdzony tabelą obejmuje trzy rozmiary dla dziewczynek i cztery dla mam, a każdy wariant odpowiada wierszowi w załączonej tabeli.',
'Najważniejsze cechy:','Ażurowa szydełkowa faktura:','Przewiewny wzór nadaje kompletowi nadmorski charakter okrycia plażowego.',
'Mama i córka w pasujących strojach:','Ta sama faktura i styl w rozmiarach dla dziewczynek i mam.',
'Fason na plażę:','Top bez rękawów z dekoltem V i dół w formie spódnicy, pokazane na dostarczonym zdjęciu produktu.',
'Rozmiary potwierdzone tabelą:','Rozmiary dla dziewczynek korzystają ze wskazówek dotyczących wieku, wzrostu, biustu, talii i długości; rozmiary dla mam — biustu, bioder i długości.',
'Pięć kolorów do wyboru:','Wybierz czarny, biały, pomarańczowy, morelowy lub zielony dla tego samego kompletu plażowego potwierdzonego tabelą.',
'Wybierz każdy rozmiar i spakuj prosty, pasujący strój plażowy na kolejne słoneczne rodzinne wspomnienia.'
]
TEXT[216,'pt-BR']=[
'Tecido:','Crochê leve de pontos abertos, com o toque arejado de uma saída de praia; a composição exata das fibras não estava visível na página bloqueada do fornecedor.',
'Estilo em família:','Um conjunto de praia coordenado para mãe e filha, feito para férias no calor, manhãs no resort e fotos combinando ao sol.',
'Estampa:','Crochet mantém o visual simples e litorâneo com um padrão vazado texturizado em preto, branco, laranja, damasco ou verde.',
'Detalhes do modelo:','Modelo sem mangas com decote em V, textura de pontos abertos, detalhe canelado na cintura e silhueta de saia combinando para mãe e filha.',
'Cuidados:','Lave à mão com água fria, remodele delicadamente, seque na horizontal à sombra e evite alvejante ou superfícies ásperas à beira da piscina.',
'Grade de tamanhos:','Meninas: Criança 6-8 anos a Criança 10-12 anos; Mãe S a Mãe XL.',
'Tabela de medidas - Conjunto de saída de praia']+headers('pt-BR',False)+[
'O conjunto de crochê para mãe e filha traz um toque arrumado às saídas de praia combinando. A blusa sem mangas de pontos abertos e a saia dão ao look um ar leve de resort, mantendo o visual suave, simples e fácil de fotografar.',
'Use sobre a roupa de banho em caminhadas na praia, cafés da manhã no resort e retratos de férias, ou combine com sandálias e acessórios trançados para passeios em família no calor. A grade respaldada pela tabela abrange três tamanhos de menina e quatro de mãe, com cada variante vinculada a uma linha da tabela em anexo.',
'Principais características:','Textura de crochê de pontos abertos:','O desenho arejado dá ao conjunto seu visual litorâneo de saída de praia.',
'Mãe e filha combinando:','O mesmo estilo texturizado nos tamanhos de menina e de mãe.',
'Silhueta pronta para a praia:','Blusa sem mangas com decote em V e parte de baixo em forma de saia mostradas na imagem fornecida do produto.',
'Tamanhos respaldados pela tabela:','Os tamanhos de menina usam orientações de idade, altura, busto, cintura e comprimento; os de mãe usam busto, quadril e comprimento.',
'Cinco opções de cores:','Escolha preto, branco, laranja, damasco ou verde para o mesmo conjunto de saída de praia respaldado pela tabela.',
'Escolha cada tamanho e leve na mala um visual de praia simples e coordenado para a próxima lembrança ensolarada em família.'
]
TEXT[219,'es']=[
'Tejido:','Tejido de vestido ligero con aspecto de tejido plano y tejido suave de camiseta; la composición exacta de fibras no era visible en la página bloqueada del proveedor.',
'Estilo en familia:','Un look coordinado en azul cielo para mamá, papá, niñas y niños, pensado para fotos de vacaciones y momentos familiares con buen tiempo.',
'Color:','Azul cielo suave con un delicado efecto degradado en los vestidos plisados y las camisetas a juego.',
'Detalles del diseño:','Las niñas y las madres llevan vestidos plisados sin mangas; los niños y los padres llevan camisetas de manga corta y cuello redondo. Los shorts no están incluidos.',
'Cuidados:','Lavar a mano con agua fría, secar tendido a la sombra y evitar la lejía o las temperaturas altas para proteger el suave color azul.',
'Rango de tallas:','Niñas y niños: Infantil 2 años a Infantil 9-10 años; Madre S a Madre 2XL; Padre M a Padre 3XL.',
'Guía de tallas - Vestido']+headers('es')+['Guía de tallas - Camiseta',
'El conjunto familiar a juego Sky Blue crea un look coordinado sencillo para padres e hijos. Los vestidos aportan una silueta plisada y ligera para las fotos de madre e hija, mientras las camisetas a juego mantienen a papá e hijo en la misma paleta azul suave.',
'Utiliza las indicaciones de estatura, peso, busto, cintura, manga y largo respaldadas por la tabla para elegir la talla de cada familiar. El anuncio incluye únicamente los vestidos y las camisetas respaldados por la guía adjunta; los shorts de la foto de estilo de vida se excluyen intencionadamente.',
'Características principales:','Toda la familia a juego:','Opciones de vestido para mamá y niñas, y de camiseta para papá y niños.',
'Paleta azul cielo:','Colores suaves pensados para fotos al sol, días de piscina y viajes a la playa.',
'Variantes respaldadas por la tabla:','Cada talla disponible procede de la tabla adjunta del proveedor.',
'Shorts no incluidos:','Las variantes que se pueden comprar son únicamente vestido y camiseta, de acuerdo con el alcance solicitado.',
'Coordinación lista para las fotos:','Fácil de combinar entre padres, hijas e hijos sin que todas las prendas tengan que ser exactamente iguales.',
'Elige las tallas de vestido y camiseta que necesitas para un look familiar azul cielo, listo para los días cálidos y las fotos de recuerdo.'
]
TEXT[219,'fr']=[
'Tissu :','Tissu de robe léger d’aspect tissé et tissu de T-shirt doux ; la composition exacte des fibres n’était pas visible sur la page bloquée du fournisseur.',
'En famille :','Un style coordonné bleu ciel pour maman, papa, filles et garçons, conçu pour les photos de vacances et les moments en famille par beau temps.',
'Couleur :','Un bleu ciel doux avec un léger effet dégradé sur les robes plissées et les T-shirts assortis.',
'Détails du modèle :','Les filles et les mères portent des robes plissées sans manches ; les garçons et les pères portent des T-shirts à manches courtes et col rond. Les shorts ne sont pas inclus.',
'Entretien :','Laver à la main à l’eau froide, sécher sur fil à l’ombre et éviter l’eau de Javel ou les températures élevées pour préserver le bleu doux.',
'Gamme de tailles :','Filles et garçons : Enfant 2 ans à Enfant 9-10 ans ; Mère S à Mère 2XL ; Père M à Père 3XL.',
'Guide des tailles - Robe']+headers('fr')+['Guide des tailles - T-shirt',
'L’ensemble familial assorti Sky Blue crée une tenue coordonnée facile à composer pour les parents et les enfants. Les robes apportent une silhouette plissée légère aux photos mère-fille, tandis que les T-shirts assortis gardent papa et fils dans la même palette bleu doux.',
'Utilisez les indications de stature, de poids, de buste, de taille, de manche et de longueur appuyées par le tableau pour choisir la taille de chaque membre de la famille. L’annonce comprend uniquement les robes et les T-shirts appuyés par le guide joint ; les shorts de la photo de mise en scène sont volontairement exclus.',
'Caractéristiques principales :','Toute la famille assortie :','Des robes pour maman et les filles, des T-shirts pour papa et les garçons.',
'Palette bleu ciel :','Des couleurs douces pensées pour les photos au soleil, les journées à la piscine et les séjours à la plage.',
'Variantes appuyées par le tableau :','Chaque taille disponible provient du tableau du fournisseur joint.',
'Shorts non inclus :','Les variantes achetables sont uniquement la robe et le T-shirt, conformément au périmètre demandé.',
'Coordination prête pour les photos :','Facile à combiner entre parents, filles et fils sans assortir chaque pièce à l’identique.',
'Choisissez les tailles de robe et de T-shirt nécessaires pour un style familial bleu ciel, prêt pour les journées chaudes et les photos souvenirs.'
]
TEXT[219,'it']=[
'Tessuto:','Tessuto leggero dall’aspetto intrecciato per gli abiti e tessuto morbido per le T-shirt; la composizione esatta delle fibre non era visibile nella pagina bloccata del fornitore.',
'Stile in famiglia:','Un look coordinato azzurro cielo per mamma, papà, bambine e bambini, pensato per foto di vacanza e momenti in famiglia nella bella stagione.',
'Colore:','Azzurro cielo tenue con un delicato effetto sfumato sugli abiti plissettati e sulle T-shirt abbinate.',
'Dettagli del modello:','Bambine e madri indossano abiti plissettati senza maniche; bambini e padri indossano magliette a maniche corte con girocollo. Gli shorts non sono inclusi.',
'Cura:','Lavare a mano in acqua fredda, asciugare appeso all’ombra ed evitare candeggina o calore elevato per proteggere il delicato colore azzurro.',
'Gamma di taglie:','Bambine e bambini: Bambino 2 anni a Bambino 9-10 anni; Madre S a Madre 2XL; Padre M a Padre 3XL.',
'Tabella taglie - Abito']+headers('it')+['Tabella taglie - Maglietta',
'Il coordinato familiare Sky Blue crea un look abbinato semplice da comporre per genitori e figli. Gli abiti offrono una linea plissettata leggera per le foto di mamma e figlia, mentre le magliette abbinate mantengono papà e figlio nella stessa delicata palette azzurra.',
'Usa le indicazioni di altezza, peso, busto, vita, manica e lunghezza supportate dalla tabella per scegliere la taglia di ogni familiare. L’inserzione comprende soltanto gli abiti e le magliette supportati dalla tabella allegata; gli shorts mostrati nella foto ambientata sono volutamente esclusi.',
'Caratteristiche principali:','Tutta la famiglia coordinata:','Opzioni di abito per mamma e bambine e di maglietta per papà e bambini.',
'Palette azzurro cielo:','Colori delicati pensati per foto al sole, giornate in piscina e gite al mare.',
'Varianti supportate dalla tabella:','Ogni taglia disponibile proviene dalla tabella allegata del fornitore.',
'Shorts non inclusi:','Le varianti acquistabili sono soltanto abito e maglietta, in linea con l’ambito richiesto.',
'Coordinazione pronta per le foto:','Facile da combinare tra genitori, figlie e figli senza rendere identico ogni capo.',
'Scegli le taglie di abito e maglietta che ti servono per un look familiare azzurro cielo, pronto per giornate calde e foto ricordo.'
]
TEXT[219,'nl']=[
'Stof:','Lichte jurkstof met een geweven uitstraling en zachte T-shirtstof; de exacte vezelsamenstelling was niet zichtbaar op de geblokkeerde leverancierspagina.',
'Voor het gezin:','Een bijpassende hemelsblauwe look voor moeder, vader, meisjes en jongens, voor vakantiefoto’s en gezinsmomenten bij warm weer.',
'Kleur:','Zacht hemelsblauw met een subtiel kleurverloop op de plooijurken en bijpassende T-shirts.',
'Ontwerpdetails:','Meisjes en moeders dragen mouwloze plooijurken; jongens en vaders dragen shirts met korte mouwen en een ronde hals. Shorts zijn niet inbegrepen.',
'Wasvoorschrift:','Koud met de hand wassen, aan de lijn in de schaduw drogen en bleekmiddel of hoge temperaturen vermijden om de zachte blauwe kleur te beschermen.',
'Maatbereik:','Meisjes en jongens: Kind 2 jaar tot Kind 9-10 jaar; Moeder S tot Moeder 2XL; Vader M tot Vader 3XL.',
'Maattabel - Jurk']+headers('nl')+['Maattabel - Shirt',
'De Sky Blue-familieset creëert een eenvoudige, bijpassende outfit voor ouders en kinderen. De jurken geven moeder-dochterfoto’s een luchtig geplooid silhouet, terwijl de bijpassende shirts vader en zoon in hetzelfde zachte blauwe kleurenpalet houden.',
'Gebruik de richtlijnen voor lichaamslengte, gewicht, buste, taille, mouw en lengte uit de tabel om de maat voor elk gezinslid te kiezen. De aanbieding bevat alleen de jurken en shirts die door de bijgevoegde maattabel worden ondersteund; de shorts op de sfeerfoto zijn bewust uitgesloten.',
'Belangrijkste kenmerken:','Het hele gezin in dezelfde stijl:','Jurkopties voor moeder en meisjes, shirtopties voor vader en jongens.',
'Hemelsblauw kleurenpalet:','Zachte kleuren voor zonnige foto’s, zwembaddagen en stranduitjes.',
'Varianten op basis van de maattabel:','Elke beschikbare maat komt uit de bijgevoegde tabel van de leverancier.',
'Geen shorts inbegrepen:','De koopbare varianten zijn uitsluitend de jurk en het shirt, overeenkomstig de gevraagde afbakening.',
'Bijpassende look voor foto’s:','Gemakkelijk te combineren tussen ouders, dochters en zonen zonder elk kledingstuk precies hetzelfde te maken.',
'Kies de jurk- en shirtmaten die je nodig hebt voor een hemelsblauwe familielook voor warme dagen en foto’s om te bewaren.'
]
TEXT[219,'pl']=[
'Materiał:','Lekki materiał sukienkowy o wyglądzie tkaniny i miękki materiał T-shirtowy; dokładny skład włókien nie był widoczny na zablokowanej stronie dostawcy.',
'Rodzinny styl:','Pasujący błękitny strój dla mamy, taty, dziewczynek i chłopców, stworzony na zdjęcia z wakacji i rodzinne chwile w ciepłe dni.',
'Kolor:','Delikatny błękit z łagodnym efektem przejścia koloru na plisowanych sukienkach i pasujących T-shirtach.',
'Szczegóły fasonu:','Dziewczynki i mamy noszą plisowane sukienki bez rękawów; chłopcy i ojcowie noszą koszulki z krótkim rękawem i okrągłym dekoltem. Szorty nie są wliczone.',
'Pielęgnacja:','Prać ręcznie w zimnej wodzie, suszyć rozwieszone w cieniu i unikać wybielacza oraz wysokiej temperatury, aby chronić delikatny błękit.',
'Zakres rozmiarów:','Dziewczynki i chłopcy: Dziecko 2 lata do Dziecko 9-10 lat; Mama S do Mama 2XL; Tata M do Tata 3XL.',
'Tabela rozmiarów - Sukienka']+headers('pl')+['Tabela rozmiarów - Koszulka',
'Rodzinny zestaw Sky Blue tworzy łatwy do skomponowania, pasujący strój dla rodziców i dzieci. Sukienki nadają zdjęciom mamy i córki lekką plisowaną formę, a pasujące koszulki utrzymują tatę i syna w tej samej delikatnej błękitnej palecie.',
'Korzystaj ze wskazówek dotyczących wzrostu, masy ciała, biustu, talii, rękawa i długości podanych w tabeli, aby wybrać rozmiar każdego członka rodziny. Oferta obejmuje wyłącznie sukienki i koszulki potwierdzone załączoną tabelą rozmiarów; szorty widoczne na zdjęciu stylizacyjnym zostały celowo wykluczone.',
'Najważniejsze cechy:','Pasujące stroje dla całej rodziny:','Sukienki dla mamy i dziewczynek, koszulki dla taty i chłopców.',
'Błękitna paleta:','Delikatne kolory stworzone na słoneczne zdjęcia, dni przy basenie i wyjazdy na plażę.',
'Warianty potwierdzone tabelą:','Każdy dostępny rozmiar pochodzi z załączonej tabeli dostawcy.',
'Bez szortów:','Do zakupu dostępne są wyłącznie warianty sukienki i koszulki, zgodnie z zamówionym zakresem.',
'Koordynacja gotowa do zdjęć:','Łatwe łączenie strojów rodziców, córek i synów bez konieczności idealnego dopasowywania każdej części.',
'Wybierz potrzebne rozmiary sukienek i koszulek, aby stworzyć błękitny rodzinny strój na ciepłe dni i pamiątkowe zdjęcia.'
]
TEXT[219,'pt-BR']=[
'Tecido:','Tecido leve para vestido com aparência de trama plana e tecido macio de camiseta; a composição exata das fibras não estava visível na página bloqueada do fornecedor.',
'Estilo em família:','Um visual coordenado azul-celeste para mãe, pai, meninas e meninos, feito para fotos de férias e momentos em família nos dias quentes.',
'Cor:','Azul-celeste suave com um delicado efeito degradê nos vestidos plissados e nas camisetas combinando.',
'Detalhes do modelo:','Meninas e mães usam vestidos plissados sem mangas; meninos e pais usam camisetas de manga curta com gola redonda. Shorts não estão incluídos.',
'Cuidados:','Lave à mão com água fria, seque no varal à sombra e evite alvejante ou calor elevado para proteger o azul suave.',
'Grade de tamanhos:','Meninas e meninos: Criança 2 anos a Criança 9-10 anos; Mãe S a Mãe 2XL; Pai M a Pai 3XL.',
'Tabela de medidas - Vestido']+headers('pt-BR')+['Tabela de medidas - Camiseta',
'O conjunto familiar Sky Blue cria uma proposta coordenada fácil de montar para pais e filhos. Os vestidos trazem uma silhueta plissada leve para as fotos de mãe e filha, enquanto as camisetas combinando mantêm pai e filho na mesma paleta azul suave.',
'Use as orientações de altura, peso, busto, cintura, manga e comprimento respaldadas pela tabela para escolher o tamanho de cada pessoa da família. O anúncio inclui somente os vestidos e as camisetas respaldados pela tabela em anexo; os shorts mostrados na foto de ambientação foram excluídos intencionalmente.',
'Principais características:','Toda a família combinando:','Opções de vestido para mãe e meninas, e de camiseta para pai e meninos.',
'Paleta azul-celeste:','Cores suaves feitas para fotos ao sol, dias na piscina e passeios na praia.',
'Variantes respaldadas pela tabela:','Cada tamanho disponível vem da tabela do fornecedor em anexo.',
'Shorts não incluídos:','As variantes disponíveis para compra são somente vestido e camiseta, de acordo com o escopo solicitado.',
'Coordenação pronta para as fotos:','Fácil de combinar entre pais, filhas e filhos sem deixar todas as peças exatamente iguais.',
'Escolha os tamanhos de vestido e camiseta de que precisa para um visual familiar azul-celeste, pronto para dias quentes e fotos de recordação.'
]
TEXT[220,'fr']=[
'Tissu et toucher :','Tissu léger tissé pour les beaux jours ; la composition exacte des fibres n’était pas visible dans les éléments fournis.',
'En famille :','Un style de plage lumineux et coordonné pour maman, papa, filles et garçons autour d’un même thème de marguerites jaunes.',
'Motif :','Un tissu jaune soleil brodé de marguerites blanches, à l’esprit doux de vacances.',
'Détails du modèle :','Les filles et les mamans portent la robe sans manches à encolure volantée ; les garçons et les papas portent la chemise boutonnée à manches courtes. Shorts, chapeaux, sacs, chaussures et accessoires servent uniquement à la mise en scène.',
'Entretien :','Laver en machine à l’eau froide sur cycle délicat, sécher sur fil, ne pas utiliser d’eau de Javel et, si nécessaire, repasser sur l’envers à basse température.',
'Gamme de tailles :','Enfant 2 ans à Enfant 9-10 ans, Mère S-3XL et Père M-4XL.',
'Guide des tailles - Robe']+headers('fr')+['Guide des tailles - Chemise',
'L’ensemble familial assorti Sunshine Daisy est conçu pour les séjours à la plage, les photos de famille au soleil, les dîners de vacances et les célébrations coordonnées par beau temps. Les robes donnent aux filles et aux mamans une allure douce, prête pour les photos, tandis que les chemises des garçons et des papas gardent un style assorti décontracté et facile à porter.',
'Ce brouillon suit fidèlement le tableau joint : des variantes de robe sont créées pour les filles et les mères, et des variantes de chemise pour les garçons et les pères. Le tableau source publie aussi des mesures de shorts dans les lignes masculines, mais les shorts sont exclus de cette annonce à la demande de l’opérateur.',
'Caractéristiques principales :','Options familiales coordonnées :','Les choix de robe et de chemise sont regroupés dans un même produit familial assorti.',
'Marguerites pour les vacances :','Le style floral jaune fait ressortir l’ensemble sur les photos à la plage et au complexe hôtelier.',
'Tailles indiquant le membre de la famille :','Les libellés de taille distinguent clairement les lignes Enfant, Mère et Père.',
'Brouillon appuyé par le tableau :','Seules les lignes visibles dans le guide des tailles fourni sont incluses comme variantes.',
'Shorts exclus :','Les shorts blancs montrés sur l’image et dans le tableau servent uniquement à la mise en scène et ne sont pas vendus dans ce brouillon.',
'Choisissez le Type et la Taille pour chaque membre de la famille, puis composez une tenue assortie lumineuse pour les vacances, les photos de famille et les journées au soleil ensemble.'
]
TEXT[220,'it']=[
'Tessuto e sensazione al tatto:','Tessuto leggero a trama piatta per la bella stagione; la composizione esatta delle fibre non era visibile nelle prove fornite.',
'Stile in famiglia:','Un vivace look da spiaggia coordinato per mamma, papà, bambine e bambini, uniti da un tema giallo con margherite.',
'Motivo:','Tessuto giallo sole con ricami di margherite bianche e una delicata atmosfera di vacanza.',
'Dettagli del modello:','Bambine e mamme indossano l’abito senza maniche con scollo a volant; bambini e papà indossano la camicia a maniche corte con bottoni. Shorts, cappelli, borse, scarpe e accessori servono soltanto a comporre il look.',
'Cura:','Lavare in lavatrice in acqua fredda con ciclo delicato, asciugare appeso, non candeggiare e, se necessario, stirare al rovescio a bassa temperatura.',
'Gamma di taglie:','Bambino 2 anni fino a Bambino 9-10 anni, Madre S-3XL e Padre M-4XL.',
'Tabella taglie - Abito']+headers('it')+['Tabella taglie - Camicia',
'Il coordinato familiare Sunshine Daisy è pensato per gite al mare, foto di famiglia al sole, cene in vacanza e festeggiamenti coordinati nella bella stagione. Gli abiti mantengono dolce e pronto per le foto il look di bambine e mamme, mentre le camicie di bambini e papà danno all’abbinamento un’aria rilassata e semplice.',
'Questa bozza segue attentamente la tabella allegata: vengono create varianti di abito per bambine e madri e varianti di camicia per bambini e padri. La tabella di origine pubblica anche misure degli shorts nelle righe maschili, ma gli shorts sono esclusi da questa inserzione su richiesta dell’operatore.',
'Caratteristiche principali:','Opzioni coordinate per la famiglia:','Le opzioni di abito e camicia sono riunite in un unico prodotto coordinato per la famiglia.',
'Look a margherite pronto per le vacanze:','Lo stile floreale giallo fa risaltare il completo nelle foto in spiaggia e al resort.',
'Taglie che indicano il ruolo familiare:','Le etichette delle taglie distinguono chiaramente le righe Bambino, Madre e Padre.',
'Bozza supportata dalla tabella:','Sono incluse come varianti soltanto le righe visibili nella tabella taglie fornita.',
'Shorts esclusi:','Gli shorts bianchi mostrati nell’immagine e nella tabella servono soltanto a comporre il look e non sono venduti in questa bozza.',
'Scegli il Tipo e la Taglia per ogni familiare, poi crea un look coordinato vivace per vacanze, foto di famiglia e giornate di sole insieme.'
]
TEXT[220,'nl']=[
'Stof en gevoel:','Lichte geweven stof voor warm weer; de exacte vezelsamenstelling was niet zichtbaar in het aangeleverde bewijsmateriaal.',
'Voor het gezin:','Een vrolijke, bijpassende strandlook voor moeder, vader, meisjes en jongens, rond één geel madeliefjesthema.',
'Print:','Zongeel materiaal met witte madeliefjesborduursels en een zachte vakantie-uitstraling.',
'Ontwerpdetails:','Meisjes en moeders dragen de mouwloze jurk met ruches aan de hals; jongens en vaders dragen het overhemd met korte mouwen en knopen. Shorts, hoeden, tassen, schoenen en accessoires dienen alleen voor de styling.',
'Wasvoorschrift:','Machinewas koud op een fijnwasprogramma, aan de lijn drogen, niet bleken en zo nodig binnenstebuiten op lage temperatuur strijken.',
'Maatbereik:','Kind 2 jaar tot en met Kind 9-10 jaar, Moeder S-3XL en Vader M-4XL.',
'Maattabel - Jurk']+headers('nl')+['Maattabel - Overhemd',
'De Sunshine Daisy-familieset is gemaakt voor stranduitjes, zonnige gezinsfoto’s, vakantiediners en bijpassende outfits voor feestelijke gelegenheden bij warm weer. De jurken geven meisjes en moeders een lieve look die mooi op foto’s uitkomt, terwijl de overhemden voor jongens en vaders de gezamenlijke stijl ontspannen en gemakkelijk houden.',
'Dit concept volgt de bijgevoegde tabel nauwkeurig: jurkvarianten worden gemaakt voor meisjes en moeders, overhemdvarianten voor jongens en vaders. De brontabel vermeldt ook shortmaten op de mannelijke rijen, maar shorts zijn op verzoek van de uitvoerder uitgesloten van deze aanbieding.',
'Belangrijkste kenmerken:','Bijpassende opties voor het gezin:','Jurk- en overhemdkeuzes zijn samengebracht in één bijpassend familieproduct.',
'Madeliefjeslook voor de vakantie:','De gele bloemenstijl laat de set opvallen in strand- en resortfoto’s.',
'Maten met gezinsrol:','De maatlabels maken duidelijk onderscheid tussen de rijen Kind, Moeder en Vader.',
'Concept op basis van de maattabel:','Alleen de rijen die zichtbaar zijn in de aangeleverde maattabel zijn als varianten opgenomen.',
'Shorts uitgesloten:','De witte shorts op de afbeelding en in de tabel dienen alleen voor de styling en worden in dit concept niet verkocht.',
'Kies het Type en de Maat voor elk gezinslid en stel een vrolijke, bijpassende look samen voor vakanties, gezinsfoto’s en zonnige dagen samen.'
]
TEXT[220,'pl']=[
'Materiał i odczucie w dotyku:','Lekka tkanina na ciepłe dni; dokładny skład włókien nie był widoczny w dostarczonych materiałach źródłowych.',
'Rodzinny styl:','Wyrazisty, pasujący strój plażowy dla mamy, taty, dziewczynek i chłopców ze wspólnym żółtym motywem stokrotek.',
'Wzór:','Słonecznie żółty materiał z haftem białych stokrotek i delikatnym wakacyjnym charakterem.',
'Szczegóły fasonu:','Dziewczynki i mamy noszą sukienkę bez rękawów z falbanką przy dekolcie; chłopcy i ojcowie noszą koszulę z krótkim rękawem zapinaną na guziki. Szorty, kapelusze, torby, buty i dodatki służą wyłącznie stylizacji.',
'Pielęgnacja:','Prać w pralce w zimnej wodzie na delikatnym programie, suszyć rozwieszone, nie wybielać i w razie potrzeby prasować na lewej stronie w niskiej temperaturze.',
'Zakres rozmiarów:','Dziecko 2 lata do Dziecko 9-10 lat, Mama S-3XL i Tata M-4XL.',
'Tabela rozmiarów - Sukienka']+headers('pl')+['Tabela rozmiarów - Koszula',
'Rodzinny zestaw Sunshine Daisy powstał z myślą o wyjazdach na plażę, słonecznych zdjęciach rodzinnych, wakacyjnych kolacjach i wspólnych uroczystościach w pasujących strojach w ciepłe dni. Sukienki nadają dziewczynkom i mamom uroczy wygląd gotowy do zdjęć, a koszule chłopców i ojców utrzymują swobodny i niewymuszony charakter wspólnego stylu.',
'Ten szkic ściśle odpowiada załączonej tabeli: warianty sukienek są tworzone dla dziewczynek i mam, a warianty koszul dla chłopców i ojców. Tabela źródłowa podaje także wymiary szortów w męskich wierszach, ale szorty wykluczono z tej oferty na prośbę operatora.',
'Najważniejsze cechy:','Pasujące opcje rodzinne:','Sukienki i koszule są zgrupowane w jednym produkcie z pasującymi strojami dla rodziny.',
'Wakacyjny motyw stokrotek:','Żółta kwiatowa stylizacja wyróżnia zestaw na zdjęciach z plaży i kurortu.',
'Rozmiary z oznaczeniem roli rodzinnej:','Etykiety rozmiarów wyraźnie oddzielają wiersze Dziecko, Mama i Tata.',
'Szkic potwierdzony tabelą:','Jako warianty uwzględniono wyłącznie wiersze widoczne w dostarczonej tabeli rozmiarów.',
'Szorty wykluczone:','Białe szorty widoczne na zdjęciu i w tabeli służą wyłącznie stylizacji i nie są sprzedawane w tym szkicu.',
'Wybierz Typ i Rozmiar dla każdej osoby w rodzinie, a następnie stwórz wyrazisty, pasujący strój na wakacje, rodzinne zdjęcia i wspólne słoneczne dni.'
]
TEXT[220,'pt-BR']=[
'Tecido e toque:','Tecido leve de trama plana para os dias quentes; a composição exata das fibras não estava visível nas evidências fornecidas.',
'Estilo em família:','Um visual de praia vibrante e coordenado para mãe, pai, meninas e meninos, com um tema único de margaridas amarelas.',
'Estampa:','Tecido amarelo-sol com bordado de margaridas brancas e um toque suave de férias.',
'Detalhes do modelo:','Meninas e mães usam o vestido sem mangas com babado no decote; meninos e pais usam a camisa de manga curta com botões. Shorts, chapéus, bolsas, calçados e acessórios servem apenas para compor o visual.',
'Cuidados:','Lave à máquina com água fria no ciclo delicado, seque no varal, não use alvejante e, se necessário, passe do avesso em temperatura baixa.',
'Grade de tamanhos:','Criança 2 anos a Criança 9-10 anos, Mãe S-3XL e Pai M-4XL.',
'Tabela de medidas - Vestido']+headers('pt-BR')+['Tabela de medidas - Camisa',
'O conjunto familiar Sunshine Daisy foi feito para passeios na praia, fotos de família ao sol, jantares nas férias e comemorações coordenadas nos dias quentes. Os vestidos dão às meninas e mães um visual delicado e pronto para as fotos, enquanto as camisas dos meninos e pais mantêm a combinação descontraída e fácil de usar.',
'Este rascunho segue de perto a tabela em anexo: são criadas variantes de vestido para meninas e mães e variantes de camisa para meninos e pais. A tabela da fonte também apresenta medidas de shorts nas linhas masculinas, mas os shorts estão excluídos deste anúncio conforme a solicitação do operador.',
'Principais características:','Opções coordenadas para a família:','As opções de vestido e camisa estão agrupadas em um único produto para a família combinar.',
'Visual de margaridas pronto para as férias:','O estilo floral amarelo destaca o conjunto nas fotos de praia e resort.',
'Tamanhos com identificação familiar:','Os nomes dos tamanhos separam claramente as linhas Criança, Mãe e Pai.',
'Rascunho respaldado pela tabela:','Apenas as linhas visíveis na tabela fornecida são incluídas como variantes.',
'Shorts excluídos:','Os shorts brancos mostrados na imagem e na tabela servem apenas para compor o visual e não são vendidos neste rascunho.',
'Escolha o Tipo e o Tamanho para cada pessoa da família e monte um visual vibrante combinando para férias, fotos em família e dias ensolarados juntos.'
]
TEXT[221,'es']=[
'Tejido:','Aspecto de tul suave en capas, con la ligereza de una falda de fiesta; la composición exacta de fibras no era visible en las pruebas facilitadas.',
'Estilo en familia:','Faldas a juego para mamá e hija, pensadas para cumpleaños, retratos, salidas especiales y días de juego con disfraces.',
'Estampado:','Pink & Blue Tulle mantiene un estilo dulce y pastel con colores rosa y azul para elegir.',
'Detalles del diseño:','Silueta de tul en capas con volumen, cintura de poner sin cierre y una forma ideal para dar vueltas, tanto para madre como para niña.',
'Cuidados:','Lavar a mano con agua fría, devolver suavemente la forma, secar en plano y evitar la lejía o las superficies ásperas que puedan enganchar el tul.',
'Rango de tallas:','Niñas: Infantil 2 años a Infantil 12 años; Madre S a Madre L.',
'Guía de tallas - Falda de tul']+headers('es')+['Hasta 50 kg / 110.2 lbs','Hasta 57.5 kg / 126.8 lbs','Hasta 65 kg / 143.3 lbs',
'El anuncio de faldas para mamá e hija Pink & Blue Tulle facilita el look a juego: elige una talla infantil, una talla de madre y el color pastel que encaje con la sesión de fotos. Las imágenes facilitadas muestran la misma idea de falda suave en capas para mamá e hija, con opciones rosa y azul disponibles en la misma fuente.',
'La tabla adjunta respalda las filas de tallas publicadas y las orientaciones de ajuste para adultas. No publica medidas de cintura, cadera ni largo de falda, por lo que esas celdas permanecen vacías en lugar de inventarse valores.',
'Características principales:','Mamá e hija a juego:','Estilo de falda coordinado en tallas infantiles y de madre.',
'Dos colores para elegir:','Rosa y azul se gestionan como variantes de Color de un mismo producto.',
'Tul pensado para dar vueltas:','El volumen en capas aporta al conjunto un alegre aire de fiesta.',
'Filas de tallas respaldadas por la tabla:','Cada variante corresponde a una fila de talla visible en la fuente.',
'Anuncio preparado como borrador:','Creado para su revisión antes de cualquier paso de publicación por separado.',
'Elige rosa o azul y crea un sencillo look de faldas a juego para retratos, fiestas y salidas de madre e hija.'
]
TEXT[221,'fr']=[
'Tissu :','Un aspect de tulle doux superposé, avec la légèreté d’une jupe de fête ; la composition exacte des fibres n’était pas visible dans les éléments fournis.',
'En famille :','Des jupes assorties pour mère et fille, conçues pour les anniversaires, les portraits, les sorties spéciales et les journées de déguisement ludiques.',
'Motif :','Pink & Blue Tulle garde un style doux et pastel avec des couleurs rose et bleue au choix.',
'Détails du modèle :','Une silhouette ample en couches de tulle, une taille à enfiler et une forme faite pour tournoyer, pour la mère comme pour l’enfant.',
'Entretien :','Laver à la main à l’eau froide, remettre délicatement en forme, sécher à plat et éviter l’eau de Javel ou les surfaces rugueuses qui pourraient accrocher le tulle.',
'Gamme de tailles :','Filles : Enfant 2 ans à Enfant 12 ans ; Mère S à Mère L.',
'Guide des tailles - Jupe en tulle']+headers('fr')+['Jusqu’à 50 kg / 110.2 lbs','Jusqu’à 57.5 kg / 126.8 lbs','Jusqu’à 65 kg / 143.3 lbs',
'L’annonce de jupes pour mère et fille Pink & Blue Tulle simplifie les tenues assorties : choisissez une taille enfant, une taille mère et la couleur pastel adaptée à vos photos. Les images fournies montrent le même style de jupe douce superposée pour maman et sa fille, avec du rose et du bleu disponibles auprès de la même source.',
'Le tableau joint appuie les lignes de tailles publiées et les indications d’ajustement pour adultes. Il ne publie pas les mesures de taille, de hanches ni de longueur de jupe ; ces cellules restent donc vides dans le tableau au lieu d’être estimées.',
'Caractéristiques principales :','Mère et fille assorties :','Un style de jupe coordonné dans les tailles enfant et mère.',
'Deux couleurs au choix :','Le rose et le bleu sont gérés comme des variantes de Couleur dans un même produit.',
'Tulle fait pour tournoyer :','Le volume superposé donne à la tenue un esprit de fête ludique.',
'Lignes de tailles appuyées par le tableau :','Chaque variante correspond à une ligne de taille visible dans la source.',
'Annonce préparée en brouillon :','Conçue pour être relue avant toute étape distincte de publication.',
'Choisissez rose ou bleu et composez facilement des jupes assorties pour les portraits, les fêtes et les sorties mère-fille.'
]
TEXT[221,'it']=[
'Tessuto:','Aspetto morbido in tulle a strati, con la leggerezza di una gonna da festa; la composizione esatta delle fibre non era visibile nelle prove fornite.',
'Stile in famiglia:','Gonne abbinate per mamma e figlia, pensate per compleanni, ritratti, uscite speciali e divertenti giornate in cui travestirsi.',
'Motivo:','Pink & Blue Tulle mantiene un look dolce e pastello con rosa e blu tra i colori disponibili.',
'Dettagli del modello:','Silhouette ampia in tulle a strati, vita da infilare e una forma adatta alle piroette sia per mamma sia per bambina.',
'Cura:','Lavare a mano in acqua fredda, ridare delicatamente la forma, asciugare in piano ed evitare candeggina o superfici ruvide che possano impigliare il tulle.',
'Gamma di taglie:','Bambine: Bambino 2 anni a Bambino 12 anni; Madre S a Madre L.',
'Tabella taglie - Gonna in tulle']+headers('it')+['Fino a 50 kg / 110.2 lbs','Fino a 57.5 kg / 126.8 lbs','Fino a 65 kg / 143.3 lbs',
'L’inserzione di gonne per mamma e figlia Pink & Blue Tulle rende semplice l’abbinamento: scegli una taglia da bambina, una da madre e il colore pastello adatto alle foto che hai in mente. Le immagini fornite mostrano la stessa idea di gonna morbida a strati per mamma e figlia, con opzioni rosa e blu disponibili dalla stessa fonte.',
'La tabella allegata supporta le righe delle taglie pubblicate e le indicazioni di vestibilità per adulte. Non pubblica misure della vita, dei fianchi o della lunghezza della gonna, quindi queste celle restano vuote nella tabella anziché essere stimate.',
'Caratteristiche principali:','Mamma e figlia coordinate:','Stile della gonna coordinato nelle taglie da bambina e da madre.',
'Due colori a scelta:','Rosa e blu sono gestiti come varianti di Colore in un unico prodotto.',
'Look in tulle adatto alle piroette:','Il volume a strati conferisce all’outfit un’aria giocosa da festa.',
'Righe delle taglie supportate dalla tabella:','Ogni variante corrisponde a una riga di taglia visibile nella fonte.',
'Inserzione predisposta come bozza:','Preparata per la revisione prima di qualsiasi fase separata di pubblicazione.',
'Scegli rosa o blu e crea un semplice abbinamento di gonne per ritratti, feste e uscite di mamma e figlia.'
]
TEXT[221,'nl']=[
'Stof:','Zachte, gelaagde tulelook met het lichte gevoel van een feestrok; de exacte vezelsamenstelling was niet zichtbaar in het aangeleverde bewijsmateriaal.',
'Voor het gezin:','Bijpassende rokken voor moeder en dochter, voor verjaardagen, portretten, bijzondere uitjes en speelse verkleeddagen.',
'Print:','Pink & Blue Tulle houdt de look lief en pastel, met roze en blauw als kleurkeuzes.',
'Ontwerpdetails:','Een vol silhouet van lagen tule, een instaptaille en een model dat mooi meedraait, voor zowel moeder als kind.',
'Wasvoorschrift:','Koud met de hand wassen, voorzichtig in model brengen, plat drogen en bleekmiddel of ruwe oppervlakken waaraan tule kan blijven haken vermijden.',
'Maatbereik:','Meisjes: Kind 2 jaar tot Kind 12 jaar; Moeder S tot Moeder L.',
'Maattabel - Tulerok']+headers('nl')+['Tot 50 kg / 110.2 lbs','Tot 57.5 kg / 126.8 lbs','Tot 65 kg / 143.3 lbs',
'De aanbieding voor Pink & Blue Tulle-rokken voor moeder en dochter maakt een bijpassende look eenvoudig: kies een kindermaat, een moedermaat en de pastelkleur die bij het fotoplan past. De aangeleverde beelden tonen hetzelfde zachte, gelaagde rokidee voor moeder en dochter, met roze en blauwe opties uit dezelfde bron.',
'De bijgevoegde tabel ondersteunt de gepubliceerde maatrijen en de pasvormrichtlijnen voor volwassenen. Er staan geen maten voor de taille, heup of lengte van de rok in; die cellen blijven daarom leeg in plaats van dat er waarden worden geschat.',
'Belangrijkste kenmerken:','Moeder en dochter in dezelfde stijl:','Bijpassende rokstijl in kinder- en moedermaten.',
'Twee kleurkeuzes:','Roze en blauw worden als Kleur-varianten binnen één product aangeboden.',
'Tulelook om in rond te draaien:','Het gelaagde volume geeft de outfit een speels feestelijk gevoel.',
'Maatrijen op basis van de tabel:','Elke variant komt overeen met een zichtbare maatrij in de bron.',
'Aanbieding als concept voorbereid:','Gemaakt voor beoordeling vóór een afzonderlijke publicatiestap.',
'Kies roze of blauw en creëer een eenvoudige, bijpassende rokkenlook voor portretten, feesten en uitjes van moeder en dochter.'
]
TEXT[221,'pl']=[
'Materiał:','Wygląd miękkiego, warstwowego tiulu o lekkości imprezowej spódnicy; dokładny skład włókien nie był widoczny w dostarczonych materiałach źródłowych.',
'Rodzinny styl:','Pasujące spódnice dla mamy i córki, stworzone na urodziny, portrety, wyjątkowe wyjścia i dni pełne zabawy w przebieranie.',
'Wzór:','Pink & Blue Tulle zachowuje delikatny, pastelowy wygląd z różowym i niebieskim do wyboru.',
'Szczegóły fasonu:','Pełny fason z warstw tiulu, wciągana talia i kształt, który pięknie wiruje, zarówno dla mamy, jak i dziecka.',
'Pielęgnacja:','Prać ręcznie w zimnej wodzie, delikatnie przywrócić kształt, suszyć na płasko i unikać wybielacza oraz szorstkich powierzchni, które mogą zahaczyć tiul.',
'Zakres rozmiarów:','Dziewczynki: Dziecko 2 lata do Dziecko 12 lat; Mama S do Mama L.',
'Tabela rozmiarów - Spódnica tiulowa']+headers('pl')+['Do 50 kg / 110.2 lbs','Do 57.5 kg / 126.8 lbs','Do 65 kg / 143.3 lbs',
'Oferta spódnic dla mamy i córki Pink & Blue Tulle upraszcza stworzenie pasującego stroju: wybierz rozmiar dziecięcy, rozmiar mamy i pastelowy kolor odpowiedni do planowanych zdjęć. Dostarczone materiały zdjęciowe pokazują ten sam pomysł miękkiej, warstwowej spódnicy dla mamy i córki, z różowym i niebieskim wariantem z tego samego źródła.',
'Załączona tabela potwierdza opublikowane wiersze rozmiarów i wskazówki dotyczące dopasowania dla dorosłych. Nie podaje wymiarów talii, bioder ani długości spódnicy, więc te komórki pozostają puste zamiast zawierać szacunkowe wartości.',
'Najważniejsze cechy:','Mama i córka w pasujących strojach:','Pasujący fason spódnicy w rozmiarach dziecięcych i dla mam.',
'Dwa kolory do wyboru:','Różowy i niebieski są obsługiwane jako warianty Koloru w jednym produkcie.',
'Tiulowy wygląd do wirowania:','Warstwowa objętość nadaje strojowi radosny, imprezowy charakter.',
'Wiersze rozmiarów potwierdzone tabelą:','Każdy wariant odpowiada widocznemu wierszowi rozmiaru w źródle.',
'Oferta przygotowana jako szkic:','Utworzona do sprawdzenia przed odrębnym etapem publikacji.',
'Wybierz różowy lub niebieski i stwórz prosty, pasujący strój ze spódnicami na portrety, przyjęcia i wyjścia mamy z córką.'
]
TEXT[221,'pt-BR']=[
'Tecido:','Visual suave de tule em camadas, com a leveza de uma saia de festa; a composição exata das fibras não estava visível nas evidências fornecidas.',
'Estilo em família:','Saias combinando para mãe e filha, feitas para aniversários, retratos, passeios especiais e dias divertidos de brincar de se fantasiar.',
'Estampa:','Pink & Blue Tulle mantém o visual delicado e em tons pastel, com rosa e azul como opções de cores.',
'Detalhes do modelo:','Silhueta volumosa de tule em camadas, cintura de vestir sem fecho e um formato que acompanha os giros, tanto para mãe quanto para criança.',
'Cuidados:','Lave à mão com água fria, remodele delicadamente, seque na horizontal e evite alvejante ou superfícies ásperas que possam puxar fios do tule.',
'Grade de tamanhos:','Meninas: Criança 2 anos a Criança 12 anos; Mãe S a Mãe L.',
'Tabela de medidas - Saia de tule']+headers('pt-BR')+['Até 50 kg / 110.2 lbs','Até 57.5 kg / 126.8 lbs','Até 65 kg / 143.3 lbs',
'O anúncio de saias para mãe e filha Pink & Blue Tulle simplifica a combinação: escolha um tamanho infantil, um tamanho de mãe e a cor pastel que combina com o plano das fotos. As imagens fornecidas mostram a mesma proposta de saia suave em camadas para mãe e filha, com opções rosa e azul disponíveis na mesma fonte.',
'A tabela em anexo respalda as linhas de tamanhos publicadas e as orientações de ajuste para adultas. Ela não apresenta medidas de cintura, quadril ou comprimento da saia, por isso essas células ficam vazias na tabela, sem valores estimados.',
'Principais características:','Mãe e filha combinando:','Estilo de saia coordenado nos tamanhos infantis e de mãe.',
'Duas opções de cores:','Rosa e azul são tratados como variantes de Cor em um único produto.',
'Visual de tule para girar:','O volume em camadas dá ao look um ar divertido de festa.',
'Linhas de tamanhos respaldadas pela tabela:','Cada variante corresponde a uma linha de tamanho visível na fonte.',
'Anúncio preparado como rascunho:','Criado para revisão antes de qualquer etapa separada de publicação.',
'Escolha rosa ou azul e monte um visual fácil de saias combinando para retratos, festas e passeios de mãe e filha.'
]
