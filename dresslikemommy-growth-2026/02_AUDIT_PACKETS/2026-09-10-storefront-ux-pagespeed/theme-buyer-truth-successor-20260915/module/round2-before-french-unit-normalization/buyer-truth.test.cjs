const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const repo = path.resolve(__dirname, '../../../../..');
const source = fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8');
const arabic = JSON.parse(fs.readFileSync(path.join(__dirname, '../arabic-before.json'), 'utf8'));
const originalTables = arabic.state.tables.filter(table => table.id);

// Execute the real module without running its DOMContentLoaded entrypoint.
// Its private closure functions are extracted unchanged; parsing, role grouping,
// garment routing, units, tooltips, card markup and table markup are production code.
function declaration(name, variable = false) {
  const start = new RegExp('^([ \\t]*)' + (variable ? 'var ' + name + ' = function' : 'function ' + name) + '\\s*\\(', 'm').exec(source);
  assert.ok(start, name);
  const tail = source.slice(start.index + start[0].length);
  const end = new RegExp('^' + start[1] + '\\}' + (variable ? ';' : '') + '$', 'm').exec(tail);
  assert.ok(end, 'closing line: ' + name);
  return source.slice(start.index, start.index + start[0].length + end.index + end[0].length);
}

const privateNames = [
  'normalizeSizeKey', 'makeSizeMeasurementLookup', 'makeMeasurementEntryKey', 'getMeasurementRoleKeysFromText',
  'getSizeMeasurementTableContextText', 'comparableSizeTokens', 'mergeComparableSizeTokens', 'adultSizeRank',
  'numericTokenValues', 'sizeTokenMatchRank', 'roleKeysCompatible', 'garmentKeysCompatible',
  'inferBaseRoleKeyFromMeasurementSize', 'headerGarmentKeys', 'headerMatchesGarment',
  'getMeasurementGarmentKeysFromHeaders', 'pruneMeasurementsForRole', 'addSizeMeasurementEntry',
  'addPrunedSizeMeasurementEntries', 'indexParsedSizeGuideRows', 'buildSizeMeasurementsLookup',
  'findMeasurementsForOption', 'isMeaningfulMeasurementValue', 'extractValueForUnit', 'convertRangeValue',
  'roundMeasurement', 'tidyMeasurementValue', 'buildMeasurementsHtml', 'getGroupByKey', 'getOptionByVariantId',
  'getDistinctSizesForGroup', 'getAxisNamesForGroup', 'getAxisValuesForGroup', 'getTypeAxisNamesForGroup',
  'getOptionTypeValue', 'getTypeValuesForGroupSize', 'getSelectedTypeValue', 'getPendingMeasurementAxisLabel',
  'getMeasurementTypeValue', 'getMeasurementGarmentKey', 'getMeasurementContextForInstance',
  'resolveVariantInGroup', 'renderInstanceSizeBlurb', 'renderCard', 'getSizeGuideTableContextText',
  'tableMatchesSelectedType', 'contextContainsGarmentKey', 'getFitModalGroups', 'fitGarmentKeysCompatible',
  'getFitHeaderGarmentKeys', 'getFitRoleFamilyKey', 'getFitRowRoleKey', 'pruneFitGroupForRole',
  'pruneFitGroupForGarment', 'findActiveFitGroupInList', 'getFitGroupFromProductTables', 'getFitModalActiveGroup',
  'getFitTriggerSelectedMatch', 'closeInlineFitPanel', 'renderInlineFitPanel', 'renderVisibleInlineFitPanels',
  'buildSizeMatchTokens', 'extractComparableAdultToken', 'getAdultSizeRank', 'hasComparableSizeData',
  'parseComparableSize', 'getPrimaryComparableSize', 'getGuideRowValues', 'areSizeGuideRolesCompatible',
  'getGuideRowMatchScore', 'formatGuideSizeLabel', 'isSelectedGuideRow', 'pickPreferredGuideUnitIndex',
  'formatGuideNumericValue', 'convertGuideValueBetweenUnits', 'stripGuideTrailingUnit', 'getGuideTargetUnit',
  'convertGuideCellText', 'formatGuideHeaderLabel', 'formatGuideCellValue', 'hasUnitToggle', 'renderGuideUnitToggle',
];

