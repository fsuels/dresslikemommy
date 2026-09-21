import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { createConfiguredAdminReader } from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/admin-reader.js';
const config={storeDomain:'fixture-expiry-review.myshopify.com',apiVersion:'2026-07'};
const env={SHOPIFY_AUTH_MODE:'client_credentials',SHOPIFY_CLIENT_ID:'synthetic-review-expiry-id',SHOPIFY_CLIENT_SECRET:'synthetic-review-expiry-secret'};
let time=Date.parse('2026-09-14T00:00:00Z'), issuedAt=time, exchanges=0, adminCalls=0;
const options={now:()=>time,fetchImpl:async(url,request)=>{
 if(url.endsWith('/admin/oauth/access_token')){exchanges++;issuedAt=time;return new Response(JSON.stringify({access_token:'synthetic-review-token-'+exchanges,scope:'read_products',expires_in:86399}),{headers:{'Content-Type':'application/json'}});}
 adminCalls++;
 if(time>=issuedAt+86399_000) return new Response('{}',{status:401});
 time+=50000;
 return new Response(JSON.stringify({data:{products:{nodes:[]}}}),{headers:{'Content-Type':'application/json'}});
}};
await createConfiguredAdminReader(env,config,options);
time=issuedAt+86399_000-61000;
const read=await createConfiguredAdminReader(env,config,options);
assert.equal(exchanges,1);
await read('query SyntheticExpiryCase { products(first: 1) { nodes { id } } }',{});
await read('query SyntheticExpiryCase { products(first: 1) { nodes { id } } }',{});
let code=null;
try{await read('query SyntheticExpiryCase { products(first: 1) { nodes { id } } }',{});}catch(error){code=error.code;}
assert.equal(code,'shopify_http_401');
assert.equal(exchanges,1);
const result={status:'REPRODUCED_EXPIRY_WINDOW_FAILURE',case:'A new queue reader accepts a cached token with 61 seconds remaining, then two 50-second successful Admin operations exhaust that lifetime. Third read retains the expired token.',exchanges,adminCalls,resultCode:code,realShopifyExpirySeconds:86399,virtualSuccessfulOperationLatencySeconds:50,realNetworkCalls:0,credentials:'synthetic only',productionImplication:'A consumer can fail near token expiry even though its total runtime is well inside the 15-minute queue limit. Preserve fail-closed behavior, but guarantee sufficient remaining token lifetime for the entire consumer or resolve validity at each request.'};
await writeFile(new URL('near-expiry-reproduction.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
