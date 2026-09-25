# -*- coding: utf-8 -*-
"""Source-unique measurement row matching; only erroneous first-cell labels change."""
import copy,hashlib,html,json,re,unicodedata
from collections import defaultdict,Counter
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
load=lambda p:json.loads(p.read_text())
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
fs=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dump=lambda name,d:(H/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
work=load(H/'classified1090_worklist.json')
assert fs(R/work['sourceInventoryFile'])==work['sourceInventorySHA256']
invfile=R/'review/body-structure-audit/effective_body_inventory.json'
inv={(r['resourceId'],r['locale']):r for r in load(invfile)['rows']}
sfile=R/'review/article-title-independent/body_structure375_reviewed.json'
hfile=R/'review/body-header-localization/header_candidates_v2.json'
assert fs(sfile)=='f8ae9d61b29a01f6628edf21cbf84421efd9c893f7d40f1e86c13538818ac501'
assert fs(hfile)=='30ac93375168fb7df4b2a355aed666a8e19c597e099ce98a2b42acca8e05c142'
structure={(r['resourceId'],r['locale']):r for r in load(sfile)['rows']}
headers={(r['resourceId'],r['locale']):r for r in load(hfile)['rows']}
corrections={(r['resourceId'],r['locale']):r for r in load(R/'review/article-title-independent/body_structure375_independent_corrections.json')['rows']}
plain=lambda s:html.unescape(re.sub(r'<[^>]*>','',s)).strip()
def nums(s):return tuple(x.replace(',','.') for x in re.findall(r'\d+(?:[.,]\d+)?',unicodedata.normalize('NFKC',s)))
def table_rows(value):
    result=[]
    for ti,table in enumerate(re.finditer(r'<table\b[^>]*>(.*?)</table>',value,re.S)):
        for ri,row in enumerate(re.finditer(r'<tr\b[^>]*>(.*?)</tr>',table[1],re.S)):
            cells=list(re.finditer(r'<(td|th)\b[^>]*>(.*?)</\1>',row[1],re.S))
            if len(cells)<2:continue
            texts=[plain(c[2]) for c in cells];signature=tuple(nums(c) for c in texts[1:])
            if sum(map(len,signature))<2:continue
            start=table.start(1)+row.start(1)+cells[0].start(2);end=table.start(1)+row.start(1)+cells[0].end(2)
            result.append({'tableIndex':ti,'rowIndex':ri,'label':texts[0],'labelHTML':cells[0][2],'labelStart':start,'labelEnd':end,'signature':signature,'nonLabelCellHTML':[c[0] for c in cells[1:]]})
    return result
stripheaders=lambda v:re.sub(r'(<th\b[^>]*>).*?(</th>)',r'\1\2',v,flags=re.S|re.I)
roles={
'ar':{'Mother':'الأم','Father':'الأب','Adult':'للكبار'},
'ja':{'Mother':'母','Father':'父','Adult':'大人'},
'hi':{'Mother':'माँ','Father':'पिता','Adult':'वयस्क'},
'ko':{'Mother':'엄마','Father':'아빠','Adult':'성인'},
'it':{'Mother':'Mamma','Father':'Papà','Adult':'Adulto'},
'nl':{'Mother':'Mama','Father':'Papa','Adult':'Volwassene'},
'pl':{'Mother':'Mama','Father':'Tata','Adult':'Dorosły'},
'pt-BR':{'Mother':'Mãe','Father':'Pai','Adult':'Adulto'},
'ru':{'Mother':'Мама','Father':'Папа','Adult':'Взрослый'}}
child={'ar':'طفل {age} سنوات','ja':'子ども {age}歳','hi':'बच्चा {age} वर्ष','ko':'아동 {age}세','it':'Bambino {age} anni','nl':'Kind {age} jaar','pl':'Dziecko {age} lat','pt-BR':'Criança de {age} anos','ru':'Ребёнок {age} лет'}
def localized_label(source,locale):
    src=source.replace('\u00a0',' ')
    match=re.fullmatch(r'(Mother|Father|Adult) (XXXL|XXL|XXS|XS|[2-6]XL|XL|S|M|L)',src)
    if match:return roles[locale][match[1]]+' '+match[2]
    match=re.fullmatch(r'Child (\d+(?:-\d+)?) [Yy]ears',src)
    assert match,src
    result=child[locale].format(age=match[1])
    if locale=='ar' and int(match[1].split('-')[-1])>=11:result=result.replace(' سنوات',' سنة')
    return result
groups=defaultdict(list)
for r in work['rows']:
    if not r['semanticClassification'].startswith('EQUIVALENT'):groups[(r['resourceId'],r['locale'])].append(r)
all_candidates=[];patches=[];checks=[];raw_cache={}
for key,findings in groups.items():
    original=inv[key];baseline=original['expectedEffectiveBeforeValue'];dependencies=[]
    sf=structure.get(key);hf=headers.get(key)
    if sf:
        assert sf['sourceDigest']==original['sourceDigest'] and sf['sourceValue']==original['source']
        baseline=sf['value'];dependencies.append({'file':str(sfile.relative_to(R)),'fileSHA256':fs(sfile),'valueSHA256':sha(baseline)})
    if hf:
        assert hf['sourceDigest']==original['sourceDigest']
        base_header=hf['expectedEffectiveBeforeValue'];after_header=hf['value']
        assert base_header==baseline,(key,'header baseline must be exact planned structural/current value')
        assert stripheaders(after_header)==stripheaders(baseline)
        baseline=after_header;dependencies.append({'file':str(hfile.relative_to(R)),'fileSHA256':fs(hfile),'authorValueSHA256':hf['valueSHA256'],'valueSHA256AfterRequiredIndependentAltEncoding':sha(baseline)})
    assert original['before']['outdated'] is False and original['before']==original['rawBefore']
    raw_path=R/original['rawFile'];assert fs(raw_path)==original['rawFileSHA256']
    if raw_path not in raw_cache:raw_cache[raw_path]=load(raw_path)
    node=next(n for n in raw_cache[raw_path]['data']['translatableResourcesByIds']['nodes'] if n['resourceId']==key[0])
    source=next(t for t in node['translatableContent'] if t['key']=='body_html')
    before=next(t for t in node['tr_'+key[1].replace('-','_')] if t['key']=='body_html')
    assert source['value']==original['source'] and source['digest']==original['sourceDigest'] and before==original['before']
    source_rows=table_rows(source['value']);target_rows=table_rows(baseline);source_index=defaultdict(list)
    for row in source_rows:source_index[row['signature']].append(row)
    target_index={(row['tableIndex'],row['rowIndex']):row for row in target_rows}
    replacements=[]
    for finding in findings:
        tr=target_index[(finding['targetRow']['tableIndex'],finding['targetRow']['rowIndex'])]
        assert tr['label']==finding['targetRow']['label'] and tr['labelHTML']==finding['targetRow']['labelHTML']
        assert tr['signature']==tuple(tuple(x) for x in finding['targetRow']['signature'])
        sr=source_index[tr['signature']];assert len(sr)==1;sr=sr[0]
        assert sr['label']==finding['sourceRow']['label']
        desired=localized_label(sr['label'],key[1]);assert desired!=tr['label']
        # All affected labels are plain text; markup preservation is exact.
        assert '<' not in tr['labelHTML'] and '>' not in tr['labelHTML']
        encoded=html.escape(desired,quote=False)
        rep={'reviewIndex':finding['reviewIndex'],'tableIndex':tr['tableIndex'],'rowIndex':tr['rowIndex'],'beforeLabel':tr['label'],'beforeLabelHTML':tr['labelHTML'],'afterLabel':desired,'afterLabelHTML':encoded,'labelStart':tr['labelStart'],'labelEnd':tr['labelEnd'],'sourceTableIndex':sr['tableIndex'],'sourceRowIndex':sr['rowIndex'],'sourceLabel':sr['label'],'sourceLabelHTML':sr['labelHTML'],'sourceUniqueNumericSignature':sr['signature'],'classification':finding['semanticClassification']}
        replacements.append(rep)
    value=baseline
    for rep in sorted(replacements,key=lambda x:x['labelStart'],reverse=True):
        assert value[rep['labelStart']:rep['labelEnd']]==rep['beforeLabelHTML']
        value=value[:rep['labelStart']]+rep['afterLabelHTML']+value[rep['labelEnd']:]
    final_rows=table_rows(value);assert len(final_rows)==len(target_rows)
    changed={(r['tableIndex'],r['rowIndex']):r for r in replacements}
    for first,last in zip(target_rows,final_rows):
        assert first['nonLabelCellHTML']==last['nonLabelCellHTML'] and first['signature']==last['signature']
        address=(first['tableIndex'],first['rowIndex'])
        assert last['labelHTML']==(changed[address]['afterLabelHTML'] if address in changed else first['labelHTML'])
    assert re.findall(r'<[^>]*>',baseline)==re.findall(r'<[^>]*>',value)
    # Reverse only the indexed replacement ranges from the finalized parse and require complete byte equality.
    back=value
    for row in reversed(final_rows):
        address=(row['tableIndex'],row['rowIndex'])
        if address in changed:back=back[:row['labelStart']]+changed[address]['beforeLabelHTML']+back[row['labelEnd']:]
    assert back==baseline
    candidate={'productIndex':original['productIndex'],'resourceId':key[0],'locale':key[1],'key':'body_html','marketId':None,'sourceValue':source['value'],'source':source['value'],'sourceDigest':source['digest'],'sourceSHA256':sha(source['value']),'rawFile':original['rawFile'],'rawFileSHA256':original['rawFileSHA256'],'rawBefore':before,'before':None if dependencies else before,'expectedEffectiveBeforeValue':baseline,'expectedEffectiveBeforeValueSHA256':sha(baseline),'expectedBeforeValueSHA256':sha(baseline),'beforeValueSHA256':sha(baseline),'value':value,'valueSHA256':sha(value),'plannedBeforeDependencies':dependencies,'requiresFreshEffectiveBeforeObject':bool(dependencies),'requiresFreshLiveSourceAndBeforeGuard':True,'reviewStatus':'AUTHOR_SOURCE_BOUND_SIZE_LABELS_PENDING_ROOT_REVIEW','reason':'Restore size letters or age/role labels from the only English row with the exact same numeric measurement-cell signature. All other bytes, all measurement cells, all headers and all HTML attributes preserved. Native equivalent size lettering retained elsewhere.','sizeLabelRepairs':replacements}
    all_candidates.append(candidate)
    patches.append({'productIndex':original['productIndex'],'resourceId':key[0],'locale':key[1],'sourceDigest':source['digest'],'plannedBeforeValueSHA256':sha(baseline),'valueSHA256':sha(value),'rows':replacements})
    checks.append({'productIndex':original['productIndex'],'resourceId':key[0],'locale':key[1],'labelsCorrected':len(replacements),'uniqueSourceMeasurementRows':'PASS','allMeasurementCellBytes':'PASS','allHTMLTagsAttributesHeaders':'PASS','allOtherBytesRoundTrip':'PASS','plannedStructuralHeaderAndAltEncodingBaseline':'PASS'})
assert len(all_candidates)==156 and sum(len(r['sizeLabelRepairs']) for r in all_candidates)==704
p51=[r for r in all_candidates if r['productIndex']==51]
dump('candidate_all156.json',{'rows':all_candidates});dump('candidate_p51_first5.json',{'rows':p51})
dump('size_label_correction_ledger704.json',{'rows':patches});dump('checks156.json',{'rows':checks})
manifest={'status':'AUTHOR_COMPLETE_SOURCE_BOUND_PENDING_ROOT_INDEPENDENT_REVIEW','classifiedFlaggedRows':1090,'retainedEquivalentNativeSizeRows':386,'correctedRows':704,'bodyCandidates':156,'p51FirstBatchBodies':len(p51),'p51FirstBatchLabelRepairs':sum(len(r['sizeLabelRepairs']) for r in p51),'bodyCandidatesByLocale':dict(Counter(r['locale'] for r in all_candidates)),'measurementCellBytesUnchanged':156,'otherBytesReversibleExact':156,'headerCandidatesFrozenFileSHA256':fs(hfile),'structuralReviewedFrozenFileSHA256':fs(sfile),'candidateFileSHA256':fs(H/'candidate_all156.json'),'p51FileSHA256':fs(H/'candidate_p51_first5.json'),'notes':['S/M/L/XL digits inside size identifiers and child ages can change only within the evidenced first label cells; all actual measurement numbers and units stay byte-identical.','Native Arabic/Hindi/Cyrillic letters and Japanese/Korean adjacent-script equivalents retained if faithful.','Correctable row matching requires exactly one English numeric-cell signature. Ambiguous/unmatched source rows from the broader inventory excluded.','Root must apply against exactly the merged structural375/header2028 planned before value, carrying7 independent alt encodings, or rebase and re-review any concurrent body edits.']}
dump('manifest.json',manifest);print(json.dumps(manifest,ensure_ascii=False))