function tableDom(record, heading) {
  const cell = text => ({ textContent: text });
  const rows = [record.headers, ...record.rows].map((values, index) => ({
    querySelectorAll(selector) { return selector === 'td' && index === 0 ? [] : values.map(cell); },
    querySelector() { return cell(values[0]); },
  }));
  return {
    id: record.id, previousElementSibling: heading ? { tagName: 'H3', textContent: heading, previousElementSibling: null } : null,
    querySelectorAll(selector) {
      if (selector === 'tr') return rows;
      if (selector === 'tr:first-child th, tr:first-child td') return record.headers.map(cell);
      throw new Error('Unmodeled table selector: ' + selector);
    },
    record,
  };
}

function fixtures(locale = 'en') {
  const roleLabels = locale === 'fr' ? ['Maman', 'Fille'] : ['Mother', 'Girl'];
  const childSizes = ['2 Years', '3 Years', '4 Years', '5 Years', '6-7 Years', '8 Years', '9-10 Years'];
  return originalTables.map((original, index) => {
    const record = JSON.parse(JSON.stringify(original));
    if (locale !== 'ar') {
      record.headers = ['Size', 'Age', 'Weight (kg/lbs)', 'Height (cm/in)', 'Chest/Bust (cm/in)',
        index ? 'Sleeve Length (cm/in)' : 'Skirt Length (cm/in)', 'Pants/Shorts or - (cm/in)',
        locale === 'fr' ? 'Hanches (cm/in)' : 'Hip (cm/in)', 'Waist (cm/in)', 'Garment Length (cm/in)'];
      record.rows = record.rows.map((row, i) => [i < 7 ? roleLabels[1] + ' ' + childSizes[i] : roleLabels[0] + ' ' + ['S', 'M', 'L', 'XL', '2XL'][i - 7],
        ...row.slice(1).map(value => value.replaceAll('كجم', 'kg').replaceAll('رطل', 'lbs').replaceAll('بوصة', 'in').replaceAll('سم', 'cm'))]);
    }
    const heading = locale === 'ar' ? (index ? 'مخطط المقاسات - كارديجان' : 'جدول المقاسات - فستان') :
      (locale === 'fr' ? 'Guide des tailles - ' : 'Size Chart - ') + (index ? 'Cardigan' : locale === 'fr' ? 'Robe' : 'Dress');
    return tableDom(record, heading);
  });
}

