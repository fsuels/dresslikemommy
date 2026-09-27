const {test} = require('node:test');
const {assert, fixtures, copy, environment, matches, product, choose, fields, assertSourceValues} = require('./residual-size-guide-harness.cjs');
const OCEAN = 'ocean-dot-family-matching-set';
const TERRA = 'terracotta-tile-family-matching-set';
const count = result => result.cases.filter(c => c.match).length;

test('exact row role plus unique chart-named Type retains all reviewed source choices', () => {
 for (const [handle, expected] of [[OCEAN,26],[TERRA,28]]) {
  const fixture = product(handle), original = JSON.stringify(fixture), result = matches(fixture);
  assert.equal(count(result), expected, handle); assert.equal(result.cases.length, expected);
  assertSourceValues(result);
  assert.equal(JSON.stringify(fixture), original, 'source fixture remains unchanged');
 }
});


test('all projected values come from the exact source row for the uniquely sold role Type', () => {
 for (const [handle,role,type,size,label] of [[OCEAN,'mother','Top','S','Mother S'],[OCEAN,'girl','Dress','2 Years','Child 2 Years'],[TERRA,'mother','Dress','S','Mother S'],[TERRA,'girl','Top','2 Years','Child 2 Years']]) {
  const fixture=product(handle), result=matches(fixture), values=fields(choose(result,role,type,size).match);
  const table=fixture.tables[0], row=table.rows.find(r=>r[0]===label);
  for (const [h,v] of Object.entries(values)) assert.equal(v,row[table.headers.indexOf(h)]);
  if(handle===OCEAN&&role==='mother') assert.equal(values['Garment Length (cm/in)'],'58 cm / 23 in');
  if(handle===TERRA&&role==='mother') assert.equal(values['Skirt Length (cm/in)'],'110 cm / 43 in');
  if(handle===TERRA&&role==='girl') {assert.equal(values['Chest/Bust (cm/in)'],'67 cm / 26 in');assert.ok(!('Skirt Length (cm/in)' in values));}
 }
});

test('a second Dress/Top Type at any size invalidates the role-wide ownership proof', () => {
 for (const handle of [OCEAN,TERRA]) {
  const fixture=product(handle), originalType=handle===OCEAN?'Top':'Dress', opposite=handle===OCEAN?'Dress':'Top';
  const source=fixture.variants.find(v=>v.option1===originalType&&v.option2==='Mother M');
  fixture.variants.push({...source,id:999999,option1:opposite,title:opposite+' / Mother M',available:false});
  const env=environment(fixture);env.ctx.productData.variants[env.ctx.productData.variants.length-1].available=false;
  const group=env.ctx.roleGroupsCache.find(g=>g.roleKey==='mother');
  const option=group.options.find(o=>o.axes.Type===originalType&&o.sizeLabel==='S');
  const context=env.ctx.getMeasurementContextForInstance(group,{axisSelections:option.axes,sizeLabel:'S'},option);
  assert.equal(env.ctx.findMeasurementsForOption(group,option,context),null,handle);
  assert.equal(env.ctx.getExactChartRoleType(env.ctx.productData,'mother',['dress','top']),'');
 }
});

test('nonempty wrong-garment and mixed-component headers never enter role projection', () => {
 for (const handle of [OCEAN,TERRA]) {
  const fixture=product(handle);
  fixture.tables[0].headers.push('Cardigan Length (cm)','Top/Dress Length (cm)','Top Length (cm)','Dress Length (cm)');
  fixture.tables[0].rows.forEach(r=>r.push('888','777','111','222'));
  const result=matches(fixture);
  for(const c of result.cases.filter(c=>c.axes.Type!=='Shirt')) {
   const v=fields(c.match);
   assert.ok(!Object.values(v).some(x=>x==='888'||x==='777'));
   assert.equal(v[c.axes.Type+' Length (cm)'],c.axes.Type==='Top'?'111':'222');
   assert.ok(!((c.axes.Type==='Top'?'Dress':'Top')+' Length (cm)' in v));
  }
 }
});

test('role, garment, size qualifier, range, and ambiguous-selection guards stay exact', () => {
 const result=matches(product(OCEAN)), selected=choose(result,'mother','Top','S');
 for(const size of ['S/M','S Tall']) assert.equal(result.ctx.findMeasurementsForOption(selected.group,{...selected.option,sizeLabel:size,fullLabel:'Mother '+size},selected.context),null);
 assert.equal(result.ctx.findMeasurementsForOption({...selected.group,roleKey:'father',key:'father'},selected.option,selected.context),null);
 assert.equal(result.ctx.findMeasurementsForOption(selected.group,selected.option,{...selected.context,ambiguous:true}),null);
 assert.equal(result.ctx.findMeasurementsForOption(selected.group,selected.option,{...selected.context,garmentKey:'dress',typeValue:'Dress'}),null);
 const child=choose(result,'girl','Dress','2 Years');
 assert.equal(result.ctx.findMeasurementsForOption(child.group,{...child.option,sizeLabel:'1-2 Years',fullLabel:'Girl 1-2 Years'},child.context),null);
});

test('generic child role cannot derive ownership from the garment name alone', () => {
 const fixture=product(OCEAN);
 fixture.variants.filter(v=>v.option1==='Dress').forEach(v=>v.sku='');
 const result=matches(fixture);
 assert.equal(count(result),14,'unknown scoped role blocks the new route conservatively');
 assert.ok(result.cases.filter(c=>c.axes.Type==='Dress').every(c=>!c.match));
 const conflict=product(TERRA);
 conflict.variants.find(v=>v.option2==='Mother S').sku='DLM-GRL-TOP-S';
 assert.equal(count(matches(conflict)),14,'contradictory explicit size role and SKU must not prove ownership');
});

test('conflicting exact rows and tables remain ambiguous', () => {
 for(const duplicateTable of [false,true]) {
  const fixture=product(OCEAN), table=fixture.tables[0];
  if(duplicateTable){const extra=copy(table);extra.rows[7][4]='777 cm';fixture.tables.push(extra);}
  else{const row=copy(table.rows[7]);row[4]='777 cm';table.rows.push(row);}
  assert.equal(choose(matches(fixture),'mother','Top','S').match,null);
 }
});

test('changed table scope and age-only rows cannot supply Dress/Top measurements', () => {
 const fixture=product(OCEAN);fixture.tables[0].heading='Size Chart — Clothing (Mom & Girl)';
 assert.equal(count(matches(fixture)),14);
 const empty=product(TERRA), row=empty.tables[0].rows.find(r=>r[0]==='Child 2 Years');
 row[4]='—';row[5]='—';
 assert.equal(choose(matches(empty),'girl','Top','2 Years').match,null);
});
