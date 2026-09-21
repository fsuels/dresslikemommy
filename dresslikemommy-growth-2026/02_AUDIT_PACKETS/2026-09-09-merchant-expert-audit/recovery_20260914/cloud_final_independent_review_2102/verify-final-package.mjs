import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {runtimeConfig,refreshMarket,currentManifest} from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/worker.js';
import {enqueueRefresh} from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/checkpoint.js';
import {config as fixtureConfig,market,product,source,Bucket} from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/test/fixtures.js';
const pipe='/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/', activation='/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260914/cloud_activation_review_2042/';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const json=async file=>JSON.parse(await readFile(file,'utf8'));
const receiptFile=path.join(activation,'integration_validation_final.json');
const receipt=await json(receiptFile);
for(const [name,expected]of Object.entries(receipt.files))assert.equal(sha(await readFile(path.join(pipe,name))),expected,name);
for(const [name,expected]of Object.entries(receipt.bundleFiles))assert.equal(sha(await readFile(path.join(activation,name))),expected,name);
const map=await json(path.join(activation,'package-final/automation.js.map'));
assert.equal(map.sources.length,11);assert.equal(map.sourcesContent.length,11);
for(let i=0;i<map.sources.length;i++){
 const filename='src/'+path.basename(map.sources[i]);
 assert.equal(sha(map.sourcesContent[i]),receipt.files[filename],filename+' source-map equality');
}
const metadata=await json(path.join(activation,'package-final/bundle-meta.json'));
assert.equal(Object.keys(metadata.inputs).length,11);
const bundleMeta=Object.values(metadata.outputs).find(v=>v.entryPoint==='src/automation.js');
assert.deepEqual(bundleMeta.imports,[]);
assert.equal(bundleMeta.bytes,(await readFile(path.join(activation,'package-final/automation.js'))).length);
const bindings=JSON.parse(execFileSync('/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',['-c',
 'import json,tomllib,sys; d=tomllib.load(open(sys.argv[1],"rb")); assert set(d["vars"])=={"SHOPIFY_AUTH_MODE","MERCHANT_CONFIG_JSON","MERCHANT_ELIGIBILITY_HOLDS_JSON"}; print(json.dumps(d["vars"]))',
 path.join(pipe,'wrangler.toml')],{encoding:'utf8'}));
assert.equal(bindings.SHOPIFY_AUTH_MODE,'client_credentials');
const reviewed=await json(path.join(pipe,'config.json')), effective=runtimeConfig(bindings);
assert.deepEqual(effective,reviewed);
assert.equal(JSON.stringify(effective),JSON.stringify(reviewed));
assert.equal(effective.eligibilityHolds.holds.length,6);
const sizes=Object.fromEntries(Object.entries(bindings).map(([key,value])=>[key,Buffer.byteLength(value)]));
assert.ok(Object.values(sizes).every(bytes=>bytes<5000));
assert.deepEqual(effective.markets.filter(m=>m.enabled).map(m=>m.key),['us-en']);
const wrong=[
 {...bindings,MERCHANT_ELIGIBILITY_HOLDS_JSON:undefined},
 {...bindings,MERCHANT_ELIGIBILITY_HOLDS_JSON:'null'},
 {...bindings,MERCHANT_ELIGIBILITY_HOLDS_JSON:'['},
 {...bindings,MERCHANT_CONFIG_JSON:JSON.stringify(reviewed)},
 {...bindings,MERCHANT_CONFIG_JSON:JSON.stringify({...reviewed,eligibilityHoldsExternal:true})},
 {...bindings,MERCHANT_CONFIG_JSON:JSON.stringify({...JSON.parse(bindings.MERCHANT_CONFIG_JSON),eligibilityHoldsExternal:false})},
];
for(const bad of wrong)assert.throws(()=>runtimeConfig(bad),error=>error.code==='feed_config_missing_or_invalid');
assert.ok((await readFile(path.resolve(activation,receipt.priorHoldReview))).length>0);
assert.ok((await readFile(path.resolve(activation,receipt.tokenRepairReceipt))).length>0);

