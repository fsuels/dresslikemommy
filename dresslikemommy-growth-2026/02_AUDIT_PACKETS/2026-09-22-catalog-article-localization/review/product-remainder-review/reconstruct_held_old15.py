# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,html,importlib.util,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
rows=[r for r in json.loads((P/'translation_only_held_worklist.json').read_text())['rows'] if r['priorHoldArtifact']=='older_stale_table_holds.json']
headsource=['Size','Length','Bust','Shoulder Width','Sleeve Length','Pant Length','Hip','Suggested Height','Suggested Weight']
heads={
'ar':['المقاس','الطول','محيط الصدر','عرض الكتفين','طول الكم','طول البنطال','محيط الوركين','الطول المقترح','الوزن المقترح'],
'hi':['आकार','लंबाई','छाती का घेरा','कंधों की चौड़ाई','आस्तीन की लंबाई','पैंट की लंबाई','कूल्हों का घेरा','सुझाई गई ऊँचाई','सुझाया गया वजन'],
'it':['Taglia','Lunghezza','Circonferenza del torace','Larghezza delle spalle','Lunghezza delle maniche','Lunghezza dei pantaloni','Circonferenza dei fianchi','Altezza consigliata','Peso consigliato'],
'ja':['サイズ','着丈','胸囲','肩幅','袖丈','パンツ丈','ヒップ','推奨身長','推奨体重'],
'ko':['사이즈','총장','가슴둘레','어깨너비','소매 길이','바지 길이','엉덩이둘레','권장 키','권장 체중'],
'nl':['Maat','Lengte','Borstomvang','Schouderbreedte','Mouwlengte','Broeklengte','Heupomvang','Aanbevolen lengte','Aanbevolen gewicht'],
'pl':['Rozmiar','Długość','Obwód klatki piersiowej','Szerokość ramion','Długość rękawa','Długość spodni','Obwód bioder','Zalecany wzrost','Zalecana waga'],
'pt-BR':['Tamanho','Comprimento','Busto','Largura dos ombros','Comprimento da manga','Comprimento da calça','Quadril','Altura sugerida','Peso sugerido'],
}
roles={
'ar':['الأب','الأم','ولد','بنت','سنوات'],'hi':['पिता','माँ','लड़का','लड़की','वर्ष'],'it':['Papà','Mamma','Bambino','Bambina','anni'],'ja':['パパ','ママ','男の子','女の子','歳'],'ko':['아빠','엄마','남아','여아','세'],'nl':['Vader','Moeder','Jongen','Meisje','jaar'],'pl':['Tata','Mama','Chłopiec','Dziewczynka','lat'],'pt-BR':['Pai','Mãe','Menino','Menina','anos']}
fixes=[
('ar','القمصان البيضاء','التيشيرتات البيضاء'),('ar','قمصان بيضاء','تيشيرتات بيضاء'),('ar','وقمصان مع شورتات','وتيشيرتات مع شورتات'),
('hi','आकर्षक, आकर्षक लुक','हवादार और आकर्षक लुक'),
('hi','मां और बेटियों के लिए आकर्षक पोशाकें','माँ और बेटियों के लिए लहराती हुई ड्रेस'),
('hi','आकस्मिक गर्मियों की सैर','आरामदायक गर्मियों की सैर'),
('ko','하늘거리는 계층 맥시 드레스','하늘거리는 티어드 맥시 원피스'),
('ko','해변과 여름 모험을 위한 생동감 넘치는 가족 의상','해변과 여름 모험을 위한 생동감 넘치는 매칭 가족 의상'),
('nl','Wijde jurken','Zwierige jurken'),
('pt-BR','manter a calma','manter o frescor'),
('pt-BR','Vestidos femininos e femininos:','Vestidos para mulheres e meninas:'),
('pt-BR','Roupas masculinas e masculinas:','Roupas para homens e meninos:'),
('pt-BR','roupas familiares vibrantes e tropicais','roupas familiares combinando, vibrantes e tropicais'),
('pt-BR','Roupas familiares vibrantes para','Roupas familiares vibrantes e combinando para'),
('it','Abbigliamenti familiari vivaci e coordinati','Vivaci abiti coordinati per la famiglia'),
]
def textparts(s):return [(i,html.unescape(x.strip())) for i,x in enumerate(re.split('(<[^>]*>)',s)) if x.strip() and not x.startswith('<')]
def tabletext(s,l):
 numeric=re.sub(r'\b(?:cm|in|kg|lbs|approx)\b','',s)
 if re.fullmatch(r'[\d\s.,/()<>+\-–—]+',numeric):return s.replace('approx',{'ar':'تقريبًا','hi':'लगभग','it':'circa','ja':'約','ko':'약','nl':'circa','pl':'około','pt-BR':'aprox.'}[l])
 m=re.fullmatch(r'(.+?)(\s*\((?:cm|kg)\s*/\s*(?:in|lbs)\))?',s)
 if m and m[1] in headsource:return heads[l][headsource.index(m[1])]+(m[2] or '')
 m=re.fullmatch(r'(Father|Mother|Boy|Girl)\s+(.+)',s)
 if m:
  role=roles[l][['Father','Mother','Boy','Girl'].index(m[1])];tail=m[2]
  if tail.endswith(' Years'):
   n=tail[:-6];return role+' '+n+('' if l in ['ja','ko'] else ' ')+roles[l][4]
  return role+' '+tail
 raise ValueError((l,s))
out=[];checks=[]
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
for r in rows:
 source=r['source'];parts=re.split('(<[^>]*>)',source);sp=textparts(source);n=len(textparts(source.split('<table',1)[0]));tp=textparts(r['before']['value'])[:n];changes=[]
 assert len(tp)==n
 for index,(i,s) in enumerate(sp):
  val=tp[index][1] if index<n else tabletext(s,r['locale'])
  original=val
  for locale,old,new in fixes:
   if r['locale']==locale:val=val.replace(old,new)
  if val!=original:changes.append({'source':s,'beforeText':original,'valueText':val})
  old=parts[i];lead=old[:len(old)-len(old.lstrip())];trail=old[len(old.rstrip()):];parts[i]=lead+html.escape(val,quote=False)+trail
 value=''.join(parts);check=v.verify_text(source,value,r['locale']);assert not check['errors'],(r['resourceId'],r['locale'],check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']};rr.update(sourceValue=source,value=value,marketId=None,reason='Reconstruct complete current-source body and chart; remove malformed translated HTML and duplicate translated-only chart, retaining reviewed equivalent prose with listed corrections.',independentReview='FULL_AUTHOR_MEANING_REVIEW_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'sourcePreservation':check,'meaning':'FULL_AUTHOR_REVIEW_PASS','priorMalformedChart':'REPLACED_WITH_EXACT_SOURCE_HTML_AND_FACTS','corrections':changes,'sourceSHA256':hashlib.sha256(source.encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest()})
assert len(out)==15
for name,data in [('held_old15_candidate.json',{'rows':out}),('held_old15_checks.json',{'fields':checks,'limit':'Offline candidate. Root independently reviews and performs current source/before and live guards.'})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(out),'preservationFailures':0}))
