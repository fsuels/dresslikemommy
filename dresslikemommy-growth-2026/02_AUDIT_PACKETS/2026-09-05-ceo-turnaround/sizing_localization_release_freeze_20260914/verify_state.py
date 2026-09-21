"""Compare captured read-only Shopify responses; this file cannot write to Shopify."""
from pathlib import Path
import json, hashlib, sys
BASE=Path(__file__).resolve().parent
SOURCE='c1c3ca1fa58097d25857d12fb361f82ac60ae7d45f5545a717ca9a6ab04aea88'
def read(n): return json.loads((BASE/n).read_text())
def data(n):
    r=read(n)['result']
    assert not r.get('errors'), r.get('errors')
    return r['data']
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def run(stage):
    assert stage in ['prewrite','after']
    checks={}; inv=data('inventory-before.json'); nowinv=data('inventory-'+stage+'.json')
    checks['locale_market_inventory_unchanged']=inv==nowinv
    checks['market_pagination_complete']=not nowinv['markets']['pageInfo']['hasNextPage']
    a=data('article-before.json'); na=data('article-'+stage+'.json')
    checks['shop_identity_unchanged']=a['shop']==na['shop']
    checks['article_locale_inventory_unchanged']=a['shopLocales']==na['shopLocales']
    checks['english_body_unchanged']=na['article']['body']==a['article']['body'] and sha(na['article']['body'])==SOURCE
    for key in ['id','handle','title','summary','tags','isPublished','publishedAt','createdAt','templateSuffix','blog','author','image']:
        checks['protected_article_'+key]=a['article'][key]==na['article'][key]
    before=data('translations-before.json')['translatableResource']; current=data('translations-'+stage+'.json')['translatableResource']
    checks['same_query_aliases']=set(before)==set(current)
    checks['same_resource_identity']=before['resourceId']==current['resourceId']==a['article']['id']
    rows=read('mutation-variables.json'); rollback=read('rollback-variables.json')
    expected={r['locale']:r for r in rows['translations']}
    checks['exact_18_inputs']=len(rows['translations'])==len(expected)==18
    checks['body_global_only']=all(set(r)=={'locale','key','value','translatableContentDigest'} and r['key']=='body_html' and r['translatableContentDigest']==SOURCE for r in rows['translations'])
    checks['target_identity']=rows['resourceId']==rollback['resourceId']==a['article']['id']
    source=next(s for s in current['s_g'] if s['key']=='body_html')
    checks['current_digest_and_english_exact']=source['digest']==SOURCE and source['value']==na['article']['body']
    body_count=other_count=0
    locales=read('translations-before.json')['locales']
    for alias,value in before.items():
        if alias=='resourceId': continue
        if alias.startswith('s_'):
            checks['source_'+alias]=current[alias]==value
        elif not alias.startswith('g_'):
            checks['market_empty_'+alias]=value==current[alias]==[]
        else:
            old={(r['locale'],r['key'],r['market']['id'] if r['market'] else None):r for r in value}
            new={(r['locale'],r['key'],r['market']['id'] if r['market'] else None):r for r in current[alias]}
            checks['identities_'+alias]=set(old)==set(new) and len(new)==len(current[alias])
            for ident,b in old.items():
                lc,key,market=ident
                if key=='body_html':
                    body_count+=1; e=expected[lc]; n=new.get(ident,{})
                    checks['before_local_file_'+lc]=sha(b['value'])==sha((BASE/'locales'/lc/'before.html').read_text())
                    checks['payload_candidate_'+lc]=e['value']==(BASE/'locales'/lc/'candidate.html').read_text()
                    checks['rollback_'+lc]=next(r for r in rollback['translations'] if r['locale']==lc)['value']==b['value']
                    checks['body_'+lc]=(n==b if stage=='prewrite' else n.get('value')==e['value'] and n.get('outdated') is False and n.get('market') is None and n.get('key')=='body_html' and n.get('locale')==lc)
                else:
                    other_count+=1; checks['unrelated_'+lc+'_'+key]=new.get(ident)==b
    checks['18_existing_body_rows']=body_count==18
    checks['72_unrelated_global_rows']=other_count==72
    return {'stage':stage,'status':'PASS' if all(checks.values()) else 'HOLD','passed':sum(checks.values()),'total':len(checks),'checks':checks,'article_updatedAt_before':a['article']['updatedAt'],'article_updatedAt_observed':na['article']['updatedAt'],'source_digest':SOURCE,'limit':'Checks captured API responses only. Public behavior and independent reviews are separate.'}
if __name__=='__main__':
    result=run(sys.argv[1]); (BASE/('state-verification-'+sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'})); print('Failed:',[k for k,v in result['checks'].items() if not v])
    sys.exit(0 if result['status']=='PASS' else 1)
