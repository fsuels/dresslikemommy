#!/usr/bin/env python3
"""Human-authored local translation corrections. No network or Shopify calls."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
audit=json.loads((HERE/'audit_fields.json').read_text())['fields']
sources=list(dict.fromkeys(part for r in audit for part in re.split(r'(\n+)',r['source']) if part.strip()))
edits=[]
def source(prefix):
    hits=[s for s in sources if s.startswith(prefix)]
    assert len(hits)==1,(prefix,len(hits))
    return hits[0]
def put(locale,src,value,reason='Human-authored semantic/markup repair'):
    assert locale not in ('en','da','he','ko')
    p=HERE/f'cache_{locale}.json';data=json.loads(p.read_text());data.setdefault(locale,{})[src]=value
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    edits.append({'locale':locale,'source':src,'value':value,'reason':reason})
def group(prefix,translations):
    s=source(prefix)
    for l,v in translations.items():put(l,s,v)

group('<h2>Returns &amp;',{'ar':'<h2>الإرجاع &amp; الاستبدال</h2>'})
group('<p><em>Last updated:',{'ar':'<p><em>آخر تحديث: يناير 2026</em></p>','ja':'<p><em>最終更新：2026年1月</em></p>'})
group('<li>Returns accepted within',{'ar':'<li>تُقبل المرتجعات خلال <strong>30 يومًا</strong> من التسليم</li>'})
group('<p>Your use of our site is also',{'ar':'<p>يخضع استخدامك لموقعنا أيضًا <a href="https://dresslikemommy.com/policies/privacy-policy">لسياسة الخصوصية</a>، التي تشرح كيفية جمع معلوماتك واستخدامها وحمايتها.</p>'})

group('<p>Email us at <strong>',{
'cs':'<p>Napište nám na <strong>info@dresslikemommy.com</strong> nebo zavolejte na <strong>(786) 309-6006</strong> (po–pá, 9 AM – 5 PM EST).</p>',
'el':'<p>Στείλτε μας email στο <strong>info@dresslikemommy.com</strong> ή καλέστε στο <strong>(786) 309-6006</strong> (Δευ–Παρ, 9 AM – 5 PM EST).</p>',
'fi':'<p>Lähetä sähköpostia osoitteeseen <strong>info@dresslikemommy.com</strong> tai soita numeroon <strong>(786) 309-6006</strong> (ma–pe, 9 AM – 5 PM EST).</p>',
'no':'<p>Send oss en e-post til <strong>info@dresslikemommy.com</strong> eller ring <strong>(786) 309-6006</strong> (man–fre, 9 AM – 5 PM EST).</p>',
'ro':'<p>Scrieți-ne la <strong>info@dresslikemommy.com</strong> sau sunați la <strong>(786) 309-6006</strong> (lun–vin, 9 AM – 5 PM EST).</p>',
'sv':'<p>Mejla oss på <strong>info@dresslikemommy.com</strong> eller ring <strong>(786) 309-6006</strong> (mån–fre, 9 AM – 5 PM EST).</p>'})
group('<p><strong>Dress Like Mommy</strong> is operated',{
'cs':'<p><strong>Dress Like Mommy</strong> provozuje společnost <strong>FKG Trading LLC</strong>, společnost s ručením omezeným založená na Floridě. Na vašem soukromí nám záleží — tyto zásady vysvětlují, jaké informace shromažďujeme, jak je používáme a jaká máte práva.</p>',
'el':'<p>Το <strong>Dress Like Mommy</strong> λειτουργεί από την <strong>FKG Trading LLC</strong>, εταιρεία περιορισμένης ευθύνης στη Φλόριντα. Το απόρρητό σας έχει σημασία για εμάς — αυτή η πολιτική εξηγεί ποιες πληροφορίες συλλέγουμε, πώς τις χρησιμοποιούμε και ποια είναι τα δικαιώματά σας.</p>',
'fi':'<p><strong>Dress Like Mommy</strong> -verkkokauppaa ylläpitää <strong>FKG Trading LLC</strong>, floridalainen rajoitetun vastuun yhtiö. Yksityisyytesi on meille tärkeää — tässä käytännössä kerrotaan, mitä tietoja keräämme, miten käytämme niitä ja mitä oikeuksia sinulla on.</p>',
'ro':'<p><strong>Dress Like Mommy</strong> este operat de <strong>FKG Trading LLC</strong>, o societate cu răspundere limitată din Florida. Confidențialitatea dumneavoastră contează pentru noi — această politică explică ce informații colectăm, cum le folosim și ce drepturi aveți.</p>'})
group('<li><strong>Payment information',{
'cs':'<li><strong>Platební údaje</strong> — údaje o kreditní/debetní kartě (bezpečně je zpracovává Shopify Payments; úplné číslo vaší karty nikdy nevidíme ani neukládáme)</li>',
'el':'<li><strong>Στοιχεία πληρωμής</strong> — στοιχεία πιστωτικής/χρεωστικής κάρτας (υποβάλλονται σε ασφαλή επεξεργασία από το Shopify Payments· δεν βλέπουμε ούτε αποθηκεύουμε ποτέ τον πλήρη αριθμό της κάρτας σας)</li>',
'fi':'<li><strong>Maksutiedot</strong> — luotto-/pankkikortin tiedot (Shopify Payments käsittelee ne turvallisesti; emme koskaan näe tai tallenna koko korttinumeroasi)</li>'})
group('<li><strong>Shopify Payments (Stripe)',{
'cs':'<li><strong>Shopify Payments (Stripe)</strong> — zpracování plateb v souladu s PCI-DSS</li>',
'el':'<li><strong>Shopify Payments (Stripe)</strong> — επεξεργασία πληρωμών σύμφωνα με το PCI-DSS</li>',
'fi':'<li><strong>Shopify Payments (Stripe)</strong> — PCI-DSS-vaatimusten mukainen maksujen käsittely</li>',
'fr':'<li><strong>Shopify Payments (Stripe)</strong> — traitement des paiements conforme à la norme PCI-DSS</li>',
'no':'<li><strong>Shopify Payments (Stripe)</strong> — betalingsbehandling i samsvar med PCI-DSS</li>',
'ro':'<li><strong>Shopify Payments (Stripe)</strong> — procesarea plăților conformă cu PCI-DSS</li>',
'sv':'<li><strong>Shopify Payments (Stripe)</strong> — betalningshantering som uppfyller PCI-DSS</li>'})
group('<p><strong>GDPR (EEA/UK/Switzerland):',{
'cs':'<p><strong>GDPR (EHP/Spojené království/Švýcarsko):</strong> Přenositelnost údajů, omezení zpracování nebo námitka proti němu, odvolání souhlasu a podání stížnosti.</p>',
'el':'<p><strong>GDPR (ΕΟΧ/Ηνωμένο Βασίλειο/Ελβετία):</strong> Φορητότητα δεδομένων, περιορισμός της επεξεργασίας ή εναντίωση σε αυτήν, ανάκληση συγκατάθεσης και υποβολή καταγγελιών.</p>',
'fi':'<p><strong>GDPR (ETA/Yhdistynyt kuningaskunta/Sveitsi):</strong> Tietojen siirtäminen järjestelmästä toiseen, käsittelyn rajoittaminen tai vastustaminen, suostumuksen peruuttaminen ja valituksen tekeminen.</p>',
'no':'<p><strong>GDPR (EØS/Storbritannia/Sveits):</strong> Dataportabilitet, begrensning av eller innsigelse mot behandling, tilbaketrekking av samtykke og innlevering av klager.</p>',
'ro':'<p><strong>GDPR (SEE/Regatul Unit/Elveția):</strong> Portabilitatea datelor, restricționarea prelucrării sau opoziția față de aceasta, retragerea consimțământului și depunerea de plângeri.</p>',
'sv':'<p><strong>GDPR (EES/Storbritannien/Schweiz):</strong> Dataportabilitet, begränsning av eller invändning mot behandling, återkallande av samtycke och inlämnande av klagomål.</p>'})
group('<p>Welcome to <strong>',{
'cs':'<p>Vítejte na <strong>Dress Like Mommy</strong> (dresslikemommy.com), které provozuje <strong>FKG Trading LLC</strong>, společnost s ručením omezeným založená na Floridě. Vstupem na naše webové stránky nebo odesláním objednávky souhlasíte s těmito podmínkami služby.</p>',
'el':'<p>Καλώς ήρθατε στο <strong>Dress Like Mommy</strong> (dresslikemommy.com), το οποίο λειτουργεί από την <strong>FKG Trading LLC</strong>, εταιρεία περιορισμένης ευθύνης στη Φλόριντα. Με την πρόσβαση στον ιστότοπό μας ή την υποβολή παραγγελίας, αποδέχεστε αυτούς τους Όρους Υπηρεσίας.</p>',
'fi':'<p>Tervetuloa <strong>Dress Like Mommy</strong> -verkkokauppaan (dresslikemommy.com), jota ylläpitää <strong>FKG Trading LLC</strong>, floridalainen rajoitetun vastuun yhtiö. Käyttämällä verkkosivustoamme tai tekemällä tilauksen hyväksyt nämä käyttöehdot.</p>',
'no':'<p>Velkommen til <strong>Dress Like Mommy</strong> (dresslikemommy.com), som drives av <strong>FKG Trading LLC</strong>, et selskap med begrenset ansvar i Florida. Ved å besøke nettstedet vårt eller legge inn en bestilling godtar du disse bruksvilkårene.</p>',
'ro':'<p>Bun venit la <strong>Dress Like Mommy</strong> (dresslikemommy.com), operat de <strong>FKG Trading LLC</strong>, o societate cu răspundere limitată din Florida. Accesând site-ul nostru sau plasând o comandă, acceptați acești Termeni și condiții.</p>',
'sv':'<p>Välkommen till <strong>Dress Like Mommy</strong> (dresslikemommy.com), som drivs av <strong>FKG Trading LLC</strong>, ett bolag med begränsat ansvar i Florida. Genom att besöka vår webbplats eller lägga en beställning godkänner du dessa användarvillkor.</p>'})
group('<p>If your destination does not appear',{
'cs':'<p>Pokud se vaše destinace nezobrazuje při placení nebo se pro vaši adresu nezobrazuje žádný způsob dopravy, kontaktujte nás před objednáním na <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>',
'el':'<p>Εάν ο προορισμός σας δεν εμφανίζεται στο ταμείο ή δεν εμφανίζεται μέθοδος αποστολής για τη διεύθυνσή σας, επικοινωνήστε μαζί μας στο <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> πριν παραγγείλετε.</p>',
'fi':'<p>Jos määränpääsi ei näy kassalla tai osoitteellesi ei näytetä toimitustapaa, ota meihin yhteyttä osoitteessa <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> ennen tilaamista.</p>'})
group('<p>All content on this website',{'de':'<p>Alle Inhalte dieser Website — einschließlich Texten, Bildern, Logos, Grafiken und Produktfotos — stehen im Eigentum von FKG Trading LLC oder sind an das Unternehmen lizenziert und durch Urheber- und Markenrechte geschützt. Sie dürfen unsere Inhalte ohne schriftliche Genehmigung weder vervielfältigen noch verbreiten oder nutzen.</p>'})
group('<p>Every order includes a tracking',{'de':'<p>Jede Bestellung enthält eine Sendungsverfolgungsnummer, sofern der Versanddienstleister eine bereitstellt. Nach der Vergabe der Nummer kann es 24-48 Stunden dauern, bis die Sendungsverfolgung aktualisiert wird.</p>'})
group('<p><strong>Dress Like Mommy sells',{'el':'<p><strong>Το Dress Like Mommy πουλά παιδικά ρούχα, αλλά ο ιστότοπός μας δεν απευθύνεται σε παιδιά.</strong> Όλες οι αγορές πρέπει να πραγματοποιούνται από ενήλικα (18+). Δεν συλλέγουμε εν γνώσει μας πληροφορίες από άτομα κάτω των 16 ετών (ή 13 ετών στις ΗΠΑ).</p>'})
group('<li>Payment is processed securely',{
'el':'<li>Η πληρωμή διεκπεραιώνεται με ασφάλεια μέσω του <strong>Shopify Payments</strong> (με την τεχνολογία της Stripe)</li>',
'fi':'<li>Maksu käsitellään turvallisesti <strong>Shopify Payments</strong> -palvelun kautta (palvelun tarjoaa Stripe)</li>'})
group('<li><strong>IP address',{'fr':'<li><strong>Adresse IP et localisation approximative</strong> (à l’échelle de la ville/région)</li>'})
group('<p>You must be at least',{
'fr':'<p>Vous devez avoir au moins <strong>18 ans</strong>, avoir la capacité juridique de conclure un accord contraignant et fournir des informations exactes. Bien que nous vendions des vêtements pour enfants, tous les achats doivent être effectués par un adulte.</p>',
'hi':'<p>आपकी आयु कम से कम <strong>18 वर्ष</strong> होनी चाहिए, आपके पास बाध्यकारी समझौता करने की कानूनी क्षमता होनी चाहिए और आपको सही जानकारी देनी होगी। हालाँकि हम बच्चों के कपड़े बेचते हैं, सभी खरीदारी किसी वयस्क द्वारा की जानी चाहिए।</p>',
'ja':'<p>ご利用には<strong>18歳以上</strong>であること、法的拘束力のある契約を締結する法的能力があること、および正確な情報を提供することが必要です。当店では子ども服を販売していますが、購入はすべて成人が行う必要があります。</p>'})
group('  <li><strong>Shipped:',{'fr':'  <li><strong>Expédiée :</strong> les informations de suivi sont envoyées par e-mail lorsqu’elles sont disponibles.</li>'})
group('<p>You have <strong>',{'ja':'<p>返品または交換は、配達日から<strong>30日以内</strong>にお申し込みください。</p>'})
group('<p><strong>Last Updated:',{'ja':'<p><strong>最終更新：</strong>2026年1月28日</p>'})
group('<p>You agree to indemnify',{'ja':'<p>お客様は、当サイトの利用、本規約への違反、または第三者の権利の侵害に起因するあらゆる請求、損害、費用について、FKG Trading LLCを補償し、免責することに同意するものとします。</p>'})
group('<p>Shopify servers may',{'ro':'<p>Serverele Shopify pot fi situate în afara țării dumneavoastră. Transferurile SEE/Regatul Unit/Elveția utilizează Clauzele contractuale standard.</p>'})

# Contact addresses and time values remain exact, while visible labels and weekdays localize.
contact=source('<h3>Dress Like Mommy</h3>')
labels={
'cs':['Majitel','E-mail','Telefon','Pondělí – pátek','Adresa'],
'de':['Inhaber','E-Mail','Telefon','Montag – Freitag','Adresse'],
'el':['Ιδιοκτήτης','Email','Τηλέφωνο','Δευτέρα – Παρασκευή','Διεύθυνση'],
'es':['Propietario','Correo electrónico','Teléfono','Lunes – viernes','Dirección'],
'fi':['Omistaja','Sähköposti','Puhelin','Maanantai – perjantai','Osoite'],
'fr':['Propriétaire','E-mail','Téléphone','Lundi – vendredi','Adresse'],
'no':['Eier','E-post','Telefon','Mandag – fredag','Adresse'],
'pt-BR':['Proprietário','E-mail','Telefone','Segunda – sexta-feira','Endereço'],
'ro':['Proprietar','E-mail','Telefon','Luni – vineri','Adresă'],
'sv':['Ägare','E-post','Telefon','Måndag – fredag','Adress']}
for l,values in labels.items():
    value=contact
    for old,new in zip(['Owner','Email','Phone','Monday – Friday','Address'],values):value=value.replace(old,new)
    put(l,contact,value)

if __name__=='__main__':
    (HERE/'manual_repairs_log.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    print('Local manual segment repairs:',len(edits))
