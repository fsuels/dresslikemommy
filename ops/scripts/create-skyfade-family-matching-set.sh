#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi
: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"
export SHOPIFY_STORE_DOMAIN SHOPIFY_ADMIN_ACCESS_TOKEN
python3 - <<'PYRUN'
import csv, html, json, math, mimetypes, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
ROOT=Path('/Users/fsuels/Projects/dresslikemommy')
API=f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN=os.environ['SHOPIFY_ADMIN_ACCESS_TOKEN']
HANDLE='skyfade-family-matching-set'
TITLE='Skyfade Family Matching Set - Dress & Shirt'
SEO_TITLE='Skyfade Family Matching Set | Dress Like Mommy'
SEO_DESCRIPTION='Airy ombre family matching set in blue or lavender for mom, dad, girls & boys. Dress and shirt sizes 2Y-10Y, Mother S-3XL, Father S-4XL.'
VENDOR_URL='https://detail.1688.com/offer/893219853492.html'
PRODUCT_TYPE='Matching Family Sets'
TAXONOMY_GID='gid://shopify/TaxonomyCategory/aa-1-11'
EXPECTED_TAXONOMY='Apparel & Accessories > Clothing > Outfit Sets'
SHORTCODE='SKYF'
COLORWAYS=[('Blue','BLUE'),('Lavender','LAV')]
CHILD_PRICE='31.99'; ADULT_PRICE='36.99'
def cmp(price):
    v=float(price)*1.15; d=math.floor(v); c=d+0.99
    if c < v: c=d+1.99
    return f'{c:.2f}'
CHILD_COMPARE=cmp(CHILD_PRICE); ADULT_COMPARE=cmp(ADULT_PRICE)
LISTING_MD=ROOT/f'ops/listings/{HANDLE}-listing.md'
CSV_OUT=ROOT/f'ops/listings/{HANDLE}-shopify-import.csv'
VERIFY_JSON_OUT=ROOT/f'ops/listings/verify-{HANDLE}.json'
SIZE_CHART_OUT=ROOT/f'ops/listings/size-chart-{HANDLE}.json'
BODY_HTML_OUT=ROOT/f'ops/listings/body-{HANDLE}.html'
UPLOAD_DIR=ROOT/f'uploads/{HANDLE}'
SCRIPT_PATH=ROOT/'ops/scripts/create-skyfade-family-matching-set.sh'
CSV_HEADER_SOURCE=ROOT/'bird-chirping-mommy-and-me-pajamas-shopify-import.csv'
for p in [LISTING_MD.parent, UPLOAD_DIR]: p.mkdir(parents=True, exist_ok=True)
# Source chart: attached image Screenshot 2026-04-24 at 10.37.44 AM. Weight source is vendor 斤, converted to kg for storage/display.
def kg(jin):
    lo,hi=[float(x) for x in re.split(r'[-–]',jin)]
    return f'{lo/2:g}-{hi/2:g} kg'
chart=[]
def add(aud,role,gar,vendor,picker,age,weight,height,chest,length,skirt=0,shoulder=0,sleeve=0):
    if gar=='Dress':
        hip=chest+4 if aud=='child' else chest+6; waist=chest if aud=='child' else hip-8
    else:
        hip=chest; waist=chest if aud=='child' else chest-12
    tok={'Child 2 Years':'KID2Y','Child 3 Years':'KID3Y','Child 4 Years':'KID4Y','Child 5 Years':'KID5Y','Child 6-7 Years':'KID67Y','Child 8 Years':'KID8Y','Child 9-10 Years':'KID910Y','Mother S':'S','Mother M':'M','Mother L':'L','Mother XL':'XL','Mother 2XL':'2XL','Mother 3XL':'3XL','Father S':'S','Father M':'M','Father L':'L','Father XL':'XL','Father 2XL':'2XL','Father 3XL':'3XL','Father 4XL':'4XL'}[picker]
    chart.append(dict(audience=aud,role=role,garment=gar,vendor_label=vendor,picker_label=picker,sku_suffix=tok,age=age,weight=weight,height=height,chest_cm=chest,hip_cm=hip,waist_cm=waist,length_cm=length,skirt_cm=skirt,sleeve_cm=sleeve,shoulder_cm=shoulder,pant_cm=0))
