#!/usr/bin/env python3
"""Exhaustive field coverage audit with conservative, explicitly limited language flags."""
from __future__ import annotations
import collections,hashlib,html,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
LOCALES=[x['locale'] for x in json.loads((HERE/'counts_before.json').read_text())['data']['shopLocales'] if not x['primary']]
OWN=json.loads((HERE/'resource_ownership.json').read_text())
def text(value):
    value=re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', value or '', flags=re.I|re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',value))).strip()
def digest(value):return hashlib.sha256(value.encode()).hexdigest()
def write(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def rows():
    seen=set()
    for f in sorted(HERE.glob('translations_batch_*.json')):
        raw=json.loads(f.read_text())
        for n in raw['data']['translatableResourcesByIds']['nodes']:
            assert n['resourceId'] not in seen;seen.add(n['resourceId'])
            yield f.name,n
def selected(n):
    keys={'title','body_html','product_type','meta_title','meta_description'} if OWN[n['resourceId']]['kind']=='Product' else {'name'}
    return [s for s in n['translatableContent'] if s['key'] in keys]
def invariant(value,locale):
    t=text(value).strip().lower()
    if not re.search(r'[a-zA-Z]',t):return True
    if t in {'default title','dress like mommy','dlm','peter rabbit'}:return True
    # Independently reviewed identical words that are also correct in these locales.
    identical={'es':{'color','top','tops'},'cs':{'leopard','text','cardigan','top'},'da':{'leopard','juice','design','cardigan','type','top','vest'},'de':{'leopard','sets','overall','text','design','pullover','top'},'no':{'leopard','overall','juice','design','cardigan','type','vest'},'ro':{'leopard','text','cardigan','top'},'nl':{'sets','pullover','type','shirt','top','vest'},'it':{'cardigan','pullover','top'},'fr':{'style','type','cardigan'},'sv':{'cardigan'},'pl':{'top'},'pt-BR':{'top'}}
    if t in identical.get(locale,set()):return True
    if locale=='ro' and re.fullmatch(r'adult\s+(?:[2-5]?xl|[sml])',t):return True
    if re.fullmatch(r'(?:[0-9. /+\-]|x{0,4}[sl]|m|os|one size numeric|cm|mm|kg|lb|oz|y|t)+',t):return True
    borrowed={'t-shirt','t-shirts','polo','polo shirt','denim','bikini','tankini','leggings','hoodie','hoodies','shorts','jeans','maxi','mini','3d'}
    if t in borrowed:return True
    common={'beige','navy','khaki','mint','burgundy','apricot','coffee','wine red','orange','pink','blue','black','white','green','purple','red','gray','grey','gold','rose','coral','camel','champagne','multicolor','multicolour','one size'}
    local={'da':{'beige','khaki','orange','pink','coral','navy'},'de':{'beige','khaki','orange','pink','navy'},'fr':{'beige','orange','rose','coral'},'nl':{'beige','khaki','orange','pink','navy'},'no':{'beige','khaki','pink','navy'},'sv':{'beige','khaki','orange','navy'},'fi':{'beige','khaki','pink','navy'},'cs':{'khaki'},'it':{'beige','khaki','denim'},'es':{'beige','coral'},'pt-BR':{'beige','coral'},'ro':{'beige','coral'}}
    if t in common and t in local.get(locale,set()):return True
    return False
def prepare():
    values={}
    for _,n in rows():
        for s in selected(n):
            t=text(s.get('value')); 
            if len(t)>=35:values[digest(t)]=t
        for locale in LOCALES:
            for tr in n['tr_'+locale.replace('-','_')]:
                if tr['locale']!=locale or tr.get('market') is not None:continue
                t=text(tr.get('value'))
                if len(t)>=35:values[digest(t)]=t
    with (HERE/'language_inputs.jsonl').open('w') as f:
        for k,v in sorted(values.items()):f.write(json.dumps({'sha256':k,'text':v},ensure_ascii=False)+'\n')
    print('Unique offline language inputs:',len(values))
def final():
    predictions={x['sha256']:x['hypotheses'] for x in map(json.loads,(HERE/'language_predictions.jsonl').read_text().splitlines())}
    defects=[];review=[];bylocale=collections.defaultdict(collections.Counter);keys=collections.Counter();exempt=collections.Counter();checked=0;alias_issues=[];market_issues=[];fields=0;empty=0
    scripts={'ar':r'[\u0600-\u06ff]','he':r'[\u0590-\u05ff]','hi':r'[\u0900-\u097f]','el':r'[\u0370-\u03ff]','ru':r'[\u0400-\u04ff]','ja':r'[\u3040-\u30ff\u4e00-\u9fff]','ko':r'[\uac00-\ud7af]'}
    close=[{'da','no','nb','nn','sv'},{'cs','sk'},{'ru','uk'},{'es','pt','pt-BR','gl'},{'hi','mr'}]
    for filename,n in rows():
        own=OWN[n['resourceId']]
        for locale in LOCALES:
            for tr in n['tr_'+locale.replace('-','_')]:
                if tr['locale']!=locale:alias_issues.append({'resourceId':n['resourceId'],'alias':locale,'rowLocale':tr['locale'],'key':tr['key']})
                if tr.get('market') is not None:market_issues.append({'resourceId':n['resourceId'],'locale':tr['locale'],'market':tr['market'],'key':tr['key']})
        for s in selected(n):
            fields+=1;keys[own['kind']+'.'+s['key']]+=1;source=text(s.get('value'))
            if not source:empty+=1;continue
            for locale in LOCALES:
                checked+=1;found=[x for x in n['tr_'+locale.replace('-','_')] if x['key']==s['key'] and x['locale']==locale and x.get('market') is None]
                assert len(found)<=1, 'Duplicate exact locale/global field'
                tr=found[0] if found else None;value=text(tr.get('value')) if tr else ''; reasons=[]
                base={'resourceId':n['resourceId'],'productId':own['productId'],'kind':own['kind'],'key':s['key'],'locale':locale,'sourceDigest':s.get('digest'),'sourceSHA256':digest(s.get('value') or ''),'currentSHA256':digest(tr.get('value') or '') if tr else None,'rawFile':filename,'hasVariants':own.get('hasVariants')}
                if invariant(s.get('value'),locale):
                    exempt[own['kind']]+=1
                    if tr and tr.get('outdated'):review.append(dict(base,reasons=['outdated_invariant_copy']))
                    continue
                if not tr or not value:reasons.append('missing')
                else:
                    if tr['outdated']:reasons.append('outdated')
                    if value.casefold()==source.casefold():reasons.append('source_english')
                    pred=predictions.get(digest(value),[])
                    if pred and len(value)>=50:
                        top=pred[0];lang=top['language'];wanted='pt' if locale=='pt-BR' else locale
                        ambiguous=any(lang in g and wanted in g for g in close)
                        if lang!=wanted and not ambiguous and top['probability']>=0.99:
                            if locale in scripts and not re.search(scripts[locale],value) and len(re.findall(r'\w+',value))>=6:
                                reasons.append('wrong_script_language');base['detectedLanguage']=top
                            elif len(value)>=140 and len(re.findall(r'\w+',value))>=20:
                                review.append(dict(base,reasons=['probable_wrong_language'],detectedLanguage=top,currentTextPreview=value[:180]))
                    # Whole English paragraphs copied verbatim are meaningful leakage; table codes excluded.
                    if s['key']=='body_html' and value.casefold()!=source.casefold():
                        chunks=[text(x) for x in re.split(r'</(?:p|li|h[1-6])\s*>',s.get('value') or '',flags=re.I)]
                        matches=[x for x in chunks if len(re.findall(r'[A-Za-z]+',x))>=12 and len(x)>=90 and x.casefold() in value.casefold()]
                        if matches:reasons.append('source_english_paragraph');base['matchedEnglishParagraphs']=matches[:3]
                if reasons:
                    base['reasons']=sorted(set(reasons));defects.append(base)
                    for reason in base['reasons']:bylocale[locale][reason]+=1
    with (HERE/'defects.jsonl').open('w') as f:
        for x in defects:f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
    with (HERE/'language_review_candidates.jsonl').open('w') as f:
        for x in review:f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
    summary={'publishedLocalesIncludingSource':21,'translationLocales':LOCALES,'uniqueResourcesAudited':len(OWN),'sourceFieldsAudited':fields,'sourceFieldsByType':dict(keys),'sourceEmptyFieldsNotMissingTranslationDefects':empty,'nonemptyFieldLocaleChecks':checked,'invariantFieldLocaleChecksExemptFromMissingEnglish':dict(exempt),'defectFieldLocaleRows':len(defects),'distinctAffectedProducts':len(set(x['productId'] for x in defects)),'defectsByLocale':dict(bylocale),'defectsByResourceKind':dict(collections.Counter(x['kind'] for x in defects)),'reviewCandidates':len(review),'unexpectedAliasLocaleRows':len(alias_issues),'unexpectedMarketRows':len(market_issues),'scope':'Global translations, explicit row.locale equality and market=null. All active online-store products; all options and option values, including inactive values. English source included, not requested as a translation.','limits':['Language detection runs offline with Apple NaturalLanguage; statistical candidates are not semantic certification.','No full manual meaning review of every product body; exhaustive inventory and deterministic field coverage, plus clear script and English leakage screening.','Market-specific overrides are separately checked only for the three parent-observed Danish homepage cases; global export exposes only returned market rows.','Variant display copy is covered by all option names and option values; variant counts exact, no SKU, prices, inventory or individual variant selected-option combinations fetched.','Arbitrary product metafields, image alt text, media, vendor and handle translations are excluded. SEO meta_title/meta_description are included.','Standard size codes, brand names and conservative borrowed-term allowlists excluded from missing/English defect counts.']}
    write('audit_summary.json',summary);write('alias_locale_anomalies.json',alias_issues);write('returned_market_rows.json',market_issues)
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':
    (prepare if sys.argv[1]=='prepare' else final)()
