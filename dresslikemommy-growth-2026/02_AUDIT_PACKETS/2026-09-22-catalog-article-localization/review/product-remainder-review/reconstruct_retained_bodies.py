from pathlib import Path
import hashlib, importlib.util, json, re
P=Path(__file__).resolve().parent;R=P.parent.parent
rows=[r for r in json.loads((P/'retained96_worklist.json').read_text())['rows'] if r['key']=='body_html']
spec=importlib.util.spec_from_file_location('v',R/'tooling/offline_translation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
roles={
'cs':['Otec','Matka','Chlapec','Dívka','Dítě','let'],
'da':['Far','Mor','Dreng','Pige','Barn','år'],
'de':['Vater','Mutter','Junge','Mädchen','Kind','Jahre'],
'el':['Πατέρας','Μητέρα','Αγόρι','Κορίτσι','Παιδί','ετών'],
'es':['Padre','Madre','Niño','Niña','Niño/a','años'],
'fi':['Isä','Äiti','Poika','Tyttö','Lapsi','vuotta'],
'fr':['Père','Mère','Garçon','Fille','Enfant','ans'],
'he':['אבא','אמא','ילד','ילדה','ילד/ה','שנים'],
'hi':['पिता','माँ','लड़का','लड़की','बच्चा','वर्ष'],
'ko':['아빠','엄마','남아','여아','어린이','세'],
'no':['Far','Mor','Gutt','Jente','Barn','år'],
'pt-BR':['Pai','Mãe','Menino','Menina','Criança','anos'],
'ro':['Tată','Mamă','Băiat','Fată','Copil','ani'],
}
overrides=[
('cs','Vyrobeno z lehké a prodyšné látky, tyto sladěné outfity jsou ideální pro udržení chladu a zároveň elegantní vzhled.','Tyto sladěné outfity jsou vyrobené z lehké a prodyšné látky a pomohou vám zůstat v chladu a zároveň vypadat elegantně.'),
('cs','bílé trička','bílá trička'),
('da','De kvindelige og pigernes lyse gule lagdelte maxikjoler','Kvindernes og pigernes klare gule maxikjoler med lag'),
('fi','Valmistettu kevyestä ja hengittävästä kankaasta, nämä yhteensopivat asut pitävät sinut viileänä ja tyylikkäänä.','Kevyestä ja hengittävästä kankaasta valmistetut yhteensopivat asut pitävät sinut viileänä ja tyylikkäänä.'),
('cs','Vyrobeno z lehké, prodyšné látky, tyto outfity jsou ideální pro dny na pláži, rodinné fotografie a zábavné letní výlety.','Tyto outfity jsou vyrobené z lehké, prodyšné látky a jsou ideální pro dny na pláži, rodinné fotografie a zábavné letní výlety.'),
('da','flydende kjoler','let faldende kjoler'),('da','Flydende kjoler','Let faldende kjoler'),
('da','Blød, behagelig pasform med nemme at have på-stilarter til både voksne og børn','Blød og behagelig pasform med modeller, der er lette at tage på, til både voksne og børn'),
('fi','virtaavat mekot','kauniisti laskeutuvat mekot'),('fi','Virtaavat mekot','Kauniisti laskeutuvat mekot'),
('fi','Valmistettu kevyestä, hengittävästä kankaasta, nämä asut sopivat täydellisesti rantapäiviin, perhekuvauksiin ja hauskoihin kesäretkiin.','Kevyestä, hengittävästä kankaasta valmistetut asut sopivat täydellisesti rantapäiviin, perhekuvauksiin ja hauskoihin kesäretkiin.'),
('fr','Confortables et élégantes, ces tenues assorties rendront chaque instant de vos vacances encore plus précieux.','Avec leur coupe confortable et leur design accrocheur, ces tenues assorties rendront chaque instant de vos vacances encore plus précieux.'),
('he','שמלות זרימה','שמלות נשפכות'),('he','שמלת זרימה','שמלות נשפכות'),
('he','עשויים מבד קל ונושם, התלבושות מושלמות','התלבושות עשויות מבד קל ונושם ומושלמות'),
('no','flytende kjoler','lett fallende kjoler'),('no','Flytende kjoler','Lett fallende kjoler'),
('no','lettbrukte stiler','modeller som er enkle å ta på'),
('cs','Vyrobeno z lehké a prodyšné látky, tyto šaty zajistí, že vy i vaše malá zůstanete v teplých dnech chladní a pohodlní.','Tyto šaty jsou vyrobené z lehké a prodyšné látky, takže vám i vaší holčičce bude v teplých dnech příjemně a nebudete se přehřívat.'),
('cs','Měkký modrý a krémový květovaný vzor','Jemný modro-krémový květinový potisk'),
('da','flydende nederdel','let faldende nederdel'),
('da','Blødt blå og creme blomsterprint','Blomsterprint i bløde blå og cremefarvede toner'),
('da','Pufærmer tilføjer et strejf','Korte pufærmer tilføjer et strejf'),
('fi','Resoripintainen yläosa','Smokkirypytetty yläosa'),
('fi','sininen ja kerma kukkakuosi','sininen ja kermanvärinen kukkakuosi'),
('fi','Pehmeä sininen ja kermanvärinen kukkakuosi','Hennon sininen ja kermanvärinen kukkakuosi'),
('fi','Pussihihat lisäävät','Lyhyet pussihihat lisäävät'),('fi','pussihihat lisäävät','lyhyet pussihihat lisäävät'),
('he','שמלות כתף חשופות','שמלות עם כתפיים חשופות'),('he','שמלת כתף חשופה','שמלה עם כתפיים חשופות'),
('he','החלק העליון עם גומי','החלק העליון המכווץ בתפירת גומי'),('he','חלק עליון עם גומי','חלק עליון מכווץ בתפירת גומי'),
('he','הדפס פרחים רך','הדפס פרחים עדין'),
('hi','फुला हुआ छोटा आस्तीन','फूली हुई छोटी आस्तीनें'),
('hi','आस्तीनें एक आकर्षक, विंटेज प्रेरित स्पर्श जोड़ता है','आस्तीनें एक आकर्षक, विंटेज प्रेरित स्पर्श जोड़ती हैं'),
('hi','आस्तीनें आकर्षण और शालीनता का स्पर्श जोड़ता है','आस्तीनें आकर्षण और शालीनता का स्पर्श जोड़ती हैं'),
('hi','नरम नीला और क्रीम फूलों का प्रिंट','हल्के नीले और क्रीम रंग का फूलों वाला प्रिंट'),
('ko','편안하고 날씬해 보이는 핏','편안하고 아름다운 실루엣'),
('no','det flytende skjørtet','det lett fallende skjørtet'),('no','flytende skjørt','lett fallende skjørt'),
('no','Klær lengde','Plaggets lengde'),('da','Tøj længde','Tøjlængde'),
('ro','Corsetul cu elastic','Partea superioară încrețită cu elastic'),('ro','Corset cu elastic','Parte superioară încrețită cu elastic'),
('fi','Olkapään leveys','Hartialeveys'),
('pt-BR','eventos ao ar livre','eventos em espaços abertos'),
]
def textparts(s):return [(i,x) for i,x in enumerate(re.split('(<[^>]*>)',s)) if x.strip() and not x.startswith('<')]
def role_label(s,locale):
 m=re.fullmatch(r'(Father|Mother|Boy|Girl|Child)\s+(.+)',s)
 if not m:return None
 label=roles[locale][['Father','Mother','Boy','Girl','Child'].index(m[1])];tail=m[2]
 age=re.fullmatch(r'(\d+(?:-\d+)?) [Yy]ears?',tail)
 if age:
  n=age[1];suffix=roles[locale][5]
  if locale=='he':return label+' '+n+' '+('שנה' if n=='1' else 'שנים')
  if locale=='ko':return label+' '+n+'세'
  if n=='1':suffix={'cs':'rok','fi':'vuosi','fr':'an','pt-BR':'ano','ro':'an','es':'año'}.get(locale,suffix)
  if locale=='cs' and n in ['2','3','4']:suffix='roky'
  return label+' '+n+' '+suffix
 return label+' '+tail
out=[];checks=[]
for r in rows:
 source=r['source'];before=r['before']['value'];parts=re.split('(<[^>]*>)',source);s=textparts(source);t=textparts(before);assert len(s)==len(t)
 changes=[]
 for (i,ss),(_,tt) in zip(s,t):
  original=ss.strip();value=tt.strip();role=role_label(original,r['locale'])
  numeric=re.sub(r'\b(?:cm|in|kg|lbs|approx)\b','',original)
  if re.fullmatch(r'[\d\s.,/()+\-–—]+',numeric):
   approximate={'cs':'přibližně','da':'ca.','de':'ca.','el':'περίπου','es':'aprox.','fi':'noin','fr':'env.','he':'בקירוב','hi':'लगभग','ko':'약','no':'ca.','pt-BR':'aprox.','ro':'aprox.'}
   value=original.replace('approx',approximate[r['locale']])
  elif role is not None:value=role
  elif re.search(r'\((?:cm|kg)\s*/\s*(?:in|lbs)\)',original):
   suffix=re.search(r'\((?:cm|kg)\s*/\s*(?:in|lbs)\)',original)[0]
   value=re.sub(r'\([^)]*\)',suffix,value)
  if original.startswith('Hip (') and r['locale']=='he':value='היקף אגן (cm/in)'
  for locale,old,new in overrides:
   if r['locale']==locale:value=value.replace(old,new)
  if value!=tt.strip():changes.append({'source':original,'beforeText':tt.strip(),'valueText':value})
  lead=ss[:len(ss)-len(ss.lstrip())];trail=ss[len(ss.rstrip()):];parts[i]=lead+value+trail
 value=''.join(parts);check=v.verify_text(source,value,r['locale'])
 if check['errors']:
  (P/'retained_body_debug.json').write_text(json.dumps({'source':source,'value':value,'locale':r['locale'],'checks':check},ensure_ascii=False,indent=2))
 assert not check['errors'],(r['resourceId'],r['locale'],check)
 rr={k:r[k] for k in ['resourceId','productId','locale','key','sourceDigest','before','rawFile']};rr.update(sourceValue=source,value=value,marketId=None,reason='Reconstruct full current-source HTML/images and numeric cells, preserving reviewed localized prose and correcting listed meaning/grammar defects; replace stale inherited markup and untranslated labels.',independentReview='AUTHOR_FULL_MEANING_REVIEW_PENDING_ROOT_INDEPENDENT_REVIEW')
 out.append(rr);checks.append({'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'meaning':'FULL_PROSE_AND_LABEL_AUTHOR_REVIEW_PASS','sourceTextNodes':len(s),'preservation':check,'changes':changes,'sourceSHA256':hashlib.sha256(source.encode()).hexdigest(),'beforeSHA256':hashlib.sha256(before.encode()).hexdigest(),'valueSHA256':hashlib.sha256(value.encode()).hexdigest()})
assert len(out)==24
for name,data in [('retained_body24_candidate.json',{'rows':out}),('retained_body24_checks.json',{'fields':checks,'method':'Exact original source HTML template with all aligned nonempty localized text nodes individually reviewed; numeric cells/role labels rebuilt from source; English source facts remain unchanged.','limits':'Offline evidence only; root independent review and live source/before guards required.'})]:(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':24,'structuralFailures':0,'textCorrections':sum(len(x['changes']) for x in checks)}))
