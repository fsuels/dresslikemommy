--- candidate-before/assets/product-desktop-ux-20260513-ruler-sync.js
+++ candidate-after/assets/product-desktop-ux-20260513-ruler-sync.js
@@ -313,15 +313,15 @@
   zh: { mother: '妈妈', father: '爸爸', girl: '女孩', boy: '男孩', child: '儿童', baby: '婴儿', adult: '成人' },
 };
 var GARMENT_LABELS_BY_LOCALE = {
-  en: { dress: 'Dress', shirt: 'Shirt', shorts: 'Shorts', top: 'Top', romper: 'Romper', pants: 'Pants', shirtShortsSet: 'Shirt & Shorts Set' },
-  ar: { dress: 'فستان', shirt: 'قميص', shorts: 'شورت', top: 'توب', romper: 'رومبر', pants: 'بنطال', shirtShortsSet: 'طقم قميص وشورت' },
+  en: { dress: 'Dress', cardigan: 'Cardigan', shirt: 'Shirt', shorts: 'Shorts', top: 'Top', romper: 'Romper', pants: 'Pants', shirtShortsSet: 'Shirt & Shorts Set' },
+  ar: { dress: 'فستان', cardigan: 'سترة', shirt: 'قميص', shorts: 'شورت', top: 'توب', romper: 'رومبر', pants: 'بنطال', shirtShortsSet: 'طقم قميص وشورت' },
   cs: { dress: 'Šaty', shirt: 'Košile', shorts: 'Šortky', top: 'Top', romper: 'Overal', pants: 'Kalhoty', shirtShortsSet: 'Set košile a šortek' },
   da: { dress: 'Kjole', shirt: 'Skjorte', shorts: 'Shorts', top: 'Top', romper: 'Heldragt', pants: 'Bukser', shirtShortsSet: 'Skjorte- og shortssæt' },
   de: { dress: 'Kleid', shirt: 'Hemd', shorts: 'Shorts', top: 'Top', romper: 'Strampler', pants: 'Hose', shirtShortsSet: 'Hemd- und Shorts-Set' },
   el: { dress: 'Φόρεμα', shirt: 'Πουκάμισο', shorts: 'Σορτς', top: 'Τοπ', romper: 'Φορμάκι', pants: 'Παντελόνι', shirtShortsSet: 'Σετ πουκάμισο και σορτς' },
   es: { dress: 'Vestido', shirt: 'Camisa', shorts: 'Shorts', top: 'Top', romper: 'Pelele', pants: 'Pantalón', shirtShortsSet: 'Conjunto de camisa y shorts' },
   fi: { dress: 'Mekko', shirt: 'Paita', shorts: 'Shortsit', top: 'Yläosa', romper: 'Haalari', pants: 'Housut', shirtShortsSet: 'Paita- ja shortsisetti' },
-  fr: { dress: 'Robe', shirt: 'Chemise', shorts: 'Short', top: 'Haut', romper: 'Barboteuse', pants: 'Pantalon', shirtShortsSet: 'Ensemble chemise et short' },
+  fr: { dress: 'Robe', cardigan: 'Cardigan', shirt: 'Chemise', shorts: 'Short', top: 'Haut', romper: 'Barboteuse', pants: 'Pantalon', shirtShortsSet: 'Ensemble chemise et short' },
   he: { dress: 'שמלה', shirt: 'חולצה', shorts: 'מכנסיים קצרים', top: 'טופ', romper: 'אוברול', pants: 'מכנסיים', shirtShortsSet: 'סט חולצה ומכנסיים קצרים' },
   hi: { dress: 'ड्रेस', shirt: 'शर्ट', shorts: 'शॉर्ट्स', top: 'टॉप', romper: 'रोम्पर', pants: 'पैंट', shirtShortsSet: 'शर्ट और शॉर्ट्स सेट' },
   it: { dress: 'Vestito', shirt: 'Camicia', shorts: 'Shorts', top: 'Top', romper: 'Pagliaccetto', pants: 'Pantaloni', shirtShortsSet: 'Set camicia e shorts' },
@@ -520,6 +520,8 @@
     decreaseQuantity: 'Diminuer la quantité',
     increaseQuantity: 'Augmenter la quantité',
     findFit: 'Trouver la taille pour {role}',
+    roleSize: 'Taille pour {role}',
+    fitUnavailable: 'Le guide des tailles est indisponible pour cette sélection.',
     addRole: '+ Ajouter {role}',
     addAnotherFamilyMember: 'Ajouter un autre membre de la famille',
     customerPhotos: 'Photos clients',
@@ -675,6 +677,8 @@
   },
   ar: {
     chooseRoleStep: "اختر من سيرتدي هذه القطعة",
+    pickAxis: 'اختر {axis}',
+    fitUnavailable: 'دليل المقاسات غير متاح لهذا الاختيار.',
     chooseOptionsStep: "اختر المقاس والخيارات",
     chooseRoleCta: "اختر فردًا من العائلة",
     addCurrentPiece: "أضف هذه القطعة إلى السلة",
@@ -813,7 +817,7 @@
     key: 'girl',
     label: 'Girl',
     labels: { ar: 'البنت', es: 'Niña', fr: 'Fille' },
-    aliases: ['girl', 'daughter', 'daughter dress', 'hija', 'filha', 'figlia', 'tochter', 'fille', 'daughter', 'nina', 'niña', 'menina', 'ragazza', 'bambina', 'tyttö', 'mädchen', 'maedchen', 'pige', 'jente', 'flicka', 'dziewczynka', 'dívka', 'κορίτσι', 'fată', 'אילדה', 'ילדה', 'девочка', 'дочь', '女孩', '女の子', '娘', '여아', '딸', 'लड़की', 'البنت', 'ابنة', 'الابنة', 'فتاة', 'الفتاة'],
+    aliases: ['girl', 'daughter', 'daughter dress', 'hija', 'filha', 'figlia', 'tochter', 'fille', 'daughter', 'nina', 'niña', 'menina', 'ragazza', 'bambina', 'tyttö', 'mädchen', 'maedchen', 'pige', 'jente', 'flicka', 'dziewczynka', 'dívka', 'κορίτσι', 'fată', 'אילדה', 'ילדה', 'девочка', 'дочь', '女孩', '女の子', '娘', '여아', '딸', 'लड़की', 'البنت', 'ابنة', 'الابنة', 'فتاة', 'الفتاة', 'للبنات عمر', 'للبنات'],
   },
   {
     key: 'boy',
@@ -1177,6 +1181,9 @@
   if (/(dress|skirt|robe|vestido|vestito|kleid|jurk|kjole|sukienka|rochie|плать|فستان|שמלה|ड्रेस|ワンピース|드레스|连衣裙|連衣裙|洋裝)/i.test(text)) {
     add('dress');
   }
+  if (/(\bcardigans?\b|كارديجان)/i.test(text)) {
+    add('cardigan');
+  }
   if (/(shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص|חולצה|शर्ट|シャツ|셔츠|衬衫|襯衫)/i.test(text)) {
     add('shirt');
   }
@@ -1204,6 +1211,61 @@
 function getSingularGarmentKey(value) {
   var keys = getGarmentKeys(value);
   return keys.length === 1 ? keys[0] : '';
+}
+
+function getProductTypeValues(productData) {
+  var values = [];
+  var options = productData && productData.options || [];
+  var sizeIndex = findSizeOptionIndex(options);
+  (productData && productData.variants || []).forEach(function (variant) {
+    var value = getTypeOptionValue(variant, options, sizeIndex);
+    if (value && values.indexOf(value) === -1) values.push(value);
+  });
+  return values;
+}
+
+function getSizeChartContextText(table) {
+  if (!table) return '';
+  var context = [table.id || ''];
+  var previous = table.previousElementSibling;
+  while (previous) {
+    if (/^H[1-6]$/i.test(previous.tagName)) {
+      context.push(cellText(previous));
+      break;
+    }
+    if (/^TABLE$/i.test(previous.tagName)) break;
+    previous = previous.previousElementSibling;
+  }
+  return context.join(' ');
+}
+
+function getSizeChartGarmentKey(table, productData, tableCount) {
+  var keys = getGarmentKeys(getSizeChartContextText(table));
+  if (keys.length) return keys.length === 1 ? keys[0] : '';
+  if (Array.from(table.querySelectorAll('tr:first-child th, tr:first-child td')).some(function (cell, index) {
+    return index > 0 && getGarmentKeys(cellText(cell)).length;
+  })) return '';
+  // A single generic chart can inherit a product's only Type. Multiple
+  // Types or multiple charts require explicit table/header provenance.
+  var types = getProductTypeValues(productData);
+  return tableCount === 1 && types.length === 1 ? getSingularGarmentKey(types[0]) : '';
+}
+
+function getGarmentKeyWithChartContext(value, tables) {
+  var key = getSingularGarmentKey(value);
+  if (key) return key;
+  // This Arabic Type also means jacket. Resolve it as Cardigan only
+  // when this product actually supplies the canonical Cardigan chart.
+  if (normalizeText(value) === 'سترة' && (tables || []).some(function (table) {
+    return table.id === 'size-chart-cardigan' && getSingularGarmentKey(getSizeChartContextText(table)) === 'cardigan';
+  })) return 'cardigan';
+  return '';
+}
+
+function getProductSizeChartTables(wrapper) {
+  var sourceRoot = wrapper.closest('[id^="MainProduct-"]') || wrapper;
+  var descriptionRoot = sourceRoot.querySelector('[data-product-description]');
+  return descriptionRoot ? Array.from(descriptionRoot.querySelectorAll('table#size-chart, table[id*="size-chart"], table.size-chart')) : [];
 }
 
 function isSharedFitMeasurementHeader(header) {
@@ -1889,22 +1951,7 @@
   }
 
   function getSizeMeasurementTableContextText(table) {
-    if (!table) return '';
-
-    var context = [];
-    if (table.id) context.push(table.id);
-
-    var previous = table.previousElementSibling;
-    while (previous) {
-      if (/^H[1-6]$/i.test(previous.tagName)) {
-        context.push(cellText(previous));
-        break;
-      }
-      if (/^TABLE$/i.test(previous.tagName)) break;
-      previous = previous.previousElementSibling;
-    }
-
-    return context.join(' ');
+    return getSizeChartContextText(table);
   }
 
   function comparableSizeTokens(value) {
@@ -2145,12 +2192,12 @@
     return keys;
   }
 
-  function pruneMeasurementsForRole(roleKey, headers, row, garmentKey) {
+  function pruneMeasurementsForRole(roleKey, headers, row, garmentKey, hasDeclaredGarmentContext) {
     if (!headers || !row || !row.length) return null;
     var hasRoleColumns = headers.some(function (header, index) {
       return index > 0 && !!parseRoleFromHeader(header);
     });
-    var hasGarmentHeaders = !!garmentKey && headers.some(function (header, index) {
+    var hasGarmentHeaders = !!garmentKey && !hasDeclaredGarmentContext && headers.some(function (header, index) {
       return index > 0 && headerGarmentKeys(header).length > 0;
     });
 
@@ -2218,6 +2265,11 @@
   }
 
   function addPrunedSizeMeasurementEntries(lookup, roleKey, contextGarmentKey, label, headers, row) {
+    if (contextGarmentKey) {
+      var tableMeasurements = pruneMeasurementsForRole(roleKey, headers, row, contextGarmentKey, true);
+      if (tableMeasurements) addSizeMeasurementEntry(lookup, roleKey, contextGarmentKey, label, tableMeasurements.headers, tableMeasurements.row);
+      return;
+    }
     var headerGarmentKeys = getMeasurementGarmentKeysFromHeaders(headers);
     var targetGarmentKeys = headerGarmentKeys.length ? headerGarmentKeys : [];
     if (!targetGarmentKeys.length && contextGarmentKey) targetGarmentKeys.push(contextGarmentKey);
@@ -2235,10 +2287,12 @@
     });
   }
 
-  function indexParsedSizeGuideRows(lookup, parsed, table) {
+  function indexParsedSizeGuideRows(lookup, parsed, table, tableCount) {
     var contextText = getSizeMeasurementTableContextText(table);
+    if (getGarmentKeys(contextText).length > 1) return;
     var contextRoleKeys = getMeasurementRoleKeysFromText(contextText);
-    var contextGarmentKey = getSingularGarmentKey(contextText);
+    var contextGarmentKey = getSizeChartGarmentKey(table, productData, tableCount);
+    var firstEntryIndex = lookup.entries.length;
     var grouped = typeof buildSizeGuideGroups === 'function' ? buildSizeGuideGroups(parsed) : [];
 
     grouped.forEach(function (group) {
@@ -2253,29 +2307,20 @@
 
       var parsedRole = parseRoleFromSizeLabel(rawLabel);
       if (parsedRole) {
-        var parsedRoleMeasurements = pruneMeasurementsForRole(parsedRole.key, parsed.headers, row, contextGarmentKey);
-        if (parsedRoleMeasurements) {
-          addSizeMeasurementEntry(
-            lookup,
-            parsedRole.key,
-            contextGarmentKey,
-            parsedRole.sizeLabel || rawLabel,
-            parsedRoleMeasurements.headers,
-            parsedRoleMeasurements.row
-          );
-        }
+        addPrunedSizeMeasurementEntries(lookup, parsedRole.key, contextGarmentKey, parsedRole.sizeLabel || rawLabel, parsed.headers, row);
       }
 
       contextRoleKeys.forEach(function (roleKey) {
         var baseRoleKey = inferBaseRoleKeyFromMeasurementSize(rawLabel);
         if (baseRoleKey && !roleKeysCompatible(roleKey, baseRoleKey)) return;
-        var roleMeasurements = pruneMeasurementsForRole(roleKey, parsed.headers, row, contextGarmentKey);
-        if (!roleMeasurements) return;
         var roleSizeLabel = parsedRole && parsedRole.sizeLabel ? parsedRole.sizeLabel : rawLabel;
-        addSizeMeasurementEntry(lookup, roleKey, contextGarmentKey, roleSizeLabel, roleMeasurements.headers, roleMeasurements.row);
+        addPrunedSizeMeasurementEntries(lookup, roleKey, contextGarmentKey, roleSizeLabel, parsed.headers, row);
       });
 
-      addSizeMeasurementEntry(lookup, '', contextGarmentKey, rawLabel, parsed.headers, row);
+      addPrunedSizeMeasurementEntries(lookup, '', contextGarmentKey, rawLabel, parsed.headers, row);
+    });
+    lookup.entries.slice(firstEntryIndex).forEach(function (entry) {
+      entry.sourceTable = table;
     });
   }
 
@@ -2283,13 +2328,14 @@
     if (sizeMeasurementsByLabel) return sizeMeasurementsByLabel;
     sizeMeasurementsByLabel = makeSizeMeasurementLookup();
 
-    var tables = Array.from(document.querySelectorAll('table#size-chart, table[id*="size-chart"], table.size-chart'));
+    var tables = getProductSizeChartTables(wrapper);
+    sizeMeasurementsByLabel.allowGeneric = tables.length === 1 && getProductTypeValues(productData).length <= 1;
     if (!tables.length || typeof parseSizeGuideTable !== 'function') return sizeMeasurementsByLabel;
 
     tables.forEach(function (table) {
       var parsed = parseSizeGuideTable(table);
       if (!parsed || !parsed.rows || !parsed.headers) return;
-      indexParsedSizeGuideRows(sizeMeasurementsByLabel, parsed, table);
+      indexParsedSizeGuideRows(sizeMeasurementsByLabel, parsed, table, tables.length);
     });
 
     return sizeMeasurementsByLabel;
@@ -2316,40 +2362,36 @@
     }
     if (option.sizeLabel) candidates.push(option.sizeLabel);
 
-    for (var i = 0; i < candidates.length; i += 1) {
-      var key = normalizeSizeKey(candidates[i]);
-      var roleGarmentMatch = lookup.byRoleGarmentLabel[makeMeasurementEntryKey(roleKey, garmentKey, key)];
-      if (roleGarmentMatch) return roleGarmentMatch;
-      var roleMatch = lookup.byRoleLabel[makeMeasurementEntryKey(roleKey, '', key)];
-      if (roleMatch && garmentKeysCompatible(garmentKey, roleMatch.garmentKey)) return roleMatch;
-    }
-
+    if (measurementContext.ambiguous || (!garmentKey && !lookup.allowGeneric)) return null;
     var selectedTokens = mergeComparableSizeTokens(candidates);
+    var candidateKeys = candidates.map(normalizeSizeKey);
     var bestMatch = null;
     var bestScore = Infinity;
+    var ambiguous = false;
     lookup.entries.forEach(function (entry) {
-      if (!roleKeysCompatible(roleKey, entry.roleKey)) return;
-      if (!garmentKeysCompatible(garmentKey, entry.garmentKey)) return;
+      var entryRole = entry.roleKey || inferBaseRoleKeyFromMeasurementSize(entry.row[0]);
+      if (!roleKeysCompatible(roleKey, entryRole)) return;
+      if (!entryRole && !lookup.allowGeneric) return;
+      if (garmentKey !== entry.garmentKey && !(lookup.allowGeneric && !entry.garmentKey)) return;
+      if (garmentKey && !entry.garmentKey && getMeasurementGarmentKeysFromHeaders(entry.headers).length) return;
 
       var tokenRank = sizeTokenMatchRank(selectedTokens, entry.sizeTokens);
-      if (!tokenRank) return;
-
-      var score =
-        tokenRank * 10 +
-        (entry.roleKey === roleKey ? 0 : 2) +
-        (entry.garmentKey && entry.garmentKey === garmentKey ? 0 : 1);
+      // A size pill promises this size's measurements, not a nearby fit.
+      if (tokenRank !== 1) return;
+      var score = tokenRank * 10 + (entry.roleKey === roleKey ? 0 : 2) +
+        (candidateKeys.indexOf(entry.labelKey) !== -1 ? 0 : 1);
       if (score < bestScore) {
         bestScore = score;
         bestMatch = entry;
+        ambiguous = false;
+      } else if (score === bestScore && bestMatch && (
+        entry.sourceTable !== bestMatch.sourceTable ||
+        JSON.stringify(entry.row.slice(1)) !== JSON.stringify(bestMatch.row.slice(1))
+      )) {
+        ambiguous = true;
       }
     });
-    if (bestMatch) return bestMatch;
-
-    for (var fallbackIndex = 0; fallbackIndex < candidates.length; fallbackIndex += 1) {
-      var fallbackKey = normalizeSizeKey(candidates[fallbackIndex]);
-      if (lookup.byLabel[fallbackKey]) return lookup.byLabel[fallbackKey];
-    }
-    return null;
+    return ambiguous ? null : bestMatch;
   }
 
   function isMeaningfulMeasurementValue(value) {
@@ -2371,7 +2413,7 @@
     var parts = (typeof splitGuideMeasurementParts === 'function')
       ? splitGuideMeasurementParts(text)
       : text.split(/\s+\/\s+/).map(function (p) { return p.trim(); }).filter(Boolean);
-    var units = (header && header.units) ? header.units : [];
+    var units = (header && header.units) ? header.units.map(normalizeGuideUnit) : [];
 
     // Multi-unit cell: pick the index matching activeUnit.
     if (parts.length >= 2 && units.length >= 2) {
@@ -2453,7 +2495,7 @@
       var headerUnits = [];
       if (header && typeof header === 'object') {
         headerLabel = header.label || header.raw || '';
-        headerUnits = (header.units || []).map(function (u) { return String(u).toLowerCase(); });
+        headerUnits = (header.units || []).map(normalizeGuideUnit);
       } else {
         headerLabel = String(header || '');
       }
@@ -2646,7 +2688,7 @@
     return getTypeValuesForGroupSize(group, sizeLabel).length > 1 ? typeAxisNames[0] : '';
   }
 
-  function getMeasurementGarmentKey(group, option, context) {
+  function getMeasurementTypeValue(group, option, context) {
     var measurementContext = context || {};
     var selectedTypeValue = getSelectedTypeValue(group, measurementContext.axisSelections || {});
     var typeValue = selectedTypeValue || '';
@@ -2659,7 +2701,12 @@
     var typeAxes = getTypeAxisNamesForGroup(group);
     if (!typeValue && !typeAxes.length) typeValue = (group && (group.helperRaw || group.helper)) || '';
 
-    return getGarmentKey(typeValue);
+    return typeValue;
+  }
+
+  function getMeasurementGarmentKey(group, option, context) {
+    var typeValue = getMeasurementTypeValue(group, option, context);
+    return getGarmentKeyWithChartContext(typeValue, normalizeText(typeValue) === 'سترة' ? getProductSizeChartTables(wrapper) : []);
   }
 
   function getMeasurementContextForInstance(group, inst, option) {
@@ -2673,6 +2720,7 @@
         axisSelections: axisSelections,
         sizeLabel: sizeLabel,
         garmentKey: '',
+        typeValue: '',
       };
     }
 
@@ -2681,6 +2729,7 @@
       pendingAxisName: '',
       axisSelections: axisSelections,
       sizeLabel: sizeLabel,
+      typeValue: getMeasurementTypeValue(group, option, { axisSelections: axisSelections, sizeLabel: sizeLabel }),
       garmentKey: getMeasurementGarmentKey(group, option, {
         axisSelections: axisSelections,
         sizeLabel: sizeLabel,
@@ -3268,6 +3317,8 @@
     var fitPanelId = 'DlmInlineFitPanel-' + String(sectionId || 'product') + '-' + inst.instanceId;
     var fitMeasurementContext = selectedMeasurementContext || getMeasurementContextForInstance(group, inst, selectedPanelOption);
     var fitGarmentKey = fitMeasurementContext && !fitMeasurementContext.ambiguous ? fitMeasurementContext.garmentKey : '';
+    var instanceHelper = fitMeasurementContext && !fitMeasurementContext.ambiguous
+      ? localizeTypeLabel(fitMeasurementContext.typeValue) : '';
 
     return (
       '<div class="product-matching-set__card" data-instance-card="' +
@@ -3285,12 +3336,12 @@
       escapeHtml(group.label) +
       '</span>' +
       '</div>' +
-      (group.helper
-        ? '<span class="product-matching-set__card-helper">' + escapeHtml(group.helper) + '</span>'
+      (instanceHelper
+        ? '<span class="product-matching-set__card-helper">' + escapeHtml(instanceHelper) + '</span>'
         : '') +
       '<div class="product-matching-set__size-row">' +
       '<div class="product-matching-set__pills" role="group" aria-label="' +
-      escapeHtml(group.label + ' size') +
+      escapeHtml(uiLabel('roleSize', '{role} size', { role: group.label })) +
       '">' +
       pillsHtml +
       '</div>' +
@@ -3300,6 +3351,8 @@
       escapeHtml(group.roleKey || group.key) +
       '" data-fit-garment-key="' +
       escapeHtml(fitGarmentKey) +
+      '" data-fit-pending-axis="' +
+      escapeHtml(fitMeasurementContext && fitMeasurementContext.pendingAxisName || '') +
       '" data-fit-size-label="' +
       escapeHtml(inst.sizeLabel || '') +
       '" aria-controls="' +
@@ -4310,22 +4363,7 @@
   }
 
   function getSizeGuideTableContextText(table) {
-    if (!table) return '';
-
-    var context = [];
-    if (table.id) context.push(table.id);
-
-    var previous = table.previousElementSibling;
-    while (previous) {
-      if (/^H[1-6]$/i.test(previous.tagName)) {
-        context.push(cellText(previous));
-        break;
-      }
-      if (/^TABLE$/i.test(previous.tagName)) break;
-      previous = previous.previousElementSibling;
-    }
-
-    return normalizeText(context.join(' '));
+    return normalizeText(getSizeChartContextText(table));
   }
 
   function tableMatchesSelectedType(table, selectedTypeValue) {
@@ -4334,7 +4372,7 @@
 
     var context = getSizeGuideTableContextText(table);
     if (!context) return false;
-    var selectedGarmentKey = getGarmentKey(selectedTypeValue);
+    var selectedGarmentKey = getGarmentKeyWithChartContext(selectedTypeValue, [table]);
     var contextGarmentKey = getGarmentKey(context);
     var idGarmentKey = getGarmentKey(table.id || '');
 
@@ -4379,6 +4417,7 @@
     var text = normalizeText(context);
     if (!text || !garmentKey) return false;
     if (garmentKey === 'dress') return /(dress|skirt|robe|vestido|vestito|kleid|jurk|kjole|sukienka|rochie|плать|فستان|שמלה|ワンピース|드레스|连衣裙|連衣裙|洋裝)/i.test(text);
+    if (garmentKey === 'cardigan') return getGarmentKeys(text).indexOf('cardigan') !== -1;
     if (garmentKey === 'shirt') return /(shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص|חולצה|シャツ|셔츠|衬衫|襯衫)/i.test(text);
     if (garmentKey === 'shorts') return /(short|shorts|trunk|bermuda|шорт|شورت|מכנסיים קצרים|ショーツ|반바지|短裤|短褲)/i.test(text);
     if (garmentKey === 'shirtShortsSet') return contextContainsGarmentKey(text, 'shirt') && contextContainsGarmentKey(text, 'shorts');
@@ -5422,11 +5461,13 @@
       return areSizeGuideRolesCompatible(roleKey, rowRoleKey) || rowRoleKey === roleFamilyKey;
     });
     var hasMatchingRows = rowMatches.some(function (matches) { return matches === true; });
-    var hasNonMatchingRows = rowMatches.some(function (matches) { return matches === false; });
-    if (!hasMatchingRows || !hasNonMatchingRows) return group;
+    var groupHasRole = !!getFitRoleFamilyKey(group.key);
+    var groupMatchesRole = groupHasRole && areSizeGuideRolesCompatible(roleKey, group.key);
+    if (groupHasRole && !groupMatchesRole) return null;
+    if (!hasMatchingRows && !groupMatchesRole) return null;
 
     var filteredRows = group.rows.filter(function (_row, index) {
-      return rowMatches[index] !== false;
+      return rowMatches[index] === true || (rowMatches[index] === null && groupMatchesRole);
     });
     if (!filteredRows.length) return null;
 
@@ -5442,7 +5483,7 @@
     };
   }
 
-  function pruneFitGroupForGarment(group, garmentKey) {
+  function pruneFitGroupForGarment(group, garmentKey, hasDeclaredGarmentContext) {
     if (!group || !garmentKey || !group.headers || !group.rows) return group || null;
 
     var hasGarmentHeaders = group.headers.some(function (header, index) {
@@ -5458,7 +5499,7 @@
       .filter(function (index) {
         if (index === 0) return true;
         var headerKeys = getFitHeaderGarmentKeys(group.headers[index]);
-        if (!headerKeys.length) return isSharedFitMeasurementHeader(group.headers[index]);
+        if (!headerKeys.length) return hasDeclaredGarmentContext || isSharedFitMeasurementHeader(group.headers[index]);
         var matches = headerKeys.some(function (headerKey) {
           return fitGarmentKeysCompatible(garmentKey, headerKey);
         });
@@ -5466,7 +5507,7 @@
         return matches;
       });
 
-    if (!matchedSpecificHeader || keepIndexes.length <= 1) return null;
+    if ((!matchedSpecificHeader && !hasDeclaredGarmentContext) || keepIndexes.length <= 1) return null;
 
     var pruned = pruneGuideGroupColumns(
       keepIndexes.map(function (index) {
@@ -5518,7 +5559,8 @@
       findCompatible(normalizedRoleKey) ||
       findExact(normalizedGroupKey) ||
       findCompatible(normalizedGroupKey) ||
-      modalGroups[0];
+      findExact('all') ||
+      (!normalizedRoleKey && !normalizedGroupKey ? modalGroups[0] : null);
 
     if (!activeGroup) return null;
     var rolePrunedGroup = pruneFitGroupForRole(activeGroup, normalizedRoleKey || normalizedGroupKey);
@@ -5527,20 +5569,26 @@
   }
 
   function getFitGroupFromProductTables(groupKey, roleKey, garmentKey) {
-    if (!garmentKey) return null;
     var sourceRoot = getCurrentDescriptionRoot();
     var sourceTables = sourceRoot
       ? Array.from(sourceRoot.querySelectorAll('table#size-chart, table[id*="size-chart"], table.size-chart'))
       : [];
     if (!sourceTables.length) return null;
+    var allowGeneric = sourceTables.length === 1 && getProductTypeValues(productData).length <= 1;
+    if (!garmentKey && !allowGeneric) return null;
+    var matches = [];
 
     for (var index = 0; index < sourceTables.length; index += 1) {
       var table = sourceTables[index];
-      var contextGarmentKey = getSingularGarmentKey(getSizeGuideTableContextText(table));
-      if (contextGarmentKey && !fitGarmentKeysCompatible(garmentKey, contextGarmentKey)) continue;
+      if (getGarmentKeys(getSizeGuideTableContextText(table)).length > 1) continue;
+      var contextGarmentKey = getSizeChartGarmentKey(table, productData, sourceTables.length);
+      if (contextGarmentKey && garmentKey !== contextGarmentKey) continue;
 
       var tableParsed = parseSizeGuideTable(table);
       if (!tableParsed) continue;
+      if (!contextGarmentKey && !allowGeneric && !tableParsed.headers.some(function (header, headerIndex) {
+        return headerIndex > 0 && getFitHeaderGarmentKeys(header).indexOf(garmentKey) !== -1;
+      })) continue;
       var tableGroups = buildSizeGuideGroups(tableParsed);
       var activeGroup = findActiveFitGroupInList(tableGroups.length ? tableGroups : [{
         key: 'all',
@@ -5548,11 +5596,16 @@
         helper: '',
         headers: tableParsed.headers,
         rows: tableParsed.rows,
-      }], groupKey, roleKey, garmentKey);
-      if (activeGroup) return activeGroup;
-    }
-
-    return null;
+      }], groupKey, roleKey, contextGarmentKey ? '' : garmentKey);
+      if (activeGroup && contextGarmentKey) activeGroup = pruneFitGroupForGarment(activeGroup, garmentKey, true);
+      if (activeGroup) {
+        activeGroup.sourceTable = table;
+        activeGroup.garmentKey = contextGarmentKey || garmentKey || '';
+        matches.push(activeGroup);
+      }
+    }
+
+    return matches.length === 1 ? matches[0] : null;
   }
 
   function getFitModalActiveGroup(groupKey, roleKey, garmentKey) {
@@ -5669,15 +5722,21 @@
 
     var bestRow = null;
     var bestScore = -Infinity;
+    var ambiguousRow = false;
     activeGroup.rows.forEach(function (row) {
+      var rowTokens = buildSizeMatchTokens(getGuideRowValues(row[0]));
+      if (!Object.keys(rowTokens).some(function (token) { return selectedState.tokens[token]; })) return;
       var score = getGuideRowMatchScore(row[0], selectedState, activeGroup.key);
       if (score > bestScore) {
         bestScore = score;
         bestRow = row;
+        ambiguousRow = false;
+      } else if (score === bestScore) {
+        ambiguousRow = true;
       }
     });
 
-    if (!bestRow || bestScore === -Infinity) return null;
+    if (!bestRow || bestScore === -Infinity || ambiguousRow) return null;
     return {
       label: activeGroup.label || '',
       helper: activeGroup.helper || '',
@@ -5715,16 +5774,22 @@
     var triggerGroupKey = trigger.getAttribute('data-fit-group-key');
     var triggerRoleKey = trigger.getAttribute('data-fit-role-key');
     var triggerGarmentKey = trigger.getAttribute('data-fit-garment-key');
-    var activeGroup =
-      getFitGroupFromProductTables(triggerGroupKey, triggerRoleKey, triggerGarmentKey) ||
-      getFitModalActiveGroup(triggerGroupKey, triggerRoleKey, triggerGarmentKey);
-    if (!activeGroup) return false;
+    var pendingAxis = trigger.getAttribute('data-fit-pending-axis');
+    var activeGroup = pendingAxis ? null : getFitGroupFromProductTables(triggerGroupKey, triggerRoleKey, triggerGarmentKey);
+    if (!activeGroup) {
+      panel.innerHTML = '<p role="status">' + escapeHtml(pendingAxis
+        ? uiLabel('pickAxis', 'Pick a {axis}', { axis: pendingAxis })
+        : uiLabel('fitUnavailable', 'The size guide is unavailable for this selection.')) + '</p>';
+      panel.removeAttribute('hidden');
+      trigger.setAttribute('aria-expanded', 'true');
+      return true;
+    }
 
     var activeHeaders = activeGroup.headers || [];
     var mobileMinWidthRem = 5.2 + Math.max(activeHeaders.length - 1, 0) * 7;
     panel.style.setProperty('--dlm-fit-table-min-width', mobileMinWidthRem.toFixed(1) + 'rem');
 
-    var selectedMatch = getFitTriggerSelectedMatch(trigger, activeGroup) || getSelectedGuideMatch(getSelectedSizeState());
+    var selectedMatch = getFitTriggerSelectedMatch(trigger, activeGroup);
     panel.innerHTML =
       '<div class="product-matching-set__inline-fit-panel-bar">' +
       '<strong>' +