function environment(locale = 'en', initialTables = fixtures(locale), types) {
  const panels = new Map();
  const triggers = [];
  let tables = initialTables;
  const typeValues = types || (locale === 'ar' ? ['فستان', 'سترة'] : locale === 'fr' ? ['Robe', 'Cardigan'] : ['Dress', 'Cardigan']);
  const axisName = locale === 'ar' ? 'النوع' : 'Type';
  const sizeName = locale === 'ar' ? 'المقاس' : locale === 'fr' ? 'Taille' : 'Size';
  const description = { querySelectorAll() { return tables; } };
  const productRoot = { querySelector(selector) { assert.equal(selector, '[data-product-description]'); return description; } };
  const ctx = vm.createContext({ console, document: {
    addEventListener() {}, documentElement: { getAttribute() { return locale; } },
    getElementById(id) { return panels.get(id); },
  }, window: {} });
  vm.runInContext(source, ctx);
  vm.runInContext(privateNames.map(name => declaration(name)).join('\n') + '\n' + declaration('renderTableCard', true), ctx);
  const productData = {
    options: [{name: axisName, position: 1}, {name: sizeName, position: 2}],
    variants: typeValues.flatMap((type, typeIndex) => originalTables[0].rows.map((row, index) => ({
      id: (typeIndex + 1) * 100 + index, option1: type,
      option2: locale === 'ar' ? row[0] : (index < 7 ? 'Girl ' + ['2 Years', '3 Years', '4 Years', '5 Years', '6-7 Years', '8 Years', '9-10 Years'][index] : 'Mother ' + ['S', 'M', 'L', 'XL', '2XL'][index - 7]),
      sku: index < 7 ? 'fixture-GRL-' + index : 'fixture-MOM-' + index,
      available: true, price: index < 7 ? 2499 : 2999,
    }))),
  };
  Object.assign(ctx, {
    productData, sizeMeasurementsByLabel: null, wrapper: { closest() { return productRoot; } },
    getCurrentDescriptionRoot() { return description; },
    sizeGuideRoot: { querySelectorAll(selector) {
      if (selector === '[data-fit-inline-panel]') return [...panels.values()];
      if (selector.includes('[data-pdp-fit-inline-trigger]')) return triggers.filter(trigger => !selector.includes('aria-expanded') || trigger.getAttribute('aria-expanded') === 'true');
      return [];
    } },
    sectionId: 'fixture', currency: 'USD', unitSystem: 'metric', selectedUnitSystem: 'metric',
    closedPanels: {}, debug: false, compareLabel: 'Size chart', unitToggleLabel: 'Size chart units',
    isInlineFitMobileViewport() { return false; }, bindInlineFitPanelScroll() {}, bindUnitToggleEvents() {},
    getSelectedGuideMatch() { throw new Error('Inline fit must not consult native selected chart'); },
    getSelectedSizeState() { throw new Error('Inline fit must not consult native selected size'); },
  });
  ctx.roleGroupsCache = ctx.buildRoleGroups(productData, {}, true, {skipTypeFilter: true});
  function setTables(next) { tables = next; ctx.sizeMeasurementsByLabel = null; }
  function instance(role, type, size = '', id = role) {
    return { instanceId: id, roleKey: role, groupKey: role, axisSelections: type ? {[axisName]: type} : {}, sizeLabel: size, quantity: 1 };
  }
  function triggerFor(inst) {
    const html = ctx.renderCard(inst);
    const tag = html.match(/<button[^>]+data-pdp-fit-inline-trigger[^>]+>/);
    assert.ok(tag, 'real renderCard fit trigger');
    const attrs = Object.fromEntries([...tag[0].matchAll(/([\w-]+)="([^"]*)"/g)].map(match => [match[1], match[2]]));
    const panel = { id: attrs['aria-controls'], hidden: true, innerHTML: '', style: { setProperty() {} },
      hasAttribute(name) { return name === 'hidden' && this.hidden; },
      setAttribute(name) { if (name === 'hidden') this.hidden = true; },
      removeAttribute(name) { if (name === 'hidden') this.hidden = false; },
    };
    const trigger = { getAttribute(name) { return attrs[name] || ''; }, setAttribute(name, value) { attrs[name] = value; } };
    panels.set(panel.id, panel); triggers.push(trigger);
    return { trigger, panel, html, attrs };
  }
  return { ctx, instance, triggerFor, setTables, tables: initialTables, typeValues, productData };
}

for (const locale of ['en', 'fr', 'ar']) {
  for (const role of ['mother', 'girl']) {
    test(locale + ' ' + role + ': Dress → Cardigan → Dress; selected/unselected size; units and reopen', () => {
      const env = environment(locale), {ctx} = env;
      const group = ctx.getGroupByKey(role);
      assert.ok(group);
      const size = role === 'mother' ? 'M' : group.options[1].sizeLabel;
      const beforeProduct = JSON.stringify(env.productData);
      const beforeMeasurements = JSON.stringify(env.tables.map(table => table.record));
      for (const sizeLabel of ['', size]) {
        const inst = env.instance(role, env.typeValues[0], sizeLabel);
        for (const typeIndex of [0, 1, 0]) {
          inst.axisSelections = {[locale === 'ar' ? 'النوع' : 'Type']: env.typeValues[typeIndex]};
          const rendered = env.triggerFor(inst);
          assert.equal(rendered.attrs['data-fit-garment-key'], typeIndex ? 'cardigan' : 'dress');
          assert.match(rendered.html, new RegExp('card-helper">' + ctx.localizeTypeLabel(env.typeValues[typeIndex]) + '<'));
          const active = ctx.getFitGroupFromProductTables(role, role, typeIndex ? 'cardigan' : 'dress');
          assert.equal(active.sourceTable, env.tables[typeIndex]);
          assert.equal(active.rows.length, role === 'mother' ? 5 : 7);
          assert.equal(active.garmentKey, typeIndex ? 'cardigan' : 'dress');
          const sleeve = locale === 'ar' ? 'طول الكم' : 'Sleeve Length';
          const skirt = locale === 'ar' ? 'طول التنورة' : 'Skirt Length';
          for (const unit of ['metric', 'imperial', 'metric']) {
            ctx.selectedUnitSystem = ctx.unitSystem = unit;
            assert.equal(ctx.renderInlineFitPanel(rendered.trigger, true), true);
            assert.ok(rendered.panel.innerHTML.includes(typeIndex ? sleeve : skirt));
            assert.ok(!rendered.panel.innerHTML.includes(typeIndex ? skirt : sleeve));
            assert.ok(rendered.panel.innerHTML.includes(unit === 'metric' ? '(cm)</th>' : '(in)</th>'));
            assert.equal((rendered.panel.innerHTML.match(/class="is-selected"/g) || []).length, sizeLabel ? 1 : 0);
            const option = ctx.resolveVariantInGroup(group, size || group.options[0].sizeLabel, inst.axisSelections);
            const context = ctx.getMeasurementContextForInstance(group, inst, option);
            const measurement = ctx.findMeasurementsForOption(group, option, context);
            assert.ok(measurement);
            assert.equal(measurement.sourceTable, env.tables[typeIndex]);
            const tooltip = ctx.buildMeasurementsHtml(measurement);
            assert.ok(tooltip.includes(typeIndex ? sleeve : skirt));
            assert.ok(!tooltip.includes(typeIndex ? skirt : sleeve));
            const expectedRowIndex = role === 'mother' ? 8 : 1;
            const chestPart = env.tables[typeIndex].record.rows[expectedRowIndex][4].split(' / ')[unit === 'metric' ? 0 : 1];
            const chestNumber = String(parseFloat(chestPart));
            assert.ok(tooltip.includes('>' + chestNumber + ' '), 'tooltip retains the source chest value for this garment and unit');
          }
          ctx.renderInlineFitPanel(rendered.trigger);
          assert.equal(rendered.panel.hidden, true);
          ctx.renderInlineFitPanel(rendered.trigger);
          assert.equal(rendered.panel.hidden, false);
        }
      }
      assert.equal(JSON.stringify(env.productData), beforeProduct, 'variant IDs/prices/options unchanged');
      assert.equal(JSON.stringify(env.tables.map(table => table.record)), beforeMeasurements, 'source measurement rows unchanged');
    });
  }
}

test('two independent cards retain different Types and sizes', () => {
  const env = environment(), {ctx} = env;
  const mother = env.instance('mother', 'Cardigan', 'M', 'one');
  const girl = env.instance('girl', 'Dress', '4 Years', 'two');
  const savedGirl = JSON.stringify(girl);
  const a = env.triggerFor(mother), b = env.triggerFor(girl);
  ctx.renderInlineFitPanel(a.trigger); ctx.renderInlineFitPanel(b.trigger);
  assert.match(b.panel.innerHTML, /Skirt Length/);
  mother.axisSelections.Type = 'Dress';
  assert.equal(env.triggerFor(mother).attrs['data-fit-garment-key'], 'dress');
  assert.equal(JSON.stringify(girl), savedGirl);
  assert.equal(ctx.resolveVariantInGroup(ctx.getGroupByKey('girl'), girl.sizeLabel, girl.axisSelections).axes.Type, 'Dress');
});

test('unselected Type shows choice prompt and no helper, tooltip, table or selected highlight', () => {
  const env = environment();
  for (const size of ['', 'M']) {
    const card = env.triggerFor(env.instance('mother', '', size));
    assert.equal(card.attrs['data-fit-pending-axis'], 'Type');
    assert.doesNotMatch(card.html, /card-helper|role="tooltip"/);
    env.ctx.renderInlineFitPanel(card.trigger);
    assert.match(card.panel.innerHTML, /Pick a Type/);
    assert.doesNotMatch(card.panel.innerHTML, /<table|is-selected/);
  }
});

test('reversed tables preserve exact chart and tooltip source', () => {
  const tables = fixtures().reverse(), env = environment('en', tables), {ctx} = env;
  for (const garment of ['dress', 'cardigan']) {
    const table = tables.find(table => table.id === (garment === 'dress' ? 'size-chart' : 'size-chart-cardigan'));
    assert.equal(ctx.getFitGroupFromProductTables('mother', 'mother', garment).sourceTable, table);
    const inst = env.instance('mother', garment === 'dress' ? 'Dress' : 'Cardigan', 'M');
    const option = ctx.resolveVariantInGroup(ctx.getGroupByKey('mother'), 'M', inst.axisSelections);
    assert.equal(ctx.findMeasurementsForOption(ctx.getGroupByKey('mother'), option, ctx.getMeasurementContextForInstance(ctx.getGroupByKey('mother'), inst, option)).sourceTable, table);
  }
});

for (const mode of ['missing', 'untyped', 'conflicting-heading', 'duplicate']) {
  test(mode + ' Cardigan source never falls back to Dress', () => {
    const env = environment(), {ctx} = env;
    let next = [env.tables[0]];
    if (mode === 'untyped') next.push(tableDom({...env.tables[1].record, id: 'size-chart-other'}, 'Size Chart'));
    if (mode === 'conflicting-heading') next.push(tableDom(env.tables[1].record, 'Size Chart - Dress'));
    if (mode === 'duplicate') next.push(env.tables[1], tableDom({...env.tables[1].record}, 'Size Chart - Cardigan'));
    env.setTables(next);
    assert.equal(ctx.getFitGroupFromProductTables('mother', 'mother', 'cardigan'), null);
    const inst = env.instance('mother', 'Cardigan', 'M'), group = ctx.getGroupByKey('mother');
    const option = ctx.resolveVariantInGroup(group, 'M', inst.axisSelections);
    assert.equal(ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option)), null);
    const card = env.triggerFor(inst); ctx.renderInlineFitPanel(card.trigger);
    assert.match(card.panel.innerHTML, /unavailable/);
    assert.doesNotMatch(card.panel.innerHTML, /<table|is-selected/);
  });
}

