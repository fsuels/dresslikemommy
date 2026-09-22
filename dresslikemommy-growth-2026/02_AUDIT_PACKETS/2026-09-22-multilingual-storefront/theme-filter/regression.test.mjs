import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const packet = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(packet, '../../../..');
const sourcePath = 'assets/daddy-me-collection-filter.js';
const before = fs.readFileSync(path.join(packet, 'before', sourcePath), 'utf8');
const candidate = fs.readFileSync(path.join(repo, sourcePath), 'utf8');
const collections = JSON.parse(fs.readFileSync(path.join(packet, 'source_collections_readback.json'), 'utf8')).data;
const localeReadback = JSON.parse(fs.readFileSync(path.join(packet, '..', 'shop_locales_before.json'), 'utf8'));
const locales = localeReadback.structuredContent.data.shopLocales.filter(locale => locale.published).map(locale => locale.locale);
const observedDanish = JSON.parse(fs.readFileSync(path.join(packet, '../../2026-09-22-danish-localization/danish_shirt_browser_titles.json'), 'utf8')).titles;

function countForms(locale) {
  const file = locale === 'en' ? 'en.default' : locale;
  const text = fs.readFileSync(path.join(repo, 'locales', `${file}.json`), 'utf8');
  const values = JSON.parse(text.slice(text.indexOf('{'))).products?.facets?.product_count_simple;
  return Object.fromEntries(Object.entries(values || {}).map(([category, text]) => [category, text.replaceAll('{{ count }}', '__DLM_COUNT__')]));
}

function run(source, {lang='en', handle='daddy-me-shirts', products=collections.shirts.products.nodes, search='', forms=countForms(lang), withNav=true, withContainer=true}={}) {
  const documentListeners = {}; const windowListeners = {}; const observations = []; const history = [];
  let countWrites = 0;
  const counterElements = Object.fromEntries(['ProductCount', 'ProductCountDesktop'].map(id => {
    let text = 'server count';
    return [id, {get textContent() {return text;}, set textContent(value) {countWrites++; text = value;}}];
  }));
  const cards = products.map(product => {
    const item = {hidden:false};
    return {dataset:{analyticsTitle:product.title, analyticsHandle:product.handle}, item, closest(selector) {assert.equal(selector, 'li.grid__item'); return item;}};
  });
  const links = ['all', 'button-downs', 'tees'].map(filter => {
    const item = {hidden:false}; const attributes = {}; const classes = new Set();
    return {
      dataset:{daddyFilter:filter}, item, attributes, classes,
      classList:{toggle(name,value) {if(value) classes.add(name); else classes.delete(name);}},
      setAttribute(key,value) {attributes[key]=value;},
      getAttribute(key) {return attributes[key]??null;},
      removeAttribute(key) {delete attributes[key];},
      closest(selector) {if(selector === '.collection-category-nav__item') return item; if(selector === "[data-daddy-collection-nav='true']") return nav; throw new Error(selector);},
    };
  });
  const secondary = {hidden:false, querySelectorAll(selector) {assert.equal(selector, '.collection-category-nav__item'); return links.map(link => link.item);}};
  const nav = {
    dataset:{currentCollectionHandle:handle},
    getAttribute(attribute) {return forms[attribute.replace('data-daddy-count-', '')]??null;},
    querySelectorAll(selector) {assert.equal(selector, '[data-daddy-filter]'); return links;},
    querySelector(selector) {assert.equal(selector, '.collection-category-nav__row--secondary'); return secondary;},
  };
  const container = {id:'ProductGridContainer'};
  const location = {search, href:`https://www.dresslikemommy.com/${lang}/collections/${handle}${search}`};
  const document = {
    documentElement:{lang},
    querySelector(selector) {assert.equal(selector, "[data-daddy-collection-nav='true']"); return withNav?nav:null;},
    querySelectorAll(selector) {assert.equal(selector, '#product-grid .product-card-wrapper'); return cards;},
    getElementById(id) {return id === 'ProductGridContainer' ? (withContainer?container:null) : (counterElements[id]??null);},
    addEventListener(event,callback) {documentListeners[event] = callback;},
  };
  const window = {
    location,
    history:{replaceState(_state,_title,url) {history.push(url.toString()); location.href=url.toString(); location.search=url.search;}},
    addEventListener(event,callback) {windowListeners[event]=callback;},
  };
  class MutationObserver {
    constructor(callback) {this.callback=callback; observations.push(this);}
    observe(target,options) {this.target=target; this.options=JSON.parse(JSON.stringify(options));}
  }
  vm.runInNewContext(source, {document, window, URLSearchParams, URL, MutationObserver, Intl}, {timeout:1000});
  function snapshot() {return {
    hidden:cards.map(card => card.item.hidden),
    counts:Object.fromEntries(Object.entries(counterElements).map(([key,value]) => [key,value.textContent])),
    links:links.map(link => ({filter:link.dataset.daddyFilter, hidden:link.item.hidden, current:link.attributes['aria-current']??null, active:link.classes.has('is-active')})),
    secondaryHidden:secondary.hidden,
    url:location.href,
  };}
  return {snapshot, cards, observations, windowListeners, documentListeners, links, history, countWrites:() => countWrites};
}

