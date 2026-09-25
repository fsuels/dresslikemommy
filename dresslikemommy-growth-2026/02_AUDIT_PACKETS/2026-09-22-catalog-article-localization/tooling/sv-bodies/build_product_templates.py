"""Expand only manually translated, exact source templates and product labels."""
import json,pathlib,re
b=pathlib.Path(__file__).resolve().parent
names=json.loads((b/'template_names_source.json').read_text());values=json.loads((b/'product_name_translations.json').read_text())
assert len(names)==len(values)
names=dict(zip(names,values));a=json.loads((b/'source_segments.json').read_text());result={}
patterns=[
(r'This (.+) is one of our bestsellers for a reason\. The fabric is soft, the fit is flattering for all body types, and it washes beautifully even after dozens of cycles\.',lambda n:'Produkten '+n+' är en av våra bästsäljare av goda skäl. Tyget är mjukt, passformen är smickrande för alla kroppstyper och plagget håller sig fint i tvätten även efter dussintals tvättar.'),
(r'The (.+) combines timeless style with everyday practicality\. Parents love the quality construction, and kids love how comfortable it feels\.',lambda n:'Produkten '+n+' förenar tidlös stil med praktisk användning i vardagen. Föräldrar älskar den välgjorda konstruktionen och barnen älskar hur bekväm den känns.'),
(r"We can't stop recommending the (.+)\. It's the kind of piece that gets compliments every single time you wear it out\.",lambda n:'Vi kan inte sluta rekommendera '+n+'. Det är den sortens plagg som får komplimanger varje gång du bär det ute.'),
(r'Shop the (.+) →',lambda n:'Handla '+n+' →')]
for r in a[735:]:
    if r['source'] in names:result[r['id']]=names[r['source']]
    for pattern,fn in patterns:
        m=re.fullmatch(pattern,r['source'])
        if m:result[r['id']]=fn(names[m[1]])
(b/'manual_0736_onward_product_templates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Manual product/template segments:',len(result))
