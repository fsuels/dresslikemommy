/*
 * Visible size-guide text link for the PDP matching-set builder.
 *
 * Each builder card (rendered by product-desktop-ux-20260513-ruler-sync.js)
 * has only an icon-only ruler button (.product-matching-set__fit-icon). This
 * adds a small text link ("Size guide & fit", the localized
 * data-size-guide-single-label) to the card header, next to the role name and
 * right above the size pills. Clicking it clicks that card's ruler button, so
 * the existing inline fit panel and size chart open exactly as before.
 * Cards are re-rendered with innerHTML, so a MutationObserver re-adds links.
 */
(function () {
  'use strict';

  var CARD = '[data-instance-card]';
  var HEADER = '.product-matching-set__card-header';
  var ICON = '[data-pdp-fit-inline-trigger]';
  var LINK_ATTR = 'data-dlm-size-chart-link';
  var FALLBACK_LABEL = 'Size guide & fit';
  var ICON_LABEL_ATTR = 'data-dlm-icon-labelled';
  var HELPER_ATTR = 'data-dlm-size-helper';

  function labelFor(card) {
    var wrapper = card.closest('[data-size-guide-single-label]') || document.querySelector('[data-size-guide-single-label]');
    var label = wrapper ? String(wrapper.getAttribute('data-size-guide-single-label') || '').trim() : '';
    // The source attribute is HTML-escaped twice ("&amp;amp;"), so decode leftover entities
    // before the label goes into textContent.
    if (label.indexOf('&') !== -1 && typeof DOMParser === 'function') {
      label = new DOMParser().parseFromString(label, 'text/html').documentElement.textContent.trim();
    }
    if (!label || /translation missing/i.test(label)) label = FALLBACK_LABEL;
    return label;
  }

  function decode(label) {
    label = String(label || '').trim();
    if (label.indexOf('&') !== -1 && typeof DOMParser === 'function') {
      label = new DOMParser().parseFromString(label, 'text/html').documentElement.textContent.trim();
    }
    return /translation missing/i.test(label) ? '' : label;
  }

  function wrapperAttr(card, name) {
    var wrapper = card.closest('[' + name + ']') || document.querySelector('[' + name + ']');
    return wrapper ? decode(wrapper.getAttribute(name)) : '';
  }

  // The ruler button gets a visible, translated "Size chart" label and a matching accessible name.
  function labelIcon(card) {
    var icon = card.querySelector(ICON);
    if (!icon || icon.hasAttribute(ICON_LABEL_ATTR)) return;
    var label = wrapperAttr(card, 'data-size-chart-icon-label');
    if (!label) return;
    icon.setAttribute(ICON_LABEL_ATTR, '');
    icon.classList.add('product-matching-set__fit-icon--labelled');
    var span = document.createElement('span');
    span.className = 'dlm-fit-icon-label';
    span.textContent = label;
    icon.appendChild(span);
    var name = icon.getAttribute('aria-label');
    icon.setAttribute('aria-label', name && name.indexOf(label) === -1 ? label + ': ' + name : label);
  }

  // One helper line under the first size row: the existing "open the full chart" sentence.
  function addHelper(card) {
    var row = card.querySelector('.product-matching-set__size-row');
    if (!row || (row.nextElementSibling && row.nextElementSibling.hasAttribute(HELPER_ATTR))) return;
    if (document.querySelector('[' + HELPER_ATTR + ']')) return;
    var text = wrapperAttr(card, 'data-size-guide-compare-hint');
    if (!text) return;
    var line = document.createElement('p');
    line.className = 'dlm-size-helper';
    line.setAttribute(HELPER_ATTR, '');
    line.textContent = text;
    row.parentNode.insertBefore(line, row.nextSibling);
  }

  function addLink(card) {
    labelIcon(card);
    var header = card.querySelector(HEADER);
    var icon = card.querySelector(ICON);
    if (!header || !icon || header.querySelector('[' + LINK_ATTR + ']')) return;
    var link = document.createElement('button');
    link.type = 'button';
    link.className = 'dlm-size-chart-link';
    link.setAttribute(LINK_ATTR, '');
    var controls = icon.getAttribute('aria-controls');
    if (controls) link.setAttribute('aria-controls', controls);
    link.textContent = labelFor(card);
    header.appendChild(link);
  }

  function scan(root) {
    var cards = (root || document).querySelectorAll(CARD);
    Array.prototype.forEach.call(cards, addLink);
    if (cards.length) addHelper(cards[0]);
  }

  document.addEventListener('click', function (event) {
    var link = event.target && event.target.closest ? event.target.closest('[' + LINK_ATTR + ']') : null;
    if (!link) return;
    var card = link.closest(CARD);
    var icon = card ? card.querySelector(ICON) : null;
    if (!icon) return;
    event.preventDefault();
    icon.click();
  });

  function start() {
    var builders = document.querySelectorAll('.product-matching-set');
    if (!builders.length) return;
    scan(document);
    if (typeof MutationObserver !== 'function') return;
    var observer = new MutationObserver(function () {
      scan(document);
    });
    Array.prototype.forEach.call(builders, function (builder) {
      observer.observe(builder, { childList: true, subtree: true });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
