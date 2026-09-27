const {test}=require('node:test');const assert=require('node:assert/strict');
const {fixture,clone,environment}=require('./native-size-guide-harness.cjs');
const unresolved='M (Adult Extended Edition)';
test('reviewed exact-product alias resolves the unique extended M row without changing normal M',()=>{
  const env=environment(clone(fixture));let count=0;
  for(const input of env.inputs){env.select(input.value);if(env.render().match)count++;}assert.equal(count,14);
  env.select(unresolved);let result=env.render();assert.equal(result.match.row[1],'125 / 49.2');assert.equal(result.match.row[2],'90 / 35.4');
  env.ctx.selectedUnitSystem='imperial';assert.ok(env.render().html.includes('>49.2</strong>'));
  env.select('M (Adult Normal Version)');assert.equal(env.render().match.row[1],'120 / 47.2');
});
test('alias stays scoped to product and extended M; canonicalized duplicate rows remain unresolved',()=>{
  let record=clone(fixture);record.handle='another-product';let env=environment(record);env.select(unresolved);assert.equal(env.render().match,null);
  for(const conflict of [false,true]){
    record=clone(fixture);const row=clone(record.tables[0].rows.find(row=>row[0]==='M (adult extended version)'));row[0]=unresolved;if(conflict)row[1]='999 / 393.3';record.tables[0].rows.push(row);
    env=environment(record);env.select(unresolved);assert.equal(env.render().match,null);
  }
  record=clone(fixture);record.variants[11].option1='S (Adult Extended Edition)';env=environment(record);env.select('S (Adult Extended Edition)');assert.equal(env.render().match,null);
});
