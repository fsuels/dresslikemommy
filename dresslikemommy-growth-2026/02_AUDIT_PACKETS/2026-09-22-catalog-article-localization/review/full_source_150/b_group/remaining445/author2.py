import json, re, html, hashlib
from pathlib import Path
from html.parser import HTMLParser

H = Path(__file__).resolve().parent
B = H.parents[3]
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
pid = 'gid://shopify/Product/7229128441953'
historical = json.loads((B/'review/article-title-independent/product_source_disposition846.json').read_text())['rows']
work = [r for r in historical if r['resourceId'] == pid and r['key'] == 'body_html']
assert len(work) == 2 and {r['locale'] for r in work} == {'ru', 'sv'}
source = work[0]['source']
prose_source = [html.unescape(x.strip()) for x in re.findall(r'>([^<>]*)<', re.sub(r'<table\b[\s\S]*?</table>', '', source)) if x.strip()]
TEXT = {
'ru': [
'Ткань:',
'Мягкая, дышащая хлопковая смесь, гладкая на ощупь и легко растягивающаяся — для прогулок в тёплую погоду, игр во дворе и семейных фотосессий на весь послеобеденный период.',
'Семейная история:',
'Радужный комплект для четырёх семейных ролей — мама и девочки в жизнерадостных жёлтых полукомбинезонах поверх футболок в радужную полоску, папа и мальчики в сочетающихся жёлтых шортах с такими же футболками. Каждый член семьи — в едином согласованном образе.',
'Рисунок:',
'Яркие радужные полосы — выразительные горизонтальные полосы красного, оранжевого, жёлтого, зелёного, синего и фиолетового цветов на белой футболке в сочетании с солнечно-жёлтой нижней частью наряда.',
'Дизайн:',
'Выберите',
'футболку',
'в радужную полоску для каждого (круглый вырез, короткие рукава, свободная посадка) и сочетайте её с',
'жёлтым полукомбинезоном',
'(для мамы и девочек — регулируемые бретели, застёжка на пуговицы, нагрудный карман) или',
'жёлтыми шортами',
'(для папы и мальчиков — эластичный пояс, удобная длина до середины бедра).',
'Уход:',
'Машинная стирка в холодной воде с вещами похожих цветов, деликатный режим. Сушите в сушильной машине при низкой температуре или развесьте для сушки. При необходимости гладьте при низкой температуре. Не отбеливать.',
'Размерный ряд:',
'Мальчики 2–14 лет · Девочки 2–14 лет · Мама S–2XL · Папа M–3XL — точные измерения ниже.',
'Таблица размеров — нижняя часть наряда (полукомбинезон и шорты)',
'Таблица размеров — футболка (для всех)',
'Vibrant Rainbow объединяет всех членов семьи в одном кадре — яркие радужные полосы на груди, солнечно-жёлтые полукомбинезоны или шорты и единая тканевая тема для всей семьи. Мама и девочки кружатся в полукомбинезонах с регулируемыми бретелями, папа и мальчики сохраняют прохладу в шортах без застёжки, а всех объединяет одна и та же весёлая радужная футболка.',
'Возьмите комплект для солнечных дней в парке, поездок на пляж, поздних завтраков в выходные и фотографий на день рождения. Хлопковая смесь помогает детям чувствовать себя комфортно во время долгих часов подвижных игр и чётко выглядит на фотографиях при любом освещении. Сочетайте вещи по размеру — добавьте варианты для братьев, сестёр, двоюродных братьев и сестёр или бабушек и дедушек — и оденьте всю семью для одного яркого радужного момента.',
'Основные особенности:',
'Сочетающиеся образы для четырёх семейных ролей:',
'Одна радужная футболка для всех, а также жёлтые полукомбинезоны для мамы и девочек и жёлтые шорты для папы и мальчиков.',
'Регулируемые полукомбинезоны:',
'Регулируемые бретели позволяют дольше сохранять подходящую посадку; застёжка на пуговицы и нагрудный карман.',
'Шорты с эластичным поясом:',
'Удобные шорты без застёжки для папы и мальчиков, длиной до середины бедра, без лишних хлопот.',
'Мягкая хлопковая смесь:',
'Дышащая, эластичная и простая в стирке — подойдёт и для дней в парке, и для семейных фотосессий.',
'Палитра для фотографий:',
'Выразительные радужные полосы на фоне солнечно-жёлтого — чётко смотрятся в кадре при любом освещении.',
'Примечание о больших детских размерах: фабрика публикует измерения до размера «Ребёнок 9–10 лет» (≈150 cm). Для детских размеров 10–12, 11–12, 12–14 и 13–14 мы рекомендуем следующий размер после самого большого опубликованного в таблице — и будем рады обменять товар или вернуть деньги, если размер не подойдёт.',
'Оденьте всю семью в Vibrant Rainbow и превратите каждый выход в повод для фотографии — во дворе, на пляже, за поздним завтраком или на дне рождения — в радостных сочетающихся радужных нарядах.'
],
'sv': [
'Tyg:',
'Mjuk bomullsblandning som andas, med slät känsla och följsam stretch — för utflykter i varmt väder, lek i trädgården och familjefotograferingar som varar hela eftermiddagen.',
'Familjetema:',
'Ett regnbågsset för fyra familjeroller — mamma och flickorna i glada gula hängselbyxor över en regnbågsrandig t-shirt, pappa och pojkarna i matchande gula shorts med samma t-shirt. Varje familjemedlem får en samordnad look.',
'Mönster:',
'Livfulla regnbågsränder — tydliga vågräta band i rött, orange, gult, grönt, blått och violett på en rent vit t-shirt, tillsammans med solgula underdelar.',
'Design:',
'Välj den regnbågsrandiga',
't-shirten',
'till alla (rund halsringning, kort ärm, ledig passform) och kombinera den med',
'gula hängselbyxor',
'(mamma och flickor — justerbara axelband, knappstängning, bröstficka framtill) eller',
'gula shorts',
'(pappa och pojkar — resår i midjan, bekväm längd till mitten av låret).',
'Skötsel:',
'Maskintvätta kallt med liknande färger på skonsamt program. Torktumla på låg värme eller hängtorka. Stryk på låg värme vid behov. Använd inte blekmedel.',
'Storleksintervall:',
'Pojkar 2–14 år · Flickor 2–14 år · Mamma S–2XL · Pappa M–3XL — exakta mått nedan.',
'Storlekstabell — underdelar (hängselbyxor och shorts)',
'Storlekstabell — t-shirt (alla)',
'Vibrant Rainbow samlar varje familjemedlem i samma bild — klara regnbågsränder över bröstet, solgula hängselbyxor eller shorts nedtill och ett gemensamt tygtema för hela familjen. Mamma och flickorna snurrar runt i hängselbyxor med justerbara axelband, pappa och pojkarna håller sig svala i shorts som enkelt dras på, och alla har samma glada regnbågs-t-shirt.',
'Packa med setet för soliga parkdagar, strandutflykter, helgbruncher och födelsedagsbilder. Bomullsblandningen håller barnen bekväma under timmars spring och lek och framträder tydligt på bild i alla ljus. Kombinera efter storlek — lägg till fler plagg till syskon, kusiner eller mor- och farföräldrar — och klä hela familjen för ett regnbågsfärgat ögonblick.',
'Viktiga egenskaper:',
'Matchning för fyra familjeroller:',
'En regnbågs-t-shirt till alla, plus gula hängselbyxor till mamma och flickorna och gula shorts till pappa och pojkarna.',
'Justerbara hängselbyxor:',
'Axelbanden kan justeras så att plagget passar längre; knappstängning och bröstficka framtill.',
'Shorts med resår i midjan:',
'Bekväma shorts som enkelt dras på för pappa och pojkarna, med längd till mitten av låret, utan krångel.',
'Mjuk bomullsblandning:',
'Andas, är stretchig och lätt att tvätta — redo för både parkdagar och familjefotograferingar.',
'Palett som passar på bild:',
'Tydliga regnbågsränder mot solgult — framträder klart på bild i alla ljus.',
'Observera om större barnstorlekar: fabriken publicerar mått upp till Barn 9–10 år (≈150 cm). För Barn 10–12, 11–12, 12–14 och 13–14 rekommenderar vi nästa storlek över den största publicerade raden — och vi hjälper gärna till med byte eller återbetalning om passformen inte blir rätt.',
'Klä hela familjen i Vibrant Rainbow och gör varje utflykt till ett fototillfälle — i trädgården, på stranden, vid brunchen eller på födelsedagen — med matchande regnbågsglädje.'
]}
HEADERS = {
'ru': {'Size':'Размер','Age':'Возраст','Weight':'Вес','Height':'Рост','Waist':'Талия','Hip':'Бёдра','Pants Length':'Длина брюк','Chest/Bust':'Грудь','Shoulder':'Плечо','Sleeve':'Рукав','Garment Length':'Длина изделия'},
'sv': {'Size':'Storlek','Age':'Ålder','Weight':'Vikt','Height':'Kroppslängd','Waist':'Midja','Hip':'Höft','Pants Length':'Byxlängd','Chest/Bust':'Bröst/byst','Shoulder':'Axel','Sleeve':'Ärm','Garment Length':'Plagglängd'}}

