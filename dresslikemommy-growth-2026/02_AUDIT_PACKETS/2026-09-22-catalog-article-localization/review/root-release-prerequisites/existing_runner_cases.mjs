import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
const here=path.dirname(new URL(import.meta.url).pathname);
const runner=fs.readFileSync(path.resolve(here,'../../tooling/guarded_release_runner.js'),'utf8');
const cases=['success','source_drift','before_drift','supporting_source_drift','unpublished','missing_alias','mutation_user_error','after_query_error','after_value_mismatch','after_outdated','after_pagination','receipt_throws','pending_resume'];
const results=[];
for(const type of cases){
 const id='gid://shopify/Article/1', row={resourceId:id,locale:'he',key:'body_html',sourceValue:'<p>source</p>',sourceDigest:'digest',before:{value:'old',outdated:false},value:'<p>חדש</p>',supportingSourceDigests:{title:'title-digest'}};
 const state=new Map([['test',[row]],['catalogPacket','mock'],['catalogGenericQuery','query'],['catalogGenericMutation1','mutation']]);
 if(type==='pending_resume')state.set('testPending',{status:'MUTATION_REQUESTED'});
 let queryCount=0,mutations=0,patches=0;const output=[];
 function response(after=false){return {structuredContent:{data:{scope:[{id,isPublished:type!=='unpublished'}],translatableResourcesByIds:{nodes:[{resourceId:id,translatableContent:[{key:'body_html',value:type==='source_drift'?'drift':row.sourceValue,digest:'digest'},{key:'title',value:'title',digest:type==='supporting_source_drift'?'changed':'title-digest'}],tr_he:[{key:'body_html',locale:'he',market:null,value:after?(type==='after_value_mismatch'?'wrong':row.value):(type==='before_drift'?'changed':'old'),outdated:after&&type==='after_outdated'}]}],pageInfo:{hasNextPage:after&&type==='after_pagination'}}}}};}
 const context={load:k=>state.get(k),store:(k,v)=>state.set(k,v),text:x=>output.push(x),setTimeout:fn=>fn(),Promise,tools:{
  mcp__codex_apps__shopify_graphql_query:async()=>{queryCount++;return queryCount===2&&type==='after_query_error'?{isError:true,content:['mock']} :response(queryCount>1);},
  mcp__codex_apps__shopify_graphql_mutation:async()=>{mutations++;return {structuredContent:{data:type==='missing_alias'?{}:{r0:{translations:[{locale:'he',key:'body_html',value:row.value,outdated:false}],userErrors:type==='mutation_user_error'?[{message:'mock'}]:[]}}}};},
  apply_patch:async()=>{patches++;if(type==='receipt_throws'&&patches===2)throw Error('mock receipt failure');return {success:true};}
 }};
 let error=null;try{await vm.runInNewContext('('+runner+')',context)('test',1);}catch(e){error=e.message;}
 const expectMutation=['success','missing_alias','mutation_user_error','after_query_error','after_value_mismatch','after_outdated','after_pagination','receipt_throws'].includes(type)?1:0;
 const ok=mutations===expectMutation && (type==='success'?(state.get('testOffset')===1&&!state.get('testPending')):!state.get('testOffset')) && (expectMutation===1&&type!=='success'?!!state.get('testPending'):true);
 results.push({case:type,status:ok?'PASS':'FAIL',mutations,queryCount,patches,offset:state.get('testOffset')??0,pending:!!state.get('testPending'),caughtError:error});
}
const report={status:results.every(x=>x.status==='PASS')?'PASS':'FAIL',review:'Independent local mocks; no API/provider/network/browser/Git calls',runnerSHA256:crypto.createHash('sha256').update(runner).digest('hex'),cases:results};
fs.writeFileSync(path.join(here,'existing_runner_cases_result.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,cases:results.length,failures:results.filter(x=>x.status==='FAIL')}));
