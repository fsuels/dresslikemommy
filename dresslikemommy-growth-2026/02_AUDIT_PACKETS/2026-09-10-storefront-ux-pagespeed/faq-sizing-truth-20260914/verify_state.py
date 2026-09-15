"""Narrow release-state checks; no Shopify/Git writes."""
import argparse, hashlib, json
from pathlib import Path
from datetime import datetime, timezone
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(); ap.add_argument('--phase',choices=['preflight','page','final'],required=True); a=ap.parse_args()
def read(name): return json.loads((P/name).read_text())
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def recs(raw):
    rows={}
    for k,rs in raw['data']['translatableResource'].items():
        if k.startswith('t_'):
            for r in rs:
                identity=(r['locale'],(r['market'] or {}).get('id'),r['key'])
                assert identity not in rows
                rows[identity]=r
    return rows
man=read('release-source-manifest.json')
before=read('inventory-before.json')['data']; now=read('inventory-'+a.phase+'.json')['data']
expected=(P/('before/en.html' if a.phase=='preflight' else 'candidates/en.html')).read_bytes().decode()
source=next(x for x in now['translatableResource']['translatableContent'] if x['key']=='body_html')
checks={
 'page_identity':now['page']['id']==man['page_id'],
 'shop_identity':now['shop']==before['shop'],
 'page_protected_fields':all(now['page'][k]==v for k,v in man['protected_page_fields'].items()),
 'page_body_exact':now['page']['body']==expected,
 'source_body_exact':source['value']==expected and source['digest']==sha(expected),
 'nonbody_source_exact':[x for x in now['translatableResource']['translatableContent'] if x['key']!='body_html']==man['protected_translatable_source'],
 'source_keys_preserved':sorted(x['key'] for x in now['translatableResource']['translatableContent'])==sorted(x['key'] for x in before['translatableResource']['translatableContent']),
 'enabled_locales_preserved':now['shopLocales']==before['shopLocales'],
 'all_markets_preserved':now['markets']==before['markets'],
}
qualified={(x['locale'],None,'body_html'):x for x in man['qualified'] if x['locale']!='en'}
results=[]
for scope in man['market_scope_reads']:
    suffix=scope['scope']['id'].split('/')[-1] if scope['scope']['id'] else 'global'
    if a.phase=='page' and suffix!='global':continue
    b=recs(read('translations-before-'+suffix+'.json')); n=recs(read('translations-'+a.phase+'-'+suffix+'.json'))
    checks['record_identity_'+suffix]=set(b)==set(n)
    for ident,old in b.items():
        actual=n.get(ident); q=qualified.get(ident)
        expected_value=(P/q['candidate_path']).read_bytes().decode() if q and a.phase=='final' else old['value']
        allowed=['value','updatedAt','outdated'] if q and a.phase=='final' else (['outdated'] if q and a.phase=='page' else [])
        protected=actual is not None and all(actual[k]==v for k,v in old.items() if k not in allowed)
        meta=actual is not None and (actual['outdated'] is False if q and a.phase=='final' else True)
        results.append({'locale':ident[0],'scope':suffix,'key':ident[2],'value_exact':actual is not None and actual['value']==expected_value,'protected_metadata_exact':protected,'expected_metadata':meta,'after_sha256':sha(actual['value']) if actual else None})
checks['all_translation_values_and_metadata']=all(x['value_exact'] and x['protected_metadata_exact'] and x['expected_metadata'] for x in results)
if a.phase=='preflight':
    checks['english_updatedAt_unchanged']=now['page']['updatedAt']==before['page']['updatedAt']
    prior_guide=read('guide-source-before.json')['data']; current_guide=read('guide-source-preflight.json')['data']
    checks['qualified_guide_source_unchanged']=current_guide==prior_guide
result={'observedAt':datetime.now(timezone.utc).isoformat(),'phase':a.phase,'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'translation_records_checked':len(results),'translation_records':results,'page_body_sha256':sha(now['page']['body']),'source_digest':source['digest']}
(P/('state-verification-'+a.phase+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='translation_records'},indent=2))
assert all(checks.values()),[k for k,v in checks.items() if not v]
