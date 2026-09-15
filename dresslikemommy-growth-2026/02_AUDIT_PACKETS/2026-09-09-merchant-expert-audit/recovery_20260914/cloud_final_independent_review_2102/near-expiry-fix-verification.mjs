import assert from 'node:assert/strict';
import { readFile,writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createConfiguredAdminReader } from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/admin-reader.js';
const authHash=createHash('sha256').update(await readFile('/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/shopify-auth.js')).digest('hex');
assert.equal(authHash,'11c3253ff5a5a4afcdf15d32e46d368a656078d604f769f918079b720256a8d3');
const config={storeDomain:'fixture-expiry-fixed-review.myshopify.com',apiVersion:'2026-07'};
const env={SHOPIFY_AUTH_MODE:'client_credentials',SHOPIFY_CLIENT_ID:'synthetic-review-fixed-expiry-id',SHOPIFY_CLIENT_SECRET:'synthetic-review-fixed-expiry-secret'};
let time=Date.parse('2026-09-14T00:00:00Z'),issuedAt=time,exchanges=0,adminCalls=0;
const options={now:()=>time,fetchImpl:async(url,request)=>{
 if(url.endsWith('/admin/oauth/access_token')){exchanges++;issuedAt=time;return new Response(JSON.stringify({access_token:'synthetic-review-fixed-token-'+exchanges,scope:'read_products',expires_in:86399}),{headers:{'Content-Type':'application/json'}});}
 adminCalls++;
 if(time>=issuedAt+86399_000)return new Response('{}',{status:401});
 time+=50000;
 return new Response(JSON.stringify({data:{products:{nodes:[]}}}),{headers:{'Content-Type':'application/json'}});
}};
await createConfiguredAdminReader(env,config,options);
time=issuedAt+86399_000-61000;
const read=await createConfiguredAdminReader(env,config,options);
assert.equal(exchanges,2,'Refresh the near-expiry cache before returning a reader');
for(let i=0;i<18;i++) await read('query SyntheticExpiryCase { products(first: 1) { nodes { id } } }',{});
assert.equal(exchanges,2,'No per-Admin OAuth calls');
assert.equal(adminCalls,18);
const result={status:'PASS_EXPIRY_DEFECT_FIXED',authSha256:authHash,case:'A warm cached token with 61 seconds remaining is replaced before the reader is created; 18 simulated 50-second Admin operations complete without another exchange or expired-token use.',exchangesAcrossTwoReaders:exchanges,exchangesInsideNewConsumer:1,adminCalls,simulatedConsumerDurationSeconds:900,realNetworkCalls:0,sourceCredentials:'synthetic only'};
await writeFile(new URL('near-expiry-fix-verification.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
