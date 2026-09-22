import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const root=path.dirname(fileURLToPath(import.meta.url));
const relative='assets/daddy-me-collection-filter.js';
const before=fs.readFileSync(path.join(root,'before',relative),'utf8');
const candidate=fs.readFileSync(path.join(root,'theme',relative),'utf8');
const observed=JSON.parse(fs.readFileSync(path.join(root,'..','danish_shirt_browser_titles.json'),'utf8')).titles;
const teeTitles=[
  'Far og søn matchende t-shirts',
  'Matchende far og barn t-shirt',
  'Far og søn skjorter og t-shirts',
  'Matchende tees og hawaiiskjorter',
  'Matching tee skjortesæt',
  'Father and Son T-Shirt Shirts',
];
const englishTitles=[
  'Father and Son Matching Shirts',
  'Father Son Hawaiian Shirt',
  'Matching Button-Down Shirts',
  'Family T-shirts',
  'Father Son T-Shirt',
  'Dad and Kid Tee Shirts',
  'Matching tees',
  'Shirt and tee collection',
  'Family jacket',
  '',
];

function run(source,{lang='da',handle='daddy-me-shirts',titles=observed,search='',withNav=true,withContainer=true}={}) {
  const documentListeners={};const windowListeners={};const observations=[];const history=[];
  const counterElements={ProductCount:{textContent:'server count'},ProductCountDesktop:{textContent:'server count'}};
  const cards=titles.map(title=>{
    const item={hidden:false};
    return {dataset:{analyticsTitle:title},item,closest(selector){assert.equal(selector,'li.grid__item');return item;}};
  });
  const links=['all','button-downs','tees'].map(filter=>{
    const item={hidden:false};const attributes={};const classes=new Set();
    return {
      dataset:{daddyFilter:filter},item,attributes,classes,
      classList:{toggle(name,value){if(value)classes.add(name);else classes.delete(name);}},
      setAttribute(key,value){attributes[key]=value;},
      getAttribute(key){return attributes[key]??null;},
      removeAttribute(key){delete attributes[key];},
      closest(selector){if(selector==='.collection-category-nav__item')return item;if(selector==="[data-daddy-collection-nav='true']")return nav;throw new Error(selector);},
    };
  });
  const secondary={hidden:false,querySelectorAll(selector){assert.equal(selector,'.collection-category-nav__item');return links.map(link=>link.item);}};
  const nav={
    dataset:{currentCollectionHandle:handle},
    querySelectorAll(selector){assert.equal(selector,'[data-daddy-filter]');return links;},
    querySelector(selector){assert.equal(selector,'.collection-category-nav__row--secondary');return secondary;},
  };
  const container={id:'ProductGridContainer'};
  const location={search,href:`https://www.dresslikemommy.com/da/collections/${handle}${search}`};
  const document={
    documentElement:{lang},
    querySelector(selector){assert.equal(selector,"[data-daddy-collection-nav='true']");return withNav?nav:null;},
    querySelectorAll(selector){assert.equal(selector,'#product-grid .product-card-wrapper');return cards;},
    getElementById(id){return id==='ProductGridContainer'?(withContainer?container:null):(counterElements[id]??null);},
    addEventListener(event,callback){documentListeners[event]=callback;},
  };
  const window={
    location,
    history:{replaceState(_state,_title,url){history.push(url.toString());location.href=url.toString();location.search=url.search;}},
    addEventListener(event,callback){windowListeners[event]=callback;},
  };
  class MutationObserver {
    constructor(callback){this.callback=callback;observations.push(this);}
    observe(target,options){this.target=target;this.options=JSON.parse(JSON.stringify(options));}
  }
  vm.runInNewContext(source,{document,window,URLSearchParams,URL,MutationObserver},{timeout:1000});
  function snapshot(){return {
    hidden:cards.map(card=>card.item.hidden),
    counts:Object.fromEntries(Object.entries(counterElements).map(([key,value])=>[key,value.textContent])),
    links:links.map(link=>({filter:link.dataset.daddyFilter,hidden:link.item.hidden,current:link.attributes['aria-current']??null,active:link.classes.has('is-active')})),
    secondaryHidden:secondary.hidden,
    url:location.href,
  };}
  return {snapshot,cards,observations,windowListeners,documentListeners,links,history};
}

test('actual script reproduces all 23 Danish cards hidden before repair, then shows all 23',()=>{
  assert.equal(observed.length,23);
  const original=run(before).snapshot();
  assert.equal(original.hidden.filter(hidden=>!hidden).length,0);
  assert.equal(original.counts.ProductCount,'0 products');
  const fixed=run(candidate).snapshot();
  assert.equal(fixed.hidden.filter(hidden=>!hidden).length,23);
  assert.deepEqual(fixed.counts,{ProductCount:'23 produkter',ProductCountDesktop:'23 produkter'});
  assert.equal(fixed.links.find(link=>link.filter==='button-downs').hidden,false);
});

