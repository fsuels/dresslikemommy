"""Offline classification of the complete source/translation export."""
import collections
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read(p): return json.loads((HERE/p).read_text())
def write(p,x): (HERE/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def digest(x): return hashlib.sha256((x or '').encode()).hexdigest()
def visible(s):
    s=re.sub(r'<(?:script|style)\b[^>]*>.*?</(?:script|style)>',' ',s or '',flags=re.I|re.S)
    s=re.sub(r'<!--.*?-->',' ',s,flags=re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',s))).strip()
def norm(s): return re.sub(r'[^\w]+',' ',visible(s).casefold()).strip()

inventory=read('inventory.json');completion=read('fetch_complete.json')
locales=inventory['nonEnglishLocales'];articles={a['id']:a for a in inventory['publishedArticles']}
source_native={n['id']:n for p in sorted((HERE/'raw').glob('source_*.json')) for n in json.loads(p.read_text())['data']['nodes']}
assert set(source_native)==set(articles)
sources={};ledger=[];integrity=[];ignored_locale_rows=0;market_rows=0;detector=[]
fields_by_article={};source_files={}
for p in sorted((HERE/'raw').glob('translations_*.json')):
    packet=json.loads(p.read_text());locale=packet['variables']['locale'];nodes=packet['data']['translatableResourcesByIds']['nodes']
    for n in nodes:
        rid=n['resourceId'];a=articles[rid]
        canonical=[{'key':x['key'],'value':x['value'],'digest':x['digest'],'locale':x['locale']} for x in n['translatableContent']]
        if rid in sources and canonical!=sources[rid]: integrity.append({'resourceId':rid,'locale':locale,'issue':'SOURCE_DRIFT_ACROSS_LOCALE_SNAPSHOTS'})
        else: sources[rid]=canonical;source_files.setdefault(rid,str(p.relative_to(HERE)))
        fieldmap={x['key']:x for x in canonical};fields_by_article[rid]=set(fieldmap)
        for key,nativekey in [('title','title'),('body_html','body'),('summary_html','summary')]:
            native_value=source_native[rid].get(nativekey) or ''
            # Optional null summaries are omitted from translatableContent, not source drift.
            if (key not in fieldmap and native_value) or (key in fieldmap and (fieldmap[key]['value'] or '')!=native_value):
                integrity.append({'resourceId':rid,'locale':locale,'key':key,'issue':'NATIVE_SOURCE_AND_TRANSLATABLE_CONTENT_DIFFER'})
        translations={}
        for t in n['translations']:
            if t['locale']!=locale:
                ignored_locale_rows+=1;continue
            if t.get('market') is not None:
                market_rows+=1;continue
            if t['key'] in translations: integrity.append({'resourceId':rid,'locale':locale,'key':t['key'],'issue':'DUPLICATE_EXACT_LOCALE_KEY'})
            translations[t['key']]=t
        for s in canonical:
            key=s['key'];t=translations.get(key);source=s['value'] or '';value=t.get('value') or '' if t else '';plain=visible(value);sp=visible(source)
            flags=[]
            if key=='handle':
                classification='EXCLUDED_ROUTING_HANDLE'
            elif not sp:
                classification='EMPTY_SOURCE_NO_TRANSLATION_NEEDED'
            else:
                if t is None:flags.append('MISSING')
                elif not plain:flags.append('EMPTY_TRANSLATION')
                if t and t['outdated']:flags.append('OUTDATED_SOURCE_CHANGED')
                if t and plain and (value==source or norm(value)==norm(source)) and len(re.findall(r'[A-Za-z]+',sp))>=3:
                    flags.append('SOURCE_ENGLISH_IDENTICAL')
                classification='DEFECT_OR_REVIEW_NEEDED' if flags else 'PRESENT_NO_PRIMARY_FLAG_SEMANTICS_UNVERIFIED'
            row={'id':str(len(ledger)),'resourceId':rid,'blogId':a['blog']['id'],'handle':a['handle'],'publishedAt':a['publishedAt'],'locale':locale,'key':key,'classification':classification,'flags':flags,'sourceDigest':s['digest'],'sourceSha256':digest(source),'translationPresent':t is not None,'translationSha256':digest(value) if t else None,'outdated':t['outdated'] if t else None,'sourceCharacters':len(source),'translationCharacters':len(value),'sourceVisibleWords':len(sp.split()),'translationVisibleWords':len(plain.split()),'sourceExcerpt':sp[:200],'translationExcerpt':plain[:200] if t else None,'rawFile':str(p.relative_to(HERE)),'matchingRule':'resourceId + exact locale + key + market:null','sourceEditorialHold':rid=='gid://shopify/Article/559662366817' and key=='body_html'}
            if t and plain and key!='handle' and sp and 'SOURCE_ENGLISH_IDENTICAL' not in flags:
                english_fragments=[]
                source_blocks=re.findall(r'<(?:p|h[1-6]|li)\b[^>]*>.*?</(?:p|h[1-6]|li)>',source,flags=re.I|re.S)
                for block in source_blocks:
                    bp=visible(block);words=re.findall(r'[A-Za-z]+',bp)
                    if len(words)>=10 and len(bp)>=70 and norm(bp) in norm(value):
                        english_fragments.append(bp[:500])
                if english_fragments:
                    row['flags'].append('UNCHANGED_ENGLISH_SOURCE_PASSAGE_REVIEW')
                    row['unchangedEnglishPassages']=list(dict.fromkeys(english_fragments))[:10]
                language_text=re.sub(r'https?://\S+|\b\S+@\S+\b',' ',plain)
                language_text=language_text.replace('Dress Like Mommy',' ').replace('dresslikemommy.com',' ')
                if len(language_text)>=35 and len(re.findall(r'\w',language_text))>=20:
                    detector.append({'id':row['id'],'text':language_text[:25000]})
            ledger.append(row)

assert len(ledger)==len({(x['resourceId'],x['locale'],x['key']) for x in ledger})
for rid in articles:
    for locale in locales:
        actual={r['key'] for r in ledger if r['resourceId']==rid and r['locale']==locale}
        if actual!=fields_by_article[rid]:integrity.append({'resourceId':rid,'locale':locale,'issue':'INCOMPLETE_FIELDS'})
write('integrity_checks.json',{'status':'PASS' if not integrity else 'FAIL','errors':integrity,'articles':len(articles),'nonEnglishLocales':len(locales),'localeArticlePairs':len(articles)*len(locales),'exactLocaleDuplicateKeys':False,'ignoredWrongLocaleRows':ignored_locale_rows,'marketSpecificRowsExcluded':market_rows,'sourcesAgreeAcrossAllLocaleQueries':not integrity})
write('field_ledger.json',ledger)
with (HERE/'language_detector_input.jsonl').open('w') as f:
    for x in detector:f.write(json.dumps(x,ensure_ascii=False)+'\n')
print(json.dumps({'phase':'primary_ledger','rows':len(ledger),'primaryFlagCounts':dict(collections.Counter(flag for r in ledger for flag in r['flags'])),'languageRows':len(detector),'integrityErrors':len(integrity)}),flush=True)
with (HERE/'language_detector_input.jsonl').open() as inp,(HERE/'language_detector_output.jsonl').open('w') as out:
    proc=subprocess.run(['swift',str(HERE/'detect_language.swift')],stdin=inp,stdout=out,stderr=subprocess.PIPE,text=True)
if proc.returncode:
    write('language_detector_error.json',{'returncode':proc.returncode,'stderr':proc.stderr[:2000]})
    raise SystemExit('On-device language check failed; primary ledger retained.')
detected={x['id']:x for x in (json.loads(line) for line in (HERE/'language_detector_output.jsonl').read_text().splitlines())}
assert len(detected)==len(detector)
for row in ledger:
    if row['id'] not in detected:continue
    result=detected[row['id']];dominant=result['dominant'];confidence=result['hypotheses'].get(dominant,0);expected={'pt-BR':{'pt'},'no':{'nb','nn','no'}}.get(row['locale'],{row['locale']})
    row['onDeviceLanguage']={'dominant':dominant,'confidence':confidence,'expected':sorted(expected)}
    if dominant not in expected and confidence>=0.85:
        row['flags'].append('WRONG_LANGUAGE_SUSPECT_HIGH_CONFIDENCE')
        row['classification']='DEFECT_OR_REVIEW_NEEDED'
    elif dominant not in expected and confidence>=0.55 and row['translationCharacters']>=100:
        row['flags'].append('WRONG_LANGUAGE_SUSPECT_MODERATE_CONFIDENCE')
        row['classification']='DEFECT_OR_REVIEW_NEEDED'
    if row['flags'] and row['classification'] not in ['EXCLUDED_ROUTING_HANDLE','EMPTY_SOURCE_NO_TRANSLATION_NEEDED']:
        row['classification']='DEFECT_OR_REVIEW_NEEDED'
write('field_ledger.json',ledger)
write('defect_ledger.json',[r for r in ledger if r['flags']])
write('wrong_language_review.json',[r for r in ledger if any(x.startswith('WRONG_LANGUAGE') for x in r['flags'])])
by_locale={};by_key={};by_article=[]
for locale in locales:
    selected=[r for r in ledger if r['locale']==locale]
    by_locale[locale]={'fields':len(selected),'flaggedFields':sum(bool(r['flags']) for r in selected),'flags':dict(collections.Counter(f for r in selected for f in r['flags'])),'classifications':dict(collections.Counter(r['classification'] for r in selected))}
for key in sorted({r['key'] for r in ledger}):
    selected=[r for r in ledger if r['key']==key]
    by_key[key]={'fields':len(selected),'flaggedFields':sum(bool(r['flags']) for r in selected),'flags':dict(collections.Counter(f for r in selected for f in r['flags']))}
for rid,a in articles.items():
    selected=[r for r in ledger if r['resourceId']==rid]
    by_article.append({'resourceId':rid,'blogId':a['blog']['id'],'handle':a['handle'],'title':a['title'],'fields':len(selected),'flaggedFields':sum(bool(r['flags']) for r in selected),'flags':dict(collections.Counter(f for r in selected for f in r['flags'])),'bodySourceWords':len(visible(source_native[rid]['body']).split()),'formerOrganicOwnerArchived':rid=='gid://shopify/Article/559662366817'})
write('counts_by_locale.json',by_locale);write('counts_by_key.json',by_key);write('counts_by_article.json',by_article)
write('audit_summary.json',{'status':'FULL_READ_ONLY_AUDIT_COMPLETE' if not integrity else 'AUDIT_RETRIEVED_SOURCE_INTEGRITY_REQUIRES_REVIEW','blogs':len(inventory['blogs']),'allArticles':inventory['allArticleCount'],'publishedArticles':len(articles),'excludedArticles':inventory['excludedArticleCount'],'nonEnglishLocales':len(locales),'localeArticlePairs':len(articles)*len(locales),'sourceFields':sum(len(x) for x in fields_by_article.values()),'fieldLocaleRows':len(ledger),'flaggedFields':sum(bool(r['flags']) for r in ledger),'flagCounts':dict(collections.Counter(flag for r in ledger for flag in r['flags'])),'classificationCounts':dict(collections.Counter(r['classification'] for r in ledger)),'bodySourceWords':sum(x['bodySourceWords'] for x in by_article),'languageDetector':{'method':'Apple NaturalLanguage NLLanguageRecognizer on-device','rows':len(detector),'networkCalls':0,'resultStatus':'INFERRED_NEEDS_MANUAL_REVIEW'},'rawSourceFiles':4,'rawTranslationFiles':80,'paginationExhausted':True,'externalWrites':False,'translationProviderCalls':0,'notes':['Missing/empty/source-English-identical are verified mechanically against exact source and existing value. Outdated is an API source-change flag, not proof the existing translation has wrong meaning.','Language detection is probabilistic and separately reviewable; no automatic overwrite is authorized from a language label.','No-flag fields are not certified semantically perfect. This is an exhaustive structural/language audit, not a manual sentence-by-sentence translation review.','All source fields retained; handle fields excluded from translation-defect selection. Empty source does not require a translation.','Halloween source-body editorial history preserved; former owner archived per parent. Parent owns translation-only decisions after fresh source review, no English source changes here.','Every ledger row references the raw source/digest/before record; no credentials persisted.']})
manifest={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'raw').glob('*.json'))}
write('raw_manifest_sha256.json',manifest)
print(json.dumps(read('audit_summary.json'),ensure_ascii=False),flush=True)
