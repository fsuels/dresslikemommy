"""Manually authored translations of current-source additions and timing correction."""
ADDITIONS={}; TIMING={}
def add(locale,text,heading,timing):
    lines=text.strip().splitlines();assert len(lines)==20,(locale,len(lines));ADDITIONS[locale]=lines;TIMING[locale]=(heading,timing)
add('ar','''خطّط لملابس كل شخص قبل الطلب
خصّص سطرًا لكل شخص في الصورة: القطعة التي سيرتديها، والمقاس المختار، والكمية المطلوبة، وأي ملابس يملكها بالفعل وتتناسب معها. ابدأ بنقشة أو لون تحبه، ثم نسّق بقية الإطلالة حوله.
اختر القطع.
حدّد من يحتاج إلى فستان أو قميص أو قطعة أخرى. تحقّق مما يتضمّنه كل خيار للمنتج قبل إضافته إلى حقيبتك.
تحقّق من مقاس كل شخص.
افتح جدول المقاسات في صفحة ذلك المنتج تحديدًا. قارن القياسات والوحدات المعروضة، واستخدم الأعمار المذكورة كنقطة بداية. قد تختلف نطاقات المقاسات بين التصاميم.
احسب عدد القطع.
بالنسبة إلى الفساتين التي تُباع منفصلة، أضف مقاس الأم ومقاس الابنة كخيارين منفصلين. راجع كل سطر والسعر الإجمالي في حقيبتك.
تحقّق من المواعيد لوجهتك.
اقرأ تقدير التسليم الحالي ومعلومات الشحن قبل الطلب، واترك وقتًا لتجربة جميع القطع. إذا كان موعد التصوير قريبًا، فاستخدم ملابس تملكها بالفعل.
أكمل الإطلالة.
ضع الملابس معًا مع الأحذية وأي طبقات إضافية تملكها. تأكّد من أن الجميع يستطيع الجلوس والمشي والتحرّك براحة.
إطلالتان بفساتين للأم والابنة لتنسيق بقية الملابس حولهما
فساتين Vibrant Rainbow الطويلة المتناسقة للأم والابنة
: ابدأ بخطوط قوس قزح، ثم استخدم أحد ألوانها في ملابس بقية أفراد العائلة.
فساتين Pastel Bloom المتناسقة للأم والابنة
: نسّق الإطلالة حول نقشة الزهور بألوان الباستيل مع قطع تملكها بالفعل.
في كلتا الإطلالتين، يُباع كل فستان للأم أو للابنة منفصلًا. تحقّق من صفحة المنتج الحالية للاطّلاع على المقاسات المتاحة للاختيار والأسعار وإرشادات المقاسات وتقديرات التسليم. لمزيد من الخيارات، تصفّح
فساتين الأم والابنة المتناسقة
.''','خطّط وفقًا لتقدير التسليم','تحقّق من التقدير الخاص بوجهتك واترك وقتًا لتجربة الملابس قبل جلسة التصوير')
add('cs','''Naplánujte oblečení pro každého ještě před objednáním
Pro každou osobu na fotografii si napište jeden řádek: co bude mít na sobě, zvolenou velikost, potřebný počet kusů a oblečení, které už má a které se k němu hodí. Začněte jedním oblíbeným vzorem nebo barvou a podle nich slaďte zbytek.
Vyberte jednotlivé kusy.
Rozhodněte, kdo potřebuje šaty, košili nebo jiný kus oblečení. Před vložením do tašky zkontrolujte, co každá zvolená varianta produktu obsahuje.
Zkontrolujte velikost každé osoby.
Otevřete tabulku velikostí na stránce konkrétního produktu. Porovnejte uvedené míry a jednotky; věkové označení použijte jako výchozí bod. Různé modely mohou mít různé rozsahy velikostí.
Spočítejte kusy.
U šatů prodávaných samostatně přidejte velikost pro maminku a velikost pro dceru jako samostatné položky. V tašce zkontrolujte každý řádek i celkovou cenu.
Ověřte termín doručení do svého cíle.
Před objednáním si přečtěte aktuální odhad doručení a informace o dopravě a nechte si čas na vyzkoušení všeho oblečení. Pokud se termín focení blíží, použijte outfit, který už máte.
Dolaďte celý vzhled.
Rozložte oblečení společně s botami a dalšími vrstvami, které už máte. Zkontrolujte, že všichni mohou pohodlně sedět, chodit a pohybovat se.
Dva styly šatů pro maminku a dceru jako základ outfitu
Dlouhé sladěné šaty pro maminku a dceru Vibrant Rainbow
: začněte duhovými pruhy a některou z jejich barev použijte na oblečení ostatních členů rodiny.
Sladěné šaty pro maminku a dceru Pastel Bloom
: vyjděte z pastelového květinového vzoru a slaďte jej s kousky, které už máte.
U obou stylů se každé šaty pro maminku nebo dceru prodávají samostatně. Na aktuální stránce produktu zkontrolujte dostupné velikosti, ceny, pokyny k výběru velikosti a odhady doručení. Další možnosti najdete v kolekci
šatů pro maminku a dceru
.''','Plánujte podle odhadu doručení','ověřte odhad doručení do svého cíle a nechte si před focením čas na vyzkoušení oblečení')
add('da','''Planlæg hver persons outfit, før du bestiller
Skriv én linje for hver person på billedet: det tøj, personen skal have på, den valgte størrelse, det antal, I har brug for, og tøj, personen allerede har, som passer til. Start med ét print eller én farve, du elsker, og byg videre derfra.
Vælg delene.
Beslut, hvem der har brug for en kjole, en skjorte eller noget andet. Tjek, hvad hvert produktvalg indeholder, før du lægger det i kurven.
Tjek hver persons størrelse.
Åbn størrelsesguiden på netop den produktside. Sammenlign de viste mål og enheder, og brug aldersangivelser som udgangspunkt. Forskellige styles kan have forskellige størrelsesintervaller.
Tæl delene.
Ved kjoler, der sælges separat, skal du tilføje en størrelse til mor og en størrelse til datter som separate valg. Gennemgå hver linje og den samlede pris i kurven.
Tjek leveringstiden til din destination.
Læs det aktuelle leveringsestimat og leveringsoplysningerne, før du bestiller, og giv jer tid til at prøve det hele. Hvis fotodatoen er tæt på, så brug et outfit, I allerede har.
Gør looket færdigt.
Læg tøjet sammen med sko og eventuelle ekstra lag, I allerede har. Tjek, at alle kan sidde, gå og bevæge sig behageligt.
To kjolelooks til mor og datter at bygge videre på
Vibrant Rainbow matchende maxikjoler til mor og datter
: start med regnbuestriberne, og brug derefter en af farverne i de andre familiemedlemmers tøj.
Pastel Bloom matchende kjoler til mor og datter
: tag udgangspunkt i det pastelfarvede blomsterprint, og kombinér med tøj, I allerede har.
I begge looks sælges hver kjole til mor eller datter separat. Tjek den aktuelle produktside for valgbare størrelser, priser, størrelsesvejledning og leveringsestimater. Se flere muligheder blandt vores
matchende kjoler til mor og datter
.''','Planlæg efter leveringsestimatet','tjek estimatet til din destination, og giv jer tid til at prøve tøjet før fotosessionen')
add('el','''Σχεδίασε το ντύσιμο κάθε ατόμου πριν παραγγείλεις
Γράψε μία γραμμή για κάθε άτομο στη φωτογραφία: το ρούχο που θα φορέσει, το επιλεγμένο μέγεθος, την ποσότητα που χρειάζεσαι και όσα ήδη έχει και ταιριάζουν. Ξεκίνα με ένα σχέδιο ή χρώμα που αγαπάς και χτίσε την εμφάνιση γύρω του.
Διάλεξε τα κομμάτια.
Αποφάσισε ποιος χρειάζεται φόρεμα, πουκάμισο ή άλλο είδος. Έλεγξε τι περιλαμβάνει κάθε επιλογή προϊόντος πριν την προσθέσεις στο καλάθι.
Έλεγξε το μέγεθος κάθε ατόμου.
Άνοιξε τον πίνακα μεγεθών στη σελίδα του συγκεκριμένου προϊόντος. Σύγκρινε τις διαστάσεις και τις μονάδες που αναγράφονται· χρησιμοποίησε τις ενδείξεις ηλικίας ως αφετηρία. Διαφορετικά σχέδια μπορεί να έχουν διαφορετικά εύρη μεγεθών.
Μέτρησε τα τεμάχια.
Για φορέματα που πωλούνται χωριστά, πρόσθεσε ένα μέγεθος για τη μαμά και ένα για την κόρη ως ξεχωριστές επιλογές. Έλεγξε κάθε γραμμή και τη συνολική τιμή στο καλάθι.
Έλεγξε τον χρόνο παράδοσης για τον προορισμό σου.
Διάβασε την τρέχουσα εκτίμηση παράδοσης και τις πληροφορίες αποστολής πριν παραγγείλεις και άφησε χρόνο για να δοκιμάσετε τα πάντα. Αν η φωτογράφιση πλησιάζει, χρησιμοποίησε ρούχα που ήδη έχεις.
Ολοκλήρωσε την εμφάνιση.
Άπλωσε τα ρούχα μαζί με τα παπούτσια και τις επιπλέον στρώσεις που ήδη έχετε. Έλεγξε ότι όλοι μπορούν να καθίσουν, να περπατήσουν και να κινηθούν άνετα.
Δύο εμφανίσεις με φορέματα για μαμά και κόρη ως βάση
Ασορτί μάξι φορέματα Vibrant Rainbow για μαμά και κόρη
: ξεκίνα με τις ρίγες ουράνιου τόξου και χρησιμοποίησε ένα από αυτά τα χρώματα στα ρούχα των υπόλοιπων μελών της οικογένειας.
Ασορτί φορέματα Pastel Bloom για μαμά και κόρη
: χτίσε την εμφάνιση γύρω από το παστέλ φλοράλ σχέδιο και συνδύασέ το με κομμάτια που ήδη έχετε.
Και στις δύο εμφανίσεις, κάθε φόρεμα για μαμά ή κόρη πωλείται χωριστά. Έλεγξε την τρέχουσα σελίδα προϊόντος για τα διαθέσιμα μεγέθη, τις τιμές, τις οδηγίες μεγεθών και τις εκτιμήσεις παράδοσης. Για περισσότερες επιλογές, δες τα
ασορτί φορέματα για μαμά και κόρη
.''','Σχεδίασε με βάση την εκτίμηση παράδοσης','έλεγξε την εκτίμηση για τον προορισμό σου και άφησε χρόνο για να δοκιμάσετε τα ρούχα πριν τη φωτογράφιση')
add('es','''Planifica el atuendo de cada persona antes de hacer el pedido
Anota una línea por cada persona que saldrá en la foto: la prenda que llevará, su talla elegida, la cantidad que necesitas y cualquier prenda que ya tenga y combine. Empieza con un estampado o color que te guste y crea el resto del look a partir de él.
Elige las prendas.
Decide quién necesita un vestido, una camisa u otra prenda. Comprueba qué incluye cada selección de producto antes de añadirla a la bolsa.
Comprueba la talla de cada persona.
Abre la guía de tallas de la página de ese producto concreto. Compara las medidas y unidades indicadas; usa las edades como punto de partida. Los distintos modelos pueden tener rangos de tallas diferentes.
Cuenta las prendas.
Para los vestidos que se venden por separado, añade una talla para la madre y otra para la hija como selecciones independientes. Revisa cada línea y el precio total en la bolsa.
Comprueba los plazos para tu destino.
Lee la estimación de entrega actual y la información de envío antes de hacer el pedido, y deja tiempo para probarlo todo. Si la fecha de las fotos está cerca, usa un atuendo que ya tengas.
Completa el look.
Coloca juntos los atuendos, los zapatos y las capas adicionales que ya tengas. Comprueba que todos puedan sentarse, caminar y moverse cómodamente.
Dos looks de vestidos madre e hija como punto de partida
Vestidos largos a juego para mamá e hija Vibrant Rainbow
: empieza con las rayas de arcoíris y usa uno de esos colores en la ropa de los demás miembros de la familia.
Vestidos a juego para mamá e hija Pastel Bloom
: crea el look a partir del estampado floral en tonos pastel y combínalo con prendas que ya tengas.
En ambos looks, cada vestido de madre o hija se vende por separado. Consulta la página actual del producto para ver las tallas disponibles, los precios, las indicaciones de tallaje y las estimaciones de entrega. Para ver más opciones, explora los
vestidos a juego para mamá e hija
.''','Planifica según la estimación de entrega','comprueba la estimación para tu destino y deja tiempo para probar los atuendos antes de la sesión de fotos')
add('fi','''Suunnittele jokaisen asu ennen tilaamista
Kirjoita jokaiselle kuvassa olevalle henkilölle oma rivi: hänen vaatteensa, valittu kokonsa, tarvittava kappalemäärä ja jo omistetut vaatteet, jotka sopivat kokonaisuuteen. Aloita yhdestä mieluisasta kuosista tai väristä ja rakenna asut sen ympärille.
Valitse vaatteet.
Päätä, kuka tarvitsee mekon, paidan tai muun vaatteen. Tarkista ennen ostoskoriin lisäämistä, mitä kukin tuotevalinta sisältää.
Tarkista jokaisen koko.
Avaa juuri kyseisen tuotteen sivulla oleva kokotaulukko. Vertaa ilmoitettuja mittoja ja mittayksiköitä; käytä ikämerkintöjä lähtökohtana. Eri malleissa voi olla erilaiset kokovalikoimat.
Laske vaatteiden määrä.
Kun mekot myydään erikseen, lisää äidin koko ja tyttären koko erillisinä valintoina. Tarkista ostoskorin jokainen rivi ja yhteishinta.
Tarkista toimitusaika määränpäähäsi.
Lue ajantasainen toimitusarvio ja toimitustiedot ennen tilaamista ja varaa aikaa kaikkien vaatteiden sovittamiseen. Jos kuvauspäivä on pian, käytä jo omistamaasi asua.
Viimeistele kokonaisuus.
Asettele asut vierekkäin kenkien ja jo omistamiesi lisäkerrosten kanssa. Tarkista, että jokainen voi istua, kävellä ja liikkua mukavasti.
Kaksi äidin ja tyttären mekkotyyliä kokonaisuuden pohjaksi
Äidin ja tyttären yhteensopivat Vibrant Rainbow -maksimekot
: aloita sateenkaariraidoista ja käytä jotakin niiden väreistä muiden perheenjäsenten vaatteissa.
Äidin ja tyttären yhteensopivat Pastel Bloom -mekot
: rakenna kokonaisuus pastellisävyisen kukkakuosin ympärille ja yhdistä se jo omistamiisi vaatteisiin.
Molemmissa tyyleissä jokainen äidin tai tyttären mekko myydään erikseen. Tarkista ajantasaiselta tuotesivulta valittavissa olevat koot, hinnat, koko-ohjeet ja toimitusarviot. Lisää vaihtoehtoja löydät
äidin ja tyttären mekoista
.''','Suunnittele toimitusarvion mukaan','tarkista arvio määränpäähäsi ja varaa aikaa asujen sovittamiseen ennen kuvausta')
add('fr','''Prévoyez la tenue de chaque personne avant de commander
Notez une ligne pour chaque personne sur la photo : le vêtement qu’elle portera, la taille choisie, la quantité nécessaire et les pièces qu’elle possède déjà et qui s’accordent avec lui. Commencez par un imprimé ou une couleur que vous aimez, puis composez le reste autour.
Choisissez les pièces.
Déterminez qui a besoin d’une robe, d’une chemise ou d’un autre vêtement. Vérifiez ce que comprend chaque sélection de produit avant de l’ajouter au panier.
Vérifiez la taille de chaque personne.
Ouvrez le guide des tailles sur la page du produit précis. Comparez les mesures et les unités indiquées ; utilisez les indications d’âge comme point de départ. Les gammes de tailles peuvent varier selon les modèles.
Comptez les articles.
Pour les robes vendues séparément, ajoutez une taille pour la mère et une taille pour la fille comme deux sélections distinctes. Vérifiez chaque ligne et le prix total dans votre panier.
Vérifiez les délais pour votre destination.
Lisez l’estimation de livraison actuelle et les informations d’expédition avant de commander, et prévoyez le temps de tout essayer. Si la date des photos est proche, utilisez une tenue que vous possédez déjà.
Finalisez le look.
Disposez les tenues avec les chaussures et les couches supplémentaires que vous possédez. Vérifiez que chacun peut s’asseoir, marcher et bouger confortablement.
Deux looks de robes mère-fille comme point de départ
Robes longues assorties mère-fille Vibrant Rainbow
: partez des rayures arc-en-ciel, puis reprenez l’une de ces couleurs dans les vêtements des autres membres de la famille.
Robes assorties mère-fille Pastel Bloom
: composez le look autour de l’imprimé floral pastel et coordonnez-le avec les pièces que vous possédez déjà.
Pour ces deux looks, chaque robe pour la mère ou la fille est vendue séparément. Consultez la page actuelle du produit pour connaître les tailles proposées, les prix, les conseils de taille et les estimations de livraison. Pour plus de choix, parcourez les
robes assorties mère-fille
.''','Organisez-vous selon l’estimation de livraison','vérifiez l’estimation pour votre destination et prévoyez le temps d’essayer les tenues avant la séance photo')
add('hi','''ऑर्डर करने से पहले हर व्यक्ति के कपड़ों की योजना बनाएँ
फोटो में शामिल हर व्यक्ति के लिए एक पंक्ति लिखें: वह कौन-सा कपड़ा पहनेगा, चुना गया साइज़, ज़रूरी संख्या और उसके पास पहले से मौजूद कौन-से कपड़े उससे मेल खाते हैं। अपनी पसंद के एक प्रिंट या रंग से शुरुआत करें और बाकी कपड़े उसके अनुसार चुनें।
कपड़े चुनें।
तय करें कि किसे ड्रेस, शर्ट या कोई अन्य कपड़ा चाहिए। बैग में जोड़ने से पहले जाँचें कि हर उत्पाद विकल्प में क्या शामिल है।
हर व्यक्ति का साइज़ जाँचें।
ठीक उसी उत्पाद के पेज पर साइज़ चार्ट खोलें। दी गई मापों और इकाइयों की तुलना करें; उम्र के लेबल को शुरुआती आधार मानें। अलग-अलग स्टाइल में साइज़ की सीमाएँ अलग हो सकती हैं।
कपड़ों की संख्या गिनें।
अलग-अलग बेची जाने वाली ड्रेस के लिए माँ का साइज़ और बेटी का साइज़ अलग विकल्पों के रूप में जोड़ें। बैग में हर पंक्ति और कुल कीमत जाँचें।
अपने गंतव्य के लिए समय जाँचें।
ऑर्डर करने से पहले मौजूदा डिलीवरी अनुमान और शिपिंग की जानकारी पढ़ें, और सभी कपड़े पहनकर देखने के लिए समय रखें। अगर फोटो की तारीख पास है, तो पहले से मौजूद कपड़े पहनें।
लुक पूरा करें।
कपड़ों को जूतों और अपने पास मौजूद अतिरिक्त परतों के साथ रखकर देखें। जाँचें कि हर कोई आराम से बैठ, चल और हिल-डुल सके।
माँ और बेटी की ड्रेस के दो लुक, जिनसे शुरुआत कर सकते हैं
माँ और बेटी की मैचिंग Vibrant Rainbow मैक्सी ड्रेस
: इंद्रधनुषी धारियों से शुरुआत करें, फिर उनके किसी एक रंग को परिवार के दूसरे सदस्यों के कपड़ों में इस्तेमाल करें।
माँ और बेटी की मैचिंग Pastel Bloom ड्रेस
: पेस्टल फूलों वाले प्रिंट के आधार पर लुक बनाएँ और उसे पहले से मौजूद कपड़ों के साथ मिलाएँ।
दोनों लुक में माँ या बेटी की हर ड्रेस अलग से बेची जाती है। चुने जा सकने वाले साइज़, कीमतें, साइज़ संबंधी मार्गदर्शन और डिलीवरी अनुमान के लिए उत्पाद का मौजूदा पेज देखें। अधिक विकल्पों के लिए देखें
माँ और बेटी की मैचिंग ड्रेस
।''','डिलीवरी अनुमान के अनुसार योजना बनाएँ','अपने गंतव्य के लिए अनुमान जाँचें और फोटो सत्र से पहले कपड़े पहनकर देखने के लिए समय रखें')
add('it','''Pianifica l’outfit di ogni persona prima di ordinare
Dedica una riga a ogni persona nella foto: il capo che indosserà, la taglia scelta, la quantità necessaria e ciò che possiede già e si abbina. Parti da una fantasia o da un colore che ami, poi costruisci il resto intorno.
Scegli i capi.
Decidi chi ha bisogno di un vestito, di una camicia o di un altro capo. Controlla cosa include ogni selezione di prodotto prima di aggiungerla al carrello.
Controlla la taglia di ogni persona.
Apri la tabella taglie sulla pagina di quello specifico prodotto. Confronta le misure e le unità indicate; usa le età riportate come punto di partenza. Modelli diversi possono avere gamme di taglie diverse.
Conta i capi.
Per i vestiti venduti separatamente, aggiungi una taglia per la mamma e una per la figlia come selezioni distinte. Controlla ogni riga e il prezzo totale nel carrello.
Verifica i tempi per la tua destinazione.
Leggi la stima di consegna attuale e le informazioni sulla spedizione prima di ordinare e lascia il tempo di provare tutto. Se la data delle foto è vicina, usa un outfit che possiedi già.
Completa il look.
Disponi gli outfit insieme alle scarpe e agli eventuali strati aggiuntivi che già possiedi. Controlla che tutti possano sedersi, camminare e muoversi comodamente.
Due look con vestiti mamma e figlia da cui partire
Vestiti lunghi coordinati mamma e figlia Vibrant Rainbow
: parti dalle righe arcobaleno, poi usa uno di quei colori per i vestiti degli altri familiari.
Vestiti coordinati mamma e figlia Pastel Bloom
: costruisci il look intorno alla stampa floreale pastello e abbinala ai capi che possiedi già.
Per entrambi i look, ogni vestito per la mamma o per la figlia è venduto separatamente. Controlla la pagina attuale del prodotto per le taglie selezionabili, i prezzi, le indicazioni sulle taglie e le stime di consegna. Per altre opzioni, esplora i
vestiti coordinati mamma e figlia
.''','Organizzati in base alla stima di consegna','controlla la stima per la tua destinazione e lascia il tempo di provare gli outfit prima della sessione fotografica')
add('ja','''注文前に一人ひとりの服装を計画する
写真に写る一人ひとりについて、着るアイテム、選ぶサイズ、必要な数量、手持ちで合わせられる服を一行ずつ書き出しましょう。好きな柄や色を一つ選び、それを基準に全体を組み合わせます。
アイテムを選ぶ。
誰にドレス、シャツ、または別のアイテムが必要かを決めましょう。バッグに追加する前に、選択した商品に何が含まれるかを確認してください。
全員のサイズを確認する。
その商品のページにあるサイズ表を開きます。記載された寸法と単位を比較し、年齢表示は目安として使いましょう。スタイルによってサイズ展開が異なる場合があります。
アイテムの数を数える。
別売りのドレスは、ママ用のサイズと娘用のサイズをそれぞれ別の選択として追加してください。バッグの各明細と合計金額を確認しましょう。
お届け先への配送時期を確認する。
注文前に最新の配達予定と配送情報を読み、全員が試着できる時間を確保してください。撮影日が近い場合は、すでに持っている服を使いましょう。
コーディネートを仕上げる。
服を靴や手持ちの重ね着用アイテムと一緒に並べます。全員が楽に座り、歩き、動けることを確認しましょう。
コーデの基準にできるママと娘のドレス二つのスタイル
ママと娘のお揃いVibrant Rainbowマキシドレス
：虹色のストライプを基準に、その中の一色をほかの家族の服にも取り入れましょう。
ママと娘のお揃いPastel Bloomドレス
：パステルカラーの花柄を中心に、すでに持っているアイテムと組み合わせましょう。
どちらのスタイルも、ママ用と娘用のドレスは一着ずつ別売りです。選べるサイズ、価格、サイズの選び方、配達予定は現在の商品ページで確認してください。ほかの選択肢は、こちらの
ママと娘のお揃いドレス
をご覧ください。''','配達予定に合わせて計画する','お届け先への配達予定を確認し、撮影前に服を試着できる時間を確保しましょう')
add('ko','''주문하기 전에 각자의 의상을 계획하세요
사진에 나올 사람마다 한 줄씩 적어 보세요. 입을 옷, 선택한 사이즈, 필요한 수량, 이미 가지고 있는 옷 중 어울리는 것을 적습니다. 마음에 드는 프린트나 색상 하나를 정하고 이를 중심으로 코디하세요.
옷을 선택하세요.
누구에게 드레스, 셔츠 또는 다른 옷이 필요한지 정하세요. 장바구니에 담기 전에 선택한 상품에 무엇이 포함되는지 확인하세요.
각자의 사이즈를 확인하세요.
바로 그 상품 페이지의 사이즈표를 여세요. 표시된 치수와 단위를 비교하고, 연령 표시는 출발점으로 참고하세요. 스타일마다 사이즈 범위가 다를 수 있습니다.
상품 수량을 세어 보세요.
별도로 판매되는 드레스는 엄마 사이즈와 딸 사이즈를 각각 따로 선택해 담으세요. 장바구니의 각 항목과 합계 금액을 확인하세요.
배송지에 따른 일정을 확인하세요.
주문 전에 현재 배송 예상일과 배송 정보를 읽고, 모든 옷을 입어 볼 시간을 확보하세요. 촬영 날짜가 가깝다면 이미 가지고 있는 옷을 활용하세요.
스타일을 완성하세요.
의상을 신발과 이미 가지고 있는 겉옷 등과 함께 펼쳐 보세요. 모두 편안하게 앉고 걷고 움직일 수 있는지 확인하세요.
코디의 기준으로 삼을 엄마와 딸의 드레스 스타일 두 가지
엄마와 딸의 Vibrant Rainbow 시밀러룩 맥시드레스
: 무지개 줄무늬를 기준으로 그중 한 가지 색상을 다른 가족의 옷에도 활용하세요.
엄마와 딸의 Pastel Bloom 시밀러룩 드레스
: 파스텔 꽃무늬를 중심으로 이미 가지고 있는 옷과 조화롭게 코디하세요.
두 스타일 모두 엄마용 또는 딸용 드레스가 각각 별도로 판매됩니다. 선택 가능한 사이즈, 가격, 사이즈 안내, 배송 예상일은 현재 상품 페이지에서 확인하세요. 더 많은 선택지는
엄마와 딸의 시밀러룩 드레스
에서 살펴보세요.''','배송 예상일에 맞춰 계획하세요','배송지의 예상일을 확인하고 촬영 전에 의상을 입어 볼 시간을 확보하세요')
add('nl','''Plan de outfit van iedere persoon voordat je bestelt
Schrijf voor iedere persoon op de foto één regel: het kledingstuk dat diegene gaat dragen, de gekozen maat, het benodigde aantal en bijpassende kleding die diegene al heeft. Begin met één print of kleur die je mooi vindt en bouw daarop voort.
Kies de kledingstukken.
Bepaal wie een jurk, een overhemd of iets anders nodig heeft. Controleer wat elke productkeuze bevat voordat je deze in je winkelmandje legt.
Controleer de maat van iedere persoon.
Open de maattabel op de pagina van dat specifieke product. Vergelijk de vermelde maten en eenheden; gebruik leeftijdsaanduidingen als uitgangspunt. Verschillende stijlen kunnen verschillende maatreeksen hebben.
Tel de artikelen.
Voeg voor jurken die apart worden verkocht een moedermaat en een dochtermaat toe als afzonderlijke keuzes. Controleer elke regel en de totaalprijs in je winkelmandje.
Controleer de timing voor jouw bestemming.
Lees vóór het bestellen de actuele bezorgindicatie en verzendinformatie en houd tijd over om alles te passen. Is de fotodatum dichtbij, gebruik dan een outfit die je al hebt.
Maak de look af.
Leg de outfits bij elkaar met schoenen en eventuele extra lagen die je al hebt. Controleer of iedereen comfortabel kan zitten, lopen en bewegen.
Twee moeder-dochterjurkenlooks om op voort te bouwen
Bijpassende Vibrant Rainbow-maxijurken voor moeder en dochter
: begin met de regenboogstrepen en gebruik daarna één van die kleuren voor de kleding van de andere gezinsleden.
Bijpassende Pastel Bloom-jurken voor moeder en dochter
: neem de pastelkleurige bloemenprint als basis en combineer deze met kleding die je al hebt.
Bij beide looks wordt iedere moeder- of dochterjurk apart verkocht. Controleer op de actuele productpagina de beschikbare maten, prijzen, maatadviezen en bezorgindicaties. Bekijk voor meer opties de
bijpassende jurken voor moeder en dochter
.''','Plan op basis van je bezorgindicatie','controleer de indicatie voor jouw bestemming en houd vóór de fotosessie tijd over om de outfits te passen')
add('no','''Planlegg antrekket til hver person før du bestiller
Skriv én linje for hver person på bildet: plagget de skal ha på, valgt størrelse, antallet du trenger, og klær de allerede har som passer til. Begynn med ett mønster eller én farge du liker, og bygg videre derfra.
Velg plaggene.
Bestem hvem som trenger en kjole, en skjorte eller et annet plagg. Kontroller hva hvert produktvalg inkluderer før du legger det i handlekurven.
Kontroller størrelsen til hver person.
Åpne størrelsestabellen på siden til akkurat det produktet. Sammenlign målene og enhetene som vises, og bruk aldersangivelser som utgangspunkt. Ulike stiler kan ha forskjellige størrelsesutvalg.
Tell plaggene.
For kjoler som selges separat, legger du til en størrelse til mor og en størrelse til datter som separate valg. Gå gjennom hver linje og samlet pris i handlekurven.
Kontroller leveringstiden til leveringsstedet ditt.
Les gjeldende leveringsestimat og fraktinformasjon før du bestiller, og sett av tid til å prøve alt. Hvis fotodatoen nærmer seg, bruk et antrekk du allerede har.
Fullfør antrekket.
Legg antrekkene sammen med sko og ekstra lag dere allerede har. Kontroller at alle kan sitte, gå og bevege seg komfortabelt.
To kjolestiler for mor og datter å bygge videre på
Matchende Vibrant Rainbow-maxikjoler for mor og datter
: start med regnbuestripene, og bruk deretter en av fargene i klærne til de andre familiemedlemmene.
Matchende Pastel Bloom-kjoler for mor og datter
: bygg rundt det pastellfargede blomstermønsteret, og kombiner med plagg dere allerede har.
For begge stilene selges hver kjole til mor eller datter separat. Se den gjeldende produktsiden for valgbare størrelser, priser, størrelsesveiledning og leveringsestimater. For flere alternativer kan du se
matchende kjoler for mor og datter
.''','Planlegg etter leveringsestimatet','kontroller estimatet for leveringsstedet ditt, og sett av tid til å prøve antrekkene før fotograferingen')
add('pt-BR','''Planeje a roupa de cada pessoa antes de fazer o pedido
Anote uma linha para cada pessoa na foto: a peça que ela vai usar, o tamanho escolhido, a quantidade necessária e qualquer roupa que ela já tenha e que combine. Comece com uma estampa ou cor de que você goste e monte o restante a partir dela.
Escolha as peças.
Decida quem precisa de um vestido, uma camisa ou outra peça. Confira o que cada opção de produto inclui antes de adicioná-la à sacola.
Confira o tamanho de cada pessoa.
Abra a tabela de medidas na página daquele produto específico. Compare as medidas e as unidades indicadas; use as faixas etárias como ponto de partida. Estilos diferentes podem ter faixas de tamanhos diferentes.
Conte os itens.
Para vestidos vendidos separadamente, adicione um tamanho para a mãe e um para a filha como escolhas separadas. Revise cada linha e o preço total na sacola.
Confira os prazos para o seu destino.
Leia a estimativa de entrega atual e as informações de envio antes de fazer o pedido e reserve tempo para experimentar tudo. Se a data das fotos estiver próxima, use uma roupa que você já tenha.
Finalize o look.
Coloque as roupas juntas com os sapatos e as camadas extras que você já tem. Confira se todos conseguem sentar, caminhar e se movimentar com conforto.
Dois looks de vestidos mãe e filha para usar como base
Vestidos longos combinando para mãe e filha Vibrant Rainbow
: comece pelas listras de arco-íris e use uma dessas cores nas roupas dos outros familiares.
Vestidos combinando para mãe e filha Pastel Bloom
: monte o look a partir da estampa floral em tons pastéis e combine com peças que você já tem.
Nos dois looks, cada vestido de mãe ou filha é vendido separadamente. Confira a página atual do produto para ver os tamanhos disponíveis, os preços, as orientações de tamanho e as estimativas de entrega. Para mais opções, explore os
vestidos combinando para mãe e filha
.''','Planeje de acordo com a estimativa de entrega','confira a estimativa para o seu destino e reserve tempo para experimentar as roupas antes da sessão de fotos')
add('ro','''Planifică ținuta fiecărei persoane înainte să comanzi
Scrie câte un rând pentru fiecare persoană din fotografie: piesa pe care o va purta, mărimea aleasă, cantitatea necesară și hainele pe care le are deja și care se asortează. Începe cu un imprimeu sau o culoare care îți place, apoi construiește restul în jurul acestora.
Alege piesele.
Decide cine are nevoie de o rochie, o cămașă sau alt articol. Verifică ce include fiecare opțiune de produs înainte să o adaugi în coș.
Verifică mărimea fiecărei persoane.
Deschide tabelul de mărimi de pe pagina acelui produs. Compară dimensiunile și unitățile afișate; folosește indicațiile de vârstă ca punct de pornire. Modelele diferite pot avea game diferite de mărimi.
Numără articolele.
Pentru rochiile vândute separat, adaugă o mărime pentru mamă și una pentru fiică drept selecții distincte. Verifică fiecare rând și prețul total din coș.
Verifică termenele pentru destinația ta.
Citește estimarea actuală de livrare și informațiile despre expediere înainte să comanzi și lasă timp pentru a proba toate hainele. Dacă data fotografiilor este aproape, folosește o ținută pe care o ai deja.
Finalizează ținuta.
Așază hainele împreună cu încălțămintea și straturile suplimentare pe care le ai deja. Verifică dacă toată lumea poate sta jos, merge și se poate mișca în confort.
Două stiluri de rochii mamă-fiică de la care să pornești
Rochii maxi asortate pentru mamă și fiică Vibrant Rainbow
: pornește de la dungile curcubeu, apoi folosește una dintre acele culori pentru hainele celorlalți membri ai familiei.
Rochii asortate pentru mamă și fiică Pastel Bloom
: construiește ținuta în jurul imprimeului floral pastel și asortează-l cu piesele pe care le ai deja.
Pentru ambele stiluri, fiecare rochie pentru mamă sau fiică se vinde separat. Verifică pagina actuală a produsului pentru mărimile disponibile, prețuri, îndrumări privind mărimea și estimări de livrare. Pentru mai multe opțiuni, explorează
rochiile asortate pentru mamă și fiică
.''','Planifică în funcție de estimarea de livrare','verifică estimarea pentru destinația ta și lasă timp pentru a proba ținutele înainte de ședința foto')
assert len(ADDITIONS)==15
