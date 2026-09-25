#!/usr/bin/env python3
"""Compile source-bound plans from existing local authored caches, without network."""
from prepare_candidates import HERE,AUDIT,FOOTER,qualify,split_source,jwrite
import collections,hashlib,json,re

plans=[];blocked=[];checks=[];violations=[];rollback=[]
manual={}
for name in ['manual_repairs_log.json','manual_storefront_repairs_log.json','manual_collections_footer_log.json','manual_critical_policy_log.json','manual_policy_quality_log.json']:
    for entry in json.loads((HERE/name).read_text()):manual[(entry['locale'],entry['source'])]=entry
def tags(s):return re.findall(r'<[^>]+>',s)
def numbers(s):return collections.Counter(re.findall(r'\d+',s))
for locale in sorted({r['locale'] for r in AUDIT['fields']} - {'en','da','he','ko'}):
    cache=json.loads((HERE/f'cache_{locale}.json').read_text())[locale]
    rp={};locale_blocked=[]
    for r in AUDIT['fields']:
        reason=qualify(r)
        if r['locale']!=locale or not reason:continue
        input_text=FOOTER.get(r['source'],r['source']);parts=split_source(input_text);new=[];missing=[];authored=[]
        for part in parts:
            text=bool(part.strip() and re.sub(r'<[^>]+>|&[A-Za-z#0-9]+;','',part).strip())
            if text:
                if part not in cache or cache[part] is None:missing.append(part)
                new.append(cache.get(part) or part)
                if (locale,part) in manual:authored.append(part)
            else:new.append(part)
        if missing:
            locale_blocked.append({'row':r,'missingSegments':missing});continue
        value=''.join(new)
        markup_ok=tags(value)==tags(r['source'])
        links_ok=re.findall(r'href="([^"]+)"',value)==re.findall(r'href="([^"]+)"',r['source'])
        expected_nums=numbers(r['source'])
        # Japanese normally renders January numerically. Verify exact calendar date separately.
        date_exception=locale=='ja' and '/ShopPolicy/' in r['resourceId'] and 'January' in r['source']
        if date_exception:expected_nums['1']+=r['source'].count('January')
        numeric_ok=numbers(value)==expected_nums
        clean_tokens=not re.search(r'QZXTOKEN|QXZ|DLMSEP',value)
        checks.append({'locale':locale,'resourceId':r['resourceId'],'key':r['key'],'markup':markup_ok,'href':links_ok,'numbers':numeric_ok,'dateMonthNumeric':date_exception,'tokens':clean_tokens,'manualSegments':len(authored)})
        if not all([markup_ok,links_ok,numeric_ok,clean_tokens]):violations.append(checks[-1])
        out=dict(r,value=value,reason=reason,reviewStatus='LOCAL_PREPARED_FOR_INDEPENDENT_REVIEW',manualSegments=len(authored))
        if r['source'] in FOOTER:out['translationInput']=input_text
        if 'free shipping on all orders' in r['source']:
            out['approvedQualification']='Root explicitly directed standard shipping included instead of all-orders free-shipping claim; source/digest remain exact.'
        rp.setdefault(r['resourceId'],{'resourceId':r['resourceId'],'locale':locale,'rows':[]})['rows'].append(out)
    locale_plans=list(rp.values());plans.extend(locale_plans);blocked.extend(locale_blocked)
    jwrite(HERE/f'candidate_{locale}.json',{'status':'LOCAL_PREPARED_FOR_INDEPENDENT_REVIEW','locale':locale,'plans':locale_plans,'blocked':locale_blocked,'generation':'Public-text Google first pass; rejected corruption repaired locally by author; fashion semantics manually corrected. No network after429. Source policy meaning retained.'})
for plan in plans:
    restore=[];remove=[]
    for r in plan['rows']:
        if r['before'] is None:remove.append(r['key'])
        else:restore.append({'key':r['key'],'value':r['before']['value'],'translatableContentDigest':r['sourceDigest']})
    rollback.append({'resourceId':plan['resourceId'],'locale':plan['locale'],'restore':restore,'remove':remove})
common={'status':'LOCAL_PREPARED_FOR_INDEPENDENT_REVIEW','scope':'17 locales, 9 baseline resources, exact selected fields only; he/ko delegated separately; en/da untouched','plans':plans,'blocked':blocked}
jwrite(HERE/'candidate_17_locales.json',common)
for label,test in [('missing_english',lambda r:r['reason']!='OUTDATED_MEANING_CHANGED'),('stale_meaning',lambda r:r['reason']=='OUTDATED_MEANING_CHANGED')]:
    subset=[]
    for plan in plans:
        rs=[r for r in plan['rows'] if test(r)]
        if rs:subset.append(dict(plan,rows=rs))
    jwrite(HERE/f'candidate_17_{label}.json',dict(common,plans=subset))
jwrite(HERE/'rollback_17_locales.json',{'status':'NOT_EXECUTED','rollback':rollback,'note':'Recheck original source digests and expected current translated values before rollback. API does not restore outdated flag independently.'})
totals={'resourceLocalePlans':len(plans),'selectedFields':sum(len(p['rows']) for p in plans),'blocked':len(blocked),'violations':violations,'localeCounts':dict(collections.Counter(p['locale'] for p in checks)),
        'reasonCounts':dict(collections.Counter(r['reason'] for p in plans for r in p['rows'])),'manualReviewedSegments':sum(x['manualSegments'] for x in checks),
        'sha256':hashlib.sha256((HERE/'candidate_17_locales.json').read_bytes()).hexdigest(),'checks':checks}
jwrite(HERE/'candidate_validation.json',totals)
print(json.dumps({k:v for k,v in totals.items() if k!='checks'},ensure_ascii=False,indent=2))
