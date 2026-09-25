#!/usr/bin/env python3
"""Read public English text; generate local, unapplied translation candidates only."""
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path('/Users/fsuels/Projects/dresslikemommy')
sys.path.insert(0, str(ROOT / 'ops/scripts'))
from translation_utils import TranslationBackend

HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / 'audit_fields.json').read_text())
assert not AUDIT['sourceDrift'] and not AUDIT['duplicateLocaleMarketKeys']
FOOTER = {
    't:sections.footer_headings.company_info': 'Company Information',
    't:sections.footer_headings.customer_care': 'Customer Care',
}
LITERALS = [
    'FKG Trading LLC', 'Dress Like Mommy', 'Francisco Suels', 'Shopify Payments',
    'Google Analytics', 'Shopify', 'Stripe', 'info@dresslikemommy.com',
    '14937 Indigo Lakes Dr, Naples, FL 34119, USA', '14937 Indigo Lakes Dr',
    'Naples, FL 34119', '(786) 309-6006', 'Collier County, Florida',
    'SSL/TLS', 'PCI-DSS', 'GDPR', 'CCPA', 'EST', 'AM', 'PM', 'Final Sale',
]
PROTECT = re.compile(
    r'<[^>]+>|\{\{.*?\}\}|\{%.*?%\}|https?://[^\s<>]+|'
    r'[\w.+-]+@[\w.-]+\.[A-Za-z]+|&[A-Za-z#0-9]+;|'
    + '|'.join(re.escape(x) for x in sorted(LITERALS, key=len, reverse=True))
    + r'|\d+(?::\d+)?(?:[–-]\d+)?(?:%|\+)?', re.S)
TOKEN = re.compile(r'QZXTOKEN\d{5}QXZ')

