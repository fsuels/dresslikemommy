"""Canonical manual translations of two parent-approved FAQ source paragraphs.
Offline artifact authoring only; inputs/candidates/source documents are read-only.
"""
import hashlib
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent
H = R.parent / 'help-translations'
texts = {
 'ar': [
  'نشحن إلى البلدان والمناطق المعروضة عند إتمام الشراء. إذا لم يكن بلدك مدرجًا عند إتمام الشراء، فتواصل معنا قبل تقديم الطلب.',
  'قد يفرض بلد الوجهة رسومًا جمركية أو ضرائب استيراد أو رسومًا محلية، ويتحمل العميل مسؤوليتها، ما لم يُذكر صراحةً عند إتمام الشراء أنها مشمولة. لا يمكننا وضع علامة على الطلبات على أنها هدايا أو شحنات ذات قيمة أقل.',
 ],
 'cs': [
  'Zasíláme do zemí a regionů zobrazených při placení. Pokud vaše země není při placení uvedena, kontaktujte nás před zadáním objednávky.',
  'Cílová země může účtovat clo, dovozní daně nebo místní poplatky, za které odpovídá zákazník, pokud při placení není výslovně uvedeno, že jsou zahrnuty. Objednávky nemůžeme označovat jako dárky ani jako zásilky s nižší hodnotou.',
 ],
 'da': [
  'Vi sender til de lande og områder, der vises ved betaling. Hvis dit land ikke vises ved betaling, skal du kontakte os, før du afgiver en ordre.',
  'Destinationslandet kan opkræve told, importafgifter eller lokale gebyrer, som kunden er ansvarlig for, medmindre det udtrykkeligt fremgår ved betaling, at de er inkluderet. Vi kan ikke mærke ordrer som gaver eller angive en lavere værdi for forsendelserne.',
 ],
 'de': [
  'Wir versenden in die Länder und Regionen, die beim Bezahlvorgang angezeigt werden. Wenn Ihr Land dort nicht aufgeführt ist, kontaktieren Sie uns bitte vor der Bestellung.',
  'Ihr Zielland kann Zölle, Einfuhrsteuern oder lokale Gebühren erheben. Diese trägt der Kunde, sofern beim Bezahlvorgang nicht ausdrücklich angegeben wird, dass sie enthalten sind. Wir können Bestellungen nicht als Geschenke oder als Sendungen mit niedrigerem Wert deklarieren.',
 ],
 'el': [
  'Αποστέλλουμε στις χώρες και τις περιοχές που εμφανίζονται κατά την ολοκλήρωση της αγοράς. Αν η χώρα σας δεν εμφανίζεται εκεί, επικοινωνήστε μαζί μας πριν υποβάλετε παραγγελία.',
  'Η χώρα προορισμού μπορεί να επιβάλλει τελωνειακούς δασμούς, φόρους εισαγωγής ή τοπικά τέλη, για τα οποία ευθύνεται ο πελάτης, εκτός αν αναφέρεται ρητά κατά την ολοκλήρωση της αγοράς ότι περιλαμβάνονται. Δεν μπορούμε να δηλώσουμε τις παραγγελίες ως δώρα ή ως αποστολές χαμηλότερης αξίας.',
 ],
 'es': [
  'Enviamos a los países y regiones que aparecen al finalizar la compra. Si tu país no figura allí, ponte en contacto con nosotros antes de realizar un pedido.',
  'El país de destino puede cobrar aranceles aduaneros, impuestos de importación o tasas locales, que son responsabilidad del cliente, salvo que al finalizar la compra se indique expresamente que están incluidos. No podemos marcar los pedidos como regalos ni como envíos de menor valor.',
 ],
 'fi': [
  'Toimitamme kassalla näkyviin maihin ja alueille. Jos maasi ei näy kassalla, ota meihin yhteyttä ennen tilaamista.',
  'Määrämaa saattaa periä tullimaksuja, tuontiveroja tai paikallisia maksuja, joista asiakas vastaa, ellei kassalla nimenomaisesti ilmoiteta niiden sisältyvän hintaan. Emme voi merkitä tilauksia lahjoiksi tai arvoltaan todellista pienemmiksi lähetyksiksi.',
 ],
 'fr': [
  'Nous livrons dans les pays et régions affichés lors du paiement. Si votre pays ne figure pas dans la liste au moment du paiement, contactez-nous avant de passer commande.',
  'Votre pays de destination peut appliquer des droits de douane, des taxes à l’importation ou des frais locaux, qui sont à la charge du client, sauf s’il est expressément indiqué lors du paiement qu’ils sont inclus. Nous ne pouvons pas déclarer les commandes comme des cadeaux ni comme des envois de valeur inférieure.',
 ],
 'he': [
  'אנו שולחים למדינות ולאזורים המוצגים בקופה. אם מדינתכם אינה מופיעה בקופה, צרו איתנו קשר לפני ביצוע ההזמנה.',
  'מדינת היעד עשויה לגבות מכס, מיסי יבוא או אגרות מקומיות, והאחריות לתשלומם היא של הלקוח, אלא אם מצוין במפורש בקופה שהם כלולים. איננו יכולים לסמן הזמנות כמתנות או כמשלוחים בעלי ערך נמוך יותר.',
 ],
 'hi': [
  'हम चेकआउट पर दिखाए गए देशों और क्षेत्रों में शिपिंग करते हैं। यदि आपका देश चेकआउट की सूची में नहीं है, तो ऑर्डर देने से पहले हमसे संपर्क करें।',
  'गंतव्य देश सीमा शुल्क, आयात कर या स्थानीय शुल्क लगा सकता है, जिनकी ज़िम्मेदारी ग्राहक की होती है, जब तक कि चेकआउट पर स्पष्ट रूप से न कहा गया हो कि वे शामिल हैं। हम ऑर्डर को उपहार या कम मूल्य वाले शिपमेंट के रूप में चिह्नित नहीं कर सकते।',
 ],
 'it': [
  'Spediamo nei paesi e nelle regioni mostrati al momento del pagamento. Se il tuo paese non compare, contattaci prima di effettuare un ordine.',
  'Il paese di destinazione può applicare dazi doganali, imposte sulle importazioni o oneri locali, che sono a carico del cliente, salvo che al momento del pagamento sia espressamente indicato che sono inclusi. Non possiamo contrassegnare gli ordini come regali o come spedizioni di valore inferiore.',
 ],
 'ja': [
  '購入手続き画面に表示される国と地域へ発送しています。お住まいの国が購入手続き画面に表示されない場合は、ご注文前にお問い合わせください。',
  '配送先の国で関税、輸入税、現地の手数料が課される場合があり、購入手続き画面で含まれていると明示されている場合を除き、お客様のご負担となります。ご注文を贈答品として申告したり、実際より低い金額の貨物として申告したりすることはできません。',
 ],
 'ko': [
  '결제 화면에 표시되는 국가와 지역으로 배송합니다. 결제 화면에 고객님의 국가가 표시되지 않으면 주문 전에 문의해 주세요.',
  '배송지 국가에서 관세, 수입세 또는 현지 수수료를 부과할 수 있으며, 결제 화면에 포함되어 있다고 명시된 경우를 제외하고 해당 비용은 고객 부담입니다. 주문을 선물로 표시하거나 실제보다 낮은 금액의 배송품으로 신고할 수 없습니다.',
 ],
 'nl': [
  'We verzenden naar de landen en regio’s die bij het afrekenen worden weergegeven. Staat je land daar niet bij, neem dan contact met ons op voordat je een bestelling plaatst.',
  'Het land van bestemming kan douanerechten, invoerbelastingen of lokale kosten in rekening brengen. Deze zijn voor rekening van de klant, tenzij bij het afrekenen uitdrukkelijk wordt vermeld dat ze inbegrepen zijn. We kunnen bestellingen niet als cadeau of als zending met een lagere waarde aangeven.',
 ],
 'no': [
  'Vi sender til landene og områdene som vises i kassen. Hvis landet ditt ikke er oppført i kassen, må du kontakte oss før du legger inn en bestilling.',
  'Destinasjonslandet kan kreve toll, importavgifter eller lokale gebyrer. Kunden er ansvarlig for disse, med mindre det uttrykkelig står i kassen at de er inkludert. Vi kan ikke merke bestillinger som gaver eller oppgi en lavere verdi på forsendelsene.',
 ],
 'pl': [
  'Wysyłamy do krajów i regionów widocznych podczas finalizacji zakupu. Jeśli Twojego kraju nie ma na tej liście, skontaktuj się z nami przed złożeniem zamówienia.',
  'Kraj docelowy może naliczyć cło, podatki importowe lub opłaty lokalne, za które odpowiada klient, chyba że podczas finalizacji zakupu wyraźnie wskazano, że są one wliczone. Nie możemy oznaczać zamówień jako prezentów ani jako przesyłek o niższej wartości.',
 ],
 'pt-BR': [
  'Enviamos para os países e regiões exibidos na finalização da compra. Se o seu país não estiver na lista, entre em contato conosco antes de fazer um pedido.',
  'O país de destino pode cobrar taxas alfandegárias, impostos de importação ou taxas locais, que são de responsabilidade do cliente, a menos que a finalização da compra informe expressamente que estão incluídos. Não podemos declarar os pedidos como presentes nem como remessas de valor inferior.',
 ],
 'ro': [
  'Livrăm în țările și regiunile afișate la finalizarea comenzii. Dacă țara dumneavoastră nu apare în listă la finalizarea comenzii, contactați-ne înainte de a plasa o comandă.',
  'Țara de destinație poate percepe taxe vamale, impozite la import sau taxe locale, care sunt în responsabilitatea clientului, cu excepția cazului în care la finalizarea comenzii se precizează explicit că sunt incluse. Nu putem declara comenzile drept cadouri sau drept expedieri cu o valoare mai mică.',
 ],
 'ru': [
  'Мы отправляем заказы в страны и регионы, указанные при оформлении заказа. Если вашей страны нет в списке при оформлении, свяжитесь с нами до размещения заказа.',
  'В стране назначения могут взиматься таможенные пошлины, налоги на импорт или местные сборы. Их оплачивает покупатель, если при оформлении заказа прямо не указано, что они включены. Мы не можем указывать заказы как подарки или как отправления с заниженной стоимостью.',
 ],
 'sv': [
  'Vi skickar till de länder och regioner som visas i kassan. Om ditt land inte finns med i kassan ber vi dig kontakta oss innan du beställer.',
  'Destinationslandet kan ta ut tull, importskatter eller lokala avgifter, som kunden ansvarar för, om det inte uttryckligen står i kassan att de ingår. Vi kan inte märka beställningar som gåvor eller ange ett lägre värde på försändelserna.',
 ],
}

