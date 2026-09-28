import json,re
S=json.load(open('seo_state.json'))
COLORS=[('light blue','Light blue'),('sky blue','Sky blue'),('light green','Light green'),('navy','Navy'),('black','Black'),('white','White'),('red','Red'),('pink','Pink'),('blush','Pink'),('blue','Blue'),('green','Green'),('yellow','Yellow'),('orange','Orange'),('cream','Cream'),('ivory','Ivory'),('purple','Purple'),('lilac','Lilac'),('gray','Gray'),('grey','Gray'),('charcoal','Charcoal'),('brown','Brown'),('beige','Beige'),('burgundy','Burgundy'),('apricot','Apricot'),('coral','Coral'),('khaki','Khaki'),('sage','Sage'),('mint','Mint'),('lavender','Lavender'),('teal','Teal'),('gold','Gold'),('multi color','Multicolor'),('multi-color','Multicolor'),('multicolor','Multicolor'),('rainbow','Multicolor')]
BLACK=['red panda','red heart raglan-overdeler']  # design names, not garment colors
def colors_in(text):
    t=' '+text.lower()+' '
    for b in BLACK: t=t.replace(b,' ')
    found=[]
    for k,lab in COLORS:
        if re.search(r'(?<![a-z])'+re.escape(k)+r'(?![a-z])',t):
            t=re.sub(r'(?<![a-z])'+re.escape(k)+r'(?![a-z])',' ',t)
            if lab not in found: found.append(lab)
    return found
PAT_OK=r'print|floral|stripe|plaid|gingham|dot|solid|block|chevron|lace|dye|ombr|eyelet|crochet|leopard'
PMAP={'Solid Ivory':'Solid','Denim Blue':'Solid denim','Washed Denim':'Washed denim','Indigo Pocket':'Solid','Embroidered Ivory':'Embroidered',
'Solid White with Rosette Applique':'Solid with rosette appliqué','Trail Plaid Cargo':'Plaid','Ivory Stripe Cargo':'Striped','Fresh Blue Plaid':'Plaid',
'Summer Sky Stripe':'Striped','Blue Striped Crochet Coastal':'Striped crochet','Rainbow Stripe Multicolor':'Rainbow stripe','Blue Tie-Dye Butterfly Ombré':'Tie-dye butterfly ombré',
'Pink Horizon Ombre':'Ombré','Blue Apricot Heart':'Heart print','Safari Caravan Animal Print':'Safari animal print','Color Block':'Color block','Polka Dot':'Polka dot',
'Animal Print':'Animal print','Tropical Meadow Wildflower Floral':'Wildflower floral','Citrus Bloom Floral':'Floral','Bluebell Meadow Floral':'Floral','Scarlet Blossom Floral':'Floral',
'Blush Floral':'Floral','Pink Floral':'Floral','Green Floral':'Floral','Watercolor Floral':'Watercolor floral','Vintage Cottage Floral Print':'Vintage floral print',
'Good Night Song of the Sea watercolor ocean print with whales, turtles, jellyfish, mermaids':'Watercolor sea-life print','Summer Puppies watercolor golden retriever print':'Watercolor puppy print',
'Watercolor bunnies + meadow floral print':'Watercolor bunny floral print','Watercolor Grapevine print — grapes, leaves, trailing vines on cream':'Watercolor grapevine print',
'Peach Sweetheart watercolor peach print':'Watercolor peach print','Little Pear cartoon fruit print on cream with sage leaves':'Cartoon pear print',
'Ladybug Dots wildflower print on pale blue bamboo-cotton gauze':'Ladybug and wildflower print','Red Panda watercolor red panda + peach orchard print':'Watercolor red panda print',
'Watercolor bunnies + eucalyptus meadow print':'Watercolor bunny print','Watercolor Welsh dragon + baby dinosaur cloud meadow print':'Watercolor dragon and dinosaur print',
'Watercolor fairy-tale messenger bunny + swan meadow village print':'Watercolor bunny and swan print','Bamboo Garden Panda Print':'Panda print','Bird Chirping Fruit Orchard Print':'Bird and fruit print',
'Little Sheep Meadow Print':'Sheep print','Grape Vineyard Print':'Grape print','Fluttering Butterflies Print':'Butterfly print','Polar Adventure Watercolor Print':'Watercolor polar animal print',
'Meow Star Garden Print':'Cat print','Autumn Woodland Bunny':'Woodland bunny print','Lace':'Lace','Powder Blue Eyelet':'Eyelet','Gingham':'Gingham','Chevron':'Chevron','Striped':'Striped','Floral':'Floral','Solid':'Solid','Tropical':'Tropical print'}
def pattern(v):
    if not v: return None
    v=v.strip()
    if v in PMAP: return PMAP[v]
    if re.search(PAT_OK,v,re.I): return v[0].upper()+v[1:].lower()
    return v[0].upper()+v[1:].lower()+' print'
