"""Offline review artifact only. Does not edit candidate inputs or call providers."""
import hashlib
import html
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent
H = R.parent / 'help-translations'

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def blocks(s):
    return [x for x in re.findall(r'<(?:p|h[23]|li)\b[^>]*>.*?</(?:p|h[23]|li)>', s, re.S)
            if html.unescape(re.sub('<[^>]*>', '', x)).strip()]

def link(label):
    return '<a href="https://www.dresslikemommy.com/policies/shipping-policy" alt="Shipping Policy">' + label + '</a>'

EMAIL = '<a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>'

# Exact source-role replacements; six FAQ and five About Us blocks per locale.
T = {
 'ar': {
  3: 'نعم. تستضيف Shopify عملية إتمام الشراء بشكل آمن، وتدعم وسائل الدفع المعروضة عند إتمام الشراء. لا نخزن تفاصيل بطاقتك الكاملة على موقعنا.',
  25: 'نشحن حاليًا إلى البلدان المدرجة في سياسة الشحن لدينا. إذا لم يكن بلدك مدرجًا عند إتمام الشراء، فتواصل معنا قبل تقديم الطلب.',
  27: 'تختلف أوقات معالجة الطلب والنقل باختلاف الوجهة وشركة الشحن. راجع ' + link('سياسة الشحن') + ' للاطلاع على تفاصيل الشحن الحالية قبل إتمام الشراء.',
  29: 'قد يفرض بلد الوجهة رسومًا جمركية أو ضرائب استيراد أو رسومًا محلية، ويتحمل العميل مسؤوليتها. لا يمكننا وضع علامة على الطلبات على أنها هدايا أو شحنات ذات قيمة أقل.',
  61: 'يرجى التواصل معنا على ' + EMAIL + ' وتزويدنا برقم طلبك. تخضع عمليات الاستبدال المعتمدة لسياسة الاسترداد الحالية، بما في ذلك متطلبات حالة المنتجات ومسؤولية تكاليف شحن الإرجاع.',
  63: 'يرجى التواصل معنا على ' + EMAIL + ' وتزويدنا برقم طلبك. راجع سياسة الاسترداد لمعرفة شروط الأهلية وشحن الإرجاع ومواعيد الاسترداد قبل إعادة أي شيء.',
  'a3': 'نشأت Dress Like Mommy من فكرة عائلية لدى فرانسيسكو في Naples، فلوريدا: الفرحة التي كانت تشعر بها بناته عندما يرتدين ملابس متناسقة مع والدتهن. تلك الشرارة — الضحكات والصور ولحظات «نرتدي ملابس متشابهة!» — أصبحت جوهر عمل يهدف إلى التقريب بين العائلات من خلال الأزياء.',
  'a7': 'نخدم العائلات في الولايات المتحدة وكندا والمملكة المتحدة وأستراليا. سواء كان الأمر يتعلق ببيجامات متناسقة في صباح عيد الميلاد، أو جلسة تصوير عائلية، أو يوم ممتع ترتدي فيه ملابس متناسقة مع طفلك، يقصدنا عملاؤنا للحصول على ملابس متناسقة تجعل ارتداء الملابس معًا أسهل.',
  'a13': '<strong>تنسيق ملابس العائلة بسهولة</strong> — ملابس متناسقة للصور والأعياد والرحلات واللحظات اليومية',
  'a14': '<strong>إرجاع سهل</strong> — إرشادات واضحة للإرجاع والاستبدال في سياسة الاسترداد لدينا',
  'a21': '<em>Dress Like Mommy — نجعل لحظات العائلة أكثر تميزًا.</em>',
 },
 'cs': {
  3: 'Ano. Pokladnu bezpečně provozuje Shopify a podporuje platební metody zobrazené při placení. Na našich stránkách neukládáme úplné údaje o vaší kartě.',
  25: 'Aktuálně zasíláme do zemí uvedených v našich přepravních podmínkách. Pokud vaše země není při placení uvedena, kontaktujte nás před zadáním objednávky.',
  27: 'Doba zpracování a přepravy se liší podle místa doručení a dopravce. Před placením si přečtěte aktuální informace v našich ' + link('přepravních podmínkách') + '.',
  29: 'Cílová země může účtovat clo, dovozní daně nebo místní poplatky, za které odpovídá zákazník. Objednávky nemůžeme označovat jako dárky ani jako zásilky s nižší hodnotou.',
  61: 'Kontaktujte nás na ' + EMAIL + ' a uveďte číslo objednávky. Schválené výměny se řídí aktuálními podmínkami vrácení peněz, včetně požadavků na stav zboží a odpovědnosti za zpáteční přepravu.',
  63: 'Kontaktujte nás na ' + EMAIL + ' a uveďte číslo objednávky. Před odesláním čehokoli zpět si přečtěte podmínky vrácení peněz, kde najdete informace o způsobilosti k vrácení, zpáteční přepravě a lhůtách pro vrácení peněz.',
  'a3': 'Dress Like Mommy vyrostlo z Franciscova rodinného nápadu v Naples na Floridě: z radosti jeho dcer, když měly sladěné oblečení s maminkou. Tato jiskra — smích, fotografie a chvíle „vypadáme jako dvojčata!“ — se stala srdcem podniku, který prostřednictvím módy sbližuje rodiny.',
  'a7': 'Sloužíme rodinám ve Spojených státech, Kanadě, Spojeném království a Austrálii. Ať jde o sladěná pyžama na vánoční ráno, rodinné focení nebo zábavný den ve stejném oblečení s vaším dítětem, naši zákazníci k nám přicházejí pro sladěné outfity, které usnadňují společné oblékání.',
  'a13': '<strong>Sladit rodinu je snadné</strong> — Sladěné oblečení na focení, svátky, výlety i každodenní chvíle',
  'a14': '<strong>Snadné vrácení</strong> — Jasné pokyny k vrácení a výměně v našich podmínkách vrácení peněz',
  'a21': '<em>Dress Like Mommy — Děláme rodinné okamžiky ještě výjimečnějšími.</em>',
 },
 'da': {
  3: 'Ja. Betalingen foregår sikkert hos Shopify og understøtter de betalingsmetoder, der vises ved betaling. Vi gemmer ikke dine fulde kortoplysninger på vores hjemmeside.',
  25: 'Vi sender i øjeblikket til de lande, der er angivet i vores fragtpolitik. Hvis dit land ikke vises ved betaling, skal du kontakte os, før du afgiver en ordre.',
  27: 'Behandlings- og transporttider varierer efter destination og transportør. Læs ' + link('fragtpolitikken') + ' for at få de aktuelle oplysninger om forsendelse, før du går til betaling.',
  29: 'Destinationslandet kan opkræve told, importafgifter eller lokale gebyrer, som kunden er ansvarlig for. Vi kan ikke mærke ordrer som gaver eller angive en lavere værdi for forsendelserne.',
  61: 'Kontakt os på ' + EMAIL + ', og oplys dit ordrenummer. Godkendte ombytninger følger den aktuelle refusionspolitik, herunder krav til varernes stand og ansvar for returfragten.',
  63: 'Kontakt os på ' + EMAIL + ', og oplys dit ordrenummer. Læs refusionspolitikken om betingelser for returnering, returfragt og refusionstider, før du sender noget retur.',
  'a3': 'Dress Like Mommy voksede ud af Franciscos familieidé i Naples, Florida: den glæde, hans døtre følte, når de havde matchende tøj på med deres mor. Den gnist — latteren, billederne og øjeblikkene med ”vi matcher!” — blev kernen i en virksomhed, der bringer familier tættere sammen gennem mode.',
  'a7': 'Vi hjælper familier i USA, Canada, Storbritannien og Australien. Uanset om det gælder matchende nattøj julemorgen, en familiefotografering eller en sjov dag ude i matchende tøj med dit barn, kommer vores kunder til os efter koordineret tøj, der gør det lettere at klæde sig på sammen.',
  'a13': '<strong>Nemt at matche hele familien</strong> — Koordineret tøj til billeder, højtider, rejser og hverdagens øjeblikke',
  'a14': '<strong>Nem returnering</strong> — Klar vejledning om returnering og ombytning i vores refusionspolitik',
  'a21': '<em>Dress Like Mommy — Gør familiens øjeblikke endnu mere særlige.</em>',
 },
 'el': {
  3: 'Ναι. Η διαδικασία πληρωμής φιλοξενείται με ασφάλεια από το Shopify και υποστηρίζει τους τρόπους πληρωμής που εμφανίζονται κατά την ολοκλήρωση της αγοράς. Δεν αποθηκεύουμε τα πλήρη στοιχεία της κάρτας σας στον ιστότοπό μας.',
  25: 'Αυτή τη στιγμή αποστέλλουμε στις χώρες που αναφέρονται στην πολιτική αποστολών μας. Αν η χώρα σας δεν εμφανίζεται κατά την ολοκλήρωση της αγοράς, επικοινωνήστε μαζί μας πριν υποβάλετε παραγγελία.',
  27: 'Οι χρόνοι διεκπεραίωσης και μεταφοράς διαφέρουν ανάλογα με τον προορισμό και τον μεταφορέα. Διαβάστε την ' + link('πολιτική αποστολών') + ' για τις τρέχουσες πληροφορίες αποστολής πριν προχωρήσετε στην ολοκλήρωση της αγοράς.',
  29: 'Η χώρα προορισμού μπορεί να επιβάλλει τελωνειακούς δασμούς, φόρους εισαγωγής ή τοπικά τέλη, για τα οποία ευθύνεται ο πελάτης. Δεν μπορούμε να δηλώσουμε τις παραγγελίες ως δώρα ή ως αποστολές χαμηλότερης αξίας.',
  61: 'Επικοινωνήστε μαζί μας στο ' + EMAIL + ' και δώστε τον αριθμό της παραγγελίας σας. Οι εγκεκριμένες αλλαγές διέπονται από την ισχύουσα πολιτική επιστροφής χρημάτων, συμπεριλαμβανομένων των απαιτήσεων για την κατάσταση των ειδών και της ευθύνης για τα έξοδα επιστροφής.',
  63: 'Επικοινωνήστε μαζί μας στο ' + EMAIL + ' και δώστε τον αριθμό της παραγγελίας σας. Πριν στείλετε οτιδήποτε πίσω, διαβάστε την πολιτική επιστροφής χρημάτων για τις προϋποθέσεις επιστροφής, την αποστολή επιστροφής και τον χρόνο επιστροφής χρημάτων.',
  'a3': 'Το Dress Like Mommy αναπτύχθηκε από μια οικογενειακή ιδέα του Francisco στο Naples της Φλόριντα: τη χαρά που ένιωθαν οι κόρες του όταν φορούσαν ασορτί ρούχα με τη μαμά τους. Αυτή η σπίθα — τα γέλια, οι φωτογραφίες και οι στιγμές «φοράμε τα ίδια!» — έγινε η καρδιά μιας επιχείρησης αφιερωμένης στο να φέρνει τις οικογένειες πιο κοντά μέσα από τη μόδα.',
  'a7': 'Εξυπηρετούμε οικογένειες στις Ηνωμένες Πολιτείες, τον Καναδά, το Ηνωμένο Βασίλειο και την Αυστραλία. Είτε πρόκειται για ασορτί πιτζάμες το πρωί των Χριστουγέννων, μια οικογενειακή φωτογράφιση ή μια διασκεδαστική έξοδο με ασορτί ρούχα με το παιδί σας, οι πελάτες μας έρχονται σε εμάς για συνδυασμένα σύνολα που κάνουν το κοινό ντύσιμο πιο εύκολο.',
  'a13': '<strong>Εύκολοι συνδυασμοί για όλη την οικογένεια</strong> — Ασορτί ρούχα για φωτογραφίες, γιορτές, ταξίδια και καθημερινές στιγμές',
  'a14': '<strong>Εύκολες επιστροφές</strong> — Σαφείς οδηγίες για επιστροφές και αλλαγές στην πολιτική επιστροφής χρημάτων μας',
  'a21': '<em>Dress Like Mommy — Κάνουμε τις οικογενειακές στιγμές ακόμη πιο ξεχωριστές.</em>',
 },
 'fi': {
  3: 'Kyllä. Shopify tarjoaa turvallisen kassapalvelun, joka tukee kassalla näkyviä maksutapoja. Emme tallenna täydellisiä korttitietojasi sivustollemme.',
  25: 'Toimitamme tällä hetkellä toimituskäytännössämme lueteltuihin maihin. Jos maasi ei näy kassalla, ota meihin yhteyttä ennen tilaamista.',
  27: 'Käsittely- ja kuljetusajat vaihtelevat määränpään ja kuljetusliikkeen mukaan. Lue ajantasaiset toimitustiedot ' + link('toimituskäytännöstämme') + ' ennen kassalle siirtymistä.',
  29: 'Määrämaa saattaa periä tullimaksuja, tuontiveroja tai paikallisia maksuja, joista asiakas vastaa. Emme voi merkitä tilauksia lahjoiksi tai arvoltaan todellista pienemmiksi lähetyksiksi.',
  61: 'Ota meihin yhteyttä osoitteeseen ' + EMAIL + ' ja ilmoita tilausnumerosi. Hyväksyttyihin vaihtoihin sovelletaan voimassa olevaa hyvityskäytäntöämme, mukaan lukien tuotteiden kuntoa koskevat vaatimukset ja vastuu palautuskuluista.',
  63: 'Ota meihin yhteyttä osoitteeseen ' + EMAIL + ' ja ilmoita tilausnumerosi. Lue hyvityskäytännöstä palautusehdot, palautuskulut ja hyvityksen aikataulu ennen kuin lähetät mitään takaisin.',
  'a3': 'Dress Like Mommy kasvoi Franciscon perheideasta Naplesissa, Floridassa: ilosta, jota hänen tyttärensä tunsivat pukeutuessaan yhteensopiviin asuihin äitinsä kanssa. Tuo kipinä — nauru, valokuvat ja ”meillä on samanlaiset asut!” -hetket — muodostui sydämeksi yritykselle, joka tuo perheitä lähemmäs toisiaan muodin avulla.',
  'a7': 'Palvelemme perheitä Yhdysvalloissa, Kanadassa, Yhdistyneessä kuningaskunnassa ja Australiassa. Olipa kyseessä jouluaamun yhteensopiva pyjama, perhekuvaus tai hauska päivä lapsen kanssa samanlaisissa asuissa, asiakkaamme etsivät meiltä yhteensopivia vaatteita, jotka helpottavat yhdessä pukeutumista.',
  'a13': '<strong>Perheen asujen yhdistäminen on helppoa</strong> — Yhteensopivia vaatteita valokuviin, juhliin, matkoille ja arjen hetkiin',
  'a14': '<strong>Helpot palautukset</strong> — Selkeät palautus- ja vaihto-ohjeet hyvityskäytännössämme',
  'a21': '<em>Dress Like Mommy — Teemme perheen hetkistä entistä erityisempiä.</em>',
 },
 'he': {
  3: 'כן. תהליך התשלום מתארח באופן מאובטח אצל Shopify ותומך באמצעי התשלום המוצגים בקופה. איננו שומרים את פרטי הכרטיס המלאים שלכם באתר שלנו.',
  25: 'אנו שולחים כרגע למדינות הרשומות במדיניות המשלוחים שלנו. אם מדינתכם אינה מופיעה בקופה, צרו איתנו קשר לפני ביצוע ההזמנה.',
  27: 'זמני הטיפול וההובלה משתנים בהתאם ליעד ולחברת השילוח. עיינו ב' + link('מדיניות המשלוחים') + ' לקבלת פרטי המשלוח העדכניים לפני המעבר לקופה.',
  29: 'מדינת היעד עשויה לגבות מכס, מיסי יבוא או אגרות מקומיות, והאחריות לתשלומם היא של הלקוח. איננו יכולים לסמן הזמנות כמתנות או כמשלוחים בעלי ערך נמוך יותר.',
  61: 'צרו איתנו קשר בכתובת ' + EMAIL + ' וציינו את מספר ההזמנה. החלפות שאושרו כפופות למדיניות ההחזרים הכספיים העדכנית, כולל הדרישות למצב הפריטים והאחריות למשלוח ההחזרה.',
  63: 'צרו איתנו קשר בכתובת ' + EMAIL + ' וציינו את מספר ההזמנה. לפני שליחת פריט בחזרה, עיינו במדיניות ההחזרים הכספיים לקבלת מידע על הזכאות להחזרה, משלוח ההחזרה ומועדי ההחזר הכספי.',
  'a3': 'Dress Like Mommy צמחה מתוך רעיון משפחתי של Francisco בנייפלס, פלורידה: השמחה שבנותיו הרגישו כשהתלבשו בבגדים תואמים לאמא שלהן. הניצוץ הזה — הצחוקים, התמונות ורגעי ״אנחנו לבושות אותו הדבר!״ — הפך ללבו של עסק שנועד לקרב בין משפחות באמצעות אופנה.',
  'a7': 'אנו משרתים משפחות ברחבי ארצות הברית, קנדה, בריטניה ואוסטרליה. בין שמדובר בפיג׳מות תואמות בבוקר חג המולד, בצילומי משפחה או ביום כיף בבגדים תואמים עם הילד או הילדה שלכם, הלקוחות שלנו פונים אלינו לקבלת בגדים מתואמים שמקלים על ההתלבשות המשותפת.',
  'a13': '<strong>קל להתאים בגדים לכל המשפחה</strong> — בגדים מתואמים לצילומים, לחגים, לטיולים ולרגעי היומיום',
  'a14': '<strong>החזרות קלות</strong> — הנחיות ברורות להחזרות ולהחלפות במדיניות ההחזרים הכספיים שלנו',
  'a21': '<em>Dress Like Mommy — הופכים את רגעי המשפחה למיוחדים עוד יותר.</em>',
 },
 'hi': {
  3: 'हाँ। चेकआउट Shopify पर सुरक्षित रूप से होस्ट किया जाता है और इसमें चेकआउट पर दिखाई जाने वाली भुगतान विधियाँ उपलब्ध हैं। हम अपनी साइट पर आपके कार्ड का पूरा विवरण संग्रहीत नहीं करते।',
  25: 'फ़िलहाल हम अपनी शिपिंग नीति में सूचीबद्ध देशों में शिपिंग करते हैं। यदि आपका देश चेकआउट पर सूची में नहीं है, तो ऑर्डर देने से पहले हमसे संपर्क करें।',
  27: 'ऑर्डर संसाधित करने और परिवहन में लगने वाला समय गंतव्य तथा वाहक के अनुसार बदलता है। चेकआउट से पहले मौजूदा शिपिंग विवरण के लिए ' + link('शिपिंग नीति') + ' पढ़ें।',
  29: 'गंतव्य देश सीमा शुल्क, आयात कर या स्थानीय शुल्क लगा सकता है, जिनकी ज़िम्मेदारी ग्राहक की होती है। हम ऑर्डर को उपहार या कम मूल्य वाले शिपमेंट के रूप में चिह्नित नहीं कर सकते।',
  61: 'कृपया ' + EMAIL + ' पर हमसे संपर्क करें और अपना ऑर्डर नंबर दें। स्वीकृत एक्सचेंज मौजूदा रिफंड नीति के अनुसार होते हैं, जिसमें वस्तुओं की स्थिति से जुड़ी शर्तें और वापसी शिपिंग की ज़िम्मेदारी शामिल हैं।',
  63: 'कृपया ' + EMAIL + ' पर हमसे संपर्क करें और अपना ऑर्डर नंबर दें। कोई भी वस्तु वापस भेजने से पहले पात्रता, वापसी शिपिंग और रिफंड के समय के बारे में रिफंड नीति पढ़ें।',
  'a3': 'Dress Like Mommy की शुरुआत नेपल्स, फ़्लोरिडा में Francisco के एक पारिवारिक विचार से हुई: उनकी बेटियों को अपनी माँ के साथ मैचिंग कपड़े पहनकर जो खुशी मिलती थी। वही चिंगारी — हँसी, तस्वीरें और ”हम एक जैसे दिख रहे हैं!” वाले पल — फ़ैशन के ज़रिए परिवारों को करीब लाने के लिए समर्पित व्यवसाय का आधार बनी।',
  'a7': 'हम संयुक्त राज्य अमेरिका, कनाडा, यूनाइटेड किंगडम और ऑस्ट्रेलिया के परिवारों की सेवा करते हैं। चाहे क्रिसमस की सुबह मैचिंग पजामे पहनना हो, परिवार का फ़ोटोशूट हो या अपने बच्चे के साथ मैचिंग कपड़ों में बाहर घूमने का मज़ेदार दिन, हमारे ग्राहक ऐसे मेल खाते कपड़ों के लिए हमारे पास आते हैं जो साथ मिलकर तैयार होना आसान बनाते हैं।',
  'a13': '<strong>पूरे परिवार के लिए मैचिंग कपड़े चुनना आसान</strong> — तस्वीरों, त्योहारों, यात्राओं और रोज़मर्रा के पलों के लिए मेल खाते कपड़े',
  'a14': '<strong>आसान वापसी</strong> — हमारी रिफंड नीति में वापसी और एक्सचेंज के स्पष्ट निर्देश',
  'a21': '<em>Dress Like Mommy — परिवार के पलों को और भी खास बनाते हुए।</em>',
 },
}

