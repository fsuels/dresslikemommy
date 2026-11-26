# Listing claims check, baseline 2026-11-26 (read-only)

Script: `ops/scripts/check_listing_claims.py` (tests: `ops/tests/test_check_listing_claims.py`, 21 pass). Run: `python3 ops/scripts/check_listing_claims.py --all-locales --json`. Source: Admin API 2026-10 reads only, nothing changed.

Scope: 328 ACTIVE products, fields title, body, SEO title, SEO description; locales en + ar, cs, da, de, el, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv.

Result: **496 findings in 105 products**.

## Counts by category

| category | findings |
|---|---|
| craft | 1 |
| english_leftover | 6 |
| health_skin | 1 |
| internal_leak | 3 |
| performance | 17 |
| translated_claim | 141 |
| translation_defect | 327 |

## Counts by rule

| category/rule | findings |
|---|---|
| craft/handmade | 1 |
| english_leftover/handmade | 3 |
| english_leftover/long-lasting | 3 |
| health_skin/gentle-skin | 1 |
| internal_leak/internal-note | 1 |
| internal_leak/vendor-host | 2 |
| performance/fabric-behavior | 3 |
| performance/perfect-fit | 11 |
| performance/wrinkle | 3 |
| translated_claim/performance | 141 |
| translation_defect/glued-letter | 327 |

Glued-letter findings by locale: cs=104, fi=46, ko=33, ro=29, pt-BR=28, pl=18, sv=17, no=14, de=13, fr=11, da=8, es=4, hi=1, he=1

Translated-claim findings by locale: es=44, it=21, de=20, pl=17, nl=15, pt-BR=12, cs=6, fr=6

## Triage
- Real, English (11 perfect-fit/ensure-fit sentences, 3 'wrinkles low' + 3 fabric-behavior, 1 hand-dyed, 1 'gentle against skin', 1 'measurements are not available'): same wording class the 2026-11-26 claim fixes removed; these are leftovers the hand scans missed. Owner: claims fixer.
- Real, vendor host in translation: 2 products (he, el) still carry a supplier image host in body_html (host printed masked).
- Real, translations: 141 es/de/nl/pl/it/pt-BR/fr/cs 'guarantees/perfect fit' renderings of English 'ensures'. They mirror claims removed from English; need retranslation.
- Real, translator bug: 327 glued capital letters (cs 104, fi 46, ko 33, ro 29, pt-BR 28, ...), e.g. EHelppo, PTisk, APřidejte, E이지; the 'E' and 'P' come from the label prefix of the English list item.
- english_leftover (6): 'Hand-Dyed' left in da/no/sv, 'durable' quality in fr/ro; real (same sentence as the English claim).
- truncated-item: 0 after tuning. First pass gave 2,637 false positives (valid short last words such as 'plagg', 'foto'); the rule now needs a locale-vocabulary signal (rare last word, frequent longer word) and returns nothing without a vocabulary. Recall is unproven on live data; covered by fixture tests only.
- brand-altered: 0 findings.
- Likely false positives remaining: none obvious. Borderline: 'run closer to true-to-size' (allowlisted), made-to-order lead time 'ready to ship in about N days' on maternity gowns (allowlisted, honest lead time).

## Tuning done on this baseline
- 'TODO' case-sensitive (Spanish/Portuguese 'todo'); dropped 'temu' (Polish 'temu' = 'this') and 'wholesale', 'one-of-a-kind'.
- Allowlist: not-guaranteed phrases, 'find your perfect fit', 'organic shape/print', 'UV print', made-to-order lead time, 'runs true-to-size'.
- Glued letter: ignore digit+capital (26W), Dutch 'IJ', size-letter + CJK/Hangul (T, V, A, U, O, X, Y, S, M, L, D), skip zh/ja for non-Latin glue.

## Findings (handle, locale, field, matched text up to 80 chars)

