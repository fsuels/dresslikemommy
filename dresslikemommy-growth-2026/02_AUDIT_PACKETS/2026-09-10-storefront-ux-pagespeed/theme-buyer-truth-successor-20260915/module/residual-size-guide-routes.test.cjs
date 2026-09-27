const {test} = require('node:test');
const {assert, fixtures, copy, environment, matches, product, choose, fields, assertSourceValues} = require('./residual-size-guide-harness.cjs');
const RAINBOW = 'vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings';
const STRIPE = 'ivory-stripe-cargo-family-matching-set';
const LINEN = 'ivory-linen-family-matching-set';
const count = result => result.cases.filter(c => c.match).length;

test('exact source routes retain expected coverage after all reviewed component repairs', () => {
 const expected = {[RAINBOW]: [40, 48], [STRIPE]: [31, 39], [LINEN]: [26, 26]};
 for (const [handle, [matched, checked]] of Object.entries(expected)) {
  const fixture = product(handle), original = JSON.stringify(fixture), result = matches(fixture);
  assert.equal(count(result), matched, handle); assert.equal(result.cases.length, checked);
  assertSourceValues(result);
  assert.equal(JSON.stringify(fixture), original, 'source fixture remains unchanged');
 }
});


test('Shirt projection keeps reviewed upper-body fields and exact source guidance', () => {
 const fixture = product(STRIPE);
 fixture.tables[1].headers.push('Shirt/Shorts Length (cm)', 'Cardigan Length (cm)', 'Generic Hip (cm)');
 fixture.tables[1].rows.forEach(row => row.push('777', '888', '999'));
 const result = matches(fixture);
 assert.equal(count(result), 31);
 const father = fields(choose(result, 'father', 'Shirt', 'S').match);
 assert.deepEqual(father, {'Weight (kg/lbs)': '48–58 kg / 105–127 lbs', 'Chest/Bust (cm/in)': '122 cm / 48 in',
  'Shoulder (cm/in)': '53 cm / 21 in', 'Shirt Length (cm/in)': '68 cm / 27 in'});
 const child = fields(choose(result, 'boy', 'Shirt', '1-2 Years').match);
 assert.equal(child['Shirt Length (cm/in)'], '38 cm / 15 in');
 assert.equal(child.Age, '1–2');
 assert.equal(result.cases.filter(c => c.axes.Type === 'Shorts' && c.match).length, 6);
 assert.ok(result.cases.filter(c => c.axes.Type === 'Shorts' && c.match).every(c => !('Shirt Length (cm/in)' in fields(c.match))),
  'later reviewed Shorts component matches cannot borrow the Shirt field');
 for (const c of result.cases.filter(c => c.axes.Type === 'Shirt')) {
  assert.ok(!Object.keys(fields(c.match)).some(k => /pants|hip|cardigan|shirt\/shorts/i.test(k)));
 }
 assertSourceValues(result);
});

test('literal Vest chart keeps exact source row and excludes other garment headers', () => {
 const fixture = product(LINEN);
 fixture.tables[0].headers.push('Cardigan Length (cm)', 'Top/Vest Length (cm)');
 fixture.tables[0].rows.forEach(row => row.push('888', '999'));
 const result = matches(fixture);
 assert.equal(count(result), 26);
 assert.equal(result.cases.filter(c => c.axes.Type === 'Vest' && c.match).length, 12);
 assert.deepEqual(fields(choose(result, 'mother', 'Vest', 'S').match), {
  'Weight (kg/lbs)': '38–45 kg / 83–99 lbs', 'Chest/Bust (cm/in)': '108 cm / 43 in', 'Garment Length (cm/in)': '106 cm / 42 in',
 });
 assert.equal(fields(choose(result, 'girl', 'Vest', '2 Years').match)['Garment Length (cm/in)'], '61 cm / 24 in');
 assert.equal(result.cases.filter(c => c.axes.Type === 'Shirt' && c.match).length, 14);
 assert.ok(result.cases.filter(c => c.axes.Type === 'Shirt').every(c => c.match.sourceTable.record !== fixture.tables[0]),
  'later reviewed Shirt matches come from their independent component chart');
});

test('row suffix routes preserve exact values and do not equate Short, Overall, and T-shirt', () => {
 const result = matches(product(RAINBOW));
 const short = fields(choose(result, 'boy', 'Short', '2 Years').match);
 const overall = fields(choose(result, 'girl', 'Overall', '2 Years').match);
 const shirt = fields(choose(result, 'girl', 'T-shirt', '2 Years').match);
 assert.equal(short['Waist (cm/in)'], '40 cm / 16 in');
 assert.equal(short['Pants Length (cm/in)'], '29 cm / 11 in');
 assert.equal(overall['Waist (cm/in)'], '64.8 cm / 26 in');
 assert.equal(overall['Pants Length (cm/in)'], '37.5 cm / 15 in');
 assert.equal(shirt['Chest/Bust (cm/in)'], '62.8 cm / 25 in');
 assert.equal(shirt['Garment Length (cm/in)'], '37.8 cm / 15 in');
 assert.ok(!Object.keys(shirt).some(k => /waist|pants/i.test(k)));
 assert.ok(!Object.keys(overall).some(k => /chest|sleeve/i.test(k)));
 assert.equal(result.cases.filter(c => !c.match).length, 8, 'age-only rows are not physical measurements');
 for (const c of result.cases.filter(c => c.match)) {
  const source = c.match.sourceTable.record;
  const row = source.rows.find(row => row[0].toLowerCase().replace(/\s+/g, ' ').trim() ===
    [c.option.fullLabel, '/', c.axes.Color].join(' ').toLowerCase().replace(/\s+/g, ' ').trim());
  assert.ok(row, c.role + ' ' + c.size);
  for (const [header,value] of Object.entries(fields(c.match))) assert.equal(value, row[source.headers.indexOf(header)]);
 }
});

