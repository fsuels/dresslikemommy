"""Assemble manual Swedish product-body proposals, no external operations."""
import json,pathlib,sys,hashlib,re
from prepare_segments import parts,norm,neutral
B=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(B.parents[2]/'tooling'))
from offline_translation import verify_text
rows=json.loads((B/'selected_baseline.json').read_text())['rows'];segments=json.loads((B/'segments.json').read_text());index={x['source']:x['id'] for x in segments};manual={}
for p in B.glob('manual_*.json'):
 for k,v in json.loads(p.read_text()).items():
  assert k not in manual or manual[k]==v
  manual[k]=v
mixed={
 'Tyg: Cotton':'Tyg: bomull',
 'Mönster: tropical/botanical floral':'Mönster: tropiskt/botaniskt blommönster',
 'Mönster: tropical floral/leaf (navy multi)':'Mönster: tropiska blommor/löv (marinblått, flerfärgat)',
 'Colour/Mönster:':'Färg/mönster:',
 'Girls Flicka 2 år to Flicka 9-10 år; Mamma M to Mamma 3XL.':'Flickor från Flicka 2 år till Flicka 9-10 år; Mamma M till Mamma 3XL.',
 'Blue daisy Mönster:':'Blått prästkragsmönster:',
 'Mamma Sizes':'Mammastorlekar',
 'Vuxen Sizes':'Vuxenstorlekar',
 'Premium Tyg:':'Tyg av förstklassig kvalitet:',

 'Easy Skötsel: Machine washable, durable print':'Enkel skötsel: Maskintvättbart, hållbart tryck',
 'Durable and Stretchable Tyg:':'Slitstarkt och elastiskt tyg:',
 'Soft and Stretchy Tyg:':'Mjukt och elastiskt tyg:',
 'Premium Quality Tyg: Crafted from a blend of nylon and spandex, experience the perfect mix of flexibility and durability for all-day comfort.':'Tyg av förstklassig kvalitet: Upplev den perfekta kombinationen av följsamhet och hållbarhet för komfort hela dagen, med en blandning av nylon och spandex.',
 'Easy Skötsel: Machine washable and resistant to fading, keep your swimwear looking new all season long.':'Enkel skötsel: Badkläderna kan maskintvättas och motstår blekning så att de håller sig som nya hela säsongen.',
 'Skötsel: follow the garment care label.':'Skötsel: följ plaggets skötseletikett.',
 'Sizing varies by brand and region—use the provided size chart and garment measurements before ordering. Skötsel: follow the care label instructions.':'Storlekar varierar mellan märken och regioner – använd den angivna storlekstabellen och plaggmåtten innan du beställer. Skötsel: följ skötseletikettens anvisningar.',
 'Skötsel: follow the garment care label for best results.':'Skötsel: följ plaggets skötseletikett för bästa resultat.',
 'One koordinerad t-shirt:':'En koordinerad t-shirt:',
 'Storlekstabell - Swim Dress':'Storlekstabell – badklänning'
}
completed=[];held=[];pending=[];checks=[];inverse=[];blocked=[]
source_blocked={x['resourceId'] for x in json.loads((B/'new_source_blockers.json').read_text())['rows']}
for r in rows:
 if r['resourceId'] in source_blocked or 'numeric_values_changed' in r['initialVerification']['errors']:
  blocked.append({k:v for k,v in r.items() if k!='baseValue'})
  continue
 out=[];missing=[];changed=[]
 for tag,text in parts(r['baseValue']):
  if tag or not text.strip():out.append(text);continue
  n=norm(text);value=None
  if n in index:
   id=index[n]
   if id not in manual:missing.append(id)
   else:value=manual[id]
  elif n in mixed:value=mixed[n]
  elif re.fullmatch(r'(?:Barn|Flicka|Pojke) \d+(?:-\d+)? [Yy]ears?(?: [A-Z]| \(\d+\)| / (?:Short|Overall|T-shirt))?',n):
   value=re.sub(r'\b[Yy]ears?\b','år',n)
   value=re.sub(r' / Short$',' / Shorts',value)
  if r['resourceId']=='gid://shopify/Product/7502791082081' and n=='Comfortable':value='Bekväm'
  if value is None:out.append(text);continue
  prefix=text[:len(text)-len(text.lstrip())];suffix=text[len(text.rstrip()):]
  out.append(prefix+value+suffix);changed.append({'beforeText':text.strip(),'value':value})
 if missing:
  pending.append({'resourceId':r['resourceId'],'missingSegments':sorted(set(missing),key=int)});continue
 value=''.join(out);result=verify_text(r['source'],value,'sv');preserve=verify_text(r['baseValue'],value,'sv')
 # Existing Swedish numbers are already locale-formatted. Shape/attrs/links checks
 # are strict; source numeric check is independent and authoritative for proposal.
 candidate={k:v for k,v in r.items() if k not in ['baseValue','initialVerification']}
 candidate.update({'value':value,'sourceSHA256':hashlib.sha256(r['source'].encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest(),'reason':'Manually translated English text spans; existing Swedish retained. Exact source/digest/before bound.','changedTextNodes':changed,'verification':result})
 (held if result['errors'] else completed).append(candidate)
 checks.append({'resourceId':r['resourceId'],'sourceComparison':result,'basePreservationComparison':preserve})
 inverse.append({'resourceId':r['resourceId'],'locale':'sv','key':'body_html','value':r['before']['value'] if r['before'] else None,'sourceDigest':r['sourceDigest'],'expectedCurrentValueSHA256':candidate['valueSHA256'],'operation':'translationsRegister' if r['before'] else 'translationsRemove','beforeMetadata':r['before'],'requiresFreshSourceAndCurrentValueGuard':True})
for fn,data in [('completed_candidates.json',{'rows':completed}),('held_completed_candidates.json',{'rows':held}),('pending.json',{'rows':pending}),('verification.json',{'rows':checks}),('inverse.json',{'rows':inverse}),('blocked_fields.json',{'rows':blocked})]:
 (B/fn).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'manualSegments':len(manual),'completedPassing':len(completed),'completedHeld':len(held),'pending':len(pending),'sourceOrMeasurementBlocked':len(blocked)}))
