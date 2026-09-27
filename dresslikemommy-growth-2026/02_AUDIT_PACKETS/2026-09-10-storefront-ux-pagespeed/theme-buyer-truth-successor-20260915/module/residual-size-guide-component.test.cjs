const {test}=require('node:test');
const {assert, fixtures, copy, environment, matches, product, choose, fields, assertSourceValues} = require('./residual-size-guide-harness.cjs');
const GEO='geometric-blue-family-matching-set', GREEN='green-palm-safari-family-matching-set', MARBLE='ocean-marble-family-matching-set', LINEN='ivory-linen-family-matching-set', CARGO='ivory-stripe-cargo-family-matching-set', SEA='seaside-blue-plaid-family-matching-set';
const count=r=>r.cases.filter(c=>c.match).length;
const expected={[GEO]:39,[GREEN]:30,[MARBLE]:26,[LINEN]:26,[CARGO]:31,[SEA]:26};

test('fully scoped component routes retain expected exact source coverage including Seaside Dad/Boy',()=>{
 for(const [handle,matched] of Object.entries(expected)){
  const p=product(handle),raw=JSON.stringify(p),result=matches(p);
  assert.equal(count(result),matched,handle);
  assertSourceValues(result);
  assert.equal(JSON.stringify(p),raw,'source fixture remains unchanged');
 }
});


test('component metrics retain exact original cells and never repurpose generic body or length fields',()=>{
 const geo=matches(product(GEO));
 const shirt=fields(choose(geo,'boy','Shirt','1-2 Years').match),shorts=fields(choose(geo,'boy','Shorts','1-2 Years').match);
 assert.equal(shirt['Chest/Bust (cm/in)'],'74 cm / 29 in');assert.equal(shirt['Shoulder (cm/in)'],'34 cm / 13 in');
 assert.equal(shorts['Pants Length (cm/in)'],'29 cm / 11 in');
 const green=fields(choose(matches(product(GREEN)),'father','Shirt','S').match);assert.equal(green['Chest/Bust (cm/in)'],'96 cm / 37.8 in');
 const marble=fields(choose(matches(product(MARBLE)),'boy','Shirt','2 Years').match);assert.equal(marble['Sleeve (cm/in)'],'11 cm / 4 in');
 const cargo=matches(product(CARGO));assert.equal(fields(choose(cargo,'father','Shirt','S').match)['Shirt Length (cm/in)'],'68 cm / 27 in');
 assert.equal(fields(choose(cargo,'father','Shorts','S').match)['Pants Length (cm/in)'],'56 cm / 22 in');
 for(const handle of Object.keys(expected)){
  const p=product(handle),result=matches(p),table=p.tables[1];
  for(const c of result.cases.filter(c=>c.match&&(c.axes.Type==='Shirt'||c.axes.Type==='Shorts'))){
   const values=fields(c.match);
   assert.ok(!Object.keys(values).some(h=>/^(?:hip|waist|garment length)\b/i.test(h)));
   if(c.axes.Type==='Shirt')assert.ok(!Object.keys(values).some(h=>/^pants|^short length/i.test(h)));
   if(c.axes.Type==='Shorts')assert.ok(!Object.keys(values).some(h=>/chest|bust|shoulder|sleeve|^shirt /i.test(h)));
   const sourceRows=table.rows.filter(r=>r[0]===(c.role==='boy'?'Child ': 'Father ')+c.size);
   assert.ok(sourceRows.some(r=>Object.entries(values).every(([h,v])=>r[table.headers.indexOf(h)]===v)),handle+'/'+c.role+'/'+c.size);
  }
 }
});

test('mixed, unknown garment, and contradictory duplicate headers are rejected',()=>{
 const p=product(GEO);p.tables[1].headers.push('Overall Length (cm)','Jacket Length (cm)','Longueur de jupe (cm)','Shirt/Overall Length (cm)','Shirt/Shorts Length (cm)','Sleeve or Skirt (cm)');p.tables[1].rows.forEach(r=>r.push('701','702','703','704','705','706'));
 const result=matches(p);assert.equal(count(result),39);
 for(const c of result.cases.filter(c=>c.axes.Type!=='Dress'))assert.ok(!Object.values(fields(c.match)).some(v=>/^70[1-6]$/.test(v)));
 const duplicate=product(GEO);duplicate.tables[1].headers.push('Chest/Bust (cm/in)');duplicate.tables[1].rows.forEach(r=>r.push('777 cm / 306 in'));
 assert.equal(choose(matches(duplicate),'father','Shirt','S').match,null);
});

test('full heading validation prevents standalone Shirt-to-Shorts and added third-garment routing',()=>{
 for(const heading of ['Size Chart — Shirt (Dad & Boy)','Size Chart — Shirt & Shorts and Cardigan (Dad & Boy)','Size Chart — Shirt & Shorts (Dad & Boy) and Romper (Baby)','Size Chart — Shirt & Shorts (Mom & Girl)']){
  const p=product(GEO);p.tables[1].heading=heading;const env=environment(p);
  assert.equal(env.ctx.getExactCompoundChartScope(env.tables[1],env.ctx.productData),null,heading);
  const result=matches(p);assert.ok(result.cases.filter(c=>c.axes.Type==='Shorts').every(c=>!c.match),heading);
 }
 const negative=matches(product('rainbow-stripe-family-matching-set'));
 assert.equal(count(negative),12);assert.ok(negative.cases.filter(c=>/Shorts/.test(c.axes.Type)).every(c=>!c.match));
});