const bundle=(await import(pathToFileURL(path.join(activation,'package-final/automation.js')))).default;
assert.deepEqual(Object.keys(bundle).sort(),['fetch','queue','scheduled']);
assert.equal((await bundle.fetch(new Request('https://fixture-worker.example/health'),{})).status,200);
const cfg=structuredClone(fixtureConfig);cfg.storeDomain='fixture-bundle-failure.myshopify.com';cfg.eligibilityHolds=reviewed.eligibilityHolds;
const store=new Bucket(), queue={messages:[],async send(m){this.messages.push(m);}};
const env={MERCHANT_CONFIG_JSON:JSON.stringify(cfg),MERCHANT_FEED_BUCKET:store,MERCHANT_REFRESH_QUEUE:queue};
await refreshMarket(env,market.key,{graphql:source([product()]).graphql,now:()=>new Date()});
const prior=await currentManifest(store,market.key);
const base=structuredClone(cfg);delete base.eligibilityHolds;base.eligibilityHoldsExternal=true;
env.MERCHANT_CONFIG_JSON=JSON.stringify(base);
env.MERCHANT_ELIGIBILITY_HOLDS_JSON=JSON.stringify(reviewed.eligibilityHolds);
env.SHOPIFY_AUTH_MODE='client_credentials';env.SHOPIFY_CLIENT_ID='synthetic-bundle-review-id';env.SHOPIFY_CLIENT_SECRET='synthetic-bundle-review-secret';
Object.defineProperty(env,'SHOPIFY_ADMIN_ACCESS_TOKEN',{get(){throw Error('Legacy credential getter must never run');}});
await enqueueRefresh(env,market.key);
let authRequests=0,acked=0,retried=0;
const originalFetch=globalThis.fetch;
globalThis.fetch=async(url,request)=>{
 authRequests++;assert.equal(url,'https://fixture-bundle-failure.myshopify.com/admin/oauth/access_token');
 assert.equal(request.redirect,'error');
 return new Response(JSON.stringify({access_token:'synthetic-overprivileged-token',scope:'read_products,write_products',expires_in:86399}),{headers:{'Content-Type':'application/json'}});
};
try{
 await bundle.queue({messages:[{body:queue.messages.shift(),ack(){acked++;},retry(){retried++;}}]},env);
}finally{globalThis.fetch=originalFetch;}
assert.equal(authRequests,1);assert.equal(acked,1);assert.equal(retried,0);
assert.deepEqual(await currentManifest(store,market.key),prior);
const status=JSON.parse(await(await store.get('merchant/us-en/status.json')).text());
const control=JSON.parse(await(await store.get('merchant/us-en/refresh.json')).text());
assert.equal(status.code,'shopify_auth_scope_not_allowed');assert.equal(control.status,'FAILED');
assert.ok(!JSON.stringify([...store.objects]).includes('synthetic-overprivileged-token'));
assert.ok(!JSON.stringify([...store.objects]).includes(env.SHOPIFY_CLIENT_SECRET));
const served=await bundle.fetch(new Request('https://fixture-worker.example/feeds/us-en.tsv'),env);
assert.equal(served.status,200);assert.equal(served.headers.get('X-DLM-Feed-Rows'),'1');
assert.equal((await bundle.fetch(new Request('https://fixture-worker.example/feeds/us-en.tsv',{method:'POST'}),env)).status,405);
const result={status:'PASS_FINAL_LOCAL_PACKAGE_AND_BINDING',checkedAt:new Date().toISOString(),integrationReceiptSha256:sha(await readFile(receiptFile)),
 verifiedSourceHashes:receipt.files,verifiedBundleHashes:receipt.bundleFiles,bundledSourceContentsMatch:true,modules:11,bundleBytes:bundleMeta.bytes,
 bindingBytes:sizes,effectiveConfigExactAndFingerprintPreserved:true,holds:6,enabledMarkets:['us-en'],invalidBindingCasesRejected:wrong.length,
 evidenceLinksExist:true,bundledAuthFailure:{authRequests,legacyFallback:false,controlStatus:control.status,statusCode:status.code,priorPointerPreserved:true,messageAcked:true,secretMaterialPersisted:false,existingImmutableFeedStillServed:true,publicPostRejected:true},
 actualDeployment:false,realNetworkCalls:0,realCredentialsRead:false,
 limits:['Real dedicated grant eligibility, scopes, full source read, cloud plan/resources and live refresh remain unverified.','No claim of Merchant source receipt or market buyer readiness.']};
await writeFile(new URL('final-package-verification.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,modules:result.modules,bindingBytes:sizes,bundledAuthFailure:result.bundledAuthFailure}));
