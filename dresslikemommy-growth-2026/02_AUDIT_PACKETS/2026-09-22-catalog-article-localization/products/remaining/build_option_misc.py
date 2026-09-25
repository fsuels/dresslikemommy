#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
HERE=pathlib.Path(__file__).resolve().parent
PRODUCTS=HERE.parent
sys.path.insert(0,str(PRODUCTS.parent/'tooling'))
import offline_translation as ot
base=json.loads((HERE/'baseline.json').read_text())['rows']
lex=json.loads((PRODUCTS/'option_dictionary.json').read_text())
manual=json.loads((HERE/'option_misc_values.json').read_text())
rows=[];nochange=[]
for r in base:
    if r['key']!='name':continue
    s=r['source'];locale=r['locale'];value=None
    if locale=='sv' and s in manual['noChangeSwedish']:
        nochange.append({**r,'disposition':'SEMANTICALLY_CORRECT_NO_COPY_CHANGE','reason':manual['reasonNoChange']})
        continue
    if s=='Size':value=lex[locale]['Size']
    if locale=='sv':
        value=manual['sv'].get(s,value)
        role=re.fullmatch(r'(Child|Girl|Boy|Baby|Mother|Father|Mom)\s+(.+)',s)
        if role and s!='Boy Shorts':
            roles={'Child':'Barn','Girl':'Flicka','Boy':'Pojke','Baby':'Bebis','Mother':'Mamma','Father':'Pappa','Mom':'Mamma'}
            ending=role[2]
            age=re.fullmatch(r'(\d+\s*(?:-\s*\d+)?)\s+([Yy]ears?|[Mm]onths?)',ending)
            if age:
                span=re.sub(r'\s+','',age[1]);unit='år' if age[2].lower().startswith('year') else 'månad' if span=='1' else 'månader'
                value=roles[role[1]]+' '+span+' '+unit
            elif re.fullmatch(r'(?:\d+(?:-\d+)?T|[2-5]?XL|XXL|XS|[SML](?:-XL)?)',ending):value=roles[role[1]]+' '+ending
    version=re.fullmatch(r'([SML]) \(Adult (Normal|Extended) (?:Version|Edition)\)',s)
    if version and locale in ('ru','sv'):
        label={'ru':{'Normal':'стандартная версия для взрослых','Extended':'удлинённая версия для взрослых'},'sv':{'Normal':'standardmodell för vuxna','Extended':'förlängd modell för vuxna'}}[locale][version[2]]
        value=version[1]+' ('+label+')'
    if value is None:continue
    assert re.findall(r'\d+',s)==re.findall(r'\d+',value)
    rows.append({**r,'value':value,'method':'manual_option_lexicon_preserving_all_size_and_age_codes','marketId':None})
f=HERE/'option_misc_candidate.json';f.write_text(json.dumps({'status':'PENDING_PARENT_INDEPENDENT_REVIEW','rows':rows},ensure_ascii=False,indent=2)+'\n')
rep=ot.verify_rows(rows,base);(HERE/'option_misc_structure.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
(HERE/'option_misc_no_change.json').write_text(json.dumps({'rows':nochange},ensure_ascii=False,indent=2)+'\n')
(HERE/'option_misc_rollback.json').write_text(json.dumps([{'resourceId':r['resourceId'],'locale':r['locale'],'key':r['key'],'action':'restore' if r['before'] else 'remove','value':r['before']['value'] if r['before'] else None,'marketId':None} for r in rows],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'noChange':len(nochange),'structuralFailures':rep['failedRows'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}))
