import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../scripts/render_marketing_cockpit.py', import.meta.url), 'utf8');
const script = source.match(/LIVE_SCRIPT = """\n([\s\S]*?)\n"""/)[1];
const good = (revision = 'r1', extra = {}) => ({service:'dlm-growth-dashboard',online:true,revision,content_error:null,last_source_change_at:'2026-09-09T15:00:00Z',recent_handoffs:[],...extra});
const flush = () => new Promise(resolve => setImmediate(resolve));

function harness({revision = 'r1', responses = [good()], auto = true, protocol = 'http:'} = {}) {
  const nodes = new Map();
  function node(id) {
    if (nodes.has(id)) return nodes.get(id);
    const value = {id, textContent:'', dataset:{}, checked:true, disabled:false, open:false, listeners:{}, children:[],
      addEventListener(name, callback) { this.listeners[name] = callback; },
      append(...items) { this.children.push(...items); },
      replaceChildren(...items) { this.children = items; },
      setAttribute(name, val) { this[name] = val; }};
    nodes.set(id, value); return value;
  }
  const timers = [], saved = new Map([['dlm-live-auto',String(auto)]]);
  let reloads = 0, requests = 0, assigned = null;
  const document = {hidden:false, activeElement:{tagName:'BODY'}, listeners:{},
    getElementById:node, querySelector:() => ({content:revision}), querySelectorAll:() => [],
    createElement:() => node(Symbol()), addEventListener(name, fn) { this.listeners[name] = fn; }};
  const context = {
    document, Date, CSS:{escape:value=>value}, AbortSignal, scrollY:234,
    location:{protocol,hostname:'127.0.0.1',reload:()=>{reloads++;},assign:value=>{assigned=value;}},
    localStorage:{getItem:key=>saved.get(key),setItem:(key,value)=>saved.set(key,value)},
    sessionStorage:{getItem:key=>saved.get(key),setItem:(key,value)=>saved.set(key,value),removeItem:key=>saved.delete(key)},
    window:{addEventListener(){},scrollTo(){}}, requestAnimationFrame:fn=>fn(),
    setTimeout:(fn,ms)=>{timers.push({fn,ms}); return timers.length;},clearTimeout(){},
    fetch:async()=>{requests++; const next=responses.shift() ?? good(); if (next instanceof Error) throw next; return {ok:true,json:async()=>next};}
  };
  vm.runInNewContext(script, context);
  return {node,document,saved,timers,responses, reloads:()=>reloads, requests:()=>requests, assigned:()=>assigned,
    check:()=>node('liveCheck').listeners.click()};
}

test('connected current content does not reload or invent running agents', async () => {
  const h = harness(); await flush();
  assert.equal(h.node('liveStatus').textContent,'Live view connected');
  assert.equal(h.reloads(),0);
  assert.equal(h.node('liveHandoffs').children[0].textContent,'No recent handoffs recorded.');
  assert.equal(h.timers.at(-1).ms,5000);
});

test('cold-start source failure remains a source error and repaired content reloads once', async () => {
  const h = harness({revision:'',responses:[good(null,{content_error:'invalid source'}),good('r2')]});
  await flush();
  assert.equal(h.node('liveStatus').textContent,'Source needs attention');
  assert.equal(h.reloads(),0);
  await h.check(); assert.equal(h.reloads(),1);
  const mounted = harness({revision:'r2',responses:[good('r2')]}); await flush();
  assert.equal(mounted.reloads(),0);
});

test('network interruption recovers without erasing the displayed checkpoint', async () => {
  const h = harness({responses:[new Error('offline'),good()]}); await flush();
  assert.equal(h.node('liveStatus').textContent,'Connection interrupted');
  assert.equal(h.reloads(),0);
  await h.check();
  assert.equal(h.node('liveStatus').textContent,'Live view connected');
  assert.equal(h.reloads(),0);
});

test('paused view keeps updates ready until a manual check preserves position and reloads', async () => {
  const h = harness({auto:false,responses:[good('r2'),good('r2')]}); await flush();
  assert.equal(h.node('liveStatus').textContent,'Updates ready');
  assert.equal(h.reloads(),0);
  await h.check(); assert.equal(h.reloads(),1);
  assert.equal(JSON.parse(h.saved.get('dlm-live-position')).y,234);
});

test('open continuation or focused input prevents an interrupting automatic reload', async () => {
  const h = harness(); await flush();
  h.node('resumeDialog').open = true; h.responses.push(good('r2'));
  await h.check(); assert.equal(h.reloads(),0);
  h.node('resumeDialog').open = false; h.document.activeElement.tagName='INPUT'; h.responses.push(good('r2'));
  await h.check(); assert.equal(h.reloads(),0);
  h.document.activeElement.tagName='BODY'; h.responses.push(good('r2'));
  await h.check(); assert.equal(h.reloads(),1);
});

test('empty handoff response removes old items and metadata remains plain text', async () => {
  const h = harness({responses:[good('r1',{recent_handoffs:[{title:'<img onerror=alert(1)>',date:'2026-09-09',task_ids:['TA-06'],anchor:'saved'}]}),good()]});
  await flush();
  assert.equal(h.node('liveHandoffs').children[0].children[0].textContent,'<img onerror=alert(1)>');
  await h.check();
  assert.equal(h.node('liveHandoffs').children.length,1);
  assert.equal(h.node('liveHandoffs').children[0].textContent,'No recent handoffs recorded.');
});

test('saved-file mode never claims a connection or polls accounts', async () => {
  const h = harness({protocol:'file:'}); await flush();
  assert.equal(h.node('liveStatus').textContent,'Saved file');
  assert.equal(h.node('liveAuto').disabled,true);
  assert.equal(h.requests(),0); h.check();
  assert.equal(h.assigned(),'http://127.0.0.1:8767/');
});
