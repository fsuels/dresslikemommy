from pathlib import Path
import json,re
P=Path(__file__).parent
# Reviewed public interface labels. Conditional physical-store and unsupported
# delivery-journey assertions stay outside this translation repair.
text='''Enter store using password:|כניסה לחנות באמצעות סיסמה:
Enter using password|כניסה באמצעות סיסמה
Password|סיסמה
Your password|הסיסמה שלך
Wrong password!|הסיסמה שגויה!
Enter|כניסה
Are you the store owner? <a href="/admin" class="link underlined-link">Log in here</a>|האם החנות בבעלותך? <a href="/admin" class="link underlined-link">כניסה כאן</a>
This shop will be powered by {{ shopify }}|החנות הזו תפעל באמצעות {{ shopify }}
Share on Facebook|שיתוף ב־Facebook
Share on X|שיתוף ב־X
Pin on Pinterest|שמירה ב־Pinterest
Continue shopping|המשך קנייה
Pagination|ניווט בין עמודים
Page {{ number }}|עמוד {{ number }}
Next page|העמוד הבא
Previous page|העמוד הקודם
Search for products|חיפוש מוצרים
Clear search term|ניקוי מונח החיפוש
View cart ({{ count }})|הצגת הסל ({{ count }})
View cart|הצגת הסל
Item added to your cart|הפריט נוסף לסל שלך
Close share|סגירת חלון השיתוף
Copy link|העתקת קישור
Link|קישור
Link copied to clipboard|הקישור הועתק ללוח
of|מתוך
Slide right|החלקה ימינה
Slide left|החלקה שמאלה
Slider|מצגת
Home|דף הבית
Email|אימייל
Thanks for subscribing|תודה על ההרשמה
Subscribe|הרשמה
Skip to content|דילוג לתוכן
Skip to product information|דילוג למידע על המוצר
Close|סגירה
per|לכל
Vendor:|ספק:
Error|שגיאה
Choosing a selection results in a full page refresh.|בחירת אפשרות תגרום לטעינה מחדש של העמוד כולו.
Opens in a new window.|נפתח בחלון חדש.
Opens external website.|פותח אתר חיצוני.
Loading...|בטעינה...
total reviews|סך כל הביקורות
{{ rating_value }} out of {{ rating_max }} stars|{{ rating_value }} מתוך {{ rating_max }} כוכבים
Collapsible content|תוכן שניתן לכווץ
Complementary products|מוצרים משלימים
Blog|בלוג
Read more: {{ title }}|לקריאה נוספת: {{ title }}
Please note, comments need to be approved before they are published.|לתשומת לבך, התגובות דורשות אישור לפני פרסומן.
Leave a comment|כתיבת תגובה
Name|שם
Comment|תגובה
Post comment|פרסום תגובה
Back to blog|חזרה לבלוג
Share this article|שיתוף הכתבה
Your comment was posted successfully! Thank you!|התגובה שלך פורסמה בהצלחה! תודה!
Your comment was posted successfully. We will publish it in a little while, as our blog is moderated.|התגובה שלך נשלחה בהצלחה. נפרסם אותה בקרוב לאחר בדיקה, כיוון שהתגובות בבלוג דורשות אישור.
Example product title|שם מוצר לדוגמה
Your collection's name|שם הקולקציה שלך
Add to cart|הוספה לסל
Choose options|בחירת אפשרויות
Choose options for {{ product_name }}|בחירת אפשרויות עבור {{ product_name }}
Description|תיאור
In stock|במלאי
{{ quantity }} in stock|{{ quantity }} במלאי
Low stock|מלאי מוגבל
Low stock: {{ quantity }} left|מלאי מוגבל: נותרו {{ quantity }}
Out of stock|אזל מהמלאי
Sale|מבצע
Product variants|גרסאות המוצר
Gallery Viewer|מציג הגלריה
Load image {{ index }} in gallery view|טעינת תמונה {{ index }} בתצוגת הגלריה
Load 3D Model {{ index }} in gallery view|טעינת דגם תלת־ממד {{ index }} בתצוגת הגלריה
Play video {{ index }} in gallery view|הפעלת סרטון {{ index }} בתצוגת הגלריה
Image {{ index }} is now available in gallery view|תמונה {{ index }} זמינה כעת בתצוגת הגלריה
Open media {{ index }} in modal|פתיחת מדיה {{ index }} בחלון קופץ
Play 3D Viewer|הפעלת מציג תלת־ממד
Play video|הפעלת סרטון
Quantity|כמות
Quantity for {{ product }}|כמות עבור {{ product }}
Increase quantity for {{ product }}|הגדלת הכמות עבור {{ product }}
Decrease quantity for {{ product }}|הקטנת הכמות עבור {{ product }}
Minimum of {{ quantity }}|מינימום {{ quantity }}
Maximum of {{ quantity }}|מקסימום {{ quantity }}
Increments of {{ quantity }}|בקפיצות של {{ quantity }}
Min {{ quantity }}|מינ׳ {{ quantity }}
Max {{ quantity }}|מקס׳ {{ quantity }}
<span class="quantity-cart">{{ quantity }}</span> in cart|<span class="quantity-cart">{{ quantity }}</span> בסל
View quantity rules|הצגת כללי הכמות
Volume Pricing|תמחור לפי כמות
Volume pricing available|תמחור לפי כמות זמין
at {{ price }}/ea|במחיר {{ price }} ליחידה
From {{ price }}|החל מ־{{ price }}
Regular price|מחיר רגיל
Sale price|מחיר מבצע
Unit price|מחיר ליחידה
Share this product|שיתוף המוצר
Sold out|אזל מהמלאי
Unavailable|לא זמין
Vendor|ספק
{{ option_value }} - Unavailable|{{ option_value }} - לא זמין
Variant sold out or unavailable|הגרסה אזלה מהמלאי או אינה זמינה
{{ title }} opens full screen video in same window.|{{ title }} פותח סרטון במסך מלא באותו חלון.
View full details|הצגת כל הפרטים
View in your space|צפייה במרחב שלך
View in your space, loads item in augmented reality window|צפייה במרחב שלך, טוענת את הפריט בחלון מציאות רבודה
Tax included.|המס כלול.
Select size|בחירת מידה
Select color|בחירת צבע
Please select a size before adding to cart.|יש לבחור מידה לפני ההוספה לסל.
Media gallery|גלריית מדיה
Match all|התאמה לכל התנאים
Apply|החלה
Clear|ניקוי
Remove all|הסרת הכול
From|מ־
Filter and sort|סינון ומיון
Filter:|סינון:
Filter|סינון
{{ type }} ({{ count }} filters selected)|{{ type }} (נבחרו {{ count }} מסננים)
Show more|הצגת עוד
Show less|הצגת פחות
The highest price is {{ price }}|המחיר הגבוה ביותר הוא {{ price }}
Reset|איפוס
Sort|מיון
Sort by:|מיון לפי:
To|עד
Remove filter|הסרת מסנן
Page not found|העמוד לא נמצא
No results found for “{{ terms }}”. Check the spelling or use a different word or phrase.|לא נמצאו תוצאות עבור “{{ terms }}”. יש לבדוק את האיות או להשתמש במילה או בביטוי אחרים.
Page|עמוד
Products|מוצרים
Search results|תוצאות חיפוש
Search for “{{ terms }}”|חיפוש “{{ terms }}”
Suggestions|הצעות
Pages|עמודים
Cart|סל
Contact form|טופס יצירת קשר
Send|שליחה
Thanks for contacting us. We'll get back to you as soon as possible.|תודה שפנית אלינו. נחזור אליך בהקדם האפשרי.
Please adjust the following:|יש לתקן את הפרטים הבאים:
Tees|חולצות טי
Country/region|מדינה/אזור
Language|שפה
Update language|עדכון שפה
Update country/region|עדכון מדינה/אזור
Search|חיפוש
Popular countries/regions|מדינות/אזורים נפוצים
{{ count }} countries/regions found|נמצאו {{ count }} מדינות/אזורים
Account|חשבון
Account details|פרטי החשבון
View addresses|הצגת כתובות
Return to Account details|חזרה לפרטי החשבון
Activate account|הפעלת החשבון
Create your password to activate your account.|יש ליצור סיסמה כדי להפעיל את החשבון.
Confirm password|אישור סיסמה
Decline invitation|דחיית ההזמנה
Addresses|כתובות
Default|ברירת מחדל
Add a new address|הוספת כתובת חדשה
Edit address|עריכת כתובת
First name|שם פרטי
Last name|שם משפחה
Company|חברה
Address 1|שורת כתובת 1
Address 2|שורת כתובת 2
City|עיר
Province|מחוז
Postal/ZIP code|מיקוד
Set as default address|הגדרה ככתובת ברירת מחדל
Add address|הוספת כתובת
Update address|עדכון כתובת
Cancel|ביטול
Edit|עריכה
Delete|מחיקה
Are you sure you wish to delete this address?|האם למחוק את הכתובת הזו?
Log in|כניסה
Log out|יציאה
Create account|יצירת חשבון
Forgot your password?|שכחת את הסיסמה?
Continue|המשך
Continue as a guest|המשך כאורח
Login|כניסה
Sign in|כניסה
Submit|שליחה
or|או
Order {{ name }}|הזמנה {{ name }}
Placed on {{ date }}|בוצעה בתאריך {{ date }}
Order Cancelled on {{ date }}|ההזמנה בוטלה בתאריך {{ date }}
Reason: {{ reason }}|סיבה: {{ reason }}
Billing Address|כתובת לחיוב
Payment Status|מצב התשלום
Shipping Address|כתובת למשלוח
Fulfillment Status|מצב הטיפול בהזמנה
Discount|הנחה
Shipping|משלוח
Tax|מס
Product|מוצר
Price|מחיר
Total|סך הכול
Refunded|הוחזר
Fulfilled {{ date }}|הטיפול הושלם בתאריך {{ date }}
Track shipment|מעקב אחר המשלוח
Tracking link|קישור למעקב
Carrier|חברת שילוח
Tracking number|מספר מעקב
Subtotal|סכום ביניים
Duties|מכסים
Order history|היסטוריית הזמנות
Order|הזמנה
Order number {{ number }}|מספר הזמנה {{ number }}
Date|תאריך
Payment status|מצב התשלום
Fulfillment status|מצב הטיפול בהזמנה
Reset your password|איפוס הסיסמה
We will send you an email to reset your password|נשלח לך אימייל לאיפוס הסיסמה
We've sent you an email with a link to update your password.|שלחנו לך אימייל עם קישור לעדכון הסיסמה.
Create|יצירה
Reset account password|איפוס סיסמת החשבון
Enter a new password|הזנת סיסמה חדשה
Reset password|איפוס הסיסמה
Here's your {{ value }} gift card balance for {{ shop }}!|יתרת כרטיס המתנה שלך עבור {{ shop }} היא {{ value }}!
Your gift card|כרטיס המתנה שלך
Gift card code|קוד כרטיס המתנה
Visit online store|מעבר לחנות המקוונת
Add to Apple Wallet|הוספה ל־Apple Wallet
QR code — scan to redeem gift card|קוד QR — יש לסרוק כדי לממש את כרטיס המתנה
Copy gift card code|העתקת קוד כרטיס המתנה
Expires {{ expires_on }}|בתוקף עד {{ expires_on }}
Code copied successfully|הקוד הועתק בהצלחה
Expired|פג תוקף
I want to send this as a gift|ברצוני לשלוח את הפריט כמתנה
Gift card recipient form expanded|טופס מקבל כרטיס המתנה הורחב
Gift card recipient form collapsed|טופס מקבל כרטיס המתנה כווץ
Recipient email|אימייל של מקבל המתנה
Recipient email (optional)|אימייל של מקבל המתנה (לא חובה)
{{ count }} comment|תגובה {{ count }}
{{ count }} comments|{{ count }} תגובות
{{ count }} selected|נבחרו {{ count }}
{{ product_count }} of {{ count }} product|{{ product_count }} מתוך {{ count }} מוצר
{{ product_count }} of {{ count }} products|{{ product_count }} מתוך {{ count }} מוצרים
{{ count }} product|מוצר {{ count }}
{{ count }} products|{{ count }} מוצרים
{{ count }} page|עמוד {{ count }}
{{ count }} pages|{{ count }} עמודים
{{ count }} suggestion|הצעה {{ count }}
{{ count }} suggestions|{{ count }} הצעות
{{ count }} result|תוצאה {{ count }}
{{ count }} results|{{ count }} תוצאות
{{ count }} result found for “{{ terms }}”|נמצאה תוצאה {{ count }} עבור “{{ terms }}”
{{ count }} results found for “{{ terms }}”|נמצאו {{ count }} תוצאות עבור “{{ terms }}”
Phone number|מספר טלפון
Phone|טלפון
You haven't placed any orders yet.|עדיין לא ביצעת הזמנות.'''
translations=dict(l.split('|',1) for l in text.splitlines())
def read(f):s=f.read_text();return s[:s.index('{')],json.loads(s[s.index('{'):])
def flat(o,p=''):
 if isinstance(o,dict):
  for k,v in o.items():yield from flat(v,p+'.'+k if p else k)
 else:yield p,o
def setp(o,k,v):
 parts=k.split('.');d=o
 for p in parts[:-1]:d=d.setdefault(p,{})
 d[parts[-1]]=v
_,base=read(P/'before/locales/en.default.json');f=Path('locales/he.json');header,o=read(f);current=dict(flat(o));changes=[]
for k,en in flat(base):
 if k.startswith(('products.pickup_availability.','products.product.pickup_availability.','products.delivery_journey.')) or k=='gift_cards.issued.how_to_use_gift_card':continue
 if (k not in current or current[k]==en) and en in translations:
  v=translations[en];assert sorted(re.findall(r'{{.*?}}',en))==sorted(re.findall(r'{{.*?}}',v)),k;assert re.findall(r'<[^>]+>',en)==re.findall(r'<[^>]+>',v),k
  setp(o,k,v);changes.append({'key':k,'before':current.get(k),'after':v})
f.write_text(header+json.dumps(o,ensure_ascii=False,indent=2)+'\n')
(P/'hebrew_interface_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print('Hebrew interface repair',len(changes),'keys')