| handle | locale | field | category/rule | matched text |
|---|---|---|---|---|
| abstract-print-mommy-and-me-swimsuits | en | body | performance/perfect-fit | …from toddler to adult, ensuring a perfect fit for every mother and daughter duo. |
| abstract-print-mommy-and-me-swimsuits | de | body | translated_claim/performance | …nkind bis Erwachsener, um eine perfekte Passform für jedes Mutter-Tochter-Duo zu… |
| abstract-print-mommy-and-me-swimsuits | es | body | translated_claim/performance | …ños pequeños hasta adultos, lo que garantiza un ajuste perfecto para cada dúo de… |
| abstract-print-mommy-and-me-swimsuits | es | body | translated_claim/performance | …asta adultos, lo que garantiza un ajuste perfecto para cada dúo de madre e hija. |
| abstract-print-mommy-and-me-swimsuits | es | body | translated_claim/performance | …en una amplia gama de tallas para garantizar la combinación perfecta tanto para… |
| abstract-print-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ll'età adulta, per garantire una vestibilità perfetta a ogni duo madre e figlia. |
| abstract-print-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …Van peuter tot volwassene, voor een perfecte pasvorm voor elk moeder-dochterduo. |
| abstract-print-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …chów po dorosłych, zapewniając idealne dopasowanie dla każdej pary mama i córka. |
| animal-ruffle-mommy-and-me-swimsuits | es | body | translated_claim/performance | …solo luce genial, sino que también garantiza que tú y tu pequeño estén cómodos d… |
| animal-ruffle-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ign non solo è bello da vedere, ma garantisce anche comfort a te e al tuo piccol… |
| animal-ruffle-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | …design não só é bonito, mas também garante conforto para você e seu pequeno dur… |
| autumn-woodland-bunny-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E상세 디테일: 노치 칼라, 대비색 파이핑, 버튼 플래킷, 모든 상단에 가슴 포켓. |
| autumn-woodland-bunny-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | EDetalhes elevados: Gola entalhada, debrum contrastante, carcela abotoada e bols… |
| bamboo-garden-panda-cotton-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E이지 케어 & 통기성: 찬물로 세탁기 세탁, 저온에서 회전식 건조. |
| bird-chirping-mommy-and-me-pajamas | en | body | performance/fabric-behavior | Breathable cotton weave keeps airflow high and wrinkles low. |
| bird-chirping-mommy-and-me-pajamas | en | body | performance/wrinkle | Breathable cotton weave keeps airflow high and wrinkles low. |
| bird-chirping-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PStahovací šortky: Měkký elastický pas pro snadné oblékání a svlékání a pohodlí… |
| bird-chirping-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost pro matku a odpovídající velikost pro děti, aby kaž… |
| bird-chirping-mommy-and-me-pajamas | de | body | translation_defect/glued-letter | BVogel zwitschert Obstgarten-Druck: Ein Aquarell-Obstgarten aus Äpfeln, Birnen,… |
| bird-chirping-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo hoito ja hengittävä: Konepesu kylmässä, rumpukuivaus matalalla. |
| bird-chirping-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | …/ 46,5 pouces  65 cm / 25,6 pouces  ONotre ensemble de pyjama maman et moi au c… |
| bird-chirping-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E간편한 관리 및 통기성: 찬물로 기계 세탁, 낮은 온도로 회전식 건조. |
| bird-chirping-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven for å få… |
| bird-chirping-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla matki i odpowiadający mu rozmiar dla dziecka, aby… |
| bird-chirping-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | ECuidado fácil e respirável: Lavar à máquina com água fria e secar em temperatur… |
| bird-chirping-mommy-and-me-pajamas | ro | body | translation_defect/glued-letter | IDimensiuni inclusive: Fete 2–10 ani și Mame S–XL — adăugați-le pe ambele în coș… |
| bird-chirping-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ELättskött och andningsbar: Maskintvättas kallt, torktumlas låg. |
| bird-chirping-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din kundvagn för att… |
| black-and-white-stripe-mommy-and-me-sweaters | es | body | translated_claim/performance | …gedor, estos suéteres son ideales para el frío, garantizando comodidad y estilo. |
| black-and-white-stripe-mommy-and-me-sweaters | nl | body | translated_claim/performance | …jke stof en zijn ideaal voor koeler weer, wat zowel comfort als mode garandeert. |
| black-white-spelling-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Černobílé srdce spojuje tělo bílého trička s černými raglánovými rukávy a… |
| black-white-spelling-family-matching-tops | cs | body | translation_defect/glued-letter | EStyl pro snadné teplé počasí: Uvolněný tvar trička se přirozeně hodí ke šortkám… |
| black-white-spelling-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo muotoilu lämpimässä säässä: Rento t-paidan muoto sopii luonnollisesti sh… |
| black-white-spelling-family-matching-tops | ko | body | translation_defect/glued-letter | E편한 따뜻한 날씨 스타일링: 여유로운 티셔츠 모양은 반바지, 청바지, 스커트 또는 캐주얼 휴가 의상과 자연스럽게 어울립니다. |
| black-white-spelling-family-matching-tops | pt-BR | body | translation_defect/glued-letter | EEstilo fácil para clima quente: O formato descontraído da camiseta combina natu… |
| blue-apricot-heart-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Blue Apricot Letter spojuje meruňkové tělo s námořnickými rukávy, červený… |
| blue-apricot-heart-family-matching-tops | cs | body | translation_defect/glued-letter | EStyl pro snadné teplé počasí: Uvolněný tvar trička se přirozeně hodí k džínovým… |
| blue-apricot-heart-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo muotoilu lämpimässä säässä: Rento tee-muoto sopii luonnollisesti farkkus… |
| blue-apricot-heart-family-matching-tops | ko | body | translation_defect/glued-letter | E따뜻한 날씨 스타일링: 여유로운 티셔츠 모양은 데님 반바지, 청바지, 스커트 또는 캐주얼 휴가 의상과 자연스럽게 어울립니다. |
| blue-baroque-mommy-and-me-swimsuits | es | body | translated_claim/performance | …ambién te permite ajustar el ajuste a tu gusto, garantizando estilo y comodidad. |
| blue-monstera-citrus-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Blue Monstera Citrus kombinuje bílou zeminu, živé modré listy monstery, b… |
| blue-monstera-citrus-family-matching-tops | es | body | translation_defect/glued-letter | ODetalles en naranja: Los motivos frutales añaden un cálido contraste en todo el… |
| blue-monstera-citrus-family-matching-tops | ro | body | translation_defect/glued-letter | Caracteristici cheie:  OSiluetă de familie: Același stil unisex cu guler cu nast… |
| blue-monstera-citrus-family-matching-tops | ro | body | translation_defect/glued-letter | OAccente de portocaliu: Motivele cu fructe adaugă un contrast cald pe tot modelu… |
| blue-paisley-mommy-and-me-swimsuits | de | body | translated_claim/performance | …lbare Nackenbinde: Finde deine perfekte Passform mit der verstellbaren Nackenbin… |
| blue-paisley-mommy-and-me-swimsuits | es | body | translated_claim/performance | …cuello ajustable: encuentre su ajuste perfecto con la corbata de cuello ajustab… |
| blue-paisley-mommy-and-me-swimsuits | es | body | translated_claim/performance | …se adapta con gracia a la figura, garantizando un ajuste que favorece y libera. |
| blue-paisley-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ile dietro il collo: trova la vestibilità perfetta con il laccio regolabile diet… |
| blue-paisley-mommy-and-me-swimsuits | nl | body | translated_claim/performance | Verstelbare nekband: Vind uw perfecte pasvorm met de verstelbare nekband, ontwor… |
| blue-paisley-mommy-and-me-swimsuits | pl | body | translated_claim/performance | Regulowany krawat: Znajdź idealne dopasowanie dzięki regulowanemu krawatowi na s… |
| blue-stripe-family-matching-shirts | cs | body | translation_defect/glued-letter | PTisk: Blue Stripe udržuje outfit jednoduchý a všestranný, s klasickým tvarem ko… |
| blue-stripe-family-matching-shirts | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled se zapínáním na knoflí… |
| blue-stripe-family-matching-shirts | cs | body | translation_defect/glued-letter | PPruh připravený k fotografování: Měkká modrá barva, svislé pruhy, náprsní kapsy… |
| blue-stripe-family-matching-shirts | cs | body | translation_defect/glued-letter | EJednoduchý styl: Navrstvěte bílá trička s ležérními kalhotami pro čistý rodinný… |
| blue-stripe-family-matching-shirts | fi | body | translation_defect/glued-letter | EHelppo muotoilu: Kerros valkoisten t-paiden päällä rento housuilla puhtaan perh… |
| blue-stripe-family-matching-shirts | ko | body | translation_defect/glued-letter | E쉬운 스타일링 : 흰색 티셔츠 위에 캐주얼 팬츠를 레이어드해 깔끔한 패밀리룩을 연출해보세요. |
| blue-stripe-family-matching-shirts | pt-BR | body | translation_defect/glued-letter | EEstilo fácil: Camada sobre camisetas brancas com calças casuais para um visual… |
| blue-stripe-family-matching-shirts | ro | body | translation_defect/glued-letter | EStil facil: Strat peste tricouri albe cu pantaloni casual pentru un aspect cura… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | en | body | craft/handmade | Print: Blue Tie-Dye Butterfly — a hand-dyed sky-and-cloud ombré in cream and ind… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | da | body | english_leftover/handmade | Hand-Dyed Ombré Print: Creme-to-indigo vaskmed hviskende-hvide sommerfugle-accen… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | de | body | translation_defect/glued-letter | BDieses Kleid wurde für die Kombination von Mutter-Tochter-Momenten entwickelt u… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | de | body | translation_defect/glued-letter | HAusschnitt im Neckholder-Stil: Weiche geraffte Passe und Bindeband hinten, die… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | de | body | translation_defect/glued-letter | BAtmungsaktive Baumwollmischung: Leicht, weich auf der Haut und leicht zu wasche… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | es | body | translated_claim/performance | …os, el lazo trasero mantiene el ajuste perfecto durante los días largos y la pal… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | no | body | english_leftover/handmade | Hand-Dyed Ombré-trykk: Krem-til-indigo-vaskmed hviskehvite sommerfuglaksenter —… |
| blue-tie-dye-butterfly-mommy-and-me-dresses | sv | body | english_leftover/handmade | Hand-Dyed Ombré Mönster: Cream-to-indigo washmed viskvita fjärilsaccenter — inga… |
| bluebell-meadow-family-matching-set | cs | body | translation_defect/glued-letter | PTisk: „Bluebell Meadow“ vrství květy brčál, máslově žluté snítky a svěží zelené… |
| blush-garden-mommy-and-me-swimsuits | cs | body | translation_defect/glued-letter | APřipevněné spodky: Přiléhavé vnitřní slipy udržují bezpečné krytí při plavání,… |
| blush-garden-mommy-and-me-swimsuits | de | body | translation_defect/glued-letter | EJeder Anzug behält den bedeckungsfreundlichen Look eines kleinen Badekleids, wä… |
| blush-garden-mommy-and-me-swimsuits | fi | body | translation_defect/glued-letter | AKiinnitetyt pohjat: Tiiviit sisähousut pitävät suojan uimista, kahlaamista ja v… |
| blush-garden-mommy-and-me-swimsuits | fr | body | translation_defect/glued-letter | RDétail de l'encolure volantée : Le volant bordé de roses encadre les épaules po… |
| blush-garden-mommy-and-me-swimsuits | ko | body | translation_defect/glued-letter | E각 슈트는 커버력이 좋은 작은 수영복의 룩을 유지하며, 부착된 바닥은 물장구를 치고, 수영하고, 수영장 주변의 어린 아이들을 쫓아갈 준비가 되… |
| blush-garden-mommy-and-me-swimsuits | no | body | translation_defect/glued-letter | AFeste underdeler: Den tettsittende innerbuksen holder dekningen sikker for svøm… |
| blush-garden-mommy-and-me-swimsuits | pt-BR | body | translation_defect/glued-letter | ECada terno mantém a aparência de fácil cobertura de um vestidinho de banho, enq… |
| blush-garden-mommy-and-me-swimsuits | ro | body | translation_defect/glued-letter | IMărimea mamei inclusă: Mărimile mamei variază de la M la 4XL alături de setul d… |
| blush-garden-mommy-and-me-swimsuits | sv | body | translation_defect/glued-letter | AFästa underdel: Den tättslutande innertrosan håller täckningen säker för simnin… |
| bright-paint-splash-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Bright Paint Splash vrství živé modré, modrozelené, oranžové, červené a ž… |
| bright-paint-splash-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| bright-paint-splash-family-matching-tops | cs | body | translation_defect/glued-letter | ESnadný styl do teplého počasí: Tvar s krátkým rukávem na knoflíky se snadno kom… |
| bright-paint-splash-family-matching-tops | fi | body | translation_defect/glued-letter | EIlmainen maalitulostus: Kirkkaat siniset, sinivihreät, oranssit, punaiset ja ke… |
| bright-paint-splash-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo muotoilu lämpimässä säässä: Lyhythihainen nappimuoto sopii helposti yksi… |
| bright-paint-splash-family-matching-tops | ko | body | translation_defect/glued-letter | E따뜻한 날씨 스타일링: 반팔 버튼업 형태로 심플한 가족룩과 잘 어울립니다. |
| bright-paint-splash-family-matching-tops | pl | body | translation_defect/glued-letter | EWyrazisty nadruk farbą: Żywe plamy w kolorze niebieskim, turkusowym, pomarańczo… |
| bright-paint-splash-family-matching-tops | pt-BR | body | translation_defect/glued-letter | EEstilo fácil para clima quente: O formato de botão de manga curta combina facil… |
| bright-paint-splash-family-matching-tops | ro | body | translation_defect/glued-letter | EImprimare cu vopsea expresivă: Stropi vii de albastru, verdeață, portocaliu, ro… |
| bright-paint-splash-family-matching-tops | sv | body | translation_defect/glued-letter | EExpressivt färgtryck: Levande blå, kricka, orange, röda och gula stänk skapar e… |
| cable-horse-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Kabelový kůň spojuje slonovinový kabelový úplet s malou nášivkou červenéh… |
| cable-horse-family-matching-tops | cs | body | translation_defect/glued-letter | PHrudní nášivka připravená k fotografování: Motiv červeného koně udržuje rodinno… |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | en | body | performance/perfect-fit | …swimsuits offer a range of sizes ensuring a perfect fit for every family member. |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | cs | body | translated_claim/performance | …okou škálu velikostí, které zajišťují dokonalé padnutí pro každého člena rodiny. |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | de | body | translated_claim/performance | …an Größen, die für jedes Familienmitglied eine perfekte Passform gewährleisten. |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | es | body | translated_claim/performance | …frecen una variedad de tamaños que garantizan un ajuste perfecto para cada miemb… |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | es | body | translated_claim/performance | …ad de tamaños que garantizan un ajuste perfecto para cada miembro de la familia. |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | it | body | translated_claim/performance | …mi offrono una gamma di taglie che garantisce una vestibilità perfetta per ogni… |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | it | body | translated_claim/performance | …di taglie che garantisce una vestibilità perfetta per ogni membro della famigli… |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | nl | body | translated_claim/performance | …pakken een reeks maten die zorgen voor een perfecte pasvorm voor elk familielid. |
| chic-mother-daughter-matching-swimsuit-set-with-floral-cover-up-family-beachwear-collection | pl | body | translated_claim/performance | …ki wybór rozmiarów, zapewniając idealne dopasowanie dla każdego członka rodziny. |
| coastal-banana-leaf-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Pobřežní banánový list vrství na bílém podkladu živé modré a zelené banán… |
| coastal-banana-leaf-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| coastal-banana-leaf-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo lämpimän sään kerros: Rento napitusmuoto toimii yksinkertaisen aluspaida… |
| coastal-banana-leaf-family-matching-tops | ko | body | translation_defect/glued-letter | E편안한 따뜻한 날씨 레이어: 여유로운 버튼업 모양으로 심플한 언더셔츠 위에 착용하거나 독립형 상의로도 활용 가능합니다. |
| coastal-banana-leaf-family-matching-tops | pl | body | translation_defect/glued-letter | EWygodna warstwa na ciepłe dni: Swobodny, zapinany krój można nosić na prostym p… |
| coastal-banana-leaf-family-matching-tops | pt-BR | body | translation_defect/glued-letter | ECamada fácil para clima quente: O formato descontraído de botões funciona sobre… |
| color-block-mommy-and-me-swimsuits | es | body | translated_claim/performance | …e de cintura alta complementario, lo que garantiza la sincronización del estilo. |
| color-block-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | …enquanto o maiô combinando da filha garante que as pequenas possam espelhar o vi… |
| colorful-family-matching-love-t-shirts-fun-bold-lettering-design-in-multiple-colors | hi | body | translation_defect/glued-letter | …O की जगह गुलाबी दिल, बैंगनी V और हरा E। हर टी-शर्ट पर पूरा शब्द है। सफ़ेद, नीला… |
| colorful-family-matching-love-t-shirts-fun-bold-lettering-design-in-multiple-colors | ko | body | translation_defect/glued-letter | 파란 지그재그 L, O 자리의 분홍 하트, 보라색 V, 초록색 E로 되어 있습니다. |
| cow-print-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | A estampa única de vaca garante que você se destaque, seja relaxando à beira da… |
| denim-blue-family-matching-set | cs | body | translation_defect/glued-letter | PTisk: Džínová modrá udržuje vzhled čistý a všestranný, s kontrastním prošíváním… |
| denim-blue-family-matching-set | cs | body | translation_defect/glued-letter | ETvar pro snadné teplé počasí: Krátké rukávy a šortky jsou praktické pro letní c… |
| denim-blue-family-matching-set | fi | body | translation_defect/glued-letter | EHelppo lämpimän sään muoto: Lyhyet hihat ja shortsit pitävät setin käytännöllis… |
| denim-blue-family-matching-set | ko | body | translation_defect/glued-letter | E따뜻한 날씨에 어울리는 형태: 반소매와 반바지로 여름 여행, 테마파크, 브런치, 가족 사진 촬영에 실용성을 더해줍니다. |
| denim-blue-family-matching-set | pl | body | translation_defect/glued-letter | EProsty kształt na ciepłe dni: Krótkie rękawy i spodenki sprawiają, że zestaw je… |
| denim-blue-family-matching-set | pt-BR | body | translation_defect/glued-letter | EForma fácil para clima quente: Mangas curtas e shorts mantêm o conjunto prático… |
| denim-blue-family-matching-set | sv | body | translation_defect/glued-letter | ELätt form i varmt väder: Korta ärmar och shorts håller setet praktiskt för somm… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | en | body | performance/perfect-fit | …stic waistband and drawstring ensure a perfect fit that adapts to any activity,… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | de | body | translated_claim/performance | …der Kordelzug sorgen für eine perfekte Passform, die sich jeder Aktivität anpas… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | es | body | translated_claim/performance | …lástica y el cordón aseguran un ajuste perfecto que se adapta a cualquier activi… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | it | body | translated_claim/performance | …ca e il laccio assicurano una vestibilità perfetta che si adatta a qualsiasi att… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | nl | body | translated_claim/performance | …nd en trekkoord zorgen voor een perfecte pasvorm die zich aanpast aan elke activ… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | pl | body | translated_claim/performance | Elastyczny pas i sznurek gwarantują idealne dopasowanie, które sprawdzi się podc… |
| dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set | pl | body | translated_claim/performance | …czny pas i sznurek gwarantują idealne dopasowanie, które sprawdzi się podczas en… |
| emerald-leaf-family-matching-set | cs | body | translation_defect/glued-letter | PTisk: „Emerald Leaf“ vrství krémové tropické listy a siluety zvířat na bohaté z… |
| eucalyptus-bunny-gauze-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E라스틱 웨이스트 팬츠: 신축성 있는 풀온 허리밴드가 있는 스트레이트 레그 실루엣으로 어린 아이에게도 쉽고 엄마에게도 편안합니다. |
| eucalyptus-bunny-gauze-mommy-and-me-pajamas | pl | body | translated_claim/performance | …u i długie rękawy umożliwiają idealne dopasowanie do snu — bez skrótów do t-shir… |
| eucalyptus-bunny-gauze-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | ECalça de cintura elástica: Silhueta de perna reta com cós elástico - fácil para… |
| family-matching-cable-knit-sweaters-heart-embroidered-unisex-pullovers | es | body | translated_claim/performance | …informal, estos suéteres a juego te garantizan un look coordinado y con estilo. |
| family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style | es | body | translated_claim/performance | Su suave tejido de punto garantiza comodidad durante todo el día, mientras que s… |
| family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style | it | body | translated_claim/performance | Il morbido materiale in maglia garantisce comfort per tutto il giorno, mentre il… |
| family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style | pt-BR | body | translated_claim/performance | O material de malha macia garante conforto durante todo o dia, enquanto o design… |
| father-and-baby-matching-ctrl-c-ctrl-v-t-shirt-set-copy-and-paste-duo | ko | seo_description | translation_defect/glued-letter | CTRL+C와 CTRL+V 복사-붙여넣기 프린트의 아빠와 아기 블랙 커플 티셔츠. |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | cs | body | translated_claim/performance | …všem typům postav a velikostem, což zaručuje skvělý den na pláži pro celou rodin… |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | de | body | translated_claim/performance | …er und Kinder jeden Alters, um für jeden die perfekte Passform zu gewährleisten. |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | de | body | translated_claim/performance | …rinnerungen, die mit dieser markanten Strandbekleidung garantiert folgen werden. |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | es | body | translated_claim/performance | …niños de todas las edades, lo que garantiza una combinación perfecta para todos… |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | es | body | translated_claim/performance | …e adaptan a todo tipo de cuerpos, garantizando un día de playa fantástico para t… |
| father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear | pl | body | translated_claim/performance | …y do ojców i dzieci w każdym wieku, zapewniając idealne dopasowanie dla każdego. |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | en | body | performance/perfect-fit | …adjustable drawstring make for a perfect fit that can handle the rough and tumb… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | cs | body | translated_claim/performance | …itelný šňůrkový pásek zajišťují dokonalé padnutí, které zvládne i divoké aktivit… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | de | body | translated_claim/performance | …bare Kordelzug sorgen für eine perfekte Passform, die jedem Strandabenteuer stan… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | es | body | translated_claim/performance | …el cordón ajustable ofrecen un ajuste perfecto que resiste las inclemencias de… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | it | body | translated_claim/performance | …o regolabile garantiscono una vestibilità perfetta che può affrontare qualsiasi… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | nl | body | translated_claim/performance | …lbare trekkoord zorgen voor een perfecte pasvorm die bestand is tegen het ruige… |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | pl | body | translated_claim/performance | Elastyczny pas ze sznurkiem gwarantuje dopasowanie i regulację. |
| father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow | pl | body | translated_claim/performance | …regulowany sznurek zapewniają idealne dopasowanie, które poradzi sobie z wszelki… |
| father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear | de | body | translated_claim/performance | …seinen kleinen Sohn suchst, unsere passenden Badehosen sind garantiert ein Hit. |
| father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear | es | body | translated_claim/performance | …maños para hombres y niños, lo que garantiza un ajuste perfecto para los papás y… |
| father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear | es | body | translated_claim/performance | …hombres y niños, lo que garantiza un ajuste perfecto para los papás y sus hijos. |
| father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print | es | body | translated_claim/performance | …se adapta a todo tipo de cuerpos, garantizando un ajuste perfecto tanto para jug… |
| father-and-son-matching-swim-trunks-tropical-paradise-red-and-green-print | es | body | translated_claim/performance | …ipo de cuerpos, garantizando un ajuste perfecto tanto para jugar como para relaj… |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | en | body | performance/perfect-fit | Available in various sizes for a perfect fit for both dad and baby |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | cs | body | translated_claim/performance | …ozici v různých velikostech pro dokonalé padnutí jak pro tatínka, tak pro mimink… |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | de | body | translated_claim/performance | In verschiedenen Größen erhältlich für eine perfekte Passform für Vater und Baby |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | es | body | translated_claim/performance | …onible en varias tallas para un ajuste perfecto tanto para papá como para el beb… |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | it | body | translated_claim/performance | …nibile in varie taglie per una vestibilità perfetta sia per papà che per bambino |
| father-baby-mr-fix-it-mr-broke-it-matching-t-shirt-onesie-set-perfect-gift-for-handy-dads | nl | body | translated_claim/performance | …gbaar in verschillende maten voor een perfecte pasvorm voor zowel vader als baby |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | en | body | performance/perfect-fit | Available in multiple sizes to ensure a perfect fit for both dad and baby |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | cs | body | translated_claim/performance | …pozici v několika velikostech pro dokonalé padnutí jak pro otce, tak pro miminko |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | de | body | translated_claim/performance | …ren Größen erhältlich, um eine perfekte Passform für Vater und Baby zu gewährlei… |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | es | body | translated_claim/performance | …varias tallas para asegurar un ajuste perfecto tanto para papá como para el beb… |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | it | body | translated_claim/performance | …n più taglie per garantire una vestibilità perfetta sia per papà che per bambino |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | nl | body | translated_claim/performance | …jgbaar in meerdere maten om een perfecte pasvorm voor zowel vader als baby te ga… |
| father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift | pl | body | translated_claim/performance | …ielu rozmiarach, aby zapewnić idealne dopasowanie zarówno dla taty, jak i dzieck… |
| flower-accent-mommy-and-me-swimsuits | es | body | translated_claim/performance | …tano para un estiramiento cómodo y garantizar un ajuste favorecedor tanto para a… |
| fluttering-butterflies-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost matky a odpovídající velikost dítěte, aby se každý… |
| fluttering-butterflies-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | ALisää ostoskoriisi äidin koko ja sitä vastaava lapsen koko, jotta jokainen hetk… |
| fluttering-butterflies-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven din for… |
| fluttering-butterflies-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla mamy i odpowiadający mu rozmiar dla dziecka, aby k… |
| fluttering-butterflies-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din varukorg för att… |
| geometric-print-mommy-and-me-swimsuits | en | body | performance/perfect-fit | …adjustable tie-shoulder straps ensure the perfect fit for both adults and kids. |
| geometric-print-mommy-and-me-swimsuits | en | body | performance/perfect-fit | …houlder straps and stretchable fabric ensure a comfortable fit for all-day wear. |
| geometric-print-mommy-and-me-swimsuits | de | body | translated_claim/performance | …n an den Schultern sorgen für die perfekte Passform bei Erwachsenen und Kindern. |
| geometric-print-mommy-and-me-swimsuits | es | body | translated_claim/performance | …; las correas de hombro ajustables garantizan un ajuste perfecto tanto para adul… |
| geometric-print-mommy-and-me-swimsuits | es | body | translated_claim/performance | …hombro ajustables garantizan un ajuste perfecto tanto para adultos como para niñ… |
| geometric-print-mommy-and-me-swimsuits | fr | body | english_leftover/long-lasting | …re-fille – la combinaison parfaite d'élégance, de confort et de qualité durable. |
| geometric-print-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ine regolabili con nodo assicurano la vestibilità perfetta per adulti e bambini. |
| geometric-print-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …banden met strik zorgen voor de perfecte pasvorm voor zowel volwassenen als kind… |
| geometric-print-mommy-and-me-swimsuits | ro | body | english_leftover/long-lasting | …u mamă și fiică – combinația perfectă de eleganță, confort și calitate durabilă. |
| good-night-song-of-the-sea-mommy-and-me-pajamas | en | body | performance/fabric-behavior | The open gauze weave keeps airflow high and wrinkles low. |
| good-night-song-of-the-sea-mommy-and-me-pajamas | en | body | performance/wrinkle | The open gauze weave keeps airflow high and wrinkles low. |
| good-night-song-of-the-sea-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PStahovací šortky: Měkký elastický pas pro snadné oblékání a svlékání a pohodlí… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost matky a odpovídající velikost dětí, aby každý okamž… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo hoito ja hengittävä: Konepesu kylmässä, rumpukuivaus matalalla. |
| good-night-song-of-the-sea-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | ALisää ostoskoriisi äidin koko ja vastaava lasten koko, jotta jokainen hetki sop… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | …/ 46,5 pouces  65 cm / 25,6 pouces  ONotre ensemble de pyjama maman et moi Good… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E이지 케어 & 통기성: 찬물로 세탁기 세탁, 저온에서 회전식 건조. |
| good-night-song-of-the-sea-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven for å få… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla matki i odpowiadający mu rozmiar dla dziecka, aby… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | ro | body | translation_defect/glued-letter | IDimensiuni inclusive: Fete 2–10 ani și Mame S–XL — adăugați-le pe ambele în coș… |
| good-night-song-of-the-sea-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din kundvagn för att… |
| grape-vineyard-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PNatahovací levandulové šortky: Elastický pas a odpovídající levandulový barevný… |
| grape-vineyard-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost matky a odpovídající velikost dětí, aby každý okamž… |
| grape-vineyard-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo hoito ja hengittävä: Konepesu kylmänä nurinpäin, rumpukuivaus alhaalla. |
| grape-vineyard-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | ALisää ostoskoriisi äidin koko ja vastaava lasten koko, jotta jokainen hetki sop… |
| grape-vineyard-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | RManches courtes raglan : Bordure lavande contrastée douce à l'encolure et aux c… |
| grape-vineyard-mommy-and-me-pajamas | he | body | translation_defect/glued-letter | Eטיפול קל & לנשימה: כביסה במכונה קרה מבפנים החוצה, ייבוש במייבש נמוך. |
| grape-vineyard-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E이지 케어 & 통기성: 세탁기로 찬물을 뒤집어서 세탁하고, 낮은 온도로 회전식 건조하세요. |
| grape-vineyard-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven for å få… |
| grape-vineyard-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla matki i odpowiadający mu rozmiar dla dziecka, aby… |
| grape-vineyard-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din kundvagn för att… |
| grapevine-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PTisk: Ručně ilustrované hrozny, listy, vinná réva a malí tygři v zaprášené růži… |
| green-botanical-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | APřidejte velikosti, které potřebujete, a vytvořte si svěže padnoucí šaty pro př… |
| green-botanical-ruffle-mommy-and-me-dresses | da | body | translation_defect/glued-letter | ATilføj de størrelser, du har brug for, og skab et luftigt matchende kjoleøjebli… |
| green-botanical-ruffle-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | ALisää tarvitsemasi koot ja luo raikas yhteensopiva pukeutumishetki seuraavaa au… |
| green-botanical-ruffle-mommy-and-me-dresses | no | body | translation_defect/glued-letter | ALegg til størrelsene du trenger og skap et luftig matchende kjoleøyeblikk for d… |
| green-lace-garden-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | OVěrný krajkový límec: Výrazný bílý límeček dodává mamince a mini šatech okouzlu… |
| green-lace-garden-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | EHelppo rypytetty hame: Rento midi-muoto liikkuu kauniisti juhliin, lomiin ja mu… |
| green-lace-garden-mommy-and-me-dresses | ko | body | translation_defect/glued-letter | E이지 개더 스커트: 여유로운 미디 형태가 파티, 휴가, 인물 사진에 아름답게 움직입니다. |
| green-lace-garden-mommy-and-me-dresses | pt-BR | body | translation_defect/glued-letter | ESaia franzida fácil: O formato midi descontraído combina perfeitamente com fest… |
| green-lace-garden-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | OGuler de dantelă de dimensiuni mari: Gulerul alb adaugă un finisaj fermecător d… |
| green-lace-garden-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | EFusta strânsă ușor: Forma midi relaxată se mișcă frumos pentru petreceri, vacan… |
| green-palm-safari-family-matching-set | cs | body | translation_defect/glued-letter | PTisk: „Green Palm Safari“ vrství krémové tropické listy a siluety zvířat na boh… |
| ivory-bow-back-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | SVroubkovaný lem: Jemné vroubkované lemy rámují průramky bez rukávů se sladkým l… |
| ivory-bow-back-mommy-and-me-dresses | de | body | translation_defect/glued-letter | Hauptmerkmale:  BAtmungsaktives Baumwollgefühl: Weiche gewebte Baumwolle. |
| ivory-bow-back-mommy-and-me-dresses | fr | body | translation_defect/glued-letter | ODétail de nœud surdimensionné au dos : Un nœud spectaculaire au dos ajoute une… |
| ivory-bow-back-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | ODetaliu supradimensionat pe fundul spate: O fundă dramatică pe spate adaugă un… |
| ivory-cascade-mommy-and-me-set | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  ADvoudílná vzdušná silueta: Top bez rukávů a splývavá sukně… |
| ivory-cascade-mommy-and-me-set | cs | body | translation_defect/glued-letter | EJednoduchý elastický pas: Sukňový pas pomáhá udržet pohodlí pro maminku i pro m… |
| ivory-cascade-mommy-and-me-set | es | body | translation_defect/glued-letter | Características principales:  ASilueta aireada de dos piezas: La blusa sin manga… |
| ivory-cascade-mommy-and-me-set | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlmainen kaksiosainen siluetti: Hihaton toppi ja lentävä hame… |
| ivory-cascade-mommy-and-me-set | fi | body | translation_defect/glued-letter | EHelppo joustava vyötärö: Hameen vyötärönauha auttaa pitämään istuvuuden mukavan… |
| ivory-cascade-mommy-and-me-set | ko | body | translation_defect/glued-letter | E쉬운 신축성 있는 허리 : 스커트 허리밴드가 엄마와 미니 모두에게 편안한 핏을 유지시켜줍니다. |
| ivory-cascade-mommy-and-me-set | pl | body | translation_defect/glued-letter | Kluczowe cechy:  APrzewiewna dwuczęściowa sylwetka: Top bez rękawów i zwiewna sp… |
| ivory-cascade-mommy-and-me-set | pl | body | translation_defect/glued-letter | EWygodna elastyczna talia: Pasek spódnicy zapewnia wygodne dopasowanie zarówno d… |
| ivory-cascade-mommy-and-me-set | pt-BR | body | translation_defect/glued-letter | ECintura elástica fácil: O cós da saia ajuda a manter o ajuste confortável para… |
| ivory-cascade-mommy-and-me-set | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASiluetă aerisită din două piese: Topul fără mâneci și fu… |
| ivory-dot-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  AVzdušný tkaný pocit: Lehký polyester udržuje siluetu snadn… |
| ivory-dot-mommy-and-me-dresses | da | body | translation_defect/glued-letter | Nøglefunktioner:  AVævet fornemmelse: Letvægtspolyester holder silhuetten let og… |
| ivory-dot-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlmainen kudottu tunne: Kevyt polyesteri pitää siluetin helpo… |
| ivory-dot-mommy-and-me-dresses | fr | body | translation_defect/glued-letter | RCorsage froncé : Les fronces douces sur le devant ajoutent de la texture tout e… |
| ivory-dot-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASenzație de țesut aerian: Poliesterul ușor menține silue… |
| ivory-dot-mommy-and-me-dresses | sv | body | translation_defect/glued-letter | Nyckelfunktioner:  AVärlig vävd känsla: Lätt polyester håller silhuetten enkel o… |
| ivory-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  AVzdušný tkaný pocit: Lehký polyester udržuje siluetu snadn… |
| ivory-ruffle-mommy-and-me-dresses | da | body | translation_defect/glued-letter | Nøglefunktioner:  AVævet fornemmelse: Letvægtspolyester holder silhuetten let og… |
| ivory-ruffle-mommy-and-me-dresses | de | body | translation_defect/glued-letter | BLuftiger ärmelloser Schnitt: Eine einfache Form, die sich gut für Reisen, Party… |
| ivory-ruffle-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlmainen kudottu tunne: Kevyt polyesteri pitää siluetin helpo… |
| ivory-ruffle-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASenzație de țesut aerian: Poliesterul ușor menține silue… |
| ivory-ruffle-mommy-and-me-dresses | sv | body | translation_defect/glued-letter | Nyckelfunktioner:  AVärlig vävd känsla: Lätt polyester håller silhuetten enkel o… |
| ivory-tiered-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  AVzdušný tkaný pocit: Lehký polyester udržuje siluetu snadn… |
| ivory-tiered-ruffle-mommy-and-me-dresses | da | body | translation_defect/glued-letter | Nøglefunktioner:  AVævet fornemmelse: Letvægtspolyester holder silhuetten let og… |
| ivory-tiered-ruffle-mommy-and-me-dresses | de | body | translation_defect/glued-letter | BLuftiger ärmelloser Schnitt: Eine einfache Form, die sich gut für Reisen, Party… |
| ivory-tiered-ruffle-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlmainen kudottu tunne: Kevyt polyesteri pitää siluetin helpo… |
| ivory-tiered-ruffle-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASenzație de țesut aerian: Poliesterul ușor menține silue… |
| ivory-tiered-ruffle-mommy-and-me-dresses | sv | body | translation_defect/glued-letter | Nyckelfunktioner:  AVärlig vävd känsla: Lätt polyester håller silhuetten enkel o… |
| ladybug-dots-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PPříběh připravený k tisku: Drobné berušky, luční květiny a vážky vytvářejí kouz… |
| ladybug-dots-mommy-and-me-pajamas | de | body | translation_defect/glued-letter | …en Moment zusammenpassen lässt  BAtmungsaktiver Gazestoff: Die Bambus-Baumwoll-K… |
| ladybug-dots-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | …/ 30,7 pouces  68 cm / 26,8 pouces  ONotre ensemble de pyjama maman et moi Lady… |
| lavender-hydrangea-family-matching-set | cs | body | translation_defect/glued-letter | PTisk: „Levandulová hortenzie“ spojuje akvarelově fialové květy ve stylu hortenz… |
| lavender-hydrangea-family-matching-set | cs | body | translation_defect/glued-letter | SDlouhé šaty bez rukávů: Tvar šatů dává dívkám a maminkám modrá ramínka, vzdušný… |
| lavender-hydrangea-family-matching-set | cs | body | translation_defect/glued-letter | SLesk na košile: Košile s límečkem s krátkým rukávem dodávají chlapcům a tatínků… |
| leopard-mesh-mommy-and-me-swimsuits | en | body | performance/perfect-fit | …nd of nylon and polyester fiber, ensuring a perfect fit and freedom of movement. |
| leopard-mesh-mommy-and-me-swimsuits | de | body | translated_claim/performance | …und Polyesterfasern, die eine perfekte Passform und Bewegungsfreiheit gewährlei… |
| leopard-mesh-mommy-and-me-swimsuits | es | body | translated_claim/performance | …ibra de nailon y poliéster, lo que garantiza un ajuste perfecto y libertad de mo… |
| leopard-mesh-mommy-and-me-swimsuits | es | body | translated_claim/performance | …ailon y poliéster, lo que garantiza un ajuste perfecto y libertad de movimiento. |
| leopard-mesh-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ca di nylon e fibra di poliestere, garantisce una vestibilità perfetta e libertà… |
| leopard-mesh-mommy-and-me-swimsuits | it | body | translated_claim/performance | …fibra di poliestere, garantisce una vestibilità perfetta e libertà di movimento. |
| leopard-mesh-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …on- en polyestervezels, die een perfecte pasvorm en bewegingsvrijheid garanderen… |
| leopard-mesh-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …nylonowych i poliestrowych, zapewniającej idealne dopasowanie i swobodę ruchów. |
| leopard-ruffle-mommy-and-me-swimsuits | de | body | translated_claim/performance | …sondern verleiht auch eine feminine Note, die garantiert Blicke auf sich zieht. |
| leopard-ruffle-mommy-and-me-swimsuits | es | body | translated_claim/performance | …odos los lugares correctos, lo que garantiza un ajuste favorecedor para cada fig… |
| leopard-ruffle-mommy-and-me-swimsuits | es | body | translated_claim/performance | …irradia un aire feroz y elegante, garantizando que tú y tu mini-yo seáis el cent… |
| leopard-ruffle-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …kim, a zarazem eleganckim stylem, gwarantując, że Ty i Twoja mała kopia będzieci… |
| little-pear-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | EJednoduché zapínání/snadné vypínání: Stahovací vršek u krku a elastické šortky… |
| little-pear-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | SVklouzněte do sady a každé ráno si udělejte o něco dokonalejší obraz – protože… |
| little-pear-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo päällä / Easy Off: Pyöreä pääntie ja joustava vyötäröshortsit – ei nappe… |
| little-pear-mommy-and-me-pajamas | ro | body | translation_defect/glued-letter | EUșor de pornit/Ușor de dezactivat: Top cu pulover și pantaloni scurți cu talie… |
| little-sheep-meadow-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku odpovídající velikosti pro matku a dceru, aby každý okamžik… |
| little-sheep-meadow-mommy-and-me-pajamas | de | body | translation_defect/glued-letter | BAtmungsaktiver Baumwollstrick: Leicht und luftig für den Schlaf bei warmem Wett… |
| little-sheep-meadow-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo hoito: Konepesu kylmässä, rumpukuivaus alhainen. |
| little-sheep-meadow-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | …/ 30,7 pouces  68 cm / 26,8 pouces  ONotre ensemble de pyjama maman et moi Litt… |
| little-sheep-meadow-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E간편한 관리: 찬물로 기계 세탁, 저온에서 회전식 건조. |
| little-sheep-meadow-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til de matchende mor- og datterstørrelsene i handlekurven for å få hvert ø… |
| little-sheep-meadow-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka pasujące rozmiary matki i córki, aby każda chwila była dopasow… |
| little-sheep-meadow-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | ECuidado fácil: Lavar à máquina com água fria e secar em temperatura baixa. |
| little-sheep-meadow-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ELättskötsel: Maskintvättas kallt, torktumlas låg. |
| little-sheep-meadow-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till de matchande mor- och dotterstorlekarna i din kundvagn för att få var… |
| matching-dad-and-son-pink-black-color-block-swim-shorts | fr | body | translated_claim/performance | Technologie de séchage rapide : Conçu avec un tissu à séchage rapide, ce maillot… |
| matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids | de | body | translated_claim/performance | …Look, während die lockere Passform Komfort für Erwachsene und Kinder garantiert. |
| matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids | es | body | translated_claim/performance | …ral, mientras que su corte holgado garantiza comodidad tanto para adultos como p… |
| matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids | it | body | translated_claim/performance | …empo, mentre la vestibilità comoda garantisce comfort sia per adulti che per bam… |
| matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids | pt-BR | body | translated_claim/performance | …temporal, enquanto o caimento relaxado garante conforto para adultos e crianças. |
| matching-family-love-t-shirt-set-adorable-family-heart-design | es | body | translated_claim/performance | Tela de algodón suave y transpirable que garantiza comodidad todo el día |
| matching-family-love-t-shirt-set-adorable-family-heart-design | it | body | translated_claim/performance | …l tessuto in cotone morbido e traspirante garantisce comfort per tutto il giorno |
| matching-family-love-t-shirt-set-adorable-family-heart-design | pt-BR | body | translated_claim/performance | Tecido de algodão macio e respirável garante conforto durante todo o dia |
| matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set | he | body | internal_leak/vendor-host | URL host c***.com |
| meow-star-garden-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost matky a odpovídající velikost dítěte, aby se každý… |
| meow-star-garden-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | ALisää ostoskoriisi äidin koko ja sitä vastaava lapsen koko, jotta jokainen hetk… |
| meow-star-garden-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | RCoupe de pantalon long décontractée : Mouvement facile pour l'heure du coucher,… |
| meow-star-garden-mommy-and-me-pajamas | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven din for… |
| meow-star-garden-mommy-and-me-pajamas | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla mamy i odpowiadający mu rozmiar dla dziecka, aby k… |
| meow-star-garden-mommy-and-me-pajamas | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din varukorg för att… |
| midnight-paint-splash-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Midnight Paint Splash vrství živé modré, šedozelené, červené, oranžové a… |
| midnight-paint-splash-family-matching-tops | cs | body | translation_defect/glued-letter | EExpresivní abstraktní tisk: Tmavý podklad a světlé vícebarevné motivy s rozstři… |
| midnight-paint-splash-family-matching-tops | fi | body | translation_defect/glued-letter | EIlmainen abstrakti printti: Tumma pohja ja kirkkaat moniväriset maaliroiskeaihe… |
| midnight-paint-splash-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo lämpimän sään kerros: Rento napitusmuoto toimii yksinkertaisen aluspaida… |
| midnight-paint-splash-family-matching-tops | ko | body | translation_defect/glued-letter | E편안한 따뜻한 날씨 레이어: 여유로운 버튼업 모양으로 심플한 언더셔츠 위에 착용하거나 독립형 상의로도 활용 가능합니다. |
| midnight-paint-splash-family-matching-tops | pl | body | translation_defect/glued-letter | EWyrazisty abstrakcyjny nadruk: Ciemne podłoże i jasne, wielokolorowe motywy pla… |
| midnight-paint-splash-family-matching-tops | pl | body | translation_defect/glued-letter | EWygodna warstwa na ciepłe dni: Swobodny, zapinany krój można nosić na prostym p… |
| midnight-paint-splash-family-matching-tops | pt-BR | body | translation_defect/glued-letter | ECamada fácil para clima quente: O formato descontraído de botões funciona sobre… |
| midnight-paint-splash-family-matching-tops | ro | body | translation_defect/glued-letter | EImprimare abstractă expresivă: Un sol întunecat și motive luminoase cu stropi d… |
| midnight-paint-splash-family-matching-tops | sv | body | translation_defect/glued-letter | EExpressivt abstrakt tryck: En mörk grund och ljusa flerfärgade målarstänksmotiv… |
| midnight-palm-blossom-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Midnight Palm Blossom vrství zelené a světlé palmové listy s růžovými a k… |
| midnight-palm-blossom-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| midnight-palm-blossom-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo lämpimän sään kerros: Rento napitusmuoto toimii yksinkertaisen aluspaida… |
| midnight-palm-blossom-family-matching-tops | ko | body | translation_defect/glued-letter | E편안한 따뜻한 날씨 레이어: 여유로운 버튼업 모양으로 심플한 언더셔츠 위에 착용하거나 독립형 상의로도 활용 가능합니다. |
| midnight-palm-blossom-family-matching-tops | pl | body | translation_defect/glued-letter | EWygodna warstwa na ciepłe dni: Swobodny, zapinany krój można nosić na prostym p… |
| midnight-palm-blossom-family-matching-tops | pt-BR | body | translation_defect/glued-letter | ECamada fácil para clima quente: O formato descontraído de botões funciona sobre… |
| mommy-and-me-french-halter-neck-tiered-dress-white-cotton-silk-sleeveless-a-line-beach-dress | en | body | health_skin/gentle-skin | …(viscose shell / polyester lining) feels gentle against skin, with a fluid drape |
| monochrome-palm-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Monochromatická dlaň umístí černé siluety palmy na čistou bílou zem. |
| monochrome-palm-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| monochrome-palm-family-matching-tops | cs | body | translation_defect/glued-letter | ESnadný styl do teplého počasí: Tvar s krátkým rukávem na knoflíky se snadno kom… |
| monochrome-palm-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo muotoilu lämpimässä säässä: Lyhythihainen nappimuoto sopii helposti yksi… |
| monochrome-palm-family-matching-tops | ko | body | translation_defect/glued-letter | E따뜻한 날씨 스타일링: 반팔 버튼업 형태로 심플한 가족룩과 잘 어울립니다. |
| monochrome-palm-family-matching-tops | pt-BR | body | translation_defect/glued-letter | EEstilo fácil para clima quente: O formato de botão de manga curta combina facil… |
| navy-red-floral-family-matching-set | cs | body | translation_defect/glued-letter | SDlouhé šaty bez rukávů: Tvar šatů dává dívkám a maminkám vzdušný výstřih a snad… |
| navy-red-floral-family-matching-set | cs | body | translation_defect/glued-letter | SLesk na košile: Košile s límečkem s krátkým rukávem dodávají chlapcům a tatínků… |
| pastel-bloom-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | APřidejte své velikosti a přineste si domů odpovídající sadu letních šatů, která… |
| pastel-bloom-mommy-and-me-dresses | da | body | translation_defect/glued-letter | ATilføj dine størrelser og tag et matchende solkjolesæt med hjem, der føles klar… |
| pastel-bloom-mommy-and-me-dresses | de | body | translation_defect/glued-letter | BLuftige ärmellose Passform: Die leichte gewebte Konstruktion sorgt für eine loc… |
| pastel-bloom-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | ALisää kokoasi ja tuo kotiin sopiva aurinkomekkosetti, joka tuntuu valmiilta jok… |
| pastel-bloom-mommy-and-me-dresses | no | body | translation_defect/glued-letter | ALegg til størrelsene dine og få med deg et matchende sundress-sett som føles kl… |
| pastel-mermaid-mommy-and-me-swimsuits | de | body | translated_claim/performance | …rjungfrauen-Schuppen-Design sticht garantiert hervor, während die zusätzlichen R… |
| pastel-watercolor-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | PTisk: Pastelový akvarel mísí růžové, broskvové, žluté a zelené květinové nádech… |
| pastel-watercolor-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | PPastelová květinová paleta: Růžové, broskvové, žluté a zelené tóny jemně ladí p… |
| pastel-watercolor-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | AVzdušný vrstvený vzhled: Styl překrytí bez rukávů udržuje šaty lehké a příjemné… |
| pastel-watercolor-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | AIlmainen kerroksittainen ulkoasu: Hihaton päällysmuotoilu pitää mekon kevyenä j… |
| pastel-watercolor-mommy-and-me-dresses | no | body | translation_defect/glued-letter | AHelt lagvis utseende: Ermeløs overleggsstyling holder kjolen lett og bevegelses… |
| pastel-watercolor-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | AAspect stratificat aeris: Modelul suprapus fără mâneci menține rochia lejeră și… |
| peach-sweetheart-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | EJednoduché natahovací šortky: Zakrytý elastický pas pro pohodlí po celou noc. |
| peach-sweetheart-mommy-and-me-pajamas | fi | body | translation_defect/glued-letter | EHelppo vedettävät shortsit: Peitetty joustava vyötärö mukavuutta koko yön ajan. |
| peach-sweetheart-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E쉬운 풀온 반바지: 신축성 있는 허리로 밤새 편안함을 선사합니다. |
| peach-sweetheart-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | EShorts pull-on fáceis: Cintura elástica coberta para conforto a noite toda. |
| picnic-plaid-family-matching-set | cs | body | translation_defect/glued-letter | PDetaily připravené na fotografování: Krajkové panely a ginghamové šeky jsou vyl… |
| pink-horizon-family-matching-set | cs | body | translation_defect/glued-letter | SLesk na košile: Košile s límečkem vepředu na knoflíky dodávají tatínkům a chlap… |
| pink-horizon-family-matching-set | cs | body | translation_defect/glued-letter | VKomfort připravený na dovolenou: Lehká tkaná bavlna udržuje celou sadu prodyšno… |
| pink-lace-garden-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | OVěrný krajkový límec: Výrazný bílý límeček dodává mamince a mini šatech okouzlu… |
| pink-lace-garden-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | EHelppo rypytetty hame: Rento midi-muoto liikkuu kauniisti juhliin, lomiin ja mu… |
| pink-lace-garden-mommy-and-me-dresses | ko | body | translation_defect/glued-letter | E이지 개더 스커트: 여유로운 미디 형태가 파티, 휴가, 인물 사진에 아름답게 움직입니다. |
| pink-lace-garden-mommy-and-me-dresses | pt-BR | body | translation_defect/glued-letter | ESaia franzida fácil: O formato midi descontraído combina perfeitamente com fest… |
| pink-lace-garden-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | OGuler de dantelă de dimensiuni mari: Gulerul alb adaugă un finisaj fermecător d… |
| pink-lace-garden-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | EFusta strânsă ușor: Forma midi relaxată se mișcă frumos pentru petreceri, vacan… |
| pink-resort-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | PTisk: Pink Resort Ruffle udržuje vzhled jemný a připravený na dovolenou v příbě… |
| pink-resort-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | PDekolt připravený k fotografování: Volný stylový rámeček pro portréty za tepléh… |
| pink-resort-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | EJednoduchá růžová paleta: Jednobarevná růžová udržuje jednoduchý vzhled pro plá… |
| pink-resort-ruffle-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | APřidejte velikosti, které potřebujete, a vytvořte jemné ladící šaty pro příští… |
| pink-resort-ruffle-mommy-and-me-dresses | da | body | translation_defect/glued-letter | ATilføj de størrelser, du har brug for, og skab et blødt matchende kjoleøjeblik… |
| pink-resort-ruffle-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | EHelppo vaaleanpunainen paletti: Yksinkertainen vaaleanpunainen pitää ulkonäön y… |
| pink-resort-ruffle-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | ALisää tarvitsemasi koot ja luo pehmeä yhteensopiva mekkohetki seuraavaa aurinko… |
| pink-resort-ruffle-mommy-and-me-dresses | ko | body | translation_defect/glued-letter | E이지 핑크 팔레트: 솔리드 핑크는 해변, 리조트, 생일 및 가족 사진 의상에 심플한 룩을 유지합니다. |
| pink-resort-ruffle-mommy-and-me-dresses | no | body | translation_defect/glued-letter | ALegg til størrelsene du trenger og skap et mykt, matchende kjoleøyeblikk for ne… |
| pink-resort-ruffle-mommy-and-me-dresses | pt-BR | body | translation_defect/glued-letter | EPaleta rosa fácil: Rosa sólido mantém a aparência simples para roupas de praia,… |
| pink-resort-ruffle-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | EPaletă roz ușoară: Rozul solid păstrează aspectul simplu pentru ținute de plajă… |
| pink-tropical-mommy-and-me-swimsuits | fr | body | translated_claim/performance | …le de nylon et de polyester, ce duo garantit à vous et à votre enfant un confort… |
| playful-cat-parade-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Hravý kočičí průvod zaplňuje měkkou pastelovou půdu živým davem kreslenýc… |
| playful-cat-parade-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| playful-cat-parade-family-matching-tops | cs | body | translation_defect/glued-letter | EStyl pro snadné teplé počasí: Uvolněný tvar s krátkým rukávem a zapínáním na kn… |
| playful-cat-parade-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo muotoilu lämpimässä säässä: Rento lyhythihainen nappikiinnitys toimii it… |
| playful-cat-parade-family-matching-tops | ko | body | translation_defect/glued-letter | E따뜻한 날씨에 간편한 스타일링: 여유로운 반소매 버튼업 형태가 캐주얼 계획에 독립형 탑으로 적합합니다. |
| playful-cat-parade-family-matching-tops | pt-BR | body | translation_defect/glued-letter | EEstilo fácil para clima quente: O formato descontraído de manga curta com botõe… |
| playful-cat-parade-family-matching-tops | ro | body | translation_defect/glued-letter | EStil facil pe vreme caldă: Forma relaxată, cu mânecă scurtă, cu nasturi, funcți… |
| playful-graphic-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Hravá grafika umisťuje veselé kreslené ikony přes rameno a hruď pro jasný… |
| playful-graphic-family-matching-tops | cs | body | translation_defect/glued-letter | ESilueta jednoduchého trička: Topy s krátkým rukávem a výstřihem se přirozeně ho… |
| playful-graphic-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo t-siluetti: Pyöreäkauluksiset lyhythihaiset topit sopivat luonnollisesti… |
| playful-graphic-family-matching-tops | ko | body | translation_defect/glued-letter | E이지 티셔츠 실루엣: 크루넥 반소매 탑은 데님, 반바지, 스커트 또는 캐주얼 바지와 자연스럽게 어울립니다. |
| playful-graphic-family-matching-tops | pl | body | translation_defect/glued-letter | EProsta sylwetka koszulki: Topy z okrągłym dekoltem i krótkim rękawem doskonale… |
| playful-graphic-family-matching-tops | pt-BR | body | translation_defect/glued-letter | ESilhueta fácil de camiseta: Tops de manga curta com gola redonda combinam natur… |
| polar-adventure-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E간편한 관리: 찬물로 기계 세탁, 저온에서 회전식 건조. |
| polar-adventure-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | ECuidado fácil: Lavar à máquina com água fria e secar em temperatura baixa. |
| polka-dot-mommy-and-me-dresses | es | body | translation_defect/glued-letter | REscote con ribete de volantes: Los suaves volantes delanteros y el escote cuadr… |
| polka-dot-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | EHelppo rypytetty hame: Rento midi-muoto liikkuu kauniisti juhliin, lomiin ja mu… |
| polka-dot-mommy-and-me-dresses | fr | body | translation_defect/glued-letter | REncolure à volants : Des volants doux sur le devant et une encolure carrée ajou… |
| polka-dot-mommy-and-me-dresses | ko | body | translation_defect/glued-letter | E이지 개더 스커트: 여유로운 미디 형태가 파티, 휴가, 인물 사진에 아름답게 움직입니다. |
| polka-dot-mommy-and-me-dresses | pt-BR | body | translation_defect/glued-letter | ESaia franzida fácil: O formato midi descontraído combina perfeitamente com fest… |
| polka-dot-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | EFusta strânsă ușor: Forma midi relaxată se mișcă frumos pentru petreceri, vacan… |
| powder-blue-mommy-and-me-set | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  AVzdušný letní pocit: Lehké tkané struktury. |
| powder-blue-mommy-and-me-set | cs | body | translation_defect/glued-letter | PKontrast připravený na fotografování: Prášková modrá a ostrá bílá vytvářejí svě… |
| powder-blue-mommy-and-me-set | cs | body | translation_defect/glued-letter | APřidejte své velikosti a zajistěte, aby další den na pláži, prázdninová večeře… |
| powder-blue-mommy-and-me-set | da | body | translation_defect/glued-letter | ATilføj dine størrelser og få den næste stranddag, feriemiddag eller familiebill… |
| powder-blue-mommy-and-me-set | es | body | translation_defect/glued-letter | AComodidad ajustable: Las correas y una cinturilla fácil ayudan a que cada talla… |
| powder-blue-mommy-and-me-set | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlman kesätunnelma: Kevyet kudotut pinnat. |
| powder-blue-mommy-and-me-set | fi | body | translation_defect/glued-letter | ASäädettävä mukavuus: Hihnat ja helppo vyötärönauha helpottavat jokaisen koon mu… |
| powder-blue-mommy-and-me-set | fi | body | translation_defect/glued-letter | ALisää kokoasi ja saat seuraavan rantapäivän, lomaillallisen tai perhekuvan tunt… |
| powder-blue-mommy-and-me-set | no | body | translation_defect/glued-letter | ALegg til størrelsene dine og få neste stranddag, feriemiddag eller familiebilde… |
| powder-blue-mommy-and-me-set | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASenzație de vară aerisită: Texturi țesute ușoare. |
| powder-blue-mommy-and-me-set | ro | body | translation_defect/glued-letter | AConfort reglabil: Curelele și o centură ușoară ajută la purtarea confortabilă a… |
| rainbow-stripe-family-matching-set | cs | body | translation_defect/glued-letter | SVklouzněte do Rainbow Stripe a připravte se na to, aby každý okamžik odpovídal… |
| rainbow-trim-mommy-and-me-swimsuits | es | body | translated_claim/performance | …a silueta fresca y moderna, que te garantiza un aspecto tan atractivo como te si… |
| rainbow-trim-mommy-and-me-swimsuits | fr | body | translated_claim/performance | …la piscine, ce maillot de bain vous garantit une coupe à la fois confortable et… |
| rainbow-trim-mommy-and-me-swimsuits | pl | body | translated_claim/performance | Szykowny design gwarantuje, że poczujesz się pewnie, a zabawne detale zachwycą d… |
| rainbow-trim-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | O design chique garante que você se sinta confiante, enquanto os detalhes divert… |
| red-gingham-mommy-and-me-set | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  AVzdušný letní pocit: Lehká tkanina ze směsi bavlny udržuje… |
| red-gingham-mommy-and-me-set | cs | body | translation_defect/glued-letter | PKontrast připravený na fotografování: Bílé krajkové lemování a červený gingham… |
| red-gingham-mommy-and-me-set | cs | body | translation_defect/glued-letter | PPohodlí při navlékání: Snadný pas a uvolněný široký střih nohavic pomáhá každé… |
| red-gingham-mommy-and-me-set | cs | body | translation_defect/glued-letter | APřidejte své velikosti a zajistěte, aby byl příští piknik, prázdninový den nebo… |
| red-gingham-mommy-and-me-set | da | body | translation_defect/glued-letter | ATilføj dine størrelser og få den næste picnic, feriedag eller familiebillede ti… |
| red-gingham-mommy-and-me-set | fi | body | translation_defect/glued-letter | Pääominaisuudet:  AIlman kesätunnelma: Kevyt puuvillasekoitekangas pitää setin m… |
| red-gingham-mommy-and-me-set | fi | body | translation_defect/glued-letter | ALisää kokosi ja tee seuraava piknik, lomapäivä tai perhevalokuva heti koordinoi… |
| red-gingham-mommy-and-me-set | no | body | translation_defect/glued-letter | ALegg til størrelsene dine og få neste piknik, feriedag eller familiebilde til å… |
| red-gingham-mommy-and-me-set | ro | body | translation_defect/glued-letter | Caracteristici cheie:  ASensă de vară aerisită: Țesătura ușoară din amestec de b… |
| red-plaid-family-matching-tops | cs | body | translation_defect/glued-letter | PReference na tisk: Červený pléd kombinuje červené, zelené a bílé kostky pro tep… |
| red-stripe-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Červený proužek udržuje outfit jednoduchý a všestranný, s klasickým tvare… |
| red-stripe-family-matching-tops | cs | body | translation_defect/glued-letter | PPruh připravený k fotografování: Jemná červená barva, vodorovné pruhy, malá srd… |
| red-stripe-family-matching-tops | cs | body | translation_defect/glued-letter | EJednoduchý styl: Pár s ležérními kalhotami pro čistý rodinný vzhled. |
| red-stripe-family-matching-tops | ko | body | translation_defect/glued-letter | E간편한 스타일링 : 캐주얼 팬츠와 함께 깔끔한 패밀리룩을 연출해보세요. |
| red-stripe-family-matching-tops | pt-BR | body | translation_defect/glued-letter | EEstilo fácil: Combine com calças casuais para um visual familiar limpo. |
| red-stripe-family-matching-tops | ro | body | translation_defect/glued-letter | EStil facil: Pereche cu pantaloni casual pentru un aspect curat de familie. |
| red-tropical-mommy-and-me-swimsuits | es | body | translated_claim/performance | …la de fibras de nailon y poliéster garantiza un tacto suave y una gran elasticid… |
| red-tropical-mommy-and-me-swimsuits | it | body | translated_claim/performance | …mix di fibre di nylon e poliestere garantisce una sensazione morbida e un'ampia… |
| red-tropical-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …miękkość i dużą rozciągliwość, co gwarantuje komfort noszenia przez cały dzień. |
| red-tropical-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | …ura de fibras de náilon e poliéster garante um toque suave e bastante elasticida… |
| red-tropical-mommy-and-me-swimsuits | ro | body | english_leftover/long-lasting | Este o dovadă a stilului durabil și a legăturilor familiale, învăluită în bucuri… |
| ring-accent-mommy-and-me-swimsuits | es | body | translated_claim/performance | …ste personalizado y seguro, lo que garantiza comodidad para el uso durante todo… |
| ring-accent-mommy-and-me-swimsuits | it | body | translated_claim/performance | …elezione di colori vivaci e audaci garantisce che ogni coppia possa trovare il p… |
| ring-accent-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …bare, veilige pasvorm, die comfort garandeert voor de hele dag tijdens elke wate… |
| ring-accent-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | …ções em cores vibrantes e marcantes garante que cada dupla encontre sua combinaç… |
| ruffle-hem-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | PTisk: Volánkový lem je dodáván v jemných fialových a růžových barvách s romanti… |
| ruffle-hem-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | STvar letních šatů bez rukávů: Kulatý výstřih a snadný střih udrží vzhled pohodl… |
| ruffle-top-mommy-and-me-swimsuits | en | body | performance/perfect-fit | …n top with adjustable straps ensures a perfect fit and adds a touch of feminine… |
| ruffle-top-mommy-and-me-swimsuits | cs | body | translated_claim/performance | …s nastavitelnými ramínky zajišťuje dokonalé padnutí a přidává nádech ženskosti. |
| ruffle-top-mommy-and-me-swimsuits | de | body | translated_claim/performance | …llbaren Trägern sorgt für eine perfekte Passform und verleiht eine feminine Note… |
| ruffle-top-mommy-and-me-swimsuits | es | body | translated_claim/performance | …de volantes y tirantes ajustables garantiza un ajuste perfecto y añade un toque… |
| ruffle-top-mommy-and-me-swimsuits | es | body | translated_claim/performance | …irantes ajustables garantiza un ajuste perfecto y añade un toque de estilo femen… |
| ruffle-top-mommy-and-me-swimsuits | fr | body | translated_claim/performance | …t bretelles réglables assure une coupe parfaite et ajoute une touche de féminité… |
| ruffle-top-mommy-and-me-swimsuits | it | body | translated_claim/performance | …e con volant e spalline regolabili garantisce una vestibilità perfetta e aggiung… |
| ruffle-top-mommy-and-me-swimsuits | it | body | translated_claim/performance | …ine regolabili garantisce una vestibilità perfetta e aggiunge un tocco di femmin… |
| ruffle-top-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …stelbare bandjes zorgt voor een perfecte pasvorm en voegt een vleugje vrouwelijk… |
| ruffle-top-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …regulowanymi ramiączkami zapewnia idealne dopasowanie i dodaje kobiecego uroku. |
| ruffle-top-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | …ante com babados e alças ajustáveis garante um ajuste perfeito e adiciona um toq… |
| safari-caravan-family-matching-set | cs | body | translation_defect/glued-letter | SLesk na košile: Košile s límečkem s krátkým rukávem dodávají chlapcům a tatínků… |
| safari-caravan-family-matching-set | cs | body | translation_defect/glued-letter | VKomfort připravený na dovolenou: Lehká tkaná bavlna udržuje vzhled celé rodiny… |
| scarlet-blossom-family-matching-set | cs | body | translation_defect/glued-letter | SLesk na košile: Košile s límečkem s krátkým rukávem dodávají chlapcům a tatínků… |
| seaside-blue-plaid-family-matching-set | cs | body | translation_defect/glued-letter | SRozsah velikostí: dívky a chlapci 1-2Y-10Y; Matka S-XL; Otec M-4XL. |
| sky-daisy-doodle-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Doodle Sky Daisy spojuje nadměrně velké bílé sedmikrásky a teplé žluté st… |
| sky-daisy-doodle-family-matching-tops | cs | body | translation_defect/glued-letter | Klíčové vlastnosti:  OJedna sladěná košile: Stejný vzhled s krátkým rukávem a za… |
| sky-daisy-doodle-family-matching-tops | fi | body | translation_defect/glued-letter | EHelppo lämpimän sään kerros: Rento napitusmuoto toimii yksinkertaisen aluspaida… |
| sky-daisy-doodle-family-matching-tops | ko | body | translation_defect/glued-letter | E편안한 따뜻한 날씨 레이어: 여유로운 버튼업 모양으로 심플한 언더셔츠 위에 착용하거나 독립형 상의로도 활용 가능합니다. |
| sky-daisy-doodle-family-matching-tops | pl | body | translation_defect/glued-letter | EWygodna warstwa na ciepłe dni: Swobodny, zapinany krój można nosić na prostym p… |
| sky-daisy-doodle-family-matching-tops | pt-BR | body | translation_defect/glued-letter | ECamada fácil para clima quente: O formato descontraído de botões funciona sobre… |
| spooky-skeleton-family-matching-onesie-pajamas | en | body | internal_leak/internal-note | Weight and waist measurements are not available. |
| summer-plaid-family-matching-set | de | body | translated_claim/performance | …mischung für die Cargoshorts — gut im Lagenlook zu tragen und schnell trocknend. |
| summer-plaid-family-matching-set | es | body | translated_claim/performance | …e algodón para los shorts cargo — fácil de combinar en capas y de secado rápido. |
| summer-plaid-family-matching-set | fr | body | translated_claim/performance | …en coton mélangé pour le short cargo — facile à superposer et à séchage rapide. |
| summer-plaid-family-matching-set | nl | body | translated_claim/performance | …van katoenmix voor de cargoshort: makkelijk in laagjes te dragen en sneldrogend. |
| summer-plaid-family-matching-set | pt-BR | body | translated_claim/performance | …lgodão misto para a bermuda cargo: fácil de usar em camadas e de secagem rápida. |
| sunlit-tropical-bloom-family-matching-tops | cs | body | translation_defect/glued-letter | PTisk: Sunlit Tropical Bloom vrství zelené tropické listy, žluté květy a oranžov… |
| sunlit-tropical-bloom-family-matching-tops | ro | body | translation_defect/glued-letter | Caracteristici cheie:  OPrint de familie: Aceeași opera de artă florală tropical… |
| tie-shoulder-mommy-and-me-swimsuits | de | body | translated_claim/performance | …zahl von Größen finden Sie die perfekte Passform, die jede Kurve betont und Selb… |
| tie-shoulder-mommy-and-me-swimsuits | es | body | translated_claim/performance | …rantes, comodidad y versatilidad, garantizando que ambas destaquen en cualquier… |
| tie-shoulder-mommy-and-me-swimsuits | es | body | translated_claim/performance | …riedad de tamaños, encuentre el ajuste perfecto que favorezca cada curva e infun… |
| tie-shoulder-mommy-and-me-swimsuits | fr | body | translated_claim/performance | …e variété de tailles, trouvez la coupe parfaite qui mettra en valeur toutes les… |
| tie-shoulder-mommy-and-me-swimsuits | it | body | translated_claim/performance | …a varietà di taglie, trova la vestibilità perfetta che valorizza ogni curva e in… |
| tie-shoulder-mommy-and-me-swimsuits | nl | body | translated_claim/performance | …heidenheid aan maten vind je de perfecte pasvorm die elke curve flatteert en zel… |
| tie-shoulder-mommy-and-me-swimsuits | pl | body | translated_claim/performance | …różnorodnym rozmiarom znajdź idealne dopasowanie, które podkreśla każdą sylwetk… |
| top-dad-and-top-son-matching-t-shirt-onesie-set-inspired-family-outfit | de | body | translated_claim/performance | …ing oder um eure coole Verbindung zu zeigen, dieses Set wird garantiert ein Hit. |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | en | body | performance/perfect-fit | …omprehensive range of sizes to ensure a great fit for fathers and sons of all ag… |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | de | body | translated_claim/performance | …assende Größenauswahl für eine perfekte Passform von Vätern und Söhnen jeden Alt… |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | es | body | translated_claim/performance | …todos : amplia gama de tallas para garantizar un ajuste perfecto para padres e h… |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | es | body | translated_claim/performance | …ma de tallas para garantizar un ajuste perfecto para padres e hijos de todas las… |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | nl | body | translated_claim/performance | …ebreid assortiment maten om een perfecte pasvorm te garanderen voor vaders en zo… |
| tropical-flair-father-and-son-matching-swim-trunks-flamingo-and-foliage-print | pl | body | translated_claim/performance | …borowi rozmiarów łatwo znaleźć idealne dopasowanie zarówno dla taty, jak i syna. |
| tropical-matching-family-beach-outfits-colorful-leaf-print-summer-dresses-shorts-set | el | body | internal_leak/vendor-host | URL host c***.com |
| tropical-meadow-family-matching-set | cs | body | translation_defect/glued-letter | PPrint: Tropická louka — malířsky poseté květiny se žlutými, růžovými, purpurový… |
| tropical-meadow-family-matching-set | cs | body | translation_defect/glued-letter | SVklouzněte do Tropical Meadow a propojte každý okamžik – od brunche po pláž, př… |
| tropical-meadow-family-matching-set | de | body | translation_defect/glued-letter | AVerstellbare Passform (Kleider): Schulterbänder und elastische Empire-Taille fü… |
| tropical-meadow-family-matching-set | pl | body | translation_defect/glued-letter | ARegulowany krój (sukienki): Wiązania na ramionach i elastyczna talia typu Empir… |
| tropical-meadow-family-matching-set | pt-BR | body | translation_defect/glued-letter | AAjuste ajustável (vestidos): Laços de ombro e cintura império elástica para fác… |
| tropical-zip-mommy-and-me-swimsuits | es | body | translated_claim/performance | …o fácil y un ajuste seguro, lo que garantiza comodidad durante las actividades a… |
| tropical-zip-mommy-and-me-swimsuits | it | body | translated_claim/performance | Il materiale morbido e traspirante garantisce comfort per tutto il giorno sia pe… |
| tropical-zip-mommy-and-me-swimsuits | pt-BR | body | translated_claim/performance | Material macio e respirável garante conforto o dia todo para adultos e crianças. |
| vintage-cottage-floral-mommy-and-me-pajama-set | en | body | performance/fabric-behavior | Breathable cotton weave keeps airflow high and wrinkles low. |
| vintage-cottage-floral-mommy-and-me-pajama-set | en | body | performance/wrinkle | Breathable cotton weave keeps airflow high and wrinkles low. |
| vintage-cottage-floral-mommy-and-me-pajama-set | cs | body | translation_defect/glued-letter | VKvětinový potisk staré chalupy: Kytice hortenzií, tulipánů a divokých květin ro… |
| vintage-cottage-floral-mommy-and-me-pajama-set | cs | body | translation_defect/glued-letter | PStahovací šortky: Měkký elastický pas pro snadné oblékání a svlékání a pohodlí… |
| vintage-cottage-floral-mommy-and-me-pajama-set | cs | body | translation_defect/glued-letter | APřidejte do košíku velikost pro matku a odpovídající velikost pro děti, aby kaž… |
| vintage-cottage-floral-mommy-and-me-pajama-set | fi | body | translation_defect/glued-letter | EHelppo hoito ja hengittävä: Konepesu kylmässä, rumpukuivaus matalalla. |
| vintage-cottage-floral-mommy-and-me-pajama-set | fi | body | translation_defect/glued-letter | ALisää äitikoko ja vastaava lasten koko ostoskoriin, jotta jokainen hetki sopii… |
| vintage-cottage-floral-mommy-and-me-pajama-set | ko | body | translation_defect/glued-letter | E간편한 관리 및 통기성: 찬물로 기계 세탁, 낮은 온도로 회전식 건조. |
| vintage-cottage-floral-mommy-and-me-pajama-set | no | body | translation_defect/glued-letter | ALegg til morstørrelsen og den matchende barnestørrelsen i handlekurven for å få… |
| vintage-cottage-floral-mommy-and-me-pajama-set | pl | body | translation_defect/glued-letter | ADodaj do koszyka rozmiar dla matki i odpowiadający mu rozmiar dla dziecka, aby… |
| vintage-cottage-floral-mommy-and-me-pajama-set | pt-BR | body | translation_defect/glued-letter | ECuidado fácil e respirável: Lavar à máquina com água fria e secar em temperatur… |
| vintage-cottage-floral-mommy-and-me-pajama-set | ro | body | translation_defect/glued-letter | IDimensiuni inclusive: Fete 2–10 ani și Mame S–XL — adăugați-le pe ambele în coș… |
| vintage-cottage-floral-mommy-and-me-pajama-set | sv | body | translation_defect/glued-letter | ELättskött och andningsbar: Maskintvättas kallt, torktumlas låg. |
| vintage-cottage-floral-mommy-and-me-pajama-set | sv | body | translation_defect/glued-letter | ALägg till moderstorleken och den matchande barnstorleken i din kundvagn för att… |
| watercolor-bunny-garden-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | …výška (cm/in)  Hrudník/prsa (cm/in)  SDélka rukávu (cm/in)  Boky (cm/in)  Délka… |
| welsh-dinosaur-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PTisk: Akvarel Velšští dinosauři a pohádkoví draci plující na pastelových oblací… |
| welsh-dinosaur-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | SRozsah velikosti: Dítě od 2 let do 9–10 let pro nejmenší; Matka S až Matka XL p… |
| welsh-dinosaur-mommy-and-me-pajamas | cs | body | translation_defect/glued-letter | PPerfect Print: Akvarelové umění velšského draka a dinosauřího mláděte, které kr… |
| welsh-dinosaur-mommy-and-me-pajamas | de | body | translation_defect/glued-letter | EShorts mit elastischem Bund: Sommershorts mit entspanntem Bein und dehnbarem An… |
| welsh-dinosaur-mommy-and-me-pajamas | fr | body | translation_defect/glued-letter | EShort à taille élastique : Short d'été à jambe décontractée avec une taille ext… |
| welsh-dinosaur-mommy-and-me-pajamas | ko | body | translation_defect/glued-letter | E탄성 허리 반바지: 신축성 있는 풀온 허리밴드가 있는 편안한 다리의 여름 반바지 - 어린 아이에게도 쉽고 엄마에게도 편안합니다. |
| welsh-dinosaur-mommy-and-me-pajamas | pt-BR | body | translation_defect/glued-letter | EShorts de cintura elástica: Shorts de verão com pernas relaxadas e cós elástico… |
| willow-mist-mommy-and-me-dresses | cs | body | translation_defect/glued-letter | SLetní tvar bez rukávů: Pásky na zavazování a vzdušný živůtek udržují siluetu sl… |
| willow-mist-mommy-and-me-dresses | fi | body | translation_defect/glued-letter | EHelppo rypytetty hame: Rento midi-muoto liikkuu kauniisti juhliin, lomiin ja mu… |
| willow-mist-mommy-and-me-dresses | ko | body | translation_defect/glued-letter | E이지 개더 스커트: 여유로운 미디 형태가 파티, 휴가, 인물 사진에 아름답게 움직입니다. |
| willow-mist-mommy-and-me-dresses | pt-BR | body | translation_defect/glued-letter | ESaia franzida fácil: O formato midi descontraído combina perfeitamente com fest… |
| willow-mist-mommy-and-me-dresses | ro | body | translation_defect/glued-letter | EFusta strânsă ușor: Forma midi relaxată se mișcă frumos pentru petreceri, vacan… |