test('role pruning returns no chart when only the other role is present, and rejects unknown mixed rows', () => {
  const env = environment(), {ctx} = env;
  const parsed = ctx.parseSizeGuideTable(env.tables[0]);
  const group = {key: 'all', headers: parsed.headers, rows: parsed.rows.slice(0, 7)};
  assert.equal(ctx.pruneFitGroupForRole(group, 'mother'), null);
  group.rows.push(['Unclassified size', ...parsed.rows[7].slice(1)], parsed.rows[7]);
  assert.equal(ctx.pruneFitGroupForRole(group, 'mother').rows.length, 1);
});

test('single generic single-Type chart and no-Type family chart remain useful', () => {
  const record = {...fixtures()[0].record, id: 'size-chart'};
  const generic = tableDom(record, 'Size Chart');
  const env = environment('en', [generic], ['Dress']), {ctx} = env;
  assert.equal(ctx.getFitGroupFromProductTables('mother', 'mother', 'dress').rows.length, 5);
  const inst = env.instance('mother', '', 'M'), group = ctx.getGroupByKey('mother');
  const option = ctx.resolveVariantInGroup(group, 'M', {});
  assert.ok(ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option)));
  ctx.productData = {options: [{name: 'Size'}], variants: [{option1: 'Mother M'}]};
  assert.equal(ctx.getFitGroupFromProductTables('mother', 'mother', '').rows.length, 5);
  assert.equal(ctx.getFitGroupFromProductTables('girl', 'girl', '').rows.length, 7);
});

