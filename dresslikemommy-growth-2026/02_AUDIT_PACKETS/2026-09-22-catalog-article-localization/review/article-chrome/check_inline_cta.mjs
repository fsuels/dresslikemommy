import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const dir=dirname(fileURLToPath(import.meta.url));
const input=JSON.parse(readFileSync(join(dir,'js_fixtures.json'),'utf8'));
const results=[];
function execute(script,{paragraphCount=8,data=null,hasContent=true}={}) {
  const inserted=[];
  const parent={insertBefore(node,nextSibling){inserted.push({node,nextSibling});}};
  const paragraphs=Array.from({length:paragraphCount},(_,i)=>({parentNode:parent,nextSibling:i+1}));
  const content={querySelectorAll(selector){assert.equal(selector,'p');return paragraphs;}};
  const document={
    querySelector(selector){
      if(selector==='.article-template__content')return hasContent?content:null;
      if(selector==='.article-template__inline-cta-data')return data?{getAttribute(key){return data[key]??null;}}:null;
      throw new Error('Unexpected selector '+selector);
    },
    createElement(tag){return {tag,className:'',textContent:'',attrs:{},children:[],appendChild(child){this.children.push(child);},setAttribute(key,value){this.attrs[key]=value;}};}
  };
  new vm.Script(script).runInNewContext({document});
  return inserted;
}
for (const f of input.fixtures) {
  const fallback=execute(f.script);assert.equal(fallback.length,1);
  const [copy,link]=fallback[0].node.children;
  assert.equal(copy.textContent,f.expectedText);assert.equal(link.textContent,f.expectedLabel);assert.equal(link.href,f.expectedUrl);
  assert.equal(fallback[0].nextSibling,4);assert.deepEqual(link.attrs,{});
  const data={'data-inline-cta-text':f.expectedText+' " & <test>','data-inline-cta-label':f.expectedLabel+' " & <test>','data-inline-cta-url':f.expectedUrl.replace('matching-outfits','dresses'),'data-inline-cta-article-handle':'a-stable-article-handle','data-inline-cta-collection-handle':'dresses'};
  const chosen=execute(f.script,{data})[0].node.children;
  assert.equal(chosen[0].textContent,data['data-inline-cta-text']);assert.equal(chosen[1].textContent,data['data-inline-cta-label']);assert.equal(chosen[1].href,data['data-inline-cta-url']);
  assert.equal(chosen[1].attrs['data-style-journal-destination-title'],data['data-inline-cta-label']);assert.equal(chosen[1].attrs['data-style-journal-source-article-handle'],'a-stable-article-handle');assert.equal(chosen[1].attrs['data-style-journal-destination-handle'],'dresses');
  assert.equal(execute(f.script,{paragraphCount:5}).length,0);assert.equal(execute(f.script,{hasContent:false}).length,0);
  if(f.locale==='en'){
    assert.equal(JSON.stringify(fallback),JSON.stringify(execute(input.beforeEnglishScript)));
    assert.equal(JSON.stringify(execute(f.script,{data})),JSON.stringify(execute(input.beforeEnglishScript,{data})));
  }
  results.push({locale:f.locale,checks:['script parses','localized missing-data fallback','selected destination preserved','literal text safely assigned through textContent','tracking preserved','paragraph placement','short-content guard','missing-content guard',...(f.locale==='en'?['English before/after fallback and selected-data outputs identical']:[])]});
}
writeFileSync(join(dir,'inline_cta_results.json'),JSON.stringify({status:'PASS',locales:results.length,results},null,2)+'\n');
console.log('PASS actual inline-CTA JavaScript for21 locales: fallbacks, selected routes, literal text, tracking, guards, placement; English before/after identical.');