child_rows=[('90','Child 2 Years','2',kg('20-25'),'80-90 cm'),('100','Child 3 Years','3',kg('25-30'),'90-100 cm'),('110','Child 4 Years','4',kg('30-35'),'100-110 cm'),('120','Child 5 Years','5',kg('35-45'),'110-120 cm'),('130','Child 6-7 Years','6-7',kg('45-55'),'120-130 cm'),('140','Child 8 Years','8',kg('55-65'),'130-140 cm'),('150','Child 9-10 Years','9-10',kg('65-75'),'140-150 cm')]
for vendor,picker,age,weight,height,chest,skirt in [(r[0],r[1],r[2],r[3],r[4],c,s) for r,(s,c) in zip(child_rows,[(57,54),(60,58),(63,62),(66,66),(69,70),(72,74),(75,78)])]: add('child','Girl Dress','Dress',vendor,picker,age,weight,height,chest,skirt,skirt=skirt)
for vendor,picker,weight,height,chest,skirt in [('S','Mother S',kg('75-85'),'150-155 cm',84,100),('M','Mother M',kg('85-100'),'155-160 cm',88,104),('L','Mother L',kg('100-115'),'160-165 cm',92,108),('XL','Mother XL',kg('115-130'),'165-170 cm',96,112),('2XL','Mother 2XL',kg('130-145'),'170-175 cm',100,116),('3XL','Mother 3XL',kg('145-160'),'175-180 cm',104,120)]: add('mother','Mother Dress','Dress',vendor,picker,'-',weight,height,chest,skirt,skirt=skirt)
for vendor,picker,age,weight,height,length,chest,shoulder,sleeve in [(r[0],r[1],r[2],r[3],r[4],l,c,sh,sl) for r,(l,c,sh,sl) in zip(child_rows,[(37,60,25.5,11),(40,64,27,12),(43,68,28.5,13),(46,72,30,14),(49,76,31.5,15),(52,80,33,16),(55,84,34.5,17)])]: add('child','Boy Shirt','Shirt',vendor,picker,age,weight,height,chest,length,shoulder=shoulder,sleeve=sleeve)
for vendor,picker,weight,height,length,chest,shoulder,sleeve in [('S','Father S',kg('80-95'),'155-160 cm',65,94,40,19),('M','Father M',kg('95-110'),'160-165 cm',67,98,42,20),('L','Father L',kg('110-125'),'165-170 cm',69,102,44,21),('XL','Father XL',kg('125-145'),'170-175 cm',71,106,46,22),('2XL','Father 2XL',kg('145-165'),'175-180 cm',73,110,48,23),('3XL','Father 3XL',kg('165-195'),'180-185 cm',75,114,50,24),('4XL','Father 4XL',kg('195-210'),'185-190 cm',77,118,52,25)]: add('father','Father Shirt','Shirt',vendor,picker,'-',weight,height,chest,length,shoulder=shoulder,sleeve=sleeve)
size_map={'Child 2 Years':('gid://shopify/Metaobject/129972863073','2-3 years'),'Child 3 Years':('gid://shopify/Metaobject/129972895841','3-4 years'),'Child 4 Years':('gid://shopify/Metaobject/129972928609','4-5 years'),'Child 5 Years':('gid://shopify/Metaobject/129972961377','5-6 years'),'Child 6-7 Years':('gid://shopify/Metaobject/139840323681','6-7 years'),'Child 8 Years':('gid://shopify/Metaobject/129973026913','8'),'Child 9-10 Years':('gid://shopify/Metaobject/129971552353','10'),'Mother S':('gid://shopify/Metaobject/129975255137','S'),'Mother M':('gid://shopify/Metaobject/129975222369','M'),'Mother L':('gid://shopify/Metaobject/129975189601','L'),'Mother XL':('gid://shopify/Metaobject/129975287905','XL'),'Mother 2XL':('gid://shopify/Metaobject/129975156833','2XL'),'Mother 3XL':('gid://shopify/Metaobject/139840421985','3XL'),'Father S':('gid://shopify/Metaobject/129975255137','S'),'Father M':('gid://shopify/Metaobject/129975222369','M'),'Father L':('gid://shopify/Metaobject/129975189601','L'),'Father XL':('gid://shopify/Metaobject/129975287905','XL'),'Father 2XL':('gid://shopify/Metaobject/129975156833','2XL'),'Father 3XL':('gid://shopify/Metaobject/139840421985','3XL'),'Father 4XL':('gid://shopify/Metaobject/139840716897','4XL')}
role_tok={'Girl Dress':'GRL','Mother Dress':'MOM','Boy Shirt':'BOY','Father Shirt':'DAD'}
def sku(row,ctok): return f"DLM-{SHORTCODE}-{role_tok[row['role']]}-{row['sku_suffix']}-{ctok}"
def n(v):
    try:
        f=float(v); return str(int(f)) if f.is_integer() else f'{f:g}'
    except Exception: return str(v)