rows = []
input_hashes = {}

def base_row(file, r):
    return {
        'inputFile': str(file), 'resourceId': r['resourceId'], 'locale': r['locale'],
        'key': r['key'], 'handle': r.get('handle'), 'sourceDigest': r['sourceDigest'],
        'sourceChangePending': r.get('sourceChangePending', False),
        'sourceSha256': sha(r['source']), 'reviewedValueSha256': sha(r['value']),
        'source': r['source'], 'beforeValue': r['value'], 'proposedValue': r['value'],
        'repairs': [],
    }

def change(out, before, after, source, reason):
    assert out['proposedValue'].count(before) == 1, (out['locale'], before)
    out['proposedValue'] = out['proposedValue'].replace(before, after)
    out['repairs'].append({'before': before, 'after': after, 'source': source, 'reason': reason})

file = H / 'faq_corrections_group_b.json'
input_hashes[str(file)] = sha(file.read_text())
group = json.loads(file.read_text())
for r in group['rows']:
    out = base_row(file, r)
    src, old = blocks(r['source']), blocks(r['value'])
    assert len(src) == len(old)
    if r['handle'] == 'faqs':
        for i in [3, 25, 27, 29, 61, 63]:
            change(out, old[i], '<p>' + T[r['locale']][i] + '</p>', src[i],
                   'Replace superseded claim with faithful translation of the corrected source; preserve current conditions, caveats, and negation.')
        extras = {
            'cs': {43: '<p><strong>3. Můj sledovací kód uvádí „platnost vypršela“</strong></p>'},
            'da': {32: '<p><strong>1. Hvad betyder ordrestatussen ”Ikke ekspederet”?</strong></p>',
                   34: '<p><strong>2. Hvad betyder ordrestatussen ”Ekspederet”?</strong></p>'},
            'fi': {6: '<p><strong>3. Missä sijaitsette?</strong></p>',
                   32: '<p><strong>1. Mitä tilauksen tila ”Käsittelemätön” tarkoittaa?</strong></p>',
                   34: '<p><strong>2. Mitä tilauksen tila ”Käsitelty” tarkoittaa?</strong></p>',
                   59: '<p>Ota meihin yhteyttä osoitteeseen ' + EMAIL + ' ja ilmoita tilausnumerosi. Jos virhe on meidän, voit lähettää tuotteet takaisin, ja lähetämme oikeat tuotteet omalla kustannuksellamme (tai hyvitämme maksun).</p>'},
        }
        for i, after in extras.get(r['locale'], {}).items():
            change(out, old[i], after, src[i], 'Correct malformed wording or ambiguous fulfillment/refund meaning without changing the source condition.')
    else:
        for i in [3, 7, 13, 14, 21]:
            tag = 'li' if i in [13, 14] else 'p'
            change(out, old[i], '<' + tag + '>' + T[r['locale']]['a' + str(i)] + '</' + tag + '>', src[i],
                   'Remove superseded founding-date/social-proof/return claims and translate the corrected source exactly in meaning.')
    rows.append(out)

