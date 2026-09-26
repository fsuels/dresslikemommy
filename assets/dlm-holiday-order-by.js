/*
 * Holiday order-by line for the PDP purchase-confidence card.
 *
 * On a Halloween or Christmas product (detected from the product's own tags
 * via one same-origin /products/<handle>.js request) this adds one line under
 * the delivery estimate, e.g. "Order by Thu, Oct 15 for estimated Halloween
 * arrival". The cutoff comes from the upper bound of the same localized window
 * that assets/dlm-delivery-dates.js reads ([data-dlm-delivery-window], e.g.
 * "12-16 days"), with the same Sunday-to-Monday roll, so cutoff + max days
 * never lands after the holiday. The line is hidden after the cutoff, before
 * the lead window opens, when the window cannot be parsed, and when JS fails.
 * Delivery timing is an estimate only; the copy never guarantees arrival.
 */
(function () {
  'use strict';

  var TARGET = '[data-pdp-purchase-confidence] [data-dlm-delivery-window]';
  var MARK = 'data-dlm-holiday-checked';
  var LINE_ATTR = 'data-dlm-holiday-order-by';
  // Only show the line in the weeks before the cutoff, not all year.
  var LEAD_DAYS = 60;
  var DAY_MS = 86400000;

  // month is 0-based. Christmas targets Dec 24 because many storefront
  // markets celebrate on Christmas Eve.
  var HOLIDAYS = {
    halloween: { month: 9, day: 31, tag: /^(family )?halloween\b/ },
    christmas: { month: 11, day: 24, tag: /^(family )?christmas\b/ }
  };
  var ORDER = ['halloween', 'christmas'];

  // {date} is replaced with the locale-formatted cutoff date.
  var COPY = {
    en: {
      halloween: 'Order by {date} for estimated Halloween arrival',
      christmas: 'Order by {date} for estimated Christmas arrival'
    },
    es: {
      halloween: 'Pide a más tardar el {date} para una llegada estimada antes de Halloween',
      christmas: 'Pide a más tardar el {date} para una llegada estimada antes de Navidad'
    },
    fr: {
      halloween: 'Commandez d’ici le {date} pour une livraison estimée avant Halloween',
      christmas: 'Commandez d’ici le {date} pour une livraison estimée avant Noël'
    },
    de: {
      halloween: 'Bis {date} bestellen für die voraussichtliche Lieferung vor Halloween',
      christmas: 'Bis {date} bestellen für die voraussichtliche Lieferung vor Weihnachten'
    },
    it: {
      halloween: 'Ordina entro {date} per l’arrivo stimato prima di Halloween',
      christmas: 'Ordina entro {date} per l’arrivo stimato prima di Natale'
    },
    nl: {
      halloween: 'Bestel uiterlijk {date} voor geschatte levering vóór Halloween',
      christmas: 'Bestel uiterlijk {date} voor geschatte levering vóór Kerstmis'
    },
    pt: {
      halloween: 'Peça até {date} para a entrega estimada antes do Halloween',
      christmas: 'Peça até {date} para a entrega estimada antes do Natal'
    },
    da: {
      halloween: 'Bestil senest {date} for anslået levering før halloween',
      christmas: 'Bestil senest {date} for anslået levering før jul'
    },
    sv: {
      halloween: 'Beställ senast {date} för beräknad leverans före halloween',
      christmas: 'Beställ senast {date} för beräknad leverans före jul'
    },
    no: {
      halloween: 'Bestill innen {date} for estimert levering før halloween',
      christmas: 'Bestill innen {date} for estimert levering før jul'
    },
    pl: {
      halloween: 'Zamów do {date}, aby otrzymać szacowaną dostawę przed Halloween',
      christmas: 'Zamów do {date}, aby otrzymać szacowaną dostawę przed Bożym Narodzeniem'
    },
    cs: {
      halloween: 'Objednejte do {date} pro odhadované doručení před Halloweenem',
      christmas: 'Objednejte do {date} pro odhadované doručení před Vánoci'
    },
    fi: {
      halloween: 'Tilaa viimeistään {date}, niin arvioitu toimitus on ennen halloweenia',
      christmas: 'Tilaa viimeistään {date}, niin arvioitu toimitus on ennen joulua'
    },
    ro: {
      halloween: 'Comandă până {date} pentru livrarea estimată înainte de Halloween',
      christmas: 'Comandă până {date} pentru livrarea estimată înainte de Crăciun'
    },
    el: {
      halloween: 'Παραγγείλτε έως {date} για εκτιμώμενη παράδοση πριν από το Halloween',
      christmas: 'Παραγγείλτε έως {date} για εκτιμώμενη παράδοση πριν από τα Χριστούγεννα'
    },
    hu: {
      halloween: 'Rendeljen legkésőbb {date} a becsült Halloween előtti kézbesítéshez',
      christmas: 'Rendeljen legkésőbb {date} a becsült karácsony előtti kézbesítéshez'
    },
    tr: {
      halloween: 'Cadılar Bayramı’ndan önce tahmini teslimat için en geç {date} sipariş verin',
      christmas: 'Noel’den önce tahmini teslimat için en geç {date} sipariş verin'
    },
    ru: {
      halloween: 'Закажите не позднее {date} — ориентировочная доставка до Хэллоуина',
      christmas: 'Закажите не позднее {date} — ориентировочная доставка до Рождества'
    },
    ar: {
      halloween: 'اطلب بحلول {date} للتوصيل المتوقع قبل الهالوين',
      christmas: 'اطلب بحلول {date} للتوصيل المتوقع قبل عيد الميلاد'
    },
    he: {
      halloween: 'הזמינו עד {date} להגעה משוערת לפני האלווין',
      christmas: 'הזמינו עד {date} להגעה משוערת לפני חג המולד'
    },
    hi: {
      halloween: 'हैलोवीन से पहले अनुमानित डिलीवरी के लिए {date} तक ऑर्डर करें',
      christmas: 'क्रिसमस से पहले अनुमानित डिलीवरी के लिए {date} तक ऑर्डर करें'
    },
    ja: {
      halloween: '{date}までのご注文で、ハロウィンまでのお届け目安',
      christmas: '{date}までのご注文で、クリスマスまでのお届け目安'
    },
    ko: {
      halloween: '{date}까지 주문 시 할로윈 전 도착 예상',
      christmas: '{date}까지 주문 시 크리스마스 전 도착 예상'
    },
    zh: {
      halloween: '{date}前下单，预计万圣节前送达',
      christmas: '{date}前下单，预计圣诞节前送达'
    },
    'zh-hant': {
      halloween: '{date}前下單，預計萬聖節前送達',
      christmas: '{date}前下單，預計聖誕節前送達'
    }
  };

  function parseWindow(value) {
    var matches = String(value || '').match(/\d+/g);
    if (!matches) return null;
    var min = Number(matches[0]);
    var max = Number(matches[1] || matches[0]);
    if (!(min >= 1) || !(max >= min) || max > 90) return null;
    return { min: min, max: max };
  }

  function dateOnly(date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate());
  }

  // Same arithmetic as dlm-delivery-dates.js: calendar days, Sunday -> Monday.
  function addDays(start, days) {
    var date = dateOnly(start);
    date.setDate(date.getDate() + days);
    if (date.getDay() === 0) date.setDate(date.getDate() + 1);
    return date;
  }

  function daysBetween(from, to) {
    return Math.round((dateOnly(to).getTime() - dateOnly(from).getTime()) / DAY_MS);
  }

  // Latest order day whose estimated latest arrival is on or before holiday.
  function computeCutoff(holiday, maxDays) {
    var cutoff = dateOnly(holiday);
    cutoff.setDate(cutoff.getDate() - maxDays);
    while (addDays(cutoff, maxDays).getTime() > dateOnly(holiday).getTime()) {
      cutoff.setDate(cutoff.getDate() - 1);
    }
    return cutoff;
  }

  function holidayDate(key, year) {
    var spec = HOLIDAYS[key];
    return spec ? new Date(year, spec.month, spec.day) : null;
  }

  // Returns { holiday, cutoff, date } when the line should show today, else null.
  function orderByFor(key, windowValue, today) {
    var days = parseWindow(windowValue);
    if (!days || !HOLIDAYS[key]) return null;
    var now = dateOnly(today || new Date());
    var years = [now.getFullYear(), now.getFullYear() + 1];
    for (var i = 0; i < years.length; i += 1) {
      var target = holidayDate(key, years[i]);
      var cutoff = computeCutoff(target, days.max);
      var remaining = daysBetween(now, cutoff);
      if (remaining < 0) continue;
      if (remaining > LEAD_DAYS) return null;
      return { holiday: key, cutoff: cutoff, date: target };
    }
    return null;
  }

  function detectHolidays(tags) {
    var list = tags;
    if (typeof list === 'string') list = list.split(',');
    if (!list || typeof list.length !== 'number') return [];
    var found = [];
    for (var h = 0; h < ORDER.length; h += 1) {
      var pattern = HOLIDAYS[ORDER[h]].tag;
      for (var t = 0; t < list.length; t += 1) {
        if (pattern.test(String(list[t] || '').trim().toLowerCase())) {
          found.push(ORDER[h]);
          break;
        }
      }
    }
    return found;
  }

  // Earliest still-open cutoff among the product's holidays.
  function pickOrderBy(tags, windowValue, today) {
    var holidays = detectHolidays(tags);
    var best = null;
    for (var i = 0; i < holidays.length; i += 1) {
      var candidate = orderByFor(holidays[i], windowValue, today);
      if (candidate && (!best || candidate.cutoff.getTime() < best.cutoff.getTime())) best = candidate;
    }
    return best;
  }

  function languageKey(locale) {
    var value = String(locale || '').toLowerCase().replace('_', '-');
    if (/^zh-(tw|hk|mo|hant)/.test(value)) return 'zh-hant';
    var base = value.split('-')[0];
    if (base === 'nb' || base === 'nn') return 'no';
    return COPY[base] ? base : 'en';
  }

  function formatDate(date, locale) {
    var options = { weekday: 'short', month: 'short', day: 'numeric' };
    var formatter;
    try {
      formatter = new Intl.DateTimeFormat(locale || undefined, options);
    } catch (_error) {
      formatter = new Intl.DateTimeFormat('en-US', options);
    }
    return formatter.format(date);
  }

  // Split the sentence around the date so the date can be emphasised.
  function messageParts(holiday, locale) {
    var copy = COPY[languageKey(locale)] || COPY.en;
    var template = copy[holiday] || COPY.en[holiday];
    if (!template) return null;
    var index = template.indexOf('{date}');
    return { before: template.slice(0, index), after: template.slice(index + 6) };
  }

  function message(holiday, cutoff, locale) {
    var parts = messageParts(holiday, locale);
    return parts ? parts.before + formatDate(cutoff, locale) + parts.after : '';
  }

  function currentLocale() {
    var shopify = window.Shopify && window.Shopify.locale;
    var lang = document.documentElement && document.documentElement.lang;
    return shopify || lang || undefined;
  }

  function productHandle() {
    var match = String((window.location && window.location.pathname) || '').match(/\/products\/([^\/?#]+)/);
    return match ? match[1] : '';
  }

  function productUrl(handle) {
    var root = (window.Shopify && window.Shopify.routes && window.Shopify.routes.root) || '/';
    if (root.charAt(root.length - 1) !== '/') root += '/';
    return root + 'products/' + handle + '.js';
  }

  function buildLine(result, locale) {
    var parts = messageParts(result.holiday, locale);
    if (!parts) return null;
    var line = document.createElement('p');
    line.className = 'dlm-pc-row__summary dlm-holiday-order-by';
    line.setAttribute(LINE_ATTR, result.holiday);
    line.style.margin = '4px 0 0';
    line.appendChild(document.createTextNode(parts.before));
    var strong = document.createElement('strong');
    strong.textContent = formatDate(result.cutoff, locale);
    line.appendChild(strong);
    line.appendChild(document.createTextNode(parts.after));
    return line;
  }

  // Inserts the line after the paragraph holding each unprocessed estimate.
  function render(tags, root, today) {
    var elements = (root || document).querySelectorAll(TARGET);
    var locale = currentLocale();
    var inserted = 0;
    Array.prototype.forEach.call(elements, function (element) {
      var host = element.parentNode;
      if (!host || !host.parentNode || host.hasAttribute(MARK)) return;
      host.setAttribute(MARK, '');
      var result = pickOrderBy(tags, element.getAttribute('data-dlm-delivery-window'), today || new Date());
      if (!result) return;
      var line = buildLine(result, locale);
      if (!line) return;
      host.parentNode.insertBefore(line, host.nextSibling);
      inserted += 1;
    });
    return inserted;
  }

  // True when any holiday could show today for this window (skips the fetch).
  function anyOpen(windowValue, today) {
    for (var i = 0; i < ORDER.length; i += 1) {
      if (orderByFor(ORDER[i], windowValue, today)) return true;
    }
    return false;
  }

  window.DLMHolidayOrderBy = {
    parseWindow: parseWindow,
    computeCutoff: computeCutoff,
    orderByFor: orderByFor,
    detectHolidays: detectHolidays,
    pickOrderBy: pickOrderBy,
    languageKey: languageKey,
    formatDate: formatDate,
    message: message,
    render: render,
    copy: COPY
  };

  function start() {
    var first = document.querySelector(TARGET);
    var handle = productHandle();
    if (!first || !handle || typeof window.fetch !== 'function') return;
    if (!anyOpen(first.getAttribute('data-dlm-delivery-window'), new Date())) return;
    window
      .fetch(productUrl(handle), { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (response) {
        return response.ok ? response.json() : null;
      })
      .then(function (product) {
        if (!product || !detectHolidays(product.tags).length) return;
        render(product.tags, document);
        // Re-apply if the purchase-confidence card is re-rendered.
        if (typeof MutationObserver === 'function' && document.body) {
          new MutationObserver(function () {
            var pending = document.querySelector(TARGET);
            if (pending && pending.parentNode && !pending.parentNode.hasAttribute(MARK)) render(product.tags, document);
          }).observe(document.body, { childList: true, subtree: true });
        }
      })
      ['catch'](function () {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
