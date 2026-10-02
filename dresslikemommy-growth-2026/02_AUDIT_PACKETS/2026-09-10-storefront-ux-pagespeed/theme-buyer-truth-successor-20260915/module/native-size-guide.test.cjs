const {test} = require('node:test');
const assert = require('node:assert/strict');
const {fixture, clone, environment: sourceEnvironment, load} = require('./native-size-guide-harness.cjs');

// General exact matching must stay strict outside the separately reviewed
// one-product Edition/Version alias. Keep all actual source rows and variants.
function environment(record = clone(fixture)) {
  return sourceEnvironment({...record, handle: 'native-size-guide-exact-match-fixture'});
}
const unresolved = 'M (Adult Extended Edition)';

test('native radios match 13/14 source rows without a product-specific semantic alias', () => {
  const env = environment(); const original = JSON.stringify(env.record); let matched = 0;
  for (const input of env.inputs) {
    env.select(input.value); const result = env.render();
    if (result.match) {
      matched++; const row = fixture.tables[0].rows.find(row => row[0].toLowerCase() === input.value.toLowerCase());
      assert.deepEqual(Array.from(result.match.row), row);
      assert.equal(result.selected.rawValue, input.value);
      assert.ok(result.html.includes('aria-expanded="true"'));
      assert.ok(!result.html.includes('data-matching-size-guide-metrics hidden'));
      assert.ok(result.html.includes(input.value));
    } else { assert.equal(result.html, ''); assert.ok(env.snapshot.hasAttribute('hidden')); }
    if (input.value === unresolved) assert.equal(result.match, null);
  }
  assert.equal(matched, 13); assert.equal(JSON.stringify(env.record), original);
});

test('normal and extended lengths remain distinct in cm and source inches', () => {
  const env = environment();
  for (const [size, cm, inches] of [['90cm','64','25.2'],['160cm','99','39.0'],
    ['S (Adult Normal Version)','115','45.3'],['S (Adult Extended Version)','120','47.2'],
    ['M (Adult Normal Version)','120','47.2'],['L (Adult Normal Version)','125','49.2'],['L (Adult Extended Version)','130','51.2']]) {
    env.select(size);
    for (const [unit, value] of [['metric',cm],['imperial',inches]]) {
      env.ctx.selectedUnitSystem=unit; const result=env.render();
      assert.ok(result.html.includes('>' + value + '</strong>'), size + ' ' + unit);
      assert.ok(result.html.includes(unit === 'metric' ? 'Length (cm)' : 'Length (in)'));
    }
  }
  env.select(unresolved); assert.equal(env.render().html, '', 'unresolved option clears previously shown measurements');
});

test('only case and whitespace normalize; conflicting or duplicate rows fail closed', () => {
  const altered=clone(fixture); altered.tables[0].rows[0][0]='  90CM  ';
  let env=environment(altered); env.select('90cm'); assert.ok(env.render().match);
  for(const conflict of [false,true]) {
    const record=clone(fixture); const row=clone(record.tables[0].rows[0]); if(conflict) row[1]='999 / 393.3'; record.tables[0].rows.push(row);
    env=environment(record); env.select('90cm'); assert.equal(env.render().match,null);
  }
  const record=clone(fixture); record.tables[0].rows=record.tables[0].rows.filter(row=>row[0]!=='90cm');
  env=environment(record); env.select('90cm'); assert.equal(env.render().match,null);
});

test('native route rejects Type, varying other axes, multiple charts, family routing and conflicting context', () => {
  const cases=[
    r=>{r.options[1].name='Type';},
    r=>{r.options[1].name='Material';r.variants.push({...r.variants[0],id:999,option2:'blue'});},
    r=>{r.tables.push(clone(r.tables[0]));},
    r=>{r.variants.forEach(v=>{v.option1='Mother S';});},
    r=>{r.tables[0].id='size-chart-cardigan';r.tables[0].heading='Size Chart - Dress';},
    r=>{r.tables[0].rows=[];},
  ];
  for(const alter of cases){const record=clone(fixture);alter(record);const env=environment(record);assert.equal(env.ctx.getNativeRadioGuideContext(),null);assert.equal(env.render().match,null);}
});

test('a varying Color option keeps the single source chart in every locale label', () => {
  for (const name of ['Color', 'Farbe', 'Couleur', 'カラー', 'اللون', 'Cor', 'Χρώμα']) {
    const record = clone(fixture); record.options[1].name = name;
    const env = environment(record); const variants = env.ctx.productData.variants;
    variants.push(...variants.map(v => ({...v, id: v.id + 1, option2: 'blue', title: v.option1 + ' / blue'})));
    assert.ok(env.ctx.getNativeRadioGuideContext(), name);
    env.select('90cm'); const result = env.render();
    assert.deepEqual(Array.from(result.match.row), fixture.tables[0].rows.find(row => row[0] === '90cm'), name);
  }
  const record = clone(fixture); record.options[1].name = 'Colorway Length';
  record.variants.push({...record.variants[0], id: 999, option2: 'blue'});
  assert.equal(environment(record).ctx.getNativeRadioGuideContext(), null, 'only an exact colour option name may vary');
});

