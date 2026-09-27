const {test}=require('node:test');
const {assert,product,copy,environment,matches,choose,fields,assertSourceValues}=require('./residual-size-guide-harness.cjs');
const RAINBOW='vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings';
const GENERIC='blue-tropical-floral-family-matching-beach-dress-and-shirt-set';
const routes=[
 ['ivory-linen-family-matching-set','mother','Vest','S',0],
 ['ocean-dot-family-matching-set','mother','Top','S',0],
 [RAINBOW,'mother','Overall','S',0],
 ['geometric-blue-family-matching-set','father','Shirt','S',1],
 ['geometric-blue-family-matching-set','father','Shorts','S',1],
 [GENERIC,'father','T-Shirt','L',0],
 [GENERIC,'mother','Dress','S',0],
];
const count=r=>r.cases.filter(c=>c.match).length;

test('all reviewed source-backed gains survive explicit raw-unit validation',()=>{
 const expected={
  [RAINBOW]:40,'ivory-stripe-cargo-family-matching-set':31,'ivory-linen-family-matching-set':26,
  'ocean-dot-family-matching-set':26,'terracotta-tile-family-matching-set':28,
  'geometric-blue-family-matching-set':39,'green-palm-safari-family-matching-set':30,
  'ocean-marble-family-matching-set':26,'seaside-blue-plaid-family-matching-set':26,
  [GENERIC]:21,'tropical-floral-family-matching-shirt-and-dress-outfit-set':21,'tropical-palm-floral-family-matching-shirt-and-dress-set':21,
 };
 for(const [handle,n]of Object.entries(expected)){
  const p=product(handle),original=JSON.stringify(p),result=matches(p);
  assert.equal(count(result),n,handle);
  assertSourceValues(result);
  assert.equal(JSON.stringify(p),original,'source fixture remains unchanged');
 }

});

test('missing, unknown and wrong-family physical units cannot borrow enriched units',()=>{
 for(const [handle,role,type,size,tableIndex]of routes)for(const suffix of ['', ' (unknown)', ' (kg)']){
  const p=product(handle),t=p.tables[tableIndex];
  t.headers=t.headers.map((raw,i)=>{const label=raw.replace(/\s*\([^)]*\)\s*$/,'');return !i||/^(Age|Weight|Height)$/.test(label)?raw:label+suffix;});
  assert.equal(choose(matches(p),role,type,size).match,null,handle+'/'+type+'/'+suffix);
 }
});

test('one unitless physical column is omitted without losing other original measurements',()=>{
 for(const [handle,role,type,size,tableIndex]of routes){
  const p=product(handle),t=p.tables[tableIndex],index=t.headers.findIndex(h=>/^(?:Chest\/Bust|Bust)\s*\(/.test(h));
  if(index<0)continue;const raw=t.headers[index].replace(/\s*\([^)]*\)\s*$/,'');t.headers[index]=raw;
  const selected=choose(matches(p),role,type,size);
  assert.ok(!selected.match||!selected.match.headers.some(h=>h.raw===raw),handle+'/'+type);
 }
 const p=product(GENERIC);p.tables[0].headers[1]='Length';
 assert.deepEqual(fields(choose(matches(p),'mother','Dress','S').match),{'Bust (cm)':'45'});
});

test('shared guidance needs its own source unit while original unitless Age stays guidance only',()=>{
 const p=product('geometric-blue-family-matching-set'),t=p.tables[1];
 t.headers=t.headers.map(h=>h.replace(/^Weight\s*\([^)]*\)$/,'Weight').replace(/^Height\s*\([^)]*\)$/,'Height'));
 const selected=choose(matches(p),'father','Shirt','S');assert.ok(selected.match);
 assert.ok(!selected.match.headers.some(h=>h.raw==='Weight'||h.raw==='Height'));
 const q=product(RAINBOW);q.tables.forEach(t=>{t.rows.forEach(r=>{for(let i=1;i<r.length;i++)if(t.headers[i]!=='Age')r[i]='—';});});
 assert.equal(count(matches(q)),0);
});

test('qualified generic Height cannot silently become an unqualified converted number',()=>{
 const p=product(GENERIC),r=matches(p);
 assert.deepEqual(fields(choose(r,'boy','T-Shirt','2T').match),{'Bust (cm)':'33'});
 assert.deepEqual(fields(choose(r,'girl','Dress','1-2T').match),{'Length (cm)':'73','Bust (cm)':'29'});
 for(const value of ['90 and below','at least 90','90+','under 90','about 90','90–100']){
  const q=product(GENERIC);q.tables[0].rows.find(row=>row[0]==='Boy 2T')[5]=value;
  assert.deepEqual(fields(choose(matches(q),'boy','T-Shirt','2T').match),{'Bust (cm)':'33'},value);
 }
 const q=product(GENERIC);q.tables[0].rows.find(row=>row[0]==='Boy 2T')[5]='90-100';
 assert.deepEqual(fields(choose(matches(q),'boy','T-Shirt','2T').match),{'Bust (cm)':'33','Height (cm)':'90-100'});
});
