#!/usr/bin/env python3
"""Author exactly the assigned 16 shipping-info translations, entirely offline."""
import json,re,collections,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
HELP=HERE.parent/'help-translations'
EMAIL='<a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>'
D={
'ar':{
'h':['معلومات الشحن','خيارات الشحن القياسي والسريع','الوجهات التي نشحن إليها','أوقات معالجة الطلب والتسليم','تتبع الطلب','الجمارك والرسوم وضرائب الاستيراد','أسئلة شائعة حول الشحن'],
1:'نحن في <strong>Dress Like Mommy</strong> متجر إلكتروني نشحن ملابس عائلية متناسقة إلى الوجهات المتاحة عند الدفع، من خلال شركائنا في الشحن وتنفيذ الطلبات. إليك كيفية التأكد من الشحن وموعد التسليم والتتبع قبل تقديم طلبك.',
5:'تعتمد إمكانية الشحن على البلد/المنطقة والعنوان المُدخلين عند الدفع. إذا ظهرت طريقة شحن لعنوانك، فيمكننا الشحن إليه وفقًا للطريقة والسعر المعروضين.',
6:'إذا لم تظهر وجهتك عند الدفع، أو لم تظهر طريقة شحن، فراسلنا على {e} قبل الطلب.',
9:'تختلف تقديرات التسليم باختلاف الوجهة وشركة النقل وإجراءات الجمارك وطريقة الشحن المعروضة عند الدفع. راجع طريقة الشحن وموعد التسليم التقديري الظاهرين عند الدفع قبل تقديم طلبك.',
10:'قد يستغرق تحديث التتبع 24-48 ساعة بعد إصدار رقم التتبع.',
12:'بعد شحن طلبك، تحقق من بريدك الإلكتروني للاطلاع على معلومات التتبع. يمكنك أيضًا زيارة حسابك أو استخدام رابط التتبع في رسالة تأكيد الشحن عندما يكون متاحًا.',
17:'<strong>هل يمكنني تغيير عنوان الشحن بعد الطلب؟</strong><br>تواصل معنا في أقرب وقت ممكن على {e}. إذا لم يدخل طلبك مرحلة التنفيذ بعد، فيمكننا مراجعة ما إذا كان تغيير العنوان لا يزال ممكنًا.',
18:'<strong>هل تشحنون إلى صناديق البريد؟</strong><br>تعتمد إمكانية الشحن إلى صناديق البريد على الوجهة وخيارات شركات النقل المعروضة عند الدفع.',
19:'<strong>لم يصل طردي بعد.</strong><br>تحقق من رابط التتبع أولًا. إذا لم تُحدَّث معلومات التتبع لعدة أيام عمل أو انقضى موعد التسليم التقديري، فراسلنا عبر البريد الإلكتروني مع رقم طلبك.'},
'cs':{
'h':['Informace o dopravě','Možnosti standardní a expresní dopravy','Kam doručujeme','Doba zpracování a doručení','Sledování objednávky','Clo, poplatky a dovozní daně','Časté dotazy k dopravě'],
1:'<strong>Dress Like Mommy</strong> je internetový obchod, který prostřednictvím partnerů pro dopravu a vyřizování objednávek zasílá sladěné rodinné oblečení do destinací dostupných při placení. Zde zjistíte, jak před objednáním ověřit dopravu, termín doručení a sledování zásilky.',
5:'Dostupnost dopravy závisí na zemi/regionu a adrese zadaných při placení. Pokud se pro vaši adresu zobrazí způsob dopravy, můžeme na ni doručit uvedeným způsobem a za zobrazenou cenu.',
6:'Pokud se vaše destinace nebo žádný způsob dopravy při placení nezobrazuje, napište nám před objednáním na {e}.',
9:'Odhadované doručení se liší podle destinace, dopravce, celního odbavení a způsobu dopravy uvedeného při placení. Před odesláním objednávky si zkontrolujte zobrazený způsob dopravy a odhad doručení.',
10:'Aktualizace sledování může po přidělení sledovacího čísla trvat 24-48 hodin.',
12:'Po odeslání objednávky najdete informace o sledování v e-mailu. Můžete také navštívit svůj účet nebo použít odkaz na sledování v e-mailu s potvrzením odeslání, pokud je k dispozici.',
17:'<strong>Mohu po objednání změnit doručovací adresu?</strong><br>Co nejdříve nás kontaktujte na {e}. Pokud se objednávka ještě nezačala vyřizovat, můžeme prověřit, zda je změna adresy stále možná.',
18:'<strong>Doručujete do poštovních přihrádek?</strong><br>Dostupnost doručení do poštovních přihrádek závisí na destinaci a možnostech dopravce zobrazených při placení.',
19:'<strong>Moje zásilka ještě nedorazila.</strong><br>Nejprve zkontrolujte odkaz na sledování. Pokud se sledování několik pracovních dnů neaktualizovalo nebo uplynul odhadovaný termín doručení, napište nám e-mail s číslem objednávky.'},
'da':{
'h':['Forsendelsesoplysninger','Standard- og ekspresforsendelse','Hvor vi sender til','Behandlings- og leveringstider','Ordresporing','Told, afgifter og importskatter','Ofte stillede spørgsmål om forsendelse'],
1:'Hos <strong>Dress Like Mommy</strong> er vi en netbutik, der sender matchende familietøj til de destinationer, der er tilgængelige ved betaling, gennem vores partnere inden for forsendelse og ordreekspedition. Her kan du se, hvordan du kontrollerer forsendelse, leveringstid og sporing, før du afgiver en ordre.',
5:'Muligheden for forsendelse afhænger af det land/den region og den adresse, der indtastes ved betaling. Hvis der vises en forsendelsesmetode for din adresse, kan vi sende dertil med den viste metode og til den viste pris.',
6:'Hvis din destination ikke vises ved betaling, eller hvis der ikke vises en forsendelsesmetode, skal du skrive til os på {e}, før du bestiller.',
9:'Forventede leveringstider varierer afhængigt af destination, transportør, toldbehandling og den forsendelsesmetode, der vises ved betaling. Gennemgå den viste forsendelsesmetode og forventede leveringstid, før du afgiver din ordre.',
10:'Det kan tage 24-48 timer, før sporingen opdateres, efter at sporingsnummeret er udstedt.',
12:'Når din ordre er afsendt, skal du tjekke din e-mail for sporingsoplysninger. Du kan også besøge din konto eller bruge sporingslinket i forsendelsesbekræftelsen, når det er tilgængeligt.',
17:'<strong>Kan jeg ændre min leveringsadresse efter bestilling?</strong><br>Kontakt os hurtigst muligt på {e}. Hvis din ordre endnu ikke er gået videre til ekspedition, kan vi undersøge, om det stadig er muligt at ændre adressen.',
18:'<strong>Sender I til postbokse?</strong><br>Muligheden for levering til postbokse afhænger af destinationen og de transportørmuligheder, der vises ved betaling.',
19:'<strong>Min pakke er ikke ankommet endnu.</strong><br>Tjek først dit sporingslink. Hvis sporingen ikke er opdateret i flere hverdage, eller den forventede leveringsdato er overskredet, skal du sende os en e-mail med dit ordrenummer.'},
'de':{
'h':['Versandinformationen','Standard- und Expressversand','Wohin wir versenden','Bearbeitungs- und Lieferzeiten','Sendungsverfolgung','Zoll, Abgaben und Einfuhrsteuern','Häufige Fragen zum Versand'],
1:'<strong>Dress Like Mommy</strong> ist ein Onlineshop, der über Versand- und Abwicklungspartner aufeinander abgestimmte Familienkleidung an die beim Bezahlen verfügbaren Ziele versendet. Hier erfahren Sie, wie Sie Versand, Lieferzeit und Sendungsverfolgung vor einer Bestellung prüfen.',
5:'Die Versandverfügbarkeit richtet sich nach dem Land/der Region und der Adresse, die beim Bezahlen eingegeben werden. Wenn für Ihre Adresse eine Versandmethode angezeigt wird, können wir mit der angezeigten Methode und zum angezeigten Preis dorthin liefern.',
6:'Wenn Ihr Ziel oder keine Versandmethode beim Bezahlen angezeigt wird, schreiben Sie uns vor der Bestellung an {e}.',
9:'Die voraussichtliche Lieferzeit hängt von Zielort, Versanddienstleister, Zollabfertigung und der beim Bezahlen angezeigten Versandmethode ab. Prüfen Sie die angezeigte Methode und Lieferprognose, bevor Sie bestellen.',
10:'Nach Vergabe der Sendungsnummer kann es 24-48 Stunden dauern, bis die Sendungsverfolgung aktualisiert wird.',
12:'Prüfen Sie nach dem Versand Ihrer Bestellung Ihre E-Mails auf Informationen zur Sendungsverfolgung. Sie können auch Ihr Konto aufrufen oder, sofern verfügbar, den Tracking-Link in der Versandbestätigung verwenden.',
17:'<strong>Kann ich meine Lieferadresse nach der Bestellung ändern?</strong><br>Kontaktieren Sie uns so schnell wie möglich unter {e}. Wenn Ihre Bestellung noch nicht in die Abwicklung übergegangen ist, können wir prüfen, ob eine Adressänderung noch möglich ist.',
18:'<strong>Versenden Sie an Postfächer?</strong><br>Ob eine Lieferung an Postfächer möglich ist, hängt vom Zielort und den beim Bezahlen angezeigten Versandoptionen ab.',
19:'<strong>Mein Paket ist noch nicht angekommen.</strong><br>Prüfen Sie zuerst den Tracking-Link. Wenn die Sendungsverfolgung seit mehreren Werktagen nicht aktualisiert wurde oder der voraussichtliche Liefertermin verstrichen ist, senden Sie uns eine E-Mail mit Ihrer Bestellnummer.'},
'el':{
'h':['Πληροφορίες αποστολής','Επιλογές κανονικής και ταχείας αποστολής','Πού αποστέλλουμε','Χρόνοι επεξεργασίας και παράδοσης','Παρακολούθηση παραγγελίας','Τελωνείο, δασμοί και φόροι εισαγωγής','Συχνές ερωτήσεις για την αποστολή'],
1:'Το <strong>Dress Like Mommy</strong> είναι ηλεκτρονικό κατάστημα που αποστέλλει ασορτί οικογενειακά ρούχα στους προορισμούς που είναι διαθέσιμοι στο ταμείο, μέσω των συνεργατών μας για αποστολή και διεκπεραίωση παραγγελιών. Δείτε πώς να επιβεβαιώσετε την αποστολή, τον χρόνο παράδοσης και την παρακολούθηση πριν παραγγείλετε.',
5:'Η διαθεσιμότητα αποστολής βασίζεται στη χώρα/περιοχή και τη διεύθυνση που καταχωρίζετε στο ταμείο. Αν εμφανίζεται μέθοδος αποστολής για τη διεύθυνσή σας, μπορούμε να στείλουμε εκεί με τη μέθοδο και τη χρέωση που εμφανίζονται.',
6:'Αν ο προορισμός σας δεν εμφανίζεται στο ταμείο ή δεν εμφανίζεται μέθοδος αποστολής, στείλτε μας email στο {e} πριν παραγγείλετε.',
9:'Οι εκτιμήσεις παράδοσης διαφέρουν ανάλογα με τον προορισμό, τον μεταφορέα, τον εκτελωνισμό και τη μέθοδο αποστολής που εμφανίζεται στο ταμείο. Ελέγξτε τη μέθοδο και την εκτίμηση παράδοσης πριν υποβάλετε την παραγγελία σας.',
10:'Η ενημέρωση της παρακολούθησης μπορεί να χρειαστεί 24-48 ώρες μετά την έκδοση του αριθμού παρακολούθησης.',
12:'Μόλις αποσταλεί η παραγγελία σας, ελέγξτε το email σας για πληροφορίες παρακολούθησης. Μπορείτε επίσης να επισκεφθείτε τον λογαριασμό σας ή να χρησιμοποιήσετε τον σύνδεσμο παρακολούθησης στο email επιβεβαίωσης αποστολής, όταν είναι διαθέσιμος.',
17:'<strong>Μπορώ να αλλάξω τη διεύθυνση αποστολής μετά την παραγγελία;</strong><br>Επικοινωνήστε μαζί μας το συντομότερο δυνατό στο {e}. Αν η παραγγελία σας δεν έχει ακόμη περάσει στο στάδιο διεκπεραίωσης, μπορούμε να εξετάσουμε αν παραμένει δυνατή η αλλαγή διεύθυνσης.',
18:'<strong>Αποστέλλετε σε ταχυδρομικές θυρίδες;</strong><br>Η διαθεσιμότητα αποστολής σε ταχυδρομικές θυρίδες εξαρτάται από τον προορισμό και τις επιλογές μεταφορέα που εμφανίζονται στο ταμείο.',
19:'<strong>Το δέμα μου δεν έχει φτάσει ακόμη.</strong><br>Ελέγξτε πρώτα τον σύνδεσμο παρακολούθησης. Αν δεν έχει ενημερωθεί για αρκετές εργάσιμες ημέρες ή έχει περάσει η εκτιμώμενη ημερομηνία παράδοσης, στείλτε μας email με τον αριθμό παραγγελίας σας.'},
'fi':{
'h':['Toimitustiedot','Vakio- ja pikatoimituksen vaihtoehdot','Minne toimitamme','Käsittely- ja toimitusajat','Tilauksen seuranta','Tullit, maksut ja tuontiverot','Usein kysyttyä toimituksesta'],
1:'<strong>Dress Like Mommy</strong> on verkkokauppa, joka toimittaa yhteensopivia perheasuja kassalla saatavilla oleviin kohteisiin toimitus- ja tilaustenkäsittelykumppaniensa kautta. Näin voit tarkistaa toimituksen, toimitusajan ja seurannan ennen tilaamista.',
5:'Toimituksen saatavuus perustuu kassalla annettuun maahan/alueeseen ja osoitteeseen. Jos osoitteellesi näytetään toimitustapa, voimme toimittaa sinne näytetyllä tavalla ja hinnalla.',
6:'Jos määränpääsi ei näy kassalla tai toimitustapaa ei näytetä, lähetä meille sähköpostia osoitteeseen {e} ennen tilaamista.',
9:'Toimitusaika-arviot vaihtelevat määränpään, kuljetusliikkeen, tullikäsittelyn ja kassalla näytettävän toimitustavan mukaan. Tarkista kassalla näytetty toimitustapa ja arvio ennen tilaamista.',
10:'Seurannan päivittyminen voi kestää 24-48 tuntia seurantanumeron antamisen jälkeen.',
12:'Kun tilauksesi on lähetetty, tarkista seurantatiedot sähköpostistasi. Voit myös käydä tililläsi tai käyttää lähetysvahvistuksen seurantalinkkiä, jos se on saatavilla.',
17:'<strong>Voinko muuttaa toimitusosoitetta tilaamisen jälkeen?</strong><br>Ota meihin yhteyttä mahdollisimman pian osoitteessa {e}. Jos tilauksesi ei ole vielä siirtynyt toimituksen valmisteluun, voimme selvittää, onko osoitteen muuttaminen yhä mahdollista.',
18:'<strong>Toimitatteko postilokeroihin?</strong><br>Toimitus postilokeroihin riippuu määränpäästä ja kassalla näytettävistä kuljetusliikkeen vaihtoehdoista.',
19:'<strong>Pakettini ei ole vielä saapunut.</strong><br>Tarkista ensin seurantalinkki. Jos seuranta ei ole päivittynyt useaan arkipäivään tai arvioitu toimitusaika on mennyt, lähetä meille sähköpostia ja kerro tilausnumerosi.'},
'fr':{
'h':['Informations de livraison','Options de livraison standard et express','Où nous livrons','Délais de traitement et de livraison','Suivi de commande','Douanes, droits et taxes à l’importation','Questions fréquentes sur la livraison'],
1:'<strong>Dress Like Mommy</strong> est une boutique en ligne qui expédie des tenues familiales assorties vers les destinations disponibles au moment du paiement, par l’intermédiaire de ses partenaires de transport et de préparation des commandes. Voici comment vérifier la livraison, ses délais et le suivi avant de commander.',
5:'La disponibilité de la livraison dépend du pays/de la région et de l’adresse saisis lors du paiement. Si un mode de livraison est affiché pour votre adresse, nous pouvons y livrer selon le mode et le tarif indiqués.',
6:'Si votre destination n’apparaît pas au moment du paiement, ou si aucun mode de livraison n’est proposé, écrivez-nous à {e} avant de commander.',
9:'Les délais estimés varient selon la destination, le transporteur, le dédouanement et le mode de livraison affiché lors du paiement. Vérifiez le mode de livraison et l’estimation indiqués avant de passer commande.',
10:'La mise à jour du suivi peut prendre 24-48 heures après l’émission du numéro de suivi.',
12:'Une fois votre commande expédiée, consultez vos e-mails pour obtenir les informations de suivi. Vous pouvez également accéder à votre compte ou utiliser le lien de suivi dans l’e-mail de confirmation d’expédition lorsqu’il est disponible.',
17:'<strong>Puis-je modifier mon adresse de livraison après avoir commandé ?</strong><br>Contactez-nous au plus vite à {e}. Si votre commande n’est pas encore entrée en préparation, nous pouvons vérifier si un changement d’adresse reste possible.',
18:'<strong>Livrez-vous aux boîtes postales ?</strong><br>La livraison aux boîtes postales dépend de la destination et des options de transporteur affichées lors du paiement.',
19:'<strong>Mon colis n’est pas encore arrivé.</strong><br>Consultez d’abord le lien de suivi. Si le suivi n’a pas été mis à jour depuis plusieurs jours ouvrables ou si la date estimée de livraison est dépassée, envoyez-nous un e-mail avec votre numéro de commande.'},
'he':{
'h':['מידע על משלוחים','אפשרויות משלוח רגיל ומהיר','לאן אנחנו שולחים','זמני טיפול ומשלוח','מעקב אחר הזמנה','מכס, היטלים ומסי יבוא','שאלות נפוצות על משלוחים'],
1:'<strong>Dress Like Mommy</strong> היא חנות מקוונת ששולחת בגדים תואמים למשפחות ליעדים הזמינים בתהליך התשלום, באמצעות שותפי המשלוח והטיפול בהזמנות שלנו. כאן מוסבר כיצד לבדוק את המשלוח, מועד המסירה והמעקב לפני ביצוע הזמנה.',
5:'זמינות המשלוח נקבעת לפי המדינה/האזור והכתובת שהוזנו בתהליך התשלום. אם מוצגת שיטת משלוח לכתובת שלכם, נוכל לשלוח אליה בשיטה ובמחיר המוצגים.',
6:'אם היעד שלכם אינו מופיע בתהליך התשלום, או שלא מוצגת שיטת משלוח, כתבו לנו אל {e} לפני ההזמנה.',
9:'הערכות זמני המסירה משתנות לפי היעד, חברת השילוח, הטיפול במכס ושיטת המשלוח המוצגת בתהליך התשלום. בדקו את שיטת המשלוח ואת ההערכה המוצגות לפני ביצוע ההזמנה.',
10:'עדכון המעקב עשוי להימשך 24-48 שעות לאחר הנפקת מספר המעקב.',
12:'לאחר שליחת ההזמנה, בדקו את הדוא״ל לקבלת פרטי המעקב. אפשר גם להיכנס לחשבון שלכם או להשתמש בקישור המעקב שבדוא״ל אישור המשלוח, כאשר הוא זמין.',
17:'<strong>האם אפשר לשנות את כתובת המשלוח לאחר ההזמנה?</strong><br>צרו איתנו קשר בהקדם האפשרי בכתובת {e}. אם ההזמנה טרם עברה לשלב הטיפול לביצוע, נוכל לבדוק אם שינוי הכתובת עדיין אפשרי.',
18:'<strong>האם אתם שולחים לתיבות דואר?</strong><br>אפשרות המשלוח לתיבות דואר תלויה ביעד ובאפשרויות חברות השילוח המוצגות בתהליך התשלום.',
19:'<strong>החבילה שלי עדיין לא הגיעה.</strong><br>בדקו תחילה את קישור המעקב. אם המעקב לא עודכן במשך כמה ימי עסקים או שהמועד המשוער למסירה חלף, שלחו לנו דוא״ל עם מספר ההזמנה.'},
}
D.update({
'hi':{
'h':['शिपिंग की जानकारी','मानक और एक्सप्रेस शिपिंग के विकल्प','हम कहाँ भेजते हैं','प्रसंस्करण और डिलीवरी का समय','ऑर्डर ट्रैकिंग','सीमा शुल्क, शुल्क और आयात कर','शिपिंग संबंधी आम प्रश्न'],
1:'<strong>Dress Like Mommy</strong> एक ऑनलाइन स्टोर है, जो अपने शिपिंग और ऑर्डर पूरा करने वाले साझेदारों के माध्यम से परिवार के मेल खाते कपड़े चेकआउट पर उपलब्ध गंतव्यों तक भेजता है। ऑर्डर देने से पहले शिपिंग, डिलीवरी के समय और ट्रैकिंग की पुष्टि करने का तरीका यहाँ दिया गया है।',
5:'शिपिंग की उपलब्धता चेकआउट पर दर्ज देश/क्षेत्र और पते पर निर्भर करती है। यदि आपके पते के लिए शिपिंग का कोई तरीका दिखता है, तो हम दिखाए गए तरीके और दर पर वहाँ भेज सकते हैं।',
6:'यदि आपका गंतव्य चेकआउट पर नहीं दिखता या शिपिंग का कोई तरीका नहीं दिखाया जाता, तो ऑर्डर देने से पहले हमें {e} पर ईमेल करें।',
9:'अनुमानित डिलीवरी का समय गंतव्य, वाहक, सीमा शुल्क प्रक्रिया और चेकआउट पर दिखाए गए शिपिंग के तरीके के अनुसार बदलता है। ऑर्डर देने से पहले दिखाए गए शिपिंग के तरीके और डिलीवरी के अनुमान की जाँच करें।',
10:'ट्रैकिंग नंबर जारी होने के बाद ट्रैकिंग अपडेट होने में 24-48 घंटे लग सकते हैं।',
12:'ऑर्डर भेजे जाने के बाद ट्रैकिंग की जानकारी के लिए अपना ईमेल देखें। आप अपने खाते पर भी जा सकते हैं या उपलब्ध होने पर शिपिंग की पुष्टि वाले ईमेल में दिए ट्रैकिंग लिंक का उपयोग कर सकते हैं।',
17:'<strong>क्या मैं ऑर्डर देने के बाद शिपिंग का पता बदल सकता हूँ?</strong><br>जितनी जल्दी हो सके {e} पर हमसे संपर्क करें। यदि आपका ऑर्डर अभी तक उसे पूरा करने के चरण में नहीं पहुँचा है, तो हम जाँच सकते हैं कि पता बदलना अब भी संभव है या नहीं।',
18:'<strong>क्या आप पी.ओ. बॉक्स पर भेजते हैं?</strong><br>पी.ओ. बॉक्स पर शिपिंग की उपलब्धता गंतव्य और चेकआउट पर दिखाए गए वाहक विकल्पों पर निर्भर करती है।',
19:'<strong>मेरा पैकेज अभी तक नहीं पहुँचा है।</strong><br>पहले अपना ट्रैकिंग लिंक देखें। यदि कई कार्यदिवसों से ट्रैकिंग अपडेट नहीं हुई है या अनुमानित डिलीवरी का समय बीत चुका है, तो अपने ऑर्डर नंबर के साथ हमें ईमेल करें।'},
'ja':{
'h':['配送について','通常配送と速達配送の選択肢','配送可能な地域','注文処理と配送にかかる時間','注文の追跡','税関、関税、輸入税','配送に関するよくある質問'],
1:'<strong>Dress Like Mommy</strong>は、配送・注文処理パートナーを通じて、ご購入手続き時に表示される配送先へ家族のおそろい服をお届けするオンラインストアです。ご注文前に、配送の可否、お届け時期、追跡方法を確認する手順をご案内します。',
5:'配送の可否は、ご購入手続き時に入力した国・地域と住所に基づきます。その住所に利用できる配送方法が表示される場合、表示された方法と料金で配送できます。',
6:'ご購入手続きで配送先が表示されない場合、または配送方法が表示されない場合は、ご注文前に{e}までメールでご連絡ください。',
9:'お届け予定は、配送先、配送業者、通関手続き、ご購入手続き時に表示される配送方法によって異なります。注文を確定する前に、表示された配送方法とお届け予定をご確認ください。',
10:'追跡番号の発行後、追跡情報の更新に24-48時間かかる場合があります。',
12:'ご注文の発送後、追跡情報が届いているかメールをご確認ください。アカウントにアクセスするか、発送確認メールに追跡リンクがある場合はそのリンクをご利用いただくこともできます。',
17:'<strong>注文後に配送先住所を変更できますか？</strong><br>できるだけ早く{e}までご連絡ください。ご注文がまだ出荷手配の段階に進んでいない場合、住所変更が引き続き可能かどうか確認できます。',
18:'<strong>私書箱に配送できますか？</strong><br>私書箱への配送の可否は、配送先とご購入手続き時に表示される配送業者の選択肢によって異なります。',
19:'<strong>荷物がまだ届きません。</strong><br>まず追跡リンクをご確認ください。数営業日にわたり追跡情報が更新されない場合や、お届け予定を過ぎた場合は、注文番号を添えてメールでご連絡ください。'},
'ko':{
'h':['배송 안내','일반 및 특급 배송 옵션','배송 가능 지역','주문 처리 및 배송 기간','주문 배송 조회','통관, 관세 및 수입세','배송 관련 자주 묻는 질문'],
1:'<strong>Dress Like Mommy</strong>는 배송 및 주문 이행 파트너를 통해 결제 단계에서 이용 가능한 배송지로 가족이 맞춰 입는 옷을 보내는 온라인 스토어입니다. 주문 전에 배송 가능 여부, 예상 배송 기간, 배송 조회 방법을 확인하는 방법을 안내합니다.',
5:'배송 가능 여부는 결제 시 입력한 국가/지역과 주소에 따라 결정됩니다. 해당 주소의 배송 방법이 표시되면 표시된 방법과 요금으로 배송할 수 있습니다.',
6:'결제 단계에서 배송지가 나타나지 않거나 배송 방법이 표시되지 않으면 주문 전에 {e}로 이메일을 보내 주세요.',
9:'예상 배송 기간은 배송지, 배송업체, 통관 절차 및 결제 시 표시되는 배송 방법에 따라 달라집니다. 주문하기 전에 결제 단계에 표시된 배송 방법과 예상 기간을 확인하세요.',
10:'운송장 번호 발급 후 배송 조회 정보가 업데이트되기까지 24-48시간이 걸릴 수 있습니다.',
12:'주문이 발송되면 이메일에서 배송 조회 정보를 확인하세요. 계정에 접속하거나 발송 확인 이메일에 배송 조회 링크가 제공되는 경우 해당 링크를 이용할 수도 있습니다.',
17:'<strong>주문 후 배송지 주소를 변경할 수 있나요?</strong><br>가능한 한 빨리 {e}로 연락해 주세요. 주문이 아직 이행 단계로 넘어가지 않았다면 주소 변경이 여전히 가능한지 확인할 수 있습니다.',
18:'<strong>사서함으로 배송하나요?</strong><br>사서함 배송 가능 여부는 배송지와 결제 시 표시되는 배송업체 옵션에 따라 달라집니다.',
19:'<strong>택배가 아직 도착하지 않았어요.</strong><br>먼저 배송 조회 링크를 확인하세요. 여러 영업일 동안 조회 정보가 업데이트되지 않았거나 예상 배송일이 지났다면 주문 번호를 포함하여 이메일을 보내 주세요.'},
'nl':{
'h':['Verzendinformatie','Standaard- en expresverzending','Waarheen we verzenden','Verwerkings- en levertijden','Je bestelling volgen','Douane, invoerrechten en invoerbelastingen','Veelgestelde vragen over verzending'],
1:'<strong>Dress Like Mommy</strong> is een webwinkel die via onze verzend- en afhandelingspartners bijpassende gezinsoutfits verstuurt naar bestemmingen die bij het afrekenen beschikbaar zijn. Hier lees je hoe je de verzending, levertijd en tracking controleert voordat je bestelt.',
5:'De beschikbaarheid van verzending hangt af van het land/de regio en het adres die bij het afrekenen zijn ingevoerd. Als er voor je adres een verzendmethode wordt getoond, kunnen we daarheen verzenden met de weergegeven methode en tegen het weergegeven tarief.',
6:'Als je bestemming niet verschijnt bij het afrekenen of er geen verzendmethode wordt getoond, mail ons dan vóór het bestellen op {e}.',
9:'De geschatte levertijden verschillen per bestemming, vervoerder, douaneafhandeling en verzendmethode die bij het afrekenen wordt getoond. Controleer de weergegeven verzendmethode en geschatte levertijd voordat je bestelt.',
10:'Het kan 24-48 uur na de afgifte van het trackingnummer duren voordat de tracking wordt bijgewerkt.',
12:'Controleer je e-mail op trackinginformatie zodra je bestelling is verzonden. Je kunt ook je account bezoeken of de trackinglink in de verzendbevestiging gebruiken wanneer die beschikbaar is.',
17:'<strong>Kan ik mijn verzendadres na het bestellen wijzigen?</strong><br>Neem zo snel mogelijk contact op via {e}. Als je bestelling nog niet in de afhandelingsfase zit, kunnen we nagaan of een adreswijziging nog mogelijk is.',
18:'<strong>Verzenden jullie naar postbussen?</strong><br>Verzending naar postbussen hangt af van de bestemming en de vervoerdersopties die bij het afrekenen worden getoond.',
19:'<strong>Mijn pakket is nog niet aangekomen.</strong><br>Controleer eerst je trackinglink. Als de tracking al enkele werkdagen niet is bijgewerkt of de geschatte leverdatum voorbij is, mail ons dan met je bestelnummer.'},
'no':{
'h':['Fraktinformasjon','Standard- og ekspressfrakt','Hvor vi sender','Behandlings- og leveringstider','Ordresporing','Toll, avgifter og importskatter','Vanlige spørsmål om frakt'],
1:'<strong>Dress Like Mommy</strong> er en nettbutikk som sender matchende familieantrekk til destinasjoner som er tilgjengelige i kassen, gjennom våre partnere for frakt og ordrebehandling. Her kan du se hvordan du bekrefter frakt, leveringstid og sporing før du bestiller.',
5:'Tilgjengelig frakt avhenger av landet/regionen og adressen som oppgis i kassen. Hvis det vises en fraktmetode for adressen din, kan vi sende dit med metoden og prisen som vises.',
6:'Hvis destinasjonen din ikke vises i kassen, eller hvis ingen fraktmetode vises, send oss en e-post til {e} før du bestiller.',
9:'Anslått leveringstid varierer med destinasjon, transportør, tollbehandling og fraktmetoden som vises i kassen. Kontroller metoden og leveringsanslaget som vises før du legger inn bestillingen.',
10:'Det kan ta 24-48 timer før sporingen oppdateres etter at sporingsnummeret er utstedt.',
12:'Når bestillingen er sendt, sjekk e-posten din for sporingsinformasjon. Du kan også besøke kontoen din eller bruke sporingslenken i e-posten med forsendelsesbekreftelsen når den er tilgjengelig.',
17:'<strong>Kan jeg endre leveringsadressen etter bestilling?</strong><br>Kontakt oss så snart som mulig på {e}. Hvis bestillingen ennå ikke har gått videre til ordreekspedisjon, kan vi undersøke om det fortsatt er mulig å endre adressen.',
18:'<strong>Sender dere til postbokser?</strong><br>Om vi kan sende til postbokser, avhenger av destinasjonen og transportøralternativene som vises i kassen.',
19:'<strong>Pakken min har ikke kommet ennå.</strong><br>Sjekk sporingslenken først. Hvis sporingen ikke har blitt oppdatert på flere virkedager eller den anslåtte leveringstiden har passert, send oss en e-post med ordrenummeret ditt.'},
'pl':{
'h':['Informacje o wysyłce','Opcje wysyłki standardowej i ekspresowej','Dokąd wysyłamy','Czas realizacji i dostawy','Śledzenie zamówienia','Odprawa celna, cła i podatki importowe','Często zadawane pytania o wysyłkę'],
1:'<strong>Dress Like Mommy</strong> to sklep internetowy, który za pośrednictwem partnerów zajmujących się wysyłką i realizacją zamówień dostarcza dopasowane stroje rodzinne do miejsc dostępnych podczas składania zamówienia. Oto jak sprawdzić wysyłkę, termin dostawy i śledzenie przed zakupem.',
5:'Dostępność wysyłki zależy od kraju/regionu oraz adresu podanych przy finalizacji zamówienia. Jeśli wyświetla się metoda wysyłki dla Twojego adresu, możemy wysłać tam zamówienie wyświetloną metodą i według podanej stawki.',
6:'Jeśli miejsce docelowe nie pojawia się przy finalizacji zamówienia lub nie wyświetla się metoda wysyłki, napisz do nas na {e} przed zakupem.',
9:'Szacowany termin dostawy zależy od miejsca docelowego, przewoźnika, odprawy celnej oraz metody wysyłki wyświetlanej przy finalizacji zamówienia. Przed złożeniem zamówienia sprawdź wyświetloną metodę i przewidywany termin dostawy.',
10:'Aktualizacja śledzenia może potrwać 24-48 godzin od nadania numeru przesyłki.',
12:'Po wysłaniu zamówienia sprawdź e-mail z informacjami o śledzeniu. Możesz też odwiedzić swoje konto lub skorzystać z linku do śledzenia w potwierdzeniu wysyłki, jeśli jest dostępny.',
17:'<strong>Czy mogę zmienić adres dostawy po złożeniu zamówienia?</strong><br>Skontaktuj się z nami jak najszybciej pod adresem {e}. Jeśli zamówienie nie przeszło jeszcze do etapu realizacji, możemy sprawdzić, czy zmiana adresu jest nadal możliwa.',
18:'<strong>Czy wysyłacie do skrytek pocztowych?</strong><br>Dostępność wysyłki do skrytek pocztowych zależy od miejsca docelowego i opcji przewoźnika wyświetlanych przy finalizacji zamówienia.',
19:'<strong>Moja paczka jeszcze nie dotarła.</strong><br>Najpierw sprawdź link do śledzenia. Jeśli informacje nie były aktualizowane od kilku dni roboczych lub minął przewidywany termin dostawy, napisz do nas e-mail z numerem zamówienia.'},
'ru':{
'h':['Информация о доставке','Варианты стандартной и экспресс-доставки','Куда мы доставляем','Сроки обработки и доставки','Отслеживание заказа','Таможня, пошлины и налоги на импорт','Частые вопросы о доставке'],
1:'<strong>Dress Like Mommy</strong> — интернет-магазин, который через партнёров по доставке и исполнению заказов отправляет семейную одежду в едином стиле по направлениям, доступным при оформлении заказа. Здесь объясняется, как до заказа проверить возможность доставки, её сроки и отслеживание.',
5:'Возможность доставки зависит от страны/региона и адреса, указанных при оформлении заказа. Если для вашего адреса отображается способ доставки, мы можем отправить заказ этим способом и по указанному тарифу.',
6:'Если ваш пункт назначения не отображается при оформлении заказа или не указан способ доставки, до заказа напишите нам на {e}.',
9:'Ориентировочные сроки зависят от места назначения, перевозчика, таможенного оформления и способа доставки, указанного при оформлении заказа. Перед заказом проверьте отображаемый способ доставки и предполагаемый срок.',
10:'После выдачи номера отслеживания обновление информации может занять 24-48 часов.',
12:'После отправки заказа проверьте электронную почту: там будут сведения для отслеживания. Вы также можете зайти в свой аккаунт или воспользоваться ссылкой в письме с подтверждением отправки, если она доступна.',
17:'<strong>Можно ли изменить адрес доставки после оформления заказа?</strong><br>Как можно скорее свяжитесь с нами по адресу {e}. Если заказ ещё не перешёл на этап исполнения, мы можем проверить, остаётся ли возможность изменить адрес.',
18:'<strong>Доставляете ли вы на абонентские ящики?</strong><br>Возможность доставки на абонентские ящики зависит от места назначения и вариантов перевозчика, указанных при оформлении заказа.',
19:'<strong>Моя посылка ещё не пришла.</strong><br>Сначала проверьте ссылку для отслеживания. Если сведения не обновлялись несколько рабочих дней или предполагаемый срок доставки прошёл, напишите нам по электронной почте, указав номер заказа.'},
'sv':{
'h':['Fraktinformation','Alternativ för standard- och expressfrakt','Vart vi skickar','Hanterings- och leveranstider','Spåra din beställning','Tull, avgifter och importskatter','Vanliga frågor om frakt'],
1:'<strong>Dress Like Mommy</strong> är en nätbutik som skickar matchande familjekläder till de destinationer som är tillgängliga i kassan, genom våra frakt- och orderhanteringspartner. Här ser du hur du kontrollerar frakt, leveranstid och spårning innan du beställer.',
5:'Tillgänglig frakt beror på landet/regionen och adressen som anges i kassan. Om en fraktmetod visas för din adress kan vi skicka dit med den metod och till det pris som visas.',
6:'Om din destination inte visas i kassan eller om ingen fraktmetod visas, mejla oss på {e} innan du beställer.',
9:'Beräknade leveranstider varierar beroende på destination, transportör, tullhantering och fraktmetoden som visas i kassan. Kontrollera den visade metoden och leveransuppskattningen innan du beställer.',
10:'Det kan ta 24-48 timmar innan spårningen uppdateras efter att spårningsnumret har utfärdats.',
12:'När beställningen har skickats hittar du spårningsinformationen i din e-post. Du kan också besöka ditt konto eller använda spårningslänken i leveransbekräftelsen när den finns tillgänglig.',
17:'<strong>Kan jag ändra leveransadressen efter beställningen?</strong><br>Kontakta oss så snart som möjligt på {e}. Om beställningen ännu inte har gått vidare till expediering kan vi undersöka om det fortfarande går att ändra adressen.',
18:'<strong>Skickar ni till postboxar?</strong><br>Om leverans till postboxar är möjlig beror på destinationen och de transportörsalternativ som visas i kassan.',
19:'<strong>Mitt paket har inte kommit fram ännu.</strong><br>Kontrollera spårningslänken först. Om spårningen inte har uppdaterats på flera arbetsdagar eller den beräknade leveranstiden har passerat, mejla oss med ditt ordernummer.'}
})

