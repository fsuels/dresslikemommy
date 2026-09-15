const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const repo = path.resolve(__dirname, '../../../../..');
const sourcePath = process.argv[2] ? path.resolve(process.argv[2]) : path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js');
const source = fs.readFileSync(sourcePath, 'utf8');
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



const sourceSha256 = require('node:crypto').createHash('sha256').update(source).digest('hex');
const ctx = environment('fr').ctx;
const observations = [];
function observe(name, actual, expected) {
  observations.push({name, actual, expected, pass:JSON.stringify(actual) === JSON.stringify(expected)});
}
observe('French header po normalization',ctx.normalizeGuideUnit('po'),'in');
observe('French header pouces normalization',ctx.normalizeGuideUnit('pouces'),'in');
observe('French paired source imperial value, comma and wording preserved',
  JSON.parse(JSON.stringify(ctx.extractValueForUnit('80 cm / 31,5 pouces',{units:['cm','po']},'in'))),
  {value:'31,5 pouces',unit:'in'});
observe('French paired source metric value preserved',
  JSON.parse(JSON.stringify(ctx.extractValueForUnit('80 cm / 31,5 pouces',{units:['cm','po']},'cm'))),
  {value:'80 cm',unit:'cm'});
observe('English paired source imperial holdout',
  JSON.parse(JSON.stringify(ctx.extractValueForUnit('80 cm / 31.5 in',{units:['cm','in']},'in'))),
  {value:'31.5 in',unit:'in'});
observe('Arabic paired source imperial holdout',
  JSON.parse(JSON.stringify(ctx.extractValueForUnit('80 سم / 31.5 بوصة',{units:['سم','بوصة']},'in'))),
  {value:'31.5 بوصة',unit:'in'});
ctx.unitSystem = 'imperial';
const rendered = ctx.buildMeasurementsHtml({headers:[{label:'Taille',units:[]},{label:'Poitrine/Buste',units:['cm','po']}],row:['S','80 cm / 31,5 pouces']});
observe('Compact rendered header and value use imperial source together',rendered.includes('<dt>Poitrine/Buste (in)</dt>') && rendered.includes('<dd>31,5 pouces</dd>') && !rendered.includes('80 cm'),true);
ctx.unitSystem = 'metric';
const restored = ctx.buildMeasurementsHtml({headers:[{label:'Taille',units:[]},{label:'Poitrine/Buste',units:['cm','po']}],row:['S','80 cm / 31,5 pouces']});
observe('Compact rendered metric return preserves source',restored.includes('<dt>Poitrine/Buste (cm)</dt>') && restored.includes('<dd>80 cm</dd>'),true);
console.log(JSON.stringify({sourcePath,sourceSha256,observations},null,2));
if (observations.some(x=>!x.pass)) process.exitCode=1;