test('fresh Admin fixtures have complete pagination and expected source memberships', () => {
  assert.equal(locales.length, 21);
  for (const [key, size] of [['all',64], ['tees',13], ['shirts',23]]) {
    assert.equal(collections[key].products.nodes.length, size);
    assert.equal(collections[key].products.pageInfo.hasNextPage, false);
  }
});

test('exact English snapshots are unchanged across every current source membership and filter', () => {
  for (const collection of Object.values(collections)) {
    for (const search of ['', '?dlm-daddy-filter=button-downs', '?dlm-daddy-filter=all']) {
      const options = {handle:collection.handle, products:collection.products.nodes, search};
      assert.deepEqual(run(candidate, options).snapshot(), run(before, options).snapshot(), `${collection.handle} ${search}`);
    }
  }
});

test('translated or missing titles cannot change any product subset in any published locale', () => {
  for (const lang of locales) {
    for (const collection of Object.values(collections)) {
      for (const search of ['', '?dlm-daddy-filter=button-downs']) {
        const expected = run(before, {handle:collection.handle, products:collection.products.nodes, search}).snapshot().hidden;
        const products = collection.products.nodes.map((product, i) => ({...product, title:i%2 ? 'قميص skjorte シャツ chemise koszula' : ''}));
        const actual = run(candidate, {lang, handle:collection.handle, products, search}).snapshot();
        assert.deepEqual(actual.hidden, expected, `${lang} ${collection.handle} ${search}`);
      }
    }
  }
});

test('the 23 actual Danish compound titles remain visible with their source handles', () => {
  assert.equal(observedDanish.length,23);
  const products = collections.shirts.products.nodes.map((product,i) => ({...product,title:observedDanish[i]}));
  const actual = run(candidate, {lang:'da', products}).snapshot();
  assert.deepEqual(actual.hidden, Array(23).fill(false));
  assert.equal(actual.counts.ProductCount, '23 produkter');
  assert.deepEqual(actual.hidden, run(before, {lang:'da',products}).snapshot().hidden);
});

test('tee exclusions use handles even when the display title claims shirts or is translated', () => {
  const handles = ['family-t-shirt', 'family-t-shirts', 'family-tee-shirts', 'family-tees-shirt', 'shirt-and-tee', 'shirts-and-tees'];
  const products = handles.map(handle => ({handle,title:'Skjortesæt Hawaiian Shirt'}));
  const shirts = run(candidate, {lang:'da',products}).snapshot();
  assert.deepEqual(shirts.hidden, Array(handles.length).fill(true));
  assert.equal(shirts.counts.ProductCount, '0 produkter');
  const tees = run(candidate, {lang:'da',products,handle:'daddy-me-t-shirts'}).snapshot();
  assert.deepEqual(tees.hidden, Array(handles.length).fill(false));
});