def policy_map(locale):
    if locale not in ['da','he','ko']:
        return json.loads((HERE/f'cache_{locale}.json').read_text())[locale]
    if locale=='da':
        p=HERE.parent.parent/'2026-09-22-danish-localization/policy_translation_plan.json'
        plans=json.loads(p.read_text())['plans']
        row=next(x for x in plans if x['resourceId']=='gid://shopify/ShopPolicy/29845782625')['rows'][0]
    else:
        row=next(x for x in json.loads((HERE/f'{locale}_manual.json').read_text())['rows'] if x['resourceId']=='gid://shopify/ShopPolicy/29845782625')
    src=re.findall(r'<p>.*?</p>',row['source'],re.S);dst=re.findall(r'<p>.*?</p>',row['value'],re.S)
    assert len(src)==len(dst),(locale,len(src),len(dst))
    return dict(zip(src,dst))

if __name__=='__main__':
    pending=json.loads((HELP/'shipping_pending.json').read_text())['rows'];out=[];checks=[]
    for row in pending:
        locale=row['locale'];values=D[locale];old=[s for s in row['source'].splitlines() if s];assert len(old)==20
        translated={}
        for index,label in zip([0,2,4,7,11,13,16],values['h']):
            tag='h2' if index==0 else 'h3';translated[index]=f'<{tag}>{label}</{tag}>'
        for index,body in values.items():
            if isinstance(index,int):translated[index]='<p>'+body.replace('{e}',EMAIL)+'</p>'
        cache=policy_map(locale)
        for index in [3,8,15]:
            assert old[index] in cache,(locale,index,'missing exact existing paragraph')
            translated[index]=cache[old[index]]
        equivalent=[s for s in cache if s.startswith('<p>For orders shipped outside the United States,')]
        assert len(equivalent)==1,(locale,'missing customs equivalent')
        translated[14]=cache[equivalent[0]]
        assert set(translated)==set(range(20))
        cursor=0;result=[]
        for line in row['source'].splitlines(keepends=True):
            if line.strip():
                result.append(translated[cursor]+ ('\n' if line.endswith('\n') else ''));cursor+=1
            else:result.append(line)
        value=''.join(result)
        assert re.findall(r'<[^>]+>',value)==re.findall(r'<[^>]+>',row['source']),(locale,'markup')
        assert collections.Counter(re.findall(r'\d+',value))==collections.Counter(re.findall(r'\d+',row['source'])),(locale,'numbers')
        assert re.findall(r'href="([^"]+)"',value)==re.findall(r'href="([^"]+)"',row['source']),(locale,'href')
        assert not re.search(r'QZXTOKEN|QXZ|DLMSEP|\{e\}',value)
        out.append(dict(row,value=value,reviewStatus='AUTHOR_PREPARED_FOR_INDEPENDENT_REVIEW',provenance='Human-authored new copy;3 exact cached policy paragraphs and1 semantically equivalent customs paragraph reused; entirely offline'))
        checks.append({'locale':locale,'sourceBinding':True,'markup':True,'numericValues':True,'href':True,'humanAuthoredNewParagraphs':9,'exactReusedParagraphs':3,'equivalentCustomsParagraph':1})
    result={'status':'LOCAL_CANDIDATE_NOT_APPLIED','scope':'Exactly16shipping-info body_html rows; Danishincluded only this page; source shipping conditions preserved','rows':out,'checks':checks,'limitations':'Requires independent semantic review and fresh source/destination readback by parent. No external writes.'}
    path=HELP/'shipping_manual.json';path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('READY',len(out),'SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
