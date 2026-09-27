const {test}=require('node:test');
const {assert, fixtures, copy, environment, matches, product, choose, fields, assertSourceValues} = require('./residual-size-guide-harness.cjs');
const HANDLES=['blue-tropical-floral-family-matching-beach-dress-and-shirt-set','tropical-floral-family-matching-shirt-and-dress-outfit-set','tropical-palm-floral-family-matching-shirt-and-dress-set'];
const PRIMARY=HANDLES[0],count=r=>r.cases.filter(c=>c.match).length;

test('three exact fixed-role charts retain all 63 choices with unchanged source facts',()=>{
 for(const handle of HANDLES){
  const p=product(handle),original=JSON.stringify(p),result=matches(p);
  assert.equal(count(result),21,handle);assert.equal(result.cases.length,21);
  assertSourceValues(result);assert.equal(JSON.stringify(p),original,'source fixture remains unchanged');
 }
});


test('Dress and T-Shirt retain exact original physical cells and omit qualified Height',()=>{
 const p=product(PRIMARY),r=matches(p);
 assert.deepEqual(fields(choose(r,'mother','Dress','S').match),{'Length (cm)':'120','Bust (cm)':'45'});
 assert.deepEqual(fields(choose(r,'father','T-Shirt','L').match),{'Bust (cm)':'54'});
 assert.deepEqual(fields(choose(r,'boy','T-Shirt','2T').match),{'Bust (cm)':'33'});
 assert.deepEqual(fields(choose(r,'girl','Dress','1-2T').match),{'Length (cm)':'73','Bust (cm)':'29'});
 for(const c of r.cases){const values=fields(c.match),row=p.tables[0].rows.find(row=>row[0]===c.option.fullLabel);assert.ok(row,c.option.fullLabel);for(const [h,v]of Object.entries(values))assert.equal(row[p.tables[0].headers.indexOf(h)],v);if(c.axes.Type==='T-Shirt')assert.ok(!Object.keys(values).some(h=>/length|waist|pants/i.test(h)));}
});

test('a second Type for the same role at any size blocks ownership; other literal Type sets do not qualify',()=>{
 const p=product(PRIMARY),v=p.variants.find(v=>v.option2==='Mother M');p.variants.push({...v,id:99881,option1:'T-Shirt',sku:'TEST-MOM-SHIRT-M',title:'T-Shirt / Mother M'});
 assert.equal(choose(matches(p),'mother','Dress','S').match,null);
 for(const [handle,expected] of [['family-matching-red-cable-knit-cardigans-elegant-heart-button-design',0],['gradient-ombre-family-matching-outfits-pink-blue-t-shirts-with-white-shorts-set',13],['powder-blue-mommy-and-me-set',0]]){const result=matches(product(handle));assert.equal(count(result),expected,handle);assertSourceValues(result);}
 const q=product(PRIMARY);q.variants[0].option1='Cardigan';assert.equal(count(matches(q)),0);
});

test('one untitled generic chart is required; named or duplicate charts cannot use this rule',()=>{
 const p=product(PRIMARY);p.tables.push(copy(p.tables[0]));assert.equal(count(matches(p)),0);
 for(const [id,heading]of [['size-chart-shirt',''],['size-chart','Size Chart — Shirt'],['size-chart','Size Chart — Clothing']]){const q=product(PRIMARY);q.tables[0].id=id;q.tables[0].heading=heading;const env=environment(q);assert.equal(env.ctx.isExactGenericRoleChart(env.tables[0],env.ctx.productData,1),false);}
});

test('both source and variant roles must be literal and exact',()=>{
 const p=product(PRIMARY);p.tables[0].rows.filter(r=>r[0].startsWith('Boy ')).forEach(r=>r[0]=r[0].replace(/^Boy /,'Child '));const result=matches(p);assert.ok(result.cases.filter(c=>c.role==='boy').every(c=>!c.match));
 const q=product(PRIMARY);q.variants.filter(v=>v.option2.startsWith('Boy ')).forEach(v=>v.option2=v.option2.replace(/^Boy /,'Child '));assert.equal(count(matches(q)),0);
 const r=matches(product(PRIMARY)),selected=choose(r,'father','T-Shirt','L');assert.equal(r.ctx.findMeasurementsForOption({...selected.group,roleKey:'mother',key:'mother'},selected.option,selected.context),null);
});

test('contradictory SKU role family or garment metadata rejects the proof',()=>{
 const original=matches(product(PRIMARY));
 for(const sku of ['TEST-KID-SHIRT-L','TEST-MOM-SHIRT-L','TEST-DAD-DRESS-L']){const p=product(PRIMARY);p.variants.find(v=>v.option2==='Father L').sku=sku;const env=environment(p),selected=choose(original,'father','T-Shirt','L');assert.equal(env.ctx.findMeasurementsForOption(selected.group,selected.option,selected.context),null,sku);}
 const p=product(PRIMARY);p.variants.find(v=>v.option2==='Boy 2T').sku='TEST-ADULT-SHIRT-2T';const env=environment(p),selected=choose(original,'boy','T-Shirt','2T');assert.equal(env.ctx.findMeasurementsForOption(selected.group,selected.option,selected.context),null);
});

test('unknown component fields and populated Dress bottom columns fail closed',()=>{
 for(const h of ['Overall Length (cm)','Jacket Length (cm)','Longueur de jupe (cm)','Shirt/Overall Length (cm)']){const p=product(PRIMARY);p.tables[0].headers.push(h);p.tables[0].rows.forEach(r=>r.push('777'));assert.equal(count(matches(p)),0,h);}
 const p=product(PRIMARY),row=p.tables[0].rows.find(r=>r[0]==='Mother S');row[3]='777';assert.equal(choose(matches(p),'mother','Dress','S').match,null);
});

test('exact full role/size labels reject qualifiers and nearby ranges on both sides',()=>{
 const r=matches(product(PRIMARY)),selected=choose(r,'mother','Dress','S');for(const size of ['S/M','S Tall'])assert.equal(r.ctx.findMeasurementsForOption(selected.group,{...selected.option,sizeLabel:size,fullLabel:'Mother '+size},selected.context),null);
 assert.equal(r.ctx.findMeasurementsForOption(selected.group,selected.option,{...selected.context,ambiguous:true}),null);
 const p=product(PRIMARY);p.tables[0].rows.find(r=>r[0]==='Mother S')[0]='Mother S Tall';assert.equal(choose(matches(p),'mother','Dress','S').match,null);
 const girl=choose(r,'girl','Dress','1-2T');assert.equal(r.ctx.findMeasurementsForOption(girl.group,{...girl.option,sizeLabel:'2T',fullLabel:'Girl 2T'},girl.context),null);
});

test('conflicting duplicate row/header values and no physical data do not become measurements',()=>{
 const p=product(PRIMARY),row=copy(p.tables[0].rows.find(r=>r[0]==='Father L'));row[2]='777';p.tables[0].rows.push(row);assert.equal(choose(matches(p),'father','T-Shirt','L').match,null);
 const q=product(PRIMARY);q.tables[0].headers.push('Bust (cm)');q.tables[0].rows.forEach(r=>r.push('777'));assert.equal(count(matches(q)),0);
 const empty=product(PRIMARY);empty.tables[0].rows.forEach(r=>{r[1]='—';r[2]='—';});assert.equal(count(matches(empty)),0);
});