test('exact axes, exact role, exact size, and ambiguity guards apply to new routes', () => {
 for (const [handle, role, axis, size] of [[LINEN, 'mother', 'Vest', 'S'], [STRIPE, 'father', 'Shirt', 'S'], [RAINBOW, 'mother', 'Overall', 'S']]) {
  const result = matches(product(handle)), selected = choose(result, role, axis, size);
  for (const altered of ['S/M', 'S Tall']) {
   const option = {...selected.option, sizeLabel: altered, fullLabel: role + ' ' + altered};
   assert.equal(result.ctx.findMeasurementsForOption(selected.group, option, selected.context), null, handle + '/' + altered);
  }
  assert.equal(result.ctx.findMeasurementsForOption({...selected.group, key: 'adult', roleKey: 'adult'}, selected.option, selected.context), null);
  assert.equal(result.ctx.findMeasurementsForOption(selected.group, selected.option, {...selected.context, ambiguous: true}), null);
 }
 const result = matches(product(RAINBOW)), selected = choose(result, 'mother', 'Overall', 'S');
 assert.equal(result.ctx.findMeasurementsForOption(selected.group, selected.option, {...selected.context, axisSelections: {}}), null,
  'unselected Color does not silently take the representative garment');
 assert.equal(result.ctx.findMeasurementsForOption(selected.group, selected.option, {...selected.context, axisSelections: {Color: 'Short'}}), null,
  'Mother has no Short source');
 assert.equal(result.ctx.findMeasurementsForOption(selected.group, selected.option, {...selected.context, axisSelections: {Color: 'Blue'}}), null);
});

test('duplicate conflicting rows and tables stay blocked', () => {
 for (const [handle, role, axis, size, tableIndex, rowIndex, column] of [
  [LINEN, 'mother', 'Vest', 'S', 0, 7, 4],
  [STRIPE, 'father', 'Shirt', 'S', 1, 16, 6],
  [RAINBOW, 'mother', 'Overall', 'S', 0, 14, 4],
 ]) {
  for (const duplicateTable of [false, true]) {
   const fixture = product(handle), table = fixture.tables[tableIndex];
   if (duplicateTable) { const extra = copy(table); extra.rows[rowIndex][column] = '777 cm'; fixture.tables.push(extra); }
   else { const row = copy(table.rows[rowIndex]); row[column] = '777 cm'; table.rows.push(row); }
   assert.equal(choose(matches(fixture), role, axis, size).match, null, handle + '/duplicateTable=' + duplicateTable);
  }
 }
});

test('missing physical columns, changed headings, and absent garment suffix cannot gain a match', () => {
 const linen = product(LINEN); linen.tables[0].heading = 'Size Chart — Cardigan (Mom & Girl)';
 const linenResult = matches(linen);
 assert.equal(count(linenResult), 14);
 assert.ok(linenResult.cases.filter(c => c.axes.Type === 'Vest').every(c => !c.match));
 const stripe = product(STRIPE); stripe.tables[1].headers[6] = 'Garment Length (cm/in)';
 const stripeResult = matches(stripe);
 assert.equal(count(stripeResult), 31);
 assert.ok(stripeResult.cases.filter(c => c.axes.Type === 'Shirt' && c.match).every(c => !('Garment Length (cm/in)' in fields(c.match))),
  'the explicit Shirt length route must not retain a newly generic length');
 assertSourceValues(stripeResult);
 const rainbow = product(RAINBOW);
 rainbow.tables.forEach(t => t.rows.forEach(r => {r[0] = r[0].replace(/ \/ .+$/, '');}));
 assert.equal(count(matches(rainbow)), 0);
 const wrongAxis = product(RAINBOW); wrongAxis.options[1].name = 'Style';
 const after = matches(wrongAxis);
 assert.equal(count(after), 33, 'non-Color axis retains the known legacy count');
 assert.ok(after.cases.filter(c => c.match).every(c => !c.match.garmentKey.startsWith('rowLiteral:')));
});


test('row suffix evidence cannot fabricate a purchasable garment selection', () => {
 const fixture = product(RAINBOW);
 const motherOverall = fixture.tables[0].rows.find(r => r[0] === 'Mother S / Overall');
 fixture.tables[0].rows.push(['Mother S / Short', ...motherOverall.slice(1)]);
 const result = matches(fixture), selected = choose(result, 'mother', 'Overall', 'S');
 assert.equal(result.ctx.findMeasurementsForOption(selected.group, selected.option,
  {...selected.context, axisSelections: {Color: 'Short'}}), null);
});
