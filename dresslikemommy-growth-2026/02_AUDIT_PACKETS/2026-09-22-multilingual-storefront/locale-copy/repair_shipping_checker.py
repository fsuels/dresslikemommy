from pathlib import Path
import json,re
P=Path(__file__).parent
keys=['checker_trigger','checker_trigger_meta','checker_trigger_meta_country','checker_footer_heading','checker_footer_text','checker_title','checker_summary','checker_current_country','checker_search_label','checker_search_placeholder','checker_result_label','checker_selected_badge','checker_available_badge','checker_no_results','checker_note_html','checker_close','checker_result_single_label']
rows={
'ar':'''هل نشحن إلى بلدك؟
الشحن متاح إلى {{ count }} بلدًا
تم اختيار {{ country }} / {{ count }} بلدًا
تحقق من الشحن قبل الطلب
ابحث في قائمة البلدان المتاحة حاليًا عند الدفع وتحقق من وجهتك خلال ثوانٍ.
هل نشحن إلى بلدك؟
نعم، إذا كان بلدك ظاهرًا أدناه. تتوفر هذه البلدان والمناطق وعددها {{ count }} حاليًا عند الدفع.
البلد المحدد حاليًا هو {{ country }}.
ابحث عن بلد أو منطقة
اكتب اسم بلد أو رمزه أو عملته
بلدان معروضة
محدد
نشحن إلى هنا
لم يتم العثور على بلد مطابق في قائمة الدفع الحالية. جرّب تهجئة أخرى أو راسلنا قبل الطلب.
الشحن القياسي مشمول في أسعار المنتجات حيث تتوفر طريقة شحن قياسية. يؤكد إتمام الطلب الطريقة المحددة وموعد التسليم التقديري وأي ترقية للشحن السريع قبل الدفع. <a href="{{ link }}">تفاصيل الشحن</a> · <a href="mailto:{{ email }}">{{ email }}</a>
إغلاق التحقق من البلدان
بلد معروض''',
'fi':'''Toimitammeko maahasi?
Toimitus käytössä {{ count }} maahan
{{ country }} valittu / {{ count }} maata
Tarkista toimitus ennen tilaamista
Hae kassalla tällä hetkellä käytettävissä olevasta maaluettelosta ja tarkista toimituskohteesi hetkessä.
Toimitammeko maahasi?
Kyllä, jos maasi löytyy alta. Nämä {{ count }} maata ja aluetta ovat tällä hetkellä valittavissa kassalla.
Tällä hetkellä valittu maa on {{ country }}.
Hae maata tai aluetta
Kirjoita maan nimi, maatunnus tai valuutta
maata näkyvissä
Valittu
Toimitus saatavilla
Nykyisestä kassalla käytettävästä maaluettelosta ei löytynyt vastaavaa maata. Kokeile toista kirjoitusasua tai lähetä meille sähköpostia ennen tilaamista.
Vakiotoimitus sisältyy tuotteiden hintoihin siellä, missä vakiotoimitustapa on saatavilla. Tarkka toimitustapa, toimitusarvio ja mahdollinen pikatoimitus vahvistetaan kassalla ennen maksua. <a href="{{ link }}">Toimitustiedot</a> · <a href="mailto:{{ email }}">{{ email }}</a>
Sulje maatarkistus
maa näkyvissä''',
'he':'''האם אנחנו שולחים למדינה שלך?
משלוח זמין ל־{{ count }} מדינות
נבחרה {{ country }} / {{ count }} מדינות
בדקו את אפשרויות המשלוח לפני ההזמנה
חפשו ברשימת המדינות הזמינות כעת בקופה ואמתו את היעד שלכם בתוך שניות.
האם אנחנו שולחים למדינה שלך?
כן, אם המדינה שלך מופיעה למטה. {{ count }} המדינות והאזורים האלה זמינים כעת בקופה.
המדינה שנבחרה כרגע היא {{ country }}.
חיפוש מדינה או אזור
הקלידו שם מדינה, קוד מדינה או מטבע
מדינות מוצגות
נבחרה
משלוח ליעד זה
לא נמצאה מדינה תואמת ברשימת הקופה הנוכחית. נסו איות אחר או שלחו לנו אימייל לפני ההזמנה.
משלוח רגיל כלול במחירי המוצרים כאשר שיטת משלוח רגילה זמינה. בקופה יאושרו השיטה המדויקת, מועד המסירה המשוער וכל שדרוג למשלוח מהיר לפני התשלום. <a href="{{ link }}">פרטי משלוח</a> · <a href="mailto:{{ email }}">{{ email }}</a>
סגירת בדיקת המדינות
מדינה מוצגת''',
'hi':'''क्या हम आपके देश में शिपिंग करते हैं?
{{ count }} देशों में शिपिंग उपलब्ध
{{ country }} चुना गया / {{ count }} देश
ऑर्डर करने से पहले शिपिंग जाँचें
चेकआउट पर उपलब्ध देशों की मौजूदा सूची में खोजें और कुछ ही सेकंड में अपने गंतव्य की पुष्टि करें।
क्या हम आपके देश में शिपिंग करते हैं?
हाँ, यदि आपका देश नीचे दिखता है। ये {{ count }} देश और क्षेत्र अभी चेकआउट पर उपलब्ध हैं।
आपका वर्तमान चुना हुआ देश {{ country }} है।
देश या क्षेत्र खोजें
देश का नाम, कोड या मुद्रा लिखें
देश दिखाए गए
चुना गया
यहाँ शिपिंग उपलब्ध है
मौजूदा चेकआउट सूची में कोई मेल खाता देश नहीं मिला। दूसरी वर्तनी आज़माएँ या ऑर्डर करने से पहले हमें ईमेल करें।
जहाँ मानक शिपिंग उपलब्ध है, वहाँ उसकी लागत उत्पाद की कीमत में शामिल है। भुगतान से पहले चेकआउट पर सटीक तरीका, अनुमानित डिलीवरी और किसी भी एक्सप्रेस अपग्रेड की पुष्टि होती है। <a href="{{ link }}">शिपिंग विवरण</a> · <a href="mailto:{{ email }}">{{ email }}</a>
देश जाँच बंद करें
देश दिखाया गया''',
'ja':'''お住まいの国へ配送できますか？
{{ count }}か国への配送が有効
選択中：{{ country }} / {{ count }}か国
ご注文前に配送先をご確認ください
チェックアウトで現在選択できる国の一覧を検索し、配送先をすぐに確認できます。
お住まいの国へ配送できますか？
下の一覧に国があれば配送できます。現在、チェックアウトではこれら{{ count }}の国と地域が有効です。
現在選択されている国は{{ country }}です。
国または地域を検索
国名、国コード、通貨を入力
か国を表示
選択中
配送可能
現在のチェックアウト一覧に一致する国が見つかりません。別の表記を試すか、ご注文前にメールでお問い合わせください。
通常配送が利用できる場合、その配送料は商品価格に含まれます。お支払い前にチェックアウトで具体的な配送方法、お届け予定、速達への変更オプションをご確認いただけます。 <a href="{{ link }}">配送の詳細</a> · <a href="mailto:{{ email }}">{{ email }}</a>
配送先の確認を閉じる
か国を表示''',
'ko':'''거주 국가로 배송되나요?
{{ count }}개 국가 배송 가능
{{ country }} 선택됨 / {{ count }}개 국가
주문 전에 배송 가능 여부를 확인하세요
현재 결제 시 선택 가능한 국가 목록에서 목적지를 빠르게 확인하세요.
거주 국가로 배송되나요?
아래에 국가가 표시되면 배송 가능합니다. 현재 이 {{ count }}개 국가 및 지역을 결제 시 선택할 수 있습니다.
현재 선택한 국가는 {{ country }}입니다.
국가 또는 지역 검색
국가명, 국가 코드 또는 통화 입력
개 국가 표시됨
선택됨
배송 가능
현재 결제 국가 목록에서 일치하는 국가를 찾지 못했습니다. 다른 표기를 시도하거나 주문 전에 이메일로 문의해 주세요.
일반 배송이 가능한 경우 배송비는 제품 가격에 포함됩니다. 정확한 배송 방법, 예상 배송일, 빠른 배송 옵션은 결제 전에 확인할 수 있습니다. <a href="{{ link }}">배송 안내</a> · <a href="mailto:{{ email }}">{{ email }}</a>
국가 확인 닫기
개 국가 표시됨''',
'no':'''Sender vi til landet ditt?
Frakt aktivert til {{ count }} land
{{ country }} valgt / {{ count }} land
Sjekk frakten før du bestiller
Søk i den gjeldende landlisten i kassen og bekreft reisemålet ditt på få sekunder.
Sender vi til landet ditt?
Ja, hvis landet ditt står nedenfor. Disse {{ count }} landene og områdene er tilgjengelige i kassen nå.
Landet du har valgt nå, er {{ country }}.
Søk etter land eller område
Skriv et landsnavn, en landskode eller en valuta
land vises
Valgt
Vi sender hit
Fant ikke et tilsvarende land i den gjeldende kasselisten. Prøv en annen skrivemåte eller send oss en e-post før du bestiller.
Standardfrakt er inkludert i produktprisene der en standard fraktmetode er tilgjengelig. Kassen bekrefter nøyaktig metode, leveringsestimat og eventuell ekspressoppgradering før betaling. <a href="{{ link }}">Fraktdetaljer</a> · <a href="mailto:{{ email }}">{{ email }}</a>
Lukk landkontrollen
land vises''',
'ru':'''Доставляем ли мы в вашу страну?
Доставка доступна в {{ count }} стран
Выбрана страна: {{ country }} / {{ count }} стран
Проверьте доставку перед заказом
Найдите свою страну в актуальном списке оформления заказа и за несколько секунд проверьте доступность доставки.
Доставляем ли мы в вашу страну?
Да, если ваша страна указана ниже. Эти {{ count }} стран и регионов сейчас доступны при оформлении заказа.
Сейчас выбрана страна: {{ country }}.
Поиск страны или региона
Введите название страны, код или валюту
стран показано
Выбрано
Доставка доступна
Совпадений в текущем списке стран при оформлении заказа не найдено. Попробуйте другое написание или напишите нам перед заказом.
Стандартная доставка включена в стоимость товаров там, где доступен стандартный способ доставки. Точный способ, предполагаемый срок и возможный переход на экспресс-доставку подтверждаются при оформлении заказа до оплаты. <a href="{{ link }}">Информация о доставке</a> · <a href="mailto:{{ email }}">{{ email }}</a>
Закрыть проверку стран
страна показана'''
}
def read(f):s=f.read_text();return s[:s.index('{')],json.loads(s[s.index('{'):])
_,en=read(P/'before/locales/en.default.json');source=en['products']['shipping_country'];changes=[]
for l,t in rows.items():
 vals=t.splitlines();assert len(vals)==len(keys),(l,len(vals));f=Path('locales/'+l+'.json');header,o=read(f);d=o['products']['shipping_country']
 for k,v in zip(keys,vals):
  if d.get(k)!=source[k]:continue
  assert sorted(re.findall(r'{{.*?}}',source[k]))==sorted(re.findall(r'{{.*?}}',v)),(l,k)
  assert re.findall(r'<[^>]+>',source[k])==re.findall(r'<[^>]+>',v),(l,k)
  changes.append({'locale':l,'key':'products.shipping_country.'+k,'before':d.get(k),'after':v});d[k]=v
 f.write_text(header+json.dumps(o,ensure_ascii=False,indent=2)+'\n')
(P/'shipping_checker_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('Shipping checker repaired',len(changes),'values with exact markup/placeholders')
