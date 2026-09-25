#!/usr/bin/env python3
"""Read-only exhaustive catalog translation snapshot; no provider calls or writes."""
from __future__ import annotations
import hashlib,json,re,sys,time,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'ops/scripts/shopify_admin_config.py').exists())
sys.path.insert(0,str(ROOT/'ops/scripts'))
from shopify_admin_config import resolve_store_domain,load_access_token
DOMAIN=resolve_store_domain()
TOKEN=load_access_token()
URL='https://'+DOMAIN+'/admin/api/2026-07/graphql.json'
LEDGER=[]
def now(): return datetime.now(timezone.utc).isoformat()
def save(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def gql(query,variables=None):
    assert query.lstrip().startswith('query '), 'Read-only queries only'
    req=urllib.request.Request(URL,data=json.dumps({'query':query,'variables':variables or {}}).encode(),headers={'Content-Type':'application/json','X-Shopify-Access-Token':TOKEN})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req,timeout=90) as r: result=json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (500,502,503,504) and not attempt: time.sleep(2);continue
            raise RuntimeError('Admin HTTP '+str(e.code)+'; stopped without dumping response') from None
        except (TimeoutError,urllib.error.URLError):
            if not attempt:time.sleep(2);continue
            raise RuntimeError('Admin transport failure after one retry') from None
    if result.get('errors'):
        codes=[e.get('extensions',{}).get('code','SCHEMA_OR_QUERY_ERROR') for e in result['errors']]
        raise RuntimeError('Admin GraphQL error codes '+repr(codes)+'; stopped')
    c=result.get('extensions',{}).get('cost',{})
    LEDGER.append({'at':now(),'operation':query.split('(')[0].split('{')[0].strip(),'variables_sha256':hashlib.sha256(json.dumps(variables or {},sort_keys=True).encode()).hexdigest(),'cost':c})
    throttle=c.get('throttleStatus',{})
    remain=throttle.get('currentlyAvailable',1000);rate=throttle.get('restoreRate',50)
    wait=max(0,(950-remain)/rate) if remain<950 else 0
    if wait:time.sleep(min(wait,20))
    return result

def main():
    start=now(); products=[];after=None;pages=[]
    while True:
        raw=gql((HERE/'inventory.graphql').read_text(),{'after':after})
        page=raw['data']['products'];pages.append(page['pageInfo']);products.extend(page['nodes'])
        save('inventory_page_%03d.json'%len(pages),raw)
        print('inventory',len(pages),len(products),flush=True)
        if not page['pageInfo']['hasNextPage']:break
        after=page['pageInfo']['endCursor'];assert after
    assert len({p['id'] for p in products})==len(products)
    assert all(p['status']=='ACTIVE' and p['onlineStoreUrl'] for p in products)
    ids=[];ownership={}
    for p in products:
        ids.append(p['id']);ownership[p['id']]={'productId':p['id'],'kind':'Product','handle':p['handle']}
        for o in p['options']:
            ids.append(o['id']);ownership[o['id']]={'productId':p['id'],'kind':'ProductOption','optionName':o['name']}
            for v in o['optionValues']:
                ids.append(v['id']);ownership[v['id']]={'productId':p['id'],'optionId':o['id'],'kind':'ProductOptionValue','hasVariants':v['hasVariants']}
    assert len(ids)==len(set(ids))
    save('resource_ownership.json',ownership)
    summary={'startedAt':start,'inventoryCompletedAt':now(),'productCount':len(products),'inventoryPages':len(pages),'terminalPage':pages[-1],'resourceCounts':{k:sum(x['kind']==k for x in ownership.values()) for k in ['Product','ProductOption','ProductOptionValue']},'variantCount':sum(p['variantsCount']['count'] for p in products),'variantPrecision':sorted(set(p['variantsCount']['precision'] for p in products)),'onlineStoreUrlVerified':len(products),'resourceIds':len(ids)}
    save('inventory_summary.json',summary)
    query=(HERE/'translations.graphql').read_text();seen=set();batch_pages=0
    for batch,offset in enumerate(range(0,len(ids),40),1):
        selected=ids[offset:offset+40];after=None;subpage=0
        while True:
            raw=gql(query,{'ids':selected,'after':after});subpage+=1;batch_pages+=1
            connection=raw['data']['translatableResourcesByIds']
            for node in connection['nodes']:
                assert node['resourceId'] not in seen;seen.add(node['resourceId'])
                # Do not retain unnecessary vendor or routing-handle fields.
                for key,value in list(node.items()):
                    if isinstance(value,list):node[key]=[x for x in value if x.get('key') not in ('vendor','handle')]
            save('translations_batch_%03d_page_%02d.json'%(batch,subpage),raw)
            if not connection['pageInfo']['hasNextPage']:break
            after=connection['pageInfo']['endCursor'];assert after
        save('request_ledger.json',LEDGER)
        print('translations',batch,'resources',len(seen),'/',len(ids),flush=True)
    summary.update({'completedAt':now(),'translationBatchPages':batch_pages,'translationResourceCount':len(seen),'missingResourceIds':sorted(set(ids)-seen)})
    save('export_summary.json',summary);save('request_ledger.json',LEDGER)
    final=gql((HERE/'counts.graphql').read_text());save('counts_after.json',final)
    assert final['data']['published']['count']==len(products), 'Catalog count changed during export'
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        save('export_error.json',{'at':now(),'type':type(exc).__name__,'message':str(exc),'requestsCompleted':len(LEDGER)})
        save('request_ledger.json',LEDGER)
        print(type(exc).__name__+': '+str(exc),file=sys.stderr,flush=True);sys.exit(1)
