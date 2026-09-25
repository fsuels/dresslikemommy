#!/usr/bin/env python3
import collections,json,pathlib,re
from build_metadata import BASE,HERE,save
SOURCES=json.loads((HERE/'meta_title_sources.json').read_text())
D=json.loads((HERE/'seo_template_dictionary.json').read_text())
nodes={n['resourceId']:n for f in HERE.parent.glob('translations_batch_*json') for n in json.loads(f.read_text())['data']['translatableResourcesByIds']['nodes']}
manual={
 (74,'ar'):'أطقم بيكيني متناسقة للعائلة - طبعة زهور',
 (74,'nl'):'Bijpassende bikinisets voor het gezin - Bloemenprint',
 (81,'pl'):'Dopasowane rodzinne koszule zapinane na guziki - Kwiatowy nadruk',
 (85,'ar'):'قمصان متناسقة للعائلة بأزرار - طبعة زهور خضراء',
 (85,'nl'):'Bijpassende overhemden voor het gezin - Groen bloemenpatroon'
}
explicit_conflicts={
 2:'English title calls item bikini, body explicitly one-piece, and SEO Halloween Print unsupported by same-product title/body.',
 16:'Source meta_title combines Bikini Sets with One-Piece; same-product title says two-piece while bullet says one-piece. Source garment construction conflicted.',
 66:'Source SEO Halloween Print contradicts same-product battery-theme title and body; no Halloween design described.',
 70:'Source SEO Christmas Print contradicts same-product Beautiful rainbow/sunshine title and body; no Christmas design described.',
 88:'Source SEO Green Christmas Print contradicts same-product tropical leaf swim-shorts title and body.',
 90:'Source SEO Pink Black Christmas contradicts same-product pink/black color-block swim-shorts title and body.'
}
rows=[];held=[];nochange=[]
for r in BASE:
 if r['key']!='meta_title':continue
 i=SOURCES.index(r['source'])
 if i in [40,92,93,94,95,96]:continue
 src={x['key']:x for x in nodes[r['resourceId']]['translatableContent']}
 body=re.sub('<[^>]*>',' ',src.get('body_html',{}).get('value',''))
 reason=explicit_conflicts.get(i)
 if 'T-Shirts' in r['source'] and re.search(r'button[- ](?:up|front|down|through)|collar',body,re.I):
  reason='English SEO calls garment T-Shirts while same-product title/body describes collared button-front shirts. Existing translated garment type must not be changed to T-shirt.'
 if reason:
  held.append({**r,'status':'ROOT_ENGLISH_SOURCE_DISPOSITION_REQUIRED','reason':reason,'sourceTitle':src.get('title',{}).get('value'),'supportingSourceDigests':{k:src[k]['digest'] for k in ['title','body_html'] if k in src}});continue
 if r['locale'] in ['ru','sv']:
  j=['ru','sv'].index(r['locale']);category,trait=r['source'].removesuffix(' | Dress Like Mommy').split(' - ')
  value=D['categories'][category][j]+' — '+D['traits'][trait][j]+' | Dress Like Mommy'
 elif (i,r['locale']) in manual:value=manual[(i,r['locale'])]+' | Dress Like Mommy'
 else:
  nochange.append({**r,'status':'NO_COPY_CHANGE','reason':'Existing localized SEO title remains accurate against same-product title/body. An outdated marker or different wording alone does not require replacing a good translation.'});continue
 rows.append({**r,'value':value,'marketId':None,'method':'manual_category_attribute_translation_after_same_product_source_conflict_screen'})
save('ordinary_meta_titles',rows,'RU/SV missing ordinary SEO titles and five material translated-label defects. Source genre/pattern conflicts excluded; good existing localized titles retained despite stale markers.')
for name,rr in [('meta_titles_source_holds',held),('meta_titles_no_change',nochange)]:
 (HERE/(name+'.json')).write_text(json.dumps({'rows':rr},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'candidate':len(rows),'held':len(held),'noChange':len(nochange),'heldProducts':len(set(r['resourceId'] for r in held)),'heldReasons':dict(collections.Counter(r['reason'] for r in held))}))
