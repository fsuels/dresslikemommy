import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {runInContext} from 'node:vm';
import test from 'node:test';
const require=createRequire(import.meta.url);
const {JSDOM,VirtualConsole}=require('/Users/fsuels/Projects/timelytables.com/node_modules/jsdom');
const read=p=>readFileSync(new URL(p,import.meta.url),'utf8');
const before=read('../../candidate/assets/size-conversion.js');
const after=read('./proposed/assets/size-conversion.js');
const esc=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
const span=(value,text=value)=>`<span data-size-display-value="${esc(value)}">${esc(text)}</span>`;
async function boot(code,body='') {
  const dom=new JSDOM(`<!doctype html><body>${body}</body>`,{url:'https://example.test/cart',runScripts:'outside-only',virtualConsole:new VirtualConsole()});
  const w=dom.window, observers=[],errors=[];
  const Observer=w.MutationObserver;
  w.MutationObserver=class extends Observer {constructor(fn){super(fn);observers.push(this);}};
  w.addEventListener('error',e=>{errors.push(String(e.error));e.preventDefault();});
  w.fetch=()=>{throw new Error('Network is forbidden in this regression');};
  const loaded=new Promise(resolve=>w.document.addEventListener('DOMContentLoaded',resolve,{once:true}));
  runInContext(code.replace('  const sizeSelect        = findSizeSelect();','  window.testUnits = {convertValueBetweenUnits, convertMeasurementText};\n  const sizeSelect        = findSizeSelect();'),dom.getInternalVMContext());
  await loaded;await new Promise(resolve=>setImmediate(resolve));
  return {w,close(){observers.forEach(o=>o.disconnect());w.close();assert.deepEqual(errors,[]);}};
}
test('baseline reproduces cart100cm becoming an unsupported age label',async()=>{
  const h=await boot(before,span('100cm'));try{assert.equal(h.w.document.querySelector('span').textContent,'2–3Y');}finally{h.close();}
});
test('all raw height, adult edition, role and order variant labels survive initial render',async()=>{
  const labels=['90cm','100cm','110cm','120cm','130cm','140cm','150cm','160cm','100','S (Adult Normal Version)','M (Adult Extended Edition)','Girl 1-2 Years','Boy 1-2 Years','100cm / white','S / Lavender','<100cm> & special'];
  const h=await boot(after,labels.map(s=>span(s)).join(''));try{
    assert.deepEqual(Array.from(h.w.document.querySelectorAll('span')).map(e=>e.textContent),labels);
    assert.equal(h.w.document.querySelectorAll('special').length,0);
  }finally{h.close();}
});
test('dynamically replaced drawer and cart updated events preserve and restore the source label',async()=>{
  const h=await boot(after,'<cart-drawer></cart-drawer>');try{
    const d=h.w.document;d.querySelector('cart-drawer').innerHTML=span('100cm','2–3Y');
    await new Promise(resolve=>setImmediate(resolve));assert.equal(d.querySelector('span').textContent,'100cm');
    d.querySelector('span').textContent='2–3Y';d.dispatchEvent(new h.w.Event('cart:updated'));
    assert.equal(d.querySelector('span').textContent,'100cm');
    assert.equal(d.querySelector('span').getAttribute('data-size-display-value'),'100cm');
  }finally{h.close();}
});
test('native dropdowns preserve source size labels and submitted values',async()=>{
  const markup='<select name="options[Size]" data-size-option="true"><option value="100cm" selected>100cm</option><option value="S (Adult Normal Version)">S (Adult Normal Version)</option></select>';
  const h=await boot(after,markup);try{
    const options=Array.from(h.w.document.querySelectorAll('option'));
    assert.deepEqual(options.map(e=>[e.value,e.textContent]),[['100cm','100cm'],['S (Adult Normal Version)','S (Adult Normal Version)']]);
    assert.equal(h.w.document.querySelector('select').value,'100cm');
  }finally{h.close();}
});
test('measurement conversion and existing guide formatter behavior are unchanged',async()=>{
  const a=await boot(before),b=await boot(after);try{
    for(const h of [a,b]) {
      assert.equal(h.w.testUnits.convertValueBetweenUnits(25.4,'cm','in'),10);
      assert.equal(h.w.testUnits.convertMeasurementText('25.4–50.8','cm','in'),'10–20');
      assert.equal(h.w.testUnits.convertValueBetweenUnits(1,'kg','lbs'),2.20462);
    }
    for(const v of ['100cm','S (Adult Normal Version)','100cm / white','Child 3 Years']) {
      assert.equal(a.w.DLMSizeLabelFormatter.formatSizeLabel(v),b.w.DLMSizeLabelFormatter.formatSizeLabel(v));
      assert.equal(a.w.DLMSizeLabelFormatter.replaceSizeTokensInText(v),b.w.DLMSizeLabelFormatter.replaceSizeTokensInText(v));
    }
  }finally{a.close();b.close();}
});
