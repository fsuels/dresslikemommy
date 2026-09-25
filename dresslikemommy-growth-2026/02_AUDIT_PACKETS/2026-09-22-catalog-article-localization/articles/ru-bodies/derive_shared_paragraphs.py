"""Exact source-format reuse of manually authored Russian boilerplate; offline."""
from pathlib import Path
import re,json
P=Path(__file__).resolve().parent
nodes=json.loads((P/'source_segments.json').read_text());manual={}
for f in P.glob('manual_nodes_*.json'):
    if f.name=='manual_nodes_07_paragraphs.json':continue
    manual.update(json.loads(f.read_text()))
group_pre={
 'family matching outfits':'семейных нарядах в едином стиле',
 'mommy and me matching outfits':'парных нарядах для мамы и ребёнка',
 'daddy and me matching outfits':'парных нарядах для папы и ребёнка',
 'mommy and me outfits':'нарядах для мамы и ребёнка',
 'daddy and me outfits':'нарядах для папы и ребёнка'}
group_acc={
 'family matching outfits':'семейные наряды в едином стиле',
 'mommy and me outfits':'наряды для мамы и ребёнка',
 'daddy and me outfits':'наряды для папы и ребёнка'}
group_gen={'family matching outfits':'семейных нарядов в едином стиле','mommy and me matching outfits':'парных нарядов для мамы и ребёнка','daddy and me matching outfits':'парных нарядов для папы и ребёнка'}
occasion={
 "Valentine's Day":'в День святого Валентина',"Mother's Day":'в День матери',"Father's Day":'в День отца',
 'Thanksgiving':'в День благодарения','winter season':'зимой','beach vacation':'во время пляжного отпуска','fall':'осенью','Halloween':'на Хэллоуин',
 'matching family outfits':'когда вся семья одевается в едином стиле','Christmas':'на Рождество','spring':'весной','Easter':'на Пасху','summer':'летом',
 'matching swimwear':'при выборе парной купальной одежды','back-to-school season':'к началу учебного года','family photo sessions':'для семейных фотосессий'}
when={k: v[0].upper()+v[1:] for k,v in occasion.items()}
when['matching family outfits']='Когда речь идёт о семейных нарядах в едином стиле,'
when['matching swimwear']='Когда речь идёт о парной купальной одежде,'
finding={
 'fall family matching outfits':'осенних семейных нарядов в едином стиле',
 'Thanksgiving family matching outfits':'семейных нарядов в едином стиле для Дня благодарения',
 'spring daddy and me outfits':'весенних нарядов для папы и ребёнка',
 'summer mommy and me outfits':'летних нарядов для мамы и ребёнка',
 'Christmas family matching outfits':'рождественских семейных нарядов в едином стиле',
 'matching family outfits family matching outfits':'семейных нарядов в едином стиле'}
out={};provenance=[]
for n in nodes:
    if n['id'] in manual:continue
    s=n['source'];v=None;rule=None
    m=re.fullmatch(r"There's something magical about (.*?), especially during (.*?)\. At Dress Like Mommy, we've spent years helping families create those unforgettable coordinated moments\. Here's our expert guide to the best looks for (\d+)\.",s)
    if m and m[1] in group_pre and m[2] in occasion:
        v=f"В {group_pre[m[1]]} есть что-то волшебное, особенно {occasion[m[2]]}. В Dress Like Mommy мы уже много лет помогаем семьям создавать незабываемые моменты в едином стиле. Вот наш экспертный гид по лучшим образам {m[3]} года.";rule='exact_magic_intro'
    m=re.fullmatch(r"When it comes to (.*?), nothing beats the joy of stepping out in perfectly coordinated (.*?)\. We've tested dozens of matching sets and selected only the best for comfort, style, and that wow factor everyone loves\.",s)
    if m and m[1] in when and m[2] in group_pre:
        v=f"{when[m[1]]} ничто не сравнится с радостью выхода в идеально сочетающихся {group_pre[m[2]]}. Мы протестировали десятки парных комплектов и выбрали лучшие по удобству, стилю и тому самому впечатляющему эффекту, который всем нравится.";rule='exact_testing_intro'
    m=re.fullmatch(r"Finding the perfect (.*?) doesn't have to be stressful\. Whether you're planning for a special occasion or just want to add some coordinated style to your everyday life, we've curated the best matching looks that combine comfort, quality, and picture-perfect style\.",s)
    if m and m[1] in finding:
        v=f"Поиск идеальных {finding[m[1]]} не должен вызывать стресс. Готовитесь ли вы к особому случаю или просто хотите добавить согласованный стиль в повседневную жизнь, мы подобрали лучшие парные образы, сочетающие удобство, качество и красоту в кадре.";rule='exact_finding_intro'
    m=re.fullmatch(r"Coordinating (.*?) for (.*?) is one of our favorite things to help families with\. From casual everyday looks to special occasion ensembles, this guide covers everything you need to create those picture-perfect matching moments\.",s)
    if m and m[1] in group_acc and m[2] in occasion:
        v=f"Помогать семьям подбирать {group_acc[m[1]]} {occasion[m[2]]} — одно из наших любимых занятий. От повседневных образов до ансамблей для особых случаев — этот гид расскажет всё необходимое для красивых парных образов в кадре.";rule='exact_coordination_intro'
    m=re.fullmatch(r"Don't miss out on these (.*?) matching looks — our most popular styles sell out fast! Shop now and create memories your family will cherish forever\.",s)
    if m and m[1] in occasion:
        v=f"Не упустите эти парные образы {occasion[m[1]]} — самые популярные модели быстро раскупают! Покупайте сейчас и создавайте воспоминания, которые ваша семья будет хранить всегда.";rule='exact_urgency_cta'
    m=re.fullmatch(r"Browse our complete collection of (.*?) and find your family's perfect look\. With free shipping on all orders and our happiness guarantee, there's never been a better time to start twinning!",s)
    if m and m[1] in group_gen:
        v=f"Посмотрите полную коллекцию {group_gen[m[1]]} и найдите идеальный образ для вашей семьи. С бесплатной доставкой всех заказов и нашей гарантией удовлетворённости ещё не было лучшего времени, чтобы начать одеваться одинаково!";rule='exact_shipping_cta_source_review_hold'
    if v:out[n['id']]=v;provenance.append({'id':n['id'],'rule':rule,'sourceValue':s})
(P/'manual_nodes_07_paragraphs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'shared_paragraph_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('exact shared paragraphs',len(out))
