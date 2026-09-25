#!/usr/bin/env python3
from manual_repairs import put,source,edits,HERE
import json

# 'Sale items' means discounted merchandise, not everything offered for sale.
# 'Final sale' retains its no-return meaning rather than a literal end-of-sale event.
sale={
'ar':'السلع المخفضة والسلع المخصصة تُباع بيعًا نهائيًا ولا يمكن إرجاعها',
'cs':'Zlevněné zboží a zboží upravené na míru nelze vrátit',
'de':'Reduzierte und personalisierte Artikel sind von der Rückgabe ausgeschlossen',
'el':'Τα είδη σε έκπτωση και τα εξατομικευμένα είδη πωλούνται οριστικά και δεν επιστρέφονται',
'es':'Los artículos rebajados y personalizados son de venta final y no admiten devolución',
'fi':'Alennustuotteita ja yksilöllisesti muokattuja tuotteita ei voi palauttaa',
'fr':'Les articles soldés et personnalisés sont vendus définitivement et ne peuvent pas être retournés',
'hi':'छूट वाले और व्यक्तिगत रूप से तैयार किए गए सामान की बिक्री अंतिम है और उन्हें वापस नहीं किया जा सकता',
'it':'Gli articoli in saldo e quelli personalizzati sono venduti in via definitiva e non possono essere restituiti',
'ja':'セール品とカスタマイズ品は返品できません',
'nl':'Afgeprijsde en gepersonaliseerde artikelen kunnen niet worden geretourneerd',
'no':'Salgsvarer og personlig tilpassede varer kan ikke returneres',
'pl':'Produktów przecenionych i personalizowanych nie można zwrócić',
'pt-BR':'Itens em promoção e itens personalizados são de venda final e não podem ser devolvidos',
'ro':'Articolele reduse și cele personalizate sunt vândute definitiv și nu pot fi returnate',
'ru':'Товары со скидкой и персонализированные товары возврату не подлежат',
'sv':'Reavaror och personligt anpassade varor kan inte returneras'}
for l,v in sale.items():put(l,source('<li>Sale items and personalized'),'<li>'+v+'</li>','Correct sale-versus-for-sale and final-sale policy meaning')

conduct={
'ar':'تلتزم بالامتناع عن: استخدام الموقع لأغراض غير قانونية، أو التدخل في وظائف الموقع، أو محاولة الوصول غير المصرح به، أو تقديم معلومات كاذبة، أو استخدام أدوات آلية لاستخراج المحتوى، أو انتهاك حقوق الآخرين.',
'cs':'Zavazujete se, že nebudete: používat web k nezákonným účelům, zasahovat do jeho fungování, pokoušet se o neoprávněný přístup, poskytovat nepravdivé informace, používat automatizované nástroje ke sběru obsahu ani porušovat práva jiných osob.',
'de':'Sie verpflichten sich, Folgendes zu unterlassen: die Website für rechtswidrige Zwecke zu nutzen, ihre Funktionalität zu beeinträchtigen, unbefugten Zugriff zu versuchen, falsche Informationen zu übermitteln, Inhalte mit automatisierten Werkzeugen auszulesen oder die Rechte anderer zu verletzen.',
'el':'Δεσμεύεστε να μην κάνετε τα εξής: να χρησιμοποιείτε τον ιστότοπο για παράνομους σκοπούς, να παρεμβαίνετε στη λειτουργικότητά του, να επιχειρείτε μη εξουσιοδοτημένη πρόσβαση, να υποβάλλετε ψευδείς πληροφορίες, να χρησιμοποιείτε αυτοματοποιημένα εργαλεία για εξαγωγή περιεχομένου ή να παραβιάζετε τα δικαιώματα άλλων.',
'es':'Te comprometes a no utilizar el sitio con fines ilegales, interferir en su funcionamiento, intentar acceder sin autorización, enviar información falsa, usar herramientas automatizadas para extraer contenido ni infringir los derechos de otras personas.',
'fi':'Sitoudut siihen, ettet käytä sivustoa laittomiin tarkoituksiin, häiritse sen toimintaa, yritä päästä siihen luvatta, lähetä vääriä tietoja, käytä automaattisia työkaluja sisällön keräämiseen tai loukkaa muiden oikeuksia.',
'fr':'Vous vous engagez à ne pas utiliser le site à des fins illégales, perturber son fonctionnement, tenter un accès non autorisé, fournir de fausses informations, utiliser des outils automatisés pour extraire du contenu ni porter atteinte aux droits d’autrui.',
'hi':'आप निम्न कार्य न करने के लिए सहमत हैं: साइट का गैरकानूनी उद्देश्यों के लिए उपयोग करना, साइट के संचालन में बाधा डालना, अनधिकृत पहुँच का प्रयास करना, गलत जानकारी देना, सामग्री निकालने के लिए स्वचालित उपकरणों का उपयोग करना या दूसरों के अधिकारों का उल्लंघन करना।',
'it':'Ti impegni a non utilizzare il sito per scopi illeciti, interferire con il suo funzionamento, tentare accessi non autorizzati, fornire informazioni false, usare strumenti automatizzati per estrarre contenuti o violare i diritti altrui.',
'ja':'お客様は、サイトを違法な目的で利用すること、サイトの機能を妨害すること、不正アクセスを試みること、虚偽の情報を送信すること、自動化ツールを使ってコンテンツを収集すること、または他者の権利を侵害することを行わないことに同意します。',
'nl':'U verbindt zich ertoe de volgende handelingen achterwege te laten: de site voor onwettige doeleinden gebruiken, de werking ervan verstoren, ongeoorloofde toegang proberen te krijgen, onjuiste informatie indienen, geautomatiseerde hulpmiddelen gebruiken om inhoud te verzamelen of de rechten van anderen schenden.',
'no':'Du forplikter deg til ikke å bruke nettstedet til ulovlige formål, forstyrre funksjonaliteten, forsøke uautorisert tilgang, sende inn uriktige opplysninger, bruke automatiserte verktøy til å hente ut innhold eller krenke andres rettigheter.',
'pl':'Zobowiązujesz się nie używać witryny do celów niezgodnych z prawem, nie zakłócać jej działania, nie podejmować prób nieuprawnionego dostępu, nie podawać fałszywych informacji, nie korzystać z automatycznych narzędzi do pozyskiwania treści ani nie naruszać praw innych osób.',
'pt-BR':'Você se compromete a não usar o site para fins ilegais, interferir no funcionamento do site, tentar obter acesso não autorizado, enviar informações falsas, usar ferramentas automatizadas para extrair conteúdo nem infringir os direitos de outras pessoas.',
'ro':'Vă angajați să nu utilizați site-ul în scopuri ilegale, să nu îi perturbați funcționarea, să nu încercați accesul neautorizat, să nu furnizați informații false, să nu folosiți instrumente automate pentru extragerea conținutului și să nu încălcați drepturile altora.',
'ru':'Вы обязуетесь не использовать сайт в незаконных целях, не нарушать его работу, не предпринимать попыток несанкционированного доступа, не предоставлять ложные сведения, не использовать автоматизированные инструменты для сбора контента и не нарушать права других лиц.',
'sv':'Du förbinder dig att inte använda webbplatsen för olagliga ändamål, störa dess funktion, försöka få obehörig åtkomst, lämna falska uppgifter, använda automatiserade verktyg för att samla in innehåll eller kränka andras rättigheter.'}
for l,v in conduct.items():put(l,source('<p>You agree not to:'),'<p>'+v+'</p>','Unambiguous prohibition scope and automated-content-extraction meaning')