# Read all Swedish15 fields. Quoted operational labels are retained with localized glosses.
file = H / 'sv_manual.json'
input_hashes[str(file)] = sha(file.read_text())
sv = json.loads(file.read_text())
for r in sv['rows']:
    if r['handle'] == 'faqs' and r['key'] == 'body_html':
        out = base_row(file, r)
        src, old = blocks(r['source']), blocks(r['value'])
        fixes = {
            32: '<p><strong>1. Vad betyder orderstatusen ”Unfulfilled” (inte expedierad)?</strong></p>',
            34: '<p><strong>2. Vad betyder orderstatusen ”Fulfilled” (expedierad)?</strong></p>',
            41: '<p><strong>2. Min spårningskod visar ”pending” (väntar) eller ”no information available at the moment” (ingen information tillgänglig just nu).</strong></p>',
            43: '<p><strong>3. Min spårningskod visar ”expired” (utgången)</strong></p>',
        }
        for i, after in fixes.items():
            change(out, old[i], after, src[i], 'Add Swedish meaning beside quoted English operational status label; retain label to identify the status shoppers may see.')
        rows.append(out)

file = R / 'candidate_17_locales.json'
input_hashes[str(file)] = sha(file.read_text())
consolidated = json.loads(file.read_text())
plan = next(p for p in consolidated['plans'] if p['locale'] == 'pl' and p['resourceId'].endswith('/14695685'))
r = dict(next(r for r in plan['rows'] if r['key'] == 'body'), resourceId=plan['resourceId'], locale='pl', handle='refund-policy')
out = base_row(file, r)
src, old = blocks(r['source']), blocks(r['value'])
assert len(src) == len(old)
fixes = [
 ('<p>Chcemy, aby Ty i Twoja rodzina pokochali pasujące stroje! Jeśli coś jest nie tak, jesteśmy tutaj, aby Ci pomóc.</p>', '<p>Chcemy, aby cała Twoja rodzina pokochała dopasowane do siebie stroje! Jeśli coś jest nie tak, jesteśmy tutaj, aby pomóc.</p>', 'Correct Polish agreement while retaining family-matching fashion meaning.'),
 ('<li><strong>Ewyślij do nas wiadomość e-mail</strong> na adres info@dresslikemommy.com, podając numer zamówienia i powód zwrotu</li>', '<li><strong>Wyślij do nas wiadomość e-mail</strong> na adres info@dresslikemommy.com, podając numer zamówienia i powód zwrotu</li>', 'Remove malformed leftover E prefix.'),
 ('<li>Wyślij przedmiot(y) z powrotem do oryginalnego opakowania</li>', '<li>Odeślij produkt lub produkty w oryginalnym opakowaniu</li>', 'Source requires shipment in original packaging, not shipment into packaging.'),
 ('<li>W zależności od banku pojawienie się na wyciągu może zająć dodatkowe 2–5 dni robocze</li>', '<li>W zależności od banku zaksięgowanie kwoty na wyciągu może zająć dodatkowe 2–5 dni roboczych</li>', 'Clarify the subject and correct Polish declension; preserve additional delay.'),
 ('<li>Enapisz do nas na info@dresslikemommy.com, a my zbadamy sprawę</li>', '<li>Napisz do nas na info@dresslikemommy.com, a my zbadamy sprawę</li>', 'Remove malformed leftover E prefix.'),
 ('<p>Enapisz do nas na <strong>info@dresslikemommy.com</strong> lub zadzwoń do <strong>(786) 309-6006</strong> (pon.–pt., 9 AM – 5 PM EST).</p>', '<p>Napisz do nas na <strong>info@dresslikemommy.com</strong> lub zadzwoń pod numer <strong>(786) 309-6006</strong> (pon.–pt., 9 AM – 5 PM EST).</p>', 'Remove malformed E prefix and correct phone preposition; retain literal schedule/time zone.'),
]
for before, after, reason in fixes:
    i = old.index(before)
    change(out, before, after, src[i], reason)
