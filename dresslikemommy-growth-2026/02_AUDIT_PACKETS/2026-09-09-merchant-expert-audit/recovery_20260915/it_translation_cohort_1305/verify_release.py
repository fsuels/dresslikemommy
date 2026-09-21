#!/usr/bin/env python3
"""Read-only exact before/after verifier for this bounded Italian registration."""
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIVATE = Path('/Users/fsuels/.config/dresslikemommy/merchant-execution-receipts/20260915-it-cohort-1305')
RAW_SHA = '2b1b8e4f6c5fc1db0b5bddf777bcaf56c83ef2a0c563b4ae091f82baeddde4a6'
SCOPE = [
 ('7227375714401', ['body_html']),
 ('7227378892897', ['title','meta_title','meta_description']),
 ('7536709664865', ['title']),
 ('7536984359009', ['title']),
 ('7545279217761', ['title','body_html','product_type','meta_title','meta_description']),
 ('7545279512673', ['body_html','meta_title','meta_description']),
 ('7545279840353', ['body_html','meta_title','meta_description']),
 ('7545373130849', ['body_html','meta_title','meta_description']),
 ('7546613530721', ['title','body_html','meta_title','meta_description']),
]
def read(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def time(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def by_id(d): return {n['resourceId']:n for n in d['translatableResourcesByIds']['nodes']}
def by_key(a): return {n['key']:n for n in a}
def verify(mode, snapshot, override):
    checks=[]
    def ck(label, value):
        checks.append({'check':label,'pass':bool(value)})
    raw=PRIVATE/'before.json'
    ck('private_before_hash',digest(raw)==RAW_SHA)
    before=read(raw)['data']; new=read(snapshot)['data']
    b=by_id(before); n=by_id(new)
    variables=read(HERE/'register.variables.json')
    review=read(HERE/'independent_proposal_review.json')
    ck('independent_review_pass',review.get('status') in ('PASS','PASS_WITH_LIMITS') and review.get('reviewerRole')=='DID_NOT_BUILD_OR_EXECUTE')
    for name in ('register.graphql','register.variables.json','verify_release.py','proposal.json','rollback.variables.json'):
        ck('reviewed_binding:'+name,review.get('bindings',{}).get(name)==digest(HERE/name))
    ck('exact_variable_names',set(variables)=={f'{p}{i}' for i in range(9) for p in ('resource','translations')})
    ck('shop_identity',new['shop']==before['shop'] and new['shop']['id']=='gid://shopify/Shop/15571635' and new['shop']['myshopifyDomain']=='dresslikemommy-com.myshopify.com')
    ck('ten_resources',set(n)==set(b) and len(n)==10)
    ck('all_source_pagination_complete',not new['translatableResourcesByIds']['pageInfo']['hasNextPage'] and not new['markets']['pageInfo']['hasNextPage'] and all(not p['variants']['pageInfo']['hasNextPage'] for p in new['nodes']))
    ck('active_products_and_167_complete_variants',len(new['nodes'])==10 and all(p['status']=='ACTIVE' for p in new['nodes']) and sum(len(p['variants']['nodes']) for p in new['nodes'])==167)
    ck('published_locales_exact',new['shopLocales']==before['shopLocales'])
    ck('italian_published',any(x['locale']=='it' and x['published'] for x in new['shopLocales']))
    ck('market_configuration_exact',new['markets']==before['markets'])
    ck('native_products_variants_prices_status_source_exact',new['nodes']==before['nodes'])
    expected={}
    for i,(pid,keys) in enumerate(SCOPE):
        rid='gid://shopify/Product/'+pid
        ck(f'{pid}:exact_resource',variables.get('resource'+str(i))==rid)
        inputs=variables['translations'+str(i)]
        ck(f'{pid}:exact_keys',len(inputs)==len(keys) and {x['key'] for x in inputs}==set(keys))
        expected[rid]={x['key']:x for x in inputs}
        source=by_key(b[rid]['translatableContent']); old=by_key(b[rid]['italian'])
        for t in inputs:
            k=t['key']
            ck(f'{pid}/{k}:italian_global_only',set(t)=={'locale','key','value','translatableContentDigest','marketId'} and t['locale']=='it' and t['marketId'] is None)
            ck(f'{pid}/{k}:current_source_digest',t['translatableContentDigest']==source[k]['digest'])
            ck(f'{pid}/{k}:existing_outdated_field',old[k]['outdated'] is True)
            ck(f'{pid}/{k}:nonempty_actual_correction',bool(t['value'].strip()) and t['value']!=old[k]['value'])
            ck(f'{pid}/{k}:no_private_url_or_script',not re.search(r'(?:https?://[^\s<>]*?(?:alicdn|alibaba|aliexpress|1688|taobao|tmall|admin\.shopify)|<script\b)',t['value'],re.I))
    ck('exact_24_inputs',sum(len(x) for x in expected.values())==24)
    for rid in b:
        ck(rid+':english_exact',n[rid]['translatableContent']==b[rid]['translatableContent'])
        for lang in ('spanish','french','german'):
            ck(rid+':'+lang+'_exact',n[rid][lang]==b[rid][lang])
        old=by_key(b[rid]['italian']); current=by_key(n[rid]['italian'])
        ck(rid+':italian_key_set_preserved',set(old)==set(current))
        for k,x in old.items():
            target=expected.get(rid,{}).get(k)
            if mode=='before' or target is None:
                ck(rid+'/'+k+':exact_preservation',current.get(k)==x)
            else:
                y=current[k]
                ck(rid+'/'+k+':exact_saved_value',y['value']==target['value'])
                ck(rid+'/'+k+':fresh_global_italian',y['locale']=='it' and y['market'] is None and y['outdated'] is False and bool(y['updatedAt']))
    base_overrides=read(HERE/'market_overrides_before.json')['data']
    current_overrides=read(override)['data']
    ck('all_market_overrides_exact',base_overrides==current_overrides)
    override_rows=current_overrides['translatableResourcesByIds']['nodes']
    ck('sixty_empty_global_override_contexts',len(override_rows)==10 and all(row[market]==[] for row in override_rows for market in ('au','ca','eu','international','gb','us')))
    ck('override_pagination_complete',not current_overrides['translatableResourcesByIds']['pageInfo']['hasNextPage'])
    if mode=='before':
        now=datetime.now(timezone.utc)
        ck('live_snapshot_under_five_minutes',0 <= (now-time(read(snapshot)['observed']['receivedAt'])).total_seconds() <= 300)
        ck('live_override_snapshot_under_five_minutes',0 <= (now-time(read(override)['observed']['receivedAt'])).total_seconds() <= 300)
        ck('original_source_under_two_hours',0 <= (now-time(read(raw)['observed']['receivedAt'])).total_seconds() <= 7200)
    return {'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','mode':mode,'verifiedAtUTC':datetime.now(timezone.utc).isoformat(),'checkCount':len(checks),'failed':[x['check'] for x in checks if not x['pass']],'checks':checks,'bindings':{str(p):digest(p) for p in (raw,snapshot,override,HERE/'register.variables.json',HERE/'register.graphql')},'externalWritesByThisVerifier':0}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['before','after']);p.add_argument('snapshot',type=Path);p.add_argument('override',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();result=verify(a.mode,a.snapshot,a.override);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','mode','checkCount','failed')}))
    raise SystemExit(0 if result['status']=='PASS' else 1)
