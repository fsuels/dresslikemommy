import json,re
exec(open('build.py').read().split('# --- body-text fallback')[0].replace("json.dump(rows,open('draft.json','w'),indent=1,ensure_ascii=False)",''))
Sx={x['id']:x for x in S}
FIBW='cotton|polyester|spandex|elastane|nylon|viscose|rayon|acrylic|wool|linen|bamboo|modal|lyocell|tencel|polyamide'
def composition(body):
    m=re.findall(r'(\d{1,3})\s?%\s?('+FIBW+r')',body,re.I)
    seen=[];tot=0
    for p,f in m:
        f=f.lower().replace('elastane','spandex')
        if f in [s[1] for s in seen]: continue
        seen.append((int(p),f)); tot+=int(p)
        if tot>=100: break
    if seen and 95<=tot<=100:
        return ', '.join(f'{p}% {f}' for p,f in seen)
    return None
BODYFIB=[(r'cotton[- ]blend','cotton blend'),(r'polyester[- ]blend','polyester blend'),(r'(?<![a-z-])cotton(?![- ](feel|blend))','cotton'),(r'polyester(?![- ]blend)','polyester'),(r'chiffon','chiffon'),(r'velvet','velvet'),
(r'fleece','fleece'),(r'denim','denim'),(r'linen(?![- ]look)','linen'),(r'spandex|elastane','spandex'),(r'nylon','nylon'),(r'viscose|rayon','viscose'),(r'acrylic','acrylic'),(r'bamboo(?! garden)','bamboo')]
BASE={'cotton','cotton blend','polyester','polyester blend','viscose','linen','acrylic','bamboo'}
def body_single(b):
    b=b.lower(); found=[]
    for pat,lab in BODYFIB:
        if re.search(r'(?<![a-z])'+pat,b) and lab not in found: found.append(lab)
    if 'cotton blend' in found and 'cotton' in found: found.remove('cotton')
    if 'polyester blend' in found and 'polyester' in found: found.remove('polyester')
    base=[f for f in found if f in BASE]
    if len(base)>1 and set(base)!={'bamboo','cotton'}: return None,'ambiguous:'+','.join(found)
    if set(base)=={'bamboo','cotton'}: found=['bamboo cotton']+[f for f in found if f not in('bamboo','cotton')]
    return (found or None),None
PAT_TITLE=[(r'fair isle','Fair Isle'),(r'stripe','Striped'),(r'plaid','Plaid'),(r'gingham','Gingham'),(r'floral|flower','Floral'),(r'leopard','Leopard print'),(r'cow print','Cow print'),
(r'geometric','Geometric print'),(r'polka|dots?\b','Polka dot'),(r'heart','Heart print'),(r'dino|saurus','Dinosaur graphic print'),(r'tropical|palm|leaf|hibiscus|monstera','Tropical print'),
(r'watercolor','Watercolor print'),(r'tie[- ]dye','Tie-dye'),(r'ombr[eé]|gradient','Ombré'),(r'camo','Camouflage'),(r'letter|slogan|text','Graphic lettering print')]
def title_pattern(t):
    for p,l in PAT_TITLE:
        if re.search(p,t,re.I): return l
    return None
out=[];notes=[]
for r in rows:
    x=Sx[r['id']]; lead=(x['seo']['description'] or '').strip()
    if not lead: r['new']=None; r['skip']='no_seo_description'; out.append(r); continue
    # pattern fixes
    pat=r['pattern']
    tp=title_pattern(x['title'])
    if pat and re.fullmatch(r'solid',pat,re.I) and tp: notes.append((x['handle'],'pattern Solid->'+tp)); pat=tp
    if pat and re.search('fair isle',pat,re.I): pat=re.sub(r'(?i)\s*print$','',pat)
    MOTIF=r'reindeer|santa|heart|star|snow|ghost|pumpkin|skeleton|bunny|bunnies|boo|trick or treat|halloween|christmas|stocking|candy cane|jingle|merry|jolly|family|dino|panda|cat|sheep|grape|peach|pear|butterfl|ladybug|bird|puppy|sea|polar|bear|daisy|floral|flower|bloom|blossom|palm|leaf|monstera|banana|tropical|hydrangea|tulle|smile|smiley|moon|horse|safari|animal|leopard|marble|paint|geometric|tile|fair isle|confetti|dot|graphic|cartoon|lights|tree|village|pom-pom|watercolor|doodle|lettering'
    if pat and re.search(r'(?i)botanical',pat): pat='Botanical print'
    elif pat and pat.endswith(' print') and not re.search(MOTIF,pat,re.I):
        notes.append((x['handle'],'design-name pattern dropped: '+pat)); pat=None
    if not pat and tp: pat=tp
    # material
    comp=composition(x['description'])
    tagm=r['material']; msrc=None; mat=None
    if comp:
        mat=comp; msrc='body_composition'
        cons=[t for t in (tagm or []) if t in ('knit','cable knit','jacquard knit','open knit','velvet','gauze','muslin','denim','fleece','lace')]
        if cons and cons[0] not in comp: mat=comp+' '+cons[0]
    elif tagm: mat=join(tagm); msrc='tags'
    else:
        fablines=' '.join(re.findall(r'(?i)(?:^|\W)(?:fabric|material)s?\s*[:：][^.\n]*',x['description']))
        bs,note=body_single(lead+' '+fablines)
        if bs: mat=join(bs); msrc='body_text'
        elif note: notes.append((x['handle'],note))
    if comp and tagm and not any(t.split()[0] in comp for t in tagm): notes.append((x['handle'],f'tag {tagm} vs composition {comp}'))
    cols=r['colors']
    parts=[]
    if cols: parts.append(('Colors: ' if len(cols)>1 else 'Color: ')+join(cols)+'.')
    if pat: parts.append('Pattern: '+pat+'.')
    if mat: parts.append('Material: '+mat[0].upper()+mat[1:]+'.')
    if lead and not lead.endswith(('.','!','?')): lead+='.'
    r.update(pattern=pat,material=mat,material_src=msrc,new=(lead+' '+' '.join(parts)).strip(),len=0)
    r['len']=len(r['new']); r.pop('material_note',None)
    if r['new']==x['seo']['description']: r['skip']='unchanged'
    out.append(r)
json.dump(out,open('final.json','w'),indent=1,ensure_ascii=False)
from collections import Counter
todo=[r for r in out if not r.get('skip')]
print('to write',len(todo),'skips',Counter(r.get('skip') for r in out if r.get('skip')))
print('with color',sum(1 for r in todo if r['colors']),'pattern',sum(1 for r in todo if r['pattern']),'material',sum(1 for r in todo if r['material']),Counter(r['material_src'] for r in todo))
print('maxlen',max(r['len'] for r in todo))
for n in notes: print('NOTE',n)
