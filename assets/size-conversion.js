document.addEventListener("DOMContentLoaded", function () {
  console.log("Size Conversion Script Loaded (DLM Smart Resolver v2).");
  // ---------------------------------------------------------------------------
  // UNIT CONVERSION HELPERS
  // ---------------------------------------------------------------------------
  const UNIT_SYSTEM_STORAGE_KEY = "dlm_size_chart_unit_system";
  const normalizeUnit = (unit) => String(unit || "").trim().toLowerCase();
  const formatNumericValue = (num) => {
    if (num === null || Number.isNaN(num)) return "";
    return Number(num).toFixed(2).replace(/\.00$/, "").replace(/(\.\d)0$/, "$1");
  };
  const convertValueBetweenUnits = (num, fromUnit, toUnit) => {
    const from = normalizeUnit(fromUnit);
    const to   = normalizeUnit(toUnit);
    if (!from || !to || from === to) return num;
    if (from === "cm" && to === "in") return num / 2.54;
    if (from === "in" && to === "cm") return num * 2.54;
    if (from === "kg" && to === "lbs") return num * 2.20462;
    if (from === "lbs" && to === "kg") return num / 2.20462;
    return null;
  };
  const convertMeasurementText = (rawText, fromUnit, toUnit) => {
    const text = String(rawText || "").trim();
    if (!text) return "";
    if (normalizeUnit(fromUnit) === normalizeUnit(toUnit)) return text;

    const singleMatch = text.match(/^(-?\d+(?:\.\d+)?)$/);
    if (singleMatch) {
      const convertedSingle = convertValueBetweenUnits(parseFloat(singleMatch[1]), fromUnit, toUnit);
      return convertedSingle === null ? null : formatNumericValue(convertedSingle);
    }

    const rangeMatch = text.match(/^(-?\d+(?:\.\d+)?)\s*([\-–])\s*(-?\d+(?:\.\d+)?)$/);
    if (rangeMatch) {
      const convertedMin = convertValueBetweenUnits(parseFloat(rangeMatch[1]), fromUnit, toUnit);
      const convertedMax = convertValueBetweenUnits(parseFloat(rangeMatch[3]), fromUnit, toUnit);
      if (convertedMin === null || convertedMax === null) return null;
      return formatNumericValue(convertedMin) + rangeMatch[2] + formatNumericValue(convertedMax);
    }

    return null;
  };
  const getUnitForSystem = (sourceUnit, unitSystem) => {
    const normalizedSource = normalizeUnit(sourceUnit);
    if (!normalizedSource) return "";

    if (unitSystem === "imperial") {
      if (normalizedSource === "cm") return "in";
      if (normalizedSource === "kg") return "lbs";
    }

    if (unitSystem === "metric") {
      if (normalizedSource === "in" || normalizedSource === "inch" || normalizedSource === "inches") return "cm";
      if (normalizedSource === "lb" || normalizedSource === "lbs") return "kg";
    }

    return sourceUnit;
  };
  const inferUnitFromText = (text) => {
    const match = String(text || "").toLowerCase().match(/\b(cm|in|inch|inches|kg|lb|lbs)\b/);
    if (!match) return "";
    const token = match[1];
    if (token === "inch" || token === "inches") return "in";
    if (token === "lb") return "lbs";
    return token;
  };
  const getStoredUnitSystem = () => {
    try {
      const stored = window.localStorage.getItem(UNIT_SYSTEM_STORAGE_KEY);
      return stored === "imperial" || stored === "metric" ? stored : null;
    } catch (_error) {
      return null;
    }
  };
  const storeUnitSystem = (system) => {
    try {
      window.localStorage.setItem(UNIT_SYSTEM_STORAGE_KEY, system);
    } catch (_error) {
      // no-op: localStorage may be unavailable
    }
  };
  const stripTrailingUnit = (value, unit) => {
    const text = String(value || "").trim();
    const u    = String(unit || "").trim();
    if (!u) return text;
    const escaped = u.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return text.replace(new RegExp("\\s*" + escaped + "$", "i"), "").trim();
  };
  const pickPreferredUnitIndex = (units, unitSystem) => {
    const normalizedUnits = units.map((u) => normalizeUnit(u));
    const preferredTokens = unitSystem === "imperial"
      ? ["in", "inch", "inches", "lbs", "lb"]
      : ["cm", "kg"];
    for (let i = 0; i < preferredTokens.length; i++) {
      const index = normalizedUnits.indexOf(preferredTokens[i]);
      if (index !== -1) return index;
    }
    return unitSystem === "imperial" ? Math.min(1, units.length - 1) : 0;
  };
  const getMeasurementForUnitSystem = (rawValue, units, unitSystem) => {
    const unitList = Array.isArray(units) ? units.map((u) => String(u || "").trim()).filter(Boolean) : [];
    const rawParts = String(rawValue || "").split("/").map((part) => part.trim()).filter(Boolean);

    if (unitList.length < 2) {
      if (rawParts.length >= 2) {
        const inferredUnits = rawParts.map((part) => inferUnitFromText(part));
        const usableUnits = inferredUnits.filter(Boolean);
        if (usableUnits.length >= 2) {
          const preferredIndex = pickPreferredUnitIndex(inferredUnits, unitSystem);
          const preferredUnit  = inferredUnits[preferredIndex] || inferredUnits[0];
          const selectedPart   = rawParts[preferredIndex] || rawParts[0];
          return {
            value: stripTrailingUnit(selectedPart, preferredUnit),
            unit: preferredUnit,
          };
        }
      }

      const baseRaw = rawParts[0] || String(rawValue || "").trim();
      const sourceUnit = unitList[0] || inferUnitFromText(baseRaw);
      const targetUnit = getUnitForSystem(sourceUnit, unitSystem);
      const base = stripTrailingUnit(baseRaw, sourceUnit);
      const converted = convertMeasurementText(base, sourceUnit, targetUnit);
      return {
        value: converted !== null ? converted : base,
        unit: targetUnit || sourceUnit,
      };
    }

    const preferredIndex = pickPreferredUnitIndex(unitList, unitSystem);
    const preferredUnit  = unitList[preferredIndex] || "";
    const sourceUnit     = unitList[0] || "";

    if (rawParts.length >= 2) {
      const selectedPart = rawParts[preferredIndex] || rawParts[0];
      return {
        value: stripTrailingUnit(selectedPart, preferredUnit || sourceUnit),
        unit: preferredUnit || sourceUnit,
      };
    }

    const singlePart = rawParts[0] || String(rawValue || "").trim();
    const strippedSingle = stripTrailingUnit(singlePart, sourceUnit);
    if (preferredUnit) {
      const convertedText = convertMeasurementText(strippedSingle, sourceUnit, preferredUnit);
      if (convertedText !== null) {
        return {
          value: convertedText,
          unit: preferredUnit,
        };
      }
    }

    return {
      value: strippedSingle,
      unit: sourceUnit,
    };
  };
  const escapeHtml = (value) => String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
  // ---------------------------------------------------------------------------
  // DOM REFERENCES
  // ---------------------------------------------------------------------------
  const sizeSelect        = document.querySelector("select.size-select");
  const sizeChartWrapper  = document.querySelector(".size-chart-wrapper");
  const sizeChartContent  = document.getElementById("size-chart-content");
  let selectedUnitSystem  = getStoredUnitSystem() || "metric";
  if (!sizeSelect) {
    console.error("Size dropdown not found.");
    return;
  }
  if (!sizeChartWrapper) {
    console.error("Size chart wrapper not found.");
    return;
  }
  // ---------------------------------------------------------------------------
  // HEADER PARSER
  // Reads <th> cells and returns a map of { colIndex: { name, units[] } }
  // Handles "Bust (cm/in)", "Age", "Size", etc.
  // ---------------------------------------------------------------------------
  const parseHeaders = (headerCells) => {
    const headerMap = {};
    for (let i = 0; i < headerCells.length; i++) {
      const headerText = headerCells[i].textContent.trim();
      const regex      = /^(.+?)\s*\((.*?)\)$/;
      const match      = headerText.match(regex);
      if (match) {
        let measurementName = match[1].trim();
        const unitsPart     = match[2].trim();
        const units         = unitsPart.split("/").map((u) => u.trim());
        // Correct common vendor typos
        const lower = measurementName.toLowerCase();
        if (lower === "bst")  measurementName = "Bust";
        if (lower === "wist") measurementName = "Waist";
        headerMap[i] = { name: measurementName, units };
      } else {
        // No parentheses — plain label (e.g. "Age", "Size")
        headerMap[i] = { name: headerText, units: [] };
      }
    }
    return headerMap;
  };
  // ---------------------------------------------------------------------------
  // TABLE READER
  // Returns { [factorySizeKey]: { [measurementName]: { value, units } } }
  // Also attaches raw Age and Height values to each entry for smart resolution.
  // ---------------------------------------------------------------------------
  const getFactorySizes = () => {
    const sizeChartTable = document.querySelector(
      "table#size-chart, table[id*='size-chart'], table[class*='size-chart']"
    );
    const factorySizes   = {};
    if (!sizeChartTable) {
      console.error("Size chart table not found.");
      return factorySizes;
    }
    const rows = sizeChartTable.getElementsByTagName("tr");
    if (!rows || rows.length === 0) return factorySizes;
    const headerCells = rows[0].getElementsByTagName("th");
    if (!headerCells || headerCells.length === 0) return factorySizes;
    const headerMap = parseHeaders(headerCells);
    // Find the Size column index
    let sizeIndex = -1;
    for (let i = 0; i < headerCells.length; i++) {
      if ((headerMap[i]?.name || "").toLowerCase().includes("size")) {
        sizeIndex = i;
        break;
      }
    }
    if (sizeIndex === -1) {
      console.error("No 'Size' column found in size chart table.");
      return factorySizes;
    }
    // Read every data row
    for (let i = 1; i < rows.length; i++) {
      const cells    = rows[i].getElementsByTagName("td");
      if (!cells || cells.length === 0) continue;
      const sizeName = (cells[sizeIndex]?.textContent || "").trim();
      if (!sizeName) continue;
      factorySizes[sizeName] = { _meta: { ageMin: null, ageMax: null, heightMin: null, heightMax: null } };
      for (let j = 0; j < cells.length; j++) {
        if (j === sizeIndex) continue;
        const measurementInfo = headerMap[j];
        if (!measurementInfo) continue;
        const measurementName = measurementInfo.name;
        const units           = measurementInfo.units;
        const cellContent     = (cells[j]?.textContent || "").trim();
        factorySizes[sizeName][measurementName] = { value: cellContent, units };
        // ── Harvest Age metadata for smart resolution ──
        if (measurementName.toLowerCase() === "age" && cellContent && cellContent !== "—") {
          const ageNums = cellContent.match(/[\d.]+/g);
          if (ageNums && ageNums.length >= 1) {
            factorySizes[sizeName]._meta.ageMin = parseFloat(ageNums[0]);
            factorySizes[sizeName]._meta.ageMax = parseFloat(ageNums[ageNums.length - 1]);
          }
        }
        // ── Harvest Height metadata for smart resolution ──
        if (measurementName.toLowerCase() === "height" && cellContent && cellContent !== "—") {
          const hNums = cellContent.match(/[\d.]+/g);
          if (hNums && hNums.length >= 1) {
            factorySizes[sizeName]._meta.heightMin = parseFloat(hNums[0]);
            factorySizes[sizeName]._meta.heightMax = parseFloat(hNums[hNums.length - 1]);
          }
        }
      }
    }
    return factorySizes;
  };
  // ---------------------------------------------------------------------------
  // NORMALIZE HELPER
  // ---------------------------------------------------------------------------
  function normalizeKey(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }
  // ---------------------------------------------------------------------------
  // ADULT TOKEN EXTRACTOR
  // "Mother 2XL" → "2XL", "Father XXL" → "2XL", "Adult XL" → "XL"
  // ---------------------------------------------------------------------------
  function extractAdultToken(label) {
    const m = String(label || "").toUpperCase()
      .match(/\b(XXXXL|XXXL|XXL|2XL|3XL|4XL|XL|XS|S|M|L)\b/);
    if (!m) return null;
    const raw = m[1];
    if (raw === "XXL")   return "2XL";
    if (raw === "XXXL")  return "3XL";
    if (raw === "XXXXL") return "4XL";
    return raw;
  }
  // ---------------------------------------------------------------------------
  // SMART AGE RESOLVER  ← NEW
  //
  // Extracts a numeric age range from the dropdown label, then scores every
  // factory row by how well its Age cell overlaps or is nearest.
  //
  // Scoring:
  //   +100  exact overlap  (label age falls inside factory age range)
  //   +50   partial overlap
  //   distance penalty: −|midpoint difference| (so closer rows rank higher)
  //
  // Returns: { key: factorySizeKey, isExact: bool } | null
  // ---------------------------------------------------------------------------
  function resolveByAgeRange(label, factorySizes) {
    // Extract age numbers from label, e.g. "Child 2-3 years" → [2, 3]
    const ageMatch = String(label).match(/(\d+)\s*[-–]\s*(\d+)\s*(?:yr|year|years|y\.o\.?)?/i)
                  || String(label).match(/(\d+)\s*(?:yr|year|years|y\.o\.?)/i);
    if (!ageMatch) return null;
    let labelAgeMin, labelAgeMax;
    if (ageMatch[2] !== undefined) {
      labelAgeMin = parseFloat(ageMatch[1]);
      labelAgeMax = parseFloat(ageMatch[2]);
    } else {
      labelAgeMin = parseFloat(ageMatch[1]);
      labelAgeMax = labelAgeMin;
    }
    const labelAgeMid = (labelAgeMin + labelAgeMax) / 2;
    let bestKey   = null;
    let bestScore = -Infinity;
    let bestExact = false;
    for (const [key, data] of Object.entries(factorySizes)) {
      if (key === "_meta") continue;
      const meta = data._meta;
      if (meta.ageMin === null) continue;  // row has no age data — skip
      const factAgeMin = meta.ageMin;
      const factAgeMax = meta.ageMax !== null ? meta.ageMax : meta.ageMin;
      const factAgeMid = (factAgeMin + factAgeMax) / 2;
      let score    = 0;
      let isExact  = false;
      // Overlap check
      const overlapMin = Math.max(labelAgeMin, factAgeMin);
      const overlapMax = Math.min(labelAgeMax, factAgeMax);
      if (overlapMax >= overlapMin) {
        // There is overlap
        const overlapSize    = overlapMax - overlapMin;
        const labelRangeSize = labelAgeMax - labelAgeMin || 1;
        score   += 50 + (overlapSize / labelRangeSize) * 50; // up to +100
        isExact  = (overlapSize / labelRangeSize) >= 1.0;
      }
      // Distance penalty — penalise rows whose midpoint is far away
      score -= Math.abs(factAgeMid - labelAgeMid) * 2;
      if (score > bestScore) {
        bestScore = score;
        bestKey   = key;
        bestExact = isExact;
      }
    }
    return bestKey ? { key: bestKey, isExact: bestExact } : null;
  }
  // ---------------------------------------------------------------------------
  // SMART HEIGHT RESOLVER  ← NEW
  //
  // Same idea as age resolver but reads height from labels like
  // "Child 110-120 cm" or factory rows with a Height column.
  // Used as a tertiary fallback after age resolution fails.
  // ---------------------------------------------------------------------------
  function resolveByHeightRange(label, factorySizes) {
    const hMatch = String(label).match(/(\d{2,3})\s*[-–]\s*(\d{2,3})\s*cm/i)
                || String(label).match(/(\d{2,3})\s*cm/i);
    if (!hMatch) return null;
    let labelHMin, labelHMax;
    if (hMatch[2] !== undefined) {
      labelHMin = parseFloat(hMatch[1]);
      labelHMax = parseFloat(hMatch[2]);
    } else {
      labelHMin = parseFloat(hMatch[1]);
      labelHMax = labelHMin;
    }
    const labelHMid = (labelHMin + labelHMax) / 2;
    let bestKey   = null;
    let bestScore = -Infinity;
    let bestExact = false;
    for (const [key, data] of Object.entries(factorySizes)) {
      if (key === "_meta") continue;
      const meta = data._meta;
      if (meta.heightMin === null) continue;
      const factHMin = meta.heightMin;
      const factHMax = meta.heightMax !== null ? meta.heightMax : meta.heightMin;
      const factHMid = (factHMin + factHMax) / 2;
      let score   = 0;
      let isExact = false;
      const overlapMin = Math.max(labelHMin, factHMin);
      const overlapMax = Math.min(labelHMax, factHMax);
      if (overlapMax >= overlapMin) {
        const overlapSize    = overlapMax - overlapMin;
        const labelRangeSize = labelHMax - labelHMin || 1;
        score   += 50 + (overlapSize / labelRangeSize) * 50;
        isExact  = (overlapSize / labelRangeSize) >= 1.0;
      }
      score -= Math.abs(factHMid - labelHMid) * 0.5;
      if (score > bestScore) {
        bestScore = score;
        bestKey   = key;
        bestExact = isExact;
      }
    }
    return bestKey ? { key: bestKey, isExact: bestExact } : null;
  }
  // ---------------------------------------------------------------------------
  // AGE-LABEL RESOLVER (size-key fallback)
  //
  // Handles products where age is encoded in size-key labels themselves
  // (e.g. "Baby 9 Months", "Child 1-2 years") and no dedicated Age column exists.
  // ---------------------------------------------------------------------------
  function extractAgeRangeInMonths(text) {
    const label = String(text || "").toLowerCase();
    if (!label) return null;

    const monthRange = label.match(/(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:month|months|mo|mos|mth|mths)\b/i);
    if (monthRange) {
      return { min: parseFloat(monthRange[1]), max: parseFloat(monthRange[2]) };
    }

    const yearRange = label.match(/(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:year|years|yr|yrs|y)\b/i);
    if (yearRange) {
      return { min: parseFloat(yearRange[1]) * 12, max: parseFloat(yearRange[2]) * 12 };
    }

    const monthSingle = label.match(/(\d+(?:\.\d+)?)\s*(?:month|months|mo|mos|mth|mths)\b/i);
    if (monthSingle) {
      const value = parseFloat(monthSingle[1]);
      return { min: value, max: value };
    }

    const yearSingle = label.match(/(\d+(?:\.\d+)?)\s*(?:year|years|yr|yrs|y)\b/i);
    if (yearSingle) {
      const value = parseFloat(yearSingle[1]) * 12;
      return { min: value, max: value };
    }

    return null;
  }
  function resolveByAgeLabelInSizeKey(label, factorySizes) {
    const targetRange = extractAgeRangeInMonths(label);
    if (!targetRange) return null;

    const targetMin = targetRange.min;
    const targetMax = targetRange.max;
    const targetMid = (targetMin + targetMax) / 2;

    let bestKey   = null;
    let bestScore = -Infinity;
    let bestExact = false;

    for (const key of Object.keys(factorySizes)) {
      if (key === "_meta") continue;
      const candidateRange = extractAgeRangeInMonths(key);
      if (!candidateRange) continue;

      const candMin = candidateRange.min;
      const candMax = candidateRange.max;
      const candMid = (candMin + candMax) / 2;

      let score = 0;
      let isExact = false;

      const overlapMin = Math.max(targetMin, candMin);
      const overlapMax = Math.min(targetMax, candMax);
      if (overlapMax >= overlapMin) {
        const overlapSize = overlapMax - overlapMin;
        const targetSize = targetMax - targetMin || 1;
        score += 50 + (overlapSize / targetSize) * 50;
        isExact = (overlapSize / targetSize) >= 1.0;
      }

      score -= Math.abs(candMid - targetMid) * 0.5;

      if (score > bestScore) {
        bestScore = score;
        bestKey = key;
        bestExact = isExact;
      }
    }

    return bestKey ? { key: bestKey, isExact: bestExact } : null;
  }
  // ---------------------------------------------------------------------------
  // MASTER RESOLVER
  // Tries every strategy in order, returns { key, isExact, note } | null
  // ---------------------------------------------------------------------------
  function resolveFactoryKey(selectedLabel, factorySizes) {
    const label = String(selectedLabel || "").trim();
    if (!label) return null;
    // 1. Direct match (factory key used verbatim as dropdown label)
    if (factorySizes[label]) {
      return { key: label, isExact: true, note: null };
    }
    // 2. Per-product explicit aliases (window.DLM_SIZE_ALIASES)
    const aliases = (window.DLM_SIZE_ALIASES && typeof window.DLM_SIZE_ALIASES === "object")
      ? window.DLM_SIZE_ALIASES : null;
    if (aliases && aliases[label]) {
      const mapped = String(aliases[label]).trim();
      if (factorySizes[mapped]) {
        return { key: mapped, isExact: true, note: null };
      }
    }
    // 3. Adult token stripping ("Mother XL" → "XL", "Father XXL" → "2XL")
    const adultToken = extractAdultToken(label);
    if (adultToken) {
      const candidates = [
        adultToken,
        adultToken === "2XL" ? "XXL"   : null,
        adultToken === "3XL" ? "XXXL"  : null,
        adultToken === "4XL" ? "XXXXL" : null,
      ].filter(Boolean);
      for (const c of candidates) {
        if (factorySizes[c]) return { key: c, isExact: true, note: null };
      }
    }
    // 4. Smart age-range resolution (e.g. "Child 2-3 years" → nearest age row)
    const ageResult = resolveByAgeRange(label, factorySizes);
    if (ageResult) {
      const note = ageResult.isExact
        ? null
        : "Closest available size shown — exact measurements for this age are not available from the manufacturer.";
      return { key: ageResult.key, isExact: ageResult.isExact, note };
    }
    // 5. Smart height-range resolution (e.g. "Child 110-120cm")
    const heightResult = resolveByHeightRange(label, factorySizes);
    if (heightResult) {
      const note = heightResult.isExact
        ? null
        : "Closest available size shown — exact measurements for this height are not available from the manufacturer.";
      return { key: heightResult.key, isExact: heightResult.isExact, note };
    }
    // 6. Fallback by age embedded in size-key labels (e.g. "Baby 9 Months")
    const ageLabelResult = resolveByAgeLabelInSizeKey(label, factorySizes);
    if (ageLabelResult) {
      const note = ageLabelResult.isExact
        ? null
        : "Closest available size shown — exact measurements for this age are not available from the manufacturer.";
      return { key: ageLabelResult.key, isExact: ageLabelResult.isExact, note };
    }
    // 7. Soft normalize fallback (case/whitespace insensitive)
    const wanted = normalizeKey(label);
    for (const k of Object.keys(factorySizes)) {
      if (normalizeKey(k) === wanted) return { key: k, isExact: true, note: null };
    }
    return null;
  }
  // ---------------------------------------------------------------------------
  // SIZE CHART UPDATER
  // ---------------------------------------------------------------------------
  const updateSizeMessage = function () {
    const selectedSize = sizeSelect ? String(sizeSelect.value || "").trim() : "";
    console.log(`Selected Size: ${selectedSize}`);
    if (!selectedSize) {
      sizeChartWrapper.style.display = "none";
      sizeChartContent.innerHTML     = "";
      return;
    }
    const factorySizes = getFactorySizes();
    const resolved     = resolveFactoryKey(selectedSize, factorySizes);
    if (!resolved) {
      sizeChartContent.innerHTML =
        '<div class="sc-empty"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg><span>Size information not available for this selection.</span></div>';
      sizeChartWrapper.style.display = "block";
      return;
    }
    const factorySize = factorySizes[resolved.key];

    // --- Build premium card HTML ---
    let htmlContent = '';

    // Header with ruler icon, selected size name, and unit toggle
    htmlContent += '<div class="sc-header">';
    htmlContent += '<div class="sc-header__main">';
    htmlContent += '<svg class="sc-header__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0z"/><line x1="14.5" y1="12.5" x2="11.5" y2="9.5"/><line x1="11.5" y1="15.5" x2="8.5" y2="12.5"/><line x1="8.5" y1="18.5" x2="5.5" y2="15.5"/><line x1="17.5" y1="9.5" x2="14.5" y2="6.5"/></svg>';
    htmlContent += '<span class="sc-header__title">Size Details - ' + escapeHtml(selectedSize) + '</span>';
    htmlContent += '</div>';
    htmlContent += '<div class="sc-unit-toggle" role="group" aria-label="Size chart units">';
    htmlContent += '<button type="button" class="sc-unit-toggle__btn' + (selectedUnitSystem === "metric" ? ' is-active' : '') + '" data-sc-unit-system="metric" aria-pressed="' + (selectedUnitSystem === "metric") + '">cm</button>';
    htmlContent += '<button type="button" class="sc-unit-toggle__btn' + (selectedUnitSystem === "imperial" ? ' is-active' : '') + '" data-sc-unit-system="imperial" aria-pressed="' + (selectedUnitSystem === "imperial") + '">in</button>';
    htmlContent += '</div>';
    htmlContent += '</div>';

    // Approximate match note
    if (resolved.note) {
      htmlContent += '<div class="sc-note">';
      htmlContent += '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
      htmlContent += '<span>' + resolved.note + '</span>';
      htmlContent += '</div>';
    }

    // Measurement rows
    htmlContent += '<div class="sc-table">';
    let rowIndex = 0;
    for (const measurementName in factorySize) {
      if (measurementName === "_meta") continue;
      const measurementData = factorySize[measurementName];
      const units           = measurementData.units;
      const value           = measurementData.value;
      if (!value || String(value).trim() === "" || String(value).trim() === "—") continue;

      const isEven = rowIndex % 2 === 0;
      const display = getMeasurementForUnitSystem(value, units, selectedUnitSystem);
      if (!display.value) continue;

      htmlContent += '<div class="sc-row' + (isEven ? ' sc-row--alt' : '') + '">';
      htmlContent += '<span class="sc-row__label">' + escapeHtml(measurementName) + '</span>';
      htmlContent += '<div class="sc-row__values">';
      htmlContent += '<span class="sc-pill">' + escapeHtml(display.value) + '</span>';
      htmlContent += '</div>';
      htmlContent += '</div>';
      rowIndex++;
    }

    if (rowIndex === 0) {
      htmlContent += '<div class="sc-empty"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg><span>Size information not available for this selection.</span></div>';
    }

    htmlContent += '</div>';

    sizeChartContent.innerHTML     = htmlContent;
    sizeChartWrapper.style.display = "block";

    const unitToggleButtons = sizeChartContent.querySelectorAll("[data-sc-unit-system]");
    unitToggleButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const nextSystem = button.getAttribute("data-sc-unit-system");
        if (nextSystem !== "metric" && nextSystem !== "imperial") return;
        if (nextSystem === selectedUnitSystem) return;
        selectedUnitSystem = nextSystem;
        storeUnitSystem(selectedUnitSystem);
        updateSizeMessage();
      });
    });
  };
  // ---------------------------------------------------------------------------
  // INIT
  // ---------------------------------------------------------------------------
  const insertSelectSizeOption = function () {
    const firstOption = sizeSelect.options[0];
    if (!firstOption || firstOption.value !== "") {
      const opt      = document.createElement("option");
      opt.value      = "";
      opt.textContent = "Select size";
      opt.disabled   = true;
      opt.selected   = true;
      sizeSelect.insertBefore(opt, sizeSelect.firstChild);
    }
  };
  const resetSizeSelect = function () {
    sizeSelect.value = "";
    updateSizeMessage();
  };
  insertSelectSizeOption();
  resetSizeSelect();
  sizeSelect.addEventListener("change", updateSizeMessage);
});
