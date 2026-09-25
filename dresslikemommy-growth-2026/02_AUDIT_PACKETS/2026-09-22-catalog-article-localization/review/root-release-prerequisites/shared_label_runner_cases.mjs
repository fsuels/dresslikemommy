import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
const here=path.dirname(new URL(import.meta.url).pathname), base=path.resolve(here,'../..');
const runner=fs.readFileSync(path.join(base,'tooling/guarded_release_runner.js'),'utf8');
const rows=JSON.parse(fs.readFileSync(path.join(base,'review/shared_colors_release_scope.json'),'utf8'));
const links=JSON.parse(fs.readFileSync(path.join(base,'review/shared_colors_live_product_links.json'),'utf8'));
const checks=rows.map(r=>{
 const p=links.readback.data.nodes.find(p=>p.id===r.productId),o=p?.options.find(o=>o.id===r.linkedOptionId),v=o?.optionValues.find(v=>v.id===r.linkedOptionValueId);
 const ok=p?.status==='ACTIVE'&&!!p.onlineStoreUrl&&v?.hasVariants===true&&v.linkedMetafieldValue===r.resourceId;
 return {resourceId:r.resourceId,locale:r.locale,productId:r.productId,optionId:r.linkedOptionId,optionValueId:r.linkedOptionValueId,hasVariants:v?.hasVariants,linkedMetafieldValue:v?.linkedMetafieldValue,status:ok?'PASS':'FAIL'};
});
const types=['linked_success','missing_product_mapping','missing_option_mapping','missing_value_mapping','changed_link','inactive_parent','unpublished_parent','wrong_parent','wrong_option','wrong_option_value','has_variants_false','options_missing'];
const results=[];
for(const type of types){
 const id='gid://shopify/Metaobject/1',pid='gid://shopify/Product/1',oid='gid://shopify/ProductOption/1',vid='gid://shopify/ProductOptionValue/1';
 const row={resourceId:id,productId:pid,linkedOptionId:oid,linkedOptionValueId:vid,locale:'ru',key:'label',source:'Red',sourceDigest:'digest',before:null,value:'Красный'};
 if(type==='missing_product_mapping')delete row.productId;
 if(type==='missing_option_mapping')delete row.linkedOptionId;
 if(type==='missing_value_mapping')delete row.linkedOptionValueId;
 const state=new Map([['test',[row]],['catalogPacket','mock'],['catalogGenericQuery','GENERIC'],['catalogGenericLinkedQuery','LINKED'],['catalogGenericMutation1','MUTATION']]);
 let queryCount=0,mutations=0,patches=0;const querySelections=[];
 const option={id:type==='wrong_option'?'wrong':oid,optionValues:[{id:type==='wrong_option_value'?'wrong':vid,hasVariants:type!=='has_variants_false',linkedMetafieldValue:type==='changed_link'?'gid://shopify/Metaobject/2':id}]};
 const p={id:type==='wrong_parent'?'wrong':pid,status:type==='inactive_parent'?'DRAFT':'ACTIVE',onlineStoreUrl:type==='unpublished_parent'?null:'https://example.invalid/products/one',...(type==='options_missing'?{}:{options:[option]})};
 const context={load:k=>state.get(k),store:(k,v)=>state.set(k,v),text:()=>{},setTimeout:fn=>fn(),Promise,tools:{
 mcp__codex_apps__shopify_graphql_query:async({query,variables})=>{querySelections.push(query);queryCount++;return {structuredContent:{data:{scope:[p],translatableResourcesByIds:{nodes:[{resourceId:id,translatableContent:[{key:'label',value:'Red',digest:'digest'}],tr_ru:queryCount>1?[{locale:'ru',key:'label',market:null,value:row.value,outdated:false}]:[]}],pageInfo:{hasNextPage:false}}}}};},
 mcp__codex_apps__shopify_graphql_mutation:async()=>{mutations++;return {structuredContent:{data:{r0:{translations:[],userErrors:[]}}}};},apply_patch:async()=>{patches++;return {success:true};}}};
 let error=null;try{await vm.runInNewContext('('+runner+')',context)('test',1)}catch(e){error=e.message}
 const ok=querySelections.every(q=>q==='LINKED')&&(type==='linked_success'?mutations===1&&state.get('testOffset')===1&&!state.get('testPending'):mutations===0&&!state.get('testOffset')&&!state.get('testPending')&&!!error);
 results.push({case:type,status:ok?'PASS':'FAIL',queryCount,mutations,patches,offset:state.get('testOffset')??0,pending:!!state.get('testPending'),querySelections,caughtError:error});
}
const report={status:[...checks,...results].every(x=>x.status==='PASS')?'PASS':'FAIL',runnerSHA256:crypto.createHash('sha256').update(runner).digest('hex'),scopeFields:rows.length,sharedResources:new Set(rows.map(x=>x.resourceId)).size,sourceReadbackAt:links.at,scopeEvidenceChecks:checks,cases:results,limits:'Offline mocks and exact persisted readback reconciliation; does not independently execute or validate the GraphQL query schema. Root must retain current source/before/publication/link guards and exact after readback.'};
fs.writeFileSync(path.join(here,'shared_label_runner_cases_result.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,evidence:checks.length,cases:results.length,failures:[...checks,...results].filter(x=>x.status==='FAIL')}));