test('single unclassified garment chart remains available; multi-Type unknown cannot choose another garment', () => {
  const generic = tableDom({...fixtures()[1].record, id: 'size-chart'}, 'Size Chart');
  const env = environment('en', [generic], ['Sweater']);
  assert.equal(env.ctx.getFitGroupFromProductTables('mother', 'mother', '').rows.length, 5);
  env.ctx.productData.variants.push({option1: 'Dress', option2: 'Mother M'});
  assert.equal(env.ctx.getFitGroupFromProductTables('mother', 'mother', ''), null);
});

test('inline highlight requires this card size and cannot borrow a nearby/native size', () => {
  const env = environment(), {ctx} = env;
  const active = ctx.getFitGroupFromProductTables('mother', 'mother', 'cardigan');
  for (const size of ['', '3XL']) {
    const card = env.triggerFor(env.instance('mother', 'Cardigan', size));
    assert.equal(ctx.getFitTriggerSelectedMatch(card.trigger, active), null);
  }
  const card = env.triggerFor(env.instance('mother', 'Cardigan', 'M'));
  assert.equal(ctx.getFitTriggerSelectedMatch(card.trigger, active).row[0], 'M');
  const duplicated = {...active, rows: [...active.rows, active.rows[1].slice()]};
  assert.equal(ctx.getFitTriggerSelectedMatch(card.trigger, duplicated), null);
});

