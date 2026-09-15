const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');
const crypto = require('crypto');

const repo = path.resolve(__dirname, '../../../../..');
const previous = path.join(repo, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/faq-sizing-truth-20260914/diagnostics/source');
const sources = {
  main: JSON.parse(fs.readFileSync(path.join(previous, 'main-module-checksum-bound-source.json'), 'utf8')).content,
  candidate: fs.readFileSync(path.join(repo, 'assets/product-desktop-ux-20260513-ruler-sync.js'), 'utf8'),
};
const digest = text => crypto.createHash('sha256').update(text).digest('hex');
assert.equal(digest(sources.main), 'a2d55e4177b65213ebce2d842f0e8cbedaff486e9aee46bfc20b95c986e33024');
assert.equal(digest(sources.candidate), '3f830b1bd48153ee4ac429240928a2eb8316e95a436e3c53e8743d3d8c5bba20');

function extract(source, name) {
  const match = new RegExp('^([ \\t]*)function ' + name + '\\(', 'm').exec(source);
  assert(match, name);
  const tail = source.slice(match.index + match[0].length);
  const next = new RegExp('^' + match[1] + 'function ', 'm').exec(tail);
  assert(next, 'Next declaration for ' + name);
  const text = source.slice(match.index, match.index + match[0].length + next.index).trimEnd();
  return { text, line: source.slice(0, match.index).split('\n').length, sha256: digest(text) };
}

const names = [
  'stripDiacritics', 'replaceLocaleDigits', 'normalizeText', 'containsDictionaryToken', 'isTypeLikeLabel',
  'getGarmentKeys', 'getGarmentKey', 'getSingularGarmentKey', 'getCurrentOptionContext', 'getOptionNameFromControl',
  'getAxisNamesForGroup', 'getTypeAxisNamesForGroup', 'getOptionTypeValue', 'getTypeValuesForGroupSize',
  'getSelectedTypeValue', 'getPendingMeasurementAxisLabel', 'getMeasurementGarmentKey', 'getMeasurementContextForInstance',
  'getSelectedGuideTypeValue', 'getSizeGuideTableContextText', 'tableMatchesSelectedType', 'contextContainsGarmentKey',
  'getSizeGuideTable', 'getFitGroupFromProductTables', 'getFitModalGroups', 'findActiveFitGroupInList',
  'getFitModalActiveGroup', 'pruneFitGroupForGarment', 'getFitHeaderGarmentKeys', 'fitGarmentKeysCompatible',
  'isSharedFitMeasurementHeader', 'pruneGuideGroupColumns', 'isGuideEmptyValue', 'cellText', 'renderInlineFitPanel',
  'makeSizeMeasurementLookup', 'makeMeasurementEntryKey', 'normalizeSizeKey', 'addSizeMeasurementEntry',
  'findMeasurementsForOption', 'garmentKeysCompatible',
];
const lineage = names.map(name => ({
  name,
  main: extract(sources.main, name),
  candidate: extract(sources.candidate, name),
})).map(({name, main, candidate}) => ({
  name, mainLine: main.line, candidateLine: candidate.line,
  mainSha256: main.sha256, candidateSha256: candidate.sha256,
  identical: main.text === candidate.text,
}));

function makeContext(source, recognizeCardigan) {
  const ctx = { console };
  vm.createContext(ctx);
  const typeTokens = source.match(/var TYPE_LABEL_TOKENS = \[[\s\S]*?\n\];/);
  assert(typeTokens);
  let code = typeTokens[0] + '\n' + names.map(name => extract(source, name).text).join('\n');
  if (recognizeCardigan) {
    const original = extract(source, 'getGarmentKeys').text;
    const lastReturn = original.lastIndexOf('  return keys;');
    assert(lastReturn > -1);
    const proposed = original.slice(0, lastReturn) +
      "  if (/(^|[^a-z])cardigans?([^a-z]|$)/i.test(text)) add('cardigan');\n" + original.slice(lastReturn);
    code = code.replace(original, proposed);
  }
  vm.runInContext(code, ctx);
  return ctx;
}

function table(id, caption, markers, sleeve) {
  const headers = ['Size', 'Chest/Bust', sleeve ? 'Sleeve Length' : 'Skirt Length', 'Garment Length']
    .map(label => ({ raw: label, label, units: [] }));
  const groups = ['mother', 'girl'].map((key, index) => ({
    key, label: key, helper: '', headers,
    rows: [['S', ...markers.map(value => String(value + index))]],
  }));
  return {
    id, previousElementSibling: { tagName: 'H3', textContent: caption, previousElementSibling: null },
    parsed: { headers, rows: groups.flatMap(group => group.rows), groups },
  };
}

const results = [];
for (const [label, source] of Object.entries(sources)) {
  for (const recognizeCardigan of [false, true]) {
    const c = makeContext(source, recognizeCardigan);
    const dress = table('size-chart', 'Size Chart - Dress', [111, 222, 333], false);
    const cardigan = table('size-chart-cardigan', 'Size Chart - Cardigan', [444, 555, 666], true);
    const nativeControl = { value: 'Dress', getAttribute: () => 'options[Type]' };
    const nativeControls = { querySelectorAll: () => [nativeControl] };
    let tables = [dress, cardigan];
    const description = { querySelectorAll: () => tables };
    const root = { querySelector: () => description, querySelectorAll: () => [] };
    let rendered = null;
    const panel = {
      hidden: true, style: { setProperty() {} },
      hasAttribute: name => name === 'hidden' && panel.hidden,
      removeAttribute: name => { if (name === 'hidden') panel.hidden = false; },
      setAttribute: name => { if (name === 'hidden') panel.hidden = true; },
    };
    Object.assign(c, {
      getCurrentVariantSelects: () => nativeControls,
      getCurrentDescriptionRoot: () => description,
      getImageBasedSizeGuidePreset: () => null,
      getSelectedRoleKeyForTableSelection: () => 'mother',
      tableHasCompatibleSelectedRole: () => true,
      parseSizeGuideTable: value => value.parsed,
      buildSizeGuideGroups: value => value.groups,
      pruneFitGroupForRole: group => group,
      areSizeGuideRolesCompatible: (a, b) => a === b,
      sizeGuideRoot: root, compareLabel: 'Synthetic comparison',
      document: { getElementById: () => panel, querySelector: () => description },
      isInlineFitMobileViewport: () => false,
      getFitTriggerSelectedMatch: () => null,
      getSelectedGuideMatch: () => null,
      getSelectedSizeState: () => ({}),
      renderGuideUnitToggle: () => '',
      escapeHtml: String,
      renderTableCard: (headers, rows, _label, _helper, _match, role) => {
        rendered = { headers: headers.map(header => header.label), rows, role };
        return JSON.stringify(rendered);
      },
      bindInlineFitPanelScroll() {}, bindUnitToggleEvents() {},
      comparableSizeTokens: value => [String(value).toLowerCase()],
    });
    const cachedTable = c.getSizeGuideTable(root, null, c.getSelectedGuideTypeValue());
    c.parsed = cachedTable.parsed;
    c.groups = cachedTable.parsed.groups;

    for (const role of ['mother', 'girl']) {
      for (const selectedType of ['Dress', 'Cardigan']) {
        const group = {
          roleKey: role, key: role, label: role,
          options: ['Dress', 'Cardigan'].map(Type => ({ sizeLabel: 'S', axes: { Type } })),
        };
        const inst = { sizeLabel: '', axisSelections: { Type: selectedType } };
        const measurement = c.getMeasurementContextForInstance(group, inst, null);
        const attrs = {
          'aria-controls': 'synthetic-panel', 'data-fit-group-key': role, 'data-fit-role-key': role,
          'data-fit-garment-key': measurement.ambiguous ? '' : measurement.garmentKey,
        };
        const trigger = { getAttribute: key => attrs[key] || '', setAttribute: (key, value) => { attrs[key] = value; } };
        panel.hidden = true; rendered = null;
        assert.equal(c.renderInlineFitPanel(trigger), true);
        const expectedTable = selectedType === 'Cardigan' && recognizeCardigan ? cardigan : dress;
        const expected = expectedTable.parsed.groups.find(value => value.key === role);
        assert.equal(rendered.rows[0][1], expected.rows[0][1]);
        assert.equal(rendered.headers.includes('Sleeve Length'), expectedTable === cardigan);
        assert.equal(rendered.headers.includes('Skirt Length'), expectedTable === dress);
        results.push({ source: label, mode: recognizeCardigan ? 'IN_MEMORY_CARDIGAN_RECOGNITION_ONLY' : 'UNCHANGED_SOURCE', role,
          selectedType, nativeType: c.getSelectedGuideTypeValue(), triggerGarmentKey: attrs['data-fit-garment-key'],
          renderedRows: rendered.rows, renderedHeaders: rendered.headers,
          expectedSyntheticChart: expectedTable.id,
        });
      }
    }

    const lookup = c.makeSizeMeasurementLookup();
    c.addSizeMeasurementEntry(lookup, 'mother', c.getGarmentKey('Dress'), 'S', dress.parsed.headers, dress.parsed.groups[0].rows[0]);
    c.addSizeMeasurementEntry(lookup, 'mother', c.getGarmentKey('Cardigan'), 'S', cardigan.parsed.headers, cardigan.parsed.groups[0].rows[0]);
    c.buildSizeMeasurementsLookup = () => lookup;
    const tooltip = c.findMeasurementsForOption({roleKey: 'mother', label: 'Mother'}, { sizeLabel: 'S' }, {garmentKey: c.getGarmentKey('Cardigan')});
    assert.equal(JSON.stringify(tooltip.row), JSON.stringify(cardigan.parsed.groups[0].rows[0]));
    results.push({source: label, mode: recognizeCardigan ? 'IN_MEMORY_CARDIGAN_RECOGNITION_ONLY' : 'UNCHANGED_SOURCE',
      case: 'compact-tooltip-cardigan', returnedGarmentKey: tooltip.garmentKey, row: tooltip.row,
      explanation: recognizeCardigan ? 'Exact role + cardigan key' : 'Untyped Cardigan entry overwrites generic role/size lookup; apparent success is not exact garment discrimination'});

    nativeControl.value = 'Cardigan';
    assert.equal(c.getSizeGuideTable(root, null, c.getSelectedGuideTypeValue()).id, cardigan.id);
    results.push({source: label, mode: recognizeCardigan ? 'IN_MEMORY_CARDIGAN_RECOGNITION_ONLY' : 'UNCHANGED_SOURCE',
      case: 'native-controls-cardigan', selectedTable: cardigan.id, explanation: 'Raw native type matching can find Cardigan; builder selection is a separate state path'});
  }
}

const result = {
  status: 'PASS_SOURCE_DIAGNOSIS_AND_BOUNDED_IN_MEMORY_PROPOSAL',
  syntheticOnly: true,
  sourceSha256: Object.fromEntries(Object.entries(sources).map(([key, text]) => [key, digest(text)])),
  lineage, cases: results,
  unchangedSourceCoreFunctionsIdentical: lineage.every(item => item.identical),
  isolation: {
    actualSourceExecuted: 'Garment classifier, builder measurement context, native type reader, source-table selector, inline-fit routing, garment pruning, compact lookup index/read',
    modeledDependencies: 'Synthetic parsed tables/groups, fixed role compatibility and role pruning, token generation, no-op display bindings; table parser, broader role inference and real DOM rendering not tested',
    numericData: 'Invented markers 111/222/333 and 444/555/666; no actual product measurement cells copied',
    writes: 'This packet only; no theme, product, test suite, browser, Git, canonical, network or API writes',
  },
};
fs.writeFileSync(path.join(__dirname, 'HARNESS_RESULT.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({status: result.status, cases: result.cases.length, identicalFunctions: result.lineage.filter(item => item.identical).length, totalFunctions: result.lineage.length}));