def role(s,l):
    m = re.fullmatch(r'(Boy|Girl) (\d+(?:-\d+)?) years / (Short|Overall|T-shirt)',s)
    if m:
        sex,age,item=m.groups()
        if l=='ru':
            n=int(age.split('-')[-1]);unit='года' if n in [2,3,4] else 'лет'
            return {'Boy':'Мальчик','Girl':'Девочка'}[sex]+' '+age+' '+unit+' / '+{'Short':'шорты','Overall':'полукомбинезон','T-shirt':'футболка'}[item]
        return {'Boy':'Pojke','Girl':'Flicka'}[sex]+' '+age+' år / '+{'Short':'shorts','Overall':'hängselbyxor','T-shirt':'t-shirt'}[item]
    m=re.fullmatch(r'(Mother|Father)( +)([\dA-Z]+) / (Short|Overall|T-shirt)',s)
    if m:
        who,space,size,item=m.groups()
        names={'ru':{'Mother':'Мама','Father':'Папа'},'sv':{'Mother':'Mamma','Father':'Pappa'}}
        items={'ru':{'Short':'шорты','Overall':'полукомбинезон','T-shirt':'футболка'},'sv':{'Short':'shorts','Overall':'hängselbyxor','T-shirt':'t-shirt'}}
        return names[l][who]+space+size+' / '+items[l][item]