for prefix,values in [
("<li>Return shipping costs are the customer's",{
'de':'Die Kosten der Rücksendung trägt der Kunde, sofern der Artikel nicht beschädigt oder defekt angekommen ist',
'fr':'Les frais de retour sont à la charge du client, sauf si l’article est arrivé endommagé ou défectueux',
'hi':'वापसी शिपिंग की लागत ग्राहक की जिम्मेदारी है, जब तक कि सामान क्षतिग्रस्त या दोषपूर्ण अवस्था में न पहुँचा हो'}),
('<li>Return shipping costs are the customer’s',{
'de':'Die Kosten der Rücksendung trägt der Kunde, sofern uns kein Fehler unterlaufen ist',
'fr':'Les frais de retour sont à la charge du client, sauf erreur de notre part'})]:
    for l,v in values.items():put(l,source(prefix),'<li>'+v+'</li>','Preserve exact exception; repair corrupted initial text')

for l,v in {
'ar':'<p>هل استلمت سلعة تالفة أو معيبة؟ تواصل معنا خلال 7 أيام من التسليم وأرفق صورًا للمشكلة. سنرسل سلعة بديلة أو نرد المبلغ كاملًا — ولا حاجة لإعادة السلعة التالفة.</p>',
'el':'<p>Παραλάβατε κατεστραμμένο ή ελαττωματικό προϊόν; Επικοινωνήστε μαζί μας εντός 7 ημερών από την παράδοση και στείλτε φωτογραφίες του προβλήματος. Θα στείλουμε αντικατάσταση ή θα επιστρέψουμε ολόκληρο το ποσό — δεν χρειάζεται να επιστρέψετε το κατεστραμμένο προϊόν.</p>',
'fr':'<p>Vous avez reçu un article endommagé ou défectueux ? Contactez-nous dans les 7 jours suivant la livraison avec des photos du problème. Nous enverrons un article de remplacement ou effectuerons un remboursement intégral — inutile de retourner l’article endommagé.</p>',
'ro':'<p>Ați primit un articol deteriorat sau defect? Contactați-ne în termen de 7 zile de la livrare, cu fotografii ale problemei. Vom trimite un articol de înlocuire sau vom rambursa integral suma — nu trebuie să returnați articolul deteriorat.</p>'}.items():put(l,source('<p>Received a damaged'),v)
put('fr',source('<p>Our website and products are provided'),' <p>Notre site et nos produits sont fournis « tels quels », sans garantie d’aucune sorte, expresse ou implicite. Nous ne garantissons pas que notre site fonctionne sans interruption ni erreur. La qualité des produits repose sur les spécifications du fabricant et peut présenter de légères variations.</p>'.lstrip())
for l,v in {
'fi':'<p>Lain sallimassa enimmäislaajuudessa FKG Trading LLC:n kokonaisvastuu rajoittuu summaan, jonka olet maksanut kyseessä olevasta tuotteesta tai palvelusta. Emme vastaa välillisistä, satunnaisista, erityisistä tai seurannaisvahingoista.</p>',
'ru':'<p>В максимально допустимой законом степени общая ответственность FKG Trading LLC ограничивается суммой, уплаченной вами за конкретный продукт или услугу, о которых идёт речь. Мы не отвечаем за косвенные, случайные, особые убытки или убытки, возникшие как следствие.</p>'}.items():put(l,source('<p>To the maximum extent'),v)

if __name__=='__main__':
    (HERE/'manual_critical_policy_log.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    print('Critical policy corrections:',len(edits))