def jwrite(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def skeleton(value):
    return re.findall(r'<[^>]+>|&[A-Za-z#0-9]+;', value)

def qualify(row):
    if row['locale'] in ('en', 'da'):
        return None
    if row['reason'] in ('MISSING', 'EMPTY', 'ENGLISH_EQUALS_SOURCE'):
        return row['reason']
    if row['reason'] != 'OUTDATED_REVIEW':
        return None
    # Outdated alone is insufficient: preserve the four semantically correct values.
    if '/OnlineStoreThemeSectionGroup/' in row['resourceId']:
        return None
    if 'curated_product_grid_main.button_label:' in row['key']:
        return None
    return 'OUTDATED_MEANING_CHANGED'

class PublicBackend(TranslationBackend):
    """Reuse established Google public-text backend, with no secondary-provider fallback."""
    def _protect(self, text, locale):
        replacements = []
        def sub(match):
            token = f'QZXTOKEN{len(replacements):05d}QXZ'
            replacements.append((token, match.group(0)))
            return token
        return PROTECT.sub(sub, text), replacements

def split_source(value):
    # Whole paragraphs/lines retain context and inline formatting; exact separators stay local.
    return re.split(r'(\n+)', value)

def translate_locale(locale, fields):
    backend = PublicBackend(cache_path=HERE / f'cache_{locale}.json', retries=2,
        request_timeout=30, batch_size=20, batch_char_limit=3200,
        pause_seconds=0.15, cleanup_rules_path=None)
    cache = backend.cache.setdefault(locale, {})
    inputs = {}
    for row in fields:
        value = FOOTER.get(row['source'], row['source'])
        for part in split_source(value):
            if part.strip() and re.sub(r'<[^>]+>|&[A-Za-z#0-9]+;', '', part).strip():
                inputs.setdefault(part, None)
    pending=[]
    for source in inputs:
        if source in cache and cache[source] is not None:
            continue
        lead=re.match(r'^\s*',source).group();trail=re.search(r'\s*$',source).group()
        core=source[len(lead):len(source)-len(trail) if trail else len(source)]
        protected,replacements=backend._protect(core,locale)
        if not TOKEN.sub('',protected).strip(' .,;:()[]—–-&|/?!"'):
            cache[source]=source
        else:
            pending.append((source,lead,trail,protected,replacements))
    batches=[];batch=[];chars=0
    for item in pending:
        if batch and (len(batch)>=20 or chars+len(item[3])>3200):
            batches.append(batch);batch=[];chars=0
        batch.append(item);chars+=len(item[3])+20
    if batch:batches.append(batch)
    failures=[]
    for index,batch in enumerate(batches):
        output=None
        for attempt in range(2):
            try:
                output=backend._http_translate_batch(locale,[x[3] for x in batch]);break
            except Exception as error:
                if attempt==1:
                    failures.append({'batch':index+1,'error':str(error),'source_count':len(batch)})
                else:time.sleep(0.5)
        if output is not None:
            for item,translated in zip(batch,output):
                source,lead,trail,protected,replacements=item
                original_tokens=TOKEN.findall(protected);new_tokens=TOKEN.findall(translated)
                if collections.Counter(original_tokens)!=collections.Counter(new_tokens):
                    failures.append({'source':source,'reason':'PROTECTED_TOKEN_DRIFT','raw':translated})
                    continue
                restored=lead+backend._restore(translated,replacements)+trail
                if skeleton(restored)!=skeleton(source):
                    failures.append({'source':source,'reason':'HTML_EVENT_DRIFT','raw':restored})
                    continue
                # Numeric order can naturally move; all original numeric values must remain.
                if collections.Counter(re.findall(r'\d+',restored))!=collections.Counter(re.findall(r'\d+',source)):
                    failures.append({'source':source,'reason':'NUMERIC_DRIFT','raw':restored})
                    continue
                cache[source]=restored
        backend._save_cache()
        if index==0 or (index+1)%5==0 or index+1==len(batches):
            print(f'{locale}: batch {index+1}/{len(batches)}, cached {len(cache)}/{len(inputs)}, failures {len(failures)}',flush=True)
        time.sleep(0.15)
    plans={};blocked=[]
    for row in fields:
        value=FOOTER.get(row['source'],row['source']);parts=split_source(value);result=[];missing=[]
        for part in parts:
            if part in inputs:
                translated=cache.get(part)
                if translated is None:missing.append(part)
                result.append(translated or part)
            else:result.append(part)
        if missing:
            blocked.append({'row':row,'missingSegments':missing});continue
        new=''.join(result)
        if skeleton(new)!=skeleton(value):raise AssertionError('Reconstruction tag mismatch')
        out=dict(row,value=new,reason=qualify(row),translationInput=value,
                 reviewStatus='CANDIDATE_REQUIRES_INDEPENDENT_SEMANTIC_REVIEW')
        plans.setdefault(row['resourceId'],{'resourceId':row['resourceId'],'locale':locale,'rows':[]})['rows'].append(out)
    payload={'status':'CANDIDATE_NOT_APPLIED','locale':locale,'source':'before_'+locale+'.json',
        'generation':'Google public translation endpoint via repository TranslationBackend; public text only; protected markup/numbers/contact literals; no external mutations',
        'plans':list(plans.values()),'blocked':blocked,'segmentFailures':failures}
    jwrite(HERE/f'candidate_{locale}.json',payload)
    return {'locale':locale,'selected':len(fields),'ready':sum(len(x['rows']) for x in plans.values()),'blocked':len(blocked),'segmentFailures':len(failures)}

if __name__=='__main__':
    by_locale=collections.defaultdict(list)
    for row in AUDIT['fields']:
        if qualify(row):by_locale[row['locale']].append(row)
    assert sum(map(len,by_locale.values()))==711
    jwrite(HERE/'candidate_selection.json',{'selectedCount':711,'reasonCounts':dict(collections.Counter(qualify(r) for rows in by_locale.values() for r in rows)),
        'semanticallyPreservedOutdated':[r for r in AUDIT['fields'] if r['reason']=='OUTDATED_REVIEW' and not qualify(r)],
        'localeCounts':{k:len(v) for k,v in by_locale.items()}})
    chosen=sys.argv[1:] or list(by_locale)
    results=[]
    with ThreadPoolExecutor(max_workers=3) as pool:
        future={pool.submit(translate_locale,l,by_locale[l]):l for l in chosen}
        for f in as_completed(future):
            try:result=f.result()
            except Exception as e:result={'locale':future[f],'error':str(e)}
            results.append(result);jwrite(HERE/'generation_status.json',results);print(result,flush=True)