source_file = H / 'english_source_updates.json'
source_row = next(x for x in json.loads(source_file.read_text())['rows'] if x['id'] == 'gid://shopify/Page/161933381')
paragraphs = re.findall(r'<p\b[^>]*>.*?</p>', source_row['body'], re.S)
expected = {
 25: '<p>We ship to the countries and regions shown at checkout. If your country is not listed at checkout, contact us before placing an order.</p>',
 31: "<p>Customs duties, import taxes, or local fees may be charged by your destination country and are the customer's responsibility, unless checkout explicitly says they are included. We cannot mark orders as gifts or lower-value shipments.</p>",
}
assert len(paragraphs) == 70
for index, value in expected.items():
    assert paragraphs[index] == value
assert len(texts) == 20 and 'en' not in texts
rows = []
for locale, values in texts.items():
    rows.append({
        'resourceId': source_row['id'], 'locale': locale, 'key': 'body_html',
        'paragraphCountExpected': 70,
        'canonicalParagraphs': [
            {'paragraphIndexZeroBased': index, 'source': expected[index], 'value': '<p>' + value + '</p>',
             'role': 'destination_availability' if index == 25 else 'customs_responsibility_with_checkout_inclusion_exception'}
            for index, value in zip([25, 31], values)
        ],
    })
    for p in rows[-1]['canonicalParagraphs']:
        assert re.findall('<[^>]*>', p['value']) == ['<p>', '</p>']
        assert not re.search(r'QZX\w*|https?://|\d', p['value'])

