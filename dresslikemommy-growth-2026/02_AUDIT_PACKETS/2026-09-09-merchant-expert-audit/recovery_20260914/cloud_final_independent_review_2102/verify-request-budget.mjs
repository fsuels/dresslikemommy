import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { enqueueRefresh,consumeRefresh } from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/checkpoint.js';
import { config,market,product,source,Bucket } from '/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/test/fixtures.js';
const api=source(Array.from({length:30},(_,i)=>product(i+1)));
const bucket=new Bucket();const counts={get:0,put:0,delete:0,queueSend:0,authFetches:0,adminFetches:0};
for(const method of ['get','put','delete']){const original=bucket[method].bind(bucket);bucket[method]=async(...args)=>{counts[method]++;return original(...args);};}
const queue={messages:[],async send(message){counts.queueSend++;this.messages.push(message);}};
const env={MERCHANT_CONFIG_JSON:JSON.stringify({...config,refresh:{maxSourceCallsPerInvocation:20}}),MERCHANT_FEED_BUCKET:bucket,MERCHANT_REFRESH_QUEUE:queue,
 SHOPIFY_AUTH_MODE:'client_credentials',SHOPIFY_CLIENT_ID:'synthetic-request-budget-review',SHOPIFY_CLIENT_SECRET:'synthetic-budget-secret'};
const originalFetch=globalThis.fetch;let attempts=0;
globalThis.fetch=async(url,request)=>{
 if(url===`https://${config.storeDomain}/admin/oauth/access_token`){counts.authFetches++;return new Response(JSON.stringify({access_token:'synthetic-budget-token',scope:'read_products',expires_in:86399}),{headers:{'Content-Type':'application/json'}});}
 assert.equal(url,`https://${config.storeDomain}/admin/api/${config.apiVersion}/graphql.json`);
 assert.equal(request.redirect,'error');assert.equal(request.headers['X-Shopify-Access-Token'],'synthetic-budget-token');
 counts.adminFetches++;attempts++;
 if(attempts%2===1)return new Response('{}',{status:503});
 const {query,variables}=JSON.parse(request.body);
 return new Response(JSON.stringify({data:await api.graphql(query,variables)}),{headers:{'Content-Type':'application/json'}});
};
let result;
try {
 await enqueueRefresh(env,market.key);
 const before={...counts};
 result=await consumeRefresh(env,queue.messages.shift());
 const perConsumer=Object.fromEntries(Object.keys(counts).map(k=>[k,counts[k]-before[k]]));
 assert.equal(result.checkpointed,true);assert.equal(result.newCalls,20);
 assert.equal(perConsumer.authFetches,1);assert.equal(perConsumer.adminFetches,40);
 assert.ok(perConsumer.get+perConsumer.put+perConsumer.delete+perConsumer.queueSend<1000);
 const receipt={status:'PASS_SYNTHETIC_MAXIMUM_EXTERNAL_FETCH_REHEARSAL',perConsumer,logicalSourceCalls:result.newCalls,
 externalFetches:perConsumer.authFetches+perConsumer.adminFetches,checkpointed:true,realNetworkCalls:0,livePlanReadback:false,
 limitsSource:'https://developers.cloudflare.com/workers/platform/limits/',limitation:'Counts one deterministic checkpoint branch; does not prove live CPU, memory, wall time, account quota or grant eligibility.'};
 await writeFile(new URL('request-budget.json',import.meta.url),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt));
}finally{globalThis.fetch=originalFetch;}