test('French role labels and four prepared controls are preserved for fr and fr-CA', () => {
  const expected = {
    chooseRoleCta: 'Choisissez un membre de la famille', chooseOptionsStep: 'Choisissez la taille et les options',
    addCurrentPiece: 'Ajouter cette pièce au panier', readyToAdd: 'Prête à être ajoutée',
  };
  for (const locale of ['fr', 'fr-CA']) {
    const env = environment(locale), {ctx} = env;
    for (const [key, value] of Object.entries(expected)) assert.equal(ctx.uiLabel(key), value);
    for (const [role, label] of [['mother', 'Maman'], ['girl', 'Fille']]) {
      const card = env.triggerFor(env.instance(role, env.typeValues[1]));
      assert.ok(card.html.includes('aria-label="Taille pour ' + label + '"'));
      assert.ok(!card.html.includes(label + ' size'));
    }
  }
});

test('one shared chart with explicit garment columns retains correct measurements for both Types', () => {
  const table = tableDom({id: 'size-chart',
    headers: ['Size', 'Chest (cm/in)', 'Dress Length (cm/in)', 'Cardigan Sleeve (cm/in)', 'Cardigan Length (cm/in)'],
    rows: [['Mother M', '88 / 34.6', '116 / 45.7', '57 / 22.4', '51 / 20.1'], ['Girl 3 Years', '64 / 25.2', '60 / 23.6', '40 / 15.7', '33 / 13']],
  }, 'Size Chart');
  const env = environment('en', [table]), {ctx} = env;
  for (const [type, garment, expected, excluded] of [['Dress', 'dress', 'Dress Length', 'Cardigan Sleeve'], ['Cardigan', 'cardigan', 'Cardigan Sleeve', 'Dress Length']]) {
    const active = ctx.getFitGroupFromProductTables('mother', 'mother', garment);
    assert.ok(active.headers.some(header => header.label === expected));
    assert.ok(!active.headers.some(header => header.label === excluded));
    const inst = env.instance('mother', type, 'M'), group = ctx.getGroupByKey('mother');
    const option = ctx.resolveVariantInGroup(group, 'M', inst.axisSelections);
    const measurement = ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option));
    assert.ok(measurement.headers.some(header => header.label === expected));
    assert.ok(!measurement.headers.some(header => header.label === excluded));
  }
});

test('single chart with Mother/Girl measurement columns preserves separate role groups', () => {
  const table = tableDom({id: 'size-chart', headers: ['Size', 'Mother Chest (cm/in)', 'Girl Chest (cm/in)'],
    rows: [['M', '88 / 34.6', '-'], ['3 Years', '-', '64 / 25.2']],
  }, 'Size Chart');
  const env = environment('en', [table], ['Dress']);
  for (const [role, expected] of [['mother', '88 / 34.6'], ['girl', '64 / 25.2']]) {
    const group = env.ctx.getFitGroupFromProductTables(role, role, 'dress');
    assert.equal(group.rows.length, 1);
    assert.equal(group.rows[0][1], expected);
  }
});

