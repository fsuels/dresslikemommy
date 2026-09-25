"""Author-approved literal template renderers; no network or fuzzy translation."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
nodes=json.loads((P/'source_segments.json').read_text())
manual={}
for f in sorted(P.glob('manual_nodes_*.json')):
    if f.name=='manual_nodes_06_templates.json':continue
    manual.update(json.loads(f.read_text()))
by_source={n['source']:manual[n['id']] for n in nodes if n['id'] in manual}
templates=[
 (r'This (.*?) is one of our bestsellers for a reason\. The fabric is soft, the fit is flattering for all body types, and it washes beautifully even after dozens of cycles\.',
  'Модель «{}» не зря входит в число наших бестселлеров. Ткань мягкая, фасон хорошо смотрится на любой фигуре, а вещь прекрасно переносит даже десятки стирок.'),
 (r'The (.*?) combines timeless style with everyday practicality\. Parents love the quality construction, and kids love how comfortable it feels\.',
  'Модель «{}» сочетает вневременной стиль и повседневную практичность. Родителям нравится качество пошива, а детям — удобство.'),
 (r"We can't stop recommending the (.*?)\. It's the kind of piece that gets compliments every single time you wear it out\.",
  'Мы не устаём рекомендовать модель «{}». Это та вещь, в которой вы получаете комплименты каждый раз, когда выходите из дома.')]
names=set()
for n in nodes:
    for pattern,_ in templates:
        m=re.fullmatch(pattern,n['source'])
        if m:names.add(m[1])
result={};provenance=[]
for n in nodes:
    if n['id'] in manual:continue
    for pattern,target in templates:
        m=re.fullmatch(pattern,n['source'])
        if m and m[1] in by_source:
            result[n['id']]=target.format(by_source[m[1]])
            provenance.append({'id':n['id'],'method':'exact_literal_template_plus_manually_translated_complete_source_product_name','sourceProductName':m[1]})
            break
    if n['id'] in result:continue
    m=re.fullmatch(r'Shop the (.*?) →',n['source'])
    if m:
        matches=[name for name in names if name.startswith(m[1]) and name in by_source]
        targets={by_source[name] for name in matches}
        if len(targets)==1:
            result[n['id']]='Посмотрите модель «'+next(iter(targets))+'» →'
            provenance.append({'id':n['id'],'method':'source_CTA_exact_prefix_of_one_known_full_source_product_title','sourceProductNames':matches})
(P/'manual_nodes_06_templates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'exact_template_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
print('derived exact template nodes',len(result))