ship = json.loads((H / 'shipping_pending.json').read_text())['rows'][0]['source']
customs = next(x for x in re.findall(r'<p>.*?</p>', ship, re.S) if 'These are the customer' in x)
assert 'unless checkout explicitly says they are included' in customs
out = {
    'status': 'REVIEWED_CANONICAL_PARAGRAPHS_NOT_APPLIED',
    'sourceArtifact': str(source_file),
    'sourceBodySha256': hashlib.sha256(source_row['body'].encode()).hexdigest(),
    'rows': rows,
    'counts': {'locales': 20, 'paragraphs': 40},
    'checks': {'all20NonEnglishLocales': True, 'sourceParagraphsExact': True, 'paragraphCount70': True, 'eachReplacementSingleP': True, 'noPlaceholderTokensOrInventedNumbers': True},
    'shippingInfoEnglishCustomsSource': customs,
    'notes': [
        'Parent-approved source alignment only. Apply canonical new paragraphs by locale/resource/key and zero-based p index, not by old wording; earlier repairs may already be integrated.',
        'Require exactly70 p elements and verify adjacent destination/customs questions before replacement. These are p25 and p31 when blank p elements are counted.',
        'All20 non-English published locales included, including Danish. No English candidate or source edited here.',
        'Customer responsibility remains conditional: destination may charge, except where checkout explicitly includes charges. Gift/undervaluation prohibition retained.',
        'shipping-info captured English source already includes the same checkout exception and needs no matching source repair.',
        'Parent must refresh sourceDigest after applying English source update. This artifact deliberately does not reuse the old digest.',
        'No external calls and no candidate edits.',
    ],
}
path = R / 'final_faq_destination_customs_20.json'
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'locales':20,'paragraphs':40,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