rawrows=json.loads((B/'review/body-structure-audit/effective_body_inventory.json').read_text())['rows']
R={(r['resourceId'],r['locale']):r for r in rawrows if r['resourceId']==pid and r['locale'] in ['ru','sv']}
effective={k:(r['expectedEffectiveBeforeValue'],[]) for k,r in R.items()}
files=['review/article-title-independent/body_structure375_reviewed.json','review/body-header-localization/header_candidates_root_reviewed.json','review/size-label-repair/candidate_root_reviewed156.json','review/size-label-repair/placeholder-review/placeholder88_root_bound.json','review/body-header-localization/prose-completion-review/prose_completion11_root_bound.json','review/native-header-final/current22_root_reviewed.json','review/native-header-semantics-independent/full7/full7_reviewed.json','review/native-header-semantics-independent/native_header2145_reviewed.json']
for f in files:
    p=B/f
    for r in json.loads(p.read_text())['rows']:
        k=r['resourceId'],r['locale']
        if k in effective:
            _,dep=effective[k];effective[k]=(r['value'],dep+[{'file':f,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'valueSHA256':sha(r['value'])}])
class Audit(HTMLParser):
    def __init__(self,s):super().__init__(convert_charrefs=False);self.events=[];self.feed(s)
    def handle_starttag(self,t,a):self.events.append(('start',t,a,self.get_starttag_text()))
    def handle_startendtag(self,t,a):self.events.append(('startend',t,a,self.get_starttag_text()))
    def handle_endtag(self,t):self.events.append(('end',t))
    def handle_comment(self,s):self.events.append(('comment',s))