rows.append(out)

for out in rows:
    out['proposedValueSha256'] = sha(out['proposedValue'])
    out['check'] = {
        'blockCountSource': len(blocks(out['source'])),
        'blockCountProposed': len(blocks(out['proposedValue'])),
        'noPlaceholderTokens': not re.search(r'QZX\w*', out['proposedValue']),
        'uniqueExactReplacementPreconditionsPassed': True,
    }
    assert out['check']['blockCountSource'] == out['check']['blockCountProposed']
    # Each repair maintains source tag sequence. Attributes use corrected source for the shipping-policy link.
    for x in out['repairs']:
        tags = lambda s: re.findall(r'</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', s)
        assert tags(x['source']) == tags(x['after']), (out['locale'], x)

artifact = {
    'status': 'INDEPENDENT_REVIEW_REPAIRS_ONLY_NOT_APPLIED',
    'inputFileSha256': input_hashes,
    'reviewCoverage': {'faqCorrectionsGroupBRows': 14, 'swedishManualRows': 15, 'polishRefundBodies': 1},
    'reviewFindings': {
        'materialSupersededParagraphs': 77,
        'additionalGroupBWordingRepairs': 7,
        'swedishOperationalStatusGlosses': 4,
        'polishRefundWordingRepairs': 6,
        'unchangedSwedishRows': 14,
    },
    'rows': rows,
    'notes': [
        'No candidate file was edited and no external read/write/translation request was made.',
        'Parent owns integration. Match locale/resource/key plus source/value hashes before applying exact repairs; do not overwrite newer work.',
        'FAQ/About English source updates are still pending as indicated by inputs. Refresh sourceDigest after source changes before registration.',
        'Shipping-policy href uses the corrected English source destination. Parent should apply the existing same-locale href normalization after integration.',
        'Swedish contact-us faithfully retains source since2016 statement while About Us source removes that claim. This is a source-consistency issue, not a translation defect; parent decides source repair.',
        'Final Sale is preserved as a quoted item label inside nonreturnable lists; this is intentional label fidelity, not untranslated policy prose.',
        'No business condition, return exclusion, deadline, customs obligation, or negation was changed beyond translation of the exact corrected source.',
    ],
}
(R / 'independent_help_review_repairs.json').write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'rows': len(rows), 'repairs': sum(len(x['repairs']) for x in rows), 'sha256': sha((R/'independent_help_review_repairs.json').read_text())}))
