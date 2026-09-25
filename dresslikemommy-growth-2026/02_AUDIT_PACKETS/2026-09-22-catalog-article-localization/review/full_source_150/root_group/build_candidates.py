import json, re, hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
sources=json.loads((HERE/'prose_source_nodes.json').read_text())
rows=json.loads((HERE/'worklist21.json').read_text())['rows']
prose={l:json.loads((HERE/(l+'_prose.json')).read_text()) for l in ['ru','sv','de']}
common_sources=['Fabric:','Family story:','Print reference:','Design details:','Care:','Size range:','Key Features:','Print:','Color:','Fabric &amp; feel:']
common={
 'ru':['Ткань:','Семейная история:','Рисунок:','Детали дизайна:','Уход:','Размерный ряд:','Основные особенности:','Рисунок:','Цвет:','Ткань и ощущения:'],
 'sv':['Tyg:','Familjetema:','Mönster:','Designdetaljer:','Skötsel:','Storleksintervall:','Viktiga egenskaper:','Mönster:','Färg:','Tyg och känsla:'],
 'de':['Stoff:','Familienthema:','Muster:','Designdetails:','Pflege:','Größensortiment:','Wichtige Merkmale:','Muster:','Farbe:','Stoff und Tragegefühl:']}
header_sources=['Size','Age','Weight','Bust','Chest/Bust','Height','Hip','Waist','Garment Length','Coat Length','Shoulder Width','Sleeve Length','Sleeve / Skirt','Sleeve or Skirt','Pant / Short','Pant/Short or -','Adjustable Strap','Hem/Body Opening','Top Chest/Bust','Top Length','Pants Length','Top Hip','Top Waist','Pants Waist']
headers={
 'ru':['Размер','Возраст','Вес','Обхват груди','Обхват груди','Рост','Обхват бёдер','Обхват талии','Длина изделия','Длина изделия','Ширина плеч','Длина рукава','Рукав / юбка','Рукав или юбка','Брюки / шорты','Брюки/шорты или -','Регулируемая бретель','Нижнее отверстие изделия','Обхват груди топа','Длина топа','Длина брюк','Обхват бёдер топа','Обхват талии топа','Обхват талии брюк'],
 'sv':['Storlek','Ålder','Vikt','Bystomfång','Bröst-/bystomfång','Kroppslängd','Höftomfång','Midjeomfång','Plagglängd','Plagglängd','Axelbredd','Ärmlängd','Ärm / kjol','Ärm eller kjol','Byxor / shorts','Byxor/shorts eller -','Justerbart axelband','Fåll-/kroppsöppning','Toppens bröst-/bystomfång','Topplängd','Byxlängd','Toppens höftomfång','Toppens midjeomfång','Byxornas midjeomfång'],
 'de':['Größe','Alter','Gewicht','Brustumfang','Brustumfang','Körpergröße','Hüftumfang','Taillenumfang','Kleidungslänge','Kleidungslänge','Schulterbreite','Ärmellänge','Ärmel / Rock','Ärmel oder Rock','Hose / Shorts','Hose/Shorts oder -','Verstellbarer Träger','Saum-/Körperöffnung','Brustumfang des Oberteils','Oberteillänge','Hosenlänge','Hüftumfang des Oberteils','Taillenumfang des Oberteils','Taillenumfang der Hose']}

def role(s,l):
 m=re.fullmatch(r'Child (\d+(?:-\d+)?) [Yy]ears?',s)
 if m:
  a=m[1]
  if l=='ru':
   n=int(a.split('-')[-1]); unit='год' if n%10==1 and n%100!=11 else 'года' if n%10 in [2,3,4] and n%100 not in [12,13,14] else 'лет'
   return f'Ребёнок {a} {unit}'
  return f'Barn {a} år' if l=='sv' else f'Kind {a} '+('Jahr' if a=='1' else 'Jahre')
 for en,ls in [('Mother',['Мама','Mamma','Mutter']),('Father',['Папа','Pappa','Vater']),('Adult',['Взрослый','Vuxen','Erwachsene'])]:
  if s.startswith(en+' '): return ls[['ru','sv','de'].index(l)]+s[len(en):]
 if s.startswith('Up to '): return {'ru':'До ','sv':'Upp till ','de':'Bis zu '}[l]+s[6:]
 return None

out=[];pairs=[]
for r in rows:
 i=str(r['productIndex']);l=r['locale'];assert len(sources[i])==len(prose[l][i]),(i,l)
 mp=dict(zip(sources[i],prose[l][i]));mp.update(zip(common_sources,common[l]));h=dict(zip(header_sources,headers[l]));ledger=[]
 def trans(m):
  raw=m[1];s=raw.strip()
  if not s:return m[0]
  target=mp.get(s)
  if target is None:
   hs=re.fullmatch(r'(.+?)( \([^)]*\))?',s)
   if hs and hs[1] in h:target=h[hs[1]]+(hs[2] or '')
  if target is None:target=role(s,l)
  if target is None:
   assert not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',s)),(i,l,s)
   target=s
  assert not re.search('[<>]',target)
  ledger.append({'source':s,'target':target})
  return '>'+raw[:len(raw)-len(raw.lstrip())]+target+raw[len(raw.rstrip()):]+'<'
 value=re.sub(r'>([^<>]*)<',trans,r['sourceValue'])
 assert re.findall(r'<[^>]+>',value)==re.findall(r'<[^>]+>',r['sourceValue'])
 assert re.findall(r'\d+(?:\.\d+)?',value)==re.findall(r'\d+(?:\.\d+)?',r['sourceValue']),(i,l,'numbers')
 assert not re.search(r'QZ\d|QX\d|\dQXZ',value)
 out.append({**r,'value':value,'valueSHA256':sha(value),'reviewStatus':'AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW','reconstruction':'Full current-source text translation with exact source tags/attributes/numeric tokens/measurement units preserved.'})
 pairs.append({'resourceId':r['resourceId'],'productIndex':int(i),'locale':l,'nodes':ledger})
(HERE/'candidates21.json').write_text(json.dumps({'rows':out},ensure_ascii=False,indent=2)+'\n')
(HERE/'node_pairs21.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'sourceNodesRead':sum(len(r['nodes']) for r in pairs),'candidateSHA256':hashlib.sha256((HERE/'candidates21.json').read_bytes()).hexdigest()}))
