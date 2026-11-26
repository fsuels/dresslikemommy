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


  // Christmas order-by line: shown only while an order placed today could still
  // arrive by 23 December under the same day window (an estimate, not a promise).
  function renderChristmasOrderBy(root) {
    var nodes = (root || document).querySelectorAll('[data-dlm-christmas-order-by]:not([data-dlm-cob-done])');
    if (!nodes.length) return;
    var now = new Date();
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var arrive = new Date(now.getFullYear(), 11, 23);
    var locale = currentLocale();
    var fmt;
    try { fmt = new Intl.DateTimeFormat(locale || undefined, { weekday: 'short', month: 'short', day: 'numeric' }); }
    catch (_error) { fmt = new Intl.DateTimeFormat('en-US', { weekday: 'short', month: 'short', day: 'numeric' }); }
    Array.prototype.forEach.call(nodes, function (node) {
      node.setAttribute('data-dlm-cob-done', '');
      var max = Number(node.getAttribute('data-max-days'));
      var text = node.getAttribute('data-text') || '';
      if (!(max >= 1) || max > 60 || text.indexOf('{order}') < 0) return revealCobSlot(node, false);
      var last = new Date(arrive.getFullYear(), arrive.getMonth(), arrive.getDate() - max);
      while (last >= today && addDays(last, max).getTime() > arrive.getTime()) last.setDate(last.getDate() - 1);
      if (last < today || today > arrive) return revealCobSlot(node, false);
      node.textContent = text.replace('{order}', fmt.format(last)).replace('{arrive}', fmt.format(arrive));
      node.hidden = false;
      revealCobSlot(node, true);
    });
  }

  // The PDP value strip reserves a slot for the line (snippets/dlm-pdp-value-strip.liquid)
  // so it does not shift the buy box: show it when the line is filled, collapse it when not.
  function revealCobSlot(node, filled) {
    var slot = typeof node.closest === 'function' ? node.closest('[data-dlm-cob-slot]') : null;
    if (!slot) return;
    if (filled) slot.setAttribute('data-dlm-cob-ready', '');
    else slot.hidden = true;
  }

  window.DLMDeliveryDates = { computeWindow: computeWindow, formatWindow: formatWindow, render: render };

  function start() {
    render(document);
    renderChristmasOrderBy(document);
    // The cart drawer and /cart footer are re-rendered from section HTML on
    // every cart change, so pick up fresh estimate nodes as they arrive.
    if (typeof MutationObserver === 'function' && document.body) {
      // Page scripts add many nodes in bursts; one pass per burst is enough.
      var scheduled = false;
      new MutationObserver(function () {
        if (scheduled) return;
        scheduled = true;
        setTimeout(function () {
          scheduled = false;
          if (document.querySelector(SELECTOR)) render(document);
          renderChristmasOrderBy(document);
        }, 80);
      }).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