FAB=[('Bamboo Cotton Gauze','bamboo-cotton gauze'),('Bamboo Gauze','bamboo gauze'),('Cotton Gauze','cotton gauze'),('Four-Layer Gauze','four-layer gauze'),('Four Layer Gauze','four-layer gauze'),('Gauze','gauze'),
('Cotton Muslin','cotton muslin'),('Muslin','muslin'),('Bamboo Cotton','bamboo cotton'),('Cotton Blend','cotton blend'),('Cotton','cotton'),('Bamboo','bamboo'),('Nylon','nylon'),('Spandex','spandex'),
('Velvet','velvet'),('Denim','denim'),('Washed Denim','denim'),('Cable Knit','cable knit'),('Jacquard Knit','jacquard knit'),('Open Knit','open knit'),('Knit Sweater','knit'),('Knit','knit'),('Lace','lace'),('Linen Look','linen-look fabric'),('Chiffon Dress','chiffon')]
def material(tags):
    ts=set(tags); out=[]
    for tag,lab in FAB:
        if tag in ts and lab not in out: out.append(lab)
    words=' '.join(out)
    # drop components already covered by a compound
    res=[]
    for m in out:
        if any(m!=o and re.search(r'(?<![a-z-])'+re.escape(m)+r'(?![a-z])',o) for o in out): continue
        res.append(m)
    if 'cotton blend' in res and 'cotton' in res: res.remove('cotton')
    if 'knit' in res and any('knit' in r and r!='knit' for r in res): res.remove('knit')
    return res
def join(xs):
    return xs[0] if len(xs)==1 else ', '.join(xs[:-1])+' and '+xs[-1]
rows=[]
for x in S:
    lead=(x['seo']['description'] or '').strip()
    opts={o['name'].lower():[v['name'] for v in o['optionValues']] for o in x['options']}
    cols=[]
    for v in opts.get('color',[]):
        for c in colors_in(v):
            if c not in cols: cols.append(c)
    src='option'
    if not cols:
        cols=colors_in(x['title']); src='title'
    if len(cols)>6: cols=cols[:6]
    pat=pattern((x.get('metafield') or {}).get('value'))
    mat=material(x['tags'])
    parts=[]
    if cols: parts.append(('Colors: ' if len(cols)>1 else 'Color: ')+join(cols)+'.')
    if pat: parts.append('Pattern: '+pat+'.')
    if mat: m=join(mat); parts.append('Material: '+m[0].upper()+m[1:]+'.')
    tail=' '.join(parts)
    if lead and not lead.endswith(('.','!','?')): lead+='.'
    new=(lead+' '+tail).strip() if lead else None
    rows.append({'id':x['id'],'handle':x['handle'],'title':x['title'],'before':x['seo']['description'],'new':new,'colors':cols,'color_src':src,'pattern':pat,'material':mat,'len':len(new or '')})
json.dump(rows,open('draft.json','w'),indent=1,ensure_ascii=False)
import collections
print('n',len(rows),'no lead',sum(1 for r in rows if not r['new']))
print('no color',sum(1 for r in rows if not r['colors']),'no pattern',sum(1 for r in rows if not r['pattern']),'no material',sum(1 for r in rows if not r['material']))
print('maxlen',max(r['len'] for r in rows),'>320',sum(1 for r in rows if r['len']>320))

# --- body-text fallback for material (store's own published copy; skip if ambiguous)
BODYFIB=[(r'cotton[- ]blend','cotton blend'),(r'bamboo','bamboo'),(r'(?<!non-)cotton','cotton'),(r'polyester','polyester'),(r'chiffon','chiffon'),(r'velvet','velvet'),
(r'fleece','fleece'),(r'denim','denim'),(r'linen(?![- ]look)','linen'),(r'knit(?:ted)?','knit'),(r'spandex|elastane','spandex'),(r'nylon','nylon'),(r'viscose|rayon','viscose'),(r'acrylic','acrylic')]
Sx={x['id']:x for x in S}
for r in rows:
    if r['material'] or not r['new']: continue
    b=Sx[r['id']]['description'].lower()
    found=[]
    for pat,lab in BODYFIB:
        if re.search(r'(?<![a-z])'+pat,b):
            if lab=='cotton' and 'cotton blend' in found: continue
            if lab not in found: found.append(lab)
    wov={'cotton','cotton blend','polyester','viscose','linen','acrylic','bamboo'}
    fibers=[f for f in found if f in wov]
    # ambiguous if 2+ competing base fibers (other than bamboo+cotton)
    if len(fibers)>1 and set(fibers)!={'bamboo','cotton'}: r['material_note']='ambiguous:'+','.join(found); continue
    mat=[f for f in found if f in wov or f in {'chiffon','velvet','fleece','denim','knit','spandex','nylon'}]
    if not mat: continue
    if set(mat)>={'bamboo','cotton'}: mat=['bamboo cotton']+[m for m in mat if m not in('bamboo','cotton')]
    r['material']=mat; r['material_src']='body'
    m=join(mat); r['new']=r['new']+' Material: '+m[0].upper()+m[1:]+'.'; r['len']=len(r['new'])
json.dump(rows,open('draft.json','w'),indent=1,ensure_ascii=False)
print('after body fallback: no material',sum(1 for r in rows if not r['material']),'maxlen',max(r['len'] for r in rows))