test('Danish compounds and casing work for da, da-DK and DA',()=>{
  for(const lang of ['da','da-DK','DA']) {
    const actual=run(candidate,{lang,titles:['SKJORTE','Skjorter','Bomuldsskjorte','bomuldsskjorter','Hawaiiskjorte','hawaiiskjorter','Skjortesæt','bomuldsskjortesæt']}).snapshot();
    assert.equal(actual.hidden.filter(hidden=>!hidden).length,8,lang);
    assert.equal(actual.counts.ProductCount,'8 produkter');
  }
});

test('existing tee exclusions win even when Danish shirt words also occur',()=>{
  const actual=run(candidate,{titles:teeTitles}).snapshot();
  assert.deepEqual(actual.hidden,teeTitles.map(()=>true));
  assert.equal(actual.counts.ProductCount,'0 produkter');
  assert.equal(actual.counts.ProductCountDesktop,'0 produkter');
});

test('Danish count is correct for zero, one and multiple visible cards',()=>{
  for(const [titles,count] of [[teeTitles,0],[[observed[0],...teeTitles],1],[observed.slice(0,2),2]]) {
    const actual=run(candidate,{titles}).snapshot();
    const expected=count===1?'1 produkt':`${count} produkter`;
    assert.equal(actual.counts.ProductCount,expected);
    assert.equal(actual.counts.ProductCountDesktop,expected);
  }
});

test('non-shirt Danish words do not match merely a partial skjorte stem',()=>{
  const actual=run(candidate,{titles:['Tøj med skjortemønster','Skjortekjole','Navy jakke','']}).snapshot();
  assert.deepEqual(actual.hidden,[true,true,true,true]);
});

test('Danish tee collection remains the inverse of shirt classification',()=>{
  const titles=[...observed,...teeTitles];
  const actual=run(candidate,{handle:'daddy-me-t-shirts',titles}).snapshot();
  assert.deepEqual(actual.hidden,[...observed.map(()=>true),...teeTitles.map(()=>false)]);
  assert.equal(actual.counts.ProductCount,`${teeTitles.length} produkter`);
});

test('English and all sampled non-Danish behavior exactly matches baseline across handles and filters',()=>{
  for(const lang of ['en','en-US','fr','de','es','it','']) {
    for(const handle of ['daddy-me-shirts','daddy-me-t-shirts','daddy-me','unrelated']) {
      for(const search of ['','?dlm-daddy-filter=button-downs','?dlm-daddy-filter=all']) {
        const options={lang,handle,search,titles:[...englishTitles,...observed,...teeTitles]};
        assert.deepEqual(run(candidate,options).snapshot(),run(before,options).snapshot(),`${lang} ${handle} ${search}`);
      }
    }
  }
});

test('parent collection all/button-down filter navigation and unrelated query values are preserved',()=>{
  const actual=run(candidate,{handle:'daddy-me',search:'?country=DK&preview_theme_id=137888792673',titles:[...observed,...teeTitles]});
  let prevented=false;
  const link=actual.links.find(link=>link.dataset.daddyFilter==='button-downs');
  actual.documentListeners.click({target:{closest(selector){assert.equal(selector,'[data-daddy-filter]');return link;}},preventDefault(){prevented=true;}});
  assert.equal(prevented,true);
  const state=actual.snapshot();
  assert.equal(state.hidden.filter(hidden=>!hidden).length,23);
  const url=new URL(state.url);
  assert.equal(url.pathname,'/da/collections/daddy-me');
  assert.equal(url.searchParams.get('country'),'DK');
  assert.equal(url.searchParams.get('preview_theme_id'),'137888792673');
  assert.equal(url.searchParams.get('dlm-daddy-filter'),'button-downs');
  assert.equal(actual.history.length,1);
});

test('repeat observer/popstate callbacks are idempotent; observer options are unchanged',()=>{
  const actual=run(candidate);
  assert.equal(actual.observations.length,1);
  assert.deepEqual(actual.observations[0].options,{childList:true,subtree:true});
  const initial=actual.snapshot();
  for(let i=0;i<5;i++) {
    actual.observations[0].callback();
    actual.windowListeners.popstate();
    assert.deepEqual(actual.snapshot(),initial);
  }
});

test('missing nav and empty DOM keep existing no-op behavior',()=>{
  for(const options of [{withNav:false},{titles:[]},{withContainer:false,lang:'en'}]) {
    assert.deepEqual(run(candidate,options).snapshot(),run(before,options).snapshot());
  }
});