num=lambda s:re.findall(r'\d+(?:\.\d+)?',s)
out=[];pairs=[];checks=[]
for w in work:
    l=w['locale'];rr=R[(pid,l)];assert rr['source']==source==w['source'];assert w['sourceDigest']==sha(source)
    assert len(prose_source)==len(TEXT[l]),(len(prose_source),len(TEXT[l]))
    mp=dict(zip(prose_source,TEXT[l]));parts=re.split(r'(<[^>]*>)',source);valueparts=list(parts);intable=False;cell=None;ledger=[]
    for i,s in enumerate(parts):
        if s.startswith('<table'):intable=True
        elif s.startswith('</table'):intable=False
        elif re.match(r'<(th|td)(?:\s|>)',s):cell=re.match(r'<(th|td)',s).group(1)
        elif s in ['</th>','</td>']:cell=None
        elif not s.startswith('<') and s.strip():
            text=html.unescape(s.strip())
            if not intable:target=mp[text];kind='prose'
            elif cell=='th':
                m=re.fullmatch(r'(.+?)( \([^)]*\))?',text);target=HEADERS[l][m[1]]+(m[2] or '');kind='th'
            elif cell=='td':
                target=role(text,l) or text;kind='td'
                if target==text:assert not re.search('[A-Za-z]',re.sub(r'\b(?:cm|in|kg|lbs)\b','',text)),text
            else:raise AssertionError((i,s))
            valueparts[i]=s[:len(s)-len(s.lstrip())]+html.escape(target,quote=False)+s[len(s.rstrip()):]
            ledger.append({'partIndex':i,'kind':kind,'source':text,'target':target})
    value=''.join(valueparts)
    assert Audit(source).events==Audit(value).events
    assert num(source)==num(value)
    assert not re.search(r'QZXTOKEN|QZX|XTOKEN',value)
    for s,t in zip(re.findall(r'<td\b[^>]*>([\s\S]*?)</td>',source),re.findall(r'<td\b[^>]*>([\s\S]*?)</td>',value)):
        if not re.search(r'Boy|Girl|Mother|Father',s):assert s==t,(s,t)
    before,deps=effective[(pid,l)]
    row={z:rr[z] for z in ['productIndex','resourceId','locale','key','source','sourceDigest','sourceSHA256','rawBefore','rawFile','rawFileSHA256','onlineStoreUrl']}
    row.update({'sourceValue':source,'marketId':None,'before':None,'expectedEffectiveBeforeValue':before,'expectedEffectiveBeforeValueSHA256':sha(before),'beforeValueSHA256':sha(before),'expectedBeforeValueSHA256':sha(before),'value':value,'valueSHA256':sha(value),'plannedBeforeDependencies':deps,'requiresFreshEffectiveBeforeObject':True,'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'FULL_CURRENT_SOURCE_MANUAL_TRANSLATION_PENDING_ROOT_INDEPENDENT_REVIEW','reason':'Previously overbroad extrapolated_sizes hold: full current-source translation preserves published-through9–10 qualification, all larger-child blank measurements, qualified size-up advice and exact source numeric/unit/HTML structure.'})
    out.append(row);pairs.append({'resourceId':pid,'productIndex':rr['productIndex'],'locale':l,'nodes':ledger});checks.append({'locale':l,'sourceRawDigestBindings':True,'markupAttributesCommentsExact':True,'wholeSourceNumericSequenceExact':True,'allNumericMeasurementCellsExact':True,'allProseNodesTranslated':len(TEXT[l]),'genericDimensionsDoNotAddCircumferenceOrWidth':True,'unknownLargerChildMeasurementsRetainBlanks':True,'source9To10LimitAndQualifiedAdvicePreserved':True,'plannedBeforeDependencies':deps})
for name,data in [('candidates2.json',{'rows':out}),('node_pairs2.json',{'rows':pairs}),('checks2.json',{'rows':checks})]:(H/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print({'rows':len(out),'proseNodesPerLocale':len(prose_source),'candidateSHA256':hashlib.sha256((H/'candidates2.json').read_bytes()).hexdigest()})
