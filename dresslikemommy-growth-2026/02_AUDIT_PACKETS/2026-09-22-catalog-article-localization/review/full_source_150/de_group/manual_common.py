# Human/model-authored literal translations; no machine-translation providers.
LOCALES=['cs','da','el','fi','no','ro']
COMMON={l:{} for l in LOCALES}
def common(source,values):
 assert len(values)==6
 for l,v in zip(LOCALES,values):COMMON[l][source]=v
common('Fabric:', ['Materiál:','Materiale:','Ύφασμα:','Materiaali:','Stoff:','Material:'])
common('Fabric &amp; feel:', ['Materiál a omak:','Materiale og fornemmelse:','Ύφασμα και αίσθηση:','Materiaali ja tuntu:','Stoff og følelse:','Material și senzație:'])
common('Family story:', ['Rodinný styl:','Familiens stil:','Οικογενειακό στυλ:','Perheen tyyli:','Familiens stil:','Stil pentru familie:'])
common('Print:', ['Vzor:','Mønster:','Σχέδιο:','Kuvio:','Mønster:','Model:'])
common('Print reference:', ['Popis vzoru:','Mønsterbeskrivelse:','Περιγραφή σχεδίου:','Kuvion kuvaus:','Mønsterbeskrivelse:','Descrierea modelului:'])
common('Color:', ['Barva:','Farve:','Χρώμα:','Väri:','Farge:','Culoare:'])
common('Design details:', ['Detaily provedení:','Designdetaljer:','Λεπτομέρειες σχεδιασμού:','Mallin yksityiskohdat:','Designdetaljer:','Detalii de design:'])
common('Care:', ['Péče:','Pleje:','Φροντίδα:','Hoito:','Vedlikehold:','Îngrijire:'])
common('Size range:', ['Rozsah velikostí:','Størrelsesudvalg:','Διαθέσιμα μεγέθη:','Kokovalikoima:','Størrelsesutvalg:','Gama de mărimi:'])
common('Key Features:', ['Hlavní vlastnosti:','Vigtigste egenskaber:','Βασικά χαρακτηριστικά:','Keskeiset ominaisuudet:','Viktige egenskaper:','Caracteristici principale:'])
common('Size', ['Velikost','Størrelse','Μέγεθος','Koko','Størrelse','Mărime'])
common('Age', ['Věk','Alder','Ηλικία','Ikä','Alder','Vârstă'])
common('Weight', ['Hmotnost','Vægt','Βάρος','Paino','Vekt','Greutate'])
common('Height', ['Výška','Højde','Ύψος','Pituus','Høyde','Înălțime'])
common('Chest/Bust', ['Hrudník/prsa','Bryst','Στήθος','Rinta','Bryst','Torace/bust'])
common('Sleeve or Skirt', ['Rukáv nebo sukně','Ærme eller nederdel','Μανίκι ή φούστα','Hiha tai hame','Erme eller skjørt','Mânecă sau fustă'])
common('Pant/Short or -', ['Kalhoty/šortky nebo -','Bukser/shorts eller -','Παντελόνι/σορτς ή -','Housut/shortsit tai -','Bukser/shorts eller -','Pantaloni/pantaloni scurți sau -'])
common('Hip', ['Boky','Hofte','Γοφοί','Lantio','Hofte','Șolduri'])
common('Waist', ['Pas','Talje','Μέση','Vyötärö','Midje','Talie'])
common('Garment Length', ['Délka oděvu','Beklædningslængde','Μήκος ενδύματος','Vaatteen pituus','Plaggets lengde','Lungimea articolului'])
common('Skirt Length', ['Délka sukně','Nederdelslængde','Μήκος φούστας','Hameen pituus','Skjørtlengde','Lungimea fustei'])
common('Sleeve or -', ['Rukáv nebo -','Ærme eller -','Μανίκι ή -','Hiha tai -','Erme eller -','Mânecă sau -'])
common('Adjustable Strap', ['Nastavitelné ramínko','Justerbar skulderstrop','Ρυθμιζόμενη τιράντα','Säädettävä olkain','Justerbar skulderstropp','Bretea reglabilă'])
common('Hem/Body Opening', ['Lem/otvor oděvu','Søm/åbning på overdelen','Στρίφωμα/άνοιγμα ενδύματος','Helma/vaatteen aukko','Fald/plaggåpning','Tiv/deschiderea articolului'])
common('Top Chest/Bust', ['Hrudník/prsa – top','Bryst – top','Στήθος τοπ','Topin rinta','Bryst – topp','Torace/bust – top'])
common('Top Length', ['Délka topu','Toplængde','Μήκος τοπ','Topin pituus','Topplengde','Lungimea topului'])
common('Pants Length', ['Délka kalhot','Bukselængde','Μήκος παντελονιού','Housujen pituus','Bukselengde','Lungimea pantalonilor'])
common('Top Hip', ['Boky – top','Hofte – top','Γοφοί τοπ','Topin lantio','Hofte – topp','Șolduri – top'])
common('Top Waist', ['Pas – top','Talje – top','Μέση τοπ','Topin vyötärö','Midje – topp','Talie – top'])
common('Pants Waist', ['Pas kalhot','Buksernes talje','Μέση παντελονιού','Housujen vyötärö','Buksenes midje','Talia pantalonilor'])
for s,vs in [
 ('Dress',['šaty','kjole','φόρεμα','mekko','kjole','rochie']),
 ('Shirt',['košile','skjorte','μπλούζα','paita','skjorte','cămașă']),
 ('Tank Top',['tílko','top med stropper','αμάνικο τοπ','hihaton toppi','singlet','top fără mâneci']),
 ('Two-Piece Set',['dvoudílná souprava','todelt sæt','σετ δύο τεμαχίων','kaksiosainen asu','todelt sett','set din două piese']),
 ('Top and Pants',['top a kalhoty','top og bukser','τοπ και παντελόνι','toppi ja housut','topp og bukser','top și pantaloni']),
 ('Beach Coverup Set',['plážová souprava přes plavky','strandsæt til at bære over badetøj','σετ παραλίας για πάνω από το μαγιό','uima-asun päälle puettava ranta-asu','strandsett til å ha over badetøy','set de plajă pentru purtat peste costumul de baie']),
 ('Tulle Skirt',['tylová sukně','tylnederdel','φούστα από τούλι','tyllihame','tyllskjørt','fustă din tul'])]:
 for l,v,pre in zip(LOCALES,vs,['Tabulka velikostí – ','Størrelsestabel – ','Πίνακας μεγεθών – ','Kokotaulukko – ','Størrelsestabell – ','Tabel de mărimi – ']):COMMON[l]['Size Chart - '+s]=pre+v
