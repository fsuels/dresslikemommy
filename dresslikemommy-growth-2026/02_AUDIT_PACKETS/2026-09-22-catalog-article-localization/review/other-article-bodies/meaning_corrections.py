"""Exact corrections identified during full existing-body reading, excluding shared source update."""
PATCHES={
'ar':[
('الكريمي، البيج، الأسمر، والأبيض','الكريمي، البيج، البني الفاتح، والأبيض'),('الكروشيه، الكتان','القطع المحبوكة، الكتان'),('الزمرد، الياقوت، الياقوت الأحمر','الزمرد، الياقوت الأزرق، الياقوت الأحمر'),('الأحذية، الأوشحة','الأحذية ذات الساق العالية، الأوشحة'),('الكنزات الشتوية','كنزات الأعياد'),('اكوي أو أبخر كل شيء','اكوِ كل الملابس أو استخدم البخار'),('القبعات، الأقواس','القبعات، الفيونكات')],
'cs':[
('Krémová, béžová, tan a bílá','Krémová, béžová, světle hnědá a bílá'),('mommy and me šaty','šaty pro maminku a dceru'),('sladte ostatní','slaďte ostatní'),('Boty, šály','Kotníkové a vysoké boty, šály'),('vrásky jsou na fotkách vidět','záhyby jsou na fotkách vidět'),('Tátové a já outfity','Outfity pro tatínka a dítě')],
'da':[
('Koordinerede familieudseender','Koordinerede familielooks'),('farver, der komplimenterer hinanden','farver, der passer godt sammen'),('Creme, beige, tan og hvid','Creme, beige, lysebrun og hvid'),('efterårsbagskaber','efterårsbaggrunde'),('friske og strandede ud','friske og strandagtige ud'),('rynker ses på billeder','folder ses på billeder'),('familie fotografer','familiefotografer')],
'el':[
('οικογενειακά looks','οικογενειακές εμφανίσεις'),('για τα social media','για τα κοινωνικά δίκτυα'),('Τόνους Πολύτιμων Λίθων','Τόνοι Πολύτιμων Λίθων'),('μωβ γαλάζιο','απαλό γαλάζιο'),('casual πουκάμισα','καθημερινά πουκάμισα'),('μια δυσάρεστη με τέλεια ρούχα','μια οικογένεια που δεν αισθάνεται άνετα, ακόμη και με τέλεια ρούχα'),('Έτοιμα Σετ Οικογενειακής Αντιστοιχίας','Έτοιμα Ασορτί Οικογενειακά Σύνολα'),('Σετ οικογενειακής αντιστοιχίας','Ασορτί οικογενειακά σετ'),('Ολόκληρη οικογενειακή αντιστοιχία','Ασορτί ρούχα για όλη την οικογένεια'),('η απόλυτη ευκαιρία για αντιστοιχία','η απόλυτη ευκαιρία για ασορτί ντύσιμο')],
'es':[
('Fotos de invierno/vacaciones','Fotos de invierno y de fiestas'),('Las fotos de vacaciones son la mejor oportunidad para encontrar coincidencias','Las fotos de las fiestas son la mejor oportunidad para llevar prendas a juego'),('Emparejamiento familiar completo','Ropa a juego para toda la familia'),('todos coinciden, sin estrés','todos van a juego, sin estrés')],
'fi':[
('mitä me kaikki pukeudumme','mitä me kaikki puemme päällemme'),('Liina- tai puuvilla-asut','Pellava- tai puuvilla-asut'),('häiritsevät kasvoja','vievät huomion kasvoista')],
'fr':[
('coordonnez le reste de la tenue autour de celle-ci','coordonnez les tenues de tous les autres autour de celle-ci'),('Crème, beige, taupe et blanc','Crème, beige, brun clair et blanc'),('à la lumière dorée du crépuscule','à la lumière de l’heure dorée'),('les photos de vacances','les photos des fêtes'),("Photos d'hiver / de vacances","Photos d'hiver / des fêtes"),('Les photos de vacances sont l\'occasion idéale de faire des rencontres','Les photos des fêtes sont l’occasion idéale de porter des tenues assorties'),('La saison idéale pour les photos de famille','La saison la plus populaire pour les photos de famille'),('Repasser ou défroisser à la vapeur tout le temps','Repasser ou défroisser tous les vêtements à la vapeur'),('Appariement familial complet','Tenues assorties pour toute la famille')],
'hi':[
('पूरी परिवार','पूरा परिवार'),('ड्रेसy आउटफिट्स','औपचारिक कपड़े'),('candid शॉट्स','सहज तस्वीरें'),('झुर्रियां तस्वीरों में दिखती हैं','सिलवटें तस्वीरों में दिखती हैं'),('छुट्टियों','त्योहारों'),('सपनों जैसे और स्त्रीलिंग','सपनों जैसे और नारीसुलभ')],
'it':[
('fantasie e colori pieni','fantasie e tinte unite'),('Gli abiti coordinati fotografano magnificamente','Gli abiti coordinati rendono magnificamente in foto')],
'ja':[
('夕暮れ時の光に映え','ゴールデンアワーの光に映え'),('ママと私のドレス','ママと娘のお揃いドレス'),('の瞬間にぴったり','を楽しむ場面にぴったり'),('淡い色は自然光の下で','淡い色は柔らかな自然光の下で'),('快適な家族は、完璧な服装でも不快な家族より','笑顔で快適に過ごす家族は、完璧な服装でも居心地の悪い家族より')],
'ko':[
('드레스와 청바지를 섞지','무도회용 드레스와 청바지를 섞지'),('크림, 베이지, 탄, 흰색','크림, 베이지, 황갈색, 흰색'),('최고의 맞춤 기회','시밀러룩을 입기에 가장 좋은 기회'),('준비된 맞춤 가족 의상','바로 고를 수 있는 가족 시밀러룩'),('맞춤 가족 의상이','가족 시밀러룩이'),('엄마와 나 맞춤 의상','엄마와 아이의 시밀러룩'),('가족 맞춤 세트','가족 시밀러룩 세트'),('가족 전체 맞춤복','온 가족 시밀러룩')],
'nl':[
("vakantiefoto's maakt","foto's voor feestdagenkaarten maakt"),("op vakantiefoto's","op feestdagenfoto's"),('Crème, beige, tan en wit','Crème, beige, lichtbruin en wit'),('mommy and me-jurken','jurken voor moeder en dochter'),('om te laagjes te maken','om laagjes te maken'),('Mama en ik matching outfits','Bijpassende outfits voor moeder en kind'),('Familie matching sets','Bijpassende gezinssets'),('Volledige familie-matching','Bijpassende kleding voor het hele gezin')],
'no':[
('Krem, beige, tan og hvitt','Krem, beige, lysebrunt og hvitt'),('Linne- eller bomullsantrekk','Lin- eller bomullsantrekk'),('casual skjorter','uformelle skjorter'),('Accessorize','Bruk tilbehør'),('rynker vises på bilder','skrukker vises på bilder')],
'pt-BR':[
('na luz do pôr do sol','na luz da hora dourada'),('camisas sociais coordenadas','camisas de botão coordenadas'),('Maiôs','Trajes de banho'),('rugas aparecem nas fotos','amassados aparecem nas fotos')],
'ro':[
('cel mai popular schemă','cea mai populară schemă'),('mamă și copil','în rochii asortate pentru mamă și fiică')]
}