def cm_in(v): return '—' if not v else f"{n(v)} cm / {n(float(v)/2.54)} in"
def dual_range(txt,unit,mult,out):
    if txt in ['-','—']: return '—'
    m=re.match(r'([\d.]+)-([\d.]+) '+unit,txt)
    if not m: return html.escape(txt)
    a,b=map(float,m.groups()); return f'{n(a)}-{n(b)} {unit} / {n(a*mult)}-{n(b*mult)} {out}'
def esc(x): return html.escape(str(x))
def table(rows,gar):
    h2='Skirt Length (cm/in)' if gar=='Dress' else 'Sleeve Length (cm/in)'
    body=[]
    for r in rows:
        body.append('<tr>' + ''.join(f'<td>{v}</td>' for v in [esc(r['picker_label']),esc(r['age'] if r['age']!='-' else '—'),esc(dual_range(r['weight'],'kg',2.20462,'lbs')),esc(dual_range(r['height'],'cm',1/2.54,'in')),cm_in(r['chest_cm']),cm_in(r['skirt_cm'] if gar=='Dress' else r['sleeve_cm']),cm_in(0),cm_in(r['hip_cm']),cm_in(r['waist_cm']),cm_in(r['length_cm'])]) + '</tr>')
    return f"<h3>Size Chart — {gar}</h3>\n<table id=\"size-chart-{gar.lower()}\"><thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>{h2}</th><th>Pant/Short or — (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody>"+'\n'.join(body)+"</tbody></table>"
body='\n'.join(['<ul>','<li><strong>Fabric:</strong> Lightweight woven fabric with a floaty, beach-ready drape; exact fiber content was not visible from the blocked vendor page.</li>','<li><strong>Family story:</strong> A four-role family matching look for moms, dads, girls, and boys in coordinated ombre vacation colors.</li>','<li><strong>Colorways:</strong> Choose Blue or Lavender, both fading softly into white for a breezy seaside feel.</li>','<li><strong>Design details:</strong> Girls and moms wear the strappy ombre dress; boys and dads wear the matching short-sleeve crewneck shirt. Shorts, hats, jewelry, bags, and sandals are styling only.</li>','<li><strong>Care:</strong> Machine wash cold on gentle, line dry, do not bleach, and use a cool iron inside-out if needed.</li>','<li><strong>Size range:</strong> Child 2 Years through Child 9-10 Years, Mother S-3XL, and Father S-4XL.</li>','</ul>',table([r for r in chart if r['garment']=='Dress'],'Dress'),table([r for r in chart if r['garment']=='Shirt'],'Shirt'),'<p>Skyfade keeps family matching light, simple, and polished for sunny photos. The dress option has a soft strappy neckline and airy ombre skirt for moms and girls, while the shirt option gives dads and boys an easy crewneck tee in the same fade effect.</p>','<p>Use the Type, Size, and Color selectors to build the exact set you need for beach trips, resort dinners, family portraits, or summer weekends. The listing includes only the dress and shirt garments shown in the size chart.</p>','<h3>Key Features:</h3>','<ul>','<li><strong>Two garment choices:</strong> Dress for girls and moms, shirt for boys and dads.</li>','<li><strong>Two colorways:</strong> Blue and Lavender share the same vendor size chart.</li>','<li><strong>Four-role matching:</strong> Size labels are role-bearing for clearer family ordering.</li>','<li><strong>Warm-weather styling:</strong> Lightweight ombre pieces feel relaxed for beach and vacation plans.</li>','<li><strong>Chart-backed sizing:</strong> Every variant is backed by a row from the attached vendor size chart.</li>','</ul>','<p>Choose the color and each family member\'s type and size to create a soft matching look for your next sunny memory.</p>'])
BODY_HTML_OUT.write_text(body)
SIZE_CHART_OUT.write_text(json.dumps(chart,indent=2))
variants=[]; recap=[]
for r in chart:
    price=CHILD_PRICE if r['audience']=='child' else ADULT_PRICE; compare=CHILD_COMPARE if r['audience']=='child' else ADULT_COMPARE
    for cname,ctok in COLORWAYS:
        variants.append({'price':price,'compareAtPrice':compare,'inventoryPolicy':'DENY','inventoryItem':{'sku':sku(r,ctok),'tracked':True,'requiresShipping':True},'optionValues':[{'optionName':'Type','name':r['garment']},{'optionName':'Size','name':r['picker_label']},{'optionName':'Color','name':cname}]})
        gid,cl=size_map[r['picker_label']]; recap.append({**r,'color':cname,'sku':sku(r,ctok),'price':price,'compare':compare,'size_gid':gid,'catalog_label':cl})
