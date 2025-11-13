(() => {
  const dataElement = document.getElementById('shipping-promise-data');
  if (!dataElement) return;

  let config;
  try {
    config = JSON.parse(dataElement.textContent || '{}');
  } catch (error) {
    console.warn('[shipping-promises] Invalid JSON payload', error);
    return;
  }

  const body = document.body;
  const countryCode = (body.dataset.customerCountry || 'US').toUpperCase();
  const countryName = body.dataset.customerCountryName || countryCode;

  const toNumber = (value, fallback) => {
    const parsed = parseInt(value, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const processingMin = toNumber(config?.processing?.min, 2);
  const processingMax = toNumber(config?.processing?.max, processingMin);
  const transitMinDefault = toNumber(config?.transit?.min, 7);
  const transitMaxDefault = toNumber(config?.transit?.max, transitMinDefault);

  const regionOverride =
    Array.isArray(config?.regions) &&
    config.regions.find((region) => region.iso === countryCode);

  const transitMin = toNumber(regionOverride?.min, transitMinDefault);
  const transitMax = toNumber(regionOverride?.max, transitMaxDefault);

  const totalMin = processingMin + transitMin;
  const totalMax = processingMax + transitMax;

  const addBusinessDays = (start, days) => {
    const result = new Date(start.getTime());
    let added = 0;
    while (added < days) {
      result.setDate(result.getDate() + 1);
      const day = result.getDay();
      if (day !== 0 && day !== 6) {
        added += 1;
      }
    }
    return result;
  };

  const formatDate = (date) =>
    date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });

  const today = new Date();
  const etaStart = addBusinessDays(today, totalMin);
  const etaEnd = addBusinessDays(today, totalMax);
  const etaString = `${formatDate(etaStart)}–${formatDate(etaEnd)}`;
  const detailCopy = `Delivers to ${countryCode} by ${etaString}`;

  document.querySelectorAll('[data-shipping-estimate-text]').forEach((node) => {
    node.textContent = detailCopy;
  });

  document.querySelectorAll('[data-shipping-summary]').forEach((node) => {
    node.textContent = `Free shipping • ${etaString}`;
  });

  const holidayLabel = config?.holidayCutoff?.label?.trim();
  const holidayDateRaw = config?.holidayCutoff?.date?.trim();
  let showHolidayNote = false;
  if (holidayLabel && holidayDateRaw) {
    const holidayDate = new Date(`${holidayDateRaw}T23:59:59`);
    showHolidayNote = !Number.isNaN(holidayDate.valueOf()) && today <= holidayDate;
    document.querySelectorAll('[data-shipping-holiday-note]').forEach((node) => {
      if (showHolidayNote) {
        node.textContent = holidayLabel;
        node.removeAttribute('hidden');
      } else {
        node.setAttribute('hidden', 'hidden');
      }
    });
  }
})();