test('generic source roles need one actual proven role across all component variants',()=>{
 const p=product(GREEN);p.variants.filter(v=>v.option1==='Shirt').forEach(v=>{if(v.option2.startsWith('Child'))v.sku='';});
 assert.ok(matches(p).cases.filter(c=>c.axes.Type==='Shirt'&&c.role==='boy').every(c=>!c.match));
 assert.ok(choose(matches(p),'father','Shirt','S').match,'explicit Father proof remains independent');
 const both=product(GREEN),source=both.variants.find(v=>v.option1==='Shirt'&&v.option2==='Child 2 Years');
 both.variants.push({...source,id:999111,option2:'Child 17 Years',sku:'DLM-TEST-GRL-17Y',title:'Shirt / Child 17 Years'});
 assert.equal(choose(matches(both),'boy','Shirt','2 Years').match,null,'second child role at another size blocks generic Child ownership');
 const bad=product(GEO);bad.variants.find(v=>v.option1==='Shirt'&&v.option2==='Father S').sku='DLM-KID-SHIRT-S';
 assert.equal(choose(matches(bad),'father','Shirt','S').match,null,'generic child SKU cannot support Father');
});

test('new component entries reject size ranges, qualifiers, wrong roles, and non-purchasable sizes',()=>{
 const result=matches(product(GEO)),s=choose(result,'father','Shorts','S');
 for(const size of ['S/M','S Tall','4XL'])assert.equal(result.ctx.findMeasurementsForOption(s.group,{...s.option,sizeLabel:size,fullLabel:'Father '+size},s.context),null,size);
 assert.equal(result.ctx.findMeasurementsForOption({...s.group,roleKey:'mother',key:'mother'},s.option,s.context),null);
 assert.equal(result.ctx.findMeasurementsForOption(s.group,s.option,{...s.context,ambiguous:true}),null);
 const child=choose(result,'boy','Shirt','2 Years');assert.equal(result.ctx.findMeasurementsForOption(child.group,{...child.option,sizeLabel:'1-3 Years',fullLabel:'Boy 1-3 Years'},child.context),null);
 const absent=product(GEO);absent.tables[1].rows.push(['Father 4XL',...absent.tables[1].rows[8].slice(1)]);
 const none=matches(absent);assert.equal(none.ctx.findMeasurementsForOption(s.group,{...s.option,sizeLabel:'4XL',fullLabel:'Father 4XL'},s.context),null,'source row alone cannot invent a variant');
});

test('conflicting projected rows, tables, and shared guidance remain blocked without merging',()=>{
 for(const handle of [GEO,CARGO])for(const duplicateTable of [false,true]){
  const p=product(handle),table=p.tables[1],index=table.rows.findIndex(r=>r[0]==='Father S'&&r[4]!=='—');
  if(duplicateTable){const extra=copy(table);extra.rows[index][4]='777 cm';p.tables.push(extra);}
  else{const row=copy(table.rows[index]);row[4]='777 cm';table.rows.push(row);}
  assert.equal(choose(matches(p),'father','Shirt','S').match,null);
 }
 const p=product(GEO),row=copy(p.tables[1].rows.find(r=>r[0]==='Father S'));row[2]='999 kg';p.tables[1].rows.push(row);
 assert.equal(choose(matches(p),'father','Shorts','S').match,null,'conflicting retained source guidance rejects duplicate rows');
});

test('physical metrics are required; empty component rows and age-only rows stay unmatched',()=>{
 const p=product(GEO),row=p.tables[1].rows.find(r=>r[0]==='Child 1-2 Years');row[4]='—';row[5]='—';
 assert.equal(choose(matches(p),'boy','Shirt','1-2 Years').match,null);
 row[7]='—';assert.equal(choose(matches(p),'boy','Shorts','1-2 Years').match,null);
 const q=product(CARGO),r=q.tables[1].rows.find(r=>r[0]==='Father S'&&r[8]!=='—');r[8]='—';
 assert.equal(choose(matches(q),'father','Shorts','S').match,null);
});

test('exact Seaside Dad/Boy scope excludes Baby and third-garment rows even at matching sizes',()=>{
 const p=product(SEA),table=p.tables[1];table.rows.push(['Baby 2 Years','2','999 kg','999 cm','777 cm','888 cm','999 cm','666 cm','555 cm']);
 const babyTemplate=p.variants.find(v=>v.option1==='Shirt'&&v.option2==='Child 2 Years');
 p.variants.push({...babyTemplate,id:999223,title:'Shirt / Baby 2 Years',option2:'Baby 2 Years',sku:'DLM-TEST-BABY-2Y'});
 const result=matches(p);assert.equal(fields(choose(result,'boy','Shirt','2 Years').match)['Chest/Bust (cm/in)'],'80 cm / 31 in');
 assert.equal(choose(result,'baby','Shirt','2 Years').match,null);
 assert.ok(result.ctx.buildSizeMeasurementsLookup().entries.filter(e=>e.sourceTable&&e.sourceTable.record===table&&e.requiresExactRoleScope).every(e=>['father','boy'].includes(e.roleKey)));
 const explicitRomper=copy(p);explicitRomper.tables[1].rows.push(['Boy 2 Years / Romper','2','','','444 cm','','','','']);
 assert.equal(fields(choose(matches(explicitRomper),'boy','Shirt','2 Years').match)['Chest/Bust (cm/in)'],'80 cm / 31 in');
});


test('opaque BSH SKU does not become a Boy role alias',()=>{
 const result=matches(product(CARGO));
 assert.ok(result.cases.filter(c=>c.axes.Type==='Shorts'&&c.role==='boy').every(c=>!c.match));
 assert.equal(result.cases.filter(c=>c.axes.Type==='Shorts'&&c.role==='father'&&c.match).length,6);
 assert.equal(result.ctx.inferRoleKeyFromSku('DLM-ISCG-BSH-KID2Y-SAGE'),'');
});
