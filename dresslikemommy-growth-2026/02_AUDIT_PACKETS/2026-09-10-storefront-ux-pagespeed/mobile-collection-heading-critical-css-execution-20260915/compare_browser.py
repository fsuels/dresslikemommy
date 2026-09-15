from pathlib import Path
import json,sys,re
P=Path(__file__).parent; B=P/'browser'
OLD=P.parent/'mobile-collection-heading-execution-20260915'/'browser'
before=json.loads((OLD/'after-cases.json').read_text())+json.loads((OLD/'after-shared-cases.json').read_text())
after=json.loads((B/'after-cases.json').read_text())+json.loads((B/'after-shared-cases.json').read_text())
old={x['label'].replace('after-',''):x for x in before}; checks=[]
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),**({'detail':detail} if detail is not None else {})})
for x in after:
 key=x['label'].replace('critical-','');o=old.get(key);r=x['h1']['rect'];h=x['hero'];mobile=x['width']<=767
 check(key+':before_pair_exists',o is not None)
 if o is None:continue
 check(key+':exact_theme',x['theme']['id']==137888792673 and x['theme']['role']=='unpublished')
 check(key+':exact_route_locale',x['url']==o['url']==x['requestedUrl'] and x['lang']==o['lang'])
 check(key+':one_visible_native_h1',x['h1Count']==1 and len(x['axLevel1'])==1 and r['width']>0 and r['height']>0 and h['rect']['display']!='none' and x['h1']['text']==o['h1']['text'])
 check(key+':h1_inside_viewport',r['x']>=0 and r['x']+r['width']<=x['width']+0.1)
 check(key+':no_page_horizontal_overflow',x['scrollWidth']<=x['width'])
 check(key+':same_card_count_order',[(c['href'],c['title']) for c in x['cards']]==[(c['href'],c['title']) for c in o['cards']])
 check(key+':same_country_currency_cart',x['country']==o['country'] and x['cart']==o['cart'])
 check(key+':no_console_errors',not x['consoleErrors'])
 check(key+':filter_available',x['filters'] is not None and x['filters']['height']>0)
 if mobile:
  check(key+':support_blocks_stay_hidden',all(c['rect']['display']=='none' for c in h['children'] if 'collection-hero__title' not in c['className']) and (h['image'] is None or h['image']['display']=='none'))
  check(key+':no_image_padding_or_half_column',h['rect']['padding']=='0px' and h['textWrapper']['padding']=='0px' and h['textWrapper']['flexBasis']=='100%')
  links=[a for a in x['categoryLinks'] if a['rect']['height']>0 and a['rect']['width']>0]
  check(key+':category_controls_below_heading',bool(links) and min(a['rect']['y'] for a in links)>=r['bottom']-1)
 else:
  geometry=['x','y','width','height','bottom']
  check(key+':desktop_heading_geometry_unchanged',all(abs(r[k]-o['h1']['rect'][k])<0.1 for k in geometry),{'before':o['h1']['rect'],'after':r})
  check(key+':desktop_hero_content_preserved',[(c['tag'],c['text'],c['rect']['display']) for c in h['children']]==[(c['tag'],c['text'],c['rect']['display']) for c in o['hero']['children']])
  check(key+':desktop_first_card_geometry_unchanged',all(abs(x['cards'][0]['rect'][k]-o['cards'][0]['rect'][k])<0.1 for k in geometry))
result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAILED','pairs':len(after),'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'limits':['Rendered snapshots only; cold-load traces, interaction and independent review are separate.','Image-enabled and scroll-reveal branches require actual enabled surfaces; none invented.']}
(P/'BROWSER_COMPARISON.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}));print(json.dumps([c for c in checks if not c['pass']],ensure_ascii=False))
sys.exit(bool(result['failed']))
