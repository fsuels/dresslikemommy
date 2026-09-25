#!/usr/bin/env python3
"""Local author review of policy headings, garment exclusions and markup boundaries."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
edits=[]
audit=json.loads((HERE/'audit_fields.json').read_text())['fields']
sources=list(dict.fromkeys(s for r in audit for s in r['source'].splitlines()))
def source(prefix):
    x=[s for s in sources if s.startswith(prefix)];assert len(x)==1,(prefix,len(x));return x[0]
def put(l,s,v):
    f=HERE/f'cache_{l}.json';a=json.loads(f.read_text());a[l][s]=v;f.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');edits.append({'locale':l,'source':s,'value':v,'reason':'Human semantic/heading/markup-boundary review'})
refund={
'ar':['الإرجاع &amp; الاستبدال','مهلة الإرجاع','شروط الإرجاع','سلع لا يمكن إرجاعها','كيفية بدء الإرجاع','استرداد الأموال','الاستبدال','السلع التالفة أو المعيبة','المبالغ المستردة المتأخرة أو غير المستلمة','تكاليف الشحن','هل لديك أسئلة؟'],
'cs':['Vrácení &amp; výměna zboží','Lhůta pro vrácení','Podmínky vrácení','Zboží, které nelze vrátit','Jak zahájit vrácení','Vrácení peněz','Výměna zboží','Poškozené nebo vadné zboží','Opožděné nebo chybějící vrácení peněz','Náklady na dopravu','Máte otázky?'],
'de':['Rückgabe &amp; Umtausch','Rückgabefrist','Voraussetzungen für die Rückgabe','Von der Rückgabe ausgeschlossene Artikel','So veranlassen Sie eine Rückgabe','Rückerstattungen','Umtausch','Beschädigte oder defekte Artikel','Verspätete oder fehlende Rückerstattungen','Versandkosten','Fragen?'],
'el':['Επιστροφές &amp; αλλαγές','Προθεσμία επιστροφής','Προϋποθέσεις επιστροφής','Είδη που δεν επιστρέφονται','Πώς να ξεκινήσετε μια επιστροφή','Επιστροφές χρημάτων','Αλλαγές','Κατεστραμμένα ή ελαττωματικά είδη','Καθυστερημένες ή μη ληφθείσες επιστροφές χρημάτων','Έξοδα αποστολής','Έχετε ερωτήσεις;'],
'es':['Devoluciones &amp; cambios','Plazo de devolución','Condiciones para devolver artículos','Artículos que no se pueden devolver','Cómo iniciar una devolución','Reembolsos','Cambios','Artículos dañados o defectuosos','Reembolsos retrasados o no recibidos','Gastos de envío','¿Tienes preguntas?'],
'fi':['Palautukset &amp; vaihdot','Palautusaika','Palautuksen ehdot','Tuotteet, joita ei voi palauttaa','Palautuksen aloittaminen','Rahojen palautus','Tuotteiden vaihto','Vahingoittuneet tai vialliset tuotteet','Myöhästyneet tai puuttuvat maksunpalautukset','Toimituskulut','Kysyttävää?'],
'fr':['Retours &amp; échanges','Délai de retour','Conditions de retour','Articles ne pouvant pas être retournés','Comment demander un retour','Remboursements','Échanges','Articles endommagés ou défectueux','Remboursements retardés ou non reçus','Frais de livraison','Des questions ?'],
'hi':['वापसी &amp; बदलाव','वापसी की समय-सीमा','वापसी की पात्रता','वापस न किए जा सकने वाले सामान','वापसी की प्रक्रिया कैसे शुरू करें','धनवापसी','सामान बदलना','क्षतिग्रस्त या दोषपूर्ण सामान','विलंबित या न मिली धनवापसी','शिपिंग लागत','कोई प्रश्न?'],
'it':['Resi &amp; cambi','Termine per il reso','Condizioni per il reso','Articoli non restituibili','Come richiedere un reso','Rimborsi','Cambi','Articoli danneggiati o difettosi','Rimborsi in ritardo o non ricevuti','Spese di spedizione','Domande?'],
'ja':['返品 &amp; 交換','返品の受付期間','返品の条件','返品できない商品','返品の申請方法','返金','商品の交換','破損品・不良品','返金の遅延・未入金','送料','ご質問はありますか？'],
'nl':['Retouren &amp; omruilen','Retourtermijn','Voorwaarden voor retourzendingen','Artikelen die niet kunnen worden geretourneerd','Een retour aanvragen','Terugbetalingen','Omruilen','Beschadigde of defecte artikelen','Vertraagde of ontbrekende terugbetalingen','Verzendkosten','Vragen?'],
'no':['Retur &amp; bytte','Returfrist','Vilkår for retur','Varer som ikke kan returneres','Slik starter du en retur','Refusjoner','Bytte','Skadde eller defekte varer','Forsinkede eller manglende refusjoner','Fraktkostnader','Spørsmål?'],
'pl':['Zwroty &amp; wymiany','Termin zwrotu','Warunki zwrotu','Produkty, których nie można zwrócić','Jak rozpocząć zwrot','Zwroty pieniędzy','Wymiana produktów','Uszkodzone lub wadliwe produkty','Opóźnione lub nieotrzymane zwroty pieniędzy','Koszty wysyłki','Pytania?'],
'pt-BR':['Devoluções &amp; trocas','Prazo para devolução','Condições para devolução','Itens que não podem ser devolvidos','Como solicitar uma devolução','Reembolsos','Trocas','Itens danificados ou com defeito','Reembolsos atrasados ou não recebidos','Custos de envio','Dúvidas?'],
'ro':['Retururi &amp; schimburi','Termenul de retur','Condiții pentru retur','Articole care nu pot fi returnate','Cum inițiați un retur','Rambursări','Schimburi de produse','Articole deteriorate sau defecte','Rambursări întârziate sau neprimite','Costuri de expediere','Întrebări?'],
'ru':['Возврат &amp; обмен','Срок возврата','Условия возврата','Товары, не подлежащие возврату','Как оформить возврат','Возврат денежных средств','Обмен товаров','Повреждённые или дефектные товары','Задержка или отсутствие возврата средств','Стоимость доставки','Есть вопросы?'],
'sv':['Returer &amp; byten','Returfrist','Villkor för retur','Varor som inte kan returneras','Så begär du en retur','Återbetalningar','Byten','Skadade eller defekta varor','Försenade eller uteblivna återbetalningar','Fraktkostnader','Frågor?']}
original=['Returns &amp; Exchanges','Return Window','Eligibility','Non-Returnable Items','How to Start a Return','Refunds','Exchanges','Damaged or Defective Items','Late or Missing Refunds','Shipping Costs','Questions?']
for l,values in refund.items():
    for i,(s,v) in enumerate(zip(original,values)):
        tag='h2' if i==0 else 'h3';put(l,f'<{tag}>{s}</{tag}>',f'<{tag}>{v}</{tag}>')
underwear={
'ar':'ملابس السباحة والملابس الداخلية (لأسباب صحية)',
'cs':'Plavky a spodní prádlo (z hygienických důvodů)',
'de':'Bademode und Unterwäsche (aus hygienischen Gründen)',
'el':'Μαγιό και εσώρουχα (για λόγους υγιεινής)',
'es':'Trajes de baño y ropa interior (por motivos de higiene)',
'fi':'Uima-asut ja alusvaatteet (hygieniasyistä)',
'fr':'Maillots de bain et sous-vêtements (pour des raisons d’hygiène)',
'hi':'तैराकी के कपड़े और अंतर्वस्त्र (स्वच्छता संबंधी कारणों से)',
'it':'Costumi da bagno e biancheria intima (per motivi igienici)',
'ja':'水着と下着（衛生上の理由）',
'nl':'Zwemkleding en ondergoed (om hygiënische redenen)',
'no':'Badetøy og undertøy (av hygieniske grunner)',
'pl':'Stroje kąpielowe i bielizna (ze względów higienicznych)',
'pt-BR':'Roupas de banho e roupas íntimas (por motivos de higiene)',
'ro':'Costume de baie și lenjerie intimă (din motive de igienă)',
'ru':'Купальники и нижнее бельё (по гигиеническим соображениям)',
'sv':'Badkläder och underkläder (av hygieniska skäl)'}
for l,v in underwear.items():put(l,'<li>Swimwear and intimates (for hygiene reasons)</li>','<li>'+v+'</li>')
heads={
'cs':{'<h1>Privacy Policy</h1>':'<h1>Zásady ochrany osobních údajů</h1>','<h2>Order Tracking</h2>':'<h2>Sledování objednávky</h2>'},
'de':{'<h2>10. International Transfers</h2>':'<h2>10. Internationale Datenübermittlungen</h2>','<h2>11. Indemnification</h2>':'<h2>11. Freistellung</h2>'},
'fr':{'<h2>10. International Transfers</h2>':'<h2>10. Transferts internationaux de données</h2>','<h2>Order Tracking</h2>':'<h2>Suivi des commandes</h2>'},
'fi':{'<h2>How Our Shipping Works</h2>':'<h2>Näin toimitus toimii</h2>','<h2>16. Severability</h2>':'<h2>16. Ehtojen osittainen pätemättömyys</h2>'},
'ja':{'<h2>17. Entire Agreement</h2>':'<h2>17. 完全合意</h2>'},
'pl':{'<h2>6. Returns and Refunds</h2>':'<h2>6. Zwroty towarów i pieniędzy</h2>'},
'ro':{'<h2>5. Shipping and Delivery</h2>':'<h2>5. Expediere și livrare</h2>'},
'ru':{'<h2>5. Shipping and Delivery</h2>':'<h2>5. Отправка и доставка</h2>'}}
for l,rows in heads.items():
    for s,v in rows.items():put(l,s,v)

# The following exact malformed initial-capital pattern was inspected in all 63 occurrences.
# Skip EMail: it is normalized explicitly to E-Mail, not stripped to Mail.
for l in refund:
    data=json.loads((HERE/f'cache_{l}.json').read_text())[l]
    for s,v in data.items():
        new=re.sub(r'(?<![\w])[A-Z]([A-ZÁČĎÉĚÍĽĹŇÓŘŠŤÚŮÝŽÅÄÖØÆ][a-zà-ž])',r'\1',v.replace('EMail-Marketing','E-Mail-Marketing'))
        if new!=v:put(l,s,new)

# Explicit corrections where a translated clause escaped its containing paragraph/list item.
fixes={
'de':{
'<li>Items returned after':'<li>Artikel, die nach 30 Tagen zurückgegeben werden</li>',
'<li>Our team will review':'<li>Unser Team prüft Ihre Anfrage und antwortet innerhalb von 1 Werktag</li>',
'<li>If approved, your refund':'<li>Bei Genehmigung wird die Rückerstattung innerhalb von <strong>5–10 Werktagen</strong> über Ihre ursprüngliche Zahlungsmethode bearbeitet</li>',
'<li>Depending on your bank':'<li>Je nach Bank kann es weitere 2–5 Werktage dauern, bis die Erstattung auf Ihrem Kontoauszug erscheint</li>',
'<li>Placing an order':'<li>Eine Bestellung ist ein Kaufangebot; wir können es nach eigenem Ermessen annehmen oder ablehnen</li>',
'<li>Returns accepted within':'<li>Rückgaben werden innerhalb von <strong>30 Tagen</strong> nach der Lieferung akzeptiert</li>',
'<li>Refunds processed to':'<li>Rückerstattungen werden innerhalb von <strong>5–10 Werktagen</strong> über die ursprüngliche Zahlungsmethode bearbeitet</li>',
'<p>These Terms are governed':'<p>Diese Bedingungen unterliegen den Gesetzen des <strong>Bundesstaates Florida</strong>. Alle Streitigkeiten sind vor den Gerichten von <strong>Collier County, Florida</strong> zu klären.</p>'},
'fi':{'<p>These Terms are governed':'<p>Näihin ehtoihin sovelletaan <strong>Floridan osavaltion</strong> lakeja. Mahdolliset riidat ratkaistaan alueen <strong>Collier County, Florida</strong> tuomioistuimissa.</p>'},
'fr':{'<p>These Terms are governed':'<p>Ces conditions sont régies par les lois de l’<strong>État de Floride</strong>. Tout litige sera tranché devant les tribunaux de <strong>Collier County, Florida</strong>.</p>'},
'hi':{
'<li>Items marked as':'<li>"Final Sale" के रूप में चिह्नित सामान</li>',
'<li>Product images are':'<li>उत्पाद की तस्वीरें यथासंभव सटीक हैं; स्क्रीन की सेटिंग्स के कारण रंग में थोड़ा अंतर हो सकता है</li>',
'<li>Payment is processed':'<li>भुगतान <strong>Shopify Payments</strong> (Stripe द्वारा संचालित) के माध्यम से सुरक्षित रूप से संसाधित किया जाता है</li>',
'<li>All prices include':'<li>सभी कीमतों में लागू छूट शामिल हैं; कर और शिपिंग शुल्क चेकआउट के समय गणना किए जाते हैं</li>',
'<p>For full return details':'<p>वापसी की पूरी जानकारी के लिए हमारी <a href="https://dresslikemommy.com/policies/refund-policy">वापसी नीति</a> देखें।</p>',
'<p>These Terms are governed':'<p>ये शर्तें <strong>फ्लोरिडा राज्य</strong> के कानूनों द्वारा शासित हैं। किसी भी विवाद का निपटारा <strong>Collier County, Florida</strong> की अदालतों में किया जाएगा।</p>',
'<p>For shipping questions':'<p>शिपिंग संबंधी प्रश्नों के लिए <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> पर ईमेल करें।</p>'},
'ja':{
'<li>Items marked as':'<li>「Final Sale」と表示されている商品</li>',
'<li>Payment is processed':'<li>お支払いは <strong>Shopify Payments</strong>（Stripeを利用）を通じて安全に処理されます</li>',
'<p>For full return details':'<p>返品の詳細は、<a href="https://dresslikemommy.com/policies/refund-policy">返品ポリシー</a>をご覧ください。</p>',
'<p>These Terms are governed':'<p>本規約は<strong>フロリダ州</strong>の法律に準拠します。あらゆる紛争は、<strong>Collier County, Florida</strong>の裁判所で解決されるものとします。</p>',
'<p><em>Terms of Service':'<p><em>Dress Like Mommyの運営会社FKG Trading LLCによる利用規約。</em></p>',
'<p>For shipping questions':'<p>配送に関するご質問は、<a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>までメールでお問い合わせください。</p>'},
'nl':{'<li>Placing an order':'<li>Het plaatsen van een bestelling is een aanbod tot aankoop; wij kunnen dit naar eigen inzicht accepteren of weigeren</li>'}}
for l,rs in fixes.items():
    for prefix,v in rs.items():put(l,source(prefix),v)
for l,prefix in [('no','<p>We are not liable for delays'),('ru','<p>These Terms are governed')]:
    s=source(prefix);v=json.loads((HERE/f'cache_{l}.json').read_text())[l][s];put(l,s,v.rstrip('.'))

if __name__=='__main__':
    (HERE/'manual_policy_quality_log.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    print('Heading, exclusion and markup-boundary corrections:',len(edits))
