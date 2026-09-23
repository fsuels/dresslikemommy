async function(key,count){
if(load(key+"Pending"))throw Error("Pending mutation requires explicit read-only recovery before resuming "+key);
const all=load(key), idsAll=[...new Set(all.map(r=>r.resourceId))]; let pos=load(key+"Offset")||0, fields=0,done=0;
for(;done<count&&pos<idsAll.length;done++,pos+=5){
const ids=idsAll.slice(pos,pos+5),rows=all.filter(r=>ids.includes(r.resourceId));
const scopeIds=[...new Set(rows.map(r=>r.productId||r.resourceId))];
const vars={ids,scopeIds};
const b=await tools.mcp__codex_apps__shopify_graphql_query({query:load("catalogGenericQuery"),variables:vars});
const data=b.structuredContent?.data,c=data?.translatableResourcesByIds;
if(b.isError||!c||c.pageInfo.hasNextPage||c.nodes.length!==ids.length){store(key+"Failure",{phase:"before",pos,result:b});text({key,stopped:pos,phase:"before",error:b.structuredContent||b.content});return;}
if(data.scope.length!==scopeIds.length||data.scope.some(n=>!n||(!n.isPublished&&(n.status!=="ACTIVE"||!n.onlineStoreUrl))))throw Error("Publication drift "+pos);
for(const r of rows){
 const n=c.nodes.find(n=>n.resourceId===r.resourceId),s=n.translatableContent.find(s=>s.key===r.key),old=n["tr_"+r.locale.replace("-","_")].filter(t=>t.locale===r.locale&&!t.market&&t.key===r.key);
 if(s?.value!==(r.sourceValue??r.source)||s.digest!==r.sourceDigest)throw Error("Source drift "+r.resourceId+"/"+r.key);
 for(const [k,d]of Object.entries(r.supportingSourceDigests||{})) if(n.translatableContent.find(s=>s.key===k)?.digest!==d)throw Error("Supporting source drift "+r.resourceId+"/"+k);
 if(r.before===null ? old.length!==0 : old.length!==1||old[0].value!==r.before.value||old[0].outdated!==r.before.outdated)throw Error("Before drift "+r.resourceId+"/"+r.locale+"/"+r.key);
}
const v={};ids.forEach((id,i)=>{v["id"+i]=id;v["tr"+i]=rows.filter(r=>r.resourceId===id).map(r=>({locale:r.locale,key:r.key,value:r.value,translatableContentDigest:r.sourceDigest}));});
store(key+"Pending",{pos,ids,rows:rows.length,status:"MUTATION_REQUESTED"});
await tools.apply_patch("*** Begin Patch\n*** Add File: "+load("catalogPacket")+"/releases/"+key+"_"+String(pos).padStart(4,"0")+"_intent.json\n+"+JSON.stringify({pos,ids,fields:rows.length,status:"MUTATION_REQUESTED",vars:v},null,2).split("\n").join("\n+")+"\n*** End Patch");
const m=await tools.mcp__codex_apps__shopify_graphql_mutation({query:load("catalogGenericMutation"+ids.length),variables:v}),md=m.structuredContent?.data;
store(key+"LastMutation",{pos,ids,rows:rows.length,mutation:md});
if(m.isError||!md||Object.keys(md).length!==ids.length||ids.some((_,i)=>!md["r"+i]||md["r"+i].userErrors?.length)){store(key+"Failure",{phase:"mutation",pos,result:m});text({key,stopped:pos,phase:"mutation",error:m.structuredContent||m.content});return;}

const a=await tools.mcp__codex_apps__shopify_graphql_query({query:load("catalogGenericQuery"),variables:vars}),nn=a.structuredContent?.data?.translatableResourcesByIds?.nodes;
if(a.isError||!nn||nn.length!==ids.length||a.structuredContent.data.translatableResourcesByIds.pageInfo.hasNextPage){store(key+"Failure",{phase:"after",pos,result:a});text({key,stopped:pos,phase:"after",error:a.structuredContent||a.content});return;}
for(const r of rows){const n=nn.find(n=>n.resourceId===r.resourceId),t=n["tr_"+r.locale.replace("-","_")].filter(t=>t.locale===r.locale&&!t.market&&t.key===r.key);if(t.length!==1||t[0].value!==r.value||t[0].outdated)throw Error("After mismatch "+r.resourceId+"/"+r.locale+"/"+r.key);}
const rec={cohort:key,resourceOffset:pos,resourceIds:ids,fields:rows.length,beforeSourceAndTranslationGuard:"PASS",publicationGuard:"PASS",afterExactValueAndCurrentGuard:"PASS",mutation:md};
await tools.apply_patch("*** Begin Patch\n*** Add File: "+load("catalogPacket")+"/releases/"+key+"_"+String(pos).padStart(4,"0")+".json\n+"+JSON.stringify(rec,null,2).split("\n").join("\n+")+"\n*** End Patch");
store(key+"Pending",null);store(key+"Offset",pos+ids.length);
fields+=rows.length;await new Promise(resolve=>setTimeout(resolve,2000));
}
text({cohort:key,completedResources:load(key+"Offset"),totalResources:idsAll.length,newVerifiedFields:fields,batches:done});
}