test('native rows require explicit supported units for every displayed measurement', () => {
  for (const form of ['no-units', 'unknown-units', 'partial-units', 'mixed-unknown-units', 'cell-units-only', 'no-numeric']) {
    const record = clone(fixture);
    if (form === 'no-units') record.tables[0].headers = ['Size', 'Length', 'Bust'];
    if (form === 'unknown-units') record.tables[0].headers = ['Size', 'Length (unknown)', 'Bust (unknown)'];
    if (form === 'partial-units') record.tables[0].headers = ['Size', 'Length (cm/in)', 'Bust'];
    if (form === 'mixed-unknown-units') record.tables[0].headers = ['Size', 'Length (cm/unknown)', 'Bust (cm/in)'];
    if (form === 'cell-units-only') {
      record.tables[0].headers = ['Size', 'Length', 'Bust'];
      record.tables[0].rows[0] = ['90cm', '64 cm / 25.2 in', '58 cm / 22.8 in'];
    }
    if (form === 'no-numeric') record.tables[0].rows[0] = ['90cm', 'not available', 'not available'];
    const env = environment(record); env.select('90cm');
    assert.equal(env.render().match, null, form);
    env.ctx.syncNativeSizeGuideTooltips();
    assert.equal(env.inputs[0].nextElementSibling.querySelector('[data-native-size-tooltip]'), null, form);
  }
  const record = clone(fixture); record.tables[0].headers[2] = 'Unspecified'; record.tables[0].rows[0][2] = '';
  const env = environment(record); env.select('90cm');
  assert.equal(env.render().match.row[1], '64 / 25.2', 'empty nonmeasurement column is not displayed');
});

test('disabled, aria-disabled, unavailable, unsupported and ambiguous checked inputs never receive details', () => {
  for(const mode of ['disabled','aria-disabled','unavailable','unsupported','two-checked','none-checked']) {
    const env=environment(); env.select('90cm'); const input=env.inputs[0];
    if(mode==='disabled')input.disabled=true;
    if(mode==='aria-disabled')input.attrs['aria-disabled']='true';
    if(mode==='unavailable')env.ctx.productData.variants[0].available=false;
    if(mode==='unsupported')input.value='91cm';
    if(mode==='two-checked')env.inputs[1].checked=true;
    if(mode==='none-checked')input.checked=false;
    assert.equal(env.render().match,null,mode);
  }
});

test('hover preserves Dawn controls and label associations, stays aria-hidden and refreshes without duplicates', () => {
  const env=environment();
  const before=env.inputs.map(input=>JSON.stringify({id:input.id,value:input.value,checked:input.checked,disabled:input.disabled,attrs:input.attrs}));
  const labels=env.inputs.map(input=>input.nextElementSibling); const labelText=labels.map(label=>label.textContent);
  env.ctx.syncNativeSizeGuideTooltips(); env.ctx.syncNativeSizeGuideTooltips();
  assert.equal(labels.filter(label=>label.querySelector('[data-native-size-tooltip]')).length,13);
  for(const [index,input] of env.inputs.entries()) {
    assert.equal(input.nextElementSibling,labels[index]); assert.equal(labels[index].textContent,labelText[index]);
    assert.equal(labels[index].getAttribute('for'),input.id); assert.equal(labels[index].getAttribute('class'),'existing-class');
    assert.equal(JSON.stringify({id:input.id,value:input.value,checked:input.checked,disabled:input.disabled,attrs:input.attrs}),before[index]);
    const tips=labels[index].children.filter(child=>child.hasAttribute('data-native-size-tooltip')); assert.ok(tips.length<=1);
    if(tips.length){assert.equal(tips[0].getAttribute('aria-hidden'),'true');assert.equal(tips[0].tagName,'SPAN');assert.equal(labels[index].listeners.pointerenter.length,1);assert.doesNotMatch(tips[0].innerHTML,/<(?:input|select|fieldset|button)\b/);}
  }
  env.ctx.selectedUnitSystem='imperial';env.ctx.syncNativeSizeGuideTooltips();
  assert.ok(labels[0].querySelector('[data-native-size-tooltip]').innerHTML.includes('25.2'));
  labels[0].left=990; labels[0].listeners.pointerenter[0]();
  const tooltip=labels[0].querySelector('[data-native-size-tooltip]');assert.equal(990+parseFloat(tooltip.style.left),768);
  env.inputs[0].disabled=true;env.ctx.syncNativeSizeGuideTooltips();assert.equal(labels[0].querySelector('[data-native-size-tooltip]'),null);
  env.ctx.productData.options[1].name='Type';env.ctx.syncNativeSizeGuideTooltips();assert.equal(labels.filter(label=>label.querySelector('[data-native-size-tooltip]')).length,0);
});

test('existing non-native snapshots remain collapsed and native toggle remains reversible', () => {
  const env=environment();env.select('90cm');const {match,selected}=env.render();
  const toggle=env.snapshot.querySelector('[data-matching-size-guide-metrics-toggle]'); const panel=env.snapshot.querySelector('[data-matching-size-guide-metrics]');
  toggle.listeners.click[0]();assert.equal(toggle.getAttribute('aria-expanded'),'false');assert.ok(panel.hasAttribute('hidden'));
  toggle.listeners.click[0]();assert.equal(toggle.getAttribute('aria-expanded'),'true');assert.ok(!panel.hasAttribute('hidden'));
  env.ctx.renderSelectedGuideSnapshot(match,{...selected,nativeExact:false});assert.ok(env.snapshot.innerHTML.includes('data-matching-size-guide-metrics hidden'));
});

test('desktop-only native CSS stays scoped without matching-set activation; existing render updates tooltips', () => {
  const {source, css}=load();
  const marker='/* Exact-source native size help. Keep Dawn radios and adjacent labels intact. */';
  assert.ok(css.includes(marker), 'native tooltip CSS is present');
  const delta=css.slice(css.indexOf(marker));
  assert.match(delta,/min-width: 750px/);assert.match(delta,/hover: hover/);assert.match(delta,/pointer: fine/);
  assert.match(delta,/pointer-events: none/);assert.match(delta,/data-matching-set-fallback="true"/);
  assert.doesNotMatch(delta,/product__info-container--matching-set/);
  assert.ok(source.includes('renderSelectedGuideSnapshot(selectedMatch, selectedState);\n    syncNativeSizeGuideTooltips();'));
});