size_values=[]
for r in chart:
    if r['picker_label'] not in size_values: size_values.append(r['picker_label'])
options=[{'name':'Type','values':[{'name':'Dress'},{'name':'Shirt'}]},{'name':'Size','values':[{'name':x} for x in size_values]},{'name':'Color','values':[{'name':'Blue'},{'name':'Lavender'}]}]
tags=sorted(set(['Family Matching','Mommy and Me','Daddy and Me','Matching Family Set','Matching Family Outfits','Matching Family Dress','Matching Family Shirt','Dress & Shirt','Sets','Summer','Beach','Vacation','Resort','Ombre','Gradient','Blue','Lavender','Purple','White','Skyfade','Girls Dress','Mother Dress','Boy Shirt','Father Shirt','Short Sleeve Shirt','Sleeveless Dress','Spaghetti Strap Dress','Crewneck Shirt','Four-Role Matching',VENDOR_URL]+size_values+['Mother S','Mother M','Mother L','Mother XL','Mother 2XL','Mother 3XL','Father S','Father M','Father L','Father XL','Father 2XL','Father 3XL','Father 4XL']))
def gql(query,variables=None):
    data=json.dumps({'query':query,'variables':variables or {}}).encode()
    req=urllib.request.Request(API,data=data,headers={'X-Shopify-Access-Token':TOKEN,'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as r: out=json.loads(r.read())
    if out.get('errors'): raise SystemExit(out['errors'])
    return out
def user_errors(out,path):
    cur=out
    for p in path.split('.'):
        if p: cur=cur.get(p,{})
    if cur: raise SystemExit(cur)
# preflight taxonomy
node=gql('query($id:ID!){node(id:$id){... on TaxonomyCategory{id fullName}}}',{'id':TAXONOMY_GID})['data']['node']
assert node['fullName']==EXPECTED_TAXONOMY
existing=gql('query($handle:String!){productByHandle(handle:$handle){id variants(first:100){nodes{id sku}}}}',{'handle':HANDLE})['data']['productByHandle']
product_input={'handle':HANDLE,'title':TITLE,'descriptionHtml':body,'vendor':'dresslikemommy.com','productType':PRODUCT_TYPE,'tags':tags,'status':'ACTIVE','category':TAXONOMY_GID,'seo':{'title':SEO_TITLE,'description':SEO_DESCRIPTION}}
if existing:
    pid=existing['id']
    out=gql('mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id} userErrors{field message}}}',{'product':{'id':pid,**product_input}}); user_errors(out,'data.productUpdate.userErrors')
    live_skus=sorted([v['sku'] for v in existing['variants']['nodes'] if v.get('sku')])
    spec_skus=sorted([v['inventoryItem']['sku'] for v in variants])
    if live_skus and live_skus!=spec_skus: raise SystemExit(f'existing product has unexpected SKUs: {live_skus}')
    if live_skus==spec_skus:
        q='mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$productId,variants:$variants){userErrors{field message}}}'
        bysku={v['sku']:v['id'] for v in existing['variants']['nodes']}
        ups=[{'id':bysku[v['inventoryItem']['sku']],'price':v['price'],'compareAtPrice':v['compareAtPrice'],'inventoryPolicy':'DENY','optionValues':v['optionValues']} for v in variants]
        out=gql(q,{'productId':pid,'variants':ups}); user_errors(out,'data.productVariantsBulkUpdate.userErrors')
    else:
        out=gql('mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}',{'productId':pid,'variants':variants,'strategy':'REMOVE_STANDALONE_VARIANT'}); user_errors(out,'data.productVariantsBulkCreate.userErrors')
else:
    out=gql('mutation($input:ProductInput!){productCreate(input:$input){product{id} userErrors{field message}}}',{'input':{**product_input,'productOptions':options}}); user_errors(out,'data.productCreate.userErrors')
    pid=out['data']['productCreate']['product']['id']
    out=gql('mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){productVariantsBulkCreate(productId:$productId,variants:$variants,strategy:$strategy){userErrors{field message}}}',{'productId':pid,'variants':variants,'strategy':'REMOVE_STANDALONE_VARIANT'}); user_errors(out,'data.productVariantsBulkCreate.userErrors')
metas=[
{'ownerId':pid,'namespace':'custom','key':'category1','type':'single_line_text_field','value':'Family Matching'}, {'ownerId':pid,'namespace':'custom','key':'subcategory','type':'single_line_text_field','value':'Set'}, {'ownerId':pid,'namespace':'custom','key':'subcategory2','type':'single_line_text_field','value':'Summer Family Matching Set'}, {'ownerId':pid,'namespace':'custom','key':'pattern','type':'single_line_text_field','value':'Skyfade Ombre'}, {'ownerId':pid,'namespace':'custom','key':'style','type':'single_line_text_field','value':'Matching Family Set'}, {'ownerId':pid,'namespace':'custom','key':'type','type':'single_line_text_field','value':'Two-Piece Set'},
{'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_product','type':'boolean','value':'false'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'gender','type':'single_line_text_field','value':'unisex'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'age_group','type':'single_line_text_field','value':'adult'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'condition','type':'single_line_text_field','value':'new'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_label_0','type':'single_line_text_field','value':'Family Matching'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_label_1','type':'single_line_text_field','value':'Skyfade'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_label_2','type':'single_line_text_field','value':'Summer'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_label_3','type':'single_line_text_field','value':'Dress & Shirt'}, {'ownerId':pid,'namespace':'mm-google-shopping','key':'custom_label_4','type':'single_line_text_field','value':'Four-Role Matching'},
{'ownerId':pid,'namespace':'shopify','key':'age-group','type':'list.metaobject_reference','value':json.dumps(['gid://shopify/Metaobject/128116523105','gid://shopify/Metaobject/128116490337'])}, {'ownerId':pid,'namespace':'shopify','key':'care-instructions','type':'list.metaobject_reference','value':json.dumps(['gid://shopify/Metaobject/130283503713'])}, {'ownerId':pid,'namespace':'shopify','key':'color-pattern','type':'list.metaobject_reference','value':json.dumps(['gid://shopify/Metaobject/69639766113','gid://shopify/Metaobject/130284126305','gid://shopify/Metaobject/69639733345'])}, {'ownerId':pid,'namespace':'shopify','key':'size','type':'list.metaobject_reference','value':json.dumps(list(dict.fromkeys(size_map[r['picker_label']][0] for r in chart)))}, {'ownerId':pid,'namespace':'shopify','key':'target-gender','type':'list.metaobject_reference','value':json.dumps(['gid://shopify/Metaobject/129971617889','gid://shopify/Metaobject/130231107681'])}, {'ownerId':pid,'namespace':'global','key':'title_tag','type':'single_line_text_field','value':SEO_TITLE}, {'ownerId':pid,'namespace':'global','key':'description_tag','type':'single_line_text_field','value':SEO_DESCRIPTION}]
for i in range(0,len(metas),25):
    out=gql('mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){userErrors{field message}}}',{'metafields':metas[i:i+25]}); user_errors(out,'data.metafieldsSet.userErrors')
pubs=[{'publicationId':x} for x in ['gid://shopify/Publication/55169925','gid://shopify/Publication/21969633377','gid://shopify/Publication/29172400225','gid://shopify/Publication/76582879329','gid://shopify/Publication/76604768353']]
out=gql('mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id status} userErrors{field message}}}',{'product':{'id':pid,'status':'ACTIVE'}}); user_errors(out,'data.productUpdate.userErrors')
out=gql('mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}',{'id':pid,'input':pubs}); user_errors(out,'data.publishablePublish.userErrors')
# media upload local assets, if present
media=gql('query($id:ID!){product(id:$id){media(first:50){nodes{... on MediaImage{id alt image{url}}}}}}',{'id':pid})['data']['product']['media']['nodes']
alts={m.get('alt') for m in media}
for image_path in sorted(list(UPLOAD_DIR.glob('*.png'))+list(UPLOAD_DIR.glob('*.jpg'))+list(UPLOAD_DIR.glob('*.jpeg'))+list(UPLOAD_DIR.glob('*.webp'))):
    alt='Family wearing Skyfade matching ombre dress and shirt set in blue.' if image_path.name.startswith('01') else 'Family wearing Skyfade matching ombre dress and shirt set in lavender.'
    if alt in alts: continue
    mime=mimetypes.guess_type(str(image_path))[0] or 'image/png'
    out=gql('mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}',{'input':[{'filename':image_path.name,'mimeType':mime,'resource':'IMAGE','httpMethod':'POST'}]}); user_errors(out,'data.stagedUploadsCreate.userErrors')
    target=out['data']['stagedUploadsCreate']['stagedTargets'][0]
    args=['curl','-sS','-X','POST',target['url']]
    for p in target['parameters']: args += ['-F',f"{p['name']}={p['value']}"]
    args += ['-F',f'file=@{image_path}']
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)
    out=gql('mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){userErrors{field message}}}',{'productId':pid,'media':[{'originalSource':target['resourceUrl'],'mediaContentType':'IMAGE','alt':alt}]}); user_errors(out,'data.productCreateMedia.userErrors')
out=gql('mutation($product:ProductUpdateInput!){productUpdate(product:$product){product{id status} userErrors{field message}}}',{'product':{'id':pid,'status':'ACTIVE'}}); user_errors(out,'data.productUpdate.userErrors')
out=gql('mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}',{'id':pid,'input':pubs}); user_errors(out,'data.publishablePublish.userErrors')
time.sleep(3)
verify=gql('query($id:ID!){product(id:$id){id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping}}} collections(first:50){nodes{title handle}} metafields(first:100){nodes{namespace key type value}} resourcePublicationsV2(first:20){nodes{isPublished publication{id name}}}}}',{'id':pid})
VERIFY_JSON_OUT.write_text(json.dumps(verify,indent=2))
p=verify['data']['product']; live=p['variants']['nodes']; live_skus=sorted(v['sku'] for v in live); spec_skus=sorted(v['inventoryItem']['sku'] for v in variants)
checks=[]
checks.append(('title length',len(p['title'])<=70,len(p['title']))); checks.append(('seo title length',len(p['seo']['title'])<=60,len(p['seo']['title']))); checks.append(('seo description length',len(p['seo']['description'])<=155,len(p['seo']['description']))); checks.append(('variant count',len(live)==len(variants),f"{len(live)} vs {len(variants)}")); checks.append(('sku parity',live_skus==spec_skus,', '.join(live_skus))); checks.append(('taxonomy',p['category']['fullName']==EXPECTED_TAXONOMY,p['category']['fullName'])); checks.append(('status active',p['status']=='ACTIVE',p['status'])); checks.append(('published',bool(p['publishedAt']),p['publishedAt'])); checks.append(('online url',bool(p['onlineStoreUrl']),p['onlineStoreUrl']))
price_ok=all(v['price']==next(x['price'] for x in variants if x['inventoryItem']['sku']==v['sku']) and v['compareAtPrice']==next(x['compareAtPrice'] for x in variants if x['inventoryItem']['sku']==v['sku']) and v['inventoryPolicy']=='DENY' and v['inventoryItem']['tracked'] and v['inventoryItem']['requiresShipping'] for v in live)
checks.append(('price/inventory parity',price_ok,'FORCE_SPEC_PRICES true'))
if not all(c[1] for c in checks): raise SystemExit('verification failed '+repr(checks))
# CSV
with CSV_HEADER_SOURCE.open(newline='') as fh: header=next(csv.reader(fh))
rows=[]
for r in recap:
    row={h:'' for h in header}
    vals={'Handle':HANDLE,'Title':TITLE,'Body (HTML)':body,'Vendor':'dresslikemommy.com','Product Category':EXPECTED_TAXONOMY,'Type':PRODUCT_TYPE,'Tags':', '.join(p['tags']),'Published':'TRUE','Option1 Name':'Type','Option1 Value':r['garment'],'Option2 Name':'Size','Option2 Value':r['picker_label'],'Option3 Name':'Color','Option3 Value':r['color'],'Variant SKU':r['sku'],'Variant Grams':'0','Variant Inventory Tracker':'shopify','Variant Inventory Policy':'deny','Variant Fulfillment Service':'manual','Variant Price':r['price'],'Variant Compare At Price':r['compare'],'Variant Requires Shipping':'TRUE','Variant Taxable':'TRUE','SEO Title':SEO_TITLE,'SEO Description':SEO_DESCRIPTION,'Google Shopping / Gender':'unisex','Google Shopping / Age Group':'adult','Google Shopping / Condition':'new','Google Shopping / Custom Product':'FALSE','Google Shopping / Custom Label 0':'Family Matching','Google Shopping / Custom Label 1':'Skyfade','Google Shopping / Custom Label 2':'Summer','Google Shopping / Custom Label 3':'Dress & Shirt','Google Shopping / Custom Label 4':'Four-Role Matching','Category1 (product.metafields.custom.category1)':'Family Matching','Pattern (product.metafields.custom.pattern)':'Skyfade Ombre','Style (product.metafields.custom.style)':'Matching Family Set','SubCategory (product.metafields.custom.subcategory)':'Set','SubCategory2 (product.metafields.custom.subcategory2)':'Summer Family Matching Set','Type (product.metafields.custom.type)':'Two-Piece Set','Google: Custom Product (product.metafields.mm-google-shopping.custom_product)':'false','Age group (product.metafields.shopify.age-group)':'kids, adults','Color (product.metafields.shopify.color-pattern)':'Blue, Purple, White','Size (product.metafields.shopify.size)':', '.join(size_values),'Status':'active'}
    for k,v in vals.items():
        if k in row: row[k]=v
    rows.append(row)
with CSV_OUT.open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=header); w.writeheader(); w.writerows(rows)
written=sorted([f"{m['namespace']}.{m['key']}" for m in p['metafields']['nodes'] if m['namespace'] in ['custom','mm-google-shopping','shopify','global']])
skipped={'shopify.fabric':'Vendor page was blocked and screenshots/size chart do not confirm fiber composition.','shopify.dress-occasion':'Mixed outfit-set taxonomy; dress-only occasion would overstate the product.','shopify.dress-style':'Mixed dress and shirt product under Outfit Sets.','shopify.neckline':'Dress straps and shirt crewneck cannot map to one honest product-level neckline.','shopify.skirt-dress-length-type':'Mixed product under Outfit Sets, not dress-only taxonomy.','shopify.sleeve-length-type':'Dress is sleeveless/strappy while shirts are short sleeve; one product-level value would be misleading.','shopify.top-length-type':'Mixed dresses and shirts; no single top-length value is honest.','shopify.pants-length-type':'Shorts are styling only and excluded.'}
lines=[f'# {TITLE}','','## Links',f'- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/{pid.split("/")[-1]}',f'- **Live:** {p["onlineStoreUrl"]}',f'- **Vendor:** {VENDOR_URL}',f'- **Product GID:** `{pid}`',f'- **Handle:** `{HANDLE}`','','## Inputs (resolved)','| Field | Value |','|---|---|',f'| VENDOR_URL | {VENDOR_URL} |','| SIZE_CHART_SOURCE | attached image |','| LISTING_MODE | Family Matching |','| PRIMARY_CATEGORY | FamilySet (Shopify taxonomy: Outfit Sets) |','| DESIGNS_TO_LIST | One listing with Type = Dress/Shirt and Color = Blue/Lavender |','| FORCE_SPEC_PRICES | true |','| SHORTCODE | auto -> `SKYF` |','| COLOR_TOKEN | Blue -> `BLUE`; Lavender -> `LAV` |','','## Vendor fetch status','The direct 1688 page was treated as blocked/unreliable for this run; the attached product screenshots and attached size chart image were used as authoritative. The chart publishes full garment measurements for girl dresses, adult dresses, child shirts, and adult shirts, so no neighbor garment measurements were borrowed. The adult shirt chart is labeled men/women by the vendor, but the listing scopes it to father shirt sizes to match the supplied family photos and avoid offering an unsupported mother-shirt presentation.','','## Option axes','- Option 1: Type -> Dress, Shirt','- Option 2: Size -> role-bearing size labels','- Option 3: Color -> Blue, Lavender',f'- Variants live: {len(live)} ({len(chart)} size rows x 2 colors)','','## SIZE_CHART / Variant Recap','| Role | Vendor | Picker | Color | Type | SKU | Price | shopify.size GID |','|---|---|---|---|---|---|---|---|']
for r in recap: lines.append(f"| {r['role']} | {r['vendor_label']} | {r['picker_label']} | {r['color']} | {r['garment']} | `{r['sku']}` | {r['price']} | `{r['size_gid']}` ({r['catalog_label']}) |")
lines += ['','## Derivations','- Vendor weights were listed in `斤` and converted to kg in the saved SIZE_CHART and shopper-facing table.','- Dress hip and waist were derived where the vendor omitted them: child hip = chest + 4, child waist = chest; adult dress hip = bust + 6, waist = hip - 8.','- Shirt hip and waist were derived where omitted: child hip/waist = chest; adult shirt hip = chest, waist = chest - 12.','- Styling-only shorts, hats, sunglasses, bags, jewelry, and footwear are excluded from the sellable variant set.','','## Verification','| Check | Result | Detail |','|---|---|---|']
for name,ok,detail in checks: lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines += ['','## Metafields Written'] + [f'- `{x}`' for x in written] + ['','## Metafields Skipped'] + [f'- `{k}`: {v}' for k,v in skipped.items()] + ['','## Smart Collections',', '.join(sorted(c['handle'] for c in p['collections']['nodes'])) or 'Pending smart collection propagation.','','## Publications',', '.join(sorted(n['publication']['name'] for n in p['resourcePublicationsV2']['nodes'] if n['isPublished'])),'','## Saved Files',f'- `{SCRIPT_PATH}`',f'- `{LISTING_MD}`',f'- `{CSV_OUT}`',f'- `{SIZE_CHART_OUT}`',f'- `{BODY_HTML_OUT}`',f'- `{VERIFY_JSON_OUT}`','','## Manual Follow-ups','- Inventory quantities and per-variant weights still need operator stock values.','- Re-check fiber composition if the vendor page becomes directly readable later; `shopify.fabric` is intentionally skipped rather than guessed.']
LISTING_MD.write_text('\n'.join(lines)+'\n')
print(json.dumps({'product_id':pid,'admin_url':f'https://admin.shopify.com/store/dresslikemommy/products/{pid.split("/")[-1]}','live_url':p['onlineStoreUrl'],'variants':len(live),'checks':checks,'listing':str(LISTING_MD),'csv':str(CSV_OUT)},indent=2))
PYRUN
