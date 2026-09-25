"""Offline, exact-match German prose template assembly; no provider calls."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
nodes=json.loads((P/'source_segments.json').read_text());manual={}
for f in sorted(P.glob('manual_*.tsv')):
 d=dict(x.split('\t',1) for x in f.read_text().splitlines());manual.update(d)
 (P/('manual_nodes_'+f.stem.split('_')[-1]+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
by_source={n['source']:manual[n['id']] for n in nodes if n['id'] in manual}
templates=[
(r'This (.*?) is one of our bestsellers for a reason\. The fabric is soft, the fit is flattering for all body types, and it washes beautifully even after dozens of cycles\.', 'Das Modell „{}“ zählt nicht ohne Grund zu unseren Bestsellern. Der Stoff ist weich, der Schnitt schmeichelt jedem Figurtyp und es übersteht selbst Dutzende Waschgänge hervorragend.'),
(r'The (.*?) combines timeless style with everyday practicality\. Parents love the quality construction, and kids love how comfortable it feels\.', 'Das Modell „{}“ verbindet zeitlosen Stil mit Alltagstauglichkeit. Eltern schätzen die hochwertige Verarbeitung, und Kinder lieben das bequeme Tragegefühl.'),
(r"We can't stop recommending the (.*?)\. It's the kind of piece that gets compliments every single time you wear it out\.", 'Wir können das Modell „{}“ gar nicht oft genug empfehlen. Es ist eines dieser Stücke, für die du jedes Mal Komplimente bekommst, wenn du es außer Haus trägst.')]
groups={'family matching outfits':'passende Familienoutfits','mommy and me matching outfits':'passende Outfits für Mama und Kind','daddy and me matching outfits':'passende Outfits für Papa und Kind','mommy and me outfits':'Outfits für Mama und Kind','daddy and me outfits':'Outfits für Papa und Kind'}
occasion={"Valentine's Day":'zum Valentinstag',"Mother's Day":'zum Muttertag',"Father's Day":'zum Vatertag','Thanksgiving':'zu Thanksgiving','winter season':'im Winter','beach vacation':'im Strandurlaub','fall':'im Herbst','Halloween':'zu Halloween','matching family outfits':'beim Familien-Partnerlook','Christmas':'zu Weihnachten','spring':'im Frühling','Easter':'zu Ostern','summer':'im Sommer','matching swimwear':'bei passender Badebekleidung','back-to-school season':'zum Schulstart','family photo sessions':'bei Familienfotoshootings'}
finding={'fall family matching outfits':'passenden Familienoutfits für den Herbst','Thanksgiving family matching outfits':'passenden Familienoutfits für Thanksgiving','spring daddy and me outfits':'Frühlingsoutfits für Papa und Kind','summer mommy and me outfits':'Sommeroutfits für Mama und Kind','Christmas family matching outfits':'passenden Familienoutfits für Weihnachten','matching family outfits family matching outfits':'passenden Familienoutfits','matching family outfits mommy and me outfits':'passenden Familienoutfits für Mama und Kind'}
names=set()
for n in nodes:
 for pat,_ in templates:
  m=re.fullmatch(pat,n['source'])
  if m:names.add(m[1])
out={};provenance=[]
for n in nodes:
 if n['id'] in manual:continue
 s=n['source'];v=None;rule=None
 for pat,tar in templates:
  m=re.fullmatch(pat,s)
  if m and m[1] in by_source:v=tar.format(by_source[m[1]].replace('„', '‚').replace('“', '‘'));rule='exact_product_prose_template';break
 if v is None:
  m=re.fullmatch(r'Shop the (.*?) →',s)
  if m:
   matches=[name for name in names if name.startswith(m[1]) and name in by_source]; targets={by_source[name] for name in matches}
   if len(targets)==1:v='Modell „'+next(iter(targets)).replace('„', '‚').replace('“', '‘')+'“ shoppen →';rule='exact_unique_product_CTA'
 m=re.fullmatch(r"There's something magical about (.*?), especially during (.*?)\. At Dress Like Mommy, we've spent years helping families create those unforgettable coordinated moments\. Here's our expert guide to the best looks for (\d+)\.",s)
 if m and m[1] in groups and m[2] in occasion:
  v=f"{groups[m[1]][0].upper()+groups[m[1]][1:]} haben etwas Magisches, besonders {occasion[m[2]]}. Bei Dress Like Mommy helfen wir Familien seit Jahren, solche unvergesslichen Momente im Partnerlook zu schaffen. Hier ist unser Expertenleitfaden zu den besten Looks für {m[3]}.";rule='exact_magic_intro'
 m=re.fullmatch(r"When it comes to (.*?), nothing beats the joy of stepping out in perfectly coordinated (.*?)\. We've tested dozens of matching sets and selected only the best for comfort, style, and that wow factor everyone loves\.",s)
 if m and m[1] in occasion and m[2] in groups:
  v=f"{occasion[m[1]][0].upper()+occasion[m[1]][1:]} geht nichts über die Freude, in perfekt abgestimmter Kleidung auszugehen: {groups[m[2]]}. Wir haben Dutzende passende Sets getestet und nur die besten in Sachen Komfort, Stil und dem Wow-Effekt ausgewählt, den alle lieben.";rule='exact_testing_intro'
 m=re.fullmatch(r"Finding the perfect (.*?) doesn't have to be stressful\. Whether you're planning for a special occasion or just want to add some coordinated style to your everyday life, we've curated the best matching looks that combine comfort, quality, and picture-perfect style\.",s)
 if m and m[1] in finding:
  v=f"Die Suche nach den perfekten {finding[m[1]]} muss nicht stressig sein. Ob du einen besonderen Anlass planst oder deinen Alltag um einen abgestimmten Stil ergänzen möchtest: Wir haben die besten Partnerlooks ausgewählt, die Komfort, Qualität und fototauglichen Stil verbinden.";rule='exact_finding_intro'
 m=re.fullmatch(r"Coordinating (.*?) for (.*?) is one of our favorite things to help families with\. From casual everyday looks to special occasion ensembles, this guide covers everything you need to create those picture-perfect matching moments\.",s)
 if m and m[1] in groups and m[2] in occasion:
  v=f"Wir helfen Familien besonders gern dabei, {groups[m[1]]} {occasion[m[2]]} zusammenzustellen. Von lässigen Alltagslooks bis zu Ensembles für besondere Anlässe: Dieser Leitfaden bietet alles, was ihr für fototaugliche gemeinsame Momente im Partnerlook braucht.";rule='exact_coordination_intro'
 m=re.fullmatch(r"Don't miss out on these (.*?) matching looks — our most popular styles sell out fast! Shop now and create memories your family will cherish forever\.",s)
 if m and m[1] in occasion:
  v=f"Verpasst diese Partnerlooks {occasion[m[1]]} nicht – unsere beliebtesten Modelle sind schnell ausverkauft! Shoppt jetzt und schafft Erinnerungen, die eure Familie für immer schätzen wird.";rule='exact_urgency_cta'
 m=re.fullmatch(r"Browse our complete collection of (.*?) and find your family's perfect look\. With free shipping on all orders and our happiness guarantee, there's never been a better time to start twinning!",s)
 if m and m[1] in groups:
  v=f"Entdecke unsere komplette Kollektion für {groups[m[1]]} und finde den perfekten Look für deine Familie. Mit kostenlosem Versand für alle Bestellungen und unserer Zufriedenheitsgarantie gab es nie einen besseren Zeitpunkt, mit dem Partnerlook anzufangen!";rule='exact_shipping_CTA'
 if v:out[n['id']]=v;provenance.append({'id':n['id'],'rule':rule,'sourceValue':s})
(P/'manual_nodes_99_templates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'template_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('exact template nodes',len(out))
missing=[n for n in nodes if n['id'] not in manual and n['id'] not in out]
(P/'missing.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2)+'\n')
print('remaining',len(missing))
