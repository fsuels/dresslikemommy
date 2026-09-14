import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { runInContext } from 'node:vm';
import test from 'node:test';
const require=createRequire(import.meta.url);
const {JSDOM}=require('/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const read=(url)=>readFileSync(new URL(url,import.meta.url),'utf8');
const parse=(url)=>JSON.parse(read(url).replace(/^\s*\/\*[\s\S]*?\*\/\s*/,''));
const asset='assets/product-desktop-ux-20260513-ruler-sync.js';
const old=read('../candidate/'+asset), next=read('./proposed/'+asset);
const sourceRoot='../../2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/international_candidate/';
const bindingText=read(sourceRoot+'au-en.sku-template-binding_20260911.json');
assert.equal(createHash('sha256').update(bindingText).digest('hex'),'0b984b5a72b7374b88cdb43f81231c257c42575d52939b4a5e1631cf31c6c59d');
const binding=JSON.parse(bindingText), snapshot=parse(sourceRoot+'au-en.snapshot.json');
const byId=new Map(binding.products.map(p=>[p.id,p]));
const fixtures=new Map(snapshot.products.map(p=>{
 const bound=byId.get(p.id); assert(bound);const bv=new Map(bound.variants.map(v=>[v.id,v]));
 const options=p.variants[0].selectedOptions.map((o,i)=>({name:o.name,position:i+1}));
 const variants=p.variants.map(v=>{const s=bv.get(v.id);assert(s);assert.deepEqual(s.selectedOptions,v.selectedOptions);
 const price=Math.round(Number(v.contextualPricing.price.amount)*100);
 return {id:v.id.split('/').pop(),sku:s.sku,price,price_text:`$${(price/100).toFixed(2)} AUD`,available:v.availableForSale,
 title:s.selectedOptions.map(o=>o.value).join(' / '),...Object.fromEntries(s.selectedOptions.map((o,i)=>['option'+(i+1),o.value]))};});
 return [p.id.split('/').pop(),{options,variants,currency:'AUD',default_price_html:''}];
}));
const plain=v=>JSON.parse(JSON.stringify(v));
function harness(source,body='',width=1280){
 const dom=new JSDOM(`<!doctype html><html lang="en"><head></head><body>${body}</body></html>`,{url:'http://127.0.0.1/products/fixture',runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window,observers=[],errors=[];
 const NativeMutationObserver=w.MutationObserver;
 w.MutationObserver=class extends NativeMutationObserver{constructor(cb){super(cb);observers.push(this);}};
 w.addEventListener('error',event=>{errors.push(event.error);event.preventDefault();});
 w.fetch=()=>{throw Error('No network in regression');};
 w.matchMedia=q=>({matches:q.includes('max-width')?width<=749:width>=990,addEventListener(){},addListener(){}});
 w.IntersectionObserver=class{constructor(cb){this.cb=cb;this.targets=new Set();}observe(el){this.targets.add(el);}unobserve(el){this.targets.delete(el);}disconnect(){this.targets.clear();}};
 w.HTMLElement.prototype.scrollIntoView=function(){};w.scrollTo=()=>{};
 runInContext(source,dom.getInternalVMContext(),{filename:asset});
 return {dom,w,close:()=>{observers.forEach(o=>o.disconnect());w.close();assert.deepEqual(errors,[],'No uncaught fixture/runtime errors');}};
}
function groups(w,d){return plain(w.buildRoleGroups(d,{},true,{skipTypeFilter:!!w.detectImplicitTypeMapping(d).implicit}));}
function collisions(gs){const seen=new Map(),duplicates=[];for(const g of gs)for(const o of g.options){const key=JSON.stringify([g.roleKey,o.sizeLabel,Object.entries(o.axes).sort()]);if(seen.has(key))duplicates.push([seen.get(key),o.id]);else seen.set(key,o.id);}return duplicates;}
function coverage(gs){return gs.flatMap(g=>g.options.map(o=>o.id)).sort();}
const core=['7672336646241','7230336729185','7229828202593','7505372282977','7536992976993','7535944368225'];
const exceptions=['7516369715297','7516479848545'];

test('frozen V7 reproduces E1 empty builder and E2 six omitted height variants',()=>{const h=harness(old);try{
 assert.deepEqual(groups(h.w,fixtures.get(exceptions[0])),[]);
 const gs=groups(h.w,fixtures.get(exceptions[1]));assert.equal(coverage(gs).length,3);assert.equal(fixtures.get(exceptions[1]).variants.length,9);
 assert.equal(collisions(groups(h.w,fixtures.get('7536337125473'))).length,16);
}finally{h.close();}});

test('E1 and E2 use native picker for all raw size labels without invented roles or altered source',()=>{const h=harness(next);try{
 for(const id of exceptions){const data=fixtures.get(id),before=JSON.stringify(data);assert.equal(h.w.needsNativeVariantPicker(data),true);const size=h.w.findSizeOptionIndex(data.options);
 for(const v of data.variants){if(/cm/.test(v['option'+(size+1)]))assert.equal(h.w.getRoleInfoForVariant(v,data.options,size),null);}
 assert.equal(JSON.stringify(data),before);}
}finally{h.close();}});

test('currency and contextual price do not change coverage or role collision behavior',()=>{for(const code of [old,next]){const h=harness(code);try{
 for(const id of [...exceptions,'7536337125473',...core]){const a=fixtures.get(id),b={...a,currency:'USD',variants:a.variants.map(v=>({...v,price:v.price+123,price_text:'different contextual text'}))};
 const identity=gs=>gs.map(g=>[g.key,g.roleKey,g.options.map(o=>[o.id,o.sizeLabel,o.fullLabel,o.axes])]);assert.deepEqual(identity(groups(h.w,a)),identity(groups(h.w,b)));
 if(code===next)assert.equal(h.w.needsNativeVariantPicker(a),h.w.needsNativeVariantPicker(b));}
}finally{h.close();}}});

test('all 56 Trail Plaid variants retain exact explicit role and distinct selection identity',()=>{const h=harness(next);try{
 const data=fixtures.get('7536337125473'),before=JSON.stringify(data),gs=groups(h.w,data);assert.equal(data.variants.length,56);assert.equal(h.w.needsNativeVariantPicker(data),false);
 assert.equal(collisions(gs).length,0);assert.deepEqual(coverage(gs),data.variants.map(v=>v.id).sort());
 const idx=h.w.findSizeOptionIndex(data.options);
 for(const v of data.variants){const label=v['option'+(idx+1)],role=label.split(' ')[0].toLowerCase(),group=gs.find(g=>g.options.some(o=>o.id===v.id)),o=group.options.find(o=>o.id===v.id);
 assert.equal(group.roleKey,role);assert.equal(o.fullLabel,label);assert.equal(o.price,v.price);assert.equal(o.available,v.available);}
 assert.equal(JSON.stringify(data),before);
}finally{h.close();}});

test('six tested core products preserve the complete prior selector result',()=>{const a=harness(old),b=harness(next);try{
 for(const id of core){const d=fixtures.get(id);assert.equal(b.w.needsNativeVariantPicker(d),false);assert.deepEqual(groups(b.w,d),groups(a.w,d),id);}
}finally{a.close();b.close();}});

test('all 240 exact-SKU source products change grouping only for Trail Plaid; native fallback exactly E1/E2',()=>{const a=harness(old),b=harness(next);try{
 const changed=[],fallback=[];for(const [id,d]of fixtures){if(JSON.stringify(groups(a.w,d))!==JSON.stringify(groups(b.w,d)))changed.push(id);if(b.w.needsNativeVariantPicker(d))fallback.push(id);}
 assert.deepEqual(changed,['7536337125473']);assert.deepEqual(fallback.sort(),exceptions.slice().sort());
}finally{a.close();b.close();}});

const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function body(data){const controls=data.options.map((o,idx)=>`<div class="product-form__input"><label class="form__label">${esc(o.name)}</label><select name="options[${esc(o.name)}]" ${o.name==='Size'?'aria-describedby="size-conversion-message"':''}>${[...new Set(data.variants.map(v=>v['option'+(idx+1)]))].map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('')}</select></div>`).join('');return `
<style>.product__info-container--matching-set .product-form__buttons,.product__info-container--matching-set variant-selects>.product-form__input{display:none!important}</style>
<div id="ProductInfo-test" class="product__info-container product__info-container--matching-set" data-has-matching-set="true">
 <div id="price-test"><div class="price" data-price-current-text="${esc(data.variants[0].price_text)}"><div class="price__regular"><span class="price-item--regular">${esc(data.variants[0].price_text)}</span></div></div></div>
 <variant-selects id="variant-selects-test">${controls}</variant-selects><div id="size-conversion-message" hidden></div>
 <form id="product-form-test"><input name="id" value="${data.variants[0].id}"><div class="product-form__buttons"><button id="ProductSubmitButton-test" type="button" name="add"><span>Add to cart</span></button></div></form>
 <details data-matching-size-guide><summary>Size chart</summary><p>Source measurements unchanged</p></details>
 <div data-product-desktop-ux data-section-id="test" data-matching-set-copy="Choose a piece">
 <section data-matching-set-builder hidden><div data-matching-set-roles></div><div data-matching-set-summary hidden><p data-matching-set-empty-copy></p><div data-matching-set-chips></div><strong data-matching-set-total></strong></div><button data-matching-set-add-button disabled>Add this piece to bag</button><p data-matching-set-status hidden></p></section>
 <div data-photo-review-panel>Existing review panel</div></div>
 <div data-desktop-sticky-atc><span data-desktop-sticky-price></span><span data-desktop-sticky-size></span><button data-desktop-sticky-button>Add</button></div>
</div><div id="StickyMobileATC-test"><span data-sticky-mobile-atc-price></span><span data-sticky-mobile-atc-size></span><span data-sticky-mobile-atc-shipping></span><button data-sticky-mobile-atc-button>Add</button></div>`;}
function mobileScript(){const section=read('./proposed/sections/main-product.liquid');const start=section.indexOf('    (function () {\n      var sticky =');assert(start>0);let script=section.slice(start,section.indexOf('</script>',start));const locale=parse('../candidate/locales/en.default.json');script=script.replaceAll('{{ section.id }}','test').replace(/\{\{\s*'([^']+)'\s*\|\s*t\s*\|\s*json\s*\}\}/g,(_,key)=>{const value=key.split('.').reduce((a,k)=>a?.[k],locale);assert.equal(typeof value,'string',key);return JSON.stringify(value);});assert(!script.includes('{{'));return script;}

for(const width of [390,1280])test(`native fallback restores controls and both sticky routes at ${width}px`,()=>{for(const id of exceptions){const data=fixtures.get(id),h=harness(next,body(data),width);try{
 const w=h.w,doc=w.document,wrapper=doc.querySelector('[data-product-desktop-ux]'),native=doc.getElementById('ProductSubmitButton-test'),form=doc.getElementById('product-form-test'),guide=doc.querySelector('[data-matching-size-guide]');
 const beforeControls=[...doc.querySelectorAll('variant-selects select')].map(el=>el.outerHTML),beforeForm=form.innerHTML,beforeGuide=guide.outerHTML;let nativeClicks=0,hiddenBundleClicks=0;
 native.addEventListener('click',()=>nativeClicks++);doc.querySelector('[data-matching-set-add-button]').addEventListener('click',()=>hiddenBundleClicks++);
 runInContext(mobileScript(),h.dom.getInternalVMContext(),{filename:'inline-mobile-sticky.js'});
 w.initMatchingSetBuilder(wrapper,'test',data);w.initDesktopStickyAtc(wrapper,'test');
 assert.equal(doc.getElementById('ProductInfo-test').getAttribute('data-has-matching-set'),'false');assert(!doc.getElementById('ProductInfo-test').classList.contains('product__info-container--matching-set'));
 assert(doc.querySelector('[data-matching-set-builder]').hidden);assert.deepEqual([...doc.querySelectorAll('variant-selects select')].map(el=>el.outerHTML),beforeControls);assert.equal(form.innerHTML,beforeForm);assert.equal(guide.outerHTML,beforeGuide);
 assert.notEqual(w.getComputedStyle(native.parentElement).display,'none');assert.notEqual(w.getComputedStyle(doc.querySelector('variant-selects>.product-form__input')).display,'none');
 for(const select of doc.querySelectorAll('variant-selects select'))select.dispatchEvent(new w.Event('change',{bubbles:true}));
 doc.querySelector('[data-sticky-mobile-atc-button]').click();doc.querySelector('[data-desktop-sticky-button]').click();
 assert.equal(nativeClicks,2);assert.equal(hiddenBundleClicks,0);
 native.disabled=true;doc.querySelector('[data-sticky-mobile-atc-button]').click();doc.querySelector('[data-desktop-sticky-button]').click();assert.equal(nativeClicks,2);
 assert.equal(doc.querySelector('[data-photo-review-panel]').textContent,'Existing review panel');
}finally{h.close();}}});

test('frozen V7 bytes unchanged and proposal changes exactly the three declared files',()=>{const m=parse('./proposed-manifest.json');assert.equal(m.changes.length,3);for(const f of m.changes){assert.equal(createHash('sha256').update(read('../candidate/'+f.filename)).digest('hex'),f.baseline_sha256);assert.equal(createHash('sha256').update(read('./proposed/'+f.filename)).digest('hex'),f.proposed_sha256);}});

for(const width of [390,1280])test(`supported matching-set sticky controls keep their original bundle route at ${width}px`,()=>{const data=fixtures.get(core[0]),h=harness(next,body(data),width);try{
 const w=h.w,doc=w.document,wrapper=doc.querySelector('[data-product-desktop-ux]'),bundle=doc.querySelector('[data-matching-set-add-button]');let nativeClicks=0,bundleClicks=0;
 assert.equal(w.needsNativeVariantPicker(data),false);bundle.disabled=false;doc.querySelector('[data-matching-set-builder]').hidden=false;
 w.DLMMatchingSetStickyState={test:{isReady:true,totalText:'A$39.00',pieceCountLabel:'One piece',summaryText:'Adult S'}};
 doc.getElementById('ProductSubmitButton-test').addEventListener('click',()=>nativeClicks++);bundle.addEventListener('click',()=>bundleClicks++);
 runInContext(mobileScript(),h.dom.getInternalVMContext(),{filename:'inline-mobile-sticky.js'});w.initDesktopStickyAtc(wrapper,'test');
 doc.dispatchEvent(new w.CustomEvent('dlm:matching-set-fallback',{detail:{sectionId:'another-section'}}));
 doc.querySelector('[data-sticky-mobile-atc-button]').click();doc.querySelector('[data-desktop-sticky-button]').click();assert.equal(bundleClicks,2);assert.equal(nativeClicks,0);
}finally{h.close();}});