common('Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed.', ['Perte v pračce ve studené vodě na jemný program, sušte zavěšené, nebělte a v případě potřeby žehlete naruby při nízké teplotě.','Maskinvask koldt på skåneprogram, hæng til tørre, undgå blegemiddel, og stryg om nødvendigt på vrangen ved lav temperatur.','Πλύσιμο στο πλυντήριο με κρύο νερό σε απαλό πρόγραμμα, στέγνωμα απλωμένο, χωρίς λευκαντικό και, αν χρειάζεται, σιδέρωμα από την ανάποδη σε χαμηλή θερμοκρασία.','Konepesu kylmässä vedessä hellävaraisella ohjelmalla, ripustuskuivaus, ei valkaisuainetta ja tarvittaessa silitys nurjalta puolelta matalalla lämmöllä.','Maskinvask kaldt på skåneprogram, heng til tørk, ikke bruk blekemiddel, og stryk om nødvendig på vrangen ved lav temperatur.','Spălați la mașină cu apă rece, pe program delicat, uscați pe sârmă, nu folosiți înălbitor și, dacă este necesar, călcați pe dos la temperatură scăzută.'])
common('Machine wash cold on gentle, turn inside out, line dry, and avoid bleach.', ['Perte v pračce ve studené vodě na jemný program, obraťte naruby, sušte zavěšené a nepoužívejte bělidlo.','Maskinvask koldt på skåneprogram, vend på vrangen, hæng til tørre, og undgå blegemiddel.','Πλύσιμο στο πλυντήριο με κρύο νερό σε απαλό πρόγραμμα, γυρισμένο από την ανάποδη, στέγνωμα απλωμένο και χωρίς λευκαντικό.','Konepesu kylmässä vedessä hellävaraisella ohjelmalla, käännä nurinpäin, ripustuskuivaus ja vältä valkaisuainetta.','Maskinvask kaldt på skåneprogram, vreng plagget, heng til tørk og unngå blekemiddel.','Spălați la mașină cu apă rece, pe program delicat, întoarceți pe dos, uscați pe sârmă și evitați înălbitorul.'])
common('Mother-daughter sizing:', ['Velikosti pro maminky a dcery:','Størrelser til mor og datter:','Μεγέθη για μαμά και κόρη:','Koot äidille ja tyttärelle:','Størrelser til mor og datter:','Mărimi pentru mamă și fiică:'])
common('Photo-ready palette:', ['Barvy vhodné pro fotografie:','Farver klar til fotos:','Χρωματική παλέτα για φωτογραφίες:','Valokuvaukseen sopivat värit:','Farger klare for bilder:','Paletă de culori pentru fotografii:'])
common('Chart-backed variants:', ['Varianty podložené tabulkou:','Varianter baseret på tabellen:','Παραλλαγές με βάση τον πίνακα:','Taulukkoon perustuvat vaihtoehdot:','Varianter basert på tabellen:','Variante susținute de tabel:'])
common('Mom + daughter match:', ['Sladění maminky a dcery:','Match til mor og datter:','Ασορτί για μαμά και κόρη:','Yhteensopiva tyyli äidille ja tyttärelle:','Match til mor og datter:','Asortare pentru mamă și fiică:'])
common('Exact fiber composition was not visible in the supplied evidence.', ['Přesné složení vláken nebylo v poskytnutých podkladech viditelné.','Den præcise fibersammensætning fremgik ikke af det fremlagte materiale.','Η ακριβής σύνθεση των ινών δεν ήταν ορατή στα παρεχόμενα στοιχεία.','Tarkka kuitukoostumus ei käynyt ilmi toimitetusta aineistosta.','Den nøyaktige fibersammensetningen fremgikk ikke av det oppgitte materialet.','Compoziția exactă a fibrelor nu era vizibilă în dovezile furnizate.'])