test('all available locale templates retain their own wording and plural choice for 0,1,2,3,5,11,21,23,101', () => {
  for (const lang of locales) {
    const forms = countForms(lang);
    if (!forms.other) continue; // Missing locale data is reported separately, never invented here.
    const rules = new Intl.PluralRules(lang);
    for (const count of [0,1,2,3,5,11,21,23,101]) {
      const products = [...Array.from({length:count}, () => collections.shirts.products.nodes[0]), collections.tees.products.nodes[0]];
      const actual = run(candidate, {lang,products}).snapshot();
      const expected = (forms[rules.select(count)] || forms.other).replaceAll('__DLM_COUNT__', String(count));
      assert.equal(actual.counts.ProductCount, expected, `${lang} ${count}`);
      assert.equal(actual.counts.ProductCountDesktop, expected, `${lang} desktop ${count}`);
      assert.equal(actual.counts.ProductCount.includes('__DLM_COUNT__'), false);
    }
  }
});

test('plural category fallbacks use the localized other template without adding English', () => {
  const forms = {one:'__DLM_COUNT__ منتج',other:'__DLM_COUNT__ منتجات'};
  for (const count of [0,2,3,11]) {
    const products = [...Array.from({length:count}, () => collections.shirts.products.nodes[0]), collections.tees.products.nodes[0]];
    assert.equal(run(candidate,{lang:'ar',products,forms}).snapshot().counts.ProductCount, `${count} منتجات`);
  }
});

test('missing templates preserve server-rendered text instead of generating English', () => {
  const actual = run(candidate, {lang:'de',forms:{}});
  assert.equal(actual.snapshot().counts.ProductCount, 'server count');
  assert.equal(actual.countWrites(),0);
});

test('parent filter navigation preserves locale path and unrelated query parameters', () => {
  const actual = run(candidate, {lang:'de',handle:'daddy-me',products:collections.all.products.nodes,search:'?country=DE&sort_by=price-ascending'});
  let prevented=false;
  const link=actual.links.find(link => link.dataset.daddyFilter==='button-downs');
  actual.documentListeners.click({target:{closest:() => link},preventDefault() {prevented=true;}});
  assert.equal(prevented,true);
  const state=actual.snapshot();
  assert.equal(state.hidden.filter(hidden => !hidden).length,24);
  const url = new URL(state.url);
  assert.equal(url.pathname, '/de/collections/daddy-me');
  assert.equal(url.searchParams.get('country'), 'DE');
  assert.equal(url.searchParams.get('sort_by'), 'price-ascending');
  assert.equal(url.searchParams.get('dlm-daddy-filter'), 'button-downs');
});

test('observer callbacks write each count only when changed and handle replacement card data', () => {
  const actual = run(candidate);
  assert.deepEqual(actual.observations[0].options,{childList:true,subtree:true});
  assert.equal(actual.countWrites(),2);
  for (let i=0;i<5;i++) {actual.observations[0].callback(); actual.windowListeners.popstate();}
  assert.equal(actual.countWrites(),2);
  actual.cards[0].dataset.analyticsHandle='matching-family-t-shirt';
  actual.observations[0].callback();
  assert.equal(actual.snapshot().counts.ProductCount,'22 products');
  assert.equal(actual.countWrites(),4);
  actual.observations[0].callback();
  assert.equal(actual.countWrites(),4);
});

test('unrelated collection, missing nav, and empty grid remain no-ops', () => {
  for (const options of [{withNav:false},{products:[]},{handle:'unrelated'}]) {
    assert.deepEqual(run(candidate, options).snapshot(), run(before, options).snapshot());
  }
});

test('existing card handle metadata is unchanged and Liquid only exposes escaped count templates', () => {
  const cardPath = 'snippets/card-product.liquid';
  assert.equal(fs.readFileSync(path.join(repo,cardPath),'utf8'),fs.readFileSync(path.join(packet,'before',cardPath),'utf8'));
  assert.match(fs.readFileSync(path.join(repo,cardPath),'utf8'),/data-analytics-handle="{{ card_product.handle \| escape }}"/);
  const breadcrumbs = fs.readFileSync(path.join(repo,'snippets/collection-breadcrumbs.liquid'),'utf8');
  assert.match(breadcrumbs,/daddy_count_key \| t: count: '__DLM_COUNT__'/);
  assert.match(breadcrumbs,/data-daddy-count-{{ daddy_count_form }}="{{ daddy_count_template \| escape }}"/);
});
