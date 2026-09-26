/*
 * Delivery arrival dates for the PDP, cart drawer and /cart.
 *
 * Liquid renders the localized day window (e.g. "12-16 days") inside
 * [data-dlm-delivery-window]. This script swaps it for a concrete calendar
 * range such as "Thu, Oct 8 – Mon, Oct 12". The day window stays in place
 * when JS is off or the window cannot be parsed. Sundays roll to Monday.
 */
(function () {
  'use strict';

  var SELECTOR = '[data-dlm-delivery-window]:not([data-dlm-delivery-rendered])';

  function parseWindow(value) {
    var matches = String(value || '').match(/\d+/g);
    if (!matches) return null;
    var min = Number(matches[0]);
    var max = Number(matches[1] || matches[0]);
    if (!(min >= 1) || !(max >= min) || max > 90) return null;
    return { min: min, max: max };
  }

  function addDays(start, days) {
    var date = new Date(start.getFullYear(), start.getMonth(), start.getDate());
    date.setDate(date.getDate() + days);
    if (date.getDay() === 0) date.setDate(date.getDate() + 1);
    return date;
  }

  function computeWindow(value, today) {
    var days = parseWindow(value);
    if (!days) return null;
    var start = today || new Date();
    return { from: addDays(start, days.min), to: addDays(start, days.max) };
  }

  function formatWindow(range, locale) {
    var options = { weekday: 'short', month: 'short', day: 'numeric' };
    var formatter;
    try {
      formatter = new Intl.DateTimeFormat(locale || undefined, options);
    } catch (_error) {
      formatter = new Intl.DateTimeFormat('en-US', options);
    }
    if (range.from.getTime() === range.to.getTime()) return formatter.format(range.from);
    if (typeof formatter.formatRange === 'function') {
      try {
        return formatter.formatRange(range.from, range.to);
      } catch (_error) {}
    }
    return formatter.format(range.from) + ' – ' + formatter.format(range.to);
  }

  function currentLocale() {
    var shopify = window.Shopify && window.Shopify.locale;
    var lang = document.documentElement && document.documentElement.lang;
    return shopify || lang || undefined;
  }

  function render(root) {
    var elements = (root || document).querySelectorAll(SELECTOR);
    if (!elements.length) return;
    var today = new Date();
    var locale = currentLocale();
    Array.prototype.forEach.call(elements, function (element) {
      element.setAttribute('data-dlm-delivery-rendered', '');
      var range = computeWindow(element.getAttribute('data-dlm-delivery-window'), today);
      if (!range) return;
      element.textContent = formatWindow(range, locale);
    });
  }

  window.DLMDeliveryDates = { computeWindow: computeWindow, formatWindow: formatWindow, render: render };

  function start() {
    render(document);
    // The cart drawer and /cart footer are re-rendered from section HTML on
    // every cart change, so pick up fresh estimate nodes as they arrive.
    if (typeof MutationObserver === 'function' && document.body) {
      new MutationObserver(function () {
        if (document.querySelector(SELECTOR)) render(document);
      }).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
