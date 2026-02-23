document.addEventListener("DOMContentLoaded", function () {
  console.log("Size Conversion Script Loaded (DLM Smart Resolver v2).");
  // ---------------------------------------------------------------------------
  // UNIT CONVERSION HELPERS
  // ---------------------------------------------------------------------------
  const cmToInches = (cm) => (cm / 2.54).toFixed(2);
  const kgToLbs    = (kg) => (kg * 2.20462).toFixed(2);
  // ---------------------------------------------------------------------------
  // DOM REFERENCES
  // ---------------------------------------------------------------------------
  const sizeSelect        = document.querySelector("select.size-select");
  const sizeChartWrapper  = document.querySelector(".size-chart-wrapper");
  const sizeChartContent  = document.getElementById("size-chart-content");
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
      const regex      = /^(.+?)\\s*\\((.*?)\\)$/;
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
    const sizeChartTable = document.getElementById("size-chart");
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
          const ageNums = cellContent.match(/[\\d.]+/g);
          if (ageNums && ageNums.length >= 1) {
            factorySizes[sizeName]._meta.ageMin = parseFloat(ageNums[0]);
            factorySizes[sizeName]._meta.ageMax = parseFloat(ageNums[ageNums.length - 1]);
          }
        }
        // ── Harvest Height metadata for smart resolution ──
        if (measurementName.toLowerCase() === "height" && cellContent && cellContent !== "—") {
          const hNums = cellContent.match(/[\\d.]+/g);
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
  // FORMAT MEASUREMENT WITH UNITS
  // Handles single value, dual value (already split), and auto-conversion.
  // ---------------------------------------------------------------------------
  function formatMeasurementWithUnits(value, units) {
    const parts = String(value).split("/").map((p) => p.trim());
    // Already pre-split "88 / 34.6"
    if (parts.length === 2 && units.length === 2) {
      const alreadyHas0 = parts[0].toLowerCase().endsWith(units[0].toLowerCase());
      const alreadyHas1 = parts[1].toLowerCase().endsWith(units[1].toLowerCase());
      const p0 = alreadyHas0 ? parts[0] : `${parts[0]} ${units[0]}`;
      const p1 = alreadyHas1 ? parts[1] : `${parts[1]} ${units[1]}`;
      return `${p0} / ${p1}`;
    }
    // Single value, single unit — display raw
    if (parts.length === 1 && units.length <= 1) {
      return parts[0];
    }
    // Single stored value + dual units → auto-convert
    if (parts.length === 1 && units.length === 2) {
      const num = parseFloat(parts[0]);
      if (!isNaN(num)) {
        let converted;
        if      (units[1].toLowerCase() === "in")  converted = cmToInches(num);
        else if (units[1].toLowerCase() === "lbs") converted = kgToLbs(num);
        else                                        converted = parts[0];
        return `${parts[0]} ${units[0]} / ${converted} ${units[1]}`;
      }
      return `${parts[0]} ${units[0]}`;
    }
    return String(value);
  }
  // ---------------------------------------------------------------------------
  // NORMALIZE HELPER
  // ---------------------------------------------------------------------------
  function normalizeKey(s) {
    return String(s || "").trim().replace(/\\s+/g, " ").toLowerCase();
  }
  // ---------------------------------------------------------------------------
  // ADULT TOKEN EXTRACTOR
  // "Mother 2XL" → "2XL", "Father XXL" → "2XL", "Adult XL" → "XL"
  // ---------------------------------------------------------------------------
  function extractAdultToken(label) {
    const m = String(label || "").toUpperCase()
      .match(/\\b(XXXXL|XXXL|XXL|2XL|3XL|4XL|XL|XS|S|M|L)\\b/);
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
    const ageMatch = String(label).match(/(\\d+)\\s*[-–]\\s*(\\d+)\\s*(?:yr|year|years|y\\.o\\.?)?/i)
                  || String(label).match(/(\\d+)\\s*(?:yr|year|years|y\\.o\\.?)/i);
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
    const hMatch = String(label).match(/(\\d{2,3})\\s*[-–]\\s*(\\d{2,3})\\s*cm/i)
                || String(label).match(/(\\d{2,3})\\s*cm/i);
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
    // 6. Soft normalize fallback (case/whitespace insensitive)
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

    // Header with ruler icon and selected size name
    htmlContent += '<div class="sc-header">';
    htmlContent += '<svg class="sc-header__icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0z"/><line x1="14.5" y1="12.5" x2="11.5" y2="9.5"/><line x1="11.5" y1="15.5" x2="8.5" y2="12.5"/><line x1="8.5" y1="18.5" x2="5.5" y2="15.5"/><line x1="17.5" y1="9.5" x2="14.5" y2="6.5"/></svg>';
    htmlContent += '<span class="sc-header__title">Size Details — ' + selectedSize + '</span>';
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

      const parts = String(value).split("/").map(p => p.trim());
      const isEven = rowIndex % 2 === 0;

      htmlContent += '<div class="sc-row' + (isEven ? ' sc-row--alt' : '') + '">';
      htmlContent += '<span class="sc-row__label">' + measurementName + '</span>';
      htmlContent += '<div class="sc-row__values">';

      if (parts.length === 2 && units.length === 2) {
        // Two pre-split values
        const p0 = parts[0].toLowerCase().endsWith(units[0].toLowerCase()) ? parts[0] : parts[0] + ' ' + units[0];
        const p1 = parts[1].toLowerCase().endsWith(units[1].toLowerCase()) ? parts[1] : parts[1] + ' ' + units[1];
        htmlContent += '<span class="sc-pill">' + p0 + '</span>';
        htmlContent += '<span class="sc-pill">' + p1 + '</span>';
      } else if (parts.length === 1 && units.length === 2) {
        // Single value, auto-convert
        const num = parseFloat(parts[0]);
        if (!isNaN(num)) {
          let converted;
          if (units[1].toLowerCase() === "in") converted = cmToInches(num);
          else if (units[1].toLowerCase() === "lbs") converted = kgToLbs(num);
          else converted = parts[0];
          htmlContent += '<span class="sc-pill">' + parts[0] + ' ' + units[0] + '</span>';
          htmlContent += '<span class="sc-pill">' + converted + ' ' + units[1] + '</span>';
        } else {
          htmlContent += '<span class="sc-pill">' + parts[0] + (units[0] ? ' ' + units[0] : '') + '</span>';
        }
      } else {
        // Plain value
        htmlContent += '<span class="sc-pill">' + String(value) + (units[0] ? ' ' + units[0] : '') + '</span>';
      }

      htmlContent += '</div>';
      htmlContent += '</div>';
      rowIndex++;
    }
    htmlContent += '</div>';

    sizeChartContent.innerHTML     = htmlContent;
    sizeChartWrapper.style.display = "block";
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