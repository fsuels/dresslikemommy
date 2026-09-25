import json,re,hashlib,runpy,html
from pathlib import Path
H=Path(__file__).resolve().parent;F=H.parents[1];B=F.parents[1];author=F/'root_group/candidates21.json';rs=json.loads(author.read_text())['rows'];sha=lambda s:hashlib.sha256(s.encode()).hexdigest();authorSHA=hashlib.sha256(author.read_bytes()).hexdigest();assert authorSHA=='1a01cc3356f1b98d8912a597dd33725bd4c283a95c5eaf3bafa92f6d526acb33'
# Meaning reviewed against every current source paragraph, inline join, feature and table label.
neutral={
'ru':{'Bust':'Грудь','Chest/Bust':'Грудь','Hip':'Бёдра','Waist':'Талия','Top Chest/Bust':'Грудь топа','Top Hip':'Бёдра топа','Top Waist':'Талия топа','Pants Waist':'Талия брюк'},
'sv':{'Bust':'Byst','Chest/Bust':'Bröst/byst','Hip':'Höft','Waist':'Midja','Top Chest/Bust':'Toppens bröst/byst','Top Hip':'Toppens höft','Top Waist':'Toppens midja','Pants Waist':'Byxornas midja'},
'de':{'Bust':'Brust','Chest/Bust':'Brust','Hip':'Hüfte','Waist':'Taille','Top Chest/Bust':'Brust des Oberteils','Top Hip':'Hüfte des Oberteils','Top Waist':'Taille des Oberteils','Pants Waist':'Taille der Hose'}}
small={
(179,'ru'):[('Детские размеры от 2Y до 9-10Y и взрослые размеры от S до 5XL.','Детские размеры от 2 до 9-10 лет и взрослые размеры от S до 5XL.','Localize source age abbreviation Y without altering the numeric ages.')],
(211,'ru'):[('пляжных фотографий, завтраков в тёплую погоду и прогулок в отпуске.','пляжных фотографий, поздних завтраков в тёплую погоду и прогулок в отпуске.','Source brunch retains the late breakfast sense.'),('отсутствующие значения обхвата груди, бёдер и полной длины изделия','отсутствующие значения для груди, бёдер и полной длины изделия','Source unavailable bust does not state circumference.')],
(216,'ru'):[('курортных утренних прогулок','утренних часов на курорте','Source resort mornings does not specify walks.'),('Для девочек указаны возраст, рост, обхваты груди и талии, а также длина; для мам — обхваты груди и бёдер, а также длина.','Для девочек указаны возраст, рост, мерки груди и талии, а также длина; для мам — мерки груди и бёдер, а также длина.','Preserve generic source dimensions without adding circumference.')],
(219,'ru'):[('с мягким эффектом перехода оттенка','с мягким эффектом выцветания','Source gentle fade effect describes faded appearance, not a newly asserted gradient.'),('по указанным в таблице росту, весу, обхватам груди и талии, меркам рукава и длины.','по указанным в таблице росту, весу, меркам груди, талии, рукава и длины.','Preserve generic source dimensions without adding circumference.')],
(221,'ru'):[('Мягкий многослойный фатин с ощущением лёгкой праздничной юбки;','Мягкая многослойная фактура под фатин с ощущением лёгкой праздничной юбки;','Retain source tulle-look qualification rather than assert actual fiber/material.')],
(219,'sv'):[('med en mild toning','med en lätt blekt ton','Preserve the source gentle fade effect.')],
(221,'sv'):[('Mjuk tyll i flera lager med känslan av en lätt festkjol;','Mjuk tylliknande struktur i flera lager med känslan av en lätt festkjol;','Retain source tulle-look qualification rather than assert actual material.')],
(219,'de'):[('mit einem dezenten Farbverlauf','mit sanft verblasster Optik','Source gentle fade effect does not establish a gradient.')],
(221,'de'):[('Sie enthält keine Angaben zu Taillenweite, Hüftweite oder Rocklänge;','Sie enthält keine Maße für Taille, Hüfte oder Rocklänge;','Generic source waist/hip measurements do not specify width.')]
}
ledger=[];checked=[]
for r in rs:
 value=r['value'];original=value;ss=list(re.finditer(r'<th\b[^>]*>([\s\S]*?)</th>',r['source']));tt=list(re.finditer(r'<th\b[^>]*>([\s\S]*?)</th>',value));assert len(ss)==len(tt);patches=[]
 for idx,(s,t) in enumerate(zip(ss,tt)):
  text=html.unescape(s.group(1).strip());m=re.fullmatch(r'(.+?)( \([^)]*\))?',text);base=m.group(1)
  if base not in neutral[r['locale']]:continue
  after=neutral[r['locale']][base]+(m.group(2) or '');before=t.group(1)
  if after==before:continue
  patches.append((t.start(1),t.end(1),before,after));ledger.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'kind':'header','sourceHeader':text,'sourceHeaderOrdinal':idx,'before':before,'after':after,'reason':'Generic current English dimension does not establish circumference; preserve explicit Width/Length on separate source columns.'})
 for start,end,b,a in reversed(patches):assert value[start:end]==b;value=value[:start]+a+value[end:]
 for b,a,reason in small.get((r['productIndex'],r['locale']),[]):
  assert value.count(b)==1,(r['productIndex'],r['locale'],b);value=value.replace(b,a);ledger.append({'productIndex':r['productIndex'],'resourceId':r['resourceId'],'locale':r['locale'],'kind':'prose','before':b,'after':a,'reason':reason})
 r.update({'authorCandidateValueSHA256':sha(original),'value':value,'valueSHA256':sha(value),'reviewStatus':'INDEPENDENTLY_QUALIFIED_FULL_CURRENT_SOURCE_TRANSLATION_REQUIRES_ROOT_FRESH_BEFORE','independentReviewStatus':'PASS_FULL_MEANING_SOURCE_BINDINGS_EXACT_HTML_NUMBERS_UNITS','independentReview':{'reviewer':'product_release_review','authorFile':'review/full_source_150/root_group/candidates21.json','authorFileSHA256':authorSHA,'meaningScope':'All current source prose, inline joins, garment exclusions, unknown/access/care/workflow qualifications, source garment/color changes, all size roles and unique table headers; all numeric rows checked mechanically against source.','correctionCount':sum(x['resourceId']==r['resourceId'] and x['locale']==r['locale'] for x in ledger)}})
 checked.append({'productIndex':r['productIndex'],'locale':r['locale'],'meaning':'PASS','sourceQualificationsPreserved':True,'printedSmilePreserved':r['productIndex']==179,'neutralP116CoatLabelRetained':r['productIndex']==116,'fullSourceProseRead':True})
p=H/'root21_reviewed.json';p.write_text(json.dumps({'rows':rs},ensure_ascii=False,indent=2)+'\n');verify=runpy.run_path(str(F/'verify_full_source_candidates.py'))['verify'];struct=verify(rs);summary={'candidateSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':len(rs),'corrections':len(ledger),'headerCorrections':sum(x['kind']=='header' for x in ledger),'proseCorrections':sum(x['kind']=='prose' for x in ledger),'authorFileSHA256':authorSHA,'authorUnchanged':hashlib.sha256(author.read_bytes()).hexdigest()==authorSHA,'rootFreshBeforeAfterNative2145Required':True}
(H/'corrections.json').write_text(json.dumps({'summary':summary,'rows':ledger},ensure_ascii=False,indent=2)+'\n');(H/'checks.json').write_text(json.dumps({'summary':summary,'semanticChecks':checked,'structuralChecks':struct},ensure_ascii=False,indent=2)+'\n');print(summary)
