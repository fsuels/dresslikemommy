from pathlib import Path
import json,re,html
P=Path(__file__).resolve().parent;R=P.parent.parent;S=R/'products/remaining'
rows=json.loads((P/'translation_only_held_worklist.json').read_text())['rows']
maps={};provenance={}
for locale,sourcefile,sourcekey in [('ru','english_segments.json','sourceSpan'),('sv','segments.json','source')]:
 d=S/(locale+'-bodies');sources=json.loads((d/sourcefile).read_text());values={}
 for f in sorted(d.glob('manual_*.json')):values.update(json.loads(f.read_text()))
 maps[locale]={html.unescape(x[sourcekey]).strip():values[x['id']] for x in sources if x['id'] in values}
 provenance[locale]={'sources':str((d/sourcefile).relative_to(R)),'values':[str(f.relative_to(R)) for f in sorted(d.glob('manual_*.json'))]}
if (P/'held_sv_manual.tsv').exists():
 manual=dict(line.split('\t',1) for line in (P/'held_sv_manual.tsv').read_text().splitlines() if line)
 for r in json.loads((P/'held_ru_sv_manual_sources.json').read_text()):
  assert r['id'] in manual
  maps[r['locale']][r['source']]=manual[r['id']]

roleWords={
 'ru':{'Father':'Папа','Mother':'Мама','Boy':'Мальчик','Girl':'Девочка','Child':'Ребёнок','Baby':'Малыш','Men':'Мужчины','Women':'Женщины','Adult':'Взрослый'},
 'sv':{'Father':'Pappa','Mother':'Mamma','Boy':'Pojke','Girl':'Flicka','Child':'Barn','Baby':'Baby','Men':'Män','Women':'Kvinnor','Adult':'Vuxen'},
}
headers={
'Size':('Размер','Storlek'),'Length':('Длина','Längd'),'Clothing Length':('Длина изделия','Plaggets längd'),'Garment Length':('Длина изделия','Plaggets längd'),'Bust':('Обхват груди','Bystmått'),'Chest':('Обхват груди','Bröstmått'),'Shoulder Width':('Ширина плеч','Axelbredd'),'Sleeve Length':('Длина рукава','Ärmlängd'),'Pant Length':('Длина брюк','Byxlängd'),'Hip':('Обхват бёдер','Höftmått'),'Waist':('Обхват талии','Midjemått'),'Suggested Height':('Рекомендуемый рост','Rekommenderad längd'),'Recommended Height':('Рекомендуемый рост','Rekommenderad längd'),'Suggested Weight':('Рекомендуемый вес','Rekommenderad vikt'),'Recommended Weight':('Рекомендуемый вес','Rekommenderad vikt'),'Height':('Рост','Längd'),'Weight':('Вес','Vikt')}
headers.update({'Chest Width':('Ширина груди','Bröstbredd'),'Chest/Bust':('Обхват груди','Bröst-/bystmått')})
def mechanical(s,locale):
 if re.fullmatch(r'[\d\s.,/()<>+\-–—]+',re.sub(r'\b(?:cm|in|kg|lbs|approx)\b','',s)):
  return s.replace('approx','прибл.' if locale=='ru' else 'cirka')
 if s in ['S','M','L','XL','XXL','2XL','3XL','4XL']:return s
 m=re.fullmatch(r'(.+?)(\s*\((?:cm|kg)\s*/\s*(?:in|lbs)\))?',s)
 if m and m[1] in headers:return headers[m[1]][0 if locale=='ru' else 1]+(m[2] or '')
 m=re.fullmatch(r'(Father|Mother|Boy|Girl|Child|Baby|Men|Women|Adult)\s+(.+)',s)
 if m:
  label=roleWords[locale][m[1]];tail=m[2];age=re.fullmatch(r'(\d+(?:-\d+)?)\s+([Yy]ears?|[Mm]onths?)',tail)
  if not age:return label+' '+tail
  n,unit=age.groups()
  if locale=='sv':return label+' '+n+(' månader' if unit.lower().startswith('month') else ' år')
  if unit.lower().startswith('month'):return label+' '+n+' мес.'
  last=int(n.split('-')[-1]);word='год' if last==1 else 'года' if last in [2,3,4] else 'лет'
  return label+' '+n+' '+word
 return None

def prose_nodes(s):
 s=re.sub(r'<table\b.*?</table>','',s,flags=re.S|re.I)
 return [html.unescape(x).strip() for x in re.split('(<[^>]*>)',s) if x.strip() and not x.startswith('<')]
prior={}
for n in ['ru-bodies/held_complete_candidates.json','sv-bodies/held_completed_candidates.json','sv-bodies/legacy_image_hold_candidates.json']:
 for r in json.loads((S/n).read_text())['rows']:prior[(r['resourceId'],r['locale'])]=r
pending=[];pairs=[];selected=[]
for r in rows:
 if r['locale'] not in maps:continue
 priorrow=prior.get((r['resourceId'],r['locale']));oldvalue=priorrow['value'] if priorrow else ((r['before'] or {}).get('value') or '')
 sp,tp=prose_nodes(r['source']),prose_nodes(oldvalue)
 resourceMap={ss:tt for ss,tt in zip(sp,tp) if ss!=tt} if len(sp)==len(tp) else {}
 fields=[]
 for i,p in enumerate(re.split('(<[^>]*>)',r['source'])):
  if not p.strip() or p.startswith('<'):continue
  source=html.unescape(p.strip());value=mechanical(source,r['locale']);method='mechanical_source_facts'
  if value is None:value=maps[r['locale']].get(source);method='exact_source_segment_reuse'
  if value is None:value=resourceMap.get(source);method='same_resource_prose_reuse_pending_meaning_review'
  if value is None:pending.append({'resourceId':r['resourceId'],'locale':r['locale'],'partIndex':i,'source':source})
  else:pairs.append({'resourceId':r['resourceId'],'locale':r['locale'],'source':source,'value':value,'method':method})
  fields.append({'partIndex':i,'source':source,'value':value,'method':method})
 selected.append({**r,'nodes':fields})
for name,data in [('held_ru_sv_prepared.json',{'rows':selected,'reuseProvenance':provenance}),('held_ru_sv_pending.json',{'rows':pending}),('held_ru_sv_review_pairs.json',{'rows':pairs})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selected':len(selected),'pendingNodes':len(pending),'uniquePending':len(set((r['locale'],r['source']) for r in pending)),'mappedNodes':len(pairs)}))