test('Arabic jacket wording only resolves to Cardigan with compatible product chart provenance', () => {
  const env = environment('ar'), {ctx} = env;
  assert.equal(ctx.getGarmentKey('سترة'), '', 'generic Arabic jacket is not a global Cardigan alias');
  assert.equal(ctx.getGarmentKeyWithChartContext('سترة', env.tables), 'cardigan');
  assert.equal(ctx.getGarmentKeyWithChartContext('سترة', [env.tables[0]]), '');
  assert.equal(ctx.getGarmentKeyWithChartContext('سترة', [tableDom(env.tables[1].record, 'Size Chart - Dress')]), '');
  const generic = tableDom({...env.tables[1].record, id: 'size-chart'}, 'جدول المقاسات');
  const single = environment('ar', [generic], ['سترة']);
  const group = single.ctx.getGroupByKey('mother');
  const context = single.ctx.getMeasurementContextForInstance(group, single.instance('mother', 'سترة', 'M'), group.options[1]);
  assert.equal(context.garmentKey, '');
  assert.equal(single.ctx.getFitGroupFromProductTables('mother', 'mother', '').rows.length, 5);
});

test('independent review: available Mother M with only Mother L source cannot borrow L tooltip values', () => {
  const env = environment(), {ctx} = env;
  const record = JSON.parse(JSON.stringify(env.tables[1].record));
  record.rows = [record.rows.find(row => row[0] === 'Mother L')];
  assert.ok(record.rows[0]);
  env.setTables([env.tables[0], tableDom(record, 'Size Chart - Cardigan')]);
  const group = ctx.getGroupByKey('mother');
  const inst = env.instance('mother', 'Cardigan', 'M');
  const option = ctx.resolveVariantInGroup(group, 'M', inst.axisSelections);
  assert.equal(ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option)), null);
});

test('independent review: Cardigan ID and heading cannot override explicit Dress Length header', () => {
  const env = environment(), {ctx} = env;
  const record = JSON.parse(JSON.stringify(env.tables[1].record));
  record.headers = record.headers.map(header => header.includes('Sleeve Length') ? 'Dress Length (cm/in)' : header);
  env.setTables([env.tables[0], tableDom(record, 'Size Chart - Cardigan')]);
  const result = ctx.getFitGroupFromProductTables('mother', 'mother', 'cardigan');
  assert.ok(result === null || !JSON.stringify(result.headers).includes('Dress Length'));
  const group = ctx.getGroupByKey('mother'), inst = env.instance('mother', 'Cardigan', 'M');
  const option = ctx.resolveVariantInGroup(group, 'M', inst.axisSelections);
  const tooltip = ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option));
  assert.ok(tooltip === null || !JSON.stringify(tooltip.headers).includes('Dress Length'));
});

test('exact normalized XXL/2XL aliases remain available without nearby size substitution', () => {
  const env = environment(), {ctx} = env, group = ctx.getGroupByKey('mother');
  const inst = env.instance('mother', 'Cardigan', 'XXL');
  const option = {...ctx.resolveVariantInGroup(group, '2XL', inst.axisSelections), sizeLabel: 'XXL', fullLabel: 'Mother XXL'};
  const measurement = ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option));
  assert.ok(measurement);
  assert.ok(ctx.comparableSizeTokens(measurement.row[0]).includes('adult:2xl'));
});

test('a single-role mixed garment-column chart retains exact Type-specific tooltips', () => {
  const table = tableDom({id: 'size-chart', headers: ['Size', 'Dress Length (cm/in)', 'Cardigan Length (cm/in)'],
    rows: [['Mother M', '116 / 45.7', '51 / 20.1']],
  }, 'Size Chart');
  const env = environment('en', [table]), {ctx} = env, group = ctx.getGroupByKey('mother');
  for (const [type, expected] of [['Dress', '116 / 45.7'], ['Cardigan', '51 / 20.1']]) {
    const inst = env.instance('mother', type, 'M');
    const option = ctx.resolveVariantInGroup(group, 'M', inst.axisSelections);
    const measurement = ctx.findMeasurementsForOption(group, option, ctx.getMeasurementContextForInstance(group, inst, option));
    assert.equal(measurement.row[1], expected);
    assert.equal(measurement.headers.length, 2);
  }
});
